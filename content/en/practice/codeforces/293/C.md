---
title: "CF 293C - Cube Problem"
description: "The three original cubes had side lengths $a$, $b$, and $c$. Their total number of unit cubes was $$a^3+b^3+c^3.$$ Vitaly wanted to build one larger cube whose side length was $a+b+c$, which would require $$(a+b+c)^3$$ unit cubes."
date: "2026-06-05T17:22:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 293
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2013 - Round 2"
rating: 2400
weight: 293
solve_time_s: 157
verified: false
draft: false
---

[CF 293C - Cube Problem](https://codeforces.com/problemset/problem/293/C)

**Rating:** 2400  
**Tags:** brute force, math, number theory  
**Solve time:** 2m 37s  
**Verified:** no  

## Solution
## Problem Understanding

The three original cubes had side lengths $a$, $b$, and $c$. Their total number of unit cubes was

$$a^3+b^3+c^3.$$

Vitaly wanted to build one larger cube whose side length was $a+b+c$, which would require

$$(a+b+c)^3$$

unit cubes.

He was short by exactly $n$ cubes, so

$$(a+b+c)^3-(a^3+b^3+c^3)=n.$$

We are given only $n$, and we must count how many positive integer triples $(a,b,c)$ could have produced that value.

The bound $n \le 10^{14}$ immediately rules out any search over possible values of $a$, $b$, or $c$. Cube roots of $10^{14}$ are around $4.6 \times 10^4$, so even a triple loop over all possible side lengths would require more than $10^{13}$ iterations.

The key observation is that the expression has a strong algebraic structure. Once it is transformed into a multiplicative equation, the problem becomes one of enumerating divisors of a number up to about $3.3 \times 10^{13}$. Numbers of that size have relatively few divisors, making divisor-based enumeration practical.

Several edge cases are easy to mishandle.

For example, if

```
n = 1
```

then

$$(a+b+c)^3-(a^3+b^3+c^3)$$

is always divisible by $3$, so the answer must be $0$. A solution that starts enumerating divisors without checking divisibility by $3$ wastes work and may produce incorrect results.

Another subtle case is

```
n = 24
```

which corresponds to

$$3(a+b)(b+c)(c+a)=24.$$

The factor triple $(1,1,8)$ satisfies the product condition, but it does not correspond to positive integer values of $a,b,c$. Recovering $a,b,c$ requires both parity and positivity constraints. Ignoring those constraints overcounts.

A third common mistake is forgetting that $(a,b,c)$ is ordered. The triples $(1,2,3)$ and $(2,1,3)$ are different solutions. When we enumerate sorted factor triples, we must restore the correct multiplicity.

## Approaches

Start from the identity

$$(a+b+c)^3-(a^3+b^3+c^3) = 3(a+b)(b+c)(c+a).$$

Let

$$x=a+b,\quad y=b+c,\quad z=c+a.$$

Then the problem becomes

$$3xyz=n.$$

If $n$ is not divisible by $3$, there are no solutions.

A brute-force idea would be to enumerate all factor triples $(x,y,z)$ whose product is $n/3$, reconstruct $a,b,c$, and count the valid ones. This is already much better than enumerating $a,b,c$, because the number of divisors of a $10^{13}$-sized integer is small.

The remaining challenge is counting efficiently.

Given

$$m=\frac n3,$$

we need all positive integer triples satisfying

$$xyz=m.$$

From

$$a=\frac{x+z-y}{2},\quad b=\frac{x+y-z}{2},\quad c=\frac{y+z-x}{2},$$

a triple corresponds to valid positive integers exactly when

$$x+y+z \equiv 0 \pmod 2$$

and the strict triangle inequalities hold:

$$x+y>z,\quad y+z>x,\quad z+x>y.$$

Since we enumerate factor triples in sorted order $x \le y \le z$, only

$$x+y>z$$

needs to be checked.

The brute-force factor enumeration is correct, but enumerating all positive triples independently would still be too large. The observation that $xyz=m$ lets us enumerate only divisors of $m$. Even for the worst possible $m$, the divisor count is only a few thousand, so checking divisor pairs is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $a,b,c$ | $O((\sqrt[3]{n})^3)$ | $O(1)$ | Too slow |
| Divisor Enumeration | $O(d(m)^2)$ | $O(d(m))$ | Accepted |

Here $d(m)$ denotes the number of divisors of $m$.

## Algorithm Walkthrough

1. Read $n$.
