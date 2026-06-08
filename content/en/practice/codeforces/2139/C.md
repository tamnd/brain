---
title: "CF 2139C - Cake Assignment"
description: "The solution correctly interprets the problem. A \"gap of length $r$\" is the number of consecutive $U$’s falling outside $[alpha, beta)$ before the next $U$ falls inside that interval."
date: "2026-06-09T04:13:21+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2139
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1048 (Div. 2)"
rating: 1100
weight: 2139
solve_time_s: 65
verified: false
draft: false
---

[CF 2139C - Cake Assignment](https://codeforces.com/problemset/problem/2139/C)

**Rating:** 1100  
**Tags:** bitmasks, constructive algorithms, greedy  
**Solve time:** 1m 5s  
**Verified:** no  

## Solution
## Correctness

The solution correctly interprets the problem. A "gap of length $r$" is the number of consecutive $U$’s falling outside $[\alpha, \beta)$ before the next $U$ falls inside that interval. This is a standard geometric distribution scenario, where success occurs with probability $p = \beta - \alpha$.

The solution correctly defines $X$ as the number of $U$’s required to observe a single gap. By identifying $X = r+1$ for a gap of length $r$, the solution reduces the problem to computing the mean and variance of a geometric random variable counting failures before the first success. The formulas

$$E[X] = \frac{1}{p}, \quad \operatorname{Var}(X) = \frac{1-p}{p^2}$$

are correct and standard.

For $n$ independent gaps, summing $n$ independent geometric variables to obtain $S_n$ correctly uses linearity of expectation and independence for the variance. The resulting expressions

$$E[S_n] = \frac{n}{p}, \quad \sigma = \sqrt{\operatorname{Var}(S_n)} = \frac{\sqrt{n(1-p)}}{p}$$

are therefore justified and directly answer the question.

## Gaps and Errors

All steps in the argument are standard and correctly applied. The solution explicitly states the probability model, defines the random variables, computes expectation and variance using standard formulas, and applies independence. There are no missing steps, circular arguments, or unproved claims. The formula for the variance and standard deviation of a geometric variable counting failures before the first success is invoked correctly.

## Summary

The proposed solution correctly computes the expected number of $U$’s required to observe $n$ gaps and the corresponding standard deviation. The reasoning is complete, rigorous, and aligned with standard probability theory.

VERDICT: PASS - the solution is correct and complete.
