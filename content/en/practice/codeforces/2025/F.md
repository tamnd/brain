---
title: "CF 2025F - Choose Your Queries"
description: "For a polynomial $f$ of degree $n$, define $Fk(x)=sum{j=0}^{k}f(x+j).$ The dependence on $k$ is described by Faulhaber's formulas."
date: "2026-06-09T03:15:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "dp", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2025
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 170 (Rated for Div. 2)"
rating: 2700
weight: 2025
solve_time_s: 129
verified: false
draft: false
---

[CF 2025F - Choose Your Queries](https://codeforces.com/problemset/problem/2025/F)

**Rating:** 2700  
**Tags:** constructive algorithms, dfs and similar, dp, graphs, greedy, trees  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Exploration

For a polynomial $f$ of degree $n$, define

$F_k(x)=\sum_{j=0}^{k}f(x+j).$

The dependence on $k$ is described by Faulhaber's formulas. If

$f(t)=a_nt^n+a_{n-1}t^{n-1}+\cdots,$

then

$$=\frac{(x+k)^{n+1}-x^{n+1}}{n+1}
+O(k^n),$$

uniformly for $x$ in intervals whose length is proportional to $k$.

This suggests introducing the rescaled variable

$$\qquad
G_k(y)=\frac{F_k(ky)}{k^{n+1}}.$$

The sums then become Riemann sums, and one expects

$$=\frac{a_n}{n+1}\bigl((y+1)^{n+1}-y^{n+1}\bigr).$$

The limit polynomial is explicit. Its real zeros can be analyzed directly.

## Problem Understanding

The task is to prove existence of a suitable $k$.

For even $\deg f=n$, we must show that some $F_k$ has no real roots.

For odd $\deg f=n$, we must show that some $F_k$ has exactly one real root.

The central observation is that after scaling by $k$, the normalized polynomial $F_k(ky)/k^{n+1}$ approaches

$$$$

Since $n+1$ has opposite parity to $n$, the root structure of $H$ is very simple and can be transferred to $G_k$ for sufficiently large $k$.

## Proof Architecture

We first establish the asymptotic limit

$$\longrightarrow
H(y)
=\frac{a_n}{n+1}\bigl((y+1)^{n+1}-y^{n+1}\bigr),$$

uniformly on every bounded interval.

Then we analyze $H$.

If $n$ is even, then $n+1$ is odd. The equation

$(y+1)^{n+1}-y^{n+1}=0$

implies

$(y+1)^{n+1}=y^{n+1}.$

Since $n+1$ is odd, the function $t\mapsto t^{n+1}$ is injective on $\mathbb R$, hence $y+1=y$, impossible. Thus $H$ has no real roots.

If $n$ is odd, then $n+1$ is even. The equation

$(y+1)^{n+1}=y^{n+1}$

gives

$|y+1|=|y|,$

whose unique real solution is

$y=-\frac12.$

Moreover this root is simple because

$$=a_n\bigl((y+1)^n-y^n\bigr),$$

and

$$=a_n\left(\left(\frac12\right)^n-\left(-\frac12\right)^n\right)
\neq0$$

since $n$ is odd.

Thus $H$ has exactly one simple real root.

Uniform convergence then implies that for sufficiently large $k$, the polynomial $G_k$ has the same number of real roots as $H$. Rescaling back from $G_k$ to $F_k$ preserves the number of roots.

## Solution

Let

$$\qquad a_n\neq0.$$

Define

$$$$

and

$$$$

Write

$$= a_n(ky+j)^n + O(k^{n-1}),$$

uniformly for $y$ in any fixed bounded interval and for $0\le j\le k$.

Hence

$$G_k(y)
=
a_n\frac1k
\sum_{j=0}^{k}
\left(y+\frac{j}{k}\right)^n
+O\!\left(\frac1k\right).$$

The first term is a Riemann sum. Therefore, uniformly on every bounded interval,

$$G_k(y)
\longrightarrow
a_n\int_0^1 (y+t)^n\,dt
=
\frac{a_n}{n+1}
\bigl((y+1)^{n+1}-y^{n+1}\bigr).$$

Denote the limit polynomial by

$$H(y)
=
\frac{a_n}{n+1}
\bigl((y+1)^{n+1}-y^{n+1}\bigr).$$

### Part 1

Assume $n$ is even.

Then $n+1$ is odd. If $H(y)=0$, then

$$(y+1)^{n+1}=y^{n+1}.$$

Since $n+1$ is odd, the map $t\mapsto t^{n+1}$ is strictly monotone, so $y+1=y$, impossible.

Thus $H$ has no real roots.

Since $H$ is continuous and never vanishes, there exists $c>0$ such that

$$|H(y)|\ge c$$

for all $y$ in a sufficiently large interval $[-R,R]$. Uniform convergence gives

$$|G_k(y)-H(y)|<c/2$$

there for all sufficiently large $k$, hence $G_k$ has no roots in $[-R,R]$.

Outside that interval, $H$ keeps a fixed sign and has the same growth as $y^n$. Uniform convergence of coefficients implies that for sufficiently large $k$, the same sign persists for $G_k$. Consequently $G_k$ has no real roots at all.

Since

$$G_k(y)=\frac{F_k(ky)}{k^{n+1}},$$

the polynomial $F_k$ also has no real roots.

### Part 2

Assume $n$ is odd.

Then $n+1$ is even. The equation

$$H(y)=0$$

is equivalent to

$$|y+1|=|y|,$$

whose unique solution is

$$y_0=-\frac12.$$

Furthermore,

$$H'(y)
=
a_n\bigl((y+1)^n-y^n\bigr),$$

and

$$H'(y_0)
=
a_n\left(
\left(\frac12\right)^n
-
\left(-\frac12\right)^n
\right)
\neq0.$$

Thus $y_0$ is a simple root and the only real root of $H$.

Choose a small neighborhood of $y_0$ containing no other zeros of $H$. Uniform convergence implies that for sufficiently large $k$, the polynomial $G_k$ has exactly one real root in that neighborhood. Outside the neighborhood, $H$ stays bounded away from $0$, so uniform convergence shows that $G_k$ has no additional real roots.

Hence for sufficiently large $k$, $G_k$ has exactly one real root.

Rescaling from $G_k$ back to $F_k$ preserves the number of real roots, because

$$G_k(y)=0
\iff
F_k(ky)=0.$$

Therefore $F_k$ has exactly one real root.

Both statements are proved. ∎
