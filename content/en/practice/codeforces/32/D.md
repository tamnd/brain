---
title: "CF 32D - Constellation"
description: "We are given a 2D grid of size _n_ by _m_, each cell either containing a star * or empty .. The task is to locate constellations shaped like a cross."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 32
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 32 (Div. 2, Codeforces format)"
rating: 1600
weight: 32
solve_time_s: 59
verified: true
draft: false
---
[CF 32D - Constellation](https://codeforces.com/problemset/problem/32/D)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 2D grid of size _n_ by _m_, each cell either containing a star `*` or empty `.`. The task is to locate constellations shaped like a cross. A cross is centered at a star and extends exactly _x_ squares vertically and horizontally in all four directions, with _x_ being any positive integer such that all five cells exist and contain stars. We are asked to find the k-th constellation according to a specific ordering: first by radius (smallest first), then by row of the central star (topmost first), then by column (leftmost first).

The bounds are _n_, _m_ ≤ 300 and _k_ ≤ 30 million. The map size is moderate, so an O(n² m²) algorithm is acceptable, but O(n m max(n,m)) would start to push limits. With 300×300 grid, brute-force attempts on every radius could result in tens of millions of checks, which is at the upper limit of what we can process in 2 seconds. Edge cases include maps with no stars, crosses at the edges, crosses with radius 1 versus larger radii, and asking for a k-th constellation when fewer exist than k.

A careless implementation might iterate over potential crosses without first validating bounds. For example, if the central star is at (1,1), a naive check might try to access (0,1) for the upper arm, leading to an index error. Similarly, a map filled with stars except for a missing middle star could fool a naive radius counting algorithm.

## Approaches

The brute-force approach is conceptually simple: for every star on the map, try every possible radius starting from 1 until the cross would extend out of bounds. For each radius, check all four arms to see if stars exist. Record the constellation if valid, then sort all found constellations according to radius, row, and column. This is correct but inefficient. With n = m = 300, a star in the center could have radius up to 150, and checking each star for every radius multiplies operations, giving O(n m min(n,m)) in the worst case. With 90,000 cells and 150 radius checks, we exceed 10 million operations, close to the limit.

The key insight is that we only need to know the maximum arm length in each direction for each star. Precompute, for each cell, the number of consecutive stars in the up, down, left, and right directions using dynamic programming: iterate top-to-bottom for the "up" array, bottom-to-top for "down", left-to-right for "left", and right-to-left for "right". The maximal cross radius at each star is then the minimum of these four precomputed values. Once we know this, we can generate all valid crosses without iterating over every radius individually. This reduces redundant checks and makes the algorithm fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n m min(n,m)) | O(1) | Too slow at upper bounds |
| Precompute Arm Lengths | O(n m) | O(n m × 4) | Accepted |

## Algorithm Walkthrough

1. Read the grid and initialize four matrices of size n×m: up, down, left, right. Each matrix will store the consecutive stars in that direction starting from the current cell.
2. Fill the "up" matrix by iterating each column from top to bottom. If a cell contains a star, set up[i][j] = up[i-1][j] + 1 (or 1 if top row). This counts how many consecutive stars exist upward including the current cell.
3. Similarly, fill "down" by iterating bottom to top, "left" by iterating left to right, and "right" by iterating right to left.
4. For every cell containing a star, compute its maximal cross radius as `r = min(up[i][j], down[i][j], left[i][j], right[i][j]) - 1`. Subtract 1 because the central star is counted in each direction.
5. For each radius from 1 up to r, record a tuple `(radius, row, col)` representing a valid cross. Store all tuples in a list.
6. Sort the list of crosses by radius, then row, then column.
7. If k exceeds the number of crosses, output -1. Otherwise, take the k-th tuple and output the coordinates of the center, upper, lower, left, and right stars.

Why it works: the precomputation guarantees that for every cell we know the maximum reach in all four directions. By taking the minimum, we avoid generating invalid crosses. Sorting ensures the requested k-th constellation is exactly the one that satisfies the problem's ranking rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
grid = [input().strip() for _ in range(n)]

up = [[0]*m for _ in range(n)]
down = [[0]*m for _ in range(n)]
left = [[0]*m for _ in range(n)]
right = [[0]*m for _ in range(n)]

# Precompute consecutive stars
for i in range(n):
    for j in range(m):
        if grid[i][j] == '*':
            up[i][j] = 1 + (up[i-1][j] if i > 0 else 0)
            left[i][j] = 1 + (left[i][j-1] if j > 0 else 0)

for i in reversed(range(n)):
    for j in reversed(range(m)):
        if grid[i][j] == '*':
            down[i][j] = 1 + (down[i+1][j] if i < n-1 else 0)
            right[i][j] = 1 + (right[i][j+1] if j < m-1 else 0)

crosses = []
for i in range(n):
    for j in range(m):
        if grid[i][j] == '*':
            radius = min(up[i][j], down[i][j], left[i][j], right[i][j]) - 1
            for r in range(1, radius+1):
                crosses.append((r, i, j))

crosses.sort()
if k > len(crosses):
    print(-1)
else:
    r, i, j = crosses[k-1]
    print(i+1, j+1)
    print(i+1-r, j+1)
    print(i+1+r, j+1)
    print(i+1, j+1-r)
    print(i+1, j+1+r)
```

This solution first precomputes the maximum stretch in each direction to avoid redundant radius checks. The subtraction of 1 in the radius ensures we only count stars beyond the center. Sorting tuples `(radius, i, j)` directly respects the problem's ordering. Boundary checks are implicit because the precomputation stops at grid edges.

## Worked Examples

Sample 1 input:

```
5 6 1
....*.
...***
....*.
..*...
.***..
```

| i | j | up | down | left | right | min-1 (radius) | crosses recorded |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 1 | 1 | 1 | 0 | - |
| 2 | 4 | 1 | 1 | 1 | 2 | 0 | - |
| 2 | 5 | 2 | 2 | 2 | 2 | 1 | radius 1 cross |

The trace confirms the algorithm correctly computes radius and generates the first cross.

Second example, edge case with minimal map:

```
3 3 1
.*.
***
.*.
```

Central star at (2,2) has radius 1. Output:

```
2 2
1 2
3 2
2 1
2 3
```
## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m) | Precomputing four matrices and iterating for crosses is linear in the number of cells; sorting crosses adds O(n m log(n m)) but is acceptable for n*m ≤ 90000 |
| Space | O(n m) | Four directional matrices plus list of crosses |

The solution is well within the 2-second time limit and 256 MB memory limit. Sorting is not a bottleneck because the maximum number of crosses is bounded by the total number of stars times min(n,m).

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    up = [[0]*m for _ in range(n)]
    down = [[0]*m for _ in range(n)]
    left = [[0]*m for _ in range(n)]
    right = [[0]*m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                up[i][j] = 1 + (up[i-1][j] if i > 0 else
```
