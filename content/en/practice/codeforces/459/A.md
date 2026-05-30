---
title: "CF 459A - Pashmak and Garden"
description: "We are given the coordinates of two distinct trees on a Cartesian plane, and we know that the garden forms a perfect square aligned with the axes. Each vertex of the square has a tree, so there are exactly four trees."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 459
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 261 (Div. 2)"
rating: 1200
weight: 459
solve_time_s: 63
verified: true
draft: false
---

[CF 459A - Pashmak and Garden](https://codeforces.com/problemset/problem/459/A)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the coordinates of two distinct trees on a Cartesian plane, and we know that the garden forms a perfect square aligned with the axes. Each vertex of the square has a tree, so there are exactly four trees. The task is to determine the coordinates of the other two trees. If no square exists that satisfies these conditions, we must output -1.

The input consists of four integers representing the x and y coordinates of the two known trees. Each coordinate ranges from -100 to 100, and the output coordinates are allowed to be as large as ±1000. Because the input size is fixed (only two points), we do not need to worry about efficiency beyond simple arithmetic operations. Any solution that involves only a few constant-time checks will run comfortably within the time and memory limits.

Edge cases are subtle. If the two trees share the same x-coordinate, the square is vertical; if they share the same y-coordinate, it is horizontal. If neither coordinate matches, the trees must be diagonally opposite vertices of the square, and the distance along x must equal the distance along y. If this condition fails, no square can be formed. Naive implementations might overlook these conditions and try to construct impossible points.

For example, input `0 0 1 2` cannot form a square aligned with axes because the horizontal and vertical distances differ, so the correct output is -1. Similarly, input `0 0 0 1` represents a vertical side of a square, and the other two vertices must have x-coordinate shifted by the vertical distance (1), yielding `(1, 0)` and `(1, 1)`.

## Approaches

A brute-force approach would attempt to generate all possible squares given the first two points and check which configuration forms a valid square with sides parallel to the axes. This would involve multiple conditional branches for horizontal, vertical, and diagonal placements, and checking all permutations of the remaining two points. It works because a square is highly constrained, but it introduces unnecessary complexity.

The optimal approach is to classify the relationship between the two given points. If they lie on the same vertical line, the side of the square is vertical, and the other two vertices are shifted horizontally by the vertical distance. If they lie on the same horizontal line, the side is horizontal, and the remaining vertices are shifted vertically. If they form a diagonal of a square, the horizontal and vertical distances must be equal, and the other two vertices lie at `(x1, y2)` and `(x2, y1)`. If none of these cases hold, there is no valid square.

This observation reduces the problem to three constant-time checks and simple arithmetic, ensuring O(1) time and space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Overcomplicated, unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coordinates `(x1, y1)` and `(x2, y2)`.
2. Check if the two points are on the same vertical line (`x1 == x2`). If so, compute the horizontal distance as `d = abs(y2 - y1)`. The remaining vertices are `(x1 + d, y1)` and `(x2 + d, y2)`. Print these and exit.
3. If the two points are on the same horizontal line (`y1 == y2`), compute the vertical distance `d = abs(x2 - x1)`. The other vertices are `(x1, y1 + d)` and `(x2, y2 + d)`. Print and exit.
4. If the absolute horizontal distance equals the absolute vertical distance (`abs(x2 - x1) == abs(y2 - y1)`), the points form a diagonal. The other vertices are `(x1, y2)` and `(x2, y1)`. Print and exit.
5. If none of the above conditions hold, output -1, as no valid square can be formed.

Why it works: In each case, we exploit the axis-aligned property of the square. Vertical and horizontal side cases rely on translating along the perpendicular axis by the correct side length. The diagonal case works because in a square, the difference in x-coordinates equals the difference in y-coordinates for diagonally opposite vertices. These three checks cover all possible placements of two vertices on an axis-aligned square, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

x1, y1, x2, y2 = map(int, input().split())

if x1 == x2:
    d = abs(y2 - y1)
    print(x1 + d, y1, x2 + d, y2)
elif y1 == y2:
    d = abs(x2 - x1)
    print(x1, y1 + d, x2, y2 + d)
elif abs(x2 - x1) == abs(y2 - y1):
    print(x1, y2, x2, y1)
else:
    print(-1)
```

The code directly implements the three cases identified in the algorithm. The order of checks matters: we first check vertical alignment, then horizontal, and finally the diagonal. The `abs` ensures positive side lengths, and the print order matches the problem's requirement to output coordinates in any order.

## Worked Examples

### Example 1

Input: `0 0 0 1`

| Variable | Value |
| --- | --- |
| x1, y1 | 0, 0 |
| x2, y2 | 0, 1 |
| x1 == x2 | True |
| d | 1 |
| Output | 1 0 1 1 |

This demonstrates a vertical side case. The algorithm correctly computes the horizontal shift and finds the other two vertices.

### Example 2

Input: `0 0 1 1`

| Variable | Value |
| --- | --- |
| x1, y1 | 0, 0 |
| x2, y2 | 1, 1 |
| abs(x2 - x1) == abs(y2 - y1) | True |
| Output | 0 1 1 0 |

This is a diagonal case. The algorithm swaps coordinates to form the other two vertices along the square.

### Example 3

Input: `0 0 1 2`

| Variable | Value |
| --- | --- |
| x1, y1 | 0, 0 |
| x2, y2 | 1, 2 |
| No conditions hold | True |
| Output | -1 |

This shows an impossible configuration. The algorithm correctly detects no valid square exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed. |
| Space | O(1) | Only a few integer variables are stored; no arrays or data structures proportional to input. |

With maximum coordinates of ±100 and a single arithmetic step, the solution is well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    x1, y1, x2, y2 = map(int, input().split())
    if x1 == x2:
        d = abs(y2 - y1)
        return f"{x1 + d} {y1} {x2 + d} {y2}"
    elif y1 == y2:
        d = abs(x2 - x1)
        return f"{x1} {y1 + d} {x2} {y2 + d}"
    elif abs(x2 - x1) == abs(y2 - y1):
        return f"{x1} {y2} {x2} {y1}"
    else:
        return "-1"

# Provided sample
assert run("0 0 0 1\n") == "1 0 1 1", "sample 1"

# Custom cases
assert run("0 0 1 1\n") == "0 1 1 0", "diagonal square"
assert run("0 0 1 2\n") == "-1", "impossible square"
assert run("2 3 2 5\n") == "4 3 4 5", "vertical side"
assert run("5 7 8 7\n") == "5 10 8 10", "horizontal side"
assert run("-100 -100 -100 -98\n") == "-98 -100 -98 -98", "negative coordinates vertical"
assert run("100 100 102 100\n") == "100 102 102 102", "positive coordinates horizontal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 1 | 1 0 1 1 | vertical side case |
| 0 0 1 1 | 0 1 1 0 | diagonal case |
| 0 0 1 2 | -1 | impossible square |
| 2 3 2 5 | 4 3 4 5 | vertical with distance > 1 |
| 5 7 8 7 | 5 10 8 10 | horizontal side |
| -100 -100 -100 -98 | -98 -100 -98 -98 | negative coordinates |
| 100 100 102 |  |  |
