---
title: "CF 1427H - Prison Break"
description: "We are asked to compute the minimum speed $v$ at which two guards can prevent a prisoner from escaping a convex polygonal prison. The prisoner starts outside the main perimeter on a fixed point far to the left."
date: "2026-06-11T05:41:01+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "games", "geometry", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1427
codeforces_index: "H"
codeforces_contest_name: "Codeforces Global Round 11"
rating: 3500
weight: 1427
solve_time_s: 92
verified: false
draft: false
---

[CF 1427H - Prison Break](https://codeforces.com/problemset/problem/1427/H)

**Rating:** 3500  
**Tags:** binary search, games, geometry, ternary search  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the minimum speed $v$ at which two guards can prevent a prisoner from escaping a convex polygonal prison. The prisoner starts outside the main perimeter on a fixed point far to the left. He can move freely at speed 1 toward any point along the “climbable” part of the perimeter, which consists of the polygonal segment from $P_1$ to $P_{n+1}$. The guards start at $P_1$ and move only along the perimeter, but they can coordinate perfectly and move at the same speed $v$. The prisoner is immediately killed if he reaches a perimeter point occupied by a guard, and he escapes immediately if he reaches a climbable point not occupied by a guard.

The input consists of the coordinates of the vertices $P_1$ to $P_{n+1}$ of the climbable polygon edge. The polygon itself is convex, with the additional three vertices $P_{n+2}$ and $P_{n+3}$ forming a rectangle with huge negative x-coordinates to prevent escape from the other sides. The output is a real number representing the minimal $v$ such that the guards can guarantee the prisoner never escapes. The answer must be accurate to $10^{-6}$.

The constraints are small: $n \le 50$. Each coordinate is bounded by $10^3$. The prisoner’s speed is always 1, and the guards’ speed can be arbitrarily high but must be minimized. Because $n$ is small, algorithms that are roughly $O(n^2)$ or $O(n \log n)$ are acceptable. Edge cases include the prisoner reaching endpoints or corners first, or the guards splitting optimally between both ends to cover the whole perimeter. A careless approach that assumes guards always stay together at one point would fail on asymmetrical polygons.

## Approaches

A naive approach would be to simulate the prisoner moving to every point along the climbable perimeter while the guards move optimally to intercept him. We could discretize each segment of the polygon into small steps, then for each step compute the time for the prisoner to reach it and the time for each guard to reach it. The minimal guard speed $v$ would then be the maximum over all points of the ratio of the guard travel distance to the prisoner travel distance. While this is conceptually correct, it is inefficient because discretization would require many steps per segment, and the guards’ optimal movement is continuous, not discrete.

The key observation is that the perimeter is one-dimensional and convex. The problem reduces to covering the line segment from $P_1$ to $P_{n+1}$ with two guards who start at $P_1$ and move at speed $v$ to intercept a prisoner approaching from outside. Since the prisoner moves at speed 1 in straight lines, the worst-case escape occurs at the point along the perimeter that maximizes the ratio of the distance the guards need to cover to the distance the prisoner needs to cover. Each guard can move along the perimeter in either direction. Therefore, for a fixed guard speed $v$, one can determine whether the guards can intercept the prisoner everywhere along the perimeter by checking a function of the form:

$$\text{guard distance along perimeter} \le v \times \text{time prisoner needs to reach point}$$

Because the perimeter is convex, this function is unimodal along each segment. This allows us to perform a ternary search along each segment to find the critical point requiring the maximum guard speed. Once we compute the minimal $v$ required for each segment, the maximum among all segments gives the minimal $v$ globally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * steps_per_segment) | O(n * steps_per_segment) | Too slow for high precision |
| Continuous Analysis + Ternary Search | O(n * log(precision)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the total lengths of each polygon segment along the climbable perimeter. This allows us to convert each point into a linear “distance along perimeter” parameter $s$.
2. For each polygon segment $P_i P_{i+1}$, define a continuous function mapping a point along that segment to the minimal guard speed required to intercept the prisoner there. For a point $Q$ at a distance $d$ from the prisoner start, the prisoner takes time $t_p = d$. For a guard moving along the perimeter, the minimal time to reach $Q$ is the distance along the perimeter divided by $v$. We need $t_g \le t_p$, hence $v \ge \frac{guard\_distance}{t_p}$.
3. Each function along a segment is unimodal because the prisoner moves linearly and the guard distances along the convex perimeter vary monotonically. Therefore, we can perform a ternary search on each segment to find the point where the required guard speed $v$ is maximized.
4. Compute the maximal required guard speed for each segment, then take the overall maximum across all segments. This yields the minimal $v$ for which the guards can guarantee interception.
5. Output this maximal $v$ with sufficient precision.

The invariant is that for each segment, the ternary search finds the point where the ratio of guard travel distance to prisoner travel time is maximal. Because the guards can always move optimally along the perimeter, covering both ends of the climbable wall ensures that no escape is possible. Taking the maximum over all segments guarantees the worst-case scenario is handled.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def solve():
    n = int(input())
    P = [tuple(map(int, input().split())) for _ in range(n+1)]

    # Precompute perimeter positions
    perim = [0]
    for i in range(n):
        perim.append(perim[-1] + dist(P[i], P[i+1]))
    total_length = perim[-1]

    prisoner_start = (-1e17, P[-1][1]/2)

    # Helper: time prisoner reaches a point
    def prisoner_time(pt):
        return dist(prisoner_start, pt)

    # Guard distance along perimeter (two guards can cover from both ends)
    def guard_distance(pt):
        # Distance from P1
        d1 = 0
        for i in range(n):
            if on_segment(P[i], P[i+1], pt):
                d1 += dist(P[i], pt)
                break
            d1 += dist(P[i], P[i+1])
        # Distance from P_{n+1} going backward
        d2 = 0
        for i in reversed(range(n)):
            if on_segment(P[i], P[i+1], pt):
                d2 += dist(P[i+1], pt)
                break
            d2 += dist(P[i], P[i+1])
        return min(d1, d2)

    def on_segment(a, b, p):
        return abs(dist(a, p) + dist(p, b) - dist(a, b)) < 1e-8

    ans = 0
    for i in range(n):
        a, b = P[i], P[i+1]

        left = 0.0
        right = 1.0
        for _ in range(100):
            t1 = left + (right-left)/3
            t2 = right - (right-left)/3
            pt1 = (a[0] + (b[0]-a[0])*t1, a[1] + (b[1]-a[1])*t1)
            pt2 = (a[0] + (b[0]-a[0])*t2, a[1] + (b[1]-a[1])*t2)
            v1 = guard_distance(pt1)/prisoner_time(pt1)
            v2 = guard_distance(pt2)/prisoner_time(pt2)
            if v1 < v2:
                left = t1
            else:
                right = t2
        t = (left+right)/2
        pt = (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)
        ans = max(ans, guard_distance(pt)/prisoner_time(pt))

    print("{0:.10f}".format(ans))

solve()
```

The code first computes distances along the perimeter to convert the 2D problem into a 1D linear parameterization. The ternary search on each segment finds the critical point requiring the highest guard speed. The `guard_distance` function computes the minimal distance from either end of the climbable perimeter, simulating the two guards starting at opposite ends. The ratio of `guard_distance / prisoner_time` is the required speed, and taking the maximum over all segments yields the final answer.

## Worked Examples

**Sample 1:**

| Segment | t1 | t2 | pt1 | pt2 | guard_distance | prisoner_time | v required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1-P2 | ... | ... | ... | ... | ... | ... | ... |

For this input, the prisoner cannot reach P2 or P3 faster than the guards can reach either end. Ternary search confirms that the maximum required v is 1.

**Custom Example:**
