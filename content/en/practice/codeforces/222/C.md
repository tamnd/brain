---
title: "CF 222C - Reducing Fractions"
description: "This is a Type C - Optimization problem. The task is to determine the maximum number of intersections among perpendiculars drawn from each of five points to lines formed by the other four points."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1800
weight: 222
solve_time_s: 34
verified: false
draft: false
---

[CF 222C - Reducing Fractions](https://codeforces.com/problemset/problem/222/C)

**Rating:** 1800  
**Tags:** implementation, math, number theory, sortings  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type C - Optimization** problem. The task is to determine the maximum number of intersections among perpendiculars drawn from each of five points to lines formed by the other four points. Therefore, a complete proof must establish both an upper bound on the number of intersections and exhibit a geometric configuration achieving this bound. The proof must also verify that equality is possible and describe conditions under which it occurs.

## Step-by-Step Verification

**Step 1: Counting perpendiculars** - "Each point contributes 6 perpendiculars, total 30 perpendiculars." - **VALID**

The reasoning correctly counts the lines joining four points as $\binom{4}{2}=6$, and each of the five points produces a perpendicular to each of these six lines. The arithmetic $5 \cdot 6 = 30$ is correct.

**Step 2: Lemma 1 - Perpendiculars from one point to lines joining 3 other points intersect in exactly 3 points.** - **UNJUSTIFIED**

Claiming that "each pair of perpendiculars intersects exactly once" is made without proof. While the perpendiculars from a point to distinct lines in general position typically intersect, it is not justified that the intersection is always unique or that no three lines are concurrent. The step assumes a generic position but does not rigorously argue that degeneracies cannot occur, nor does it show a method to guarantee exactly 3 intersections.

_Classification_: **Justification gap**. The claim is plausible, but the argument is informal.

**Step 3: Lemma 2 - Total intersections counted as 360 using combinatorial subtraction.** - **WRONG**

The formula $\binom{30}{2} - 5 \cdot \binom{6}{2} = 360$ is **not justified geometrically**. Subtracting pairs of perpendiculars from the same point does not account for the fact that perpendiculars from different points may be parallel or coincide in degenerate ways, and it does not consider that some intersections may not exist if perpendiculars are arranged in general position. There is no rigorous argument showing that **all 360 intersections are achievable**. Counting combinatorially without geometric verification is insufficient in this problem.

_Classification_: **Critical error**. The upper bound is assumed without proof and the counting method is incorrect.

**Step 4: Lemma 3 - Convex pentagon construction achieves maximum intersections.** - **UNJUSTIFIED**

Claiming that a convex pentagon in general position produces all 360 intersections is stated without geometric proof. There is no construction or argument showing that perpendiculars from distinct points intersect exactly as required, or that triple intersections are avoided.

_Classification_: **Justification gap**. The existence of a configuration achieving the claimed maximum is not rigorously established.

**Step 5: Verification of key steps** - Subtracting 75 pairs to get 360 intersections. - **WRONG**

The verification repeats the flawed combinatorial argument from Step 3. There is no geometric reasoning confirming that no perpendiculars from distinct points fail to intersect. Counting alone cannot guarantee maximality.

**Step 6: Equality condition and final conclusion** - **UNJUSTIFIED**

The statement that equality occurs for a convex pentagon in general position relies on Lemma 3, which itself is unjustified. There is no proof that no better configuration exists.

## Completeness Check

The proof fails to rigorously justify:

1. That perpendiculars from one point to lines joining three other points intersect exactly as claimed (Step 2).
2. That the combinatorial count $\binom{30}{2} - 5 \cdot \binom{6}{2}$ accurately gives the maximum number of intersections (Step 3).
3. That a convex pentagon construction achieves the maximal number without triple intersections or parallel perpendiculars (Step 4).
4. That no configuration can exceed the claimed number of intersections.

All these gaps are critical. Without geometric verification, the combinatorial subtraction method cannot be trusted. The proof implicitly assumes "generic position ensures maximal intersections" but provides no rigorous argument.

## Summary

The proposed solution counts perpendiculars correctly but fundamentally miscalculates the number of intersections. It assumes combinatorial formulas give a geometric maximum without proof and claims a convex pentagon achieves the maximum without constructing or verifying the perpendicular intersections. The main flaws are in Step 2 (perpendicular intersection count), Step 3 (total intersections), and Step 4 (construction verification). Because the claimed maximum and equality configuration are unjustified, the proof **fails** as a rigorous solution.

VERDICT: FAIL - the proof assumes combinatorial counts reflect maximal intersections without rigorous geometric justification and fails to prove the existence of a configuration achieving the claimed maximum.
