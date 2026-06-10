---
title: "CF 1530C - Pursuit"
description: "We have a contest with multiple stages, each stage giving between 0 and 100 points. You and Ilya have already completed n stages, and we know the scores for both of you."
date: "2026-06-10T16:52:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1530
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 733 (Div. 1 + Div. 2, based on VK Cup 2021 - Elimination (Engine))"
rating: 1200
weight: 1530
solve_time_s: 45
verified: false
draft: false
---

[CF 1530C - Pursuit](https://codeforces.com/problemset/problem/1530/C)

**Rating:** 1200  
**Tags:** binary search, brute force, greedy, sortings  
**Solve time:** 45s  
**Verified:** no  

## Solution
## Problem Understanding

We have a contest with multiple stages, each stage giving between 0 and 100 points. You and Ilya have already completed `n` stages, and we know the scores for both of you. The contest ranks a contestant by taking only the highest `k - floor(k / 4)` scores out of the first `k` stages, summing them to get the overall score.

The problem asks: given your current scores and Ilya's scores, what is the smallest number of additional perfect-scoring stages (100 points) you need to theoretically reach a total that is at least equal to Ilya's total, assuming Ilya scores nothing in these additional stages?

The input guarantees that the sum of `n` across all test cases is at most `10^5`. Since `n` can reach `10^5`, any algorithm that naively tries all possibilities for extra stages would be too slow. We need something faster than `O(n
