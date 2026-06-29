---
title: "CF 104686K - Skills in Pills"
description: "We are building a schedule over a line of n days. On each day, we may or may not take two different pills, but with a strict constraint that both pills can never be taken on the same day."
date: "2026-06-29T08:51:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104686
codeforces_index: "K"
codeforces_contest_name: "2022-2023 ICPC Central Europe Regional Contest (CERC 22)"
rating: 0
weight: 104686
solve_time_s: 20
verified: false
draft: false
---

[CF 104686K - Skills in Pills](https://codeforces.com/problemset/problem/104686/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are building a schedule over a line of `n` days. On each day, we may or may not take two different pills, but with a strict constraint that both pills can never be taken on the same day.

Pill A has a recurrence rule: in any stretch of `k` consecutive days, at least one day must include pill A. Equivalently, there is no gap of `k` consecutive days without A. Pill B has the same type of requirement with parameter `j`. The goal is to construct a valid schedule over `n` days that respects both spacing constraints while respecting the mutual exclusion rule, and we want to minimize the total number of pill intakes.

The output is simply this minimum total number of taken pills across all days, counting A and B separately.

The key constraint is `n ≤ 10^6`, which immediately rules out any exponential or quadratic search over schedules. Even an `O(n log n)` construction is borderline but still feasible. Any correct solution must essentially reason in terms of densities or periodic structure rather than explicit enumeration of all valid schedules.

A naive idea would be to simulate all possible placements of A and B, but even for small `n`, the number of valid configurations grows combinatorially. Another tempting mistake is to greedily place A every `k` days and B every `j` days independently; this fails because overlap days are forbidden, so independent construction can produce collisions or force unnecessary extra pills.

A subtle edge case appears when `k` and `j` are close, for example `k = j = 2`. A naive alternating schedule quickly breaks because both pills try to occupy every other day, but they cannot coincide, forcing additional placements.

## Approaches

The core difficulty is that each pill independently imposes a minimum density of usage, but they compete
