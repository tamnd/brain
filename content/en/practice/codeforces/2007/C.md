---
title: "CF 2007C - Dora and C++"
description: "This is a Type B (prove) problem. The solution must establish that for every point $P$ in the plane and for every choice of distinguished vertex of an isosceles trapezoid, the distance from $P$ to that vertex is strictly smaller than the sum of the distances from $P$ to the…"
date: "2026-06-08T13:28:47+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2007
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 969 (Div. 2)"
rating: 1500
weight: 2007
solve_time_s: 67
verified: false
draft: false
---

[CF 2007C - Dora and C++](https://codeforces.com/problemset/problem/2007/C)

**Rating:** 1500  
**Tags:** math, number theory  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B (prove)** problem. The solution must establish that for every point $P$ in the plane and for every choice of distinguished vertex of an isosceles trapezoid, the distance from $P$ to that vertex is strictly smaller than the sum of the distances from $P$ to the other three vertices. The proposed solution attempts to handle vertices on the shorter base separately from vertices on the longer base. Handling each case or providing a fully justified symmetry argument is required.

## Step-by-Step Verification

**Step 1: Let $ABCD$ be an isosceles trapezoid with $AB\parallel CD$ and $AB>CD$, and $AD=BC$ as the legs. - VALID.**

The trapezoid normalization is standard and establishes the relevant side lengths and parallelism.

**Step 2: Classify vertices into two types: shorter base ($C,D$) and longer base ($A,B$). - VALID.**

Correctly identifies the two distinct geometric situations that must be handled.

**Step 3: For a vertex on the shorter base, say $D$, apply $PA+PB\ge AB$ and $PD-PC\le CD$, then conclude $PA+PB+PC-PD\ge AB-(PD-PC)\ge AB-CD>0$. - VALID.**

This is a correct application of the triangle inequality and reverse triangle inequality and establishes strict positivity. The same argument applies to vertex $C$.

**Step 4: For a vertex on the longer base, say $A$, apply $PC+PD\ge CD$ and $|PA-PD|\le AD$. - VALID as individual inequalities.**

The inequalities themselves are true but require careful combination to establish the desired strict inequality.

**Step 5: Attempt to conclude $PB+PC+PD-PA\ge PC+PD-(PA-PB)\ge CD-AD>0$. - WRONG (Critical error).**

This step is invalid. The bound $CD-AD$ may be negative, and the derivation $PB+PC+PD-PA\ge PC+PD-(PA-PB)$ is unjustified. The proposed solution assumes the inequality is strictly positive without providing a rigorous geometric argument for all points $P$. This is a critical error because it leaves the longer base vertices ($A,B$) unproved.

**Step 6: Deduce the vertex $B$ case by symmetry. - UNJUSTIFIED.**

The deduction relies on Step 5, which is invalid. Symmetry alone cannot establish strict positivity without first proving the inequality for $A$.

**Step 7: Conclude that all four vertex cases are proved. - WRONG (Critical error).**

Since vertices on the longer base remain unproved, the final conclusion does not follow.

## Completeness Check

The solution successfully proves the inequality for the vertices on the shorter base ($C,D$) but completely fails for vertices on the longer base ($A,B$). The approach for these vertices contains a critical error and an unjustified assumption about side lengths and triangle inequalities. No alternative argument is provided, and the claim of symmetry cannot compensate. The proof is therefore incomplete.

## Summary

The solution correctly handles vertices on the shorter base but fails entirely for vertices on the longer base. The critical flaw is the invalid derivation of strict positivity for the distances involving vertices $A$ and $B$, leaving the proof incomplete.

VERDICT: FAIL - the proof fails to establish the inequality for vertices on the longer base of the trapezoid.
