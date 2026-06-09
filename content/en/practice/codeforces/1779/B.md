---
title: "CF 1779B - MKnez's ConstructiveForces Task"
description: "This is a Type B problem: prove impossibility. The solution correctly identifies that the task is to show that no plane can cut a regular $n$-gonal pyramid into a regular $(n+1)$-gon when $n ge 5$."
date: "2026-06-09T11:27:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1779
codeforces_index: "B"
codeforces_contest_name: "Hello 2023"
rating: 900
weight: 1779
solve_time_s: 62
verified: false
draft: false
---

[CF 1779B - MKnez's ConstructiveForces Task](https://codeforces.com/problemset/problem/1779/B)

**Rating:** 900  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a Type B problem: prove impossibility. The solution correctly identifies that the task is to show that no plane can cut a regular $n$-gonal pyramid into a regular $(n+1)$-gon when $n \ge 5$. The proposed solution is consistent with the requirements for Type B: it assumes the existence of such a section and derives a contradiction.

## Step-by-Step Verification

**Step 1: Counting vertices and edges of the pyramid and section.**

Claim: a regular $n$-gonal pyramid has $n+1$ vertices, $2n$ edges, and a section with $n+1$ vertices must meet all $n$ lateral edges and exactly one base edge. - **VALID**.

Reasoning is correct; the convexity argument ensures the section meets at most one connected base segment.

**Step 2: Labeling intersection points $P_i$ on lateral edges and $Q$ on base edge.**

Claim: section polygon is $QP_2P_3\cdots P_nP_1$. - **VALID**.

This is a legitimate labeling and preserves the cycle order.

**Step 3: Introducing parameters $t_i = SP_i/SA_i$ and analyzing side lengths $P_iP_{i+1}$.**

Claim: equality of section sides forces $t_1 = \cdots = t_n$. - **JUSTIFICATION GAP**.

The solution sketches that squared distances in lateral faces contain a term $(t_i - t_{i+1})^2$ whose vanishing is necessary for equality. While plausible, this is not rigorously proven; it assumes the dependency is quadratic with nonnegative coefficient without explicit computation. For full rigor, one must show that no other combination of $t_i$ produces equal side lengths in all lateral faces. This is the **most delicate step**, correctly identified as such.

**Step 4: Deduction that $P_1 \cdots P_n$ lies in a plane parallel to the base.**

Claim: equal $t_i$ imply plane is parallel to the base, forming a regular $n$-gon. - **VALID**, assuming Step 3.

This follows from affine geometry: all lateral edges are scaled identically from the apex.

**Step 5: Analyzing vertex $Q$ on base edge $A_1A_2$.**

Claim: sides $QP_1, QP_2 < P_1P_2$ for $n \ge 5$. - **JUSTIFICATION GAP**.

The argument invokes the interior angle of the regular $n$-gon ($\ge 108^\circ$) and claims $Q$ lies “outside” the $n$-gon, making $QP_1, QP_2 < P_1P_2$. While intuitively correct, it is stated qualitatively without precise metric or angle argument. A rigorous proof should compute the distances in terms of $t$ and the base side length.

**Step 6: Concluding contradiction and impossibility.**

Claim: section cannot be a regular $(n+1)$-gon. - **VALID**, provided Steps 3 and 5 hold.

## Completeness Check

All cases are considered: the section can only meet all lateral edges plus one base edge. The labeling is exhaustive, and the contradiction arises for $n \ge 5$. The argument does not explicitly check $n=5$ or $n=6$ numerically, but the qualitative angle argument is intended to cover all $n \ge 5$. The solution does not handle $n < 5$, but the problem specifies $n \ge 5$, so that restriction is acceptable.

The only unhandled detail is the precise verification that the distances from $Q$ to $P_1$ and $P_2$ are strictly smaller than $t a$ for all $n \ge 5$. Without a metric check, Step 5 is a **justification gap** rather than a critical error, but it is the most nontrivial missing piece.

## Summary

The solution is **essentially correct in strategy**: counting vertices, introducing parameters along lateral edges, and deriving a contradiction with an extra base vertex is the standard approach. The combinatorial reasoning and geometric labeling are valid. The two critical lemmas (equality of $t_i$ and the distance comparison with $Q$) are not fully justified with explicit computation, leaving small but nontrivial gaps.

If graded strictly for rigorous proof, these gaps prevent declaring the solution fully complete. The overall argument is likely correct and would convince a careful reader, but a mathematician seeking absolute rigor would want a precise metric or algebraic confirmation of Steps 3 and 5.

VERDICT: FAIL - equality of lateral-edge parameters $t_i$ and the distance comparison for vertex $Q$ are assumed without full rigorous justification.
