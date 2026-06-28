---
title: "CF 104941F - Fun Tournament"
description: "We are given a set of contestants, each described by two integers. Think of each contestant as carrying two “moves”: the first move is $ai$, and the second move is $bi$."
date: "2026-06-28T18:17:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "F"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 34
verified: false
draft: false
---

[CF 104941F - Fun Tournament](https://codeforces.com/problemset/problem/104941/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of contestants, each described by two integers. Think of each contestant as carrying two “moves”: the first move is $a_i$, and the second move is $b_i$. If we pick two different contestants $i$ and $j$, they play two games: in the first game we compare $a_i$ vs $a_j$, and in the second game we compare $b_i$ vs $b_j$. The score of each game is the absolute difference of the chosen values. So the first game contributes $|a_i - a_j|$, the second contributes $|b_i - b_j|$.

A pair of contestants is considered bad if these two values coincide, meaning

$$|a_i - a_j| = |b_i - b_j|.$$

The task is to count how many pairs are good, i.e. how many pairs violate this equality.

The input size goes up to $n = 3 \cdot 10^5$, so any quadratic enumeration over pairs is immediately too slow. A solution must be close to linear or $n \log n$, since $n^2$ would mean about $10^{10}$ comparisons in the worst case.

A subtle edge case is when many pairs share the same structure, which can cause naive hashing of differences to collide or miss sign variants. For example, if all contestants are identical, every pair satisfies equality, so the answer is zero. Any approach that only partially captures the absolute difference condition without handling sign symmetry will fail on cases like:

$$(1, 5), (5, 1), (3, 3).$$

Another tricky scenario is when differences are equal but come from different sign configurations, such as:

$$|a_i - a_j| = |b_i - b_j| \iff a_i - a_j = b_i - b_j \ \text{or}\ a_i - a_j = -(b_i - b_j).$$

Missing one of these cases leads to overcounting good pairs.

## Approaches

The direct approach is straightforward: iterate over all pairs $i < j$ and check whether $|a_i - a_j| = |b_i - b_j|$. This is correct but costs $O(n^2)$ comparisons. With $n = 3 \cdot 10^5$, this is far beyond feasible.

The key observation is to eliminate the absolute value condition by splitting it into two linear equalities:

$$a_i - a_j = b_i - b_j \quad \text{or} \quad a_i - a_j = -(b_i - b_j).$$

Rearranging gives:

$$a_i - b_i = a_j - b_j \quad \text{or} \quad a_i + b_i = a_j + b_j.$$

So a pair is “bad” exactly when either the value $a_i - b_i$ matches or the value $a_i + b_i$ matches. This reduces the problem into counting equal pairs in two different derived arrays.

However, directly summing both counts overcounts pairs where both equalities hold simultaneously. That happens exactly when both:

$$a_i - b_i = a_j - b_j \quad \text{and} \quad a_i + b_i = a_j + b_j,$$

which implies $(a_i, b_i) = (a_j, b_j)$. So duplicates must be corrected carefully.

We therefore compute:

1. total pairs,
2. subtract pairs that are “bad” via sum and difference equalities, with careful handling of duplicates using frequency counting.

The efficient solution uses sorting or hash maps to count frequencies of the transformed keys $a_i - b_i$ and $a_i + b_i$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ or $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We rewrite the condition into two independent key systems: $d_i = a_i - b_i$ and $s_i = a_i + b_i$. We count how many pairs share the same value in each system.

1. Compute total number of pairs as $\frac{n(n-1)}{2}$. This is the baseline from which we subtract “bad” pairs.
2. Build a frequency map for all values $d_i = a_i - b_i$. For each distinct value occurring $f$ times, it contributes $\frac{f(f-1)}{2}$ bad pairs. This counts all pairs satisfying $a_i - b_i = a_j - b_j$.
3. Build a second frequency map for all values $s_i = a_i + b_i$. Similarly, each frequency $f$ contributes $\frac{f(f-1)}{2}$ pairs where $a_i + b_i = a_j + b_j$.
4. Add the contributions from both maps to get the total number of pairs satisfying at least one of the bad equalities. This sum double-counts pairs where both conditions hold.
5. Identify duplicates where
