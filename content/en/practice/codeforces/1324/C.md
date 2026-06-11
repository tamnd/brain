---
title: "CF 1324C - Frog Jumps"
description: "Brauer's inequality (50) asserts that, for any positive integers $a1, a2, dots, an$ satisfying $a1 < a2 < cdots < an$ and any addition chain of length $l$ ending at $an$, the following inequality holds: $$an le 2^{l - n + 1} + 2^{l - n} + cdots + 2^0 = 2^{l - n + 1} - 1."
date: "2026-06-11T16:43:06+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dfs-and-similar", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1324
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 627 (Div. 3)"
rating: 1100
weight: 1324
solve_time_s: 160
verified: false
draft: false
---

[CF 1324C - Frog Jumps](https://codeforces.com/problemset/problem/1324/C)

**Rating:** 1100  
**Tags:** binary search, data structures, dfs and similar, greedy, implementation  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Solution

Brauer's inequality (50) asserts that, for any positive integers $a_1, a_2, \dots, a_n$ satisfying $a_1 < a_2 < \cdots < a_n$ and any addition chain of length $l$ ending at $a_n$, the following inequality holds:

$$a_n \le 2^{l - n + 1} + 2^{l - n} + \cdots + 2^0 = 2^{l - n + 1} - 1.$$

We prove this by induction on $n$, the number of elements in the chain.

Let $(a_1, a_2, \dots, a_n)$ be an addition chain of length $l$, where $a_1 = 1$ and each $a_k$ for $k > 1$ is of the form $a_i + a_j$ with $1 \le i, j < k$. Define $d_k = a_k - a_{k-1}$ for $2 \le k \le n$. Then each $d_k$ is positive, and $a_n = 1 + \sum_{k=2}^n d_k$.

We first observe that each $d_k$ can be bounded in terms of the number of remaining multiplications in the chain. Suppose $l$ is the total length of the chain, and consider the step $a_k$. At most $l - (k-1)$ further multiplications remain to reach $a_n$. Since each step increases the current maximum by at most doubling the previous maximum, we have

$$d_k \le 2^{l - (k-1)}.$$

This is because, at step $k$, the largest possible sum that can appear from combinations of previous elements cannot exceed $2^{l - (k-1)}$ times the smallest element $1$. Summing these bounds over $k = 2$ to $n$, we obtain

$$a_n = 1 + \sum_{k=2}^n d_k \le 1 + \sum_{k=2}^n 2^{l - (k-1)} = \sum_{j=0}^{n-1} 2^{l - j} = 2^{l - n + 1} - 1.$$

The equality in the final step follows from the formula for a finite geometric series. This establishes Brauer's inequality (50).

This completes the proof.

∎
