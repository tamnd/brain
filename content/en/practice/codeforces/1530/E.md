---
title: "CF 1530E - Minimax"
description: "The solution is attempting to justify formula (25) via polynomial interpolation of the product polynomial values."
date: "2026-06-10T16:55:59+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1530
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 733 (Div. 1 + Div. 2, based on VK Cup 2021 - Elimination (Engine))"
rating: 2100
weight: 1530
solve_time_s: 153
verified: false
draft: false
---

[CF 1530E - Minimax](https://codeforces.com/problemset/problem/1530/E)

**Rating:** 2100  
**Tags:** constructive algorithms, greedy, strings  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Correctness

The solution is attempting to justify formula (25) via polynomial interpolation of the product polynomial values. The general strategy, using evaluation at $2r+1$ points and Vandermonde inversion, is mathematically sound and does lead to the standard identity that coefficients of a degree-$2r$ polynomial are linear combinations of its values at $2r+1$ distinct points.

However, the exercise in TAOCP Section 4.3.3 is not merely asking to restate the interpolation principle. In that section, formula (25) refers to a specific structured identity derived from Algorithm T, where the coefficients of $W(x)$ are expressed explicitly in terms of the computed values $W(0), \ldots, W(2r)$ via the finite-difference / factorial basis construction shown earlier in equations (14)-(18). The expected proof is that this explicit transformation is correct.

The submitted solution instead proves a weaker and more general statement: existence of a linear transformation via $A^{-1}$. This does not establish the specific form of (25) in the text, nor does it connect to the factorial basis or the concrete reconstruction procedure used in the section.

Thus, even if the linear-algebraic statement is true, it does not match the required identity.

## Gaps and Errors

The main issue is a justification gap that becomes a structural mismatch with the target result.

The argument replaces the finite-difference construction underlying (25) with a Vandermonde inversion argument. While Vandermonde invertibility guarantees existence and uniqueness of coefficients, it does not reproduce the explicit formula (25) as given in TAOCP, which depends on structured evaluation and conversion between power basis and falling factorial basis. This step is not equivalent to the identity in the text, so it does not answer the exercise as stated.

Additionally, the claim that “Thus the computation of all coefficients $W_k$ requires exactly $2r+1$ multiplications” is not justified in the TAOCP model. The cost model in Section 4.3.3 is not purely algebraic; it is about bit operations and structured evaluation complexity. The argument omits the connection to the specific computational structure used in Algorithm T.

The statement “The identity (25) follows directly” is unsupported. It is a circular reference to the interpolation framework already introduced, without deriving the specific transformation used in (25).

All of these issues are justification gaps rather than algebraic errors in Vandermonde theory, but collectively they prevent the solution from addressing the actual exercise.

## Summary

The solution is mathematically correct at a high level of abstraction but does not derive the specific formula (25) from Section 4.3.3 and does not connect to the required finite-difference structure of the text.

VERDICT: FAIL - the solution replaces the required finite-difference identity (25) with a general Vandermonde interpolation argument and does not prove the stated formula.
