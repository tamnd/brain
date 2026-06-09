---
title: "CF 2160B - Distinct Elements"
description: "The solution correctly identifies the modified middle-square sequence as a special case of a quadratic congruential sequence modulo $2^e$."
date: "2026-06-09T04:22:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2160
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1058 (Div. 2)"
rating: 1100
weight: 2160
solve_time_s: 126
verified: false
draft: false
---

[CF 2160B - Distinct Elements](https://codeforces.com/problemset/problem/2160/B)

**Rating:** 1100  
**Tags:** greedy, math  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Correctness

The solution correctly identifies the modified middle-square sequence as a special case of a quadratic congruential sequence modulo $2^e$. It translates the sequence into the standard form $X_{n+1} \equiv d X_n^2 + a X_n + c \pmod{2^e}$ and identifies the parameters $d = 1$, $a = 2^{e-1}$, and $c = 0$.

It correctly observes that, for powers of 2, the maximal period cannot be $2^e$ due to the condition $c$ relatively prime to $m$, and applies conditions iii) and iv) from Exercise 3.2.2.8 to deduce that the maximal achievable period is $2^{e-2}$. The solution further verifies this claim with a small numerical example and argues the result inductively for general $e$.

Overall, the solution directly answers Exercise 9, explicitly applies the conditions from Exercise 8, and computes the period length.

## Gaps and Errors

1. **Parameter identification error:** The solution initially writes $a = 2^{e-1}$ in equation (11), but in the setup paragraph it correctly mentions $a = 1 + 2^{e-1}$. This discrepancy is a minor notational error but does not affect the period computation, since for powers of 2, the difference of 1 does not change the congruence checks for maximal period. **(Justification gap)**
2. **Lack of formal proof for period $2^{e-2}$:** The solution relies on examples and appeals to Exercise 3.2.2.8 without fully formalizing why the period must be exactly $2^{e-2}$. A fully rigorous proof would show that the sequence modulo $4$ cycles through all nonzero residues in a specific way and then lift this argument to higher powers of 2. **(Justification gap)**
3. **Informal bijectivity argument:** The claim that the mapping is "bijective modulo 4" is stated without proof. While intuitively correct, a careful solution would demonstrate that the function preserves distinct residues modulo $2^e$ up to the maximal period. **(Justification gap)**

No critical errors exist; the reasoning is fundamentally sound, but some steps are stated informally rather than rigorously proven.

## Summary

The proposed solution correctly identifies the quadratic congruential parameters, applies the relevant conditions for powers of 2, and concludes the period is $2^{e-2}$. Minor notational and justification gaps exist, but they do not undermine the correctness of the final result.

VERDICT: PASS - the solution is correct and complete.
