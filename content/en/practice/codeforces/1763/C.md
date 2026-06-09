---
title: "CF 1763C - Another Array Problem"
description: "We are given an array of integers, and we are allowed to repeatedly apply a very specific transformation: pick two positions $i < j$, compute the absolute difference of the values at the ends, and overwrite the entire segment $[i, j]$ with that single value."
date: "2026-06-09T13:35:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1763
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 840 (Div. 2) and Enigma 2022 - Cybros LNMIIT"
rating: 2000
weight: 1763
solve_time_s: 160
verified: false
draft: false
---

[CF 1763C - Another Array Problem](https://codeforces.com/problemset/problem/1763/C)

**Rating:** 2000  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we are allowed to repeatedly apply a very specific transformation: pick two positions $i < j$, compute the absolute difference of the values at the ends, and overwrite the entire segment $[i, j]$ with that single value.

This operation is powerful because it collapses whole intervals into a constant block. After enough operations, the array becomes piecewise constant, and every operation effectively replaces a segment by a value that depends only on its endpoints.

The goal is to choose a sequence of such segment collapses so that the final sum of the array is as large as possible. Since every operation reduces structure but can increase or decrease values depending on chosen endpoints, the problem is about understanding what values can be “generated” and how they propagate.

The constraints are large, with total array size up to $2 \cdot 10^5$ across all test cases, so any solution must be linear or near-linear per test. This immediately rules out any simulation of operations or interval DP that considers all segments, since that would be at least quadratic.

A common failure mode here is assuming that local greedy merges are sufficient. For example, trying to repeatedly apply the best immediate gain operation fails because early choices can destroy the ability to generate larger differences later. The process is globally constrained through reachability of values, not local improvement.

## Approaches

A brute force perspective would simulate all possible operations. Each operation picks a pair $(i, j)$ and replaces a segment, so the state space grows exponentially. Even for $n = 20$, the number of possible sequences explodes because every merge changes all future valid differences. This is completely infeasible.

The key structural observation is that the operation does not preserve ordering in a complicated way, it only depends on differences of chosen endpoints. Once we view the array as a set of values, the operation repeatedly introduces values that are absolute differences of existing ones. This is exactly the closure process under subtraction.

The crucial simplification is that the final achievable values form a set closed under absolute difference, which implies they are all multiples of the gcd of pairwise differences in the initial array. Once this invariant is identified, the process becomes purely arithmetic: the smallest step size that can ever appear is the gcd of differences, and every value in the final optimal configuration lies on an arithmetic progression determined by this gcd.

The optimal strategy effectively spreads this progression across the interval from minimum to maximum value, because nothing outside this range can be created, and everything inside aligned to the gcd can be reached.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | exponential | Too slow |
| GCD-based structure | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to understanding the structure of all values reachable via repeated interval difference operations.

1. Compute the minimum and maximum element in the array. These define the bounds of any value that can ever appear after operations, since all constructed values come from differences of existing elements.
2. Compute the greatest common divisor of all differences $a_i - a_1$. This captures the invariant step size of the system, because every operation produces absolute differences that preserve divisibility by this gcd.
3. Interpret this gcd as the fundamental unit of the reachable set. Every value that can appear is congruent modulo this gcd to the original elements, and repeated operations fill all reachable intermediate points.
4. The final configuration that maximizes the sum corresponds
