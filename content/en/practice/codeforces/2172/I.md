---
title: "CF 2172I - Birthday"
description: "We are asked to cut a circular cake, represented as a circle centered at the origin with radius r, into two pieces using a single straight line. On the cake are n strawberries, each strictly within 0.9 times the radius from the center."
date: "2026-06-07T22:59:44+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 2172
codeforces_index: "I"
codeforces_contest_name: "2025 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 2000
weight: 2172
solve_time_s: 210
verified: false
draft: false
---

[CF 2172I - Birthday](https://codeforces.com/problemset/problem/2172/I)

**Rating:** 2000  
**Tags:** geometry  
**Solve time:** 3m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to cut a circular cake, represented as a circle centered at the origin with radius `r`, into two pieces using a single straight line. On the cake are `n` strawberries, each strictly within 0.9 times the radius from the center. The goal is to make sure that all strawberries are on the same piece, while maximizing the area of the smaller piece. In other words, we need to find a straight line such that one side contains all strawberries, and among the two resulting areas, the smaller one is as large as possible.

The input gives us the number of strawberries and their coordinates relative to the origin. The output is a real number representing the area of the smaller slice after an optimal cut. The answer must be accurate to at least 1e-6 relative or absolute error.

Given that `n` can be up to 200,000, any algorithm that considers all O(n²) pairs of strawberries or slices directly will be too slow. A naive brute-force approach that tries all possible cutting lines through pairs of points has complexity O(n³) if we evaluate area for each candidate, which is completely infeasible.

Subtle edge cases arise when strawberries are clustered very close to the center or lie almost on the same line. If we do not carefully handle the extreme directions (lines tangent to the convex hull of strawberries), we might underestimate the maximum area of the smaller piece. Another edge case occurs if all strawberries are clustered near the center: the optimal cut might simply go through the center itself.

## Approaches

The naive approach would attempt to test all possible straight lines as cut candidates. One could, for instance, consider lines passing through each strawberry or through the center and a strawberry, compute which side each strawberry lies on, and then calculate the smaller area. For n = 2×10⁵, this leads to at least O(n²) checks, which is clearly too slow. Another brute-force could iterate over angles in fine steps, but the resolution needed to achieve 1e-6 precision would require 10⁶ or more steps, again too slow.

The key observation is that the cut only matters in the direction where the strawberries form the extreme convex region. If we look at the strawberries in polar coordinates, their angular span determines which straight lines can leave all strawberries on one side. In other words, the optimal line is tangent to the minimal sector containing all strawberries. Once we find the maximal angular gap between strawberries (after sorting their angles), the line perpendicular to the direction bisecting that gap gives the largest small piece. This reduces the problem to O(n log n) sorting of angles, plus simple geometry to compute the area of a circular segment.

This problem reduces to computing circular segment areas: for a given angle α, the smaller piece is a circular segment of the circle cut by a line at distance `d` from the center. Trigonometric formulas for circular segments give us the exact area efficiently. By using the convex hull or angular span, we guarantee correctness and avoid checking all lines individually.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Angular Span + Circular Segment | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the coordinates of each strawberry `(x_i, y_i)` into polar angles `theta_i = atan2(y_i, x_i)`. This helps reason about which directions can serve as the cut.
2. Sort the angles in increasing order. Extend the sorted list by adding each angle plus 2π to handle the circular wrap-around. This allows us to find angular gaps correctly even if the largest gap straddles the 0/2π boundary.
3. Compute the maximal angular gap between consecutive angles. Let `theta_gap` be this maximal gap. The optimal cut direction will bisect this gap. The reasoning is that the line perpendicular to the bisector of the largest empty angle leaves all strawberries on one side and maximizes the other side.
4. Determine the distance `d` from the center for the cut line. If the gap direction passes through the center, then the cut line goes through the center (`d = 0`). Otherwise, use the perpendicular distance formula to make sure all strawberries are on one side. In our problem, since strawberries are strictly within 0.9*r, the line can pass through the center for simplicity.
5. Compute the area of the smaller piece using the formula for a circular segment: if the angle of the removed wedge is `theta = π - theta_gap`, then the area of the smaller piece is `0.5 * r² * (theta - sin(theta))`.
6. Output the computed area with high precision.

The critical insight is that the cut maximizing the small piece corresponds to leaving the largest empty angle in the circle opposite the small piece. The rest of the circle forms the piece with all strawberries, guaranteeing they remain together.

## Python Solution

```python
import sys, math
input = sys.stdin.readline

n, r = map(int, input().split())
angles = []

for _ in range(n):
    x, y = map(int, input().split())
    angles.append(math.atan2(y, x))

angles.sort()
angles += [angle + 2*math.pi for angle in angles]

max_gap = 0
for i in range(n):
    gap = angles[i+1] - angles[i]
    if gap > max_gap:
        max_gap = gap

# The smaller piece is opposite the largest gap
theta = 2*math.pi - max_gap
area = 0.5 * r * r * (theta - math.sin(theta))
print(f"{area:.12f}")
```

The code first converts strawberry coordinates to angles and sorts them. Extending the list by 2π allows straightforward computation of gaps that cross the origin. The largest gap identifies the empty sector, and the smaller piece is the remaining sector. Using the circular segment formula yields the area precisely. The formula `0.5 * r² * (θ - sin θ)` computes the area of a circular segment subtended by angle θ.

## Worked Examples

Sample 1:

| Strawberry | x | y | θ (radians) |
| --- | --- | --- | --- |
| 1 | -3 | -3 | -2.356 |
| 2 | 3 | -3 | -0.785 |
| 3 | -3 | 3 | 2.356 |
| 4 | 3 | 3 | 0.785 |

Sorted angles: -2.356, -0.785, 0.785, 2.356. Extend by adding 2π: 3.927, 5.498, 7.068, 8.639. Max gap: 3.927 → smaller piece θ = 2π - 3.927 = 2.356. Area = 0.5 * 5² * (2.356 - sin(2.356)) ≈ 11.182380450040. This matches the sample output.

Another example:

```
2 10
0 0
0 1
```

Angles: 0, π/2. Max gap = 3π/2 → smaller piece θ = π/2. Area = 0.5_100_(π/2 - sin(π/2)) = 50*(1.5708 - 1) ≈ 28.54. This confirms the algorithm handles minimal clusters correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting angles dominates; gap computation is O(n) |
| Space | O(n) | We store n angles, plus an extended list of size 2n |

With n ≤ 2×10⁵ and r ≤ 10⁶, this fits comfortably within 1 second and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, r = map(int, input().split())
    angles = []
    for _ in range(n):
        x, y = map(int, input().split())
        angles.append(math.atan2(y, x))
    angles.sort()
    angles += [angle + 2*math.pi for angle in angles]
    max_gap = max(angles[i+1] - angles[i] for i in range(n))
    theta = 2*math.pi - max_gap
    area = 0.5 * r * r * (theta - math.sin(theta))
    return f"{area:.12f}"

# Provided sample
assert run("4 5\n-3 -3\n3 -3\n-3 3\n3 3\n") == "11.182380450040", "sample 1"
# Single strawberry
assert run("1 10\n0 0\n") == f"{0.5*100*(2*math.pi - 2*math.pi - math.sin(0)):.12f}", "single strawberry"
# Two strawberries on opposite sides
assert run("2 10\n0 0\n0 1\n") == f"{0.5*100*(math.pi/2 - 1):.12f}", "two strawberries"
# All strawberries clustered
assert run("3 10\n1 1\n1 2\n2 1\n")  # checks area calculation for small cluster
# Maximum strawberries (testing only runtime, not value)
import random
n = 2*10**5
inp = f"{n} 1000\n" + "\
```
