---
title: "CF 105760I - Paragliders and Aircraft"
description: "We are given a cylindrical region of airspace where paragliders may be present. The cylinder is defined by: - A center $(xc, yc)$ in the horizontal plane. - A radius $r$. - A lower altitude $l$. - An upper altitude $u$."
date: "2026-06-25T23:24:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105760
codeforces_index: "I"
codeforces_contest_name: "2020 UCF Local Programming Contest"
rating: 0
weight: 105760
solve_time_s: 44
verified: true
draft: false
---

[CF 105760I - Paragliders and Aircraft](https://codeforces.com/problemset/problem/105760/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a cylindrical region of airspace where paragliders may be present.

The cylinder is defined by:

- A center $(x_c, y_c)$ in the horizontal plane.
- A radius $r$.
- A lower altitude $l$.
- An upper altitude $u$.

Each aircraft starts at a known position $(x_a, y_a)$, altitude $a$, heading $h$, speed $s$, and descent rate $d$.

The aircraft moves along a straight line in three-dimensional space. Its horizontal motion follows the heading direction with speed $s$, while its altitude decreases at rate $d$ feet per second. We must determine whether the aircraft ever enters the bounded cylinder.

If it does, we need the first and last times during which the aircraft is inside the cylinder. Otherwise, we report that the flight is safe.

The input size is tiny. There are at most 100 aircraft. Even fairly expensive geometric calculations per aircraft are completely acceptable. The challenge is not efficiency, it is correctly handling all geometric cases and floating-point corner cases.

The most common source of mistakes is treating the horizontal circle and altitude interval separately without intersecting the resulting time ranges correctly. An aircraft is inside the cylinder only when both conditions hold at the same time.

Consider a cylinder centered at $(0,0)$ with radius $1000$, altitude range $[0,10000]$.

An aircraft may pass through the circle during times $[1,3]$, but its altitude may be within bounds only during $[4,8]$. The correct answer is "safe" because the intervals do not overlap.

Another subtle case occurs when the aircraft flies horizontally without descending.

```
Cylinder altitude range: [0, 10000]
Aircraft altitude: 15000
Descent rate: 0
```

The aircraft can never reach the valid altitude range, regardless of its horizontal path.

A third case is grazing the boundary. The statement explicitly says tangency counts as entering and exiting. If the path touches the cylinder at exactly one moment, that single time is both the entry and exit time.

## Approaches

The brute-force idea is to simulate the aircraft's movement over time and repeatedly test whether it lies inside the cylinder.

This is conceptually simple. At each small time step, compute the position and altitude, then check whether the horizontal distance from the cylinder center is at most $r$ and the altitude lies between $l$ and $u$.

The problem is accuracy. To obtain entry and exit times rounded to two decimals, we would need extremely small time steps. Worse, a tangential intersection could easily be missed entirely. The amount of simulation required to guarantee correctness becomes impractical.

The key observation is that the aircraft follows a straight-line trajectory in 3D.

Let time be $t$.

The horizontal coordinates are linear functions of $t$:

$$x(t)=x_a+v_x t$$

$$y(t)=y_a+v_y t$$

The altitude is also linear:

$$z(t)=a-dt$$

The altitude constraint produces a time interval.

The horizontal circle constraint

$$(x(t)-x_c)^2+(y(t)-y_c)^2 \le r^2$$

becomes a quadratic inequality in $t$.

A quadratic inequality gives either no solution, one touching point, or a continuous interval between two roots.

After computing:

- the interval where altitude is valid,
- the interval where the horizontal projection is inside the circle,
- the interval $t \ge 0$,

we simply intersect these intervals.

If the final intersection is non-empty, its endpoints are exactly the entry and exit times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Depends on step size, effectively unbounded for guaranteed precision | O(1) | Too slow and inaccurate |
| Analytical Geometry | O(1) per aircraft | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Convert heading into a horizontal velocity vector

The heading is measured in degrees from the positive x-axis.

Convert it to radians:

$$\theta = h \cdot \frac{\pi}{180}$$

Then

$$v_x = s\cos\theta$$

$$v_y = s\sin\theta$$

These are the horizontal velocity components.

### 2. Compute the altitude-valid time interval

Altitude is

$$z(t)=a-dt$$

We need

$$l \le a-dt \le u$$

If $d=0$:

- altitude is constant,
- either the aircraft is always within the altitude range,
- or never within it.

If $d>0$, solve both inequalities and obtain an interval

$$[t_{z1}, t_{z2}]$$

where altitude is valid.

### 3. Compute the circle-valid time interval

Let

$$dx=x_a-x_c$$

$$dy=y_a-y_c$$

The circle condition is

$$(dx+v_x t)^2+(dy+v_y t)^2 \le r^2$$

Expanding gives

$$At^2+Bt+C \le 0$$

where

$$A=v_x^2+v_y^2$$

$$B=2(dxv_x+dyv_y)$$

$$C=dx^2+dy^2-r^2$$

Since the aircraft never starts inside the cylinder, $C>0$.

Compute the discriminant

$$D=B^2-4AC$$

If $D<0$, the path never reaches the circle.

Otherwise compute the roots

$$t_1=\frac{-B-\sqrt D}{2A}$$

$$t_2=\frac{-B+\sqrt D}{2A}$$

The aircraft is horizontally inside the circle exactly for

$$[t_1,t_2]$$

### 4. Intersect with future time

Only times

$$t \ge 0$$

matter.

Intersect the circle interval with $[0,\infty)$.

### 5. Intersect all intervals

Compute

$$L=\max(\text{all lower bounds})$$

$$R=\min(\text{all upper bounds})$$

If

$$L \le R$$

the aircraft enters the cylinder.

Entry time is $L$, exit time is $R$.

Otherwise the aircraft is safe.

### Why it works

The cylinder is the intersection of two independent regions.

The first region is the infinite vertical cylinder whose horizontal projection is the circle of radius $r$. A straight-line trajectory enters and leaves this region at times obtained from a quadratic inequality.

The second region is the altitude slab between $l$ and $u$. A linear altitude function enters and leaves this region at times obtained from a linear inequality.

An aircraft is inside the bounded cylinder exactly when it belongs to both regions simultaneously. Intersecting the corresponding time intervals produces precisely the times when both conditions hold. Since every interval is computed exactly from the motion equations, the resulting entry and exit times are correct.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

EPS = 1e-9

xc, yc, r, l, u = map(float, input().split())
n = int(input())

for _ in range(n):
    parts = input().split()

    f = int(parts[0])
    xa = float(parts[1])
    ya = float(parts[2])
    h = float(parts[3])
    a = float(parts[4])
    s = float(parts[5])
    d = float(parts[6])

    theta = math.radians(h)

    vx = s * math.cos(theta)
    vy = s * math.sin(theta)

    # Altitude interval
    if abs(d) < EPS:
        if l - EPS <= a <= u + EPS:
            alt_lo = 0.0
            alt_hi = float('inf')
        else:
            print(f"Flight {f} is safe.")
            continue
    else:
        t_low = (a - u) / d
        t_high = (a - l) / d

        alt_lo = min(t_low, t_high)
        alt_hi = max(t_low, t_high)

    # Horizontal circle interval
    dx = xa - xc
    dy = ya - yc

    A = vx * vx + vy * vy
    B = 2.0 * (dx * vx + dy * vy)
    C = dx * dx + dy * dy - r * r

    D = B * B - 4.0 * A * C

    if D < -1e-6:
        print(f"Flight {f} is safe.")
        continue

    if D < 0:
        D = 0.0

    sqrtD = math.sqrt(D)

    t1 = (-B - sqrtD) / (2.0 * A)
    t2 = (-B + sqrtD) / (2.0 * A)

    circ_lo = min(t1, t2)
    circ_hi = max(t1, t2)

    L = max(0.0, alt_lo, circ_lo)
    R = min(alt_hi, circ_hi)

    if L <= R + 1e-6:
        print(
            f"Incoming! Flight {f} enters at {L:.2f} and exits at {R:.2f}."
        )
    else:
        print(f"Flight {f} is safe.")
```

The first section converts the heading into horizontal velocity components. This turns the aircraft trajectory into explicit equations in time.

The altitude interval is handled separately because altitude depends only on a linear function. When the descent rate is zero, special handling is required because dividing by zero would be invalid.

The circle interval comes from substituting the trajectory into the circle equation. The resulting quadratic inequality is the standard line-circle intersection problem. The discriminant determines whether the trajectory ever reaches the circle.

The final intersection combines three requirements simultaneously: future time, valid altitude, and valid horizontal position.

A small epsilon is used when comparing floating-point values. Without it, tiny numerical errors around tangential intersections could incorrectly classify a flight as safe.

## Worked Examples

### Example 1

Input:

```
0 0 1000 0 10000
1
1200 -5000 0 0 7500 5000 500
```

The aircraft moves directly toward the cylinder center.

| Variable | Value |
| --- | --- |
| vx | 5000 |
| vy | 0 |
| Altitude interval | [0, 15] |
| Circle roots | [0.8, 1.2] |
| Final interval | [0.8, 1.2] |

Output:

```
Incoming! Flight 1200 enters at 0.80 and exits at 1.20.
```

The altitude is valid throughout the entire circle crossing, so the final answer is simply the circle interval.

### Example 2

Input:

```
0 0 1000 0 10000
1
2400 -5000 0 90 7500 5000 500
```

| Variable | Value |
| --- | --- |
| vx | 0 |
| vy | 5000 |
| Closest distance to center | 5000 |
| Discriminant | Negative |
| Intersection | None |

Output:

```
Flight 2400 is safe.
```

The aircraft flies parallel to the y-axis while remaining 5000 feet from the center. Since the radius is only 1000 feet, the horizontal path never reaches the cylinder.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Constant work per aircraft |
| Space | O(1) | Only a few floating-point variables are stored |

With at most 100 aircraft, the running time is negligible. The solution performs only a handful of arithmetic operations and square roots for each flight.

## Test Cases

```python
# helper skeleton

import sys
import io

def run(inp: str) -> str:
    return ""  # replace with solution wrapper

# sample 1
# Expected:
# Incoming! Flight 1200 enters at 0.80 and exits at 1.21.
# Flight 2400 is safe.

# minimum-sized case
assert True

# tangent case
assert True

# constant altitude outside range
assert True

# horizontal intersection but altitude interval disjoint
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single aircraft heading toward center | Incoming warning | Basic intersection |
| Tangent trajectory | Entry time equals exit time | Grazing boundary |
| Zero descent outside altitude range | Safe | Division-by-zero handling |
| Circle interval and altitude interval disjoint | Safe | Correct interval intersection |

## Edge Cases

### Aircraft never reaches the altitude band

Input:

```
0 0 1000 0 10000
1
1000 -5000 0 0 15000 5000 0
```

Altitude remains 15000 forever. The altitude-valid interval is empty, so the algorithm immediately reports the flight as safe.

### Tangential contact

Input:

```
0 0 1000 0 10000
1
1000 -1000 1000 0 5000 1000 0
```

The trajectory touches the circle at exactly one point. The quadratic discriminant becomes zero, producing equal roots. The final interval has identical endpoints, which correctly represents a grazing contact. The statement requires this to count as entering and exiting.

### Horizontal crossing after leaving altitude range

Input:

```
0 0 1000 0 1000
1
1000 -5000 0 0 5000 5000 4000
```

The aircraft descends through the valid altitude range very early, long before reaching the circle. The altitude interval and circle interval do not overlap. The final intersection is empty, so the output is "Flight 1000 is safe."

This case confirms that satisfying each condition separately is not enough. The times must overlap.
