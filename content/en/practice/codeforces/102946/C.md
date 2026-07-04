---
title: "CF 102946C - Chicken Nuggets"
description: "Let the $2times 2times 3$ torus be the Cartesian product $$T = mathbb{Z}2 times mathbb{Z}2 times mathbb{Z}3,$$ so each element is a triple $(x,y,z)$ with $x,y in {0,1}$ and $z in {0,1,2}$, with arithmetic taken modulo $2,2,3$ respectively. This gives $12$ vertices."
date: "2026-07-04T07:31:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102946
codeforces_index: "C"
codeforces_contest_name: "NCTU PCCA Winter Contest 2021"
rating: 0
weight: 102946
solve_time_s: 152
verified: false
draft: false
---

[CF 102946C - Chicken Nuggets](https://codeforces.com/problemset/problem/102946/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Solution

Let the $2\times 2\times 3$ torus be the Cartesian product

$$T = \mathbb{Z}_2 \times \mathbb{Z}_2 \times \mathbb{Z}_3,$$

so each element is a triple $(x,y,z)$ with $x,y \in {0,1}$ and $z \in {0,1,2}$, with arithmetic taken modulo $2,2,3$ respectively. This gives $12$ vertices.

The torus structure in (69) is the Cayley graph of $T$ with the standard generators corresponding to unit increments in each coordinate. For a vertex $u=(x,y,z)$, define the three forward neighbors by increasing one coordinate modulo its cycle length. This produces the local forward move structure that defines $\alpha$. The inverse moves define $\beta$.

The function $\alpha$ maps each vertex to the set of vertices obtained by applying one forward generator. Thus,

$$\alpha(x,y,z)
=
\{(x+1 \bmod 2, y, z),\ (x, y+1 \bmod 2, z),\ (x, y, z+1 \bmod 3)\}.$$

The function $\beta$ maps each vertex to the set obtained by applying the inverse generators, which subtract $1$ in each coordinate modulo the corresponding modulus. Thus,

$$\beta(x,y,z)
=
\{(x-1 \bmod 2, y, z),\ (x, y-1 \bmod 2, z),\ (x, y, z-1 \bmod 3)\}.$$

Writing these explicitly using representatives in ${0,1}$ and ${0,1,2}$ gives

$$x-1 \bmod 2 = 1-x,\quad y-1 \bmod 2 = 1-y,\quad z-1 \bmod 3 =
\begin{cases}
2,& z=0\\
0,& z=1\\
1,& z=2.
\end{cases}$$

Hence

$$\beta(x,y,z)
=
\{(1-x, y, z),\ (x, 1-y, z),\ (x, y, z-1 \bmod 3)\}.$$

Each vertex of the torus has exactly three $\alpha$-images and three $\beta$-preimages, matching the 3-generator structure of the $2\times 2\times 3$ cyclic product graph. The pair $(\alpha,\beta)$ forms the forward and backward adjacency operators of this Cayley torus, consistent with the cross-order duality framework of the preceding exercises.

This completes the computation. ∎
