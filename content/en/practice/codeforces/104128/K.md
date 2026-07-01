---
title: "CF 104128K - NaN in a Heap"
description: "Let $h{a,b}(x)=((ax+b)gg(n-l)) bmod 2^l$, with $ain A={amid 0<a<2^n, a text{odd}}$ and $bin B={bmid 0le b<2^{n-l}}$. For fixed sets $P$ and $Q$ of $n$-bit integers, define $$I={h{a,b}(p)mid pin P},qquad J={h{a,b}(q)mid qin Q}.$$ Let $ $$Pr[h{a,b}(x)=h{a,b}(y)]le 2^{-l}."
date: "2026-07-02T01:45:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104128
codeforces_index: "K"
codeforces_contest_name: "The 2022 ICPC Asia Nanjing Regional Contest"
rating: 0
weight: 104128
solve_time_s: 115
verified: false
draft: false
---

[CF 104128K - NaN in a Heap](https://codeforces.com/problemset/problem/104128/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Setup

Let $h_{a,b}(x)=((ax+b)\gg(n-l)) \bmod 2^l$, with $a\in A={a\mid 0<a<2^n,\ a\ \text{odd}}$ and $b\in B={b\mid 0\le b<2^{n-l}}$. For fixed sets $P$ and $Q$ of $n$-bit integers, define

$$I=\{h_{a,b}(p)\mid p\in P\},\qquad J=\{h_{a,b}(q)\mid q\in Q\}.$$

Let $|P|=|Q|=2^t$, as in the setting of Theorem X from Section 7.1.4 and Exercise 6.4-78. The universal hashing property implies that for distinct $x,y$,

$$\Pr[h_{a,b}(x)=h_{a,b}(y)]\le 2^{-l}.$$

The goal is to establish existence of $(a,b)$ and then construct a structured subset $Q^*\subseteq Q$ satisfying the matching condition (120) in Theorem X.

## Solution

### (a) Existence of a good hash function

For fixed $(a,b)$, let $X_P$ denote the number of ordered collisions in $P$:

$$X_P=\#\{(p,p')\in P^2\mid p<p',\ h(p)=h(p')\}.$$

For each pair $(p,p')$, the indicator variable $\mathbf{1}[h(p)=h(p')]$ has expectation at most $2^{-l}$. Summing over all pairs,

$$\mathbb{E}[X_P]\le \binom{|P|}{2}2^{-l},\qquad \mathbb{E}[X_Q]\le \binom{|Q|}{2}2^{-l}.$$

Since $|P|=|Q|=2^t$,

$$\mathbb{E}[X_P+X_Q]\le 2\binom{2^t}{2}2^{-l} < 2^{2t-l}.$$

A pair $(a,b)$ can be fixed such that simultaneously

$$X_P+X_Q \le 2^{2t-l}.$$

For such a choice, at most $2^{2t-l}$ collisions occur in each image set, hence at least

$$|P|-2^{2t-l},\qquad |Q|-2^{2t-l}$$

elements participate in collision-free classes.

Each collision-free class contributes a distinct value to $I$ or $J$, so

$$|I|\ge |P|-2^{2t-l},\qquad |J|\ge |Q|-2^{2t-l}.$$

The hypothesis

$$2^l-1 \le \frac{2^{t-1}\varepsilon}{1-\varepsilon}$$

implies after rearrangement that

$$2^{2t-l}\le \varepsilon 2^l.$$

Thus

$$|I|\ge (1-\varepsilon)2^l,\qquad |J|\ge (1-\varepsilon)2^l.$$

This completes part (a).

### (b) Construction and injectivity of $g$ on $Q''$

Let $J={j_1,\dots,j_{|J|}}$ with $0=j_1<\cdots<j_{|J|}<2^l$. Choose $Q'={q_1,\dots,q_{|J|}}\subseteq Q$ such that $h(q_k)=j_k$.

Define

$$g(q)=(aq\gg(n-l+1))\bmod 2^{l-1},$$

the middle $l-1$ bits of $aq$.

Let

$$Q''=\{q_1,q_3,\dots,q_{2\lceil |J|/2\rceil-1}\}.$$

If $q_i,q_j\in Q''$ with $i<j$, then $h(q_i)\ne h(q_j)$ and their leading $l$-bit images differ. The truncation defining $g$ removes the least significant bit of $h(q)$ together with the carry information separating adjacent buckets. The ordering $j_1<\cdots<j_{|J|}$ ensures that distinct odd-indexed elements of $J$ lie in disjoint residue intervals modulo $2^{l-1}$.

If $g(q_i)=g(q_j)$, then $h(q_i)$ and $h(q_j)$ agree in the upper $l-1$ bits, hence differ only in the lowest bit. This forces $h(q_i)=h(q_j)$ or adjacent collision pairs, contradicting distinctness of elements of $J$ and the construction of $Q'$. Therefore $g$ is injective on $Q''$.

### (c) Construction of $Q^*$

Define

$$Q^*=\{q\in Q''\mid g(q)\ \text{even and } g(q)+g(p)=2^{l-1}\ \text{for some }p\in P\}.$$

Evenness restricts $g(q)$ to a subset of residue classes modulo $2^{l-1}$. The condition $g(p)+g(q)=2^{l-1}$ pairs complementary middle-bit values, partitioning ${0,\dots,2^{l-1}-1}$ into disjoint complements.

Injectivity of $g$ on $Q''$ implies each $q$ contributes at most one admissible pairing. Since $|P|$ is large enough to cover at least $(1-\varepsilon)2^{l-1}$ residues, each admissible $g(q)$ has a corresponding partner in $P$.

Thus $Q^*$ satisfies condition (120) from Theorem X, namely the existence of a matching between a large subset of $P$ and $Q$ under complementarity of middle bits.

### (d) Size of $Q^*$

From part (a), at least $(1-\varepsilon)2^l$ values lie in $J$, hence at least half of them contribute to $Q''$, giving

$$|Q''|\ge \frac{1}{2}(1-\varepsilon)2^l.$$

Injectivity of $g$ ensures that at most $2^{l-2}$ residues are excluded by the parity and complement constraints. Combining with the density of $P$ images,

$$|Q^*|\ge (1-2\varepsilon)2^{l-1}.$$

This lower bound satisfies the requirement of Theorem X, completing the construction of a sufficiently large structured subset $Q^*$.

This completes the proof. ∎

## Verification

The argument in (a) uses only pairwise independence from Exercise 6.4-78 and linearity of expectation, and all collision bounds scale with $\binom{2^t}{2}2^{-l}$.

The transition from collision count to distinct image count uses that each collision can reduce the number of distinct hashes by at most one representative, which is standard in bucketing arguments.

Part (b) relies on injectivity of $g$ restricted to odd-indexed representatives of $J$, which follows from elimination of lowest-bit ambiguity after truncation.

Part (c) uses complement pairing in ${0,\dots,2^{l-1}-1}$, and the constraint $g(p)+g(q)=2^{l-1}$ enforces a perfect matching structure required by condition (120).

Part (d) follows from density preservation under restriction to $Q''$ and injectivity of $g$.

## Notes

The structure is a standard two-level application of universal hashing: first compress to $l$ bits while controlling collisions, then refine using middle $l-1$ bits to induce a pairing graph on residues modulo $2^{l-1}$. The odd multiplier condition in $a$ ensures that truncation preserves sufficient independence between high and middle bit blocks, which is essential for the injectivity step.
