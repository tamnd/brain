---
title: "CF 1763D - Valid Bitonic Permutations"
description: "We are asked to count the number of permutations of the numbers from 1 to n that are bitonic and satisfy two fixed positions. A bitonic permutation is one that strictly increases up to a certain peak index, then strictly decreases afterward."
date: "2026-06-09T13:36:57+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1763
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 840 (Div. 2) and Enigma 2022 - Cybros LNMIIT"
rating: 2200
weight: 1763
solve_time_s: 70
verified: false
draft: false
---

[CF 1763D - Valid Bitonic Permutations](https://codeforces.com/problemset/problem/1763/D)

**Rating:** 2200  
**Tags:** combinatorics, dp, implementation, math, number theory  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of permutations of the numbers from 1 to n that are **bitonic** and satisfy two fixed positions. A bitonic permutation is one that strictly increases up to a certain peak index, then strictly decreases afterward. For each test case, the input provides positions `i` and `j` along with the numbers `x` and `y` that must occupy those positions. The output is the number of bitonic permutations that respect these constraints, modulo $10^9 + 7$.

The constraints allow up to 100 test cases with `n` up to 100. This rules out generating all permutations explicitly since n! grows rapidly, even for n = 15 the number of permutations exceeds 10^12. We need a combinatorial approach rather than brute-force enumeration.

Non-obvious edge cases include situations where the peak of the bitonic permutation is forced to be before or after one of the fixed positions, which can make the count zero. For example, if `i = 1` with `x` equal to the largest number, it cannot be part of an increasing prefix, so no valid bitonic permutation exists. Another tricky case is when the two fixed numbers `x` and `y` force contradictory conditions on the peak; for instance, if `x < y` but `i > j`, then `x` would have to appear before `y` in a decreasing sequence, which is impossible.

## Approaches

The **naive approach** is to generate all n! permutations and count those that are bitonic and satisfy the constraints. This works for n ≤ 6 but fails even for n = 10 due to factorial growth. The reason it is correct is simple: you can explicitly verify the permutation shape and fixed positions. It fails for larger n because 100! operations is completely infeasible.

The **key insight** is that we do not need to generate permutations. Once we fix the peak of the bitonic array, the left side must contain all numbers smaller than the peak in strictly increasing order, and the right side all numbers smaller than the peak in strictly decreasing order. By considering the peak as a variable and splitting the array into "left of peak" and "right of peak", we can model the problem combinatorially. The counts reduce to **combinations** of how to distribute numbers smaller or larger than the peak across the two segments. The constraints `B_i = x` and `B_j = y` allow us to prune impossible configurations immediately.

The observation that each side of the peak is fully determined by which numbers go there lets us compute the answer efficiently using factorials and combinations, rather than iterating through permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Combinatorial / Factorials | O(n^2) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo $10^9 + 7$ up to n = 100. These will allow us to calculate combinations efficiently.
2. For each test case, initialize a counter for valid bitonic permutations.
3. Iterate through all possible peak positions `k` from 1 to n. The peak value must satisfy `1 ≤ peak ≤ n` and cannot coincide with other fixed numbers unless one of the fixed positions is exactly at `k`.
4. Check if either of the fixed positions `i` or `j` lies before, at, or after the peak. If `i` is before the peak, `B_i = x` must be less than the peak. If `i` is after the peak, `B_i = x` must be less than the peak but occupy a position in the decreasing segment. If `i = k`, then `x` must equal the peak. Apply the same logic for `j` and `y`. If these conditions fail, skip this peak.
5. Count how many numbers are smaller than the peak and how many are larger. Let `a` numbers go to the left (increasing) and `b
