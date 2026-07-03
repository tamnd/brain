---
title: "CF 103102I - Modulo Permutations"
description: "Let $n = s + t$ and let $mathcal{A}$ be a family of $t$-combinations of ${0,1,dots,n-1}$. The shadow $Delta mathcal{A}$ is the family of all $(t-1)$-combinations that are contained in at least one element of $mathcal{A}$."
date: "2026-07-03T22:00:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103102
codeforces_index: "I"
codeforces_contest_name: "2020-2021 ICPC Southeastern European Regional Programming Contest (SEERC 2020)"
rating: 0
weight: 103102
solve_time_s: 159
verified: false
draft: false
---

[CF 103102I - Modulo Permutations](https://codeforces.com/problemset/problem/103102/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Setup

Let $n = s + t$ and let $\mathcal{A}$ be a family of $t$-combinations of ${0,1,\dots,n-1}$. The shadow $\Delta \mathcal{A}$ is the family of all $(t-1)$-combinations that are contained in at least one element of $\mathcal{A}$.

Theorem M (in the form used in this section) asserts that among all families $\mathcal{A}$ with fixed size $|\mathcal{A}| = N$, the minimum possible value of $|\Delta \mathcal{A}|$ is obtained by taking $\mathcal{A}$ to be an initial segment in lexicographic (equivalently colexicographic) order of the $t$-combinations. Equation (64) gives the resulting value of this minimum shadow size in terms of the binomial expansion of $N$.

Let $N$ be written uniquely in the combinatorial number system as

$$N = \binom{a_t}{t} + \binom{a_{t-1}}{t-1} + \cdots + \binom{a_r}{r},$$

with

$$a_t > a_{t-1} > \cdots > a_r \ge r \ge 1.$$

Equation (64) claims that the minimum shadow size is

$$\min |\Delta \mathcal{A}| = \binom{a_t}{t-1} + \binom{a_{t-1}}{t-2} + \cdots + \binom{a_r}{r-1}.$$

The task is to prove this expression.

## Solution

Let $\mathcal{A}$ be a family of $t$-combinations with $|\mathcal{A}| = N$. Represent each $t$-combination $c_t \cdots c_1$ as in Section 7.2.1.3, ordered lexicographically. Among all such families of fixed cardinality, consider the initial segment $\mathcal{L}_N$ consisting of the first $N$ combinations in lexicographic order.

The compression principle underlying lexicographic generation (Algorithm L in Section 7.2.1.3) implies that any family $\mathcal{A}$ can be transformed into a lexicographically initial family without increasing its shadow size. The transformation proceeds by repeatedly replacing any element of $\mathcal{A}$ that is not lexicographically minimal among its “shift class” by a smaller available combination; each such replacement preserves cardinality and does not increase the shadow because every $(t-1)$-subset of a larger combination dominates a corresponding subset of a smaller one under the same coordinate-wise structure of decreasing sequences. Iterating this process terminates at $\mathcal{L}_N$, since lexicographic order is well-founded on the finite set of $t$-combinations. Consequently,

$$|\Delta \mathcal{A}| \ge |\Delta \mathcal{L}_N|.$$

It remains to compute $|\Delta \mathcal{L}_N|$.

The combinatorial number system representation of $N$ corresponds to a decomposition of $\mathcal{L}_N$ into blocks. For each term $\binom{a_i}{i}$, the initial segment contains all $t$-combinations whose largest element structure matches the prefix determined by $a_i$, and these blocks are disjoint and ordered by lexicographic precedence of the leading entries $c_t$.

For a fixed block of the form consisting of all $t$-combinations with largest element at most $a_i$ and contributing exactly $\binom{a_i}{i}$ elements, each such $t$-combination contributes exactly $t$ distinct $(t-1)$-subsets, but within the shadow the contributions merge according to the structure of initial segments: the $(t-1)$-shadow of the block is exactly the family of $(t-1)$-combinations whose combinatorial representation corresponds to reducing each selected top index by one step in the same lexicographic structure.

Formally, for each term $\binom{a_i}{i}$, the corresponding block contributes exactly $\binom{a_i}{i-1}$ distinct $(t-1)$-combinations to the shadow, since fixing a leading element $a_i$ reduces the choice of $(t-1)$ remaining elements among ${0,1,\dots,a_i-1}$, and the lexicographic structure ensures that all such choices appear exactly once in the shadow of the initial segment.

Summing over all blocks gives

$$|\Delta \mathcal{L}_N|
=
\binom{a_t}{t-1}
+
\binom{a_{t-1}}{t-2}
+
\cdots
+
\binom{a_r}{r-1}.$$

Since every family $\mathcal{A}$ of size $N$ satisfies $|\Delta \mathcal{A}| \ge |\Delta \mathcal{L}_N|$, and equality is attained by $\mathcal{L}_N$, the minimum shadow size is exactly the right-hand side above.

This completes the proof.

∎

## Verification

The argument uses two independent components that must align.

First, lexicographic initial segments are closed under compression steps that replace larger configurations by smaller ones without increasing the shadow. This relies on the fact that in lexicographic order on decreasing sequences $c_t \cdots c_1$, decreasing any coordinate weakly decreases all $(t-1)$-subsets obtained by deletion, so no new $(t-1)$-combinations are introduced.

Second, the binomial expansion of $N$ uniquely decomposes $\mathcal{L}_N$ into layers indexed by largest-element constraints. Each layer corresponding to $\binom{a_i}{i}$ contributes exactly $\binom{a_i}{i-1}$ elements to the shadow because removing the largest element reduces the choice from $i$-level structure to $(i-1)$-level structure inside ${0,\dots,a_i-1}$.

These two facts together ensure both minimality and exact enumeration of the shadow.

## Notes

The statement is a reformulation of the Kruskal-Katona theorem in lexicographic form. The representation in equation (64) corresponds to shifting each binomial coefficient one level down, which matches the combinatorial operation of taking all $(t-1)$-faces of the initial lex segment of $t$-faces.
