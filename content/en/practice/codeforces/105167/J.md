---
title: "CF 105167J - Just Too Much Procrastination"
description: "We are given an array of distinct integers, representing heat levels of server racks arranged in a line. We are allowed to rearrange this array using adjacent swaps, where each swap exchanges neighboring elements."
date: "2026-06-27T10:36:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105167
codeforces_index: "J"
codeforces_contest_name: "ETH Zurich Competitive Programming Contest Spring 2024"
rating: 0
weight: 105167
solve_time_s: 17
verified: false
draft: false
---

[CF 105167J - Just Too Much Procrastination](https://codeforces.com/problemset/problem/105167/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of distinct integers, representing heat levels of server racks arranged in a line. We are allowed to rearrange this array using adjacent swaps, where each swap exchanges neighboring elements.

After rearranging, we evaluate the quality of the configuration by summing the absolute differences between every pair of adjacent elements. Formally, for a permutation $b$, the score is

$$\sum_{i=2}^{n} |b_{i-1} - b_i|.$$

The task has two parts for each test case. First, we must determine the maximum possible value of this score over all permutations of the array. Second, among all permutations achieving this maximum, we must compute the minimum number of adjacent swaps needed to reach one such optimal arrangement.

The constraints allow up to $2 \cdot 10^5$ test cases with total $n \le 4 \cdot 10^5$. This forces an essentially linear or near-linear solution per test case. Any approach that explicitly tries permutations or simulates swaps will fail because even (O(n^2)\
