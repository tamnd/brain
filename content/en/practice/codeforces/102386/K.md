---
title: "CF 102386K - \u041c\u0430\u043b\u044b\u0448 \u0438 \u041a\u0430\u0440\u043b\u0441\u043e\u043d"
description: "We have a strictly convex polygon whose vertices are integer lattice points and are listed counterclockwise. We need a straight line that divides the polygon into two regions of exactly the same area."
date: "2026-08-14T13:42:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "K"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 246
verified: false
draft: false
---

[CF 102386K - \u041c\u0430\u043b\u044b\u0448 \u0438 \u041a\u0430\u0440\u043b\u0441\u043e\u043d](https://codeforces.com/problemset/problem/102386/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We have a strictly convex polygon whose vertices are integer lattice points and are listed counterclockwise. We need a straight line that divides the polygon into two regions of exactly the same area. The line itself must contain two distinct integer lattice points, so equivalently we need an area-bisecting line with rational slope and rational intercept.

The key geometric freedom is that we are allowed to choose any line, not necessarily one passing through polygon vertices. However, choosing a particular vertex gives us a much stronger structure. Fix the first vertex (V_0). As a point (P) moves along the polygon boundary from (V_1) toward (V_{n-1}), the line (V_0P) sweeps through all possible cuts whose one endpoint on the boundary is (V_0). For every boundary position (P), the area on one side of (V_0P) changes continuously from zero to the whole polygon area. Since the polygon is convex, exactly one such (P) gives half the area.

The input has at most (1000) vertices, and every coordinate has absolute value at most (10^5). A direct (O(n^2)) solution is already numerically small at this limit, roughly one million elementary geometric operations, but the structure allows an (O(n)) construction. The coordinate bound also makes exact integer arithmetic practical. A cross product of two coordinate differences is at most about (8\cdot10^{10}), and the sum over at most (1000) triangles is below (10^{14}). Python integers have no overflow problem here, while even signed 64-bit arithmetic would be sufficient for the area calculations.

There are several edge cases that can silently break a floating-point implementation. First, the required cut can pass exactly through another polygon vertex. For example,

```
4
0 0
4 0
4 2
0 2
```

has area (8), and the diagonal from ((0,0)) to ((4,2)) divides it into two areas of (4). A comparison involving floating-point parameters can accidentally put the endpoint into the next edge. Exact integer comparisons avoid this.

Another case is when the half-area point lies strictly inside an edge. The sample has exactly this behavior for the cut through (y=4). The line does not pass through a polygon vertex, but the intersection with the right vertical edge is an integer point. More generally that intersection is only guaranteed to be rational, not integer. We must construct an integer direction for the entire line rather than requiring the intersection itself to be an integer point.

Finally, the total doubled area can be odd. In the sample the doubled area is (15), so half of it is (15/2). A solution based on integer area alone would incorrectly conclude that an exact cut is impossible. The cut point can simply have rational coordinates, and the resulting line still has an integer direction after scaling.

## Approaches

A natural brute-force construction starts by choosing a polygon vertex (V_i) as the fixed endpoint of the cutting line. We can then walk around the remaining boundary, determine on which edge the half-area intersection lies, and solve for the position along that edge. If this entire search is repeated independently for every (V_i), it takes (O(n^2)) time. For (n=1000), this is around (10^6) edge checks, so it is not actually excluded by the given constraints, but it repeats exactly the same geometric work many times.

The useful observation is that we do not need to try every vertex. Pick (V_0) once. The polygon can be divided into the triangles

[
(V_0,V_1,V_2),\quad
(V_0,V_2,V_3),\quad\ldots,\quad
(V_0,V_{n-2},V_{n-1}).
]

Because the polygon is strictly convex and counterclockwise, all these triangles have positive area, and their areas add up to the area of the polygon.

Suppose the required half-area point lies on edge (V_iV_{i+1}). The region bounded by (V_0), the boundary chain (V_0,V_1,\ldots,V_i,P), and the segment (PV_0) consists of all preceding fan triangles plus triangle (V_0V_iP). Along the edge (V_iV_{i+1}), the latter triangle's area is linear in the position of (P). Consequently, once we know the edge containing the target, the exact position of (P) is just a rational fraction of that edge.

The final step is the part that makes the lattice requirement easy. Write

[
P=V_i+\frac pq(V_{i+1}-V_i).
]

Then

(q-p)(V_i-V_0)+p(V_{i+1}-V_0).
]

The vector on the right has integer coordinates. It is a direction vector of the desired line, so (V_0) and (V_0+D) are two integer points on the cutting line. There is no need to construct (P) using floating-point coordinates at all.

This also proves that a valid answer always exists under the problem's guarantees. The (-1) output case is never reached for a valid input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Try every vertex and scan the boundary | (O(n^2)) | (O(n)) | Accepted for (n\le1000), but unnecessary |
| Fix one vertex and scan the fan once | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Choose (V_0) as the fixed vertex of the cutting line. Since the polygon is convex, every line from (V_0) to a point on the opposite boundary cuts off a well-defined region whose area grows continuously from zero to the full polygon area.
2. Compute the doubled area (S) of the polygon using a fan from (V_0). For each (i=1,\ldots,n-2), calculate

[
T_i=\operatorname{cross}(V_i-V_0,V_{i+1}-V_0).
]

The sum of all (T_i) is exactly the doubled polygon area (S).

1. Walk through the fan triangles while maintaining `prefix`, the doubled area of all complete triangles before the current edge (V_iV_{i+1}). The half-area target is (S/2). To avoid fractions, test

[
2\cdot prefix\le S\le2(prefix+T_i).
]

The first edge satisfying this condition contains the desired boundary point (P). The convexity and positive triangle areas guarantee that exactly one edge is needed, apart from harmless equality at a shared vertex.

1. Let

[
r=S-2\cdot prefix.
]

This is twice the amount of doubled area still needed inside triangle (V_0V_iV_{i+1}). If (P) divides (V_iV_{i+1}) in the ratio (p), then

[
\frac pq=\frac{r}{2T_i}.
]

Reduce this fraction by their greatest common divisor. We use integers throughout, so even an odd (S) causes no special case.

1. Define

[
a=V_i-V_0,\qquad b=V_{i+1}-V_0.
]

The vector from (V_0) toward (P), multiplied by (q), is

[
D=(q-p)a+pb.
]

Both (a) and (b) are integer vectors, so (D) is an integer vector. Since (P) is on the polygon boundary and the cut has positive area on both sides, (D) cannot be zero.

1. Output (V_0) and (V_0+D). They are distinct integer points on the same area-bisecting line.

The invariant behind the construction is that `prefix` always equals the doubled area of the part already swept off by the line (V_0P). Each next fan triangle adds a positive amount, so eventually the target (S/2) lies inside exactly one triangle. Inside that triangle, area depends linearly on the position of (P), which gives the exact rational parameter used to construct the integer direction vector.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def solve():
    n = int(input())
    p = [tuple(map(int, input().split())) for _ in range(n)]

    x0, y0 = p[0]

    triangles = []
    total = 0

    for i in range(1, n - 1):
        xi, yi = p[i]
        xj, yj = p[i + 1]

        ax = xi - x0
        ay = yi - y0
        bx = xj - x0
        by = yj - y0

        t = cross(ax, ay, bx, by)
        triangles.append(t)
        total += t

    prefix = 0

    for i in range(1, n - 1):
        t = triangles[i - 1]

        if 2 * prefix <= total <= 2 * (prefix + t):
            r = total - 2 * prefix
            den = 2 * t

            g = gcd(r, den)
            num = r // g
            den //= g

            xi, yi = p[i]
            xj, yj = p[i + 1]

            ax = xi - x0
            ay = yi - y0
            bx = xj - x0
            by = yj - y0

            dx = (den - num) * ax + num * bx
            dy = (den - num) * ay + num * by

            print(x0, y0)
            print(x0 + dx, y0 + dy)
            return

        prefix += t

if __name__ == "__main__":
    solve()
```

The first loop computes all fan triangle areas. Using vectors relative to (V_0) avoids having to write the full shoelace formula and makes the later direction construction use exactly the same quantities.

The second loop searches for the target triangle. The comparison is deliberately written as `2 * prefix <= total <= 2 * (prefix + t)`. This handles both even and odd total doubled areas and never converts anything to `float`.

Once the target edge is found, `r / den` is the fraction (p/q) describing the position of the half-area point along that edge. `gcd` is not required for correctness, but reducing the fraction keeps the resulting direction vector smaller.

The expression

```
dx = (den - num) * ax + num * bx
```

is the integer form of

[
q(P-V_0)=(q-p)(V_i-V_0)+p(V_{i+1}-V_0).
]

The output point can be much farther away than the original polygon, which is allowed. Its size is still safely below (10^{18}). Each coordinate difference in the original polygon is at most (2\cdot10^5), each fan triangle has doubled area at most (8\cdot10^{10}), and after scaling the resulting direction coordinates remain far below (10^{18}).

The implementation never prints `-1`, because the construction proves that a valid lattice line exists for every polygon satisfying the input guarantees.

## Worked Examples

For the provided sample, the polygon is

```
(0,3), (3,0), (3,6), (0,7)
```

The fan from (V_0=(0,3)) has two triangles.

| Edge | `prefix` | `t` | `total` | Target condition | `r / (2t)` |
| --- | --- | --- | --- | --- | --- |
| (V_1V_2) | 0 | 18 | 30 | (0\le30\le36) | (30/36=5/6) |

The target lies on (V_1V_2). Thus (p=5), (q=6). Relative to (V_0),

[
V_1-V_0=(3,-3),
\qquad
V_2-V_0=(3,3).
]

The integer direction is

[
(6-5)(3,-3)+5(3,3)=(18,12).
]

The program can consequently output

```
0 3
18 15
```

The line has slope (12/18=2/3). The sample's line (y=4) is another valid answer, so different correct outputs are expected.

As a second example, consider a right triangle.

```
3
0 0
4 0
0 4
```

There is only one fan triangle.

| Edge | `prefix` | `t` | `total` | `r` | Reduced fraction |
| --- | --- | --- | --- | --- | --- |
| (V_1V_2) | 0 | 16 | 16 | 16 | (1/2) |

The half-area point is the midpoint of (V_1V_2), so the cutting line goes from ((0,0)) to ((2,2)). The direction formula gives

[
(2-1)(4,0)+1(0,4)=(4,4).
]

Thus the program outputs

```
0 0
4 4
```

The line (y=x) splits the triangle into two congruent triangles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | One pass computes the fan areas and one pass locates the target edge |
| Space | (O(n)) | The vertices and fan triangle areas are stored |

The linear solution easily fits (n\le1000). The dominant operations are integer additions, multiplications, comparisons, and one gcd computation. All geometric decisions are exact, so the solution does not depend on numerical precision.

## Test Cases

The test harness below checks the produced line geometrically with exact `Fraction` arithmetic. This is useful because the answer is not unique, so comparing the output against one particular pair of points would incorrectly reject many correct solutions.

```python
import sys
import io
from fractions import Fraction
from math import gcd, atan2

def solve_text(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    p = [(int(next(it)), int(next(it))) for _ in range(n)]

    x0, y0 = p[0]

    triangles = []
    total = 0

    for i in range(1, n - 1):
        xi, yi = p[i]
        xj, yj = p[i + 1]

        ax = xi - x0
        ay = yi - y0
        bx = xj - x0
        by = yj - y0

        t = ax * by - ay * bx
        triangles.append(t)
        total += t

    prefix = 0

    for i in range(1, n - 1):
        t = triangles[i - 1]

        if 2 * prefix <= total <= 2 * (prefix + t):
            r = total - 2 * prefix
            den = 2 * t

            g = gcd(r, den)
            num = r // g
            den //= g

            xi, yi = p[i]
            xj, yj = p[i + 1]

            ax = xi - x0
            ay = yi - y0
            bx = xj - x0
            by = yj - y0

            dx = (den - num) * ax + num * bx
            dy = (den - num) * ay + num * by

            return f"{x0} {y0}\n{x0 + dx} {y0 + dy}\n"

        prefix += t

    return "-1\n"

def polygon_area2(poly):
    s = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - y1 * x2
    return s

def clip_halfplane(poly, A, B, keep_positive):
    ax, ay = A
    bx, by = B
    dx = bx - ax
    dy = by - ay

    def side(P):
        px, py = P
        return dx * (py - ay) - dy * (px - ax)

    result = []

    for i in range(len(poly)):
        P = poly[i]
        Q = poly[(i + 1) % len(poly)]

        fP = side(P)
        fQ = side(Q)

        inP = fP >= 0 if keep_positive else fP <= 0
        inQ = fQ >= 0 if keep_positive else fQ <= 0

        if inP:
            result.append(P)

        if inP != inQ:
            t = Fraction(fP, fP - fQ)
            x = P[0] + t * (Q[0] - P[0])
            y = P[1] + t * (Q[1] - P[1])
            result.append((x, y))

    return result

def area2_fraction(poly):
    if len(poly) < 3:
        return Fraction(0)

    s = Fraction(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - y1 * x2
    return abs(s)

def valid_answer(inp: str, out: str) -> bool:
    data = inp.strip().split()
    n = int(data[0])
    poly = []
    pos = 1

    for _ in range(n):
        poly.append((int(data[pos]), int(data[pos + 1])))
        pos += 2

    ans = out.strip().split()
    if len(ans) != 4:
        return False

    A = (int(ans[0]), int(ans[1]))
    B = (int(ans[2]), int(ans[3]))

    if A == B:
        return False

    if any(abs(v) > 10**18 for v in A + B):
        return False

    total = Fraction(abs(polygon_area2(poly)))

    positive = clip_halfplane(poly, A, B, True)
    negative = clip_halfplane(poly, A, B, False)

    ap = area2_fraction(positive)
    an = area2_fraction(negative)

    return ap * 2 == total or an * 2 == total

def make_max_polygon():
    vectors = []

    for x in range(1, 51):
        for y in range(0, 51):
            if x == 0 and y == 0:
                continue
            if gcd(x, y) == 1:
                vectors.append((x, y))

    vectors.sort(key=lambda v: atan2(v[1], v[0]))
    vectors = vectors[:500]

    edges = vectors[:]

    for x, y in vectors:
        edges.append((-x, -y))

    poly = []
    x = 0
    y = 0

    for dx, dy in edges:
        poly.append((x, y))
        x += dx
        y += dy

    min_x = min(x for x, y in poly)
    max_x = max(x for x, y in poly)
    min_y = min(y for x, y in poly)
    max_y = max(y for x, y in poly)

    shift_x = -(min_x + max_x) // 2
    shift_y = -(min_y + max_y) // 2

    return [(x + shift_x, y + shift_y) for x, y in poly]

sample1 = """\
4
0 3
3 0
3 6
0 7
"""

assert valid_answer(sample1, solve_text(sample1)), "sample 1"

triangle = """\
3
0 0
4 0
0 4
"""

assert valid_answer(triangle, solve_text(triangle)), "minimum-size triangle"

half_vertex = """\
4
0 0
4 0
4 2
0 2
"""

assert valid_answer(half_vertex, solve_text(half_vertex)), "half-area at a vertex"

boundary_coordinates = """\
3
-100000 -100000
100000 -100000
0 100000
"""

assert valid_answer(
    boundary_coordinates,
    solve_text(boundary_coordinates)
), "boundary coordinates"

max_poly = make_max_polygon()
assert len(max_poly) == 1000
assert max(abs(x) <= 10**5 and abs(y) <= 10**5 for x, y in max_poly)

max_input = str(len(max_poly)) + "\n"
max_input += "\n".join(f"{x} {y}" for x, y in max_poly) + "\n"

assert valid_answer(max_input, solve_text(max_input)), "maximum-size polygon"

# A polygon with all coordinates equal cannot satisfy the input guarantees:
# three distinct vertices would be impossible. Such a test is intentionally
# excluded because it is not a valid instance of the problem.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided sample | Any exact half-area line, such as the program's output | Rational intersection strictly inside an edge |
| (3)-vertex right triangle | A line through two integer points bisecting the triangle | Minimum valid polygon |
| (4\times2) rectangle | A diagonal through an opposite vertex | Half-area target exactly at a fan-triangle boundary |
| Triangle using (\pm10^5) coordinates | Any valid integer line within the (10^{18}) output bound | Boundary coordinate arithmetic |
| Generated (1000)-vertex polygon | Any valid integer line | Maximum (n) and linear scan |
| All coordinates equal | No valid input exists | Confirms why this cannot be a legitimate test case |

## Edge Cases

When the half-area point is exactly a polygon vertex, the target can be shared by two consecutive fan triangles. For

```
4
0 0
4 0
4 2
0 2
```

the first fan triangle has doubled area (8), while the whole polygon has doubled area (16). The target is reached exactly at (V_2=(4,2)). The integer comparison accepts the first edge with equality, giving the direction (V_2-V_0=(4,2)). No epsilon is involved.

When the half-area point lies strictly inside an edge, the parameter is rational. In the sample, the first fan triangle has doubled area (18), while the total is (30). The required fraction is

[
\frac{30}{36}=\frac56.
]

The point is consequently rational, but the scaled direction

[
(6-5)(3,-3)+5(3,3)=(18,12)
]

is integral. The output line therefore contains two integer points even though its boundary intersection does not need to be an integer point.

When the total doubled area is odd, the algorithm still works unchanged. If (S=15), the target is (7.5) in doubled-area units. The comparison multiplies everything by two, so it searches for

[
2\cdot prefix\le15\le2(prefix+T_i).
]

The resulting numerator is odd, but `gcd` reduces the rational fraction normally. No parity assumption about the polygon area is required.

When coordinates are near the input limit, all computations remain exact. The polygon coordinates contribute differences of at most (2\cdot10^5), and a single fan triangle has doubled area at most (8\cdot10^{10}). Even after scaling the rational direction, the output coordinates stay comfortably below (10^{18}). Python's arbitrary-precision integers make the arithmetic straightforward.

A degenerate input with all vertices equal, or with three collinear vertices, would invalidate the geometric assumptions used by the construction. Such inputs are explicitly excluded by the problem, so the algorithm does not need defensive handling for them.
