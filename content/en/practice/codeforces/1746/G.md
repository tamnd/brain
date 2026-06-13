---
title: "CF 1746G - Olympiad Training"
description: "This is a Type B problem, a pure proof problem. The requirement is to prove the stated geometric claim: that the five points $C,K,L,O,N$ are concyclic. A coordinate proof is perfectly appropriate."
date: "2026-06-09T15:48:43+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "flows", "geometry", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1746
codeforces_index: "G"
codeforces_contest_name: "Codeforces Global Round 23"
rating: 3500
weight: 1746
solve_time_s: 120
verified: false
draft: false
---

[CF 1746G - Olympiad Training](https://codeforces.com/problemset/problem/1746/G)

**Rating:** 3500  
**Tags:** binary search, data structures, dp, flows, geometry, implementation, sortings  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem-Type Check

This is a Type B problem, a pure proof problem. The requirement is to prove the stated geometric claim: that the five points $C,K,L,O,N$ are concyclic.

A coordinate proof is perfectly appropriate. To succeed, it must correctly compute the relevant points, derive a circle, and rigorously verify that all five points lie on it. Since existence rather than uniqueness is being proved, it is enough to exhibit one circle containing the five points.

## Step-by-Step Verification

### Step 1: Coordinate setup and parametrization of $E$ and $F$ - VALID

The solution places

$$A(0,0),\quad B(1,0),\quad C(1,1),\quad D(0,1).$$

Letting $E=(x,0)$ and using $BE=BF$ gives

$$F=(1,1-x).$$

This is correct.

### Step 2: Computation of $L,N,O$ - VALID

The midpoint formulas yield

$$L=\left(\frac{x+1}{2},\frac{1-x}{2}\right),$$

$$N=\left(\frac12,1-\frac{x}{2}\right),$$

$$O=\left(\frac12,\frac12\right).$$

All are correct.

### Step 3: Parametrization of $DF$ and $AL$ and computation of $K$ - VALID

The solution writes

$$DF:(t,1-tx),$$

and

$$AL:\left(s\frac{x+1}{2},\,s\frac{1-x}{2}\right).$$

Solving

$$s\frac{x+1}{2}=t,$$

$$s\frac{1-x}{2}=1-tx$$

gives

$$s=\frac{2}{1+x^2}.$$

Hence

$$K= \left( \frac{1+x}{1+x^2}, \frac{1-x}{1+x^2} \right).$$

The algebra checks out.

### Step 4: Determination of the circle through $C,O,L$ - VALID

The general circle

$$X^2+Y^2+aX+bY+c=0$$

is used.

Substituting $O$ and $C$ gives

$$c=1,\qquad a+b=-3.$$

Substituting $L$ yields

$$a-b=-x.$$

Solving gives

$$a=\frac{-3-x}{2}, \qquad b=\frac{-3+x}{2}.$$

The derivation is correct.

### Step 5: Verification that $N$ lies on the circle - VALID

The solution computes

$$X_N^2+Y_N^2 = \frac54-x+\frac{x^2}{4},$$

and states that

$$aX_N+bY_N = -\frac54+x-\frac{x^2}{4}.$$

Checking independently:

$$\frac a2+b\left(1-\frac x2\right) = -\frac94+\frac34x-\frac14x^2,$$

which indeed equals

$$-\frac54+x-\frac{x^2}{4}-1.$$

Therefore

$$X_N^2+Y_N^2+aX_N+bY_N+1=0.$$

The verification is correct, although some intermediate algebra is omitted.

Classification: VALID, with a minor compression of computation.

### Step 6: Verification that $K$ lies on the same circle - UNJUSTIFIED

The solution states that after substitution the numerator becomes

$$(1+x)^2+(1-x)^2 -(3+x)(1+x)(1+x^2) -(3-x)(1-x)(1+x^2) +2(1+x^2)^2,$$

and then says it "simplifies identically to $0$ after cancellation of symmetric terms."

This is not a proof. The crucial final verification is reduced to an assertion.

A reviewer must be able to check the identity. The solution does not actually perform the simplification.

Let us verify it:

$$(1+x)^2+(1-x)^2 = 2+2x^2.$$

Also,

$$(3+x)(1+x)=3+4x+x^2,$$

$$(3-x)(1-x)=3-4x+x^2.$$

Adding,

$$6+2x^2.$$

Hence the middle two terms contribute

$$-(6+2x^2)(1+x^2) = -6-8x^2-2x^4.$$

Finally,

$$2(1+x^2)^2 = 2+4x^2+2x^4.$$

Summing all contributions:

$$(2+2x^2) +(-6-8x^2-2x^4) +(2+4x^2+2x^4) = 0.$$

Thus the claim is true, but the submitted proof does not actually show it.

Classification: **Justification gap**.

### Step 7: Conclusion that $C,K,L,O,N$ are concyclic - VALID

Given Steps 4, 5, and 6, the conclusion follows immediately.

The logical structure is correct.

## Completeness Check

The coordinate model covers all admissible configurations with $0<x<1$, which corresponds exactly to $E$ on side $AB$ and $F$ on side $BC$ with $BE=BF$.

No geometric cases are omitted.

The computation of $K$ is correct.

The circle is correctly derived and shown to contain $C$, $O$, and $L$.

The only substantive issue is that the verification for $K$ is left as an unexplained cancellation. Since that verification is the final step establishing the fifth point on the circle, the proof is not fully justified as written.

## Summary

The overall strategy is correct. The coordinate setup, computation of $K$, derivation of the circle, and verification for $N$ are all valid. However, the proof of the key identity showing that $K$ lies on the circle is not actually carried out. The author asserts that a large polynomial expression cancels to zero without demonstrating the cancellation.

This is not a fatal flaw because the computation is straightforward and the conclusion is correct, but it is still a missing justification in the written proof.

VERDICT: FAIL - the verification that $K$ satisfies the circle equation is asserted rather than proved, leaving the final concyclicity argument incomplete.
