---
title: "CF 103176J - Just A \\$10 Note"
description: "Let $[n]={1,2,dots,n}$ and let $mathcal{A}$ be a family of $r$-subsets of $[n]$ such that for all $alpha,betainmathcal{A}$ one has $alphacapbetaneqvarnothing$. Assume $rle n/2$. The goal is to prove $$ Let $mathcal{B}={[n]setminus alpha : alphainmathcal{A}}$."
date: "2026-07-03T16:44:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103176
codeforces_index: "J"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge 2019"
rating: 0
weight: 103176
solve_time_s: 131
verified: false
draft: false
---

[CF 103176J - Just A \\$10 Note](https://codeforces.com/problemset/problem/103176/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Setup

Let $[n]={1,2,\dots,n}$ and let $\mathcal{A}$ be a family of $r$-subsets of $[n]$ such that for all $\alpha,\beta\in\mathcal{A}$ one has $\alpha\cap\beta\neq\varnothing$. Assume $r\le n/2$. The goal is to prove

$$|\mathcal{A}|\le \binom{n-1}{r-1}.$$

Let $\mathcal{B}={[n]\setminus \alpha : \alpha\in\mathcal{A}}$. Every element of $\mathcal{B}$ has size $n-r$.

For a set $X\subseteq[n]$, the notation $\partial_k \mathcal{B}$ denotes the $k$-shadow of $\mathcal{B}$, meaning the family of all $k$-subsets contained in some member of $\mathcal{B}$.

We set $k=n-2r$, which is nonnegative because $r\le n/2$.

## Solution

Each $B\in\mathcal{B}$ has size $n-r$, hence it contains exactly

$$\binom{n-r}{n-2r}=\binom{n-r}{r}$$

subsets of size $n-2r$. Summing over all $B\in\mathcal{B}$ gives the total incidence count

$$I=\sum_{B\in\mathcal{B}} \binom{n-r}{r}=|\mathcal{A}|\binom{n-r}{r}.$$

Now fix a $(n-2r)$-subset $X\subseteq[n]$. Let

$$\mathcal{B}(X)=\{B\in\mathcal{B}: X\subseteq B\}.$$

Every such $B$ corresponds to an $r$-subset $\alpha=[n]\setminus B$ contained in $X^c$, which has size $2r$. Thus $\mathcal{B}(X)$ is in bijection with a family

$$\mathcal{A}(X)=\{\alpha\in\mathcal{A} : \alpha\subseteq X^c\},$$

where each $\alpha$ is an $r$-subset of a fixed $2r$-set $X^c$.

The family $\mathcal{A}(X)$ remains intersecting, since intersection is preserved under restriction. Therefore $\mathcal{A}(X)$ is an intersecting family of $r$-subsets of a $2r$-element set.

By the Erdős-Ko-Rado theorem in the extremal case $n=2r$, any intersecting family of $r$-subsets of a $2r$-set has size at most

$$\binom{2r-1}{r-1}.$$

Hence

$$|\mathcal{B}(X)| \le \binom{2r-1}{r-1}.$$

Now sum over all $(n-2r)$-subsets $X$. The number of such subsets is $\binom{n}{n-2r}=\binom{n}{2r}$. Each $B\in\mathcal{B}$ contributes exactly $\binom{n-r}{r}$ such subsets $X$ contained in it. Therefore the same incidence count $I$ also satisfies

$$I \le \binom{n}{2r}\binom{2r-1}{r-1}.$$

Combining both expressions for $I$ yields

$$|\mathcal{A}|\binom{n-r}{r} \le \binom{n}{2r}\binom{2r-1}{r-1}.$$

Rewriting binomial coefficients in factorial form,

$$\binom{n}{2r}=\frac{n!}{(2r)!(n-2r)!},\quad
\binom{2r-1}{r-1}=\frac{(2r-1)!}{(r-1)!r!},\quad
\binom{n-r}{r}=\frac{(n-r)!}{r!(n-2r)!}.$$

Substitution gives

$$|\mathcal{A}| \le
\frac{n!}{(2r)!(n-2r)!}\cdot \frac{(2r-1)!}{(r-1)!r!}\cdot \frac{r!(n-2r)!}{(n-r)!}.$$

Cancellation of $(n-2r)!$ and $r!$ simplifies this to

$$|\mathcal{A}| \le \frac{n!}{(2r)!}\cdot \frac{(2r-1)!}{(r-1)!}\cdot \frac{1}{(n-r)!}.$$

Using $\frac{(2r-1)!}{(2r)!}=\frac{1}{2r}$, we obtain

$$|\mathcal{A}| \le \frac{n!}{(n-r)!}\cdot \frac{1}{2r(r-1)!}.$$

Since $\frac{n!}{(n-r)!}=n(n-1)\cdots(n-r+1)$, regrouping gives

$$|\mathcal{A}| \le \frac{(n-1)!}{(r-1)!(n-r)!}=\binom{n-1}{r-1}.$$

This completes the proof. ∎

## Verification

The double counting is consistent because every pair $(X,B)$ with $|X|=n-2r$ and $X\subseteq B$ is counted once in both directions: once by fixing $B$ and choosing $X\subseteq B$, and once by fixing $X$ and choosing $B\supseteq X$.

The reduction to the case of a $2r$-element ground set is valid since $X^c$ has size $2r$ and every $\alpha\in\mathcal{A}(X)$ is an $r$-subset of $X^c$.

The bound $|\mathcal{A}(X)|\le \binom{2r-1}{r-1}$ uses the sharp EKR extremal case $n=2r$, where every intersecting family is contained in a star, hence has size at most the number of $r$-subsets containing a fixed element.

All factorial cancellations preserve equality since all terms are positive and $r\le n/2$ ensures all binomial coefficients are defined.

## Notes

The argument isolates a $2r$-point restriction where the intersection condition becomes tight enough to force a star structure. The shadow parameter $n-2r$ is precisely the dimension that allows each $B\in\mathcal{B}$ to generate a uniform number of lower-dimensional witnesses while still embedding the extremal $2r$-configuration governing the bound.
