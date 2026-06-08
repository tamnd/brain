---
title: "CF 1924D - Balanced Subsequences"
description: "We are working with strings made only from two types of parentheses, and we fix how many opening and closing brackets we must use. Each test case gives three numbers: how many '(' we must place, how many ')' we must place, and a target parameter k."
date: "2026-06-08T19:07:39+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1924
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 921 (Div. 1)"
rating: 2700
weight: 1924
solve_time_s: 32
verified: false
draft: false
---

[CF 1924D - Balanced Subsequences](https://codeforces.com/problemset/problem/1924/D)

**Rating:** 2700  
**Tags:** combinatorics, dp, math  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with strings made only from two types of parentheses, and we fix how many opening and closing brackets we must use. Each test case gives three numbers: how many '(' we must place, how many ')' we must place, and a target parameter k.

Among all possible ways to arrange these brackets, we care about the longest balanced subsequence. A balanced subsequence is defined in the usual bracket sense: after deleting some characters (without reordering), we should be able to match parentheses so that it behaves like a valid expression. The key twist is that we do not require the whole string to be balanced, only that some subsequence can be fully matched, and we measure the maximum possible size of such a subsequence.

The task is to count how many distinct bracket sequences produce a longest balanced subsequence of exactly length 2k.

The constraints are tight: each of n, m, k can be up to 2000, and there are up to 3000 test cases. Any solution that tries to enumerate sequences or simulate subsequences directly will immediately fail, since the number of sequences itself is on the order of binomial coefficients like C(4000, 2000), which is astronomically large. Even dynamic programming that is cubic or worse per test case is not viable; we need something close to O(nm) or better per test.

A subtle edge case appears when k is large compared to min(n, m). For example, if n = m = 2 and k = 2, only fully balanced sequences contribute, because the longest possible balanced subsequence cannot exceed 4. If k is too large relative to available parentheses, the answer becomes zero immediately. A naive solution might still attempt to count configurations and overcount impossible states.

Another important corner case is when k is small. For instance, if k = 1, we are forcing the longest balanced subsequence to be exactly two characters, meaning no pair of matching parentheses can be fully embedded in a longer structure. This strongly restricts nesting and is easy to mis-handle in greedy reasoning.

## Approaches

The brute-force approach would enumerate all strings with n opening and m closing brackets and, for each string, compute its longest balanced subsequence using a stack-like or DP matching process. Computing the best balanced subsequence of a fixed string is linear, but the number of strings is C(n+m, n), which is exponential in input size. Even for n = m = 20 this already becomes infeasible, so enumeration is completely out of reach.

We need to replace “checking each sequence independently” with “counting all sequences by structure”.

The key structural observation is that the longest balanced subsequence of a bracket sequence depends only on how many pairs can be matched in an optimal subsequence, which is equivalent to the maximum number of correctly paired '(' and ')' that can be extracted while preserving order. This maximum is governed by how many prefixes allow enough unmatched ')' and how many '(' remain available for pairing later. In effect, any sequence induces a greedy matching process: scan left to right, maintain a balance counter, and match whenever possible. This greedy matching produces the maximum number of pairs in any subsequence, so the problem reduces to counting sequences whose greedy matching produces exactly k pairs.

This transforms the problem into a constrained lattice path counting problem. We think of '(' as +1 and ')' as -1, and we simulate the balance, but we do not require it to stay non-negative. Instead, we track how many matches are actually formed in the best subsequence, which corresponds to how many times a ')' finds a previous unmatched '(' in an optimal pairing process.

The standard trick is to reinterpret the process as DP over prefix length and current balance, but that is still too large. The real simplification is to observe that only the difference between available opens and closes and how many matches have already been formed matters. Once we fix that the optimal subsequence has k matches, we are effectively choosing which k ')' symbols will be matched with which k '(' symbols, while ensuring feasibility constraints on ordering are satisfied.

This leads to a combinatorial DP where we process the string left to right, tracking three quantities: how many '(' and ')' we have used so far, and how many pairs we have already formed in the optimal matching. The transition depends only on whether the next character is '(' or ')', and whether it is used to form a new potential match or becomes unmatched. The DP state space is O(nm) per test case.

To make this efficient across all test cases, we precompute factorials and inverse factorials up to 4000 to handle binomial transitions if needed, and reuse DP tables carefully.

In summary, brute force fails because it enumerates structures explicitly, while the optimized solution compresses a
