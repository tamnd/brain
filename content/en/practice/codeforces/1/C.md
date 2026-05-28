---
title: "CF 1C - Ancient Berland Circus"
description: "We are given the coordinates of three vertices of some regular polygon. The polygon itself is unknown: we do not know ho"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 1"
rating: 2100
weight: 1
solve_time_s: 100
verified: true
draft: false
---
## Solution
## Problem Understanding

We are given the coordinates of three vertices of some regular polygon. The polygon itself is unknown: we do not know how many sides it has, where its center is, or which vertices the three points correspond to. Among all regular polygons that could contain these three points as vertices, we must find the one with the smallest area.

The key geometric fact is that every regular polygon has a circumcircle. All vertices lie on the same circle, equally spaced by angle. Since three non-collinear points uniquely determine a circle, the three pillars already fix the circumcircle completely. The only remaining question is how many equally spaced vertices exist on that circle so that all three given points land on vertex positions.

The constraints are tiny in terms of input size, there are only three points. The challenge is entirely mathematical. A brute-force search over all polygons up to 100 sides is completely feasible, but we still need a reliable geometric characterization of when three points can belong to the same regular polygon.

Floating point precision is the dangerous part of this problem. The correct polygon may depend on angles like π/7 or π/13, and direct equality checks will fail because of rounding error. Another subtle issue is that the three points are not guaranteed to be adjacent vertices. A naive solution that assumes consecutive vertices immediately produces wrong answers.

Consider this example:

```
0 0
1 0
0 1
```

These three points form a right triangle. A careless approach might assume the polygon is a triangle because three vertices are known. But these points are actually vertices of a square, whose area is smaller than the circumscribed equilateral triangle through the same points.

Another tricky situation appears when the polygon has many sides and the central angles become very small. For example, if the true polygon has 97 sides, accumulated floating point error in repeated angle computations can easily make a gcd-style angle reduction unstable unless we use an epsilon carefully.

A third common mistake is computing the circumcenter incorrectly for nearly degenerate triangles. Even though the input guarantees a valid answer, unstable formulas can produce huge precision loss if implemented carelessly.

## Approaches

The brute-force idea starts from the observation that the number of polygon sides is at most 100. We can try every possible `n` from 3 to 100.

For a fixed `n`, a regular `n`-gon divides the circle into arcs of angle `2π/n`. If the three given points are vertices of that polygon, then the central angles between every pair of points must be integer multiples of `2π/n`.

So the brute-force algorithm looks like this:

1. Compute the circumcenter and circumradius of the three points.
2. Compute the polar angle of each point around the center.
3. For every `n` from 3 to 100:

- Check whether all pairwise angle differences are multiples of `2π/n`.
- If yes, compute the polygon area.
4. Output the minimum area.

This already works within limits. We only test 98 polygon sizes, and each test uses constant-time geometry. The total work is negligible.

The real challenge is not speed but correctness. Comparing floating point angles against exact multiples is fragile. If we check:

```
diff % step == 0
```

the solution fails immediately because of precision noise.

The important insight is that the polygon structure can be described through the greatest common divisor of central angles.

Suppose the three points correspond to vertices separated by `a`, `b`, and `c` steps on the polygon. Their central angles are:

```
a * 2π/n
b * 2π/n
c * 2π/n
```

That means every angle difference must share the same fundamental unit angle. The smallest valid polygon is exactly the one whose unit angle is the gcd of all central angle differences.

In integer arithmetic we use Euclid's algorithm for gcd. For floating point angles, we simulate the same idea numerically. Since `n ≤ 100`, an even simpler strategy is enough: try every `n` and verify whether all angles are integer multiples of `2π/n` within epsilon.

Once the correct `n` is known, the polygon area follows from a standard decomposition into isosceles triangles. A regular `n`-gon with circumradius `R` has area:

$A = \frac{nR^2\sin\left(\frac{2\pi}{n}\right)}{2}$

The brute-force and optimal approaches are effectively the same asymptotically because the side limit is only 100. The optimality comes from the geometric insight that reduces the validation of a polygon to angle divisibility on the circumcircle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all polygons with naive angle checks | O(100) | O(1) | Risky due to precision |
| Geometric angle divisibility with epsilon | O(100) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three points.

The three points uniquely determine a circumcircle because they are guaranteed to be non-collinear.
2. Compute the side lengths of the triangle formed by the points.

We need these lengths to compute the circumradius using the triangle area formula.
3. Compute the triangle area using the cross product.

If the triangle vertices are `A`, `B`, and `C`, then:

$\text{Area} = \frac{|(B-A) \times (C-A)|}{2}$
4. Compute the circumradius `R`.

Using the standard relation:

$R = \frac{abc}{4\Delta}$

where `a`, `b`, and `c` are the side lengths and `Δ` is the triangle area.
5. Compute the three central angles.

Each side of the triangle subtends some angle at the circumcenter. By the extended law of sines:

$\theta = 2\arcsin\left(\frac{a}{2R}\right)$

We compute this for all three triangle sides.
6. Try every polygon size `n` from 3 to 100.

The basic angle step of a regular `n`-gon is:

$\frac{2\pi}{n}$
7. For each central angle, check whether it is an integer multiple of the step angle.

We compute:

```
ratio = angle / step
```

and verify that `ratio` is sufficiently close to an integer.
8. The first valid `n` gives the smallest area.

A larger `n` means more sides on the same circumcircle, which always increases the polygon area toward the circle area.
9. Compute the area of the regular polygon using the circumradius formula.
10. Print the answer with enough precision.

### Why it works

The three points lie on a unique circumcircle. Any regular polygon containing them must use this exact circle as its circumcircle.

A regular `n`-gon partitions the circle into equal angular steps of `2π/n`. So every arc between two polygon vertices must be an integer multiple of that step. The three given points determine three central angles, and these angles must all be divisible by the same fundamental step angle.

By checking every `n` from smallest to largest, the first valid polygon is guaranteed to have minimum area. For a fixed circumradius, increasing the number of sides strictly increases the regular polygon area.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

EPS = 1e-6

def dist(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

def is_multiple(angle, step):
    k = round(angle / step)
    return abs(angle - k * step) < EPS

def solve():
    points = [tuple(map(float, input().split())) for _ in range(3)]

    (x1, y1), (x2, y2), (x3, y3) = points

    a = dist(x2, y2, x3, y3)
    b = dist(x1, y1, x3, y3)
    c = dist(x1, y1, x2, y2)

    cross = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
    triangle_area = cross / 2.0

    R = (a * b * c) / (4.0 * triangle_area)

    angles = []
    for side in [a, b, c]:
        value = side / (2.0 * R)
        value = max(-1.0, min(1.0, value))
        angles.append(2.0 * math.asin(value))

    answer = 0.0

    for n in range(3, 101):
        step = 2.0 * math.pi / n

        ok = True

        for angle in angles:
            if not is_multiple(angle, step):
                ok = False
                break

        if ok:
            answer = 0.5 * n * R * R * math.sin(2.0 * math.pi / n)
            break

    print(f"{answer:.10f}")

solve()
```

The first section computes the triangle side lengths and area. The cross product formula is numerically stable and avoids Heron's formula, which can lose precision for skinny triangles.

The circumradius computation uses the classic relation between side lengths and triangle area. Since all coordinates are small, floating point overflow is not a concern.

The central angles are derived from chord lengths. For a chord of length `a` in a circle of radius `R`, the corresponding central angle satisfies:

```
a = 2R sin(theta / 2)
```

We invert this relation using `asin`. The clamp to `[-1, 1]` is important because floating point error can produce values like `1.0000000002`, which would crash `asin`.

The validation step checks whether each angle is a multiple of the polygon step angle. We round the ratio to the nearest integer and compare the reconstruction error against epsilon. Direct modulus operations on floating point numbers are much less reliable.

The loop starts from `n = 3`, so the first valid polygon automatically has minimum area.

## Worked Examples

### Example 1

Input:

```
0 0
1 1
0 1
```

The points form three vertices of a square.

| Variable | Value |
| --- | --- |
| a | 1 |
| b | 1 |
| c | √2 |
| Triangle area | 0.5 |
| Circumradius R | 0.70710678 |

The central angles become:

| Side | Central angle |
| --- | --- |
| 1 | π/2 |
| 1 | π/2 |
| √2 | π |

Now we test polygon sizes:

| n | Step angle | Valid? |
| --- | --- | --- |
| 3 | 2π/3 | No |
| 4 | π/2 | Yes |

Area:

| Formula result |
| --- |
| 1.0 |

This trace shows why the polygon is not necessarily a triangle. The three points align perfectly with the vertex spacing of a square.

### Example 2

Input:

```
1 0
0 1
-1 0
```

These are three vertices of a regular hexagon on the unit circle.

| Variable | Value |
| --- | --- |
| a | √2 |
| b | 2 |
| c | √2 |
| Triangle area | 1 |
| Circumradius R | 1 |

Central angles:

| Side | Central angle |
| --- | --- |
| √2 | π/2 |
| 2 | π |
| √2 | π/2 |

Polygon search:

| n | Step angle | Valid? |
| --- | --- | --- |
| 3 | 2π/3 | No |
| 4 | π/2 | Yes |

Area:

| Formula result |
| --- |
| 2.0 |

This example demonstrates that multiple polygons may contain the same three points. A hexagon works, but the square appears earlier and has smaller area.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100) | We test at most 98 polygon sizes |
| Space | O(1) | Only a few floating point variables are stored |

The runtime is effectively constant. Even Python handles this instantly because all computations are basic trigonometric operations on a fixed number of values. The memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    EPS = 1e-6

    def dist(x1, y1, x2, y2):
        return math.hypot(x1 - x2, y1 - y2)

    def is_multiple(angle, step):
        k = round(angle / step)
        return abs(angle - k * step) < EPS

    points = [tuple(map(float, input().split())) for _ in range(3)]

    (x1, y1), (x2, y2), (x3, y3) = points

    a = dist(x2, y2, x3, y3)
    b = dist(x1, y1, x3, y3)
    c = dist(x1, y1, x2, y2)

    cross = abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
    triangle_area = cross / 2.0

    R = (a * b * c) / (4.0 * triangle_area)

    angles = []

    for side in [a, b, c]:
        value = side / (2.0 * R)
        value = max(-1.0, min(1.0, value))
        angles.append(2.0 * math.asin(value))

    answer = 0.0

    for n in range(3, 101):
        step = 2.0 * math.pi / n

        ok = True

        for angle in angles:
            if not is_multiple(angle, step):
                ok = False
                break

        if ok:
            answer = 0.5 * n * R * R * math.sin(2.0 * math.pi / n)
            break

    return f"{answer:.8f}"

# provided sample
assert run(
"""0 0
1 1
0 1
"""
) == "1.00000000", "sample 1"

# equilateral triangle
assert run(
"""0 0
1 0
0.5 0.8660254038
"""
) == "0.43301270", "equilateral triangle"

# square on unit circle
assert run(
"""1 0
0 1
-1 0
"""
) == "2.00000000", "square"

# regular hexagon vertices
assert run(
"""1 0
0.5 0.8660254038
-0.5 0.8660254038
"""
) == "2.59807621", "hexagon"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | 1.00000000 | Basic correctness |
| Equilateral triangle | 0.43301270 | Smallest possible polygon |
| Unit circle square points | 2.00000000 | Non-adjacent vertices |
| Hexagon vertices | 2.59807621 | Larger regular polygons |

## Edge Cases

A common failure case is assuming the three points are consecutive vertices.

Input:

```
0 0
1 1
0 1
```

The triangle formed by these points is not regular. A naive algorithm might stop at `n = 3` and compute the circumtriangle area. Our algorithm instead checks divisibility of central angles. The triangle fails because the angles are not multiples of `2π/3`. The square succeeds because all angles are multiples of `π/2`.

Another subtle case is when floating point rounding pushes values slightly outside valid trigonometric ranges.

Input:

```
1 0
-1 0
0 1
```

Mathematically, one chord length equals exactly `2R`, so the expression inside `asin` should be exactly `1`. Floating point arithmetic may produce `1.0000000001`. Without clamping, `asin` throws a domain error. The implementation explicitly bounds the value to `[-1, 1]`.

A third dangerous scenario is polygons with many sides, where angular steps become tiny.

Input:

```
1 0
0.9980267284 0.0627905195
0.9921147013 0.1253332336
```

These are consecutive vertices of a regular 100-gon. Direct equality checks on floating point angles fail because the computed angles contain accumulated numerical noise. The epsilon-based integer multiple check correctly recognizes the polygon structure.
