---
title: "CF 198A - About Bacteria"
description: "The problem involves modeling bacterial growth in a test tube according to a discrete-time recurrence. Each bacterium splits into k bacteria every second, and an additional b bacteria are added due to abnormal effects."
date: "2026-06-03T16:22:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 198
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 125 (Div. 1)"
rating: 1700
weight: 198
solve_time_s: 35
verified: false
draft: false
---

[CF 198A - About Bacteria](https://codeforces.com/problemset/problem/198/A)

**Rating:** 1700  
**Tags:** implementation, math  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

The problem involves modeling bacterial growth in a test tube according to a discrete-time recurrence. Each bacterium splits into _k_ bacteria every second, and an additional _b_ bacteria are added due to abnormal effects. After _n_ seconds starting from one bacterium, the first experiment reaches exactly _z_ bacteria. The second experiment starts with _t_ bacteria, and we want to determine the minimum number of seconds required for the same growth process to reach at least _z_ bacteria.

The inputs _k_, _b_, _n_, and _t_ are all integers between 1 and 10^6. This implies that any iterative computation over time should avoid linear scans of _z_ or large loops up to _z_, because the number of bacteria can grow extremely fast - exponentially in _n_ for the multiplicative factor _k_. Overflow is not an issue in Python, but in other languages, care would be needed. The output is a single integer, representing the number of seconds.

Edge cases arise when the starting number of bacteria _t_ is already equal to or greater than the target _z_. For example, if _t_ = _z_, the answer sh
