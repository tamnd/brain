---
title: "CF 1742G - Orray"
description: "The task is to rearrange a given array of nonnegative integers so that the prefix OR array is lexicographically as large as possible."
date: "2026-06-09T16:18:34+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1742
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 827 (Div. 4)"
rating: 1500
weight: 1742
solve_time_s: 120
verified: false
draft: false
---

[CF 1742G - Orray](https://codeforces.com/problemset/problem/1742/G)

**Rating:** 1500  
**Tags:** bitmasks, brute force, greedy, math, sortings  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

The task is to rearrange a given array of nonnegative integers so that the prefix OR array is lexicographically as large as possible. The prefix OR array is defined as $b_i = a_1 ,\mathsf{OR}, a_2 ,\mathsf{OR}, \dots ,\mathsf{OR}, a_i$, meaning each element $b_i$ represents the cumulative bitwise OR from the start of the array up to position $i$. The goal is to permute $a$ to maximize $b$ in lexicographical order, which means the first element of $b$ should be as large as possible, and if there is a tie, the second element should be as large as possible, and so on.

The input contains multiple test cases, and the total size of all arrays does not exceed $2 \cdot 10^5$. This constraint implies that algorithms with $O(n^2)$ complexity will not run efficiently, but $O(n \log n)$ or $O(n \cdot 30)$ operations are acceptable because each number is at most $10^9$, meaning at most
