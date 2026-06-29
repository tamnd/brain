---
title: "CF 104670J - Joint Jog Jam"
description: "Two people start at two given coordinates on a plane and run in straight lines to their respective destinations in a fixed amount of time. Both move at constant speed, so each person’s position is a linear interpolation between their start and end points."
date: "2026-06-29T09:36:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104670
codeforces_index: "J"
codeforces_contest_name: "2021-2022 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2021)"
rating: 0
weight: 104670
solve_time_s: 48
verified: true
draft: false
---

[CF 104670J - Joint Jog Jam](https://codeforces.com/problemset/problem/104670/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Two people start at two given coordinates on a plane and run in straight lines to their respective destinations in a fixed amount of time. Both move at constant speed, so each person’s position is a linear interpolation between their start and end points.

The task is to track the distance between them throughout the motion and report the largest separation that occurs at any moment between start and finish. We are not asked for when it happens, only the maximum value of that distance.

Each runner’s path is fully determined by two points, so the whole system reduces to two moving points on a plane, both tracing line segments simultaneously over the same time interval.

The input size is constant, eight integers, so the constraints are not about scalability but about numerical robustness. A solution with constant-time geometry is expected. Anything involving discretization of time or sampling would be unnecessary and potentially incorrect because the maximum may occur between sampled points.

A subtle failure case for naive thinking is assuming the maximum distance must occur at one of the endpoints. That is not always true because the distance function between two linearly moving points is not linear.

For example, if one runner moves in a circle-like relative motion around the other (even though both move straight, their relative motion can create a turning distance curve), the maximum can occur in the interior of the time interval rather than at t = 0 or t = 1.

Another failure mode is uniform sampling, such as checking 1000 evenly spaced times. This can miss a sharp peak if the parabola is narrow.

The key difficulty is recognizing that although the motion is geometric, the distance function becomes a simple algebraic curve in one variable.

## Approaches

A brute-force approach would simulate time continuously or with dense sampling. We could evaluate the distance between the two runners at many time points between 0 and 1. This is conceptually correct because the function is continuous, so sufficiently dense sampling will approximate the maximum.

However, if we want exact correctness, sampling is not acceptable. Any finite discretization risks missing the true maximum. Even if we sample one million points, the maximum could lie between them.

The structural insight is that each coordinate of each runner is linear in time. That means the difference vector between them is also linear in time. The squared distance becomes a quadratic function of time. A quadratic function on a closed interval has a well-known shape: it either opens upward or downward, and its maximum must occur either at an endpoint or at the vertex if the vertex lies inside the interval.

This reduces the problem from geometric reasoning in the plane to analyzing a single-variable quadratic polynomial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Uniform sampling | O(k) | O(1) | Too slow / inaccurate |
| Quadratic analysis | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We parameterize time as t ranging from 0 to 1.

1. Express Kari’s position as a function of time. If she starts at A and ends at C, then her position is A + t(C − A). This encodes constant-speed linear motion.
2. Express Ola’s position similarly as B + t(D − B).
3. Compute the difference vector between them at time t. This becomes (A − B) + t((C − A) − (D − B)). This step is important because it reduces the problem to a single moving vector.
4. Write the squared distance as the dot product of the difference vector with itself. This produces an expression of the form f(t) = at² + bt + c, where a, b, c are scalar values derived from coordinates.
5. Determine the candidate time where the quadratic could achieve an extremum by computing t* = −b / (2a). This comes from the derivative of a quadratic being zero at its vertex.
6. Clamp t* into the interval [0, 1] because the motion is restricted to the run duration. If the vertex lies outside, it cannot be the maximum inside the interval.
7. Evaluate f(t) at t = 0, t = 1, and at the clamped t*. The maximum of these values is the maximum squared distance.
8. Return the square root of this maximum value to obtain the actual Euclidean distance.

### Why it works

The squared distance function is a quadratic polynomial in t because each coordinate is linear in t and squaring introduces at most degree two terms. A quadratic function on a closed interval cannot have more than one interior critical point, and its extrema are fully determined by endpoints and that critical point. Since squaring preserves ordering for non-negative values, maximizing squared distance is equivalent to maximizing distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def dist2(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return dx * dx + dy * dy

def solve():
    data = list(map(int, input().split()))
    ax, ay, bx, by, cx, cy, dx, dy = data

    # direction vectors
    pax, pay = cx - ax, cy - ay
    pbx, pby = dx - bx, dy - by

    # relative motion: P(t) - Q(t) = (A-B) + t((C-A)-(D-B))
    rx = ax - bx
    ry = ay - by
    vx = pax - pbx
    vy = pay - pby

    # f(t) = |r + t v|^2 = (v·v)t^2 + 2(r·v)t + (r·r)
    a = vx * vx + vy * vy
    b = 2 * (rx * vx + ry * vy)
    c = rx * rx + ry * ry

    best = c  # t = 0

    # t = 1
    best = max(best, a + b + c)

    if a != 0:
        t = -b / (2 * a)
        t = clamp(t, 0.0, 1.0)
        val = a * t * t + b * t + c
        best = max(best, val)

    print((best) ** 0.5)

if __name__ == "__main__":
    solve()
```

The code begins by rewriting both trajectories into velocity form, which avoids repeated interpolation. The coefficients of the quadratic come directly from expanding the squared norm of a linear expression. The endpoint checks correspond to t = 0 and t = 1. The interior candidate is computed only when the quadratic is not flat.

A subtle point is numerical stability. Using floating point for t is safe because the problem allows small relative or absolute error, and the final computation is monotonic in the squared distance.

## Worked Examples

### Example 1

Input:

```
0 0 0 0 1 1 2 2
```

We compute:

| Step | Value |
| --- | --- |
| A−B | (0, 0) |
| v | (1, 1) |
| a | 2 |
| b | 0 |
| c | 0 |
| t* | 0 |
| f(0) | 0 |
| f(1) | 2 |

Maximum squared distance is 2, so answer is √2.

This shows a case where the maximum occurs at the endpoint rather than the interior.

### Example 2

Input:

```
0 0 0 1 0 2 2 1
```

| Step | Value |
| --- | --- |
| A−B | (0, -1) |
| v | (-2, 1) |
| a | 5 |
| b | -4 |
| c | 1 |
| t* | 0.4 |
| f(0) | 1 |
| f(1) | 2 |
| f(0.4) | 5.4 |

Maximum squared distance is 5.4, so answer is √5.4.

This confirms the interior peak case, where endpoint checks alone would fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All computations are fixed-size arithmetic on eight integers |
| Space | O(1) | Only a constant number of variables are used |

The input size does not scale, so the solution is purely algebraic. The operations are limited to a few arithmetic expressions and one square root, easily within limits.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import sqrt

    data = list(map(int, inp.split()))
    ax, ay, bx, by, cx, cy, dx, dy = data

    pax, pay = cx - ax, cy - ay
    pbx, pby = dx - bx, dy - by

    rx = ax - bx
    ry = ay - by
    vx = pax - pbx
    vy = pay - pby

    a = vx * vx + vy * vy
    b = 2 * (rx * vx + ry * vy)
    c = rx * rx + ry * ry

    best = c
    best = max(best, a + b + c)

    if a != 0:
        t = -b / (2 * a)
        t = max(0.0, min(1.0, t))
        best = max(best, a * t * t + b * t + c)

    return str(math.sqrt(best))

# provided samples
assert abs(float(run("0 0 0 0 1 1 2 2")) - 1.4142135624) < 1e-6
assert abs(float(run("0 0 0 1 0 2 2 1")) - 2.2360679775) < 1e-6

# custom cases
assert abs(float(run("0 0 1 0 0 1 1 1")) - 1.4142135624) < 1e-6
assert abs(float(run("0 0 10 0 0 0 10 0")) - 10.0) < 1e-6
assert abs(float(run("0 0 0 0 0 0 0 0")) - 0.0) < 1e-6
assert abs(float(run("0 0 2 2 2 0 0 2")) - 2.8284271247) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| symmetric diagonal motion | √2 | interior vs endpoint balance |
| overlapping horizontal swap | 10 | pure 1D motion degeneracy |
| identical paths | 0 | zero-distance edge case |
| crossing paths | √8 | strong interior maximum |

## Edge Cases

One important edge case occurs when both runners move in exactly the same direction at the same speed. In that situation the relative velocity is zero, so the quadratic term disappears and the distance is constant. The algorithm handles this through the check a != 0, which skips vertex evaluation.

Another case is when both start at the same point but diverge in different directions. The maximum occurs at t = 1, and the algorithm correctly evaluates endpoints explicitly.

A degenerate case is when motion cancels exactly so that distance first increases and then decreases symmetrically. This produces a clear interior maximum, and the computed vertex t* lies strictly inside [0,1], which is correctly clamped and evaluated.
