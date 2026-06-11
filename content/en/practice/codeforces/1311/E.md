---
title: "CF 1311E - Construct the Binary Tree"
description: "Yes, the inequality $nu(n) le 2^{l(n) - lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $lambda(n)$ be the length of a shortest chain consisting only of doubling steps."
date: "2026-06-11T17:17:42+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "trees"]
categories: ["algorithms"]
codeforces_contest: 1311
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 624 (Div. 3)"
rating: 2200
weight: 1311
solve_time_s: 80
verified: false
draft: false
---

[CF 1311E - Construct the Binary Tree](https://codeforces.com/problemset/problem/1311/E)

**Rating:** 2200  
**Tags:** brute force, constructive algorithms, trees  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
Yes, the inequality $\nu(n) \le 2^{l(n) - \lambda(n)}$ holds for all positive integers $n$. Consider an addition chain of minimal length $l(n)$ and let $\lambda(n)$ be the length of a shortest chain consisting only of doubling steps. Each nondoubling step can at most double the number of ones in the binary representation of the current exponent. Therefore, starting from a single $1$, after $l(n) - \lambda(n)$ nondoubling steps, the number of ones $\nu(n)$ satisfies $\nu(n) \le 2^{l(n) - \lambda(n)}$.

This establishes the bound directly. Consequently, applying this inequality to $2^n - 1$, whose binary representation consists of $n$ ones, we obtain the lower bound $l(2^n - 1) \ge n - 1 + \lfloor \lg n \rfloor$, in agreement with equations (17) and (49). This completes the argument. ∎
