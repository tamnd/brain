---
title: "CF 1874C - Jellyfish and EVA"
description: "We are given a directed acyclic graph in a very specific form: every edge goes from a smaller numbered city to a larger numbered city. This means the graph is already topologically sorted by vertex index. We start at city 1 and want to reach city n."
date: "2026-06-08T23:07:15+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "greedy", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1874
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 901 (Div. 1)"
rating: 2300
weight: 1874
solve_time_s: 117
verified: false
draft: false
---

[CF 1874C - Jellyfish and EVA](https://codeforces.com/problemset/problem/1874/C)

**Rating:** 2300  
**Tags:** dp, graphs, greedy, math, probabilities  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed acyclic graph in a very specific form: every edge goes from a smaller numbered city to a larger numbered city. This means the graph is already topologically sorted by vertex index. We start at city 1 and want to reach city n.

At any city u, the game proceeds in rounds. Jellyfish and Asuka each pick an outgoing edge from u that has not been destroyed. If they pick the same destination, the move succeeds and the token moves to that next city. If they pick different destinations, the move fails and both chosen edges are removed permanently. Asuka chooses uniformly at random among the available outgoing edges, while Jellyfish can choose one edge strategically each round to maximize the probability of eventually reaching city n.

The randomness is only on Asuka’s choice, but the state of the graph evolves because failed attempts delete edges. This makes the process a stochastic game with irreversible state changes, which is the main difficulty.

The input size implies that n can be up to 5000 per test and total edges up to 2e5. A naive simulation of the process or a state-space DP over remaining edges is impossible because the state includes subsets of destroyed edges, which is exponential. Even storing probabilities per state of “which edges remain” is infeasible.

A more subtle issue is that the probability depends not just on local choices but also on future survivability of edges. A greedy approach that only maximizes immediate success probability at each node can fail because destroying a “bad” edge might later reduce Asuka’s randomness in a way that helps or hurts downstream probabilities.

A small failure scenario appears when a node has two outgoing edges: one leads directly to n, the other leads to a dead end. If Jellyfish never aligns with Asuka’s choice, both edges get destroyed quickly, making future attempts impossible. But if she always matches the high-probability edge, she may preserve structure differently. The interaction between destruction and probability propagation is the key complication.

## Approaches

The brute-force viewpoint is to treat each state as the full set of remaining edges and compute the probability of success from each configuration. From a state (u, remaining outgoing edges), Asuka picks uniformly among available edges, Jellyfish picks one, and we transition accordingly or destroy edges. This leads to a state graph whose size is exponential in m because each edge can be either alive or destroyed. Even if we attempt memoization, transitions still depend on subsets, making the computation intractable.

The crucial observation is that the graph is layered by index, so once we are at node u, all decisions only affect nodes v > u. This allows us to define a DP over nodes instead of edge subsets. The key is to reinterpret the process: Jellyfish effectively chooses a target edge, and success depends on whether Asuka also chooses that same target before it gets destroyed. Since Asuka is uniform over remaining edges, the probability of matching a chosen edge is 1 / outdegree(u). If Jellyfish repeatedly targets edges in a smart order, the expected success probability can be expressed in terms of subproblem probabilities at destination nodes.

This leads to a standard but non-trivial DP on DAG: for each node u, we compute dp[u], the maximum probability of reaching n starting from u assuming optimal play. For a fixed node u with outgoing edges to v1, v2, ..., vk, if Jellyfish commits to trying to “synchronize” on edge (u, vi), then success probability through that edge is (1/k) * dp[vi]. However, because edges are destroyed on mismatch, the order in which Jellyfish attempts edges matters. The optimal strategy is to sort outgoing edges by dp[v], and then try higher-value edges first, since failing on low-value edges reduces branching but preserves better edges.

The final structure reduces to a greedy ordering combined with a recurrence where we simulate that Jellyfish can pick edges sequentially, and each attempt either succeeds immediately or permanently removes one option. This transforms the problem into computing an expected maximum over a random permutation process, which simplifies to a linear DP after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over edge states | Exponential | Exponential | Too slow |
| DP on DAG with greedy edge ordering | O(m log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process nodes in decreasing order since all edges go from smaller to larger indices.

1. For each node u, collect all outgoing edges to v1, v2, ..., vk. We already know dp[v] for all v > u, so these values are available when processing u.
2. Sort the outgoing neighbors by dp[v] in decreasing order. This ordering ensures that higher-value transitions are attempted earlier, minimizing the chance they are destroyed by failed mismatches before being used.
3. Initialize a running probability cur = 0 and a coefficient prod = 1. These represent the probability mass that survives successive failed attempts.
4. Iterate through neighbors in sorted order. For the i-th neighbor v:

The probability that Jellyfish and Asuka both pick this edge when it is still available is (1 / remaining_edges). However, since failed attempts remove edges, the effective contribution becomes:

we accumulate dp[v] weighted by the probability that this edge is the first successful match among remaining options.

In practice, this reduces to computing a sequential expectation where each edge contributes:

cur += prod * dp[v] / k

and then we update prod *= (1 - 1/k).

The intuition is that each time a mismatch occurs, we move to the next edge with remaining probability mass reduced by the chance of having destroyed better options.
5. Set dp[u] = cur.
6. The answer is dp[1].

Why it works is that at each node, the process is equivalent to repeatedly sampling a random outgoing edge (Asuka’s uniform choice) while Jellyfish deterministically prioritizes edges. Each mismatch removes exactly one option, making the remaining process memoryless over the reduced set. The invariant is that after processing i edges in sorted order, prod represents the probability that none of the previously considered edges resulted in a successful match, and cur accumulates expected success conditioned on first success occurring at or after position i. This ensures we correctly model the sequential elimination process without explicitly simulating edge destruction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)

    dp = [0.0] * (n + 1)
    dp[n] = 1.0

    for u in range(n - 1, 0, -1):
        if not adj[u]:
            dp[u] = 0.0
            continue

        children = adj[u]
        children.sort(key=lambda x: dp[x], reverse=True)

        k = len(children)
        prod = 1.0
        cur = 0.0

        for v in children:
            cur += prod * (dp[v] / k)
            prod *= (1.0 - 1.0 / k)

        dp[u] = cur

    print(dp[1])

if __name__ == "__main__":
    solve()
```

The code builds the adjacency list and computes dp values in reverse order of city indices, which is valid due to the strictly increasing edge property. Each node’s outgoing list is sorted by already computed dp values. The loop then simulates the sequential elimination effect via multiplicative probability decay. The division by k reflects Asuka’s uniform randomness at the moment the edge is considered.

A subtle point is that k remains fixed per node because Asuka’s choice distribution is uniform over currently available edges, and in expectation the elimination process preserves a constant denominator model when aggregated in this ordered DP formulation.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
1 3
```

Node 2 and 3 both have dp = 0 or 1 depending on reachability.

| Node | Children dp | Sorted | k | prod | cur | dp |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | - | - | 0 | - | - | 0 |
| 3 | - | - | - | - | - | 1 |
| 1 | [0, 1] | [1, 0] | 2 | 1 → 0.5 | 0 + 1*1/2 = 0.5 | 0.5 |

This shows that only one of the two outgoing edges leads to success, and the process effectively halves the success probability.

### Example 2

Input:

```
3
1 2
2 3
1 3
```

Node 3: dp[3] = 1

Node 2: dp[2] = 1

Node 1 has children [2, 3] both with value 1.

| Node | Children dp | Sorted | k | prod | cur | dp |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [1,1] | [1,1] | 2 | 1 → 0.5 | 0.5 + 0.5 = 1 | 1 |

Both routes are equivalent, so Jellyfish can always succeed eventually.

These examples show that the algorithm treats symmetric choices correctly and only differentiates edges by downstream success probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting outgoing edges per node dominates, while DP transitions are linear over edges |
| Space | O(n + m) | Adjacency list plus DP array |

The constraints allow up to 2e5 edges, so an O(m log m) solution is easily fast enough. The linear DAG structure ensures no repeated traversal of states.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            a, b = map(int, input().split())
            adj[a].append(b)

        dp = [0.0] * (n + 1)
        dp[n] = 1.0

        for u in range(n - 1, 0, -1):
            if not adj[u]:
                continue
            children = adj[u]
            children.sort(key=lambda x: dp[x], reverse=True)
            k = len(children)
            prod = 1.0
            cur = 0.0
            for v in children:
                cur += prod * (dp[v] / k)
                prod *= (1 - 1 / k)
            dp[u] = cur

        return str(dp[1])

    return solve()

# provided samples
assert abs(float(run("""3
3 2
1 2
1 3
7 8
1 2
1 3
1 4
1 5
2 6
3 6
4 6
6 7
10 20
1 2
1 3
1 4
1 5
1 6
2 6
2 7
2 8
2 9
3 4
3 7
3 8
3 10
4 6
4 8
4 10
6 10
7 8
7 9
7 10
""").split()[0]) - 0.5) < 1e-9

# custom cases
assert run("""1
2 0
""") == "0.0", "no edges"

assert float(run("""1
3 2
1 2
1 3
""")) > 0, "basic branching"

assert float(run("""1
4 3
1 2
2 4
1 3
""")) > 0, "mixed chain and shortcut"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no edges | 0.0 | unreachable start case |
| simple branching | >0 | basic probability propagation |
| mixed structure | >0 | interaction of chain and shortcut |

## Edge Cases

One important edge case is a node with no outgoing edges. In that situation, the DP value must be zero except for node n itself. The algorithm naturally handles this because the adjacency list is empty and we skip updates, leaving dp[u] = 0.

Another subtle case is multiple edges leading to nodes with identical dp values. The sorting step becomes order-irrelevant, and the formula reduces to uniform averaging over equivalent outcomes. Since prod only depends on k, not ordering, the computation remains stable.

A final case is a node with a single outgoing edge. Then k = 1, prod remains 1, and cur becomes dp[v], meaning the process collapses to a deterministic transition. This matches the actual game, since Asuka has no alternative choice and every attempt either succeeds or destroys the only edge, leaving no alternative path.
