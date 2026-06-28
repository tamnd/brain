---
title: "CF 104757D - Cornhusker"
description: "We are simulating a simplified agricultural estimation process for corn yield. The input describes five sampled corn ears, where each ear is characterized by two measurements: how many kernels wrap around the ear and how many kernels run along its length."
date: "2026-06-28T22:47:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104757
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC East North America Regional Contest (ECNA 2023)"
rating: 0
weight: 104757
solve_time_s: 23
verified: false
draft: false
---

[CF 104757D - Cornhusker](https://codeforces.com/problemset/problem/104757/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a simplified agricultural estimation process for corn yield. The input describes five sampled corn ears, where each ear is characterized by two measurements: how many kernels wrap around the ear and how many kernels run along its length. From these five samples we compute an average kernel count per ear.

After that, we scale this average by the total number of ears in a fixed row segment. This gives an estimate of total kernels in that segment. Finally, we convert kernels into bushels using a divisor called the Kernel Weight Factor (KWF), and we are instructed to use integer arithmetic throughout, meaning division is truncating toward zero.

The key point is that all structure is linear. We reduce raw measurements into a single averaged value, multiply by a count, and divide by a constant. There is no combinatorial or algorithmic complexity beyond careful integer arithmetic and ordering of operations.

The constraints are extremely small: only five ears, fixed-size inputs, and values bounded in the tens. This guarantees that any correct solution is essentially constant time. The only failure mode comes from mishandling integer division order. If we divide too early, we lose precision permanently and the final result becomes incorrect.

A subtle pitfall appears if a solver averages early using integer division. For example, if kernel totals for five ears sum to so
