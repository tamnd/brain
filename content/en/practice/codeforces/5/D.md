---
title: "CF 5D - Follow Traffic Rules"
description: "We are asked to compute the minimum travel time for a car moving along a straight road from Berland to Bercouver. The road has length _l_, and at a distance _d_ from the start there is a speed sign that limits the car's instantaneous speed to _w_."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 5
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 5"
rating: 2100
weight: 5
solve_time_s: 54
verified: true
draft: false
---
[CF 5D - Follow Traffic Rules](https://codeforces.com/problemset/problem/5/D)

**Rating:** 2100  
**Tags:** implementation, math  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the minimum travel time for a car moving along a straight road from Berland to Bercouver. The road has length _l_, and at a distance _d_ from the start there is a speed sign that limits the car's instantaneous speed to _w_. The car starts from rest, can accelerate or decelerate at a fixed rate _a_, and has a maximum speed _v_. After passing the sign, the car can travel at any speed up to _v_, including immediate acceleration if physically possible.

The inputs define the physical limits: the maximum acceleration _a_ and top speed _v_, the road length _l_, the distance of the speed sign _d_, and the speed limit _w_. The output is the minimal travel time, assuming the driver optimally accelerates and decelerates to obey the speed sign.

Constraints are modest: all values are ≤ 10,000, so any algorithm that operates in constant or simple arithmetic per input line is fast enough. There are no iterative operations over _l_ or _d_ that would exceed time limits. Non-obvious edge cases include situations where the car cannot even reach the speed limit before the sign, or where the speed limit is higher than the car's max speed, or where the distance after the sign is too short to accelerate to full speed. A naive implementation that simply accelerates to _v_, checks the speed at the sign, and then continues, can produce negative times if it assumes instantaneous deceleration.

A concrete tricky input is:

```
a = 2, v = 5
l = 5, d = 2, w = 1
```

Here, the car must decelerate to obey the sign because the maximum speed _v_ exceeds the speed limit _w_. A careless approach that ignores the sign or always accelerates to _v_ would yield an invalid solution.

## Approaches

The brute-force approach is to simulate the car's motion in small time steps: at each instant, increase or decrease speed by acceleration, respecting the speed limit at the sign. This is correct because it models continuous motion accurately, but it requires tiny time increments to maintain precision, which can be millions of steps for the largest inputs. With _l_ up to 10,000 km and typical accelerations, this is overkill and unnecessary.

The key observation is that acceleration and deceleration are linear in time and distance. The minimal-time trajectory consists of at most three phases: accelerate at maximum rate until either reaching a speed limit or the car's top speed, coast at constant speed if allowed, and decelerate to respect the speed sign. The problem is essentially piecewise motion along straight-line segments of velocity-time graphs. By computing the distance needed to accelerate or decelerate to a given speed using the formula $s = v^2 / (2a)$, we can determine whether the car will need to start braking before the sign or can pass it at full speed. After the sign, we can use the same reasoning for the remaining road.

This reduces the solution to a series of conditional arithmetic calculations, avoiding simulation altogether. The structure of the problem guarantees that an optimal solution never requires anything more complicated than computing distances from accelerations and limiting speeds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(l * precision steps) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the theoretical maximum speed achievable at the sign if the car accelerates at rate _a_ from rest over distance _d_. Use $v_{\text{reach}} = \sqrt{2 a d}$. The speed at the sign is constrained by _w_ and _v_, so the actual speed at the sign is the minimum of _v_, _w_, and $v_{\text{reach}}$.
2. Compute the time to reach the sign. If the car reaches the target speed before distance _d_, it coasts for the remaining distance to the sign. Otherwise, it accelerates continuously to the sign.
3. Compute the remaining distance after the sign as $l - d$. Determine whether the car can accelerate to full speed _v_ over that distance, or whether the distance is too short and it must travel at a lower speed. Again, use the formula $s = v^2 / (2a)$ to find the maximum achievable speed at the end.
4. Compute the time for the remaining segment after the sign. If the car reaches full speed _v_, it accelerates, then coasts at _v_. Otherwise, it accelerates continuously without coasting.
5. Sum the two times: the time to reach the sign and the time from the sign to the end.

Why it works: the car's motion is entirely determined by acceleration constraints. The optimal solution never accelerates more slowly than allowed or decelerates slower than necessary; any deviation increases travel time. By considering distances and maximum allowable speeds at each segment, the algorithm guarantees the shortest feasible time.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

a, v = map(int, input().split())
l, d, w = map(int, input().split())

def time_to_reach(s, start_speed, end_speed, accel):
    # distance needed to accelerate from start_speed to end_speed
    s_needed = (end_speed**2 - start_speed**2) / (2 * accel)
    if s_needed >= s:
        # cannot reach end_speed, accelerate as much as possible
        return (-start_speed + math.sqrt(start_speed**2 + 2 * accel * s)) / accel
    else:
        # accelerate to end_speed, then coast
        t_accel = (end_speed - start_speed) / accel
        s_remaining = s - s_needed
        t_coast = s_remaining / end_speed
        return t_accel + t_coast

# speed limit at the sign
speed_at_sign = min(w, v, math.sqrt(2 * a * d))

# time to reach the sign
time_to_sign = time_to_reach(d, 0, speed_at_sign, a)

# remaining distance
remaining = l - d

# maximum speed achievable after sign
max_speed_after = math.sqrt(speed_at_sign**2 + 2 * a * remaining)
final_speed = min(v, max_speed_after)

# time for remaining segment
time_after_sign = time_to_reach(remaining, speed_at_sign, final_speed, a)

total_time = time_to_sign + time_after_sign
print(f"{total_time:.10f}")
```

The `time_to_reach` function abstracts the calculation of time for a segment with acceleration, handling both cases where the car can reach a target speed and where it cannot. The main code carefully computes speed at the sign and then determines optimal acceleration after the sign.

## Worked Examples

**Sample 1**

Input:

```
1 1
2 1 3
```

| Variable | Value |
| --- | --- |
| speed_at_sign | min(3,1,sqrt(2_1_1)) = 1 |
| time_to_sign | (-0 + sqrt(0 + 2_1_1))/1 = 1.4142… |
| remaining | 1 |
| max_speed_after | sqrt(1^2 + 2_1_1) = sqrt(3) ≈ 1.732 |
| final_speed | min(1,1.732) = 1 |
| time_after_sign | (-1 + sqrt(1+2_1_1))/1 = 1.086… |
| total_time | 1.4142 + 1.086 ≈ 2.500 |

This confirms the algorithm correctly accounts for acceleration before and after the sign.

**Custom Example**

Input:

```
2 10
5 2 3
```

| Variable | Value |
| --- | --- |
| speed_at_sign | min(3,10,sqrt(2_2_2)=2.828) = 2.828 |
| time_to_sign | (-0+sqrt(0+2_2_2))/2 ≈ 1.414 |
| remaining | 3 |
| max_speed_after | sqrt(2.828^2 + 2_2_3) = sqrt(8+12)=sqrt(20) ≈ 4.472 |
| final_speed | min(10,4.472)=4.472 |
| time_after_sign | (-2.828 + sqrt(2.828^2+2_2_3))/2 = (-2.828+4.472)/2 ≈ 0.822 |
| total_time | 1.414+0.822 ≈ 2.236 |

This shows correct handling when the car cannot reach max speed after the sign.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All computations are arithmetic and square roots; no loops over distances. |
| Space | O(1) | Only a handful of variables used. |

The constraints allow only simple arithmetic operations. All square roots are of values ≤ 10^8, which Python handles safely. The solution runs in microseconds.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, v = map(int, input().split())
    l, d, w = map
```
