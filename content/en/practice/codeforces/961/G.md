---
title: "CF 961G - Partitions"
description: "We are given $n$ weighted elements. Each element $i$ has a weight $wi$. We consider all ways to split these $n$ elements into exactly $k$ non-empty groups. Each such grouping is an unordered partition, so only the membership structure matters, not any labeling of groups."
date: "2026-06-17T01:47:40+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 961
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 41 (Rated for Div. 2)"
rating: 2700
weight: 961
solve_time_s: 25
verified: false
draft: false
---

[CF 961G - Partitions](https://codeforces.com/problemset/problem/961/G)

**Rating:** 2700  
**Tags:** combinatorics, math, number theory  
**Solve time:** 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given $n$ weighted elements. Each element $i$ has a weight $w_i$. We consider all ways to split these $n$ elements into exactly $k$ non-empty groups. Each such grouping is an unordered partition, so only the membership structure matters, not any labeling of groups.

For any fixed partition, its value is computed as follows. Every subset contributes a score equal to its size multiplied by the sum of weights inside it. The total value of the partition is the sum of these subset contributions. The task is to sum this value over all valid partitions into exactly $k$ subsets.

The difficulty is not in evaluating one partition, but in aggregating contributions over an enormous family of partitions, whose count grows roughly like Stirling numbers of the second kind, which is exponential in $n$. With $n$ up to $2 \cdot 10^5$, enumerating partitions is impossible, and even $O(n^2)$ is too slow.

A subtle issue appears if one tries to treat partitions independently per element or per subset size. For example, a naive idea might try to count how many times a weight appears in a subset of size $s$, but this ignores that the subset size distribution is coupled across all elements through the global constraint of having exactly $k$ subsets.

A small illustrative failure: if all weights are 1 and $n=3, k=2$, a naive attempt that treats elements independently might overcount configurations where different elements land in subsets of different sizes without respecting that partitions are global objects.

The correct solution must aggregate contributions by symmetry over elements, reducing the problem to counting how often a fixed element contributes across all partitions.

## Approaches

The key observation is linearity over elements. The partition weight is a sum over subsets, and each subset weight is itself a sum over elements, multiplied by subset size. Expanding everything, we rewrite the contribution of a partition $R$:

$$W(R) = \sum_{S \in R} |S| \sum_{i \in S} w_i$$

Swap summations:

$$W(R) = \sum_{i=1}^n w_i \cdot |S(i)|,$$

where $S(i)$ is the subset containing element $i$, and $|S(i)|$ is its size. So each element contributes its weight multiplied by the size of its own block.

Now the entire problem reduces to computing, for each element $i$, the total sum over all partitions of the size of the block containing $i$. By symmetry, this value is identical for all elements, so the answer becomes:

$$\left(\sum_{i=1}^n w_i\right) \cdot F(n,k),$$

where $F(n,k)$ is the total sum of sizes of the block containing a fixed element over all partitions into $k$ blocks.

We now fix element 1. Suppose its block has size $s$. Then we choose the remaining $s-1$ elements of its block in $\binom{n-1}{s-1}$ ways. After fixing this block, the remaining $n-s$ elements must be partitioned into $k-1$ blocks, contributing $S(n-s,k-1)$, the Stirling number of the second kind.

Thus:

$$F(n,$$
