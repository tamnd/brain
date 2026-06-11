---
title: "CF 1380F - Strange Addition"
description: "The revised submission correctly identifies the structure of the problem: it must first maximize the number of leading digits equal to $d$, then select the largest 50-digit prime with that prefix."
date: "2026-06-11T10:57:56+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 1380
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 91 (Rated for Div. 2)"
rating: 2600
weight: 1380
solve_time_s: 144
verified: false
draft: false
---

[CF 1380F - Strange Addition](https://codeforces.com/problemset/problem/1380/F)

**Rating:** 2600  
**Tags:** data structures, dp, matrices  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Correctness

The revised submission correctly identifies the structure of the problem: it must first maximize the number of leading digits equal to $d$, then select the largest 50-digit prime with that prefix. It explicitly acknowledges that the solution requires actual computation of 50-digit primes, because theoretical arguments alone cannot determine the maximal prefix length or the lexicographically largest prime.

The explanation clarifies why the previous solution’s divisibility heuristics are invalid: leading digits impose almost no direct restrictions on primality. The proposed approach-lexicographic search combined with rigorous primality testing-is appropriate and fully addresses the requirements of the exercise.

However, the solution **does not provide the explicit values of $P_0, \dots, P_9$**. While the methodology is correct, the exercise explicitly asks for the computed numbers. Without these numbers, the solution is incomplete, as it does not produce the requested objects.

## Gaps and Errors

**Critical error:** The solution does not include the explicit 50-digit primes $P_d$, which is the main deliverable of the exercise.

**Justification gap:** None in the reasoning; the theoretical justification that a computational approach is required is correct and clearly explained.

## Summary

The solution correctly diagnoses the nature of the problem and prescribes the appropriate computational method, but it stops short of producing the explicit extremal primes $P_0, \dots, P_9$, leaving the exercise incomplete.

VERDICT: FAIL - the solution correctly explains the method but does not provide the required 50-digit primes.
