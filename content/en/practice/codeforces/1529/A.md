---
title: "CF 1529A - Eshag Loves Big Arrays"
description: "Let $U(x)$ and $V(x)$ be polynomials of degree $r$ with integer coefficients, and let $W(x) = U(x)V(x),$ so $W(x)$ has degree at most $2r$. Write $U(x) = sum{i=0}^{r} Ui x^i, qquad V(x) = sum{i=0}^{r} Vi x^i, qquad W(x) = sum{k=0}^{2r} Wk x^k."
date: "2026-06-10T16:59:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1529
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 722 (Div. 2)"
rating: 800
weight: 1529
solve_time_s: 151
verified: false
draft: false
---

[CF 1529A - Eshag Loves Big Arrays](https://codeforces.com/problemset/problem/1529/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 2m 31s  
**Verified:** no  

## Solution
## Solution

Let $U(x)$ and $V(x)$ be polynomials of degree $r$ with integer coefficients, and let

$W(x) = U(x)V(x),$

so $W(x)$ has degree at most $2r$.

Write

$U(x) = \sum_{i=0}^{r} U_i x^i, \qquad V(x) = \sum_{i=0}^{r} V_i x^i, \qquad W(x) = \sum_{k=0}^{2r} W_k x^k.$

Fix $2r+1$ distinct integers $x_0, x_1, \ldots, x_{2r}$. Define

$P_j = U(x_j), \qquad Q_j = V(x_j), \qquad R_j = W(x_j) = P_jQ_j.$

Since $W(x)$ has degree at most $2r$, the mapping

$W(x) \mapsto (W(x_0), W(x_1), \ldots, W(x_{2r}))$

is injective. Indeed, if a polynomial of degree at most $2r$ vanishes at $2r+1$ distinct points, then it is identically zero.

Hence the values $R_0, \ldots, R_{2r}$ determine the coefficients $W_0, \ldots, W_{2r}$ uniquely.

Define the $(2r+1)\times(2r+1)$ Vandermonde matrix $A$ by

$A_{j,k} = x_j^k, \qquad 0 \le j,k \le 2r.$

Then the evaluation identity for $W(x)$ is

$R = AW,$

where

$R = (W(x_0), \ldots, W(x_{2r}))^T, \qquad W = (W_0, \ldots, W_{2r})^T.$

Distinctness of the $x_j$ implies that $A$ is invertible, since its determinant equals

$\prod_{0 \le i < j \le 2r} (x_j - x_i) \ne 0.$

Thus

$W = A^{-1}R.$

Let $\lambda_{k,j}$ denote the entries of $A^{-1}$. Then for each $k$,

W_k = \sum_{j=0}^{2r} \lambda_{k,j} W(x_j). \tag{25}

Each coefficient $W_k$ is therefore a fixed linear combination of the values $W(x_j)$, where the constants $\lambda_{k,j}$ depend only on the chosen interpolation points $x_0, \ldots, x_{2r}$ and not on $U$ or $V$.

Since $W(x_j) = U(x_j)V(x_j)$ and each $U(x_j), V(x_j)$ is obtained by evaluating a degree-$r$ polynomial at a fixed integer argument, each such evaluation consists of finitely many additions and multiplications by fixed integers determined by $x_j$. Each $W(x_j)$ is then one multiplication of two integers of bounded size relative to the input size parameter $n$ in the recursive multiplication model of Section 4.3.3.

The reconstruction formula (25) applies a fixed $(2r+1)\times(2r+1)$ linear transformation to the vector $(W(x_0), \ldots, W(x_{2r}))$. Since the coefficients $\lambda_{k,j}$ are fixed integers independent of $n$, this transformation consists only of additions and multiplications by constants.

This establishes that each coefficient $W_k$ is obtained from the values $W(x_0), \ldots, W(x_{2r})$ by the linear relation (25).

This completes the proof. ∎
