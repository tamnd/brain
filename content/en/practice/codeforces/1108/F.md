---
title: "CF 1108F - MST Unification"
description: "We are given a connected undirected graph with n vertices and m edges, each with a positive weight. The goal is to adjust some edge weights by incrementing them, so that the graph's minimum spanning tree (MST) remains the same cost as initially but becomes unique."
date: "2026-06-12T05:19:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dsu", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1108
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 535 (Div. 3)"
rating: 2100
weight: 1108
solve_time_s: 45
verified: true
draft: false
---

[CF 1108F - MST Unification](https://codeforces.com/problemset/problem/1108/F)

**Rating:** 2100  
**Tags:** binary search, dsu, graphs, greedy  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected undirected graph with `n` vertices and `m` edges, each with a positive weight. The goal is to adjust some edge weights by incrementing them, so that the graph's minimum spanning tree (MST) remains the same cost as initially but becomes unique. In other words, the graph may initially have multiple MSTs of the same total cost, and we want to break ties in a minimal way by slightly increasing edge weights without changing the overall MST cost.

The input provides the graph as a list of edges with endpoints and weights. The output is a single integer: the minimum number of "increment by one" operations needed to achieve a unique MST.

Constraints are tight: `n` and `m` can be up to 200,000, and edge weights can reach `10^9`. Any solution that tries to enumerate all MSTs or check all cycles explicitly will be too slow because even `O(m^2)` operations are unfeasible. This suggests we need a solution that works roughly in `O(m log n)` time, ideally combining MST construction with an efficient way to identify ambiguous edges.

A subtle edge case is a graph where many edges have the same weight and multiple MSTs exist. For example, a triangle with edges `(1,2,1)`, `(2,3,1)`, `(1,3,1)` has three MSTs. Any naive algorithm that just picks an MST and increments edges not in it could accidentally change the MST cost or increment more edges than needed. The correct approach carefully identifies edges whose weight increments will break ties without affecting the original MST cost.

## Approaches

The brute-force approach would try to generate all MSTs, find edges present in some but not all MSTs, and increment them. This works because MST uniqueness fails only when there is an edge outside the current MST that could replace an MST edge without increasing total cost. However, enumerating all MSTs is impractical; even using a cycle check for each non-MST edge leads to `O(m * n)` or worse. With `n` up to `2 * 10^5`, this is far too slow.

The key insight is that MST ambiguity arises only from edges outside the MST that have weight equal to the maximum edge weight on the cycle they would form in the MST. If we consider an MST and a non-MST edge `(u, v, w)`, it forms a cycle with the MST. If `w` equals the maximum weight along that cycle in the MST, we can swap edges and get another MST. To prevent ambiguity, we must increase the weight of some of these non-MST edges minimally so they no longer match the maximum along their cycles. This reduces the problem to computing, for each non-MST edge, the maximum edge weight along the unique path in the MST between its endpoints.

Computing maximum edge weights along paths can be done efficiently using binary lifting with `O(n log n)` preprocessing, and then querying each non-MST edge in `O(log n)`. The total time is `O(m log n)`, which fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n) | O(n + m) | Too slow |
| Optimal | O(m log n) | O(n log n + m) | Accepted |

## Algorithm Walkthrough

1. Construct any MST of the graph using Kruskal's algorithm. Store which edges belong to the MST. This is valid because all MSTs have the same total weight, and any MST will work for analysis.
2. Build the MST as a tree and prepare binary lifting tables for LCA queries. For each node, store ancestors at powers of two and the maximum edge weight on the path to each ancestor. This allows querying the maximum weight on the path between any two nodes in `O(log n)`.
3. For each non-MST edge `(u, v, w)`, compute the maximum edge weight along the path from `u` to `v` in the MST using the binary lifting tables. If `w` equals this maximum, then this edge could be swapped with an MST edge to produce another MST.
4. Count each such edge. Incrementing its weight by one will break the ambiguity, because it will exceed the maximum weight along its cycle. The minimum number of operations is the total number of these critical edges.
5. Output this count.

Why it works: MST uniqueness is equivalent to ensuring no non-MST edge has weight equal to the maximum on the MST path connecting its endpoints. The algorithm identifies exactly these edges and increments them. Binary lifting guarantees correct maximum path queries for all non-MST edges efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))
    edges.sort()
    
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        x, y = find(x), find(y)
        if x == y: return False
        parent[y] = x
        return True

    mst_edges = []
    for w, u, v in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
    
    # build tree for LCA
    from collections import defaultdict, deque
    adj = defaultdict(list)
    for u, v, w in mst_edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    LOG = 20
    up = [[-1]*LOG for _ in range(n)]
    max_edge = [[0]*LOG for _ in range(n)]
    depth = [0]*n
    
    def dfs(u, p):
        for v, w in adj[u]:
            if v == p: continue
            up[v][0] = u
            max_edge[v][0] = w
            depth[v] = depth[u] + 1
            for i in range(1, LOG):
                if up[v][i-1] != -1:
                    up[v][i] = up[up[v][i-1]][i-1]
                    max_edge[v][i] = max(max_edge[v][i-1], max_edge[up[v][i-1]][i-1])
            dfs(v, u)
    
    dfs(0, -1)
    
    def query(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        res = 0
        for i in reversed(range(LOG)):
            if up[u][i] != -1 and depth[up[u][i]] >= depth[v]:
                res = max(res, max_edge[u][i])
                u = up[u][i]
        if u == v:
            return res
        for i in reversed(range(LOG)):
            if up[u][i] != -1 and up[u][i] != up[v][i]:
                res = max(res, max_edge[u][i], max_edge[v][i])
                u, v = up[u][i], up[v][i]
        res = max(res, max_edge[u][0], max_edge[v][0])
        return res

    mst_set = set((min(u,v), max(u,v)) for u,v,w in mst_edges)
    ans = 0
    for w, u, v in edges:
        if (min(u,v), max(u,v)) in mst_set:
            continue
        if w == query(u,v):
            ans += 1
    print(ans)

if __name__ == "__main__":
    main()
```

The code first constructs an MST using Kruskal and marks the MST edges. It builds a tree structure with adjacency lists to run DFS and fill in binary lifting tables for maximum edge queries. Each non-MST edge is then checked: if its weight equals the maximum along its path in the MST, it is a candidate for increment. Counting all such edges gives the answer.

## Worked Examples

**Sample 1:**

```
n = 8, m = 10
edges = [
1 2 1, 2 3 2, 2 4 5, 1 4 2, 6 3 3,
6 1 3, 3 5 2, 3 7 1, 4 8 1, 6 2 4
]
```

After Kruskal, MST edges include weights 1,1,1,2,2,2,3. The edge `(6,2,4)` is outside the MST and forms a cycle with maximum weight 4. Since `w == max_cycle`, incrementing it resolves ambiguity. Only one such edge exists. Output is `1`.

**Custom Input:**

```
n = 3, m = 3
edges = [
1 2 1, 2 3 1, 1 3 1
]
```

All edges have weight 1. MST chooses any two. Non-MST edge `(1,3,1)` has `w == max_cycle` and must be incremented. Output is `1`.

| Step | u | v | max on path | is critical edge? | count |
| --- | --- | --- | --- | --- | --- |
| check (1, |  |  |  |  |  |
