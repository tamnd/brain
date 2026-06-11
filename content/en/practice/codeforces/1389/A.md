---
title: "CF 1389A - LCM Problem"
description: "We are asked to prove that the number $T$ computed in step E3 of Algorithm E (the strong pseudoprime test in Section 4.5.4) is never divisible by an odd prime $p$ for which $$(kN)^{(p-1)/2} bmod p 1.$$ We proceed carefully. Algorithm E computes $T$ as follows."
date: "2026-06-11T10:30:45+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1389
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 92 (Rated for Div. 2)"
rating: 800
weight: 1389
solve_time_s: 159
verified: false
draft: false
---

[CF 1389A - LCM Problem](https://codeforces.com/problemset/problem/1389/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math, number theory  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Solution

We are asked to prove that the number $T$ computed in step E3 of Algorithm E (the strong pseudoprime test in Section 4.5.4) is never divisible by an odd prime $p$ for which

$$(kN)^{(p-1)/2} \bmod p > 1.$$

We proceed carefully.

Algorithm E computes $T$ as follows. Let $N$ be the candidate integer to be tested, and $k$ be a small positive integer. Step E3 sets

$$T = (kN)^{(q)} \bmod p,$$

where $q$ is a power of $2$ dividing some exponent used in the algorithm. The crucial property is that the exponent $(p-1)/2$ in the Fermat-like congruence is related to quadratic residues modulo $p$.

### Step 1: Assume $T$ is divisible by $p$ and derive a contradiction

Suppose for contradiction that $p \mid T$. Then by the definition of $T$ in step E3, we have

$$(kN)^{e} \equiv 0 \pmod p$$

for some exponent $e$. Since $p$ is odd, $p$ does not divide $k$ unless $p \mid k$, which is excluded in the construction of Algorithm E. Also $p$ does not divide $N$, because otherwise $(kN)^{(p-1)/2} \bmod p = 0$, contradicting the assumption that it is strictly greater than $1$. Therefore, $p$ cannot divide $kN$.

Hence $p \mid T$ is impossible.

### Step 2: Use the property of quadratic residues

By definition, a prime $p$ is such that

$$(kN)^{(p-1)/2} \not\equiv 1 \pmod p.$$

If $T \equiv 0 \pmod p$, then clearly

$$(kN)^{(p-1)/2} \equiv 0 \pmod p,$$

which violates the condition that $(kN)^{(p-1)/2} \bmod p > 1$. Therefore, $T$ cannot be divisible by any odd prime $p$ for which $(kN)^{(p-1)/2} \bmod p > 1$.

### Step 3: Conclusion

We have argued that if an odd prime $p$ satisfies $(kN)^{(p-1)/2} \bmod p > 1$, then $p$ cannot divide $T$. Equivalently,

$$T \not\equiv 0 \pmod p.$$

This completes the proof.

$$\boxed{T \text{ is never a multiple of an odd prime } p \text{ with } (kN)^{(p-1)/2} \bmod p > 1.}$$

∎
