---
title: "CF 1034B - Little C Loves 3 II"
description: "We are given a very large rectangular grid where each cell can be identified by coordinates $(x, y)$. We repeatedly place two chess pieces at a time, but only if the Manhattan distance between the two chosen empty cells is exactly 3."
date: "2026-06-16T19:22:08+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "flows", "graph-matchings"]
categories: ["algorithms"]
codeforces_contest: 1034
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 511 (Div. 1)"
rating: 2200
weight: 1034
solve_time_s: 211
verified: false
draft: false
---

[CF 1034B - Little C Loves 3 II](https://codeforces.com/problemset/problem/1034/B)

**Rating:** 2200  
**Tags:** brute force, constructive algorithms, flows, graph matchings  
**Solve time:** 3m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a very large rectangular grid where each cell can be identified by coordinates $(x, y)$. We repeatedly place two chess pieces at a time, but only if the Manhattan distance between the two chosen empty cells is exactly 3. Each such placement consumes two distinct unused cells, and once a cell is used it cannot be reused in any later pair.

The task is to maximize the number of placed pairs, meaning we want to maximize how many disjoint pairs of cells we can form such that every pair has Manhattan distance exactly 3. Equivalently, we are looking for a maximum matching in a graph where each cell is a node and edges connect pairs of cells at Manhattan distance 3.

The grid size constraints are extremely large, up to $10^9 \times 10^9$, so any solution that depends on iterating over cells or even rows and columns is impossible. The solution must depend only on structural properties of the grid and local patterns.

A key subtlety is that even though the grid is infinite in scale, the pairing rule is local: only relative offsets of the form $(dx, dy)$ with $|dx| + |dy| = 3$ matter. That means the structure repeats periodically, and any optimal strategy must be expressible as a tiling or decomposition of small patterns.

Edge cases appear immediately when one dimension is small. If either $n < 2$ or $m < 2$, no pair is possible. More interestingly, if both dimensions are small but non-trivial, such as $n = m = 2$, there is still no valid pair because the maximum Manhattan distance is 2, so the answer is 0 even though the board is not empty. A naive approach that assumes “large grid implies many matches” would fail here unless it explicitly checks feasibility.

Another important boundary case is when one dimension is very small, for example $n = 1$. Even though the other dimension can be extremely large, all distances reduce to horizontal distances only, so only pairs with difference exactly 3 along a line matter. This reduces the problem to a one-dimensional pairing problem with spacing constraints.

## Approaches

If we try to model the problem directly, we can think of each cell as a node and connect edges between all pairs of cells whose Manhattan distance is 3. Each valid move consumes one edge in a matching. A brute-force strategy would explicitly construct this graph and run a maximum matching algorithm such as Hopcroft-Karp on a bipartite split of the grid.

This is conceptually correct because the graph is bipartite under parity of $(x + y)$, and matching ensures disjoint usage of vertices. However, the graph size is $n \cdot m$, which can be as large as $10^{18}$. Even constructing adjacency implicitly is impossible, since each node has a constant number of neighbors but there are still too many nodes to process.

The key observation is that the grid can be partitioned into independent local structures. Every cell only interacts with cells at offsets $(\pm 3, 0), (\pm 2, \pm 1), (\pm 1, \pm 2), (0, \pm 3)$. This is a fixed finite neighborhood. Such problems typically reduce to finding how many edges in an optimal packing can be formed per unit area.

We then notice that the structure behaves differently depending on the grid shape. If both dimensions are at least 3, the grid can be tiled by blocks where each block contributes a fixed number of pairs. If one dimension is 1 or 2, the interaction graph degenerates and must be handled separately.

For large grids, the optimal matching saturates almost all cells except a bounded remainder pattern along edges, so the answer becomes linear in $n \cdot m$ with a small correction depending on residues modulo 3. After carefully analyzing local configurations, the result simplifies into a clean formula based on counting how many full $3 \times 3$-like interaction blocks can be formed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching on Grid Graph | O(nm) or worse | O(nm) | Too slow |
| Pattern-based Decomposition | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. If either dimension is 1, reduce the problem to a line of length $L = \max(n, m)$. In this case, only pairs at distance exactly 3 along the line are valid, so we count how many disjoint pairs we can form. This is simply $L // 4$ pairs, because each optimal segment of length 4 contributes one valid pairing.
2. If either dimension is 2, treat the grid as two parallel lines. In this case, local interactions form constrained 2-row patterns. We compute the answer by grouping columns in blocks of 4, since the optimal packing repeats every 4 columns.
3. If both dimensions are at least 3, we exploit full two-dimensional structure. We partition the grid into blocks of size $3 \times 3$. Inside each block, we can form exactly 4 valid pairs covering 8 cells, leaving one unused cell. This is the densest repeating structure compatible with Manhattan distance 3 constraints.
4. Compute how many full
