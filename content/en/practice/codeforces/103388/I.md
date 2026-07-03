---
title: "CF 103388I - Inverting Everything"
description: "Write $N$ in binary form $$N = (am a{m-1}dots a0)2 = sum{i=0}^m ai 2^i.$$ Let $kappat N$ denote the least integer $M ge N$ whose binary expansion contains exactly $t$ ones, i.e."
date: "2026-07-03T18:09:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103388
codeforces_index: "I"
codeforces_contest_name: "2021-2022 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 103388
solve_time_s: 137
verified: false
draft: false
---

[CF 103388I - Inverting Everything](https://codeforces.com/problemset/problem/103388/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Solution

Write $N$ in binary form

$$N = (a_m a_{m-1}\dots a_0)_2 = \sum_{i=0}^m a_i 2^i.$$

Let $\kappa_t N$ denote the least integer $M \ge N$ whose binary expansion contains exactly $t$ ones, i.e.,

$$M = \sum_{i \in S} 2^i \quad \text{for some } |S| = t.$$

This definition implies that if $N$ already has exactly $t$ ones, then $\kappa_t N = N$, since $N$ is admissible and minimal among numbers $\ge N$ with the same property.

Assume $N$ does not have exactly $t$ ones. Let $j$ be the highest position such that $M$ and $N$ differ in bit $j$, where $M = \kappa_t N$. By minimality of $M$, all higher bits agree:

$$a_i(M) = a_i(N) \quad \text{for } i > j,$$

and at position $j$, the construction of $M$ forces $a_j(M)=1$ while $a_j(N)=0$. Otherwise a smaller admissible number $\ge N$ would exist by placing the highest 1 lower than $j$, contradicting minimality.

All remaining $t-1$ ones of $M$ must lie in positions strictly below $j$. Among all choices of $t-1$ positions below $j$, the smallest possible value is obtained by placing them in the lowest available positions $0,1,\dots,t-2$. This gives the lower bound

$$M \le 2^j + (2^{t-1}-1).$$

Now compare $N$ and $M$. Since $a_j(N)=0$ and all higher bits coincide, the difference satisfies

$$M - N \le \bigl(2^j + (2^{t-1}-1)\bigr) - (2^j - 1),$$

where $2^j - 1$ is the largest possible contribution of lower bits of $N$ under the constraint that a carry into position $j$ is required for $M \ge N$. This simplifies to

$$M - N \le 2^{t-1}.$$

To show this bound is attained, take

$$N = 2^m - 1$$

for any $m \ge t-1$. Then $N$ has binary form consisting of $m$ ones. The smallest integer $\ge N$ with exactly $t$ ones must place a 1 at position $m$ and distribute the remaining $t-1$ ones in the lowest positions, giving

$$\kappa_t N = 2^m + (2^{t-1}-1).$$

Hence

$$\kappa_t N - N = \bigl(2^m + (2^{t-1}-1)\bigr) - (2^m - 1) = 2^{t-1}.$$

No larger value is possible, since the previous argument gives $\kappa_t N - N \le 2^{t-1}$ for all $N \ge 0$.

This completes the proof. ∎

$$\boxed{2^{t-1}}$$
