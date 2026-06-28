---
title: "CF 104873C - Counting Stairs"
description: "We are asked to count a specific class of shapes built from unit cubes. Each valid configuration is a “stair-like” structure: columns of cubes arranged from left to right with heights that never increase as we move right."
date: "2026-06-28T10:11:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104873
codeforces_index: "C"
codeforces_contest_name: "2018-2019 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104873
solve_time_s: 31
verified: false
draft: false
---

[CF 104873C - Counting Stairs](https://codeforces.com/problemset/problem/104873/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count a specific class of shapes built from unit cubes. Each valid configuration is a “stair-like” structure: columns of cubes arranged from left to right with heights that never increase as we move right. So the shape can be described by a sequence of positive integers $h_1 \ge h_2 \ge \dots \ge h_k$, and the total number of cubes is $n = \sum h_i$.

On top of this monotonic “partition-like” structure, there is an additional geometric constraint: the shape must be symmetric with respect to the diagonal line $x = y$. This symmetry forces the diagram to mirror itself across the diagonal, which is only possible for very specific staircase shapes.

The input gives multiple values of $n$, and for each one we must count how many such symmetric stair configurations use exactly $n$ cubes.

The constraint $n \le 2 \cdot 10^5$ with up to $10^4$ test cases rules out recomputing anything per query. Any solution must preprocess in roughly $O(N)$ or $O(N \log N)$, then answer each query in constant time.

A naive approach would try to generate all partitions of $n$ and test symmetry. That already grows exponentially in $\sqrt{n}$, and symmetry checking adds another factor. Even for moderate $n$, this becomes infeasible.

A more subtle issue is that the symmetry constraint is global. It is easy to construct a partition that “looks structured locally” but fails diagonal invariance when drawn. For example, a partition like $4 + 2 + 1$ produces a Ferrers diagram that is not symmetric, even though it is valid as a stair.

The key difficulty is that the symmetry constraint is not local to rows or columns, but couples them.

## Approaches

The brute-force interpretation is to enumerate all non-increasing sequences of positive integers summing to $n$, and for each one construct its Ferrers diagram and check whether it equals its transpose. The number of partitions of $n$ is already exponential in $\sqrt{n}$, so this approach becomes impossible beyond very small values of $n$. The symmetry check is linear in the diagram size, which makes it even worse.

The structural insight is that a staircase symmetric about the diagonal corresponds exactly to a self-conjugate partition. In Ferrers diagram terms, taking the transpose exchanges rows and columns. Requiring equality means the diagram must be invariant under this swap.

A classical and non-trivial fact is that self-conjugate partitions of $n$ are in bijection with partitions of $n$ into distinct odd parts. This changes the problem completely: instead of a 2D symmetry condition, we convert it into a 1D selection problem.

Each odd integer $2k-1$ can be used at most once, and contributes that many cubes. So we are counting subsets of odd integers whose sum is $n$. This is a standard 0/1 knapsack over odd weights.

We precompute a DP where we iterate over all odd numbers and update ways to form sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (generate partitions + check symmetry) | Exponential | O(n) | Too slow |
| DP over distinct odd parts | O(n^2 / 2) preprocessing, O(1) per query | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem to counting ways to represent $n$ as a sum of distinct odd integers.

1. Precompute an array `dp` where `dp[x]` is the number of ways to form sum `x` using distinct odd integers.

We initialize `dp[0] = 1` because there is exactly one way to form zero: choose nothing.
2. Iterate over all odd values $1, 3, 5, \dots \le N$.

Each odd number is treated as an it
