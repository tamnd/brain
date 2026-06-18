---
title: "CF 106268J - ICPC Board"
description: "We are given a grid where each cell originally contained one of three letters: C, I, or P. Over time, some cells remain readable, while others are replaced by a wildcard character."
date: "2026-06-18T23:09:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106268
codeforces_index: "J"
codeforces_contest_name: "The 2025 Asia Yokohama Regional Contest"
rating: 0
weight: 106268
solve_time_s: 27
verified: false
draft: false
---

[CF 106268J - ICPC Board](https://codeforces.com/problemset/problem/106268/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid where each cell originally contained one of three letters: C, I, or P. Over time, some cells remain readable, while others are replaced by a wildcard character. The task is to reconstruct any full assignment of letters to all cells that is consistent with the observed grid and satisfies a global structural constraint.

The constraint is local and uniform: every 2 by 2 subgrid in the final assignment must contain exactly two Cs, one I, and one P. This is a very strong constraint because it fully determines how adjacent cells relate to each other. Any valid solution is essentially a tiling of the grid by a repeating pattern that respects all overlapping 2 by 2 windows simultaneously.

The output is either a rejection if no completion exists, or a fully filled grid that matches all given fixed letters and satisfies the 2 by 2 condition everywhere.

The constraints are large in aggregate, with up to 1000 rows and 1000 columns summed across test cases. This rules out any approach that explicitly checks all 2 by 2 subgrids with backtracking or tries arbitrary assignments per cell. The structure must instead be deduced globally in linear time per grid.

A subtle failure case appears when a naive checker attempts to fill greedily without enforcing consistency across overlapping 2 by 2 blocks. For example, if we locally satisfy one 2 by 2 block, we might break a neighboring one because each cell participates in up to four constraints.

The key difficulty is that the constraint couples all
