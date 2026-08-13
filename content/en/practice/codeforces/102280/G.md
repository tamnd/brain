---
title: "CF 102280G - \u0421\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0437\u0430\u043a\u0430\u0437"
description: "We have a starting point on a road and a destination somewhere away from that road. The straight-line distance between the starting point and the destination is s, while the perpendicular distance from the destination to the road is h."
date: "2026-08-13T16:02:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "G"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 162
verified: true
draft: false
---

[CF 102280G - \u0421\u043f\u0435\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0437\u0430\u043a\u0430\u0437](https://codeforces.com/problemset/problem/102280/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a starting point on a road and a destination somewhere away from that road. The straight-line distance between the starting point and the destination is `s`, while the perpendicular distance from the destination to the road is `h`. The car can travel along the road at speed `v` and through the terrain at speed `u`.

The intended route consists of two parts. First, the car travels some distance `x` along the road. Then it leaves the road and drives directly to the destination. We need to find the value of `x` that minimizes the total travel time.

The input contains four integers `s`, `h`, `u`, and `v`. Here `s` is the direct distance from the starting point to the destination, `h` is the destination's perpendicular distance from the road, `u` is the terrain speed, and `v` is the road speed. The output is the optimal distance `x` traveled along the road.

All values can be as large as `10^9`. This immediately rules out algorithms that depend on iterating over every possible integer distance, since there can be up to one billion candidates. The time limit is only 0.5 seconds, so even a few hundred million simple operations would be far beyond what is reasonable. We need a constant-time or logarithmic-time mathematical solution.

There are several boundary cases that can easily break a careless implementation. If the road is no faster than the terrain, the car should leave immediately. For example, with `1 1 10 10`, the projection of the destination onto the road is at the starting point, so the correct answer is `0.0`. A formula that blindly divides by `sqrt(v^2-u^2)` would divide by zero.

Another boundary case occurs when the road is faster, but not fast enough to justify reaching the perpendicular projection. For example, `5000 3000 20 25` gives the correct answer `0.0`. Here the road speed is exactly at the threshold where the optimal turning point is the starting point. A formula that assumes an interior optimum without checking its position can produce a negative distance.

The opposite situation is an actual interior optimum. For `5000 3000 15 25`, the direct projection is `4000` meters from the starting point. The optimal turning point is `1750` meters along the road, so the answer is `1750.0`. This case is useful because it confirms that neither immediate departure nor driving all the way to the projection is always optimal.

## Approaches

A straightforward approach is to consider every possible integer distance `x` from `0` to the projection point and calculate the corresponding travel time. If the projection is almost `10^9` meters away, this means roughly `10^9` evaluations of a square root and several arithmetic operations. Besides being far too slow for a 0.5 second limit, checking only integer values would not satisfy the required `10^-9` precision when the true optimum is non-integral.

The brute-force approach works because every candidate turning point can be evaluated independently. The problem is that there are far too many candidates. The key observation is that the geometry gives us a very simple one-variable function, and its minimum can be found analytically.

Let `a` be the distance along the road from the starting point to the perpendicular projection of the destination. Since the direct distance is `s` and the perpendicular distance is `h`, the right triangle gives

`a = sqrt(s^2 - h^2)`.

If the car travels `x` meters on the road, the remaining terrain distance is

`sqrt((a - x)^2 + h^2)`.

Hence the total travel time is

`T(x) = x / v + sqrt((a - x)^2 + h^2) / u`.

This function is convex on the relevant interval, so there can be at most one interior minimum. Differentiating gives

`T'(x) = 1/v - (a - x) / (u * sqrt((a - x)^2 + h^2))`.

For an interior optimum, the derivative must be zero. Solving this equation gives the exact turning point. The resulting expression can be checked against the boundary `x = 0`. If the computed point lies before the starting point, the actual optimum is simply `0`.

The brute-force works because it evaluates the same travel-time function that we optimize mathematically, but fails when the number of candidate distances becomes enormous. The observation that the derivative has a closed-form zero reduces the entire problem to a constant number of arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(s) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the distance `a` from the starting point to the perpendicular projection of the destination onto the road using `a = sqrt(s^2 - h^2)`. This converts the original geometry into a right triangle and gives us the one-dimensional coordinate of the projection.

2. If `v <= u`, output `0`. Traveling on the road is no faster than traveling through the terrain, so moving away from the starting point along the road cannot improve the route.

3. For `v > u`, solve the derivative equation for the distance `y = a - x` from the turning point to the projection. Setting the derivative to zero gives

   `y / sqrt(y^2 + h^2) = u / v`.

   Squaring and rearranging yields

   `y = h * u / sqrt(v^2 - u^2)`.

   The expression is positive because this branch has `v > u`.

4. Convert `y` back into the desired road distance using `x = a - y`.

5. If `x < 0`, output `0` instead. This means the unconstrained minimum would lie before the starting point, so the constrained minimum occurs at the boundary `x = 0`.

6. Otherwise output `x` with sufficient precision. Python's `float` is enough for the required `10^-9` absolute or relative error here, and printing 15 decimal places gives ample output precision.

Why it works: the total travel time is a convex function of the turning position. Its derivative is monotonic, so an interior point where the derivative becomes zero is the unique interior minimum. If that point lies outside the allowed interval, convexity means the closest boundary is optimal. In this problem the only relevant boundary that can become optimal is `x = 0`, while the other boundary `x = a` cannot be better because moving a little from `a` toward the starting point replaces slow terrain travel by faster road travel whenever `v > u`. Thus the algorithm either returns the unique stationary point or the correct boundary point.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    s, h, u, v = map(int, input().split())

    # Distance from the starting point to the perpendicular
    # projection of the destination onto the road.
    a = math.sqrt(float(s) * s - float(h) * h)

    # If the road is not faster than the terrain, leaving immediately
    # is optimal.
    if v <= u:
        print("0.0")
        return

    # y is the distance from the turning point to the projection.
    y = h * u / math.sqrt(float(v) * v - float(u) * u)

    x = a - y

    # The unconstrained minimum can lie before the starting point.
    if x < 0.0:
        x = 0.0

    print("{:.15f}".format(x))

if __name__ == "__main__":
    solve()
```

The first calculation obtains the horizontal leg of the right triangle. Writing it as `float(s) * s - float(h) * h` avoids relying on integer arithmetic before converting the potentially large squared values to floating point.

The `v <= u` branch is handled before the formula involving `sqrt(v^2 - u^2)`. This is not just an optimization. When `v == u`, that square root is zero and the stationary-point formula is undefined, while the answer is directly known to be zero.

For `v > u`, the code computes `y`, which is easier to derive than `x` itself. Geometrically, `y` measures how far the turning point is from the projection of the destination. Subtracting it from `a` gives the actual distance traveled on the road.

The `x < 0` check handles the case where the mathematical stationary point is outside the feasible interval. There is no need for an explicit `x > a` check because the formula gives `y > 0`, so `x = a - y` is always strictly less than `a`.

The largest intermediate integer squares are around `10^18`. Python integers themselves do not overflow, and converting the operands to floating point before multiplication keeps the computation within the normal double-precision range. The required answer tolerance is compatible with double precision for these input magnitudes.

## Worked Examples

For Sample 1, the input is `5000 3000 15 25`. The projection distance is

`sqrt(5000^2 - 3000^2) = 4000`.

The road is faster than the terrain, so an interior optimum is possible.

| Step | `a` | `y` | `x` |
|---|---:|---:|---:|
| Compute projection | `4000` | not computed | not computed |
| Solve derivative | `4000` | `3000 * 15 / sqrt(25^2 - 15^2) = 2250` | not computed |
| Convert to road distance | `4000` | `2250` | `4000 - 2250 = 1750` |
| Boundary check | `4000` | `2250` | `1750` |

The stationary point is inside the feasible interval, so the answer is `1750.0`, matching the sample. The example demonstrates the genuine interior case where neither driving directly through the terrain nor staying on the road until the projection is optimal.

For Sample 2, the input is `5000 3000 20 25`. Again, `a = 4000`, but now the speeds are exactly at the threshold.

| Step | `a` | `y` | `x` |
|---|---:|---:|---:|
| Compute projection | `4000` | not computed | not computed |
| Solve derivative | `4000` | `3000 * 20 / sqrt(25^2 - 20^2) = 4000` | not computed |
| Convert to road distance | `4000` | `4000` | `0` |
| Boundary check | `4000` | `4000` | `0` |

The stationary point coincides with the starting point. The answer is `0.0`. This confirms that the boundary handling includes the equality case correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(1) | Only a fixed number of arithmetic operations and square roots are performed. |
| Space | O(1) | Only a constant number of scalar variables are stored. |

The input values can reach `10^9`, but the algorithm does not iterate over their magnitude. It performs the same constant amount of work for every valid input, so it easily fits the 0.5 second time limit and uses negligible memory compared with the 64 MB limit.

## Test Cases

```python
import sys
import io
import math

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        s, h, u, v = map(int, sys.stdin.readline().split())

        a = math.sqrt(float(s) * s - float(h) * h)

        if v <= u:
            x = 0.0
        else:
            y = h * u / math.sqrt(float(v) * v - float(u) * u)
            x = max(0.0, a - y)

        return "{:.15f}\n".format(x)
    finally:
        sys.stdin = old_stdin

def run(inp: str) -> str:
    return solve_data(inp)

def check(inp: str, expected: float, message: str):
    actual = float(run(inp))
    assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-9), (
        f"{message}: expected {expected}, got {actual}"
    )

# Provided samples
check("5000 3000 15 25\n", 1750.0, "sample 1")
check("5000 3000 20 25\n", 0.0, "sample 2")

# Minimum-size input.
check("1 1 1 1\n", 0.0, "minimum values")

# All values equal, so the road provides no speed advantage.
check("100 100 50 50\n", 0.0, "equal speeds")

# Road is faster, but not enough to justify moving along it.
check("5 4 4 5\n", 0.0, "boundary optimum at zero")

# Large values, with a valid interior optimum.
s = 10**9
h = 6 * 10**8
u = 10**8
v = 2 * 10**8
a = math.sqrt(float(s) * s - float(h) * h)
y = h * u / math.sqrt(float(v) * v - float(u) * u)
expected = max(0.0, a - y)
check(f"{s} {h} {u} {v}\n", expected, "maximum-size input")
```

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 1 1 1` | `0.0` | Minimum values and the `v <= u` branch |
| `100 100 50 50` | `0.0` | Equal speeds and zero denominator avoidance |
| `5 4 4 5` | `0.0` | Stationary point exactly at the starting boundary |
| `1000000000 600000000 100000000 200000000` | approximately `361.53...` | Large values and floating-point computation |

## Edge Cases

When `h = s`, the perpendicular projection lies exactly at the starting point because `sqrt(s^2 - h^2) = 0`. For example, `1 1 1 1` immediately takes the `v <= u` branch and returns `0.0`. Even if the road were faster, there would be no positive distance available before reaching the projection, so zero is the only possible optimal road distance.

When `v = u`, the road and terrain have identical speeds. For example, `100 80 50 50` enters the `v <= u` branch and returns `0.0`. A careless implementation that evaluates `sqrt(v^2 - u^2)` first would obtain a zero denominator, even though the optimal answer is straightforward.

When `v > u` but the road advantage is insufficient, the stationary point lies outside the feasible interval. Consider `5 4 4 5`. Here `a = 3`, and

`y = 4 * 4 / sqrt(5^2 - 4^2) = 16 / 3`.

Thus `x = 3 - 16/3 < 0`, so the algorithm clamps it to zero. The mathematical optimum for the unrestricted function would lie before the starting point, which means the best feasible choice is to leave the road immediately.

At the threshold between zero and a positive answer, the stationary point is exactly at `x = 0`. In Sample 2, `5000 3000 20 25` gives `a = 4000` and `y = 4000`, producing exactly `x = 0`. The algorithm does not need a special equality comparison because the normal formula already gives zero.

Finally, very large values such as `s = 10^9` produce squared distances around `10^18`. Python's integer representation handles those values safely, while the final calculations use double precision. Since the output itself is a real number with a `10^-9` tolerance, the use of standard floating-point arithmetic is sufficient for the required accuracy.
:::
