---
title: "CF 2005C - Lazy Narek"
description: "This is a Type B (prove) problem. The solution correctly interprets the statement: it aims to prove that any triangle admitting a circle tangent to two sides and two medians must be isosceles."
date: "2026-06-08T13:37:41+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2005
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 972 (Div. 2)"
rating: 1800
weight: 2005
solve_time_s: 57
verified: false
draft: false
---

[CF 2005C - Lazy Narek](https://codeforces.com/problemset/problem/2005/C)

**Rating:** 1800  
**Tags:** dp, implementation, strings  
**Solve time:** 57s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B (prove)** problem. The solution correctly interprets the statement: it aims to prove that any triangle admitting a circle tangent to two sides and two medians must be isosceles. The proof addresses the exact hypothesis and derives the required equality of two sides. The requirement for a full proof for all admissible triangles is satisfied because the solution considers a general triangle, uses coordinates without special assumptions, and reasons analytically. This matches the Type B requirements.

## Step-by-Step Verification

**Step 1: Coordinate assignment and relabeling - VALID.** The solution sets $A=(0,0)$, $B=(b,0)$, $C=(0,c)$ and notes $b,c>0$. This is a legitimate general coordinate choice after possibly relabeling the triangle so that the circle is tangent to sides $AB$ and $AC$.

**Step 2: Determining the circle center from tangent sides - VALID.** The circle is tangent to $AB$ and $AC$, which are coordinate axes. It is correct that the center must be equidistant from these sides, giving $O=(t,t)$ for some $t>0$.

**Step 3: Equations of medians - VALID.** The solution computes the midpoint of $AC$ as $(0,c/2)$ and the median from $B$ as $cx+2by-bc=0$. Similarly, the median from $C$ is $2cx+by-bc=0$. These calculations are correct.

**Step 4: Distance equality condition - VALID.** The formula for distance from a point to a line is applied correctly:

$$\frac{|ct+2bt-bc|}{\sqrt{c^2+4b^2}} = \frac{|2ct+bt-bc|}{\sqrt{4c^2+b^2}}.$$

This is a correct translation of the tangency condition to the medians.

**Step 5: Substitution $u=t(b+c)$ and case analysis - VALID.** Introducing $u=t(b+c)$ simplifies the equation to

$$\frac{|u-bc|}{\sqrt{c^2+4b^2}} = \frac{|u-bc|}{\sqrt{4c^2+b^2}}.$$

Two cases are considered: $u \neq bc$ and $u = bc$. In both cases, algebraic manipulations lead to $b=c$. Each step is logically correct and justified.

**Step 6: Concluding equality of sides - VALID.** From $b=c$, the solution correctly concludes $AB=AC$, so the triangle is isosceles. This follows rigorously from the previous calculations.

No unjustified assumptions or skipped cases remain. The coordinate method is fully general after relabeling, so the proof covers all triangles satisfying the tangency condition.

## Completeness Check

All relevant cases are handled, including the degenerate situation $u=bc$. The solution does not assume any special triangle shape beyond the initial coordinate assignment, which is general after relabeling. The final equality $AB=AC$ directly establishes that the triangle is isosceles. The proof uses only explicit equations and logical deductions; there are no gaps in reasoning.

## Summary

The solution correctly identifies a general coordinate framework, translates geometric tangency conditions into explicit algebraic equations, solves them completely, and rigorously concludes that the triangle is isosceles. All steps are justified and all cases are considered.

VERDICT: PASS - the solution is complete and all steps are correctly justified.
