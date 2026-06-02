---
title: "CF 185E - Soap Time! - 2"
description: "We are given a set of dwarves located at integer coordinates on a Cartesian plane, and optionally a set of subway stations also at integer coordinates."
date: "2026-06-03T00:57:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 185
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 118 (Div. 1)"
rating: 3000
weight: 185
solve_time_s: 23
verified: false
draft: false
---

[CF 185E - Soap Time! - 2](https://codeforces.com/problemset/problem/185/E)

**Rating:** 3000  
**Tags:** binary search, data structures  
**Solve time:** 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of dwarves located at integer coordinates on a Cartesian plane, and optionally a set of subway stations also at integer coordinates. Each dwarf can move one unit in the four cardinal directions per second, but they can also teleport instantly between any subway stations. The dwarves want to gather at a single integer coordinate in the plane, and the goal is to compute the minimum number of seconds required for all dwarves to reach that gathering point if they move optimally.

The input specifies the number of dwarves, the number of subway stations, and the coordinates of all dwarves and stations. The output is a single integer representing the minimum gathering time.

Given that the number of dwarves and subway stations can be up to 100,000 and the coordinate range extends up to 10^8 in each direction, we cannot consider all possible gathering points explicitly. A brute-force search over every integer point is infeasible because the grid is far too large. We need an approach that leverages properties of distances and the subway system to reduce the search space efficiently.

Edge cases include the absence of subway stations, a single dwarf, or multiple dwarves all starting at the same point. In the simplest case, if there are no stations and all dwarves are already together, the answer is zero. A naive approach that ignores subway stations or fails to compute distances correctly will give wrong answers on these small or degenerate cases.

## Approaches

A brute-force approach would iterate over every integer coordinate in the bounding box of dwarves and stations, compute the maximum time any dwarf needs to reach that point (either walking directly or using the subway optimally), and pick the minimum. This approach is correct but computationally impossible. Even restricting to the convex hull of dwarves would still be too slow because distances can span up to 2×10^8 and dwarves can be far apart.

The key observation is that the Manhattan distance can be separated along the x and y axes. This reduces the problem to one-dimensional distance calculations along each axis independently. The subway network effectively allows dwarves to “teleport” to one of the stations, so for each dwarf, the minimum time to a gathering point is the minimum of the direct Manhattan distance to that point and the distance to the nearest subway station plus the distan
