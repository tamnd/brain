---
title: "CF 1336C - Kaavi and Magic Spell"
description: "We have two strings, S of length n and T of length m. We start with an empty string A and can perform operations that remove the first character of S and append it either to the front or the back of A."
date: "2026-06-11T15:52:40+07:00"
tags: ["codeforces", "competitive-programming", "dp", "strings"]
categories: ["algorithms"]
codeforces_contest: 1336
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 635 (Div. 1)"
rating: 2200
weight: 1336
solve_time_s: 247
verified: false
draft: false
---

[CF 1336C - Kaavi and Magic Spell](https://codeforces.com/problemset/problem/1336/C)

**Rating:** 2200  
**Tags:** dp, strings  
**Solve time:** 4m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We have two strings, `S` of length `n` and `T` of length `m`. We start with an empty string `A` and can perform operations that remove the first character of `S` and append it either to the front or the back of `A`. The task is to count the number of operation sequences that result in `A` starting with `T`. Two sequences are different if they differ in the order or choice of front/back operations at any step. The answer must be reported modulo 998244353.

The constraint `n ≤ 3000` indicates that an algorithm with complexity O(n²) is feasible, but O(n³) would likely be too slow. A naive brute-force approach generating all 2ⁿ operation sequences is impossible because 2³⁰⁰⁰ is astronomically large. Edge cases include when `T` has length 1 or when all characters in `S` are identical, which could create many sequences producing the same prefix. A careless approach that only counts permutations without regard to order would fail on these inputs.

For example, if `S = "aa"` and `T = "a"`, then all four operation sequences (`front-front`, `front-back`, `back-front`, `back-back`) produce `A` starting with `T`. A naive approach counting only unique final strings would output 1, which is incorrect.

## Approaches

The brute-force method considers every sequence of operations. For each character in `S`, we have two choices, generating a binary tree of 2ⁿ possibilities. At each leaf, we check if `A` starts with `T`. This is correct but infeasible because even for `n = 20`, we would need to examine over a million sequences. For `n = 3000`, it is impossible.

The key insight is to notice that only the characters contributing to the first `m` positions of `A` matter, since we only care about `A` starting with `T`. We can model this as a dynamic programming problem. Let `dp[l][r]` denote the number of ways to build the substring `A[l..r]` such that it corresponds to some prefix of `T`. Initially, `dp[i][i]` represents the empty string. We can extend either the left or right side by consuming the next character from `S` and only update `dp[l][r]` if the resulting substring matches the corresponding prefix of `T`. This reduces complexity to O(n²), because for each of the n characters, we update O(n) intervals. The problem structure allows dynamic programming because the only relevant property is matching prefixes of `T`, independent of the exact sequence after `m` characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ) | O(n) | Too slow |
| Optimal (DP) | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Initialize a 2D array `dp` of size `(n+1) × (n+1)` with all zeros. Here `dp[l][r]` will store the number of ways to build `A[l..r]` such that it forms a prefix of `T` when characters are taken from `S[l..r]`.
2. For each position `i` in `0..n-1`, consider `S[i]`. For all intervals `[l, r]` that could be extended, if adding `S[i]` to the left forms a substring starting at `l-1` that matches the prefix of `T`, increment `dp[l-1][r]`. Similarly, if adding to the right forms a substring ending at `r+1` matching `T`, increment `dp[l][r+1]`.
3. Use modulo 998244353 for every increment.
4. After processing all characters of `S`, sum `dp[0][m-1]` for all valid intervals corresponding to `A` starting with `T`.

Why it works: The invariant is that `dp[l][r]` always counts the number of sequences that produce `A[l..r]` matching `T[l..r]`. Extending left or right correctly accumulates sequences because each operation is independent and sequences are distinguished by their exact operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

S = input().strip()
T = input().strip()
n = len(S)
m = len(T)

# dp[l][r] = number of ways to build substring corresponding to T[l..r]
dp = [[0] * (n+1) for _ in range(n+1)]

# base case: empty substring
for i in range(n):
    if
```
