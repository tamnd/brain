---
title: "CF 105161B - Area of the Devil"
description: "We are given five disjoint arcs on a circle. From each arc, we pick one point, and we connect the five chosen points in order, forming a closed pentagon-like star shape."
date: "2026-06-27T10:56:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105161
codeforces_index: "B"
codeforces_contest_name: "2024 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 105161
solve_time_s: 30
verified: false
draft: false
---

[CF 105161B - Area of the Devil](https://codeforces.com/problemset/problem/105161/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given five disjoint arcs on a circle. From each arc, we pick one point, and we connect the five chosen points in order, forming a closed pentagon-like star shape. The task is to compute the area of the resulting pentagram-like polygon formed by these five points on the circle.

A useful way to interpret the construction is to forget the “choice” aspect and instead think geometrically about the region that is swept when each point can vary along its arc. As the point moves along an arc, the resulting polygon area changes continuously, and the final required value corresponds to a fixed geometric decomposition that depends only on the arc endpoints.

The output is a single real number representing this area.

The underlying structure is strongly geometric: everything lies on a circle of radius r (implicitly given or derivable from coordinates or angles), so all relevant geometry reduces to circular arcs, chords, and triangles formed by chord intersections.

The constraints are not explicitly shown here, but from the editorial structure and the O(T) per test solution, we can infer that there are multiple test cases and each must be solved in constant time after preprocessing the arc geometry. This immediately rules out any approach that discretizes arcs or simulates point selection. Any method involving sweeping over points or sampling would be far too slow.

A naive geometric approach might attempt to consider all possible choices of one point per arc and compute extreme configurations, but this is combinatorially continuous and not discretizable. The key difficulty is that the solution depends only on endpoints of arcs, not on internal points.

A subtle edge case arises when arcs wrap around the 0 angle point. For example, an arc might span from 350° to 10°, which visually crosses the angle discontinuity. I
