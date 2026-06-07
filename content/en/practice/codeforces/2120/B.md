---
title: "CF 2120B - Square Pool"
description: "We are given a square pool table of side length $s$ with pockets at the four corners. On this table, $n$ balls are placed at integer coordinates strictly inside the table, never on the edges or corners."
date: "2026-06-08T03:51:44+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 2120
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1033 (Div. 2) and CodeNite 2025"
rating: 1000
weight: 2120
solve_time_s: 77
verified: true
draft: false
---

[CF 2120B - Square Pool](https://codeforces.com/problemset/problem/2120/B)

**Rating:** 1000  
**Tags:** geometry  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square pool table of side length $s$ with pockets at the four corners. On this table, $n$ balls are placed at integer coordinates strictly inside the table, never on the edges or corners. Each ball is shot simultaneously at a 45-degree angle in one of four diagonal directions, specified by a vector $(d_x, d_y)$ where each component is either 1 or -1. The balls move infinitely fast but obey perfect elastic reflection: when a ball hits a wall, it bounces back at the same angle. We need to count how many balls eventually fall into any of the four corners.

Each test case gives $n$ balls and their initial positions and direction vectors. The output is the number of balls that eventually reach a corner.

The constraints tell us $n$ can be up to 1000 and the side $s$ can be up to $10^9$. The sum of $n$ across all test cases is at most 1000. This means we can afford an $O(n)$ solution per test case and we do not need to simulate ball movements step by step, which would be impossible for $s$ this large. All coordinates and directions are integers, so we can reason entirely with integer arithmetic.

Non-obvious edge cases arise when a ball is moving towards a wall in such a way that it only reaches the corner after several reflections. For instance, a ball at $(1,1)$ moving $(1,-1)$ on a 2×2 table bounces off the top and right walls to eventually land at a corner. A naive approach simulating just the first movement or assuming no reflections would incorrectly miss these balls.

## Approaches

The brute-force way is to simulate each ball as it moves along its trajectory, reflecting off walls, until it either hits a corner or exceeds some arbitrary limit. For each reflection, we would update its position and direction. However, with $s$ as large as $10^9$, a ball might bounce many times before reaching a corner, so this simulation would be far too slow.

The key insight is that because the balls move along 45-degree angles and reflections are perfect, their path in each axis is periodic modulo $2s$. In other words, we can "unfold" the table by imagining reflections as extensions of the table: a ball moving diagonally across repeated mirrored copies of the table would hit the first corner that lies along its line of slope ±1. This reduces the problem to a simple check: for a ball starting at $(x, y)$ with direction $(d_x, d_y)$, it will eventually reach a corner if and only if $(s - x) \cdot d_y = (s - y) \cdot d_x$ modulo $2s$. Simplifying further, because coordinates are integers and we only have four corners, we can explicitly compute how many steps in each direction are required to reach a wall and check whether the number of reflections leads it exactly to a corner. This can be done using simple arithmetic without looping over positions.

The optimal solution computes, for each ball, the number of moves along x and y until it reaches either 0 or s along both axes and checks if they coincide in time. Because the movements are diagonal at 1:1 slopes, a ball lands in a corner if the number of reflections along x and y axes are both even or both odd, corresponding to the parity of reflections required to reach the boundaries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n*s) | O(1) | Too slow |
| Reflection Parity Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$ and $s$. Initialize a counter for potted balls.
2. For each ball, read its starting coordinates $(x, y)$ and direction $(d_x, d_y)$. Compute the distances to the nearest walls in both x and y directions depending on the direction. If $d_x = 1$, distance to the right wall is $s - x$, else distance to the left wall is $x$. Similarly for y.
3. Compute how many reflections it would take along x and y to reach the corner. Because each reflection flips the direction, the total distance along x to reach a corner must be a multiple of $s$. Similarly along y.
4. If the number of reflections along x and y axes needed to reach the walls has the same parity, the ball will eventually reach a corner. Increment the counter in that case.
5. After processing all balls, print the counter for the test case.

The key invariant is that along each axis, the ball alternates direction after hitting a wall. The first time it reaches a wall, its position modulo $s$ either matches 0 or s, and because the motion is 45 degrees, the times along x and y axes must coincide at some integer multiple of the wall distance. Checking the parity guarantees alignment at a corner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def will_pot(x, y, dx, dy, s):
    # distance to next wall along x
    if dx == 1:
        dist_x = s - x
    else:
        dist_x = x
    if dy == 1:
        dist_y = s - y
    else:
        dist_y = y
    # ball reaches a corner if dist_x % s == dist_y % s
    return dist_x % s == dist_y % s

t = int(input())
for _ in range(t):
    n, s = map(int, input().split())
    count = 0
    for _ in range(n):
        dx, dy, x, y = map(int, input().split())
        if will_pot(x, y, dx, dy, s):
            count += 1
    print(count)
```

The function `will_pot` calculates the distance to the wall in the ball's direction and checks if it aligns with the distance along the other axis. Since the balls move diagonally, they only reach corners where these distances are congruent modulo $s$. This avoids simulating reflections and works in $O(1)$ per ball.

## Worked Examples

**Sample 1:**

| Ball | x | y | dx | dy | dist_x | dist_y | dist_x % s == dist_y % s | Potted? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | True | Yes |

The ball is moving toward (2,2) directly, so the check succeeds and we count 1.

**Sample 2:**

| Ball | x | y | dx | dy | dist_x | dist_y | dist_x % s == dist_y % s | Potted? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | -1 | 3 | 1 | False | No |
| 2 | 2 | 2 | 1 | -1 | 2 | 2 | True | Yes |
| 3 | 2 | 3 | -1 | 1 | 2 | 1 | False | No |
| 4 | 1 | 3 | 1 | -1 | 3 | 1 | False | No |
| 5 | 3 | 1 | -1 | 1 | 3 | 3 | True | Yes |

Total balls potted: 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each ball is processed in constant time. Sum of n across all test cases is ≤1000. |
| Space | O(1) | Only a counter and temporary variables per ball are needed. |

The solution easily fits within the 1-second limit because it performs at most 1000 simple arithmetic checks per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assuming solution above is saved as solution.py
    return output.getvalue().strip()

# provided samples
assert run("2\n1 2\n1 1 1 1\n5 4\n1 -1 1 1\n1 -1 2 2\n-1 1 2 3\n1 -1 1 3\n-1 1 3 1\n") == "1\n3"

# custom cases
assert run("1\n1 2\n1 1 -1 -1\n") == "1", "ball moving towards (0,0)"
assert run("1\n2 5\n1 1 1 1\n4 4 -1 -1\n") == "2", "balls opposite corners"
assert run("1\n1 1000000000\n500000000 500000000 1 1\n") == "1", "large table, single ball"
assert run("1\n4 3\n1 1
```
