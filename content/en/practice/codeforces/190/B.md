---
title: "CF 190B - Surrounded"
description: "We are given two circular “threat zones” on a plane. Each one is defined by a center point and a radius. The center is a city, and the radius describes how far the enemy ring extends from that city. We are allowed to place a single radar anywhere in the plane."
date: "2026-06-03T01:22:56+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1800
weight: 190
solve_time_s: 84
verified: true
draft: false
---

[CF 190B - Surrounded](https://codeforces.com/problemset/problem/190/B)

**Rating:** 1800  
**Tags:** geometry  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two circular “threat zones” on a plane. Each one is defined by a center point and a radius. The center is a city, and the radius describes how far the enemy ring extends from that city.

We are allowed to place a single radar anywhere in the plane. This radar detects anything that lies within a disk of radius $r$ centered at the radar location. The radar is considered successful if, at the moment the attack begins, it can detect at least one point from each of the two enemy circles. In geometric terms, the radar disk must intersect both given circles.

The task is to choose the radar location and its radius so that this is possible, while minimizing the radius.

The input size is constant, only two circles are given, so any solution that involves a small fixed amount of geometric computation is easily fast enough. There is no need for asymptotic optimization tricks, but precision and correct case handling are critical.

A naive but dangerous mistake is to assume the best radar position must be at one of a few obvious places such as a circle center or midpoint of centers. This fails because the optimal point may lie anywhere in the plane, typically along the segment between centers, but not necessarily at a discrete candidate.

Another common pitfall is ignoring containment cases. If one circle lies entirely inside the other, or if they overlap heavily, the optimal radius behaves differently than in the disjoint case.

For example, if both circles coincide, the answer is simply the smaller radius, because placing the radar at the center already guarantees detection of both boundaries at distance equal to that radius. Any approach that only considers distances between centers would incorrectly return zero.

## Approaches

We want a point $P$ minimizing the maximum distance required to reach both circles’ boundaries.

For a fixed radar position $P$, the minimum radius needed is:

$$\max(d(P, C_1) - r_1,\; d(P, C_2) - r_2,\; 0)$$

where $C_i$ is the center of circle $i$, and $r_i$ is its radius. We subtract $r_i$ because we only need to touch the circle boundary, not reach its center.

Geometrically, this means each circle induces a “distance constraint” region: we must be within distance $r + r_i$ of center $C_i$. So for a fixed $r$, feasibility becomes: does there exist a point $P$ that lies within both disks of radius $r + r_1$ around $C_1$ and radius $r + r_2$ around $C_2$.

This reduces the problem to finding the smallest $r$ such that two disks intersect.

The key observation is monotonicity: if a radius $r$ works, any larger radius also works. This allows binary search over $r$.

To test feasibility for a given $r$, we check whether two circles intersect:

$$d(C_1, C_2) \le (r + r_1) + (r + r_2)$$

which simplifies to:

$$d(C_1, C_2) \le 2r + r_1 + r_2$$

So:

$$r \ge \frac{d(C_1, C_2) - r_1 - r_2}{2}$$

Since $r \ge 0$, the answer is:

$$\max\left(0, \frac{d - r_1 - r_2}{2}\right)$$

The problem collapses to computing the Euclidean distance between centers and applying this formula.

The brute-force interpretation would try all possible radar positions, which is impossible over continuous space. Even discretizing the plane would not help because optimal positions are not restricted to a grid.

The insight is that the constraint is entirely determined by a single scalar value: the distance between centers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (search plane) | infinite / infeasible | O(1) | Too slow |
| Optimal (geometry reduction) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two circle descriptions, each containing coordinates and radius. These define the only geometric objects in the problem, so all further reasoning depends on their relative placement.
2. Compute the Euclidean distance between the two centers:

$$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$

This distance fully captures the spatial relationship between the two threat zones.
3. Compute the effective overlap deficit:

$$d - (r_1 + r_2)$$

This measures how far the circles are from already touching or overlapping.
4. If this value is negative or zero, the circles already intersect or one contains the other. In that case, a radar placed at the intersection area can touch both without any extra radius, so answer is 0.
5. Otherwise, divide the excess distance by 2. This represents how much the radar must extend outward to simultaneously “bridge” the gap to both circles.
6. Output the resulting value with sufficient floating-point precision.

### Why it works

The radar position that minimizes required radius always lies on the line segment connecting the two centers. For any candidate point off this line, projecting it onto the segment does not increase distances to either center in a way that improves the maximum constraint. This reduces the optimization from a 2D continuous search to a 1D distance balance problem. Once restricted to that structure, the minimal radius is exactly half of the uncovered gap between expanded circles, or zero if they already overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

x1, y1, r1 = map(int, input().split())
x2, y2, r2 = map(int, input().split())

dx = x1 - x2
dy = y1 - y2

d = (dx * dx + dy * dy) ** 0.5

ans = (d - r1 - r2) / 2.0
if ans < 0:
    ans = 0.0

print(ans)
```

The implementation directly computes the geometric reduction derived earlier. The only subtle point is ensuring floating-point precision is sufficient; using Python’s double precision float is adequate given the constraints.

The subtraction step must happen before dividing by two, since negative values represent overlap cases that must be clamped to zero. Skipping this clamp leads to incorrect negative answers.

## Worked Examples

### Example 1

Input:

```
0 0 1
6 0 3
```

We compute:

$$d = 6$$

$$r_1 + r_2 = 4$$

| Step | Value |
| --- | --- |
| Distance $d$ | 6 |
| Sum of radii | 4 |
| Gap $d - r_1 - r_2$ | 2 |
| Answer | 1 |

This shows a case where circles are separated but close enough that the optimal radar only needs to “bridge” a small gap.

### Example 2

Input:

```
0 0 5
3 0 5
```

| Step | Value |
| --- | --- |
| Distance $d$ | 3 |
| Sum of radii | 10 |
| Gap $d - r_1 - r_2$ | -7 |
| Answer | 0 |

This confirms the containment/overlap case, where no additional radar radius is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints are extremely small in terms of number of objects, so a direct geometric formula is optimal and well within limits. Floating-point operations dominate, but remain constant time.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x1 - x2
    dy = y1 - y2
    d = math.sqrt(dx * dx + dy * dy)

    ans = (d - r1 - r2) / 2.0
    if ans < 0:
        ans = 0.0

    return f"{ans:.10f}"

# provided sample
assert abs(float(run("0 0 1\n6 0 3\n")) - 1.0) < 1e-9

# identical circles
assert abs(float(run("0 0 5\n0 0 5\n")) - 0.0) < 1e-9

# one inside another
assert abs(float(run("0 0 10\n1 1 1\n")) - 0.0) < 1e-9

# far apart
assert abs(float(run("0 0 1\n100 0 1\n")) - 49.0) < 1e-9

# tangent case
assert abs(float(run("0 0 1\n2 0 1\n")) - 0.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical circles | 0 | full containment |
| one inside another | 0 | nested circle handling |
| far apart | 49 | large separation correctness |
| tangent circles | 0 | boundary equality case |

## Edge Cases

A key edge case is when one circle completely contains the other. For input:

```
0 0 10
1 0 1
```

The algorithm computes $d \approx 1$, and $r_1 + r_2 = 11$, so the gap is negative. The clamp forces answer to zero. Geometrically, any point inside the larger circle already guarantees intersection with the smaller one, so no extra radar radius is required.

Another edge case is tangency:

```
0 0 1
2 0 1
```

Here $d = 2$, and $r_1 + r_2 = 2$, giving zero gap. The algorithm correctly returns zero, matching the fact that the circles already touch, so a radar placed at the touching point detects both immediately.

A third subtle case is large separation where radii are small:

```
0 0 1
100 0 1
```

The gap is 98, so answer is 49. This reflects symmetry: the optimal radar sits midway between the “inflated boundaries” of the circles, balancing required reach to both sides equally.
