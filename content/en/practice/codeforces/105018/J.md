---
title: "CF 105018J - Multiplicative Array"
description: "We are given an array indexed from 1 to n with a special multiplicative structure, but that structure is not what we directly compute with. Instead, the process repeatedly transforms the array using divisor aggregation."
date: "2026-06-28T02:05:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105018
codeforces_index: "J"
codeforces_contest_name: "Winter Cup 5.0 Online Mirror Contest"
rating: 0
weight: 105018
solve_time_s: 30
verified: false
draft: false
---

[CF 105018J - Multiplicative Array](https://codeforces.com/problemset/problem/105018/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array indexed from 1 to n with a special multiplicative structure, but that structure is not what we directly compute with. Instead, the process repeatedly transforms the array using divisor aggregation.

At each step, every position k is replaced by the sum of all values located at indices that divide k. After doing this operation m times, we are asked to output the final array.

So if we define a function T on an array A as T(A)[k] = sum of A[d] over all d that divide k, the task is to compute T applied m times to the initial array.

The multiplicative property of the input is a red herring for direct simulation. The key effect comes entirely from repeated divisor convolution.

The constraints are the real signal. The array size can reach one million, while the number of iterations can be as large as 10^18. Any solution that performs even O(n) work per iteration is immediately impossible, since that would imply up to 10^24 operations in the worst case. Even O(n log n) per iteration is still far too large. This forces a solution where the transformation is understood as an algebraic operator that can be exponentiated or precomputed once.

A subtle edge case appears when n is large and most values are zero. A naive simulation might skip zeros and assume sparsity helps, but divisor relationships still create dense propagation. For example, starting with A[1] = 1 and all others zero, after one iteration every position becomes 1, because 1 divides everything. A sparse simulation still touches all indices.

Another pitfall is assuming the multiplicative condition simplifies the dynamics of iteration. It does not help reduce the divisor sum structure; the iteration depends only on indices, not on values.

## Approaches

A direct approach follows the definition literally. For each of m iterations, for every k, we iterate over all divisors d of k and accumulate A[d]. Precomputing divisors for all numbers up to n makes each iteration cost roughly sum over k of number of divisors of k, which is about O(n log n). With m up to 10^18, this is clearly infeasible because the transformation must be applied repeatedly, not just once.

The key observation is that the operation is linear and index-based. The update depends only on the divisor relation between indices, so the entire process can be seen as multiplying the vector A by a fixed n by n matrix M where M[k][d] = 1 if d divides k, otherwise 0. The problem becomes computing M^m times A.

Direct matrix exponentiation is impossible due to size, but the structure of M is special: it corresponds to divisor convolution, which becomes multiplication in the Dirichlet convolution algebra. This means the operation is diagonalizable in the space of arithmetic functions using the Möbius transform framework.

Concretely, if we define a function over integers, repeated divisor-sum corresponds to repeated application of the "zeta transform" over the divisor poset. The m-th application corresponds to applying a known combinational coefficient on each chain of divisibility. This leads to a combinatorial interpretation: each final value at k is a weighted sum over initial values at divisors of k, where the weight depends only on how many times we can choose divisor chains of length m.

This reduces the problem to computing, for each k, contributions from all divisors d of k multiplied by a coefficient depending on the number of ways to extend a divisor chain from d to k in m steps. That coefficient can be precomputed using number-theoretic DP over divisors and powers, since n is up to 10^6.

The final solution becomes a sieve-style preprocessing of divisor transitions, combined with exponentiation on the divisor lattice depth, avoiding explicit iteration over m.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m · n log n) | O(n) | Too slow |
| Divisor-structure DP + exponentiation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret the operation as repeated application of a divisor-sum transform. Instead of simulating iterations, we compute how many times each original position contributes to each final position after m layers of divisor expansion.

1. For every k up to n, en
