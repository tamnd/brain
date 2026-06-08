---
title: "CF 1944B - Equal XOR"
description: "This is a Type A problem: find all natural numbers $x$ satisfying a given condition. For a Type A problem, the solution must do two things: 1. Derive necessary conditions and prove that every solution must satisfy them. 2."
date: "2026-06-09T01:53:09+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1944
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 934 (Div. 2)"
rating: 1100
weight: 1944
solve_time_s: 133
verified: false
draft: false
---

[CF 1944B - Equal XOR](https://codeforces.com/problemset/problem/1944/B)

**Rating:** 1100  
**Tags:** bitmasks, constructive algorithms  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a Type A problem: find all natural numbers $x$ satisfying a given condition.

For a Type A problem, the solution must do two things:

1. Derive necessary conditions and prove that every solution must satisfy them.
2. Prove that every candidate surviving those conditions is actually a solution.

The proposed solution does verify $x=5$, and it attempts to prove that no other solutions exist. So the structure matches the problem type.

## Step-by-Step Verification

### Step 1: If $x$ has $n$ digits, then prefixing digit $1$ gives $10^n+x$ - VALID

This is correct. For an $n$-digit number $x$, placing a digit $1$ before it yields $1\cdot10^n+x$.

### Step 2: Derivation of

$$\frac{x(x+1)}2=10^n+x$$

and then

$$x^2-x-2\cdot10^n=0$$

- VALID

Algebra is correct.

### Step 3: Conversion to

$$(2x-1)^2=1+8\cdot10^n$$

and definition $y=2x-1$ - VALID

Indeed,

$$4x^2-4x+1=1+8\cdot10^n.$$

No issue.

### Step 4: Factorization

$$(y-1)(y+1)=2^{n+3}5^n$$

- VALID

Since

$$y^2-1=8\cdot10^n
      =2^3\cdot2^n5^n
      =2^{n+3}5^n.$$

Correct.

### Step 5: $\gcd(y-1,y+1)=2$ - VALID

Since $y$ is odd, both factors are even, and

$$\gcd(y-1,y+1)\mid 2.$$

Because both are even, the gcd is exactly $2$.

Checked on odd examples $y=9$ and $y=31$:

$\gcd(8,10)=2$, $\gcd(30,32)=2$.

### Step 6: All powers of $5$ lie in one factor - VALID

Since the gcd is $2$, the factors share no odd prime divisor. Hence the entire factor $5^n$ must occur in exactly one factor.

Correct.

### Step 7: WLOG write

$$y-1=2^a,\qquad y+1=2^b5^n$$

with $a+b=n+3$ - VALID

Since one factor contains no factor $5$, and the only remaining prime in the product is $2$, that factor must be a pure power of $2$.

This is justified.

### Step 8: From

$$2^b5^n-2^a=2$$

deduce

$$2^{b-1}5^n-2^{a-1}=1$$

and hence $b=1$ - VALID

If $b\ge2$, then the first term is even.

Because $a\ge1$, the second term is also even.

Even minus even cannot equal $1$.

Hence $b=1$.

This argument is sound.

### Step 9: Obtain

$$5^n=2^{a-1}+1$$

- VALID

Direct substitution $b=1$.

### Step 10: Show $n$ must be even by reducing modulo $8$ - VALID

The argument is:

Since $a-1\ge2$,

$$2^{a-1}\equiv0\pmod8,$$

hence

$$5^n=2^{a-1}+1\equiv1\pmod8.$$

But

$$5^n\equiv5\pmod8$$

for odd $n$.

Therefore $n$ is even.

Correct.

Checking:

- $n=3$: $5^3=125\equiv5\pmod8$.
- $n=4$: $625\equiv1\pmod8$.

Works.

### Step 11: Let $n=2m$, then

$$(5^m-1)(5^m+1)=2^{a-1}$$

- VALID

Straightforward factorization.

### Step 12: Since the product is a power of $2$, each factor must be a power of $2$ - VALID

Both factors are positive integers and their product contains no odd prime factor.

Hence each factor is itself a power of $2$.

Correct.

### Step 13: Two powers of $2$ differing by $2$ must be $2$ and $4$ - VALID

The proof given is sufficient.

Indeed,

$$2^r+2=2^s$$

implies

$$2^{r-1}+1=2^{s-1}.$$

The left side is odd only when $r=1$, yielding $s=2$.

Correct.

### Step 14: Deduce

$$5^m-1=2,\qquad 5^m+1=4$$

and obtain contradiction - VALID

This yields $5^m=3$, impossible.

Hence $n\ge2$ gives no solution.

Correct.

### Step 15: Check $n=1$ - VALID

$$y^2=81$$

gives $y=9$ (positive root only, since $y=2x-1>0$).

Then

$$x=\frac{9+1}{2}=5.$$

Verification:

$$1+2+3+4+5=15.$$

Correct.

## Completeness Check

The proof covers all possible digit lengths $n$.

The case $n=1$ is handled separately and yields the solution $x=5$.

The case $n\ge2$ is reduced to a contradiction.

No hidden assumptions remain unproved.

One minor issue appears in the initial "Exploration" section:

> $x=14$ gives $105$, which is obtained by writing $1$ in front of $05$.

This observation is informal and irrelevant, but it is not used later and does not affect the proof.

The formal proof itself is complete.

The final conclusion follows exactly from what has been proved.

## Summary

The argument correctly transforms the condition into the Pell-type equation

$$y^2=1+8\cdot10^n,$$

factors it as

$$(y-1)(y+1)=2^{n+3}5^n,$$

uses the fact that the factors differ by $2$, forces one factor to contain all powers of $5$, derives $b=1$, proves $n$ must be even, and finally obtains an impossible factorization of a power of $2$.

All cases are covered, and every crucial step is justified.

VERDICT: PASS - the solution is complete and all steps are correctly justified.
