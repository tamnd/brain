---
title: "CF 1550C - Manhattan Subarrays"
description: "We are asked to count subarrays of an array that avoid a specific geometric degeneracy. Each element in the array represents the x-coordinate of a point, while its index in the array is treated as the y-coordinate."
date: "2026-06-10T13:26:49+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1550
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 111 (Rated for Div. 2)"
rating: 1700
weight: 1550
solve_time_s: 166
verified: false
draft: false
---

[CF 1550C - Manhattan Subarrays](https://codeforces.com/problemset/problem/1550/C)

**Rating:** 1700  
**Tags:** brute force, geometry, greedy, implementation  
**Solve time:** 2m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count subarrays of an array that avoid a specific geometric degeneracy. Each element in the array represents the x-coordinate of a point, while its index in the array is treated as the y-coordinate. A triple of points is called bad if one point lies exactly on the Manhattan path connecting the other two, that is, the distance from the first to the third equals the sum of distances through the second. A subarray is good if it contains no bad triple.

Arrays of length one or two are automatically good because three distinct indices are required to form a bad triple. The challenge lies in efficiently counting good subarrays for lengths three or more, across arrays of length up to 200,000 with up to 5000 test cases. This rules out any algorithm with worst-case complexity above roughly O(n) per test case because O(n²) operations could reach 4·10¹⁰, which is infeasible in two seconds.

A subtle edge case arises when consecutive elements form a monotone sequence. Consider the array `[1, 2, 3, 4]`. The triple `(1, 2, 3)` forms a bad triple because each point lies on the Manhattan path connecting the others along the diagonal. Any careless solution that simply counts subarrays without checking adjacency could incorrectly include such sequences as good. Another edge case is arrays with repeating elements, for instance `[5, 5, 5]`. Here,
