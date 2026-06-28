---
title: "CF 104804G - \u041e, \u043d\u0435\u0442! \u0413\u0435\u043e\u043c\u0430!!!"
description: "We are given three points in the plane, each described by integer coordinates. The points are guaranteed not to lie on the same straight line, so they form a valid triangle. The task is to construct the unique circle that passes through all three points and compute its radius."
date: "2026-06-28T16:52:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "G"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 77
verified: false
draft: false
---

[CF 104804G - \u041e, \u043d\u0435\u0442! \u0413\u0435\u043e\u043c\u0430!!!](https://codeforces.com/problemset/problem/104804/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three points in the plane, each described by integer coordinates. The points are guaranteed not to lie on the same straight line, so they form a valid triangle. The task is to construct the unique circle that passes through all three points and compute its radius.

Geometrically, this is asking for the circumradius of a triangle defined by three vertices. The output is a single real number, the radius of that circumcircle, printed with sufficient precision.

The constraints are small: coordinates are integers with absolute value at most 1000. This immediately tells us that any arithmetic involving pairwise distances or areas is safe in floating point if handled carefully. There is no need for integer overflow concerns beyond standard 64-bit safety, and no performance pressure since we only process one triangle.

The main subtle failure cases come from degenerate or numerically unstable configurations rather than performance.

A first edge case is when the triangle is almost degenerate, meaning the points are very close to collinear. Even though the problem guarantees non-collinearity, the area can be very small, which can amplify floating-point error in formulas that divide by area.

For example, consider points:

```
(0, 0)
(1000, 1)
(2000, 2)
```

This is not strictly allowed since they are collinear, but a near-collinear valid case like:

```
(0, 0)
(1000, 1)
(2000, 3)
```

produces a very large circumradius. Any formula that divides by triangle area must handle small denominators carefully.

Another issue is incorrect use of squared distances versus actual distances. If a solution forgets the square root in intermediate steps or mixes squared and unsquared quantities, it will silently produce wrong scaling.

## Approaches

A brute-force geometric approach would try to construct the circumcircle explicitly by finding the intersection of perpendicular bisectors of two sides. Each bisector is a line, so we compute midpoints, slopes, then solve a 2x2 linear system. This is correct and conceptually straightforward, but it introduces multiple divisions and special cases for vertical lines. It also risks numerical instability when slopes are large or nearly equal.

The more robust insight is to avoid explicit construction of the circle center entirely. Instead, we use a direct formula for the circumradius of a triangle. If the triangle has side lengths $a$, $b$, $c$, and area $S$, then the circumradius is

$$R = \frac{abc}{4S}.$$

This is the key simplification. The triangle structure gives us everything we need through distances and area alone, avoiding coordinate geometry edge cases like perpendicular bisector intersection.

We compute side lengths using Euclidean distance, and compute area using the cross product of two sides. The cross product gives twice the area directly, which eliminates the need for Heron’s formula and reduces numerical error.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Perpendicular bisectors | O(1) | O(1) | Risky due to precision and special cases |
| Distance + area formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three points $A(x_1, y_1)$, $B(x_2, y_2)$, and $C(x_3, y_3)$. These define a triangle in the plane.
2. Compute the side lengths $a = BC$, $b = CA$, and $c = AB$ using Euclidean distance. Each is computed as a square root of squared coordinate differences. This is necessary because the circumradius formula depends on actual geometric lengths, not squared values.
3. Compute the area of triangle $ABC$ using the cross product:

$$S = \frac{1}{2} |(B - A) \times (C - A)|.$$

The cross product gives twice the signed area, and taking absolute value ensures positivity regardless of orientation.
4. Compute the circumradius using:

$$R = \frac{a \cdot b \cdot c}{4S}.$$

This formula comes from standard triangle geometry and avoids explicitly solving for the circle center.
5. Print $R$ with sufficient floating-point precision, typically at least 5 to 10 decimal places to satisfy the requirement.

### Why it works

The circumcircle of a triangle is uniquely determined by its three vertices. The formula $R = \frac{abc}{4S}$ is derived from the relationship between a triangle’s area and its circumscribed circle. The cross product correctly computes the exact geometric area from coordinates, and Euclidean distances give exact side lengths. Since all computations are derived directly from geometric invariants of the triangle, any consistent implementation must yield the same radius regardless of coordinate order or orientation.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def dist(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
x3, y3 = map(int, input().split())

a = dist(x2, y2, x3, y3)
b = dist(x1, y1, x3, y3)
c = dist(x1, y1, x2, y2)

cross = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
area = cross / 2.0

R = (a * b * c) / (4.0 * area)

print(R)
```

The implementation directly follows the algorithm structure. The `math.hypot` function is used instead of manual squaring and square root because it is more numerically stable and avoids overflow or precision loss in intermediate squaring.

The cross product is computed from two vectors originating at the first point. This avoids any need for angle computations or trigonometric functions. Dividing by 2 converts the parallelogram area into triangle area.

The final formula is applied exactly as derived. The division by $4 \cdot area$ is safe because the problem guarantees non-collinearity, so the area is strictly positive.

## Worked Examples

### Sample 1

Input:

```
0 0
2 1
-2 1
```

We compute step by step:

| Step | Value |
| --- | --- |
| A | (0, 0) |
| B | (2, 1) |
| C | (-2, 1) |
| a = BC | 4.0 |
| b = CA | sqrt( (0+2)^2 + (0-1)^2 ) = sqrt(5) |
| c = AB | sqrt( (0-2)^2 + (0-1)^2 ) = sqrt(5) |
| cross |  |
| area | 2 |
| R | (4 * sqrt(5) * sqrt(5)) / (8) = 20 / 8 = 2.5 |

This confirms a symmetric triangle where two sides are equal, producing a clean rational radius.

### Sample 2

Input:

```
0 10
0 0
12 4
```

| Step | Value |
| --- | --- |
| A | (0, 10) |
| B | (0, 0) |
| C | (12, 4) |
| a = BC | sqrt(144 + 16) = sqrt(160) |
| b = CA | sqrt(144 + 36) = sqrt(180) |
| c = AB | 10 |
| cross |  |
| area | 60 |
| R | sqrt(160)*sqrt(180)*10 / 240 ≈ 7.07107 |

This example shows a non-symmetric triangle where direct geometric computation is essential. The cross product correctly captures orientation-independent area.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic operations on three points |
| Space | O(1) | No auxiliary data structures are used |

The computation is purely geometric and independent of input size, so it trivially satisfies any reasonable constraints.

## Test Cases

```python
import sys, io, math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import hypot

    x1, y1 = map(int, sys.stdin.readline().split())
    x2, y2 = map(int, sys.stdin.readline().split())
    x3, y3 = map(int, sys.stdin.readline().split())

    def dist(a, b, c, d):
        return math.hypot(a - c, b - d)

    a = dist(x2, y2, x3, y3)
    b = dist(x1, y1, x3, y3)
    c = dist(x1, y1, x2, y2)

    cross = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
    area = cross / 2.0

    return str((a * b * c) / (4.0 * area))

# provided samples
assert abs(float(run("0 0\n2 1\n-2 1\n")) - 2.5) < 1e-6
assert abs(float(run("0 10\n0 0\n12 4\n")) - 7.07107) < 1e-3

# custom cases
assert abs(float(run("0 0\n1 0\n0 1\n")) - math.sqrt(2)/2) < 1e-6, "right triangle"
assert abs(float(run("0 0\n2 0\n1 2\n")) - (2*math.sqrt(5)*math.sqrt(5)) / (4*2)) < 1e-6, "simple triangle"
assert abs(float(run("0 0\n1000 0\n0 1000\n")) - (1000*math.sqrt(2)/2)) < 1e-6, "large coordinates"
assert abs(float(run("0 1\n2 3\n4 0\n")) > 0), "general case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| right triangle | √2/2 | basic geometric correctness |
| simple triangle | computed formula | consistency of formula implementation |
| large coordinates | large radius | numeric stability under bounds |
| general case | positive value | non-degenerate handling |

## Edge Cases

A near-degenerate triangle is the main stress case. For example:

```
0 0
1000 1
2000 3
```

The algorithm computes a very small cross product, which leads to a large radius. The steps still behave correctly because the area is derived directly from the determinant formula, which remains stable under integer arithmetic until the final division.

The computation proceeds as follows. The cross product is non-zero, so area is positive. Side lengths are computed normally via Euclidean distance. The final division amplifies the result but does not break correctness, only precision may require careful floating-point handling.

This confirms that the method is robust even when the triangle becomes extremely thin, as long as collinearity is excluded.
