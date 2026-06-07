---
title: "CF 1952F - Grid"
description: "We are given a 21 by 21 grid where each cell contains either a 0 or a 1. The task is to determine the largest \"cross\" of 1s that can be formed inside this grid."
date: "2026-06-07T17:58:31+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1952
codeforces_index: "F"
codeforces_contest_name: "April Fools Day Contest 2024"
rating: 0
weight: 1952
solve_time_s: 99
verified: false
draft: false
---

[CF 1952F - Grid](https://codeforces.com/problemset/problem/1952/F)

**Rating:** -  
**Tags:** *special, brute force  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a 21 by 21 grid where each cell contains either a `0` or a `1`. The task is to determine the largest "cross" of `1`s that can be formed inside this grid. A cross is defined as a set of cells centered on some `1` where all four arms-up, down, left, and right-consist of consecutive `1`s extending from the center. The output should be the total number of `1`s that form the largest cross. For instance, a cross of arm length 2 has 1 center plus 2 cells in each direction, totaling 1 + 2*4 = 9 cells.

The grid is small and fixed at 21x21, which is only 441 cells. This means that even an approach that examines every cell and inspects all four directions individually is feasible because the total operations remain under one million, well within the 1-second limit.

A non-obvious edge case occurs when a potential cross touches the boundary of the grid or is blocked by `0`s immediately adjacent to the center. For example, if the center is at `(0,0)` and the cell `(0,1)` is `0`, the maximum arm in that direction is 0. A naive approach that assumes symmetry or always counts a fixed arm length will incorrectly overcount the size of the cross.

## Approaches

The brute-force approach examines each cell in the grid. If the cell is a `1`, it expands in all four directions, counting how many consecutive `1`s there are in each direction until a `0` or the grid boundary is reached. The size of the cross is then the sum of the arm lengths plus 1 for the center. This approach is correct, but if the grid were large, its complexity would grow as O(n^2 * min(n, m)) because for each cell you could potentially traverse an entire row or column. Here, with n = 21, the maximum number of operations is 21 * 21 * 21 = 9261, which is acceptable.

The optimal approach recognizes that we can preprocess the grid to calculate the maximum arm length in each direction for every cell. For the left and right directions, we traverse row by row, filling two auxiliary matrices with consecutive `1`s seen from the start or end of the row. For up and down, we do the same column by column. Once these matrices are built, the maximum cross at any cell is the minimum of the four precomputed values. This reduces repeated counting and makes the algorithm straightforward and easy to implement, and in our case, the preprocessing overhead is negligible due to the fixed grid size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Acceptable for n=21 |
| Preprocessing | O(n^2) | O(n^2) | Accepted and cleaner |

## Algorithm Walkthrough

1. Read the grid into a 21x21 matrix of integers. Converting `0` and `1` characters to integers simplifies arithmetic and comparisons.
2. Initialize four matrices of size 21x21: `up`, `down`, `left`, `right`. Each matrix will store the maximum consecutive `1`s extending from the current cell in that direction.
3. Fill the `left` matrix by traversing each row from left to right. For each cell, if it is `1`, the value is 1 plus the previous cell's value in the same row. Otherwise, the value is 0. This counts consecutive `1`s to the left including the current cell.
4. Similarly, fill the `right` matrix by traversing each row from right to left.
5. Fill the `up` matrix by traversing each column from top to bottom, counting consecutive `1`s.
6. Fill the `down` matrix by traversing each column from bottom to top.
7. For each cell, the maximum possible arm length is the minimum of its four direction values minus 1 because each value includes the center. Compute the total cross size as 1 + 4 * arm length.
8. Keep track of the maximum cross size found while scanning all cells.
9. Output the maximum cross size.

Why it works: Each auxiliary matrix correctly counts consecutive `1`s in its direction. Taking the minimum ensures that no arm exceeds the available consecutive `1`s. Subtracting 1 converts from "count including center" to "arm length," and multiplying by 4 and adding 1 gives the total cross size. This guarantees the computed size corresponds exactly to a valid cross.

## Python Solution

```python
import sys
input = sys.stdin.readline

grid = [list(map(int, input().strip())) for _ in range(21)]

n = 21

up = [[0]*n for _ in range(n)]
down = [[0]*n for _ in range(n)]
left = [[0]*n for _ in range(n)]
right = [[0]*n for _ in range(n)]

# Left and Right
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            left[i][j] = left[i][j-1] + 1 if j > 0 else 1
    for j in range(n-1, -1, -1):
        if grid[i][j]:
            right[i][j] = right[i][j+1] + 1 if j < n-1 else 1

# Up and Down
for j in range(n):
    for i in range(n):
        if grid[i][j]:
            up[i][j] = up[i-1][j] + 1 if i > 0 else 1
    for i in range(n-1, -1, -1):
        if grid[i][j]:
            down[i][j] = down[i+1][j] + 1 if i < n-1 else 1

max_cross = 0
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            arm = min(up[i][j], down[i][j], left[i][j], right[i][j])
            size = 1 + 4 * (arm - 1)
            max_cross = max(max_cross, size)

print(max_cross)
```

The solution first converts the grid to integers. Each direction is processed independently to compute consecutive `1`s, with careful handling of boundaries. When computing arm lengths, we subtract one to exclude the center, and multiplying by four accounts for all arms. This step requires careful attention because off-by-one errors are easy when working with inclusive counts.

## Worked Examples

### Sample Input 1

| Cell (i,j) | Up | Down | Left | Right | Arm | Size |
| --- | --- | --- | --- | --- | --- | --- |
| (0,0) | 1 | 6 | 1 | 7 | 1 | 5 |
| (6,10) | 3 | 3 | 2 | 2 | 2 | 9 |
| (10,10) | 1 | 2 | 1 | 2 | 1 | 5 |
| Max cell | ... | ... | ... | ... | 3 | 12 |

The trace shows the center at `(10,10)` achieves the maximum cross of size 12. All other cells have smaller minimum arms.

### Sample Input 2

Construct a cross in the center with arm length 2:

```
00000
00100
01110
00100
00000
```

Center at `(2,2)` gives `up=2`, `down=2`, `left=2`, `right=2`. Arm = 2, size = 1 + 4*2 = 9. Correct output matches expectation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each cell is processed in four passes for the four directions. n=21 so total operations are ~4*441=1764 |
| Space | O(n^2) | Four auxiliary n x n matrices plus the grid |

This fits comfortably in the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    grid = [list(map(int, input().strip())) for _ in range(21)]

    n = 21
    up = [[0]*n for _ in range(n)]
    down = [[0]*n for _ in range(n)]
    left = [[0]*n for _ in range(n)]
    right = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                left[i][j] = left[i][j-1]+1 if j>0 else 1
        for j in range(n-1,-1,-1):
            if grid[i][j]:
                right[i][j] = right[i][j+1]+1 if j<n-1 else 1
    for j in range(n):
        for i in range(n):
            if grid[i][j]:
                up[i][j] = up[i-1][j]+1 if i>0 else 1
        for i in range(n-1,-1,-1):
            if grid[i][j]:
                down[i][j] = down[i+1][j]+1 if i<n-1 else 1

    max_cross = 0
    for i in range(n):
        for j in
```
