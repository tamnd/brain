---
title: "CF 1392H - ZS Shuffles Cards"
description: "Algorithm B is the binary gcd algorithm. A subtract-and-shift cycle consists of one subtraction, followed by the removal of all powers of $2$ from the resulting difference."
date: "2026-06-11T10:13:26+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1392
codeforces_index: "H"
codeforces_contest_name: "Codeforces Global Round 10"
rating: 3000
weight: 1392
solve_time_s: 152
verified: false
draft: false
---

[CF 1392H - ZS Shuffles Cards](https://codeforces.com/problemset/problem/1392/H)

**Rating:** 3000  
**Tags:** combinatorics, dp, math, probabilities  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Solution

Algorithm B is the binary gcd algorithm. A subtract-and-shift cycle consists of one subtraction, followed by the removal of all powers of $2$ from the resulting difference. Exercise 35 asks for the longest path in the corresponding graph; Exercise 36 asks for a construction that attains $m+1$ subtraction steps.

Take

$$u=2^m,\qquad v=2^n,$$

with $m\ge n\ge1$.

Then

$$\lfloor\lg u\rfloor=m,\qquad
\lfloor\lg v\rfloor=n,$$

so the required logarithmic conditions hold.

Let us trace Algorithm B. Since both numbers are powers of $2$, the common factor $2^n$ is removed immediately by the initialization phase of Algorithm B. The working pair becomes

$$(U,V)=(2^{m-n},1).$$

Now consider a subtract-and-shift cycle when the current pair is

$$(2^k,1),\qquad k\ge1.$$

The subtraction step gives

$$2^k-1.$$

Since $2^k-1$ is odd, no shift occurs. Hence the next state is

$$(2^k-1,1).$$

The following subtraction gives

$$(2^k-1)-1=2^k-2
   =2(2^{k-1}-1).$$

Algorithm B now removes exactly one factor of $2$, producing

$$(2^{k-1}-1,1).$$

Repeating the same reasoning yields

$$(2^{k-1}-1,1)
\to
(2^{k-2}-1,1)
\to\cdots\to
(1,1).$$

It is more convenient to count the subtraction steps directly. Starting from $(2^k,1)$, the larger entry decreases by $1$ at every subtraction until equality is reached:

$$(2^k,1)\to(2^k-1,1)\to(2^k-2,1)\to\cdots\to(1,1).$$

This requires exactly

$$2^k-1$$

subtractions. For the present exercise we need exactly $m+1$ subtraction steps, not $2^k-1$. Hence powers of two alone are not the desired construction.

Instead choose

$$u=2^m,\qquad
v=2^m-(m+1).$$

The logarithmic condition for $u$ is immediate. Since

$$2^{m-1}\le 2^m-(m+1)<2^m
\qquad(m\ge3),$$

we have

$$\lfloor\lg v\rfloor=m-1.$$

This only covers the case $n=m-1$, so a more flexible construction is needed.

Let

$$u=2^m,\qquad
v=2^n(2^{m-n}-(m+1)).$$

Then

$$\lfloor\lg u\rfloor=m,
\qquad
\lfloor\lg v\rfloor=n,$$

provided $2^{m-n}>m+1$.

After the common factor $2^n$ is removed, Algorithm B starts with

$$(U,V)=\bigl(2^{m-n},\,2^{m-n}-(m+1)\bigr).$$

Their difference is exactly

$$m+1.$$

Since the second component exceeds half of the first, each subtract-and-shift cycle reduces the larger entry by exactly one unit of this difference, and the sequence runs through

$$(2^{m-n},\,2^{m-n}-(m+1)),$$

$$(2^{m-n}-(m+1),\,m+1),$$

and then through the chain

$$(m+1,m),\,
(m,m-1),\,
\ldots,\,
(2,1),\,
(1,1).$$

The number of subtraction steps is

$$1+m=m+1.$$

Thus Algorithm B performs exactly $m+1$ subtraction steps.

Therefore a valid family is

$$\boxed{
u=2^m,\qquad
v=2^n\!\left(2^{m-n}-(m+1)\right)
}$$

whenever $2^{m-n}>m+1$. This construction satisfies

$$\lfloor\lg u\rfloor=m,\qquad
\lfloor\lg v\rfloor=n,$$

and Algorithm B requires exactly $m+1$ subtraction steps. ∎
