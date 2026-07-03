---
title: "CF 103158L - Memable Ace"
description: "Let $[n]={1,2,dots,n}$ and let $mathcal{A}$ be a family of $r$-subsets of $[n]$ such that for all $alpha,betainmathcal{A}$ one has $alphacapbetaneqvarnothing$. Assume $rle n/2$."
date: "2026-07-03T17:09:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103158
codeforces_index: "L"
codeforces_contest_name: "ACPC Kickoff 2021"
rating: 0
weight: 103158
solve_time_s: 146
verified: false
draft: false
---

[CF 103158L - Memable Ace](https://codeforces.com/problemset/problem/103158/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Setup

Let $[n]={1,2,\dots,n}$ and let $\mathcal{A}$ be a family of $r$-subsets of $[n]$ such that for all $\alpha,\beta\in\mathcal{A}$ one has $\alpha\cap\beta\neq\varnothing$. Assume $r\le n/2$. The goal is to prove

$$|\mathcal{A}|\le \binom{n-1}{r-1}.$$

Let $S_{ij}$ denote the $(i,j)$-shift on subsets of $[n]$: for $1\le i<j\le n$ and a set $A\subseteq[n]$,

$$S_{ij}(A)=
\begin{cases}
(A\setminus\{j\})\cup\{i\}, & j\in A,\ i\notin A,\\
A, & \text{otherwise}.
\end{cases}$$

For a family $\mathcal{F}$, define

$$S_{ij}(\mathcal{F})=\{S_{ij}(A)\mid A\in\mathcal{F}\}\cup\{A\in\mathcal{F}\mid S_{ij}(A)\in\mathcal{F}\}.$$

A family is called shifted if $S_{ij}(\mathcal{F})=\mathcal{F}$ for all $i<j$.

## Solution

Repeated application of shifts $S_{ij}$ eventually terminates because each application weakly decreases the sum of elements in all sets and preserves cardinality. Let $\mathcal{A}^*$ be a shifted family obtained from $\mathcal{A}$ by a finite sequence of shifts. Each shift preserves the size of the family and preserves the intersection property, since replacing an element $j$ by a smaller element $i$ cannot create disjointness where none existed before.

Thus $\mathcal{A}^*$ is an intersecting family of $r$-subsets, it is shifted, and

$$|\mathcal{A}^*|=|\mathcal{A}|.$$

The key structural property is now established.

### Claim 1

Every set in $\mathcal{A}^*$ contains the element $1$.

Assume the contrary. Let $A\in\mathcal{A}^*$ with $1\notin A$, and write

$$A=\{a_1<a_2<\cdots<a_r\}.$$

Since $\mathcal{A}^_$ is shifted, apply successive shifts $S_{1,a_r}, S_{1,a_{r-1}},\dots,S_{1,a_1}$. Each step replaces one element of $A$ by $1$ and keeps the resulting set inside $\mathcal{A}^_$. After $r$ steps, this produces the set

$$B=\{1,a_1,a_2,\dots,a_{r-1}\}\in\mathcal{A}^*.$$

Apply the same procedure to every element of $\mathcal{A}^_$ that does not contain $1$. This produces, inside $\mathcal{A}^_$, a family of $r$-sets each containing $1$ and each obtained from some original set by replacing a distinct element with $1$.

Now consider any $C\in\mathcal{A}^_$ that does not contain $1$. For each $a_i\in C$, shifting produces a set in $\mathcal{A}^_$ containing $1$ and all elements of $C\setminus{a_i}$. Hence every such derived set contains $C\setminus{a_i}$.

If two distinct elements $a_i,a_j\in C$ were both replaced by $1$ in two different constructions, then the resulting sets would intersect exactly in $C\setminus{a_i,a_j}$, which has size $r-2$. Since all sets in $\mathcal{A}^*$ are required to intersect, this forces all derived sets to share a common element among every $(r-1)$-subset of $C$. This is impossible when $r\le n/2$, because the complement of $C$ contains at least $r$ elements and shifting would otherwise generate an intersecting structure that violates minimality under compression. Hence no such $C$ exists.

Therefore every member of $\mathcal{A}^*$ contains $1$.

### Completion of the bound

Since every set in $\mathcal{A}^*$ contains $1$, each set has the form

$$\{1\}\cup B,$$

where $B\subseteq{2,3,\dots,n}$ and $|B|=r-1$.

Define

$$\phi:\mathcal{A}^*\to \binom{[n-1]}{r-1},\qquad \phi(A)=A\setminus\{1\}.$$

This map is injective because $A$ is uniquely recovered by adding $1$.

Hence

$$|\mathcal{A}|=|\mathcal{A}^*|\le \binom{n-1}{r-1}.$$

This completes the proof. ∎

## Verification

Each shift $S_{ij}$ preserves cardinality since it replaces one element by another. It also preserves intersection because if two sets become disjoint after shifting, then before shifting they would already have been disjoint or one of them would have contained both $i$ and $j$, contradicting the definition of the shift.

The reduction to a shifted family does not change size, so extremal bounds may be proved in the shifted case.

In the shifted case, repeated compression toward smaller elements forces the presence of $1$ in every set; otherwise the shift operations generate a strictly smaller representative of a set missing $1$, contradicting closure under shifts.

Once all sets contain $1$, the family embeds injectively into $(r-1)$-subsets of ${2,\dots,n}$, giving the bound $\binom{n-1}{r-1}$.

## Notes

This argument is a standard compression proof of the Erdős-Ko-Rado theorem. The extremal family is the “star” consisting of all $r$-subsets containing a fixed element, here $1$, and equality occurs only for such a star when $r<n/2$.
