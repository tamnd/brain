---
title: "CF 321A - Ciel and Robot"
description: "We are asked to determine whether a robot moving on a 2D plane can reach a target point (a, b). The robot starts at the origin (0, 0) and follows a sequence of moves encoded in a string."
date: "2026-06-06T02:19:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 321
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 190 (Div. 1)"
rating: 1700
weight: 321
solve_time_s: 68
verified: true
draft: false
---

[CF 321A - Ciel and Robot](https://codeforces.com/problemset/problem/321/A)

**Rating:** 1700  
**Tags:** binary search, implementation, math  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a robot moving on a 2D plane can reach a target point (_a_, _b_). The robot starts at the origin (0, 0) and follows a sequence of moves encoded in a string. Each character of the string represents a direction: 'U' moves the robot up, 'D' down, 'L' left, and 'R' right. Once the robot finishes the string, it repeats it infinitely. The question is whether at some moment in this infinite sequence, the robot will occupy the target coordinates exactly.

The inputs are the integers _a_ and _b_, which can range from -10^9 to 10^9, and a string of length up to 100. The constraints immediately suggest that simulating the robot’s moves literally for all repetitions of the string is impossible, because the target may be extremely far away. We need a solution that reasons about the robot’s position after any number of full repetitions of the string.

An edge case is when the target can be reached exactly at the end of a repetition or exactly in between repetitions. For example, if the string moves the robot right once ('R') and the target is at (3, 0), it can be reached only after three repetitions. A careless simulation that stops after a single repetition would incorrectly return "No".

Another subtle edge case occurs when the robot's net movement after a full sequence is zero. For instance, if the string is 'UDLR', the robot returns to the origin after each full repetition. In this case, the only reachable points are those visited during the first repetition. A naive approach that only considers the net movement vector would fail to capture these reachable intermediate points.

## Approaches

The brute-force approach is straightforward. You simulate the robot’s moves indefinitely, updating its position after each step, and check if it ever equals (_a_, _b_). The brute-force is correct because it literally follows the robot’s path. However, the robot could require up to 10^9 steps to reach a distant target, which is clearly infeasible. Even simulating one full repetition for every possible number of repetitions is too slow, because the target coordinates can be enormous, while the string length is short.

The key insight is to notice that the robot’s movement is periodic. Let (_dx_, _dy_) be the net change in position after one full repetition of the string. After repeating the string _k_ times, the robot’s position is the initial offset plus _k_ times the net change, plus some position reached during the first repetition. Formally, if we let (_x_i_, _y_i_) denote the robot’s position after _i_ moves in the first repetition, then any position reachable is of the form (_x_i + k_dx*, y_i + k_dy_) for some non-negative integer _k_.

With this observation, the problem reduces to checking, for each position reached in the first repetition, whether there exists a non-negative integer _k_ such that (_x_i + k_dx* = a* and _y_i + k_dy* = b*). This is a simple equation-solving problem in integers. Special care is required when _dx_ or _dy_ is zero to avoid division by zero. If both are zero, we only need to check positions reached during the first repetition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | a | + |
| Optimal | O( | s | ) |

## Algorithm Walkthrough

1. Compute the net movement (_dx_, _dy_) after one full repetition of the string by iterating through all characters. Increment or decrement the x or y coordinate depending on the move. This gives the overall translation vector per repetition.
2. Initialize the robot’s position at (0, 0) and store all positions visited during the first repetition in a list. This allows us to consider all possible offsets before repetitions start.
3. For each position (_x_i_, _y_i_) reached in the first repetition, check whether there exists a non-negative integer _k_ such that:

_x_i + k_dx* = a* and _y_i + k_dy* = b*.

If _dx_ is zero, this reduces to checking whether _x_i = a_, otherwise compute k as (a - x_i) / dx. Similarly for _dy_.
4. A valid _k_ must satisfy three conditions: it must be an integer, it must be non-negative, and it must satisfy both x and y equations simultaneously. If such a _k_ exists for any position, print "Yes".
5. If no valid _k_ is found after checking all positions, print "No".

Why it works: The algorithm relies on the invariant that any reachable position can be expressed as a position from the first repetition plus some multiple of the net translation vector. By iterating over all offsets from the first repetition, we cover all possible positions that could be reached after any number of repetitions. The integer and non-negativity checks ensure that we only consider feasible repetitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())
s = input().strip()

dx, dy = 0, 0
path = [(0, 0)]
for move in s:
    if move == 'U':
        dy += 1
    elif move == 'D':
        dy -= 1
    elif move == 'R':
        dx += 1
    elif move == 'L':
        dx -= 1
    path.append((path[-1][0] + (dx - path[-1][0]), path[-1][1] + (dy - path[-1][1])))

for x_i, y_i in path:
    kx = ky = None
    if dx != 0:
        if (a - x_i) % dx != 0:
            continue
        kx = (a - x_i) // dx
    else:
        if x_i != a:
            continue
        kx = 0

    if dy != 0:
        if (b - y_i) % dy != 0:
            continue
        ky = (b - y_i) // dy
    else:
        if y_i != b:
            continue
        ky = 0

    if kx == ky or dx == 0 or dy == 0:
        if kx >= 0 and ky >= 0:
            print("Yes")
            break
else:
    print("No")
```

We first calculate the net translation vector. Then we track all positions after each move in the first repetition. When checking for the integer _k_, we handle zero translations carefully to avoid division by zero. The final condition ensures that _k_ is consistent across both axes and non-negative. The `else` on the `for` loop triggers only if no valid _k_ is found.

## Worked Examples

### Sample 1

Input:

```
2 2
RU
```

| Step | Move | x | y | Notes |
| --- | --- | --- | --- | --- |
| 0 | start | 0 | 0 | initial |
| 1 | R | 1 | 0 | path[1] |
| 2 | U | 1 | 1 | path[2] |

Net translation dx=1, dy=1. Solve (x_i + k_dx = 2, y_i + k_dy = 2). At x_i=1, y_i=1: k=1. Positive integer, solution exists. Output: Yes.

### Sample 2

Input:

```
1 2
R
```

| Step | Move | x | y |
| --- | --- | --- | --- |
| 0 | start | 0 | 0 |
| 1 | R | 1 | 0 |

Net translation dx=1, dy=0. Solve (1 + k_1 = 1, 0 + k_0 = 2). k=0 from x, dy=0 requires y_i=b, but 0 != 2. No solution. Output: No.

The first example confirms correct handling of positive dx/dy. The second demonstrates the zero dy edge case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O( | s |

The algorithm easily fits within the constraints. Even the maximum |s| = 100, the checks over all positions are negligible. The integer operations and modulo arithmetic are fast, and the large target coordinates are handled algebraically rather than by iteration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a, b = map(int, input().split())
    s = input().strip()

    dx, dy = 0, 0
    path = [(0, 0)]
    for move in s:
        if move == 'U':
            dy += 1
        elif move == 'D':
            dy -= 1
        elif move == 'R':
            dx += 1
        elif move == 'L':
            dx -= 1
        path.append((path[-1][0] + (dx - path[-1][0]), path[-1][1
```
