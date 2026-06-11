---
title: "CF 1194B - Yet Another Crosses Problem"
description: "We are given a grid of tiles, each either black or white, and the goal is to make it \"interesting\" by forming at least one cross. A cross exists at position $(x, y)$ if the entire row $x$ and the entire column $y$ are black."
date: "2026-06-12T00:18:26+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1194
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 68 (Rated for Div. 2)"
rating: 1300
weight: 1194
solve_time_s: 178
verified: false
draft: false
---

[CF 1194B - Yet Another Crosses Problem](https://codeforces.com/problemset/problem/1194/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 2m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of tiles, each either black or white, and the goal is to make it "interesting" by forming at least one cross. A cross exists at position $(x, y)$ if the entire row $x$ and the entire column $y$ are black. Our tool is painting individual white tiles black, and we want the minimum number of tiles to paint to create at least one cross.

Each query provides a different grid. The grid sizes can be up to $5 \cdot 10^4$ rows or columns, but the total number of tiles across all queries is at most $4 \cdot 10^5$. This means any solution must avoid $O(n \cdot m \cdot n \cdot m)$ algorithms. A solution that scans every possible row-column combination naively is too slow because it could involve $O(n \cdot m \cdot (n + m))$ operations, which reaches $10^{10}$ in the worst case.

Non-obvious edge cases include grids that are already crosses, or grids with almost full rows and columns except for one cell. For instance, a 3x3 grid with:

```
*.*
.*.
*.*
```

requires painting the center cell to form a cross, but a careless approach that counts only fully black rows or columns will miss the minimal solution.

## Approaches

The brute-force approach considers every cell as a potential cross and counts how many cells in its row and column are white. This requires iterating through all $n \cdot m$ cells and checking each row and column separately, giving $O(n \cdot m \cdot (n + m))$ operations. This works for small grids but exceeds the problem limits.

The key insight is that we only need two precomputed values per row and column: the number of black cells. For row $i$, let `row_black[i]` be the number of black cells, and for column $j`, `col_black[j]`be the number of black cells. The number of white cells to paint to make a cross at $(i, j)$ is`(m - row_black[i]) + (n - col_black[j])`. If $(i, j)$ is white, we have double-counted it, so subtract one in that case. This reduces the complexity to scanning all rows and columns once to count black cells, then scanning all cells once to compute minimal painting, giving $O(n \cdot m)$ total operations per query. This is efficient because the sum of $n \cdot m$ over all queries is $4 \cdot 10^5$.

| Approach | Time Complexity | Space Comple
