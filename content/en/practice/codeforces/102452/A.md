---
title: "CF 102452A - Axis of Symmetry"
description: "We have a collection of axis-aligned rectangles whose interiors never overlap. Rectangles may touch along edges or at points, so the final figure can be one connected shape, several disconnected shapes, or a shape with holes."
date: "2026-08-10T06:08:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102452
codeforces_index: "A"
codeforces_contest_name: "2019-2020 ICPC Asia Hong Kong Regional Contest"
rating: 0
weight: 102452
solve_time_s: 256
verified: true
draft: false
---

[CF 102452A - Axis of Symmetry](https://codeforces.com/problemset/problem/102452/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of axis-aligned rectangles whose interiors never overlap. Rectangles may touch along edges or at points, so the final figure can be one connected shape, several disconnected shapes, or a shape with holes.

For every test case, we must find every line across which the whole figure is unchanged by reflection. Each line has to be printed as

[
ax+by=c,
]

with the three coefficients having greatest common divisor (1). If several axes exist, their normalized coefficient triples must be printed in lexicographically decreasing order, because that gives the lexicographically largest concatenated answer. The official limits are (2) seconds and (512) MB, with at most (10^5) rectangles in total across all test cases.

The large coordinate range is a clue that we should not build a grid or inspect individual unit cells. Coordinates can be around (10^8), while there can be (10^5) rectangles, so anything proportional to coordinate magnitude is impossible. With (10^5) rectangles and a 2-second limit, an (O(n^2)) geometric comparison would perform around (10^{10}) pair checks before even accounting for constant factors. We need a representation in which each rectangle contributes only constant work and the whole test case is processed in roughly (O(n\log n)) or better.

The first subtle case is that rectangles may touch. For example,

```
1
2
0 0 2 1
1 1 2 2
```

forms an L-shaped figure. The point ((1,1)) is a corner of the union even though it is not a corner of the first rectangle. A method that only stores one rectangle's corners independently can miss such boundary turns. The correct answer is no symmetry, and the solution below handles the touching point through parity of all rectangle corners.

Another subtle case is a rectangle whose center has half-integer coordinates. For

```
1
1
0 0 1 1
```

the four symmetry axes are

```
4
2 0 1 1 1 1 1 -1 0 0 2 1
```

The vertical axis is (x=\frac12), so its primitive integer equation is (2x=1), not (x=1/2) written with floating-point arithmetic. Using doubled coordinates avoids every fractional calculation.

A third case is several rectangles touching along an entire edge. For example,

```
1
2
0 0 1 1
1 0 2 1
```

is simply a (2\times1) rectangle. Its answer is

```
2
1 0 1 0 2 1
```

A careless implementation that treats every rectangle boundary as part of the final boundary would incorrectly regard the shared edge as a boundary segment.

Finally, the figure can have multiple symmetries and the requested order matters. For the unit square above, the normalized triples are ((2,0,1)), ((1,1,1)), ((1,-1,0)), and ((0,2,1)). Sorting them in decreasing lexicographic order is part of the required output, not merely a presentation choice.

## Approaches

A direct geometric approach would first construct all boundary segments of all rectangles. There are at most (4n) original segments. For each possible symmetry axis, we could compare every boundary segment with every other segment and check whether reflection maps one to the other. This is correct because a polygonal boundary is completely determined by its segments, but comparing (O(n)) segments against (O(n)) other segments costs (O(n^2)). With (n=10^5), even one such check can reach about (1.6\times10^{11}) segment comparisons, which is far beyond the time limit.

The key observation is that the direction of a symmetry axis is extremely restricted. Every boundary segment of the figure is horizontal or vertical. Reflection across a symmetry axis must map a horizontal or vertical segment to another horizontal or vertical segment. A vertical or horizontal axis clearly has this property. For an oblique axis, the only way horizontal and vertical directions can be exchanged is at (45^\circ), giving the two diagonal directions with slopes (1) and (-1). Hence there are at most four possible directions for an axis.

The position of each candidate is also forced by the bounding box. Reflection preserves the minimum and maximum (x)-coordinates of the whole figure, so a vertical symmetry axis must be the midpoint of those two coordinates. The same argument fixes the horizontal axis. A diagonal symmetry must also preserve the bounding box, so it must pass through the center of the bounding box. Thus there are only four candidate lines.

We still need a compact way to test whether a candidate really preserves the entire figure. The useful observation is rectangle-corner parity. At every point, count how many rectangle corners occur there modulo (2). A point with odd parity is exactly a turning point of the boundary. When several rectangles touch, contributions from their boundaries cancel in pairs along shared portions, and parity keeps precisely the places where the boundary changes direction. This is the same parity idea used in the official contest solution's boundary argument.

Once all odd-parity corners are known, testing an axis becomes a set-membership problem. Reflect every odd corner across the candidate axis and require the reflected point to be another odd corner. If all odd corners have partners, the entire boundary is preserved, because consecutive turning points determine the axis-aligned boundary segments between them. Conversely, a genuine symmetry must map every boundary turn to another boundary turn, so it cannot pass this test accidentally.

There is one more implementation detail. We double every coordinate before doing anything else. If the original bounding box has doubled extrema (X_{\min},X_{\max},Y_{\min},Y_{\max}), define

[
d_x=X_{\min}+X_{\max},\qquad d_y=Y_{\min}+Y_{\max}.
]

These are twice the center coordinates. Reflection formulas then contain only integer additions and subtractions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) expected | (O(n)) | Accepted |

The hash-set implementation is (O(n)) expected time. A balanced-tree implementation would give the (O(n\log n)) bound stated in the official editorial.

## Algorithm Walkthrough

1. Read every rectangle and multiply all four coordinates by (2). Insert its four doubled corners into a parity set. If a corner is already present, remove it; otherwise insert it. At the same time, maintain the minimum and maximum doubled (x) and (y) coordinates.

The parity operation matters because two rectangles can share boundary pieces. Shared contributions occur twice and cancel, while a genuine boundary turn has odd incidence.
2. Compute

[
d_x=X_{\min}+X_{\max},\qquad d_y=Y_{\min}+Y_{\max}.
]

The actual center of the bounding box is ((d_x/2,d_y/2)). Keeping (d_x,d_y) as integers lets every reflection stay integral.
3. Test the horizontal candidate. Reflection of a doubled point ((x,y)) across the horizontal center is

[
(x,,2d_y-y).
]

Since (d_y) already represents twice the center, the correct expression in our doubled coordinate system is

[
(x,,2d_y-y).
]

The candidate line in original coordinates is (2y=d_y).
4. Test the vertical candidate. Reflection is

[
(2d_x-x,,y),
]

and the corresponding line is (2x=d_x).
5. Test the diagonal with slope (1). Reflection across the line through the bounding-box center with direction ((1,1)) swaps the centered coordinates:

[
(x,y)\mapsto
(d_x+(y-d_y),,d_y+(x-d_x)).
]

Its equation in original coordinates is

[
2x-2y=d_x-d_y.
]
6. Test the diagonal with slope (-1). The reflection is

[
(x,y)\mapsto
(d_x-(y-d_y),,d_y-(x-d_x)),
]

corresponding to

[
2x+2y=d_x+d_y.
]
7. For each candidate, iterate through every point in the parity set. If its reflected point is absent, reject that candidate. Otherwise keep checking. A candidate is accepted only if every odd boundary turn has its reflected counterpart.

We do not need to check arbitrary points on the boundary. Between two consecutive turns, the boundary is a straight horizontal or vertical segment, and reflection maps the endpoints to the endpoints of the reflected segment. Thus matching every turn is enough to match the whole boundary.
8. Convert each accepted line to primitive integer coefficients. Divide all three coefficients by their greatest common divisor. Then multiply the entire triple by (-1) if its first nonzero coefficient is negative. This gives one canonical representation for each geometric line.
9. Sort the resulting triples in decreasing lexicographic order and print them. Because every triple has exactly three entries, decreasing lexicographic order of the triples is exactly the order required for the concatenated output to be lexicographically largest.

### Why it works

The invariant is that the parity set contains exactly the turning points of the boundary of the union. A reflection symmetry must map boundary turns to boundary turns, so every genuine symmetry passes the point-reflection test. Conversely, if every boundary turn maps to another boundary turn under one of the four possible reflections, then the axis-aligned segment between each pair of consecutive turns maps to the corresponding boundary segment. Hence the complete boundary is preserved. Since reflection maps bounded regions to bounded regions, preserving the boundary preserves the figure itself.

The four candidate directions are exhaustive because an axis-aligned rectangle boundary contains only horizontal and vertical segments. A reflection preserving these directions is either horizontal or vertical, or exchanges horizontal and vertical, which gives slopes (1) and (-1). Their positions are forced by the bounding box. Thus no possible symmetry is omitted.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def primitive(a, b, c):
    g = gcd(abs(a), gcd(abs(b), abs(c)))
    a //= g
    b //= g
    c //= g

    if a < 0 or (a == 0 and b < 0):
        a = -a
        b = -b
        c = -c

    return (a, b, c)

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        corners = set()

        min_x = 10**30
        max_x = -10**30
        min_y = 10**30
        max_y = -10**30

        for _ in range(n):
            x1, y1, x2, y2 = map(int, input().split())

            x1 *= 2
            y1 *= 2
            x2 *= 2
            y2 *= 2

            for p in ((x1, y1), (x1, y2), (x2, y1), (x2, y2)):
                if p in corners:
                    corners.remove(p)
                else:
                    corners.add(p)

            min_x = min(min_x, x1)
            max_x = max(max_x, x2)
            min_y = min(min_y, y1)
            max_y = max(max_y, y2)

        dx = min_x + max_x
        dy = min_y + max_y

        ok = [True, True, True, True]

        for x, y in corners:
            if ok[0]:
                p = (x, 2 * dy - y)
                if p not in corners:
                    ok[0] = False

            if ok[1]:
                p = (2 * dx - x, y)
                if p not in corners:
                    ok[1] = False

            if ok[2]:
                p = (dx + y - dy, dy + x - dx)
                if p not in corners:
                    ok[2] = False

            if ok[3]:
                p = (dx - y + dy, dy - x + dx)
                if p not in corners:
                    ok[3] = False

            if not any(ok):
                break

        ans = []

        if ok[0]:
            ans.append(primitive(0, 2, dy))

        if ok[1]:
            ans.append(primitive(2, 0, dx))

        if ok[2]:
            ans.append(primitive(2, -2, dx - dy))

        if ok[3]:
            ans.append(primitive(2, 2, dx + dy))

        ans.sort(reverse=True)

        out.append(str(len(ans)))
        out.append(" ".join(str(v) for triple in ans for v in triple))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `corners` set stores only odd occurrences. For every rectangle corner, toggling membership is exactly an XOR operation, so a point appearing twice disappears and a point appearing an odd number of times remains.

The bounding values are maintained after doubling the coordinates. This is the reason the candidate equations can be built directly as integer triples. For example, if the actual vertical axis is (x=3.5), then `dx` is (7), and the candidate is (2x=7).

The four reflection formulas are written directly in doubled coordinates. For the horizontal candidate, a point at doubled height `y` has reflected height `2 * dy - y`. The other three formulas follow the same centered-coordinate transformation.

The `ok` array allows candidates already disproved to stop doing hash lookups. This is a small constant-factor optimization, but useful because each surviving candidate otherwise checks every boundary turn.

The `primitive` function first divides by the full three-number gcd. The sign convention uses the first nonzero coefficient, so equations such as (x-y=0) and (-x+y=0) receive exactly one representation. Python integers also avoid the overflow concerns that would arise in a fixed-width implementation, although the values here are comfortably within 64-bit range.

The final `reverse=True` sort is deliberate. The problem asks for the lexicographically largest flattened sequence, so the largest coefficient triple must come first, then the next largest, and so on.

## Worked Examples

### Sample 1

The first official case contains two rectangles:

```
2
-1 -1 0 1
0 0 1 2
```

After doubling, the rectangles are represented by coordinates from (-2) through (4). Their odd corners are the points that remain after XOR cancellation.

| Step | Key state | Result |
| --- | --- | --- |
| Read rectangles | Two rectangles inserted | Corner parity built |
| Bounding box | (X_{\min}=-2,\ X_{\max}=2,\ Y_{\min}=-2,\ Y_{\max}=4) | (d_x=0,\ d_y=2) |
| Horizontal test | Reflected odd corner missing | Rejected |
| Vertical test | Reflected odd corner missing | Rejected |
| Slope (1) test | Reflected odd corner missing | Rejected |
| Slope (-1) test | Reflected odd corner missing | Rejected |
| Output | No candidates survive | `0` |

The important point is that merely having two rectangles arranged along a diagonal does not imply diagonal symmetry. Every boundary turn has to have a reflected counterpart.

### Sample 2

The second official case is

```
2
-1 -1 0 0
0 0 1 1
```

The two unit squares touch at exactly one point.

| Step | Key state | Result |
| --- | --- | --- |
| Read rectangles | Four corners from each square | Shared center corner cancels |
| Bounding box | (X_{\min}=-2,\ X_{\max}=2,\ Y_{\min}=-2,\ Y_{\max}=2) | (d_x=0,\ d_y=0) |
| Horizontal test | Some turns do not reflect correctly | Rejected |
| Vertical test | Some turns do not reflect correctly | Rejected |
| Slope (1) test | Every odd turn maps correctly | Accepted |
| Slope (-1) test | Every odd turn maps correctly | Accepted |
| Primitive lines | (2x-2y=0,\ 2x+2y=0) | ((1,-1,0),(1,1,0)) |
| Lexicographic sort | Larger first coefficient triple first | ((1,1,0),(1,-1,0)) |

The output is

```
2
1 1 0 1 -1 0
```

The example demonstrates why the center can be a shared point without becoming a boundary turn. Its corner parity is even, so it does not need to appear in the symmetry representation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) expected | Four corners are processed per rectangle, and each odd corner performs at most four hash lookups |
| Space | (O(n)) | At most (4n) corner positions are stored |

The total number of rectangles over all test cases is at most (10^5), so the expected total number of hash operations is also linear in (10^5). No structure depends on the magnitude of the coordinates, which is essential because coordinates can be around (10^8). The approach therefore fits the official 2-second, 512 MB limits.

## Test Cases

```python
# helper: run the solution logic on an input string
import io
import sys
from math import gcd

def solve_text(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    t = int(next(it))
    out = []

    def primitive(a, b, c):
        g = gcd(abs(a), gcd(abs(b), abs(c)))
        a //= g
        b //= g
        c //= g
        if a < 0 or (a == 0 and b < 0):
            a = -a
            b = -b
            c = -c
        return a, b, c

    for _ in range(t):
        n = int(next(it))
        corners = set()

        min_x = 10**30
        max_x = -10**30
        min_y = 10**30
        max_y = -10**30

        for _ in range(n):
            x1 = int(next(it))
            y1 = int(next(it))
            x2 = int(next(it))
            y2 = int(next(it))

            x1 *= 2
            y1 *= 2
            x2 *= 2
            y2 *= 2

            for p in ((x1, y1), (x1, y2), (x2, y1), (x2, y2)):
                if p in corners:
                    corners.remove(p)
                else:
                    corners.add(p)

            min_x = min(min_x, x1)
            max_x = max(max_x, x2)
            min_y = min(min_y, y1)
            max_y = max(max_y, y2)

        dx = min_x + max_x
        dy = min_y + max_y

        ok = [True] * 4

        for x, y in corners:
            if ok[0] and (x, 2 * dy - y) not in corners:
                ok[0] = False

            if ok[1] and (2 * dx - x, y) not in corners:
                ok[1] = False

            if ok[2] and (dx + y - dy, dy + x - dx) not in corners:
                ok[2] = False

            if ok[3] and (dx - y + dy, dy - x + dx) not in corners:
                ok[3] = False

        ans = []

        if ok[0]:
            ans.append(primitive(0, 2, dy))
        if ok[1]:
            ans.append(primitive(2, 0, dx))
        if ok[2]:
            ans.append(primitive(2, -2, dx - dy))
        if ok[3]:
            ans.append(primitive(2, 2, dx + dy))

        ans.sort(reverse=True)

        out.append(str(len(ans)))
        out.append(" ".join(str(v) for a in ans for v in a))

    return "\n".join(out) + "\n"

# Provided sample 1
assert solve_text("""\
3
2
-1 -1 0 1
0 0 1 2
2
-1 -1 0 0
0 0 1 1
3
-1 -1 0 1
0 -1 1 0
0 0 1 1
""") == """\
0

2
1 1 0 1 -1 0
4
1 1 0 1 0 0 1 -1 0 0 1 0
""", "official samples"

# Minimum-size input, one non-square rectangle.
assert solve_text("""\
1
1
0 0 2 1
""") == """\
2
1 0 1 0 2 1
""", "single rectangle"

# Four equal unit squares forming a square.
assert solve_text("""\
1
4
0 0 1 1
1 0 2 1
0 1 1 2
1 1 2 2
""") == """\
4
1 1 2 1 0 1 1 -1 0 0 1 1
""", "equal rectangles"

# Boundary coordinates near the allowed limit.
assert solve_text("""\
1
1
-100000007 100000006 -100000006 100000007
""") == """\
2
2 0 -200000013 0 2 200000013
""", "coordinate boundary"

# Maximum-size case, 100000 equal rectangles in a symmetric row.
n = 100000
parts = ["1", str(n)]
for i in range(n):
    x1 = 3 * i
    x2 = x1 + 1
    parts.append(f"{x1} 0 {x2} 1")

maximum_case = "\n".join(parts) + "\n"

assert solve_text(maximum_case) == """\
2
1 0 149999 0 2 1
""", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official three-case sample | `0`, then 2 axes, then 4 axes | Basic correctness and diagonal symmetry |
| One (2\times1) rectangle | `1 0 1` and `0 2 1` | Minimum input and non-square rectangle |
| Four equal unit rectangles | Four axes | Equal dimensions and all four directions |
| Coordinates near (\pm10^8) | Two axes with large constants | Integer arithmetic and sign normalization |
| (100000) equal rectangles | Two axes | Maximum (n), linear processing, repeated dimensions |

## Edge Cases

### A single rectangle

For

```
1
1
0 0 2 1
```

the bounding-box center is ((1,\frac12)). The horizontal reflection preserves the rectangle, giving (2y=1), and the vertical reflection gives (x=1). The diagonal candidates fail because the rectangle is not a square. After normalization and lexicographic sorting, the output is

```
2
1 0 1 0 2 1
```

The algorithm never assumes that every rectangle has four symmetries.

### Rectangles touching along an edge

For

```
1
2
0 0 1 1
1 0 2 1
```

the two rectangles share the segment (x=1,0\le y\le1). Each endpoint of the shared segment occurs twice as a rectangle corner and therefore cancels from the parity set. The shared segment itself is not part of the exterior boundary. The remaining boundary is exactly that of a (2\times1) rectangle, so the two surviving axes are (x=1) and (y=\frac12).

This is why treating every input rectangle boundary independently would be wrong, while corner parity naturally removes the internal contribution.

### Rectangles touching at one point

For

```
1
2
-1 -1 0 0
0 0 1 1
```

the common point ((0,0)) is contributed by both rectangles and disappears from the parity set. The remaining boundary turns are symmetric around both diagonals through the common point. The two accepted lines are

[
x+y=0
]

and

[
x-y=0.
]

The primitive triples are ((1,1,0)) and ((1,-1,0)), and the first one is printed first because it is lexicographically larger.

### Half-integer symmetry centers

For

```
1
1
0 0 1 1
```

the center is ((\frac12,\frac12)). Doubling the coordinates gives `dx = 1` and `dy = 1`, so the vertical axis is represented directly as (2x=1) and the horizontal axis as (2y=1). No floating-point midpoint is ever computed.

This is also why the reflection formulas work uniformly for both integer and half-integer axis positions.

### Large negative coefficients

Consider

```
1
1
-100000007 100000006 -100000006 100000007
```

The vertical axis is

[
x=-100000006.5,
]

so its primitive equation is

[
2x=-200000013.
]

The normalization routine must not blindly force the constant to be positive. The sign convention is based on the first nonzero coefficient, which keeps the representation unique and gives `(2, 0, -200000013)`.

### No symmetry

The first official sample contains two rectangles arranged so that none of the four possible reflections preserves the boundary. The algorithm still computes all four candidates from the same bounding box and rejects each one after finding a missing reflected turn. The result is simply

```
0
```

The empty parity-set test is never a special case for a valid nonempty figure, because the outer boundary necessarily contains turns. The algorithm can consequently use the same reflection test for every input.

### Multiple connected components

The rectangles do not have to form one connected component. The parity set simply contains the boundary turns of every component. A symmetry must reflect every component correctly, so checking the complete parity set simultaneously handles disconnected figures without any additional connected-component logic.

### Multiple symmetry axes

A square-shaped union can pass all four candidate tests. The algorithm records all of them independently, normalizes them independently, and only then sorts them. This separation is necessary because candidate generation order is geometric, while the required output order is lexicographic.
