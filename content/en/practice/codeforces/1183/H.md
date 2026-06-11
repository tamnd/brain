---
title: "CF 1183H - Subsequences (hard version)"
description: "We are given a fixed string of length $n$. From it, we repeatedly choose subsequences, but every chosen subsequence must be different from all previously chosen ones."
date: "2026-06-12T01:24:47+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 1900
weight: 1183
solve_time_s: 148
verified: false
draft: false
---

[CF 1183H - Subsequences (hard version)](https://codeforces.com/problemset/problem/1183/H)

**Rating:** 1900  
**Tags:** dp, strings  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed string of length $n$. From it, we repeatedly choose subsequences, but every chosen subsequence must be different from all previously chosen ones. Each time we choose a subsequence $t$, we pay a cost equal to the number of characters we delete from the original string, which is $n - |t|$. We must eve
