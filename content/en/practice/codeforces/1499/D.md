---
title: "CF 1499D - The Number of Pairs"
description: "We are asked to count all pairs of positive integers $(a, b)$ that satisfy the equation $$c cdot mathrm{lcm}(a, b) - d cdot mathrm{gcd}(a, b) = x$$ for given integers $c$, $d$, and $x$."
date: "2026-06-10T21:23:56+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1499
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 106 (Rated for Div. 2)"
rating: 2100
weight: 1499
solve_time_s: 51
verified: false
draft: false
---

[CF 1499D - The Number of Pairs](https://codeforces.com/problemset/problem/1499/D)

**Rating:** 2100  
**Tags:** dp, math, number theory  
**Solve time:** 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count all pairs of positive integers $(a, b)$ that satisfy the equation

$$c \cdot \mathrm{lcm}(a, b) - d \cdot \mathrm{gcd}(a, b) = x$$

for given integers $c$, $d$, and $x$. The input provides multiple test cases, each with its own triple $(c, d, x)$, and for each case we must output the number of valid pairs.

The key constraints are that $c$, $d$, and $x$ are at most $10^7$, and there can be up to $10^4$ test cases. A naive approach iterating over all pairs $(a, b)$ up to $x$ would involve $O(x^2)$ operations per test case, which is infeasible given that $x$ can be $10^7$. Therefore, we need a method that reduces the search space dramatically, ideally using number-theoretic properties rather than brute-force enumeration.

Edge cases arise when $x$ is small, when $c = d$, or when the combination $c \cdot \mathrm{lcm} - d \cdot \mathrm{gcd}$ has very few divisors. For example, if $x = 1$ and $c = d = 1$, the only possible values of $a$ and $b$ are constrained by integer divisibility, and a naive attempt to loop from 1 to $x$ could return 0 when there is in fact exactly one valid pair.

## Approaches

The brute-force approach is to loop over all possible $a$ and $b$ up to $x$ and check whether

$$c \cdot \mathrm{lcm}(a, b) - d \cdot \mathrm{gcd}(a, b) = x$$

holds. This works in principle, but each test case would involve up to (10^
