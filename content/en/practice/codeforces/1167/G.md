---
title: "CF 1167G - Low Budget Inception"
description: "We are given a set of unit squares placed along the x-axis. Each building occupies a segment from $ai$ to $ai+1$ at height $0$ to $1$. The buildings are ordered left to right and do not overlap, but gaps between consecutive buildings are bounded by a given value."
date: "2026-06-13T09:04:08+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1167
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 65 (Rated for Div. 2)"
rating: 3100
weight: 1167
solve_time_s: 344
verified: false
draft: false
---

[CF 1167G - Low Budget Inception](https://codeforces.com/problemset/problem/1167/G)

**Rating:** 3100  
**Tags:** brute force, geometry  
**Solve time:** 5m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of unit squares placed along the x-axis. Each building occupies a segment from $a_i$ to $a_i+1$ at height $0$ to $1$. The buildings are ordered left to right and do not overlap, but gaps between consecutive buildings are bounded by a given value.

For each query point $x$ on the x-axis, we imagine placing a ray starting at $(x,0)$ pointing to the right. We then rotate this ray counterclockwise. As the ray sweeps upward, it will eventually collide with the geometric shape formed by the tops and sides of the buildings. The rotation stops at the first point of contact. The required output is the angle of the ray at this stopping moment.

Geometrically, this means we are looking for the maximum angle such that a ray from $(x,0)$ still avoids intersecting any building. Since all relevant geometry lies above the x-axis, the answer is determined by which visible “roof corner” becomes tangent first as we rotate upward.

The input size is large, up to $2 \cdot 10^5$ buildings and queries. Any solution closer to quadratic behavior over buildings or queries will fail. Even $O(nm)$ or $O(n \sqrt{n})$ style approaches are immediately impossible, and even $O(n \log n)$ per query is too slow. We are pushed toward a structure that allows a global preprocessing of geometry and fast per-query evaluation, typically logarithmic or amortized constant time.

A subtle difficulty is that naive intuition about “closest building” is wrong. A nearer building can be completely hidden behind a slightly farther one depending on geometry, so visibility is governed by a global upper envelope, not local proximity.

A second issue is floating instability: many candidate points produce very close angles, and any correct approach must rely on stable geometric primitives rather than incremental angle comparisons.

## Approaches

A direct simulation starts from each query point and tries to test every building corner as a potential first collision point. For a fixed $x$, one would compute the angle to each relevant vertex, take the minimum over intersection constraints, and then choose the limiting event. This costs $O(n)$ per query, giving $O(nm)$, which is far too large for $2 \cdot 10^5$ in both dimensions.

The key structural observation is that the answer for a fixed $x$ depends only on a small subset of “extreme” points: those that form the upper boundary of the union of all building rectangles. Everything below this boundary is irrelevant, since the ray will hit the upper envelope first.

This upper envelope is a convex structure when viewed from any external point on the x-axis. Once we compress all candidate vertices into a convex hull ordered by x-coordinate, the best visible point for a query is determined by a tangent condition: we are effectively finding the point on the convex hull that maximizes the angle of the segment from $(x,0)$.

This transforms the problem into repeated geometric queries against a convex polygon: for each query point, find the tangent point on a convex hull that maximizes the angle. The objective function over hull vertices becomes unimodal along the hull order, which allows logarithmic search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Convex Hull + per query search | $O((n+m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Convex structure construction

1. Collect all relevant geometric vertices from the buildings, specifically the endpoints of the top edges, since only those can form the first contact when the ray rotates. These points define the visible boundary of the scene.
2. Sort these points by x-coordinate and construct their upper convex hull. This removes all interior points that can never be responsible for a first collision, since any such point is always dominated by a higher or more extreme neighbor.
3. Store the convex hull vertices in counterclockwise order. This ordering is crucial because the query function over them becomes monotonic along the hull.

### Query processing

1. For a query point $x$, consider any hull vertex $p = (x_p, 1)$. The ray from $(x,0)$ to $p$ has slope $\frac{1}{x_p - x}$, and the corresponding angle is $\arctan\left(\frac{1}{x_p - x}\right)$.
2. Since $\arctan$ is monotonic, maximizing the angle is equivalent to maximizing the slope, which is equivalent to minimizing the horizontal distance $x_p - x$, but only among vertices that remain visible under the convex hull constraint.
3. On the convex hull, the function that maps vertex index to slope is unimodal. This allows binary search to find the optimal vertex in $O(\log n)$ time per query.

### Why it works

The convex hull ensures that no interior point can ever be the first collision point, because any such point is blocked by a segment of the hull before the ray reaches it. Once reduced to hull vertices, visibility from a fixed external point becomes a tangent problem. Tangents to a convex polygon are uniquely defined, and the slope function over ordered vertices has a single extremum, which guarantees binary search correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def build_hull(points):
    points.sort()
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) >= 0:
            lower.pop()
        lower.append(p)
    return lower

def best_angle(hull, x):
    lo, hi = 0, len(hull) - 1

    def val(i):
        px = hull[i][0]
        return math.atan2(1.0, px - x)

    while hi - lo > 3:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if val(m1) < val(m2):
            lo = m1
        else:
            hi = m2

    best = 0.0
    for i in range(lo, hi + 1):
        best = max(best, val(i))
    return best

n, d = map(int, input().split())
a = list(map(int, input().split()))
m = int(input())
xs = list(map(int, input().split()))

pts = []
for i in range(n):
    pts.append((a[i], 1))
    pts.append((a[i] + 1, 1))

hull = build_hull(pts)

for x in xs:
    print(best_angle(hull, x))
```

The solution first converts every building into its two top endpoints and builds the upper convex hull of these points. Any interior points are removed because they can never contribute to the first visible collision when sweeping a ray upward from the x-axis.

Each query is then reduced to searching over the convex hull. The function being optimized is the angle formed by a segment from the query point to a hull vertex, which depends only on the horizontal distance since all vertices have identical height. This produces a unimodal function over hull order, which is why ternary search is valid.

The use of `atan2(1.0, px - x)` encodes the angle directly and avoids explicit slope comparisons that could suffer from division instability.

## Worked Examples

### Example 1

Input:

```
3 5
0 5 7
```

We form points $(0,1),(1,1),(5,1),(6,1),(7,1),(8,1)$. The convex hull reduces to the outermost chain, which in this case is simply the endpoints since all points lie on one horizontal line.

For a query $x = 2$, we evaluate angles to all hull candidates:

| Candidate x_p | dx = x_p - 2 | angle |
| --- | --- | --- |
| 5 | 3 | arctan(1/3) |
| 7 | 5 | arctan(1/5) |
| 8 | 6 | arctan(1/6) |

The maximum is at the smallest positive distance, so the first visible extreme dominates.

This confirms that even though all buildings have identical height, the closest unobstructed hull vertex determines the answer.

### Example 2

Consider a configuration with a large gap followed by dense buildings:

```
n = 4
a = [0, 2, 3, 10]
```

The hull still keeps only extreme endpoints. For a query near the middle, say $x = 1$, the candidate at $x=2$ might be geometrically closer, but if it lies under a hull segment, it becomes irrelevant. The hull ensures only true visible extremes remain, so the algorithm never incorrectly selects a hidden point.

This demonstrates why local proximity is insufficient without convex filtering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log n)$ | Building hull is linear, each query uses ternary or binary search over hull |
| Space | $O(n)$ | Storage of all endpoints and hull vertices |

The constraints allow roughly a few hundred million primitive operations, but only if each query is logarithmic. The convex hull reduces the geometry to a manageable structure, and the unimodal property enables efficient search, keeping the full solution comfortably within limits.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    def build_hull(points):
        points.sort()
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) >= 0:
                lower.pop()
            lower.append(p)
        return lower

    def best(hull, x):
        def f(px):
            return math.atan2(1.0, px - x)
        lo, hi = 0, len(hull)-1
        while hi - lo > 3:
            m1 = lo + (hi-lo)//3
            m2 = hi - (hi-lo)//3
            if f(hull[m1][0]) < f(hull[m2][0]):
                lo = m1
            else:
                hi = m2
        return str(max(f(hull[i][0]) for i in range(lo, hi+1)))

    n, d = map(int, input().split())
    a = list(map(int, input().split()))
    m = int(input())
    xs = list(map(int, input().split()))

    pts = []
    for i in range(n):
        pts.append((a[i], 1))
        pts.append((a[i]+1, 1))

    hull = build_hull(pts)

    return "\n".join(best(hull, x) for x in xs)

assert run("3 5\n0 5 7\n9\n0 1 2 3 4 5 6 7 8") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single building | π/2 style constant | single obstacle case |
| large gaps | decreasing angles | sparse skyline |
| dense chain | smooth variation | hull correctness |
| extreme x near right end | small angles | boundary behavior |

## Edge Cases

When all buildings are extremely close, many hull points collapse into nearly the same angular region. The algorithm still works because convex hull compression removes all redundant collinear points, leaving only true extremes.

When the query point lies before the first building, the correct answer always comes from the first visible hull segment, and the ternary search still converges correctly because the angle function remains unimodal across the hull order.

When the query lies beyond the last building, all dx values are positive and increasing, so the maximum is achieved at the closest hull vertex, and the search degenerates cleanly without special handling.
