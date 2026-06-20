---
title: "CF 106202D - \u0421\u043a\u0435\u043b\u0435\u0442\u044b, \u043a\u043e\u0441\u0442\u0438, \u043a\u043b\u0430\u0434\u0431\u0438\u0449\u0435, \u0447\u0435\u0440\u0435\u043f\u0430"
description: "We are given a graph whose vertices are points on a plane, but the geometry only matters through the x-coordinates. Each edge connects two vertices, and an edge can be thought of as a straight segment, although crossings between segments do not allow traversal."
date: "2026-06-20T09:02:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106202
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106202
solve_time_s: 63
verified: true
draft: false
---

[CF 106202D - \u0421\u043a\u0435\u043b\u0435\u0442\u044b, \u043a\u043e\u0441\u0442\u0438, \u043a\u043b\u0430\u0434\u0431\u0438\u0449\u0435, \u0447\u0435\u0440\u0435\u043f\u0430](https://codeforces.com/problemset/problem/106202/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph whose vertices are points on a plane, but the geometry only matters through the x-coordinates. Each edge connects two vertices, and an edge can be thought of as a straight segment, although crossings between segments do not allow traversal.

For each query value X, we apply a hypothetical vertical cut. Every vertex whose x-coordinate equals X disappears. Any edge that spans across the line x = X also disappears, meaning an edge is removed if X lies between the x-coordinates of its endpoints, including endpoints. After these deletions, the remaining graph consists only of vertices strictly to the left of X and strictly to the right of X, and edges that lie entirely within one side.

The task for each query is to compute how many connected components remain in this filtered graph.

Each query is independent, so we always evaluate the original graph under a fresh cut.

The constraints allow up to 10^5 vertices, edges, and queries per test, so any solution that recomputes connectivity from scratch per query is too slow. A naive approach would rebuild a graph and run a traversal per query, leading to about O(q(n + m)), which is far beyond acceptable.

A subtle point is that vertices with identical x-coordinates behave specially. If X equals some vertex x-coordinate, all those vertices are removed, and edges incident to them vanish as well. Any solution must correctly separate strict inequalities from equality.

A naive implementation also risks incorrectly keeping edges that “touch” the cut. For example, if an edge connects x = 1 and x = 5, then for X = 1, it must already be removed even though only one endpoint equals X.

## Approaches

The key observation is that the vertical cut splits the graph purely by ordering vertices on the x-axis. After sorting vertices by x-coordinate, every query X partitions the vertices into three groups: those with x < X, those with x = X, and those with x > X. The middle group is discarded entirely, and there are no edges between the remaining two groups.

This means the answer for a query is simply the number of connected components in the induced subgraph on x < X plus the number of connected components in the induced subgraph on x > X.

The problem reduces to answering many queries of the form “how many connected components are there in a prefix of vertices sorted by x” and “how many components are in a suffix”.

The brute-force approach would, for each query, filter vertices and edges and run BFS or DSU from scratch. This fails because each run costs O(n + m), repeated q times.

The improvement comes from noticing that connectivity for prefixes and suffixes can be precomputed offline. If we sort vertices by x, then for any prefix we only need to maintain a DSU over already activated vertices. As we extend the prefix, we add one vertex at a time and activate edges whose both endpoints are already active. This lets us compute all prefix component counts in a single sweep. The suffix case is symmetric by processing from right to left.

After this preprocessing, each query reduces to two binary searches and a constant-time lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute per query | O(q(n + m)) | O(n + m) | Too slow |
| Prefix + suffix DSU preprocessing | O((n + m) log n + q log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We sort all vertices by their x-coordinate and remember their positions in this ordering. Every edge is also translated into these indices.

We then compute two arrays. The first array stores, for every prefix of vertices in sorted order, the number of connected components in the subgraph induced by that prefix. The second array does the same for suffixes.

1. Sort vertices by x-coordinate and assign each vertex a position from 0 to n − 1. This gives a linear order where every prefix corresponds to a set of vertices with the smallest x-values.
2. Build adjacency lists in terms of these positions. Each original edge becomes a connection between two indices.
3. Compute prefix connectivity. We start with no active vertices. We iterate from left to right in sorted order. When adding a vertex, we initially assume it forms a new component. Then for each neighbor that is already active, we union the sets. Every successful union reduces the component count. This maintains the exact number of connected components in the current prefix.
4. Compute suffix connectivity in the same way but from right to left. We again activate vertices incrementally, unioning with already active neighbors.
5. For each query X, locate its position in the sorted x-array. Let i be the first index with x ≥ X and j be the first index with x > X. Then the left side is prefix [0, i − 1] and the right side is suffix [j, n − 1]. The answer is prefix_components[i] + suffix_components[j].

The crucial reason this works is that after removing the middle group x = X, there are no edges crossing between left and right, since every such edge would necessarily span across X and is therefore removed. Connectivity on each side is fully independent.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m, q = map(int, input().split())
        xs = list(map(int, input().split()))
        ys = list(map(int, input().split()))

        edges = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            edges[u].append(v)
            edges[v].append(u)

        queries = list(map(int, input().split()))

        order = sorted(range(n), key=lambda i: xs[i])
        pos = [0] * n
        for i, v in enumerate(order):
            pos[v] = i

        adj = [[] for _ in range(n)]
        for u in range(n):
            for v in edges[u]:
                adj[pos[u]].append(pos[v])

        pref = [0] * (n + 1)
        dsu = DSU(n)
        active = [False] * n
        comp = 0

        for i in range(n):
            v = i
            active[v] = True
            comp += 1
            for to in adj[v]:
                if active[to]:
                    if dsu.union(v, to):
                        comp -= 1
            pref[i + 1] = comp

        suff = [0] * (n + 1)
        dsu = DSU(n)
        active = [False] * n
        comp = 0

        for i in range(n - 1, -1, -1):
            v = i
            active[v] = True
            comp += 1
            for to in adj[v]:
                if active[to]:
                    if dsu.union(v, to):
                        comp -= 1
            suff[i] = comp

        xs_sorted = [xs[i] for i in order]

        for X in queries:
            import bisect
            i = bisect.bisect_left(xs_sorted, X)
            j = bisect.bisect_right(xs_sorted, X)
            out.append(str(pref[i] + suff[j]))

        out.append("")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first converts the graph into the x-sorted index space so that “prefix” literally means “all vertices to the left in x-order”. The DSU is used only to maintain connectivity while we incrementally activate vertices, which avoids recomputing global connectivity from scratch.

The prefix array stores component counts as we grow the active set from left to right. The suffix array mirrors this process from right to left. Each union operation is guarded by an active check so that we never connect vertices that have not yet been included in the current prefix or suffix.

Query handling is reduced to binary search on the sorted x-coordinates. This is the only per-query cost.

## Worked Examples

Consider a small graph where vertices are already ordered by x-coordinate: x = [1, 2, 3, 4], with some edges forming a chain.

We compute prefix components as we activate vertices.

| Step | Active vertices | DSU unions | Components |
| --- | --- | --- | --- |
| 1 | {1} | none | 1 |
| 2 | {1,2} | (1-2) | 1 |
| 3 | {1,2,3} | (2-3) | 1 |
| 4 | {1,2,3,4} | (3-4) | 1 |

Now suffix behaves similarly but in reverse order.

For a query X = 2.5, we split into left {1,2} and right {3,4}. Both are connected chains, so answer is 1 + 1 = 2.

For a query X = 3, vertices with x = 3 are removed. Left is {1,2}, right is {4}. Left is connected so 1 component, right is isolated so 1 component, total is 2.

These examples show how equality with X removes entire vertices and how edges spanning across X are implicitly excluded by splitting the sorted order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n + q log n) | sorting, DSU sweeps, and binary searches per query |
| Space | O(n + m) | adjacency in sorted space and DSU arrays |

The total limits across all test cases remain within 10^5, so linearithmic preprocessing and logarithmic queries are comfortably fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else ""

# The full solution is not embedded here for brevity in the test harness context.
# These are structural tests rather than executable assertions.

# minimum case
# 1 vertex, no edges, one query
# expected answer is always 1 or 0 depending on removal; here no removal
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node, no edges | 1 | base connectivity |
| two nodes, one edge, cut between them | 2 | split handling |
| chain of 5 nodes | 1 1 2 | prefix/suffix interaction |
| all nodes same x | 0 | full deletion at that x |

## Edge Cases

A critical case is when many vertices share the same x-coordinate. If X equals that value, all of them are removed simultaneously, so both prefix and suffix must exclude that entire block. The binary search split ensures this correctly because all equal elements fall between lower_bound and upper_bound, leaving both sides empty for that segment.

Another edge case is when X is smaller than all x-coordinates. In that case, the left part is empty and the answer depends only on the suffix structure. The prefix array correctly returns zero components at index 0, while suffix covers the full graph.

When X is larger than all coordinates, the suffix is empty and only prefix remains, again handled by boundary values of the precomputed arrays.
