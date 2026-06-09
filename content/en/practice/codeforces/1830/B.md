---
title: "CF 1830B - The BOSS Can Count Pairs"
description: "The solution correctly generalizes the serial test from pairs to $k$-tuples by grouping the sequence into disjoint blocks of length $k$, ensuring independence under the null hypothesis."
date: "2026-06-09T07:12:26+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1830
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 875 (Div. 1)"
rating: 2000
weight: 1830
solve_time_s: 130
verified: false
draft: false
---

[CF 1830B - The BOSS Can Count Pairs](https://codeforces.com/problemset/problem/1830/B)

**Rating:** 2000  
**Tags:** brute force, math  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Correctness

The solution correctly generalizes the serial test from pairs to $k$-tuples by grouping the sequence into disjoint blocks of length $k$, ensuring independence under the null hypothesis. It correctly identifies that the counts of each possible $k$-tuple follow a multinomial distribution with $d^k$ categories and equal probabilities $1/d^k$ under uniformity. The application of the chi-square test to these counts is correct.

It also correctly notes the practical constraint that $d^k$ must not be too large relative to $n$, so that expected frequencies remain sufficient for the chi-square approximation.

## Gaps and Errors

1. **Justification of independence for disjoint $k$-tuples**: The solution implicitly assumes that the $Y_i$ are i.i.d. and therefore disjoint $k$-tuples are independent. This is correct but not explicitly stated. This is a **justification gap**, not a critical error.
2. **Clarity on sequence length**: The formula $(Y_{kj}, \ldots, Y_{kj+k-1})$ assumes the total number of terms used is exactly $kn$, which requires that the sequence length is at least $kn$. This is standard in TAOCP treatments but is not stated. This is a minor omission.
3. **No discussion of overlapping tuples**: The solution does not explicitly warn against using overlapping $k$-tuples, which would introduce dependence. Given the context of Exercise 3.3.2.1, a brief mention would improve completeness. This is a minor completeness gap.

Overall, these are minor omissions; the core method and reasoning are correct.

## Summary

The solution correctly generalizes the serial test to $k$-tuples, applies the chi-square test appropriately, and notes practical constraints on $d$ and $n$. Minor omissions in explicit statements about independence and sequence length do not affect correctness.

VERDICT: PASS - the solution correctly generalizes the serial test to $k$-tuples and identifies the chi-square procedure.
