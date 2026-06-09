---
title: "CF 2002C - Black Circles"
description: "This is a counting problem, so it falls under Type C. The goal is to determine the exact number of admissible fillings of the strip. The solution must provide a precise count and justify the enumeration rigorously."
date: "2026-06-08T13:53:49+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2002
codeforces_index: "C"
codeforces_contest_name: "EPIC Institute of Technology Round August 2024 (Div. 1 + Div. 2)"
rating: 1200
weight: 2002
solve_time_s: 82
verified: false
draft: false
---

[CF 2002C - Black Circles](https://codeforces.com/problemset/problem/2002/C)

**Rating:** 1200  
**Tags:** brute force, geometry, greedy, math  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **counting problem**, so it falls under Type C. The goal is to determine the exact number of admissible fillings of the strip. The solution must provide a precise count and justify the enumeration rigorously. The proposed solution attempts a complete count via a bijection between fillings and sequences of left/right expansions, which is appropriate for Type C.

## Step-by-Step Verification

**Step 1: Computation of small cases $a_1=1$, $a_2=2$, $a_3=4$. - VALID.**

Direct enumeration for $n=1,2,3$ is correct.

**Step 2: Observation that the occupied squares always form a contiguous interval. - VALID.**

Induction argument is correct: if the occupied set is $[L,R]$, the next square must be $L-1$ or $R+1$ (when they exist), so the interval property is preserved.

**Step 3: Every filling for fixed starting position $i$ corresponds to a sequence of $i-1$ $L$ moves and $n-i$ $R$ moves. - VALID.**

This follows from the interval property. Each step enlarges the interval at one of the two ends.

**Step 4: Every sequence of $i-1$ $L$s and $n-i$ $R$s gives a valid filling. - VALID.**

Checked carefully: at each stage, there is always at least one square available at the intended end. No sequence can run out of available squares prematurely.

**Step 5: The correspondence between fillings and $L/R$-sequences is bijective. - VALID.**

Injectivity: sequence is uniquely determined by the filling.

Surjectivity: Step 4 ensures every such sequence produces a filling.

**Step 6: Number of fillings for fixed $i$ is $\binom{n-1}{i-1}$. - VALID.**

Choosing the positions of the $i-1$ left expansions among $n-1$ steps is correct combinatorics.

**Step 7: Total number of fillings is $\sum_{i=1}^{n} \binom{n-1}{i-1} = 2^{n-1}$. - VALID.**

Direct application of the binomial theorem.

**Step 8: Verification for small $n$ and generalization. - VALID.**

Formula matches manually computed values for $n=1,2,3,4$, and argument applies for all $n\ge 1$.

**Step 9: Alternative arguments (backward construction, time of left expansions). - VALID.**

These provide independent confirmation of the count and strengthen the solution.

## Completeness Check

All implicit assumptions are justified:

- Interval property: proved by induction.
- Bijection: both injectivity and surjectivity argued carefully.
- Counting: uses standard combinatorial reasoning.
- Edge cases ($n=1,2$) handled.
- No unhandled cases remain.

The final conclusion follows directly from the established lemmas and combinatorial count.

## Summary

The proposed solution is thorough, mathematically rigorous, and free of gaps. The bijection argument, counting, and verification steps fully justify the answer.

VERDICT: PASS - the solution is complete and all steps are correctly justified.
