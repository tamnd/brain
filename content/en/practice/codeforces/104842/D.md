---
title: "CF 104842D - Deep Primes"
description: "We are looking at integers written in decimal form, but the key constraint is not about their numeric value alone. Each number is interpreted as a string, and every contiguous block of digits inside that string is turned back into an integer by stripping leading zeros."
date: "2026-06-28T11:31:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104842
codeforces_index: "D"
codeforces_contest_name: "2020-2021 ICPC, Moscow Subregional"
rating: 0
weight: 104842
solve_time_s: 29
verified: false
draft: false
---

[CF 104842D - Deep Primes](https://codeforces.com/problemset/problem/104842/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are looking at integers written in decimal form, but the key constraint is not about their numeric value alone. Each number is interpreted as a string, and every contiguous block of digits inside that string is turned back into an integer by stripping leading zeros. Those derived integers are required to satisfy a strong condition.

A number is called valid if it is prime, and additionally every substring of its decimal representation corresponds to a prime integer after conversion. The task is to count how many such numbers lie inside a given interval $[n, m]$, where both endpoints can be as large as $10^{18}$.

The constraint immediately implies that a brute force check per number is impossible. Even checking primality is already expensive at this scale, and the interval can contain up to $10^{18}$ candidates in the worst case. Any solution must instead generate all valid numbers directly.

A first subtle issue comes from substrings of length one. Every single digit must itself represent a prime number.
