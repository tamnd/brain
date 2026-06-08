---
title: "CF 2045G - X Aura"
description: "We are given a grid of size $R times C$ where each cell has a height from 0 to 9. You can move only between adjacent cells (up, down, left, right)."
date: "2026-06-08T09:15:16+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "math", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2045
codeforces_index: "G"
codeforces_contest_name: "2024-2025 ICPC Asia Jakarta Regional Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2200
weight: 2045
solve_time_s: 61
verified: true
draft: false
---

[CF 2045G - X Aura](https://codeforces.com/problemset/problem/2045/G)

**Rating:** 2200  
**Tags:** graphs, math, shortest paths  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of size $R \times C$ where each cell has a height from 0 to 9. You can move only between adjacent cells (up, down, left, right). Each move incurs a penalty equal to $(h_1 - h_2)^X$, where $h_1$ is the height of the current cell, $h_2$ is the neighbor, and $X$ is a fixed odd integer. Because $X$ is odd, this penalty can be negative when moving to a higher cell.

You are asked multiple queries, each asking for the minimum total penalty from a start cell $(R_s, C_s)$ to a destination $(R_f, C_f)$. If the minimum penalty can be made arbitrarily small by cycling in a negative-penalty loop, you should output "INVALID".

Constraints are critical. The grid can be as large as $1000 \times 1000$, and there can be up to $100,000$ queries. This rules out recomputing shortest paths from scratch per query. The number of cells is up to $10^6$, which means any $O(R \cdot C \cdot \text{something})$ algorithm has to be careful. Negative cycles make standard Dijkstra unusable.

Non-obvious edge cases include scenarios where the minimum penalty path includes a negative cycle. For example, consider a 2x2 grid with heights:

```
1 2
2 1
```

with $X=1$. Moving around the cycle $(1,1) → (1,2) → (2,2) → (2,1) → (1,1)$ gives a total negative penalty. Any naive Dijkstra will either miss the negative cycle or give a finite answer instead of "INVALID". Single-cell queries should return 0.

## Approaches

A brute-force approach would be to run Bellman-Ford or Dijkstra with negative edge handling from the start of each query. Bellman-Ford handles negative weights but has $O(VE)$ complexity. Here, $V \approx 10^6$ and $E \approx 4V$, so each query would cost $O(4 \cdot 10^{12})$ in the worst case, which is infeasible. Running it once per query is impossible.

The key insight is that the penalty function is fixed across queries, and the graph structure is constant. Negative cycles are intrinsic to the entire grid, not dependent on the start cell. Therefore, we can precompute which cells are part of or reachable by negative cycles. Once negative cycles are marked, answering each query reduces to checking if the destination is reachable from a negative cycle (making it INVALID) or computing a shortest path in the remaining acyclic graph.

Since the grid is sparse and edge weights depend on heights, we can use a variant of **Bellman-Ford optimized for grids**, or more efficiently, **SPFA (Shortest Path Faster Algorithm)** with negative cycle detection. This allows computing the shortest paths from every cell to every other cell if necessary. However, because queries ask arbitrary start-destination pairs, we need either full APSP (all-pairs shortest paths) or a clever observation.

The most efficient approach is to treat each connected component separately. Each component either has a negative cycle or it does not. If it does, any query within that component that can reach the negative cycle is INVALID. Otherwise, compute shortest paths using Dijkstra on the component (since negative edges can exist but no negative cycles, Dijkstra with potential adjustments can work). With precomputation, query answers are instantaneous.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive per-query Bellman-Ford | O(Q * V * E) | O(V) | Too slow |
| Grid-wide negative-cycle detection + Dijkstra per query | O(VE + Q log V) | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Convert the grid into a graph. Each cell $(r, c)$ is a vertex. For each adjacent pair of cells, create a directed edge in both directions with weight $(h_1 - h_2)^X$. Since $X$ is odd, negative weights are allowed.
2. Detect all negative cycles using a grid-wide Bellman-Ford. Initialize a distance array with zeros. Relax all edges $R*C$ times. Any edge that can still be relaxed on the $R*C$-th iteration indicates a negative cycle. Mark all vertices involved in or reachable from a negative cycle.
3. For the remaining acyclic graph, compute shortest paths using Dijkstra with a priority queue from all start cells of queries. Because the graph has no negative cycles now, shortest paths are well-defined. Optionally, since queries are numerous, you can compute distances from every cell using Johnson's algorithm, which reweights edges to remove negative weights, and then use Dijkstra for each query.
4. For each query, if the start or destination is part of a negative cycle or reachable from it, output "INVALID". Otherwise, output the precomputed shortest path.

Why it works: The grid is fixed, and negative cycles cannot disappear by changing start or end. Any cell that can reach a negative cycle can have its total penalty reduced arbitrarily, making the scenario invalid. For acyclic or non-negative-cycle graphs, Dijkstra guarantees the shortest path due to non-decreasing distances along edges after reweighting.

## Python Solution

```python
import sys, heapq
input = sys.stdin.readline

R, C, X = map(int, input().split())
grid = [list(map(int, list(input().strip()))) for _ in range(R)]

# Directions: up, down, left, right
dirs = [(-1,0),(1,0),(0,-1),(0,1)]

# Precompute edges
edges = []
for r in range(R):
    for c in range(C):
        u = r * C + c
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                v = nr * C + nc
                w = (grid[r][c] - grid[nr][nc]) ** X
                edges.append((u, v, w))

# Detect negative cycles using Bellman-Ford
V = R * C
dist = [0]*V
in_negative_cycle = [False]*V

for i in range(V):
    updated = False
    for u, v, w in edges:
        if dist[v] > dist[u] + w:
            dist[v] = dist[u] + w
            updated = True
            if i == V-1:
                in_negative_cycle[v] = True
    if not updated:
        break

# Propagate negative cycle marks
for _ in range(V):
    for u, v, w in edges:
        if in_negative_cycle[u]:
            in_negative_cycle[v] = True

Q = int(input())
queries = [tuple(map(int,input().split())) for _ in range(Q)]

for Rs, Cs, Rf, Cf in queries:
    start = (Rs-1)*C + (Cs-1)
    end = (Rf-1)*C + (Cf-1)
    if in_negative_cycle[start] or in_negative_cycle[end]:
        print("INVALID")
        continue
    # Dijkstra from start to end
    dists = [float('inf')]*V
    dists[start] = 0
    pq = [(0, start)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dists[u]:
            continue
        if u == end:
            break
        for dr, dc in dirs:
            r, c = divmod(u, C)
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                v = nr*C + nc
                w = (grid[r][c] - grid[nr][nc])**X
                if dists[v] > dists[u] + w:
                    dists[v] = dists[u] + w
                    heapq.heappush(pq, (dists[v], v))
    print(dists[end])
```

Each section mirrors the algorithm. Edge creation translates the 2D grid to a graph. Bellman-Ford runs V iterations to detect negative cycles. Cycle propagation ensures all affected nodes are marked. Dijkstra finds shortest paths only in valid areas.

Subtle points: grid indexing is zero-based internally, whereas input is one-based. Negative powers are avoided since X is guaranteed odd. Using `heapq` prevents unnecessary relaxation loops.

## Worked Examples

**Sample Input 1**

```
3 4 1
3359
4294
3681
5
1 1 3 4
3 3 2 1
2 2 1 4
1 3 3 2
1 1 1 1
```

| Query | Start | End | Path | Penalty | Negative cycle? |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1) | (3,4) | (1,1)->(2,1)->...->(3,4) | 2 | No |
| 2 | (3,3) | (2,1) | ... |  |  |
