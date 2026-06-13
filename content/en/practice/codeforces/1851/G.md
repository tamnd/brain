---
title: "CF 1851G - Vlad and the Mountains"
description: "The solution does answer the correct exercise: it attempts to extend Lemma B from integral $c$ to arbitrary real $c$ with $0le c<k$, and it proposes an explicit reciprocity formula. However, the proof does not justify the formula it claims."
date: "2026-06-09T17:21:09+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dsu", "graphs", "implementation", "sortings", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 2000
weight: 1851
solve_time_s: 122
verified: false
draft: false
---

[CF 1851G - Vlad and the Mountains](https://codeforces.com/problemset/problem/1851/G)

**Rating:** 2000  
**Tags:** binary search, data structures, dsu, graphs, implementation, sortings, trees, two pointers  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Correctness

The solution does answer the correct exercise: it attempts to extend Lemma B from integral $c$ to arbitrary real $c$ with $0\le c<k$, and it proposes an explicit reciprocity formula.

However, the proof does not justify the formula it claims. The central difficulty in generalizing Lemma B is determining exactly how the boundary terms arising from the sawtooth function change when $c$ is no longer integral. The solution simply asserts the form of those corrections without deriving them. As a result, the displayed formula (8) is not established.

Moreover, the final consistency check with the integral case is incorrect. The claimed reduction to Lemma B does not actually reproduce the stated integral formula in all cases.

Therefore the proof is not complete and cannot be accepted as a valid derivation of the generalized reciprocity law.

## Gaps and Errors

### 1. Critical error: Equation (3) is asserted, not derived

The proof states

$$R(h,k,c) = R(h,k,0) +\frac{6c^{2}}{hk} -6\Bigl\lfloor\frac ch\Bigr\rfloor +B(c). \tag{3}$$

This is presented as something that follows from "following exactly the derivation of Lemma B".

No derivation is given.

The entire problem is to determine how the reciprocity formula changes when $c$ becomes real. The appearance of the terms

$$\frac{6c^{2}}{hk} \qquad\text{and}\qquad -6\Bigl\lfloor\frac ch\Bigr\rfloor$$

must be proved from the actual expansion. They cannot simply be imported from the integral case.

Since (3) is the foundation for everything that follows, the argument is incomplete.

### 2. Critical error: The boundary correction $B(c)$ is guessed rather than computed

The proof claims:

> Each such boundary point contributes $-3$ to the reciprocity sum.

and concludes

$$B(c) = -3\,\delta(c) -3\,\delta(r) +3.$$

No calculation is given.

The reciprocity proof of Lemma B contains a delicate lattice-point count. For real $c$, the locations where the sawtooth arguments become integral must be analyzed explicitly. The solution never performs this analysis.

Instead it identifies two possible boundary conditions and assigns a contribution $-3$ to each by assertion.

This is precisely the new phenomenon that must be established in the generalization, so the omission is fatal.

### 3. Critical error: No proof that the only boundary conditions are $c\in\mathbb Z$ and $r\in\mathbb Z$

The proof states:

$$c\in\mathbb Z, \qquad r=c-qh\in\mathbb Z.$$

and claims these are the only sources of boundary corrections.

No justification is provided.

The actual reciprocity argument involves integrality of expressions occurring inside the sawtooth functions. It is not shown that these conditions reduce exactly to the two displayed indicators.

The validity of formula (5) therefore remains unproved.

### 4. Critical error: The reduction to Lemma B is not correctly verified

The proof claims

$$-3-3[c\bmod h=0] = -3e(h,c)+3.$$

Let $c=0$.

Then the left-hand side equals

$$-3-3=-6,$$

while

$$e(h,0)=1,$$

so the right-hand side equals

$$-3(1)+3=0.$$

The two sides are not equal.

Hence the displayed identity is false.

Since this identity is used to recover Lemma B from the proposed generalization, the consistency check fails.

### 5. Critical error: The claimed equivalence with Lemma B does not follow

Because the preceding identity is false, equation (9) does not reduce to the stated form of Lemma B.

Thus the solution fails its own verification step.

Any proposed generalization must reproduce the known integral formula exactly. The proof does not establish this.

### 6. Justification gap: Use of $c \bmod h$ for real $c$

The notation

$$c\bmod h$$

is used for real $c$.

Although it can be interpreted as

$$c-h\Bigl\lfloor\frac ch\Bigr\rfloor,$$

the proof should define this explicitly before employing indicator functions such as

$$\delta(c\bmod h).$$

This issue is minor compared with the substantive errors above.

## Summary

The solution tackles the correct exercise, but the crucial boundary-term analysis is never carried out. The proposed correction term $B(c)$ is asserted rather than derived, and the final check against the known integral version of Lemma B contains a direct algebraic contradiction.

VERDICT: FAIL - the proposed reciprocity formula is not derived, and its claimed reduction to Lemma B is mathematically incorrect.
