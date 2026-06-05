---
title: "CF 293D - Ksusha and Square"
description: "We are given a convex polygon whose vertices have integer coordinates. Consider every lattice point, meaning every point with integer coordinates, that lies inside the polygon or on its boundary."
date: "2026-06-05T17:22:49+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math", "probabilities", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 293
codeforces_index: "D"
codeforces_contest_name: "Croc Champ 2013 - Round 2"
rating: 2700
weight: 293
solve_time_s: 43
verified: false
draft: false
---

[CF 293D - Ksusha and Square](https://codeforces.com/problemset/problem/293/D)

**Rating:** 2700  
**Tags:** geometry, math, probabilities, two pointers  
**Solve time:** 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a convex polygon whose vertices have integer coordinates. Consider every lattice point, meaning every point with integer coordinates, that lies inside the polygon or on its boundary.

Among all unordered pairs of distinct lattice points, we choose one pair uniformly at random. Those two points become opposite corners of a square. The task is to compute the expected area of that square.

The geometry of the square is actually the easy part. If two points are opposite vertices of a square and the diagonal length is $d$, then the side length is $d/\sqrt 2$, so the area is

$$\frac{d^2}{2}.$$

The entire problem becomes:

\mathbb E[\text{area}] = \frac12 \cdot \mathbb E[\text{squared distance be]()
