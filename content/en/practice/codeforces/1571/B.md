---
title: "CF 1571B - Epic Novel"
description: "We must compute $$(cdots((x1otimes x2)otimes x3)otimescdotsotimes x{10^6}),$$ with $$xk=1.111111.$$ Let $$sk=(cdots((x1otimes x2)otimescdots)otimes xk).$$ Since every addition is rounded to eight significant decimal digits, the recurrence is $$sk=operatorname{fl}(s{k-1}+1."
date: "2026-06-10T11:21:46+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math"]
categories: ["algorithms"]
codeforces_contest: 1571
codeforces_index: "B"
codeforces_contest_name: "Kotlin Heroes: Episode 8"
rating: 1300
weight: 1571
solve_time_s: 178
verified: false
draft: false
---

[CF 1571B - Epic Novel](https://codeforces.com/problemset/problem/1571/B)

**Rating:** 1300  
**Tags:** *special, math  
**Solve time:** 2m 58s  
**Verified:** no  

## Solution
## (a)

We must compute

$$(\cdots((x_1\otimes x_2)\otimes x_3)\otimes\cdots\otimes x_{10^6}),$$

with

$$x_k=1.111111.$$

Let

$$s_k=(\cdots((x_1\otimes x_2)\otimes\cdots)\otimes x_k).$$

Since every addition is rounded to eight significant decimal digits, the recurrence is

$$s_k=\operatorname{fl}(s_{k-1}+1.111111).$$

The exact sum after $k$ terms is

$$1.111111\,k.$$

The important observation is that once the partial sum reaches about $10^6$, the spacing between adjacent eight-digit floating-decimal numbers is

$$10^{6-8+1}=10^{-1}=0.1.$$

Thus numbers near $10^6$ are represented only to the nearest tenth.

Now

$$1.111111 = 11\times 0.1 + 0.011111.$$

Each addition contributes $0.011111$ beyond an exact multiple of $0.1$. Because rounding occurs after every step, these small excesses are repeatedly lost. The accumulated rounding error is positive and grows roughly linearly.

Carrying out the recurrence in eight-digit decimal arithmetic gives

$$s_{10^6}=1111110.0.$$

The exact sum is

$$10^6\cdot 1.111111 = 1111111.0,$$

so the final answer is smaller by $1.0$.

Hence

$$(\cdots((x_1\otimes x_2)\otimes\cdots\otimes x_{10^6}))
=
1111110.0.$$

## (b)

All data values are identical:

$$x_1=x_2=\cdots=x_n=1.111111.$$

Therefore the true variance is exactly zero and the true standard deviation is exactly zero.

### Using Eq. (14)

Equation (14) subtracts two nearly equal quantities:

$$\frac1n\sum x_i^2
\qquad\text{and}\qquad
\left(\frac1n\sum x_i\right)^2.$$

For these data,

$$x_i^2 = 1.234567654321.$$

The quantities

$$\frac1n\sum x_i^2$$

and

$$\left(\frac1n\sum x_i\right)^2$$

should be identical, but the two sums are accumulated with different rounding errors.

The subtraction therefore suffers catastrophic cancellation. In eight-digit arithmetic the computed variance becomes negative. Consequently the standard deviation is not even a real number, because one is asked to take the square root of a negative quantity.

This example is one of Knuth's demonstrations that Eq. (14) is numerically unstable.

### Using Eqs. (15) and (16)

For identical data values, the recurrence behaves perfectly.

Since

$$M_1=1.111111,$$

and every subsequent observation equals the current mean,

$$x_k-M_{k-1}=0$$

for every $k\ge 2$.

Therefore

$$M_k=M_{k-1}$$

and

$$S_k=S_{k-1}.$$

Because

$$S_1=0,$$

it follows inductively that

$$S_k=0$$

for all $k$.

The computed variance and standard deviation are therefore exactly zero.

Thus Eqs. (15) and (16) give the correct answer, while Eq. (14) fails because of cancellation.

## (c)

We must prove that

$$S_k\ge 0$$

for every choice of $x_1,\dots,x_k$.

The key identity is

$$S_k=\sum_{i=1}^k (x_i-M_k)^2.$$

We prove this by induction.

For $k=1$,

$$S_1=0$$

and

$$(x_1-M_1)^2=(x_1-x_1)^2=0,$$

so the identity holds.

Assume

$$S_{k-1}
=
\sum_{i=1}^{k-1}(x_i-M_{k-1})^2.$$

Let

$$\delta=x_k-M_{k-1}.$$

Since

$$M_k=M_{k-1}+\frac{\delta}{k},$$

we have

$$M_{k-1}-M_k=-\frac{\delta}{k}.$$

Now

$$\sum_{i=1}^{k-1}(x_i-M_k)^2
=
\sum_{i=1}^{k-1}
\left((x_i-M_{k-1})+(M_{k-1}-M_k)\right)^2.$$

Expanding and using

$$\sum_{i=1}^{k-1}(x_i-M_{k-1})=0,$$

gives

$$\sum_{i=1}^{k-1}(x_i-M_k)^2
=
S_{k-1}
+
(k-1)\frac{\delta^2}{k^2}.$$

Also,

$$(x_k-M_k)^2
=
\left(\delta-\frac{\delta}{k}\right)^2
=
\frac{(k-1)^2}{k^2}\delta^2.$$

Adding these two expressions yields

$$\sum_{i=1}^{k}(x_i-M_k)^2
=
S_{k-1}
+
\frac{k-1}{k}\delta^2.$$

But

$$\frac{k-1}{k}\delta^2
=
(x_k-M_{k-1})(x_k-M_k),$$

so by the recurrence (16),

$$\sum_{i=1}^{k}(x_i-M_k)^2
=
S_k.$$

The induction is complete.

Therefore

$$S_k
=
\sum_{i=1}^{k}(x_i-M_k)^2.$$

Since every term in this sum is a square,

$$S_k\ge 0.$$

This proves the claim.
