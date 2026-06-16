---
title: "CF 1041C - Coffee Break"
description: "We are given a set of moments inside a working day when Monocarp is willing to drink coffee. Each moment is a specific minute inside a day that lasts from minute 1 to minute m."
date: "2026-06-16T18:00:26+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1041
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 509 (Div. 2)"
rating: 1600
weight: 1041
solve_time_s: 276
verified: false
draft: false
---

[CF 1041C - Coffee Break](https://codeforces.com/problemset/problem/1041/C)

**Rating:** 1600  
**Tags:** binary search, data structures, greedy, two pointers  
**Solve time:** 4m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of moments inside a working day when Monocarp is willing to drink coffee. Each moment is a specific minute inside a day that lasts from minute 1 to minute m. Every coffee break must be assigned to a working day, and multiple breaks may go to the same day, but only if they are sufficiently far apart in time within that day. The constraint is that if two breaks happen on the same day, the difference between their minutes must be at least d.

We are not assigning arbitrary schedules, we are partitioning a fixed set of time points into several sequences, each sequence representing a day, and each sequence must respect a minimum gap constraint between consecutive chosen times. The objective is to minimize how many such sequences are needed.

The key constraint is n up to 200000, which forces an O(n log n) or O(n) approach. Anything that repeatedly scans already assigned breaks or tries to simulate day by day greedily without structure will degenerate to O(n²) in the worst case and fail.

A
