---
title: "CF 190C - STL"
description: "We are given a sequence of tokens that were spoken in order, each token being either int or pair. These tokens are supposed to form a valid nested type expression of a very specific grammar."
date: "2026-06-03T01:19:24+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1500
weight: 190
solve_time_s: 43
verified: false
draft: false
---

[CF 190C - STL](https://codeforces.com/problemset/problem/190/C)

**Rating:** 1500  
**Tags:** dfs and similar  
**Solve time:** 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of tokens that were spoken in order, each token being either `int` or `pair`. These tokens are supposed to form a valid nested type expression of a very specific grammar. The grammar is fully binary: every `int` is a leaf type, and every `pair` combines exactly two previously formed types into a new one.

The task is to determine whether we can insert angle brackets and commas so that the sequence becomes a correctly structured type, and if so, reconstruct that exact structure. If multiple valid structures were possible, we would have ambiguity, but the problem guarantees uniqueness whenever a solution exists.

This immediately suggests we are parsing a binary tree structure from a preorder-like stream where every internal node consumes exactly two children. The difficulty is that the input is not explicitly structured, so we must infer grouping purely from the sequence.

The constraint `n ≤ 10^5` (where `n` is the number of `int` tokens) implies the total number of tokens is also `O(n)`, so any solution must be linear or near-linear. A quadratic or backtracking parsing approach would explode because every placement decision could branch into multiple recursive interpretations.

A subtle edge case appears when the structure is impossible even though counts match superficially. For example, a sequence like `int pair` already violates grammar because a complete type must start with a construct that can be expanded, not end prematurely. Another failure case is when we have too many `int` tokens early, leaving no room for pending `pair` expansions.

## Approaches

A brute-force interpretation would try to simulate all possible ways to assign parentheses around the sequence, essentially trying every binary tree shape whose leaves are `int` tokens and internal nodes are `pair`. Each `pair` consumes two subtrees, so this is equivalent to enumerating all full binary tree structures over the sequence positions and checking whether the sequence of tokens matches a valid labeling.

The number of such structures grows exponentially. Even for moderate lengths, the Catalan-number explosion makes this infeasible. The core inefficiency is that we repeatedly reconsider the same suffixes of the sequence under different partial tree shapes.

The key observation is that the grammar is deterministic if we interpret it as a streaming construction problem. Every
