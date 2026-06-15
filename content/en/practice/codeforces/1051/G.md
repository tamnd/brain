---
title: "CF 1051G - Distinctification"
description: "We are given a growing sequence of points on the integer line. Each point has a position value and a weight. As we reveal more points one by one, we want to maintain a configuration where all positions are distinct, but we are allowed to move points left or right using very…"
date: "2026-06-15T10:59:54+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1051
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 51 (Rated for Div. 2)"
rating: 2900
weight: 1051
solve_time_s: 219
verified: false
draft: false
---

[CF 1051G - Distinctification](https://codeforces.com/problemset/problem/1051/G)

**Rating:** 2900  
**Tags:** data structures, dsu, greedy  
**Solve time:** 3m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a growing sequence of points on the integer line. Each point has a position value and a weight. As we reveal more points one by one, we want to maintain a configuration where all positions are distinct, but we are allowed to move points left or right using very specific rules that depend on whether collisions exist.

A move that shifts a point to the right is only allowed if that point currently shares its position with at least one other point. This move increases the position and costs its weight. A move that shifts a point to the left is only allowed if the point sits immediately to the right of some other point, and this move decreases the position with a negative cost, effectively giving a reward proportional to its weight.

The goal for each prefix is to end up in a state where no two points share the same position, while minimizing the total accumulated cost of all moves.

The important structural interpretation is that collisions at a coordinate act like a "resource pool". If multiple points sit at the same value, we can redistribute them left or right, and the cost of doing so depends only on which point is moved, not where it ends up. Because left moves require a supporting neighbor one unit below, and right moves require duplicates, the system behaves like a flow on an integer line where weights control transfer incentives.

The input size reaches two hundred thousand elements, which rules out any solution that repeatedly simulates moves or maintains explicit sets of collisions per prefix with quadratic repair. Any approach that tries to resolve conflicts greedily per prefix in linear scan per element would degenerate into quadratic behavior and fail.

A subtle edge case appears when multiple identical positions exist and weights differ significantly. For example, if several points share value 5 but one has a very large weight and others small weights, moving the wrong element first can change the total cost dramatically because increases cost positive and decreases give negative contribution. A naive greedy strategy that resolves duplicates arbitrarily fails here, since optimal behavior depends on global ordering by weights, not by arrival order.

## Approaches

The core difficulty is that duplicates at the same position must be resolved, but every resolution move carries asymmetric cost tied to
