---
title: "CF 351A - Jeff and Rounding"
description: "We are given 2 n real numbers representing Jeff's birthday gifts. Jeff dislikes fractional numbers, so he performs n pairwise operations to \"adjust\" the numbers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 351
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 204 (Div. 1)"
rating: 1800
weight: 351
solve_time_s: 97
verified: false
draft: false
---

[CF 351A - Jeff and Rounding](https://codeforces.com/problemset/problem/351/A)

**Rating:** 1800  
**Tags:** dp, greedy, implementation, math  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given 2 _n_ real numbers representing Jeff's birthday gifts. Jeff dislikes fractional numbers, so he performs _n_ pairwise operations to "adjust" the numbers. In each operation, he selects two distinct numbers that have not been used before, rounds one down to the nearest integer, and rounds the other up to the nearest integer. After all operations, we want the absolute difference between the sum of the original numbers and the sum of the adjusted numbers to be as small as possible.

Each number has exactly three decimal places. The number of operations is _n_, so all 2 _n_ numbers are used exactly once. The bounds (1 ≤ _n_ ≤ 2000, numbers up to 10⁴) suggest we need a solution roughly O(n log n) or O(n) to run comfortably within a 1-second limit, because naive exploration of all pairing combinations would be factorial in complexity and impossible for n = 2000.

Edge cases arise from numbers that are already integers. If a number is already an integer, rounding it either down or up does not change it. For example, if the input is `1.000 2.000`, the optimal difference is `0.000`. Another tricky case is numbers whose fractional parts sum to a non-integer value, because naive rounding without pairing could lead to an unnecessarily large difference. For instance, `0.500 0.500` rounded both up would yield a sum difference of `1.000`, whereas rounding one down and one up yields `0.000`.

## Approaches

A brute-force approach would attempt all possible pairings of 2 _n_ numbers and for each pair choose which to round up and which to round down, computing the resulting sum difference. This is correct in principle, but the number of pairings grows factorially, around (2 *n)!/(n! 2^n), which is astronomically large for n = 2000. This approach is thus impractical.

The key observation is that the absolute difference only depends on the fractional parts of the numbers. Rounding an integer does not contribute to the difference. For non-integers, rounding down loses the fractional part, rounding up adds `1 - fractional part` to the sum. The goal is to pair numbers so that the total sum difference is minimized. It turns out that if we count how many numbers are non-integer (say `m` numbers), the sum of fractional parts tells us the total "adjustment needed" if we round all down versus some up. To minimize the absolute difference, we should round exactly half of the non-integer numbers up and half down (since each operation affects two numbers), which effectively balances the positive and negative contributions. Sorting the fractional parts allows us to select the smallest contributions for rounding up and down efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)!/(n!2^n)) | O(2n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the list of 2 _n_ numbers.
2. Compute the sum of the original numbers; store it as `original_sum`.
3. Separate numbers into two categories: integers and non-integers. For each non-integer number, store its fractional part (`x - floor(x)`).
4. Count the total number of non-integers, which we call `m`. For the absolute difference to be minimized, the number of numbers we round up should be `m // 2` (since each operation pairs one number up and one down).
5. Sort the fractional parts of non-integers in ascending order.
6. Round down the `m // 2` largest fractional parts and round up the remaining `m - m // 2`. This ensures the sum difference is minimized.
7. Compute the adjusted sum: integers remain the same; numbers rounded down contribute floor(x); numbers rounded up contribute ceil(x).
8. Compute the absolute difference between `original_sum` and `adjusted_sum`.
9. Print the difference formatted to exactly three decimal places.

**Why it works:** The invariant is that each operation must round one number down and one number up. Since the difference from original values depends only on the fractional part,
