---
title: "CF 102219H - Are You Safe?"
description: "The sensor coordinates describe a set of points in the plane. The affected region is the shortest closed polygon that contains every sensor, which is exactly the convex hull of the sensor points."
date: "2026-08-20T04:14:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "H"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 1178
verified: false
draft: false
---

[CF 102219H - Are You Safe?](https://codeforces.com/problemset/problem/102219/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 19m 38s  
**Verified:** no  

## Solution
## Problem Understanding

The sensor coordinates describe a set of points in the plane. The affected region is the shortest closed polygon that contains every sensor, which is exactly the convex hull of the sensor points. We must print the vertices of that hull in counter-clockwise order, repeating the first vertex at the end.

After constructing the affected region, the remaining coordinates are locations whose safety must be determined. A location strictly inside the convex hull is unsafe. A location outside it is safe, and a location exactly on its boundary is also safe.

The sensor count and location count are both at most 50, and there can be at most 50 test cases. Coordinates are integers in the small range from -500 to 500. These bounds make even an O(CP) point-in-polygon check trivial, but they also make a standard O(C log C) convex hull particularly convenient. There is no need for floating-point geometry or complicated spatial data structures. Integer cross products are enough, and their magnitude is tiny enough to fit comfortably in Python integers.

The first subtle case is a location on the boundary. Consider three sensors forming a triangle:

```
3 1
0 0
4 0
0 4
2 0
```

The location `(2, 0)` lies exactly on a hull edge, so the output must be `2 0 is safe!`. A careless point-in-polygon implementation that treats boundary points as inside would incorrectly mark it unsafe.

A second case is a sensor lying on an edge between two actual hull vertices:

```
4 1
0 0
4 0
4 4
0 4
2 0
```

The point `(2, 0)` is a sensor, but it is not a vertex of the minimum-perimeter polygon. The hull should contain only `(0,0)`, `(4,0)`, `(4,4)`, and `(0,4)`. Keeping every collinear sensor would produce extra points on the printed perimeter even though they are not polygon vertices.

A third case is when all sensors are collinear:

```
3 2
0 0
2 0
4 0
1 0
5 0
```

The convex hull degenerates to the two endpoints `(0,0)` and `(4,0)`. There is no two-dimensional interior, so both query points are safe. A solution that blindly assumes the hull has at least three vertices can fail here.

Duplicate sensor coordinates create another similar degeneracy:

```
3 1
1 1
1 1
1 1
1 1
```

There is only one distinct point, so the affected region has no interior. The query point is on the degenerate hull and is safe. Removing duplicates before building the hull handles this naturally.

## Approaches

A direct brute-force solution could try every possible ordering of the sensor points, close the ordering into a polygon, check whether the resulting polygon contains every sensor, and keep the valid polygon with minimum perimeter. This is correct because the desired polygon must have its vertices among the sensor coordinates, and checking every ordering eventually considers the optimal ordering.

The problem is the number of orderings. With C = 50, there are 50! approximately 3.04 × 10^64 possible permutations. Even if checking one permutation took only O(C), the work would be on the order of 50 × 50!, roughly 1.52 × 10^66 basic geometric operations. The 15 second limit is nowhere close to allowing this.

The brute force works because the answer is a polygon whose boundary is determined by the extreme sensor points. The key observation is that any sensor lying strictly inside a convex polygon can never be needed as a vertex of the minimum-perimeter enclosing polygon. Likewise, if several sensors are collinear along one hull edge, only the two endpoints matter. What remains is precisely the convex hull.

Once the sensors are reduced to their convex hull, Andrew's monotone chain algorithm constructs it in O(C log C) time. Sorting gives the points a deterministic order, and the cross product tells us whether the most recently added point makes a left or right turn. A non-left turn in the lower or upper chain means the middle point cannot be a hull vertex, so it can be removed.

After the hull is known, each location can be classified by checking its orientation relative to every hull edge. Because the hull is counter-clockwise, a point strictly inside it has a positive cross product with every directed edge. A zero cross product means the point lies on an edge and must be classified as safe.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C · C!) | O(C) | Too slow |
| Optimal | O(C log C + CP) | O(C) | Accepted |

## Algorithm Walkthrough

1. Read the sensor coordinates and remove duplicate points. Duplicate coordinates do not create additional geometric information, so retaining them would only complicate the hull construction.
2. Sort the distinct sensor points lexicographically by `(x, y)`. This gives Andrew's algorithm the ordering it needs and also makes the leftmost and rightmost points deterministic.
3. Build the lower hull from left to right. For each new point, append it and inspect the last three points. If their cross product is less than or equal to zero, remove the middle point. A negative cross product means a clockwise turn, so the middle point lies inside the boundary. A zero cross product means the three points are collinear, and the middle point is not needed as a hull vertex.
4. Build the upper hull using the same rule, but processing the sorted points in reverse order. Concatenating the lower and upper chains gives the complete convex hull in counter-clockwise order.
5. Remove the duplicated endpoints created when joining the two chains. The resulting list contains every actual hull vertex exactly once.
6. Print every hull vertex on its own line and then print the first vertex again. The monotone chain construction gives counter-clockwise orientation, so no additional sorting or rotation is required.
7. For each query location, first handle degenerate hulls. If there are fewer than three distinct hull vertices, the hull has no two-dimensional interior, so every location is safe.
8. For a proper polygon, compute the cross product of every directed hull edge with the vector from that edge's start to the query point. If any cross product is negative, the location is outside. If any cross product is zero, it is on the boundary and is safe. Only when every cross product is strictly positive is the location strictly inside and therefore unsafe.

### Why it works

The convex hull is the smallest convex set containing all sensors. Any enclosing polygon of minimum perimeter can be replaced by the boundary of this convex hull without increasing the perimeter, while every sensor remains enclosed. Thus the required perimeter consists exactly of the convex hull vertices, with collinear points between two vertices omitted.

Andrew's algorithm maintains the invariant that each current chain is a valid convex boundary for the processed points. Whenever the last three points make a non-left turn, the middle point cannot be an extreme point of the convex hull, so removing it preserves the correct boundary. After processing every point in both directions, the two chains form the complete convex hull.

For a counter-clockwise convex polygon, every interior point lies strictly to the left of every directed edge. Hence all edge cross products are positive exactly for points in the strict interior. A zero cross product identifies the boundary, which the problem explicitly classifies as safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - \
           (b[1] - a[1]) * (c[0] - a[0])

def convex_hull(points):
    points = sorted(set(points))

    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def strictly_inside(hull, p):
    n = len(hull)

    if n < 3:
        return False

    for i in range(n):
        a = hull[i]
        b = hull[(i + 1) % n]
        value = cross(a, b, p)

        if value <= 0:
            return False

    return True

def solve():
    t = int(input())
    output = []

    for case_no in range(1, t + 1):
        c, p = map(int, input().split())

        sensors = [tuple(map(int, input().split())) for _ in range(c)]
        locations = [tuple(map(int, input().split())) for _ in range(p)]

        hull = convex_hull(sensors)

        output.append(f"Case {case_no}")

        if hull:
            for x, y in hull:
                output.append(f"{x} {y}")
            output.append(f"{hull[0][0]} {hull[0][1]}")

        for x, y in locations:
            if strictly_inside(hull, (x, y)):
                status = "unsafe!"
            else:
                status = "safe!"
            output.append(f"{x} {y} is {status}")

        if case_no != t:
            output.append("")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The `cross` function computes the signed area of the triangle formed by three points, multiplied by two. Its sign is what the hull construction needs. Positive means a counter-clockwise turn, zero means collinearity, and negative means a clockwise turn.

The `convex_hull` function first uses `set` to eliminate duplicate coordinates, then sorts the points. The `<= 0` condition is deliberate. Using `< 0` would retain collinear points on hull edges, but the required perimeter consists of the actual polygon vertices, so intermediate collinear sensors must be removed.

The two chains share their first and last point, which is why `lower[:-1]` and `upper[:-1]` are concatenated. This avoids duplicating those endpoints inside the hull representation. The first hull point is printed once more separately because the required output explicitly closes the polygon.

The containment test uses only integer arithmetic. The query is unsafe only if every cross product is strictly positive. A cross product of zero immediately returns `False`, correctly treating an edge or vertex as safe. Python integers do not overflow, although with the coordinate bounds the actual products are already very small.

The implementation does not use floating point anywhere. That is useful for this problem because a point can lie exactly on an edge, and floating-point comparisons could turn an exact boundary case into an incorrect inside or outside classification.

## Worked Examples

### Sample Case 1

The six sensors are:

```
(-477,-180)
(31,-266)
(-474,28)
(147,49)
(323,-53)
(277,-79)
```

After sorting, Andrew's algorithm removes `(277,-79)` because it is inside the turn formed by the surrounding hull vertices. The resulting hull has five vertices.

| Stage | Current operation | Hull state |
| --- | --- | --- |
| Sorted points | Process left to right | `(-477,-180), (-474,28), (31,-266), (147,49), (277,-79), (323,-53)` |
| Lower hull | Remove clockwise/collinear turns | `(-477,-180), (31,-266), (323,-53)` |
| Upper hull | Process in reverse | `(-477,-180), (-474,28), (147,49), (323,-53)` |
| Combined hull | Join both chains | `(-477,-180), (31,-266), (323,-53), (147,49), (-474,28)` |
| Close polygon | Repeat first point | `(-477,-180)` |

For the five locations, `(-139,-183)` produces a positive cross product against every hull edge, so it is strictly inside and unsafe. The other four locations are either outside or on the boundary, so they are safe. The output begins at `(-477,-180)`, follows the hull counter-clockwise, and ends by repeating that point.

### Sample Case 2

The five sensors are:

```
(-52,-325)
(104,420)
(315,356)
(-192,8)
(493,146)
```

All five points are hull vertices.

| Stage | Current operation | Hull state |
| --- | --- | --- |
| Sorted points | Process left to right | `(-192,8), (-52,-325), (104,420), (315,356), (493,146)` |
| Lower hull | Remove non-left turns | `(-192,8), (-52,-325), (493,146)` |
| Upper hull | Process in reverse | `(-192,8), (104,420), (315,356), (493,146)` |
| Combined hull | Join both chains | `(-192,8), (-52,-325), (493,146), (315,356), (104,420)` |
| Close polygon | Repeat first point | `(-192,8)` |

The query `(404,228)` lies strictly inside because every edge sees it on its left side. It is consequently unsafe. The query `(-239,484)` lies outside the polygon and is safe.

The two traces also show why the hull is built from turns rather than by testing every possible polygon. Points that cannot remain on a convex boundary disappear as soon as the local turn proves they are unnecessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C log C + CP) | Sorting dominates hull construction, then every location checks at most C hull edges |
| Space | O(C) | The sorted points and the two hull chains contain O(C) points |

With C and P at most 50, the worst case for one test case performs only a few thousand cross-product operations after the O(C log C) sort. Even with 50 test cases, this is comfortably inside the 15 second limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

input = sys.stdin.readline

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - \
           (b[1] - a[1]) * (c[0] - a[0])

def convex_hull(points):
    points = sorted(set(points))

    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def strictly_inside(hull, p):
    if len(hull) < 3:
        return False

    for i in range(len(hull)):
        if cross(hull[i], hull[(i + 1) % len(hull)], p) <= 0:
            return False

    return True

def solve():
    t = int(input())
    output = []

    for case_no in range(1, t + 1):
        c, p = map(int, input().split())
        sensors = [tuple(map(int, input().split())) for _ in range(c)]
        locations = [tuple(map(int, input().split())) for _ in range(p)]

        hull = convex_hull(sensors)

        output.append(f"Case {case_no}")

        for x, y in hull:
            output.append(f"{x} {y}")
        if hull:
            output.append(f"{hull[0][0]} {hull[0][1]}")

        for x, y in locations:
            status = "unsafe!" if strictly_inside(hull, (x, y)) else "safe!"
            output.append(f"{x} {y} is {status}")

        if case_no != t:
            output.append("")

    return "\n".join(output)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample = """\
2
6 5
-477 -180
31 -266
-474 28
147 49
323 -53
277 -79
346 488
-139 -183
-427 129
386 -222
-408 -315
5 2
-52 -325
104 420
315 356
-192 8
493 146
404 228
-239 484
"""

expected_sample = """\
Case 1
-477 -180
31 -266
323 -53
147 49
-474 28
-477 -180
346 488 is safe!
-139 -183 is unsafe!
-427 129 is safe!
386 -222 is safe!
-408 -315 is safe!

Case 2
-192 8
-52 -325
493 146
315 356
104 420
-192 8
404 228 is unsafe!
-239 484 is safe!"""

assert run(sample) == expected_sample, "provided sample"

minimum_triangle = """\
1
3 4
0 0
4 0
0 4
2 2
2 0
5 5
0 4
"""

expected_minimum_triangle = """\
Case 1
0 0
4 0
0 4
0 0
2 2 is unsafe!
2 0 is safe!
5 5 is safe!
0 4 is safe!"""

assert run(minimum_triangle) == expected_minimum_triangle, \
    "minimum-size triangle and boundary cases"

collinear = """\
1
3 3
0 0
2 0
4 0
1 0
4 0
5 0
"""

expected_collinear = """\
Case 1
0 0
4 0
0 0
1 0 is safe!
4 0 is safe!
5 0 is safe!"""

assert run(collinear) == expected_collinear, \
    "collinear sensors"

duplicates = """\
1
5 3
1 1
1 1
1 1
2 2
2 2
1 1
2 2
0 0
"""

expected_duplicates = """\
Case 1
1 1
2 2
1 1
1 1 is safe!
2 2 is safe!
0 0 is safe!"""

assert run(duplicates) == expected_duplicates, \
    "duplicate and collinear sensors"

boundary_square = """\
1
8 5
0 0
10 0
10 10
0 10
5 0
10 5
5 10
0 5
5 5
0 0
10 10
11 5
5 10
"""

expected_boundary_square = """\
Case 1
0 0
10 0
10 10
0 10
0 0
5 5 is unsafe!
0 0 is safe!
10 10 is safe!
11 5 is safe!
5 10 is safe!"""

assert run(boundary_square) == expected_boundary_square, \
    "collinear edge points and boundary queries"

all_equal = """\
1
3 3
7 7
7 7
7 7
7 7
8 8
6 7
"""

expected_all_equal = """\
Case 1
7 7
7 7
7 7 is safe!
8 8 is safe!
6 7 is safe!"""

assert run(all_equal) == expected_all_equal, \
    "all sensors equal"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size triangle | Triangle vertices, interior unsafe, edge safe | Minimum valid sensor count and strict boundary handling |
| Three collinear sensors | Two endpoints and no unsafe location | Degenerate hull with no interior |
| Duplicate sensors | Two distinct endpoints | Duplicate removal and degenerate geometry |
| Square with sensors on every edge | Four corner vertices only | Collinear points on hull edges must not be printed |
| All sensors equal | One point repeated to close the perimeter | Complete degeneracy and duplicate coordinates |

## Edge Cases

The boundary rule is handled directly by the condition `cross <= 0`. For the triangle with sensors `(0,0)`, `(4,0)`, and `(0,4)`, the location `(2,0)` has cross product zero against the first edge. The function immediately returns `False`, producing `2 0 is safe!`. The interior location `(2,2)` has positive cross products against all three edges and is consequently unsafe.

For collinear sensors `(0,0)`, `(2,0)`, and `(4,0)`, the lower and upper chains collapse to the two endpoints. The final hull is `[(0,0), (4,0)]`. Since its length is less than three, `strictly_inside` returns `False` without attempting polygon-edge logic. Thus `(1,0)`, `(4,0)`, and even `(5,0)` are all safe, because a line segment has no two-dimensional interior.

When several sensors lie on the same hull edge, the `<= 0` removal condition discards the intermediate points. For the square containing `(5,0)`, `(10,5)`, `(5,10)`, and `(0,5)`, each of those points is removed while processing the corresponding chain. The printed polygon contains only `(0,0)`, `(10,0)`, `(10,10)`, and `(0,10)`, which are the actual vertices of the minimum enclosing polygon.

For duplicate coordinates, `sorted(set(points))` reduces repeated sensors to one geometric point. With three copies of `(7,7)`, the hull becomes `[(7,7)]`. The code prints `(7,7)` twice so the perimeter listing begins and ends at the same point, and every query is safe because there is no two-dimensional affected interior.

The use of integer cross products also handles vertices exactly. A query equal to a hull vertex makes the cross product with one or more incident edges zero, so it is classified as safe rather than unsafe. No epsilon is needed because every coordinate and every operation is exact.
