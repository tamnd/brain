---
title: "CF 102386K - \u041c\u0430\u043b\u044b\u0448 \u0438 \u041a\u0430\u0440\u043b\u0441\u043e\u043d"
description: "We have a strictly convex polygon whose vertices are given counterclockwise and have integer coordinates. We need to draw one straight line that divides the polygon into two regions of exactly equal area."
date: "2026-08-15T18:57:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "K"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 549
verified: false
draft: false
---

[CF 102386K - \u041c\u0430\u043b\u044b\u0448 \u0438 \u041a\u0430\u0440\u043b\u0441\u043e\u043d](https://codeforces.com/problemset/problem/102386/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We have a strictly convex polygon whose vertices are given counterclockwise and have integer coordinates. We need to draw one straight line that divides the polygon into two regions of exactly equal area. The line itself must contain two distinct integer-coordinate points, and their coordinates must fit inside the range from (-10^{18}) to (10^{18}).

The useful geometric property is that the polygon can be triangulated from any one of its vertices. Choose the first vertex (V_0), and connect it to every other vertex. This produces (N-2) triangles whose doubled areas are integers because every coordinate is integral. The whole problem then becomes finding where half of the total doubled area falls in this sequence of triangles. The original problem uses (N\le 1000), coordinates bounded by (10^5), and a one-second limit. That is small enough for a linear or quadratic algorithm, but there is no reason to do anything quadratic once the fan triangulation is recognized. Exact integer arithmetic is also preferable to floating point because the required equality is exact.

A direct exhaustive search over all integer-coordinate pairs (A,B) is finite because the coordinates are bounded, but completely useless. There are roughly ((4\cdot10^{36})^2/2\approx8\cdot10^{72}) unordered pairs of lattice points, and checking one line against all polygon edges would add another factor of (N). With (N=1000), that is on the order of (10^{75}) basic geometric operations. More reasonable-looking brute force approaches, such as trying lines through pairs of polygon vertices, are also not sufficient because a valid cutting line need not pass through two polygon vertices.

There are several boundary cases that a careless implementation can mishandle. For the triangle

```
3
0 0
4 0
0 2
```

the answer is the median from ((0,0)) to the midpoint of the opposite edge. The midpoint itself need not have integer coordinates, so simply looking for an integer point on the edge can fail. Our construction multiplies the rational point by its denominator and obtains an integer point on the same line.

For the square

```
4
0 0
2 0
2 2
0 2
```

the first fan triangle already has exactly half the polygon's doubled area. A careless implementation that only handles the case where the half lies strictly inside a triangle may move on to the next triangle and access invalid indices. The equality case must be handled immediately, and the diagonal from ((0,0)) to ((2,2)) is a valid answer.

The supplied sample is another useful case:

```
4
0 3
3 0
3 6
0 7
```

The half-area point lies strictly inside the first fan triangle. A floating-point implementation might approximate the cutting point, but the checker requires exact equality. We instead construct an integer point on exactly the same line using integer multiplication.

Under the stated constraints, a solution always exists, so the `-1` output is never necessary. The construction below explicitly produces one for every valid input.

## Approaches

The most literal brute-force solution would search over integer points and test candidate lines. That is already impossible from the coordinate bound alone, since the lattice contains about (4\cdot10^{36}) points. Even restricting the search to lines through pairs of polygon vertices leaves (O(N^2)) candidates, and checking each candidate against the polygon takes (O(N)) time. The worst case is then about (N^3/2), roughly (5\cdot10^8) edge operations for (N=1000). More importantly, that restricted search is not complete, because the required line can meet the polygon boundary at two points lying strictly inside edges.

The key observation is that we do not need to search over directions at all. Fix the first polygon vertex (V_0), and triangulate the polygon as

[
(V_0,V_1,V_2),\quad
(V_0,V_2,V_3),\quad
\dots,\quad
(V_0,V_{N-2},V_{N-1}).
]

The doubled area of each triangle is an integer. As we walk through these triangles, the accumulated area starts at zero and ends at the doubled area of the whole polygon. Consequently, there is a first triangle whose inclusion makes the accumulated area reach or exceed half of the total.

If the accumulated area is exactly half after some complete triangle, the diagonal from (V_0) to that triangle's last vertex is already the desired cutting line.

Otherwise, half of the total area lies strictly inside one triangle (V_0BC). Inside that triangle, every line through (V_0) and a point (P) on (BC) cuts off a triangle (V_0BP). Its area changes linearly as (P) moves along (BC), so we can choose the exact required ratio on (BC).

The remaining difficulty is that (P) may be rational rather than integral. This is where the unusually large (10^{18}) output bound becomes useful. If

[
P=\frac{(2T-d)B+dC}{2T},
]

we can simply use

[
Q=(2T-d)B+dC.
]

The point (Q) has integer coordinates, and it lies on the same ray from (V_0) as (P). Hence the line (V_0Q) is exactly the required cutting line. There is no division and no floating-point arithmetic anywhere.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) after restricting candidates to vertex pairs | (O(N)) | Too slow and not complete |
| Optimal | (O(N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Choose the first polygon vertex (V_0) as the common vertex of a fan triangulation. Translate every other vertex by subtracting (V_0), so (V_0) becomes the origin. Translation does not change areas or lines through (V_0).
2. For every consecutive pair (V_i,V_{i+1}), with (1\le i<N-1), compute

[
T_i=\left|\operatorname{cross}(V_i,V_{i+1})\right|.
]

This is twice the area of triangle (V_0V_iV_{i+1}). Because all coordinates are integers, every (T_i) is an integer.

1. Sum all (T_i) to obtain (S), the doubled area of the whole polygon. We deliberately work with doubled areas so that the target is exactly (S/2), without introducing fractions.
2. Walk through the triangles while maintaining their prefix doubled area. Find the first triangle (V_0BC) for which the new prefix satisfies (2\cdot\text{prefix}\ge S). Convexity guarantees that all fan triangles lie inside the polygon and have positive area, so such a triangle always exists.
3. If (2\cdot\text{prefix}=S), output (V_0) and the last vertex of the current triangle. The fan triangles before this diagonal have exactly half of the total area.
4. Otherwise, let `before` be the doubled area of all fan triangles before (V_0BC), and let (T) be the doubled area of (V_0BC). Define

[
d=S-2\cdot\text{before}.
]

The desired part of the current triangle must have doubled area (d/2). Since the current triangle is the first one crossing the half-area boundary,

[
0<d<2T.
]

1. Let (B=V_i) and (C=V_{i+1}). A point on (BC) can be written as

[
P=\frac{(2T-d)B+dC}{2T}.
]

The triangle (V_0BP) has doubled area

# \frac{d}{2T}\operatorname{cross}(B,C)

\frac d2.
]

Thus the area before this triangle plus the area of (V_0BP) is exactly (S/2).

1. We do not output (P), because it can be fractional. Instead compute

[
Q=(2T-d)B+dC.
]

All coordinates of (Q) are integers. Since (Q=2T\cdot P), the points (V_0,P,Q) are collinear, so the line through (V_0) and (Q) is the required cutting line.

After the numbered steps, the invariant is that the accumulated fan triangles represent exactly the area on one side of the candidate diagonal. Before the selected triangle this area is strictly below half, and after adding the selected triangle it is at least half. If equality happens at a triangle boundary, the corresponding diagonal solves the problem. Otherwise the required amount is strictly between zero and the full area of the selected triangle, so the unique point (P) described above lies strictly inside its edge. The scaled integer point (Q) lies on exactly the same line, proving that the output line has integer points and bisects the polygon exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def solve():
    n = int(input())
    p = [tuple(map(int, input().split())) for _ in range(n)]

    ox, oy = p[0]

    # Translate the polygon so p[0] becomes (0, 0).
    q = [(x - ox, y - oy) for x, y in p]
    q[0] = (0, 0)

    # Doubled areas of the fan triangles.
    areas = []
    total = 0

    for i in range(1, n - 1):
        ax, ay = q[i]
        bx, by = q[i + 1]
        t = abs(cross(ax, ay, bx, by))
        areas.append(t)
        total += t

    prefix = 0

    for i, t in enumerate(areas, start=1):
        prefix += t

        # The current fan triangle ends at q[i + 1].
        if prefix * 2 == total:
            x, y = q[i + 1]
            print(ox, oy)
            print(ox + x, oy + y)
            return

        if prefix * 2 > total:
            before = prefix - t
            d = total - 2 * before

            # Current triangle is q[0], q[i], q[i + 1].
            bx, by = q[i]
            cx, cy = q[i + 1]

            # Q = (2T-d) * B + d * C.
            #
            # Q is a scaled version of the exact rational
            # point on BC, so OQ is the same cutting line.
            qx = (2 * t - d) * bx + d * cx
            qy = (2 * t - d) * by + d * cy

            print(ox, oy)
            print(ox + qx, oy + qy)
            return

if __name__ == "__main__":
    solve()
```

The first part of the implementation translates the polygon by the first vertex. This makes the area formula particularly simple, since every fan triangle has the origin as one vertex.

The `cross` function is the only geometric primitive required. For two vectors (u) and (v), its absolute value is the doubled area of the triangle formed by the origin and those vectors. Python integers have arbitrary precision, so the intermediate products are safe even though the constructed output can be much larger than the input coordinates.

The first loop computes the fan triangle areas and their total. The second loop searches for the first prefix crossing half of that total. The equality branch is separate because in that case the desired line is already a polygon diagonal.

In the strict-crossing branch, `before` is the doubled area already accounted for. The quantity `d = total - 2 * before` is twice the remaining area needed from the current triangle. The coefficients `2 * t - d` and `d` are both positive, so the constructed point is on the segment between the current two polygon vertices before scaling.

The code never divides by `2 * t`. That is the central implementation trick. The rational point is multiplied by its denominator, producing the integer point `Q` on the same line. With input coordinates bounded by (10^5), every translated coordinate has magnitude at most (2\cdot10^5), while (2T\le8\cdot10^{10}) for an individual triangle. Thus the constructed coordinate is comfortably below (10^{18}).

## Worked Examples

For the supplied sample,

```
4
0 3
3 0
3 6
0 7
```

translation by the first vertex gives ((0,0),(3,-3),(3,3),(0,4)). The fan consists of two triangles.

| Triangle | Vertices relative to (V_0) | Doubled area | Prefix |
| --- | --- | --- | --- |
| 1 | ((0,0),(3,-3),(3,3)) | 18 | 18 |
| 2 | ((0,0),(3,3),(0,4)) | 12 | 30 |

The total doubled area is (30), so the target is (15). The first triangle already crosses the target. Here `before = 0`, (T=18), and (d=30). The scaled point is

[
Q=(36-30)(3,-3)+30(3,3)=(108,72).
]

After translating back, the program outputs

```
0 3
108 75
```

The cutting line intersects the polygon at ((0,3)) and ((3,5)), and the resulting triangle has area (15/2), exactly half of the polygon's area. The sample's output is different, but multiple valid answers are allowed.

For the second example, consider the square

```
4
0 0
2 0
2 2
0 2
```

| Triangle | Vertices relative to (V_0) | Doubled area | Prefix |
| --- | --- | --- | --- |
| 1 | ((0,0),(2,0),(2,2)) | 4 | 4 |
| 2 | ((0,0),(2,2),(0,2)) | 4 | 8 |

The total doubled area is (8), so half is (4). The first prefix is already exactly (4), which activates the equality branch. The algorithm outputs

```
0 0
2 2
```

The diagonal divides the square into two triangles of area (2) each.

A third small example is the triangle

```
3
0 0
4 0
0 2
```

There is only one fan triangle, so its doubled area is (8). The target is (4), which corresponds to the midpoint of the opposite edge. The construction gives

[
Q=8(4,0)+8(0,2)=(32,16),
]

so the output line is the line through ((0,0)) and ((32,16)), equivalently (y=x/2). It passes through the midpoint ((2,1)) of the opposite edge and is exactly the triangle's median.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Each polygon vertex is processed a constant number of times. |
| Space | (O(N)) | The polygon and fan triangle areas are stored explicitly. |

For (N\le1000), linear time is far below the available limit. The largest integer values arise from cross products and from scaling the point on one polygon edge, but Python's arbitrary-precision integers handle them exactly. The final constructed coordinates stay well below (10^{18}), so the output restriction is also satisfied.

## Test Cases

The following test harness uses exact integer geometry to validate the returned line. Since geometry problems usually allow many different outputs, the tests check the mathematical property of the output rather than requiring one particular pair of points.

```python
# helper: run solution on input string, return output string
import sys
import io
from fractions import Fraction
import math

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def solve_data(data):
    it = iter(data.strip().split())
    n = int(next(it))
    p = [(int(next(it)), int(next(it))) for _ in range(n)]

    ox, oy = p[0]
    q = [(x - ox, y - oy) for x, y in p]

    areas = []
    total = 0

    for i in range(1, n - 1):
        ax, ay = q[i]
        bx, by = q[i + 1]
        t = abs(cross(ax, ay, bx, by))
        areas.append(t)
        total += t

    prefix = 0

    for i, t in enumerate(areas, start=1):
        prefix += t

        if prefix * 2 == total:
            x, y = q[i + 1]
            return f"{ox} {oy}\n{ox + x} {oy + y}\n"

        if prefix * 2 > total:
            before = prefix - t
            d = total - 2 * before

            bx, by = q[i]
            cx, cy = q[i + 1]

            qx = (2 * t - d) * bx + d * cx
            qy = (2 * t - d) * by + d * cy

            return f"{ox} {oy}\n{ox + qx} {oy + qy}\n"

    return "-1\n"

def run(inp: str) -> str:
    return solve_data(inp)

def polygon_double_area(p):
    s = 0
    n = len(p)
    for i in range(n):
        x1, y1 = p[i]
        x2, y2 = p[(i + 1) % n]
        s += x1 * y2 - y1 * x2
    return abs(s)

def line_value(a, b, p):
    ax, ay = a
    bx, by = b
    x, y = p
    return (bx - ax) * (y - ay) - (by - ay) * (x - ax)

def clip_halfplane(poly, a, b, keep_positive):
    if not poly:
        return []

    result = []

    def inside(v):
        return v >= 0 if keep_positive else v <= 0

    for i in range(len(poly)):
        p = poly[i]
        q = poly[(i + 1) % len(poly)]
        fp = line_value(a, b, p)
        fq = line_value(a, b, q)
        inp = inside(fp)
        inq = inside(fq)

        if inp:
            result.append(p)

        if inp != inq:
            den = fq - fp
            t = Fraction(-fp, den)
            x = p[0] + t * (q[0] - p[0])
            y = p[1] + t * (q[1] - p[1])
            result.append((x, y))

    return result

def double_area_fraction(poly):
    if len(poly) < 3:
        return Fraction(0)

    s = Fraction(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - y1 * x2
    return abs(s)

def valid_cut(inp, out):
    tokens = out.strip().split()
    if len(tokens) == 1 and tokens[0] == "-1":
        return False

    if len(tokens) != 4:
        return False

    a = (int(tokens[0]), int(tokens[1]))
    b = (int(tokens[2]), int(tokens[3]))

    if a == b:
        return False

    it = iter(inp.strip().split())
    n = int(next(it))
    poly = [(int(next(it)), int(next(it))) for _ in range(n)]

    total = Fraction(polygon_double_area(poly))

    left = clip_halfplane(poly, a, b, True)
    right = clip_halfplane(poly, a, b, False)

    return (
        double_area_fraction(left) * 2 == total
        and double_area_fraction(right) * 2 == total
        and abs(a[0]) <= 10**18
        and abs(a[1]) <= 10**18
        and abs(b[0]) <= 10**18
        and abs(b[1]) <= 10**18
    )

# Provided sample.
sample1 = """\
4
0 3
3 0
3 6
0 7
"""
assert valid_cut(sample1, run(sample1)), "sample 1"

# Minimum-size polygon.
triangle = """\
3
0 0
4 0
0 2
"""
assert run(triangle) == "0 0\n32 16\n", "minimum-size triangle"

# Equal fan areas, exercising the exact-half branch.
square = """\
4
0 0
2 0
2 2
0 2
"""
assert run(square) == "0 0\n2 2\n", "exact prefix half"

# Coordinates at the input boundary.
boundary_triangle = """\
3
100000 100000
-100000 100000
-100000 -100000
"""
assert valid_cut(boundary_triangle, run(boundary_triangle)), "coordinate boundary"

# A nontrivial polygon where half the area lies strictly inside a fan triangle.
pentagon = """\
5
0 0
4 0
5 2
3 5
0 4
"""
assert run(pentagon) == "0 0\n144 145\n", "interior fan triangle"

# Maximum-size stress test.
# Points are sampled from a large circle and slightly perturbed radially.
# The radius is large enough that rounding preserves strict convexity.
n = 1000
pts = []
for i in range(n):
    angle = 2.0 * math.pi * i / n
    r = 90000 + (i % 7)
    x = int(round(r * math.cos(angle)))
    y = int(round(r * math.sin(angle)))
    pts.append((x, y))

# Rotate the generated order if necessary so it is counterclockwise.
area = polygon_double_area(pts)
if area < 0:
    pts.reverse()

max_case = str(n) + "\n" + "\n".join(f"{x} {y}" for x, y in pts) + "\n"
assert valid_cut(max_case, run(max_case)), "maximum-size stress test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any exact area-bisecting integer line | Nontrivial cut inside the first fan triangle |
| `3 / 0 0 / 4 0 / 0 2` | `0 0` and `32 16` | Minimum polygon and rational midpoint scaling |
| `4 / 0 0 / 2 0 / 2 2 / 0 2` | `0 0` and `2 2` | Exact prefix equal to half |
| Boundary triangle with coordinates (\pm100000) | Any valid integer line | Large input coordinates and large constructed integers |
| Five-vertex polygon | `0 0` and `144 145` | Strictly interior fan-triangle construction |
| Generated 1000-vertex polygon | Any valid integer line | Maximum (N), integer arithmetic, and linear-time traversal |

## Edge Cases

For the minimum triangle

```
3
0 0
4 0
0 2
```

the algorithm has exactly one fan triangle with doubled area (8). The prefix immediately equals the total, but the half-area condition is reached inside that triangle rather than after the whole triangle. Here `before = 0`, (T=8), and (d=8). The constructed integer point is (Q=8(4,0)+8(0,2)=(32,16)). The line from ((0,0)) to ((32,16)) is the median, so both parts have area (4).

For the exact-prefix case

```
4
0 0
2 0
2 2
0 2
```

the first fan triangle has doubled area (4), while the total doubled area is (8). The equality test fires before the strict-crossing branch. The output diagonal ((0,0)) to ((2,2)) divides the square into two equal triangles. This case catches both an off-by-one error in selecting the current triangle and an implementation that assumes the half-area point is always inside an edge.

For the supplied sample

```
4
0 3
3 0
3 6
0 7
```

the first triangle has doubled area (18), while the entire polygon has doubled area (30). Since (18>15), the target lies inside that triangle. The exact scaled point is ((108,72)) in coordinates relative to the first vertex, giving the output point ((108,75)). The line through ((0,3)) and ((108,75)) intersects the polygon again at ((3,5)), and the resulting triangle has area (7.5), exactly half of the polygon's area (15).

For the boundary-coordinate case

```
3
100000 100000
-100000 100000
-100000 -100000
```

the input uses the largest permitted coordinate magnitude. After translating by the first vertex, the other points are ((-200000,0)) and ((-200000,-200000)). The construction scales the opposite-edge midpoint by the triangle's doubled area and produces a point with magnitude around (10^{13}), still far below (10^{18}). No floating-point operation is required, so there is no loss of precision at the boundary.

The most subtle edge case is a rational cutting point that is not itself an integer point. The algorithm never attempts to round that point. Instead it represents the point as a rational affine combination of two integer vertices and multiplies the entire combination by its denominator. Scaling a vector from the fixed integer vertex (V_0) changes its length but not its direction, so the resulting integer point determines exactly the same cutting line. This is the reason the construction works for every valid integer-coordinate convex polygon rather than only for polygons whose half-area cut happens to pass through an existing lattice point.
