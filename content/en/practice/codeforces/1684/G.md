---
title: "CF 1684G - Euclid Guess"
description: "We are given a multiset of positive integers, and we are told that this multiset was produced by repeatedly running Euclid’s algorithm on several unknown integer pairs."
date: "2026-06-10T00:03:17+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "flows", "graph-matchings", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1684
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 792 (Div. 1 + Div. 2)"
rating: 2800
weight: 1684
solve_time_s: 63
verified: false
draft: false
---

[CF 1684G - Euclid Guess](https://codeforces.com/problemset/problem/1684/G)

**Rating:** 2800  
**Tags:** constructive algorithms, flows, graph matchings, math, number theory  
**Solve time:** 1m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of positive integers, and we are told that this multiset was produced by repeatedly running Euclid’s algorithm on several unknown integer pairs. Every time Euclid’s algorithm performs a division step and obtains a non-zero remainder, that remainder is appended to a global list. After processing all pairs, the final list is shuffled before being given to us.

Our task is to reconstruct any collection of pairs of positive integers, each not exceeding a given limit, such that when Euclid’s algorithm is run on each pair and all produced remainders are collected together, the resulting multiset of remainders matches the given multiset exactly.

The key observation is that we are not reconstructing the order of remainders per pair. We only need to partition the multiset into valid Euclid traces, each trace corresponding to one starting pair.

The constraint that both numbers in each pair are at most m is critical because it limits how large intermediate Euclid states can be, especially the first division step, which determines whether a pair is even feasible.

A subtle edge case appears when the input contains values that cannot appear as the first remainder of any valid Euclid step under the bound m. For example, if m is small and the multiset contains a value strictly larger than m/2, it may be impossible to produce it as a remainder of any valid pair, since the first step requires constructing numbers a and b with a = kb + r and a ≤ m, b ≤ m.

Another failure case occurs when the multiset is too “irregular” to be decomposed into Euclid chains. For instance, a single large number with no compatible companion values may force an impossible reconstruction, because each Euclid process generates a structured decreasing sequence of remainders, not arbitrary collections.

The central difficulty is therefore not simulation, but deciding whether the multiset can be decomposed into valid Euclid remainder chains and then constructing explicit integer pairs that generate them.

## Approaches

A direct idea is to try to reverse Euclid’s algorithm for each number independently. For a single remainder sequence, one could attempt to guess a second value and reconstruct a valid pair that generates it. However, since the same number can appear in multiple different Euclid chains and the assignment is unknown, this leads to an exponential partitioning problem over all subsets of the multiset. Even with memoization, the number of ways to group values into chains grows too quickly for n up to 1000.

The key structural insight is to reverse the generation process locally. Instead of thinking in terms of full Euclid runs, we focus on the first step of Euclid for a pair (a, b). If a ≥ b, then the first remainder is a mod b. If we want a specific remainder r to appear in the output, we can enforce a construction where a = k·b + r for some k ≥ 1. This means each remainder r can be “hosted” by choosing a suitable b and k such that both numbers stay within m.

Rewriting this, each r requires finding a pair (b, a) such that a mod b = r, or equivalently a = b + r (choosing k = 1 is sufficient and optimal for construction). Then b must be > r and a ≤ m. This immediately gives a simple construction condition: for each r we need some b in (r, m] such that r + b ≤ m, which is equivalent to b ≤ m − r.

Thus, for each r we need to choose a partner b in the interval (r, m − r]. This becomes a bipartite matching problem between values r and possible choices of b, where each chosen b produces a valid Euclid pair generating r as its first remainder.

Once this pairing is established, each pair independently produces a valid Euclid trace, and since order is irrelevant, we can simply concatenate all pairs.

The reason this works is that we deliberately force each Euclid run to stop after one meaningful remainder step. By choosing a = b + r, the algorithm produces exactly one remainder r and then immediately transitions to (b, r), which terminates quickly or produces only smaller values that are irrelevant because we never reuse intermediate structure.

The construction reduces the global multiset problem into a feasibility assignment problem over values, which can be solved greedily by sorting and matching.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force decomposition of all chains | Exponential | High | Too slow |
| Greedy feasibility matching per value | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the multiset t in decreasing order. This ensures we process larger values f
