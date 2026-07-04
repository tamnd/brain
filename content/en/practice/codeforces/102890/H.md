---
title: "CF 102890H - How to Work Less to Pass a Programming Course in Planet E-13"
description: "A partition $alpha$ is self-conjugate when its Ferrers diagram is symmetric across the main diagonal. The diagonal cells form a staircase of size $k$ for some $k ge 0$, and the diagram is determined by the hook lengths emanating symmetrically from these $k$ diagonal cells."
date: "2026-07-04T13:03:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102890
codeforces_index: "H"
codeforces_contest_name: "2020 ICPC Gran Premio de Mexico 3ra Fecha"
rating: 0
weight: 102890
solve_time_s: 179
verified: false
draft: false
---

[CF 102890H - How to Work Less to Pass a Programming Course in Planet E-13](https://codeforces.com/problemset/problem/102890/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Solution

A partition $\alpha$ is self-conjugate when its Ferrers diagram is symmetric across the main diagonal. The diagonal cells form a staircase of size $k$ for some $k \ge 0$, and the diagram is determined by the hook lengths emanating symmetrically from these $k$ diagonal cells.

Let the $i$-th diagonal cell have arm length $a_i$ to the right and leg length $a_i$ downward. Self-conjugacy forces equality of arm and leg lengths, so each diagonal cell contributes a hook of size $2a_i + 1$, and these hook sizes are strictly decreasing as $i$ increases. Equivalently, the partition is determined by a strictly decreasing sequence of positive integers of the form $2a_i+1$, hence by a partition into distinct odd parts.

Conversely, given a partition into distinct odd parts

$\lambda_1 > \lambda_2 > \cdots > \lambda_k,$

with each $\lambda_i = 2a_i+1$, one constructs a Ferrers diagram with $k$ diagonal cells, and the $i$-th diagonal cell having arm and leg length $a_i$. The strict decrease of the $\lambda_i$ ensures the diagram fits and produces a valid partition, and symmetry across the diagonal holds by construction. This correspondence is bijective between self-conjugate partitions and partitions into distinct odd parts.

The generating function for partitions into distinct odd parts is obtained by independent choice of each odd part $2j-1$, either included once or not included. Each inclusion contributes weight $x^{2j-1}$, and exclusion contributes $1$, so each part contributes a factor $(1 + x^{2j-1})$. Multiplying over all odd integers gives the full generating function

$\sum_{n \ge 0} sc(n)x^n = \prod_{j \ge 1} (1 + x^{2j-1}).$

This completes the derivation of the generating function. ∎
