---
title: "CF 104797H - Radar"
description: "We are given a radar system that produces a finite set of scanned points in the plane. Each scanned point is formed by choosing a direction and a distance from the origin, then going that distance along that direction."
date: "2026-06-28T13:45:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104797
codeforces_index: "H"
codeforces_contest_name: "2021-2022 ICPC Central Europe Regional Contest (CERC 21)"
rating: 0
weight: 104797
solve_time_s: 31
verified: false
draft: false
---

[CF 104797H - Radar](https://codeforces.com/problemset/problem/104797/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a radar system that produces a finite set of scanned points in the plane. Each scanned point is formed by choosing a direction and a distance from the origin, then going that distance along that direction.

Concretely, the input provides a list of radii and a list of directions. Each direction comes from a non-zero vector, meaning it defines a ray starting at the origin. For every radius and every direction, the radar produces a point located exactly at that radius along that ray. So the scanned set is all points of the form $r \cdot \frac{v}{\|v\|}$, where $r$ is from the radius list and $v$ is one of the direction vectors.

Then we are given query points in the plane, and for each one we must compute the Euclidean distance to the closest scanned point.

The constraints are tight: up to $10^5$ radii, $10^5$ directions, and $10^5$ queries. A naive construction of all scanned points would create up to $10^{10}$ points, which is completely infeasible. Even iterating over all combinations per query would be far beyond time limits.

The output requires high precision, so the solution must avoid unstable geometric shortcuts and instead rely on stable algebraic reductions.

A subtle issue arises from geometry degeneracy. For example, if a query lies exactly on one of the rays and its distance matches a radius, the answer is zero. Another issue is angular wrap-around: directions near 0 degrees and 360 degrees must be considered adjacent when searching for closest direction.

## Approaches

A brute-force approach would explicitly generate every scanned point and, for each query point, compute the minimum Euclid
