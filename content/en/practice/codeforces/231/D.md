---
title: "CF 231D - Magic Box"
description: "We are asked to compute the sum of numbers visible on a box from a given viewpoint in three-dimensional space. The box is axis-aligned, meaning all edges run along the X, Y, and Z axes. Its minimal corner is at the origin, and the opposite corner is at coordinates $(x1, y1, z1)$."
date: "2026-06-04T09:11:58+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 231
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 143 (Div. 2)"
rating: 1600
weight: 231
solve_time_s: 89
verified: true
draft: false
---

[CF 231D - Magic Box](https://codeforces.com/problemset/problem/231/D)

**Rating:** 1600  
**Tags:** brute force, geometry  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the sum of numbers visible on a box from a given viewpoint in three-dimensional space. The box is axis-aligned, meaning all edges run along the X, Y, and Z axes. Its minimal corner is at the origin, and the opposite corner is at coordinates $(x_1, y_1, z_1)$. Each of the six faces has a number written at its center. Vasya's position is strictly outside the box at $(x, y, z)$. The task is to determine which of the six numbers he can see and sum them.

Each face is associated with a plane. For the X-direction, one face lies at $x=0$ and the opposite at $x=x_1$. Similarly, the Y-direction faces lie at $y=0$ and $y=y_1$, and Z-direction faces lie at $z=0$ and $z=z_1$. A number is visible only if Vasya’s viewpoint is on the outside side of that face. If his coordinate along a dimension equals the face’s coordinate, he cannot see it.

Constraints tell us that all coordinates and numbers fit within $10^6$ in absolute value. Because only six checks are required per input, the solution is constant time. There is no need to worry about algorithmic efficiency for these bounds.

A non-obvious edge case arises when Vasya is aligned exactly with a plane of the box but outside. For example, if the box spans from 0 to 1 along all axes, and Vasya is at (2,0,0), he is outside but his y-coordinate equals the y=0 face. He should not see the face at y=0 but will see the other faces along x and z directions. A careless implementation might incorrectly assume he sees a face whenever he is outside along the corresponding axis without handling equality correctly.

## Approaches

A brute-force approach would conceptually simulate the viewpoint in 3D, tracing rays toward the box center or checking occlusion per face. This would involve a lot of geometric computation, floating-point arithmetic, and potentially $O(n)$ per ray if discretized. For a single box, this is overkill, but it scales poorly if extended to multiple boxes or more detailed visibility checks.

The key insight is that the box is axis-aligned and rectangular. This allows us to treat visibility along each axis independently. Along X, if Vasya’s x-coordinate is greater than x1, he sees the face at x=x1; if less than 0, he sees x=0. He cannot see both faces along the same axis. Applying this for each axis gives us a simple rule: check each dimension separately and add the number of the visible face if Vasya is on the outside side. This reduces the problem to at most three comparisons and three additions.

The brute-force approach is conceptually correct but unnecessarily complex. The axis-aligned observation reduces it to a constant-time computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force 3D ray simulation | O(1) for single box, higher for general case | O(1) | Overkill |
| Axis-aligned comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read Vasya’s coordinates $(x, y, z)$, box’s far corner $(x_1, y_1, z_1)$, and face numbers $a_1$ through $a_6$. This sets up the inputs.
2. Initialize a variable `total` to zero. This will accumulate the sum of visible numbers.
3. Determine visibility along the X-axis. If $x > x_1$, Vasya is to the right of the box and can see the face at x=x1 (number a2). If $x < 0$, he is to the left and can see the face at x=0 (number a1). Equality is ignored because he cannot see faces exactly on his plane.
4. Apply the same logic along the Y-axis. If $y > y_1$, he sees the far face y=y1 (number a4). If $y < 0$, he sees y=0 (number a3).
5. Apply the same logic along the Z-axis. If $z > z_1$, he sees the top face z=z1 (number a6). If $z < 0$, he sees the bottom face z=0 (number a5).
6. Sum the numbers identified as visible and print the result.

Why it works: Each axis has exactly two faces. Vasya can only be on one side of the box along each axis, so he sees at most one face per axis. Checking each axis independently guarantees that all visible faces are counted and none are double-counted or missed. The invariants are that the coordinate comparison correctly maps to visibility and that equality is treated as non-visible.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, y, z = map(int, input().split())
x1, y1, z1 = map(int, input().split())
a1, a2, a3, a4, a5, a6 = map(int, input().split())

total = 0

# X-axis visibility
if x < 0:
    total += a1
elif x > x1:
    total += a2

# Y-axis visibility
if y < 0:
    total += a3
elif y > y1:
    total += a4

# Z-axis visibility
if z < 0:
    total += a5
elif z > z1:
    total += a6

print(total)
```

The solution directly implements the axis-aligned comparison strategy. The X-axis section correctly identifies the left and right faces, the Y-axis section handles front and back, and the Z-axis section handles bottom and top. Off-by-one errors are avoided by strictly using `<` and `>` comparisons, matching the problem requirement that equality means the face is not visible.

## Worked Examples

**Sample 1:**

Input:

```
2 2 2
1 1 1
1 2 3 4 5 6
```

| Variable | Value | Reasoning |
| --- | --- | --- |
| x > x1 | 2>1 | True, add a2=2 |
| y > y1 | 2>1 | True, add a4=4 |
| z > z1 | 2>1 | True, add a6=6 |
| total | 12 | sum of visible faces |

This shows that when Vasya is outside in all axes positive, he sees the far faces along each axis.

**Sample 2:**

Input:

```
-1 0 2
1 1 1
1 2 3 4 5 6
```

| Variable | Value | Reasoning |
| --- | --- | --- |
| x < 0 | -1<0 | True, add a1=1 |
| y < 0 | 0<0 | False, add nothing |
| z > z1 | 2>1 | True, add a6=6 |
| total | 7 | sum of visible faces |

This demonstrates handling of equality: y=0 is on the plane of a3, so it is not visible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only six comparisons and at most three additions |
| Space | O(1) | Only a few integer variables are used |

Given the problem constraints, this solution completes almost instantly for any allowed input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, y, z = map(int, input().split())
    x1, y1, z1 = map(int, input().split())
    a1, a2, a3, a4, a5, a6 = map(int, input().split())
    total = 0
    if x < 0:
        total += a1
    elif x > x1:
        total += a2
    if y < 0:
        total += a3
    elif y > y1:
        total += a4
    if z < 0:
        total += a5
    elif z > z1:
        total += a6
    return str(total)

# provided samples
assert run("2 2 2\n1 1 1\n1 2 3 4 5 6\n") == "12", "sample 1"
assert run("-1 0 2\n1 1 1\n1 2 3 4 5 6\n") == "7", "custom sample"

# minimum size input, all numbers 1
assert run("-1 -1 -1\n1 1 1\n1 1 1 1 1 1\n") == "3", "min size all 1"

# maximum coordinates
assert run("1000000 1000000 1000000\n1 1 1\n1 2 3 4 5 6\n") == "12", "max positive"

# all coordinates negative
assert run("-1000000 -1000000 -1000000\n1 1 1\n1 2 3 4 5 6\n") == "9", "max negative"

# equality with plane
assert run("0 0 2\n1
```
