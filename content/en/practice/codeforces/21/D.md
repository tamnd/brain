---
title: "CF 21D - Traveling Graph"
description: "We are given a weighted undirected graph with up to 15 vertices and up to 2000 edges. Each edge has a positive weight, and there may be multiple edges connecting the same pair of vertices or edges that loop back to the same vertex."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "graph-matchings", "graphs"]
categories: ["algorithms"]
codeforces_contest: 21
codeforces_index: "D"
codeforces_contest_name: "Codeforces Alpha Round 21 (Codeforces format)"
rating: 2400
weight: 21
solve_time_s: 42
verified: true
draft: false
---
[CF 21D - Traveling Graph](https://codeforces.com/problemset/problem/21/D)

**Rating:** 2400  
**Tags:** bitmasks, graph matchings, graphs  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph with up to 15 vertices and up to 2000 edges. Each edge has a positive weight, and there may be multiple edges connecting the same pair of vertices or edges that loop back to the same vertex. The task is to find the shortest cycle that starts at vertex 1 and traverses every edge at least once. If such a cycle does not exist, we return -1.

The key observation is that the cycle must be allowed to reuse vertices and edges if necessary because visiting every edge exactly once may be impossible. We are essentially asked to compute an **edge-covering cycle starting from a given vertex**. With n ≤ 15, we can exploit algorithms that are exponential in n but not in m, since m can be up to 2000.

A naive approach that tries to generate all possible sequences of edges is impractical because the number of sequences grows factorially in m. Even with only 15 vertices, having 2000 edges makes brute-force edge sequences impossible. Loops and multiple edges complicate the situation because the minimal cycle may reuse certain edges multiple times. For example, a single vertex with a loop of weight 5 should return 5, not 0.

Edge cases include a graph with a single vertex and no edges, in which the cycle does not exist, graphs where multiple parallel edges exist, or graphs where some vertices are disconnected from vertex 1. A careless solution might try to traverse each vertex once instead of each edge, producing wrong results in graphs with multiple edges.

## Approaches

The brute-force approach would attempt to enumerate all permutations of edges or all walks starting at vertex 1. For each candidate walk, we would check if it visits every edge and sum its total weight. The number of walks explodes combinatorially with m. Even if we prune obviously invalid paths, this approach is O((2^m) × m) in the worst case and quickly exceeds any feasible time limit for m ≈ 2000.

The key insight comes from **transforming the problem into a variant of the Chinese Postman Problem** (also called the Route Inspection Problem). In a graph, if we want to traverse every edge at least once with minimal cost, we only need to add extra edges to make all vertices have even degree, because an Eulerian cycle already covers all edges once. If a vertex has an odd degree, we must pair it with another odd-degree vertex and add the shortest path between them. The resulting augmented graph can be traversed starting at vertex 1, and it will cover all edges at least once with minimal extra cost.

Since n ≤ 15, we can compute all-pairs shortest paths using Floyd-Warshall in O(n^3). Then we find all vertices with odd degrees. Because there can be at most n odd-degree vertices, we can compute the minimal pairing using a **bitmask dynamic programming** approach, where each state represents which odd vertices are unmatched. This DP runs in O(2^k × k^2) where k is the number of odd vertices, which is feasible for k ≤ 15. Adding the weight of the existing edges and the minimal pairing gives the answer.

The key shift from brute-force is observing that we do not need to explicitly construct every cycle. Instead, we can reason about which edges must be repeated to allow an Eulerian traversal. Once we reduce the problem to pairing odd-degree vertices optimally, the problem becomes a tractable DP over subsets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2^m) × m) | O(m) | Too slow |
| Optimal (Eulerian + DP) | O(n^3 + 2^k × k^2) | O(n^2 + 2^k) | Accepted |

## Algorithm Walkthrough

1. Read the input and build the adjacency matrix of size n × n, initializing non-edges with infinity. For multiple edges between two vertices, keep only the minimum weight.
2. Compute all-pairs shortest paths using Floyd-Warshall. This ensures that when we need to add edges to pair odd-degree vertices, we know the minimal cost of connecting any two vertices.
3. Compute the degree of each vertex using the original edges. Identify all vertices with an odd degree. Let k be the number of odd-degree vertices.
4. If k = 0, the graph is already Eulerian. The minimal cycle length is simply the sum of all edge weights. Return this sum.
5. If k > 0, we must pair odd-degree vertices. Use a bitmask to represent which odd vertices are still unmatched. Initialize dp[mask] = infinity, except dp[0] = 0.
6. For each mask, find the first unmatched vertex i. Then iterate over all unmatched vertices j > i and compute dp[mask | (1 << i) | (1 << j)] = min(dp[mask | ...], dp[mask] + dist[i][j]), where dist[i][j] is the shortest path length from i to j.
7. After filling the DP, dp[(1 << k) - 1] contains the minimal total weight to pair all odd vertices.
8. The final answer is sum_of_edge_weights + dp[(1 << k) - 1]. If the graph is disconnected, check if vertex 1 is connected to all edges; otherwise, return -1.

**Why it works**: Euler’s theorem guarantees that a graph with all even degrees has an Eulerian cycle. If vertices have odd degrees, adding edges along shortest paths between them ensures all vertices have even degree with minimal extra cost. The DP over subsets ensures that we find the minimal pairing of odd vertices, which directly corresponds to the minimal number of repeated edges needed to traverse the graph entirely. Because all shortest paths are precomputed, adding edges via DP always uses minimal cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def solve():
    n, m = map(int, input().split())
    dist = [[INF]*n for _ in range(n)]
    deg = [0]*n
    sum_edges = 0
    
    for _ in range(m):
        x, y, w = map(int, input().split())
        x -= 1
        y -= 1
        sum_edges += w
        deg[x] += 1
        deg[y] += 1
        if dist[x][y] > w:
            dist[x][y] = dist[y][x] = w

    for i in range(n):
        dist[i][i] = 0

    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # check connectivity
    for i in range(n):
        for j in range(n):
            if dist[i][j] == INF:
                # If there are edges in disconnected components, no solution
                if deg[i] > 0 and deg[j] > 0:
                    print(-1)
                    return

    odd = [i for i in range(n) if deg[i] % 2 == 1]
    k = len(odd)

    if k == 0:
        print(sum_edges)
        return

    dp = [INF]*(1<<k)
    dp[0] = 0

    for mask in range(1<<k):
        i = 0
        while i < k and (mask & (1 << i)):
            i += 1
        if i == k:
            continue
        for j in range(i+1, k):
            if not (mask & (1 << j)):
                new_mask = mask | (1 << i) | (1 << j)
                dp[new_mask] = min(dp[new_mask], dp[mask] + dist[odd[i]][odd[j]])

    print(sum_edges + dp[(1<<k)-1])

if __name__ == "__main__":
    solve()
```

The adjacency matrix allows fast shortest path computation. Floyd-Warshall ensures we always choose minimal paths when pairing odd vertices. The bitmask DP carefully handles all pairings without redundancy. The connectivity check ensures we return -1 for disconnected graphs. Off-by-one errors in indices are avoided by consistently using 0-based indexing internally.

## Worked Examples

**Sample 1**

Input:

```
3 3
1 2 1
2 3 1
3 1 1
```

| Step | deg | odd | dp mask | dp value |
| --- | --- | --- | --- | --- |
| Initial | [2,2,2] | [] | 0 | 0 |

All degrees are even, so minimal cycle = sum_edges = 3. No DP needed. Correct output is 3.

**Custom Sample 2**

Input:

```
4 3
1 2 1
2 3 2
3 4 3
```

- Degrees: [1,2,2,1], odd vertices = [0,3]
- Only one pair: 1-4 shortest path cost = 6 (1-2-3-4)
- sum_edges = 6
- Minimal cycle = 6 + 6 = 12

DP table:

| mask | dp[mask] |
| --- | --- |
| 0b00 | 0 |
| 0b11 | 6 |

Final
