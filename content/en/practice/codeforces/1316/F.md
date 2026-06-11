---
title: "CF 1316F - Battalion Strength"
description: "Yes, the inequality $nu(n) le 2^{l(n) - lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $lambda(n)$ be the length of a shortest chain consisting only of doubling steps."
date: "2026-06-11T17:02:54+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1316
codeforces_index: "F"
codeforces_contest_name: "CodeCraft-20 (Div. 2)"
rating: 2800
weight: 1316
solve_time_s: 177
verified: false
draft: false
---

[CF 1316F - Battalion Strength](https://codeforces.com/problemset/problem/1316/F)

**Rating:** 2800  
**Tags:** data structures, divide and conquer, probabilities  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
Yes, the inequality $\nu(n) \le 2^{l(n) - \lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $\lambda(n)$ be the length of a shortest chain consisting only of doubling steps. Each nondoubling step can at most double the number of ones in the binary representation of the current exponent. Therefore, starting from a single $1$, after $l(n) - \lambda(n)$ nondoubling steps, the number of ones $\nu(n)$ satisfies $\nu(n) \le 2^{l(n) - \lambda(n)}$.

This establishes the bound directly. Consequently, applying this inequality to $2^n - 1$, whose binary representation consists of $n$ ones, we obtain the lower bound $l(2^n - 1) \ge n - 1 + \lfloor \lg n \rfloor$, in agreement with equations (17) and (49). This completes the argument. ∎
