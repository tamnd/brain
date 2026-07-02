---
title: "CF 103824A - \u5361\u5c14\u7684\u793c\u7269"
description: "Let $f(x1,ldots,xn)$ be a Boolean function and let $$G(z)=sum{x1=0}^1 cdots sum{xn=0}^1 z^{x1+cdots+xn} f(x1,ldots,xn)$$ be its generating function as defined in the preceding exercise."
date: "2026-07-02T08:17:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103824
codeforces_index: "A"
codeforces_contest_name: "2022 Summer Camp of XTU Qualifying Round"
rating: 0
weight: 103824
solve_time_s: 42
verified: false
draft: false
---

[CF 103824A - \u5361\u5c14\u7684\u793c\u7269](https://codeforces.com/problemset/problem/103824/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** no  

## Solution
## Solution

Let $f(x_1,\ldots,x_n)$ be a Boolean function and let

$$G(z)=\sum_{x_1=0}^1 \cdots \sum_{x_n=0}^1 z^{x_1+\cdots+x_n} f(x_1,\ldots,x_n)$$

be its generating function as defined in the preceding exercise.

Let

$$F(p_1,\ldots,p_n)=\sum_{x_1=0}^1 \cdots \sum_{x_n=0}^1
\prod_{k=1}^n (1-p_k)^{1-x_k} p_k^{x_k}\, f(x_1,\ldots,x_n)$$

be the reliability polynomial.

Specialize to the case $p_1=\cdots=p_n=p$. Then every term in the product becomes

$(1-p)^{1-x_k}p^{x_k}$, so the weight of a vector $x=(x_1,\ldots,x_n)$ depends only on

$s=x_1+\cdots+x_n$. The product simplifies to

$$\prod_{k=1}^n (1-p)^{1-x_k}p^{x_k} = (1-p)^{n-s} p^s.$$

Define

$$A_s = \sum_{x_1=0}^1 \cdots \sum_{x_n=0}^1 [x_1+\cdots+x_n=s]\; f(x_1,\ldots,x_n),$$

so that $A_s$ counts (with weight $f$) all assignments having exactly $s$ ones.

Then the reliability polynomial becomes

$$F(p)=\sum_{s=0}^n A_s p^s (1-p)^{n-s}.$$

The generating function satisfies

$$G(z)=\sum_{s=0}^n A_s z^s,$$

since grouping terms by Hamming weight $s$ produces exactly the same coefficients $A_s$.

Now rewrite $F(p)$ by factoring $(1-p)^n$:

$$F(p)=(1-p)^n \sum_{s=0}^n A_s \left(\frac{p}{1-p}\right)^s.$$

The inner sum is $G!\left(\frac{p}{1-p}\right)$ by substitution into the generating function.

Therefore

$$F(p)=(1-p)^n G\!\left(\frac{p}{1-p}\right).$$

This expresses the reliability polynomial with equal parameters directly in terms of the generating function.

$$\boxed{F(p)=(1-p)^n\, G\!\left(\frac{p}{1-p}\right)}$$

This completes the solution. ∎
