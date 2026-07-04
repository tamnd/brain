---
title: "CF 102964B - Krosh and xor of sums"
description: "The solution does not address the stated problem at all. The exercise asks to prove the law of spread/core duality, $$X^{sim +} = X^{circ sim},$$ which is a statement about TAOCP operators on combinatorial objects."
date: "2026-07-04T06:46:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102964
codeforces_index: "B"
codeforces_contest_name: "Krosh Kaliningrad Contest 1"
rating: 0
weight: 102964
solve_time_s: 153
verified: false
draft: false
---

[CF 102964B - Krosh and xor of sums](https://codeforces.com/problemset/problem/102964/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Correctness

The solution does not address the stated problem at all.

The exercise asks to prove the law of spread/core duality,

$$X^{\sim +} = X^{\circ \sim},$$

which is a statement about TAOCP operators on combinatorial objects.

The proposed solution instead discusses clutters, antichains, and enumeration of size vectors for $n=4$, which corresponds to a different exercise in Section 7.2.1.3. There is no definition of spread, core, or the duality operators appearing in the statement, and no attempt is made to manipulate or prove equality of $X^{\sim +}$ and $X^{\circ \sim}$.

Therefore, the argument is not a proof of the required statement.

## Gaps and Errors

The entire solution is a topic mismatch rather than a local error.

The following issues are fundamental:

The solution never introduces or defines the operators $\sim$, $+$, or $\circ$, so the target identity is never even interpreted. This is a critical error because the statement being proved is absent from the reasoning.

The solution instead replaces the problem with an unrelated combinatorial classification problem about antichains and size vectors. This is not a special case or reformulation of spread/core duality and has no logical connection to the required identity. This is a critical error.

All subsequent arguments about feasible size vectors, inclusion constraints, and enumeration for $n=4$ are therefore irrelevant to the exercise and do not contribute to a proof of the claimed identity. This is a critical error.

## Summary

The submission does not attempt the stated theorem and instead solves a different combinatorial enumeration problem.

VERDICT: FAIL - the solution does not address the spread/core duality identity $X^{\sim +} = X^{\circ \sim}$.
