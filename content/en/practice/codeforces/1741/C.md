---
title: "CF 1741C - Minimize the Thickness"
description: "We are given an array of positive integers and asked to partition it into consecutive segments such that all segments have the same sum. Each segment must be contiguous, and each element belongs to exactly one segment."
date: "2026-06-09T16:25:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1741
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 826 (Div. 3)"
rating: 1100
weight: 1741
solve_time_s: 159
verified: false
draft: false
---

[CF 1741C - Minimize the Thickness](https://codeforces.com/problemset/problem/1741/C)

**Rating:** 1100  
**Tags:** brute force, greedy, math, two pointers  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers and asked to partition it into consecutive segments such that all segments have the same sum. Each segment must be contiguous, and each element belongs to exactly one segment. The thickness of a split is the length of the largest segment, and the goal is to minimize this thickness.

The constraints are moderate: the array length per test case is at most 2000, and the total across all test cases is also bounded by 2000. This allows an algorithm with worst-case time complexity around $O(n^2)$ per test case, since $2000^2$ operations are acceptable within a 2-second limit.

Non-obvious edge cases include arrays that cannot be split evenly except by taking the entire array as one segment, for example, an array like `[10, 23, 7,
