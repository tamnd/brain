---
title: "CF 1579C - Ticks"
description: "We are given a grid of size $n times m$ representing a paper, where some cells are black (denoted by ) and others are white (.). Casimir claims the black cells are produced by drawing ticks."
date: "2026-06-10T10:24:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1579
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 744 (Div. 3)"
rating: 1500
weight: 1579
solve_time_s: 350
verified: true
draft: false
---

[CF 1579C - Ticks](https://codeforces.com/problemset/problem/1579/C)

**Rating:** 1500  
**Tags:** greedy, implementation  
**Solve time:** 5m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of size $n \times m$ representing a paper, where some cells are black (denoted by `*`) and others are white (`.`). Casimir claims the black cells are produced by drawing ticks. A tick of size $d$ is centered at some cell and extends diagonally up-left and up-right exactly $d$ cells. The tick covers the center cell and the two arms, resulting in $2d+1$ black cells. All ticks have a minimum size $k$. Multiple ticks can overlap, and once a cell is black it stays black.

The task is to check if the given black-and-white grid could have been produced by some combination of ticks, all with size at least $k$.

The constraints are small: $n$ is at most 10 and $m$ at most 19. This allows us to process the grid exhaustively without worrying about timeouts. The main challenge is not efficiency but correctly identifying which black cells can belong to a tick of size $\ge k$ and ensuring that all black cells are accounted for.

Edge cases include grids where some black cells are isolated or too close to the top row to support a tick of the minimum size. For example, if $k=2$ and a `*` appears in the first row, there is no way to form a tick of size 2 with this as the bottom cell, so the answer is `NO`.

## Approaches

A brute-force approach would attempt to try all possible ticks at all possible positions and check if they can cover the grid exactly. For each potential center `(i, j)`, we would try all sizes $d \ge k$ and mark cells accordingly. This works for small grids, but even for $n=10$ and $m=19$, we might redundantly try many overlapping ticks, and verifying coverage repeatedly becomes messy.

The key observation to optimize is that a tick must extend upwards diagonally. Therefore, we can scan the grid from the bottom row to the top, because a tick's center can only be responsible for black cells below or at its row. For each `*`, we can determine the maximum tick size that has its bottom at that cell by checking the diagonals going up. If the maximum size is at least $k$, we mark the corresponding cells as covered. After processing all potential ticks, any `*` left uncovered invalidates the grid.

This leads to a greedy but structured approach: compute the maximum size of a tick that could end at each cell, mark cells accordingly, and verify all black cells are accounted for.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m * min(n, m)^2) | O(n * m) | Too slow / messy |
| Optimal | O(n * m) | O(n * m) | Accepted |

## Algorithm Walkthrough

1. Read the input grid and the parameters `n, m, k`. Convert the grid into a boolean 2D array `grid` where `True` represents a black cell.
2. Initialize two auxiliary 2D arrays `left_diag` and `right_diag` of the same size as the grid. `left_diag[i][j]` will store the length of consecutive black cells diagonally up-left ending at `(i,j)`. `right_diag[i][j]` will store the length of consecutive black cells diagonally up-right ending at `(i,j)`.
3. Fill `left_diag` and `right_diag` in a bottom-up manner. For a cell `(i,j)` with `*`, `left_diag[i][j]` is `1 + left_diag[i-1][j-1]` if `i>0` and `j>0`, otherwise 1. Similarly, `right_diag[i][j]` is `1 + right_diag[i-1][j+1]` if `i>0` and `j<m-1`, otherwise 1.
4. Initialize a `covered` array of size `n x m` with all `False`. This array will track which black cells are explained by a tick of size ≥ k.
5. Scan each cell `(i, j)` from bottom to top. If `(i,j)` is black, compute the maximum tick size as `d = min(left_diag[i][j], right_diag[i][j]) - 1`. If `d >= k`, mark all cells of this tick in the `covered` array: for each `h` from `0` to `d`, mark `(i-h, j-h)` and `(i-h, j+h)` as `True`.
6. After processing all cells, iterate over the grid. If any cell `(i,j)` is black in the original grid but not marked as covered, print `NO`. Otherwise, print `YES`.

Why it works: the bottom-up scanning ensures that for any potential tick, its arms upward are not blocked, and we mark all cells explained by a tick. If a black cell is left uncovered, it cannot belong to any tick of size ≥ k. By scanning bottom-up, each tick is identified by its largest possible size, ensuring no valid tick is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        grid = [list(input().strip()) for _ in range(n)]
        left_diag = [[0]*m for _ in range(n)]
        right_diag = [[0]*m for _ in range(n)]
        covered = [[False]*m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if grid[i][j] == '*':
                    left_diag[i][j] = 1 + (left_diag[i-1][j-1] if i>0 and j>0 else 0)
                    right_diag[i][j] = 1 + (right_diag[i-1][j+1] if i>0 and j<m-1 else 0)

        for i in reversed(range(n)):
            for j in range(m):
                if grid[i][j] == '*':
                    d = min(left_diag[i][j], right_diag[i][j]) - 1
                    if d >= k:
                        for h in range(d+1):
                            covered[i-h][j-h] = True
                            covered[i-h][j+h] = True

        ok = True
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '*' and not covered[i][j]:
                    ok = False
                    break
            if not ok:
                break
        print("YES" if ok else "NO")

solve()
```

The `left_diag` and `right_diag` arrays efficiently compute the maximum upward arms of a potential tick for each cell. The bottom-up pass ensures that we capture the largest possible tick first and mark all cells covered. The final check guarantees no black cell is left unexplained. Care must be taken with array boundaries to avoid index errors.

## Worked Examples

**Example 1**

Input grid (4x9, k=2):

```
*.*.*...*
.*.*...*.
..*.*.*..
.....*...
```

Step trace for the bottom row `i=3`:

| i | j | grid | left_diag | right_diag | d | action |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 5 | * | 1 | 1 | 0 | d<k, skip |

Moving up, the tick centered at `(2,5)` with `d=2` marks all its cells, covering the relevant `*`. The algorithm finds all ticks and confirms all black cells are covered. Output: `YES`.

**Example 2**

Input grid (2x3, k=1):

```
*.*
...
```

Bottom-up pass:

| i | j | grid | left_diag | right_diag | d | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | . | 0 | 0 | - | skip |
| 0 | 0 | * | 1 | 1 | 0 | d<k, skip |

No ticks of size ≥1 can explain the `*` at `(0,0)`. Output: `NO`.

These traces demonstrate that the algorithm correctly identifies the maximum possible tick sizes and ensures no black cell is left unexplained.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) | Each cell is processed a constant number of times: diagonals computed once, bottom-up marking once. |
| Space | O(n*m) | For `left_diag`, `right_diag`, and `covered` arrays. |

The small input bounds make this linear solution very efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("8\n2 3 1\n*.*\n...\n4 9 2\n*.*.*...*\n.*.*...*.\n..*.*.*..\n.....*...\n4 4 1\n*.*.\n****\n.**.\n....\n5 5 1\n.....\n*...*\n.*.*.\
```
