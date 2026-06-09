---
title: "CF 1743B - Permutation Value"
description: "The solution correctly identifies that the sawtooth function $(u) = u - lfloor u rfloor$ captures the fractional part of $x/y$ and that multiplying it by $y$ gives the remainder when $x$ is divided by $y$."
date: "2026-06-09T16:01:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1743
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 137 (Rated for Div. 2)"
rating: 800
weight: 1743
solve_time_s: 143
verified: false
draft: false
---

[CF 1743B - Permutation Value](https://codeforces.com/problemset/problem/1743/B)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Correctness

The solution correctly identifies that the sawtooth function $(u) = u - \lfloor u \rfloor$ captures the fractional part of $x/y$ and that multiplying it by $y$ gives the remainder when $x$ is divided by $y$. This directly addresses the exercise's request to express $x \bmod y$ in terms of the sawtooth function.

The verification examples are valid and demonstrate that the formula $x \bmod y = y ,(x/y)$ using the sawtooth function recovers the correct remainder for both a non-multiple and an exact multiple of $y$.

The optional inclusion of the delta function to handle exact multiples is unnecessary in standard real analysis because the sawtooth function already satisfies $(u) = 0$ when $u \in \mathbb{Z}$. Introducing $\delta$ in the solution does not change the correctness but is somewhat misleading: the delta function is a distribution, not a conventional function, and writing $y((x/y) - \delta((x/y)))$ is not standard and does not provide any extra precision for computing $x \bmod y$.

Otherwise, all steps are justified and mathematically sound. The solution defines the sawtooth function, relates it to the modulo operation, and provides explicit formulas with clear verification.

## Gaps and Errors

1. **Use of the delta function**: Justification gap. The solution claims that the delta term is needed to handle exact multiples of $y$, but in fact the sawtooth function already evaluates to $0$ at integers. While this does not make the solution incorrect, it introduces unnecessary complexity and could mislead a reader about the role of the delta function.
2. All other steps are correctly reasoned and no critical errors are present. The main formula $x \bmod y = y(x/y)$ using the sawtooth function is correct.

## Summary

The solution is correct and complete in terms of answering the exercise. The inclusion of the delta function is unnecessary, but it does not invalidate the main formula. The solution clearly defines the sawtooth function, derives the modulo expression, and verifies it with examples.

VERDICT: PASS - the solution correctly expresses $x \bmod y$ using the sawtooth function, though the delta term is superfluous.
