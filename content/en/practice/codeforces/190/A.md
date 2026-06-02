---
title: "CF 190A - Vasya and the Bus"
description: "We are asked to compute the minimum and maximum bus fare collected given a number of grown-ups n and children m on a bus. Each grown-up pays one ruble for themselves, and each grown-up can take at most one child for free. Any additional children cost one ruble each."
date: "2026-06-03T01:26:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1100
weight: 190
solve_time_s: 21
verified: false
draft: false
---

[CF 190A - Vasya and the Bus](https://codeforces.com/problemset/problem/190/A)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the minimum and maximum bus fare collected given a number of grown-ups `n` and children `m` on a bus. Each grown-up pays one ruble for themselves, and each grown-up can take at most one child for free. Any additional children cost one ruble each. Children cannot ride alone, so `m` cannot exceed `n` times the number of children each grown-up can pay for, or else the situation is impossible.

The input is two integers `n` and `m`. The output is either two integers representing the minimum and maximum total fare, or the word "Impossible" if the combination of grown-ups and children cannot exist on the bus.

Given the constraints `0 ≤ n, m ≤ 10^5`,
