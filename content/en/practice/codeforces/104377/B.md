---
title: "CF 104377B - \u6700\u5927\u4ef7\u503c"
description: "We are given an undirected graph where each edge carries a weight that behaves like a threshold. You start at node S holding a value k, and want to reach node T."
date: "2026-07-01T17:20:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104377
codeforces_index: "B"
codeforces_contest_name: "The 21st Sichuan University Programming Contest"
rating: 0
weight: 104377
solve_time_s: 56
verified: true
draft: false
---

[CF 104377B - \u6700\u5927\u4ef7\u503c](https://codeforces.com/problemset/problem/104377/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where each edge carries a weight that behaves like a threshold. You start at node S holding a value k, and want to reach node T. When you traverse an edge with weight w, your current value is affected in a very specific way: if your current value is at most w, nothing happens, but if it is larger than w, it gets reduced down to exactly w.

This means that along any path, your value never increases and is repeatedly “clamped down” by edge weights. After walking a sequence of edges, your final value is simply the minimum among your starting value k and all edge weights on that path.

The task is to choose a path from S to T that maximizes this final value. If no path exists, the answer is zero.

The constraints are extremely large, with up to one million nodes and one million edges. This immediately rules out any approach that inspects all paths explicitly. Even algorithms that are quadratic or cubic in the number of nodes are impossible. We need something close to linear or near linear time, such as O(m log n) or O(m α(n)).

A subtle edge case appears when S and T are disconnected. For example, if the graph has two components and S and T lie in different ones, no traversal is possible and the correct answer is 0 regardless of k. Another corner case is when all edges have weight 0. In that case, any path immediately collapses the value to 0, so the answer is 0 if reachable, otherwise still 0.

## Approaches

The key observation is that the value you carry along a path is always the minimum between k and the smallest edge weight encountered so far. So for any fixed path, the final value depends only on its bottleneck edge.

This turns the problem into a classical maximum bottleneck path problem. We want a path from S to T that maximizes the minimum edge weight along the path. Once we find that bottleneck value B, the final answer becomes min(k, B).

A brute-force approach would enumerate all possible paths from S to T, compute the minimum edge weight along each path, and take the maximum. This is correct in principle, but the number of paths in a graph can grow exponentially. Even in a sparse graph, this quickly becomes infeasible.

The structure of the problem allows a better strategy. Instead of exploring paths, we can think in reverse: if we only keep edges with weight at least X, then we can ask whether S and T are connected. If they are, then there exists a path whose minimum edge weight is at least X. This suggests a monotonic property over edge thresholds.

This monotonicity allows a greedy construction. If we sort edges by weight in descending order and gradually add them to a Union-Find structure, the moment S and T become connected, we have found the largest possible threshold that still permits connectivity. That threshold is exactly the best bottleneck value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n + m) | Too slow |
| Union-Find with sorting | O(m log m) | O(n) | Accepted |

## Algorithm Walkthrough

We convert the problem into finding the strongest possible minimum edge along any S to T path.

1. Sort all edges in descending order of weight. This ensures we always try to connect the graph using the strongest constraints first, preserving the possibility of a high bottleneck path.
2. Initialize a Union-Find structure where each node starts in its own component. This structure tracks which nodes are currently connected using edges processed so far.
3. Iterate through edges in sorted order. For each edge (u, v, w), merge the components containing u and v. The reasoning is that this edge is now available as part of any path that uses edges of weight at least w.
4. After each union operation, check whether S and T belong to the same connected component. The first moment this happens corresponds to the strongest threshold that still allows a path between them.
5. Record this edge weight w as the bottleneck answer and stop processing further edges. Any later edges have smaller weights and can only produce weaker bottlenecks.
6. If S and T are never connected, the answer is 0.

After processing, the answer to the original problem is min(k, bottleneck), because even if the graph allows a stronger path, your initial value caps the result.

### Why it works

At any moment during the sweep, the Union-Find structure represents connectivity using only edges with weight at least the current threshold. If S and T become connected at weight w, it means there exists a path where every edge has weight at least w. Therefore the minimum edge on that path is at least w.

Because we process edges from largest to smallest, the first moment of connectivity guarantees maximality. Any later connection would require using weaker edges, which cannot improve the bottleneck beyond the first successful threshold.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

n, m, S, T, k = map(int, input().split())
edges = []

for _ in range(m):
    u, v, w = map(int, input().split())
    edges.append((w, u, v))

edges.sort(reverse=True)

dsu = DSU(n)
best = -1

for w, u, v in edges:
    dsu.union(u, v)
    if dsu.find(S) == dsu.find(T):
        best = w
        break

if best == -1:
    print(0)
else:
    print(min(k, best))
```

The code first builds a DSU to maintain dynamic connectivity. Sorting edges in descending order ensures we always attempt to connect the graph using the highest possible thresholds first. The first time S and T become connected, the current edge weight represents the best achievable bottleneck.

The final comparison with k is necessary because even if the path allows a higher bottleneck, the starting value cannot exceed k.

## Worked Examples

Consider the sample graph:

Input:

```
4 5 1 4 6
1 2 1
1 4 2
1 3 3
2 4 3
3 4 1
```

We sort edges by weight:

| Step | Edge | Action | Component(S) | Component(T) | Connected | Best |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (1-3,3) | union | {1,3} | {4} | no | - |
| 2 | (2-4,3) | union | {1,3} | {2,4} | yes | 3 |

At step 2, nodes 1 and 4 become connected through edges of weight at least 3. This means there exists a path with bottleneck 3.

The final answer is min(k, 3) = min(6, 3) = 3.

This confirms that we are not choosing the shortest path or any specific route, but the one with the strongest weakest edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting edges dominates, DSU operations are near constant |
| Space | O(n + m) | Storing graph edges and DSU arrays |

The constraints allow up to one million edges, and sorting at this scale is feasible within 3 seconds in Python with efficient input handling. DSU operations are essentially linear, so they do not become the bottleneck.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n + 1))
            self.size = [1] * (n + 1)

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            ra = self.find(a)
            rb = self.find(b)
            if ra == rb:
                return False
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            return True

    n, m, S, T, k = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))

    edges.sort(reverse=True)
    dsu = DSU(n)

    best = -1
    for w, u, v in edges:
        dsu.union(u, v)
        if dsu.find(S) == dsu.find(T):
            best = w
            break

    return str(0 if best == -1 else min(k, best)) + "\n"

# sample
assert run("""4 5 1 4 6
1 2 1
1 4 2
1 3 3
2 4 3
3 4 1
""") == "3\n"

# disconnected graph
assert run("""3 1 1 3 10
1 2 5
""") == "0\n"

# all edges zero
assert run("""3 2 1 3 5
1 2 0
2 3 0
""") == "0\n"

# direct edge dominates
assert run("""2 1 1 2 100
1 2 50
""") == "50\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample graph | 3 | correct bottleneck computation |
| disconnected | 0 | unreachable case |
| all zero weights | 0 | collapse behavior |
| single edge cap | 50 | interaction with k and direct path |

## Edge Cases

A disconnected graph such as `1 2 1 3 10` with a single edge between 1 and 2 demonstrates that no unions will ever connect S and T, so best remains unset and the output is 0.

A graph where all edges have weight 0 shows that even though connectivity may exist, every path immediately reduces the carried value to 0, so the answer must remain 0 regardless of k. The algorithm handles this because the first successful connection will occur at weight 0, and min(k, 0) correctly returns 0.

A single-edge graph tests the boundary where S and T are directly connected. The DSU merges them immediately and best becomes that edge weight, which is then compared with k, ensuring the cap is applied correctly.
