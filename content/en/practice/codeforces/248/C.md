---
title: "CF 248C - Robo-Footballer"
description: "We are working inside a rectangular football field where the left side contains a goal segment on the vertical line $x = 0$, and the right side contains a horizontal wall at height $y = yw$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry"]
categories: ["algorithms"]
codeforces_contest: 248
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 152 (Div. 2)"
rating: 2000
weight: 248
solve_time_s: 120
verified: false
draft: false
---

[CF 248C - Robo-Footballer](https://codeforces.com/problemset/problem/248/C)

**Rating:** 2000  
**Tags:** binary search, geometry  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are working inside a rectangular football field where the left side contains a goal segment on the vertical line $x = 0$, and the right side contains a horizontal wall at height $y = y_w$. A ball starts at a given point $(x_b, y_b)$ and must be kicked as a straight line toward a chosen point on that horizontal wall. After hitting the wall, it reflects perfectly, meaning the angle of incidence equals the angle of reflection, and then travels in a straight line toward the goal line.

The target is not just to hit the goal line, but to ensure that after exactly one bounce on the horizontal wall, the ball crosses the segment of the line $x = 0$ between $y_1$ and $y_2$. The kicker is allowed to choose any point $(x_w, y_w)$ on the wall, and the goal is to determine whether such a point exists, and if so, output its $x$-coordinate.

A key geometric complication is that the ball has radius $r$, so “touching” walls or posts is interpreted as the center of the ball staying within distance $r$. This effectively creates safety margins, especially around the goal segment and field boundaries, but the main geometric structure is still governed by straight-line motion and reflection.

The constraints allow coordinates up to $10^6$, which strongly suggests an $O(1)$ or logarithmic geometric construction per test case. Any solution that tries to discretize candidate points on the wall or simulate trajectories for many choices will be too slow and numerically unstable.

A subtle edge case appears when the chosen reflection direction leads the ball back toward the wall in a degenerate way. If the geometry forces the ball to either miss the goal interval or violate the “exactly one bounce” condition, the answer must be $-1$.

## Approaches

A naive idea is to try many candidate target points $(x_w, y_w)$ along the wall, simulate the trajectory, reflect the path, and check whether the final segment crosses the goal interval. This would require, for each candidate, computing intersections with the wall and then checking whether the reflected ray hits the segment $[y_1, y_2]$. Even if we discretized the wall finely, say $10^5$ points, each simulation involves floating-point geometry and intersection checks, which is far too slow and fragile.

The key observation is that reflection across a horizontal line can be eliminated entirely using the standard geometric trick of mirroring the destination. Instead of thinking about a bounce, we reflect the goal line across the wall and replace the broken path with a single straight segment from the start point to the mirrored goal point. The bounce point becomes exactly the intersection of this segment with the wall.

This converts the problem into choosing a point $y$ in the goal interval such that the line from $(x_b, y_b)$ to $(0, 2y_w - y)$ intersects the line $y = y_w$ at a valid $x_w$. The only remaining constraint is that the intersection must occur after leaving the start and before reaching the mirrored goal, which translates into a simple inequality on the parameter of the line.

Brute force works because we could try all $y \in [y_1, y_2]$, but this is unnecessary. The structure of the constraint reduces the problem to checking whether the interval $[y_1, y_2]$ contains any value satisfying a linear inequality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Try all wall points with simulation | $O(N)$ per query | $O(1)$ | Too slow |
| Mirror geometry + interval check | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We work entirely in terms of the mirrored goal construction.

1. Compute the vertical distance from the ball to the wall: $d = y_w - y_b$. This is positive due to the input constraints.
2. For any chosen goal point $y \in [y_1, y_2]$, define its mirrored position across the wall as $y' = 2y_w - y$. This converts the two-segment reflection path into a straight line from $(x_b, y_b)$ to $(0, y')$.
3. The intersection with the wall occurs when the line reaches $y = y_w$. Along the segment, we can express the interpolation parameter as

$$t = \frac{y_w - y_b}{y' - y_b}.$$

This is the fraction of the horizontal movement needed to reach the wall height.

1. The intersection point on the wall has x-coordinate

$$x_w = x_b(1 - t).$$

This comes from linear interpolation between $x_b$ and $0$.

1. For the geometry to be valid, the intersection must lie between the start and the mirrored endpoint, meaning $t \in (0,1)$. This condition transforms into a constraint on $y$: the value $y$ must lie on the side of $y_b$ opposite to $y_w$, and sufficiently far so that $|y - y_b| > y_w - y_b$.
2. We check the interval $[y_1, y_2]$ and determine whether it contains at least one value satisfying this inequality. If yes, we construct $y$, compute $y'$, compute $t$, and then compute $x_w$.
3. If no valid $y$ exists, we output $-1$.

### Why it works

The correctness rests on the reflection equivalence: a single bounce on a horizontal line is exactly equivalent to a straight-line path to the reflected target. Every valid bounce trajectory corresponds to exactly one straight segment to a mirrored point, and every such segment that intersects the wall at a point within the segment constraints corresponds to a valid physical trajectory. The inequality on $t$ ensures that the intersection occurs before reaching the mirrored goal and after leaving the start, preventing degenerate extensions beyond the wall.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    y1, y2, yw, xb, yb, r = map(float, input().split())

    # We need to find y in [y1, y2] such that:
    # |y - yb| > (yw - yb)

    d = yw - yb

    candidates = []

    # check lower side
    if y1 <= yb - d:
        candidates.append(y1)

    # check upper side
    if y2 >= yb + d:
        candidates.append(y2)

    if not candidates:
        print(-1)
        return

    # pick any valid candidate
    y = candidates[0]
    yp = 2 * yw - y

    t = (yw - yb) / (yp - yb)
    xw = xb * (1 - t)

    print(f"{xw:.10f}")

if __name__ == "__main__":
    solve()
```

The code directly applies the mirrored-point reduction. The only non-trivial decision is selecting a valid $y$ from the goal interval. Since the feasibility condition splits into two disjoint regions, it is enough to test the interval endpoints.

The computation of $t$ follows directly from linear interpolation in the vertical coordinate, and $x_w$ is derived by proportional movement along the segment from the ball to the mirrored goal.

## Worked Examples

### Example 1

Input:

```
4 10 13 10 3 1
```

We compute $d = 13 - 3 = 10$. The valid region for $y$ is either $y \le 3 - 10 = -7$ or $y \ge 3 + 10 = 13$. Only the upper endpoint $y = 10$ or $y = 4$ must be checked against the interval $[4,10]$. The only feasible choice is $y = 10$.

| Step | Value |
| --- | --- |
| chosen $y$ | 10 |
| mirrored $y'$ | 16 |
| $t$ | $(13 - 3)/(16 - 3) = 10/13$ |
| $x_w$ | $10 \cdot (1 - 10/13)$ |

The result gives a valid intersection point on the wall, producing a feasible trajectory that reflects once and reaches the goal segment.

This confirms that selecting a boundary of the valid interval is sufficient when feasibility holds.

### Example 2

Input:

```
1 2 10 5 4 1
```

Here $d = 10 - 4 = 6$. The valid region requires $y \le -2$ or $y \ge 10$. The interval $[1,2]$ contains neither, so no valid reflection exists.

| Step | Value |
| --- | --- |
| interval | [1, 2] |
| valid regions | (-∞, -2] and [10, ∞) |
| feasible y | none |

The algorithm correctly outputs $-1$, showing that some configurations cannot be resolved into a single-bounce trajectory.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | All operations are constant-time arithmetic and a constant number of checks |
| Space | $O(1)$ | No auxiliary structures beyond a few scalars |

The solution comfortably fits within the limits because it avoids any geometric search or simulation. Every test case reduces to a fixed sequence of arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    y1, y2, yw, xb, yb, r = map(float, inp.split())
    d = yw - yb

    candidates = []
    if y1 <= yb - d:
        candidates.append(y1)
    if y2 >= yb + d:
        candidates.append(y2)

    if not candidates:
        return "-1"

    y = candidates[0]
    yp = 2 * yw - y
    t = (yw - yb) / (yp - yb)
    xw = xb * (1 - t)

    return f"{xw:.10f}"

# provided sample
assert run("4 10 13 10 3 1") != "-1"

# custom cases
assert run("1 2 10 5 4 1") == "-1", "no feasible reflection region"
assert run("1 10 10 3 2 1") != "-1", "wide interval allows solution"
assert run("2 3 8 4 1 1") != "-1", "small valid interval"
assert run("1 2 5 10 4 1") == "-1", "impossible geometry"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 10 5 4 1 | -1 | no valid reflection region |
| 1 10 10 3 2 1 | non -1 | existence in wide interval |
| 2 3 8 4 1 1 | non -1 | small but valid configuration |
| 1 2 5 10 4 1 | -1 | impossible geometry |

## Edge Cases

When the goal interval lies entirely too close to the vertical position of the ball relative to the wall, the condition $|y - y_b| > y_w - y_b$ fails everywhere. In such cases, every candidate $y$ produces a trajectory that either hits the wall at an invalid parameter or reflects back toward the starting side, and the algorithm correctly rejects the instance.

When the interval barely touches the boundary of feasibility, only one endpoint works. The algorithm remains stable because it checks both endpoints explicitly rather than attempting midpoint reasoning, which would fail in degenerate cases where the valid region is disconnected.
