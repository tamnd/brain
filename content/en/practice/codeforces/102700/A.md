---
title: "CF 102700A - Approach"
description: "There are two friends moving simultaneously on the plane. The first starts at point (A) and walks straight toward (B). The second starts at (C) and walks straight toward (D)."
date: "2026-08-08T08:09:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "A"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 228
verified: true
draft: false
---

[CF 102700A - Approach](https://codeforces.com/problemset/problem/102700/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two friends moving simultaneously on the plane. The first starts at point (A) and walks straight toward (B). The second starts at (C) and walks straight toward (D). Their speeds are equal, so if we choose the common speed to be (1), the time needed by each friend is exactly the length of their own route. Once a friend reaches the destination, that friend stops there.

The input contains the four coordinates of (A) and (B) on the first line, followed by the four coordinates of (C) and (D) on the second line. The required output is the smallest Euclidean distance between the two friends at any time from their simultaneous departure until both have reached their destinations.

The coordinates can have absolute value up to (10^9). This makes squared distances as large as about (10^{18}), so the implementation needs arithmetic that can safely represent such values. Python integers have arbitrary precision, and floating point is only needed when we compute the actual minimizing time or the final square root. Since there are only four points and no parameter depending on the input size, the intended solution should take constant time.

A common mistake is to compare only the initial and final distances. For example,

```
0 0 10 0
5 5 5 -5
```

The initial distance is (5\sqrt{2}), while the final distance is also (5\sqrt{2}), but the friends get closer while moving. At time (5), the first friend is at ((5,0)) and the second is at ((5,0)), so the correct answer is (0). Checking only the endpoints would miss the actual minimum.

Another edge case occurs when one friend arrives earlier. For example,

```
0 0 1 0
2 0 2 10
```

The first friend reaches ((1,0)) after one unit of time and then stays there. The second friend continues moving for ten units. The minimum distance is (1), attained at the moment the first friend reaches the destination. Treating both trajectories as if they continued indefinitely would consider positions that the first friend never actually occupies and can produce an invalid answer.

A third case is when the relative velocity is zero during a time interval. For example,

```
0 0 10 0
0 1 10 1
```

The friends move in parallel with exactly the same velocity, so their distance is always (1). A formula that divides by the squared relative velocity without checking whether it is zero would divide by zero even though the problem itself is completely well-defined.

Finally, the minimum can occur exactly when one friend reaches the destination. For example,

```
0 0 2 0
1 1 1 -1
```

At time (1), the second friend reaches ((1,-1)), while the first friend is at ((1,0)), giving distance (1). Since the relevant interval is closed at the arrival time, the implementation must allow the minimizing time to equal either endpoint.

## Approaches

A direct approach is to simulate the movement in very small time increments, calculate both positions at every increment, and keep the smallest distance found. This is conceptually easy because the actual trajectories are just two line segments followed by stationary points. The problem is that there is no meaningful fixed simulation step. With coordinates up to (10^9), a route can have length on the order of (10^9), so even a simulation using one million or one billion time samples would either be too inaccurate or far too slow. More importantly, a numerical simulation can skip the exact moment when the minimum occurs, so it cannot provide the required (10^{-6}) precision reliably.

The brute force can instead sample (K) points on each trajectory. That costs (O(K)) distance evaluations, but (K) must be chosen large enough to guarantee the requested precision for every possible coordinate configuration. Since the minimum can occur in an arbitrarily narrow region when coordinates are large, no practical fixed (K) gives such a guarantee.

The key observation is that the motion is piecewise linear in time. Before either friend reaches a destination, both positions are linear functions of time. After one friend arrives, that friend's position becomes constant while the other position is still linear. After both arrive, both positions are constant.

Consider any interval of time where the two positions can be written as

[
P_1(t)=P+tV_1
]

and

[
P_2(t)=Q+tV_2.
]

Their relative position is then

[
R(t)=(P-Q)+t(V_1-V_2).
]

So on that interval, the squared distance is

[
f(t)=|R(t)|^2.
]

This is a quadratic function of (t). A quadratic of the form

[
at^2+bt+c
]

with (a\geq0) reaches its minimum either at its vertex or at an endpoint of the interval. We can calculate the vertex directly instead of sampling time.

There are only three possible movement phases. Before the first arrival, both friends move. Between the first and second arrival, one moves while the other is stationary. After the second arrival, neither moves, so the distance is constant. We can process these intervals independently and take the smallest distance.

The brute-force method works because every sampled time gives a valid pair of positions, but it fails because it has no finite sampling density that guarantees the required precision. The observation that each phase has linear relative motion reduces the entire problem to minimizing at most three one-dimensional convex quadratics, which takes constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | (O(K)) | (O(1)) | Too slow and not guaranteed accurate |
| Optimal piecewise quadratic minimization | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the four points and compute the movement vectors (B-A) and (D-C). Their lengths are the total travel times because both friends have common speed (1).
2. Represent each friend's position at time (t) using a velocity vector. Before arrival, the velocity is the normalized direction toward the destination. After arrival, the velocity is zero.

Normalizing is convenient because equal physical speeds mean both velocity vectors must have magnitude (1), regardless of how long their respective paths are.
3. Let (T_1=|B-A|) and (T_2=|D-C|). Split the timeline at (0), (\min(T_1,T_2)), and (\max(T_1,T_2)). On each resulting interval, the velocity of each friend is fixed.
4. For one interval ([L,R]), write the relative position as

[
X(t)=X_0+tV,
]

where (X_0) is the relative position at time zero and (V) is the relative velocity.

The squared distance is

[
|X_0+tV|^2.
]

Expanding it gives

[
|V|^2t^2+2(X_0\cdot V)t+|X_0|^2.
]
5. If (V\neq0), differentiate the quadratic. Its unconstrained minimum occurs at

[
t^*=-\frac{X_0\cdot V}{|V|^2}.
]

Since we are only allowed to use times inside ([L,R]), clamp this value to that interval. The candidate time is

[
\max(L,\min(R,t^*)).
]

Clamping handles the case where the quadratic keeps decreasing until one friend reaches a destination.
6. If (V=0), the relative position does not change throughout the interval, so every time has the same distance. We can simply evaluate one endpoint.
7. Evaluate the minimum on all movement phases and take the smallest squared distance. Finally, take its square root and print it with sufficient precision.

### Why it works

The invariant is that, on every processed time interval, the two position formulas exactly describe where the friends are at every time in that interval. Their relative position is linear in time, so their squared distance is a convex quadratic. The minimum of a convex quadratic over a closed interval is its vertex when the vertex lies inside the interval, otherwise one of the interval endpoints. The clamping step checks exactly that point. Since the complete timeline is partitioned at every moment when a friend's velocity changes, every possible time is covered by one of these intervals. Taking the smallest candidate over all intervals therefore gives the global minimum distance.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def norm(a):
    return math.hypot(a[0], a[1])

def position_at(p, v, t):
    return (p[0] + v[0] * t, p[1] + v[1] * t)

def solve():
    ax, ay, bx, by = map(int, input().split())
    cx, cy, dx, dy = map(int, input().split())

    a = (float(ax), float(ay))
    b = (float(bx), float(by))
    c = (float(cx), float(cy))
    d = (float(dx), float(dy))

    ab = (b[0] - a[0], b[1] - a[1])
    cd = (d[0] - c[0], d[1] - c[1])

    t1 = norm(ab)
    t2 = norm(cd)

    if t1 > 0:
        v1 = (ab[0] / t1, ab[1] / t1)
    else:
        v1 = (0.0, 0.0)

    if t2 > 0:
        v2 = (cd[0] / t2, cd[1] / t2)
    else:
        v2 = (0.0, 0.0)

    def state(t):
        if t < t1:
            p1 = position_at(a, v1, t)
        else:
            p1 = b

        if t < t2:
            p2 = position_at(c, v2, t)
        else:
            p2 = d

        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
        )

    def distance_sq(t):
        r = state(t)
        return r[0] * r[0] + r[1] * r[1]

    # The only times where velocities can change are the arrival times.
    cuts = sorted(set([0.0, t1, t2]))

    ans = float("inf")

    # Before the first arrival, both move.
    # Between arrival times, one may be stationary.
    # The final interval is constant, but processing it is harmless.
    for i in range(len(cuts)):
        if i + 1 < len(cuts):
            l = cuts[i]
            r = cuts[i + 1]
        else:
            # There is no need to search after both have arrived.
            continue

        mid = (l + r) * 0.5

        if mid < t1:
            vv1 = v1
        else:
            vv1 = (0.0, 0.0)

        if mid < t2:
            vv2 = v2
        else:
            vv2 = (0.0, 0.0)

        rel_v = (vv1[0] - vv2[0], vv1[1] - vv2[1])

        rel_l = state(l)

        vv2_norm_sq = dot(rel_v, rel_v)

        if vv2_norm_sq == 0.0:
            candidate = l
        else:
            optimum = -dot(rel_l, rel_v) / vv2_norm_sq
            candidate = max(l, min(r, optimum))

        ans = min(ans, distance_sq(candidate))

    # Both friends are stationary from max(t1, t2) onward.
    ans = min(ans, distance_sq(max(t1, t2)))

    print(f"{math.sqrt(ans):.12f}")

if __name__ == "__main__":
    solve()
```

The first part of the implementation computes the two route lengths and converts each route into a unit velocity vector. This follows directly from choosing the common walking speed as (1). If a route has zero length, the corresponding friend is already at the destination, so its velocity is set to zero rather than attempting to divide by a zero length.

The `state` function implements the piecewise motion. The comparison with the arrival time determines whether a friend is still moving or has already reached the destination. The endpoint itself is handled as a destination position, which is mathematically identical to the moving formula at that exact time.

The `cuts` array contains every time when the velocity can change. There are at most three distinct times, so the loop performs only a constant number of iterations. For each interval, the midpoint is used only to determine which velocity is active throughout that open interval. The midpoint is not a numerical approximation to the answer.

`rel_l` is the relative position at the left endpoint of the interval. Since relative velocity is constant throughout the interval, the relative position at any time (t) in the interval is

[
\text{rel}_l+(t-L)\text{rel}_v.
]

The code instead uses an equivalent global-time expression when deriving the vertex. Because `rel_l` is evaluated at time (L), the exact vertex in terms of the global time should be

[
L-\frac{\text{rel}_l\cdot\text{rel}_v}{|\text{rel}_v|^2}.
]

Thus the implementation should use that form. The complete corrected implementation is below.

```python
import sys
import math

input = sys.stdin.readline

def solve():
    ax, ay, bx, by = map(int, input().split())
    cx, cy, dx, dy = map(int, input().split())

    a = (float(ax), float(ay))
    b = (float(bx), float(by))
    c = (float(cx), float(cy))
    d = (float(dx), float(dy))

    ab = (b[0] - a[0], b[1] - a[1])
    cd = (d[0] - c[0], d[1] - c[1])

    t1 = math.hypot(ab[0], ab[1])
    t2 = math.hypot(cd[0], cd[1])

    v1 = (0.0, 0.0) if t1 == 0.0 else (ab[0] / t1, ab[1] / t1)
    v2 = (0.0, 0.0) if t2 == 0.0 else (cd[0] / t2, cd[1] / t2)

    def position(p, v, t, total, destination):
        if t >= total:
            return destination
        return (p[0] + v[0] * t, p[1] + v[1] * t)

    def relative_position(t):
        p1 = position(a, v1, t, t1, b)
        p2 = position(c, v2, t, t2, d)
        return (p1[0] - p2[0], p1[1] - p2[1])

    def dist_sq(t):
        x, y = relative_position(t)
        return x * x + y * y

    cuts = sorted(set((0.0, t1, t2)))
    ans = float("inf")

    for i in range(len(cuts) - 1):
        l = cuts[i]
        r = cuts[i + 1]

        mid = (l + r) * 0.5

        active_v1 = v1 if mid < t1 else (0.0, 0.0)
        active_v2 = v2 if mid < t2 else (0.0, 0.0)

        rv = (
            active_v1[0] - active_v2[0],
            active_v1[1] - active_v2[1],
        )

        rel_l = relative_position(l)

        rv_sq = rv[0] * rv[0] + rv[1] * rv[1]

        if rv_sq == 0.0:
            best_t = l
        else:
            # rel(t) = rel_l + (t-l) * rv
            # Minimize |rel(t)|^2.
            tau = -(rel_l[0] * rv[0] + rel_l[1] * rv[1]) / rv_sq
            best_t = max(l, min(r, l + tau))

        ans = min(ans, dist_sq(best_t))

    ans = min(ans, dist_sq(max(t1, t2)))

    print(f"{math.sqrt(ans):.12f}")

if __name__ == "__main__":
    solve()
```

The second version is the one to submit. The distinction between `tau` and `best_t` is a useful implementation detail. `tau` measures time relative to the beginning of the current interval, while `best_t` is the actual global time. Mixing these two coordinate systems is a typical source of an incorrect minimizer.

No integer overflow occurs in Python because integers have arbitrary precision. Coordinates are converted to floating point before velocity normalization, since the normalized vectors and route lengths require real arithmetic. The final error tolerance of (10^{-6}) is comfortably handled by printing twelve digits after the decimal point.

## Worked Examples

### Sample 1

The input is

```
0 0 1 0
2 0 2 1
```

The first friend travels one unit horizontally, so (T_1=1). The second travels one unit vertically, so (T_2=1). Both therefore move throughout the same interval ([0,1]).

The velocities are ((1,0)) and ((0,1)), so the relative velocity is ((1,-1)). The initial relative position is ((-2,0)).

| Interval | Relative position at left | Relative velocity | Unclamped relative time | Chosen time | Distance |
| --- | --- | --- | --- | --- | --- |
| ([0,1]) | ((-2,0)) | ((1,-1)) | (1) | (1) | (\sqrt{2}) |

At time (1), the friends are at ((1,0)) and ((2,1)), respectively. Their difference is ((-1,-1)), whose length is (\sqrt{2}). The output is consequently approximately (1.414213562373).

This example demonstrates the ordinary case where both friends move for the entire relevant interval and the quadratic minimum occurs exactly at the interval boundary.

### Sample 2

The input is

```
-2 -4 -2 -2
-3 -5 -3 -2
```

Both friends move vertically upward. The first route has length (2), while the second has length (3). Their velocities are both ((0,1)), so their relative velocity is zero during the first two units of time.

| Interval | Relative position at left | Relative velocity | Chosen time | Distance |
| --- | --- | --- | --- | --- |
| ([0,2]) | ((1,1)) | ((0,0)) | (0) | (\sqrt{2}) |
| ([2,3]) | ((1,1)) | ((0,-1)) | (3) | (1) |

During the first interval, both friends move together, so their separation remains (\sqrt{2}). At time (2), the first friend stops at ((-2,-2)), while the second is at ((-3,-3)). The second continues upward, reaching ((-3,-2)) at time (3), when the distance becomes (1). The answer is therefore (1).

This trace specifically confirms that zero relative velocity must be handled without division and that the minimum may occur after one friend has already stopped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | There are at most three distinct timeline boundaries and two movement intervals to minimize. |
| Space | (O(1)) | Only a constant number of points, vectors, and scalar values are stored. |

The coordinate bound does not affect the number of operations because the algorithm never samples the coordinate plane or time axis. Even though coordinates can be as large as (10^9), only a constant number of arithmetic operations are performed, so the solution easily fits within the one-second time limit and 512 MB memory limit.

## Test Cases

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    ax, ay, bx, by = map(int, input().split())
    cx, cy, dx, dy = map(int, input().split())

    a = (float(ax), float(ay))
    b = (float(bx), float(by))
    c = (float(cx), float(cy))
    d = (float(dx), float(dy))

    ab = (b[0] - a[0], b[1] - a[1])
    cd = (d[0] - c[0], d[1] - c[1])

    t1 = math.hypot(ab[0], ab[1])
    t2 = math.hypot(cd[0], cd[1])

    v1 = (0.0, 0.0) if t1 == 0 else (ab[0] / t1, ab[1] / t1)
    v2 = (0.0, 0.0) if t2 == 0 else (cd[0] / t2, cd[1] / t2)

    def position(p, v, t, total, destination):
        if t >= total:
            return destination
        return (p[0] + v[0] * t, p[1] + v[1] * t)

    def relative_position(t):
        p1 = position(a, v1, t, t1, b)
        p2 = position(c, v2, t, t2, d)
        return p1[0] - p2[0], p1[1] - p2[1]

    def dist_sq(t):
        x, y = relative_position(t)
        return x * x + y * y

    cuts = sorted(set((0.0, t1, t2)))
    ans = float("inf")

    for i in range(len(cuts) - 1):
        l, r = cuts[i], cuts[i + 1]
        mid = (l + r) * 0.5

        active_v1 = v1 if mid < t1 else (0.0, 0.0)
        active_v2 = v2 if mid < t2 else (0.0, 0.0)

        rv = (
            active_v1[0] - active_v2[0],
            active_v1[1] - active_v2[1],
        )

        rel_l = relative_position(l)
        rv_sq = rv[0] * rv[0] + rv[1] * rv[1]

        if rv_sq == 0.0:
            best_t = l
        else:
            tau = -(rel_l[0] * rv[0] + rel_l[1] * rv[1]) / rv_sq
            best_t = max(l, min(r, l + tau))

        ans = min(ans, dist_sq(best_t))

    ans = min(ans, dist_sq(max(t1, t2)))

    print(f"{math.sqrt(ans):.12f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def assert_close(actual: str, expected: float, message: str):
    value = float(actual)
    assert abs(value - expected) <= 1e-6, (
        f"{message}: got {value}, expected {expected}"
    )

# Provided sample 1.
assert_close(
    run("0 0 1 0\n2 0 2 1\n"),
    math.sqrt(2),
    "sample 1"
)

# Provided sample 2.
assert_close(
    run("-2 -4 -2 -2\n-3 -5 -3 -2\n"),
    1.0,
    "sample 2"
)

# Both friends start and finish at the same places.
assert_close(
    run("0 0 0 0\n0 0 0 0\n"),
    0.0,
    "both stationary at the same point"
)

# Both move with exactly the same velocity, so the distance never changes.
assert_close(
    run("0 0 10 0\n0 1 10 1\n"),
    1.0,
    "parallel identical motion"
)

# The friends meet exactly when the first friend reaches the destination.
assert_close(
    run("0 0 10 0\n5 5 5 -5\n"),
    0.0,
    "minimum exactly at an arrival boundary"
)

# One friend is already at its destination while the other moves.
assert_close(
    run("0 0 0 0\n2 0 2 10\n"),
    2.0,
    "zero-length first route"
)

# Large coordinates, checking arithmetic and precision.
assert_close(
    run("1000000000 1000000000 -1000000000 1000000000\n"
        "1000000000 1000000001 -1000000000 1000000001\n"),
    1.0,
    "large coordinates"
)

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0` and `0 0 0 0` | `0` | Both friends are stationary at the same location. |
| `0 0 10 0` and `0 1 10 1` | `1` | Relative velocity is zero, so there is no division by zero. |
| `0 0 10 0` and `5 5 5 -5` | `0` | The minimum occurs exactly at a phase boundary. |
| `0 0 0 0` and `2 0 2 10` | `2` | One route has zero length and the corresponding friend is stationary from the start. |
| Coordinates of magnitude (10^9) | `1` | Large coordinates and floating-point precision. |

## Edge Cases

### The friends meet at an arrival boundary

Consider

```
0 0 10 0
5 5 5 -5
```

Both routes take (10) units of time. At (t=5), the first friend is at ((5,0)), while the second is also at ((5,0)). The relative position is exactly zero, so the answer is (0).

The interval minimization computes the unconstrained quadratic minimum at (t=5). Since (5) lies inside the closed interval ([0,10]), it is accepted directly. This catches implementations that check only strictly interior points or only the final positions.

### One friend arrives before the other

Consider

```
0 0 1 0
2 0 2 10
```

The first friend reaches ((1,0)) at (t=1) and stays there. The second friend moves upward from ((2,0)). During the second phase, the relative position is determined by the stationary first friend and the moving second friend. The closest point is at (t=1), with distance (1).

The timeline is split at (t=1), so the algorithm does not accidentally continue the first friend's velocity after arrival.

### Relative velocity is zero

Consider

```
0 0 10 0
0 1 10 1
```

Both friends have velocity ((1,0)). Their relative velocity is ((0,0)), and their relative position is always ((0,-1)). The distance is consequently always (1).

The algorithm detects that the squared relative velocity is zero and skips the vertex formula. Any point in the interval is optimal, so evaluating the left endpoint is sufficient.

### A friend is stationary from the beginning

Consider

```
0 0 0 0
2 0 2 10
```

The first friend has a zero-length route and never moves. The second starts at distance (2) from the first and moves vertically, so the minimum distance is (2) at (t=0).

The route-length check creates a zero velocity for the first friend. The second friend's motion is then handled normally, with the first friend treated as stationary throughout the relevant interval.

### The minimum is at an interval endpoint

Suppose the quadratic distance function decreases throughout an interval and would reach its vertex after the interval ends. That vertex corresponds to a time when one of the friends has already changed velocity, so it cannot be used for that phase.

The clamping operation changes an out-of-range vertex into either (L) or (R). Since every velocity-change time is explicitly included in `cuts`, the correct endpoint is still evaluated as part of the adjacent phase. This prevents the common error of accepting a mathematically valid quadratic minimum at a time when the assumed velocities are no longer valid.
