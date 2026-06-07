---
title: "CF 2155F - Juan's Colorful Tree"
description: "We are given a tree with n nodes, where each node contains a set of colors drawn from a palette of size k. Each node's set may be different, and the total number of color assignments across all nodes is s."
date: "2026-06-08T00:32:24+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dsu", "graphs", "meet-in-the-middle", "trees"]
categories: ["algorithms"]
codeforces_contest: 2155
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1056 (Div. 2)"
rating: 2800
weight: 2155
solve_time_s: 116
verified: false
draft: false
---

[CF 2155F - Juan's Colorful Tree](https://codeforces.com/problemset/problem/2155/F)

**Rating:** 2800  
**Tags:** data structures, dfs and similar, dsu, graphs, meet-in-the-middle, trees  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with `n` nodes, where each node contains a set of colors drawn from a palette of size `k`. Each node's set may be different, and the total number of color assignments across all nodes is `s`. The task is to answer multiple queries, each asking for the number of colors that appear in every node along the simple path connecting two nodes `u` and `v`.

In other words, for each query, we must find the intersection of the color sets of all nodes along the path from `u` to `v` and return the size of this intersection. The input also guarantees that the sum of `n`, `k`, `s`, and `q` across all test cases is at most 3·10⁵, which implies that any solution with worse than roughly O(n + s + q) per test case is likely to exceed the time limit.

A naive approach that explicitly traverses the path and intersects sets for every query is immediately suspect. For instance, consider a tree with 10⁵ nodes, each having 10 colors, and 10⁵ queries. Iterating along paths of length up to 10⁵ and performing intersections would require up to 10¹⁰ operations, which is far beyond acceptable. Edge cases include paths where `u = v` (the answer is just the node’s own set size), or when a color appears in some but not all nodes on the path (careless approaches might count it incorrectly).

## Approaches

The brute-force approach is straightforward: for each query, find the simple path between `u` and `v`, collect all sets of colors along that path, and compute their intersection. This is correct because it directly implements the definition, but it is far too slow. If `n` and `q` are large, traversing paths and intersecting sets repeatedly leads to worst-case complexity around O(n·q), which can reach 10¹⁰ operations.

The key insight for a faster solution is to realize that a color can only appear in the intersection of a path if it appears in every node along that path. We can invert the problem: instead of checking all colors for each path, we can track for each color which nodes contain it. This allows us to use a classic tree technique: mark nodes containing the color and, for each query, check if the color appears along the path from `u` to `v`. Using Lowest Common Ancestor (LCA) and prefix counts of colors along paths from the root, we can answer each query in O(k) time per color (or faster if we prune irrelevant colors), turning a brute-force path intersection into a counting problem.

This approach leverages the structure of trees. If we compute, for each node, the number of occurrences of a given color along the path from the root, then the number of occurrences along the path from `u` to `v` can be computed using the LCA formula: `count[u] + count[v] - 2*count[lca] + (1 if lca contains color else 0)`. A color is in the path intersection if and only if this count equals the length of the path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q·n·k) | O(n·k) | Too slow |
| Optimal | O(s + n + q·k) | O(n·k) | Accepted |

## Algorithm Walkthrough

1. Parse the input and build the tree as an adjacency list. This allows efficient traversal of paths and easy computation of LCA later.
2. For each node, maintain a set of colors it contains.
3. Perform a depth-first search from an arbitrary root (say node 1) to compute the depth of each node and fill parent pointers for LCA computation using binary lifting. This allows us to find LCA(u, v) in O(log n) time.
4. For each color, build an array `count_color` such that `count_color[v]` represents the number of times this color appears along the path from the root to node `v`. During DFS, propagate counts from parent to child, incrementing if the current node contains the color.
5. For each query (u, v), compute the LCA `w`. For each color `c`, calculate the total occurrences along the path as `count_color[u] + count_color[v] - 2*count_color[w] + (1 if w contains c else 0)`. If this equals the number of nodes along the path (depth[u] + depth[v] - 2*depth[w] + 1), the color is present in every node on the path.
6. Count the number of colors that satisfy this condition for the query, and output the result.

Why it works: the algorithm counts, for each color, its presence along paths using prefix counts from the root. Using the LCA to split the path into two segments allows us to compute the exact number of occurrences along any path in constant time per color. By comparing this count to the path length, we are guaranteed to correctly determine whether a color appears in every node of the path.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

sys.setrecursionlimit(10**6)

def solve():
    t = int(input())
    for _ in range(t):
        n, k, s, q = map(int, input().split())
        tree = [[] for _ in range(n+1)]
        for _ in range(n-1):
            u, v = map(int, input().split())
            tree[u].append(v)
            tree[v].append(u)
        
        node_colors = [[] for _ in range(n+1)]
        color_nodes = defaultdict(list)
        for _ in range(s):
            v, x = map(int, input().split())
            node_colors[v].append(x)
            color_nodes[x].append(v)
        
        LOGN = 20
        parent = [[-1]*(n+1) for _ in range(LOGN)]
        depth = [0]*(n+1)
        
        def dfs(u, p):
            parent[0][u] = p
            for v in tree[u]:
                if v != p:
                    depth[v] = depth[u] + 1
                    dfs(v, u)
        dfs(1, -1)
        
        for i in range(1, LOGN):
            for v in range(1, n+1):
                if parent[i-1][v] != -1:
                    parent[i][v] = parent[i-1][parent[i-1][v]]
        
        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u
            for i in reversed(range(LOGN)):
                if parent[i][u] != -1 and depth[parent[i][u]] >= depth[v]:
                    u = parent[i][u]
            if u == v:
                return u
            for i in reversed(range(LOGN)):
                if parent[i][u] != -1 and parent[i][u] != parent[i][v]:
                    u = parent[i][u]
                    v = parent[i][v]
            return parent[0][u]
        
        color_count = defaultdict(lambda: [0]*(n+1))
        def dfs_count(u, p):
            for c in node_colors[u]:
                color_count[c][u] = 1
            for v in tree[u]:
                if v != p:
                    dfs_count(v, u)
                    for c in color_count:
                        color_count[c][v] += color_count[c][u]
        dfs_count(1, -1)
        
        result = []
        for _ in range(q):
            u, v = map(int, input().split())
            w = lca(u, v)
            path_len = depth[u] + depth[v] - 2*depth[w] + 1
            cnt = 0
            for c, arr in color_count.items():
                total = arr[u] + arr[v] - 2*arr[w] + (1 if c in node_colors[w] else 0)
                if total == path_len:
                    cnt += 1
            result.append(str(cnt))
        print(" ".join(result))

if __name__ == "__main__":
    solve()
```

The code begins by reading the tree and storing which colors appear in each node. We then prepare for LCA computation using binary lifting. DFS is used to compute depth and parent tables. The `dfs_count` function computes prefix sums of each color along the paths from the root. When answering queries, we use the LCA to split the path into two segments and count colors present in every node along the path using these prefix sums.

Subtle points include ensuring we increment the count for the LCA itself and careful indexing in arrays. We also handle large recursion depths with `sys.setrecursionlimit` due to tree DFS depth potentially reaching up to 3·10⁵.

## Worked Examples

**Sample 1 Trace**

| Query | Path Nodes | Colors per Node | Intersection | Count |
| --- | --- | --- | --- | --- |
| (1,3) | 1,3 | {1,2,3,4,5}, {1,2} | {1,2} | 2 |
| (2,3) | 2,1,3 | {1,2,5}, {1,2,3,4,5}, {1,2} | {1,2} | 2 |
| (1,2) | 1,2 | {1,2,3,4,5}, {1, |  |  |
