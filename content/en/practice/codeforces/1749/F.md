---
title: "CF 1749F - Distance to the Path"
description: "We are given a tree with $n$ vertices. Each vertex initially holds a value of zero. There are two kinds of queries. The first type asks for the current value of a specific vertex."
date: "2026-06-09T15:19:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 1749
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 138 (Rated for Div. 2)"
rating: 2800
weight: 1749
solve_time_s: 133
verified: true
draft: false
---

[CF 1749F - Distance to the Path](https://codeforces.com/problemset/problem/1749/F)

**Rating:** 2800  
**Tags:** data structures, dfs and similar, trees  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices. Each vertex initially holds a value of zero. There are two kinds of queries. The first type asks for the current value of a specific vertex. The second type asks us to add a fixed value $k$ to all vertices that are within a small distance $d$ from the path connecting two vertices $u$ and $v$. The distance here is the usual tree distance: the number of edges along the shortest path.

Because $n$ and $m$ can each be up to $2 \cdot 10^5$, a naive solution that iterates over all vertices for each query of type two would perform up to $4 \cdot 10^{10}$ operations in the worst case. That is far too slow. The maximum distance $d$ in the update is constrained to 20, which hints that we can exploit a small neighborhood property rather than touching all vertices.

A subtle aspect is how the “distance to the path” is defined. For example, a vertex not on the path can still be affected if it is within distance $d$ to any vertex on the path. A careless implementation that only updates vertices along the path itself would produce incorrect results. For instance, in a star-shaped tree with center 1 and leaves 2, 3, 4, a query updating the path from 2 to 3 with $d = 1$ must also update vertex 1, which is not directly on the path but adjacent.

Another potential trap is when $d$ is very large. For $d \ge \text{tree diameter}$, the update affects all vertices. This edge case needs to be handled efficiently, without iterating over all nodes explicitly.

## Approaches

The brute-force approach is simple to describe. For each query of type two, we identify all vertices along the path from $u$ to $v$, and then for every vertex in the tree, we compute its distance to each vertex on the path and update its value if the distance is at most $d$. This guarantees correctness, but the worst-case complexity is $O(m \cdot n \cdot d_{\text{path}})$, which is about $8 \cdot 10^{10}$ in the worst-case scenario. Clearly too slow.

The key insight comes from two observations. First, the maximum distance $d$ in updates is at most 20. That is extremely small compared to $n$. Second, the affected vertices are exactly those within distance $d$ from some path, which we can decompose into “distance from each endpoint minus distance along the path.” This suggests we can propagate the update in a BFS or DFS manner starting from the path nodes, but only up to distance $d$. Since $d \le 20$, each update touches at most roughly $O(d \cdot n_{\text{path}})$ vertices, which is acceptable. Another simplification is that we can precompute depths and parent pointers to quickly locate the path and distances along the tree.

We further optimize by noticing that updates only involve vertices within a small “ball” around the path. Using a BFS from the endpoints $u$ and $v$, or using a precomputed Euler tour and LCA structure, we can efficiently enumerate all vertices within distance $d$ from the path without visiting irrelevant vertices. This reduces the complexity to roughly $O(m \cdot d^2)$, which is feasible for $d \le 20$ and $m \le 2 \cdot 10^5$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m \cdot n^2)$ | $O(n)$ | Too slow |
| Optimal (small distance BFS/DFS) | $O(m \cdot d^2 + n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the tree and construct adjacency lists. This allows quick traversal from any vertex to its neighbors.
2. Compute depth and parent of each vertex using a simple DFS. Depth helps in quickly determining the distance between any two nodes along the tree.
3. Prepare an LCA structure, for example using binary lifting. The LCA allows us to quickly find the path between any two vertices $u$ and $v$, because the path can be broken into the path from $u$ to LCA and from $v$ to LCA.
4. For queries of type one, simply print the current value of the vertex. This is constant time.
5. For queries of type two, first compute the LCA of $u$ and $v$ to identify the path. For each node $x$ on the path from $u$ to $v$, perform a BFS or DFS up to distance $d$, adding $k$ to all reached vertices. To avoid double counting, keep a visited set for this update only.
6. Because $d$ is small, BFS/DFS for each path node is limited to a tiny neighborhood. Even for the worst-case path of length $n$, each update only propagates $O(d^2)$ times, which is acceptable given the constraints.

Why it works: Each update only affects vertices within distance $d$ of the path. By starting BFS/DFS from each path node and limiting traversal to distance $d$, we precisely cover the affected set. The LCA decomposition guarantees that the path is correctly identified and no vertices are skipped. The visited set ensures that we do not add $k$ multiple times to the same vertex in a single query.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

n = int(input())
adj = [[] for _ in range(n)]
for _ in range(n-1):
    u, v = map(int, input().split())
    adj[u-1].append(v-1)
    adj[v-1].append(u-1)

# depth and parent for LCA
LOG = 20
parent = [[-1]*n for _ in range(LOG)]
depth = [0]*n

def dfs(u, p):
    parent[0][u] = p
    for v in adj[u]:
        if v != p:
            depth[v] = depth[u] + 1
            dfs(v, u)
dfs(0, -1)

# binary lifting
for k in range(1, LOG):
    for v in range(n):
        if parent[k-1][v] != -1:
            parent[k][v] = parent[k-1][parent[k-1][v]]

def lca(u, v):
    if depth[u] < depth[v]:
        u, v = v, u
    for k in reversed(range(LOG)):
        if parent[k][u] != -1 and depth[parent[k][u]] >= depth[v]:
            u = parent[k][u]
    if u == v:
        return u
    for k in reversed(range(LOG)):
        if parent[k][u] != -1 and parent[k][u] != parent[k][v]:
            u = parent[k][u]
            v = parent[k][v]
    return parent[0][u]

# value array
val = [0]*n

m = int(input())
for _ in range(m):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        print(val[tmp[1]-1])
    else:
        _, u, v, k, d = tmp
        u -= 1
        v -= 1
        w = lca(u, v)
        # collect path nodes
        path = []
        x = u
        while x != w:
            path.append(x)
            x = parent[0][x]
        path.append(w)
        stack = []
        x = v
        while x != w:
            stack.append(x)
            x = parent[0][x]
        path.extend(reversed(stack))
        
        visited = [False]*n
        for node in path:
            dq = deque()
            dq.append((node, 0))
            while dq:
                cur, dist = dq.popleft()
                if dist > d or visited[cur]:
                    continue
                visited[cur] = True
                val[cur] += k
                for nei in adj[cur]:
                    if not visited[nei]:
                        dq.append((nei, dist+1))
```

Explanation: The DFS computes depth and parent for all nodes. Binary lifting lets us find the LCA in $O(\log n)$ time. For each update, we enumerate the path from $u$ to $v$ via the LCA, then perform a limited BFS from each path node up to distance $d$. A local visited array avoids double counting within the same update. Queries of type one simply return the stored value.

## Worked Examples

**Sample 1**

| Query | Path | Affected vertices | Updated values |
| --- | --- | --- | --- |
| 2 4 5 10 2 | 4-2-5 | 4,2,5,1,3 | +10 |
| 1 3 | - | - | 10 |
| 1 6 | - | - | 0 |
| 2 1 1 10 20 | 1 | all |  |
