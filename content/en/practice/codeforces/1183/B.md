---
title: "CF 1183B - Equalize Prices"
description: "We are given a list of prices for products in a shop, and the shop owner wants to make all prices equal. The catch is that each price can only be adjusted by at most k units up or down, and the new price must remain positive."
date: "2026-06-12T01:22:18+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 900
weight: 1183
solve_time_s: 152
verified: false
draft: false
---

[CF 1183B - Equalize Prices](https://codeforces.com/problemset/problem/1183/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of prices for products in a shop, and the shop owner wants to make all prices equal. The catch is that each price can only be adjusted by at most `k` units up or down, and the new price must remain positive. We are asked to determine the largest integer price `B` that all products can share after adjustment, or report that it is impossible.

Each query provides `n`, the number of products, and `k`, the maximum allowed change for each product. Then we get the current prices `a_1, a_2, ..., a_n`. The output for a query is a single integer: the maximum `B` that satisfies `|a_i - B| ≤ k` for every `i`, or `-1` if no such `B` exists.

Given the constraints, `n` can go up to 100 and `k` up to 10^8. This suggests that an O(n) solution per query is sufficient, since even in the worst case, 100 queries of 100 products is only 10,000 operations. There is no need for heavy optimization beyond simple arithmetic comparisons.

The key edge cases include situations where the prices are widely spread compared to `k`. For example, if prices are `[1, 6]` and `k = 2`, then no single price `B` can satisfy both `|1 - B| ≤ 2` and `|6 - B| ≤ 2`. Another edge case is when all prices are equal, in which case the original price itself is the maximum valid `B`.

## Approaches

A brute-force approach would attempt every integer candidate `B` from 1 up to the largest price plus `k`. For each candidate, we would check all prices to see if they can be adjusted to `B`. This is correct, but inefficient: in the worst case `B` could be as large as 10^8 and iteratin
