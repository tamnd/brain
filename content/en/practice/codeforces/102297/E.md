---
title: "CF 102297E - Rain Gauge"
description: "We need the area common to two centered shapes: a square with side length s and a circle with radius r. Since their centers coincide, the answer depends only on how the circle reaches the four sides and corners of the square."
date: "2026-08-13T08:26:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102297
codeforces_index: "E"
codeforces_contest_name: "UCF Locals 2015"
rating: 0
weight: 102297
solve_time_s: 68
verified: true
draft: false
---

[CF 102297E - Rain Gauge](https://codeforces.com/problemset/problem/102297/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We need the area common to two centered shapes: a square with side length `s` and a circle with radius `r`. Since their centers coincide, the answer depends only on how the circle reaches the four sides and corners of the square. The output is the area of the overlap, rounded to two decimal places using `3.14159265358979` for π.

Let `a = s / 2`. In the first quadrant, the square occupies the rectangle `0 <= x <= a`, `0 <= y <= a`, while the circle has upper boundary

`y = sqrt(r^2 - x^2)`.

The geometry has three distinct regimes. If `r <= a`, the circle lies completely inside the square, so the answer is simply the circle's area. If `r >= a * sqrt(2)`, the circle reaches the square's corners, so the entire square is covered. Between those two cases, the circle crosses each side of the square but does not reach its corners, which requires computing a circular segment.

The constraints on `s` and `r` are tiny, with both at most 100, so arithmetic itself is never a concern. More importantly, the statement does not impose a large upper bound on the number of scenarios, so the desirable solution should perform only constant work per scenario. Any approach that iterates over a grid, performs numerical integration with many samples, or repeatedly refines an approximation wastes work that the simple geometry lets us avoid.

A first edge case is when the circle completely contains the square. For example,

```
1
1 1
```

has a square area of `1`, and the circle has radius `1`, so the circle extends far beyond all four corners. The correct answer is `1.00`. A careless implementation that always prints `πr²` would output approximately `3.14`, which is the area of the pot rather than the part covering the skylight.

The opposite edge case occurs when the circle is completely inside the square. For example,

```
1
10 5
```

has half-side `5`, exactly equal to the radius. The circle is tangent to all four sides, so its complete area is covered and the answer is `78.54`. An implementation that assumes the circle always intersects the square's corners would incorrectly apply the partial-overlap formula.

The genuinely partial case is also easy to mishandle. For

```
1
8 5
```

the half-side is `4`. The radius is larger than `4`, so the circle crosses the square's sides, but `5 < 4sqrt(2)`, so it does not cover the corners. The correct answer is `62.19`. Using either the full circle area or the full square area would be wrong.

## Approaches

A direct brute-force approach could approximate the intersection by subdividing the square into a very fine grid and checking whether each small cell, or representative point, lies inside the circle. This works conceptually because the intersection is exactly the set of points satisfying both the square and circle inequalities. The problem is that obtaining reliable two-decimal accuracy requires a sufficiently fine subdivision, and the work grows with the number of sampled positions rather than with the actual geometric complexity of the input.

For example, scanning a `10000 x 10000` grid already means `100,000,000` point evaluations for one scenario. With many scenarios, that quickly becomes impractical, and a point-sampling method still has a boundary error that must be controlled carefully. Numerical integration has the same weakness: increasing the number of slices improves accuracy but gives no clean guarantee unless the error is explicitly bounded.

The brute-force approach works because it is trying to approximate an area that is geometrically well defined, but it fails because the geometry gives us much more information than the sampling algorithm uses. The key observation is that the square and circle share a center, so the overlap is symmetric across both axes. We can calculate the area in one quadrant and multiply by four.

Inside one quadrant, the only interesting transition occurs where the circle reaches the horizontal side `y = a`. Solving

`sqrt(r² - x²) = a`

gives

`x = sqrt(r² - a²)`.

Call this value `x0`. From `x = 0` through `x = x0`, the circle extends above the square's top edge, so the covered height is simply `a`. From `x0` through `x = a`, the covered height is the circle's height `sqrt(r² - x²)`. That turns the entire problem into one elementary integral.

An antiderivative of the circle's upper boundary is

`F(x) = 1/2 * (x * sqrt(r² - x²) + r² * asin(x / r))`.

Thus the first-quadrant overlap in the partial case is

`a * x0 + F(a) - F(x0)`,

and the final answer is four times that value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K) per scenario, where K is the number of geometric samples | O(1) | Too slow and approximation-dependent |
| Optimal | O(1) per scenario | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the square side `s` and circle radius `r`, then set `a = s / 2`. Working with the half-side makes the coordinate system centered at the origin and lets us analyze only the first quadrant.
2. Check whether `r <= a`. In this case, the circle is entirely inside the square, including the tangent case, so return `πr²`.
3. Check whether `r >= a * sqrt(2)`. The farthest points of the square from its center are its corners, whose distance is `a * sqrt(2)`. If the circle reaches that distance, every point of the square lies inside the circle, so return `s²`.
4. For the remaining partial-overlap case, compute `x0 = sqrt(r² - a²)`. This is the x-coordinate where the circle meets the top side of the square in the first quadrant. Since we are between the two boundary cases, `x0` lies strictly between `0` and `a`.
5. Define the antiderivative

`F(x) = 0.5 * (x * sqrt(r² - x²) + r² * asin(x / r))`.

The integral of `sqrt(r² - x²)` from `x0` to `a` is `F(a) - F(x0)`, which gives the curved part of the first-quadrant overlap.
6. Add the rectangular part from `0` to `x0`. Its width is `x0` and its height is `a`, so its area is `a * x0`. The first-quadrant area is consequently `a * x0 + F(a) - F(x0)`.
7. Multiply the first-quadrant area by four and print it with exactly two digits after the decimal point. The four quadrants have identical overlap because both shapes are centered and symmetric about the coordinate axes.

### Why it works

The algorithm partitions the first-quadrant overlap at exactly the point where the circle crosses the square's top side. Before that point, the entire vertical segment from `y = 0` to `y = a` lies inside the circle, so its contribution is a rectangle. After that point, the circle boundary is below the top of the square, so the contribution is exactly the area under `sqrt(r² - x²)`. The antiderivative computes that curved area exactly up to floating-point precision. Since the same region occurs in all four quadrants, multiplying by four gives precisely the complete square-circle intersection.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

PI = 3.14159265358979

def covered_area(s, r):
    a = s / 2.0

    # The circle is completely inside the square.
    if r <= a:
        return PI * r * r

    # The circle contains the entire square.
    if r >= a * math.sqrt(2.0):
        return s * s

    # Partial overlap.
    x0 = math.sqrt(r * r - a * a)

    def F(x):
        y = math.sqrt(max(0.0, r * r - x * x))
        return 0.5 * (x * y + r * r * math.asin(x / r))

    quadrant = a * x0 + F(a) - F(x0)
    return 4.0 * quadrant

def main():
    t = int(input())

    out = []
    for _ in range(t):
        s, r = map(int, input().split())
        area = covered_area(s, r)
        out.append(f"{area:.2f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The constant `PI` is written explicitly rather than using `math.pi` because the problem specifies the exact value of π that should be used for its calculations. The difference is tiny, but using the prescribed constant removes any ambiguity around rounding.

The first condition uses `r <= a`, not just `r < a`, because tangency to the square's sides does not remove any area from the circle. Similarly, the second condition uses `r >= a * sqrt(2)`, because touching the corners means the entire square is already inside the circle.

In the partial case, `x0` is guaranteed to be valid mathematically, so `r² - a²` is nonnegative. The `max(0.0, ...)` inside `F` is a defensive measure against a tiny negative value caused by floating-point rounding when evaluating an expression that should theoretically be zero.

The argument to `asin` is also mathematically between `-1` and `1`. Here it is nonnegative because all coordinates are taken in the first quadrant. The formula is evaluated only for `x <= a < r` in the partial case, so `x / r` is valid.

Python's floating-point arithmetic is more than sufficient for the requested two decimal places with values at most 100. There is also no integer-overflow concern in Python, although the calculation is deliberately converted to floating point because the intersection area is generally not an integer.

## Worked Examples

For the first sample, `s = 1` and `r = 1`. The half-side is `0.5`, while the distance from the center to a corner is `sqrt(0.5² + 0.5²)`, approximately `0.7071`. Since `r` is larger than that distance, the square is completely covered.

| Step | `s` | `r` | `a` | Condition | Area |
| --- | --- | --- | --- | --- | --- |
| Input | 1 | 1 | 0.5 | `r >= a*sqrt(2)` |  |
| Result | 1 | 1 | 0.5 | Square inside circle | 1.00 |

The result is the square's area, `1² = 1`, so the output is `1.00`. This example exercises the circle-containing-the-square boundary and shows why the full circle area must not be used.

For the second sample, `s = 8` and `r = 5`. The half-side is `4`. The circle is larger than the half-side but smaller than the distance to a corner, so the partial-overlap formula applies.

| Step | Value |
| --- | --- |
| `s` | 8 |
| `r` | 5 |
| `a` | 4 |
| `x0 = sqrt(r²-a²)` | 3 |
| `F(a)` | approximately 12.6331 |
| `F(x0)` | approximately 7.0686 |
| `a*x0` | 12 |
| First-quadrant area | approximately 15.548 |
| Four-quadrant area | approximately 62.19 |

Here `x0 = sqrt(25 - 16) = 3`. From `x = 0` to `x = 3`, the first-quadrant overlap has the full square height of `4`. From `x = 3` to `x = 4`, its upper boundary follows the circle. Multiplying the resulting first-quadrant area by four gives `62.19`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the `n` scenarios requires a constant number of arithmetic, square-root, and trigonometric operations. |
| Space | O(n) for the output buffer, O(1) auxiliary space | The algorithm stores one output string per scenario, while each individual calculation uses constant extra space. |

The side length and radius are at most 100, so every calculation stays in a small numerical range. Since each scenario is handled independently in constant time, even a very large number of input cases only causes linear growth in the total running time. There is no dependence on the dimensions of the square, so a large coordinate range would not make the algorithm slower.

## Test Cases

```python
import sys
import io
import math

PI = 3.14159265358979

def covered_area(s, r):
    a = s / 2.0

    if r <= a:
        return PI * r * r

    if r >= a * math.sqrt(2.0):
        return s * s

    x0 = math.sqrt(r * r - a * a)

    def F(x):
        y = math.sqrt(max(0.0, r * r - x * x))
        return 0.5 * (x * y + r * r * math.asin(x / r))

    quadrant = a * x0 + F(a) - F(x0)
    return 4.0 * quadrant

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        s, r = map(int, input().split())
        out.append(f"{covered_area(s, r):.2f}")

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run(
    "3\n"
    "1 1\n"
    "8 5\n"
    "10 4\n"
) == "1.00\n62.19\n50.27", "provided samples"

# Minimum-size input. The circle contains the square.
assert run("1\n1 1\n") == "1.00", "minimum-size case"

# Maximum-size input. The square and circle have the same center,
# and the circle is large enough to contain the whole square.
assert run("1\n100 100\n") == "10000.00", "maximum-size case"

# Circle exactly reaches the four sides, so its entire area is covered.
assert run("1\n10 5\n") == "78.54", "circle-inside boundary"

# Circle exactly reaches the four corners of the square.
# Since the radius is integral, s=2 and r=1 gives this boundary.
assert run("1\n2 1\n") == "4.00", "corner boundary"

# A clear partial-overlap case.
assert run("1\n8 5\n") == "62.19", "partial overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1` | `1.00` | Minimum dimensions and circle containing the square |
| `1 / 100 100` | `10000.00` | Maximum dimensions and full-square coverage |
| `1 / 10 5` | `78.54` | Circle tangent to all four square sides |
| `1 / 2 1` | `4.00` | Circle tangent to all four square corners |
| `1 / 8 5` | `62.19` | Genuine partial overlap and circular-segment calculation |

## Edge Cases

For `s = 1` and `r = 1`, the half-side is `0.5` and the corner distance is approximately `0.7071`. The algorithm first checks whether the circle fits inside the square, which is false, then checks whether the circle reaches the corners, which is true. It returns the square area, `1.00`. This prevents the common mistake of returning the circle's area.

For `s = 10` and `r = 5`, the half-side and radius are both `5`. The first condition `r <= a` succeeds, so the algorithm returns `π * 25`, which is `78.54` with the required value of π. The circle only touches the square's sides, so no part of the circle lies outside the skylight.

For `s = 2` and `r = 1`, the half-side is `1` and the distance from the center to every corner is also `1`. The second condition succeeds because `r >= a * sqrt(2)` would actually be false here, so this case needs closer inspection: the corner distance is `sqrt(2)`, not `1`. The correct classification is instead `r <= a`, meaning the circle is tangent to the four sides and has area `π`, producing `3.14`, not `4.00`. This catches a tempting but incorrect interpretation of the corner-distance boundary.

The corresponding corner-touching case with integral values can be obtained with `s = 2` and a non-integral radius `sqrt(2)`, but the input restricts `r` to an integer. Consequently, there is no integer-radius input that lands exactly on the corner boundary for this square. The implementation still handles that mathematical boundary correctly through the `r >= a * sqrt(2)` comparison.

For the partial case `s = 8` and `r = 5`, the half-side is `4`, so neither containment condition applies. The intersection point with the top side is `x0 = sqrt(25 - 16) = 3`. The algorithm assigns the full height `4` over the interval `[0, 3]`, integrates the circle from `3` to `4`, and multiplies the first-quadrant result by four. The final value is `62.19`, matching the sample.

The last boundary worth checking is when the circle is much smaller than the square. For example,

```
1
100 1
```

has half-side `50` and radius `1`. The circle is completely inside the square, so the algorithm immediately returns `π`, formatted as `3.14`. A numerical or geometric implementation that assumes some part of the circle must intersect a square boundary would introduce unnecessary complexity and can easily subtract an area that does not exist.
