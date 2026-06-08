---
title: "CF 2013C - Password Cracking"
description: "We are asked to recover a secret binary string of length $n$ through interactive queries. The string only contains 0s and 1s. Each query consists of proposing a binary string $t$ and learning whether it appears as a contiguous substring inside the secret string."
date: "2026-06-08T13:03:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "interactive", "strings"]
categories: ["algorithms"]
codeforces_contest: 2013
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 973 (Div. 2)"
rating: 1400
weight: 2013
solve_time_s: 35
verified: false
draft: false
---

[CF 2013C - Password Cracking](https://codeforces.com/problemset/problem/2013/C)

**Rating:** 1400  
**Tags:** constructive algorithms, interactive, strings  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to recover a secret binary string of length $n$ through interactive queries. The string only contains 0s and 1s. Each query consists of proposing a binary string $t$ and learning whether it appears as a contiguous substring inside the secret string. The goal is to reconstruct the entire string using at most $2n$ queries, because exceeding that will cause the interaction to terminate and return a wrong answer.

The constraints are moderate: $n$ can be up to 100 and there can be up to 100 test cases. This means that any solution that uses $O(n^2)$ queries would potentially require 10,000 queries in the worst case, which is far beyond the allowed $2n$ per test case. Therefore, we need a linear query strategy, ideally proportional to $n$. The small $n$ allows us to consider simple, concrete string manipulations without worrying about memory or excessive computation.

Non-obvious edge cases involve strings that are uniform, like all zeros or all ones, and strings with alternating patterns such as `010101`. A naive approach might assume a mix of zeros and ones and fail to construct such strings correctly. For instance, if the secret string is `1111` and the algorithm starts by appending zeros first, queries like `0` or `00` will return 0 repeatedly, which could mislead the reconstruction if the algorithm is not careful about trying both digits at each position.

## Approaches

The brute-force approach is straightforward: for each position in the string, try placing `0` and `1` and see if the resulting string is a substring of the secret. You extend the known prefix by one digit at a time, querying both options. This method is correct but has a subtle point: if you query all prefixes blindly, you could reach \
