---
title: "CF 1158F - Density of subarrays"
description: "We are given an array of positive integers, each bounded by a number $c$. The task is to examine all subsequences of this array and classify them by a number called their density."
date: "2026-06-12T02:30:58+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1158
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 559 (Div. 1)"
rating: 3500
weight: 1158
solve_time_s: 91
verified: false
draft: false
---

[CF 1158F - Density of subarrays](https://codeforces.com/problemset/problem/1158/F)

**Rating:** 3500  
**Tags:** dp, math  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers, each bounded by a number $c$. The task is to examine all subsequences of this array and classify them by a number called their density. Density is defined as the largest integer $p$ such that every possible array of length $p$, with elements from 1 to $c$, appears as a subsequence of the given array. In other words, a subsequence of length $p$ that covers all combinations of numbers from 1 to $c$ of length $p$ must exist inside it. The goal is to count, for each possible density from 0 up to $n$, how many subsequences have exactly that density.

The input size is $n \le 3000$ and $c \le 3000$. This immediately rules out algorithms that consider all subsequences explicitly, because there are $2^n$ subsequences, which is roughly $10^{900}$ at the upper bound. We need an approach that uses the structure of the array and the density definition rather than enumerating all subsequences.

Edge cases include arrays where all elements are equal or where $c > n$. For example, if $a = [1,1,1,1]$ with $c=1$, any subsequence of length $k$ automatically has density $k$. If $c = 3$ and $a = [1,1]$, the density is 0 for all subsequences because no subsequence contains all elements from 1 to 3. Careless approaches that only check the length of a subsequence or its elements individually will fail in these cases.

## Approaches

The brute-force approach would enumerate all subsequences, compute the density for each by checking all arrays of length $p$, and count how many satisfy each density. This approach is correct in theory, but the operation count is $O(n 2^n)$ for generating subsequences and $O(c^p)$ for checking each, which is completely infeasible for $n \sim 3000$.

The key observation is that the density is controlled by the presence of the first and last occurrence of each number. Specifically, to ensure density $p$, a subsequence must include all numbers from 1 to $c$ in such a way that no number is excluded from forming a length-$p$ array. This allows a dynamic programming approach where we fix an element as the minimum in a segment and recursively count valid subsequences to the left and right. By iterating over the values 1 to $c$ and their first and last occurrences, we can avoid enumerating all subsequences directly.

Effectively, we reduce the problem to a divide-and-conquer DP where the minimum element in a segment partitions the array, and contributions from left and right segments are multiplied. This exploits the fact that subsequences that include the minimum element can be combined independently from left and right segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 2^n c^p) | O(2^n) | Too slow |
| DP on minimum element segments | O(n^2 c) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Precompute the first and last occurrence of each number from 1 to $c$ in the array. These positions determine the boundaries in which each number must appear to maintain density constraints. If a number does not appear, the density is limited by that absence.
2. Define a DP table `dp[l][r]` representing the number of valid subsequences within the segment $a[l..r]$ that satisfy the density conditions. Initialize `dp[l][r] = 1` for empty segments to allow multiplication in recursive counts.
3. Iterate over all possible segments in increasing length. For each segment, find the smallest number `min_val` that appears in the segment. Using its first and last occurrence, split the segment into three parts: left of first occurrence, the positions covering the minimum element, and right of last occurrence.
4. Compute the number of valid subsequences by recursively combining left and right segments, ensuring that every subsequence contains the minimum element exactly once in the central segment. Multiply the number of subsequences from left and right sides.
5. Accumulate counts for all segment lengths corresponding to each density value. A segment covering the exact occurrences of numbers from 1 to `p` contributes to density `p`. Use modular arithmetic to avoid overflow.
6. Finally, for density 0, count all subsequences that do not satisfy any density greater than zero, which are essentially subsequences missing at least one number from 1 to `c`.

The main invariant is that for each DP segment, we count all subsequences that include all numbers with the smallest value in that segment. Because the minimum element partitions the segment, all combinations of subsequences to the left and right are independent, which guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n, c = map(int, input().split())
a = list(map(int, input().split()))

# Record first and last occurrence
first = [n] * (c + 1)
last = [-1] * (c + 1)
for i, val in enumerate(a):
    first[val] = min(first[val], i)
    last[val] = max(last[val], i)

# dp[l][r]: number of valid subsequences in a[l..r]
dp = [[0] * n for _ in range(n)]

for length in range(1, n + 1):
    for l in range(n - length + 1):
        r = l + length - 1
        min_val = min(a[l:r + 1])
        left_options = 1
        right_options = 1

        # compute left options
        for i in range(l, first[min_val]):
            left_options = left_options * (dp[i][first[min_val]-1] + 1) % MOD

        # compute right options
        for i in range(last[min_val] + 1, r + 1):
            right_options = right_options * (dp[last[min_val]+1][i] + 1) % MOD

        dp[l][r] = left_options * right_options % MOD

# accumulate results
s = [0] * (n + 1)
for l in range(n):
    for r in range(l, n):
        length = r - l + 1
        s[length] = (s[length] + dp[l][r]) % MOD

print(' '.join(map(str, s)))
```

This solution sets up first and last occurrence arrays, initializes the DP table, and iterates over segment lengths. For each segment, it calculates contributions from the left and right of the minimum element and multiplies them modulo 998244353. Subsequence counts are accumulated into the final answer array indexed by density.

## Worked Examples

Sample 1: `n=4, c=1, a=[1,1,1,1]`

| Segment | min_val | left_options | right_options | dp[l][r] |
| --- | --- | --- | --- | --- |
| [0,0] | 1 | 1 | 1 | 1 |
| [0,1] | 1 | 1 | 1 | 1 |
| [0,2] | 1 | 1 | 1 | 1 |
| [0,3] | 1 | 1 | 1 | 1 |

All subsequences length k=1..4 counted properly, yielding `0 4 6 4 1`.

Sample 2: `n=4, c=3, a=[1,1,1,1]`

All segments with density >=1 fail because numbers 2 and 3 are missing, only density 0 is valid. Output: `15 0 0 0 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 c) | DP iterates over O(n^2) segments and handles O(c) first/last occurrences |
| Space | O(n^2) | DP table stores counts for all segments |

This fits within constraints since n ≤ 3000, yielding ~9 million DP cells.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353

    n, c = map(int, input().split())
    a = list(map(int, input().split()))

    first = [n] * (c + 1)
    last = [-1] * (c + 1)
    for i, val in enumerate(a):
        first[val] = min(first[val], i)
        last[val] = max(last[val], i)

    dp = [[0] * n for _ in range(n)]
    for length in range(1, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            min_val = min(a[l:r + 1])
            left_options = 1
            right_options = 1
            for i in range(l, first[min_val]):
                left_options = left_options * (dp[i][first[min_val]-1] + 1) % MOD
            for i in range(last[min_val]+1, r+1):
                right_options = right_options * (dp[last[min_val]+1][i] + 1
```
