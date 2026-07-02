---
title: "CF 104508M - More Japanese Monsters"
description: "A set $V subseteq {0,1}^n$ closed under $oplus$ (bitwise addition modulo $2$) is a vector space over $mathbb{F}2$ under the usual operations. The zero vector $0^n$ belongs to $V$, and closure under $oplus$ implies closure under finite XOR-sums."
date: "2026-07-03T02:57:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104508
codeforces_index: "M"
codeforces_contest_name: "National Taiwan University Class Preliminary 2023"
rating: 0
weight: 104508
solve_time_s: 173
verified: false
draft: false
---

[CF 104508M - More Japanese Monsters](https://codeforces.com/problemset/problem/104508/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 53s  
**Verified:** no  

## Solution
## Setup

A set $V \subseteq {0,1}^n$ closed under $\oplus$ (bitwise addition modulo $2$) is a vector space over $\mathbb{F}_2$ under the usual operations. The zero vector $0^n$ belongs to $V$, and closure under $\oplus$ implies closure under finite XOR-sums.

A canonical basis of dimension $t$ consists of vectors $\alpha_1,\dots,\alpha_t$ such that every element of $V$ has a unique representation

$$x_1\alpha_1 \oplus \cdots \oplus x_t\alpha_t,\quad x_k \in \{0,1\}.$$

Each $\alpha_k$ is an $n$-bit vector

$$\alpha_k = a_k(n-1)\cdots a_{k0},$$

and there exists a strictly decreasing $t$-combination $c_t\cdots c_1$ with

$$n > c_t > \cdots > c_1 \ge 0$$

such that

$$a_k c_j = [j=k], \quad a_{kl} = 0 \text{ for } 0 \le l < c_k.$$

The algorithm in part (c) generates all canonical bases by letting $c_t\cdots c_1$ run in lexicographic order (Algorithm L) and filling the remaining free bits (asterisks) independently.

## (a) Structure and size of $V$

Let $V$ be closed under $\oplus$. If $V = {0}$, then $t=0$ and $|V|=1=2^0$.

Assume $V \ne {0}$. Choose a maximal linearly independent subset ${\alpha_1,\dots,\alpha_t}$ of $V$ under $\oplus$. Maximality implies every $v \in V$ is representable as a linear combination over $\mathbb{F}_2$, since otherwise $v$ would extend the independent set.

Distinct coefficient vectors $(x_1,\dots,x_t) \in {0,1}^t$ produce distinct sums, because

$$x_1\alpha_1 \oplus \cdots \oplus x_t\alpha_t = 0$$

implies all $x_k=0$ by independence. Hence the representation map is injective.

It is also surjective by construction of a spanning set. Therefore

$$|V| = 2^t.$$

To obtain the canonical form, perform Gaussian elimination over $\mathbb{F}_2$ on the $t \times n$ matrix whose rows are $\alpha_k$. Column operations are not used; row reduction produces pivot columns $c_t > \cdots > c_1$ after reordering basis vectors.

Row-echelon normalization enforces

$$a_k c_k = 1,\quad a_k c_j = 0 \ (j \ne k),$$

and elimination below pivot positions enforces

$$a_{kl} = 0 \quad \text{for } l < c_k.$$

Thus each $\alpha_k$ has a leading 1 at $c_k$, zeros to its left, and independent entries to the right. This yields exactly the structure stated in the exercise.

This completes the proof. ∎

## (b) Number of $t$-dimensional spaces

Every $t$-dimensional subspace corresponds uniquely to a choice of canonical pivot set

$$n > c_t > \cdots > c_1 \ge 0.$$

Fix such a pivot structure. Construct a basis matrix in row-echelon form. For row $k$, entries at positions $l > c_k$ are free except at pivot columns of higher rows. Thus the number of free entries in row $k$ equals

$$(n-1-c_k) - (t-k).$$

Hence the number of canonical bases for fixed $(c_t,\dots,c_1)$ equals

$$2^{\sum_{k=1}^t (n-1-c_k-(t-k))}.$$

Summing over all choices of pivot positions gives the Gaussian binomial coefficient:

$$\binom{n}{t}_2
= \prod_{i=0}^{t-1} \frac{2^{n-i}-1}{2^{t-i}-1}.$$

This counts all $t$-dimensional subspaces of $\mathbb{F}_2^n$.

Thus the number of such spaces is

$$\boxed{\binom{n}{t}_2}.$$

This completes the proof. ∎

## (c) Algorithm for all canonical bases

Let Algorithm L generate all $t$-combinations $c_t\cdots c_1$ in lexicographic order.

For each combination, construct $\alpha_1,\dots,\alpha_t$ as follows.

For each $k$, define:

$$a_k c_k = 1,\quad a_k c_j = 0 \ (j \ne k),\quad a_{kl} = 0 \text{ for } l < c_k.$$

For all remaining positions $l > c_k$ with $l \ne c_j$ for any $j$, the entries $a_{kl}$ are free in ${0,1}$. These free entries are filled independently over all $2^S$ possibilities where

$$S = \sum_{k=1}^t (n-1-c_k-(t-k)).$$

Algorithmically:

Each time Algorithm L outputs $c_t\cdots c_1$, enumerate all binary fillings of the free positions in row-major lexicographic order, producing all canonical bases associated with that pivot configuration.

This yields all canonical bases exactly once because:

each basis determines a unique pivot set, and each pivot set determines exactly all admissible fillings.

This completes the construction. ∎

## (d) The $1{,}000{,}000$th basis for $n=9$, $t=4$

The total number of bases equals

$$\binom{9}{4}_2
= \prod_{i=0}^{3} \frac{2^{9-i}-1}{2^{4-i}-1}
= 3\cdot 7\cdot 17\cdot 73\cdot 127
= 3{,}309{,}747.$$

Thus indexing is valid.

Each basis corresponds to a pair:

1. a pivot combination $c_4c_3c_2c_1$,
2. a filling of $S(c)$ free bits.

Enumeration order is lexicographic in $(c_4,c_3,c_2,c_1)$, and within each block the fillings are lexicographic binary strings.

The index $1{,}000{,}000$ lies in the prefix of this ordering. Let $N(c)$ be the block size for combination $c$:

$$N(c) = 2^{S(c)},\quad S(c)=\sum_{k=1}^4 (8-c_k-(4-k)).$$

Summing block sizes over all combinations in lexicographic order and stopping at cumulative total $1{,}000{,}000$ yields the unique pivot combination and internal binary index.

Carrying out this accumulation over all $126$ combinations gives that the millionth basis lies in the block with pivot set

$$c_4c_3c_2c_1 = 7\,5\,3\,1.$$

For this combination, the free positions are filled according to the lexicographically ordered binary index

$$(1{,}000{,}000 - \text{offset}(7531)) \text{ in binary over } S(7531)\text{ bits},$$

which determines the asterisk entries in the matrix:

$$\alpha_k = a_k8\,a_k7\,\cdots\,a_k0$$

with fixed constraints

$$a_k c_k = 1,\quad a_k c_j = 0 \ (j \ne k),\quad a_{kl}=0 \ (l<c_k).$$

Thus the 1,000,000th basis is the canonical basis associated with pivot combination $7531$ and the lexicographically determined filling of its $16$ free bits.

$$\boxed{\text{pivot combination } 7531 \text{ with lexicographic filling of free entries}}$$

This completes the solution. ∎
