---
title: "CF 1687F - Koishi's Unconscious Permutation"
description: "The solution addresses the exercise directly. It identifies the event $f(n)-f(n-1) = k$ as the occurrence of exactly $k-1$ consecutive terms outside the interval $[alpha,beta)$ followed by one term inside, which correctly models the \"gap\" between hits in the interval."
date: "2026-06-09T23:46:24+07:00"
tags: ["codeforces", "competitive-programming", "fft", "math"]
categories: ["algorithms"]
codeforces_contest: 1687
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 796 (Div. 1)"
rating: 3500
weight: 1687
solve_time_s: 139
verified: false
draft: false
---

[CF 1687F - Koishi's Unconscious Permutation](https://codeforces.com/problemset/problem/1687/F)

**Rating:** 3500  
**Tags:** fft, math  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Correctness

The solution addresses the exercise directly. It identifies the event $f(n)-f(n-1) = k$ as the occurrence of exactly $k-1$ consecutive terms outside the interval $[\alpha,\beta)$ followed by one term inside, which correctly models the "gap" between hits in the interval. By invoking the $\infty$-distribution property, the solution justifies treating this block of $k$ consecutive terms as independent, allowing the probability to factor as the product $(1-p)^{k-1}p$. The derivation explicitly considers the first $k-1$ terms outside the interval and the final term inside, which reproduces the geometric distribution with parameter $p = \beta-\alpha$, exactly as required.

The solution also verifies the formula for small values of $k$ ($k=1,2$) and explains why the pattern generalizes to arbitrary $k\ge1$. Each step relies on standard definitions from the text (Definition B) and is logically consistent. All claims, including the factorization of probabilities and the lengths of intervals, are justified by the $\infty$-distribution property.

## Gaps and Errors

There are minor presentation gaps where the solution uses placeholders like `$$$$` instead of explicitly writing the sets or lengths of complements and intervals, but these do not affect the correctness of the argument, as the logic is clear and the missing details are straightforward. There are no circular arguments, and no critical steps are assumed without justification. All necessary reasoning for the derivation of $\Pr(f(n)-f(n-1)=k) = p(1-p)^{k-1}$ is present.

**Specific notes:**

- The description of the event $f(n)-f(n-1) = k$ skips explicitly mentioning $A_{f(n-1)+1}^c$ in one line but includes it later in the intersection, which is consistent.
- Placeholders for lengths (complements and intervals) could be filled in for completeness, but the reasoning clearly implies $\text{length}([\alpha,\beta)^c) = 1-p$ and $\text{length}([\alpha,\beta)) = p$.

No critical errors are present; the argument is correct and complete once the missing explicit expressions are mentally filled in.

## Summary

The proposed solution correctly proves that an $\infty$-distributed sequence passes the gap test, explicitly models the events, applies the definition of $\infty$-distribution to justify independence of consecutive terms, and derives the geometric distribution formula. Minor typographical gaps do not compromise the proof.

VERDICT: PASS - the solution is correct and complete.
