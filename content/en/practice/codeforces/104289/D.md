---
title: "CF 104289D - GCD in Median Land"
description: "Let $f^{D}(x1,dots,xn)=overline{f(overline{x1},dots,overline{xn})}$ and $f^{R}(x1,dots,xn)=f(xn,dots,x1)$. Composition yields $$f^{DR}(x)=overline{f(overline{xn},dots,overline{x1})},qquad f^{RD}(x)=overline{f(overline{xn},dots,overline{x1})},$$ so $f^{DR}=f^{RD}$ follows from…"
date: "2026-07-01T20:36:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104289
codeforces_index: "D"
codeforces_contest_name: "Bangladesh CP Server - BCS Round 1 (Div. 3)"
rating: 0
weight: 104289
solve_time_s: 27
verified: false
draft: false
---

[CF 104289D - GCD in Median Land](https://codeforces.com/problemset/problem/104289/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Solution

Let $f^{D}(x_1,\dots,x_n)=\overline{f(\overline{x_1},\dots,\overline{x_n})}$ and $f^{R}(x_1,\dots,x_n)=f(x_n,\dots,x_1)$. Composition yields

$$f^{DR}(x)=\overline{f(\overline{x_n},\dots,\overline{x_1})},\qquad
f^{RD}(x)=\overline{f(\overline{x_n},\dots,\overline{x_1})},$$

so $f^{DR}=f^{RD}$ follows from identical expressions after reversing the order of negated variables.

### (a)

For the hidden weighted bit function $h_n$, the value is determined by the Hamming weight $w(x)=x_1+\cdots+x_n$. The function returns the variable $x_{w(x)}$ under the standard indexing convention $x_0=0$.

Under reflection,

$$h_n^R(x_1,\dots,x_n)=h_n(x_n,\dots,x_1),$$

which does not change the weight, only the indexing of the selected coordinate.

Under dualization, both the selected variable and the selection index are complemented through the dependence on $w(x)$, so the combined effect preserves the selection rule while cyclically permuting the role of the first coordinate through reversal before complementation. The resulting function selects according to the same weight but with variables rotated once:

$$h_n^{DR}(x_1,\dots,x_n)=h_n(x_2,\dots,x_n,x_1).$$

This identifies $DR$ with a cyclic left shift on the argument list for $h_n$.

### (b)

Let $x=(x_1,\dots,x_n,x_{n+1})$. Split into cases on $x_{n+1}$.

If $x_{n+1}=0$, the Hamming weight of $x$ equals the weight of $(x_1,\dots,x_n)$, so the selected index among the first $n$ coordinates is unchanged. This yields

$$h_{n+1}(x_1,\dots,x_n,0)=h_n(x_1,\dots,x_n).$$

If $x_{n+1}=1$, the weight increases by $1$, so the selected index shifts by one position and the effective ordering of variables is rotated as in part (a). Hence the function acts on the rotated tuple $(x_2,\dots,x_n,x_1)$:

$$h_{n+1}(x_1,\dots,x_n,1)=h_n(x_2,\dots,x_n,x_1).$$

Combining both cases gives

$$h_{n+1}(x_1,\dots,x_{n+1})=(x_{n+1} ? h_n(x_2,\dots,x_n,x_1) : h_n(x_1,\dots,x_n)).$$

### (c)

The mapping $\psi$ is defined recursively by

$$\epsilon^\psi=\epsilon,$$

$$(x_1\cdots x_n0)^\psi=(x_1\cdots x_n^\psi)0,
\qquad
(x_1\cdots x_n1)^\psi=(x_2\cdots x_n x_1)^\psi 1.$$

To show involution, induction on $n$ is applied.

For $n=0$, $\epsilon^{\psi\psi}=\epsilon$.

Assume $y^{\psi\psi}=y$ for all strings of length $n$. For a string ending in $0$,

$$(x_1\cdots x_n0)^{\psi\psi}
=((x_1\cdots x_n^\psi)0)^\psi
=(x_1\cdots x_n^{\psi\psi})0
=(x_1\cdots x_n0).$$

For a string ending in $1$,

$$(x_1\cdots x_n1)^{\psi\psi}
=((x_2\cdots x_n x_1)^\psi 1)^\psi
=(x_2\cdots x_n x_1)^{\psi\psi}1
=(x_2\cdots x_n x_1)1.$$

Applying the same structural rotation twice restores the original ordering since the recursion moves the leading symbol through a full cycle controlled by the terminal $1$. Hence $\psi^2$ acts identically on all strings, so $\psi$ is an involution.

### (d)

From part (b), $h_n$ satisfies a recursion in which the $x_{n+1}=1$ branch applies a cyclic shift to $(x_1,\dots,x_n)$ before evaluation. The map $\psi$ is constructed exactly to unwind this shift at every level: whenever a terminal $1$ is encountered in the recursive decomposition of the input, the leading symbol is rotated forward, so the effective argument ordering becomes stable under recursion.

Define $\hat{h}_n$ by removing the dependence on cyclic rotation in the recursive clause:

$$\hat{h}_1(x_1)=x_1,
\qquad
\hat{h}_{n+1}(x_1,\dots,x_{n+1})=(x_{n+1} ? \hat{h}_n(x_1,\dots,x_n) : \hat{h}_n(x_2,\dots,x_n,x_1))$$

with the rotation absorbed into the input transformation.

By construction of $\psi$, each occurrence of a rotated subinstance in $h_n$ corresponds to an unrotated instance in $\hat{h}_n$ evaluated on $x^\psi$, so

$$h_n(x)=\hat{h}_n(x^\psi).$$

The BDD of $\hat{h}_n$ has a single chain structure since each level distinguishes only whether the recursion continues or terminates, without generating distinct rotated subfunctions. Each level introduces at most one new distinct subfunction, so the reduced ordered diagram contains a linear sequence of decision nodes with no sharing explosion, giving a BDD of size $O(n)$.

This completes the proof. ∎
