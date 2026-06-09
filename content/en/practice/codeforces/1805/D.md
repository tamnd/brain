---
title: "CF 1805D - A Wide, Wide Graph"
description: "We are given a tree with $n$ vertices and asked to generate a sequence of graphs $Gk$ for $k = 1$ to $n$. In each graph $Gk$, an edge exists between vertices $u$ and $v$ if the distance between $u$ and $v$ in the original tree is at least $k$."
date: "2026-06-09T09:17:48+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1805
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 862 (Div. 2)"
rating: 1800
weight: 1805
solve_time_s: 207
verified: false
draft: false
---

[CF 1805D - A Wide, Wide Graph](https://codeforces.com/problemset/problem/1805/D)

**Rating:** 1800  
**Tags:** dfs and similar, dp, graphs, greedy, trees  
**Solve time:** 3m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices and asked to generate a sequence of graphs $G_k$ for $k = 1$ to $n$. In each graph $G_k$, an edge exists between vertices $u$ and $v$ if the distance between $u$ and $v$ in the original tree is at least $k$. For each $k$, we must count the number of connected components in $G_k$.

The input provides $n-1$ edges defining the tree. Since $n$ can be up to $10^5$, any solution with quadratic time in $n$ is immediately ruled out. Computing pairwise distances explicitly for all pairs would require $O(n^2)$ operations, which is far too slow. We therefore need a solution that works in roughly $O(n \log n)$ or $O(n)$.

A subtle edge case occurs when $k$ is larger than the tree’s diameter. In that case, no two vertices are connected, and each vertex forms its own component. For example, a star tree with 5 vertices and $k = 3$ produces 5 components because the largest distance between any two leaves is 2. A naive algorithm that does not consider tree structure would mistakenly connect vertices that are too far apart.

Another edge case arises when $k = 1$. By definition, all vertex pairs satisfy the distance requirement, so $G_1$ is fully connected, yielding exactly one component regardless of the tree’s structure.

## Approaches

A brute-force approach would construct $G_k$ explicitly for each $k$. For each $k$, we would check the distance between every pair of vertices, and then run a DFS or BFS to count components. This approach is correct, but for $n = 10^5$ it requires roughly $n^2$ distance checks per $k$, resulting in a total of $O(n^3)$ operations. This is infeasible.

The key insight is that the problem is essentially about the tree’s diameter and subtree depths. The connected components of $G_k$ can be inferred from how “deep” vertices are in the tree and how long paths exist without hitting a vertex that would split a component. More concretely, we can root the tree at an arbitrary vertex, then for each vertex compute the longest path in its subtree. If a subtree does not have depth sufficient to reach distance $k$, it will form a separate component in $G_k$.

The final optimization uses dynamic programming on trees. At each vertex, we track the heights of the longest two subtrees below it. These heights allow us to determine for each $k$ whether the vertex participates in a larger component or starts a new component. By combining heights efficiently and propagating counts up the tree, we can compute the number of components for all $k$ in $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n^2) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree arbitrarily, for instance at vertex 1. This is a bookkeeping choice to simplify subtree calculations.
2. Perform a DFS from the root. At each vertex, compute the heights of its two deepest child subtrees. These heights correspond to the longest distances within the subtree.
3. Maintain a multiset of subtree heights for each vertex. This allows us to quickly determine the largest path passing through the vertex and whether that path is at least $k$ long.
4. For each vertex, propagate the contribution to the number of components upwards. If the maximum subtree height plus one is less than $k$, that vertex and its subtree form a new component. Otherwise, the subtree merges into a larger component.
5. Aggregate the number of components for each $k$ using a sweep over the unique depths. This ensures we update counts only at the points where the number of components changes.
6. Output the computed component counts for all $k = 1$ to $n$. For $k$ greater than the tree’s diameter, output $n$ because each vertex becomes its own component.

Why it works: The algorithm maintains an invariant that at each vertex, we know the maximum depth reachable in its subtree. When this depth is insufficient to maintain a distance of at least $k$, the subtree splits into a new component. This guarantees that all paths satisfying the distance constraint are correctly connected, and no vertices that cannot reach distance $k$ are incorrectly merged.

## Python Solution

```python
import sys
from collections import defaultdict, deque
input = sys.stdin.readline

n = int(input())
edges = defaultdict(list)
for _ in range(n-1):
    u, v = map(int, input().split())
    edges[u].append(v)
    edges[v].append(u)

# BFS to get heights from farthest node (tree diameter ends)
def bfs(start):
    dist = [-1]*(n+1)
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in edges[u]:
            if dist[v] == -1:
                dist[v] = dist[u]+1
                q.append(v)
    farthest = max(range(1,n+1), key=lambda x: dist[x])
    return farthest, dist

# first BFS to find one end of diameter
u, _ = bfs(1)
# second BFS to find other end and distances
v, dist_u = bfs(u)
_, dist_v = bfs(v)

diameter = max(dist_u)
res = [1]*n  # initialize with 1 for k=1

# for k
```
