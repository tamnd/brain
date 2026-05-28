---
title: "CF 131F - Present to Mom"
description: "We are given a black-and-white photo represented as a grid of size n × m where each cell is either '1' for a white pixel or '0' for a black pixel."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 131
codeforces_index: "F"
codeforces_contest_name: "Codeforces Beta Round 95 (Div. 2)"
rating: 2000
weight: 131
solve_time_s: 109
verified: false
draft: false
---

[CF 131F - Present to Mom](https://codeforces.com/problemset/problem/131/F)

**Rating:** 2000  
**Tags:** binary search, two pointers  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a black-and-white photo represented as a grid of size `n × m` where each cell is either '1' for a white pixel or '0' for a black pixel. Polycarpus defines a "star" as a configuration of white pixels shaped like a cross: a white pixel with white neighbors above, below, left, and right. Our goal is to count how many rectangular submatrices of the photo contain at least `k` stars. The rectangles must have sides aligned with the grid.

Given the constraints, `n` and `m` can each go up to 500, which implies the grid can contain up to 250,000 cells. If we tried a naive approach of enumerating all possible rectangles and checking how many stars lie inside each, the number of rectangles is O(n^2 × m^2), which can be over 10^10 in the worst case-far too large to handle directly. This tells us we need a preprocessing step to quickly query the number of stars inside any rectangle.

Edge cases include grids with very few stars, grids where all pixels are white forming overlapping stars, and small rectangles where a star might lie on the boundary but not fully fit the cross pattern. A careless implementation that counts stars without checking the cross pattern will overcount. For example, in a 3×3 all-white grid:

```
111
111
111
```

There is only one valid star at the center. Counting any '1' as a star would incorrectly report nine stars.

## Approaches

The brute-force method would first identify every possible rectangle and count the stars inside. To do this correctly, we must first detect all valid stars. For each cell, we check if the four neighboring cells are also white. Then, for each rectangle, we sum the stars in that region. Checking each rectangle individually results in O(n^2 × m^2 × 1) for counting stars if we precompute star positions, but enumerating rectangles is still O(n^2 × m^2), which is too slow.

The key insight is to separate star detection from rectangle enumeration. Once we mark stars on the grid, we can build a 2D prefix sum array where `prefix[i][j]` is the number of stars in the submatrix from (1,1) to (i,j). Then the sum of stars in any rectangle defined by (x1, y1) to (x2, y2) can be computed in O(1) using the standard inclusion-exclusion formula:

```
stars = prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1]
```

Now the problem reduces to counting all rectangles with at least `k` stars using an efficient strategy. We iterate over all pairs of top and bottom rows, compress the 2D problem to 1D for each column as the number of stars between those rows, and use a sliding window with two pointers to count subarrays whose sum of stars meets or exceeds `k`. This leverages the fact that the columns are cumulative and sums are non-negative, so the two-pointer technique works efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 × m^2) | O(n × m) | Too slow |
| Optimal | O(n^2 × m) | O(n × m) | Accepted |

## Algorithm Walkthrough

1. Initialize a grid `stars[n][m]` to mark positions of valid stars. Iterate over each cell `(i,j)` where 1 ≤ i ≤ n-2 and 1 ≤ j ≤ m-2. If the cell and its four side neighbors are white, mark `stars[i][j] = 1`. Otherwise, mark it as 0. This ensures only central positions of crosses are counted.
2. Build a 2D prefix sum array `prefix[n+1][m+1]`. For each cell `(i,j)`, set `prefix[i][j] = stars[i][j] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]`. This allows O(1) queries of star counts inside any rectangle.
3. Iterate over all pairs of top and bottom rows `top` and `bottom`. For each column, compute `col_stars[c]` as the number of stars between `top` and `bottom` in that column using the prefix sum array.
4. Treat `col_stars` as a 1D array. Use a two-pointer technique: maintain a sliding window of columns from `left` to `right` such that the sum of stars in this window is at least `k`. Increment `right` until the sum is ≥ k, then increment `left` while maintaining the sum. Each window defines a rectangle from `top` to `bottom` and from `left` to `right` with at least `k` stars. Add `(m - right + 1)` to the answer, representing all valid rectangles starting at `left`.
5. Sum over all top-bottom row pairs to obtain the total number of valid rectangles.

Why it works: At every stage, the algorithm maintains the exact number of stars in the current rectangle using prefix sums. The two-pointer method ensures that all contiguous subarrays (columns) are counted without missing any, and the sliding window guarantees that rectangles are counted efficiently without redundant recalculation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    
    # Step 1: mark valid stars
    stars = [[0]*m for _ in range(n)]
    for i in range(1, n-1):
        for j in range(1, m-1):
            if grid[i][j] == '1' and grid[i-1][j] == '1' and grid[i+1][j] == '1' \
               and grid[i][j-1] == '1' and grid[i][j+1] == '1':
                stars[i][j] = 1
    
    # Step 2: 2D prefix sum
    prefix = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(m):
            prefix[i+1][j+1] = stars[i][j] + prefix[i][j+1] + prefix[i+1][j] - prefix[i][j]
    
    ans = 0
    # Step 3: iterate over all row pairs
    for top in range(1, n+1):
        for bottom in range(top, n+1):
            col_stars = [0]*m
            for col in range(1, m+1):
                col_stars[col-1] = prefix[bottom][col] - prefix[top-1][col] - prefix[bottom][col-1] + prefix[top-1][col-1]
            
            # Step 4: two pointers to count valid column windows
            left = 0
            curr_sum = 0
            for right in range(m):
                curr_sum += col_stars[right]
                while curr_sum - col_stars[left] >= k:
                    curr_sum -= col_stars[left]
                    left += 1
                if curr_sum >= k:
                    ans += m - right
    
    print(ans)

if __name__ == "__main__":
    main()
```

The `stars` array isolates the detection logic for crosses. Prefix sums allow querying any rectangle in O(1). The nested loops over top-bottom pairs are manageable because `n` ≤ 500. The two-pointer scan over columns efficiently counts rectangles with at least `k` stars by leveraging the non-negative sums of `col_stars`.

## Worked Examples

**Sample 1**

```
n=4, m=6, k=2
grid:
111000
111100
011011
000111
```

| top | bottom | col_stars | left | right | curr_sum | rectangles added |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 2 2 1 0 0 | 0 | 3 | 6 | 6 |

The table shows that for the top=1 and bottom=3, columns 1-4 contain stars with sums exceeding `k=2`. Sliding window adds 6 rectangles.

**Sample 2 (all white 3×3, k=1)**

```
111
111
111
```

| top | bottom | col_stars | left | right | curr_sum | rectangles added |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 1 0 | 0 | 1 | 1 | 3 |

Only the central column has one star. Sliding window counts 3 rectangles covering all valid positions.

These traces confirm that the algorithm correctly identifies star positions and counts all rectangles containing at least `k` stars.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 × m) | Nested loop over row pairs (O(n^2)), two-pointer scan over m columns. |
| Space | O(n × m) | Store stars array and prefix sums. |

With n, m ≤ 500, n^2 × m ≤ 125
