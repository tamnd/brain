---
title: "CF 429B - Working out"
description: "We have a two-dimensional gym represented as a grid of size n × m. Each cell contains a positive integer representing the calories burned by doing the workout at that location."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 429
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 245 (Div. 1)"
rating: 1600
weight: 429
solve_time_s: 57
verified: true
draft: false
---

[CF 429B - Working out](https://codeforces.com/problemset/problem/429/B)

**Rating:** 1600  
**Tags:** dp  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a two-dimensional gym represented as a grid of size _n_ × _m_. Each cell contains a positive integer representing the calories burned by doing the workout at that location. Two people, Iahub and Iahubina, each start from opposite corners and need to reach the other side: Iahub starts at the top-left and goes to the bottom-right, moving only down or right, while Iahubina starts at the bottom-left and goes to the top-right, moving only up or right. At exactly one cell, they meet and pause without working out. The goal is to maximize the total calories burned across both paths.

The key complexity arises from the size of the grid: _n_ and _m_ can each go up to 1000. A naive approach that tries all possible meeting points and all possible paths would be exponentially slow. Since the grid has up to 1,000,000 cells, any solution that performs O(n² · m²) operations will exceed time limits. We need something around O(n · m) to be safe.

Non-obvious edge cases include scenarios where the maximum gain comes from meeting near the borders, forcing a path to bend in non-intuitive ways. For example, consider a 3×3 grid where the middle cell has the smallest value. If the meeting cell is the center, each person must avoid wasting high-value cells unnecessarily, and a careless greedy approach might pick a local maximum but miss the optimal combined sum.

## Approaches

A brute-force approach considers every possible meeting cell. For each cell, we would compute the maximum calories collected along all possible paths from start to that cell for Iahub and from start to that cell for Iahubina. Then we would also compute the paths from the meeting cell to the end for each person. This is correct in principle, but for each of n·m meeting cells, computing a path can take O(n·m), leading to O(n²·m²) total operations. With n, m ≤ 1000, this is around 10¹² operations, far too slow.

The key insight is that each person can only move in two directions: Iahub down or right, and Iahubina up or right. This means the maximum calories collected to any cell can be precomputed using dynamic programming. Specifically, we can compute four DP arrays:

1. `dp1[i][j]` - maximum calories from top-left to `(i, j)` (Iahub start)
2. `dp2[i][j]` - maximum calories from bottom-right to `(i, j)` (Iahub end)
3. `dp3[i][j]` - maximum calories from bottom-left to `(i, j)` (Iahubina start)
4. `dp4[i][j]` - maximum calories from top-right to `(i, j)` (Iahubina end)

Once these are filled, for each potential meeting cell `(i, j)`, we can compute the total gain as the sum of two disjoint paths that avoid double-counting the meeting cell. There are two ways they can meet while maximizing total gain, corresponding to the two "crossing" patterns: one where they cross without sharing edges horizontally, and another vertically. Iterating over all internal cells (excluding the border) and computing the sum from these DP arrays is O(n·m), which is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²·m²) | O(n·m) | Too slow |
| DP Precomputation | O(n·m) | O(n·m) | Accepted |

## Algorithm Walkthrough

1. Read the dimensions `n`, `m` and the grid `a`. We need to compute maximum gains along four directions.
2. Initialize four DP arrays: `dp1`, `dp2`, `dp3`, `dp4`. Each array stores the maximum calories from a specific start to every cell. Initialize the starting cell of each DP array with the corresponding cell’s calories.
3. Fill `dp1` (Iahub top-left to bottom-right). For each cell `(i, j)`, the maximum calories to reach it is `a[i][j] + max(dp1[i-1][j], dp1[i][j-1])`. The first row and column handle edge cases where only one previous cell exists.
4. Fill `dp2` (Iahub bottom-right to top-left). For each cell `(i, j)`, `dp2[i][j] = a[i][j] + max(dp2[i+1][j], dp2[i][j+1])`. Start from the bottom-right and move backward.
5. Fill `dp3` (Iahubina bottom-left to top-right). For each cell `(i, j)`, `dp3[i][j] = a[i][j] + max(dp3[i+1][j], dp3[i][j-1])`. Start from bottom-left.
6. Fill `dp4` (Iahubina top-right to bottom-left). For each cell `(i, j)`, `dp4[i][j] = a[i][j] + max(dp4[i-1][j], dp4[i][j+1])`. Start from top-right.
7. Iterate over all internal cells `(i, j)` where `1 ≤ i ≤ n-2` and `1 ≤ j ≤ m-2`. For each cell, compute two possible crossing totals:

- Pattern 1: Iahub goes down then right, Iahubina goes right then up.

`total1 = dp1[i-1][j] + dp2[i+1][j] + dp3[i][j-1] + dp4[i][j+1]`
- Pattern 2: Iahub goes right then down, Iahubina goes up then right.

`total2 = dp1[i][j-1] + dp2[i][j+1] + dp3[i+1][j] + dp4[i-1][j]`

Update the answer with the maximum of `total1` and `total2`.
8. Output the maximum total gain.

**Why it works:** The DP arrays guarantee that for any cell, we have the maximum gain along the allowed directions. By precomputing all four directions, the crossing patterns can be combined in O(1) for each internal cell without double-counting the meeting point. Since we consider all internal cells, we ensure the optimal meeting point is selected.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

dp1 = [[0]*m for _ in range(n)]
dp2 = [[0]*m for _ in range(n)]
dp3 = [[0]*m for _ in range(n)]
dp4 = [[0]*m for _ in range(n)]

# dp1: top-left to bottom-right
for i in range(n):
    for j in range(m):
        best = 0
        if i > 0:
            best = max(best, dp1[i-1][j])
        if j > 0:
            best = max(best, dp1[i][j-1])
        dp1[i][j] = a[i][j] + best

# dp2: bottom-right to top-left
for i in range(n-1, -1, -1):
    for j in range(m-1, -1, -1):
        best = 0
        if i < n-1:
            best = max(best, dp2[i+1][j])
        if j < m-1:
            best = max(best, dp2[i][j+1])
        dp2[i][j] = a[i][j] + best

# dp3: bottom-left to top-right
for i in range(n-1, -1, -1):
    for j in range(m):
        best = 0
        if i < n-1:
            best = max(best, dp3[i+1][j])
        if j > 0:
            best = max(best, dp3[i][j-1])
        dp3[i][j] = a[i][j] + best

# dp4: top-right to bottom-left
for i in range(n):
    for j in range(m-1, -1, -1):
        best = 0
        if i > 0:
            best = max(best, dp4[i-1][j])
        if j < m-1:
            best = max(best, dp4[i][j+1])
        dp4[i][j] = a[i][j] + best

ans = 0
for i in range(1, n-1):
    for j in range(1, m-1):
        total1 = dp1[i-1][j] + dp2[i+1][j] + dp3[i][j-1] + dp4[i][j+1]
        total2 = dp1[i][j-1] + dp2[i][j+1] + dp3[i+1][j] + dp4[i-1][j]
        ans = max(ans, total1, total2)

print(ans)
```

The first four blocks compute the DP tables for all four directions. The loop over internal cells ensures we avoid the borders, as the meeting point must allow all paths to continue. The two crossing patterns handle both possible ways of combining paths without overlapping calories. Off
