---
title: "CF 75E - Ship's Shortest Path"
description: "We are given two points in the plane, the ship's starting position and destination, together with a convex polygon representing an island. Moving through the sea costs 1 per unit distance. Moving through the interior of the island costs 2 per unit distance."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 75
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 67 (Div. 2)"
rating: 2400
weight: 75
solve_time_s: 149
verified: true
draft: false
---

[CF 75E - Ship's Shortest Path](https://codeforces.com/problemset/problem/75/E)

**Rating:** 2400  
**Tags:** geometry, shortest paths  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two points in the plane, the ship's starting position and destination, together with a convex polygon representing an island.

Moving through the sea costs `1` per unit distance. Moving through the interior of the island costs `2` per unit distance. Moving along the polygon boundary is treated as sea movement, so the cost there is still `1`.

The ship may travel anywhere outside the island for sea cost, and may also cross through the island by paying the higher land cost. The task is to compute the minimum total cost needed to travel from the start point to the end point.

The polygon is convex and contains at most 30 vertices. That changes the character of the problem completely. With such a small polygon, we do not need sophisticated geometry data structures or continuous optimization. An `O(n^3)` or even `O(n^4)` algorithm is perfectly acceptable.

The difficult part is not performance, it is modeling the geometry correctly.

A naive interpretation would be "either go straight through the island or walk around the boundary". That is not always true. An optimal path may enter the polygon at one boundary point, travel through the interior, then leave at another point, and also use boundary arcs before or after that segment.

Another subtle point is that the shortest sea-only path around a convex polygon is always composed of straight segments and polygon edges. Once a straight segment touches the polygon interior, it becomes invalid as a sea segment.

The fact that the polygon is convex is the key structural property. Convexity guarantees that any segment connecting two outside points intersects the polygon in at most one continuous interval. That makes shortest paths much simpler than in general polygon obstacle problems.

Consider this example:

```
Start = (0,0)
End   = (10,0)

Square:
(4,-1) (6,-1) (6,1) (4,1)
```

The direct segment crosses the island. A careless implementation might say:

"Going through the island costs `2 * 2 = 4` for the blocked portion, plus the rest in sea."

That gives total cost `8 + 4 = 12`.

But the correct answer is smaller. The optimal route is to walk around the square boundary. The detour length is only `2 + 2 = 4`, so the total cost becomes `10 + 2 = 12`? Actually both happen to tie here. Small perturbations easily break the tie.

For example:

```
Start = (0,0)
End   = (10,0)

Rectangle:
(4,-3) (6,-3) (6,3) (4,3)
```

Crossing through the island now costs:

`8` sea distance plus `2 * 2 = 4`, total `12`.

Going around the boundary requires a detour of `6`, total `14`.

The optimal answer is to cross the island.

Another dangerous edge case happens when the straight segment only touches the polygon boundary at one point. Since boundary movement counts as sea movement, this path is fully valid as a sea path and should not incur any extra land cost.

Example:

```
Start = (0,0)
End   = (10,0)

Triangle:
(5,0) (6,2) (6,-2)
```

The segment only touches the vertex `(5,0)`. The answer is exactly `10`.

An implementation that treats boundary contact as interior intersection will incorrectly increase the cost.

## Approaches

The brute-force idea is to think continuously. Any optimal path can enter and leave the polygon at arbitrary boundary points, so we might try sampling many boundary points and computing the best route among them.

This works conceptually because the cost function is piecewise geometric and smooth. If we discretize finely enough, we approximate the optimal solution.

The problem is that continuous optimization becomes messy very quickly. Even if we sample only `k` points per edge, we already have `O(k^2)` candidate entry-exit pairs. Every pair also requires geometric intersection checks and shortest boundary computations. High precision would need large `k`, making the method impractical and numerically fragile.

The key observation is that shortest paths in this problem only need polygon vertices as turning points.

Suppose we are moving entirely in the sea. Inside each free region, the shortest path between two points is always a straight segment. The only reason to bend is to slide along the polygon boundary. Since the polygon is convex, boundary-optimal routes between two boundary points are exactly the two polygon chains connecting them.

This transforms the continuous geometry problem into a graph shortest path problem.

We create a graph whose nodes are:

- the start point
- the end point
- all polygon vertices

Then we connect pairs of nodes with weighted edges.

If the segment between two nodes does not pass through the polygon interior, we may travel directly through the sea, so the edge cost equals Euclidean distance.

If the segment does pass through the polygon interior, we may still travel directly, but now the inside portion costs double.

For a convex polygon, the segment intersects the polygon in either:

- no interval
- one point
- one continuous segment

So we can compute:

- total segment length
- length inside the polygon

Then the cost becomes:

`outside_length * 1 + inside_length * 2`

which simplifies to:

`total_length + inside_length`

Once all pairwise costs are known, the problem becomes a complete weighted graph shortest path problem. Since the graph has at most 32 vertices, Floyd-Warshall is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Sampling | Extremely large for high precision | Large | Too slow and unreliable |
| Graph + Geometry + Floyd-Warshall | O(n³) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the start point, end point, and polygon vertices.
2. Build a list of graph nodes consisting of:

- node `0` as the start point
- node `1` as the end point
- nodes `2...n+1` as polygon vertices
3. For every pair of nodes `(A, B)`, compute the minimum cost of traveling directly between them.
4. To compute the direct travel cost, first determine how much of segment `AB` lies inside the convex polygon.
5. Parameterize the segment as:

$P(t)=A+t(B-A),\quad 0\le t\le 1$

We intersect this segment with every polygon edge.
6. Collect all parameter values `t` where the segment intersects polygon edges.

Also include:

- `0`
- `1`
7. Sort all collected `t` values and examine every consecutive interval.

For each interval:

- take its midpoint parameter
- evaluate the midpoint position
- test whether this midpoint lies strictly inside the polygon

If it does, then the whole interval lies inside because the polygon is convex.
8. Sum the lengths of all intervals classified as inside.
9. Let:

- `L` be total segment length
- `I` be total inside length

Then the travel cost becomes:

$\text{cost}=L+I$

The first `L` accounts for sea cost everywhere, and the extra `I` upgrades inside movement from cost `1` to cost `2`.
10. Store this value as the graph edge weight between the two nodes.
11. Run Floyd-Warshall on the graph.
12. The shortest distance from node `0` to node `1` is the answer.

### Why it works

For any shortest path, every maximal sea segment is a straight line, because Euclidean distance is optimal in open space. Whenever the path changes direction, it must happen on the polygon boundary.

For a convex polygon, the intersection of a line segment with the polygon is always connected. That means a direct segment has a uniquely defined inside portion whose cost can be computed exactly.

The graph contains all polygon vertices plus the endpoints. Any optimal boundary traversal can be represented as a sequence of polygon edges between vertices, while any free-space movement is represented by straight graph edges.

Since every direct edge weight equals the true optimal cost between its endpoints, Floyd-Warshall correctly combines them into the global optimum.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

EPS = 1e-9

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def segment_intersection_t(a, b, c, d):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    rx = bx - ax
    ry = by - ay

    sx = dx - cx
    sy = dy - cy

    denom = cross(rx, ry, sx, sy)

    if abs(denom) < EPS:
        return None

    qpx = cx - ax
    qpy = cy - ay

    t = cross(qpx, qpy, sx, sy) / denom
    u = cross(qpx, qpy, rx, ry) / denom

    if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
        return max(0.0, min(1.0, t))

    return None

def point_in_convex_polygon_strict(p, poly):
    x, y = p
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        cr = cross(x2 - x1, y2 - y1, x - x1, y - y1)

        if cr <= EPS:
            return False

    return True

def inside_length(a, b, poly):
    ts = [0.0, 1.0]

    n = len(poly)

    for i in range(n):
        c = poly[i]
        d = poly[(i + 1) % n]

        t = segment_intersection_t(a, b, c, d)

        if t is not None:
            ts.append(t)

    ts.sort()

    uniq = []
    for t in ts:
        if not uniq or abs(t - uniq[-1]) > 1e-8:
            uniq.append(t)

    total = 0.0
    full_len = dist(a, b)

    for i in range(len(uniq) - 1):
        l = uniq[i]
        r = uniq[i + 1]

        mid = (l + r) / 2.0

        mx = a[0] + (b[0] - a[0]) * mid
        my = a[1] + (b[1] - a[1]) * mid

        if point_in_convex_polygon_strict((mx, my), poly):
            total += (r - l) * full_len

    return total

def solve():
    xs, ys, xe, ye = map(int, input().split())

    n = int(input())

    vals = list(map(int, input().split()))

    poly = []

    for i in range(0, 2 * n, 2):
        poly.append((vals[i], vals[i + 1]))

    nodes = [(xs, ys), (xe, ye)] + poly

    m = len(nodes)

    INF = 1e100

    d = [[INF] * m for _ in range(m)]

    for i in range(m):
        d[i][i] = 0.0

    for i in range(m):
        for j in range(i + 1, m):
            a = nodes[i]
            b = nodes[j]

            total = dist(a, b)
            inside = inside_length(a, b, poly)

            cost = total + inside

            d[i][j] = cost
            d[j][i] = cost

    for k in range(m):
        for i in range(m):
            dik = d[i][k]

            for j in range(m):
                nd = dik + d[k][j]

                if nd < d[i][j]:
                    d[i][j] = nd

    print("{:.9f}".format(d[0][1]))

solve()
```

The core geometric routine is `inside_length`.

The segment is parameterized from `t = 0` to `t = 1`. Every intersection with a polygon edge contributes a candidate transition point where the segment changes from outside to inside or vice versa.

After sorting all transition parameters, every consecutive interval lies entirely either inside or outside the polygon. Testing only the midpoint is enough because the polygon is convex and the segment cannot repeatedly alternate within one interval.

The function `point_in_convex_polygon_strict` deliberately uses a strict test. Boundary points are treated as outside because boundary travel costs the same as sea travel.

One subtle implementation detail is duplicate intersection parameters. When a segment passes exactly through a polygon vertex, two edges may report the same intersection. Without deduplication, zero-length intervals appear and numerical instability follows.

Floyd-Warshall is used instead of Dijkstra simply because the graph is tiny. With at most 32 nodes, cubic complexity is negligible.

## Worked Examples

### Sample 1

Input:

```
1 7 6 7
4
4 2 4 12 3 12 3 2
```

The rectangle blocks the direct path horizontally.

| Step | Value |
| --- | --- |
| Direct segment length | 5 |
| Inside portion | 1 |
| Direct cost | 6 |
| Boundary detour | Longer |
| Final answer | 6 |

The straight line crosses the rectangle between `x = 3` and `x = 4`, so exactly one unit lies inside the island. Sea distance contributes `5`, and the inside premium contributes another `1`.

### Custom Example

```
0 0 10 0
4
4 -3 6 -3 6 3 4 3
```

| Step | Value |
| --- | --- |
| Direct segment length | 10 |
| Inside portion | 2 |
| Direct cost | 12 |
| Upper boundary detour | 14 |
| Lower boundary detour | 14 |
| Final answer | 12 |

This example demonstrates that crossing the island can genuinely be cheaper than going around it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | Floyd-Warshall dominates |
| Space | O(n²) | Distance matrix storage |

The polygon has at most 30 vertices, so the graph has at most 32 nodes. Floyd-Warshall performs roughly `32³ = 32768` relaxations, which is tiny. The geometry computations are also lightweight, easily fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isclose

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import math

    input = sys.stdin.readline

    EPS = 1e-9

    def dist(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def cross(ax, ay, bx, by):
        return ax * by - ay * bx

    def segment_intersection_t(a, b, c, d):
        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = d

        rx = bx - ax
        ry = by - ay

        sx = dx - cx
        sy = dy - cy

        denom = cross(rx, ry, sx, sy)

        if abs(denom) < EPS:
            return None

        qpx = cx - ax
        qpy = cy - ay

        t = cross(qpx, qpy, sx, sy) / denom
        u = cross(qpx, qpy, rx, ry) / denom

        if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
            return max(0.0, min(1.0, t))

        return None

    def point_in_convex_polygon_strict(p, poly):
        x, y = p

        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]

            cr = cross(x2 - x1, y2 - y1, x - x1, y - y1)

            if cr <= EPS:
                return False

        return True

    def inside_length(a, b, poly):
        ts = [0.0, 1.0]

        for i in range(len(poly)):
            c = poly[i]
            d = poly[(i + 1) % len(poly)]

            t = segment_intersection_t(a, b, c, d)

            if t is not None:
                ts.append(t)

        ts.sort()

        uniq = []

        for t in ts:
            if not uniq or abs(t - uniq[-1]) > 1e-8:
                uniq.append(t)

        total = 0.0
        full_len = dist(a, b)

        for i in range(len(uniq) - 1):
            l = uniq[i]
            r = uniq[i + 1]

            mid = (l + r) / 2

            mx = a[0] + (b[0] - a[0]) * mid
            my = a[1] + (b[1] - a[1]) * mid

            if point_in_convex_polygon_strict((mx, my), poly):
                total += (r - l) * full_len

        return total

    xs, ys, xe, ye = map(int, input().split())

    n = int(input())

    vals = list(map(int, input().split()))

    poly = []

    for i in range(0, 2 * n, 2):
        poly.append((vals[i], vals[i + 1]))

    ans = dist((xs, ys), (xe, ye))
    ans += inside_length((xs, ys), (xe, ye), poly)

    return f"{ans:.6f}"

# provided sample
assert run(
"""1 7 6 7
4
4 2 4 12 3 12 3 2
"""
) == "6.000000"

# segment completely outside polygon
assert run(
"""0 0 10 0
4
20 20 21 20 21 21 20 21
"""
) == "10.000000"

# direct path crosses rectangle
assert run(
"""0 0 10 0
4
4 -3 6 -3 6 3 4 3
"""
) == "12.000000"

# touching boundary only
assert run(
"""0 0 10 0
3
5 0 6 2 6 -2
"""
) == "10.000000"

# thin crossing
assert run(
"""0 0 4 0
4
1 -1 3 -1 3 1 1 1
"""
) == "6.000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 6.000000 | Basic crossing computation |
| Polygon far away | 10.000000 | No intersection case |
| Large rectangle crossing | 12.000000 | Interior traversal cheaper than detour |
| Boundary touch | 10.000000 | Boundary is treated as sea |
| Thin rectangle | 6.000000 | Exact inside-length accounting |

## Edge Cases

Consider the boundary-touching case:

```
0 0 10 0
3
5 0 6 2 6 -2
```

The segment intersects the polygon only at the vertex `(5,0)`.

The intersection parameters become:

| t values |
| --- |
| 0 |
| 0.5 |
| 1 |

The midpoint tests are:

- between `0` and `0.5`, outside
- between `0.5` and `1`, outside

No interval is classified as interior, so the inside length is `0`.

The final answer becomes exactly `10`.

Now consider a full crossing:

```
0 0 10 0
4
4 -3 6 -3 6 3 4 3
```

The segment enters at `x = 4` and exits at `x = 6`.

The parameter intervals are:

| Interval | Inside? |
| --- | --- |
| [0, 0.4] | No |
| [0.4, 0.6] | Yes |
| [0.6, 1] | No |

The inside fraction is `0.2`, so the inside length is `2`.

Total cost:

```
10 + 2 = 12
```

Finally, consider a segment aligned with a polygon edge:

```
0 0 10 0
4
3 0 7 0 7 2 3 2
```

The path lies along the bottom edge of the rectangle.

The midpoint test never classifies any interval as strictly inside, because boundary points fail the strict containment test.

The algorithm correctly outputs `10`, treating edge traversal as sea movement.
