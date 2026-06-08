---
title: "CF 1882D - Tree XOR"
description: "We have a tree where each vertex contains a number. After choosing a root, we may repeatedly pick a vertex and XOR every value inside its subtree by some non-negative integer c. Applying such a spell costs (subtree size) × c."
date: "2026-06-08T22:35:30+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dfs-and-similar", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1882
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 899 (Div. 2)"
rating: 1900
weight: 1882
solve_time_s: 47
verified: false
draft: false
---

[CF 1882D - Tree XOR](https://codeforces.com/problemset/problem/1882/D)

**Rating:** 1900  
**Tags:** bitmasks, dfs and similar, dp, greedy, trees  
**Solve time:** 47s  
**Verified:** no  

## Solution
## Problem Understanding

We have a tree where each vertex contains a number. After choosing a root, we may repeatedly pick a vertex and XOR every value inside its subtree by some non-negative integer `c`.

Applying such a spell costs

`(subtree size) × c`.

For every possible choice of root, we must find the minimum total cost needed to make all vertex values equal.

The root matters because the notion of a subtree changes when the tree is rooted differently. The same edge can separate the tree into different parent-child relationships depending on the chosen root, so the optimal cost is generally different for different roots.

The constraints are large. Across all test cases, the total number of vertices is at most `2 · 10^5`. Any solution that recomputes the answer independently for every root would require roughly `O(n^2)` work in the worst case, which is far beyond what fits into a 3 second limit. We need something close to linear time per test case.

A subtle point is that the final common value is not f
