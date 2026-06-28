---
title: "CF 104743E - Range Modulo Queries"
description: "We are given two arrays of the same length. For every query interval, we are asked to find a modulus value $m$ such that when we take every element $ai$ in that interval and compute $ai bmod m$, we obtain exactly the corresponding $bi$."
date: "2026-06-29T01:21:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104743
codeforces_index: "E"
codeforces_contest_name: "TheForces Round #25(5^2-Forces)"
rating: 0
weight: 104743
solve_time_s: 35
verified: false
draft: false
---

[CF 104743E - Range Modulo Queries](https://codeforces.com/problemset/problem/104743/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays of the same length. For every query interval, we are asked to find a modulus value $m$ such that when we take every element $a_i$ in that interval and compute $a_i \bmod m$, we obtain exactly the corresponding $b_i$. Among all such valid $m$, we need the smallest positive one. If no positive integer works, the answer is $-1$.

The key difficulty is that each query is independent and asks about a subarray constraint that involves modular arithmetic, which is not directly composable in a naive way. The modulus must work simultaneously for all indices in the interval, which means a single global constraint must be extracted from local conditions.

The constraints are large: the total length and number of queries across all test cases sum up to $10^6$. This immediately rules out any per-query linear scan over the range. Even $O(n \log n)$ per test case would be too slow if repeated per query. The intended solution must reduce each query to a small number of precomputed range queries and then answer each query in near constant or logarithmic time.

A subtle issue appears in the meaning of modular equality. The condition $a_i \bmod m = b_i$ is only valid if $b_i < m$. This constraint is easy to miss, but it becomes critical when $b_i$ is large or when the optimal $m$ is close to the values in the arrays.

A second subtle edge case occurs when all $a_i = b_i$ in a segment. In that case, any modulus larger than all $a_i$ is valid, so the answer is not tied to divisibility constraints in the usual way.

## Approaches

Start from a brute force perspective. For a single query $[l, r]$, we could try all possible values of $m$ from $1$ up to the maximum value in the arrays and check whether it satisfies $a_i \bmod m = b_i$ for all $i$ in the range. This is straightforward to implement, since checking a candidate $m$ costs $O(r-l+1)$. However, the outer loop over $m$ up to $10^6$ makes this completely infeasible. A single query could require up to $10^{11}$ operations in the worst case.

To improve this, we reverse the viewpoint. Instead of testing $m$, we derive constraints that every valid $m$ must satisfy.

From $a_i \bmod m = b_i$, we rewrite $a_i = k_i m + b_i$, which implies that $a_i - b_i$ must be divisible by $m$. So every valid $m$ must divide all values $a_i - b_i$ in the query range. This turns the problem into a divisibility constraint over a range, which suggests using a range gcd.

There is also the hidden constraint $b_i < m$, meaning $m$ must exceed the maximum $b_i$ in the range.

So each query reduces to finding the smallest divisor $m$ of the range gcd of $(a_i - b_i)$ that is strictly greater th
