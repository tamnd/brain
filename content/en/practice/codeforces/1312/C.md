---
title: "CF 1312C - Adding Powers"
description: "We are given an array of non-negative integers, and a base $k ge 2$. Starting from an array of zeroes of the same length, we can repeatedly pick a step $i$ and add $k^i$ to any single element of the array, or skip the step."
date: "2026-06-11T17:11:42+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "implementation", "math", "number-theory", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1312
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 83 (Rated for Div. 2)"
rating: 1400
weight: 1312
solve_time_s: 68
verified: false
draft: false
---

[CF 1312C - Adding Powers](https://codeforces.com/problemset/problem/1312/C)

**Rating:** 1400  
**Tags:** bitmasks, greedy, implementation, math, number theory, ternary search  
**Solve time:** 1m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers, and a base $k \ge 2$. Starting from an array of zeroes of the same length, we can repeatedly pick a step $i$ and add $k^i$ to any single element of the array, or skip the step. The goal is to determine if there exists a sequence of such additions that transforms the zero array into the target array.

The input consists of multiple test cases. For each, we have the array length $n$ up to 30 and the target array elements up to $10^{16}$. The base $k$ can be up to 100. Since the maximum array length is small, we can afford operations linear in $n$ or logarithmic in the largest number. However, any approach that enumerates all subsets of powers for all positions becomes infeasible because each number can have up to $\log_k(10^{16})\approx 27$ powers, and we have $n$ numbers. That would explode combinatorially.

Non-obvious edge cases arise when multiple numbers require the same power of $k$. For instance, if the array is `[1,1]` and $k=2$, we would need two occurrences of $2^0=1$. Since each power can only be assigned to one position per step, this is impossible. Another edge case is arrays containing zeroes, which can be satisfied trivially by skipping all steps.

## Approaches

The brute-force approach is to generate all sequences of adding powers of $k$ to positions. For each power $k^i$, we can try adding it to any position or skip. This works because every sequence is valid, but it is extremely inefficient: with up to 27 powers per number and $n$ numbers, we have roughly $n^{\log_k(a_{max})} \sim 30^{27}$ combinations, which is astronomically large.

The key insight comes from representing numbers in a modified base-$k$ system. Any number can be uniquely expressed as a sum of powers of $k$, where each power appears at most once per position. Since we can assign each power of $k$ to at most one element of the array, we can iterate over the numbers and decompose them greedily into powers of $k$. If any power needs to be used more than once across the array, it is impossible. This reduces the problem to a counting problem on the exponents of $k$ in each number.

This observation transforms the problem into iterating over each number, repeatedly dividing by $k$ and recording the remainder. The remainder must be 0 or 1 for each power; otherwise, the number requires the same power multiple times. Summing up the counts of each power across the array, if any count exceeds 1, we cannot construct the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 2^max_exponent) | O(n * max_exponent) | Too slow |
| Optimal (greedy base-k decomposition) | O(n * log_k(a_max)) | O(log_k(a_max)) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array length $n$ and base $k$, and the target array $a$.
2. Initialize an empty map (or dictionary) `count` to track how many times each power of $k$ is used across
