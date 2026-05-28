---
title: "CF 14A - Letter"
description: "We are given a rectangular grid representing a sheet of graph paper with n rows and m columns. Some of the squares are s"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 14
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 14 (Div. 2)"
rating: 800
weight: 14
solve_time_s: 68
verified: true
draft: false
---

[CF 14A - Letter](https://codeforces.com/problemset/problem/14/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid representing a sheet of graph paper with _n_ rows and _m_ columns. Some of the squares are shaded, marked by `*`, and the rest are unshaded, marked by `.`. Bob wants to cut out the smallest rectangle that contains all shaded squares so that he can send it at minimal cost. The output is simply the contents of this rectangle, preserving the original shading pattern.

Since both dimensions are bounded by 50, the grid is small. That means any algorithm that touches every cell a few times is fast enough. The problem is essentially one of finding the smallest bounding box around all `*` characters.

Non-obvious edge cases include situations where all shaded cells are on the same row, on the same column, or clustered at a corner. For example, if the input is:

```
3 3
*..
...
...
```

The output must be just `*`, not the entire row or column. A careless implementation that, for instance, always prints full rows or columns might over-include empty cells. Similarly, a rectangle with only one row or one column should be correctly handled without generating index errors.

## Approaches

The brute-force approach would be to iterate over all possible rectangles in the grid, checking for each rectangle whether it contains all `*` and selecting the one with the minimum area. This works because correctness is guaranteed: any rectangle containing all stars is a candidate. However, the operation count is roughly `(n * m)^2 * (n * m)` for checking each rectangle, which is around 15 million iterations for `n = m = 50`. While this could still run in under a second in Python, it is inefficient and unnecessary.

The optimal approach leverages the problem structure: we only need the topmost, bottommost, leftmost, and rightmost `*` cells. If we record the smallest and largest row indices and column indices where `*` appears, these four values immediately define the minimal bounding rectangle. This reduces the work to scanning each cell exactly once and outputting the subgrid defined by these boundaries. The key observation is that the minimal rectangle must align with the extreme coordinates of shaded cells, so there is no need to test other rectangles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm)^3) | O(nm) | Too slow |
| Optimal | O(nm) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Initialize variables to track the minimal and maximal rows (`top`, `bottom`) and columns (`left`, `right`) containing `*`. Set `top` and `left` to very large numbers, and `bottom` and `right` to -1.
2. Iterate through every cell `(i, j)` in the grid. When a cell contains `*`, update `top` to `min(top, i)`, `bottom` to `max(bottom, i)`, `left` to `min(left, j)`, and `right` to `max(right, j)`. This step identifies the extremes of the shaded area.
3. After scanning, `top` to `bottom` gives the row range and `left` to `right` gives the column range of the minimal rectangle containing all stars.
4. Iterate over rows `top` to `bottom` and for each row, print the substring from column `left` to `right`. This outputs the minimal rectangle with the original shading pattern intact.

Why it works: The algorithm maintains the invariant that `top`, `bottom`, `left`, and `right` always encompass all `*` seen so far. Once all cells have been scanned, the rectangle defined by these boundaries is the smallest possible, because any smaller rectangle would miss at least one `*`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

top, bottom = n, -1
left, right = m, -1

for i in range(n):
    for j in range(m):
        if grid[i][j] == '*':
            top = min(top, i)
            bottom = max(bottom, i)
            left = min(left, j)
            right = max(right, j)

for i in range(top, bottom + 1):
    print(grid[i][left:right + 1])
```

The code reads the grid, tracks extreme positions of shaded cells, and slices the grid accordingly. Using `strip()` ensures no newline characters interfere. Off-by-one errors are avoided by including both endpoints in slicing with `right + 1` and `bottom + 1`.

## Worked Examples

**Example 1**:

Input:

```
6 7
.......
..***..
..*....
..***..
..*....
..***..
```

Tracking variables:

| Row | '*' positions | top | bottom | left | right |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 6 | -1 | 7 | -1 |
| 1 | 2,3,4 | 1 | 1 | 2 | 4 |
| 2 | 2 | 1 | 2 | 2 | 4 |
| 3 | 2,3,4 | 1 | 3 | 2 | 4 |
| 4 | 2 | 1 | 4 | 2 | 4 |
| 5 | 2,3,4 | 1 | 5 | 2 | 4 |

Rectangle extracted: rows 1-5, columns 2-4

Output:

```
***
*..
***
*..
***
```

**Example 2 (single cell)**:

Input:

```
3 3
...
.*.
...
```

Tracking variables:

| Row | '*' positions | top | bottom | left | right |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |

Output:

```
*
```

This demonstrates that even a single shaded cell is correctly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | We scan every cell exactly once and slice rows only for output. |
| Space | O(nm) | The grid itself is stored; extra variables are O(1). |

Given `n, m ≤ 50`, `nm` is at most 2500, well within the 1-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    top, bottom = n, -1
    left, right = m, -1

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                top = min(top, i)
                bottom = max(bottom, i)
                left = min(left, j)
                right = max(right, j)

    for i in range(top, bottom + 1):
        print(grid[i][left:right + 1])

    return sys.stdout.getvalue().strip()

# Provided sample
assert run("6 7\n.......\n..***..\n..*....\n..***..\n..*....\n..***..") == "***\n*..\n***\n*..\n***", "sample 1"

# Single star
assert run("3 3\n...\n.*.\n...") == "*", "single star"

# Full rectangle
assert run("2 2\n**\n**") == "**\n**", "full 2x2 rectangle"

# Row-only rectangle
assert run("3 5\n.....\n*****\n.....") == "*****", "row only"

# Column-only rectangle
assert run("4 3\n.*.\n.*.\n.*.\n.*.") == "*\n*\n*\n*", "column only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3\n...\n.*.\n...` | `*` | single cell rectangle |
| `2 2\n**\n**` | `**\n**` | full small rectangle |
| `3 5\n.....\n*****\n.....` | `*****` | single row rectangle |
| `4 3\n.*.\n.*.\n.*.\n.*.` | `*\n*\n*\n*` | single column rectangle |

## Edge Cases

If all stars lie in a single row, `top` and `bottom` are equal. Our loop correctly prints just that row. Similarly, if all stars lie in a single column, `left` and `right` are equal, producing a single-column rectangle. If the star is in the corner of the grid, such as `(0,0)`, `min` and `max` logic still computes the correct bounding rectangle. This algorithm handles minimal and maximal inputs seamlessly.
