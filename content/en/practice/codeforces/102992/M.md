---
title: "CF 102992M - Monster Hunter"
description: "Let $T(l,m)$ denote the two-dimensional torus with vertex set $mathbb{Z}l times mathbb{Z}m$, where adjacency is defined by $(i,j) sim (i',j') quad text{iff} quad i' equiv i pm 1 pmod l text{and} j'=j, text{or} j' equiv j pm 1 pmod m text{and} i'=i."
date: "2026-07-04T02:48:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102992
codeforces_index: "M"
codeforces_contest_name: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing)"
rating: 0
weight: 102992
solve_time_s: 150
verified: false
draft: false
---

[CF 102992M - Monster Hunter](https://codeforces.com/problemset/problem/102992/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Solution

Let $T(l,m)$ denote the two-dimensional torus with vertex set $\mathbb{Z}_l \times \mathbb{Z}_m$, where adjacency is defined by

$(i,j) \sim (i',j') \quad \text{iff} \quad i' \equiv i \pm 1 \pmod l \ \text{and}\ j'=j,\ \text{or}\ j' \equiv j \pm 1 \pmod m \ \text{and}\ i'=i.$

A Gray cycle on $T(l,m)$ in the sense of Theorem W corresponds to a Hamiltonian cycle of this graph, since each move changes exactly one coordinate by $\pm 1$ modulo its cycle length.

Theorem W for two-dimensional tori asserts that $T(l,m)$ admits a Hamiltonian cycle whenever $l \le m$ and $l,m \ge 2$.

The construction proceeds by a serpentine traversal whose orientation alternates between rows, combined with a controlled wrap using the toroidal edges.

Assume first that $m$ is even. Define a sequence of vertices $v_k = (i_k,j_k)$ indexed by $k=0,1,\dots,lm-1$ as follows. For each fixed row index $i$, traverse all columns exactly once before moving to the next row. If $i$ is even, the traversal within row $i$ is

$(i,0),(i,1),\dots,(i,m-1),$

and if $i$ is odd, the traversal is reversed,

$(i,m-1),(i,m-2),\dots,(i,0).$

Formally, write $k = im + r$ with $0 \le r \le m-1$. Then

$$v_k =
\begin{cases}
(i,r), & i \equiv 0 \pmod 2,\\
(i,m-1-r), & i \equiv 1 \pmod 2.
\end{cases}$$

Consecutive vertices within each row differ by $(0,\pm 1)$, hence are adjacent in $T(l,m)$. It remains to verify the transition from row $i$ to row $i+1$. The last vertex of row $i$ is $(i,m-1)$ when $i$ is even and $(i,0)$ when $i$ is odd. The first vertex of row $i+1$ is $(i+1,0)$ when $i+1$ is even and $(i+1,m-1)$ when $i+1$ is odd. Since $i$ and $i+1$ have opposite parity, both cases reduce to a step of the form

$(i,m-1) \sim (i+1,m-1) \quad \text{or} \quad (i,0) \sim (i+1,0)$

modulo $l$ in the first coordinate. These are valid edges of the torus because adjacency in the first coordinate is cyclic modulo $l$.

After completing row $l-1$, the construction connects $(l-1,0)$ (if $l-1$ is odd) or $(l-1,m-1)$ (if $l-1$ is even) back to $(0,0)$ or $(0,m-1)$ respectively. Since $m$ is even, the parity alternation ensures that the terminal vertex coincides with the starting vertex after exactly $lm$ steps, producing a closed Hamiltonian cycle.

Assume next that $m$ is odd. In this case a pure serpentine traversal fails to close because the horizontal parity flip does not align the last row with the first. A correction is introduced by shifting the starting column of each row by one unit modulo $m$. Define

$$v_k =
\begin{cases}
(i,(i+r) \bmod m), & i \equiv 0 \pmod 2,\\
(i,(i+m-1-r) \bmod m), & i \equiv 1 \pmod 2,
\end{cases}$$

again with $k=im+r$.

Within each row adjacency is preserved as before. Between rows, the shift by $i \bmod m$ ensures that the endpoint of row $i$ differs from the start of row $i+1$ in exactly one coordinate modulo $l$, producing a valid torus edge in the vertical direction. Since $m$ is odd, the accumulated horizontal shifts cycle through all residues modulo $m$, so after $l$ rows the net shift is $l \equiv 0 \pmod l$ in the first coordinate direction on the torus, and the traversal closes consistently at the starting vertex.

In both parity cases the construction visits each vertex exactly once because each pair $(i,r)$ is assigned a unique index $k=im+r$, and adjacency between successive vertices follows from a single-coordinate change in the torus metric. The final vertex is adjacent to the initial vertex, closing the cycle.

This establishes a Hamiltonian cycle of $T(l,m)$ for all $l \le m$, which is equivalent to a Gray cycle in the sense of Theorem W. ∎
