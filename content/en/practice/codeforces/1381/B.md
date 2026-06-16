---
title: "CF 1381B - Unmerge"
description: "We are given a permutation of size $2n$. The task is to decide whether we can split the numbers into two disjoint sequences $a$ and $b$, each of length $n$, such that if we repeatedly simulate a specific “two-pointer merge” process starting from the heads of $a$ and $b$, we…"
date: "2026-06-16T13:47:59+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1381
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 658 (Div. 1)"
rating: 1800
weight: 1381
solve_time_s: 88
verified: false
draft: false
---

[CF 1381B - Unmerge](https://codeforces.com/problemset/problem/1381/B)

**Rating:** 1800  
**Tags:** dp  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of size $2n$. The task is to decide whether we can split the numbers into two disjoint sequences $a$ and $b$, each of length $n$, such that if we repeatedly simulate a specific “two-pointer merge” process starting from the heads of $a$ and $b$, we recover exactly the given permutation.

The merge process is deterministic once $a$ and $b$ are fixed: at every step we compare the current front elements and always take the smaller one. This means the final sequence is fully determined by the relative ordering of elements as they appear in $a$ and $b$, not by any freedom in choices.

So the real question is not about simulating merge forward, but about whether we can reverse-engineer two valid sequences whose interleaving under this greedy comparison produces the target permutation.

The constraints are small in a very important way. Each test has $n \le 2000$ and the total sum of $n$ is also at most $2000$. This immediately rules out anything worse than roughly $O(n^2)$ per test, and strongly suggests that we should be thinking in terms of dynamic programming over positions or over splits, rather than factorial or exponential constructions.

A naive approach would be to try all ways of assigning each element to either $a$ or $b$, but that is $2^{2n}$, which is completely infeasible. Even trying to simulate validity after assignment is still exponential.

A more subtle failure case appears when we try greedy assignment based on local comparisons. Since the merge rule depends on the _front_ of each array, which evolves dynamically, any greedy assignment that ignores future constraints will break on permutations where early small elements “force” future structure incorrectly. For example, a small number placed too early in the wrong array can block later required comparisons, making a valid split impossible even if the prefix looks consistent.

## Approaches

The brute-force idea is to assign each element of the permutation to either $a$ or $b$, ensuring both receive exactly $n$ elements. For each assignment, we simulate whether the merge process reproduces the permutation. This requires maintaining two queues and repeatedly comparing their fronts, which costs $O(n)$ per simulation. Since there are $\binom{2n}{n}$ assignments, the total complexity is exponential and grows far beyond any limit.

The key observation is that the merge process does not depend on absolute labels, but on relative ordering constraints induced by prefix structure. At any point during reconstruction, what matters is which elements are still “active fronts” of the two arrays. This suggests that instead of constructing $a$ and $b$ directly, we can process the permutation and decide how to assign each prefix element while maintaining the possibility
