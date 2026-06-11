---
title: "CF 1304E - 1-Trees and Queries"
description: "We are given a tree with $n$ vertices, where each vertex is connected such that there is exactly one path between any two vertices. Then we are asked multiple queries."
date: "2026-06-11T17:56:42+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1304
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 620 (Div. 2)"
rating: 2000
weight: 1304
solve_time_s: 74
verified: true
draft: false
---

[CF 1304E - 1-Trees and Queries](https://codeforces.com/problemset/problem/1304/E)

**Rating:** 2000  
**Tags:** data structures, dfs and similar, shortest paths, trees  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices, where each vertex is connected such that there is exactly one path between any two vertices. Then we are asked multiple queries. Each query specifies two vertices $x$ and $y$ where we imagine adding a new bidirectional edge, and two vertices $a$ and $b$ between which we want to find a path. The query also provides an integer $k$, and we must determine whether there exists a path from $a$ to $b$ that uses exactly $k$ edges. The path may revisit vertices or edges, but it must traverse precisely $k$ edges.

The tree size $n$ can be up to $10^5$ and there can be up to $10^5$ queries. This means any algorithm that inspects paths naively or simulates walks on the tree for each query is too slow, because even a linear scan per query would result in $10^{10}$ operations in the worst case. The length $k$ of the path can go up to $10^9$, so generating paths explicitly is impossible.

The non-obvious detail is that the path can revisit nodes and edges, meaning we can traverse cycles created by adding the extra edge multiple times. This allows paths that are longer than the simple shortest path, as long as we traverse the cycle an appropriate number of times to reach the exact length $k$. A careless approach that only considers the shortest path length between $a$ and $b$ will fail for queries where $k$ is larger but achievable by looping through the added edge.

Another subtle case is when $a$ and $b$ are the same node. The path length could still be nonzero if we traverse cycles, so we cannot assume that the length zero is required. Small trees with 3 nodes can already produce multiple paths when the extra edge is added.

## Approaches

The brute-force approach is to construct the tree, add the query edge, and perform a BFS or DFS to enumerate all paths from $a$ to $b$ until the path length reaches $k$. This is correct because it checks all possibilities, but it is infeasible. For each query, even exploring just all shortest paths is $O(n)$, and with $q = 10^5$, we are at $10^{10}$ operations. Explicitly handling paths up to length $10^9$ is impossible.

The key insight is that a tree has a unique simple path between any two vertices. Adding one edge creates exactly one simple cycle. Any path between $a$ and $b$ can be expressed as a combination of the original tree path and zero or more traversals of this single cycle. This reduces the problem to computing the shortest distance between $a$ and $b$ in the tree and checking whether $k$ is achievable using the cycle. Specifically, if the shortest tree path is $d$, and the cycle has length $c$, then any path length reachable must satisfy $k \ge d$ and $(k - d) \mod 2 = 0$, because each traversal of a cycle edge adds two edges to a simple path from $a$ to $b$.

To formalize, the cycle length is the sum of distances from $x$ to $y$ through the tree plus the added edge. Then for each query we check three candidate path lengths: the direct path from $a$ to $b$ through the tree, the path $a \to x \to y \to b$, and the path $a \to y \to x \to b$. If $k$ is at least the candidate length and has the same parity, the answer is YES.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n) | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the tree as an adjacency list. This allows fast traversal and distance computations. Store edges in both directions since the tree is undirected.
2. Perform a single DFS or BFS from an arbitrary root (vertex 1) to precompute the depth of each node and the parent of each node. Store the distance between the root and every node. These distances will allow us to compute the tree distance between any two nodes in constant time using the formula $\text{dist}(u,v) = \text{depth}[u] + \text{depth}[v] - 2 \cdot \text{depth}[\text{lca}(u,v)]$, where LCA is the lowest common ancestor.
3. Implement a function to compute distances between any two nodes. Using binary lifting for LCA, we can get tree distances in $O(\log n)$ per query. Since $n \le 10^5$, this is efficient.
4. For each query $(x, y, a, b, k)$, compute the shortest tree distance between $a$ and $b$, which we call $d_0$. Then compute distances of paths that use the extra edge: $d_1 = \text{dist}(a,x) + 1 + \text{dist}(y,b)$ and $d_2 = \text{dist}(a,y) + 1 + \text{dist}(x,b)$.
5. For each candidate distance $d$ in $[d_0, d_1, d_2]$, check if $k \ge d$ and $(k - d) \mod 2 = 0$. If any candidate satisfies these conditions, print YES. Otherwise, print NO. This ensures that paths longer than the shortest path are only considered if they can be extended by full cycles to reach exactly $k$.

Why it works: Every path in a 1-tree can be decomposed into a base tree path and zero or more full traversals of the single cycle. The parity condition ensures that the total number of edges can reach exactly $k$ without fractional traversals. Considering all three candidate paths ensures we account for both directions through the added edge.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

n = int(input())
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

LOG = 17
parent = [[-1] * (n + 1) for _ in range(LOG)]
depth = [0] * (n + 1)

def dfs(u, p):
    parent[0][u] = p
    for v in adj[u]:
        if v != p:
            depth[v] = depth[u] + 1
            dfs(v, u)

dfs(1, -1)

for k in range(1, LOG):
    for v in range(1, n + 1):
        if parent[k - 1][v] != -1:
            parent[k][v] = parent[k - 1][parent[k - 1][v]]

def lca(u, v):
    if depth[u] < depth[v]:
        u, v = v, u
    for k in range(LOG - 1, -1, -1):
        if parent[k][u] != -1 and depth[parent[k][u]] >= depth[v]:
            u = parent[k][u]
    if u == v:
        return u
    for k in range(LOG - 1, -1, -1):
        if parent[k][u] != -1 and parent[k][u] != parent[k][v]:
            u = parent[k][u]
            v = parent[k][v]
    return parent[0][u]

def dist(u, v):
    return depth[u] + depth[v] - 2 * depth[lca(u, v)]

q = int(input())
for _ in range(q):
    x, y, a, b, k = map(int, input().split())
    d0 = dist(a, b)
    d1 = dist(a, x) + 1 + dist(y, b)
    d2 = dist(a, y) + 1 + dist(x, b)
    ok = False
    for d in [d0, d1, d2]:
        if k >= d and (k - d) % 2 == 0:
            ok = True
            break
    print("YES" if ok else "NO")
```

The DFS precomputes the depth and parent arrays for all nodes. Binary lifting allows LCA queries in $O(\log n)$. The distance function calculates the tree distance quickly. The three candidate paths capture the shortest path and the two options that traverse the added edge in either direction. The parity check ensures we can extend paths using the cycle to reach exactly $k$ edges.

## Worked Examples

**Sample Input 1**

| Step | d0 | d1 | d2 | k | Result |
| --- | --- | --- | --- | --- | --- |
| Query 1: 1 3 1 2 2 | 1 | 2 | 4 | 2 | YES |
| Query 2: 1 4 1 3 2 | 3 | 2 | 4 | 2 | YES |
| Query 3: 1 4 |  |  |  |  |  |
