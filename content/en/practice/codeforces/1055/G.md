---
title: "CF 1055G - Jellyfish Nightmare"
description: "We are given a fixed convex shape representing Bob, which can only move by translation inside a vertical swimming lane bounded by two vertical lines. Bob starts far below the plane and must reach far above it."
date: "2026-06-15T12:54:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1055
codeforces_index: "G"
codeforces_contest_name: "Mail.Ru Cup 2018 Round 2"
rating: 3500
weight: 1055
solve_time_s: 125
verified: false
draft: false
---

[CF 1055G - Jellyfish Nightmare](https://codeforces.com/problemset/problem/1055/G)

**Rating:** 3500  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed convex shape representing Bob, which can only move by translation inside a vertical swimming lane bounded by two vertical lines. Bob starts far below the plane and must reach far above it. His motion is continuous, but at every moment he is allowed to choose any direction, as long as he does not rotate his body.

Inside the lane there are circular danger zones. If Bob’s translated polygon overlaps a circle with positive area at any moment, that circle is considered triggered once, and it stops mattering afterwards. The goal is to choose a continuous path from bottom to top that minimizes how many distinct circles Bob ever overlaps.

The key difficulty is that Bob is not a point. He is a rigid convex polygon, so each circle effectively becomes a grown obstacle: collision depends on whether a translated polygon intersects a disk, not just whether a point enters it.

The input sizes are small in a geometric sense. The polygon has at most 200 vertices and there are at most 200 circles. This immediately suggests that pairwise geometric preprocessing in O(nm) or O(m²) is acceptable, while anything that tries to explicitly explore continuous paths is not.

A subtle edge case is that “touching” does not count as a hit. This matters because many geometric reductions naturally produce closed boundaries, and treating them incorrectly can overcount intersections.

Another important issue is that Bob can choose any horizontal position at any height. A naive interpretation that reduces the problem to vertical motion alone is incorrect because the optimal path can weave in x to avoid circles.

## Approaches

The brute force viewpoint is to think of the plane as being partitioned into regions: each circle defines a convex forbidden set in the space of translations of Bob. A path is valid if it is continuous and we count how many of these regions it enters. One could imagine exploring the state space continuously, but even discretizing the plane into a fine grid leads to an enormous graph, because every obstacle boundary introduces new combinatorial structure and intersections between 200 convex regions already creates too many cells.

The key simplification comes from the structure of the motion. Bob moves monotonically from y = −h to y = h, and nothing forces him to go downward. Any optimal path can be transformed into one that never decreases in y, since revisiting a lower y-level cannot help avoid future circles but can only increase opportunities for intersections.

Once motion is viewed as y-monotone, the problem becomes a sweep in the vertical direction. At any fixed y, Bob’s possible x-positions form an interval, and each circle contributes a forbidden x-interval only for the y-range where that circle is vertically active.

For a fixed circle centered at (cx, cy) with radius r, consider a horizontal slice at height y. If |y − cy| > r, the circle does not matter at that level. Otherwise, the circle projects to a horizontal interval in x of half-width √(r² − (y − cy)²). Because Bob is a rigid convex polygon with fixed x-projection width [xmin, xmax], this interval must be expanded by the polygon’s horizontal extent. Thus each circle becomes a y-dependent forbidden x-interval over a continuous y-range.

So the geometry reduces to a 2D arrangement of axis-aligned “caps”: each obstacle is active on a y-interval and, within that band, blocks an x-interval that changes continuously but has a simple analytic form. The task is to choose a continuous x(y) curve minimizing how many of these obstacles are ever entered.

Brute force would discretize y and maintain full arrangements of intervals, but transitions between y-levels change combinatorially whenever a circle becomes active or inactive, so the state space still explodes.

The crucial observation is that each circle is either never entered or entered at least once, and once entered it contributes exactly one unit of cost regardless of how long we stay inside it. This turns the problem into finding a path that minimizes the number of distinct regions intersected, which can be handled by a sweep-line dynamic programming over y-events, maintaining connectivity of free space in x.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive geometric exploration | Exponential | Exponential | Too slow |
| Sweep line over y with interval DP | O(m² log m + nm) | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Compute the horizo
