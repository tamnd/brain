---
title: "CF 104842G - Game With Stones"
description: "We are given a line of $n$ boxes and several initial configurations of $m$ identical stones distributed across them. Each configuration is simply an array of $n$ nonnegative integers whose sum is fixed to $m$."
date: "2026-06-28T11:32:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104842
codeforces_index: "G"
codeforces_contest_name: "2020-2021 ICPC, Moscow Subregional"
rating: 0
weight: 104842
solve_time_s: 26
verified: false
draft: false
---

[CF 104842G - Game With Stones](https://codeforces.com/problemset/problem/104842/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of $n$ boxes and several initial configurations of $m$ identical stones distributed across them. Each configuration is simply an array of $n$ nonnegative integers whose sum is fixed to $m$.

A single move allows us to take one stone from a box and shift it to an adjacent box. The cost between two configurations is the minimum number of such unit moves needed to transform one distribution into another. This is exactly the same as moving mass along a path graph where moving one unit across an edge costs one.

We are given $k$ such configurations. The task is to choose a new configuration $b$ (also a valid distribution of $m$ stones) that minimizes the sum of transportation costs from every given configuration to $b$.

So we are searching for a “median distribution” under the Earth Mover Distance on a line.

The constraints imply $n, k \le 1000$ and $m \le 10^9$. Even though each array sums to $m$, $m$ is too large to simulate individual stones. Any solution that expands distributions into unit tokens is immediately impossible. We must work with prefix flow representations or cumulative quantities in $O(nk)$ or better.

A key structural edge case appears when distributions are highly concentrated. For example, one distribution could place all stones in box 1, another in box $n$. A naive averaging approach that tries to take coordinate-wise medians fails because the cost is not separable per coordinate; moving mass interacts across positions.

Another subtle case is when multiple optimal answers exist. The problem allows any, so we must avoid relying on uniqueness.

## Approaches

A brute force interpretation would be to enumerate all possible distributions $b$. The number of weak compositions of $m$ into $n$ parts is $\binom{m+n-1}{n-1}$, which is astronomically large for $m = 10^9$. Even constructing candidates is impossible, so we need a structural reformulation.

The key observation is that on a line, the cost $W(a, b)$ can be interpreted as the sum over edges of absolute differences of prefix sums. If we define

$$A_i(x) = \sum_{t \le x} a_i[t],
\quad
B(x) = \sum_{t \le x} b[t],$$

then the transportation cost becomes

$$W(a_i, b) = \sum_{x=1}^{n-1} |A_i(x) - B(x)|.$$

This converts the problem into choosing a function $B(x)$ with constraints $B(x)$ nondecreasing, $B(n) = m$, minimizing a sum of absolute deviations at each position.

Now the problem decouples over positions $x$, except for the monotonicity constraint of $B(x)$. At each cut between boxes, we are effectively choosing a value $B(x)$ that minimizes the sum of distances to $A_1(x), \dots, A_k(x)$. For a fixed $x$, this is a classic fact: the minimizer of sum of absolute deviations is any median of the multiset.

So locally, the best choice is the median prefix sum at each position. The remaining issue is ensuring consistency across positions, since $B(x)$ must be nondecreasing.

This leads to a sequence of medians that may violate monotonicity. The correction is to project this sequence onto the space of nondecreasing sequences, which is exactly isotonic regression under $L_1$ loss. In this setting, the optimal solution can be obtained by processing positions left to right and maintaining a structure that merges segments whose medians violate order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of distributions | exponential in $m$ | large | Too slow |
| Median prefix + isotonic merge | $O(kn)$ | $O(kn)$ | Accepted |

## Algorithm Walkthrough

We transform each distribution into its prefix sum array.

1. Compute prefix sums $A_i(x)$ for every input distribution. This converts each configuration into cumulative mass up to each position.
2. For each position $x$, collect the values $A_1(x), A_2(x), \dots, A_k(x)$. Sort them or maintain a structure that allows median extraction. The median gives the locally optimal valu_
