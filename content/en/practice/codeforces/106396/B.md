---
title: "CF 106396B - \u732b"
description: "We are given a weighted undirected graph. Each edge connects two vertices and carries a cost. The task is to select a set of edges that connects all vertices together, forming a single connected structure, while maximizing the total sum of chosen edge weights."
date: "2026-06-19T18:05:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106396
codeforces_index: "B"
codeforces_contest_name: "Tiangong University 2025 ICPC Team Selection Contest II (Online Mirror)"
rating: 0
weight: 106396
solve_time_s: 57
verified: true
draft: false
---

[CF 106396B - \u732b](https://codeforces.com/problemset/problem/106396/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph. Each edge connects two vertices and carries a cost. The task is to select a set of edges that connects all vertices together, forming a single connected structure, while maximizing the total sum of chosen edge weights. If it is impossible to connect all vertices, the answer must be reported as impossible.

Another way to view the problem is that we want a spanning tree with maximum total edge weight. A spanning tree is a subset of edges that connects every vertex and contains no cycles. Among all such valid structures, we want the one with the largest sum of weights.

The input size is large enough that any solution trying to enumerate subsets of edges or repeatedly recompute connectivity would be too slow. With up to typical Codeforces limits for graphs, a quadratic or exponential approach is immediately ruled out. Even an $O(n^2)$ method would be too slow when the number of vertices is large and the graph is dense, since the number of edges can grow to $O(n^2)$ in worst cases.

A key constraint-driven implication is that we need a near-linear or logarithmic per-operation method for connectivity checking. This directly suggests a disjoint set union structure, since it supports fast union and find operations.

A subtle edge case arises when the graph is disconnected. For example, if we have 4 nodes and only edges (1,2) and (3,4), there is no way to form a single spanning tree. A naive greedy selection might still pick both edges and output a sum, but the correct output is -1 because the structure is not fully connected.

Another corner case is when multiple edges exist between the same pair of vertices. A careless implementation might treat them identically, but the correct algorithm must consider them independently since only the best combination contributes to the optimal spanning tree.

## Approaches

The brute-force idea is to try every subset of edges, check whether it forms a spanning tree, and compute its total weight. Checking connectivity can be done with BFS or DFS, and verifying that there are exactly $n-1$ edges ensures acyclicity. This approach is correct because it directly tests every valid candidate structure. However, the number of edge subsets is $2^m$, and each validity check costs $O(n + m)$, making the total complexity $O(2^m \cdot (n + m))$, which is infeasible even for moderately small graphs.

The key structural observation is that we are solving a maximum spanning tree problem. The problem reduces to selecting exactly $n-1$ edges that connect all vertices while maximizing total weight. This is the same as the classical minimum spanning tree problem, except we reverse the ordering to maximize instead of minimize.

Kruskal’s algorithm provides the needed structure. Instead of sorting edges in increasing order of weight, we sort them in decreasing order. We then iterate through edges and use a disjoint set union to only accept edges that connect previously disconnected components. Each accepted edge merges two components and contributes to the total weight. This greedy choice works because any edge that connects two already-connected components would create a cycle and cannot improve the spanning tree structure, while the heaviest available edges should be prioritized to maximize the sum.

At the end, if we have not used exactly $n-1$ edges, the graph is disconnected and no spanning tree exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m \cdot (n + m))$ | $O(n + m)$ | Too slow |
| Kruskal (DSU) | $O(m \log m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices and edges, then store all edges as triples containing endpoints and weight. This prepares the data for sorting by weight, which is the core of the greedy strategy.
2. Sort all edges in descending order of weight. The reasoning is that we want to consider heavier edges first so they have the highest chance of being included in the spanning tree.
3. Initialize a disjoint set union structure where each vertex starts in its own component. This structure will allow us to quickly determine whether adding an edge would connect two separate components or create a cycle.
4. Iterate over edges in sorted order. For each edge, check whether its endpoints belong to different components using DSU find operations. If they are different, we merge them and add the edge weight to the answer. If they are already in the same component, we skip it because it would form a cycle.
5. Maintain a counter of how many components remain. Each successful merge reduces the number of components by one.
6. After processing all edges, check whether only one connected component remains. If not, it means the graph was not fully connectable, so a spanning tree cannot be formed.
7. If the graph is connected, output the accumulated weight sum.

### Why it works

At any moment, the algorithm maintains a forest of connected components. Each chosen edge is the maximum possible edge that connects two distinct components at that time. This ensures that no chosen edge can be replaced by a heavier valid alternative without breaking connectivity. Since cycles are never introduced, the structure always remains a forest, and once all vertices are connected, the selected edges form a spanning tree with maximal possible total weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def solve():
    n, m = map(int, input().split())
    edges = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u - 1, v - 1, w))

    edges.sort(key=lambda x: x[2], reverse=True)

    dsu = DSU(n)
    total = 0
    used = 0

    for u, v, w in edges:
        if dsu.union(u, v):
            total += w
            used += 1

    if used != n - 1:
        print(-1)
    else:
        print(total)

if __name__ == "__main__":
    solve()
```

The DSU structure is used to maintain connected components efficiently. Path compression ensures near-constant amortized time per operation, which keeps the algorithm fast even for large graphs. Sorting in descending order guarantees that heavier edges are considered first, which is essential for maximizing the total weight.

The variable `used` tracks how many edges were successfully included. A valid spanning tree over $n$ nodes must contain exactly $n-1$ edges, so this is the final correctness check.

## Worked Examples

Consider a small graph with 4 nodes and edges: (1-2, 10), (2-3, 5), (3-4, 7), (1-4, 1).

After sorting in descending order, the edges become: (1-2, 10), (3-4, 7), (2-3, 5), (1-4, 1).

| Step | Edge | Components before | Action | Total |
| --- | --- | --- | --- | --- |
| 1 | 1-2 (10) | {1}{2}{3}{4} | merge | 10 |
| 2 | 3-4 (7) | {1,2}{3}{4} | merge | 17 |
| 3 | 2-3 (5) | {1,2}{3,4} | merge | 22 |
| 4 | 1-4 (1) | {1,2,3,4} | skip | 22 |

This trace shows how the algorithm builds a spanning tree while always selecting the highest available connecting edge.

Now consider a disconnected graph: 3 nodes with only edge (1-2, 5).

| Step | Edge | Components before | Action | Total |
| --- | --- | --- | --- | --- |
| 1 | 1-2 (5) | {1}{2}{3} | merge | 5 |

After processing, node 3 remains isolated, so the result is invalid and the output becomes -1.

This demonstrates that the final connectivity check is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m)$ | Sorting edges dominates, DSU operations are nearly constant amortized |
| Space | $O(n + m)$ | Storage for DSU arrays and edge list |

The complexity fits comfortably within typical constraints for large graphs since sorting is efficient for up to hundreds of thousands of edges, and DSU operations scale almost linearly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import inf

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
            self.s = [1] * n

        def f(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x

        def u(self, a, b):
            a = self.f(a)
            b = self.f(b)
            if a == b:
                return False
            if self.s[a] < self.s[b]:
                a, b = b, a
            self.p[b] = a
            self.s[a] += self.s[b]
            return True

    n, m = map(int, input().split())
    e = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        e.append((u - 1, v - 1, w))
    e.sort(key=lambda x: -x[2])

    d = DSU(n)
    ans = 0
    used = 0

    for u, v, w in e:
        if d.u(u, v):
            ans += w
            used += 1

    return str(ans if used == n - 1 else -1)

# provided sample-like tests
assert run("4 4\n1 2 10\n2 3 5\n3 4 7\n1 4 1\n") == "22"
assert run("3 1\n1 2 5\n") == "-1"

# custom tests
assert run("1 0\n") == "0"
assert run("2 1\n1 2 100\n") == "100"
assert run("3 3\n1 2 1\n2 3 1\n1 3 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node, no edges | 0 | single-vertex spanning tree |
| 2 nodes, one edge | 100 | simplest connected case |
| triangle graph | 2 | cycle handling in maximum spanning tree |

## Edge Cases

For a single vertex, the DSU starts with one component and no edges are needed. The algorithm never enters the edge loop meaningfully, and `used` remains zero. Since $n-1 = 0$, the condition is satisfied and the answer is 0, matching the correct definition of an empty spanning tree.

For a disconnected graph such as nodes 1-2 connected and node 3 isolated, the algorithm merges only reachable components. DSU ends with two components, so `used` becomes 1 while $n-1 = 2$. The final check correctly rejects the result and outputs -1, matching the impossibility of spanning all vertices.
