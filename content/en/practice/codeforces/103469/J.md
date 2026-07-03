---
title: "CF 103469J - Joke"
description: "We are given a fixed permutation $p$ of size $n$, and a partially specified permutation $q$ of the same size. Some positions in $q$ are known, others are zero and must be filled so that the final sequence becomes a valid permutation of $1$ to $n$."
date: "2026-07-03T06:45:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103469
codeforces_index: "J"
codeforces_contest_name: "2021 Summer Petrozavodsk Camp, Day 3: IQ test (XXII Open Cup, Grand Prix of IMO)"
rating: 0
weight: 103469
solve_time_s: 32
verified: false
draft: false
---

[CF 103469J - Joke](https://codeforces.com/problemset/problem/103469/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed permutation $p$ of size $n$, and a partially specified permutation $q$ of the same size. Some positions in $q$ are known, others are zero and must be filled so that the final sequence becomes a valid permutation of $1$ to $n$.

For every completed permutation $q$, we define a quantity $f(p,q)$. This is not defined directly as a formula but as a counting problem over a $2 \times n$ matrix filled with the numbers $1$ through $2n$, each appearing exactly once. The matrix is constrained so that within each row, the ordering of values is forced by the corresponding permutation: if we sort columns by increasing $p_i$, the first row must be strictly increasing, and similarly the second row must be strictly increasing when columns are sorted by increasing $q_i$.

Additionally, each column carries a binary label depending on whether the top entry is smaller than the bottom entry. That binary string is not fixed in advance; it is induced by the chosen matrix. The value $f(p,q)$ counts how many such valid matrices exist for a fixed pair $(p,q)$. Finally, the task is to sum $f(p,q)$ over all completions of the partial permutation $q$, modulo $998244353$.

The constraints $n \le 100$ imply that any solution involving $O(n^3)$ or worse combinatorics over permutations is still acceptable, but anything exponential in $n$ or enumerating matrices explicitly is not. Since the matrix contains $2n$ distinct values, a naive interpretation already suggests factorial-scale structures, so the real challenge is to collapse the counting into something that depends only on coarse combinatorial choices rather than explicit assignments.

A subtle failure case appears if one assumes the binary string $s$ is independent of the numeric assignment. For example, for $n=2$, different placements of values $1,2,3,4$ can produce the same $p,q$ ordering constraints but different column comparisons, so $s$ is
