---
title: "CF 102893L - The Firm Knapsack Problem"
description: "Let $a1 a2 dots am$ be a partition written in nonincreasing form, and let $b1 b2 dots bm$ be its conjugate, so $bj$ is the number of indices $i$ with $ai ge j$."
date: "2026-07-04T12:15:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102893
codeforces_index: "L"
codeforces_contest_name: "2020-2021 Russia Team Open, High School Programming Contest (VKOSHP 20)"
rating: 0
weight: 102893
solve_time_s: 165
verified: false
draft: false
---

[CF 102893L - The Firm Knapsack Problem](https://codeforces.com/problemset/problem/102893/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Solution

Let $a_1 a_2 \dots a_m$ be a partition written in nonincreasing form, and let $b_1 b_2 \dots b_m$ be its conjugate, so $b_j$ is the number of indices $i$ with $a_i \ge j$. The Ferrers diagram of $a$ consists of unit cells in row $i$ for columns $1$ through $a_i$, and the diagram of $b$ is obtained by reflecting this shape across the main diagonal.

Consider the set of outer corner cells of the Ferrers diagram of $a$, namely the cells $(i, a_i)$ for $1 \le i \le m$. These are exactly the rightmost cells in each nonempty row. Their column index is $a_i$ and their row index is $i$, so each such corner contributes the integer $a_i + i$.

Now examine the conjugate diagram. In the transposed Ferrers diagram, the outer corners correspond to the bottom cells of each nonempty column, namely the cells $(b_j, j)$ for $1 \le j \le m$. These are exactly the lowest cells in each column. Each such corner contributes the integer $b_j + j$.

Transposition of the Ferrers diagram maps each cell $(i, j)$ of $a$ to $(j, i)$ in $b$. In particular, it maps each outer corner $(i, a_i)$ of $a$ to an outer corner $(a_i, i)$ of $b$. This induces a bijection between the two sets of outer corners:

$$(i, a_i) \longleftrightarrow (a_i, i).$$

Under this correspondence, the value attached to a corner is preserved:

$$a_i + i = i + a_i,
\qquad
b_{a_i} + a_i = a_i + i.$$

Since every outer corner of $a$ is mapped to a unique outer corner of $b$, and vice versa, the collection of values ${a_i + i}$ coincides, as a multiset, with the collection ${b_j + j}$.

To make the multiset equality explicit, define

$$S = \{ a_i + i : 1 \le i \le m \}, \quad
T = \{ b_j + j : 1 \le j \le m \}.$$

The bijection between outer corners induces a bijection between indices contributing to $S$ and those contributing to $T$, preserving the value of each element. Hence $S = T$ as multisets.

This completes the proof. ∎
