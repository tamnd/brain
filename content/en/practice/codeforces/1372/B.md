---
title: "CF 1372B - Omkar and Last Class of Math"
description: "The proposed solution does not answer the exercise that was asked. The exercise is: Compute the pseudo-quotient $q(x)$ and pseudo-remainder $r(x)$ for the given polynomials $u(x)$ and $v(x)$ over the integers."
date: "2026-06-11T11:16:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1372
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 655 (Div. 2)"
rating: 1300
weight: 1372
solve_time_s: 89
verified: false
draft: false
---

[CF 1372B - Omkar and Last Class of Math](https://codeforces.com/problemset/problem/1372/B)

**Rating:** 1300  
**Tags:** greedy, math, number theory  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Correctness

The proposed solution does **not** answer the exercise that was asked.

The exercise is:

> Compute the pseudo-quotient $q(x)$ and pseudo-remainder $r(x)$ for the given polynomials $u(x)$ and $v(x)$ over the integers.

Instead of performing any polynomial pseudo-division, the proposed solution discusses an entirely different problem concerning $m$-survivors, prime-counting functions $\pi(x)$, and Exercise 4.5.4.41. It never defines the pseudo-division identity (1), never computes a pseudo-quotient, never computes a pseudo-remainder, and never uses the given polynomials $u(x)$ and $v(x)$.

Therefore it does not answer the question at all.

## Gaps and Errors

1. **Critical error:** The solution addresses a different exercise (the Lagarias-Miller-Odlyzko prime-counting exercise) instead of Exercise 4.6.1.1.
2. **Critical error:** The given polynomials

$$u(x)=x^6+x^5-x^4+2x^3+3x^2-x+2$$

and

$$v(x)=2x^2+2x^2-x+3$$

are never used.
3. **Critical error:** No pseudo-division is carried out.
4. **Critical error:** Neither the pseudo-quotient $q(x)$ nor the pseudo-remainder $r(x)$ is computed.
5. **Critical error:** The defining pseudo-division relation is never stated or verified.

## Summary

The submission is completely unrelated to the exercise being asked. Since it does not attempt the polynomial pseudo-division problem and provides neither $q(x)$ nor $r(x)$, it fails to answer the question.

VERDICT: FAIL - the proposed solution addresses an entirely different exercise and does not compute the required pseudo-quotient or pseudo-remainder.
