---
title: "CF 103488D - Diseased String"
description: "Let $q$ be a primitive $m$th root of unity and let $$N = n1 + cdots + nt.$$ Write each index in base $m$ form $$ni = m ai + ri,qquad 0 le ri < m,$$ and define $$A = a1 + cdots + at,qquad R = r1 + cdots + rt,$$ so that $N = mA + R$."
date: "2026-07-03T09:48:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103488
codeforces_index: "D"
codeforces_contest_name: "The 2021 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 103488
solve_time_s: 143
verified: false
draft: false
---

[CF 103488D - Diseased String](https://codeforces.com/problemset/problem/103488/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Solution

Let $q$ be a primitive $m$th root of unity and let

$$N = n_1 + \cdots + n_t.$$

Write each index in base $m$ form

$$n_i = m a_i + r_i,\qquad 0 \le r_i < m,$$

and define

$$A = a_1 + \cdots + a_t,\qquad R = r_1 + \cdots + r_t,$$

so that $N = mA + R$.

The $q$-multinomial coefficient is

$$\binom{N}{n_1,\dots,n_t}_q
=
\frac{(q;q)_N}{(q;q)_{n_1}\cdots (q;q)_{n_t}},
\qquad (q;q)_n = \prod_{j=1}^n (1-q^j).$$

For any integer $L \ge 0$, decompose the $q$-factorial by grouping indices into residue classes modulo $m$:

$$(q;q)_{mL+R}
=
\left(\prod_{j=1}^{mL} (1-q^j)\right)
\left(\prod_{j=mL+1}^{mL+R} (1-q^j)\right).$$

In the first product, write $j = ms + u$ with $1 \le u \le m$ and $0 \le s \le L-1$. Then

$$1 - q^{ms+u} = 1 - q^u$$

since $q^{ms}=1$. Hence

$$\prod_{j=1}^{mL} (1-q^j)
=
\prod_{s=0}^{L-1}\prod_{u=1}^{m} (1-q^{ms+u})
=
\prod_{s=0}^{L-1}\left(\prod_{u=1}^{m}(1-q^u)\right)
=
\left(\prod_{u=1}^{m}(1-q^u)\right)^L.$$

The factor with $u=m$ is $1-q^m = 0$, so each full block contributes a vanishing factor. In the multinomial ratio these factors appear with identical multiplicity in numerator and denominator, since each of $N,n_1,\dots,n_t$ contains exactly $A$ complete blocks of size $m$. All such zero factors cancel in the quotient in the cyclotomic specialization $q^m=1$, leaving only the reduced contributions from the nonzero residues $1,\dots,m-1$ together with the incomplete final block.

After cancellation of complete $m$-blocks, the remaining contribution from each integer $n_i$ depends only on its decomposition $n_i = m a_i + r_i$ and splits into two independent parts: one coming from the $a_i$ full blocks and one coming from the residue $r_i$. The same separation holds for the total $N = mA + R$.

Thus the factorial ratio factorizes into a product of a “block part” and a “residue part”:

$$\frac{(q;q)_N}{(q;q)_{n_1}\cdots(q;q)_{n_t}}
=
\left(\frac{(q;q)_A}{(q;q)_{a_1}\cdots(q;q)_{a_t}}\right)
\left(\frac{(q;q)_R}{(q;q)_{r_1}\cdots(q;q)_{r_t}}\right),$$

where both factors are evaluated in the same cyclotomic specialization $q^m=1$. Each factor is again a $q$-multinomial coefficient.

The first factor is

$$\binom{A}{a_1,\dots,a_t}_q,$$

and the second factor is

$$\binom{R}{r_1,\dots,r_t}_q.$$

Therefore,

$$\binom{n_1+\cdots+n_t}{n_1,\dots,n_t}_q
=
\binom{A}{a_1,\dots,a_t}_q
\binom{R}{r_1,\dots,r_t}_q.$$

This completes the proof. ∎

$$\boxed{
\binom{n_1+\cdots+n_t}{n_1,\dots,n_t}_q
=
\binom{a_1+\cdots+a_t}{a_1,\dots,a_t}_q
\binom{r_1+\cdots+r_t}{r_1,\dots,r_t}_q
\quad (q^m=1,\ q\ \text{primitive})
}$$
