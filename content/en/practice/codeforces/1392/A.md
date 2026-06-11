---
title: "CF 1392A - Omkar and Password"
description: "The proposed solution does not answer the exercise as stated. The exercise asks for values of $u$ and $v$ satisfying the prescribed binary-length conditions, $$lfloor lg u rfloor = m,qquad lfloor lg v rfloor = n,$$ such that Algorithm B requires exactly $m+1$ subtraction steps."
date: "2026-06-11T10:05:16+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1392
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 10"
rating: 800
weight: 1392
solve_time_s: 70
verified: false
draft: false
---

[CF 1392A - Omkar and Password](https://codeforces.com/problemset/problem/1392/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Correctness

The proposed solution does not answer the exercise as stated.

The exercise asks for values of $u$ and $v$ satisfying the prescribed binary-length conditions,

$$\lfloor \lg u \rfloor = m,\qquad \lfloor \lg v \rfloor = n,$$

such that Algorithm B requires exactly $m+1$ subtraction steps.

The proposed solution attempts to construct such values using Fibonacci numbers, but it never completes the construction, never proves that the subtraction count is $m+1$, and never verifies the required logarithmic conditions. The argument stops in the middle of the base case.

Even if the unfinished argument were completed, the displayed choice

$$u=F_{m+2},\qquad v=F_{n+1}$$

does not immediately imply

$$\lfloor \lg u \rfloor = m,\qquad \lfloor \lg v \rfloor = n,$$

and no proof of these equalities is supplied.

The exercise is existential, so it is sufficient to exhibit one valid family and prove that it works. The proposed solution does not reach that point.

## Gaps and Errors

**Critical error:** The proof is incomplete. The argument terminates after the sentence

> Then

and no further reasoning is given. There is no completed induction, no computation of the number of subtraction steps, and no conclusion.

**Critical error:** The claim

> if we set $u = F_{m+2},\ v = F_{n+1}$, the algorithm executes exactly $m+1$ subtraction steps

is stated without proof.

**Critical error:** The required conditions

$$\lfloor \lg u \rfloor = m,\qquad \lfloor \lg v \rfloor = n$$

are never established for the proposed values.

**Justification gap:** The solution cites

> Algorithm B reaches the maximum number of subtraction steps when $u$ and $v$ are consecutive Fibonacci numbers

and references Exercise 4.5.2-33. No derivation is provided. A citation could be acceptable if the referenced result directly applies, but the solution must still explain why the particular pair chosen satisfies the present exercise. That connection is missing.

**Justification gap:** The induction on $m-n$ is announced but never carried out. Neither the induction hypothesis nor the induction step is stated.

## Summary

The solution is unfinished. The central claim is asserted but not proved, the logarithmic constraints are not verified, and the argument stops before reaching any conclusion.

VERDICT: FAIL - the proposed proof is incomplete and never establishes either the subtraction count or the required logarithmic conditions.
