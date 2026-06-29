---
title: "CF 104687B - \u041e\u0442\u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We are given a sequence of integers and we are allowed to reorder it. After reordering, we compute the total “adjacent difference cost”, defined as the sum of absolute differences between every pair of consecutive elements in the array."
date: "2026-06-29T08:45:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 24
verified: false
draft: false
---

[CF 104687B - \u041e\u0442\u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/104687/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers and we are allowed to reorder it. After reordering, we compute the total “adjacent difference cost”, defined as the sum of absolute differences between every pair of consecutive elements in the array.

The task is to choose an ordering that produces a meaningful result, and then output that value after the array has been sorted in non-decreasing order. So the process is fixed: sort first, then compute the sum of absolute differences between neighbors.

The input size is very small, with at most 100 elements. This immediately removes any concern about heavy optimization or advanced data structures. Even quadratic or cubic solutions would be acceptable, since 100² is only 10⁴ operations.

A naive pitfall is to assume we are allowed to choose any permutation to minimize or maximize the expression. For example, given input `[3, 1, 2]`, one might think different reorderings change the final answer. But the problem explicitly fixes the rule: we must sort first, so all permutations collapse into a single deterministic array.

Another potential mistake is to misunderstand whether sorting is part of the output or just a preprocessing step. The correct interpretation is that sorting is mandatory before computing the sum.

Edge cases are mostly trivial but still worth noting:

For a single-element array, which is excluded by constraints here but useful conceptually, there would be no adjacent pairs, so the sum is zero.

For already sorted input like `1 2 3 4`, the computation is straightforward: differences are all positive consecutive gaps.

For reverse sorted input like `4 3 2 1`, sorting changes it into the same increasing sequence, so both cases produce identical results after sorting.

## Approaches

A brute-force misunderstanding would be to try all permutations of the array, compute the cost for each, and take the minimum or maximum depending on interpretation. This would require generating all `n!` permutations and computing a linear scan for each, leading to `O(n! * n)` complexity. Even for `n = 10`, this becomes infeasible.

However, the structure of the problem eliminates any need for permutation reasoning. Since sorting is explicitly required before eval
