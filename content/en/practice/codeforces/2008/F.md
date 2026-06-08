---
title: "CF 2008F - Sakurako's Box"
description: "This is a Type B (prove) problem. The requirement is to prove that for every point $P$ in the plane and for every choice of the distinguished vertex of the isosceles trapezoid, the sum of the distances from $P$ to the other three vertices is strictly greater than the distance…"
date: "2026-06-08T13:25:38+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2008
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 970 (Div. 3)"
rating: 1400
weight: 2008
solve_time_s: 42
verified: false
draft: false
---

[CF 2008F - Sakurako's Box](https://codeforces.com/problemset/problem/2008/F)

**Rating:** 1400  
**Tags:** combinatorics, math, number theory  
**Solve time:** 42s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B (prove)** problem.

The requirement is to prove that for every point $P$ in the plane and for every choice of the distinguished vertex of the isosceles trapezoid, the sum of the distances from $P$ to the other three vertices is strictly greater than the distance from $P$ to the distinguished vertex.

## Step-by-Step Verification

**Step 1: Let $ABCD$ be an isosceles trapezoid with $AB\parallel CD$ and $AB>CD$. - VALID.**

This is a legitimate normalization.

**Step 2: Split the vertices into two types, those on the shorter base and those on the longer base. - VALID.**

This is a reasonable proof strategy.

**Step 3: For a vertex on the shorter base, use**

$PA+PB\ge AB$

and

$PD-PC\le CD.$

**- VALID.**

These are standard triangle and reverse triangle inequalities.

**Step 4: Deduce**

$PA+PB+PC-PD\ge AB-(PD-PC)\ge AB-CD>0.$

**- VALID.**

Since $AB>CD$, this correctly proves

$PA+PB+PC>PD.$

The same argument proves the corresponding inequality for $C$.

**Step 5: For a vertex on the longer base $A$, use**

$PC+PD\ge CD$

and

$|PA-PD|\le AD.$

**- VALID.**

Both inequalities are correct.

**Step 6: Claim**

$PB+PC+PD-PA\ge PC+PD-(PA-PB)\ge CD-AD>0.$

**- WRONG (Critical error).**

The displayed inequality does not follow from the preceding estimates.

From

$|PA-PD|\le AD$

one may deduce

$PA-PD\le AD,$

but this gives no control over the quantity

$PA-PB.$

The proof silently replaces $PA-PB$ by something bounded by $AD$, which is unjustified.

Indeed, the estimate

$PC+PD-(PA-PB)\ge CD-AD$

would require

$PA-PB\le AD,$

and no such inequality has been established.

**Step 7: Claim that $CD-AD>0$. - WRONG (Critical error).**

The proof explicitly asserts strict positivity of

$CD-AD.$

This is generally false.

For an isosceles trapezoid with coordinates

$A=(-5,0),\quad B=(5,0),\quad D=(-1,4),\quad C=(1,4),$

we have

$CD=2,\qquad AD=\sqrt{32}\approx5.66,$

so

$CD-AD<0.$

Thus even if the previous step were justified, the conclusion would still fail.

**Step 8: Deduce the case of vertex $B$ by symmetry. - UNJUSTIFIED.**

The symmetry argument depends on the validity of Step 6. Since Step 6 is invalid, this deduction is unsupported.

**Step 9: Conclude that all four vertex cases are proved. - WRONG (Critical error).**

Only the cases corresponding to vertices $C$ and $D$ have actually been established.

The cases corresponding to $A$ and $B$ remain unproved.

## Completeness Check

The proof is incomplete.

The argument for vertices on the shorter base is correct and complete.

The argument for vertices on the longer base contains two independent fatal defects:

1. It uses an inequality involving $PA-PB$ that does not follow from the reverse triangle inequality applied to $A,D,P$.
2. It relies on the false claim that $CD-AD>0$.

Because of these errors, the inequalities

$PB+PC+PD>PA$

and

$PA+PC+PD>PB$

are not proved.

The final conclusion therefore does not follow from what has actually been established.

## Summary

The proof successfully handles the vertices on the shorter base but fails completely for the vertices on the longer base. The key estimate for vertex $A$ is invalid, and it additionally depends on the false inequality $CD>AD$.

VERDICT: FAIL - the proof's argument for vertices on the longer base is invalid because it unjustifiably bounds $PA-PB$ and incorrectly assumes $CD-AD>0$.
