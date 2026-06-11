---
title: "CF 1312D - Count the Arrays"
description: "Yes, the inequality $nu(n) le 2^{l(n) - lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $lambda(n)$ be the length of a shortest chain consisting only of doubling steps."
date: "2026-06-11T17:14:37+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1312
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 83 (Rated for Div. 2)"
rating: 1700
weight: 1312
solve_time_s: 174
verified: false
draft: false
---

[CF 1312D - Count the Arrays](https://codeforces.com/problemset/problem/1312/D)

**Rating:** 1700  
**Tags:** combinatorics, math  
**Solve time:** 2m 54s  
**Verified:** no  

## Solution
Yes, the inequality $\nu(n) \le 2^{l(n) - \lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $\lambda(n)$ be the length of a shortest chain consisting only of doubling steps. Each nondoubling step can at most double the number of ones in the binary representation of the current exponent. Therefore, starting from a single $1$, after $l(n) - \lambda(n)$ nondoubling steps, the number of ones $\nu(n)$ satisfies $\nu(n) \le 2^{l(n) - \lambda(n)}$.

This establishes the bound directly. Consequently, applying this inequality to $2^n - 1$, whose binary representation consists of $n$ ones, we obtain the lower bound $l(2^n - 1) \ge n - 1 + \lfloor \lg n \rfloor$, in agreement with equations (17) and (49). This completes the argument. ∎
