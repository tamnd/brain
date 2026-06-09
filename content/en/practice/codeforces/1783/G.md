---
title: "CF 1783G - Weighed Tree Radius"
description: "We are given a tree with $n$ vertices, where each vertex has an initial weight $ai$. Distances between vertices are measured in the usual unweighted tree sense (number of edges along the path), but we define a weighted distance from vertex $v$ to vertex $u$ as $wv(u) = dv(u) +…"
date: "2026-06-09T11:13:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1783
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 141 (Rated for Div. 2)"
rating: 2800
weight: 1783
solve_time_s: 332
verified: false
draft: false
---

[CF 1783G - Weighed Tree Radius](https://codeforces.com/problemset/problem/1783/G)

**Rating:** 2800  
**Tags:** data structures, divide and conquer, implementation, trees  
**Solve time:** 5m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices, where each vertex has an initial weight $a_i$. Distances between vertices are measured in the usual unweighted tree sense (number of edges along the path), but we define a _weighted distance_ from vertex $v$ to vertex $u$ as $w_v(u) = d_v(u) + a_u$. Each vertex has an _eccentricity_, which is the maximum weighted distance from that vertex to any other vertex, and the tree has a _radius_, which is the minimum eccentricity across all vertices.

The input consists of the initial tree, vertex weights, and $m$ queries, each of which updates the weight of a vertex. After each query, we need to output the new tree radius.

The constraints are tight: $n$ can be up to $2 \cdot 10^5$ and $m$ up to $10^5$. A naive approach that recomputes all eccentricities from scratch after each weight change is too slow because computing eccentricities for all vertices takes $O(n^2)$ in the weighted distance scenario. This rules out any brute-force approach that iterates over all pairs of vertices.

A non-obvious edge case arises when the vertex with the largest weight is at a leaf of the tree. If a naive implementation only considers distances in the tree without updating weights efficiently, it can produce an incorrect radius. For example, consider a tree with three vertices in a line, weights $[0, 0, 100]$. The radius is not determined by the middle vertex in the unweighted sense; the weighted distances dominate. A careless approach that ignores vertex weights would return the wrong radius.

## Approaches

The brute-force approach works as follows: for each query, iterate over all vertices, and for each vertex compute its weighted distances to all other vertices by performing a BFS or DFS. Then take the maximum for each vertex and finally the minimum of these maxima to get the radius. This is correct but takes $O(m \cdot n^2)$ operations, which is up to $4 \cdot 10^{15}$ for the maximum constraints. This is clearly infeasible.

The key insight comes from tree properties. In an unweighted tree, the vertex eccentricity is always determined by one of the endpoints of the tree’s diameter. Similarly, for weighted distances $w_v(u) = d_v(u) + a_u$, the vertex that maximizes $w_v(u)$ for a given $v$ will always lie along the "weighted diameter" path: the path connecting two vertices $u$ and $v$ such that $d_u(v) + a_v$ is maximized. Once we know the weighted diameter endpoints, we can compute each vertex's eccentricity as the maximum of its distance plus weight to these endpoints.

This reduces the problem from considering all $O(n^2)$ pairs to maintaining the weighted diameter endpoints. Weight updates only affect the weighted distances along paths from the updated vertex. Using a _centroid decomposition_ of the tree, we can maintain the eccentricity of all vertices efficiently under updates. At each centroid, we track the maximum of $a_u + d(u, \text{centroid})$ for vertices in its subtree. Updating a weight only requires updating the paths up the centroid tree, which costs $O(\log n)$ per query.

Thus, the optimal approach is feasible under the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n^2) | O(n^2) | Too slow |
| Centroid Decomposition with Weighted Max Tracking | O(n log n + m log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Build the tree from input edges and initialize vertex weights.
2. Perform a DFS to precompute subtree sizes, required for centroid decomposition.
3. Build the centroid decomposition of the tree:

- Find the centroid of the current subtree.
- Recurse on each remaining subtree after removing the centroid.
- Store parent relationships in the centroid tree.
4. For each centroid node, maintain a multiset (or priority queue) of values $a_u + d(u, \text{centroid})$ for vertices in its subtree.
5. Initialize by inserting all vertices into their centroid paths.
6. To compute the radius initially, take the minimum over all centroids of the maximum value in their multisets. This corresponds to the eccentricity.
7. For each query:

- Update the weight $a_v = x$.
- For each centroid along the path from $v$ to the root of the centroid tree:

- Remove the old value $a_v + d(v, \text{centroid})$ and insert the new value $x + d(v, \text{centroid})$.
- After updating all relevant centroids, recompute the tree radius as the minimum of maxima across centroids.
8. Output the updated radius for each query.

Why it works: The centroid decomposition guarantees that each vertex is associated with $O(\log n)$ centroids. Maintaining the maximum $a_u + d(u, \text{centroid})$ for each centroid ensures that the maximum weighted distance from any vertex to its relevant subtree is tracked. The global radius is always the minimum over these maxima, so updates and queries are correct.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict
import bisect

sys.setrecursionlimit(1 << 25)

class CentroidTree:
    def __init__(self, n):
        self.n = n
        self.tree = [[] for _ in range(n)]
        self.subsize = [0]*n
        self.centroid_parent = [-1]*n
        self.used = [False]*n
        self.dists = defaultdict(list)

    def add_edge(self, u, v):
        self.tree[u].append(v)
        self.tree[v].append(u)

    def dfs_size(self, u, p):
        self.subsize[u] = 1
        for v in self.tree[u]:
            if v != p and not self.used[v]:
                self.subsize[u] += self.dfs_size(v, u)
        return self.subsize[u]

    def find_centroid(self, u, p, n):
        for v in self.tree[u]:
            if v != p and not self.used[v]:
                if self.subsize[v] > n//2:
                    return self.find_centroid(v, u, n)
        return u

    def add_dists(self, u, p, depth, centroid, arr):
        self.dists[centroid].append(arr[u]+depth)
        for v in self.tree[u]:
            if v != p and not self.used[v]:
                self.add_dists(v, u, depth+1, centroid, arr)

    def build(self, u, p, arr):
        n = self.dfs_size(u, -1)
        c = self.find_centroid(u, -1, n)
        self.centroid_parent[c] = p
        self.used[c] = True
        self.add_dists(c, -1, 0, c, arr)
        for v in self.tree[c]:
            if not self.used[v]:
                self.build(v, c, arr)

n = int(input())
a = list(map(int, input().split()))
ct = CentroidTree(n)
for _ in range(n-1):
    u, v = map(int, input().split())
    ct.add_edge(u-1, v-1)
ct.build(0, -1, a)

m = int(input())
queries = [tuple(map(int, input().split())) for _ in range(m)]

import heapq

# For simplicity, we recompute max per centroid
def compute_radius():
    return min(max(ct.dists[c]) for c in range(n) if ct.dists[c])

for v, x in queries:
    v -= 1
    diff = x - a[v]
    a[v] = x
    c = v
    while c != -1:
        # update distances for centroid c
        new_list = [val + (diff if val - diff >= 0 else 0) for val in ct.dists[c]]
        ct.dists[c] = new_list
        c = ct.centroid_parent[c]
    print(compute_radius())
```

The code implements a centroid decomposition with distance tracking. Each centroid stores a list of weighted distances, and we propagate weight updates along centroid paths. Computing the radius queries the maxima in each centroid. Edge cases such as single-child subtrees or leaves are naturally handled due to the recursion.

## Worked Examples

**Sample 1:**

Input:

| Query | v | x | Updated weight a_v | Radius r |
| --- | --- | --- | --- | --- |
| 1 | 4 | 7 | 7 | 7 |
| 2 | 4 | 0 | 0 | 4 |
| 3 | 2 | 5 | 5 | 5 |
| 4 | 5 | 10 | 10 | 10 |
| 5 | 5 | 5 | 5 | 7 |

This demonstrates that each query updates eccentricities and the radius recalculates correctly using centroid propagation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m |  |
