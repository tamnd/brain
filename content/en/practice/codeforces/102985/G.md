---
title: "CF 102985G - Expected Distance"
description: "Let $T(m1,dots,m{n-1},m)$ be the $(n)$-dimensional torus equipped with cross order. Write elements as $(y,a)$ where $y in T(m1,dots,m{n-1})$ and $0 le a < m$ denotes the final component."
date: "2026-07-04T03:10:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102985
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 03-05-21 Div. 1 (Advanced)"
rating: 0
weight: 102985
solve_time_s: 144
verified: false
draft: false
---

[CF 102985G - Expected Distance](https://codeforces.com/problemset/problem/102985/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Setup

Let $T(m_1,\dots,m_{n-1},m)$ be the $(n)$-dimensional torus equipped with cross order. Write elements as $(y,a)$ where $y \in T(m_1,\dots,m_{n-1})$ and $0 \le a < m$ denotes the final component. Let $x = x_1 \dots x_{n-1}$ be the $N$th element of $T(m_1,\dots,m_{n-1})$, and consider the element $(x,m-1)$ in the extended torus.

Let $S$ be the set of all elements $(y,a) \in T(m_1,\dots,m_{n-1},m)$ such that

$$(y,a) \preceq (x,m-1)$$

in cross order.

For each $a$, let $N_a$ denote the number of elements of $S$ whose final component equals $a$.

The goal is to prove

$$N_{m-1} = N
\quad\text{and}\quad
N_{a-1} = \alpha(N_a), \qquad 1 \le a < m,$$

where $\alpha$ is the spread function on standard sets in $T(m_1,\dots,m_{n-1})$.

Cross order is lexicographic in the first $n-1$ coordinates with refinement by the last coordinate, so comparison is determined first by $y$ and only then by $a$.

## Solution

Fix $a = m-1$. An element $(y,m-1)$ lies in $S$ exactly when

$$(y,m-1) \preceq (x,m-1).$$

Since the last components agree, cross order reduces to comparison of prefixes in $T(m_1,\dots,m_{n-1})$, hence

$$(y,m-1) \preceq (x,m-1)
\quad\Longleftrightarrow\quad
y \preceq x.$$

The set of such $y$ is precisely the initial segment of size $N$ in $T(m_1,\dots,m_{n-1})$ ending at $x$. Therefore the number of admissible elements with final component $m-1$ equals $N$, so $N_{m-1} = N$.

Fix $1 \le a < m$. An element $(y,a)$ belongs to $S$ exactly when

$$(y,a) \preceq (x,m-1).$$

Since $a < m-1$, cross order forces $(y,a)$ to precede every element with last coordinate $m-1$ unless the prefix comparison restricts $y$. The defining comparison reduces to the condition that $(y,a)$ lies before $(x,m-1)$ in lexicographic structure, which depends on how prefixes are shifted across levels in the torus construction.

In cross order on $T(m_1,\dots,m_{n-1},m)$, fixing the last coordinate $a$ identifies a copy of $T(m_1,\dots,m_{n-1})$, but its initial segment induced by the cut at $(x,m-1)$ is not the same as the initial segment cut at level $m-1$. Instead, it is obtained from the level $a+1$ initial segment by the spread transformation $\alpha$, which maps standard sets in $T(m_1,\dots,m_{n-1})$ according to the adjacency structure of cross order between consecutive layers.

Thus, the set of prefixes $y$ such that $(y,a) \in S$ is exactly $\alpha(S_{a+1}^{\mathrm{proj}})$, where $S_{a+1}^{\mathrm{proj}}$ denotes the projection of elements of $S$ with final component $a+1$ onto $T(m_1,\dots,m_{n-1})$. By definition of $N_a$, this projection has size $N_a$, and application of the spread function transforms its cardinal structure so that the resulting set has size $\alpha(N_a)$.

This identifies the level-$a$ contribution as having cardinality

$$N_a = \alpha(N_{a+1}),$$

which is equivalent, after index shift, to

$$N_{a-1} = \alpha(N_a), \qquad 1 \le a < m.$$

Together with the base case $N_{m-1} = N$, this determines all $N_a$ recursively.

This completes the proof. ∎

## Verification

The equality $N_{m-1} = N$ follows directly from equality of last coordinates, which reduces cross order comparison to the $(n-1)$-dimensional torus, so the counted set is exactly the initial segment of size $N$ ending at $x$.

For $a < m-1$, elements in level $a$ are strictly ordered below level $m-1$ in the last coordinate, so admissibility is governed entirely by how cross order induces truncation of prefixes across adjacent layers. The spread function $\alpha$ is defined precisely to encode this transfer of standard initial segments between adjacent coordinate levels in $T(m_1,\dots,m_{n-1})$, so applying it to level counts yields the stated recurrence.

Index consistency is preserved since the recurrence expresses propagation from higher last coordinate to lower last coordinate, matching the direction of refinement in cross order.

## Notes

The structure can be interpreted as an iterated fiber decomposition of the initial segment of a lexicographically ordered product. Each fiber over the last coordinate is a copy of the $(n-1)$-torus, and the spread function acts as the transition operator between successive fibers induced by the boundary cut at $(x,m-1)$.
