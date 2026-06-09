---
title: "CF 2002E - Cosmic Rays"
description: "This is a Type C problem: a precise numerical count of admissible fillings is requested. The solution produces a combinatorial formula $an = 2^{n-1}$ and rigorously justifies it via bijection arguments and induction."
date: "2026-06-08T13:57:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2002
codeforces_index: "E"
codeforces_contest_name: "EPIC Institute of Technology Round August 2024 (Div. 1 + Div. 2)"
rating: 2300
weight: 2002
solve_time_s: 134
verified: false
draft: false
---

[CF 2002E - Cosmic Rays](https://codeforces.com/problemset/problem/2002/E)

**Rating:** 2300  
**Tags:** brute force, data structures, dp  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a Type C problem: a precise numerical count of admissible fillings is requested. The solution produces a combinatorial formula $a_n = 2^{n-1}$ and rigorously justifies it via bijection arguments and induction. The solution addresses both existence and uniqueness in the bijection and includes verification by small cases. Type requirements are satisfied.

## Step-by-Step Verification

**Step 1: Small cases enumeration $a_1=1, a_2=2, a_3=4$ - VALID.**

Direct counting confirms the sequence; checked manually for $n=1,2,3$.

**Step 2: Observation that occupied squares always form a contiguous interval - VALID.**

Inductive argument is sound: if occupied squares form $[L,R]$, the next number must be added at $L-1$ or $R+1$. Verified for small $n$ and general $n$. No interior gaps arise.

**Step 3: Encoding fillings as sequences of left/right expansions - VALID.**

Correctly models the growth of the interval; no cases are missed.

**Step 4: Counting sequences for fixed starting position $i$ as $\binom{n-1}{i-1}$ - VALID.**

Number of ways to place $i-1$ left expansions among $n-1$ steps is correct.

**Step 5: Summing over starting positions $i$ to get $2^{n-1}$ - VALID.**

Sum $\sum_{i=1}^n \binom{n-1}{i-1} = 2^{n-1}$ follows from binomial theorem. Verified for small $n=1,2,3,4$.

**Step 6: Bijection existence and uniqueness - VALID.**

Both directions of the correspondence are justified: every filling maps to a unique L/R sequence, and every L/R sequence produces a valid filling without gaps or overflows.

**Step 7: Alternative backward argument - VALID.**

Removes numbers from ends iteratively; reproduces the same count $2^{n-1}$, confirming the forward argument.

## Completeness Check

All implicit assumptions (interval property, end expansions, correct counting, adjacency rule) are explicitly justified. Small $n$ cases are checked. No unhandled configurations or boundary issues exist. The final conclusion logically follows from the proved lemmas.

## Summary

The solution is fully rigorous, carefully justified at each step, and complete. There are no gaps or errors in logic. The combinatorial reasoning and bijection are clear and correct.

VERDICT: PASS - the solution is complete and all steps are correctly justified.
