---
title: "CF 1329A - Dreamoon Likes Coloring"
description: "The solution does not successfully establish what Exercise 4.6.3.13 asks. The positive part is that the displayed constructions are now genuine star chains."
date: "2026-06-11T16:20:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1329
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 631 (Div. 1) - Thanks, Denis aramis Shitov!"
rating: 1800
weight: 1329
solve_time_s: 174
verified: false
draft: false
---

[CF 1329A - Dreamoon Likes Coloring](https://codeforces.com/problemset/problem/1329/A)

**Rating:** 1800  
**Tags:** constructive algorithms, greedy, implementation, math  
**Solve time:** 2m 54s  
**Verified:** no  

## Solution
## Correctness

The solution does not successfully establish what Exercise 4.6.3.13 asks.

The positive part is that the displayed constructions are now genuine star chains. In each case the chain first builds

$$1,2,4,\ldots,2^m,$$

and then appends terms by adding previously occurring powers of two. Every displayed step is indeed of the form

$$a_r=a_{r-1}+a_j,$$

with $j<r$. This fixes the fundamental defect in the earlier attempt.

However, the exercise is specifically about the four cases of Theorem C and asks for star chains of length $A+2$. The proposed proof identifies $A$ incorrectly.

At the beginning it states:

> In each case $A$ is the number of powers of $2$ occurring in $n-1$.

That is not the parameter used in Theorem C. If $A$ were literally the number of nonzero binary digits of $n-1$, then in Case 1,

$$n-1=2^m$$

has one nonzero binary digit, so $A=1$, not $A=m-1$ as later claimed.

The proof subsequently uses formulas

$$A=m-1,\qquad
A=m,\qquad
A=m+1,\qquad
A=m+2,$$

for the four cases, but these values are asserted without deriving them from Theorem C. The entire verification that the chain lengths equal $A+2$ depends on those identities.

Since the solution never states the actual definition of $A$ from Theorem C, and never proves the relations between $A$ and $m,k,h,g$, the central claim that the constructed chains have length exactly $A+2$ is unsupported.

A reader who only has this solution cannot verify that the chain lengths match the quantity required by the theorem.

## Gaps and Errors

**Critical error.** The parameter $A$ is misidentified.

The solution explicitly says:

$$A=\text{number of powers of }2\text{ occurring in }n-1.$$

But later it claims, for example in Case 1,

$$A=m-1.$$

These statements are incompatible. For $n-1=2^m$, the number of powers of two occurring is $1$, not $m-1$.

**Critical error.** The proof that the constructed chains have length $A+2$ is missing.

The displayed chain lengths are computed as $m+1,m+2,m+3,m+4$, but the equalities

$$A=m-1,\quad
A=m,\quad
A=m+1,\quad
A=m+2$$

are simply asserted. They are not derived from Theorem C or any definition of $A$.

Since the exercise is specifically about obtaining length $A+2$, this missing justification affects the main conclusion.

**Justification gap.** The solution assumes knowledge of the four cases of Theorem C but does not explain how the stated values of $A$ arise from that theorem. If those values are correct in the theorem's notation, they must be cited or derived.

## Summary

The construction now gives valid star chains, but the argument does not correctly relate their lengths to the parameter $A$ appearing in Theorem C. The proof of the required length $A+2$ is therefore incomplete.

VERDICT: FAIL - the solution does not correctly justify the relation between the constructed chain lengths and the parameter $A$ from Theorem C.
