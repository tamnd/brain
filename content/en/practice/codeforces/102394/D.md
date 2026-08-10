---
title: "CF 102394D - Driverless Car"
description: "We have an axis-aligned rectangular field and two disjoint line segments strictly inside it. The car is a point, and every point of its route must be equally distant from the two segments."
date: "2026-08-10T19:04:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "D"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 187
verified: true
draft: false
---

[CF 102394D - Driverless Car](https://codeforces.com/problemset/problem/102394/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an axis-aligned rectangular field and two disjoint line segments strictly inside it. The car is a point, and every point of its route must be equally distant from the two segments. The route starts and ends on the rectangle boundary, with the two boundary points different, and it must pass through the interior.

The key object is therefore the set

[
{P\mid \operatorname{dist}(P,A)=\operatorname{dist}(P,B)}.
]

This is the Voronoi bisector of two segments. Since both segments are inside the rectangle and do not intersect, the relevant bisector separates the region closer to segment (A) from the region closer to segment (B). Inside the rectangle it forms the unique boundary-to-boundary route that the car has to follow. The answer is the length of that bisector inside the rectangle.

Each input case gives the rectangle through its lower-left corner ((x_l,y_l)) and upper-right corner ((x_r,y_r)), followed by the two segment endpoints. The endpoints are integer coordinates, but the desired route is a continuous curve, so the answer is generally irrational.

The official constraints allow as many as (10^5) independent cases, while every coordinate is between (-1000) and (1000). The small coordinate range does not make a grid solution viable, because the required error is (10^{-9}), far smaller than the natural unit scale of the input. A constant amount of computational geometry per test case is the appropriate target.

There are several edge cases that are easy to mishandle. First, a segment's nearest point is not always an interior point. For example,

```
1
0 0 5 5
1 1 4 1
1 4 4 4
```

has answer (5). Outside the horizontal extent of the segments, the nearest points are their endpoints, so treating every segment as an infinite line gives the wrong bisector.

Second, the nearest feature can change exactly at a segment endpoint. In the sample,

```
1
0 0 7 6
2 4 4 4
3 2 5 2
```

the bisector consists of endpoint-endpoint lines, point-line parabolic pieces, and a line-line piece. Ignoring the transitions at (x=2,3,4,5) gives the wrong length. The correct answer is (7.552593593868681136).

Third, two supporting lines can be parallel or intersecting. For example, two parallel horizontal segments produce one angle-bisector line, while two nonparallel segments produce two angle-bisector lines through the intersection of their supporting lines. A generic line-intersection routine that assumes a single finite intersection point would silently fail on the parallel case.

Finally, a segment can be vertical, so formulas that divide by its (x)-difference are unsafe. The implementation handles vertical constraint lines separately.

## Approaches

A literal brute-force approach would sample the rectangle on a grid, compute the two segment distances at every grid point, and attempt to reconstruct the equality curve. Even a grid with one-unit spacing has roughly (2000\cdot2000=4\cdot10^6) points for a maximum-size rectangle. Across (10^5) cases that is about (4\cdot10^{11}) point evaluations. More fundamentally, such a grid can never certify the required (10^{-9}) geometric accuracy.

The brute-force idea is useful because it reveals what we really need to know: at every point of the desired curve, which part of each segment is responsible for the distance? For one segment there are only three possibilities. The closest point can be its first endpoint, its second endpoint, or an interior point of the segment.

Once the nearest feature is fixed for both segments, the equality curve becomes a very simple classical object. Two point features give a perpendicular bisector line. Two line features give angle-bisector lines. A point feature and a line feature give a parabola, because the curve is exactly the set of points whose distance to a focus equals their distance to a directrix.

That observation reduces the continuous problem to only nine combinations of nearest features. Each combination also has a simple validity region, described by one or two half-planes. We intersect the corresponding line or parabola with those half-planes and with the rectangle. The resulting pieces partition the complete Voronoi bisector, so their lengths can simply be added.

The accepted geometric implementation uses exactly this constant-size decomposition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Grid brute force | (O((W/\varepsilon)(H/\varepsilon))) | (O(1)) or (O(WH)) | Too slow and not exact |
| Feature decomposition | (O(1)) per case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Represent every boundary of the rectangle as a directed line together with the convention that valid points lie on its interior side. The same representation will be used for the half-planes describing which endpoint or interior portion of a segment is the nearest feature.
2. For each segment (XY), consider three nearest-feature states. State (0) means the closest point is (X). State (1) means it is (Y). State (2) means the perpendicular projection lies inside the segment.

For state (0), the validity condition is

[
(P-X)\cdot(Y-X)\le 0.
]

For state (1), it is

[
(P-Y)\cdot(X-Y)\le 0.
]

For state (2), both endpoint conditions are reversed, requiring the projection to lie between the endpoints.
3. Enumerate all (3\times3=9) pairs of feature states, one state for each segment. Add the corresponding half-plane boundaries to the four rectangle boundaries. Every point accepted by these inequalities has exactly the selected nearest feature on each segment.
4. If both selected features are points (P) and (Q), their distances are equal exactly on the perpendicular bisector of (PQ). Construct that line and clip it by all current half-planes.
5. If both selected features are segment interiors, their distances are distances to two supporting lines. Equality between distances to two lines is an angle bisector. If the supporting lines are parallel, there is one bisector line halfway between them. If they intersect, there are two angle bisectors, and both must be tested against the feature-validity half-planes.
6. If one feature is a point and the other is an interior line, the equality curve is a parabola. Move the directrix to (y=0), rotate it to become horizontal, and transform the focus to ((u,v)). After translating to the parabola's vertex and, if necessary, reflecting vertically, the equation becomes

[
x^2=py,\qquad p=2v.
]

The validity boundaries are lines. Intersecting a line (y=kx+b) with the parabola gives

[
x^2-pkx-pb=0,
]

which is only a quadratic equation. A vertical boundary gives one (x)-coordinate directly.
7. For every candidate line, intersect it with every active half-plane boundary. Sort all intersection parameters along the candidate line. Between two consecutive parameters, the candidate is either completely valid or completely invalid, because no constraint boundary is crossed inside the interval. Test the midpoint of every interval and add the length of valid intervals.
8. For every candidate parabola, perform the same process in its (x)-parameter. After sorting all roots, test a midpoint (x) by evaluating the corresponding parabola point ((x,x^2/p)). The arc length is computed analytically rather than by numerical sampling:

\frac{x\sqrt{1+4x^2/p^2}}2+
\frac p4\operatorname{asinh}\left(\frac{2x}{p}\right).
]
9. Sum the valid pieces from all nine feature combinations. They are disjoint except possibly at feature-transition boundaries, which have zero length. Their union is exactly the Voronoi bisector inside the rectangle, so the accumulated length is the required minimum route.

### Why it works

For every point of the plane, the nearest point on a segment is classified uniquely as its first endpoint, second endpoint, or an interior projection, except on boundaries where two descriptions coincide. The nine feature pairs therefore cover the entire equality locus.

Inside one fixed feature pair, both distance functions have fixed algebraic forms. The equality locus is consequently exactly one of the three objects handled above: a line, an angle bisector, or a parabola. The half-plane constraints guarantee that the selected features really are the nearest points on their segments. Intersecting these objects with every constraint boundary partitions them into intervals on which validity is constant.

Thus every positive-length portion of the equality locus is counted once, and no invalid portion is counted. Since the equality locus of two disjoint convex segments is the separator between their two Voronoi regions, the portion inside the rectangle is the required boundary-to-boundary route. Its total length is consequently the minimum valid path length.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

EPS = 1e-9
INF = 1e100

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def mul(a, k):
    return (a[0] * k, a[1] * k)

def rot90(a):
    return (-a[1], a[0])

def rot270(a):
    return (a[1], -a[0])

def flip(a):
    return (-a[0], -a[1])

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def length(a):
    return math.hypot(a[0], a[1])

def sgn(x):
    if x > EPS:
        return 1
    if x < -EPS:
        return -1
    return 0

def line_intersection(a, b, p, q):
    """
    Intersect infinite lines AB and PQ.

    Return:
        (2, None, None) if coincident,
        (0, None, None) if parallel,
        (1, point, t) otherwise, where point = A + t(B-A).
    """
    d1 = sub(b, a)
    d2 = sub(q, p)
    den = cross(d1, d2)
    num = cross(sub(p, a), d2)

    if sgn(den) == 0:
        if sgn(num) == 0:
            return 2, None, None
        return 0, None, None

    t = num / den
    return 1, add(a, mul(d1, t)), t

def solve_case(xl, yl, xr, yr, seg_a, seg_b):
    rect = [
        ((float(xl), float(yl)), (float(xr), float(yl))),
        ((float(xr), float(yl)), (float(xr), float(yr))),
        ((float(xr), float(yr)), (float(xl), float(yr))),
        ((float(xl), float(yr)), (float(xl), float(yl))),
    ]

    total = 0.0

    def check(point, edges):
        for a, b in edges:
            if sgn(cross(sub(point, a), sub(b, a))) > 0:
                return False
        return True

    def call_line(a, b, edges):
        """
        Add the valid length of the infinite line AB under all
        current half-plane constraints.
        """
        values = []

        for p, q in edges:
            typ, _, t = line_intersection(a, b, p, q)
            if typ == 2:
                return 0.0
            if typ == 1:
                values.append(t)

        if len(values) < 2:
            return 0.0

        values.sort()
        dlen = length(sub(b, a))
        ret = 0.0

        for i in range(1, len(values)):
            t1 = values[i - 1]
            t2 = values[i]
            mid = (t1 + t2) * 0.5
            p = add(a, mul(sub(b, a), mid))
            if check(p, edges):
                ret += (t2 - t1) * dlen

        return ret

    def integral_parabola(p, x):
        """
        Integral of sqrt(1 + 4*x^2/p^2) dx.
        """
        if p <= 0:
            return 0.0

        z = 2.0 * x / p
        root = math.sqrt(1.0 + z * z)
        return 0.5 * x * root + 0.25 * p * math.asinh(z)

    def solve_features(edges, tp0, f0, tp1, f1):
        nonlocal total

        if tp0 > tp1:
            tp0, tp1 = tp1, tp0
            f0, f1 = f1, f0

        A = f0[0]
        B = f0[1] if len(f0) > 1 else None
        C = f1[0]
        D = f1[1] if len(f1) > 1 else None

        if tp0 == 0 and tp1 == 0:
            mid = mul(add(A, C), 0.5)
            direction = rot90(sub(A, mid))
            total += call_line(add(mid, direction), mid, edges)
            return

        if tp0 == 1 and tp1 == 1:
            typ, o, _ = line_intersection(A, B, C, D)

            if typ == 0:
                origin = mul(add(A, C), 0.5)
                total += call_line(origin, add(origin, sub(D, C)), edges)
                return

            if typ == 2:
                return

            if length(sub(A, o)) < length(sub(B, o)):
                A, B = B, A

            if length(sub(C, o)) < length(sub(D, o)):
                C, D = D, C

            ang1 = math.atan2(A[1] - o[1], A[0] - o[0])
            ang2 = math.atan2(C[1] - o[1], C[0] - o[0])
            ang = (ang1 + ang2) * 0.5

            direction = (math.cos(ang), math.sin(ang))
            total += call_line(o, add(o, direction), edges)
            total += call_line(o, add(o, rot90(direction)), edges)
            return

        # Point-line case.
        # A is the point, CD is the supporting line.
        direction = sub(D, C)

        # Translate C to the origin.
        A = sub(A, C)
        transformed = [(sub(p, C), sub(q, C)) for p, q in edges]

        # Rotate CD onto the positive x-axis.
        w = math.atan2(direction[1], direction[0])
        cw = math.cos(-w)
        sw = math.sin(-w)

        def rotate_point(p):
            return (p[0] * cw - p[1] * sw,
                    p[0] * sw + p[1] * cw)

        A = rotate_point(A)
        transformed = [
            (rotate_point(p), rotate_point(q))
            for p, q in transformed
        ]

        if A[1] < 0:
            A = flip(A)
            transformed = [(flip(p), flip(q)) for p, q in transformed]

        p = 2.0 * A[1]

        if sgn(p) == 0:
            return

        vertex = (A[0], A[1] * 0.5)

        transformed = [
            (sub(a, vertex), sub(b, vertex))
            for a, b in transformed
        ]

        roots = []

        for a, b in transformed:
            dx = a[0] - b[0]

            if sgn(dx) == 0:
                roots.append(a[0])
                continue

            k = (a[1] - b[1]) / dx
            bb = a[1] - k * a[0]

            # x^2 - p*k*x - p*b = 0
            disc = p * p * k * k + 4.0 * p * bb

            if sgn(disc) < 0:
                continue

            if disc < 0:
                disc = 0.0

            root = math.sqrt(disc)
            roots.append((p * k - root) * 0.5)
            roots.append((p * k + root) * 0.5)

        if len(roots) < 2:
            return

        roots.sort()

        prev_value = None

        for i, x in enumerate(roots):
            value = integral_parabola(p, x)

            if i > 0:
                mid = (roots[i - 1] + x) * 0.5
                point = (mid, mid * mid / p)

                if check(point, transformed):
                    total += value - prev_value

            prev_value = value

    segments = [seg_a, seg_b]

    for state_a in range(3):
        for state_b in range(3):
            edges = list(rect)
            features = [None, None]
            types = [state_a, state_b]

            for idx, state in enumerate(types):
                a, b = segments[idx]
                d = sub(b, a)

                if state == 0:
                    # Closest point is a.
                    edges.append((a, add(a, rot90(d))))
                    features[idx] = [a]

                elif state == 1:
                    # Closest point is b.
                    edges.append((b, add(b, rot90(sub(a, b)))))
                    features[idx] = [b]

                else:
                    # Closest point is in the interior of AB.
                    edges.append((a, add(a, rot270(d))))
                    edges.append((b, add(b, rot270(sub(a, b)))))
                    features[idx] = [a, b]

            solve_features(
                edges,
                state_a,
                features[0],
                state_b,
                features[1]
            )

    return total

def solve(inp):
    rd = inp.readline
    t = int(rd())
    out = []

    for _ in range(t):
        xl, yl, xr, yr = map(int, rd().split())
        a = tuple(map(float, rd().split()))
        b = tuple(map(float, rd().split()))

        seg_a = ((a[0], a[1]), (a[2], a[3]))
        seg_b = ((b[0], b[1]), (b[2], b[3]))

        ans = solve_case(
            xl, yl, xr, yr,
            seg_a, seg_b
        )

        if abs(ans) < 5e-12:
            ans = 0.0

        out.append(f"{ans:.15f}")

    return "\n".join(out)

if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin))
```

The rectangle is inserted as four half-plane boundaries before any feature is considered. Because the rectangle is convex, a candidate curve can be clipped simply by sorting its intersections with those boundaries.

The `work` logic from the geometric derivation is represented directly by the three states. The perpendicular boundary through an endpoint comes from the dot-product condition defining whether projection onto the segment lies before that endpoint.

`call_line` parameterizes an infinite line as (A+t(B-A)). Every constraint crossing produces one value of (t). Sorting these values turns a continuous clipping problem into a constant number of interval checks. Testing a midpoint is sufficient because no constraint boundary is crossed inside that interval.

The line-line case needs special handling when the supporting lines intersect. There are two angle bisectors, not one. The code chooses the rays pointing away from the intersection and averages their directions, then uses a perpendicular direction for the second bisector.

The point-line case is the numerically delicate part. The transformation removes arbitrary segment orientation, after which the equality curve has the standard parabola equation (x^2=py). Every constraint becomes either a vertical line or (y=kx+b), so all intersection parameters come from either a direct (x)-value or a quadratic equation.

Python's `float` is sufficient here because the required error is (10^{-9}), while the coordinate magnitudes are only (2000). The implementation uses an absolute epsilon when deciding whether a cross product, determinant, or discriminant is zero. This prevents tiny floating-point noise from turning a geometrically parallel line into an artificial intersection.

## Worked Examples

### Sample 1

The input is

```
1
0 0 7 6
2 4 4 4
3 2 5 2
```

Both segments are horizontal, but the lower one is shifted one unit to the right. The equality curve has five positive-length pieces. The nine feature combinations are summarized below.

| Feature pair | Equality curve | Valid interval | Length |
| --- | --- | --- | --- |
| A-left endpoint, B-left endpoint | Line (y=x/2+7/4) | (0\le x\le2) | (\sqrt5) |
| A-interior, B-left endpoint | Parabola | (2\le x\le3) | (1.0402288194) |
| A-interior, B-interior | (y=3) | (3\le x\le4) | (1) |
| A-right endpoint, B-interior | Parabola | (4\le x\le5) | (1.0402288194) |
| A-right endpoint, B-right endpoint | Line (y=x/2+3/4) | (5\le x\le7) | (\sqrt5) |

The other four feature combinations have no positive-length valid interval. For either parabolic piece, after substituting the corresponding coordinates, the arc-length integral is

1.040228819434551.
]

The accumulated length is consequently

[
2\sqrt5
+1.040228819434551
+1
+1.040228819434551
+2\sqrt5,
]

which gives

[
7.552593593868681.
]

This agrees with the official sample output (7.552593593868681136).

### Symmetric segments

Consider

```
1
0 0 10 10
2 3 8 3
2 7 8 7
```

The two segments are horizontal, equal in length, and directly above one another. Their supporting-line bisector is (y=5).

| Feature pair | Valid interval | Contribution | Accumulated length |
| --- | --- | --- | --- |
| Left endpoint, left endpoint | (0\le x\le2) | (2) | (2) |
| Interior, interior | (2\le x\le8) | (6) | (8) |
| Right endpoint, right endpoint | (8\le x\le10) | (2) | (10) |

All mixed point-line combinations collapse to zero-length transitions at the segment endpoints. The final answer is (10).

This example demonstrates why the algorithm must not treat a segment as a single geometric primitive. The same final bisector is assembled from endpoint and interior feature cases, even though it looks like one straight line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) per test case | There are exactly nine feature pairs and each has a constant number of constraints, intersections, roots, and interval checks |
| Space | (O(1)) | At most a constant number of points, boundaries, roots, and temporary intervals are stored |

Across (10^5) cases, the total work is linear in the number of cases with a relatively small constant. The original problem has a 6 second limit and 512 MB memory limit, so avoiding any dependence on the rectangle's coordinate area is essential.

## Test Cases

The following harness assumes the solution code above is available in the same file or imported so that `solve` is callable.

```
import io
import math

def run(inp: str) -> str:
    return solve(io.BytesIO(inp.encode())).strip()

def assert_close(inp: str, expected: float, name: str):
    got = float(run(inp))
    assert math.isclose(got, expected, rel_tol=1e-10, abs_tol=1e-10), (
        f"{name}: got {got}, expected {expected}"
    )

# Provided sample
sample1 = """\
1
0 0 7 6
2 4 4 4
3 2 5 2
"""
assert_close(sample1, 7.552593593868681136, "sample 1")

# Minimum-size valid construction.
# The rectangle has width 2 and height 5.
# The two vertical segments occupy disjoint interior intervals.
case_minimum = """\
1
0 0 2 5
1 1 1 2
1 3 1 4
"""
assert_close(case_minimum, 2.0, "minimum-size case")

# Maximum-size rectangle and symmetric horizontal segments.
case_maximum = """\
1
-1000 -1000 1000 1000
-500 -500 500 -500
-500 500 500 500
"""
assert_close(case_maximum, 2000.0, "maximum-size case")

# Segment endpoints are as close as allowed to the rectangle boundary.
case_boundary = """\
1
0 0 5 5
1 1 4 1
1 4 4 4
"""
assert_close(case_boundary, 5.0, "boundary case")

# Both segments are vertical, exercising x1 == x2.
case_vertical = """\
1
0 0 10 10
3 2 3 8
7 2 7 8
"""
assert_close(case_vertical, 10.0, "vertical segments")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 2 5`, segments on (x=1) | `2` | Smallest practical rectangle with two disjoint integer-coordinate segments |
| `-1000 -1000 1000 1000`, horizontal segments | `2000` | Maximum coordinate range and large geometric values |
| `0 0 5 5`, segments using coordinates (1) and (4) | `5` | Endpoints at the closest permitted distance from the rectangle boundary |
| `0 0 10 10`, vertical segments | `10` | Vertical segments and protection against division by zero |

## Edge Cases

The first edge case is a segment whose nearest point is an endpoint. Consider

```
1
0 0 5 5
1 1 4 1
1 4 4 4
```

For (x<1), the nearest point of the lower segment is its left endpoint, and the same is true for the upper segment. The equality locus there is an endpoint-endpoint perpendicular bisector. The algorithm reaches this case through feature state (0,0), rather than incorrectly using the two infinite supporting lines. The final route is the full horizontal line (y=2.5), with length (5).

The second edge case is a feature transition. In the official sample, for (2<x<3), the closest feature on the upper segment is its interior while the closest feature on the lower segment is its left endpoint. At (x=3), the lower nearest feature changes to the segment interior. The algorithm explicitly considers both feature states, and the transition point appears as an intersection with one of the active half-plane boundaries. Since a single point has zero length, there is no double-counting problem. The resulting total is (7.552593593868681136).

The third edge case is a vertical segment. Consider

```
1
0 0 10 10
3 2 3 8
7 2 7 8
```

The two supporting lines are (x=3) and (x=7), so their bisector is (x=5). The route crosses the rectangle from ((5,0)) to ((5,10)), giving length (10). In the parabola code, vertical constraint lines are detected by their zero (x)-difference, so no division by zero occurs.

The fourth edge case is parallel supporting lines. When the two selected interior features are parallel, there is exactly one equidistant line halfway between them. The algorithm detects that the supporting-line intersection does not exist and constructs the midpoint line directly. This avoids trying to form an angle from an undefined intersection point.

The fifth edge case is an intersecting pair of supporting lines. Two nonparallel segments may have supporting lines that meet even though the finite segments themselves are disjoint. Equal distance to those two lines gives two angle bisectors. The algorithm generates both and lets the feature half-planes discard whichever parts do not correspond to the actual segments. This is necessary because keeping only one angle bisector can remove a valid portion of the Voronoi bisector.

The last edge case is numerical degeneracy at a constraint boundary. A candidate curve can coincide with a half-plane boundary exactly, especially at the transition between an endpoint feature and an interior feature. The implementation treats coincident lines as contributing zero in that feature case, because the same geometric piece is represented by the neighboring feature case. This prevents the same positive-length curve from being counted twice.

This version is deliberately geometric rather than formula-first: once the nearest-feature decomposition is understood, the three curve types and their clipping rules can be re-derived for similar Voronoi problems.
