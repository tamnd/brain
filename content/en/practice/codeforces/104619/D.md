---
title: "CF 104619D - Divide a Convex"
description: "We are given a convex polygon with up to 100000 vertices in order. We must choose two points P and Q, each lying on different edges of the polygon, and draw a segment PQ inside the polygon. This segment splits the polygon into two convex polygons."
date: "2026-06-29T17:25:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104619
codeforces_index: "D"
codeforces_contest_name: "2023 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 104619
solve_time_s: 24
verified: false
draft: false
---

[CF 104619D - Divide a Convex](https://codeforces.com/problemset/problem/104619/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a convex polygon with up to 100000 vertices in order. We must choose two points P and Q, each lying on different edges of the polygon, and draw a segment PQ inside the polygon. This segment splits the polygon into two convex polygons. The requirement is that these two resulting polygons must have equal perimeter, and among all such valid choices we must minimize the length of PQ.

Geometrically, picking P and Q defines a chord inside a convex polygon. Cutting along this chord produces two boundary cycles: one goes from P to Q along one direction of the polygon boundary, and the other goes from P to Q along the opposite direction. The condition is that the total perimeter along those two boundary paths, including the segment PQ, balances so both resulting polygons have the same perimeter.

The key difficulty is that P and Q are not restricted to vertices, they may lie anywhere on edges. This turns the problem from discrete combinatorics into a continuous optimization over polygon boundary positions.

The constraint n up to 100000 forces any O(n^2) reasoning over pairs of edges to fail. Even O(n log n) is only viable if each vertex is processed a constant number of times or through a linear scan. Any solution must exploit the cyclic structure of convex polygon boundaries and convert geometric conditions into a monotone function along the perimeter.

A subtle edge case arises when P or Q approaches vertices. A naive implementation that only considers vertices or assumes edges are strictly disjoint will miss optimal cuts where the balancing point lies strictly inside edges. Another pitfall is ignoring that perimeter equality depends on arc lengths along the polygon boundary, not Euclidean distances alone.

For example, in a rectangle, the optimal cut that equalizes perimeter may connect midpoints of opposite edges rather than any vertex pair. Restricting candidates to vertices would fail immediately.

## Approaches

A brute force idea is to pick two edges, parameterize points P and Q on them, and enforce the equal perimeter condition. For each pair of edges, we would solve a continuous equation in two variables and compute the best feasible segment. Even if solving each pair were O(1), there are O(n^2) edge pairs, which already exceeds 10^10 operations at the upper bound of n, so this is impossible.

The key structural observation is that convexity ensures the boundary behaves like a single cyclic sequence where distances along the perimeter are well-defined and monotone. If we fix a point P on the boundary, the condition that the two resulting perimeters are equal forces Q to be at a very specific antipodal position along the perimeter: it must split the boundary cycle into two arcs whose adjusted lengths match a fixed total constraint.

Instead of thinking in terms of geometry of segments PQ, we reinterpret the problem as choosing two points on the boundary such that the perimeter difference between the two boundary paths equals the length of PQ in a consistent way. This converts the condition into a relationship between arc lengths along a 1D circular structure.

Once everything is reduced to a circular perimeter parameter, the problem becomes: for each point P, find the corresponding point Q at a specific target perimeter distance, but P and Q must lie on different edges, so we must avoid degenerate cases where the mapping falls inside the same edge configuration. T
