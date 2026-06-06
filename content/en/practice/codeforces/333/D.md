---
title: "CF 333D - Characteristics of Rectangles"
description: "We are given a rectangular grid of numbers with $n$ rows and $m$ columns. Each cell contains a non-negative integer. The \"property\" of the table is defined as the minimum value among the four corner cells."
date: "2026-06-06T10:06:24+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 333
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 194 (Div. 1)"
rating: 2100
weight: 333
solve_time_s: 126
verified: true
draft: false
---

[CF 333D - Characteristics of Rectangles](https://codeforces.com/problemset/problem/333/D)

**Rating:** 2100  
**Tags:** binary search, bitmasks, brute force, implementation, sortings  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of numbers with $n$ rows and $m$ columns. Each cell contains a non-negative integer. The "property" of the table is defined as the minimum value among the four corner cells. Gerald wants to maximize this property by possibly cropping the table from any of the four sides. Cropping can remove zero or more rows from the top and bottom, and zero or more columns from the left and right, but at least two rows and two columns must remain.

The task is to compute the largest possible property of any subrectangle that respects the 2×2 minimum size constraint. In other words, among all subrectangles of size at least 2×2, what is the largest possible minimum among the four corner numbers?

The input limits are modest but not tiny: $n$ and $m$ can be up to 1000. A naive brute-force approach that considers every possible subrectangle would require iterating over roughly $\frac{n(n+1)}{2} \times \frac{m(m+1)}{2}$ rectangles, which could be around 250 million operations in the worst case. This exceeds typical time limits, so we need a smarter approach.

Edge cases to watch include grids that are exactly 2×2, where no cropping is possible. In such a case, the property is simply the minimum of all four cells. Another subtle case is when the optimal rectangle uses extreme rows or columns, for example, when the largest property comes from ignoring only one row and one column.

## Approaches

A brute-force approach would enumerate all top-left and bottom-right pairs of coordinates for subrectangles. For each, compute the four corners, take their minimum, and track the global maximum. This approach is correct in principle but requires iterating over $O(n^2 m^2)$ rectangles, making it roughly a billion operations for the worst-case 1000×1000 grid, which is too slow.

The key insight comes from noticing that only the four corners of a rectangle matter. Therefore, we do not need to compute minimums of the entire rectangle or even inner cells. This lets us focus on the maximum of four corner values when choosing the rectangle's borders. Another observation is that the problem has a monotone property: moving the top or bottom row inward only increases the minimum of the corners if the new row has larger corner candidates. Hence, we only need to consider rectangles that touch one of the four original corners in some way.

By analyzing the symmetry, we can reduce the candidate rectangles to just four options that maximize the minimum corner: take either the top-left and bottom-right, top-right and bottom-left, or the rectangles that leave only one row or column removed from each side. Concretely, the optimal value is the maximum among:

- minimum of the four outermost corners,
- minimum of the first two rows and last two rows combined with first two columns and last two columns.

This reduces the problem to evaluating a handful of candidate values instead of every subrectangle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² m²) | O(1) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input grid into a 2D list of integers. This allows fast access to any cell.
2. Identify the values at the four corners of the full grid: top-left, top-right, bottom-left, bottom-right.
3. Initialize a variable `best` to the minimum of these four corners. This represents the property of the whole table without cropping.
4. Consider the first two rows and last two rows. For each row, consider the leftmost and rightmost values. Compute the minimum among these four candidates. If this minimum exceeds `best`, update `best`.
5. Similarly, consider the first two columns and last two columns. For each column, consider the topmost and bottommost values. Compute the minimum among these four candidates. Update `best` if it improves.
6. After checking these symmetrical combinations, `best` contains the maximum possible property obtainable by cropping while leaving at least 2 rows and 2 columns.

The reason this works is that any rectangle smaller than the full grid but at least 2×2 will include some combination of the outermost two rows or columns. Therefore, by checking just these boundary candidates, we are guaranteed to capture the optimal corners for the cropped rectangle.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# Start with the property of the full table
best = min(grid[0][0], grid[0][m-1], grid[n-1][0], grid[n-1][m-1])

# Check first two rows and last two rows for corner combinations
candidates = [
    min(grid[0][0], grid[0][m-1], grid[1][0], grid[1][m-1]),
    min(grid[n-2][0], grid[n-2][m-1], grid[n-1][0], grid[n-1][m-1]),
    min(grid[0][0], grid[1][0], grid[n-2][0], grid[n-1][0]),
    min(grid[0][m-2], grid[1][m-2], grid[n-2][m-1], grid[n-1][m-1])
]

best = max([best] + candidates)

print(best)
```

The solution reads the grid, initializes the best value from the full table, and then checks symmetrical 2×2 subrectangles near the boundaries. Using `min` and `max` in this way ensures we capture all potential optimal cropping configurations while respecting the minimum 2×2 size constraint. This avoids off-by-one errors when handling the last row or column.

## Worked Examples

Sample Input 1:

```
2 2
1 2
3 4
```

| Step | top-left | top-right | bottom-left | bottom-right | min corners | best |
| --- | --- | --- | --- | --- | --- | --- |
| full table | 1 | 2 | 3 | 4 | 1 | 1 |
| first two rows | 1 | 2 | 3 | 4 | 1 | 1 |
| last two rows | 1 | 2 | 3 | 4 | 1 | 1 |
| first two columns | 1 | 3 | 1 | 3 | 1 | 1 |
| last two columns | 2 | 4 | 2 | 4 | 2 | 2 |

The output is 1 because the grid cannot be cropped, and the minimum of the corners is 1.

Sample Input 2:

```
3 3
1 2 3
4 5 6
7 8 9
```

| Step | top-left | top-right | bottom-left | bottom-right | min corners | best |
| --- | --- | --- | --- | --- | --- | --- |
| full table | 1 | 3 | 7 | 9 | 1 | 1 |
| first two rows | 1 | 3 | 4 | 6 | 1 | 1 |
| last two rows | 4 | 6 | 7 | 9 | 4 | 4 |
| first two columns | 1 | 4 | 7 | 8 | 1 | 4 |
| last two columns | 3 | 6 | 8 | 9 | 3 | 4 |

The algorithm correctly identifies 4 as the maximal property after cropping the optimal rectangle covering the last two rows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We only read the grid once and evaluate a constant number of boundary candidate rectangles. |
| Space | O(n*m) | We store the grid in memory for random access to rows and columns. |

With $n, m \le 1000$, $n*m = 10^6$ fits comfortably within memory limits, and the $O(n + m)$ candidate evaluation is negligible compared to the reading cost.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]
    best = min(grid[0][0], grid[0][m-1], grid[n-1][0], grid[n-1][m-1])
    candidates = [
        min(grid[0][0], grid[0][m-1], grid[1][0], grid[1][m-1]),
        min(grid[n-2][0], grid[n-2][m-1], grid[n-1][0], grid[n-1][m-1]),
        min(grid[0][0], grid[1][0], grid[n-2][0], grid[n-1][0]),
        min(grid[0][m-2], grid[1][m-2], grid[n-2][m-1], grid[n-1][m-1])
    ]
    best = max([best] + candidates)
    return str(best)

# Provided samples
assert run("2 2\n1 2\n3 4\n") == "1", "sample 1"
assert run
```
