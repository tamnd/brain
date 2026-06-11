---
title: "CF 1381B - Unmerge"
description: "The solution does not answer the exercise. Exercise 4.5.4.38 asks for the actual values of $Pd$ for each digit $0 le d le 9$."
date: "2026-06-11T10:53:15+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1381
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 658 (Div. 1)"
rating: 1800
weight: 1381
solve_time_s: 119
verified: false
draft: false
---

[CF 1381B - Unmerge](https://codeforces.com/problemset/problem/1381/B)

**Rating:** 1800  
**Tags:** dp  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Correctness

The solution does not answer the exercise.

Exercise 4.5.4.38 asks for the actual values of $P_d$ for each digit $0 \le d \le 9$. This is a computational optimization problem: for each $d$, one must determine the maximum possible number of leading digits equal to $d$, then among all 50-digit primes with that maximum prefix length, find the largest one.

The proposed solution never computes a single value $P_d$. Instead it describes a vague construction strategy and repeatedly says that the final digit should be "adjusted" or that primality should be checked by a computer program. The requested objects are not produced.

Several mathematical claims are also incorrect. For example, the statement that a prime cannot have two leading digits equal to an even digit is false. Primality depends on the last digit, not the first digits. A number beginning with $22$ can certainly be prime. Likewise, the claim that for $d \in \{1,3,7,9\}$ an additional leading $d$ would "force divisibility by 3" is unsupported and generally false.

Because the actual extremal primes are never found, neither the optimization problem nor the required proof of maximality is completed.

## Gaps and Errors

**Critical error:** The exercise asks for the numbers $P_d$, but no values of $P_d$ are given.

**Critical error:** The argument replaces the required computation by statements such as "choose the last digit to ensure primality" and "explicit numeric computation is feasible with a computer program." The exercise requires the actual extremal primes.

**Critical error:** The claim

> If $d$ is even, ... we need to choose $k=1$

is false. The first digits of a number do not determine divisibility by $2$. A prime may begin with arbitrarily many even digits provided its final digit is odd.

**Critical error:** The discussion of $d=0$ is inconsistent. The solution first declares $P_0$ undefined, then later proposes a construction for $d=0$. The exercise asks for $P_0$, so the relevant question is how many leading zeros a 50-digit number can have, namely none.

**Critical error:** The claim

> For $d \in \{1,3,7,9\}$, any additional leading $d$ beyond the constructed $k$ would force divisibility by 3

is neither proved nor true in general.

**Critical error:** No maximality proof is provided. The solution never determines the true maximum prefix length for any digit $d$.

**Justification gap:** The greedy rule "fill remaining digits with 9" is asserted without proving that a prime with the resulting prefix exists or that the lexicographically largest completion is prime.

**Justification gap:** The solution repeatedly refers to "adjusting the final digit" but never proves that such an adjustment preserves the claimed maximal number of leading digits or yields a prime.

## Summary

The submission does not solve the stated optimization problem. It neither computes the required primes nor establishes the true maximal number of leading digits for any $d$, and several of its divisibility arguments are incorrect.

VERDICT: FAIL - the solution never determines the required extremal primes $P_d$ and contains incorrect claims about how leading digits restrict primality.
