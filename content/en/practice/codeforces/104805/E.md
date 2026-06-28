---
title: "CF 104805E - Alley"
description: "We are given several circular shadows, each attached to a tree whose center lies on a single horizontal line. Every tree produces a circular region of shade in the plane, and the task is to compute the total area covered by the union of all these disks."
date: "2026-06-28T17:11:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104805
codeforces_index: "E"
codeforces_contest_name: "Central Russia Regional Contest, 2022"
rating: 0
weight: 104805
solve_time_s: 37
verified: false
draft: false
---

[CF 104805E - Alley](https://codeforces.com/problemset/problem/104805/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several circular shadows, each attached to a tree whose center lies on a single horizontal line. Every tree produces a circular region of shade in the plane, and the task is to compute the total area covered by the union of all these disks.

Geometrically, each object is a circle with center $(x_i, 0)$ and radius $r_i$. Because all centers lie on the same line, the configuration is one-dimensional in placement but still fully two-dimensional in interaction. The goal is not to count circles or overlaps, but to compute the exact area of the region covered at least once by any circle.

The constraints $n \le 1000$ and $|x_i|, r_i \le 1000$ imply that a quadratic approach in $n$ is feasible, but anything cubic or worse would be too slow. A solution that checks all pairs of circles is acceptable, but anything that tries to discretize the plane or use fine-grained grids would fail due to precision and performance.

A subtle issue is overlap structure. Even though centers are constrained to a line, circles can still overlap partially in two dimensions. A naive summation of areas $\pi r_i^2$ clearly overcounts. Another naive idea, subtracting pairwise intersections directly, also fails because triple overlaps would be subtracted multiple times in an uncontrolled way.

A concrete failure case for naive subtraction appears when three circles overlap in a chain:

Input:

```
3
0 3
4 3
8 3
```

The middle circle overlaps both others, but the outer two do not overlap directly. Pairwise subtraction double counts the overlap with the middle circle. The correct answer requires a consistent global accounting of boundary contributions, not pairwise corrections.

The structure of the problem suggests a boundary-based viewpoint: instead of reasoning about interiors, we track which parts of each circle’s boundary actually contribute to the outer surface of the union.

## Approaches

A brute-force idea is to approximate the plane with a fine grid and mark every cell covered by at least one circle. The answer would be the number of marked cells times cell area. This is conceptually simple but completely infeasible, since achieving $10^{-4}$ precision would require a grid far too fine, leading to billions of cells.

A more principled brute force is to compute the union using inclusion-exclusion. For every subset of circles, compute the intersection area and alternate signs. This is mathematically correct but exponential in $n$, making it unusable beyond very small instances.

The key observation is that union area can be computed from the boundary of the union. The boundary consists only of circular arcs. If we can identify exactly which arcs belong to the outer boundary and compute the area
