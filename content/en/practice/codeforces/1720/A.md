---
title: "CF 1720A - Burenka Plays with Fractions"
description: "We are given two fractions per test case, $frac{a}{b}$ and $frac{c}{d}$. In one operation, we may multiply either the numerator or denominator of either fraction by any nonzero integer."
date: "2026-06-09T19:24:50+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1720
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 815 (Div. 2)"
rating: 900
weight: 1720
solve_time_s: 45
verified: false
draft: false
---

[CF 1720A - Burenka Plays with Fractions](https://codeforces.com/problemset/problem/1720/A)

**Rating:** 900  
**Tags:** math, number theory  
**Solve time:** 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two fractions per test case, $\frac{a}{b}$ and $\frac{c}{d}$. In one operation, we may multiply either the numerator or denominator of either fraction by any nonzero integer. The goal is to make the two fractions represent the same real value using as few such operations as possible.

A useful way to reinterpret the operation is that each fraction is a product of two independent “scaling degrees of freedom”: numerator scaling and denominator scaling. Since we can multiply by any integer, we are not restricted to primes or fixed factors. The only constraint is that each multiplication counts as one clap, regardless of magnitude.

The output is the minimum number of such single-coordinate multiplications needed so that

$$\frac{a'}{b'} = \frac{c'}{d'}.$$

The constraints are large: up to $10^4$ test cases and values up to $10^9$. This immediately rules out any factorization-heavy or search-based approach per test case. Anything beyond $O(1)$ or $O(\log n)$ per test case is acceptable, but anything involving gcd over many transformations, dp, or enumeration of divisors would be too slow.

A key subtle case involves zeros in numerators. If both fractions are zero, they are already equal regardless of denominators. If exactly one fraction is zero, we must be able to force the other numerator to become zero, which is impossible via multiplication unless we multiply by zero, which is forbidden. So equality to zero is a special structural case rather than a numeric scaling one.

Another subtle point is that equality of fractions is not about making numerators equal and denominators equal independently. For example, $\frac{2}{1} = \frac{4}{2}$, but matching numerator and denominator separately would overcount operations. The equality condition couples numerator and denominator scaling.

## Approaches

A naive viewpoint is to treat the problem as transforming $(a,b)$ into $(c,d)$ by multiplying coordinates independently. One could attempt to search for integer multipliers that align the two fractions exactly. This quickly becomes a number theory search problem: we would try to match ratios by applying multipliers that adjust both numerator and denominator until equality holds.

However, this quickly breaks down because the space of possible multipliers is infinite in principle. Even if we restrict ourselves to factor ratios between $a,c$ and $b,d$, there is no clean bounded enumeration strategy. The number of potential combinations of multipliers grows multiplicatively with the number of prime factors, and in the worst case each number up to $10^9$ can have many factor combinations. This makes brute-force factor matching infeasible.

The key observation is that we are not required to reach exact target numerators and denominators, only equality of ratios. That means we only care about whether the cross-products can be made equal:

$$a' d' = b' c'.$$

Since each operation multiplies exactly one coordinate, each clap effectively inserts a factor into one side of this equality. The problem reduces to how many independent scaling adjustments are required to make two fractions consistent.

From this perspective, each fraction contributes a ratio $a:b$ and $c:d$. We want to make them identical. If they are already equal, answer is zero. If either fraction is zero, special handling applies. Otherwise, we can always achieve equality in at most two operations: one adjustment to align numerators or denominators into a shared ratio structure, and possibly one more if both sides need correction.

A more preci
