---
title: "CF 1493D - GCD of an Array"
description: "We are given an array of integers, and we need to handle a sequence of queries where each query multiplies a specific element of the array by a given factor. After each query, we must compute the greatest common divisor (GCD) of the entire array modulo $10^9+7$."
date: "2026-06-10T22:15:06+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "hashing", "implementation", "math", "number-theory", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1493
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 705 (Div. 2)"
rating: 2100
weight: 1493
solve_time_s: 52
verified: false
draft: false
---

[CF 1493D - GCD of an Array](https://codeforces.com/problemset/problem/1493/D)

**Rating:** 2100  
**Tags:** brute force, data structures, hashing, implementation, math, number theory, sortings, two pointers  
**Solve time:** 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we need to handle a sequence of queries where each query multiplies a specific element of the array by a given factor. After each query, we must compute the greatest common divisor (GCD) of the entire array modulo $10^9+7$. The input array can be up to $2 \cdot 10^5$ elements, and there can be as many queries. The numbers involved, including the multipliers, are also up to $2 \cdot 10^5$.

A naive solution would recompute the GCD from scratch after each query, which requires iterating through the entire array every time. With $n$ and $q$ potentially both $2 \cdot 10^5$, this would result in $O(nq) \approx 4 \cdot 10^{10}$ operations, far beyond the 2-second limit. We therefore need a faster way that avoids recomputing the full GCD repeatedly.

Non-obvious edge cases include arrays where some elements are equal to 1, or arrays where multiple elements share only part of their prime factorization. For instance, if the array is $[2, 3, 5]$ and we multiply the first element by 3, the GCD changes from 1 to 1. A naive implementation may fail if it assumes multiplying any element always increases the GCD.

We also must consider modulo arithmetic carefully. The GCD itself is computed over integers, but the final output is required modulo $10^9+7$. Careless application of modulo before computing prime factor contributions can yield wrong answers.

## Approaches

The brute-force approach iterates through the array after each query, computing the GCD of all elements. This is correct because the GCD is associative, and iterating over all elements gives the correct result. However, with $n$ and $q$ up to $2 \cdot 10^5$, the worst-case operation count is $O(nq) = 4 \cdot 10^{10}$, which is far too slow for 2 seconds.

The key observation is that the GCD of a set of numbers is determined entirely by their prime factorizations. We can represent the
