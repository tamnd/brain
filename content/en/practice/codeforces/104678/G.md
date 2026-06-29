---
title: "CF 104678G - Two ants"
description: "Two points on a number line each host an ant. Each ant starts at a known coordinate and moves at a constant but unknown speed and direction. The only information about each ant’s motion is where it starts and where it will be after a fixed amount of time."
date: "2026-06-29T09:08:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "G"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 87
verified: true
draft: false
---

[CF 104678G - Two ants](https://codeforces.com/problemset/problem/104678/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

Two points on a number line each host an ant. Each ant starts at a known coordinate and moves at a constant but unknown speed and direction. The only information about each ant’s motion is where it starts and where it will be after a fixed amount of time.

From this, the task is to determine whether the two ants ever occupy the same position at the same moment. If such a moment exists, we must compute the earliest time when this happens.

The key detail is that “after t seconds the ant is at position p” fully determines its motion. This implies uniform linear motion, so each ant’s position evolves as a straight line function of time.

The constraints are small enough that all computations can be done in constant time. Each ant is described by a few integers, all bounded by about ten thousand. This rules out any need for simulation over time. Instead, the problem reduces to solving a simple system of linear equations. Floating point arithmetic is sufficient because the final answer only needs precision up to one part in a million.

A subtle issue arises when both ants move with identical velocities. In that case, their relative distance never changes. If they are not already at the same starting position, they will never meet. Another corner case is when the computed meeting time is negative, which corresponds to an intersection that would have happened before time zero and is therefore irrelevant.

## Approaches

A brute-force approach would simulate both ants at small time increments, updating their positions and checking for equality at each step. Since velocities are constant, the positions change linearly, but a naive simulation would require iterating through a potentially large number of time steps to detect a meeting point accurately. Even with a fine step size, precision issues would appear, and the worst-case number of steps would grow unbounded if the meeting time is large or irrational.

The structure of the problem makes simulation unnecessary. Each ant follows a linear function of time. From the input we can recover its velocity directly. Once both velocities are known, the problem reduces to finding an intersection point of two lines in one dimension. That intersection, if it exists in the future, is the solution.

The core observation is that instead of tracking positions over time, we directly solve for the time when the two linear functions become equal. This converts the problem into a single algebraic equation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T) | O(1) | Too slow / unreliable |
| Algebraic Solution | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We model each ant’s motion as a linear function of time. If an ant starts at position a and is at position p after t seconds, its velocity is (p − a) / t.

We compute both velocities and then solve for the time when positions match.

1. Compute velocity of the first ant as v1 = (p1 − a1) / t1. This captures how fast and in which direction the first ant moves.
2. Compute velocity of the second ant as v2 = (p2 − a2) / t2 for the same reason.
3. If v1 and v2 are effectively equal, then both ants move in parallel with constant separation. In this case, they never meet because their initial positions are distinct.
4. Otherwise, set up the equation a1 + v1 * t = a2 + v2 * t and solve for t.
5. Rearranging gives t = (a2 − a1) / (v1 − v2). This is the only candidate meeting time.
6. If the computed t is negative, discard it since it represents an intersection in the past.
7. Otherwise, output t as the earliest meeting time.

### Why it works

Each ant’s position is a linear function of time, so the system of motion forms two straight lines in a time-position plane. Two distinct lines intersect at most once. Computing velocities converts each motion description into slope-intercept form. Solving for equality of these linear functions exactly identifies the intersection point. If slopes are equal, the lines are parallel, so no intersection occurs unless they coincide everywhere, which is impossible here because starting positions differ.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a1, t1, p1 = map(int, input().split())
    a2, t2, p2 = map(int, input().split())

    v1 = (p1 - a1) / t1
    v2 = (p2 - a2) / t2

    # parallel motion
    if abs(v1 - v2) < 1e-12:
        print(-1)
        return

    t = (a2 - a1) / (v1 - v2)

    if t < 0:
        print(-1)
    else:
        print(f"{t:.10f}")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived equations. The velocities are computed first, and everything is kept in floating point since the problem allows a small numerical tolerance. The comparison for equal velocities uses an epsilon rather than exact equality because division can introduce minor rounding differences.

The formula for t is applied only after confirming that the denominator is not effectively zero. Finally, we ensure that only non-negative times are accepted.

## Worked Examples

### Example 1

Input:

```
-3 2 5
12 1 10
```

For the first ant, velocity is (5 − (−3)) / 2 = 4. For the second, velocity is (10 − 12) / 1 = −2.

We solve for intersection time.

| Step | Value |
| --- | --- |
| v1 | 4 |
| v2 | -2 |
| t computation | (12 − (−3)) / (4 − (−2)) |
| t | 15 / 6 = 2.5 |

Output:

```
2.50000000
```

This confirms that the ants start apart but move toward a common point and meet after 2.5 seconds.

### Example 2

Input:

```
0 1 10
5 1 15
```

Here v1 = 10, v2 = 10.

| Step | Value |
| --- | --- |
| v1 | 10 |
| v2 | 10 |
| velocity comparison | equal |
| result | no meeting |

Output:

```
-1
```

This shows that identical velocities preserve the initial separation forever.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The computation is constant-time, which is appropriate given the very small input size bounds. Even with multiple queries, the solution scales linearly with input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    a1, t1, p1 = map(int, sys.stdin.readline().split())
    a2, t2, p2 = map(int, sys.stdin.readline().split())

    v1 = (p1 - a1) / t1
    v2 = (p2 - a2) / t2

    if abs(v1 - v2) < 1e-12:
        return "-1\n"

    t = (a2 - a1) / (v1 - v2)

    if t < 0:
        return "-1\n"
    return f"{t:.10f}\n"

# provided sample
assert abs(float(run("-3 2 5\n12 1 10\n").strip()) - 2.5) < 1e-6

# custom cases

# same velocity, different start
assert run("0 1 10\n5 1 15\n") == "-1\n"

# meet at t=0 (should not happen since a1 != a2, but constructed edge near)
assert run("0 1 1\n2 1 3\n") == "-1\n"

# opposite directions meeting
assert abs(float(run("0 1 2\n10 1 0\n").strip()) - 5.0) < 1e-6

# late meeting
assert abs(float(run("0 2 2\n100 2 98\n").strip()) - 50.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical velocities | -1 | parallel motion never intersects |
| opposite motion | positive t | correct intersection solving |
| large separation | large t | stability of formula |

## Edge Cases

One important case is when both ants move with exactly the same velocity. For example:

```
0 1 10
5 1 15
```

Here both move at speed 10 units per second in the same direction. The algorithm computes v1 = v2 and immediately rejects meeting. This is correct because the distance between them remains constant forever.

Another case is when the computed intersection lies in the past. Consider:

```
0 1 10
10 1 0
```

The computed meeting time from the formula would be negative if interpreted incorrectly, but the algorithm explicitly checks t < 0 and discards it. This corresponds to lines intersecting before time zero, which is outside the physical process described in the problem.

Finally, floating precision issues can arise when velocities are very close. The epsilon comparison prevents misclassifying nearly-parallel motion as intersecting, ensuring stability in borderline cases.
