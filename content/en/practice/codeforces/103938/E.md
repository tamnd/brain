---
title: "CF 103938E - Diverse Debaters"
description: "Algorithm C in this section evaluates a BDD bottom-up by assigning to each node $v$ a value depending only on its LO and HI successors, with sink nodes providing the base cases and each internal node combining results from its children."
date: "2026-07-02T07:04:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103938
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 09-30-22 Div. 1 (Advanced)"
rating: 0
weight: 103938
solve_time_s: 124
verified: false
draft: false
---

[CF 103938E - Diverse Debaters](https://codeforces.com/problemset/problem/103938/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Solution

Algorithm C in this section evaluates a BDD bottom-up by assigning to each node $v$ a value depending only on its LO and HI successors, with sink nodes providing the base cases and each internal node combining results from its children. To compute the generating function, the same traversal is used, but the numeric semiring is replaced by the polynomial semiring $\mathbb{Z}[z]$ with a weight $z$ attached to every assignment $x_i = 1$.

For a sink node corresponding to $\bot$, no assignment satisfies the function, so every term in the generating function vanishes, giving

$G_{\bot}(z)=0.$

For a sink node corresponding to $\top$, exactly one assignment contributes, namely the empty continuation, so

$G_{\top}(z)=1.$

Let $v$ be a branch node labeled by variable $x_k$ with LO successor $v_0$ and HI successor $v_1$. Every satisfying assignment extending $v_0$ assigns $x_k=0$, contributing no increase to the exponent of $z$, while every satisfying assignment extending $v_1$ assigns $x_k=1$, contributing an additional factor of $z$. The subproblems at $v_0$ and $v_1$ are disjoint and preserve the remaining variable structure by the ordering property of the BDD, so contributions combine additively. This yields the recurrence

$G_v(z)=G_{v_0}(z)+z\,G_{v_1}(z).$

Algorithm C is therefore modified by replacing the scalar addition and multiplication in its evaluation step with addition and multiplication in $\mathbb{Z}[z]$, while keeping the same traversal order and memoization structure. Each node is evaluated exactly once as in the original algorithm, and each evaluation performs one polynomial addition and one multiplication by $z$ applied to the HI branch contribution.

The resulting value stored at the root node is

$G(z)=\sum_{x_1=0}^1 \cdots \sum_{x_n=0}^1 z^{x_1+\cdots+x_n} f(x_1,\ldots,x_n),$

since each root-to-$\top$ path corresponds to a unique satisfying assignment, and the exponent accumulates precisely the number of variables set to $1$ along that path.

This completes the modification of Algorithm C. ∎
