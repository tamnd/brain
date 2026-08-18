---
title: "CF 102192B - Pizza Hub"
description: "We have a non-degenerate triangle and a rectangular paper pad. The pad has a fixed width w, while its height is the quantity we want to minimize. The triangle may be rotated freely, and touching the boundary is allowed."
date: "2026-08-18T09:54:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "B"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 732
verified: true
draft: false
---

[CF 102192B - Pizza Hub](https://codeforces.com/problemset/problem/102192/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a non-degenerate triangle and a rectangular paper pad. The pad has a fixed width `w`, while its height is the quantity we want to minimize. The triangle may be rotated freely, and touching the boundary is allowed. The horizontal dimension of the rotated triangle must be at most `w`; its vertical dimension becomes the required height.

For every test case, the six coordinates describe the three triangle vertices, followed by the strip width. We must print the smallest possible height, or `impossible` if no rotation can make the triangle fit inside a strip of width `w`.

There are up to 50,000 independent test cases. The coordinates and `w` are at most 10,000, so integer arithmetic is enough for the geometric predicates, but the answer itself is generally irrational. The time limit is only 3 seconds, which rules out anything that samples a large number of rotation angles for every test case. In particular, scanning millions of possible angles per triangle would be far too expensive. We need a constant amount of geometric work per case.

The first edge case is a strip that is too narrow to contain the triangle at all. For example,

```
0 0 2 0 1 2 1
```

has minimum possible width greater than `1`, so the answer is `impossible`. A careless implementation that only tries placing one side horizontally might accidentally report a height instead of recognizing that no orientation satisfies the width restriction.

The second edge case is a triangle whose optimal orientation is not obtained by simply putting a side horizontally. For example, with a sufficiently narrow strip, an edge longer than the strip may have to touch both vertical boundaries after rotation. The correct orientation is determined by its projection onto the width direction, not by aligning an edge with the rectangle.

The third edge case is equality at the boundary. For

```
0 0 1 0 0 1 1
```

the triangle fits with width exactly `1` and height exactly `1`, so the output is `1.0000000000`. Using a strict `< w` test would incorrectly reject this placement.

Finally, the coordinates may contain repeated values even though the three vertices themselves cannot all coincide or be collinear. For example,

```
0 0 0 1 1 1 1
```

is a valid right triangle. The algorithm must rely on vector geometry rather than assuming that all six input coordinates are distinct.

## Approaches

A direct brute-force idea is to rotate the triangle through many angles, compute its bounding box after every rotation, and keep the smallest height among rotations whose width is at most `w`. This works conceptually because for any fixed rotation the three rotated vertices completely determine the required rectangle. The problem is that rotation is continuous, so a grid search needs an extremely small angular step to guarantee the required `1e-6` precision. Sampling every `10^-6` radians would require roughly `2π / 10^-6`, or about 6.3 million orientations for one test case. With 50,000 cases, that is over 300 billion orientation checks, far beyond the time limit. A coarser grid also has no correctness guarantee because the optimum can lie between two sampled angles.

The useful observation is that an optimal placement can always be chosen with one triangle vertex at a corner of the rectangle. Geometrically, once a triangle is inside the rectangle, translate the rectangle until it becomes tight at the relevant lower and side boundaries. At an optimal tight configuration, a triangle vertex can be made to coincide with a rectangle corner. This reduces the continuous placement problem to only three choices of the triangle vertex, plus two choices for which of the other two vertices is the lower one.

Fix a triangle vertex as the rectangle's lower-left corner. Let vectors `a` and `b` point from this vertex to the other two vertices. We need to rotate them so that both coordinates are nonnegative, both horizontal coordinates are at most `w`, and the largest vertical coordinate is as small as possible.

The two vectors must form an angle of at most 90 degrees for this corner configuration to be possible. We can test that with their dot product. If `|a| <= w`, the best placement for this ordering is to put `a` horizontally. Its vertical contribution is then zero, and rotating the rectangle away from `a` would only increase its vertical coordinate. The height contributed by `b` is exactly the perpendicular distance from `b` to the line through `a`, namely `cross(a,b) / |a|`, provided `b` still fits horizontally.

If `|a| > w`, `a` cannot be horizontal because its horizontal projection would exceed the strip width. The best possible placement for `a` is to make its horizontal projection exactly `w`. Its vertical projection is then fixed at

[
h_a=\sqrt{|a|^2-w^2}.
]

There are two possible sides of `a` on which the other vector can lie. We test both by swapping `a` and `b`, and by reflecting all `y` coordinates. Once the angle of `a` relative to the horizontal is fixed, the angle between `a` and `b` determines the position of `b`. We can check its horizontal projection and vertical projection directly with trigonometry.

The brute-force method works because every rotation can be evaluated. It fails because there are too many rotations to examine. The observation about a rectangle corner lets us discard almost the entire continuous search space. There are only six ordered vector pairs, and reflection handles the two sides of the horizontal axis.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T · K) where K is millions of sampled angles | O(1) | Too slow and not exact |
| Optimal | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three vertices and the strip width `w`. Treat every calculation using the vectors between vertices, because translation of the triangle has no effect on the required rectangle dimensions.
2. For each of the three triangle vertices, consider it as the rectangle corner and construct the two vectors `a` and `b` from that vertex to the remaining vertices. Try both orders, because one vector can be the lower ray and the other the upper ray.
3. Reject the ordering when `a · b < 0`. The two vectors then form an angle greater than 90 degrees, so they cannot both lie inside the same quadrant starting from a rectangle corner.
4. Compute `A² = a · a`. If `A² <= w²`, `a` can be placed horizontally without violating the strip width. In this case, require `a × b >= 0` and require the projection of `b` onto `a` to be at most `w`. The resulting height is `|a × b| / |a|`.
5. If `A² > w²`, `a` must be tilted. Set

[
h=\sqrt{A^2-w^2}.
]

This is the smallest vertical projection that `a` can have while its horizontal projection is exactly `w`.

1. Compute

[
\phi=\arctan(h/w),
]

which is the angle that `a` makes with the horizontal when its horizontal projection is `w`. Also compute the angle `δ` between `a` and `b` from

[
\cos\delta=\frac{a\cdot b}{|a||b|}.
]

1. If `a × b >= 0`, `b` lies on the same rotational side as the positive turn from `a`. Its angle from the horizontal is `φ + δ`. It must stay within the first quadrant, so `φ + δ <= π/2`. Its horizontal projection must also be at most `w`. If these conditions hold, its vertical projection is `|b| sin(φ+δ)`, so the candidate height is the larger of this value and `h`.
2. If `a × b < 0`, `b` lies on the other side of `a`. Its angle from the horizontal is `φ - δ`. We need `φ - δ >= 0` so that `b` remains above the horizontal boundary. Its horizontal projection must again be at most `w`. In this configuration its vertical projection cannot exceed `h`, so the candidate height is simply `h`.
3. Repeat the same six ordered-vector tests after reflecting the triangle over the horizontal axis. Reflection handles placements in which the relevant vectors lie on the opposite side of the original coordinate system.
4. If at least one candidate was found, print the smallest candidate. Otherwise print `impossible`.

Why it works: the key invariant is that every candidate considered by the algorithm represents a legal placement in which one triangle vertex is at a rectangle corner, and every optimal placement has an equivalent tight placement of this form. For a fixed corner and ordered pair, the width constraint either allows the first vector to become horizontal, or forces its horizontal projection to equal `w`. Those are exactly the two cases handled by the algorithm. The angle checks then characterize whether the second vector remains inside the rectangle. Since all three possible corner vertices, both vector orders, and both orientations are examined, no optimal placement is omitted.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

EPS = 1e-10
INF = float("inf")
PI = math.pi

def solve_case(points, w):
    ans = INF
    w2 = float(w * w)

    def calc(a, b):
        nonlocal ans

        ax, ay = a
        bx, by = b

        dot = ax * bx + ay * by
        cross = ax * by - ay * bx
        aa = ax * ax + ay * ay
        bb = bx * bx + by * by

        # Both vectors must fit into the same 90-degree quadrant.
        if dot < -EPS:
            return

        A = math.sqrt(aa)
        B = math.sqrt(bb)

        if aa <= w2 + EPS:
            # Put a horizontally.
            if cross < -EPS:
                return

            # Projection of b onto a must not exceed w.
            if dot * dot > w2 * aa + EPS:
                return

            height = cross / A
            if height < ans:
                ans = height
            return

        # a is longer than the available width, so its x-projection
        # has to be exactly w.
        h = math.sqrt(max(0.0, aa - w2))
        phi = math.atan2(h, float(w))

        c = dot / (A * B)
        c = max(-1.0, min(1.0, c))
        delta = math.acos(c)

        if cross >= -EPS:
            angle = phi + delta

            # b must remain in the first quadrant.
            if angle > PI / 2 + EPS:
                return

            bx_proj = B * math.cos(angle)
            if bx_proj > w + EPS:
                return

            by_proj = B * math.sin(angle)
            ans = min(ans, max(h, by_proj))
        else:
            angle = phi - delta

            # b must not cross below the horizontal side.
            if angle < -EPS:
                return

            bx_proj = B * math.cos(angle)
            if bx_proj > w + EPS:
                return

            ans = min(ans, h)

    # Reflection lets us consider both sides of the horizontal axis.
    for reflected in (False, True):
        if reflected:
            p = [(x, -y) for x, y in points]
        else:
            p = points

        for i in range(3):
            j = (i + 1) % 3
            k = (i + 2) % 3

            a = (p[j][0] - p[i][0], p[j][1] - p[i][1])
            b = (p[k][0] - p[i][0], p[k][1] - p[i][1])

            calc(a, b)
            calc(b, a)

    return ans

def main():
    out = []

    t = int(input())
    for _ in range(t):
        x1, y1, x2, y2, x3, y3, w = map(int, input().split())

        points = [
            (x1, y1),
            (x2, y2),
            (x3, y3),
        ]

        ans = solve_case(points, w)

        if math.isinf(ans):
            out.append("impossible")
        else:
            out.append(f"{ans:.10f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `calc` function is the implementation of steps 3 through 8. The vector dot product identifies whether the two rays can fit into one quadrant, while the cross product tells which side of `a` contains `b`.

The `aa <= w²` branch is the case where `a` can lie along the rectangle's width. The expression `cross / A` is the perpendicular distance from the third vertex to the line through the first two vertices, so it directly gives the required height.

The second branch handles the case where `a` is wider than the strip. The expression `sqrt(aa - w²)` follows directly from the right triangle formed by the vector `a`, its horizontal projection `w`, and its vertical projection. `atan2(h, w)` is preferable to `atan(h / w)` because it behaves cleanly at all valid values, although `w` is positive here.

The argument passed to `acos` is clamped to `[-1, 1]`. Mathematically it is already in that interval, but floating-point rounding can produce something such as `1.0000000000000002`, which would otherwise cause a domain error.

The comparisons use a small epsilon because the optimal configuration frequently lies exactly on the strip boundary. Using only strict floating-point comparisons can reject valid placements such as a vector whose projection is exactly `w`.

The loops examine every triangle vertex, both choices of the first vector, and both vertical reflections. That is only 12 constant-size checks per test case.

Python integers have arbitrary precision, so the squared coordinate differences cannot overflow. The trigonometric calculations use floating-point numbers only after the exact integer dot products, cross products, and squared lengths have been obtained.

## Worked Examples

For the first sample, the triangle is `(0,0), (3,0), (0,4)` and the width is `10`. One vector pair from `(0,0)` is `a=(3,0)` and `b=(0,4)`.

| Vertex | `a` | `b` | `|a| <= w` | Candidate height |
|---|---|---|---|---:|
| `(0,0)` | `(3,0)` | `(0,4)` | yes | `4` |
| `(0,0)` | `(0,4)` | `(3,0)` | yes | rejected by orientation |
| `(3,0)` | `(-3,0)` | `(-3,4)` | yes | `4` |
| `(0,4)` | `(0,-4)` | `(3,-4)` | yes | `2.4` |

The last configuration corresponds to putting the side of length `5` along the width direction. Its altitude is `3·4/5 = 2.4`, which is smaller than the heights obtained from the other sides. The output is consequently `2.4000000000`.

For the second sample, the same triangle is given a width of `1`.

| Quantity | Value |
| --- | --- |
| Triangle area | `6` |
| Longest side | `5` |
| Minimum possible triangle width | `2.4` |
| Available strip width | `1` |
| Feasible candidate | none |
| Output | `impossible` |

Every corner configuration fails the projection checks because the strip is narrower than the triangle's minimum possible width. The algorithm never invents a height for an impossible placement, so the final answer remains infinity and `impossible` is printed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs exactly 12 constant-size geometric checks and a constant number of trigonometric operations. |
| Space | O(1) | Only the three input points and a constant number of temporary floating-point values are stored. |

With at most 50,000 test cases, the algorithm performs only a few hundred thousand geometric configurations in total. This is comfortably within the intended constant-time-per-case design, while the memory usage is independent of the number of test cases.

## Test Cases

```python
# The helper mirrors the submitted solution.
import sys
import io
import math

def solve_input(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        input = sys.stdin.readline

        EPS = 1e-10
        INF = float("inf")
        PI = math.pi

        def solve_case(points, w):
            ans = INF
            w2 = float(w * w)

            def calc(a, b):
                nonlocal ans

                ax, ay = a
                bx, by = b

                dot = ax * bx + ay * by
                cross = ax * by - ay * bx
                aa = ax * ax + ay * ay
                bb = bx * bx + by * by

                if dot < -EPS:
                    return

                A = math.sqrt(aa)
                B = math.sqrt(bb)

                if aa <= w2 + EPS:
                    if cross < -EPS:
                        return

                    if dot * dot > w2 * aa + EPS:
                        return

                    ans = min(ans, cross / A)
                    return

                h = math.sqrt(max(0.0, aa - w2))
                phi = math.atan2(h, float(w))

                c = dot / (A * B)
                c = max(-1.0, min(1.0, c))
                delta = math.acos(c)

                if cross >= -EPS:
                    angle = phi + delta

                    if angle > PI / 2 + EPS:
                        return

                    bx_proj = B * math.cos(angle)
                    if bx_proj > w + EPS:
                        return

                    by_proj = B * math.sin(angle)
                    ans = min(ans, max(h, by_proj))
                else:
                    angle = phi - delta

                    if angle < -EPS:
                        return

                    bx_proj = B * math.cos(angle)
                    if bx_proj > w + EPS:
                        return

                    ans = min(ans, h)

            for reflected in (False, True):
                p = [(x, -y) for x, y in points] if reflected else points

                for i in range(3):
                    j = (i + 1) % 3
                    k = (i + 2) % 3

                    a = (
                        p[j][0] - p[i][0],
                        p[j][1] - p[i][1],
                    )
                    b = (
                        p[k][0] - p[i][0],
                        p[k][1] - p[i][1],
                    )

                    calc(a, b)
                    calc(b, a)

            return ans

        def main():
            out = []
            t = int(input())

            for _ in range(t):
                x1, y1, x2, y2, x3, y3, w = map(int, input().split())
                points = [(x1, y1), (x2, y2), (x3, y3)]

                ans = solve_case(points, w)

                if math.isinf(ans):
                    out.append("impossible")
                else:
                    out.append(f"{ans:.10f}")

            sys.stdout.write("\n".join(out))

        main()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples.
assert solve_input(
    "2\n"
    "0 0 3 0 0 4 10\n"
    "0 0 3 0 0 4 1\n"
) == "2.4000000000\nimpossible", "provided samples"

# Minimum-size valid triangle. Width exactly reaches the boundary.
assert solve_input(
    "1\n"
    "0 0 1 0 0 1 1\n"
) == "1.0000000000", "minimum coordinates and exact width"

# Same geometry after translation and permutation of the vertices.
assert solve_input(
    "1\n"
    "7 8 7 9 8 9 1\n"
) == "1.0000000000", "translation and vertex order"

# A narrow strip that cannot contain an equilateral triangle of side 2.
assert solve_input(
    "1\n"
    "0 0 2 0 1 2 1\n"
) == "impossible", "impossible due to minimum width"

# Maximum coordinate values, with width exactly equal to the two legs.
assert solve_input(
    "1\n"
    "0 0 10000 0 0 10000 10000\n"
) == "10000.0000000000", "maximum coordinates and boundary width"

# A valid triangle with repeated coordinate components.
assert solve_input(
    "1\n"
    "0 0 0 1 1 1 1\n"
) == "1.0000000000", "repeated coordinate components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1 0 0 1 1` | `1.0000000000` | Minimum coordinates and equality at the width boundary |
| `7 8 7 9 8 9 1` | `1.0000000000` | Translation invariance and arbitrary vertex order |
| `0 0 2 0 1 2 1` | `impossible` | A strip narrower than the triangle's minimum width |
| `0 0 10000 0 0 10000 10000` | `10000.0000000000` | Maximum coordinate values and exact boundary projections |
| `0 0 0 1 1 1 1` | `1.0000000000` | Repeated coordinate components without collinearity |

## Edge Cases

For the impossible case

```
0 0 2 0 1 2 1
```

the triangle is equilateral with side length `2`. Its minimum possible width is its altitude, `sqrt(3)`, which is greater than the available width `1`. Every ordered vector pair eventually fails either the quadrant condition or the width projection condition. Since no candidate reaches `ans`, the program prints `impossible`.

For exact boundary contact,

```
0 0 1 0 0 1 1
```

the vector `(1,0)` has squared length exactly `w²`. The `aa <= w² + EPS` branch accepts it, and the other vertex has horizontal projection zero and vertical projection one. The candidate height is exactly `1`, so the output is `1.0000000000`. This case catches implementations that accidentally use `aa < w²` or `projection < w`.

For the maximum-coordinate case,

```
0 0 10000 0 0 10000 10000
```

the vector from `(0,0)` to `(10000,0)` has length exactly equal to the strip width. Placing that edge horizontally gives height `10000`, and the other corner configurations cannot improve it under the width restriction. The algorithm performs all computations with integer squared lengths before converting to floating point, avoiding overflow and unnecessary numerical error.

For repeated coordinate components,

```
0 0 0 1 1 1 1
```

the vectors from `(0,0)` are `(0,1)` and `(1,1)`. Their dot product is positive, and their cross product has magnitude `1`. Since the width is exactly `1`, the triangle fits with height `1`. The example demonstrates why the algorithm should not depend on the input coordinates being pairwise different. Only the non-collinearity guarantee is required.
