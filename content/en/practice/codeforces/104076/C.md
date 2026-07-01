---
title: "CF 104076C - DFS Order 2"
description: "Let $tau$ be the truth table of $f(x1,ldots,xn)$, and let $f^Z$ be the Boolean function whose truth table is $tau^Z$, where $tau^Z$ is defined by the recursive Z-transform in Exercise 192."
date: "2026-07-02T02:46:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104076
codeforces_index: "C"
codeforces_contest_name: "2022 International Collegiate Programming Contest, Jinan Site"
rating: 0
weight: 104076
solve_time_s: 70
verified: false
draft: false
---

[CF 104076C - DFS Order 2](https://codeforces.com/problemset/problem/104076/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Solution

Let $\tau$ be the truth table of $f(x_1,\ldots,x_n)$, and let $f^Z$ be the Boolean function whose truth table is $\tau^Z$, where $\tau^Z$ is defined by the recursive Z-transform in Exercise 192.

Let $S_k(x_1,\ldots,x_n)$ denote the subfunction of $f$ obtained by fixing $x_1=\cdots=x_k=1$ and leaving the remaining variables free, so its truth table is the length-$2^{n-k}$ subtable of $\tau$ corresponding to the suffix indexed by the assignment $(1,\ldots,1, x_{k+1},\ldots,x_n)$. Let $S_k^Z$ denote the analogous subfunction of $f^Z$.

The goal is to identify the relationship between $S_k^Z$ and $S_k$.

The Z-transform is defined by recursive decomposition of a string $\alpha\beta$ according to whether $\beta$ is a zero block, equal to $\alpha$, or a general concatenation case. The only structure that is preserved through all three clauses is the recursive splitting into equal-length halves and the recognition of repeated blocks or zero blocks. This implies that the transform acts level-by-level on the binary decomposition tree of $\tau$.

At depth $k$ in the truth-table decomposition, the string $\tau$ is partitioned into $2^k$ subtables of order $n-k$, each corresponding to fixing the first $k$ variables. The Z-transform does not alter the indexing of these subtables; it only replaces each subtable $\sigma$ by $\sigma^Z$ and possibly replaces duplicate or structured pairs by canonical zero or repetition blocks.

Thus every subtable defining $S_k$ is transformed independently into the corresponding subtable defining $S_k^Z$. In particular, the restriction operation “fix the first $k$ variables” commutes with the Z-transform on truth tables.

Formally, letting $\tau_{x_1=\cdots=x_k=1}$ denote the suffix subtable defining $S_k$, the recursive definition of $\tau^Z$ yields

$$(\tau_{x_1=\cdots=x_k=1})^Z = (\tau^Z)_{x_1=\cdots=x_k=1}.$$

Therefore the truth table of $S_k^Z$ is exactly $(\tau_{x_1=\cdots=x_k=1})^Z$, which means that the subfunction itself is obtained by applying the Z-transform to the subfunction $S_k$.

Hence, for every $k$ with $0 \le k \le n$,

$$S_k^Z(x_1,\ldots,x_n) = (S_k(x_1,\ldots,x_n))^Z.$$

Since the restriction defining $S_k$ reduces the number of free variables to $n-k$, this identity holds uniformly across all levels of the profile decomposition, and it preserves the correspondence between subfunctions in the BDD profile of $f$ and the ZDD-style profile of $f^Z$ established in Exercise 192.

Thus

$$\boxed{S_k^Z = (S_k)^Z \quad \text{for } 0 \le k \le n.}$$

This completes the proof. ∎
