---
title: "CF 103828E - Do you where is Naseem?"
description: "Let $G(z)=sum{x1=0}^{1}cdotssum{xn=0}^{1} z^{x1+cdots+xn} f(x1,ldots,xn)$ be the generating function defined in Exercise 25, and let $F(p)$ denote the reliability polynomial when $p1=cdots=pn=p$, so that $$F(p)=sum{x1=0}^{1}cdotssum{xn=0}^{1} (1-p)^{1-x1}p^{x1}cdots…"
date: "2026-07-02T08:14:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103828
codeforces_index: "E"
codeforces_contest_name: "(DCPC + TCPC + BCPC) 2022"
rating: 0
weight: 103828
solve_time_s: 95
verified: false
draft: false
---

[CF 103828E - Do you where is Naseem?](https://codeforces.com/problemset/problem/103828/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Solution

Let $G(z)=\sum_{x_1=0}^{1}\cdots\sum_{x_n=0}^{1} z^{x_1+\cdots+x_n} f(x_1,\ldots,x_n)$ be the generating function defined in Exercise 25, and let $F(p)$ denote the reliability polynomial when $p_1=\cdots=p_n=p$, so that

$$F(p)=\sum_{x_1=0}^{1}\cdots\sum_{x_n=0}^{1} (1-p)^{1-x_1}p^{x_1}\cdots (1-p)^{1-x_n}p^{x_n} f(x_1,\ldots,x_n).$$

For a fixed vector $x=(x_1,\ldots,x_n)$, the product factors according to the Hamming weight $w(x)=x_1+\cdots+x_n$, giving

$$(1-p)^{1-x_1}p^{x_1}\cdots (1-p)^{1-x_n}p^{x_n}=(1-p)^{n-w(x)}p^{w(x)}.$$

Substitution yields

$$F(p)=\sum_{x} f(x)\, (1-p)^{n-w(x)} p^{w(x)}.$$

Factoring out $(1-p)^n$ produces

$$F(p)=(1-p)^n \sum_{x} f(x)\left(\frac{p}{1-p}\right)^{w(x)}.$$

The remaining sum matches the definition of $G(z)$ evaluated at $z=\frac{p}{1-p}$, since $z^{w(x)}$ appears with the same exponent structure. Therefore,

$$F(p)=(1-p)^n G\!\left(\frac{p}{1-p}\right).$$

This expresses $F(p)$ as a simple rescaling of the generating function, obtained by a single substitution followed by multiplication by a monomial factor. This completes the solution. ∎
