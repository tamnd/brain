---
title: "CF 103584B - White Goosefoot"
description: "Let $a{n-1}dots a1a0$ be a binary string with $sum{j=0}^{n-1} aj=t$ and define $bj=ajoplus a{j-1}$ for $1le jle n-1$. The energy is $r=sum{j=1}^{n-1} bj.$ Each $bj=1$ exactly when $ajne a{j-1}$, so $r$ equals the number of transitions in the sequence $a0,a1,dots,a{n-1}$."
date: "2026-07-03T03:06:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103584
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 02-25-22 Div. 2 (Beginner)"
rating: 0
weight: 103584
solve_time_s: 66
verified: false
draft: false
---

[CF 103584B - White Goosefoot](https://codeforces.com/problemset/problem/103584/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
## Solution

Let $a_{n-1}\dots a_1a_0$ be a binary string with $\sum_{j=0}^{n-1} a_j=t$ and define $b_j=a_j\oplus a_{j-1}$ for $1\le j\le n-1$. The energy is

$r=\sum_{j=1}^{n-1} b_j.$

Each $b_j=1$ exactly when $a_j\ne a_{j-1}$, so $r$ equals the number of transitions in the sequence $a_0,a_1,\dots,a_{n-1}$. Hence the string decomposes uniquely into $r+1$ maximal constant runs.

Let these runs be written from left to right as

$u_1,u_2,\dots,u_{r+1},$

where $u_i\ge 1$ and

$u_1+u_2+\cdots+u_{r+1}=n.$

Let the initial bit be $\varepsilon\in{0,1}$. The runs alternate, so run $i$ consists of the bit

$\varepsilon \oplus (i-1)\bmod 2.$

The weight constraint $\sum_{j=0}^{n-1} a_j=t$ becomes a linear condition on run lengths. Define the index set

$I_1(\varepsilon)=\{\,i\mid 1\le i\le r+1,\ \varepsilon\oplus(i-1)\equiv 1 \pmod 2\,\}.$

Then

$\sum_{i\in I_1(\varepsilon)} u_i=t.$

Thus every configuration is uniquely determined by a choice of initial bit $\varepsilon$ and a composition $(u_1,\dots,u_{r+1})$ of $n$ into positive parts satisfying the linear constraint above.

For lexicographic generation it is convenient to replace the composition by the standard difference representation. Define

$p_0=u_1,\quad p_i=u_{i+1}-u_i\ \ (1\le i\le r),$

so that

$u_k=p_0+p_1+\cdots+p_{k-1}\quad (1\le k\le r+1).$

The conditions $u_i\ge 1$ translate to

$p_0\ge 1,\qquad p_0+p_1+\cdots+p_k\ge k+1\ \ (0\le k\le r).$

The total sum condition becomes

$n=\sum_{k=0}^{r} (r+1-k)p_k + \sum_{k=1}^{r} k p_k,$

which simplifies to the standard bijection between compositions and nonnegative increment sequences; in particular, each admissible $(u_1,\dots,u_{r+1})$ is represented uniquely by a composition of $n$ into $r+1$ positive parts.

Generation is therefore reduced to generating all compositions of $n$ into $r+1$ positive parts and testing the weight constraint.

Algorithmically, let $(u_1,\dots,u_{r+1})$ be generated in lexicographic order as in the standard composition generation (equivalently, by iterating the positions of $r$ separators among $n-1$ gaps). For each generated composition, compute the weight contribution by parity of runs.

A direct lexicographic construction proceeds as follows. Maintain $u_1,\dots,u_{r+1}$ with $u_i\ge 1$ and $\sum u_i=n$. At each step, increase the rightmost index $j$ such that $u_j$ can be increased while still allowing completion with positive parts:

$u_j < n - \sum_{i<j} u_i - (r+1-j).$

After increasing $u_j$, set

$u_{j+1}=\cdots=u_{r+1}=1.$

This generates all compositions exactly once in lexicographic order.

For each composition produced, compute

$t'=\sum_{i\in I_1(\varepsilon)} u_i.$

The configuration is accepted exactly when $t'=t$.

To justify correctness, every binary string with energy $r$ yields a unique run decomposition $(u_1,\dots,u_{r+1})$ and a unique initial bit $\varepsilon$, so it is produced by the procedure if and only if its associated composition is generated and satisfies the weight equation. Conversely, every generated pair $(\varepsilon,(u_1,\dots,u_{r+1}))$ defines a unique binary string whose run structure has exactly $r$ transitions and weight $t$ by construction of the alternating assignment and the sum constraint.

This establishes a bijection between valid configurations and accepted generated pairs, so the algorithm generates all and only the desired strings.

This completes the proof. ∎
