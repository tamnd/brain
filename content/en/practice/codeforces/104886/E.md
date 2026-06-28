---
title: "CF 104886E - Random Tree Path Match"
description: "We are given a rooted tree with a weight on every vertex. For each query, we look at two nodes, take the unique simple path from the root to each of them, and then try to “align” these two root-to-node paths."
date: "2026-06-28T09:06:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104886
codeforces_index: "E"
codeforces_contest_name: "USI-Team-Selection 2023-2024"
rating: 0
weight: 104886
solve_time_s: 29
verified: false
draft: false
---

[CF 104886E - Random Tree Path Match](https://codeforces.com/problemset/problem/104886/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with a weight on every vertex. For each query, we look at two nodes, take the unique simple path from the root to each of them, and then try to “align” these two root-to-node paths.

The task is not to compare the paths directly as sequences, but to pick two subsequences, one from each root-to-node path, with the same length. Once we pick such a pair of subsequences, we pair elements position-wise and compute the sum of products of the corresponding weights. The goal for each query is to maximize this value.

So conceptually, we are choosing a sequence of matched nodes along two root-to-node paths, preserving order in both, and maximizing a dot product between the chosen weights.

The tree itself is not adversarial; it is generated randomly with each node attaching to a uniformly chosen earlier node. That detail is not decorative. It ensures that typical root-to-node paths are short on average, but worst-case depth is still linear, so any solution must work for worst-case path length.

A naive interpretation would suggest comparing all subsequence pairs, but that already hints at exponential blow-up. Even restricting to dynamic programming over two sequences would still cost quadratic per query in worst cases, which is far too large if there are many queries.

A subtle but important edge case appears when one path is a prefix of the other or when both paths share a long prefix and then diverge. In these cases, many candidate subsequence matches collapse into structurally similar alignments, and naive DP recomputes the same transitions repeatedly.

For example, if both nodes are deep descendants of 1 and their paths are almost identical except for a small suffix divergence, recomputing full DP per query wastes work proportional to the full depth even though only a small suffix differs.

## Approaches

A direct brute force approach treats each query independently. We extract the two root-to-node sequences and run a classic longest common subsequence style dynamic programming, but instead of maximizing length we maximize weighted dot product. For sequences of length d1 and d2, this DP costs O(d1 · d2). In a degenerate tree where depth is O(n), a single query becomes quadratic. With up to 10^5 queries, this is completely infeasible.

The key structural observation is that both sequences are root paths in the same tree. That means they are not arbitrary arrays: they share a long prefix, and only diverge after their lowest common ancestor. If we decompose both paths into the segment from root to LCA and from LCA downwar
