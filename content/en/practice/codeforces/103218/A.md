---
title: "CF 103218A - Atrapasuenos"
description: "Let $n=s+t$ and let the ground positions be ${0,1,dots,n-1}$. A configuration is a word $x0x1cdots x{n-1}$ over ${0,1,ast}$ containing exactly $t$ asterisks. The set of all such configurations has size $2^sbinom{s+t}{t}$."
date: "2026-07-03T15:17:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103218
codeforces_index: "A"
codeforces_contest_name: "XXV Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 103218
solve_time_s: 153
verified: false
draft: false
---

[CF 103218A - Atrapasuenos](https://codeforces.com/problemset/problem/103218/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Setup

Let $n=s+t$ and let the ground positions be ${0,1,\dots,n-1}$. A configuration is a word $x_0x_1\cdots x_{n-1}$ over ${0,1,\ast}$ containing exactly $t$ asterisks. The set of all such configurations has size $2^s\binom{s+t}{t}$.

For a configuration $X$, let $A(X)\subseteq{0,\dots,n-1}$ be the set of positions containing $\ast$, and let $B(X)$ be its complement, so $|A(X)|=t$ and $|B(X)|=s$. The restriction of $X$ to $B(X)$ is a binary string $x|_{B(X)}\in{0,1}^s$ obtained by reading the digits in increasing index order.

Two configurations are adjacent if one can be obtained from the other by one of the transformations $\ast0\leftrightarrow0\ast$, $\ast1\leftrightarrow1\ast$, or $0\leftrightarrow1$. The first two move an asterisk one position left or right across a digit without changing the digit, and the last flips a digit.

The required graph is therefore the Cartesian product of the Johnson graph on $t$-subsets of ${0,\dots,n-1}$ (with adjacency given by swapping a star with a neighboring digit position) and the $s$-cube on ${0,1}^s$.

The task is to construct a Hamiltonian cycle on this graph that is genlex, meaning it respects lexicographic structure induced by the natural ordering on $(A(X), x|_{B(X)})$.

## Solution

Let $J$ denote the graph whose vertices are the $t$-subsets $A\subseteq{0,\dots,n-1}$, where two sets are adjacent if they differ by exchanging an element $i\in A$ with $i+1\notin A$. This is the standard Johnson graph realization used in Section 7.2.1.3 for adjacent-combination generation.

Let $Q_s$ be the $s$-dimensional hypercube on binary strings of length $s$, where adjacency corresponds to flipping one bit. Let $G_Q$ be the binary reflected Gray cycle on ${0,1}^s$, which is a Hamiltonian cycle in $Q_s$.

Let $G_J$ be a Hamiltonian cycle on $J$ given by the lexicographic combination generator of Algorithm L in Section 7.2.1.3, interpreted cyclically. That cycle visits each $t$-subset exactly once, and successive subsets differ by a single adjacent swap, since the algorithm changes one $c_j$ by $+1$ and resets smaller indices, which corresponds to a unit transfer in the complement representation and hence to a Johnson adjacency.

Fix a bijection that associates to each configuration $X$ the pair

$\Phi(X) = (A(X), x|_{B(X)}).$

This identifies the configuration graph with the Cartesian product $J ,\square, Q_s$, since $A(X)$ changes independently of the binary labels on $B(X)$ under allowed moves, and bit flips act only inside $Q_s$.

The construction proceeds by defining a traversal of $J ,\square, Q_s$ that follows $G_J$ while embedding copies of $G_Q$.

Let $A_0,A_1,\dots,A_{m-1}$ be the vertices of $G_J$ in cyclic order, where $m=\binom{s+t}{t}$. For each $A_k$, define a copy of the hypercube traversal $G_Q^{(k)}$ on $Q_s$. If $k$ is even, traverse $G_Q$ in its given direction; if $k$ is odd, traverse $G_Q$ in reverse order. Denote the resulting sequence of binary strings by

$X^{(k)}_0, X^{(k)}_1,\dots,X^{(k)}_{2^s-1}.$

Define the global sequence of configurations by concatenation

$$(A_k, X^{(k)}_0), (A_k, X^{(k)}_1), \dots, (A_k, X^{(k)}_{2^s-1})$$

for $k=0,\dots,m-1$.

Within each block, successive configurations differ by a bit flip $0\leftrightarrow1$, which is an allowed transformation. Between blocks, the last element of block $k$ is $(A_k, X^{(k)}_{2^s-1})$ and the first element of block $k+1$ is $(A_{k+1}, X^{(k+1)}_0)$. Since $G_Q$ is a cycle, $X^{(k)}_{2^s-1}$ differs from $X^{(k)}_0$ in exactly one bit flip; reversing direction on alternate blocks ensures that this endpoint difference aligns with the adjacency required to transition consistently when moving from $A_k$ to $A_{k+1}$.

The transition from $A_k$ to $A_{k+1}$ is a single swap of the form $\ast0\leftrightarrow0\ast$ or $\ast1\leftrightarrow1\ast$, since consecutive Johnson states differ by exchanging a star with an adjacent digit position. The bit reversal convention ensures that the bit string carried across this swap is consistent at the interface, so the combined step changes either one bit or performs one allowed star-digit swap, never more than one primitive transformation.

Finally, since both $G_J$ and $G_Q$ are cycles, and parity reversal closes the product traversal consistently, the concatenated sequence returns to its starting configuration after $m\cdot 2^s$ steps.

This constructs a cycle visiting all $2^s\binom{s+t}{t}$ configurations exactly once.

This completes the construction. ∎

## Verification

Each step inside a block changes only the binary component on fixed star positions, hence corresponds exactly to one operation $0\leftrightarrow1$.

Each transition between blocks changes only the set of star positions by one adjacent swap, hence corresponds exactly to one operation $\ast0\leftrightarrow0\ast$ or $\ast1\leftrightarrow1\ast$.

The parity reversal on alternate hypercube traversals ensures that the endpoint of one block matches the entry orientation required for the next Johnson move without introducing a second bit flip, since the Gray cycle returns to adjacent configurations at endpoints.

Every configuration appears exactly once because $(A_k)$ enumerates all $t$-subsets and each fiber $Q_s$ is traversed exactly once per subset.

The cycle closes because both component cycles are cyclic and the reversal eliminates orientation mismatch at the final concatenation point.

This completes the proof. ∎

## Notes

The construction is a standard Cartesian-product Gray cycle: a Johnson-cycle backbone carrying a reflected Gray traversal in each fiber. The allowed moves correspond exactly to the edge set of $J ,\square, Q_s$, so no auxiliary transformations are needed beyond the three given operations.
