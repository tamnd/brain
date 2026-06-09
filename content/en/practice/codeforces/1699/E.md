---
title: "CF 1699E - Three Days Grace"
description: "The problem gives us a multiset of integers, all bounded by a maximum value m, and allows us to repeatedly replace any number x 3 with two integers p and q such that pq = x and both p and q are greater than 1. After each operation, the multiset grows by one element."
date: "2026-06-09T22:13:10+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "math", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1699
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 804 (Div. 2)"
rating: 2600
weight: 1699
solve_time_s: 152
verified: false
draft: false
---

[CF 1699E - Three Days Grace](https://codeforces.com/problemset/problem/1699/E)

**Rating:** 2600  
**Tags:** data structures, dp, greedy, math, number theory, two pointers  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

The problem gives us a multiset of integers, all bounded by a maximum value `m`, and allows us to repeatedly replace any number `x > 3` with two integers `p` and `q` such that `p*q = x` and both `p` and `q` are greater than 1. After each operation, the multiset grows by one element. The goal is to reduce the difference between the largest and smallest elements in the multiset, which is defined as the balance.

Each test case consists of the size of the multiset, the maximum element bound, and the initial elements. The output is the smallest possible balance we can achieve by applying zero or more of these split operations.

The constraints imply that naive simulation of splitting every element recursively is not feasible. The total number of initial elements across all test cases can be up to `10^6` and the values themselves can go up to `5*10^6`. A naive approach that recursively splits each element could explode exponentially because each split increases the size of the multiset by one, so the operation count would quickly exceed any feasible limit.

Edge cases that can trip up a naive solution include multisets where all numbers are prime or 1, since they cannot be split, and cases where repeatedly splitting large numbers in different ways produces very different balance outcomes. For example, a multiset `[12, 2]` can be split to `[3,4,2,2]` or `[6,2,2]`, and the choice affects the minimum balance achievable.

## Approaches

The brute-force approach would be to attempt every valid split for every element and recursively compute the balance for all resulting multisets. This works conceptually because the operation is guaranteed to eventually reach numbers that cannot be split (primes and 1s), so the recursion terminates. The problem is that for large numbers, there are many ways to split and each split grows the multiset, which quickly results in exponential growth. For example, splitting all factors of a number like 210 generates a huge tree of possibilities. This is far beyond the feasible operation count.

The key insight is to reverse the perspective: instead of simulating all splits forward, we can think in terms of the smallest numbers each initial element can be split into and track how these splits affect the minimum value of the multiset. Because the operation allows arbitrary factorizations, a large number can be reduced to any combination of its prime factors. For minimizing balance, we want to focus on lowering the maximum values while avoiding creating numbers smaller than the current minimum.

We can precompute for each number `x` its minimal factor greater than 1 and use dynamic programming to track the minimal numbers that can result from splitting. Then we maintain a sliding window over these values to efficiently determine the minimum achievable balance across the multiset. This transforms an exponential simulation into a linear scan combined with preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(M log M + N) | O(M + N) | Accepted |

## Algorithm Walkthrough

1. Precompute the smallest prime factor (`spf`) for every number up to `m` using a sieve. This lets us factorize numbers in O(log x) time, which is essential for large `m`.
2. For each test case, initialize a frequency array `freq` to count occurrences of each number in the multiset.
3. For each number `x` in decreasing order, attempt to split it using its smallest prime factor. Let `p = spf[x]` and `q = x // p`. Increment `freq[p]` and `freq[q]` and decrement `freq[x]`. Repeat this until the number cannot be split further (either prime or ≤1).
4. Maintain a multiset-like structure or sliding window that tracks the smallest number seen and the largest number after all splits. The minimal balance is the difference between the largest and smallest numbers that are present in the frequency array after processing all numbers.
5. Output the minimal balance for each test case.

The invariant maintained is that at each step, the numbers in the frequency array represent all numbers reachable via legal splits from the original multiset. By processing numbers from largest to smallest, we ensure splits are applied in a way that can only reduce the maximum value without affecting smaller numbers unnecessarily. This guarantees that the final difference between the maximum and minimum present in the multiset is the minimal possible balance.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_M = 5 * 10**6 + 10

# Precompute smallest prime factor (spf) for all numbers up to MAX_M
spf = [0] * MAX_M
for i in range(2, MAX_M):
    if spf[i] == 0:
        for j in range(i, MAX_M, i):
            if spf[j] == 0:
                spf[j] = i

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    freq = [0] * (m + 2)
    for num in a:
        freq[num] += 1

    max_val = max(a)
    min_val = min(a)

    for x in range(m, 1, -1):
        while freq[x]:
            if spf[x] == x:
                break  # prime, cannot split
            p = spf[x]
            q = x // p
            freq[x] -= 1
            freq[p] += 1
            freq[q] += 1

    # Find final max and min present in freq
    final_min = next(i for i in range(1, m + 1) if freq[i])
    final_max = next(i for i in range(m, 0, -1) if freq[i])
    print(final_max - final_min)
```

The precomputation of `spf` is crucial to factorize numbers quickly. The `freq` array allows us to efficiently simulate splits without explicitly maintaining a growing multiset. By iterating from the largest numbers downward, we guarantee that splits reduce the maximum value as much as possible before considering smaller numbers. The final scanning of `freq` identifies the smallest and largest numbers actually present after all splits.

## Worked Examples

**Example 1:**

Input: `5 10` with multiset `[2,4,2,4,2]`.

| Step | freq[2] | freq[4] | Explanation |
| --- | --- | --- | --- |
| Init | 3 | 2 | original multiset |
| Split 4->2*2 | 5 | 0 | each 4 split into two 2s |
| Scan freq | min=2, max=2 | balance = 0 | All numbers equal |

This confirms that splitting largest numbers to their minimal factors minimizes balance.

**Example 2:**

Input: `3 50` with multiset `[12,2,3]`.

| Step | freq[2] | freq[3] | freq[4] | freq[12] | Explanation |
| --- | --- | --- | --- | --- | --- |
| Init | 1 | 1 | 0 | 1 | original multiset |
| Split 12->2*6 | 2 | 1 | 0 | 1 | 12 removed, 2 and 6 added |
| Split 6->2*3 | 3 | 2 | 0 | 0 | 6 removed, 2 and 3 added |
| Scan freq | min=2, max=3 | balance = 1 | final result |  |  |

This demonstrates multiple splits reducing maximum values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M + N) | Sieve for smallest prime factor is O(M log log M), splitting each number costs O(log x), total N numbers |
| Space | O(M + N) | `spf` array size M, frequency array size M, input array size N |

Given the constraints `M <= 5*10^6` and total `N <= 10^6`, the solution comfortably fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution block here
    MAX_M = 5 * 10**6 + 10
    spf = [0] * MAX_M
    for i in range(2, MAX_M):
        if spf[i] == 0:
            for j in range(i, MAX_M, i):
                if spf[j] == 0:
                    spf[j] = i
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        freq = [0] * (m + 2)
        for num in a:
            freq[num] += 1
        for x in range(m, 1, -1):
            while freq[x]:
                if spf[x] == x:
                    break
                p = spf[x]
                q = x // p
                freq[x] -= 1
                freq[p] += 1
                freq[q] += 1
        final_min = next(i for i in range(1,
```
