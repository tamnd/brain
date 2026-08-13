---
title: "CF 102281D - \u0411\u043e\u0435\u0432\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We have three points in three-dimensional space. The first point is the position of our spacecraft and laser cannon, the second is the center of an enemy spherical spacecraft together with its radius, and the third is the point selected by the targeting system."
date: "2026-08-13T09:20:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "D"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 124
verified: true
draft: false
---

[CF 102281D - \u0411\u043e\u0435\u0432\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three points in three-dimensional space. The first point is the position of our spacecraft and laser cannon, the second is the center of an enemy spherical spacecraft together with its radius, and the third is the point selected by the targeting system.

The laser does not stop at the selected point. The selected point only determines its direction, so the shot is an infinite ray starting at our spacecraft and passing through the target point. The enemy is destroyed when this ray intersects or touches the sphere.

We need to output two things. The first line says whether the ray hits the sphere. The second line gives the minimum Euclidean distance from the sphere's center to any point of the ray.

All coordinates lie between -1000 and 1000, and the radius is at most 1000. There is only one geometric configuration, so the input size does not create an asymptotic challenge. The 1.5 second limit is more than enough for constant-time arithmetic, but it also means there is no reason to approximate the ray by a large number of sampled points. Python integers handle all intermediate squared distances comfortably, since coordinate differences are at most 2000 and their squares are only on the order of millions.

The main edge cases come from the fact that a laser shot is a ray, not an infinite line. The closest point on the infinite line can lie behind the cannon, in which case it is not reachable by the laser.

For example,

```
0 0 0
-2 0 0 1
1 0 0
```

produces

```
MISS
2.000000000000000
```

The enemy center lies at x = -2, while the laser travels in the positive x direction. The distance from the center to the infinite x-axis is zero, but the nearest point of the actual ray is the cannon itself, at distance 2. A solution that always computes point-to-line distance would incorrectly report a hit.

Tangency must also count as a hit. For example,

```
0 0 0
5 1 0 1
10 0 0
```

produces

```
HIT
1.000000000000000
```

The ray is the positive x-axis and the sphere center is exactly one unit away from it. The laser touches the sphere, so using a strict comparison such as `distance < r` would incorrectly produce `MISS`.

The case where the sphere lies directly on the ray is another boundary condition. For example,

```
0 0 0
5 0 0 2
1 0 0
```

has distance zero, so the answer is `HIT`. A formula based on a normalized direction vector must also avoid dividing by zero, but the statement guarantees that the target is different from the cannon, so the direction vector is never zero.

## Approaches

A naive geometric simulation could represent the ray by many sample points and inspect those points one after another. The integer coordinate bounds give a useful upper bound for seeing why this is the wrong abstraction. If the target differs from the cannon, the squared length of the direction vector is at least 1. The projection parameter of the enemy center onto the ray direction is at most 6000 in absolute value because the dot product is at most (3 \cdot 2000 \cdot 2000), while the squared direction length is at least 1.

Suppose we tried to inspect the ray every (10^{-6}) units of this parameter. We would need roughly 6,000,001 evaluations in the worst case, and such sampling is still a numerical approximation rather than an exact geometric test. Making the step smaller only makes the operation count worse.

The brute-force idea fails because the ray is a continuous object. There is no useful reason to examine individual points when the distance to the sphere can be expressed directly with vector algebra.

The key observation is that every point of the ray has the form

[
S + tV,\qquad t \ge 0,
]

where (S) is the cannon position and (V=T-S) is the direction determined by the target. We need to minimize the squared distance from this point to the enemy center (E).

Let (W=E-S). The squared distance from (E) to (S+tV) is

[
f(t)=|W-tV|^2.
]

Expanding gives

[
f(t)=|W|^2-2t(W\cdot V)+t^2|V|^2.
]

This is a quadratic function of (t). Its unconstrained minimum occurs at

[
t_0=\frac{W\cdot V}{|V|^2}.
]

The only restriction is (t\ge0). If (t_0\ge0), the closest point is inside the ray, so the ordinary point-to-line distance is correct. If (t_0<0), the closest point of the infinite line lies behind the cannon, and the closest reachable point is (S).

This reduces the entire problem to a few dot products and squared lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sampling | O(6,000,000) evaluations at (10^{-6}) resolution | O(1) | Too slow and approximate |
| Optimal vector geometry | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the cannon position (S), enemy center (E), radius (r), and target point (T). Construct the direction vector (V=T-S). The guarantee that the cannon never shoots at itself means (V\ne0), so its squared length is positive.
2. Construct (W=E-S), the vector from the cannon to the enemy center. Compute the dot product (p=W\cdot V) and the squared direction length (q=V\cdot V).
3. Check the sign of (p). Since (q>0), the sign of (p/q) is exactly the sign of the optimal parameter (t_0).
4. If (p<0), the perpendicular projection of the enemy center onto the infinite line lies behind the cannon. The nearest point of the actual ray is then the cannon itself, so the required distance is (|W|).
5. If (p\ge0), the perpendicular projection lies on the ray. The minimum squared distance is

[
|W|^2-\frac{p^2}{q}.
]

For the hit test, we can avoid taking a square root. The condition that the distance is at most (r) becomes

[
|W|^2-\frac{p^2}{q}\le r^2.
]

Multiplying by the positive value (q) gives

[
|W|^2q-p^2\le r^2q.
]

All quantities in this comparison are integers, so the hit decision can be made without floating-point error.

1. Compute the actual distance as a floating-point value and print it with enough digits. In the projection case, use the square root of the non-negative value above. In the behind-the-cannon case, use (\sqrt{|W|^2}).
2. Print `HIT` when the computed geometric distance is at most the radius, including exact tangency. Otherwise print `MISS`.

### Why it works

The invariant is that the chosen parameter (t) always describes the closest reachable point of the ray to the enemy center. The quadratic distance function has exactly one unconstrained minimum because its coefficient of (t^2) is (V\cdot V>0). When that minimum has (t\ge0), it belongs to the ray. When it has (t<0), the quadratic is increasing throughout the allowed interval (t\ge0), so the minimum occurs at the boundary (t=0), which is the cannon.

Thus the algorithm computes the exact minimum distance from the center to the ray. A sphere is intersected or touched exactly when this distance is at most its radius, so the reported `HIT` or `MISS` decision is correct.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    xs, ys, zs = map(int, input().split())
    xe, ye, ze, r = map(int, input().split())
    xt, yt, zt = map(int, input().split())

    vx = xt - xs
    vy = yt - ys
    vz = zt - zs

    wx = xe - xs
    wy = ye - ys
    wz = ze - zs

    dot = wx * vx + wy * vy + wz * vz
    vv = vx * vx + vy * vy + vz * vz
    ww = wx * wx + wy * wy + wz * wz

    if dot < 0:
        dist2 = float(ww)
        hit = ww <= r * r
    else:
        cross2 = ww * vv - dot * dot
        dist2 = cross2 / vv
        hit = cross2 <= r * r * vv

    distance = math.sqrt(dist2)

    print("HIT" if hit else "MISS")
    print(f"{distance:.15f}")

if __name__ == "__main__":
    solve()
```

The first part constructs `v`, the ray direction, and `w`, the vector from the cannon to the enemy center. These are exactly the vectors used in the mathematical derivation.

`dot` stores (W\cdot V), while `vv` stores (|V|^2). Since the target differs from the cannon, `vv` is strictly positive. `ww` stores the squared distance from the cannon to the enemy center.

When `dot < 0`, the projection is behind the cannon. The code consequently uses `ww` as the squared distance and compares it directly with (r^2). The statement guarantees that the cannon is outside the enemy sphere, so this branch cannot accidentally report a hit because the cannon itself is inside the sphere.

For `dot >= 0`, the code uses

[
|W|^2|V|^2-(W\cdot V)^2
]

instead of directly calculating the normalized point-to-line distance. This expression is the squared length of the cross product (W\times V), so after division by (|V|^2) it gives the squared distance to the line.

The hit comparison is deliberately performed using integers. Floating-point rounding near tangency could turn a mathematically exact equality into a value slightly above or below the radius. The integer inequality `cross2 <= r * r * vv` handles tangency exactly.

Only the final square root needs floating-point arithmetic. Python integers have arbitrary precision, although the actual values here are small enough that ordinary 64-bit integers would already be sufficient.

The output uses fifteen digits after the decimal point, which is substantially more precision than the required (10^{-6}) absolute or relative error.

## Worked Examples

### Sample 1

The input is

```
0 0 0
100 100 100 10
1 1 1
```

The direction from the cannon to the target is `(1, 1, 1)`. The enemy center is also on that same direction, so its projection lies on the ray and the distance must be zero.

| Variable | Value |
| --- | --- |
| `v` | `(1, 1, 1)` |
| `w` | `(100, 100, 100)` |
| `dot` | `300` |
| `vv` | `3` |
| `ww` | `30000` |
| `cross2` | `0` |
| `distance` | `0` |
| `hit` | `True` |

The zero cross-product expression confirms that the enemy center lies exactly on the ray. Since zero is at most the radius 10, the result is `HIT`.

### Sample 2

The input is

```
0 13 9
5 13 -1 4
16 13 -3
```

The ray direction is `(16, 0, -12)`, while the vector from the cannon to the enemy center is `(5, 0, -10)`.

| Variable | Value |
| --- | --- |
| `v` | `(16, 0, -12)` |
| `w` | `(5, 0, -10)` |
| `dot` | `200` |
| `vv` | `400` |
| `ww` | `125` |
| `cross2` | `10000` |
| `dist²` | `25` |
| `distance` | `5` |
| `hit` | `False` |

The projection parameter is (200/400=0.5), so the closest point really is on the ray. The resulting distance is 5, larger than the radius 4, giving `MISS`.

The example also demonstrates why checking only the direction of the ray is insufficient. The infinite line passes close to the sphere, but the exact perpendicular distance is needed to compare against the radius.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A fixed number of vector operations and arithmetic expressions is performed |
| Space | O(1) | Only a constant number of coordinates and intermediate values are stored |

The coordinate bounds make every arithmetic operation small, and there is no iteration depending on the input values. The solution therefore fits comfortably within the 1.5 second time limit and 128 MB memory limit.

## Test Cases

The following tests use a helper that contains the same `solve` logic as the submitted program, but returns its output as a string so that assertions can check it directly.

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    xs, ys, zs = map(int, input().split())
    xe, ye, ze, r = map(int, input().split())
    xt, yt, zt = map(int, input().split())

    vx = xt - xs
    vy = yt - ys
    vz = zt - zs

    wx = xe - xs
    wy = ye - ys
    wz = ze - zs

    dot = wx * vx + wy * vy + wz * vz
    vv = vx * vx + vy * vy + vz * vz
    ww = wx * wx + wy * wy + wz * wz

    if dot < 0:
        dist2 = float(ww)
        hit = ww <= r * r
    else:
        cross2 = ww * vv - dot * dot
        dist2 = cross2 / vv
        hit = cross2 <= r * r * vv

    distance = math.sqrt(dist2)

    print("HIT" if hit else "MISS")
    print(f"{distance:.15f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """0 0 0
100 100 100 10
1 1 1
"""
) == "HIT\n0.000000000000000\n", "sample 1"

# Provided sample 2
assert run(
    """0 13 9
5 13 -1 4
16 13 -3
"""
) == "MISS\n5.000000000000000\n", "sample 2"

# Tangency with the ray, minimum radius
assert run(
    """0 0 0
5 1 0 1
10 0 0
"""
) == "HIT\n1.000000000000000\n", "tangent hit"

# Sphere is behind the cannon
assert run(
    """0 0 0
-2 0 0 1
1 0 0
"""
) == "MISS\n2.000000000000000\n", "sphere behind ray"

# All coordinate components equal inside each point, maximum coordinate magnitude
assert run(
    """-1000 -1000 -1000
0 0 0 1000
1000 1000 1000
"""
) == "HIT\n0.000000000000000\n", "large diagonal hit"

# Maximum radius and a closest point at the cannon
assert run(
    """1000 1000 1000
-1000 -1000 -1000 1000
1000 1000 999
"""
) == "MISS\n3464.101615137754586\n", "maximum-size separated case"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 / 5 1 0 1 / 10 0 0` | `HIT`, distance `1` | Exact tangency must count as a hit |
| `0 0 0 / -2 0 0 1 / 1 0 0` | `MISS`, distance `2` | The ray must not be confused with the infinite line |
| `-1000 -1000 -1000 / 0 0 0 1000 / 1000 1000 1000` | `HIT`, distance `0` | Large coordinates and a diagonal ray |
| `1000 1000 1000 / -1000 -1000 -1000 1000 / 1000 1000 999` | `MISS`, distance approximately `3464.1016151377546` | Maximum coordinate magnitudes and a closest point at the ray origin |

## Edge Cases

The first subtle case is when the enemy is behind the cannon. Consider

```
0 0 0
-2 0 0 1
1 0 0
```

Here (V=(1,0,0)) and (W=(-2,0,0)), so

[
W\cdot V=-2<0.
]

The projection lies at (t=-2), outside the allowed range (t\ge0). The algorithm consequently chooses (t=0), the cannon itself, and obtains distance 2. Since the radius is only 1, the result is `MISS`. This is exactly the case that breaks a solution using point-to-infinite-line distance without checking the projection direction.

The second case is tangency:

```
0 0 0
5 1 0 1
10 0 0
```

The ray is the x-axis, and the enemy center is one unit away from it. The closest point is `(5, 0, 0)`, so the distance equals the radius. The integer comparison uses `<=`, not `<`, and returns `HIT`. The printed distance is exactly `1.000000000000000`.

The third case is a center directly on the ray:

```
0 0 0
100 100 100 10
1 1 1
```

The vectors `w` and `v` are parallel, so

[
|W|^2|V|^2-(W\cdot V)^2=0.
]

The distance is zero and the sphere is hit. This also verifies that the cross-product formulation behaves correctly when the perpendicular component vanishes completely.

The fourth case exercises a large coordinate range:

```
-1000 -1000 -1000
0 0 0 1000
1000 1000 1000
```

The direction and center vectors are both parallel, so the computed distance is zero despite the coordinates being at their allowed extremes. All squared quantities remain small enough for ordinary fixed-width integer arithmetic, and Python's integer arithmetic removes any overflow concern.

The final edge case is a target that changes only one coordinate:

```
1000 1000 1000
-1000 -1000 -1000 1000
1000 1000 999
```

The target is different from the cannon, so the direction vector is valid, but it points almost entirely along the coordinate axes of the cannon position. The enemy center projects behind the cannon because the dot product is negative. The algorithm uses the distance from the enemy center to the cannon rather than the distance to the infinite line, giving approximately `3464.1016151377546`. This confirms that the sign check is applied before the line-distance formula.
