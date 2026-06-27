---
title: "CF 105002L - \u041c\u043e\u043d\u0441\u0442\u0440\u044b"
description: "We are given a collection of monsters, and we want to choose some of them to maximize how many we take, under a global limit on total “aggressiveness”. Each monster behaves in a slightly conditional way."
date: "2026-06-28T03:21:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105002
codeforces_index: "L"
codeforces_contest_name: "vkoshp.letovo 2022"
rating: 0
weight: 105002
solve_time_s: 23
verified: false
draft: false
---

[CF 105002L - \u041c\u043e\u043d\u0441\u0442\u0440\u044b](https://codeforces.com/problemset/problem/105002/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of monsters, and we want to choose some of them to maximize how many we take, under a global limit on total “aggressiveness”.

Each monster behaves in a slightly conditional way. If we decide to take a set of monsters of size $k$, then for each monster there is a threshold $c_i$. If the final chosen size $k$ does not exceed this threshold, the monster contributes a lower value $a_i$. If the chosen size is larger than $c_i$, the monster becomes more dangerous and contributes $b_i$, where $b_i \ge a_i$.

The goal is to pick a subset of monsters such that when their contributions are computed according to the final size of the subset, the total sum does not exceed $s$, and the size of the subset is as large as possible.

The key difficulty is that the cost of a chosen monster depends on how many monsters we pick in total, so the value of a fixed subset is not fixed in advance.

The c
