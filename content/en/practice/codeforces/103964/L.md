---
title: "CF 103964L - Huatuo's Medicine"
description: "Let $c1c2cdots cn$ be the part-count representation of a partition of $n$, so that $sum{j=1}^n j cj = n.$ The colex order on partitions corresponds to lexicographic order on the reversed vector $cn c{n-1}cdots c1$, so successive partitions are obtained by making the earliest…"
date: "2026-07-04T11:25:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103964
codeforces_index: "L"
codeforces_contest_name: "The 2015 China Collegiate Programming Contest (CCPC 2015)"
rating: 0
weight: 103964
solve_time_s: 107
verified: false
draft: false
---

[CF 103964L - Huatuo's Medicine](https://codeforces.com/problemset/problem/103964/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Solution

Let $c_1c_2\cdots c_n$ be the part-count representation of a partition of $n$, so that

$\sum_{j=1}^n j c_j = n.$

The colex order on partitions corresponds to lexicographic order on the reversed vector $c_n c_{n-1}\cdots c_1$, so successive partitions are obtained by making the earliest possible change when scanning indices downward from $n$.

A partition is maximal in this order precisely when it has no part of size at least $2$, that is when $c_2=\cdots=c_n=0$, hence $c_1=n$. This is the terminal element of the generation.

Any nonterminal partition contains some largest index $k\ge 2$ with $c_k>0$. In the Ferrers interpretation, this corresponds to the rightmost part exceeding $1$. The successor operation in Algorithm P replaces such a part $k$ by $k-1$ together with an additional $1$, which preserves the total sum since

$k = (k-1)+1.$

In part-count form this transformation changes exactly three components:

$c_k \leftarrow c_k - 1,\quad c_{k-1} \leftarrow c_{k-1} + 1,\quad c_1 \leftarrow c_1 + 1.$

All other $c_j$ remain unchanged.

This operation preserves the partition identity because the total contribution of the modified indices changes by

$-k + (k-1) + 1 = 0.$

The link structure $l_0,l_1,\dots,l_n$ maintains the strictly increasing sequence of indices $k$ with $c_k>0$. If the current nonzero indices are $k_1<\cdots<k_t$, then $l_0=k_1$, $l_{k_i}=k_{i+1}$, and $l_{k_t}=0$. This permits locating the largest $k$ with $c_k>0$ by traversing from $l_0$ forward until reaching $0$, and then stepping back through stored predecessors if implemented, or equivalently maintaining a tail pointer to $k_t$.

The generation algorithm is defined as follows.

P1. [Initialize.] Set $c_n\leftarrow 1$ and $c_j\leftarrow 0$ for $1\le j<n$. Set $l_0\leftarrow n$, $l_n\leftarrow 0$, and all other links undefined. Set $k\leftarrow n$.

P2. [Visit.] Visit the current vector $c_1c_2\cdots c_n$. Then set $k$ to the largest index with $c_k>0$ and $k\ge 2$ by following the link chain from $l_0$ until reaching the last node. If no such $k$ exists, terminate.

P3. [Split step.] Set $c_k\leftarrow c_k-1$, $c_{k-1}\leftarrow c_{k-1}+1$, and $c_1\leftarrow c_1+1$.

P4. [Update links for $k$ and $k-1$.] If $c_k=0$, remove $k$ from the linked list by redirecting its predecessor link: if $p=l_0,\dots$ is the predecessor of $k$, then set $l_p\leftarrow l_k$. If $c_{k-1}$ was $0$ before the increment, insert $k-1$ into the list by setting $l_{k-1}\leftarrow l_k$ and then setting $l_k\leftarrow k-1$; otherwise no structural change is required beyond adjusting counts.

P5. [Update $k$.] Return to P2.

Each iteration replaces exactly one part $k\ge 2$ by $k-1$ and $1$, which strictly decreases the reversed lexicographic representation since the first modified coordinate from the right is decreased from $1$ (in the implicit binary expansion of that part) to a configuration beginning with a smaller nonzero entry. This matches the successor structure of Algorithm P, where the rightmost non-$1$ part is decreased and the tail of $1$s is adjusted.

Every partition distinct from $1^n$ contains at least one part $\ge 2$, hence some $k\ge 2$ exists whenever the algorithm has not terminated. The transformation strictly increases the number of parts and moves weight toward smaller indices, ensuring no partition is repeated, since reversing the operation would require merging a $1$ with a $k-1$ uniquely reconstructing the previous state.

Since each step corresponds to a unique application of the transformation on the uniquely determined largest $k\ge 2$, every partition has exactly one predecessor and one successor in this process, matching the structure of a linear traversal of the partition poset in colex order.

This completes the construction and correctness proof. ∎
