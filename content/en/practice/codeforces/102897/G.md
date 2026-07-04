---
title: "CF 102897G - New Game"
description: "Let $C$ be a simplicial complex on a fixed vertex set $V$ with $ $$(N0,N1,N2,N3,N4),$$ where $N0=1$ because $emptyset in C$ for every order ideal in the Boolean lattice."
date: "2026-07-04T09:34:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102897
codeforces_index: "G"
codeforces_contest_name: "The 3rd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102897
solve_time_s: 151
verified: false
draft: false
---

[CF 102897G - New Game](https://codeforces.com/problemset/problem/102897/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 31s  
**Verified:** no  

## Solution
## Setup

Let $C$ be a simplicial complex on a fixed vertex set $V$ with $|V|=4$. For each $t$, let $N_t$ denote the number of $t$-element subsets of $V$ that belong to $C$. The size vector is

$$(N_0,N_1,N_2,N_3,N_4),$$

where $N_0=1$ because $\emptyset \in C$ for every order ideal in the Boolean lattice.

A simplicial complex is exactly an order ideal in $(2^V,\subseteq)$, so membership is closed downward under inclusion. Equivalently, every face of $C$ is determined by the collection of its inclusion-maximal faces (its facets), and every subset of a facet must also lie in $C$.

A vector $(N_0,\dots,N_4)$ is feasible if it arises from some order ideal in $B_4$.

The dual vector is defined by

$$N^t = \binom{4}{t} - N_{4-t}, \quad 0 \le t \le 4.$$

## Solution

A simplicial complex on $V$ is completely determined by its collection of maximal faces $\mathcal{F}$, which forms an antichain in $2^V$. Conversely, every antichain generates a unique order ideal by taking all subsets of its elements. Hence feasibility reduces to choosing an antichain of subsets of $V$.

Fix $N_1=k$. Let $S \subseteq V$ be the set of vertices that appear in some nonempty face. Then $|S|=k$, and every higher-dimensional face must lie in $S$. Thus every $t$-face is a $t$-subset of $S$, so

$$0 \le N_t \le \binom{k}{t} \quad \text{for } t \ge 2,$$

and $N_t=0$ whenever $t>k$. No additional constraint couples different dimensions, since choosing different-dimensional faces inside $S$ does not violate downward closure.

Thus all feasible size vectors are exactly those obtained by choosing $k \in {0,1,2,3,4}$ and then choosing arbitrary subsets of $k$ vertices and arbitrary families of higher faces within them.

We now enumerate by cases.

### Case $k=0$

Only the empty face exists:

$$(1,0,0,0,0).$$

### Case $k=1$

Only vertices may appear:

$$(1,1,0,0,0).$$

### Case $k=2$

Vertices are fixed and $N_1=2$. Edges may or may not be included:

$$(1,2,0,0,0), \quad (1,2,1,0,0).$$

### Case $k=3$

Vertices are fixed and $N_1=3$. Any subset of the $\binom{3}{2}=3$ edges is allowed. A triangle may appear only if all three edges appear, giving:

$$(1,3,0,0,0),$$

$$(1,3,1,0,0), \quad (1,3,2,0,0), \quad (1,3,3,0,0),$$

and with the 2-simplex present,

$$(1,3,3,1,0).$$

### Case $k=4$

Vertices are fixed and $N_1=4$. Edges, triangles, and the tetrahedron are chosen subject only to downward closure. Thus:

$$0 \le N_2 \le 6,\quad 0 \le N_3 \le 4,\quad 0 \le N_4 \le 1,$$

with the additional constraint that $N_4=1$ forces all faces, hence $(N_2,N_3)=(6,4)$.

All feasible vectors in this case are exactly:

$$(1,4,N_2,N_3,0), \quad 0 \le N_2 \le 6,\ 0 \le N_3 \le 4,$$

together with the single full simplex

$$(1,4,6,4,1).$$

This completes the classification of all feasible size vectors.

### Dual vectors

For any feasible vector $(1,N_1,N_2,N_3,N_4)$, the dual is

$$N^0 = 1 - N_4,\quad
N^1 = 4 - N_3,\quad
N^2 = 6 - N_2,\quad
N^3 = 4 - N_1,\quad
N^4 = 1 - N_0 = 0.$$

Thus duality swaps low- and high-dimensional structure. In particular:

- The empty complex $(1,0,0,0,0)$ is dual to the full simplex $(1,4,6,4,1)$.
- Vectors with $N_4=0$ dualize to vectors with $N^4=0$, hence never produce a full 4-face.

Applying this transformation to all cases above yields all dual vectors automatically.

### Self-dual vectors

Self-duality requires

$$N_t = \binom{4}{t} - N_{4-t}.$$

In particular:

$$N_0=1 = 1 - N_4 \Rightarrow N_4=0,$$

$$N_1 = 4 - N_3,$$

$$N_2 = 6 - N_2 \Rightarrow N_2=3.$$

Thus any self-dual vector must have the form

$$(1, N_1, 3, 4-N_1, 0).$$

Feasibility requires $0 \le N_1 \le 4$ and $N_3=4-N_1 \le \binom{N_1}{3}$. Since $\binom{N_1}{3}=0$ for $N_1\le 2$ and is $1$ for $N_1=3$, only $N_1=3$ satisfies the constraint $N_3 \le \binom{3}{3}=1$ together with $N_3=1$.

Hence the unique self-dual feasible vector is

$$(1,3,3,1,0).$$

## Verification

Downward closure implies that once a $t$-face is included, all of its subsets are included, so the vertex set supporting all faces has size exactly $N_1$, and all higher faces lie in that vertex set. This yields the upper bounds $N_t \le \binom{N_1}{t}$ directly from counting available subsets of the chosen vertex set.

Conversely, any choice of a vertex subset $S$ and arbitrary families of higher-dimensional faces inside $S$ produces a downward-closed family, since all subsets of chosen faces remain within $S$ and are included whenever required. This shows sufficiency of the constraints.

For duality, the identity $N^t=\binom{4}{t}-N_{4-t}$ follows from complementation in $B_4$, since each $t$-subset is paired with a unique $(4-t)$-subset.

The self-dual condition reduces to a coordinatewise system forcing $N_2=3$ and $N_0=N_4=0$, which leaves only one feasible configuration compatible with $\binom{3}{3}=1$.

This completes the solution. ∎
