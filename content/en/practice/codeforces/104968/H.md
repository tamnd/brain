---
title: "CF 104968H - Euclidean Pizza"
description: "We are given two finite point sets in the plane. One set represents topping points, and the other represents crust points. Every valid pizza slice is formed by choosing the origin together with any two crust points, forming a triangle whose third vertex is fixed at the origin."
date: "2026-06-28T06:48:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104968
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 2 (Beginner)"
rating: 0
weight: 104968
solve_time_s: 19
verified: false
draft: false
---

[CF 104968H - Euclidean Pizza](https://codeforces.com/problemset/problem/104968/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two finite point sets in the plane. One set represents topping points, and the other represents crust points. Every valid pizza slice is formed by choosing the origin together with any two crust points, forming a triangle whose third vertex is fixed at the origin.

For each topping point, we want to know whether there exists at least one such triangle that contains it, including points lying on its edges. The final answer is simply how many topping points can be covered by at least one origin anchored triangle formed from two crust points.

Geometrically, each slice is determined by two rays from the origin through crust points, and the slice is the angular region between those rays. So the problem reduces to checking whether a topping point can be covered by some angular sector defined by two crust directions.

The constraints are large, with up to 50,000 topping points and 50,000 crust points. Any approach that tests every pair of crust points is immediately infeasible because that would be quadratic in M. Even checking each topping against all slices would be far too slow since the number of slices is also quadratic.

This strongly suggests that the crust points must be processed into a structure over angles, because the origin is fixed and every triangle is determined purely by direction.

A key guarantee is that there is at least one crust point in each quadrant, and no two points share the same x or y coordinate. This ensures a clean circular ordering of crust points by angle without degeneracies like identical directions.

A subtle edge case arises from angular wraparound. A topping near the positive x-axis might be covered by a slice that crosses the negative x-axis, so naive interval checks on angles fail unless we explicitly handle circular intervals.

Another issue is boundary inclusion. Since points on edges count as inside, collinearity with crust rays must be treated as valid containment, which affects strict vs non-strict angle comparisons.

## Approaches

A brute-force approach would iterate over all pairs of crust points, compute the angular interval they define, and check how many topping points lie inside that sector. For each pair, checking all toppings is O(N), and there are O(M^2) pairs, leading to O(NM^2), which is far beyond feasibility.

Even if we fix a topping point first and ask whether any crus
