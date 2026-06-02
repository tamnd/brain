---
title: "CF 190D - Non-Secret Cypher"
description: "We are given a sequence of integers and a threshold value $k$. The task is to count how many contiguous subarrays contain some value that appears at least $k$ times inside that subarray."
date: "2026-06-03T01:19:49+07:00"
tags: ["codeforces", "competitive-programming", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1900
weight: 190
solve_time_s: 24
verified: false
draft: false
---

[CF 190D - Non-Secret Cypher](https://codeforces.com/problemset/problem/190/D)

**Rating:** 1900  
**Tags:** two pointers  
**Solve time:** 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers and a threshold value $k$. The task is to count how many contiguous subarrays contain some value that appears at least $k$ times inside that subarray.

Equivalently, for every segment of the array, we are checking whether there exists an element whose frequency inside that segment reaches $k$, and we want to count all segments where this happens.

The constraints are large: $n \le 4 \cdot 10^5$. Any approach that examines all subarrays explicitly is immediately too slow because the number of subarrays is $O(n^2)$, which reaches about $8 \cdot 10^{10}$ in the worst case. Even linear scans per subarray are impossible. This forces us into a linear or near-linear two pointers or offline counting strategy.

A subtle edge case appears when $k = 1$. In this case every subarray is valid, because any element already appears at least once. For example, for array $[5, 7, 5]$, every subarray qualifies and the answer is $\frac{n(n+1)}{2} = 6$. A naive implementation that assumes it must track repeated occurrences might still work, but it often overcomplicates this trivial case.

Another corner case happens when all elements are distinct and $k \ge 2$. For example, $[1, 2, 3, 4]$ with $k = 2$ has answer $0$. Many incorrect
