---
title: "CF 104804G - \u041e, \u043d\u0435\u0442! \u0413\u0435\u043e\u043c\u0430!!!"
description: "We are given three points in the plane, each with integer coordinates. The points are guaranteed not to lie on a single straight line, so they uniquely determine a circle passing through all three of them."
date: "2026-06-28T13:27:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "G"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 88
verified: false
draft: false
---

[CF 104804G - \u041e, \u043d\u0435\u0442! \u0413\u0435\u043e\u043c\u0430!!!](https://codeforces.com/problemset/problem/104804/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three points in the plane, each with integer coordinates. The points are guaranteed not to lie on a single straight line, so they uniquely determine a circle passing through all three of them. The task is to compute the radius of that circle and print it with sufficient precision.

Geometrically, this is asking for the circumradius of a triangle formed by the three points. The triangle is always valid because collinearity is excluded. The output is a single real number, so the entire problem reduces to deriving and implementing a stable geometric formula.

The constraints are very small in terms of coordinate magnitude, with values bounded by 1000 in absolute value. This eliminates any need for numeric optimization or worry about overflow in floating-point operations beyond standard double precision safety. A constant time geometric formula is sufficient.

The main ways solutions tend to go wrong are numerical rather than algorithmic. One common failure is attempting to compute the circumcenter explicitly using perpendicular bisectors in slope form, which becomes unstable when segments are nearly vertical. Another is computing area using integer arithmetic or determinants but forgetting that the radius formula divides by twice the triangle area, which can lead to division by zero or precision loss if the area is computed poorly. A third issue is swapping point order in vector cross products, which flips signs and can silently corrupt intermediate results.

A concrete edge case that exposes slope-based approaches is:

Input:

```
0 0
1 1000
2 1000
```

The triangle is extremely flat in one direction, and computing perpendicular bisectors using slopes like 1000/1 leads to unstable floating-point behavior.

Another case that exposes area mistakes:

```
0 0
1 0
2 0
```

This is invalid per constraints, but a buggy implementation that accidentally allows collinearity would divide by zero area when computing radius.

## Approaches

The naive geometric approach tries to construct the circumcenter explicitly. One can take two sides of the triangle, compute their perpendicular bisectors, and intersect them. Once the center is found, the radius is the distance to any vertex. This is mathematically correct, but it requires solving linear equations with slopes or determinants and is sensitive to floating-point instability when lines are close to vertical or nearly parallel. In worst-case implementations, multiple conditional branches are needed to avoid division by zero when computing slopes, and each branch introduces more numerical risk.

A cleaner approach avoids computing the center entirely. Instead, we use the classical relation between triangle area and circumradius. For a triangle with side lengths a, b, c and area S, the circumradius R satisfies R = abc / (4S). This formula comes from standard triangle geometry and remains stable if we compute S using a cross product. The key observation is that both side lengths and area can be expressed directly from coordinates using vector arithmetic, avoiding any line intersection or slope computation.

This reduces the problem to computing distances and a single determinant. The brute-force geometric construction becomes unnecessary once we recognize that all required quantities can be derived from dot products and cross products in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Perpendicular bisectors intersection | O(1) | O(1) | Risky |
| Coordinate geometry formula (abc / 4S) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We denote the three points as A, B, and C.

1. Compute the side lengths AB, BC, and CA using Euclidean distance. Each distance comes directly from the coordinate definition of the norm of a vector difference. This gives the three edges of the triangle without any geometric construction.
2. Compute the area of triangle ABC using the absolute value of the cross product of vectors AB and AC, divided by 2. The cross product in 2D acts as a signed area measure of the parallelogram formed by the vectors, and halving it gives the triangle area.
3. Substitute the computed values into the circumradius formula R = (AB × BC × CA) / (4 × area). This step is purely algebraic and avoids introducing any new geometric objects.
4. Output R as a floating-point number with sufficient precision, typically at least 1e-6 accuracy to satisfy the requirement of 4 decimal places.

Why it works comes from a standard identity in Euclidean geometry. The circumradius formula connects side lengths and area through the sine law. Since the area can be expressed as (ab sin C)/2, substituting into the sine law relations eliminates angles entirely and yields R = abc / (4S). Because both numerator and denominator are derived directly from coordinate invariants (distances and determinant-based area), the result is independent of coordinate orientation and numerically stable as long as standard double precision is used.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dist2(ax, ay, bx, by):
    dx = ax - bx
    dy = ay - by
    return dx * dx + dy * dy

def dist(ax, ay, bx, by):
    return (dist2(ax, ay, bx, by)) ** 0.5

x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
x3, y3 = map(int, input().split())

a = dist(x2, y2, x3, y3)
b = dist(x1, y1, x3, y3)
c = dist(x1, y1, x2, y2)

cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
area = abs(cross) / 2.0

r = (a * b * c) / (4.0 * area)

print(r)
```

The implementation follows the algorithm directly. Distances are computed using standard Euclidean norm. The cross product is used to compute twice the signed area, which is then converted into a positive value. The final formula is applied in floating point.

One subtle point is that we compute squared differences in integers first, then apply square root once per edge. This avoids early floating-point rounding errors in intermediate steps. Another detail is taking the absolute value of the cross product before dividing, since orientation of points affects sign but not area.

## Worked Examples

### Sample 1

Input:

```
0 0
2 1
-2 1
```

| Step | AB | BC | CA | Cross | Area | Radius |
| --- | --- | --- | --- | --- | --- | --- |
| Compute values | 2.236 | 4.000 | 4.472 | 4 | 2 | 2.5 |

The triangle is symmetric around the y-axis, and the area computed via cross product is cleanly 2. Substituting into the formula gives a stable exact value. This confirms that the method handles symmetric configurations without special casing.

### Sample 2

Input:

```
0 10
0 0
12 4
```

| Step | AB | BC | CA | Cross | Area | Radius |
| --- | --- | --- | --- | --- | --- | --- |
| Compute values | 10 | 12.649 | 12.649 | 120 | 60 | 7.07107 |

Here AB is vertical, which is where slope-based methods typically fail. The cross product remains stable since it does not rely on division. The resulting radius matches a known 45-degree geometry pattern, confirming correctness even under axis-aligned degeneracy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and square roots are performed |
| Space | O(1) | No auxiliary structures beyond a fixed number of variables |

The constraints allow a constant-time geometric computation, and the solution comfortably fits within both time and memory limits since it performs only a handful of floating-point operations.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())
    x3, y3 = map(int, input().split())

    def dist(ax, ay, bx, by):
        return math.hypot(ax - bx, ay - by)

    a = dist(x2, y2, x3, y3)
    b = dist(x1, y1, x3, y3)
    c = dist(x1, y1, x2, y2)

    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    area = abs(cross) / 2.0

    r = (a * b * c) / (4.0 * area)
    return f"{r:.6f}"

# provided samples
assert abs(float(run("0 0\n2 1\n-2 1\n")) - 2.5) < 1e-6
assert abs(float(run("0 10\n0 0\n12 4\n")) - 7.07107) < 1e-4

# custom cases
assert abs(float(run("0 0\n1 0\n0 1\n")) - math.sqrt(2)/2) < 1e-6
assert abs(float(run("0 0\n4 0\n0 3\n")) - 2.5) < 1e-6
assert abs(float(run("1 1\n2 3\n5 2\n")) > 0)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| right triangle (0,0)-(1,0)-(0,1) | √2/2 | basic correctness |
| 3-4-5 triangle | 2.5 | classic known case |
| general triangle | positive radius | non-degenerate handling |

## Edge Cases

One fragile case class is when the triangle is nearly collinear. For example:

```
0 0
1000 0
1000 1
```

The cross product is small but non-zero. The algorithm computes area as 500, so it remains stable and produces a large but valid circumradius. The key point is that division by a small area is expected and correct, not a numerical failure.

Another case is vertical alignment:

```
0 0
0 10
3 4
```

Here AB is vertical, so slope-based methods would fail. The algorithm instead uses distance and cross product only. The cross product is computed purely via multiplication, so no division instability occurs. The output remains consistent with geometric expectation.

A final case is very symmetric triangles, where floating-point rounding can accumulate:

```
-1000 -1000
1000 -1000
0 1000
```

The distances are large but still within safe floating-point range. The cross product gives a clean integer area, and the final division produces a stable radius.
