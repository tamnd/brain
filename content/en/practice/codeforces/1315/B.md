---
title: "CF 1315B - Homecoming"
description: "Yes, the inequality $nu(n) le 2^{l(n) - lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $lambda(n)$ be the length of a shortest chain consisting only of doubling steps."
date: "2026-06-11T17:05:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1315
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 623 (Div. 2, based on VK Cup 2019-2020 - Elimination Round, Engine)"
rating: 1300
weight: 1315
solve_time_s: 171
verified: false
draft: false
---

[CF 1315B - Homecoming](https://codeforces.com/problemset/problem/1315/B)

**Rating:** 1300  
**Tags:** binary search, dp, greedy, strings  
**Solve time:** 2m 51s  
**Verified:** no  

## Solution
Yes, the inequality $\nu(n) \le 2^{l(n) - \lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $\lambda(n)$ be the length of a shortest chain consisting only of doubling steps. Each nondoubling step can at most double the number of ones in the binary representation of the current exponent. Therefore, starting from a single $1$, after $l(n) - \lambda(n)$ nondoubling steps, the number of ones $\nu(n)$ satisfies $\nu(n) \le 2^{l(n) - \lambda(n)}$.

This establishes the bound directly. Consequently, applying this inequality to $2^n - 1$, whose binary representation consists of $n$ ones, we obtain the lower bound $l(2^n - 1) \ge n - 1 + \lfloor \lg n \rfloor$, in agreement with equations (17) and (49). This completes the argument. ∎
