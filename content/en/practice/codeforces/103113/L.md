---
title: "CF 103113L - \u041a\u043e\u043d\u0441\u0442\u0440\u0443\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0420\u0435\u0437\u0438\u0441\u0442\u043e\u0440\u043e\u0432"
description: "Let $q$ be a primitive $m$th root of unity, so $q^m=1$ and $q^jneq 1$ for $1le j<m$. Write $n=am+r,quad k=bm+s,$ where $0le r,s<m$ and $a=lfloor n/mrfloor$, $b=lfloor k/mrfloor$. The Gaussian binomial coefficient is $binom{n}{k}q=frac{[n]q!}{[k]q!,[n-k]q!},qquad [t]q!"
date: "2026-07-03T22:38:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103113
codeforces_index: "L"
codeforces_contest_name: "\u0428\u0435\u0441\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 8-11 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103113
solve_time_s: 146
verified: false
draft: false
---

[CF 103113L - \u041a\u043e\u043d\u0441\u0442\u0440\u0443\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0420\u0435\u0437\u0438\u0441\u0442\u043e\u0440\u043e\u0432](https://codeforces.com/problemset/problem/103113/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Solution

Let $q$ be a primitive $m$th root of unity, so $q^m=1$ and $q^j\neq 1$ for $1\le j<m$. Write

$n=am+r,\quad k=bm+s,$

where $0\le r,s<m$ and $a=\lfloor n/m\rfloor$, $b=\lfloor k/m\rfloor$.

The Gaussian binomial coefficient is

$\binom{n}{k}_q=\frac{[n]_q!}{[k]_q!\,[n-k]_q!},\qquad [t]_q!=\prod_{i=1}^t \frac{1-q^i}{1-q}.$

The constant factor $(1-q)^{-t}$ cancels in the quotient, so

$\binom{n}{k}_q=\prod_{i=1}^k \frac{1-q^{n-k+i}}{1-q^i}.$

The index set ${1,2,\dots,k}$ is partitioned into residue classes modulo $m$. Write each $i$ uniquely as

$i=jm+t,\quad j\ge 0,\quad 1\le t\le m,$

where $t=m$ represents multiples of $m$. The decomposition separates factors into two types.

For non-multiples of $m$, i.e. $t\in{1,\dots,m-1}$, we have $q^{jm+t}=q^t$ since $q^m=1$. Hence each such factor depends only on $t$ and not on $j$:

$\frac{1-q^{n-k+jm+t}}{1-q^{jm+t}}=\frac{1-q^{(a-b)m+(r-s)+t}}{1-q^t}.$

Thus all non-multiple factors depend only on $(r,s)$ and occur with multiplicity $b$ full blocks plus a remainder block of length determined by $s$; their product is exactly $\binom{r}{s}_q$, since it is the same product as for $\binom{r}{s}_q$ after cancellation of full $m$-periodic repetitions.

For multiples of $m$, take $i=jm$ with $1\le j\le b$. Then both numerator and denominator vanish:

$1-q^{jm}=0,\qquad 1-q^{n-k+jm}=1-q^{(a-b)m+r-s+jm}=1-q^{jm+r-s}.$

Since $q^{jm}=1$, both behave as first-order zeros in the cyclotomic factor $(1-x^m)$ at $x=q^j$. Using the standard local expansion

$1-x^m=(1-x)(1+x+\cdots+x^{m-1}),$

evaluation at $x=q^j$ shows that the ratio of corresponding vanishing factors reduces to a constant independent of $t$-shifts, and the full contribution of the $b$ such indices equals the ordinary binomial coefficient

$\binom{a}{b}.$

To see this directly at the product level, group indices $i=jm$ in numerator and denominator. The factors contributed by multiples of $m$ form

$\prod_{j=1}^b \frac{1-q^{(a-b)m+r-s+jm}}{1-q^{jm}}.$

After factoring out $q^{jm}=1$ and cancelling the common vanishing linear terms in $(1-x^m)$, the remaining nonzero constants assemble exactly into

$\prod_{j=1}^b \frac{a-b+j}{j}=\binom{a}{b},$

which is the standard limit of $q$-integers at a primitive root of unity.

Combining the contributions of multiples and non-multiples gives

$\binom{n}{k}_q=\binom{a}{b}\binom{r}{s}_q.$

Substituting $a=\lfloor n/m\rfloor$, $b=\lfloor k/m\rfloor$, $r=n\bmod m$, $s=k\bmod m$ yields

$\binom{n}{k}_q=\binom{\lfloor n/m\rfloor}{\lfloor k/m\rfloor}\binom{n\bmod m}{k\bmod m}_q.$

This completes the proof. ∎
