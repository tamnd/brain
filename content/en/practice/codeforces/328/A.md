---
title: "CF 328A - IQ Test"
description: "We are given exactly four integers in a sequence, each between 1 and 1000. The goal is to determine whether this sequence forms an arithmetic progression or a geometric progression. If it does, we must compute the next element of the progression."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 328
codeforces_index: "A"
codeforces_contest_name: "Testing Round 8"
rating: 1800
weight: 328
solve_time_s: 71
verified: false
draft: false
---

[CF 328A - IQ Test](https://codeforces.com/problemset/problem/328/A)

**Rating:** 1800  
**Tags:** implementation  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given exactly four integers in a sequence, each between 1 and 1000. The goal is to determine whether this sequence forms an arithmetic progression or a geometric progression. If it does, we must compute the next element of the progression. If the sequence fits neither pattern, or if the next number would not be an integer, we return 42.

An arithmetic progression is defined by a constant difference between consecutive terms. For four elements $a_1, a_2, a_3, a_4$, the differences $a_2-a_1$, $a_3-a_2$, and $a_4-a_3$ must all be equal. A geometric progression is defined by a constant ratio between consecutive terms. For nonzero elements $b_1, b_2, b_3, b_4$, the ratios $b_2/b_1$, $b_3/b_2$, and $b_4/b_3$ must all be equal, and the ratio must not be 0 or 1.

The constraints are small: exactly four numbers, each bounded by 1 and 1000. This means any algorithm that checks differences or ratios with a few arithmetic operations will run instantly. The subtlety lies in edge cases, especially when ratios are not integers, sequences contain repeated numbers, or a naive division introduces floating-point errors.

Some non-obvious edge cases include sequences like [2, 2, 2, 2], which are both arithmetic and geometric, sequences where the arithmetic difference is negative, sequences like [1, 2, 4, 8] that are geometric with integer ratios, and sequences like [1, 3, 9, 28], which match neither. Also, sequences like [1, 2, 4, 8] will produce a next element 16, but a sequence like [1, 2, 4, 9] should return 42 because the ratio 9/4 is not equal to previous ratios.

## Approaches

The brute-force approach is simple: compute the consecutive differences for arithmetic and consecutive ratios for geometric. Check if all differences are equal or all ratios are equal. If one holds, compute the next element. If both fail, return 42. This works in constant time for four elements.

The naive implementation must handle integer arithmetic carefully. For geometric progressions, division must be exact. Using floating-point division is risky because 3/2 in Python is 1.5, and equality checks may fail due to rounding. We must check that each division produces an integer before comparing
