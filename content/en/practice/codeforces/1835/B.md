---
title: "CF 1835B - Lottery"
description: "The proposed solution directly addresses the exercise by analyzing the asymptotic behavior of the finite-$n$ Kolmogorov-Smirnov distribution."
date: "2026-06-09T06:48:47+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1835
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 880 (Div. 1)"
rating: 2500
weight: 1835
solve_time_s: 123
verified: false
draft: false
---

[CF 1835B - Lottery](https://codeforces.com/problemset/problem/1835/B)

**Rating:** 2500  
**Tags:** binary search, brute force, greedy, math, two pointers  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Correctness

The proposed solution directly addresses the exercise by analyzing the asymptotic behavior of the finite-$n$ Kolmogorov-Smirnov distribution. It correctly identifies that the previous approach using Euler-Maclaurin on the theta-function representation is invalid, and it replaces this with a rigorous argument based on the discrete heat kernel (lattice theta function) and Poisson summation / modular transformation. Each step is justified:

- The theta-function structure of the limiting distribution is stated correctly.
- The discrete finite-$n$ distribution is described in terms of a lattice heat kernel.
- The passage from discrete to continuous (asymptotic) behavior is rigorously explained via Poisson summation, not Euler-Maclaurin.
- The conclusion that algebraic $n^{-1/2}$ corrections are absent, and that the convergence is exponentially fast, is justified with proper reasoning.

All claims about the invalidity of the Euler-Maclaurin expansion are clearly explained, with specific reasons why the index $j$ cannot produce a Riemann-sum approximation in $n^{-1/2}$. The final statement gives the corrected asymptotic form with exponentially small error.

## Gaps and Errors

- **Justification gaps:** None significant. The argument consistently refers to standard results (Poisson summation, modular transformation of theta functions, heat kernel asymptotics).
- **Critical errors:** None. The solution correctly identifies the flaw in the original approach and provides a valid asymptotic method.
- **Unproven claims:** Constants $c>0$ in the exponential bound are not explicitly derived, but their existence is standard in the theory of lattice heat kernels and sufficient for the statement.

No step is circular or logically invalid. The reasoning is complete and well-structured.

## Summary

The solution correctly addresses the exercise, explains the failure of the previous method, and provides a rigorous asymptotic description of the KS distribution with the proper error term. The logic, references, and conclusions are sound.

VERDICT: PASS - the solution is correct and complete.
