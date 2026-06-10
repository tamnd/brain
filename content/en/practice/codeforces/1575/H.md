---
title: "CF 1575H - Holiday Wall Ornaments"
description: "We are given a binary string representing a wall, where each character is either 0 or 1. This string, a, is of length n. Mr. Chanek wants to place his nephew’s favorite pattern, another binary string b of length m, onto the wall."
date: "2026-06-10T10:55:50+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "H"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2200
weight: 1575
solve_time_s: 37
verified: false
draft: false
---

[CF 1575H - Holiday Wall Ornaments](https://codeforces.com/problemset/problem/1575/H)

**Rating:** 2200  
**Tags:** dp, strings  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string representing a wall, where each character is either 0 or 1. This string, `a`, is of length `n`. Mr. Chanek wants to place his nephew’s favorite pattern, another binary string `b` of length `m`, onto the wall. The task is to determine, for every possible number of occurrences `k` from `0` to `n - m + 1`, the minimal number of flips in `a` needed to achieve exactly `k` occurrences of `b` as a contiguous substring.

The input strings are small enough that brute-force string matching could theoretically work, but we also have to compute minimal flips for each `k`. Each flip changes a single character in `a`, and substrings can overlap. The constraints `1 ≤ m ≤ n ≤ 500` imply that any solution worse than `O(n^3)` would likely be too slow, since `500^3` is already 125 million operations, which might push the time limit if the inner steps are non-trivial.

Edge cases arise when `b` has repetitive characters like `111` or `000`, or when `a` already contains overlapping occurrences of `b`. For example, if `a = 11111` and `b = 111`, then occurrences overlap: positions 0-2, 1-3, 2-4. A naive counting method that only looks at non-overlapping matches would produce incorrect results. Another edge case is when `k` is impossible due to string length constraints or overlapping structure, which must return `-1`.

## Approaches

A brute-force method would consider every subset of positions in `a` to flip and count the occurrences of `b` afterward. This approach is correct in principle, because it explores all possible ways to reach each `k`. However, with up to 500 positions, the number of subsets grows exponentially (`2^500`), so brute-force is completely impractical.

The key insight is that overlapping occurrences and character flips suggest dynamic programming. We can model the problem as iterati
