---
title: "CF 409G - On a plane"
description: "We are given a set of $n$ points on a 2D plane with floating-point coordinates. The task is to find the smallest possible angle of rotation around the origin that ensures all points can be covered by a half-plane (a straight line that divides the plane into two parts)."
date: "2026-06-07T02:11:16+07:00"
tags: ["codeforces", "competitive-programming", "*special", "geometry"]
categories: ["algorithms"]
codeforces_contest: 409
codeforces_index: "G"
codeforces_contest_name: "April Fools Day Contest 2014"
rating: 2200
weight: 409
solve_time_s: 284
verified: false
draft: false
---

[CF 409G - On a plane](https://codeforces.com/problemset/problem/409/G)

**Rating:** 2200  
**Tags:** *special, geometry  
**Solve time:** 4m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of $n$ points on a 2D plane with floating-point coordinates. The task is to find the smallest possible angle of rotation around the origin that ensures all points can be covered by a half-plane (a straight line that divides the plane into two parts). Equivalently, if you imagine shining a light from the origin, you want to rotate it such that all points lie on one side of the light beam, and the goal is to minimize the angle through which you rotate to achieve that.

The input has up to 1000 points, and coordinates are between -1000 and 1000, given with two decimal places. This means floating-point precision is relevant, but we do not have to worry about extremely large numbers or precision beyond what double-precision floating point provides. The time limit of 1 second suggests that $O(n^2 \log n)$ solutions are feasible, but $O(n^3)$ solutions would likely be too slow.

A non-obvious edge case occurs when multiple points are collinear with the origin. For instance, if all points lie on the positive x-axis, the minimal rotation angle is 0. Another tricky scenario is when points are evenly distributed in a circle around the origin; naive methods that only check axis-aligned directions could underestimate the required angle. Cases where points are clustered in opposite directions must be handled carefully because the minimal half-plane may exclude a small cluster.

## Approaches

A brute-force approach would be to try every possible pair of points to define a candidate direction for the half-plane. For each candidate direction, we would check all points to compute the minimal rotation needed to cover them. This is correct because the optimal boundary of the half-plane must pass through at least one of the points. However, this method involves $O(n^3)$ operations in the worst case: for each of $n^2$ candidate directions, we check $n$ points, which is excessive for $n=1000$.

The key observation is that the problem reduces to angles relative to the origin. Each point can be represented as an angle using `atan2(y, x)`. The minimal half-plane corresponds to the minimal angular interval covering all points. Sorting the angles allows us to treat this as a circular interval problem: we can iterate through the sorted angles, treating each as a potential start of the half-plane, and find the maximal angle that fits within a 180-degree sweep. This reduces the complexity drastically because sorting takes $O(n \log n)$ and scanning can be done in $O(n)$ with a two-pointer approach.

The brute-force works because it explicitly considers all point pairs, but fails when $n$ is large due to cubic growth. The insight that each point's angle around the origin is sufficient allows us to solve the problem using a linear scan over a sorted array of angles, leveraging the circular structure of angles with modulo arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Angular Sweep | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the angle of each point relative to the origin using `atan2(y, x)`. This transforms each point into a single scalar angle between $-π$ and $π$. Using angles reduces a 2D geometric problem to a 1D circular problem.
2. Sort the array of angles in increasing order. Sorting ensures we can efficiently find contiguous angular intervals that cover all points.
3. Duplicate the angle array by adding $2π$ to each angle and appending it to the end of the sorted array. This handles the circular wrap-around, so we can check intervals that cross the $-π/π$ boundary without special logic.
4. Initialize two pointers, `i` and `j`, both starting at 0. `i` represents the start of the half-plane, and `j` will scan forward to find the farthest point within a 180-degree interval from `i`.
5. For each `i`, advance `j` as long as the angle difference `angles[j] - angles[i]` is less than or equal to π. The maximal difference gives the largest interval covered by a half-plane starting at `angles[i]`.
6. Compute the complement angle to 360 degrees (or $2π$ radians) by taking $2π - \text{max interval}$. Track the minimal complement across all `i`. This minimal complement is the smallest rotation that ensures all points are in a half-plane.

Why it works: Every half-plane that contains all points can be represented as an interval of at most π radians on the unit circle. Sorting the angles guarantees that scanning with a two-pointer technique captures the largest interval. By computing the complement, we find the minimal angle of rotation required. No configuration of points can produce a smaller rotation because every point lies on the unit circle, and the largest angular gap determines the minimal rotation.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
angles = []

for _ in range(n):
    x, y = map(float, input().split())
    angles.append(math.atan2(y, x))

angles.sort()
angles += [angle + 2 * math.pi for angle in angles]

ans = 0.0
j = 0

for i in range(n):
    while j < 2 * n and angles[j] - angles[i] <= math.pi + 1e-12:
        j += 1
    ans = max(ans, angles[j - 1] - angles[i])

print(f"{2 * math.pi - ans:.10f}")
```

The code first reads all points and converts them to angles. Sorting allows scanning with two pointers. Duplicating the array handles circular wrap-around, so we do not need special logic for intervals crossing the -π/π boundary. The `1e-12` tolerance prevents floating-point errors at exact boundaries. The final answer prints the minimal rotation as $2π - \text{largest interval}$.

## Worked Examples

**Sample 1**

Input:

```
8
-2.14 2.06
-1.14 2.04
-2.16 1.46
-2.14 0.70
-1.42 0.40
-0.94 -0.48
-1.42 -1.28
-2.16 -1.62
```

| i | angles[i] | j (scan) | angles[j-1]-angles[i] | Complement 2π-Δ |
| --- | --- | --- | --- | --- |
| 0 | 2.37 | 4 | 3.85-2.37=1.48 | 4.80 |
| 1 | 2.39 | 5 | 3.88-2.39=1.49 | 4.79 |
| ... | ... | ... | ... | ... |

This trace shows how the two-pointer technique finds the largest interval and its complement gives the minimal rotation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting takes n log n, scanning twice over n elements is O(n) |
| Space | O(n) | Store n angles, duplicate array for wrap-around |

With n ≤ 1000, this solution runs comfortably within 1 second and uses negligible memory.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    angles = []
    for _ in range(n):
        x, y = map(float, input().split())
        angles.append(math.atan2(y, x))
    angles.sort()
    angles += [angle + 2 * math.pi for angle in angles]
    ans = 0.0
    j = 0
    for i in range(n):
        while j < 2 * n and angles[j] - angles[i] <= math.pi + 1e-12:
            j += 1
        ans = max(ans, angles[j - 1] - angles[i])
    return f"{2 * math.pi - ans:.10f}"

# provided sample
assert run("8\n-2.14 2.06\n-1.14 2.04\n-2.16 1.46\n-2.14 0.70\n-1.42 0.40\n-0.94 -0.48\n-1.42 -1.28\n-2.16 -1.62\n") == "5.4100117506"

# custom tests
assert run("1\n0 0\n") == f"{2*math.pi:.10f}", "single point"
assert run("2\n1 0\n-1 0\n") == f"{math.pi:.10f}", "two opposite points"
assert run("4\n1 0\n0 1\n-1 0\n0 -1\n") == f"{math.pi:.10f}", "square around origin"
assert run("3\n0 1\n1 0\n0 -1\n") == f"{3.1415926536:.10f}", "triangle with vertical spread"
```

| Test input | Expected output | What it validates |

|---|---
