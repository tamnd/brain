---
title: "CF 1777F - Comfortably Numb"
description: "We are given a sequence of non-negative integers and asked to examine every contiguous segment. For each segment, we compute two values: the bitwise XOR of all elements in the segment, and the maximum element in that same segment."
date: "2026-06-09T11:40:36+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "divide-and-conquer", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1777
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 845 (Div. 2) and ByteRace 2023"
rating: 2400
weight: 1777
solve_time_s: 34
verified: false
draft: false
---

[CF 1777F - Comfortably Numb](https://codeforces.com/problemset/problem/1777/F)

**Rating:** 2400  
**Tags:** bitmasks, data structures, divide and conquer, strings, trees  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of non-negative integers and asked to examine every contiguous segment. For each segment, we compute two values: the bitwise XOR of all elements in the segment, and the maximum element in that same segment. The “numbness” of the segment is defined as the XOR of these two values.

The task is to find the maximum possible numbness over all subarrays.

The constraints imply that the array size over all test cases is at most 2⋅10^5, so any solution with quadratic behavior per test case is impossible. A direct O(n^2) enumeration of subarrays, combined with O(1) or even O(log n) per query, would still be too slow in the worst case since it leads to roughly 2⋅10^10 subarrays across all tests.

The difficulty comes from the interaction of two global subarray statistics: XOR and maximum. XOR behaves nicely under prefix operations, while maximum does not. This mismatch is the core obstacle.

A naive implementation would also fail in subtle ways if it tries to “optimize” by fixing endpoints or greedily expanding subarrays, because increasing the maximum often changes the XOR structure in non-monotonic ways.

For example, consider `[1, 2, 3]`. The subarray `[2, 3]` has max 3 and XOR 1, giving 3 ⊕ 1 = 2. Extending to `[1, 2, 3]` increases max to 3 but XOR becomes 0, giving 3 ⊕ 0 = 3. Shrinking to `[3]` gives 3 ⊕ 3 = 0. There is no monotonic relationship between subarray size and result, so any greedy strategy based on expansion or fixed maxima fails.

## Approaches

The brute-force approach enumerates all subarrays, computes their XOR and maximum, and tracks the best result. With prefix XOR, the XOR part is O(1), but the maximum still costs O(n) unless preprocessed. Even with a sparse table, preprocessing helps queries, but we still have O(n^2) subarrays, which is far beyond limits.

The key structural insight is to reverse the perspective: instead of iterating over subarrays and computing maximum, we fix a candidate value for the maximum and only consider subarrays where that value is the maximum. If we knew that a subarray’s maximum equals some value x, then every element in the subarray is at most x, and at least one element equals x. This suggests splitting the array around positions where elements exceed x.

This leads to a standard divide-and-conquer idea over the maximum value. We recursively split the array by its global maximum position. Any subarray that does not include that maximum belongs entirely to one side, and any subarray that includes it must treat it as the maximum constraint anchor.

For a fi
