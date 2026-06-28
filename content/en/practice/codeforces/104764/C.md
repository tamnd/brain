---
title: "CF 104764C - An Odd Meal"
description: "We are given a sequence of integers representing how many jellyfish Sally eats each minute. From this sequence we want to choose a contiguous block of minutes such that the total number of jellyfish eaten in that block is odd, and among all such blocks we want the maximum…"
date: "2026-06-28T20:10:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 35
verified: false
draft: false
---

[CF 104764C - An Odd Meal](https://codeforces.com/problemset/problem/104764/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers representing how many jellyfish Sally eats each minute. From this sequence we want to choose a contiguous block of minutes such that the total number of jellyfish eaten in that block is odd, and among all such blocks we want the maximum possible length. If no contiguous block has an odd sum, the answer is -1.

The key object is a subarray, and its value is the parity of its sum. We are not asked for the maximum sum or minimum length, only whether the sum is odd and how long the interval can be.

The constraint $N \le 2 \cdot 10^5$ implies we need at least linear or near-linear time. Any approach that checks all subarrays explicitly would require $O(N^2)$ intervals and is too slow. Since each subarray sum must be evaluated, a naive prefix-sum double loop leads to about $2 \cdot 10^{10}$ operations in the worst case, which is infeasible.

A subtle point is that the values $j_i$ can be large, up to $10^9$, but only parity matters. Another important edge case is when all numbers are even, because then every subarray sum is even and the answer must be -1.

A common mistake is to think we must find a specific segment with odd sum and then optimize it, but the parity structure makes the problem much simpler than general subarray problems.

## Approaches

A brute-force solution enumerates every subarray $[l, r]$, computes its sum, and checks whether it is odd. Even with prefix sums, each check is $O(1)$, but there are $O(N^2)$ subarrays. For $N = 2 \cdot 10^5$, this is far too slow.

The key observation is that we only care about whether a subarray sum is odd. A sum is odd exactly when the number of odd elements inside it is odd. This reduces the problem to reasoning about parity structure instead of exact values.

Let us define prefix parity $p[i]$ as the parity of the sum of the first $i$ elements. Then the sum of a subarray $[l, r]$ is odd exactly when $p[r] \neq p[l-1]$. So we need two indices with different prefix parity.

To maximize the length of such a subarray, we want two positions $l-1$ and $r$ with different parity that are as far apart as possible. This means we should pair the earliest occurrence of one parity with the latest occurrence of the opposite parity.

We can simplify further: since prefix parity is either 0 or 1, we just need the first and last occurrence of each parity among prefix positions. The optimal answer is the maximum distance between a prefix index with parity 0 and one with parity 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(1)$ | Too slow |
| Prefix parity extremes | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute prefix parity while scanning the array from left to right. We maintain a running parity variable that flips whenever we see an odd number. This encodes the parity of every prefix sum without storing full sums.
2. Track the first position where each parity value appears. We store two values: first index
