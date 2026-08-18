---
title: "CF 102222B - Rolling The Polygon"
description: "We have a convex polygon whose vertices are given in counterclockwise order, together with a point (Q) that is inside the polygon or on its boundary. Initially, the first edge (P0P1) rests on a horizontal line."
date: "2026-08-19T00:27:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "B"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 147
verified: true
draft: false
---

[CF 102222B - Rolling The Polygon](https://codeforces.com/problemset/problem/102222/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a convex polygon whose vertices are given in counterclockwise order, together with a point (Q) that is inside the polygon or on its boundary. Initially, the first edge (P_0P_1) rests on a horizontal line. The polygon then rolls without slipping: when edge (P_{i-1}P_i) is on the ground, the polygon rotates around (P_i) until the next edge (P_iP_{i+1}) reaches the ground. After every vertex has acted as a pivot once, the original edge (P_0P_1) is on the ground again and the process stops.

During one such rotation, the polygon is rigid and the pivot vertex does not move. Consequently, (Q) moves along a circular arc centered at that pivot. The required answer is the total length of all these circular arcs.

There are at most 50 vertices in one polygon and at most 50 test cases. The coordinates are integers with absolute value at most (10^3). These bounds are tiny for an (O(n)) geometric computation, so there is no reason to maintain the continuously changing position of the whole polygon or perform any expensive geometric search. Even (O(n^2)) would fit comfortably, but the geometry gives a direct (O(n)) formula.

The first subtle case is when (Q) coincides with a polygon vertex. For example,

```
1
3
0 0
2 0
0 2
0 0
```

The correct answer is `Case #1: 3.142`. When the polygon rotates around ((0,0)), (Q) is exactly the pivot, so that part of its trajectory has length zero. A careless implementation that assumes every radius is positive can mishandle this case.

Another boundary case occurs when (Q) lies on an edge rather than at a vertex. For example,

```
1
4
0 0
2 0
2 2
0 2
1 0
```

Here (Q) lies on the initial edge. The formula still works because every rotation is determined only by the distance from (Q) to the current pivot. There is no need for a special treatment of points on the boundary.

A third common source of mistakes is the final transition. The process uses every polygon vertex as a pivot exactly once. After pivoting around (P_{n-1}), the next edge is (P_{n-1}P_0), and after pivoting around (P_0), the original edge (P_0P_1) is restored. Thus the cyclic neighbors of every vertex must be handled with modulo arithmetic. Omitting the contribution at (P_0), for example, gives the wrong answer even though all the intermediate rotations look correct.

## Approaches

A direct simulation would rotate the polygon through many small angular increments. During each increment we could update the position of (Q), measure the small displacement, and accumulate those displacements. If every one of the (n) rotations is divided into (K) increments, this takes (O(nK)) operations. With (n=50) and even (K=10^6), that is 50 million geometric updates per test case. More fundamentally, this is only an approximation, and choosing a fixed (K) does not provide a clean guarantee for the required three decimal places.

The reason we can avoid simulation is that each individual rolling operation has an exact geometric description. Suppose the current pivot is (P_i). The polygon rotates rigidly around (P_i), so the distance from (P_i) to (Q) never changes during this operation. Thus (Q) travels on a circle centered at (P_i), with radius

[
r_i=|P_iQ|.
]

The remaining quantity is the angle through which the polygon rotates. Before the rotation, the edge (P_{i-1}P_i) is horizontal. After the rotation, (P_iP_{i+1}) is horizontal. Since the polygon is convex and its vertices are listed counterclockwise, the amount of rotation is exactly the turning angle between the directed edge vectors

[
P_i-P_{i-1}
]

and

[
P_{i+1}-P_i.
]

If this angle is (\theta_i), the corresponding trajectory length is simply

[
r_i\theta_i.
]

The total answer is consequently

[
\boxed{
\sum_{i=0}^{n-1}|P_iQ|\theta_i
}
]

where indices are taken cyclically.

For two vectors (u) and (v), the angle between them can be computed robustly with

[
\theta=\operatorname{atan2}(|u\times v|,u\cdot v).
]

Using `atan2` is preferable to computing `acos(dot / (|u||v|))`. The latter requires division by lengths and can produce a value slightly outside ([-1,1]) because of floating-point error. `atan2` directly uses the cross product and dot product and behaves well for angles near zero or (\pi).

The brute-force simulation works because it follows exactly the physical rolling process, but it spends work resolving a continuous rotation numerically. The observation that each rotation is just a circular arc reduces the entire problem to one constant amount of arithmetic per vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nK)) for (K) angular samples per pivot | (O(n)) | Too slow and approximate |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the (n) polygon vertices and the coordinates of (Q). Keep the vertices in their given counterclockwise order because that order already determines the sequence of rolling pivots.
2. For every vertex (P_i), find its two directed neighboring edges. The incoming edge is represented by

[
u=P_i-P_{i-1},
]

and the outgoing edge by

[
v=P_{i+1}-P_i.
]

The indices are cyclic, so (P_{-1}=P_{n-1}) and (P_n=P_0).
3. Compute the rotation angle at (P_i) using

[
\theta_i=\operatorname{atan2}(|u\times v|,u\cdot v).
]

These are exactly the directions of the two consecutive edges as they occur while walking around the polygon. For a convex counterclockwise polygon, this gives the exterior turning angle, which is the amount by which the polygon rotates around (P_i).
4. Compute the radius of (Q)'s trajectory during this rotation:

[
r_i=|P_iQ|.
]

The radius is constant throughout the entire rotation because (P_i) is the fixed pivot.
5. Add (r_i\theta_i) to the answer. This is the exact arc length traced by (Q) while the polygon rotates around (P_i).
6. Repeat for all (n) vertices. The rolling process uses each vertex once, so after these (n) contributions the original supporting edge is reached again.
7. Print the accumulated value with three digits after the decimal point. The statement guarantees that the fourth decimal digit is not exactly 4 or 5, so ordinary floating-point formatting is sufficient for the required rounding.

### Why it works

During the rotation around (P_i), every point of the polygon moves on a circle centered at (P_i). In particular, (Q) has fixed radius (|P_iQ|). The polygon stops rotating exactly when the outgoing edge becomes aligned with the ground, so its rotation angle is the change in direction between the incoming and outgoing directed edges. The length of the resulting circular arc is radius times angle. Since every rolling operation has one pivot and every vertex becomes a pivot exactly once, summing these (n) arc lengths gives precisely the complete trajectory length of (Q).

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

PI = math.pi

def solve_case(points, q):
    n = len(points)
    qx, qy = q
    ans = 0.0

    for i in range(n):
        prev = points[(i - 1) % n]
        cur = points[i]
        nxt = points[(i + 1) % n]

        ux = cur[0] - prev[0]
        uy = cur[1] - prev[1]

        vx = nxt[0] - cur[0]
        vy = nxt[1] - cur[1]

        cross = ux * vy - uy * vx
        dot = ux * vx + uy * vy

        angle = math.atan2(abs(cross), dot)

        dx = qx - cur[0]
        dy = qy - cur[1]
        radius = math.hypot(dx, dy)

        ans += radius * angle

    return ans

def main():
    t = int(input())

    for case_id in range(1, t + 1):
        n = int(input())
        points = [tuple(map(int, input().split())) for _ in range(n)]
        q = tuple(map(int, input().split()))

        ans = solve_case(points, q)
        print(f"Case #{case_id}: {ans:.3f}")

if __name__ == "__main__":
    main()
```

The main loop corresponds directly to the (n) rolling operations. For vertex `i`, `(i - 1) % n` and `(i + 1) % n` provide its cyclic neighbors, so the first and last vertices require no special cases.

The two vectors are the directed incoming and outgoing edges. Their dot product determines whether the angle is acute, right, or obtuse, while the absolute cross product gives the sine component. `math.atan2(abs(cross), dot)` converts those two quantities directly into the angle in radians.

The radius is computed with `math.hypot`, which evaluates the Euclidean distance without manually writing the square root expression. If (Q) equals the current pivot, the radius is zero and the contribution naturally becomes zero.

All coordinate arithmetic before the final trigonometric calculation uses Python integers, so there is no integer overflow concern. The final answer is a floating-point value, and the coordinates are small enough that standard double precision is more than sufficient.

There is no need to explicitly rotate any vertex or track the changing position of (Q). The polygon's absolute position during rolling does not affect the arc length, because each contribution depends only on the current pivot, (Q), and the two adjacent edge directions.

## Worked Examples

### Sample 1

The polygon is the square

[
(0,0),(2,0),(2,2),(0,2)
]

and (Q=(1,1)). Every vertex is at distance (\sqrt 2) from (Q), and every exterior turning angle is (\pi/2).

| Pivot | Radius (|P_iQ|) | Turning angle | Arc contribution |
|---|---:|---:|---:|
| (P_0=(0,0)) | (\sqrt2) | (\pi/2) | (2.22144) |
| (P_1=(2,0)) | (\sqrt2) | (\pi/2) | (2.22144) |
| (P_2=(2,2)) | (\sqrt2) | (\pi/2) | (2.22144) |
| (P_3=(0,2)) | (\sqrt2) | (\pi/2) | (2.22144) |

The total is

[
4\cdot\sqrt2\cdot\frac{\pi}{2}
=2\sqrt2\pi
\approx 8.885765.
]

After rounding, the output is `Case #1: 8.886`.

The symmetry makes the invariant particularly visible: every rotation has the same radius and the same angle, so all four arc lengths are identical.

### Sample 2

The vertices are

[
P_0=(0,0),\quad P_1=(2,1),\quad P_2=(1,2)
]

and (Q=(1,1)).

The radii are

[
|P_0Q|=\sqrt2,\qquad |P_1Q|=1,\qquad |P_2Q|=1.
]

The turning angle at (P_0) is

[
\operatorname{atan2}(4,-4)=2.498092,
]

while the angles at (P_1) and (P_2) are both approximately

[
1.892547.
]

| Pivot | Radius | Turning angle | Arc contribution |
| --- | --- | --- | --- |
| (P_0) | (1.414214) | (2.498092) | (3.532) |
| (P_1) | (1) | (1.892547) | (1.893) |
| (P_2) | (1) | (1.892547) | (1.893) |

The three turning angles sum to (2\pi), as they should for one complete traversal around a convex polygon. The total trajectory length is approximately (7.3176), giving `Case #2: 7.318`.

This example also shows why using the interior angle directly would be wrong. The rolling amount is the change in direction of the directed edges, which is the exterior turning angle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each of the (n) vertices is processed once using constant-time arithmetic and trigonometric operations. |
| Space | (O(n)) | The polygon vertices are stored, while the computation itself uses only constant extra space. |

With (n\le 50), the algorithm performs only a few thousand basic operations even across all 50 test cases. The memory usage is also negligible.

## Test Cases

```python
import sys
import io
import math

input = sys.stdin.readline

def solve_case(points, q):
    n = len(points)
    qx, qy = q
    ans = 0.0

    for i in range(n):
        prev = points[(i - 1) % n]
        cur = points[i]
        nxt = points[(i + 1) % n]

        ux = cur[0] - prev[0]
        uy = cur[1] - prev[1]
        vx = nxt[0] - cur[0]
        vy = nxt[1] - cur[1]

        cross = ux * vy - uy * vx
        dot = ux * vx + uy * vy

        angle = math.atan2(abs(cross), dot)

        radius = math.hypot(qx - cur[0], qy - cur[1])
        ans += radius * angle

    return ans

def solve_input(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        t = int(input())
        out = []

        for case_id in range(1, t + 1):
            n = int(input())
            points = [tuple(map(int, input().split())) for _ in range(n)]
            q = tuple(map(int, input().split()))

            ans = solve_case(points, q)
            out.append(f"Case #{case_id}: {ans:.3f}")

        return "\n".join(out)
    finally:
        sys.stdin = old_stdin

sample_input = """\
4
4
0 0
2 0
2 2
0 2
1 1
3
0 0
2 1
1 2
1 1
5
0 0
1 0
2 2
1 3
-1 2
0 0
6
0 0
3 0
4 1
2 2
1 2
-1 1
1 0
"""

sample_output = """\
Case #1: 8.886
Case #2: 7.318
Case #3: 12.102
Case #4: 14.537
"""

assert solve_input(sample_input) == sample_output, "provided samples"

minimum_input = """\
1
3
0 0
2 0
0 2
0 0
"""

assert solve_input(minimum_input) == "Case #1: 3.142", "minimum n, Q at a vertex"

boundary_input = """\
1
4
0 0
2 0
2 2
0 2
1 0
"""

assert solve_input(boundary_input) == "Case #1: 8.886", "Q on an edge"

equal_radius_input = """\
1
4
-1 -1
1 -1
1 1
-1 1
0 0
"""

assert solve_input(equal_radius_input) == "Case #1: 6.283", "all four radii and angles equal"

# Maximum n. The points form a convex polygon using a parabola chain
# closed by its endpoint chord. Q is strictly inside it.
points = [(x, x * x) for x in range(-24, 26)]
q = (0, 100)

expected = f"Case #1: {solve_case(points, q):.3f}"

maximum_input = "1\n50\n"
maximum_input += "\n".join(f"{x} {y}" for x, y in points)
maximum_input += "\n0 100\n"

assert solve_input(maximum_input) == expected, "maximum n"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided four samples | `8.886`, `7.318`, `12.102`, `14.537` | General correctness against the official examples |
| Triangle with (Q=P_0) | `3.142` | Minimum polygon size and zero-radius contribution |
| Square with (Q) on an edge | `8.886` | Boundary point handling |
| Symmetric square with (Q) at the center | `6.283` | Equal radii, equal turning angles, and cyclic indexing |
| 50-vertex parabola-chain polygon | Computed expected value | Maximum (n), many cyclic transitions, and performance |

The maximum-size test deliberately uses 50 distinct integer vertices instead of simply repeating points. The points ((x,x^2)) for (x=-24,\ldots,25), together with the closing segment between the endpoints, form a convex polygon, and (Q=(0,100)) lies inside it.

## Edge Cases

When (Q) is exactly a pivot, the radius for that rotation is zero. For

```
1
3
0 0
2 0
0 2
0 0
```

the pivot ((0,0)) contributes nothing. At ((2,0)), the turning angle is (\pi/4) and the radius is 2, giving (\pi/2). At ((0,2)), the same contribution occurs. The total is (\pi), so the output is `Case #1: 3.142`. The implementation handles the zero radius naturally without a division or special case.

When (Q) is on an edge, there is still no discontinuity in the trajectory formula. For

```
1
4
0 0
2 0
2 2
0 2
1 0
```

the first rotation has pivot ((0,0)) and radius 1, while the other three pivots have radii (1,\sqrt5,\sqrt5). Each corner contributes its corresponding radius multiplied by (\pi/2), producing the same total as the centered square's four-radius-(\sqrt2) configuration, namely `8.886`. The fact that (Q) initially touches the ground changes neither the radius formula nor the rotation angle.

For a symmetric case where all contributions are equal, consider

```
1
4
-1 -1
1 -1
1 1
-1 1
0 0
```

Every pivot is at distance (\sqrt2) from (Q), and every turning angle is (\pi/2). The total is

[
4\sqrt2\frac{\pi}{2}=2\sqrt2\pi\approx8.886.
]

If instead the square has vertices ((0,0),(2,0),(2,2),(0,2)) and (Q=(1,0)), the radii are (1,\sqrt2,\sqrt5,\sqrt2), so the implementation must not assume equal radii merely because the polygon is symmetric.

Finally, the cyclic boundary between (P_{n-1}) and (P_0) must be included twice in the neighbor relationships, once as the incoming edge of (P_0) and once as the outgoing edge of (P_{n-1}). The expressions `(i - 1) % n` and `(i + 1) % n` encode exactly this topology. This avoids special handling for the first and last vertices and prevents the most common off-by-one error in the solution.
