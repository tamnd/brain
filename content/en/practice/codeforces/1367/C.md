---
title: "CF 1367C - Social Distance"
description: "The solution does not correctly address the statement being proved, and it does not provide a valid argument that the pseudo-remainder must be divisible by the leading coefficient $l(v)$."
date: "2026-06-11T11:58:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1367
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 650 (Div. 3)"
rating: 1300
weight: 1367
solve_time_s: 185
verified: false
draft: false
---

[CF 1367C - Social Distance](https://codeforces.com/problemset/problem/1367/C)

**Rating:** 1300  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 3m 5s  
**Verified:** no  

## Solution
## Correctness

The solution does not correctly address the statement being proved, and it does not provide a valid argument that the pseudo-remainder must be divisible by the leading coefficient $l(v)$.

The core claim is that if $\deg(u) \ge \deg(v) + 2$, then the pseudo-remainder $r(x)$ is a multiple of $l(v)$. The proposed solution attempts to justify this by tracking repeated scaling of coefficients during pseudo-division, but it does not correctly connect this scaling behavior to the actual definition of the pseudo-remainder, nor does it correctly use the structure of pseudo-division in a unique factorization domain.

The reasoning about repeated multiplication by $l(v)$ increasing divisibility is not sufficient to conclude anything about the final normalized remainder.

## Gaps and Errors

The first major issue is a conceptual mismatch between the pseudo-division algorithm and the constructed recurrence $u^{(t+1)} = l(v)u^{(t)} - q^{(t)}v$. This recurrence is not the standard pseudo-division process. In pseudo-division, each step eliminates the leading term by multiplying the current dividend by a power of $l(v)$, but the exponent depends on degree differences and is not uniform across iterations. The solution simplifies this incorrectly into a uniform multiplication by $l(v)$ at each step, which is not justified. This is a critical error because the induction is built on an incorrect model of the algorithm.

Second, the induction claim that coefficients of $u^{(t)}$ are divisible by $l(v)^t$ is unsupported. Even if one accepts the recurrence, pseudo-division does not preserve such a clean coefficient-wise divisibility structure. The subtraction $q^{(t)}(x)v(x)$ can cancel arbitrary factors of $l(v)$, so divisibility is not monotone in the way the argument assumes. This is a critical error because it invalidates the inductive invariant.

Third, the argument that “multiplication by $v(x)$ contributes a factor $v_n$ to the leading term and preserves divisibility in lower coefficients” is incorrect. Multiplying by a polynomial does not preserve coefficient-wise divisibility properties unless every coefficient of the multiplier has a known divisibility structure, which is not established here. This is a justification gap, but it affects a central step of the induction.

Fourth, the transition from “intermediate polynomial is divisible by $l(v)^2$” to “after normalization the remainder retains a factor of $l(v)$” is unjustified. The normalization step in pseudo-division is precisely where factors of $l(v)$ are divided out globally, and without a precise accounting of how many factors are introduced and removed, no conclusion about residual divisibility can be made. This is a critical error because it is the final step of the proof.

Finally, the proof never actually uses the condition $\deg(u) \ge \deg(v) + 2$ in a mathematically meaningful way. It is only referenced informally to claim “at least two steps occur,” but pseudo-division does not decompose into uniform steps of fixed effect per degree difference, so this reasoning is not valid.

## Summary

The solution is based on an incorrect abstraction of pseudo-division and an unsupported induction on coefficient divisibility. Several steps rely on properties that pseudo-division does not satisfy, and the final normalization argument is not justified.

VERDICT: FAIL - the argument misrepresents pseudo-division and does not correctly prove divisibility of the pseudo-remainder.
