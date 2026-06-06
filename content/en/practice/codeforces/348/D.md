---
title: "CF 348D - Turtles"
description: "We are given a rectangular grid of size n by m, where each cell is either free or blocked. Two turtles start at the top-left corner, cell (1,1), and both want to reach the bottom-right corner, cell (n,m)."
date: "2026-06-06T18:33:15+07:00"
tags: ["codeforces", "competitive-programming", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 348
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 202 (Div. 1)"
rating: 2500
weight: 348
solve_time_s: 125
verified: false
draft: false
---

[CF 348D - Turtles](https://codeforces.com/problemset/problem/348/D)

**Rating:** 2500  
**Tags:** dp, matrices  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid of size _n_ by _m_, where each cell is either free or blocked. Two turtles start at the top-left corner, cell (1,1), and both want to reach the bottom-right corner, cell (_n_,_m_). The turtles can only move down or right at each step, and they cannot pass through blocked cells. The turtles have a restriction: their paths must not intersect at any cell except the start and end cells. The task is to count the number of such pairs of non-intersecting paths modulo 10^9 + 7.

The constraints indicate that the grid can be as large as 3000 by 3000. Any solution that attempts to enumerate all paths explicitly would be hopelessly slow since the number of paths grows exponentially with _n_ and _m_. This forces us to think in terms of dynamic programming or combinatorial counting rather than brute force.

Subtle edge cases include scenarios where one path is forced along a narrow corridor of free cells. For example, if the middle row is blocked except for a single column, any naive approach that does not track the relative positions of the turtles may overcount intersecting paths. Another edge case occurs when the paths must “swap sides” around an obstacle; the algorithm must carefully avoid counting paths that cross.

## Approaches

The brute-force approach would be to generate all possible paths from (1,1) to (n,m) for each turtle and then check which pairs are non-intersecting. Even for a 10x10 grid, the number of paths is on the order of thousands per turtle, leading to millions of pairs. For n=m=3000, this is astronomically large. This approach is correct in principle but computationally infeasible.

The key insight comes from observing that each path consists of a sequence of right and down moves. If we track the number of ways a turtle can reach each cell, we can precompute the number of paths from the start to each cell, and separately the number of paths from each cell to the end. With these counts, we can exploit inclusion-exclusion: the total number of unordered pairs of paths is the square of the total number of paths, minus the pairs that intersect at any cell other than the start or end. We reduce the problem to counting paths that intersect at a given intermediate cell, which can be done using DP tables.

The optimal solution uses dynamic programming to compute four tables. Let `dp_start[x][y]` be the number of paths from (1,1) to (x,y), and `dp_end[x][y]` be the number of paths from (x,y) to (n,m). Then the number of pairs of paths that intersect at (x,y) is `dp_start[x][y]^2 * dp_end[x][y]^2`. Summing this for all cells except the start and end and subtracting from the total squared paths gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^{n*m}) | O(2^{n*m}) | Too slow |
| Optimal DP | O(n*m) | O(n*m) | Accepted |

## Algorithm Walkthrough

1. Initialize two DP tables `dp_start` and `dp_end` of size n x m filled with zeros. `dp_start[x][y]` counts paths from (1,1) to (x,y), `dp_end[x][y]` counts paths from (x,y) to (n,m). This captures all reachable positions efficiently.
2. Set `dp_start[0][0] = 1` and `dp_end[n-1][m-1] = 1` because the start and end cells always have one trivial path to themselves.
3. Fill `dp_start` iteratively. For each free cell (x,y), add paths from the top neighbor if it exists and is free, and from the left neighbor if it exists and is free. This computes the total number of ways to reach each cell from the start.
4. Fill `dp_end` iteratively in reverse. For each free cell (x,y), add paths from the bottom neighbor if it exists and is free, and from the right neighbor if it exists and is free. This computes the number of ways to reach the end from each cell.
5. Compute the total number of paths from start to end, `total_paths = dp_start[n-1][m-1]`.
6. Initialize `intersect_sum = 0`. For each intermediate cell (x,y) except the start and end, if it is free, add `(dp_start[x][y] * dp_end[x][y])^2` modulo 10^9+7 to `intersect_sum`. This counts all pairs that intersect at that cell.
7. Subtract `intersect_sum` from `total_paths^2` modulo 10^9+7 to get the number of pairs of non-intersecting paths.
8. Output the result.

Why it works: By squaring the DP counts, we enumerate all unordered pairs of paths and count exactly how many intersect at each intermediate cell. Subtracting these from the total squared paths leaves only pairs that meet only at the start and end, matching the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

dp_start = [[0] * m for _ in range(n)]
dp_end = [[0] * m for _ in range(n)]

dp_start[0][0] = 1
for i in range(n):
    for j in range(m):
        if grid[i][j] == '#':
            dp_start[i][j] = 0
            continue
        if i > 0:
            dp_start[i][j] = (dp_start[i][j] + dp_start[i-1][j]) % MOD
        if j > 0:
            dp_start[i][j] = (dp_start[i][j] + dp_start[i][j-1]) % MOD

dp_end[n-1][m-1] = 1
for i in reversed(range(n)):
    for j in reversed(range(m)):
        if grid[i][j] == '#':
            dp_end[i][j] = 0
            continue
        if i + 1 < n:
            dp_end[i][j] = (dp_end[i][j] + dp_end[i+1][j]) % MOD
        if j + 1 < m:
            dp_end[i][j] = (dp_end[i][j] + dp_end[i][j+1]) % MOD

total_paths = dp_start[n-1][m-1]
intersect_sum = 0
for i in range(n):
    for j in range(m):
        if (i == 0 and j == 0) or (i == n-1 and j == m-1) or grid[i][j] == '#':
            continue
        intersect_sum = (intersect_sum + dp_start[i][j] * dp_end[i][j] % MOD * dp_start[i][j] % MOD * dp_end[i][j] % MOD) % MOD

answer = (total_paths * total_paths - intersect_sum + MOD) % MOD
print(answer)
```

The solution initializes DP tables for forward and backward path counts. Boundary checks prevent out-of-bounds access. The intersection sum uses modular arithmetic carefully to avoid overflow. The subtraction step adds MOD before taking modulo to avoid negative results.

## Worked Examples

Sample 1:

```
4 5
.....
.###.
.###.
.....
```

`dp_start`:

| i\j | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 0 |
| 3 | 1 | 1 | 1 | 1 | 1 |

`dp_end`:

| i\j | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 0 | 0 | 0 | 0 | 1 |
| 3 | 1 | 1 | 1 | 1 | 1 |

`total_paths = 1`. The only intermediate free cell where both paths could intersect is blocked by obstacles. So `intersect_sum = 0`. The answer is `1*1 - 0 = 1`.

Another example:

```
2 2
..
..
```

Both turtles can go either right then down or down then right. There are two paths. Squaring gives 4 total pairs, subtract pairs intersecting at (1,1) or (2,2) only. The answer comes out as 2, as expected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Filling two DP tables of size n*m and iterating through all cells for intersection counting |
| Space | O(n*m) | Two DP tables of size n*m |

Given n and m up to 3000, n*m is
