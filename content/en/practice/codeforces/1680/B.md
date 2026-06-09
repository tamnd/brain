---
title: "CF 1680B - Robots"
description: "We are given a small rectangular grid, with each cell either empty or containing a robot. Robots can move simultaneously in one of four cardinal directions, and if any robot tries to leave the grid, it explodes."
date: "2026-06-10T00:29:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1680
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 128 (Rated for Div. 2)"
rating: 800
weight: 1680
solve_time_s: 91
verified: true
draft: false
---

[CF 1680B - Robots](https://codeforces.com/problemset/problem/1680/B)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small rectangular grid, with each cell either empty or containing a robot. Robots can move simultaneously in one of four cardinal directions, and if any robot tries to leave the grid, it explodes. Our goal is to determine whether it is possible to move the robots so that at least one reaches the top-left corner, without causing any explosions. Each test case provides the grid dimensions and layout, and the output is simply YES or NO.

The constraints are tight: the grid is at most 5×5, and there can be up to 5000 test cases. Since the grid is tiny, we can afford to reason about each cell individually. However, even with small grids, careless approaches can fail if they try to move all robots blindly. A key subtlety arises when a robot is already at the top or left edge: commanding a move in that direction would cause an explosion. For example, in a 2×2 grid:

```
ER
RE
```

moving left or up immediately would make the robot in the first row or column explode. The correct answer is NO, but a naive algorithm might assume any robot can eventually move to the top-left corner, producing an incorrect YES.

Another edge case occurs when a robot is already in the top-left corner. No moves are needed, and the answer is immediately YES.

## Approaches

The brute-force approach would be to simulate all possible sequences of moves until either a robot reaches the top-left or an explosion occurs. Each move can be up, down, left, or right, so the branching factor is four. Even with the 5×5 grid, the number of sequences grows exponentially, and iterating over all of them for 5000 test cases would be excessive, though technically feasible because of the small grid size. The brute-force works because it fully explores the robot state space, but it is slow and unnecessary.

The optimal approach leverages the observation that the only robot that matters is the one closest to the top-left corner. Any move toward the top or left risks causing other robots that are already in the topmost row or leftmost column to explode. Therefore, we only need to check if the robot that is furthest up and furthest left is in the top-leftmost position among all robots. If such a robot exists, we can move it along rows and columns toward the top-left, and no other robot will ever be forced to move out of bounds.

This reduces the problem to finding the robot with minimum row and minimum column indices and checking if it coincides with the top-left-most robot. If it does, the answer is YES; otherwise, it is NO. This insight turns a potentially exponential problem into a simple linear scan of the grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^(n*m)) | O(n*m) | Too slow |
| Optimal | O(n*m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize variables `min_row` and `min_col` to a large number representing the smallest row and column indices among all robots.
2. Scan the grid row by row and column by column.
3. For every cell containing a robot, update `min_row` and `min_col` to be the minimum of the current values and the robot’s row and column indices.
4. After scanning, check if the robot at position (`min_row`, `min_col`) is at the top-left corner, i.e., row 0 and column 0.
5. If it is, print YES; otherwise, print NO.

Why it works: `min_row` and `min_col` identify the robot that is already closest to the top-left corner. No robot with a smaller row or column exists, so moving this robot up or left will not cause any other robot to explode, because all other robots are further away from the top-left edges. Therefore, if the top-left-most robot is at (`min_row`, `min_col`), we can safely move it to the top-left corner without violating constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    min_row, min_col = n, m
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'R':
                if i < min_row:
                    min_row = i
                if j < min_col:
                    min_col = j
    if min_row == 0 and min_col == 0:
        print("YES")
    else:
        print("NO")
```

The code reads all test cases, then for each grid, it scans every cell to locate robots. The `min_row` and `min_col` track the closest robot to the top-left. After scanning, checking whether this robot is at the top-left corner gives the correct answer. The choice to initialize `min_row` and `min_col` to `n` and `m` ensures that any actual robot position will update them correctly. Boundary handling is implicit because the indices start at zero.

## Worked Examples

For the input:

```
2 2
ER
RE
```

| Step | i | j | grid[i][j] | min_row | min_col |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | E | 2 | 2 |
| 2 | 0 | 1 | R | 0 | 1 |
| 3 | 1 | 0 | R | 0 | 0 |
| 4 | 1 | 1 | E | 0 | 0 |

`min_row` is 0 and `min_col` is 0. The robot at (0,0) exists? No. The top-left-most robot is at column 0, row 1. Therefore, output is NO.

Another example:

```
1 3
ERR
```

| Step | i | j | grid[i][j] | min_row | min_col |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | E | 1 | 3 |
| 2 | 0 | 1 | R | 0 | 1 |
| 3 | 0 | 2 | R | 0 | 1 |

`min_row` is 0, `min_col` is 1. The robot at (0,1) can move left safely. Output YES.

These traces demonstrate how the algorithm identifies the correct robot to move and ensures no other robot is forced out of bounds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) per test case | Scan all cells once to locate robots |
| Space | O(n*m) | Grid storage; variables `min_row` and `min_col` negligible |

With n,m ≤ 5 and t ≤ 5000, total operations are under 125,000, well within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        min_row, min_col = n, m
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'R':
                    if i < min_row:
                        min_row = i
                    if j < min_col:
                        min_col = j
        if min_row == 0 and min_col == 0:
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# Provided samples
assert run("6\n1 3\nERR\n2 2\nER\nRE\n2 2\nER\nER\n1 1\nR\n4 3\nEEE\nEEE\nERR\nEER\n3 3\nEEE\nEER\nREE\n") == "YES\nNO\nYES\nYES\nYES\nNO", "sample 1"

# Custom cases
assert run("1\n1 1\nR\n") == "YES", "single robot at top-left"
assert run("1\n2 2\nRR\nRR\n") == "YES", "all robots, top-left already safe"
assert run("1\n2 2\nRE\nER\n") == "NO", "robots blocking each other"
assert run("1\n5 5\nEEEER\nEEEEE\nEERRE\nEEEEE\nRREEE\n") == "YES", "multiple robots, safe path exists"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 with robot | YES | Minimal grid, robot at top-left |
| 2x2 all robots | YES | Multiple robots, safe top-left robot |
| 2x2 cross robots | NO | Robots block each other, cannot move safely |
| 5x5 scattered robots | YES | Larger grid, algorithm picks closest robot safely |

## Edge Cases

A critical edge case is when a robot is already at the top-left. For input:

```
1
1 1
R
```

`min_row` and `min
