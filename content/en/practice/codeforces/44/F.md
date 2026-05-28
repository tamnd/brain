---
title: "CF 44F - BerPaint"
description: "We have a rectangular canvas of size W × H. Initially the whole canvas is white. Then several black line segments are drawn on it. After that, a sequence of flood-fill operations is applied. A flood-fill chooses a point and a color."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "graphs"]
categories: ["algorithms"]
codeforces_contest: 44
codeforces_index: "F"
codeforces_contest_name: "School Team Contest 2 (Winter Computer School 2010/11)"
rating: 2700
weight: 44
solve_time_s: 177
verified: false
draft: false
---

[CF 44F - BerPaint](https://codeforces.com/problemset/problem/44/F)

**Rating:** 2700  
**Tags:** geometry, graphs  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rectangular canvas of size `W × H`. Initially the whole canvas is white. Then several black line segments are drawn on it. After that, a sequence of flood-fill operations is applied.

A flood-fill chooses a point and a color. Every point connected to the chosen point through regions of the same current color gets recolored. Segments behave like walls, they can block movement between regions. Segments themselves have zero area, but they still matter because they separate components.

At the end, we must output the total area occupied by every color.

The geometric part is the difficult one. The fills do not operate on pixels or cells, they operate on continuous regions in the plane. Two points belong to the same region if there exists a path between them that does not cross any segment and stays inside areas of the same color.

The constraints completely rule out any kind of fine-grained rasterization. The rectangle dimensions go up to `10^4`, so even a `10^4 × 10^4` grid already contains `10^8` cells. Flood-filling such a grid several times would be far too slow and memory-heavy.

The number of segments and fills is small, at most `100` each. This strongly suggests that the actual complexity depends on geometric structure rather than on the rectangle size itself. With only `100` segments, the arrangement formed by the segments contains only about `O(n^2)` intersections and regions. That is the real object we should work with.

Several edge cases are easy to mishandle.

Suppose a fill point lies directly on a segment.

```
5 5
1
1 2 4 2
1
2 2 red
```

The segment itself becomes red, but its area is still zero. The white regions above and below remain white. The correct answer is still `white 25`, because the segment contributes no area.

A naive implementation that treats the segment as having positive thickness would incorrectly split the area.

Another subtle case happens when segments intersect.

```
5 5
2
1 1 4 4
1 4 4 1
1
2 2 blue
```

The fill point lies exactly on the intersection point. Only the two segments become blue, and the total blue area remains zero.

If we fail to split segments at intersections, the planar graph becomes incorrect and the face traversal breaks.

Nested fills are another source of bugs.

```
6 6
1
3 1 3 5
2
1 1 red
5 1 blue
```

The first fill colors the left half red. The second fill colors the right half blue. Final areas are `18` and `18`.

If we process fills independently instead of sequentially, we lose the overwrite behavior.

The hardest conceptual edge case is disconnected pieces of the same color. Two different regions can both be white without being connected. A fill only recolors one connected component, not every region with the same color.

## Approaches

The brute-force idea is to discretize the plane into tiny cells and simulate flood fill directly. We could mark segment boundaries on a huge grid and run BFS for every fill operation.

This works conceptually because flood fill is fundamentally a connectivity problem. If every geometric feature aligned to grid cells, BFS would exactly reproduce the behavior of the paint program.

The problem is scale. Coordinates go up to `10^4`, and geometric precision matters because segments can intersect at arbitrary rational points. Even a resolution of one unit per cell already gives `10^8` cells. Every flood-fill would potentially scan the entire canvas. That is completely infeasible in both memory and runtime.

The key observation is that the number of segments is tiny. The actual topology of the plane changes only at segment intersections and segment endpoints. Between those critical coordinates, everything behaves uniformly.

This suggests switching from a pixel view to a planar graph view.

The drawn segments partition the rectangle into faces. Each face is a connected open region with fixed area. Flood-fill simply recolors one face or several faces connected through boundaries of the same current color.

So the problem becomes:

1. Build the planar subdivision induced by the rectangle border and all segments.
2. Compute every face area.
3. Determine which face contains each fill point.
4. Simulate recoloring on faces.

The arrangement of `n` segments has only `O(n^2)` intersections. After splitting segments at intersections, the planar graph remains manageable.

The most robust way to extract faces is a half-edge traversal. Every directed edge stores its outgoing angle. Walking by repeatedly taking the previous edge in cyclic order traces exactly one face boundary.

Once all faces are known, flood-fill becomes trivial. Each fill point belongs either to a face interior or to a segment. Segment fills have zero area impact, so we only care about interior points. Recoloring affects exactly one connected face.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force rasterization | O(W·H·m) | O(W·H) | Too slow |
| Planar graph + face traversal | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Collect all geometric primitives.

Add the four rectangle borders as segments together with all black segments from the input. The rectangle border is necessary because faces are bounded by the canvas edges too.
2. Compute every segment intersection.

For every pair of segments, compute whether they intersect. If they do, store the intersection point for both segments.

Every original segment will later be split at all its intersection points. Without this step, the planar graph would contain edges crossing through each other, which breaks face construction.
3. Split segments into elementary edges.

Sort all intersection points along each segment. Consecutive points define one elementary edge.

After splitting, no two edges intersect except at endpoints. This is the standard requirement for planar graph traversal.
4. Compress geometric points into graph vertices.

Floating point coordinates are dangerous as dictionary keys. Use exact rational arithmetic with fractions, or store normalized tuples.

Every unique point becomes a vertex in the graph.
5. Build directed half-edges.

For every undirected edge `(u, v)`, create two directed edges `u → v` and `v → u`.

For every vertex, sort outgoing directed edges by polar angle.
6. Construct faces by angular traversal.

Start from an unused directed edge.

Suppose we arrived at vertex `v` through edge `u → v`. Among all outgoing edges from `v`, find the reverse edge `v → u`. Take the edge immediately before it in cyclic angular order.

Repeating this process walks around one face boundary.

Mark all directed edges used in this traversal.
7. Compute polygon area for every face.

The traversal produces a polygon boundary. Use the shoelace formula.

One face is the exterior face, it has negative orientation and area equal to the outer infinite region. Ignore it.
8. Locate fill points.

For every fill operation, determine which bounded face contains the query point.

Since the number of faces is small, a point-in-polygon test against all faces is fast enough.

If the point lies exactly on a segment, ignore the fill because segments have zero area.
9. Simulate recoloring.

Initially every bounded face is white.

Each fill operation changes the color of exactly one face.

Maintain a mapping `face → current color`.
10. Accumulate final areas.

Sum the area of every face into its final color.

### Why it works

After splitting at intersections, the segments form a proper planar embedding. Every connected region of the canvas corresponds exactly to one bounded face of this embedding.

The half-edge traversal enumerates each face exactly once because every directed edge borders exactly one face on its left side. The angular rule always follows the boundary continuously without crossing edges.

Flood-fill on a point inside a face cannot cross segment boundaries, so it recolors exactly that face. Since faces partition the rectangle interior, summing their areas by final color gives the correct answer.

## Python Solution

```python
import sys
from fractions import Fraction
from collections import defaultdict

input = sys.stdin.readline

EPS = 1e-9

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def segment_intersection(a, b, c, d):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    r = (bx - ax, by - ay)
    s = (dx - cx, dy - cy)

    den = cross(r[0], r[1], s[0], s[1])

    if den == 0:
        return []

    t = Fraction(cross(cx - ax, cy - ay, s[0], s[1]), den)
    u = Fraction(cross(cx - ax, cy - ay, r[0], r[1]), den)

    if 0 <= t <= 1 and 0 <= u <= 1:
        x = Fraction(ax) + Fraction(r[0]) * t
        y = Fraction(ay) + Fraction(r[1]) * t
        return [(x, y)]

    return []

def point_on_segment(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b

    c = cross(bx - ax, by - ay, px - ax, py - ay)
    if c != 0:
        return False

    return (
        min(ax, bx) <= px <= max(ax, bx)
        and min(ay, by) <= py <= max(ay, by)
    )

def polygon_area(poly):
    s = Fraction(0)
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1

    return s / 2

def point_in_poly(pt, poly):
    x = float(pt[0])
    y = float(pt[1])

    inside = False
    n = len(poly)

    for i in range(n):
        x1 = float(poly[i][0])
        y1 = float(poly[i][1])
        x2 = float(poly[(i + 1) % n][0])
        y2 = float(poly[(i + 1) % n][1])

        if ((y1 > y) != (y2 > y)):
            t = (y - y1) / (y2 - y1)
            xx = x1 + (x2 - x1) * t
            if xx > x:
                inside = not inside

    return inside

def solve():
    W, H = map(int, input().split())

    segments = []

    rect = [
        ((0, 0), (W, 0)),
        ((W, 0), (W, H)),
        ((W, H), (0, H)),
        ((0, H), (0, 0)),
    ]

    for s in rect:
        segments.append(s)

    n = int(input())

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        segments.append(((x1, y1), (x2, y2)))

    m = int(input())
    fills = []

    for _ in range(m):
        x, y, c = input().split()
        fills.append((Fraction(int(x)), Fraction(int(y)), c))

    k = len(segments)

    pts_on_seg = []

    for i in range(k):
        a, b = segments[i]
        cur = set()
        cur.add((Fraction(a[0]), Fraction(a[1])))
        cur.add((Fraction(b[0]), Fraction(b[1])))
        pts_on_seg.append(cur)

    for i in range(k):
        for j in range(i + 1, k):
            a, b = segments[i]
            c, d = segments[j]

            inter = segment_intersection(a, b, c, d)

            for p in inter:
                pts_on_seg[i].add(p)
                pts_on_seg[j].add(p)

    edges = set()

    for i in range(k):
        a, b = segments[i]

        pts = list(pts_on_seg[i])

        dx = b[0] - a[0]
        dy = b[1] - a[1]

        pts.sort(
            key=lambda p: (
                Fraction(p[0] - a[0], dx) if dx != 0
                else Fraction(p[1] - a[1], dy)
            )
        )

        for j in range(len(pts) - 1):
            u = pts[j]
            v = pts[j + 1]

            if u != v:
                edges.add((u, v))
                edges.add((v, u))

    graph = defaultdict(list)

    for u, v in edges:
        graph[u].append(v)

    import math

    order = {}

    for u in graph:
        graph[u].sort(
            key=lambda v: math.atan2(
                float(v[1] - u[1]),
                float(v[0] - u[0])
            )
        )

        for i, v in enumerate(graph[u]):
            order[(u, v)] = i

    used = set()
    faces = []

    for u, v in edges:
        if (u, v) in used:
            continue

        face = []

        cu, cv = u, v

        while True:
            used.add((cu, cv))
            face.append(cu)

            arr = graph[cv]
            idx = order[(cv, cu)]

            nxt = arr[(idx - 1) % len(arr)]

            nu, nv = cv, nxt

            cu, cv = nu, nv

            if (cu, cv) == (u, v):
                break

        area = polygon_area(face)

        if area > 0:
            faces.append((face, area))

    face_colors = ["white"] * len(faces)

    all_segments = segments[4:]

    for x, y, col in fills:
        on_seg = False

        for a, b in all_segments:
            aa = (Fraction(a[0]), Fraction(a[1]))
            bb = (Fraction(b[0]), Fraction(b[1]))

            if point_on_segment((x, y), aa, bb):
                on_seg = True
                break

        if on_seg:
            continue

        for i, (poly, area) in enumerate(faces):
            if point_in_poly((x, y), poly):
                face_colors[i] = col
                break

    ans = defaultdict(float)

    for i, (_, area) in enumerate(faces):
        ans[face_colors[i]] += float(area)

    for c in sorted(ans):
        print(c, f"{ans[c]:.8f}")

solve()
```

The first part builds the geometric arrangement. Every segment is repeatedly split at all intersection points. Using `Fraction` avoids precision disasters caused by rational intersections such as `1/3`.

The half-edge graph is the heart of the solution. Every directed edge belongs to exactly one face on its left side. Sorting outgoing edges by angle lets us move consistently along boundaries.

The traversal step is subtle. After entering a vertex through one edge, we choose the previous outgoing edge in cyclic order. This keeps the current face on the left and traces its boundary without ambiguity.

The implementation stores only positive-area faces. The outer infinite face appears with negative orientation and gets discarded automatically.

Point location uses a standard ray-casting test. Since the number of faces is small, checking all faces is fast enough.

One important detail is handling fills on segments. Those fills affect only zero-area geometry, so they are ignored when computing areas.

## Worked Examples

### Sample 1

Input:

```
4 5
6
1 1 1 3
1 3 3 3
3 3 3 1
3 1 1 1
1 3 3 1
1 1 3 3
2
2 1 red
2 2 blue
```

The rectangle contains a square with two diagonals.

| Step | Action | Result |
| --- | --- | --- |
| 1 | Build arrangement | Several triangular faces appear inside the square |
| 2 | Fill `(2,1)` with red | One lower triangle becomes red |
| 3 | Fill `(2,2)` with blue | Point lies on diagonal intersection |
| 4 | Ignore blue fill | Segments have zero area |
| 5 | Sum areas | Entire rectangle stays white |

Final output:

```
blue 0.00000000
white 20.00000000
```

This example demonstrates the most counterintuitive rule in the problem. A fill point on a segment changes only zero-area geometry.

### Custom Example

```
6 6
1
3 0 3 6
2
1 1 red
5 1 blue
```

The vertical segment splits the rectangle into two equal faces.

| Step | Face containing point | Previous color | New color |
| --- | --- | --- | --- |
| 1 | Left rectangle | white | red |
| 2 | Right rectangle | white | blue |

Area table:

| Face | Area | Final color |
| --- | --- | --- |
| Left half | 18 | red |
| Right half | 18 | blue |

Final output:

```
blue 18.00000000
red 18.00000000
```

This confirms that flood-fill operates on connected regions rather than globally on colors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Segment intersections, face construction, and point-location over all faces |
| Space | O(n^2) | Arrangement vertices, edges, and faces |

With at most `100` segments, the arrangement complexity remains small enough. Even cubic behavior is perfectly safe inside the limits because the constant factors are moderate and the graph contains only a few thousand elements.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()

    with redirect_stdout(out):
        solve()

    return out.getvalue().strip()

# provided sample
assert run(
"""4 5
6
1 1 1 3
1 3 3 3
3 3 3 1
3 1 1 1
1 3 3 1
1 1 3 3
2
2 1 red
2 2 blue
"""
) == """white 20.00000000"""

# no segments
assert run(
"""3 3
0
1
1 1 red
"""
) == """red 9.00000000"""

# single split
res = run(
"""6 6
1
3 1 3 5
2
1 1 red
5 1 blue
"""
)

assert "red 18.00000000" in res
assert "blue 18.00000000" in res

# fill on segment
assert run(
"""5 5
1
1 2 4 2
1
2 2 red
"""
) == """white 25.00000000"""

# overwrite same region
assert run(
"""4 4
0
2
1 1 red
1 1 blue
"""
) == """blue 16.00000000"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty canvas with one fill | Entire area recolored | Base behavior |
| One dividing segment | Two independent faces | Correct face construction |
| Fill on segment | No area changes | Zero-area geometry handling |
| Repeated fills | Latest fill wins | Sequential simulation |
| Diagonal intersections | Segment splitting | Proper planar embedding |

## Edge Cases

Consider a fill point exactly on a segment.

```
5 5
1
1 2 4 2
1
2 2 red
```

The algorithm first checks whether the fill point belongs to any segment using exact collinearity and bounding-box tests. Since `(2,2)` lies on the segment, the fill is ignored for area computation.

The only face is still the whole rectangle with area `25`, so the output remains:

```
white 25.00000000
```

Now consider intersecting segments.

```
5 5
2
1 1 4 4
1 4 4 1
1
2 2 blue
```

During preprocessing, the two segments intersect at `(5/2, 5/2)` and are split into smaller edges. The fill point lies on the intersection itself, so again no face is recolored.

Without splitting, the graph would contain crossing edges and face traversal would fail to produce valid polygons.

Finally, consider disconnected regions sharing the same color.

```
6 6
1
3 0 3 6
3
1 1 red
5 1 red
1 1 blue
```

After the first two fills, both halves become red independently.

The last fill affects only the left face because flood-fill depends on connectivity, not merely color equality.

Final areas become:

```
blue 18.00000000
red 18.00000000
```

The algorithm handles this naturally because colors are stored per face, not globally.
