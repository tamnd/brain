---
title: "CF 104651J - Find the Gap"
description: "We are given a set of points in three-dimensional space. The task is to place two parallel planes such that every point lies between them, and the distance between the planes is as small as possible."
date: "2026-06-29T16:30:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104651
codeforces_index: "J"
codeforces_contest_name: "The 2023 CCPC Online Contest"
rating: 0
weight: 104651
solve_time_s: 31
verified: false
draft: false
---

[CF 104651J - Find the Gap](https://codeforces.com/problemset/problem/104651/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points in three-dimensional space. The task is to place two parallel planes such that every point lies between them, and the distance between the planes is as small as possible. Equivalently, we want to find a direction in space and then project all points onto that direction, and minimize the difference between the maximum and minimum projection value.

Once viewed this way, the problem becomes a geometric optimization over directions: for any unit vector $\mathbf{u}$, each point $(x_i, y_i, z_i)$ produces a scalar projection $p_i = \mathbf{u} \cdot \mathbf{x}_i$. The gap between the two supporting planes orthogonal to $\mathbf{u}$ is exactly $\max p_i - \min p_i$. We want the smallest such value over all directions.

The input size is small, with at most 50 points. That immediately rules out anything quadratic in the number of candidate directions if we were to enumerate directions naively from all possible real vectors. However, it strongly suggests that a geometric reduction involving pairwise structures or combinatorial candidates is expected.

A naive idea would be to try all directions defined by arbitrary real vectors or even discretize the unit sphere. That fails because the answer depends on exact supporting directions, not sampled ones. Another naive idea is to fix two points and assume the optimal planes are orthogonal to the line between them, but this is incorrect in three dimensions, since the optimal direction depends on an extreme configuration of the convex hull, not just pairs of points.

A subtle edge case appears when all points are coplanar. In that case, the answer is zero because we can choose planes coinciding with that plane. Any method relying on normalization of cross products must handle the zero-area degeneracy carefully.

Another edge case occurs when all points lie on a line. Then the optimal direction is exactly the line direction, and the answer is simply the length of the projection interval along that line.

## Approaches

The key observation is that the function we want to minimize, $f(\mathbf{u}) = \max_i (\mathbf{u} \cdot \mathbf{x}_i) - \min_i (\mathbf{u} \cdot \mathbf{x}_i)$, is determined entirely by the convex hull of the points. For a fixed direction, only points on the hull matter, since interior points never define extrema.
