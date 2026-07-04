---
title: "CF 102951A - Maximum Distance"
description: "Let the 2 × 2 × 3 torus be the Cartesian product of directed cycles $C2 times C2 times C3$, with vertex set $V = {(i,j,k) mid i in {0,1}, j in {0,1}, k in {0,1,2}}."
date: "2026-07-04T07:24:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102951
codeforces_index: "A"
codeforces_contest_name: "USACO Guide Problem Submission"
rating: 0
weight: 102951
solve_time_s: 155
verified: false
draft: false
---

[CF 102951A - Maximum Distance](https://codeforces.com/problemset/problem/102951/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Solution

Let the 2 × 2 × 3 torus be the Cartesian product of directed cycles $C_2 \times C_2 \times C_3$, with vertex set

$V = \{(i,j,k) \mid i \in \{0,1\},\ j \in \{0,1\},\ k \in \{0,1,2\}\}.$

The relation underlying the torus (as in example (69)) connects each vertex to its unit forward neighbors in each coordinate direction, with wraparound modulo the coordinate sizes. For a vertex $x = (i,j,k)$ this defines three outgoing steps:

$(i,j,k) \to (i+1 \bmod 2, j, k), \quad (i,j,k) \to (i, j+1 \bmod 2, k), \quad (i,j,k) \to (i, j, k+1 \bmod 3).$

The $\alpha$ function assigns to a vertex the set of its forward images under these steps, and the $\beta$ function assigns the set of vertices that map forward into it, which is equivalently obtained by reversing each coordinate step.

Thus for every $(i,j,k) \in V$,

$\alpha(i,j,k) = \{(i+1 \bmod 2, j, k),\ (i, j+1 \bmod 2, k),\ (i, j, k+1 \bmod 3)\},$

and

$\beta(i,j,k) = \{(i-1 \bmod 2, j, k),\ (i, j-1 \bmod 2, k),\ (i, j, k-1 \bmod 3)\}.$

To compute these explicitly, it suffices to evaluate the modular increments in each coordinate.

For $i=0$, $i+1 \bmod 2 = 1$ and $i-1 \bmod 2 = 1$. For $i=1$, both $i+1 \bmod 2$ and $i-1 \bmod 2$ equal $0$. The same symmetry holds for $j$. For $k \in {0,1,2}$, the forward cycle is $0 \to 1 \to 2 \to 0$ and the backward cycle is $0 \to 2 \to 1 \to 0$.

Hence all values of $\alpha$ and $\beta$ can be listed by substituting these modular transitions.

For $\alpha$:

For $(0,0,0)$,

$\alpha(0,0,0) = \{(1,0,0),(0,1,0),(0,0,1)\}.$

For $(0,0,1)$,

$\alpha(0,0,1) = \{(1,0,1),(0,1,1),(0,0,2)\}.$

For $(0,0,2)$,

$\alpha(0,0,2) = \{(1,0,2),(0,1,2),(0,0,0)\}.$

For $(0,1,0)$,

$\alpha(0,1,0) = \{(1,1,0),(0,0,0),(0,1,1)\}.$

For $(0,1,1)$,

$\alpha(0,1,1) = \{(1,1,1),(0,0,1),(0,1,2)\}.$

For $(0,1,2)$,

$\alpha(0,1,2) = \{(1,1,2),(0,0,2),(0,1,0)\}.$

For $(1,0,0)$,

$\alpha(1,0,0) = \{(0,0,0),(1,1,0),(1,0,1)\}.$

For $(1,0,1)$,

$\alpha(1,0,1) = \{(0,0,1),(1,1,1),(1,0,2)\}.$

For $(1,0,2)$,

$\alpha(1,0,2) = \{(0,0,2),(1,1,2),(1,0,0)\}.$

For $(1,1,0)$,

$\alpha(1,1,0) = \{(0,1,0),(1,0,0),(1,1,1)\}.$

For $(1,1,1)$,

$\alpha(1,1,1) = \{(0,1,1),(1,0,1),(1,1,2)\}.$

For $(1,1,2)$,

$\alpha(1,1,2) = \{(0,1,2),(1,0,2),(1,1,0)\}.$

The $\beta$ function is obtained by reversing each of the three coordinate moves. This produces:

For $(0,0,0)$,

$\beta(0,0,0) = \{(1,0,0),(0,1,0),(0,0,2)\}.$

For $(0,0,1)$,

$\beta(0,0,1) = \{(1,0,1),(0,1,1),(0,0,0)\}.$

For $(0,0,2)$,

$\beta(0,0,2) = \{(1,0,2),(0,1,2),(0,0,1)\}.$

For $(0,1,0)$,

$\beta(0,1,0) = \{(1,1,0),(0,0,0),(0,1,2)\}.$

For $(0,1,1)$,

$\beta(0,1,1) = \{(1,1,1),(0,0,1),(0,1,0)\}.$

For $(0,1,2)$,

$\beta(0,1,2) = \{(1,1,2),(0,0,2),(0,1,1)\}.$

For $(1,0,0)$,

$\beta(1,0,0) = \{(0,0,0),(1,1,0),(1,0,2)\}.$

For $(1,0,1)$,

$\beta(1,0,1) = \{(0,0,1),(1,1,1),(1,0,0)\}.$

For $(1,0,2)$,

$\beta(1,0,2) = \{(0,0,2),(1,1,2),(1,0,1)\}.$

For $(1,1,0)$,

$\beta(1,1,0) = \{(0,1,0),(1,0,0),(1,1,2)\}.$

For $(1,1,1)$,

$\beta(1,1,1) = \{(0,1,1),(1,0,1),(1,1,0)\}.$

For $(1,1,2)$,

$\beta(1,1,2) = \{(0,1,2),(1,0,2),(1,1,1)\}.$

Each entry follows directly from applying the coordinatewise cyclic predecessor and successor operations on $C_2 \times C_2 \times C_3$. This completes the computation of the $\alpha$ and $\beta$ functions for the 2 × 2 × 3 torus. ∎
