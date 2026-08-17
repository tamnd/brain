---
title: "CF 102343H - Mountain View"
description: "The mountain outline is a piecewise linear function. The input gives its vertices from left to right as points (xi, yi), and between consecutive points the mountain is the straight line joining them. Outside the given range, the elevation is zero."
date: "2026-08-17T10:19:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "H"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 127
verified: true
draft: false
---

[CF 102343H - Mountain View](https://codeforces.com/problemset/problem/102343/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The mountain outline is a piecewise linear function. The input gives its vertices from left to right as points `(x_i, y_i)`, and between consecutive points the mountain is the straight line joining them. Outside the given range, the elevation is zero. A camera chooses a horizontal interval of fixed width `W`, namely `[x, x + W]`, and we want the largest possible average elevation inside that interval. Since every picture has the same width, maximizing the average is exactly the same as maximizing the area under the mountain inside the interval. The official constraints are `n <= 10^5`, `x_i <= 10^9`, `y_i <= 10^4`, and `W <= 10^9`.

The large value of `n` rules out algorithms that explicitly compare all pairs of mountain segments. An `O(n^2)` method would perform roughly `n(n-1)/2`, almost `5 * 10^9`, pair checks at `n = 10^5`, which is far beyond what a seven-second limit can support. The coordinates are also large, so discretizing the x-axis is not an option. We need to work directly with the continuous piecewise-linear function.

There are three boundary situations that commonly cause incorrect implementations. First, the best interval can start or finish exactly at a mountain vertex. For example, with `W = 1` and points `(0, 10), (1, 20)`, the interval `[0, 1]` has average `15`, so the correct output is `15.000000000`. An implementation that only searches strictly inside segments can miss the optimum.

Second, the best starting position does not have to be a mountain vertex or a shifted vertex. Consider

```
3 2
0 0
2 10
4 0
```

The interval `[1, 3]` has area `15`, hence average `7.5`. The correct output is `7.500000000`. A search that only checks positions `x_i` and `x_i-W` would inspect `0`, `2`, and `4`, and miss the true optimum at `x = 1`.

Third, part of the camera interval can lie outside the supplied mountain. For

```
2 10
0 10
1 20
```

the whole mountain is contained in `[0, 10]`. Its area is the triangle/trapezoid area `15`, so the answer is `1.500000000`. Treating the last input point as if the mountain continued with its final slope would produce a completely different answer. The statement explicitly defines the elevation outside the supplied landscape to be zero.

## Approaches

A direct brute-force approach can treat every segment of `y(x)` and every segment of the shifted function `y(x + W)` as a possible pair. Over an interval where both are fixed linear functions, their difference is linear, so the area function can be handled exactly with elementary calculus. The difficulty is that one segment of the first function can overlap many shifted segments of the second, and in the worst case there are `O(n^2)` such pairs. With `n = 10^5`, that means about `5 * 10^9` pair relationships, before even accounting for the arithmetic done for each one.

The key observation is that we never need to consider arbitrary pairs of segments. Define

`F(x) = integral from x to x+W of y(t) dt`.

The desired average is `F(x) / W`, and `W` is fixed, so maximizing the average means maximizing `F(x)`.

By the fundamental theorem of calculus,

`F'(x) = y(x + W) - y(x)`.

This changes the problem substantially. The only positions where the formula for `F'(x)` can change are positions where either `x` crosses an original mountain vertex or `x + W` crosses one. Those positions are exactly

`x_i` and `x_i - W`.

After sorting these event positions, every interval between two consecutive events has a very simple structure. Both `y(x)` and `y(x+W)` are linear there, so `F'(x)` is linear and `F(x)` is quadratic.

A quadratic on one interval has only two ways to attain its maximum. It can attain it at an endpoint, or, when the quadratic is concave, at its stationary point. Thus each event interval requires only its two endpoints and at most one interior candidate.

The area itself can be evaluated in constant time after building a prefix integral of the mountain. The event positions can be sorted in `O(n log n)`, and each event can locate the relevant mountain segment with binary search. This gives an `O(n log n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the piecewise-linear mountain and a prefix-area array. For every vertex `x_i`, store the area under the mountain from the first vertex up to `x_i`. This lets us compute the area under any interval `[a,b]` as `A(b) - A(a)`.
2. Define `F(x) = A(x + W) - A(x)`. This is exactly the area captured by a camera whose left edge is at `x`, so maximizing `F` solves the original problem.
3. Create all event positions `0`, every `x_i`, and every nonnegative `x_i - W`. The first group marks where `y(x)` changes its linear segment. The second shifted group marks where `y(x + W)` changes its segment. The position `0` is included because the camera starts on the nonnegative x-axis.
4. Sort and deduplicate the event positions. Between two consecutive events `[L,R]`, neither `y(x)` nor `y(x+W)` crosses a vertex, so both functions are linear throughout that interval.
5. Evaluate `F(L)` and `F(R)` for every event interval. Every global maximum that occurs at an event is now covered.
6. Inside the interval `[L,R]`, obtain the slope of `y(x)` and the slope of `y(x+W)` by evaluating both at the midpoint. Their difference is the slope of `F'(x)`. Since `F'(x)` is linear, its slope is constant over the whole interval.
7. If the slope of `F'` is negative, `F` is concave on `[L,R]`. Its stationary point is a possible interior maximum. Compute the zero of `F'(x)` and evaluate `F` there if it lies inside the interval. If the slope is nonnegative, `F` is linear or convex, so its maximum on the interval is already at an endpoint.
8. Keep the largest area found and divide it by `W` when printing the answer. Printing nine digits after the decimal point is sufficient for the required `10^-6` tolerance.

The invariant behind the algorithm is that every possible maximizer lies either at an event position or inside exactly one event interval. On each such interval, `F'(x)` is linear, so `F(x)` is quadratic. A quadratic has no other kind of local maximum. Consequently, checking the endpoints and the single stationary point when the quadratic is concave covers every possible global maximum.

## Python Solution

```python
import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.readline

    n, W = map(int, input().split())
    xs = [0] * n
    ys = [0] * n

    for i in range(n):
        xs[i], ys[i] = map(int, input().split())

    # pref[i] = area under the mountain from xs[0] to xs[i].
    pref = [0.0] * n
    for i in range(1, n):
        dx = xs[i] - xs[i - 1]
        pref[i] = pref[i - 1] + dx * (ys[i - 1] + ys[i]) * 0.5

    total_area = pref[-1]

    def area(t):
        """Integral of y from xs[0] to t."""
        if t <= xs[0]:
            return 0.0
        if t >= xs[-1]:
            return total_area

        i = bisect_right(xs, t) - 1
        dx = t - xs[i]
        slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])

        return pref[i] + ys[i] * dx + 0.5 * slope * dx * dx

    def value_slope(t):
        """Return y(t) and the slope of y at t."""
        if t < xs[0] or t > xs[-1]:
            return 0.0, 0.0

        if t == xs[-1]:
            return float(ys[-1]), 0.0

        i = bisect_right(xs, t) - 1
        dx = t - xs[i]
        slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
        value = ys[i] + slope * dx

        return value, slope

    # The derivative can change only when x or x + W
    # reaches an input vertex.
    events = {0}
    for x in xs:
        events.add(x)
        if x >= W:
            events.add(x - W)

    events = sorted(events)

    def captured_area(x):
        return area(x + W) - area(x)

    best = captured_area(0)

    for k in range(len(events) - 1):
        L = events[k]
        R = events[k + 1]

        if L == R:
            continue

        best = max(best, captured_area(L), captured_area(R))

        mid = (L + R) * 0.5

        y1, s1 = value_slope(mid)
        y2, s2 = value_slope(mid + W)

        # F'(x) = y(x + W) - y(x)
        # Its slope is s2 - s1.
        derivative_slope = s2 - s1

        derivative_at_mid = y2 - y1
        derivative_at_left = (
            derivative_at_mid
            + derivative_slope * (L - mid)
        )

        # F is concave exactly when F' is decreasing.
        if derivative_slope < 0.0:
            root = L - derivative_at_left / derivative_slope

            if L < root < R:
                best = max(best, captured_area(root))

    print(f"{best / W:.9f}")

if __name__ == "__main__":
    solve()
```

The prefix array stores trapezoid areas. Between consecutive vertices, the mountain has equation `y(x) = y_i + s(x-x_i)`, so the area over a partial segment is `y_i * dx + s * dx² / 2`. The `area` function combines that partial trapezoid with the already accumulated prefix area.

The `value_slope` function returns both the elevation and the slope at a coordinate. Outside the supplied mountain both are zero, which handles the required zero elevation beyond the endpoints. At the final vertex the right-hand slope is also zero because the landscape ends there.

The event set contains `x_i - W` only when it is nonnegative because the camera's left edge is restricted to the nonnegative x-axis. Including `x_i - W` is what captures changes caused by the right edge of the camera crossing a mountain vertex.

The midpoint is used to obtain the slopes inside an event interval. It cannot coincide with an event, so there is no ambiguity about which linear segment should be used. The derivative at the left endpoint is then obtained by moving from the midpoint along the constant derivative slope.

The expression

`root = L - derivative_at_left / derivative_slope`

comes directly from solving the linear equation `F'(x) = 0`. We only inspect this root when `F'` is decreasing, because only then is the corresponding stationary point a maximum rather than a minimum.

All coordinate and area calculations fit comfortably in Python's integer and floating-point representations. The largest possible area is on the order of `10^13`, while double precision provides substantially more than the accuracy needed for an absolute or relative error of `10^-6`.

## Worked Examples

### Sample 1

For

```
4 20
0 10
20 20
30 5
60 30
```

the event positions are `0, 10, 20, 30, 40, 60`. The relevant scan can be summarized as follows.

| Interval | Candidate type | Captured area | Average |
| --- | --- | --- | --- |
| `[0, 10]` | endpoints / stationary point | at most 400 | at most 20 |
| `[10, 20]` | endpoints / stationary point | at most 400 | at most 20 |
| `[20, 30]` | endpoints / stationary point | at most 400 | at most 20 |
| `[30, 40]` | endpoints / stationary point | at most 400 | at most 20 |
| `[40, 60]` | endpoint `x = 40` | `1300 / 3` | `65 / 3` |

The last interval contains the optimum. The camera covers `[40,60]`, where the mountain rises linearly from height `13.333...` to `30`. Its area is `433.333...`, and dividing by the width `20` gives `21.666666667`, matching the official sample.

### Sample 2

For

```
3 1
10 50
90 50
1000 49
```

the mountain is horizontal at height `50` for almost the entire useful region. The event positions relevant near the beginning and end include `0`, `10`, `89`, `90`, `999`, and `1000`.

| Interval | Camera region | Maximum relevant average |
| --- | --- | --- |
| `[0, 10]` | partly outside, then height 50 | below 50 |
| `[10, 89]` | entirely at height 50 | 50 |
| `[89, 90]` | entirely at height 50 | 50 |
| `[90, 999]` | begins to include the descending section | at most 50 |
| `[999, 1000]` | includes lower height | below 50 |

Any width-one interval lying entirely inside the horizontal section has average exactly `50`, so the answer is `50.000000000`. The example also demonstrates why a maximum does not have to occur at the final vertex.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | There are O(n) events, sorting costs O(n log n), and each event uses O(log n) binary searches. |
| Space | O(n) | The vertices, prefix areas, and event positions all use O(n) memory. |

With `n <= 10^5`, the algorithm performs only a logarithmic number of operations per event instead of billions of pairwise checks. The coordinate bounds do not affect the number of events, so the running time remains controlled even when the x-coordinates reach `10^9`. The official time limit is seven seconds and the memory limit is 256 MB.

## Test Cases

```python
# helper: run the submitted solution on an input string
import sys
import io
from bisect import bisect_right

def solve():
    input = sys.stdin.readline

    n, W = map(int, input().split())
    xs = [0] * n
    ys = [0] * n

    for i in range(n):
        xs[i], ys[i] = map(int, input().split())

    pref = [0.0] * n
    for i in range(1, n):
        dx = xs[i] - xs[i - 1]
        pref[i] = pref[i - 1] + dx * (ys[i - 1] + ys[i]) * 0.5

    total_area = pref[-1]

    def area(t):
        if t <= xs[0]:
            return 0.0
        if t >= xs[-1]:
            return total_area

        i = bisect_right(xs, t) - 1
        dx = t - xs[i]
        slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
        return pref[i] + ys[i] * dx + 0.5 * slope * dx * dx

    def value_slope(t):
        if t < xs[0] or t > xs[-1]:
            return 0.0, 0.0
        if t == xs[-1]:
            return float(ys[-1]), 0.0

        i = bisect_right(xs, t) - 1
        dx = t - xs[i]
        slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
        return ys[i] + slope * dx, slope

    events = {0}
    for x in xs:
        events.add(x)
        if x >= W:
            events.add(x - W)
    events = sorted(events)

    def captured(x):
        return area(x + W) - area(x)

    best = captured(0)

    for k in range(len(events) - 1):
        L, R = events[k], events[k + 1]

        best = max(best, captured(L), captured(R))

        mid = (L + R) * 0.5
        y1, s1 = value_slope(mid)
        y2, s2 = value_slope(mid + W)

        ds = s2 - s1
        dm = y2 - y1
        dL = dm + ds * (L - mid)

        if ds < 0.0:
            root = L - dL / ds
            if L < root < R:
                best = max(best, captured(root))

    print(f"{best / W:.9f}")

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
    """4 20
0 10
20 20
30 5
60 30
"""
) == "21.666666667\n"

# Provided sample 2
assert run(
    """3 1
10 50
90 50
1000 49
"""
) == "50.000000000\n"

# Minimum-size input.
assert run(
    """2 1
0 10
1 20
"""
) == "15.000000000\n"

# Interior stationary point, catches implementations that only inspect events.
assert run(
    """3 2
0 0
2 10
4 0
"""
) == "7.500000000\n"

# Camera width is much larger than the mountain.
assert run(
    """2 10
0 10
1 20
"""
) == "1.500000000\n"

# All equal values.
assert run(
    """4 3
0 7
5 7
10 7
15 7
"""
) == "7.000000000\n"

# Maximum-size input, generated compactly.
n = 100000
parts = [f"{n} 500"]
parts.extend(f"{i} 7" for i in range(n))
large_input = "\n".join(parts) + "\n"

assert run(large_input) == "7.000000000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 0 10 / 1 20` | `15.000000000` | Minimum input and endpoint optimum |
| `3 2 / 0 0 / 2 10 / 4 0` | `7.500000000` | Interior stationary point |
| `2 10 / 0 10 / 1 20` | `1.500000000` | Landscape ending before the camera interval |
| `4 3 / 0 7 / 5 7 / 10 7 / 15 7` | `7.000000000` | All-equal heights |
| `100000` equal-height vertices | `7.000000000` | Maximum `n` and asymptotic performance |

## Edge Cases

For the endpoint case

```
2 1
0 10
1 20
```

the event set is `{0, 1}`. The algorithm evaluates both camera positions. At `x = 0`, the captured area is the trapezoid with heights `10` and `20`, giving area `15` and average `15`. There is no missing interior maximum because the area function is quadratic only on event intervals, and here the relevant interval has no better stationary point.

For the interior maximum

```
3 2
0 0
2 10
4 0
```

the event set is `{0, 2, 4}`. On `[0,2]`, `y(x)` rises with slope `5`, while `y(x+2)` falls with slope `-5`. Hence `F'(x)` has slope `-10`. At `x = 0`, `F'(0) = 10`, and its zero is at `x = 1`. The algorithm evaluates that point and obtains area `15`, giving average `7.5`. This is precisely the case that defeats an algorithm checking only breakpoints.

For a camera wider than the landscape,

```
2 10
0 10
1 20
```

the event set contains `0` and `1`. After `x = 1`, the left edge is already beyond the mountain, so the captured area is zero. At `x = 0`, the camera covers the entire mountain and nine units of zero-height terrain. The area is `15`, so the average is `1.5`. The zero extension beyond the final point is handled directly by `area(t)`.

For equal heights,

```
4 3
0 7
5 7
10 7
15 7
```

both `y(x)` and `y(x+W)` have slope zero wherever the camera lies entirely over the mountain. Consequently `F'(x) = 0` and every such position is optimal. The algorithm does not need a special case for this. Since the derivative slope is also zero, it simply keeps the endpoint values, all of which have the same area.

For the maximum-size case, the generated input contains `100000` vertices and a constant elevation of `7`. Every camera position that stays inside the mountain captures exactly `7 * W` area, so the answer is exactly `7.000000000`. The event construction and binary searches remain `O(n log n)`, which is the intended scale for the official `n <= 10^5` constraint.
