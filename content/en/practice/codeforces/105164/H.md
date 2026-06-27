---
title: "CF 105164H - Highest Score APPQ"
description: "We are given a universe of numbers generated in a very structured way. Each number corresponds to a vector of exponents over the first $n$ primes."
date: "2026-06-27T10:45:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105164
codeforces_index: "H"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105164
solve_time_s: 42
verified: false
draft: false
---

[CF 105164H - Highest Score APPQ](https://codeforces.com/problemset/problem/105164/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a universe of numbers generated in a very structured way. Each number corresponds to a vector of exponents over the first $n$ primes. The $i$-th coordinate $e_i$ tells us how many times the $i$-th prime appears in the factorization, and each coordinate is bounded by $0 \le e_i \le a_i$. So the entire input describes a finite grid of exponent vectors, and every valid number is one point in this grid.

We must choose a subset of these numbers under a structural restriction on pairs. If we take two numbers $x < y$, then it is forbidden tha
