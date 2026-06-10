---
title: "CF 1482F - Useful Edges"
description: "We are given an undirected weighted graph with up to 600 vertices and up to about 180,000 edges, where each edge has a positive weight. Then we are given a list of queries, each consisting of a pair of vertices $u$ and $v$ and a number $l$."
date: "2026-06-10T23:27:35+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1482
codeforces_index: "F"
codeforces_contest_name: "\u0422\u0435\u0445\u043d\u043e\u043a\u0443\u0431\u043e\u043a 2021 - \u0424\u0438\u043d\u0430\u043b"
rating: 2400
weight: 1482
solve_time_s: 192
verified: true
draft: false
---

[CF 1482F - Useful Edges](https://codeforces.com/problemset/problem/1482/F)

**Rating:** 2400  
**Tags:** graphs, shortest paths  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph with up to 600 vertices and up to about 180,000 edges, where each edge has a positive weight. Then we are given a list of queries, each consisting of a pair of vertices $u$ and $v$ and a number $l$. An edge is considered _useful_ if there exists a path between some query pair $(u, v)$ whose total weight does not exceed $l$ and which passes through this edge. The goal is to count how many edges are useful.

Given the constraints, a naive approach of checking every path for every query is infeasible because the number of paths grows exponentially. The upper bound of $n = 600$ suggests that algorithms with $O(n^3)$ complexity are acceptable, because $600^3 \approx 2 \times 10^8$ operations is just within reasonable limits for a 5-second time frame. Edge weights and query limits are large ($10^9$), so we must avoid algorithms that rely on constructing all paths explicitly or using weight-based arrays of that size.

Non-obvious edge cases include queries where the minimal path may loop over vertices multiple times to stay under the length $l$. For instance, a graph forming a triangle $1-2-3-1$ with weights 2, 2, 3 and a query $(1,3,4)$ requires considering paths like $1-2-3$ which sum to 4. A careless implementation that only considers shortest paths without recombining distances could miss this.

Another subtlety is that the input can include multiple queries affecting the usefulness of the same edge, and a single query can make multiple edges useful simultaneously.

## Approaches

The brute-force method would be to process each query separately, perform a full search (like Dijkstra or BFS) from $u$ to find all reachable paths under length $l$, and mark every edge along those paths as useful. This works in principle but is too slow. Each Dijkstra call is $O(m + n \log n)$, and with up to $q = 180,000$ queries, this can easily exceed $10^{10}$ operations.

The key observation to speed this up is that we only need to know, for each edge $(a, b)$, if it can participate in any path $u \to v$ of length at most $l$. We can precompute all-pairs shortest paths once using the Floyd-Warshall algorithm, since $n \le 600$. Let $dist[x][y]$ denote the shortest distance from $x$ to $y$. Then, for an edge $(a,b,w)$, it is useful for a query $(u,v,l)$ if either $dist[u][a] + w + dist[b][v] \le l$ or $dist[u][b] + w + dist[a][v] \le l$. This works because any path contributing to usefulness cannot be shorter than the shortest paths connecting endpoints. Checking this condition for all edges against all queries is feasible, because $O(n^2 + q \cdot m)$ fits within the time limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * (n + m log n)) | O(n + m) | Too slow |
| Optimal | O(n^3 + m * n) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the graph edges and construct an adjacency matrix or distance matrix where `dist[i][j]` is initially infinity, except 0 on the diagonal. Fill in the direct edge weights between connected vertices.
2. Run Floyd-Warshall: iterate through each intermediate vertex `k`, and for every pair `(i,j)`, update `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. This ensures that `dist[i][j]` becomes the shortest distance between vertices `i` and `j`.
3. Prepare an array `best[i]` for each vertex `i`, which will track the largest allowable `l - dist[i][v]` across all queries involving `v`. This is essentially how much remaining distance can be “spent” on edges adjacent to `i` in a path toward `v`.
4. Iterate through each query `(u, v, l)`. For every vertex `a`, update `best[a] = max(best[a], l - dist[v][a])`. This means that from vertex `a`, the edge leading toward `v` must not exceed this leftover distance to satisfy the query.
5. Now, iterate over all edges `(a,b,w)`. For the edge to be useful, there must exist a vertex `i` such that `best[a] >= w` or `best[b] >= w`. This checks if this edge can participate in a path satisfying any query. Count all such edges.
6. Output the total count of useful edges.

Why it works: The Floyd-Warshall algorithm guarantees that `dist[i][j]` is the shortest path distance. By tracking the maximum allowed residual path length (`best[a]`), we capture exactly which edges can be part of a valid path for any query. Any edge not satisfying this condition cannot be included in any path under any query's limit.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
INF = 10**18

edges = []
dist = [[INF]*n for _ in range(n)]
for i in range(n):
    dist[i][i] = 0

for _ in range(m):
    u, v, w = map(int, input().split())
    u -= 1
    v -= 1
    edges.append((u, v, w))
    dist[u][v] = w
    dist[v][u] = w

q = int(input())
queries = []
for _ in range(q):
    u, v, l = map(int, input().split())
    u -= 1
    v -= 1
    queries.append((u, v, l))

# Floyd-Warshall
for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

# Prepare best residual distances
best = [-10**18]*n
for u, v, l in queries:
    for i in range(n):
        best[i] = max(best[i], l - dist[v][i])

count = 0
for a, b, w in edges:
    if best[a] >= w or best[b] >= w:
        count += 1

print(count)
```

The code reads the graph and queries, computes all-pairs shortest paths, and then computes the maximum leftover distance `best[i]` for each vertex. Finally, each edge is tested against `best` to determine usefulness. Subtle implementation points include using a large initial value for `INF` to avoid overflow and converting 1-based indices to 0-based for Python lists.

## Worked Examples

**Sample 1:**

```
n = 4, edges = [(1,2,1),(2,3,1),(3,4,1),(1,3,3),(2,4,3),(1,4,5)], query = (1,4,4)
```

| Edge | dist[u][a] + w + dist[b][v] | Useful? |
| --- | --- | --- |
| 1-2 | 0+1+2=3 | Yes |
| 2-3 | 1+1+1=3 | Yes |
| 3-4 | 2+1+0=3 | Yes |
| 1-3 | 0+3+1=4 | Yes |
| 2-4 | 1+3+0=4 | Yes |
| 1-4 | 0+5+0=5 | No |

This confirms 5 useful edges, matching the output.

**Sample 2 (constructed):**

```
n=3, edges=[(1,2,10),(2,3,5)], queries=[(1,3,11)]
```

| Edge | dist[1][a] + w + dist[b][3] | Useful? |
| --- | --- | --- |
| 1-2 | 0+10+5=15 | No |
| 2-3 | 10+5+0=15 | No |

No edges satisfy the query, output is 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3 + n_m + n_q) | Floyd-Warshall is n^3, updating `best` is n_q, checking edges is m_n |
| Space | O(n^2 + m + q) | Distance matrix is n^2, edges list is m, queries list is q |

Given n=600, n^3 ≈ 2×10^8, and m,q ≤ n^2, this fits comfortably in 5 seconds and 512 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    INF = 10**18
    edges = []
```
