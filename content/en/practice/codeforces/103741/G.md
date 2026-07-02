---
title: "CF 103741G - Nerdle"
description: "Let $f(x1,dots,xn)$ be a Boolean function, and let $G(z)$ be its generating function in the sense of Exercise 25, so that $$G(z)=sum{xin{0,1}^n} f(x), z^{w(x)},$$ where $w(x)=x1+cdots+xn$ is the Hamming weight of $x$."
date: "2026-07-02T09:06:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103741
codeforces_index: "G"
codeforces_contest_name: "HUSTPC 2022"
rating: 0
weight: 103741
solve_time_s: 131
verified: false
draft: false
---

[CF 103741G - Nerdle](https://codeforces.com/problemset/problem/103741/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Solution

Let $f(x_1,\dots,x_n)$ be a Boolean function, and let $G(z)$ be its generating function in the sense of Exercise 25, so that

$$G(z)=\sum_{x\in\{0,1\}^n} f(x)\, z^{w(x)},$$

where $w(x)=x_1+\cdots+x_n$ is the Hamming weight of $x$. Thus $G(z)$ is the ordinary generating polynomial counting satisfying assignments of $f$ by weight.

Assume $G(-1)\neq 0$. Expanding,

$$G(-1)=\sum_{x\in\{0,1\}^n} f(x)\, (-1)^{w(x)}.$$

Split assignments by the first variable. Every $x\in{0,1}^n$ is uniquely written as $(0,y)$ or $(1,y)$ with $y\in{0,1}^{n-1}$. Then

$$G(-1)=\sum_{y} f(0,y)(-1)^{w(y)} + \sum_{y} f(1,y)(-1)^{1+w(y)}.$$

This becomes

$$G(-1)=\sum_{y} \bigl(f(0,y)-f(1,y)\bigr)(-1)^{w(y)}.$$

Since $f(0,y),f(1,y)\in{0,1}$, each coefficient $f(0,y)-f(1,y)$ lies in ${-1,0,1}$.

Now consider any FBDD for $f$. Along any root-to-sink path, each tested variable is fixed once, and no variable repeats on that path. Suppose a path queries fewer than $n$ variables. Then there exists at least one variable $x_i$ not tested on that path. Fix all tested variables according to the path, and vary $x_i$. This produces two full assignments that agree on all queried variables but differ in value of $x_i$.

In an FBDD, acceptance or rejection on that path is independent of unqueried variables, since the path never branches on $x_i$. Therefore the function value contributed by all completions of that path is constant with respect to $x_i$. Such a path contributes a subcube of dimension at least $1$ to the truth table, hence contributes a term in $G(z)$ whose evaluation at $z=-1$ cancels in pairs when flipping the free variable. More precisely, for any subcube where at least one variable is free, the contributions of assignments differing only on that variable cancel in the alternating sum defining $G(-1)$.

Thus any non-evasive FBDD, one in which every root-to-sink path has length at most $n-1$, decomposes the set of satisfying assignments into pairs differing on at least one free variable along each leaf subcube, forcing total cancellation in the alternating sum. This implies $G(-1)=0$.

Taking the contrapositive, if $G(-1)\neq 0$, no such cancellation can occur. Hence every root-to-sink path in every FBDD must query all $n$ variables, since otherwise the decomposition into subcubes induced by missing variables would force $G(-1)=0$.

Therefore every FBDD for $f$ contains a downward path of length $n$, so $f$ is evasive.

This completes the proof. ∎
