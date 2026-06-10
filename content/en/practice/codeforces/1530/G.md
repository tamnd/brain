---
title: "CF 1530G - What a Reversal"
description: "We are given two binary strings, a and b, of the same length n and an integer k. Our goal is to transform a into b by repeatedly reversing substrings of a that contain exactly k ones. Each reversal can involve any number of zeros."
date: "2026-06-10T16:55:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1530
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 733 (Div. 1 + Div. 2, based on VK Cup 2021 - Elimination (Engine))"
rating: 3300
weight: 1530
solve_time_s: 49
verified: false
draft: false
---

[CF 1530G - What a Reversal](https://codeforces.com/problemset/problem/1530/G)

**Rating:** 3300  
**Tags:** constructive algorithms  
**Solve time:** 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two binary strings, `a` and `b`, of the same length `n` and an integer `k`. Our goal is to transform `a` into `b` by repeatedly reversing substrings of `a` that contain exactly `k` ones. Each reversal can involve any number of zeros. The output should either be a sequence of reversals or `-1` if the transformation is impossible within the specified limit.

The problem is constructive, but it has a subtle constraint: we cannot arbitrarily move ones. We can only reverse blocks containing exactly `k` ones. This means we need to think in terms of the positions of ones
