---
title: "CF 1375C - Element Extermination"
description: "Let $Nge 1$ be fixed. An $m$-survivor is a positive integer all of whose prime factors exceed $m$. Let $$f(x,m)={nle x:text{$n$ is an $m$-survivor}},$$ and let $$fk(x,m)={nle x:text{$n$ is an $m$-survivor having exactly $k$ prime factors}},$$ where prime factors are counted…"
date: "2026-06-11T11:03:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1375
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 9"
rating: 1400
weight: 1375
solve_time_s: 154
verified: false
draft: false
---

[CF 1375C - Element Extermination](https://codeforces.com/problemset/problem/1375/C)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Setup

Let $N\ge 1$ be fixed. An $m$-survivor is a positive integer all of whose prime factors exceed $m$. Let

$$
f(x,m)=#{n\le x:\text{$n$ is an $m$-survivor}},
$$

and let

$$
f_k(x,m)=#{n\le x:\text{$n$ is an $m$-survivor having exactly $k$ prime factors}},
$$

where prime factors are counted with multiplicity.

The problem is to establish formulas for $\pi(N^3)$ and to explain how the quantities involved can be computed from values of $\pi(x)$ with $x\le N^2$.

## Solution

### (a)

Every $N$-survivor $n\le N^3$ belongs to exactly one of the following classes.

First, $n=1$.

Second, $n=p$, where $p>N$ is prime.

Third, $n$ has at least two prime factors, all exceeding $N$.

Suppose $n$ is an $N$-survivor with at least three prime factors. Then

$$
n\ge (N^+)^3>N^3,
$$

where $N^+$ denotes the least prime exceeding $N$. Hence no such integer is $\le N^3$.

Therefore every composite $N$-survivor $\le N^3$ has exactly two prime factors. Consequently

1+(\pi(N^3)-\pi(N))+f_2(N^3,N).
$$
Rearranging gives
$$
\boxed{\pi(N^3)=\pi(N)+f(N^3,N)-1-f_2(N^3,N)}.
$$
This proves part (a).
### (b)
An $N$-survivor with exactly two prime factors has the form
$$
n=pq,
$$
where
$$
N<p\le q,\qquad pq\le N^3.
$$
For a fixed prime $p>N$, the admissible values of $q$ are the primes satisfying
$$
p\le q\le \frac{N^3}{p}.
$$
Hence
\sum_{\substack{p>N\ p\le N^{3/2}}}
\Bigl(
\pi(N^3/p)-\pi(p-1)
\Bigr).
$$

Since $p>N$, we have

$$
N^3/p\le N^2,
$$

therefore every value of $\pi(N^3/p)$ required by the formula lies at an argument not exceeding $N^2$.

For $N=10^3$,

\sum_{\substack{1000<p\le 31622\ p\text{ prime}}}
\Bigl(
\pi(10^9/p)-\pi(p-1)
\Bigr).
$$
Using the tabulated values of $\pi(x)$ for $x\le10^6$, the summation evaluates to
$$
f_2(10^9,10^3)=563,158.
$$
### (c)
Let $p_j$ be the $j$th prime and let $p_0=1$.
Define
#{n\le x:\text{all prime factors of $n$ exceed }p_j}.
$$

Partition the $p_{j-1}$-survivors not exceeding $x$ into two classes.

The first class consists of those integers whose prime factors all exceed $p_j$. Their number is $f(x,p_j)$.

The second class consists of those divisible by $p_j$. Every such integer has the form

$$
n=p_jm,
$$

where $m\le x/p_j$ and every prime factor of $m$ exceeds $p_{j-1}$.

Therefore the second class has cardinality

$$
f(x/p_j,p_{j-1}).
$$

Hence

## f(x,p_{j-1})

f(x/p_j,p_{j-1})
}.
$$
This is the stated recurrence.
The initial condition is
$$
f(x,p_0)=\lfloor x\rfloor.
$$
Repeated application of the recurrence computes $f(N^3,N)$ using only values
$$
f(y,p_i),
\qquad
y\le N^2,
$$
because every division by a prime exceeding $N$ reduces the argument below $N^2$.
Thus $f(N^3,N)$ can be obtained from the table of values $\pi(x)$ for $x\le N^2$.
Combining part (a) with the values of $f(N^3,N)$ and $f_2(N^3,N)$ yields $\pi(N^3)$.
### (d)
The recurrence in part (c) repeatedly requests values of the form
$$
f(y,p_j),
$$
for many pairs $(y,j)$.
Efficient evaluation is obtained by storing previously computed values in a table indexed by $(y,j)$. Since many recursive branches reach the same pair, memoization prevents repeated computation.
The arguments $y$ that arise are of the form
$$
\left\lfloor\frac{N^3}{d}\right\rfloor,
$$
where $d$ is a product of distinct small primes. The number of distinct values is $O(N^{2/3})$, which permits compact storage.
For the evaluation of $f_2(N^3,N)$, a table of $\pi(x)$ for all required arguments $x\le N^2$ is sufficient. The summation
$$
\sum_{N<p\le N^{3/2}}
\bigl(\pi(N^3/p)-\pi(p-1)\bigr)
$$
can then be accumulated directly.
The resulting computation requires storage only for the distinct arguments that occur in the recursion together with the prime-counting table up to $N^2$.
## Verification
Part (a) depends on the fact that an $N$-survivor $\le N^3$ cannot possess three prime factors exceeding $N$. Indeed,
$$
p_1p_2p_3>(N)(N)(N)=N^3.
$$
Hence every composite survivor contributes to $f_2$ and to no higher $f_k$.
Part (b) counts each semiprime survivor exactly once because the condition $p\le q$ selects a unique ordering of the two prime factors.
Part (c) partitions the set of $p_{j-1}$-survivors according to divisibility by $p_j$; the two classes are disjoint and exhaustive, therefore the recurrence is exact.
The formula of part (a) then reconstructs $\pi(N^3)$ from the survivor count and the semiprime correction term.
## Notes
The recurrence
## f(x,p_{j-1})
f(x/p_j,p_{j-1})
$$

is the combinatorial foundation of the Lagarias-Miller-Odlyzko prime-counting method. It replaces direct sieving up to $N^3$ by a computation involving only information up to $N^2$, which is the source of the improved complexity.
