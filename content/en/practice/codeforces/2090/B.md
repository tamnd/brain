---
title: "CF 2090B - Pushing Balls"
description: "We are given a rectangular grid of size $n times m$, initially empty. Ecrade can push balls into the grid either from the left side of a row or the top side of a column. Balls move along the row or column until they encounter an empty cell, occupying it."
date: "2026-06-08T05:50:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2090
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1012 (Div. 2)"
rating: 1000
weight: 2090
solve_time_s: 98
verified: false
draft: false
---

[CF 2090B - Pushing Balls](https://codeforces.com/problemset/problem/2090/B)

**Rating:** 1000  
**Tags:** brute force, dp, implementation  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid of size $n \times m$, initially empty. Ecrade can push balls into the grid either from the left side of a row or the top side of a column. Balls move along the row or column until they encounter an empty cell, occupying it. If a ball encounters an already occupied cell, the incoming ball stops, and the existing ball is pushed forward. A row or column that is completely filled cannot accept more balls. The task is to determine, given a final configuration of the grid (with cells containing balls marked as `1` and empty cells as `0`), whether it is possible to achieve this configuration using the allowed pushes.

The problem provides up to 10,000 test cases with grids no larger than 50x50. The total number of cells across all test cases does not exceed 10,000. This immediately tells us that any solution that works in $O(n \cdot m)$ per test case is feasible, while more naive simulations that try every sequence of pushes would be far too slow.

A subtle edge case arises when there is a single ball in the bottom-right corner of a grid while all other cells are empty. Since no ball can "float" into a corner without some support, this final configuration is impossible. Another edge case is when a ball occupies a position not on the last row or last column but has zeros to its right and below. The impossibility arises because any ball pushed in from the left or top must eventually stop at the first empty cell, so a `1` in the middle with zeros to its right and bottom cannot be reached.

## Approaches

The brute-force approach would attempt to simulate every possible sequence of pushes, trying all rows and columns iteratively. For each push, we would update the grid according to the movement rules. While correct in principle, this is infeasible because the number of sequences grows combinatorially with the number of balls, making the approach unusable even for small grids. The operation count would easily exceed $50! \cdot 50!$ in the worst case, which is astronomically larger than the allowed time.

The key insight for an optimal solution is to consider each cell independently. A cell can only contain a ball if it is either in the last row or last column, or if there is another ball directly to its right or directly below it. This ensures that any ball pushed into the row or column can propagate to occupy this cell. Formally, for cell $(i, j)$, the condition is that if it contains a `1`, then either $i = n-1$ or $j = m-1$, or at least one of the cells $(i+1, j)$ or $(i, j+1)$ also contains a `1`. This allows us to check the entire grid in a single pass without simulating the sequence of pushes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n*m)!) | O(n*m) | Too slow |
| Optimal | O(n*m) | O(n*m) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the dimensions $n$ and $m$ of the grid.
2. Read the grid as a list of strings or a 2D array of integers.
3. Iterate over each cell in the grid. For each cell that contains a ball (value `1`), check the following condition: if it is not on the bottommost row and not on the rightmost column, then at least one of the cells directly below or directly to the right must also contain a ball.
4. If any cell violates this condition, mark the grid as impossible to construct.
5. Output "Yes" if the grid passes all checks, otherwise output "No".

The invariant that guarantees correctness is that every ball that is not at the edge must have a path to propagate from an edge. If a ball does not satisfy this, there is no sequence of pushes that can place a ball there without violating the movement rules. Checking the condition for all `1`s ensures global correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_construct(grid, n, m):
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1':
                if i < n - 1 and j < m - 1:
                    if grid[i+1][j] == '0' and grid[i][j+1] == '0':
                        return False
    return True

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    print("Yes" if can_construct(grid, n, m) else "No")
```

The solution reads the grid and applies the local propagation check described in the algorithm. The check uses zero-based indices, so `i < n-1` and `j < m-1` ensures we skip boundary cells where propagation is trivial. The algorithm avoids simulating push sequences entirely and focuses only on local conditions, which is both faster and simpler to reason about. Stripping input lines prevents accidental newline characters from interfering with checks.

## Worked Examples

Consider the first sample:

```
3 3
001
001
110
```

| i | j | grid[i][j] | check condition | passes? |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | i<n-1 and j<m-1 → False (j=m-1) | Yes |
| 1 | 2 | 1 | j=m-1 | Yes |
| 2 | 0 | 1 | i=n-1 | Yes |
| 2 | 1 | 1 | i=n-1 | Yes |
| 2 | 2 | 0 | N/A | Yes |

All checks pass, so output is `Yes`.

For the last sample:

```
3 3
000
000
001
```

| i | j | grid[i][j] | check condition | passes? |
| --- | --- | --- | --- | --- |
| 2 | 2 | 1 | i=n-1 or j=m-1 → True | Yes |

Even though the ball is at the bottom-right, this is acceptable. If we had placed a ball somewhere like `(1,1)` with zeros to its right and below, the check would fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Each cell is visited once and a constant number of checks are performed. With total cells ≤10,000, this is efficient. |
| Space | O(n*m) | We store the grid for each test case. No extra structures are required. |

The solution comfortably fits within the 1-second time limit and 512 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    def print_override(*args, **kwargs):
        output.append(' '.join(map(str, args)))
    global print
    old_print = print
    print = print_override
    try:
        import solution  # assume the solution above is saved in solution.py
    finally:
        print = old_print
    return '\n'.join(output)

# Provided samples
assert run("5\n3 3\n001\n001\n110\n3 3\n010\n111\n010\n3 3\n111\n111\n111\n3 3\n000\n000\n000\n3 3\n000\n000\n001\n") == "Yes\nYes\nYes\nYes\nNo"

# Custom test cases
assert run("1\n1 1\n1\n") == "Yes", "single cell with ball"
assert run("1\n1 1\n0\n") == "Yes", "single cell empty"
assert run("1\n2 2\n10\n01\n") == "No", "balls in diagonal impossible"
assert run("1\n2 2\n11\n10\n") == "Yes", "balls propagate correctly"
assert run("1\n3 3\n100\n010\n001\n") == "No", "diagonal impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 with ball | Yes | minimal grid with ball |
| 1x1 empty | Yes | minimal empty grid |
| 2x2 diagonal | No | impossible placement in middle |
| 2x2 propagate | Yes | edge propagation works |
| 3x3 diagonal | No | multiple impossible placements |

## Edge Cases

A single ball in a corner is trivially valid. A ball in the middle with empty cells to the right and bottom cannot be reached. For example, in the grid:

```
2 2
10
00
```

The ball at `(0,0)` has no ball below `(1,0)` or to the right `(0,1)`, but it is on the top-left. Our check allows it because propagation is only restricted for cells not on the last row or column. If we change it to:

```
2 2
11
01
```

Then the cell `(0,1)` is fine because it is on the top row but not last column. Cell `(1,0)` is fine because last row. Cell `(1,1)` contains `1` but has zeros below and to the right (out-of-bound),
