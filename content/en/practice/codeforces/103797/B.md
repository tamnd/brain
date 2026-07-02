---
title: "CF 103797B - Bus Bet"
description: "Let $$G(z)=sum{xin{0,1}^n} f(x),z^{x1+cdots+xn}.$$ Then $$G(-1)=sum{x} f(x),(-1)^{ where $ Write $f$ in its unique multilinear expansion over $mathbb{R}$, $$f(x)=sum{Ssubseteq [n]} aS prod{iin S} xi,$$ so that $a{[n]}$ is the coefficient of the full monomial $x1x2cdots xn$."
date: "2026-07-02T08:47:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103797
codeforces_index: "B"
codeforces_contest_name: "IME++ Starters Try-outs 2022"
rating: 0
weight: 103797
solve_time_s: 52
verified: false
draft: false
---

[CF 103797B - Bus Bet](https://codeforces.com/problemset/problem/103797/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** no  

## Solution
## Solution

Let

$$G(z)=\sum_{x\in\{0,1\}^n} f(x)\,z^{x_1+\cdots+x_n}.$$

Then

$$G(-1)=\sum_{x} f(x)\,(-1)^{|x|},$$

where $|x|=x_1+\cdots+x_n$.

Write $f$ in its unique multilinear expansion over $\mathbb{R}$,

$$f(x)=\sum_{S\subseteq [n]} a_S \prod_{i\in S} x_i,$$

so that $a_{[n]}$ is the coefficient of the full monomial $x_1x_2\cdots x_n$.

Substituting this expansion into $G(-1)$ and exchanging summations gives

$$G(-1)=\sum_{S\subseteq[n]} a_S \sum_{x\in\{0,1\}^n} \left(\prod_{i\in S} x_i\right)(-1)^{|x|}.$$

The inner sum vanishes unless $S=[n]$. Indeed, if $j\notin S$, then for every assignment of the other variables, the two assignments obtained by flipping $x_j$ contribute equal magnitude and opposite sign because $(-1)^{|x|}$ changes sign while the factor $\prod_{i\in S} x_i$ is unchanged. This produces complete cancellation. Therefore only $S=[n]$ survives, giving

$$G(-1)=a_{[n]}\sum_{x\in\{0,1\}^n} x_1x_2\cdots x_n(-1)^{|x|}.$$

Only the single assignment $x=(1,1,\dots,1)$ contributes, so

$$G(-1)=a_{[n]}(-1)^n.$$

Hence $G(-1)\neq 0$ implies $a_{[n]}\neq 0$, so the multilinear polynomial for $f$ has degree $n$.

Every FBDD is in particular a decision tree, and the standard polynomial method for decision trees implies that any deterministic decision structure computing $f$ must have depth at least the degree of the representing multilinear polynomial. Therefore every FBDD for $f$ must contain a root-to-leaf path that queries all $n$ variables.

This is exactly the definition of evasiveness.

This completes the proof. ∎
