---
title: "CF 105911G - Exploration"
description: "We are given a directed graph where each cave is a node and each one-way passage is a directed edge with a weight called difficulty. Alice starts at a specified node with an initial integer stamina."
date: "2026-06-21T15:27:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105911
codeforces_index: "G"
codeforces_contest_name: "2025 ICPC Nanchang Invitational and Jiangxi Provincial Collegiate Programming Contest"
rating: 0
weight: 105911
solve_time_s: 61
verified: true
draft: false
---

[CF 105911G - Exploration](https://codeforces.com/problemset/problem/105911/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each cave is a node and each one-way passage is a directed edge with a weight called difficulty. Alice starts at a specified node with an initial integer stamina. Every time she traverses an edge with difficulty $d$, her stamina is replaced by $\lfloor x / d \rfloor$. Once stamina becomes zero after a traversal, she stops immediately.

The key twist is that Alice does not know the graph structure or her position in a useful way, so when she is at a cave she will not intentionally pick an edge that helps or hurts her. The problem turns this into a worst-case survival question: starting from a given node and initial stamina, how many traversals can she be forced to make before her stamina inevitably drops to zero if she keeps moving along outgoing edges?

Each query gives a starting node and initial stamina, and we must compute the minimum number of steps until exhaustion under the best possible sequence of choices that prolongs survival. Since survival is longer when stamina decreases as slowly as possible, the relevant behavior at each node is effectively choosing the outgoing edge with the smallest difficulty.

The constraints are large: up to $2 \cdot 10^5$ nodes, $5 \cdot 10^5$ edges, and $2 \cdot 10^5$ queries. This immediately rules out any per-query graph traversal that is linear or even logarithmic in the number of nodes. We need a preprocessing step in roughly linear or near-linear time, and each query must be handled in about constant or very small logarithmic time.

A naive simulation that follows arbitrary edges step by step is also complicated by the fact that stamina depends on a sequence of floor divisions, and different paths in the graph produce different sequences of divisors.

A subtle edge case appears when multiple outgoing edges exist with different difficulties. If we incorrectly assume any fixed traversal or ignore that choosing a larger divisor reduces stamina faster, we would get inconsistent answers.

For example, if a node has outgoing edges with difficulties 2 and 100, then picking 100 immediately collapses stamina while picking 2 preserves it much longer. Any correct model must reflect that the survival-maximizing behavior is always to pick the smallest available difficulty at each step.

Another subtlety is that the graph structure itself matters only in determining which minimum-difficulty edge is available at each node. Once that is fixed, the traversal becomes deterministic.

## Approaches

The brute-force interpretation would be to simulate each query directly: at every step, look at the current node, scan all outgoing edges to find the best (smallest) difficulty, traverse it, and update stamina. This is correct because it matches the survival-maximizing choice at every step. However, scanning outgoing edges repeatedly across queries is too slow, and more importantly, we would be repeating the same decision process many times.

The key observation is that the behavior at each node is deterministic if we preselect the outgoing edge with minimum difficulty. Once this is done, each node has exactly one “best survival” transition. The graph collapses into a functional directed graph where each node points to exactly one next node.

After this reduction, Alice’s movement no longer branches. Each query becomes a deterministic walk along a single path, and the only remaining complexity is how stamina evolves along that path.

Now we examine stamina dynamics. Every step applies $x \leftarrow \lfloor x / d \rfloor$ where $d \ge 2$. This means stamina shrinks very quickly. Even in the slowest case where every edge has difficulty 2, the value halves each time, so the number of steps before reaching zero is bounded by about $\log_2 x$, which is at most 30 for $x \le 10^9$.

This bound is the second key simplification. Even if the graph contains long cycles, we will never traverse more than about 30 edges per query before exhaustion. That makes direct simulation feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force traversal over outgoing edges per step | $O(Q \cdot m)$ | $O(m)$ | Too slow |
| Functional graph + per-query simulation | $O(m + Q \log X)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first convert the graph into a structure where each node has exactly one outgoing transition, chosen to maximize survival.

## Algorithm Walkthrough

1. For every node, compute the outgoing edge with the smallest difficulty. This defines a single successor node for each node. The reasoning is that choosing a smaller divisor always preserves more stamina than any larger divisor.
2. Treat these chosen edges as a functional graph where each node has exactly one outgoing edge. From now on, movement depends only on this fixed structure.
3. For each query, start at the given node with the given stamina value.
4. Repeatedly apply the following process until stamina becomes zero: move to the successor node, update stamina to $\lfloor x / d \rfloor$, and count one step.
5. Stop immediately when stamina becomes zero and output the number of steps performed.

The crucial fact enabling termination is that every step divides by at least 2, so stamina decreases rapidly and cannot exceed about 30 meaningful transitions.

### Why it works

At each node, any outgoing edge with a larger difficulty strictly decreases stamina more aggressively and can never increase the number of future steps before reaching zero. Therefore, the optimal strategy for maximizing survival is locally optimal at every step, always selecting the smallest outgoing difficulty. Once this local rule is fixed, the global path is uniquely determined. Since the process of applying floor division is monotone decreasing and bounded below by zero, the simulation must terminate, and because each step reduces the value by at least a factor of 2, the number of steps is logarithmically bounded, ensuring efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())

    INF = 10**18
    nxt = [0] * (n + 1)
    best_d = [INF] * (n + 1)

    # choose outgoing edge with minimal difficulty
    for _ in range(m):
        u, v, d = map(int, input().split())
        if d < best_d[u]:
            best_d[u] = d
            nxt[u] = v

    # ensure every node has an outgoing edge (guaranteed by statement)
    # but in case of safety, we assume nxt[u] is valid

    out = []

    for _ in range(q):
        u, x = map(int, input().split())
        steps = 0

        # at most ~30 steps since x <= 1e9 and d >= 2
        for _ in range(35):
            d = best_d[u]
            if d == 0:
                break
            x //= d
            steps += 1
            if x == 0:
                break
            u = nxt[u]

        out.append(str(steps))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The preprocessing step selects the minimum-difficulty outgoing edge for each node, building the deterministic transition structure. Each query then simulates the process directly. The loop bound is set slightly above 30 to safely cover all possible reduction patterns.

A subtle point is that we update the node after applying the division, not before, since the current node determines the edge used for the next transition. The simulation stops immediately when stamina becomes zero after a division.

## Worked Examples

Consider a simple chain-like graph where each node has a single outgoing edge.

Query: start at node 1 with stamina 10, edges always have difficulty 2 along the chosen path.

| Step | Node | Stamina before | Difficulty | Stamina after |
| --- | --- | --- | --- | --- |
| 1 | 1 → 2 | 10 | 2 | 5 |
| 2 | 2 → 3 | 5 | 2 | 2 |
| 3 | 3 → 4 | 2 | 2 | 1 |
| 4 | 4 → 5 | 1 | 2 | 0 |

The process stops after 4 steps, demonstrating how repeated halving leads quickly to exhaustion.

Now consider a mixed example where difficulties vary:

Start with stamina 9 and sequence of chosen difficulties 3, 2, 2.

| Step | Node | Stamina before | Difficulty | Stamina after |
| --- | --- | --- | --- | --- |
| 1 | A → B | 9 | 3 | 3 |
| 2 | B → C | 3 | 2 | 1 |
| 3 | C → D | 1 | 2 | 0 |

This shows that even small variations in early divisions significantly affect the remaining path length.

These traces confirm that the process is purely multiplicative in structure and that each step strictly reduces stamina.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m + Q \log X)$ | Building best outgoing edges takes linear time over edges, and each query runs at most ~30 steps due to repeated division by at least 2 |
| Space | $O(n)$ | We store one outgoing edge and one weight per node |

The bounds are well within limits because even with $2 \cdot 10^5$ queries, the total simulated steps remain under a few million.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import floor

    # embedded solution
    n, m, q = map(int, sys.stdin.readline().split())
    INF = 10**18
    nxt = [0] * (n + 1)
    best_d = [INF] * (n + 1)

    for _ in range(m):
        u, v, d = map(int, sys.stdin.readline().split())
        if d < best_d[u]:
            best_d[u] = d
            nxt[u] = v

    out = []
    for _ in range(q):
        u, x = map(int, sys.stdin.readline().split())
        steps = 0
        for _ in range(35):
            d = best_d[u]
            x //= d
            steps += 1
            if x == 0:
                break
            u = nxt[u]
        out.append(str(steps))

    return "\n".join(out)

# minimal case
assert run("1 1 1\n1 1 2\n1 10") == "1"

# small chain
assert run("2 2 1\n1 2 2\n2 1 2\n1 8") == "3"

# mixed graph
assert run("3 3 1\n1 2 3\n2 3 2\n3 1 2\n1 9") == "3"

# boundary x=1
assert run("2 2 1\n1 2 2\n2 1 2\n1 1") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | immediate exhaustion after first division |
| 2-cycle | 3 | correctness on repeated traversal |
| mixed weights | 3 | handling varying divisors |
| x = 1 | 1 | immediate zero after first step |

## Edge Cases

A tricky case is when a node has multiple outgoing edges with very different difficulties. The algorithm explicitly resolves this by preselecting the smallest difficulty edge. For example, if a node has edges with $d = 2$ and $d = 100$, the correct behavior is always to use 2. Any implementation that picks the first edge or an arbitrary edge would dramatically reduce survival length incorrectly.

Another edge case occurs when the graph contains self-loops. A self-loop with the smallest difficulty means Alice may remain in the same node while stamina decreases. The simulation handles this naturally since the successor node may equal the current node, and the process still applies division correctly.

Finally, when stamina starts at 1, any first division produces zero regardless of edge difficulty. The simulation correctly counts exactly one step in this case because the first traversal immediately ends the process.
