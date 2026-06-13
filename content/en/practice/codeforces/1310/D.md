---
title: "CF 1310D - Tourism"
description: "The proof of Ryser's identity is correct and complete. The argument expands $$prod{i=1}^n sum{j=1}^n epsilonj x{ij}$$ as a sum over all functions $f:[n]to[n]$, then evaluates the coefficient $$C(I)=(-1)^nsum{epsilonin{0,1}^n} (-1)^{ prod{jin I}epsilonj$$ where…"
date: "2026-06-11T17:23:37+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1310
codeforces_index: "D"
codeforces_contest_name: "VK Cup 2019-2020 - Elimination Round (Engine)"
rating: 2300
weight: 1310
solve_time_s: 177
verified: false
draft: false
---

[CF 1310D - Tourism](https://codeforces.com/problemset/problem/1310/D)

**Rating:** 2300  
**Tags:** dp, graphs, probabilities  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Correctness

The proof of Ryser's identity is correct and complete.

The argument expands

$$\prod_{i=1}^n \sum_{j=1}^n \epsilon_j x_{ij}$$

as a sum over all functions $f:[n]\to[n]$, then evaluates the coefficient

$$C(I)=(-1)^n\sum_{\epsilon\in\{0,1\}^n} (-1)^{|\epsilon|} \prod_{j\in I}\epsilon_j$$

where $I=\operatorname{Im}(f)$. The computation of $C(I)$ is correct: it vanishes unless $I=[n]$, and equals $1$ when $I=[n]$. Therefore only surjective maps contribute, and for a map $f:[n]\to[n]$ surjectivity is equivalent to bijectivity. Hence the surviving terms are exactly the permutation terms in the permanent. This establishes the identity.

The operation count, however, is not correct as stated.

The exercise asks for the number of addition and multiplication operations required to evaluate the permanent by the displayed formula. The proposed count attempts to evaluate the formula directly via subsets, but the addition count is derived incorrectly because it treats every subset $S$ as requiring $k-1$ additions for a row sum when $|S|=k$. For $k=0$, the row sum is $0$, which requires no additions, not $-1$ additions. Therefore the summation

$$\sum_{S\subseteq[n]}(|S|-1) = n2^{n-1}-2^n$$

does not represent the actual number of additions.

Consequently the final formula

$$A=2^{\,n-1}(n-2)^2-1$$

is not a valid operation count.

## Gaps and Errors

### Critical error

The addition count is incorrect.

The derivation assumes that for every subset $S$ of size $k$, each row sum requires $k-1$ additions. This formula fails for $k=0$. The empty subset contributes row sums equal to $0$, requiring $0$ additions, not $-1$. Therefore

$$\sum_{S\subseteq[n]}(|S|-1)$$

is not the correct total count of additions used in forming row sums.

Since the addition count is built from this incorrect expression, the final addition total is wrong.

### Justification gap

The multiplication count

$$M=(n-1)2^n$$

is correct for the direct subset evaluation described, but the solution does not explicitly discuss whether multiplication by the coefficient $(-1)^{|S|}$ is being counted as an arithmetic operation. The convention adopted is reasonable, but it should be stated explicitly when giving an exact operation count.

## Summary

The proof of Ryser's formula is correct. The operation-count portion contains a substantive counting error, so the solution does not correctly answer the second part of the exercise.

VERDICT: FAIL - the proof is correct, but the addition-operation count is incorrect because the empty subset is counted as requiring $-1$ additions per row.
