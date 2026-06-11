---
title: "CF 1348D - Phoenix and Science"
description: "Let $u(x)$ be a polynomial with integer coefficients that is squarefree over $mathbb{Z}$. This means that $u(x)$ has no repeated roots in $mathbb{C}$, equivalently, $gcd(u(x), u'(x)) = 1$ in $mathbb{Z}[x]$, where $u'(x)$ is the derivative of $u(x)$."
date: "2026-06-11T14:48:27+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1348
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 638 (Div. 2)"
rating: 1900
weight: 1348
solve_time_s: 173
verified: false
draft: false
---

[CF 1348D - Phoenix and Science](https://codeforces.com/problemset/problem/1348/D)

**Rating:** 1900  
**Tags:** binary search, constructive algorithms, greedy, implementation, math  
**Solve time:** 2m 53s  
**Verified:** no  

## Solution
## Corrected Solution for Exercise 4.6.2.23

Let $u(x)$ be a polynomial with integer coefficients that is squarefree over $\mathbb{Z}$. This means that $u(x)$ has no repeated roots in $\mathbb{C}$, equivalently, $\gcd(u(x), u'(x)) = 1$ in $\mathbb{Z}[x]$, where $u'(x)$ is the derivative of $u(x)$.

We want to show that there are only finitely many primes $p$ such that $u(x)$ is not squarefree modulo $p$, i.e., such that the reduction $\overline{u}(x) \in \mathbb{F}_p[x]$ has a repeated root.

### Step 1: Characterization of squarefreeness modulo $p$

A polynomial $v(x)$ over a field $F$ is squarefree if and only if $\gcd(v(x), v'(x)) = 1$ in $F[x]$. Therefore, $\overline{u}(x)$ is **not squarefree modulo $p$** if and only if

$$\gcd\big(\overline{u}(x), \overline{u}'(x)\big) \neq 1 \quad \text{in } \mathbb{F}_p[x].$$

Equivalently, there exists a nonconstant polynomial $d(x) \in \mathbb{F}_p[x]$ dividing both $\overline{u}(x)$ and $\overline{u}'(x)$.

### Step 2: Use the resultant

Let $R = \operatorname{Res}(u, u')$ denote the **resultant** of $u(x)$ and $u'(x)$. The resultant satisfies:

$$R = 0 \quad \text{if and only if} \quad \gcd(u, u') \neq 1 \text{ in } \mathbb{C}[x].$$

Since $u(x)$ is squarefree over $\mathbb{Z}$, we have $\gcd(u, u') = 1$ over $\mathbb{Z}[x]$, so

$$R = \operatorname{Res}(u, u') \neq 0.$$

The resultant is an integer. Furthermore, for any prime $p$, the reduction of $u$ modulo $p$ satisfies

$$\overline{u}(x) \text{ is not squarefree over } \mathbb{F}_p \quad \iff \quad p \text{ divides } R.$$

This follows because $\gcd(\overline{u}, \overline{u}') \neq 1$ over $\mathbb{F}_p[x]$ if and only if the resultant vanishes modulo $p$.

### Step 3: Only finitely many primes divide a nonzero integer

Since $R \in \mathbb{Z}$ is nonzero, it has only finitely many prime divisors. Let $p_1, p_2, \dots, p_k$ denote these primes. Then for any prime $p \notin \{p_1, \dots, p_k\}$, the polynomial $\overline{u}(x)$ is squarefree modulo $p$.

### Step 4: Conclusion

Therefore, the set of primes $p$ such that $u(x)$ is **not squarefree modulo $p$** is contained in the finite set of prime divisors of $\operatorname{Res}(u, u')$. Hence, there are only finitely many such primes.

$$\boxed{\text{Only finitely many primes } p \text{ make } u(x) \text{ not squarefree modulo } p.}$$

### Step 5: Optional remark

This argument does not require explicit computation of the roots of $u(x)$ or $u'(x)$. It relies purely on the algebraic properties of resultants and the fact that nonzero integers have finitely many prime divisors.

**End of solution.**
