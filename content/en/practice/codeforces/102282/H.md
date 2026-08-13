---
title: "CF 102282H - \u0411\u0435\u0437 \u0438\u043c\u0435\u043d\u0438"
description: "We have two circles in the Cartesian plane. Each circle is described by the integer coordinates of its center and its positive integer radius. The task is to determine how many points belong to both circles and to print those points with sufficient numerical precision."
date: "2026-08-13T09:12:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "H"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 73
verified: true
draft: false
---

[CF 102282H - \u0411\u0435\u0437 \u0438\u043c\u0435\u043d\u0438](https://codeforces.com/problemset/problem/102282/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two circles in the Cartesian plane. Each circle is described by the integer coordinates of its center and its positive integer radius. The task is to determine how many points belong to both circles and to print those points with sufficient numerical precision. Two distinct circles can have zero, one, or two common points. If the two circles are actually the same circle, every point on the circle is common, so the required answer is `MANY`.

The coordinate and radius bounds are only (10^3), so the input itself is tiny. More importantly, there are only two geometric objects and the answer contains at most two finite points. A solution should consequently use a constant number of arithmetic operations rather than iterate over the plane or search for intersection points numerically. Even a simple (O(1)) geometric derivation is comfortably inside a one-second limit and uses negligible memory. Integer quantities such as squared distances are at most on the order of (10^7), so Python integer arithmetic has no overflow concern at all.

Several cases are easy to mishandle if the implementation jumps directly into the intersection formula. If the circles have the same center and the same radius, there are infinitely many common points. For example,

```
0 0 1
0 0 1
```

must produce

```
MANY
```

A formula based on dividing by the distance between centers would divide by zero here.

If the centers coincide but the radii differ, the circles have no common point. For example,

```
0 0 1
0 0 2
```

has output

```
0
```

A careless implementation that only checks whether the centers coincide could incorrectly classify this as infinitely many intersections.

Two externally tangent circles have exactly one intersection. For example,

```
0 0 1
2 0 1
```

must produce one point, `(1, 0)`. A floating-point comparison that expects two distinct roots can accidentally print the same tangent point twice.

Internal tangency has the same issue in a different configuration. For

```
0 0 3
1 0 2
```

the smaller circle touches the larger one at `(3, 0)`, so the answer is again one point.

Finally, two circles can have one center inside the other while remaining completely disjoint. For example,

```
0 0 5
1 0 1
```

has no intersection because the distance between centers is smaller than the difference of the radii. Checking only whether the center distance is less than the sum of the radii would incorrectly treat this as an intersection case.

## Approaches

A direct brute-force approach would try to search for common points by scanning the region containing both circles and testing whether a candidate point satisfies both circle equations. Since intersection coordinates are arbitrary real numbers, a grid-based implementation has to choose some numerical resolution. To guarantee coordinates within (10^{-6}), a grid with spacing around (10^{-6}) would be required. The coordinate range can span roughly 2000 units in each direction, giving about (2\cdot10^9) positions along each axis and roughly (4\cdot10^{18}) grid points in the worst case. Even checking a single point in constant time would make this approach completely infeasible, and reducing the grid resolution would no longer guarantee the required precision.

The brute-force idea works conceptually because a true intersection is exactly a point satisfying both circle equations, but it fails because the plane is continuous and the required precision makes exhaustive sampling enormous. The useful observation is that the two circle equations can be combined algebraically. Subtracting them eliminates the quadratic terms (x^2+y^2), leaving a straight line. Every intersection point must lie on this line, called the radical axis. We can then intersect the first circle with that line, which gives at most two points directly.

There is an even cleaner way to calculate the coordinates. Let the centers be (C_1) and (C_2), and let (d) be the distance between them. The line through the two centers contains the midpoint of the common chord. If the distance from (C_1) to that chord is (a), then the Pythagorean theorem gives

[
a=\frac{r_1^2-r_2^2+d^2}{2d}.
]

The common chord is perpendicular to the line joining the centers. If (h) is the half-length of the chord, then

[
h^2=r_1^2-a^2.
]

The foot of the perpendicular from (C_1) to the chord is obtained by moving a distance (a) from (C_1) toward (C_2). A perpendicular unit vector then lets us move by (h) in both directions to obtain the two possible intersection points.

Before using these formulas, we classify the configuration using squared distances. This avoids unnecessary square roots and makes all geometric comparisons exact because the input values are integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(4\cdot10^{18})) candidate checks at (10^{-6}) resolution | (O(1)) | Too slow |
| Optimal | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the centers and radii of the two circles. Compute `dx = x2 - x1`, `dy = y2 - y1`, and the squared center distance `d2 = dx*dx + dy*dy`. Keeping `d2` instead of immediately taking a square root lets us classify all degenerate and non-intersecting configurations using exact integer comparisons.
2. If `d2 == 0` and the radii are equal, the circles coincide. Every point of one circle belongs to the other, so print `MANY` and stop.
3. If `d2 == 0` and the radii differ, the circles are concentric but distinct. They cannot meet, so print `0` and stop.
4. Compare the center distance with the sum and difference of the radii using squares. If (d > r_1+r_2), the circles are externally separated. If (d < |r_1-r_2|), one circle is strictly inside the other. In either situation there are zero intersection points.
5. Compute

[
d=\sqrt{d^2}
]

and then calculate

[
a=\frac{r_1^2-r_2^2+d^2}{2d}.
]

This is the distance from the first center to the common chord along the line connecting the centers. The formula follows by writing the two right-triangle relations for the two intersection points and subtracting them.

1. Compute

[
h^2=r_1^2-a^2.
]

For two intersecting circles this value is nonnegative. Because `a` is calculated with floating-point arithmetic, a tangent configuration can produce a tiny negative value such as `-1e-12` instead of exact zero. Clamp such a value to zero before taking the square root.

1. Find the foot of the perpendicular from the first center to the common chord:

[
p_x=x_1+a\frac{dx}{d},\qquad
p_y=y_1+a\frac{dy}{d}.
]

Then construct a unit vector perpendicular to the center line,

[
\left(-\frac{dy}{d},\frac{dx}{d}\right).
]

Multiplying this vector by (h) gives the displacement from the chord midpoint to either intersection point.

1. If (h=0), the circles are tangent, so the two possible points coincide. Print one point. Otherwise print both

[
(p_x-h\frac{dy}{d},\ p_y+h\frac{dx}{d})
]

and

[
(p_x+h\frac{dy}{d},\ p_y-h\frac{dx}{d}).
]

The order does not matter.

The invariant behind the construction is that every generated point lies on the first circle by the right-triangle relation (a^2+h^2=r_1^2), and it also lies on the second circle because the chosen chord position satisfies the corresponding radius equation. Conversely, every common point must lie on the common chord, whose position is uniquely determined by the two circle equations. The perpendicular construction finds every point on that chord that lies on the first circle, so it produces exactly all intersections.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x2 - x1
    dy = y2 - y1
    d2 = dx * dx + dy * dy

    # Coincident centers.
    if d2 == 0:
        if r1 == r2:
            print("MANY")
        else:
            print(0)
        return

    # Disjoint or one circle strictly inside the other.
    sum_r = r1 + r2
    diff_r = abs(r1 - r2)

    if d2 > sum_r * sum_r or d2 < diff_r * diff_r:
        print(0)
        return

    d = math.sqrt(d2)

    # Distance from the first center to the common chord.
    a = (r1 * r1 - r2 * r2 + d2) / (2.0 * d)

    # Half of the common chord length, squared.
    h2 = r1 * r1 - a * a

    # Floating-point roundoff can make a tangent case slightly negative.
    if h2 < 0.0:
        h2 = 0.0

    h = math.sqrt(h2)

    # Midpoint of the common chord.
    px = x1 + a * dx / d
    py = y1 + a * dy / d

    # Unit vector perpendicular to the line between centers.
    ux = -dy / d
    uy = dx / d

    # First intersection point.
    x_a = px + h * ux
    y_a = py + h * uy

    # Tangency: both mathematical constructions give the same point.
    if h == 0.0:
        print(1)
        print(f"{x_a:.10f} {y_a:.10f}")
        return

    # Two distinct intersection points.
    x_b = px - h * ux
    y_b = py - h * uy

    print(2)
    print(f"{x_a:.10f} {y_a:.10f}")
    print(f"{x_b:.10f} {y_b:.10f}")

if __name__ == "__main__":
    solve()
```

The first part computes the vector between the centers and its squared length. The special case `d2 == 0` must be handled before the general formula because the formula for `a` divides by the center distance.

The next two comparisons use integer squares. The condition `d2 > (r1 + r2)^2` means the circles are farther apart than the sum of their radii. The condition `d2 < (r1 - r2)^2` means the center distance is smaller than the absolute radius difference, so one circle lies strictly inside the other. Equality in either comparison is deliberately not rejected because equality means tangency, which gives one valid intersection point.

After the configuration is known to have one or two intersections, the code computes `d`, followed by `a` and `h2`. The expression for `a` is the central geometric formula. The value `h2` determines whether the common chord has positive length or has collapsed to a single tangent point.

The `if h2 < 0.0` correction handles only floating-point roundoff. A genuinely non-intersecting configuration has already been rejected using exact integer comparisons, so a small negative value here can only arise from arithmetic error near tangency.

The midpoint of the common chord is calculated along the center-to-center direction. The vector `(-dy / d, dx / d)` is perpendicular to that direction and has length one, so multiplying it by `h` gives exactly the offset from the chord midpoint to either intersection.

There are no integer overflow issues in Python. In a language with fixed-width integer types, the squared expressions should still be checked against the available integer range, although the given bounds are small enough for a signed 64-bit integer without difficulty.

## Worked Examples

### Sample 1

The input describes circles centered at `(0, 0)` and `(300, 0)`, both with radius `200`.

| Step | `dx` | `dy` | `d2` | `d` | `a` | `h2` |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 300 | 0 | 90000 | 300 | 150 | 17500 |

The center distance is `300`. Since `|200 - 200| < 300 < 200 + 200`, the circles intersect twice. The chord midpoint is `(150, 0)`, and the half-chord length is (\sqrt{17500}), approximately `132.2875656`. The perpendicular direction is vertical, so the two points are approximately `(150, 132.2875656)` and `(150, -132.2875656)`.

The output according to the stated format is:

```
2
150.0000000 132.2875656
150.0000000 -132.2875656
```

The construction is symmetric around the line joining the centers, exactly as the geometry predicts.

### Sample 2

The circles are centered at `(0, 0)` and `(0, 2)`, both with radius `1`.

| Step | `dx` | `dy` | `d2` | `d` | `a` | `h2` |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 0 | 2 | 4 | 2 | 1 | 0 |

Here the center distance equals the sum of the radii, so the circles are externally tangent. The common chord has zero length because `h2 = 0`. Its single point is `(0, 1)`.

The output is:

```
1
0.0000000 1.0000000
```

This trace exercises the boundary between one and two intersections and shows why the tangent case must not print the same point twice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | A fixed number of arithmetic operations and comparisons is performed. |
| Space | (O(1)) | Only a constant number of scalar variables and output coordinates are stored. |

The constraints are far smaller than what an (O(1)) geometric solution needs. The algorithm performs only a few integer operations, square roots, divisions, and formatting operations, so it easily fits within the one-second time limit and uses essentially no memory.

## Test Cases

The test harness below compares geometric answers rather than requiring one exact ordering of the two intersection points. It also checks the special `MANY` case and the required number of points.

```python
import sys
import io
import math

input = sys.stdin.readline

def solve():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x2 - x1
    dy = y2 - y1
    d2 = dx * dx + dy * dy

    if d2 == 0:
        if r1 == r2:
            print("MANY")
        else:
            print(0)
        return

    sum_r = r1 + r2
    diff_r = abs(r1 - r2)

    if d2 > sum_r * sum_r or d2 < diff_r * diff_r:
        print(0)
        return

    d = math.sqrt(d2)
    a = (r1 * r1 - r2 * r2 + d2) / (2.0 * d)
    h2 = r1 * r1 - a * a

    if h2 < 0.0:
        h2 = 0.0

    h = math.sqrt(h2)

    px = x1 + a * dx / d
    py = y1 + a * dy / d

    ux = -dy / d
    uy = dx / d

    x_a = px + h * ux
    y_a = py + h * uy

    if h == 0.0:
        print(1)
        print(f"{x_a:.10f} {y_a:.10f}")
        return

    x_b = px - h * ux
    y_b = py - h * uy

    print(2)
    print(f"{x_a:.10f} {y_a:.10f}")
    print(f"{x_b:.10f} {y_b:.10f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def parse_output(out: str):
    lines = out.strip().splitlines()

    if lines == ["MANY"]:
        return "MANY", []

    n = int(lines[0])
    points = []

    for line in lines[1:]:
        x, y = map(float, line.split())
        points.append((x, y))

    assert len(points) == n
    return n, points

def assert_points_on_circles(inp: str, out: str):
    data = list(map(int, inp.split()))
    x1, y1, r1, x2, y2, r2 = data

    result, points = parse_output(out)

    if result == "MANY":
        assert x1 == x2 and y1 == y2 and r1 == r2
        return

    for x, y in points:
        d1 = (x - x1) ** 2 + (y - y1) ** 2
        d2 = (x - x2) ** 2 + (y - y2) ** 2

        assert abs(d1 - r1 * r1) <= 1e-5 * max(1.0, r1 * r1)
        assert abs(d2 - r2 * r2) <= 1e-5 * max(1.0, r2 * r2)

# Provided sample 1.
sample1 = """\
0 0 200
300 0 200
"""
out = run(sample1)
result, points = parse_output(out)
assert result == 2, "sample 1 count"
assert_points_on_circles(sample1, out)

# Provided sample 2.
sample2 = """\
0 0 1
0 2 1
"""
out = run(sample2)
result, points = parse_output(out)
assert result == 1, "sample 2 count"
assert_points_on_circles(sample2, out)
assert abs(points[0][0]) < 1e-9
assert abs(points[0][1] - 1.0) < 1e-9

# Custom case 1: coincident circles, the minimum radius.
case1 = """\
0 0 1
0 0 1
"""
assert run(case1).strip() == "MANY", "coincident circles"

# Custom case 2: concentric circles with different radii.
case2 = """\
0 0 1
0 0 2
"""
assert run(case2).strip() == "0", "concentric distinct circles"

# Custom case 3: internal tangency.
case3 = """\
0 0 3
1 0 2
"""
out = run(case3)
result, points = parse_output(out)
assert result == 1, "internal tangency count"
assert_points_on_circles(case3, out)
assert abs(points[0][0] - 3.0) < 1e-9
assert abs(points[0][1]) < 1e-9

# Custom case 4: maximum-size coordinates and radii, two intersections.
case4 = """\
-1000 -1000 1000
1000 -1000 1000
"""
out = run(case4)
result, points = parse_output(out)
assert result == 2, "maximum-size two-intersection case"
assert_points_on_circles(case4, out)

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 200` / `300 0 200` | Two intersection points | General two-intersection construction |
| `0 0 1` / `0 2 1` | One point at `(0, 1)` | External tangency |
| `0 0 1` / `0 0 1` | `MANY` | Coincident circles and division-by-zero prevention |
| `0 0 1` / `0 0 2` | `0` | Concentric circles with different radii |
| `0 0 3` / `1 0 2` | One point at `(3, 0)` | Internal tangency |
| `-1000 -1000 1000` / `1000 -1000 1000` | Two intersection points | Maximum-size coordinates and radii |

## Edge Cases

For coincident circles, consider

```
0 0 1
0 0 1
```

The squared center distance is zero, and the radii are equal. The algorithm immediately prints `MANY` before attempting to compute the center distance as a divisor. The invariant here is that both equations describe exactly the same set of points.

For concentric circles with different radii,

```
0 0 1
0 0 2
```

the squared center distance is again zero, but the radii differ. The algorithm prints `0`. Two circles with the same center can only share points if their radii are equal.

For external tangency,

```
0 0 1
2 0 1
```

the squared center distance is `4`, exactly equal to `(1 + 1)^2`. The disjointness condition uses `>` rather than `>=`, so the case survives to the intersection calculation. The resulting value of `h2` is zero, giving the single point `(1, 0)`.

For internal tangency,

```
0 0 3
1 0 2
```

the center distance is exactly `|3 - 2| = 1`. Again the strict inequality does not reject the configuration. The formula gives `a = 3` and `h2 = 0`, producing `(3, 0)`, the point where the smaller circle touches the larger one.

For strict containment,

```
0 0 5
1 0 1
```

the center distance is `1`, while the radius difference is `4`. Since (1^2 < 4^2), the algorithm immediately prints `0`. No square root or floating-point computation is needed for this classification.

For two ordinary intersections,

```
0 0 2
3 0 2
```

the center distance is `3`, which lies strictly between the radius difference `0` and the radius sum `4`. The algorithm reaches the construction stage, obtains `a = 1.5`, and obtains a positive `h2`, so it prints two symmetric points. Their symmetry around the line joining the centers follows directly from the use of the perpendicular unit vector.

The main numerical boundary is tangency. The exact geometric value of `h2` is zero there, but floating-point evaluation can produce a tiny negative number. Clamping `h2` to zero prevents `math.sqrt` from failing while leaving all genuinely valid two-intersection cases unchanged.
