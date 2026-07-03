---
title: "CF 103448E - \u5723\u83ab\u5361\u9020\u9898\u7684\u4e03\u5929"
description: "We are given an undirected graph where each node carries a non-negative integer value. The graph structure tells us which nodes can interact, and the values evolve through an operation applied along any chosen path."
date: "2026-07-03T07:27:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103448
codeforces_index: "E"
codeforces_contest_name: "The 16-th Beihang University Collegiate Programming Contest (BCPC 2021) - Preliminary"
rating: 0
weight: 103448
solve_time_s: 42
verified: true
draft: false
---

[CF 103448E - \u5723\u83ab\u5361\u9020\u9898\u7684\u4e03\u5929](https://codeforces.com/problemset/problem/103448/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where each node carries a non-negative integer value. The graph structure tells us which nodes can interact, and the values evolve through an operation applied along any chosen path.

A single operation picks a path in the graph, say a sequence of nodes where consecutive nodes are connected by edges. If the path has length t, then nodes are paired symmetrically along the path: the first with the last, the second with the second last, and so on. Each node on the path replaces its value with the bitwise AND of its current value and the value of its paired node. All updates happen simultaneously, so the operation is based on the original values along the path, not partially updated ones.

We may perform this operation any number of times on any paths. The task is to minimize the maximum value across all nodes after arbitrarily many operations.

The constraints allow up to five hundred thousand nodes and edges, which immediately rules out anything quadratic or even near quadratic. Any solution must effectively process the graph in linear or near linear time, typically O(n + m). This strongly suggests that the answer depends on connected components and some aggregate property computed per component.

A subtle point is that operations are not local edge updates but path-wide symmetric pair interactions. It is easy to incorrectly assume this limits us to adjacent transfers only, but in fact a path can connect distant nodes and repeatedly chosen paths can simulate broader mixing.

A naive misunderstanding is to think only endpoints of chosen paths matter, or that values propagate slowly. For example, on a chain 1-2-3-4, one might think node 1 can only influence 2, but a path 1-2-3-4 simultaneously couples (1,4) and (2,3), allowing information to jump across the whole chain in one operation.

The key edge case is a tree or chain where repeated operations gradually combine values. If we incorrectly assume values only merge locally per edge, we would underestimate how quickly information spreads.

## Approaches

A direct brute force approach would simulate operations. We would repeatedly pick arbitrary paths and apply symmetric pairwise AND updates until no further improvement is possible. Each operation scans a path, and there could be exponentially many possible paths and sequences. Even restricting ourselves to simple strategies like repeatedly applying operations on edges or random paths leads to potentially O(nm) or worse behavior, which is far beyond limits.

The structural insight comes from understanding what information is actually being propagated. The operation only ever uses bitwise AND, which is monotone decreasing per bit. Once a bit becomes zero in a node, it never returns. This suggests the final state of a node is determined entirely by which initial values can be forced to interact with it through sequences of operations.

Because we can choose arbitrary paths inside a connected component, any node can eventually be paired, directly or indirectly, with any other node in the same component. Repeatedly applying path operations allows us to merge information across the entire component. This means each connected component behaves like a closed system where all values can be combined.

Inside one component, the strongest value we can force every node toward is the bitwise AND of all initial values in that component. Any bit that is missing in even one node cannot survive in a global minimum-maximization objective, because we can always design operations that eventually force that bit to be ANDed into other nodes, and conversely any surviving bit must exist in all contributing nodes.

Thus, each component collapses to a uniform value equal to the AND over its nodes. The final answer is determined by the maximum of these component-wise AND values, since different components evolve independently and the objective is to minimize the global maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n + m) | Too slow |
| Connected Components + Bitwise AND | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We translate the reasoning into a concrete procedure.

1. Identify all connected components of the graph using either DFS or BFS. Each component represents a set of nodes that can be made to interact through sequences of valid operations.
2. For each component, compute the bitwise AND of all node values inside it. This is done by initializing a running value to all bits set (or the first node’s value) and AND-ing every other node’s value in the component.
3. Track the maximum of these component-wise AND results across all components.
4. Output this maximum value.

The reason we take a maximum over components rather than a sum or something more global is that components evolve independently. No operation can ever bridge two disconnected components, so their final states do not influence each other.

Why it works

Inside a connected component, repeated path operations allow us to propagate information between any pair of nodes. Each operation can couple two nodes through symmetry on a chosen path, and by chaining such operations, every node can eventually be influenced by every other node. Because the only operation is bitwise AND, the value at any node can only decrease bitwise, and any bit that survives in all nodes can be preserved through careful pairing. The only stable value that every node can be forced to agree on is the AND of all initial values in the component, since any bit absent in any node can be eliminated by pairing paths that include that node.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    w = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    visited = [False] * n
    ans = 0

    for i in range(n):
        if visited[i]:
            continue

        stack = [i]
        visited[i] = True
        comp_and = (1 << 30) - 1  # enough for w <= 1e9

        while stack:
            u = stack.pop()
            comp_and &= w[u]
            for v in g[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

        ans = max(ans, comp_and)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first builds the adjacency list representation of the graph. It then runs an iterative DFS to avoid recursion limits on large graphs. Each time a new component is discovered, it initializes a full-bit mask and intersects it with all node values encountered in that component.

The final answer accumulates the maximum component result. The bitmask `(1 << 30) - 1` safely covers all possible values since inputs are bounded by 10^9.

## Worked Examples

Consider a small graph with two components. Suppose component one has values 5 (101) and 7 (111), and component two has a single node with value 2 (010). The algorithm processes each component independently.

For the first component, the AND becomes 101 & 111 = 101, which is 5. For the second, it is simply 2. The final answer is max(5, 2) = 5.

| Component | Nodes visited | Running AND | Component result |
| --- | --- | --- | --- |
| 1 | 5, 7 | 111 → 101 | 5 |
| 2 | 2 | 010 | 2 |

This trace shows that connectivity only matters in grouping; once grouped, values fully collapse into a single bitwise constraint.

Now
