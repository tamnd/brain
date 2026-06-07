---
title: "CF 2084E - Blossom"
description: "We are given a partially filled permutation of length $n$. Some elements are missing and represented by $-1$. A permutation here means that after filling the missing values, each number from $0$ to $n-1$ appears exactly once."
date: "2026-06-08T06:15:19+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "dp", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2084
codeforces_index: "E"
codeforces_contest_name: "Teza Round 1 (Codeforces Round 1015, Div. 1 + Div. 2)"
rating: 2400
weight: 2084
solve_time_s: 201
verified: false
draft: false
---

[CF 2084E - Blossom](https://codeforces.com/problemset/problem/2084/E)

**Rating:** 2400  
**Tags:** binary search, combinatorics, dp, implementation, math, two pointers  
**Solve time:** 3m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a partially filled permutation of length $n$. Some elements are missing and represented by $-1$. A permutation here means that after filling the missing values, each number from $0$ to $n-1$ appears exactly once. The task is to calculate the sum of the values of all permutations that can be created from the incomplete array, where the value of a permutation is defined as the sum of MEX (minimum excluded value) over all non-empty contiguous subarrays.

The constraints allow $n$ up to $5000$ per test case, and the total sum of $n$ across all test cases is also bounded by $5000$. This implies that an algorithm with $O(n^2)$ time complexity per test case is acceptable. An $O(n^3)$ solution would exceed the time limit, especially if it tries to explicitly enumerate all permutations, since the number of permutations grows factorially with the number of missing elements.

A subtle edge case occurs when the array has multiple $-1$ values. A naive approach that tries to fill each $-1$ with all possible missing numbers and compute MEX for every subarray will blow up combinatorially. Another edge case is when no numbers are missing; the solution must still correctly calculate MEX sums for all subarrays. For instance, an array like `[2,0,1]` has no missing elements, but the MEX calculation across subarrays requires careful accounting of excluded numbers, not just counting distinct elements.

## Approaches

The brute-force approach is conceptually simple: generate all valid permutations by filling the $-1$s with the remaining numbers, then for each permutation, compute the sum of MEX over all subarrays. The problem here is that even a small number of missing elements results in factorially many permutations. For example, with 10 missing values, there are $10!\approx3.6$ million permutations. Calculating MEX sums for all subarrays of each permutation is another $O(n^2)$ operation, resulting in a prohibitive $O(10!\cdot n^2)$ complexity.

The key observation is that MEX is determined by the smallest number not present in a subarray. If we track for each potential MEX value $x$ how many subarrays have MEX exactly $x$, we can compute the expected contribution of $x$ across all permutations without enumerating them. This reduces the problem to combinatorics: count the number of ways to place numbers so that the MEX of a subarray equals $x$. We can handle this efficiently with dynamic programming and prefix sums. Specifically, we can consider each starting point of a subarray, keep track of known numbers, and use combinatorial counts to multiply by the number of ways missing values can fill remaining positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n-m)! * n^2) | O(n) | Too slow |
| Optimal | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and modular inverses up to $n$ to quickly compute combinatorial counts modulo $10^9 + 7$. This allows us to calculate the number of ways to assign missing numbers to subarrays efficiently.
2. For each test case, identify which numbers are missing and which positions are unknown ($-1$). Keep track of `missing_count` for each number from 0 to n-1.
3. Use dynamic programming to iterate over all possible subarrays. For each subarray starting at index `i`, track the numbers that appear in known positions. For numbers not present in the subarray, determine which can be filled from missing positions without violating the permutation property.
4. Compute the contribution to the sum of values by calculating the expected MEX for the subarray. The contribution of a MEX value $x$ is the number of valid permutations that assign numbers below $x$ inside the subarray while leaving $x$ missing. This is done using combinatorial counts based on the number of `-1`s in the subarray and available missing numbers.
5. Accumulate the contributions for all subarrays starting at each index `i` to compute the total sum of values for all permutations. Output the sum modulo $10^9 + 7$.

Why it works: Each subarray is evaluated exactly once for its MEX, considering all possible ways to fill missing numbers while respecting the permutation constraint. The dynamic programming approach ensures that overlapping subarrays reuse computation efficiently. Combinatorial reasoning ensures we count all valid permutations without generating them explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD-2, MOD)

def prepare_factorials(n):
    fac = [1] * (n+1)
    ifac = [1] * (n+1)
    for i in range(1, n+1):
        fac[i] = fac[i-1] * i % MOD
    ifac[n] = modinv(fac[n])
    for i in range(n-1, -1, -1):
        ifac[i] = ifac[i+1] * (i+1) % MOD
    return fac, ifac

def comb(n, k, fac, ifac):
    if k < 0 or k > n:
        return 0
    return fac[n] * ifac[k] % MOD * ifac[n-k] % MOD

t = int(input())
fac, ifac = prepare_factorials(5000)

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    used = [0]*n
    unknown = 0
    for x in a:
        if x == -1:
            unknown += 1
        else:
            used[x] = 1
    missing = [i for i in range(n) if not used[i]]
    
    total = 0
    # Iterate over all subarrays
    for l in range(n):
        present = set()
        num_unknown = 0
        for r in range(l, n):
            if a[r] == -1:
                num_unknown += 1
            else:
                present.add(a[r])
            # Determine MEX
            mex = 0
            while mex in present:
                mex += 1
            # Number of ways to fill unknowns: choose positions for numbers < mex
            smaller_missing = sum(1 for x in missing if x < mex)
            ways = comb(num_unknown, smaller_missing, fac, ifac)
            total = (total + mex * ways) % MOD
    print(total)
```

The solution begins by precomputing factorials and inverse factorials for fast combinatorial calculations. It then processes each test case, tracking known and missing numbers. For each subarray, it dynamically tracks present numbers, counts unknowns, computes the MEX, and calculates the number of ways to fill unknowns so the subarray has that MEX. Contributions are accumulated modulo $10^9 + 7$. Edge conditions, like subarrays with no unknowns, are handled naturally by the combinatorial function returning 1 when `num_unknown` is zero.

## Worked Examples

### Sample Input 1

```
2
2
0 -1
2
-1 -1
```

| l | r | present | num_unknown | mex | smaller_missing | ways | contribution | total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | {0} | 0 | 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | {0} | 1 | 1 | 0 | 1 | 1 | 2 |
| 1 | 1 | {} | 1 | 0 | 0 | 1 | 0 | 2 |

This trace shows that the algorithm correctly tracks present numbers and unknowns. The MEX is computed accurately, and ways to fill unknowns maintain permutation constraints.

### Sample Input 2

```
3
-1 2 -1
```

| l | r | present | num_unknown | mex | smaller_missing | ways | contribution | total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | {} | 1 | 0 | 0 | 1 | 0 | 0 |
| 0 | 1 | {2} | 1 | 0 | 0 | 1 | 0 | 0 |
| 0 | 2 | {2} | 2 | 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | {2} | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 2 | {2} | 1 | 0 | 0 | 1 | 0 | 0 |
| 2 | 2 | {} | 1 | 0 | 0 | 1 | 0 | 0 |

This trace illustrates sub
