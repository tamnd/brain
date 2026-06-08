---
title: "CF 1923F - Shrink-Reverse"
description: "We are given a binary string s of length n and a number k representing the maximum number of allowed operations. Each operation can either swap two characters of the string or remove all leading zeros and then reverse the string."
date: "2026-06-08T19:13:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "hashing", "implementation", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 1923
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 162 (Rated for Div. 2)"
rating: 2800
weight: 1923
solve_time_s: 43
verified: false
draft: false
---

[CF 1923F - Shrink-Reverse](https://codeforces.com/problemset/problem/1923/F)

**Rating:** 2800  
**Tags:** binary search, brute force, greedy, hashing, implementation, string suffix structures, strings  
**Solve time:** 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string `s` of length `n` and a number `k` representing the maximum number of allowed operations. Each operation can either swap two characters of the string or remove all leading zeros and then reverse the string. The task is to perform at most `k` operations to minimize the integer value of the string when interpreted as a binary number.

The input size is large, up to 500,000 characters, which immediately rules out any approach that tries every possible sequence of operations. A naive approach that simulates all swaps or all sequences of SHRINK-REVERSE operations would explode combinatorially.

Non-obvious edge cases arise when zeros are already at the front, when the string is mostly zeros except for one or two ones, or when SHRINK-REVERSE actually increases the leading zeros in a way that helps a swap later. For instance, for `s = "1000"` and `k = 1`, a naive implementation that always does SHRINK-REVERSE first might miss that swapping the trailing '1' to the end would have produced a smaller value. The algorithm must carefully decide when swaps versus SHRINK-REVERSE give the maximal reduction in value.

The key insight is that the SHRINK-REVERSE operation affects the leading zeros, and swaps only matter for moving ones toward the right to minimize the overall binary value.

## Approaches

The brute-force approach would attempt all sequences of up to `k` operations, simulating swaps between every pair of indices and applying SHRINK-REVERSE anywhere. This approach is correct in principle because it explores every possible outcome, but it is hopelessly slow. For a string of length `n`, there are roughly $O(n^2)$ swaps per operation, and doing this `k` times gives $O(n^{2k})$ complexity. With `n = 5 * 10^5`, even a single swap loop is infeasible.

The key insight is that the operations interact in a predictable way. Swaps that bring ones closer to the end of the string always decrease the integer value, and SHRINK-REVERSE moves trailing zeros to the front after removing leading zeros. This means we can treat the problem as moving two ones: one to the very front and one to the very end, with a limited number of swaps. The remaining string after moving these ones will contribute minimally to the value because the ones are pushed to extremities.

This observation reduces the problem to considering at most two targeted swaps, possibly combined with SHRINK-REVERSE, and computing the resulting value. Everything else can be done greedily. We only need to examine the first and last ones and zeros to decide the optimal swaps, which gives a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^{2k}) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the first `1` in the string `s` and the last `1`. These are the only characters whose positions directly influence the pot
