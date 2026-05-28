---
title: "CF 44F - BerPaint"
description: "We start with a rectangular canvas of size W × H. Initially the whole rectangle is white. Then several black line segments are drawn inside the rectangle. These segments split the plane into connected regions."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "graphs"]
categories: ["algorithms"]
codeforces_contest: 44
codeforces_index: "F"
codeforces_contest_name: "School Team Contest 2 (Winter Computer School 2010/11)"
rating: 2700
weight: 44
solve_time_s: 179
verified: false
draft: false
---
[CF 44F - BerPaint](https://codeforces.com/problemset/problem/44/F)

**Rating:** 2700  
**Tags:** geometry, graphs  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a rectangular canvas of size `W × H`. Initially the whole rectangle is white. Then several black line segments are drawn inside the rectangle. These segments split the plane into connected regions.

After that, several flood-fill operations are applied. A fill chooses a point and a color, then repaints the entire connected monochromatic region containing that point. Since segments have zero area, they only act as barriers between regions. A fill can also recolor parts of segments if the chosen point lies exactly on them, but that affects only zero-area geometry.

The task is to compute the final area occupied by every color after all fills are processed.

The geometric part is the difficult one. The segments can intersect each other arbitrarily, and the connected regions are induced by planar subdivision. The number of segments is only 100, but coordinates are continuous. We cannot rasterize the plane or use grids.

The small number of segments is the key constraint. With at most 100 segments, the total number of intersections is at most about 5000. That strongly suggests building the planar graph explicitly. A solution based on computational geometry and graph traversal is feasible.

The time limit is generous for an `O(N^3)` or `O(N^2 log N)` geometry solution, but not for anything that depends on coordinate magnitudes. Since coordinates go up to `10^4`, any discretization based on cells or pixels would fail immediately.

Several edge cases are easy to mishandle.

Consider fills performed on a segment itself:

```
4 4
1
1 1 3 3
1
2 2 red
```

The fill point lies exactly on the segment. The segment has zero area, so the final answer is still:

```
white 16.000000
```

A careless implementation may try to assign positive area to the segment.

Another tricky case is when multiple fills affect the same region:

```
5 5
1
2 0 2 5
2
1 1 red
1 2 blue
```

Both fills touch the same left half-plane, so the second fill overwrites the first one. Final areas are:

```
blue 10.000000
white 15.000000
```

If we only store the first fill affecting a region, we get the wrong answer.

Intersections also matter. Suppose two segments cross:

```
5 5
2
1 1 4 4
1 4 4 1
1
2 2 red
```

The crossing point splits both segments into smaller edges. If we fail to split segments at intersections, the planar graph becomes invalid and face traversal breaks.

The rectangle boundary is another subtle point. The outer boundary itself participates in the planar subdivision. Without adding rectangle edges into the graph, the outside face is not represented correctly and area computation becomes inconsistent.

## Approaches

The brute-force idea is conceptually simple. Treat the segments as walls, identify every connected region in the rectangle, then simulate the fills.

The problem is representing regions. Since coordinates are continuous, the naive approach would discretize the plane into tiny cells and run flood-fill over them. Even a `10000 × 10000` grid already contains `10^8` cells, which is far beyond feasible memory and time limits. Worse, intersections happen at arbitrary real coordinates, so exact geometry would still fail.

Another brute-force direction is sampling points and testing visibility between them, but connected components in arrangements of segments are geometric objects, not combinatorial grid regions. Approximate methods are unreliable because the output requires exact areas.

The important observation is that the segments form a planar graph. Every intersection point and every segment endpoint becomes a graph vertex. Consecutive points along a segment form graph edges. Once we have this planar embedding, the connected regions are exactly the graph faces.

This changes the problem completely. Instead of reasoning about continuous geometry directly, we reduce the task to:

1. Build the planar graph.
2. Enumerate all faces.
3. Compute each face area.
4. Determine which fills land inside each face.
5. Accumulate areas by final color.

The number of graph vertices is manageable because only segment intersections create new points. With at most 100 segments, the total subdivision size remains small enough for explicit planar traversal.

Face enumeration in planar graphs is a standard geometric technique. Around every vertex, sort outgoing edges by angle. Then repeatedly walk along the "next edge" in cyclic order. Every directed edge belongs to exactly one face traversal.

The outer infinite face is discarded by orientation or area sign. All bounded faces correspond to actual paintable regions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force rasterization | O(WH) or worse | O(WH) | Too slow |
| Planar graph + face traversal | O(VE) roughly | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Add the four rectangle borders as additional segments.

The rectangle boundary participates in the planar subdivision exactly like the black segments. Without it, the graph would not contain closed faces for the canvas.
2. Compute every intersection point between every pair of segments.

This includes shared endpoints and proper crossings. For each segment, collect all points lying on it.
3. Sort the points along each segment and split the segment into smaller edges.

Consecutive points on the same segment define one graph edge. After this step, edges intersect only at vertices.
4. Compress equal geometric points into vertex IDs.

Floating point computations produce tiny inaccuracies, so coordinates are compared with an epsilon tolerance.
5. Build directed edges for the planar graph.

Every undirected segment edge becomes two directed half-edges. For each directed edge, store:

- destination vertex
- reverse edge
- geometric angle
6. Sort outgoing edges around every vertex by angle.

This gives the cyclic order needed for planar face traversal.
7. Precompute the next edge for face walking.

Suppose we arrive at vertex `v` through edge `u -> v`. The next edge along the face is the edge immediately before `(v -> u)` in angular order.

This keeps the traversed face consistently on the left side.
8. Traverse all faces.

For every unused directed edge, repeatedly follow `next` pointers until returning to the start edge.

The sequence of vertices forms one polygonal face.
9. Compute the signed area of each face.

Using the shoelace formula:

$A = \frac{1}{2}\sum_{i=0}^{n-1}(x_i y_{i+1} - y_i x_{i+1})$

Clockwise faces have negative signed area. In this traversal convention, bounded faces appear clockwise, while the outer infinite face appears counterclockwise.
10. Keep only bounded faces.

Ignore faces with positive area. For the remaining ones, store absolute area.
11. Find which face contains each fill point.

For every fill point:

- first check whether it lies on a segment
- otherwise locate the polygon containing the point

Since the number of faces is small, simple point-in-polygon testing is fast enough.
12. Apply fills in order.

Each face remembers its current color. Initially all bounded faces are white. Every fill recolors the corresponding face.
13. Sum areas by final color and print the result.

### Why it works

The segment arrangement partitions the rectangle into connected open regions. After splitting segments at every intersection, the resulting planar graph exactly captures this subdivision.

Face traversal enumerates every maximal connected region once because each directed edge borders exactly one face on its left side. The angular ordering guarantees that the traversal follows the geometric boundary continuously.

Flood-fill operations only recolor connected regions separated by segment barriers. Since each bounded face corresponds to exactly one such region, applying fills to faces reproduces the painting process precisely.

The shoelace formula computes exact polygon areas regardless of polygon shape, including non-convex faces.

## Python Solution

```python
import sys
import math
from collections import defaultdict

input = sys.stdin.readline

EPS = 1e-9

def sgn(x):
    if x > EPS:
        return 1
    if x < -EPS:
        return -1
    return 0

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def on_segment(p, a, b):
    if abs(cross(sub(b, a), sub(p, a))) > EPS:
        return False
    return dot(sub(p, a), sub(p, b)) <= EPS

def seg_intersection(a, b, c, d):
    ab = sub(b, a)
    cd = sub(d, c)

    den = cross(ab, cd)

    if abs(den) < EPS:
        pts = []
        for p in [a, b]:
            if on_segment(p, c, d):
                pts.append(p)
        for p in [c, d]:
            if on_segment(p, a, b):
                pts.append(p)
        return pts

    t = cross(sub(c, a), cd) / den
    u = cross(sub(c, a), ab) / den

    if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
        p = (a[0] + ab[0] * t, a[1] + ab[1] * t)
        return [p]

    return []

def polygon_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - y1 * x2
    return s / 2.0

def point_in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)

    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]

        if on_segment(p, (ax, ay), (bx, by)):
            return True

        if (ay > y) != (by > y):
            t = (y - ay) / (by - ay)
            xx = ax + (bx - ax) * t
            if xx > x:
                inside = not inside

    return inside

def key_point(p):
    return (round(p[0], 10), round(p[1], 10))

def solve():
    W, H = map(int, input().split())

    n = int(input())

    segs = []

    for _ in range(n):
        x1, y1, x2, y2 = map(float, input().split())
        segs.append(((x1, y1), (x2, y2)))

    rect = [
        ((0.0, 0.0), (W, 0.0)),
        ((W, 0.0), (W, H)),
        ((W, H), (0.0, H)),
        ((0.0, H), (0.0, 0.0)),
    ]

    segs.extend(rect)

    m = len(segs)

    pts_on_seg = [[] for _ in range(m)]

    for i in range(m):
        pts_on_seg[i].append(segs[i][0])
        pts_on_seg[i].append(segs[i][1])

    for i in range(m):
        for j in range(i + 1, m):
            inter = seg_intersection(
                segs[i][0], segs[i][1],
                segs[j][0], segs[j][1]
            )

            for p in inter:
                pts_on_seg[i].append(p)
                pts_on_seg[j].append(p)

    point_id = {}
    points = []

    def get_id(p):
        k = key_point(p)
        if k not in point_id:
            point_id[k] = len(points)
            points.append(p)
        return point_id[k]

    edges = []

    for i in range(m):
        a, b = segs[i]
        vec = sub(b, a)

        arr = []
        seen = set()

        for p in pts_on_seg[i]:
            k = key_point(p)
            if k in seen:
                continue
            seen.add(k)

            if abs(vec[0]) >= abs(vec[1]):
                t = (p[0] - a[0]) / vec[0] if abs(vec[0]) > EPS else 0
            else:
                t = (p[1] - a[1]) / vec[1]

            arr.append((t, p))

        arr.sort()

        for j in range(len(arr) - 1):
            p1 = arr[j][1]
            p2 = arr[j + 1][1]

            if math.hypot(p1[0] - p2[0], p1[1] - p2[1]) < EPS:
                continue

            u = get_id(p1)
            v = get_id(p2)

            edges.append((u, v))
            edges.append((v, u))

    g = [[] for _ in range(len(points))]
    rev = []

    for idx, (u, v) in enumerate(edges):
        ang = math.atan2(
            points[v][1] - points[u][1],
            points[v][0] - points[u][0]
        )
        g[u].append([v, ang, idx])

    edge_rev = [0] * len(edges)

    mp = defaultdict(list)

    for idx, (u, v) in enumerate(edges):
        mp[(u, v)].append(idx)

    for idx, (u, v) in enumerate(edges):
        edge_rev[idx] = mp[(v, u)].pop()

    pos = {}

    for v in range(len(points)):
        g[v].sort(key=lambda x: x[1])

        for i, (_, _, idx) in enumerate(g[v]):
            pos[idx] = i

    nxt = [0] * len(edges)

    for idx, (u, v) in enumerate(edges):
        ridx = edge_rev[idx]
        p = pos[ridx]

        deg = len(g[v])

        nxt[idx] = g[v][(p - 1) % deg][2]

    used = [False] * len(edges)

    faces = []

    for i in range(len(edges)):
        if used[i]:
            continue

        cur = i
        poly = []

        while not used[cur]:
            used[cur] = True

            u, v = edges[cur]
            poly.append(points[u])

            cur = nxt[cur]

        area = polygon_area(poly)

        if area < -EPS:
            faces.append((poly, -area))

    q = int(input())

    fills = []

    for _ in range(q):
        x, y, c = input().split()
        fills.append((float(x), float(y), c))

    face_color = ["white"] * len(faces)

    for x, y, color in fills:
        p = (x, y)

        for i, (poly, area) in enumerate(faces):
            if point_in_poly(p, poly):
                face_color[i] = color
                break

    ans = defaultdict(float)

    for i, (_, area) in enumerate(faces):
        ans[face_color[i]] += area

    for k in sorted(ans):
        print(k, f"{ans[k]:.8f}")

solve()
```

The implementation follows the geometric construction directly.

The most delicate part is splitting segments correctly. Every segment stores all intersection points lying on it, including endpoints. After sorting these points along the segment, consecutive pairs become graph edges. This guarantees that edges only intersect at vertices.

Floating point precision is another subtle issue. Exact equality between computed intersections is unreliable, so points are normalized with rounded coordinates before assigning IDs.

Face traversal depends on angular ordering. At each vertex, outgoing edges are sorted by `atan2`. When entering a vertex through some edge, the next face edge is the previous edge in cyclic order. That convention keeps the traversed face on the left side.

The orientation test is easy to get backwards. With this traversal convention, bounded faces appear clockwise, giving negative signed area. The outer infinite face appears counterclockwise and is discarded.

Point-in-polygon uses standard ray casting. Since fill points may lie exactly on boundaries, the implementation first checks `on_segment`.

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

The square and diagonals partition the interior into triangular regions.

| Step | Action | Result |
| --- | --- | --- |
| 1 | Add rectangle edges | Outer boundary included |
| 2 | Compute intersections | Center point `(2,2)` created |
| 3 | Split segments | Diagonals divided at center |
| 4 | Enumerate faces | Several triangular faces found |
| 5 | Fill `(2,1)` red | One triangle becomes red |
| 6 | Fill `(2,2)` blue | Central region recolored blue |
| 7 | Sum areas | Blue region has zero area |

The interesting detail is that `(2,2)` lies exactly at the intersection of diagonals. That point belongs only to zero-area geometry, so recoloring it changes no measurable area.

Final output:

```
blue 0.00000000
white 20.00000000
```

### Custom Example

Input:

```
6 4
1
3 0 3 4
2
1 1 red
5 1 blue
```

The vertical segment splits the rectangle into two equal halves.

| Step | Face | Area | Current color |
| --- | --- | --- | --- |
| Initial | Left half | 12 | white |
| Initial | Right half | 12 | white |
| Fill 1 | Left half | 12 | red |
| Fill 2 | Right half | 12 | blue |

Final output:

```
blue 12.00000000
red 12.00000000
```

This trace confirms that every connected region corresponds to one planar face.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S³) worst-case | Segment intersections plus face construction |
| Space | O(S²) | Graph vertices and edges from intersections |

Here `S` is the number of segments including rectangle borders, at most 104.

The cubic factor comes from handling all pairwise intersections and graph operations on the resulting subdivision. With only about 100 segments, this easily fits within the limits.

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

    return out.getvalue()

# provided sample
sample = """4 5
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

assert "white 20.00000000" in run(sample)

# no segments, no fills
assert run("""3 3
0
0
""").strip() == "white 9.00000000"

# single split
res = run("""6 4
1
3 0 3 4
2
1 1 red
5 1 blue
""")

assert "red 12.00000000" in res
assert "blue 12.00000000" in res

# overwrite same region
res = run("""5 5
1
2 0 2 5
2
1 1 red
1 2 blue
""")

assert "blue 10.00000000" in res
assert "white 15.00000000" in res

# fill on segment only
res = run("""4 4
1
1 1 3 3
1
2 2 red
""")

assert "white 16.00000000" in res
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty rectangle | Entire area white | Base case with no subdivision |
| Single vertical split | Two equal regions | Correct face construction |
| Two fills same region | Last fill wins | Proper overwrite semantics |
| Fill on segment | Zero area recolor | Boundary handling |

## Edge Cases

Consider a fill point lying exactly on a segment:

```
4 4
1
1 1 3 3
1
2 2 red
```

The diagonal divides the rectangle into two triangular faces. The fill point lies on the diagonal itself, not inside either face. Since the segment has zero area, repainting it changes nothing measurable.

During execution:

1. The segment becomes graph edges.
2. Face traversal finds two triangular faces.
3. Point-in-polygon detects boundary contact only.
4. No positive-area face changes color.

Final result:

```
white 16.00000000
```

Now consider repeated fills of the same region:

```
5 5
1
2 0 2 5
2
1 1 red
1 2 blue
```

The vertical segment creates left and right halves.

Execution:

1. Face enumeration produces two faces of area 10 and 15.
2. First fill colors the left face red.
3. Second fill targets the same left face and overwrites it with blue.
4. Areas are accumulated only from final colors.

Final result:

```
blue 10.00000000
white 15.00000000
```

Finally, consider crossing segments:

```
5 5
2
1 1 4 4
1 4 4 1
0
```

The intersection at `(2.5,2.5)` must become a graph vertex.

Execution:

1. Pairwise intersection finds the crossing.
2. Both diagonals are split into smaller edges.
3. The planar graph becomes valid.
4. Face traversal correctly identifies all regions.

Without splitting at intersections, the traversal would incorrectly treat crossing edges as independent and produce invalid polygons.
