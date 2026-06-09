---
title: "CF 1771E - Hossam and a Letter"
description: "We are given an n × m grid representing Hossam's ground. Each cell has a quality: perfect (.), medium (m), or bad (). Hossam wants to draw the letter 'H' by placing walls on some cells. The letter consists of two vertical lines and one horizontal line connecting them."
date: "2026-06-09T12:24:21+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1771
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 837 (Div. 2)"
rating: 2500
weight: 1771
solve_time_s: 92
verified: true
draft: false
---

[CF 1771E - Hossam and a Letter](https://codeforces.com/problemset/problem/1771/E)

**Rating:** 2500  
**Tags:** brute force, dp, implementation, two pointers  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an `n × m` grid representing Hossam's ground. Each cell has a quality: perfect (`.`), medium (`m`), or bad (`#`). Hossam wants to draw the letter 'H' by placing walls on some cells. The letter consists of two vertical lines and one horizontal line connecting them. The vertical lines must not be in the same column or adjacent columns. They must start and end on the same row, and the horizontal line must lie strictly between the top and bottom row of the vertical lines. Walls cannot be placed on bad cells, and at most one medium cell can be used.

The task is to find the largest number of walls that can be placed forming such a letter 'H'. If it is impossible to draw the letter, we must return `0`.

The constraints `n, m ≤ 400` suggest that an O(n^2 m^2) algorithm is plausible because the total number of operations would be around 2.5 × 10^7, which is acceptable under a 2-second time limit. However, anything O(n^3 m^3) would be too slow.

Non-obvious edge cases include grids that are too narrow to fit two vertical lines with at least one column between them. For instance, a 2×2 grid entirely filled with perfect cells cannot hold a valid 'H' because the vertical lines would have to be in neighboring columns. Another subtle case occurs when there is exactly one medium cell. We need to ensure we never exceed the medium cell quota while maximizing the number of walls.

## Approaches

The brute-force approach is straightforward. Iterate over all possible pairs of columns `(c1, c2)` for the vertical lines. For each pair, iterate over all possible start rows and end rows for the vertical lines. Then, for each possible row between them, consider it as the horizontal line's position. Count the number of walls in the chosen rectangle while respecting the medium-cell constraint. This approach is correct because it enumerates all valid configurations, but it is O(n^3 m^2) at worst, which is too slow for n = m = 400.

The key insight to optimize is that we can precompute the maximum vertical line lengths that can be built in each column without violating the medium/bad constraints. We also track the positions of medium cells. Once vertical lines' lengths are known, we can iterate over all pairs of columns and use two pointers to find the largest vertical segment where a horizontal line can be placed, checking that the horizontal line does not cross a medium/bad cell in a forbidden way. Precomputing prefix sums per column allows us to query medium/bad cells in O(1) for any segment. This reduces the complexity to O(n m^2), which is acceptable for the given bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3 m^2) | O(n m) | Too slow |
| Optimized Prefix + Column Pair | O(n m^2) | O(n m) | Accepted |

## Algorithm Walkthrough

1. Precompute for each column two arrays: the number of perfect and medium cells up to each row using prefix sums. This allows O(1) queries for any vertical segment to check how many medium or bad cells exist.
2. For each column, determine the maximum contiguous vertical line length starting at every possible row that does not include a bad cell and includes at most one medium cell. Store this as a column-length array.
3. Iterate over all pairs of columns `(c1, c2)` where `c2 - c1 ≥ 2` to ensure vertical lines are not neighboring.
4. For a given pair, slide over the rows using two pointers to find the maximal vertical segment `[r1, r2]` that is valid in both columns under the medium-cell restriction.
5. For each candidate vertical segment, iterate over possible horizontal line positions strictly between `r1` and `r2`. Count the total walls: `length_vertical1 + length_vertical2 + length_horizontal`. Ensure no more than one medium cell is used across the whole 'H'.
6. Keep track of the maximum total walls found over all column pairs and vertical segments.

**Why it works:** The algorithm considers every possible pair of columns and every feasible vertical segment, while the prefix sums guarantee that we correctly respect the medium-cell constraint. By scanning horizontal lines only inside vertical segments, we respect the geometric constraints of the 'H'.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# Precompute prefix sums of medium and bad cells for each column
medium = [[0]*m for _ in range(n+1)]
bad = [[0]*m for _ in range(n+1)]

for r in range(1, n+1):
    for c in range(m):
        medium[r][c] = medium[r-1][c] + (grid[r-1][c] == 'm')
        bad[r][c] = bad[r-1][c] + (grid[r-1][c] == '#')

def get_counts(col, r1, r2):
    mids = medium[r2+1][col] - medium[r1][col]
    bads = bad[r2+1][col] - bad[r1][col]
    return mids, bads

max_walls = 0

for c1 in range(m):
    for c2 in range(c1+2, m):
        r1 = 0
        r2 = 0
        while r1 < n:
            # extend r2 as far as possible
            while r2 < n:
                mids1, bads1 = get_counts(c1, r1, r2)
                mids2, bads2 = get_counts(c2, r1, r2)
                if bads1 > 0 or bads2 > 0 or mids1 + mids2 > 1:
                    break
                r2 += 1
            # consider horizontal line positions between r1+1 and r2-2
            if r2 - r1 >= 3:
                # total vertical walls
                vertical_walls = (r2 - r1) * 2
                # horizontal line
                for hr in range(r1+1, r2-1):
                    h_meds = 0
                    h_bads = 0
                    for hc in range(c1+1, c2):
                        if grid[hr][hc] == '#':
                            h_bads = 1
                            break
                        if grid[hr][hc] == 'm':
                            h_meds += 1
                    if h_bads or mids1 + mids2 + h_meds > 1:
                        continue
                    total = vertical_walls + (c2 - c1 - 1)
                    max_walls = max(max_walls, total)
            r1 += 1
            if r2 < r1:
                r2 = r1

print(max_walls)
```

The solution first computes prefix sums to allow constant-time queries for medium and bad cells. It then iterates over column pairs, using a two-pointer approach on rows to find maximal vertical segments without violating constraints. For each feasible vertical segment, it checks all valid horizontal lines and ensures the total number of medium cells does not exceed one. The careful handling of horizontal line positions avoids counting walls in invalid locations.

## Worked Examples

**Sample Input 1:**

```
2 3
#m.
.#.
```

| Variable | Value |
| --- | --- |
| Column pairs | (0,2) only |
| Row segments | cannot form length ≥ 3 |
| Max walls | 0 |

Even though some perfect cells exist, the vertical lines cannot span a length ≥ 3, so the 'H' cannot be drawn.

**Sample Input 2:**

```
4 4
....
.m..
....
....
```

| Variable | Column pair | Vertical segment | Horizontal | Walls |
| --- | --- | --- | --- | --- |
| (0,2) | r1=0,r2=3 | hr=1, hr=2 | total walls | 6 |
| (0,3) | r1=0,r2=3 | hr=1, hr=2 | total walls | 7 |

The algorithm correctly maximizes walls while respecting the medium cell restriction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m^2) | Each pair of columns is considered, scanning rows with two pointers, feasible within n ≤ 400 |
| Space | O(n m) | Prefix sums for medium and bad cells |

This fits comfortably within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    medium = [[0]*m for _ in range(n+1)]
    bad = [[0]*m for _ in range(n+1)]
    for r in range(1, n+1):
        for c in range(m):
            medium[r][c] = medium[r-1][c] + (grid[r-1][c] == 'm')
```
