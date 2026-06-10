---
title: "CF 1505E - Cakewalk"
description: "We are given a small rectangular cake divided into a grid of squares. Each square either has a berry or is empty. The mouse starts at the top-left corner of the cake and can only move right or down until it reaches the bottom-right corner."
date: "2026-06-10T20:30:42+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1505
codeforces_index: "E"
codeforces_contest_name: "April Fools Day Contest 2021"
rating: 1800
weight: 1505
solve_time_s: 123
verified: true
draft: false
---

[CF 1505E - Cakewalk](https://codeforces.com/problemset/problem/1505/E)

**Rating:** 1800  
**Tags:** *special, greedy, implementation, shortest paths  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small rectangular cake divided into a grid of squares. Each square either has a berry or is empty. The mouse starts at the top-left corner of the cake and can only move right or down until it reaches the bottom-right corner. The goal is to compute how many berries the mouse will eat along the path she chooses if she is trying to maximize her berry intake.

The input represents the cake as an `H × W` grid of characters, where `H` is the number of rows and `W` is the number of columns. Each cell contains either `'*'` for a berry or `'.'` for empty. The output is a single integer, the maximum number of berries that can be collected along a valid path from the top-left to bottom-right corner.

The constraints are very tight: `H` and `W` are at most 5. This small size allows us to consider approaches that would be too slow for large grids. In particular, even brute-force enumeration of all paths from the top-left to bottom-right is feasible because the total number of paths is at most `C(H+W-2, H-1)`, which is at most `C(8,4) = 70`.

Non-obvious edge cases arise when the path is constrained by the edges of the grid or when berries are clustered along certain rows or columns. For instance, if the top row is empty and all berries are in the bottom row, a careless greedy approach that always prefers berries immediately visible could select the wrong path. Another edge case occurs when the grid is `1×N` or `N×1`, where the mouse has only one possible path. A correct solution must handle these small dimensions without errors.

## Approaches

A naive brute-force approach would enumerate all valid paths from the top-left to the bottom-right corner. For each path, we would count the number of berries collected and return the maximum. This approach works because the number of paths is combinatorially bounded by `(H+W-2 choose H-1)`. In the worst case of a 5×5 grid, this is `C(8,4) = 70` paths, and each path takes `O(H+W)` steps to evaluate, giving a total of at most 560 operations. While feasible here, this approach does not generalize to larger grids and is tedious to implement correctly.

A more elegant and general approach uses dynamic programming. We define `dp[i][j]` as the maximum number of berries that can be collected from the top-left corner `(0,0)` to cell `(i,j)`. The key insight is that to reach cell `(i,j)`, the mouse must come either from the cell above `(i-1,j)` or from the cell to the left `(i,j-1)`. Thus the recurrence relation is `dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + (1 if cell (i,j) has a berry else 0)`. This reduces the problem to filling a simple `H×W` table, which is straightforward and ensures correctness. The brute-force idea works because it examines all paths, but dynamic programming leverages overlapping subproblems to compute the same result more efficiently and cleanly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(H+W-2, H-1)·(H+W)) | O(H+W) | Feasible here but verbose |
| Dynamic Programming | O(H·W) | O(H·W) | Accepted |

## Algorithm Walkthrough

1. Read the height `H` and width `W`, and store the cake grid as a list of strings.
2. Initialize a `dp` table of size `H×W`, where `dp[i][j]` will store the maximum berries collected to reach cell `(i,j)`.
3. Iterate over all cells `(i,j)` in row-major order. For each cell, determine the best way to reach it:

- If `i > 0`, consider `dp[i-1][j]` as the number of berries collected from the cell above.
- If `j > 0`, consider `dp[i][j-1]` as the number of berries collected from the cell to the left.
- Take the maximum of these two values. If `(i,j)` has a berry, add 1.
- Special case: the top-left cell `(0,0)` has no above or left neighbor, so `dp[0][0]` is 1 if it has a berry, 0 otherwise.
4. After filling the table, the value at `dp[H-1][W-1]` is the maximum berries the mouse can collect along a valid path.

The reason this works is that `dp[i][j]` always correctly represents the optimal solution up to cell `(i,j)`. Since the mouse can only move right or down, any path to `(i,j)` must come from either the left or above. By taking the maximum of the two possibilities at each step and adding the current cell's berry if present, we ensure that we never underestimate the optimal path. This invariant holds for the whole grid.

## Python Solution

```python
import sys
input = sys.stdin.readline

H, W = map(int, input().split())
cake = [input().strip() for _ in range(H)]

dp = [[0] * W for _ in range(H)]

for i in range(H):
    for j in range(W):
        best_from_above = dp[i-1][j] if i > 0 else 0
        best_from_left = dp[i][j-1] if j > 0 else 0
        dp[i][j] = max(best_from_above, best_from_left) + (1 if cake[i][j] == '*' else 0)

print(dp[H-1][W-1])
```

The code initializes the DP table and iterates in row-major order to fill each cell with the maximum berries collectible. We handle boundaries by checking if `i > 0` and `j > 0`. The final cell contains the answer. Using `strip()` ensures that trailing newline characters from input do not affect cell content comparison.

## Worked Examples

Sample 1:

Input:

```
4 3
*..
.*.
..*
...
```

DP table state during iteration:

| i | j | cake[i][j] | dp[i][j] | Explanation |
| --- | --- | --- | --- | --- |
| 0 | 0 | * | 1 | Starting cell, has berry |
| 0 | 1 | . | 1 | From left 1, no berry |
| 0 | 2 | . | 1 | From left 1, no berry |
| 1 | 0 | . | 1 | From above 1, no berry |
| 1 | 1 | * | 2 | max(1 from above, 1 from left) +1 berry |
| 1 | 2 | . | 2 | max(1 from above, 2 from left), no berry |
| 2 | 0 | . | 1 | from above 1, no berry |
| 2 | 1 | . | 2 | max(2 from above,1 from left), no berry |
| 2 | 2 | * | 3 | max(2,2)+1 berry |
| 3 | 0 | . | 1 | from above 1, no berry |
| 3 | 1 | . | 2 | max(2 from above,1 from left) |
| 3 | 2 | . | 3 | max(3 from above,2 from left) |

Final answer: 3

Sample 2: 1×1 grid with no berry:

Input:

```
1 1
.
```

DP table:

| 0 | 0 | . | 0 |

Answer: 0

This shows the algorithm handles single-cell grids and correctly initializes the top-left cell.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(H·W) | Each cell is visited once, and each computation is O(1) |
| Space | O(H·W) | We store one DP table of size H×W |

With H,W ≤ 5, this is negligible and completes well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    H, W = map(int, input().split())
    cake = [input().strip() for _ in range(H)]
    dp = [[0]*W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            best_from_above = dp[i-1][j] if i > 0 else 0
            best_from_left = dp[i][j-1] if j > 0 else 0
            dp[i][j] = max(best_from_above, best_from_left) + (1 if cake[i][j] == '*' else 0)
    return str(dp[H-1][W-1])

# provided sample
assert run("4 3\n*..\n.*.\n..*\n...\n") == "3", "sample 1"

# custom cases
assert run("1 1\n.\n") == "0", "single cell empty"
assert run("1 1\n*\n") == "1", "single cell with berry"
assert run("5 5\n
```
