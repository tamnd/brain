---
title: "CF 104941H - How Does It Fit?"
description: "We are given a mutable string $s$ and a pattern $p$ that contains lowercase letters and wildcard stars. A star can be replaced by any (possibly empty) string, independently of other stars."
date: "2026-06-28T18:18:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "H"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 22
verified: false
draft: false
---

[CF 104941H - How Does It Fit?](https://codeforces.com/problemset/problem/104941/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a mutable string $s$ and a pattern $p$ that contains lowercase letters and wildcard stars. A star can be replaced by any (possibly empty) string, independently of other stars. The pattern matches a string if, after replacing every star, we can obtain the string exactly.

After every single-character update to $s$, we need to answer whether there exists at least one contiguous substring of the current $s$ that matches the pattern $p$.

So the task is not to match the whole string, but to check existence of a “good window” in $s$ after each update.

The constraints separate the two objects clearly. The string $s$ is large, up to $2 \cdot 10^5$, and it changes many times, up to $2 \cdot 10^4$. The pattern $p$ is tiny, at most 200 characters. This asymmetry is the main structural hint: preprocessing and pattern-centric reasoning are mandatory, while the string must be handled dynamically.

A naive approach would scan all substrings after each update, which is immediately impossible: $O(n^2)$ substrings times up to $2 \cdot 10^4$ updates already exceeds any limit.

There are a few subtle failure cases that trip naive greedy matching.

A first issue is empty-star behavior. For example, pattern `"a*b"` matches `"ab"` (star empty) and `"axxb*
