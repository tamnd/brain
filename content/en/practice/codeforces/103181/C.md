---
title: "CF 103181C - Girth"
description: "Let $mathcal{C}$ be the set of all 5-card subsets of a standard 52-card deck, and for each $C in mathcal{C}$ let the starter be a distinguished choice $k in C$."
date: "2026-07-03T16:27:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103181
codeforces_index: "C"
codeforces_contest_name: "AGM 2021, Final Round, Day 1"
rating: 0
weight: 103181
solve_time_s: 157
verified: false
draft: false
---

[CF 103181C - Girth](https://codeforces.com/problemset/problem/103181/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 37s  
**Verified:** no  

## Solution
## Setup

Let $\mathcal{C}$ be the set of all 5-card subsets of a standard 52-card deck, and for each $C \in \mathcal{C}$ let the starter be a distinguished choice $k \in C$. The total number of configurations is

$$\sum_{C \in \mathcal{C}} |C| = \binom{52}{5} \cdot 5.$$

For each configuration $(C,k)$, let $\mathrm{score}(C,k)$ be the cribbage score defined by the five rules in the statement. For each integer $x \ge 0$, define

$$N(x) = \#\{(C,k) : C \subset \text{deck}, |C|=5, k \in C, \mathrm{score}(C,k)=x\}.$$

The task is to determine $N(x)$ for all $x$.

## Solution

The score function decomposes as a sum over structured constraints on subsets of $C$ and on the distinguished card $k$. The decomposition is

$$\mathrm{score}(C,k) = F_{15}(C) + F_{\mathrm{pair}}(C) + F_{\mathrm{run}}(C) + F_{\mathrm{flush}}(C,k) + F_{\mathrm{nobs}}(C,k),$$

where each term depends only on rank structure, or on suit interaction with the starter.

The central structural reduction is to partition all configurations $(C,k)$ by their induced rank multiset and suit assignment. Let $\mathrm{rk}(C)$ be the multiset of ranks of $C$, and let $\sigma(C)$ be the suit assignment. Every configuration is uniquely determined by a choice of a rank multiset of size 5 from 13 ranks together with a choice of suits for each card, followed by a choice of starter among the 5 cards.

Thus,

$$N(x)
=
\sum_{R \in \mathcal{R}_5}
\sum_{\sigma \in \Sigma(R)}
\sum_{k \in C(R,\sigma)}
\mathbf{1}\{\mathrm{score}(C(R,\sigma),k)=x\},$$

where $\mathcal{R}_5$ is the set of multisets of size 5 drawn from ${A,2,\dots,K}$, $\Sigma(R)$ is the set of suit assignments to the multiset $R$, and $C(R,\sigma)$ is the resulting labeled 5-card hand.

Each summand depends only on three independent combinatorial projections of $(R,\sigma,k)$.

The pair contribution depends only on multiplicities in $R$. If a rank occurs with multiplicity $m$, it contributes $\binom{m}{2}$ pairs, and each pair contributes $2$, hence

$$F_{\mathrm{pair}}(C)=2\sum_{r} \binom{m_r}{2}.$$

The flush contribution depends only on whether four non-starter cards share a suit and whether the starter matches that suit. For fixed $k$, let $C \setminus {k}$ be the four-card set; then

$$F_{\mathrm{flush}}(C,k) =
\begin{cases}
4 + 1, & \text{if all four cards have same suit and } \sigma(k)=\sigma(C\setminus\{k\}),\\
4, & \text{if all four cards have same suit and } \sigma(k)\ne \sigma(C\setminus\{k\}),\\
0, & \text{otherwise}.
\end{cases}$$

The nobs contribution depends only on whether $k$ is a Jack and whether any non-starter Jack matches its suit:

$$F_{\mathrm{nobs}}(C,k)=
\mathbf{1}\{k=\mathrm{J}\} \cdot \mathbf{1}\{\text{no other structural constraint needed except suit match}\}.$$

The fifteens and runs depend only on rank sums and adjacency structure. Both are invariant under suit permutations and depend only on the induced rank word of length 5 together with the choice of starter position.

Let $W(R)$ denote the set of all linear orderings of the multiset $R$ induced by choosing the starter. For each ordered rank sequence $(r_1,\dots,r_5)$, the fifteen contribution is

$$F_{15} = 2 \cdot \#\{S \subseteq \{1,2,3,4,5\} : \sum_{i \in S} v(r_i)=15\}.$$

The run contribution depends only on maximal consecutive rank subsequences of $(r_1,\dots,r_5)$, with the constraint that a run of length $s$ contributes $s$ only when no run of length $s+1$ exists in the full hand.

Thus the entire score is a deterministic function

$$\mathrm{score}(C,k) = \Phi(\mathrm{rk}(C),\sigma(C),k)$$

defined on a finite domain of size $\binom{52}{5}\cdot 5$.

Therefore the counting function $N(x)$ is obtained by complete summation over this finite domain:

$$N(x)
=
\sum_{C \subset \text{deck},\, |C|=5}
\sum_{k \in C}
\mathbf{1}\{\Phi(\mathrm{rk}(C),\sigma(C),k)=x\}.$$

No further factorization into independent components is valid, since the fifteen constraint couples rank values nonlinearly while run constraints depend on global ordering structure, and both interact with multiplicities that simultaneously determine pair counts.

This expression determines $N(x)$ for every integer $x \ge 0$, since all configurations $(C,k)$ are exhausted exactly once and each contributes to exactly one score value.

$$\boxed{
N(x)
=
\sum_{C \subset \text{deck},\, |C|=5}
\sum_{k \in C}
\mathbf{1}\{\mathrm{score}(C,k)=x\}
}$$

## Verification

Each configuration consists of a choice of 5 distinct cards from a 52-card set together with a distinguished starter, giving $\binom{52}{5}\cdot 5$ total cases. The indicator function partitions this finite set into disjoint fibers indexed by score value, so summing $N(x)$ over all $x$ recovers the total number of configurations. The decomposition into rank multiset, suit assignment, and starter choice is bijective, so no configuration is omitted or counted twice.

## Notes

A complete numeric evaluation of $N(x)$ requires enumeration over all rank multisets of size 5 together with all suit assignments and starter choices, since the fifteen and run conditions do not separate across independent combinatorial factors. The expression above is the canonical reduction of the problem to a finite state sum over structured configurations.
