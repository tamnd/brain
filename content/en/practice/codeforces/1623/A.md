---
title: "CF 1623A - Robot Cleaner"
description: "We have a robot moving inside a rectangular room with $n$ rows and $m$ columns. The robot starts at some cell $(rb, cb)$ and moves diagonally: one step down and one step right at a time."
date: "2026-06-10T05:40:48+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1623
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 763 (Div. 2)"
rating: 800
weight: 1623
solve_time_s: 84
verified: true
draft: false
---

[CF 1623A - Robot Cleaner](https://codeforces.com/problemset/problem/1623/A)

**Rating:** 800  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a robot moving inside a rectangular room with $n$ rows and $m$ columns. The robot starts at some cell $(r_b, c_b)$ and moves diagonally: one step down and one step right at a time. The room has walls, so whenever the robot would move past a boundary, it "bounces" off it, reversing its direction along that axis. In addition to moving, the robot cleans all cells in its current row and column every second. The goal is to determine how long it takes for the robot to clean a single dirty cell at $(r_d, c_d)$.

The input gives multiple test cases, each specifying the room size, the robot's starting location, and the dirty cell location. The output is the time, in seconds, when the robot first cleans the dirty cell.

The constraints are small: $n, m \le 100$ and up to $10^4$ test cases. This means we can simulate the robot's movement step by step, because even in the worst case, each test case will involve at most about 200 steps before the robot revisits a previous position and direction. Large-scale optimizations are unnecessary; correctness and careful handling of boundaries are more important.

Edge cases to watch for include situations where the robot starts in the same row or column as the dirty cell, which should yield time zero. Another subtle case is when the dirty cell is in a corner, which might coincide with multiple direction reversals in a single simulation step if boundaries are handled carelessly.

## Approaches

The brute-force approach is to simulate each second of the robot's movement, updating the row and column according to the current direction, reflecting off walls when necessary, and checking whether the current row or column matches the dirty cell. This works because $n$ and $m$ are small. For each test case, the robot will never need more than $2(n-1) + 2(m-1)$ steps to reach the dirty cell along its diagonal pattern. Therefore the brute-force approach is acceptable here.

A key insight is that we do not need to track the entire path of the robot, only its position and movement direction. Each step is deterministic, and the robot cleans the entire row and column at its current position, so we simply need to check whether the current row or column matches the dirty cell. The reflection logic is straightforward: if the next row would exceed the room limits, we flip the vertical direction; if the next column would exceed the room limits, we flip the horizontal direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n + m) per test case | O(1) | Accepted |
| Optimal (simulation with reflection) | O(n + m) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Loop over each test case.
2. For each test case, read the room dimensions $n$ and $m$, the robot's initial position $(r_b, c_b)$, and the dirty cell $(r_d, c_d)$.
3. Initialize the robot's movement direction to $(dr, dc) = (1, 1)$.
4. Initialize a timer variable `time = 0`.
5. Loop while the robot has not cleaned the dirty cell:

1. Check if the robot's current row `r_b` equals `r_d` or its current column `c_b` equals `c_d`. If so, break the loop because the dirty cell is cleaned.
2. Compute the next row `next_r = r_b + dr` and next column `next_c = c_b + dc`.
3. If `next_r` would exceed the room boundaries (less than 1 or greater than $n$), reverse `dr` and recompute `next_r`.
4. If `next_c` would exceed the room boundaries (less than 1 or greater than $m$), reverse `dc` and recompute `next_c`.
5. Update the robot's position to `(r_b, c_b) = (next_r, next_c)`.
6. Increment `time` by one.
6. Output the `time` for the current test case.

Why it works: at each step, the robot either moves diagonally or reflects off a wall, which guarantees that it eventually reaches a row or column that intersects the dirty cell. Since the room is finite and the movement is periodic, the robot cannot enter an infinite loop without cleaning the dirty cell. Each second corresponds exactly to a movement step, so the timer tracks the number of seconds until cleaning.

## Python Solution

```python
import sys
input = sys.stdin.readline

def robot_cleaner():
    t = int(input())
    for _ in range(t):
        n, m, r_b, c_b, r_d, c_d = map(int, input().split())
        dr, dc = 1, 1
        time = 0
        while r_b != r_d and c_b != c_d:
            if r_b + dr < 1 or r_b + dr > n:
                dr = -dr
            if c_b + dc < 1 or c_b + dc > m:
                dc = -dc
            r_b += dr
            c_b += dc
            time += 1
        print(time)

robot_cleaner()
```

In the solution, `dr` and `dc` track the vertical and horizontal directions. The order of operations ensures that direction is flipped before moving if the robot would cross a wall. The while loop checks whether the robot has already cleaned the dirty cell before moving. This avoids off-by-one errors in counting the seconds.

## Worked Examples

Trace Sample 1: `10 10 6 1 2 8`

| time | r_b | c_b | dr | dc | cleaned? |
| --- | --- | --- | --- | --- | --- |
| 0 | 6 | 1 | 1 | 1 | No |
| 1 | 7 | 2 | 1 | 1 | No |
| 2 | 8 | 3 | 1 | 1 | No |
| 3 | 9 | 4 | 1 | 1 | No |
| 4 | 10 | 5 | 1 | 1 | No |
| 5 | 9 | 6 | -1 | 1 | No |
| 6 | 8 | 7 | -1 | 1 | No |
| 7 | 7 | 8 | -1 | 1 | Yes |

The dirty cell is cleaned at time 7, which matches the expected output.

Trace Sample 2: `2 2 1 1 2 1`

| time | r_b | c_b | dr | dc | cleaned? |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | Yes |

The robot starts in the same column as the dirty cell, so the dirty cell is cleaned immediately at time 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Each step moves the robot diagonally and the robot will hit every row and column at most once before cleaning the dirty cell. |
| Space | O(1) | Only a few integers are stored per test case; no extra memory proportional to $n$ or $m$ is needed. |

The total complexity across all test cases is acceptable because $t \le 10^4$ and $n, m \le 100$, resulting in at most 2 million iterations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    robot_cleaner()
    return output.getvalue().strip()

# provided samples
assert run("5\n10 10 6 1 2 8\n10 10 9 9 1 1\n9 8 5 6 2 1\n6 9 2 2 5 8\n2 2 1 1 2 1\n") == "7\n10\n9\n3\n0", "sample 1"

# custom cases
assert run("1\n1 1 1 1 1 1\n") == "0", "single cell room"
assert run("1\n5 5 3 3 3 5\n") == "0", "same row as dirty cell"
assert run("1\n5 5 3 3 5 3\n") == "0", "same column as dirty cell"
assert run("1\n5 5 1 1 5 5\n") == "4", "opposite corner"
assert run("1\n5 5 5 5 1 1\n") == "4", "other corner diagonal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 1 1 | 0 | Minimum-size room |
| 5 5 3 3 3 5 | 0 | Robot starts in the same row as dirty cell |
| 5 5 |  |  |
