---
title: "CF 103428C - Assign or Multiply"
description: "Let $q$ be a primitive $m$th root of unity. For each $i$ with $1 le i le t$, write $$ni = m ai + bi, qquad 0 le bi < m,$$ and set $$N = n1 + cdots + nt, qquad A = a1 + cdots + at, qquad B = b1 + cdots + bt,$$ so that $N = mA + B$."
date: "2026-07-03T09:41:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103428
codeforces_index: "C"
codeforces_contest_name: "The 2021 CCPC Weihai Onsite"
rating: 0
weight: 103428
solve_time_s: 62
verified: false
draft: false
---

[CF 103428C - Assign or Multiply](https://codeforces.com/problemset/problem/103428/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Solution

Let $q$ be a primitive $m$th root of unity. For each $i$ with $1 \le i \le t$, write

$$n_i = m a_i + b_i, \qquad 0 \le b_i < m,$$

and set

$$N = n_1 + \cdots + n_t, \qquad A = a_1 + \cdots + a_t, \qquad B = b_1 + \cdots + b_t,$$

so that $N = mA + B$.

The $q$-multinomial coefficient is defined by

$$\binom{N}{n_1,\ldots,n_t}_q = \frac{[N]!_q}{[n_1]!_q \cdots [n_t]!_q}.$$

From Exercise 49, for every pair $(n,k)$ one has the factorization

$$\binom{n}{k}_q = \binom{\lfloor n/m \rfloor}{\lfloor k/m \rfloor}\binom{n \bmod m}{k \bmod m}_q.$$

The multinomial coefficient admits the telescoping decomposition

$$\binom{N}{n_1,\ldots,n_t}_q
=
\binom{N}{n_1}_q
\binom{N-n_1}{n_2}_q
\cdots
\binom{n_t}{n_t}_q,$$

since successive cancellations of $q$-factorials yield

$$\frac{[N]!_q}{[n_1]!_q \cdots [n_t]!_q}
=
\frac{[N]!_q}{[n_1]!_q [N-n_1]!_q}
\cdot
\frac{[N-n_1]!_q}{[n_2]!_q [N-n_1-n_2]!_q}
\cdots
\frac{[n_t]!_q}{[n_t]!_q}.$$

For each factor, apply the binomial result from Exercise 49. For the first factor,

$$\binom{N}{n_1}_q
=
\binom{A}{a_1}
\binom{B}{b_1}_q,$$

since $N = mA + B$ and $n_1 = ma_1 + b_1$.

After removing $n_1$, the remaining parameters are

$$N^{(1)} = N - n_1 = m(A-a_1) + (B-b_1),$$

and iterating the same decomposition gives, for each $j$,

$$\binom{N - (n_1+\cdots+n_{j-1})}{n_j}_q
=
\binom{A - (a_1+\cdots+a_{j-1})}{a_j}
\binom{B - (b_1+\cdots+b_{j-1})}{b_j}_q.$$

Multiplying these identities for $j = 1,\ldots,t$ yields cancellation in both the integer multinomial part and the $q$-multinomial part. The integer factors telescope to

$$\binom{A}{a_1}\binom{A-a_1}{a_2}\cdots\binom{a_t}{a_t}
=
\binom{A}{a_1,\ldots,a_t},$$

while the $q$-factors telescope to

$$\binom{B}{b_1}_q\binom{B-b_1}{b_2}_q\cdots\binom{b_t}{b_t}_q
=
\binom{B}{b_1,\ldots,b_t}_q.$$

Combining both parts gives

$$\binom{N}{n_1,\ldots,n_t}_q
=
\binom{A}{a_1,\ldots,a_t}
\binom{B}{b_1,\ldots,b_t}_q.$$

Substituting back $A = \sum_{i=1}^t \lfloor n_i/m \rfloor$ and $B = \sum_{i=1}^t (n_i \bmod m)$ yields the stated extension:

$$\boxed{
\binom{n_1+\cdots+n_t}{n_1,\ldots,n_t}_q
=
\binom{\sum_{i=1}^t \lfloor n_i/m \rfloor}{\lfloor n_1/m \rfloor,\ldots,\lfloor n_t/m \rfloor}
\binom{\sum_{i=1}^t (n_i \bmod m)}{n_1 \bmod m,\ldots,n_t \bmod m}_q
}.$$

This completes the proof. ∎
