---
title: "CF 103600B - Blinds"
description: "Let $Sigman = {0,1,2}^n$. Two $n$-trits $x = (x1,dots,xn)$ and $y = (y1,dots,yn)$ are adjacent in an anti-Gray ternary code if and only if $xi neq yi$ for every $1 le i le n$."
date: "2026-07-03T00:56:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103600
codeforces_index: "B"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2021"
rating: 0
weight: 103600
solve_time_s: 132
verified: false
draft: false
---

[CF 103600B - Blinds](https://codeforces.com/problemset/problem/103600/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Solution

Let $\Sigma_n = {0,1,2}^n$. Two $n$-trits $x = (x_1,\dots,x_n)$ and $y = (y_1,\dots,y_n)$ are adjacent in an anti-Gray ternary code if and only if $x_i \neq y_i$ for every $1 \le i \le n$. The task is to determine whether there exists a cyclic ordering of all $3^n$ elements of $\Sigma_n$ such that consecutive elements are adjacent in this sense.

Write addition modulo $3$ on ${0,1,2}$ and extend it coordinatewise to $\Sigma_n$. For $d \in {1,2}^n$, define $x \oplus d = (x_1 + d_1,\dots,x_n + d_n)$. Then $x$ and $y$ are adjacent exactly when $y = x \oplus d$ for some $d \in {1,2}^n$. Indeed, $d_i = y_i - x_i \not\equiv 0 \pmod 3$ for every $i$, so $d_i \in {1,2}$, and conversely any such $d$ yields $y_i \neq x_i$ for all $i$.

Thus the required structure is a Hamiltonian cycle in the Cayley graph of the abelian group $\mathbb{Z}_3^n$ with generating set ${1,2}^n$. The construction proceeds by induction on $n$.

For $n = 1$, the sequence

$$(0,1,2,0)$$

visits all elements of $\Sigma_1$ exactly once and satisfies $0 \neq 1 \neq 2 \neq 0$, so the condition holds.

Assume a cyclic ordering

$$x_0, x_1, \dots, x_{3^n-1}, x_0$$

of $\Sigma_n$ exists such that $x_k$ and $x_{k+1}$ differ in every coordinate for all $k$, where indices are taken modulo $3^n$. In particular, $x_{3^n-1}$ differs from $x_0$ in every coordinate.

Define three copies of this cycle in $\Sigma_{n+1} = \Sigma_n \times {0,1,2}$. For $r \in {0,1,2}$, define

$$x_k^{(r)} = (x_k, r).$$

Construct the sequence

$$x_0^{(0)}, x_1^{(0)}, \dots, x_{3^n-1}^{(0)},\;
x_0^{(1)}, x_1^{(1)}, \dots, x_{3^n-1}^{(1)},\;
x_0^{(2)}, x_1^{(2)}, \dots, x_{3^n-1}^{(2)},\;
x_0^{(0)}.$$

Each transition inside a fixed layer $r$ has the form

$$(x_k, r) \to (x_{k+1}, r),$$

and since $x_k$ and $x_{k+1}$ differ in every coordinate of $\Sigma_n$, the corresponding $(n+1)$-tuples differ in all $n+1$ coordinates.

The transition between layers is

$$(x_{3^n-1}, 0) \to (x_0, 1),$$

and for every coordinate $i \le n$ one has $x_{3^n-1,i} \neq x_{0,i}$ by the cycle property, while $0 \neq 1$ in the last coordinate. Hence this step also differs in every coordinate. The same argument applies to the transitions from layer $1$ to layer $2$ and from layer $2$ back to layer $0$, because addition by $1 \pmod 3$ changes every entry.

The resulting sequence contains exactly $3 \cdot 3^n = 3^{n+1}$ distinct elements of $\Sigma_{n+1}$, and every consecutive pair differs in every coordinate. It is cyclic by construction.

This completes the inductive construction of an anti-Gray ternary code for all $n \ge 1$. ∎
