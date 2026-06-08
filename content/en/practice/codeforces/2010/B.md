---
title: "CF 2010B - Three Brothers"
description: "This is a Type B (proof) problem. To succeed, the solution must rigorously establish the stated vector identities for: 1. An equilateral triangle. 2. An arbitrary regular $n$-gon. 3. A regular tetrahedron."
date: "2026-06-08T13:14:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2010
codeforces_index: "B"
codeforces_contest_name: "Testing Round 19 (Div. 3)"
rating: 800
weight: 2010
solve_time_s: 71
verified: false
draft: false
---

[CF 2010B - Three Brothers](https://codeforces.com/problemset/problem/2010/B)

**Rating:** 800  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a Type B (proof) problem.

To succeed, the solution must rigorously establish the stated vector identities for:

1. An equilateral triangle.
2. An arbitrary regular $n$-gon.
3. A regular tetrahedron.

A proof of the general regular $n$-gon case together with the specialization $n=3$ is acceptable for parts (1) and (2). A separate proof is required for the tetrahedron.

## Step-by-Step Verification

### Step 1: Derivation of

$$K_i=M+(r-u_i\cdot M)u_i$$

and

$$\overrightarrow{MK_i}=(r-u_i\cdot M)u_i$$

- VALID

The side or face is represented by

$$u_i\cdot x=r.$$

Writing

$$K_i=M+t_i u_i$$

and substituting into the equation of the side or face gives

$$u_i\cdot M+t_i=r,$$

since $|u_i|=1$. Hence

$$t_i=r-u_i\cdot M.$$

The formula follows correctly.

### Step 2: Summation formula

$$\sum \overrightarrow{MK_i}
=
r\sum u_i-\sum (u_i\cdot M)u_i$$

- VALID

This is immediate from linearity.

### Step 3: For a regular $n$-gon,

$$\sum_{i=1}^n u_i=0$$

- VALID

The outward normals are equally spaced unit vectors on the circle. Their vector sum is zero.

The statement is intended for regular polygons, hence $n\ge 3$. Checking small values:

For $n=3$, $n=4$, and $n=5$, the claim is correct.

### Step 4: Definition of

$$T(x)=\sum_i (u_i\cdot x)u_i$$

and reduction to

$$\sum_i\overrightarrow{MK_i}=-T(M)$$

- VALID

This is a direct rewriting of Step 2 using Step 3.

### Step 5: $T$ commutes with rotation by $2\pi/n$

- UNJUSTIFIED

Classification: **Justification gap**

The proof states:

> By symmetry, $T$ commutes with the rotation through $2\pi/n$.

This is true, but no argument is given in the Solution section.

A complete proof would show that the rotation permutes the normals and then compute

$$T(Rx)=RT(x).$$

The claim is standard and almost certainly intended, but it is not actually proved.

### Step 6: A symmetric $2\times2$ matrix commuting with a nontrivial rotation is a scalar multiple of the identity

- UNJUSTIFIED

Classification: **Justification gap**

The statement is correct.

However, the solution merely asserts it:

> A symmetric $2\times2$ matrix commuting with a nontrivial rotation is a scalar multiple of the identity.

No proof is supplied.

A rigorous argument would either compute the commutant of the rotation matrix explicitly or invoke a previously established linear algebra fact.

### Step 7: Trace computation

$$\operatorname{tr}(T)
=
\sum_i \operatorname{tr}(u_i u_i^T)
=
n$$

and hence

$$T=\frac n2 I$$

- VALID

Assuming Step 6, the trace computation is correct.

### Step 8: Deduction of the regular $n$-gon identity

- INCOMPLETE

Classification: **Critical error**

The proof ends with

$$T=\frac n2 I.$$

Immediately afterward the manuscript terminates with

$$\text{“Consequently }\su”$$

The argument never actually derives

$$\sum_i \overrightarrow{MK_i}
=
\frac n2\,\overrightarrow{MO},$$

nor does it explicitly derive the triangle case from $n=3$.

The intended conclusion is obvious from the preceding work, but it is not present in the submitted proof.

### Step 9: Irreducibility argument for the tetrahedron

- NOT REACHED IN THE SOLUTION

The Proof Architecture section contains a plausible irreducibility argument.

However, the actual Solution section is truncated before the tetrahedron proof begins.

A proof architecture is not a proof. Only the Solution section establishes results.

### Step 10: Tetrahedron identity

- NOT PROVED

Classification: **Critical error**

The tetrahedron argument never appears in the Solution section because the proof is cut off beforehand.

The required identity

$$\overrightarrow{MK_1}+\overrightarrow{MK_2}
+\overrightarrow{MK_3}+\overrightarrow{MK_4}
=
\frac43\,\overrightarrow{MO}$$

is never established.

## Completeness Check

The proposed solution is incomplete.

The regular $n$-gon proof is truncated before the final deduction. The equilateral-triangle conclusion is never explicitly obtained. The tetrahedron proof is entirely absent from the Solution section.

There are also two unproved assertions in the polygon argument:

$$TR=RT$$

and

> a symmetric $2\times2$ matrix commuting with a nontrivial rotation is a scalar multiple of the identity.

These are justification gaps.

The more serious issue is that the submitted proof literally stops before completing the polygon argument and before presenting any tetrahedron proof.

The final conclusions do not follow from the written Solution because the required derivations are missing.

## Summary

The mathematical approach is sound and appears headed toward a correct proof. The irreducibility argument sketched in the Proof Architecture would likely repair the tetrahedral symmetry issue that existed in earlier versions.

However, the submitted Solution is incomplete. It terminates in the middle of the polygon proof and never contains the tetrahedron proof. As written, the required statements are not proved.

VERDICT: FAIL - the solution is incomplete, terminating before finishing the polygon proof and before proving the tetrahedron case.
