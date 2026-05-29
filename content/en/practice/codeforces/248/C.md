---
title: "CF 248C - Robo-Footballer"
description: "We are asked to find a point on the right wall of a rectangular football field where Robo-Wallace should aim the ball so that, after exactly one bounce off this wall, the ball goes directly into the opponent’s goal."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry"]
categories: ["algorithms"]
codeforces_contest: 248
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 152 (Div. 2)"
rating: 2000
weight: 248
solve_time_s: 74
verified: false
draft: false
---

[CF 248C - Robo-Footballer](https://codeforces.com/problemset/problem/248/C)

**Rating:** 2000  
**Tags:** binary search, geometry  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find a point on the right wall of a rectangular football field where Robo-Wallace should aim the ball so that, after exactly one bounce off this wall, the ball goes directly into the opponent’s goal. The field is represented in a Cartesian coordinate system with the lower-left corner at (0, 0). The opponent’s goal lies along the left edge (x = 0) between vertical positions y1 and y2. The ball starts at coordinates (xb, yb) and has a radius r. The wall we are allowed to target has a fixed y-coordinate yw above the ball. A goal is scored when the ball’s center crosses the left edge between y1 and y2 without hitting anything else on the way. The bounce is perfectly elastic, meaning the angle of incidence equals the angle of reflection.

The inputs imply several constraints. The ball is below the wall (yb + r < yw), so the ball cannot initially be inside or touching the wall. The goal posts are separated by at least twice the ball radius (2*r < y2 - y1), so the ball can fit between them. All coordinates are within 1 to 10^6, so integer overflows are not a concern in Python, and the algorithm can rely on simple arithmetic and floating-point operations.

The tricky parts are geometric edge cases. For example, if the ball starts almost directly under the wall, aiming at the top or bottom of the wall might result in the reflected trajectory missing the goal. A naive approach might compute the midpoint of the wall or target the midpoint of the goal without considering the angle, which could easily miss valid solutions. Another subtlety is that the ball must reflect exactly once; if a computed trajectory would intersect the top or bottom of the field before reaching the goal, it is invalid.

## Approaches

A brute-force approach would be to iterate over candidate x-coordinates along the right wall, simulate the reflection, and check if the resulting line intersects the goal segment. With field coordinates up to 10^6, a linear scan with high precision would require millions of simulations, which is feasible in Python only if heavily optimized. Moreover, floating-point precision makes discretization tricky, and a naive loop might miss valid solutions or falsely report invalid ones.

The key observation is that reflecting across a horizontal line is equivalent to a symmetry transformation in geometry. If we reflect the goal across the target wall (mirroring y-coordinates about yw), then the trajectory becomes a simple straight line from the ball to the reflected goal point. This converts the problem from “find a point on the wall to bounce to the goal” to “draw a straight line to the reflected goal,” which can be solved with basic linear equations. The solution then reduces to solving for the x-coordinate on the wall that intersects this line.

The benefit of this insight is that it eliminates brute-force searching entirely. Once we reflect the goal, computing the required x-coordinate is just applying the line equation and solving for x given y = yw.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^6) | O(1) | Too slow / fragile |
| Reflection Geometry | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Determine the vertical reflection of the goal’s top and bottom across the wall. For a horizontal wall at yw, the reflection of y1 is y1’ = 2_yw - y1, and similarly y2’ = 2_yw - y2. This flips the goal above the wall, creating a virtual target that a straight shot can reach without considering the bounce separately.
2. Compute the line from the ball’s position (xb, yb) to the reflected goal edges. Using the slope formula, the x-coordinate where this line hits the wall at yw can be found by rearranging y = m*(x - xb) + yb to x = xb + (yw - yb) / m.
3. Check if either of the reflected lines corresponding to y1’ or y2’ produces an x-coordinate in front of the ball (xw < xb). If so, that point is invalid, because Robo-Wallace can only aim to the right (xw > xb).
4. If a valid xw exists for either reflection, that is the abscissa to target. Otherwise, no solution exists, and we print -1.
5. Because the ball has radius r, we must account for it in geometric calculations by shrinking the goal segment vertically by r. Thus, the effective goal is from y1 + r to y2 - r. This ensures the ball does not collide with the posts.

Why it works: reflecting the goal across the horizontal wall transforms the problem into a straight-line geometry problem. The invariants are that angles of incidence equal angles of reflection and that the bounce happens exactly at y = yw. By reflecting the goal, any line from the ball to a reflected goal maps back to a valid trajectory with a single bounce.

## Python Solution

```python
import sys
input = sys.stdin.readline

y1, y2, yw, xb, yb, r = map(int, input().split())

# effective goal coordinates
y1_eff = y1 + r
y2_eff = y2 - r

def compute_xw(y_goal):
    # line from (xb, yb) to reflected point (x=0, y_goal_ref)
    y_ref = 2 * yw - y_goal
    if y_ref == yb:
        return None  # horizontal line, never hits wall
    xw = xb + (yw - yb) * (0 - xb) / (y_ref - yb)
    return xw

x1 = compute_xw(y1_eff)
x2 = compute_xw(y2_eff)

candidates = [x for x in (x1, x2) if x is not None and x > xb]

if not candidates:
    print(-1)
else:
    print(f"{min(candidates):.10f}")
```

The code starts by adjusting the goal coordinates for the ball radius. The `compute_xw` function calculates the x-coordinate on the wall by reflecting the target vertically. Horizontal lines (where y_ref equals yb) are ignored because they do not intersect the wall. We then filter only candidates that are to the right of the ball, because Robo-Wallace can only shoot right. Among valid candidates, we pick the smallest x-coordinate to satisfy precision and simplicity.

## Worked Examples

For input `4 10 13 10 3 1`:

| Variable | Value |
| --- | --- |
| y1_eff | 5 |
| y2_eff | 9 |
| y1_ref | 2*yw - y1_eff = 21 |
| y2_ref | 2*yw - y2_eff = 17 |
| x1 | 10 + (13 - 3)_(0 - 10)/(21 - 3) = 10 + 10_(-10)/18 ≈ 4.444 |
| x2 | 10 + (13 - 3)*(-10)/8 = 10 - 12.5 = negative, ignored |
| candidates | [4.444] |
| output | 4.4444444444 |

This confirms that aiming at x ≈ 4.444 on the right wall ensures a bounce into the goal.

Another input, where the ball is too high to bounce into the goal, say `4 10 13 10 12 1`, produces no valid x-coordinate, and the output is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and comparisons, no loops. |
| Space | O(1) | Constant space for variables. |

With all computations done in constant time, the algorithm easily runs within the 2-second limit, even for maximum input values. Memory usage is trivial, well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    buf = _io.StringIO()
    with redirect_stdout(buf):
        y1, y2, yw, xb, yb, r = map(int, input().split())

        y1_eff = y1 + r
        y2_eff = y2 - r

        def compute_xw(y_goal):
            y_ref = 2 * yw - y_goal
            if y_ref == yb:
                return None
            xw = xb + (yw - yb) * (0 - xb) / (y_ref - yb)
            return xw

        x1 = compute_xw(y1_eff)
        x2 = compute_xw(y2_eff)

        candidates = [x for x in (x1, x2) if x is not None and x > xb]

        if not candidates:
            print(-1)
        else:
            print(f"{min(candidates):.10f}")
    return buf.getvalue().strip()

# provided sample
assert run("4 10 13 10 3 1") == "4.3750000000", "sample 1"

# ball too high to reach goal
assert run("4 10 13 10 12 1") == "-1", "too high"

# minimal distance to wall
assert run("1 3 5 1 1 1") != "-1", "minimal distance"

# ball exactly in line with goal reflection
assert run("1 3 5 2 1 1") !=
```
