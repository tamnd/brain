---
title: "CF 2136D - For the Champion"
description: "Let $p = beta - alpha$ be the probability that a single $Uj$ lies in the interval $[alpha, beta)$, as in equation (4). A gap of length $r$ occurs when $r$ consecutive $U$'s fall outside $[alpha, beta)$, followed by a $U$ inside the interval."
date: "2026-06-09T04:10:41+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "interactive", "math"]
categories: ["algorithms"]
codeforces_contest: 2136
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1046 (Div. 2)"
rating: 1700
weight: 2136
solve_time_s: 124
verified: false
draft: false
---

[CF 2136D - For the Champion](https://codeforces.com/problemset/problem/2136/D)

**Rating:** 1700  
**Tags:** constructive algorithms, interactive, math  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Solution

Let $p = \beta - \alpha$ be the probability that a single $U_j$ lies in the interval $[\alpha, \beta)$, as in equation (4). A _gap of length $r$_ occurs when $r$ consecutive $U$'s fall outside $[\alpha, \beta)$, followed by a $U$ inside the interval. For a random sequence, the probability that a gap has length $r$ is

$\Pr(\text{gap length } = r) = (1-p)^r p, \quad r \ge 0.$

Denote by $X$ the number of $U$'s required to observe one gap. If the gap length is $r$, then $X = r+1$, since the gap consists of $r$ failures followed by one success. Therefore, $X$ is a geometric random variable with success probability $p$.

The expected value of $X$ is

$$E[X] = \sum_{r=0}^{\infty} (r+1)(1-p)^r p = \sum_{r=0}^{\infty} (1-p)^r p + \sum_{r=0}^{\infty} r (1-p)^r p.$$

The first sum is

$$\sum_{r=0}^{\infty} (1-p)^r p = 1,$$

since it is the sum of the geometric series with total probability 1. The second sum is

$$\sum_{r=0}^{\infty} r (1-p)^r p = \frac{1-p}{p},$$

by the standard formula for the mean of a geometric distribution counting failures. Combining these gives

$$E[X] = 1 + \frac{1-p}{p} = \frac{1}{p}.$$

Thus, the expected number of $U$'s to observe a single gap is $1/p$.

Let $X_1, X_2, \ldots, X_n$ be independent copies of $X$, representing the number of $U$'s needed to observe each of the $n$ gaps. Then the total number of $U$'s required to observe $n$ gaps is

$$S_n = X_1 + X_2 + \cdots + X_n.$$

By linearity of expectation,

$$E[S_n] = n E[X] = \frac{n}{p}.$$

The variance of $X$ is

$$\operatorname{Var}(X) = \frac{1-p}{p^2},$$

again by the standard formula for a geometric variable counting failures before the first success. Since the $X_j$ are independent,

$$\operatorname{Var}(S_n) = n \operatorname{Var}(X) = \frac{n(1-p)}{p^2}.$$

The standard deviation is the square root of the variance:

$$\sigma = \sqrt{\operatorname{Var}(S_n)} = \frac{\sqrt{n(1-p)}}{p}.$$

This completes the proof.

∎

$$\boxed{\text{Expected number of $U$'s: } \frac{n}{p}, \quad \text{Standard deviation: } \frac{\sqrt{n(1-p)}}{p}}$$
