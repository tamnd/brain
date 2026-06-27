---
title: "CF 105003F - Erd\u0151s-Straus Conjecture"
description: "We are asked to decide whether a pair of positive integers $x, y$ exists such that a fixed rational expression equals a sum of three Egyptian fractions where the third denominator is constrained to be the product $xy$."
date: "2026-06-28T03:16:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105003
codeforces_index: "F"
codeforces_contest_name: "XXVIII Spain Olympiad in Informatics, Online Qualifier"
rating: 0
weight: 105003
solve_time_s: 38
verified: false
draft: false
---

[CF 105003F - Erd\u0151s-Straus Conjecture](https://codeforces.com/problemset/problem/105003/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to decide whether a pair of positive integers $x, y$ exists such that a fixed rational expression equals a sum of three Egyptian fractions where the third denominator is constrained to be the product $xy$. For each test case, we either output one valid pair or report impossibility.

After rewriting the equation, the input $n$ acts as a parameter controlling a Diophantine condition over two unknown integers. The task is not about approximation or search over reals, but about exact integer structure.

The constraint $n \le 10^9$ with at most 100 test cases means any approach that iterates up to $n$ is immediately impossible. Even quadratic scans over possible $x, y$ pairs are out of reach since that would explode to $10^{18}$ in the worst case. The only viable strategies must reduce the problem to something like divisor enumeration or algebraic factorization, where the search space is sublinear in $n$, typically around $O(\sqrt n)$ or better amortized.

A subtle edge case appears when $n = 1$. The expressio
