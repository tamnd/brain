---
title: "CF 2011H - Strange Matrix"
description: "This is a Type B (proof) problem. The required task is to prove the stated vector identities for: 1. An equilateral triangle. 2. A regular $n$-gon. 3. A regular tetrahedron. A valid solution must establish the identities themselves."
date: "2026-06-08T13:11:48+07:00"
tags: ["codeforces", "competitive-programming", "*special", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2011
codeforces_index: "H"
codeforces_contest_name: "Kotlin Heroes: Episode 11"
rating: 0
weight: 2011
solve_time_s: 47
verified: false
draft: false
---

[CF 2011H - Strange Matrix](https://codeforces.com/problemset/problem/2011/H)

**Rating:** -  
**Tags:** *special, graphs, greedy  
**Solve time:** 47s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B (proof)** problem.

The required task is to prove the stated vector identities for:

1. An equilateral triangle.
2. A regular $n$-gon.
3. A regular tetrahedron.

A valid solution must establish the identities themselves. No classification, optimization, or construction requirements arise.

The proposed solution attempts to prove the general regular $n$-gon statement, derive the triangle case as $n=3$, and then prove the tetrahedron case separately. That strategy is appropriate.

## Step-by-Step Verification

### Step 1: Derivation of

$$\overrightarrow{MK_i}=(r-u_i\cdot M)u_i$$

The solution writes the supporting line or plane as

$$u_i\cdot x=r$$

and represents the foot of the perpendicular as

$$K_i=M+t_i u_i.$$

Substituting into the equation of the line or plane gives

$$t_i=r-u_i\cdot M.$$

Hence

$$\overrightarrow{MK_i}=(r-u_i\cdot M)u_i.$$

**Status:** VALID.

The computation is correct for both the polygon and tetrahedron settings.

### Step 2: Summation formula

Summing the previous identity yields

$$\sum_i \overrightarrow{MK_i}
=
r\sum_i u_i
-
\sum_i (u_i\cdot M)u_i.$$

**Status:** VALID.

This follows directly from linearity.

### Step 3: For a regular $n$-gon,

$$\sum_i u_i=0$$

The outward unit normals are equally spaced around the unit circle.

**Status:** VALID.

For a regular $n$-gon with $n\ge3$, the vector sum of these equally spaced directions is indeed zero.

### Step 4: Definition of the operator

The solution defines

$$T(x)=\sum_i (u_i\cdot x)u_i$$

and rewrites the desired sum as

$$\sum_i \overrightarrow{MK_i}
=
-T(M).$$

**Status:** VALID.

### Step 5: $T$ commutes with the rotation of angle $2\pi/n$

The argument uses the fact that the rotation permutes the normals.

**Status:** VALID.

The displayed computation correctly shows

$$TR=RT.$$

### Step 6: Deduction that $T=\lambda I$ in the polygon case

The solution states that a real $2\times2$ matrix commuting with a rotation through an angle different from $0$ and $\pi$ must have the form

$$\begin{pmatrix}
a&-b\\
b&a
\end{pmatrix}.$$

Since $T$ is symmetric, it follows that $b=0$, so

$$T=\lambda I.$$

**Status:** VALID.

For regular polygons, $n\ge3$, hence $2\pi/n\neq0,\pi$.

### Step 7: Trace computation in the polygon case

The solution computes

$$\operatorname{tr}(T)
=
\sum_i \operatorname{tr}(u_i u_i^T)
=
\sum_i |u_i|^2
=
n.$$

Since $T=\lambda I$ on a two-dimensional space,

$$2\lambda=n.$$

Therefore

$$T=\frac n2 I.$$

**Status:** VALID.

### Step 8: Deduction of the regular $n$-gon identity

Substituting $T=(n/2)I$ gives

$$\sum_i \overrightarrow{MK_i}
=
-\frac n2 M.$$

Because the origin is placed at $O$,

$$\overrightarrow{MO}=-M.$$

Hence

$$\sum_i \overrightarrow{MK_i}
=
\frac n2\,\overrightarrow{MO}.$$

**Status:** VALID.

### Step 9: Derivation of the equilateral triangle case

Setting $n=3$ gives

$$\sum_{i=1}^3 \overrightarrow{MK_i}
=
\frac32\,\overrightarrow{MO}.$$

**Status:** VALID.

### Step 10: For the tetrahedron,

$$\sum_i u_i=0$$

The solution invokes tetrahedral symmetry.

**Status:** VALID.

The outward normals of the four faces are symmetrically arranged and their sum is zero.

### Step 11: Definition of the tetrahedral operator

The solution again defines

$$T(x)=\sum_{i=1}^4 (u_i\cdot x)u_i$$

and obtains

$$\sum_{i=1}^4 \overrightarrow{MK_i}
=
-T(M).$$

**Status:** VALID.

### Step 12: Claim that the tetrahedral symmetry group acts irreducibly on $\mathbb R^3$

The solution states:

> The rotation group of the tetrahedron acts irreducibly on $\mathbb R^3$.

and then applies Schur's lemma.

**Status:** UNJUSTIFIED.

**Classification:** Justification gap.

The statement is true, but the solution does not prove irreducibility.

This is a substantial omitted lemma. To invoke Schur's lemma, irreducibility must first be established. The solution provides neither a proof of irreducibility nor an alternative direct argument.

The gap is repairable. For example, one could show that any nonzero invariant subspace would contain the orbit of a nonzero vector under the tetrahedral group, and that orbit spans all of $\mathbb R^3$. Alternatively, one could bypass representation theory entirely and compute directly using coordinates for the four normals.

### Step 13: Deduction that

$$T=\lambda I$$

The conclusion follows from Schur's lemma only after irreducibility has been established.

**Status:** UNJUSTIFIED.

**Classification:** Justification gap.

The conclusion is correct, but the prerequisite needed to apply Schur's lemma was not proved.

### Step 14: Trace computation in the tetrahedron case

Assuming $T=\lambda I$,

$$\operatorname{tr}(T)
=
4,
\qquad
3\lambda=4,
\qquad
\lambda=\frac43.$$

**Status:** VALID.

### Step 15: Final tetrahedron identity

Using

$$T=\frac43 I,$$

the solution obtains

$$\sum_{i=1}^4 \overrightarrow{MK_i}
=
\frac43\,\overrightarrow{MO}.$$

**Status:** VALID provided Steps 12 and 13 are justified.

## Completeness Check

The regular polygon proof is complete and rigorous.

The tetrahedron proof is not complete. The argument relies on the statement that the tetrahedral rotation group acts irreducibly on $\mathbb R^3$, then invokes Schur's lemma. Neither the irreducibility claim nor a direct replacement argument is supplied.

The final displayed formula for the tetrahedron is also truncated in the submitted text, but the preceding discussion makes the intended conclusion clear. The real mathematical issue is the missing justification of irreducibility.

No other cases are omitted. The regular $n$-gon statement is intended for $n\ge3$, so there is no issue with $n=1$ or $n=2$.

## Summary

The polygon part is fully correct.

The tetrahedron argument still contains the same essential gap identified in the earlier review. The solution replaces the previous symmetry argument with an appeal to Schur's lemma, but it does not prove the necessary hypothesis that the tetrahedral rotation representation on $\mathbb R^3$ is irreducible. Consequently the deduction that $T$ is a scalar multiple of the identity is not established within the proof.

VERDICT: FAIL - the tetrahedron proof invokes Schur's lemma without proving the required irreducibility of the tetrahedral rotation action on $\mathbb R^3$.
