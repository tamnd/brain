---
title: "CF 102267H - Circle of Polygon"
description: "We have a regular polygon with (V) vertices, where every side has length (S). Because the polygon is regular, all of its vertices lie on one circle centered at the polygon's center. The task is to compute the area of that circle."
date: "2026-08-17T19:24:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102267
codeforces_index: "H"
codeforces_contest_name: "The 2019 University of Jordan Collegiate Programming Contest"
rating: 0
weight: 102267
solve_time_s: 194
verified: false
draft: false
---

[CF 102267H - Circle of Polygon](https://codeforces.com/problemset/problem/102267/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We have a regular polygon with (V) vertices, where every side has length (S). Because the polygon is regular, all of its vertices lie on one circle centered at the polygon's center. The task is to compute the area of that circle.

The key quantity is the circumradius (R), the distance from the center of the polygon to any vertex. Once (R) is known, the requested area is simply

[
A=\pi R^2.
]

The number of vertices satisfies (3\le V\le359), so even a linear or quadratic algorithm would be small enough in practice. The side length can be as large as (10^9), so intermediate values can be around (10^{18}). Python integers handle such values safely, and the final computation uses floating-point trigonometric functions because the answer requires numerical precision.

The interesting part is not the size of the input, but recognizing the geometry. A regular polygon can be divided into (V) identical isosceles triangles by connecting its center to every vertex. Each triangle has two sides equal to (R), while its base is the polygon side (S). The angle at the center is (2\pi/V).

There are a few cases where careless geometry can silently produce the wrong answer. For example, with input `3 2`, the polygon is an equilateral triangle. Its circumradius is (2/\sqrt3), so the circle's area is (4\pi/3), approximately (4.188790205). Using (S/\sin(\pi/V)) instead of (S/(2\sin(\pi/V))) would make the radius twice as large and the area four times too large.

Another common mistake is using degrees with a trigonometric function that expects radians. For `8 2`, the relevant angle is (\pi/8), not (22.5) passed directly to `sin`. The correct answer is approximately `21.452136491`.

The upper bound (V=359) also means there is no need for special handling of very large polygons. The formula remains numerically well behaved throughout the allowed range because (\sin(\pi/V)) is positive for every permitted (V).

## Approaches

A direct geometric implementation could explicitly construct the (V) vertices around a circle, calculate their coordinates, and then recover the radius or verify the side length. That approach is correct because a regular polygon is completely determined by its circumradius and angular spacing. It takes (O(V)) work and (O(V)) memory if all vertices are stored. At the maximum (V=359), that means only 359 vertices, so this approach is easily fast enough under the given constraints.

A more elaborate brute-force approach could search for the radius numerically. For every candidate radius, we could calculate the corresponding side length (2R\sin(\pi/V)), then use binary search until the radius is sufficiently accurate. With, for example, 60 iterations, this requires about (60) trigonometric evaluations, or (60) evaluations if the constant angle is precomputed. Even this is easily within the limit.

So unlike many Codeforces problems, the constraints do not actually make a brute-force construction too slow. The optimal solution comes from removing unnecessary computation rather than rescuing an algorithm that would time out. The structure of a regular polygon gives an exact formula for the radius, so there is no reason to construct vertices or perform numerical search.

Consider one of the (V) triangles formed by the center and two neighboring vertices. Its two equal sides have length (R), its base has length (S), and its vertex angle at the center is (2\pi/V). Splitting that triangle down the middle creates a right triangle with hypotenuse (R), opposite side (S/2), and angle (\pi/V). Thus

[
\sin\left(\frac{\pi}{V}\right)=\frac{S/2}{R}.
]

Rearranging gives

[
R=\frac{S}{2\sin(\pi/V)}.
]

Substituting this into the circle-area formula gives

[
A=\pi\left(\frac{S}{2\sin(\pi/V)}\right)^2.
]

The entire problem is consequently reduced to one sine evaluation and a few arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Explicitly construct polygon | (O(V)) | (O(V)) | Accepted, but unnecessary |
| Numerical radius search | (O(K)) | (O(1)) | Accepted, but unnecessary |
| Geometry formula | (O(1)) | (O(1)) | Accepted |

Here (K) is the number of iterations used by a numerical search. The formula-based solution is preferable because it is exact up to the precision of the standard floating-point trigonometric function and has no convergence parameter.

## Algorithm Walkthrough

1. Read (V), the number of polygon vertices, and (S), the common side length.
2. Compute the half-angle

[
\theta=\frac{\pi}{V}.
]

Each central angle is (2\pi/V), and splitting one of the corresponding isosceles triangles in half gives the angle (\pi/V).

1. Compute the circumradius using

[
R=\frac{S}{2\sin\theta}.
]

The half-side (S/2) is opposite (\theta) in the resulting right triangle, while (R) is its hypotenuse.

1. Compute the area of the circumcircle as

[
A=\pi R^2.
]

1. Print the result as a floating-point number. Python's `float` provides substantially more precision than the (10^{-6}) tolerance requires.

Why it works

The invariant behind the derivation is that every pair of neighboring vertices and the polygon center forms the same isosceles triangle. Its central angle is exactly (2\pi/V), and halving it produces a right triangle whose opposite side is exactly half of the polygon's side. The sine relationship consequently determines the same radius for every vertex:

[
S/2=R\sin(\pi/V).
]

The computed (R) is thus the actual distance from the polygon center to every vertex, which is precisely the radius of the circumscribed circle. Squaring that radius and multiplying by (\pi) gives the required area.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

v, s = map(int, input().split())

angle = math.pi / v
radius = s / (2.0 * math.sin(angle))
area = math.pi * radius * radius

print("{:.10f}".format(area))
```

The input is read once because the problem contains a single polygon. `math.pi / v` computes the half of one central angle, which is the angle required by the right-triangle derivation.

The denominator is `2.0 * math.sin(angle)`. The factor of two comes from the fact that the right triangle contains half of the polygon side, (S/2). Omitting this factor is the most direct formula error for this problem.

The radius is squared before multiplying by (\pi), exactly matching (A=\pi R^2). Python does not suffer from integer overflow here because the calculation is performed with floating-point values, and Python integers would also grow automatically if integer intermediates were used.

Printing ten digits after the decimal point is comfortably more precise than the required (10^{-6}) absolute or relative error.

## Worked Examples

For the provided sample, the input is `8 2`. The half central angle is (\pi/8), so the radius is

[
R=\frac{2}{2\sin(\pi/8)}
=\frac{1}{\sin(\pi/8)}
\approx2.6131259298.
]

The resulting area is approximately (21.452136491).

| Step | (V) | (S) | (\theta=\pi/V) | (R=S/(2\sin\theta)) | Area |
| --- | --- | --- | --- | --- | --- |
| Read input | 8 | 2 |  |  |  |
| Compute angle | 8 | 2 | 0.3926990817 |  |  |
| Compute radius | 8 | 2 | 0.3926990817 | 2.6131259298 |  |
| Compute area | 8 | 2 | 0.3926990817 | 2.6131259298 | 21.452136491 |

This trace shows why the central angle must be divided by two before applying the sine. The full central angle is (\pi/4), but the right triangle uses (\pi/8).

For a second example, consider `3 2`. This is an equilateral triangle. The half central angle is (\pi/3), whose sine is (\sqrt3/2). Hence

[
R=\frac{2}{2(\sqrt3/2)}
=\frac{2}{\sqrt3},
]

and the circle area is (4\pi/3), approximately (4.1887902048).

| Step | (V) | (S) | (\theta=\pi/V) | (R=S/(2\sin\theta)) | Area |
| --- | --- | --- | --- | --- | --- |
| Read input | 3 | 2 |  |  |  |
| Compute angle | 3 | 2 | 1.0471975512 |  |  |
| Compute radius | 3 | 2 | 1.0471975512 | 1.1547005384 |  |
| Compute area | 3 | 2 | 1.0471975512 | 1.1547005384 | 4.1887902048 |

This example exercises the minimum allowed number of vertices. It also confirms that the formula works for the smallest regular polygon allowed by the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Only one trigonometric evaluation and a constant number of arithmetic operations are performed. |
| Space | (O(1)) | Only the input values, angle, radius, and area are stored. |

The constraints allow even (O(V)) work because (V\le359), but the formula-based solution is constant time regardless of the polygon size. Its memory usage is also constant, and the numerical precision of Python's double-precision floating point is sufficient for the required (10^{-6}) tolerance.

## Test Cases

The test harness below compares floating-point results with a tolerance instead of requiring identical decimal strings. This is the correct way to test a numerical geometry solution because different valid implementations can print slightly different last digits.

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline
    v, s = map(int, input().split())

    angle = math.pi / v
    radius = s / (2.0 * math.sin(angle))
    area = math.pi * radius * radius

    print("{:.10f}".format(area))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def assert_close(inp: str, expected: float, message: str):
    actual = float(run(inp))
    assert abs(actual - expected) <= 1e-6 * max(1.0, abs(expected)), message

# Provided sample
assert_close(
    "8 2\n",
    21.452136491,
    "sample 1"
)

# Minimum number of vertices
assert_close(
    "3 2\n",
    4.1887902047863905,
    "minimum vertices"
)

# A square with side 2 has circumradius sqrt(2)
assert_close(
    "4 2\n",
    2.0 * math.pi,
    "square"
)

# Maximum number of vertices and maximum side length
v = 359
s = 10**9
expected = math.pi * (s / (2.0 * math.sin(math.pi / v))) ** 2
assert_close(
    f"{v} {s}\n",
    expected,
    "maximum constraints"
)

# Smallest side length
assert_close(
    "3 1\n",
    math.pi / 3.0,
    "minimum side length"
)

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `8 2` | `21.452136491` | Provided sample and general formula |
| `3 2` | `4.188790205` | Minimum number of vertices |
| `4 2` | `6.283185307` | Square geometry and central-angle handling |
| `359 1000000000` | Approximately (4.09\times10^{19}) | Maximum constraints and large numerical values |
| `3 1` | `1.047197551` | Minimum side length |

The maximum-size case is particularly useful for detecting implementations that accidentally use integer arithmetic for the trigonometric part or lose too much precision while squaring a large radius.

## Edge Cases

For the minimum polygon, the input `3 2` gives an equilateral triangle. The algorithm computes (\theta=\pi/3), so (\sin\theta=\sqrt3/2). The radius becomes (2/(2\cdot\sqrt3/2)=2/\sqrt3), and the area is (4\pi/3\approx4.188790205). A formula missing the factor of two would return four times this area.

For the square `4 2`, the half central angle is (\pi/4). Since (\sin(\pi/4)=\sqrt2/2), the radius is (2/(2\cdot\sqrt2/2)=\sqrt2). The circle area is consequently (2\pi\approx6.283185307). This is a useful check for accidentally using the full central angle instead of half of it.

For the largest permitted polygon, `359 1000000000`, the half central angle is very small, but still safely positive. The sine function returns a sufficiently accurate value, and the resulting radius is large because the polygon has a huge side length. Python's floating-point representation can comfortably handle the resulting area, which is on the order of (10^{19}).

For the smallest side length, `3 1`, the same triangle calculation gives (R=1/\sqrt3) and area (\pi/3\approx1.047197551). This confirms that there is no special case tied to the magnitude of (S); the formula scales quadratically with the side length.

The other common failure is passing degrees to `sin`. For `8 2`, the correct argument is (\pi/8\approx0.392699) radians. Passing `22.5` directly to Python's `math.sin` would interpret it as radians and produce an unrelated value. The implementation avoids that error by deriving the angle directly from `math.pi`.
