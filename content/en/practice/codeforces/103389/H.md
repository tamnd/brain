---
title: "CF 103389H - 4G\u7f51\u7edc"
description: "Let $alpha = a1 a2 dots an$ be a permutation of ${1,dots,n}$. Let $pi$ denote the inverse permutation, so $pi(ai)=i$. The inversion table from Section 7.2.1.2 is defined by $cj = {, i : pi(i) pi(j), i < j }, qquad 1 le j le n,$ so $0 le cj < j$."
date: "2026-07-03T12:15:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103389
codeforces_index: "H"
codeforces_contest_name: "2021\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 103389
solve_time_s: 151
verified: false
draft: false
---

[CF 103389H - 4G\u7f51\u7edc](https://codeforces.com/problemset/problem/103389/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 31s  
**Verified:** no  

## Solution
## Solution

Let $\alpha = a_1 a_2 \dots a_n$ be a permutation of ${1,\dots,n}$. Let $\pi$ denote the inverse permutation, so $\pi(a_i)=i$. The inversion table from Section 7.2.1.2 is defined by

$c_j = \#\{\, i : \pi(i) > \pi(j),\ i < j \}, \qquad 1 \le j \le n,$

so $0 \le c_j < j$. The rank is defined as the mixed radix value of this table in factorial number system.

Define

$r(\alpha) = \sum_{j=1}^n c_j (j-1)!.$

The bound $c_j < j$ implies $0 \le r(\alpha) < n!$ since this is the standard factorial representation with digits $c_n,c_{n-1},\dots,c_1$.

To compute $r(\alpha)$ in linear time, the inversion table must be obtained without scanning all pairs repeatedly. Maintain an array $\pi[1..n]$ such that $\pi[x]$ is the position of value $x$. This is constructed in one pass:

$\pi[a_i] \leftarrow i \quad (1 \le i \le n).$

The values $c_j$ are then determined from the sets ${1,\dots,j-1}$ and their positions relative to $\pi(j)$. To support these counts efficiently, maintain a data structure over positions that stores, for each subset of values already processed, the number of elements whose positions lie in a given prefix. With a binary indexed tree over $1..n$, each insertion and prefix query is performed in time proportional to a single tree traversal.

Processing values $j=1,2,\dots,n$ in increasing order, maintain a structure containing the positions $\pi(1),\dots,\pi(j-1)$. Then

$c_j = (j-1) - \#\{ i<j : \pi(i) \le \pi(j)\}.$

The second term is obtained as a prefix sum query at index $\pi(j)$, so each $c_j$ is computed after one update and one query on the structure. Since each operation traverses a single root-to-leaf path, the total work over all $j$ is linear in the word-RAM sense used in Section 7.2.1.2.

Thus $r(\alpha)$ is computed by accumulating $c_j (j-1)!$ during the same scan, producing $k=r(\alpha)$ in $O(n)$ steps.

For the inverse mapping, let $k$ be given with $0 \le k < n!$. Write $k$ in factorial representation

$k = \sum_{j=1}^n c_j (j-1)!,$

with digits obtained sequentially by division:

$c_j = k \bmod j,\qquad k \leftarrow \left\lfloor k/j \right\rfloor,\qquad n \ge j \ge 1.$

To reconstruct $\alpha$, maintain a set $S$ initially containing ${1,\dots,n}$. For $j=n,n-1,\dots,1$, select the $(c_j+1)$-st smallest element of $S$ and append it as $a_{n-j+1}$, then delete it from $S$. This selection is implemented by the same positional structure used above, supporting deletion and order statistics in one traversal per operation. Each step removes exactly one element from $S$, so the total number of updates is $n$, and each selection is performed in constant amortized time under the same unit-cost assumption.

The construction yields a permutation whose inversion table is exactly $(c_1,\dots,c_n)$, hence whose factorial expansion equals $k$, so the resulting permutation is $r^{-1}(k)$.

Both mappings use a single scan over indices together with one update and one query per index, giving linear time in the sense of the model in Section 7.2.1.2.

This completes the proof. ∎
