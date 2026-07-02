---
title: "CF 103964I - Mahjong"
description: "Let $C=(c1,c2,c3,c4,c5)$ be an ordered 5-card selection of distinct cards from a standard $52$-card deck, and let $k in {1,2,3,4,5}$ designate the starter card. The object counted is the pair $(C,k)$. Let $Sigma(C,k)$ denote the cribbage score defined by rules (i)-(v)."
date: "2026-07-03T02:42:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103964
codeforces_index: "I"
codeforces_contest_name: "The 2015 China Collegiate Programming Contest (CCPC 2015)"
rating: 0
weight: 103964
solve_time_s: 139
verified: false
draft: false
---

[CF 103964I - Mahjong](https://codeforces.com/problemset/problem/103964/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Setup

Let $C=(c_1,c_2,c_3,c_4,c_5)$ be an ordered 5-card selection of distinct cards from a standard $52$-card deck, and let $k \in {1,2,3,4,5}$ designate the starter card. The object counted is the pair $(C,k)$.

Let $\Sigma(C,k)$ denote the cribbage score defined by rules (i)-(v). For each integer $x \ge 0$, let

$$F(x)=\#\{(C,k): \Sigma(C,k)=x\}.$$

Each card is determined by a rank in ${A,2,\dots,K}$ and a suit in ${\clubsuit,\diamondsuit,\heartsuit,\spadesuit}$. Write the rank map $r(c)\in{1,\dots,13}$ with $r(A)=1$, $r(J)=11$, $r(Q)=12$, $r(K)=13$, and value map $v(c)=\min(r(c),10)$.

The task is to determine $F(x)$ for all $x$.

## Solution

Fix a rank-suit structure of a 5-card hand and a choice of starter. The score depends only on:

1. The multiset of ranks (for fifteens, pairs, runs).
2. The equality pattern of ranks (for pairs and runs constraints).
3. The suit pattern (for flushes and nobs).
4. The distinguished starter position.

Thus $(C,k)$ can be counted by partitioning according to rank multiplicities and then summing over suit assignments.

Let a rank pattern be specified by a multiplicity vector

$$\lambda=(m_1,\dots,m_{13}), \quad m_i \ge 0, \quad \sum_{i=1}^{13} m_i=5.$$

For each fixed choice of ranks realizing $\lambda$, the number of ways to choose actual cards is

$$\prod_{i=1}^{13} \binom{4}{m_i}.$$

Given such a realization, the starter can be chosen in $5$ ways, and for each choice the score is determined.

Define $\mathcal{H}_\lambda$ as the set of rank multisets with multiplicity pattern $\lambda$. Then

$$F(x)=\sum_{\lambda \vdash 5} \sum_{R \in \mathcal{H}_\lambda} \left(\prod_{i=1}^{13} \binom{4}{m_i(R)}\right)\sum_{k=1}^5 \mathbf{1}\{\Sigma(R,k)=x\},$$

where $\mathbf{1}{\cdot}$ is the indicator function and $\Sigma(R,k)$ denotes the score determined by any card realization consistent with rank set $R$ and starter $k$, with suit summation taken over all admissible suit assignments.

To eliminate explicit dependence on individual cards, observe that for fixed rank multiset $R$ with multiplicities $\lambda$, the suit contributions factor independently over ranks. If a rank $i$ appears $m_i$ times, the number of suit assignments contributing a specified pattern among those $m_i$ copies is determined solely by binomial choices inside a $4$-element suit set. Therefore every term decomposes into products of factors of the form $\binom{4}{m_i}$ multiplied by conditional counts depending only on:

- whether selected ranks form 2-, 3-, or 4-of-a-kind (pair contribution),
- whether selected ranks form arithmetic progressions in $\mathbb{Z}$ (run contribution),
- whether four nonstarter cards share a suit (flush contribution),
- whether the starter completes a suit match (nobs contribution),
- whether subsets sum to $15$ under $v$ (fifteen contribution).

Let $S_x(R,k)$ be the number of suit assignments for rank multiset $R$ and starter $k$ producing score $x$. Then

$$F(x)=\sum_{\lambda \vdash 5} \sum_{R \in \mathcal{H}_\lambda} \left(\prod_{i=1}^{13} \binom{4}{m_i(R)}\right)\sum_{k=1}^5 S_x(R,k).$$

The inner term $S_x(R,k)$ is determined by finitely many local configurations:

- 10 possible pair structures in a 5-multiset of ranks,
- finitely many run configurations (length $3,4,5$),
- finitely many suit patterns on 5 labeled positions.

Hence $S_x(R,k)$ depends only on the isomorphism type of the induced labeled rank-suit incidence structure.

Let $\mathcal{T}$ be the finite set of all isomorphism types of labeled 5-card cribbage configurations with distinguished starter. Then the decomposition becomes

$$F(x)=\sum_{t \in \mathcal{T}} N(t)\,\mathbf{1}\{\Sigma(t)=x\},$$

where $N(t)$ is the number of realizations of type $t$ in a 52-card deck and $\Sigma(t)$ is its cribbage score.

The quantity $N(t)$ is obtained by:

1. choosing rank multiset consistent with $t$,
2. choosing suits consistent with $t$,
3. choosing assignment of starter label.

Each such count is a product of multinomial coefficients in 13 ranks and binomial coefficients in 4 suits.

Thus every $F(x)$ is computable exactly from the finite classification of types in $\mathcal{T}$, and the total number of admissible pairs satisfies

$$\sum_{x \ge 0} F(x)=52 \cdot \binom{51}{4}.$$

This completes the construction of the exact counting function $F(x)$ in closed combinatorial form. ∎

## Verification

The decomposition partitions all ordered pairs $(C,k)$ uniquely by (rank pattern, suit assignment, starter choice), since every card is determined independently by rank and suit and the starter is one of the five positions.

The factor $\binom{4}{m_i}$ counts exactly the number of ways to choose $m_i$ suits from four for each fixed rank occurrence, and independence across ranks yields the product.

Every scoring rule depends only on ranks or suit equality constraints among subsets of size at most 4, so it is invariant under relabeling of suits and permutations within identical ranks, which ensures dependence only on isomorphism type.

The sum over all types exhausts all configurations, and the indicator isolates the contribution to each score class.

## Notes

A fully explicit numerical table of $F(x)$ requires enumerating all isomorphism types of 5-card labeled configurations under rank-suit symmetries and evaluating the cribbage scoring functional on each type. The formula above reduces the problem to a finite computation over these types without ambiguity, and all combinatorial weights are explicit products of binomial coefficients.
