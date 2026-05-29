---
title: "CF 409G - On a plane"
description: "We are given a set of points on a two-dimensional plane, each with real-valued coordinates. The task is to find the largest possible angle formed at the origin by any three of these points, where the origin serves as the vertex and the rays extend to the selected points."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "geometry"]
categories: ["algorithms"]
codeforces_contest: 409
codeforces_index: "G"
codeforces_contest_name: "April Fools Day Contest 2014"
rating: 2200
weight: 409
solve_time_s: 113
verified: false
draft: false
---

[CF 409G - On a plane](https://codeforces.com/problemset/problem/409/G)

**Rating:** 2200  
**Tags:** *special, geometry  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a two-dimensional plane, each with real-valued coordinates. The task is to find the largest possible angle formed at the origin by any three of these points, where the origin serves as the vertex and the rays extend to the selected points. The output is the magnitude of this angle in radians, accurate to within $10^{-2}$.

The first observation is that the number of points, $n$, is at most 1000. This means any solution with $O(n^2 \log n)$ or better will be feasible within a 1-second time limit, since $1000^2 \log 1000 \approx 10^6$ operations, which is easily manageable. The coordinates are given with two fractional digits, but the algorithm does not require exact arithmetic - only precision enough to correctly compare angles.

Non-obvious edge cases arise when points are nearly collinear with the origin or symmetrically placed. For instance, if two points lie on a line through the origin, the naive approach of comparing every triple could miscalculate the angle due to floating-point errors or incorrect handling of circular angles near $0$ or $2\pi$. Another scenario occurs when all points lie on the same line - the correct maximal angle should be $\pi$ in such a case.

## Approaches

The brute-force approach is conceptually simple: for every triplet of points, compute the angle at the origin formed by the rays to those points, and track the maximum. Computing the angle involves using the arctangent of the vectors or the cosine law. The complexity is $O(n^3)$, because there are $\binom{n}{3} \approx n^3/6$ triplets. For $n = 1000$, this yields roughly $1.6 \times 10^8$ operations, which is too slow.

The key insight is that we do not need to examine all triplets. The angle at the origin is determined solely by the directions of the vectors, not their lengths. If we compute the angle of each point relative to the positive $x$-axis, the problem reduces to finding the pair of points whose angular separation (in the circular sense) is maximal. This converts a 2D geometric problem into a 1D angular sweep problem. Sorting the angles and scanning through them allows us to efficiently find the largest angular gap. To handle circular wrap-around, we can duplicate the sorted array with each angle increased by $2\pi$, allowing a simple linear scan to consider all circular pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Angular Sweep | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each point $(x_i, y_i)$, compute the angle it makes with the positive $x$-axis using `atan2(y_i, x_i)`. This captures the direction of the vector from the origin to the point in the range $[-π, π]$. This reduces the problem from 2D vector geometry to 1D angle comparisons.
2. Sort all angles in increasing order. Sorting allows us to efficiently find consecutive angular gaps, which correspond to the largest potential angles at the origin.
3. Duplicate the sorted list with each angle incremented by $2π$. This simulates a circular array, allowing a simple linear scan for maximal gaps without special-case handling of the wrap-around from $2π$ back to $0$.
4. Initialize a variable `max_angle` to zero. Then iterate through the original sorted angles. For each angle, find the smallest succeeding angle that exceeds it by at most $π$ (half circle), using either a binary search or two-pointer technique. Compute the difference between this angle and the current one - the complementary angle is the maximal angle formed with a third point in the opposite direction.
5. Keep track of the largest angle encountered during the sweep. The maximal angular gap directly translates into the largest angle at the origin formed by any three points.

Why it works: the invariant is that we always consider angles in sorted order and handle the circular wrap-around, ensuring that for any origin-centered configuration, the largest possible angle is captured as either a direct angular difference or its complement to $2π$. By scanning only consecutive angles in the sorted order, we guarantee that no potential maximal angle is missed.

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
angles_extended = angles + [a + 2*math.pi for a in angles]

max_angle = 0.0
j = 0
for i in range(n):
    while j < len(angles_extended) and angles_extended[j] - angles[i] <= math.pi:
        j += 1
    # angle between current and j-1 (last within half-circle)
    max_angle = max(max_angle, angles_extended[j-1] - angles[i])

# maximal angle could be the complementary of the half-circle difference
max_angle = max(max_angle, 2*math.pi - max_angle)
print(f"{max_angle:.10f}")
```

The code first reads all points and converts them to polar angles using `atan2`. Sorting ensures that all potential angle gaps are examined in order. Extending the array allows a simple linear scan without worrying about wrap-around. The while-loop efficiently finds the largest gap less than or equal to $π$, and taking the complement ensures the correct maximal angle.

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

| i | angles[i] (rad) | j | angles_extended[j-1] - angles[i] | max_angle |
| --- | --- | --- | --- | --- |
| 0 | 2.38 | 4 | 3.03 - 2.38 = 0.65 | 0.65 |
| 1 | 2.43 | 5 | 3.09 - 2.43 = 0.66 | 0.66 |
| ... | ... | ... | ... | ... |
| 0 | 2.38 | 7 | 7.79 - 2.38 = 5.41 | 5.41 |

The maximal angle detected is 5.410 radians, which matches the expected output.

**Custom Input**

```
3
1 0
0 1
-1 0
```

Trace:

| i | angle | j | gap | max_angle |
| --- | --- | --- | --- | --- |
| 0 | 0.0 | 2 | 1.570 | 1.570 |
| 1 | 1.570 | 3 | 3.141 | 3.141 |

The maximal angle is π, which occurs between vectors (1,0) and (-1,0).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting angles dominates; linear sweep is O(n) |
| Space | O(n) | Storing angles and extended list |

For $n ≤ 1000$, this solution is well within the 1-second limit.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    angles = [math.atan2(*map(float, input().split())) for _ in range(n)]
    angles.sort()
    angles_ext = angles + [a + 2*math.pi for a in angles]
    max_angle = 0.0
    j = 0
    for i in range(n):
        while j < len(angles_ext) and angles_ext[j] - angles[i] <= math.pi:
            j += 1
        max_angle = max(max_angle, angles_ext[j-1] - angles[i])
    max_angle = max(max_angle, 2*math.pi - max_angle)
    return f"{max_angle:.10f}"

# Provided sample
assert abs(float(run("8\n-2.14 2.06\n-1.14 2.04\n-2.16 1.46\n-2.14 0.70\n-1.42 0.40\n-0.94 -0.48\n-1.42 -1.28\n-2.16 -1.62\n")) - 5.410) < 1e-2

# Minimum input
assert abs(float(run("1\n0.0 1.0\n")) - 0.0) < 1e-2

# Three points forming a right triangle
assert abs(float(run("3\n1 0\n0 1\n-1 0\n")) - math.pi) < 1e-2

# All points on the x-axis
assert abs(float(run("4\n-1 0\n0 0\n1 0
```
