---
title: "CF 105586I - \u5c0f P \u7231\u6298\u8dc3"
description: "We are given a directed structure hidden inside an array. Each city has exactly one outgoing teleport, and every teleport belongs to exactly one city."
date: "2026-06-22T14:45:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105586
codeforces_index: "I"
codeforces_contest_name: "\u201c\u534e\u4e3a\u676f\u201d 2024 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u65b0\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u51b3\u8d5b\uff09"
rating: 0
weight: 105586
solve_time_s: 52
verified: true
draft: false
---

[CF 105586I - \u5c0f P \u7231\u6298\u8dc3](https://codeforces.com/problemset/problem/105586/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed structure hidden inside an array. Each city has exactly one outgoing teleport, and every teleport belongs to exactly one city. If we view city $i$ as a node and draw an edge $i \to a_i$, the entire system becomes a functional graph where every node has outdegree exactly one.

From any starting city, you repeatedly follow teleports, and you eventually fall into a cycle. The requirement in the problem is that the graph should become strongly connected after we are allowed to swap the teleports assigned to cities. A swap exchanges the outgoing edges of two nodes, meaning we swap two values in the array $a$.

The goal is to compute the minimum number of swaps needed so that from any node, every other node becomes reachable through directed paths.

The constraints allow up to $10^5$ nodes per test case, with total $10^5$ across tests. This rules out any quadratic reasoning over all swaps or repeated simulation of transformations. Any solution must essentially be linear or near-linear per test case.

A subtle but important edge case is when the graph already consists of a single directed cycle of length $n$. In that case, it is already strongly connected, so the answer is zero. For example, $n=3$, $a=[2,3,1]$ works. A naive approach that tries to “connect components” without recognizing this structure might still perform unnecessary swaps.

Another corner case is when the structure is a disjoint union of multiple cycles and trees leading into them. Even though the graph always has outdegree one, it may have multiple cycles. For instance, $a=[2,1,4,3]$ splits into two 2-cycles. This is not strongly connected, and naive reasoning that only counts cycles independently will fail unless it considers how swaps can merge cycles.

## Approaches

The graph induced by the array is a classic functional graph. Every connected component contains exactly one directed cycle, with possibly trees feeding into it. However, because every node has exactly one outgoing edge, reachability is entirely controlled by the structure of these cycles.

A brute-force idea would be to simulate swaps. We could try all pairs of positions, swap them, rebuild the graph, and check if it becomes strongly connected by running DFS from every node. Checking strong connectivity itself is $O(n)$, and there are $O(n^2)$ swaps, leading to $O(n^3)$ per test case. This is immediately impossible for $n=10^5$.

Even if we reduce checking, the core issue remains: we are modifying a permutation-like structure and asking for the minimum swaps to reach a target global structure. The key observation is that the target structure must be a single cycle covering all nodes, because in a functional graph, strong connectivity implies every node has indegree exactly one as well, forcing the graph to be a single directed cycle.

So the problem becomes: we want to transform the current array into a permutation consisting of one cycle of length $n$, using swaps, where each swap exchanges two values in the array. This is equivalent to rearranging the array into a single cycle permutation, and the question becomes how far the current mapping is from such a cycle structure.

The decisive insight is to interpret the array as a permutation of destinations. Since each value $a_i$ is used exactly once as an outgoing edge source position, the structure behaves like a permutation after considering nodes in terms of outgoing edges. Each cycle in the functional graph corresponds to a cycle in this permutation decomposition.

Swapping two values merges or splits cycles in a controlled way. The known result is that any permutation can be merged into a single cycle using swaps, and the minimum number of swaps required is determined by the number of cycles present. Each swap can reduce the cycle count by at most one, because it can connect two cycles into one.

If the graph has $c$ cycles, then we need at least $c-1$ swaps to merge them into a single cycle, and this is achievable greedily by always swapping elements from different cycles.

So the answer reduces to counting the number of directed cycles in the functional graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (swap simulation + connectivity check) | $O(n^3)$ | $O(n)$ | Too slow |
| Cycle counting in functional graph | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Construct the functional graph implicitly from the array $a$, where each node $i$ points to $a_i$. This representation is not explicitly needed beyond traversal, since we can follow edges directly.
2. Traverse all nodes and detect cycles using standard visitation states. For each node that has not been visited, start walking forward along outgoing edges until either reaching a visited node or returning to a node in the current recursion path. The moment we re-enter a node in the current path, we have identified a cycle.
3. Count how many distinct cycles exist. Each node belongs to exactly one cycle or is part of a chain leading into one, but every chain eventually enters a unique cycle, so each node is assigned during traversal without ambiguity.
4. If the number of cycles is $c$, output $c - 1$.

The reason this step is valid is that each swap can merge exactly two cycles by redirecting one outgoing edge connection between them. Once two cycles are merged, they behave as a single cycle in terms of reachability.

### Why it works

The functional graph decomposes into disjoint cycles with trees feeding into them, but strong connectivity requires eliminating all branching into separate cycles. Any valid final structure must be a single directed cycle over all nodes. Each swap can only reduce the number of cycles by at most one, because it can connect two previously disjoint cycles but cannot merge more than two components at once. Since initially there are $c$ cycles, at least $c-1$ merges are required, and a constructive sequence of swaps exists that achieves exactly this bound by repeatedly connecting two different cycles. This gives both optimality and feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = [0] + list(map(int, input().split()))

        vis = [0] * (n + 1)
        cycles = 0

        for i in range(1, n + 1):
            if vis[i]:
                continue

            cur = i
            stack_index = {}
            path = []

            while True:
                if vis[cur]:
                    break
                if cur in stack_index:
                    cycles += 1
                    break

                stack_index[cur] = len(path)
                path.append(cur)
                cur = a[cur]

            for v in path:
                vis[v] = 1

        print(max(0, cycles - 1))

if __name__ == "__main__":
    solve()
```

The implementation performs a forward walk from each unvisited node. The `stack_index` dictionary is used to detect a back-edge into the current path, which indicates a cycle discovery. Once a traversal finishes, all nodes visited in that walk are marked as processed so they are never revisited.

A subtle point is that every node is assigned to exactly one traversal, so even though we only explicitly detect cycles when revisiting the current path, the cycle count remains correct because every connected functional component contributes exactly one cycle detection event.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [3, 4, 1, 2]
```

| Start | Path traversal | Cycle detected | Total cycles |
| --- | --- | --- | --- |
| 1 | 1 → 3 → 1 | yes | 1 |

Only one cycle exists, so answer is $1 - 1 = 0$.

This confirms that a single-cycle permutation is already strongly connected and requires no swaps.

### Example 2

Input:

```
n = 4
a = [2, 1, 4, 3]
```

| Start | Path traversal | Cycle detected | Total cycles |
| --- | --- | --- | --- |
| 1 | 1 → 2 → 1 | yes | 1 |
| 3 | 3 → 4 → 3 | yes | 2 |

There are two cycles, so answer is $2 - 1 = 1$.

This shows that each disjoint cycle requires one merge operation, and swaps act as cycle-joiners.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each node is visited once and processed once in a functional traversal |
| Space | $O(n)$ | Visited array and temporary path storage |

The total $n$ across all test cases is $10^5$, so a linear solution is comfortably within limits, and memory usage remains bounded by per-test allocations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite
    out = []
    
    def solve():
        T = int(input())
        for _ in range(T):
            n = int(input())
            a = [0] + list(map(int, input().split()))
            vis = [0] * (n + 1)
            cycles = 0

            for i in range(1, n + 1):
                if vis[i]:
                    continue
                cur = i
                stack_index = {}
                path = []
                while True:
                    if vis[cur]:
                        break
                    if cur in stack_index:
                        cycles += 1
                        break
                    stack_index[cur] = 1
                    path.append(cur)
                    cur = a[cur]
                for v in path:
                    vis[v] = 1
            out.append(str(max(0, cycles - 1)))

    solve()
    return "\n".join(out)

# sample
assert run("1\n1\n1\n") == "0"

# all one cycle
assert run("1\n4\n2 3 4 1\n") == "0"

# two cycles
assert run("1\n4\n2 1 4 3\n") == "1"

# chain into cycle style
assert run("1\n5\n2 3 1 5 4\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node self-loop | 0 | minimal case |
| single large cycle | 0 | already optimal |
| two 2-cycles | 1 | cycle merging requirement |
| mixed cycles | 1 | general structure correctness |

## Edge Cases

A single-node graph like $n=1, a=[1]$ immediately forms a cycle count of one, producing answer zero. The traversal starts at node 1, detects a self-loop cycle, and marks it visited.

A fully cyclic permutation such as $a=[2,3,4,1]$ is handled as one traversal with one cycle detection event. The algorithm never splits it incorrectly because no new unvisited starting point remains after marking the path.

A disjoint cycle case such as $a=[2,1,4,3]$ is handled by starting from node 1 detecting one cycle, then starting from node 3 detecting another. Each component contributes exactly one cycle detection, producing correct cycle count two and answer one.

A pathological-looking chain into a cycle still collapses into a single detected cycle because only the cycle entry triggers the back-edge condition; tree nodes are simply marked visited and never inflate the cycle count.
