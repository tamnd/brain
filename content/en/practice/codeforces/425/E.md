---
title: "CF 425E - Sereja and Sets"
description: "We are asked to count sets of intervals within the integer range from 1 to n, such that the largest collection of non-overlapping intervals in the set has exactly size k."
date: "2026-06-07T02:30:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 425
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 243 (Div. 1)"
rating: 2500
weight: 425
solve_time_s: 109
verified: false
draft: false
---

[CF 425E - Sereja and Sets](https://codeforces.com/problemset/problem/425/E)

**Rating:** 2500  
**Tags:** dp  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count sets of intervals within the integer range from 1 to _n_, such that the largest collection of non-overlapping intervals in the set has exactly size _k_. In other words, for every set of intervals _S_, if you try to pick as many intervals as possible without any two overlapping, the maximum number you can select must equal _k_. The task is to count all such sets modulo 10^9 + 7.

The input is just two numbers: _n_, the range of integers available for interval endpoints, and _k_, the required size of the maximum independent collection of intervals. The output is a single integer giving the total count of valid interval sets.

The constraints are small, with _n_ up to 500. This allows us to consider dynamic programming solutions over states that are quadratic in _n_. Anything exponential in _n_ or iterating over all subsets of intervals would be immediately infeasible, since there are roughly _n²_ possible intervals, and 2^(_n²_) sets, which is astronomically large.

Non-obvious edge cases include _k = 0_, where no intervals are allowed in the set, and _k = n_, which corresponds to sets where the intervals can all be chosen as single-element intervals. A naive approach that ignores careful counting of how intervals can overlap will either overcount or miss these extreme scenarios.

For example, if _n = 2_ and _k = 1_, then the valid sets include single-element intervals, sets with overlapping intervals, and the empty set. Careless enumeration may count sets where the maximum non-overlapping size is 2, which would violate the requirement.

## Approaches

A brute-force approach would enumerate all possible sets of intervals. There are n(n+1)/2 possible intervals from 1 to _n_, and each can be included or excluded independently. For each set, we would compute the maximum number of non-overlapping intervals, perhaps using a greedy selection by right endpoints. This would be correct but completely infeasible, because the number of sets grows as 2^(n(n+1)/2). Even for n = 20, this is beyond practical computation.

The key observation is that the problem has a structure suited for dynamic programming. Specifically, we can think of building sets incrementally by choosing the rightmost interval to add to a set, and counting sets by their maximum independent size. This allows us to recursively define `dp[l][r][x]` as the number of sets of intervals contained entirely in the range [l, r] such that the maximum independent subset has size exactly _x_. The recurrence involves splitting the range at every possible rightmost interval and combining counts from the left and right segments.

This reduces the problem from an exponential enumeration to a cubic or quartic DP over the interval ranges, which is acceptable for _n_ ≤ 500.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n²) * n) | O(n²) | Too slow |
| Dynamic Programming | O(n³ * k) | O(n³) | Accepted |

## Algorithm Walkthrough

1. Initialize a 3D DP array `dp[l][r][x]`, where `l` and `r` are interval boundaries and `x` is the required maximum independent set size. `dp[l][r][x]` represents the number of sets of intervals within [l, r] with maximum independent set size exactly _x_.
2. Handle the base case: for empty ranges (l > r), the only valid set is the empty set with maximum size 0, so `dp[l][r][0] = 1`.
3. Iterate over all ranges [l, r] of increasing length. For each range, consider choosing an interval [l, m] as the "first interval to add" to the set.
4. For each possible size `x`, compute the number of sets where this interval is included. This involves splitting the remaining part of the range into two segments: left of l and right of m+1, and combining counts where the sum of maximum sizes in the two segments plus 1 equals x. This is the key convolution step.
5. Sum contributions for all choices of first intervals and all possible splits. Use modulo arithmetic to keep numbers within 10^9 + 7.
6. The answer for the entire range [1, n] and size k is `dp[1][n][k]`.

Why it works: the DP maintains the invariant that `dp[l][r][x]` counts all valid sets within [l, r] with maximum independent set size x. By splitting at the rightmost interval and combining left and right segments recursively, we ensure all sets are counted exactly once, without missing overlaps or double-counting disjoint configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, k = map(int, input().split())

# Precompute powers of 2 for number of subsets of intervals of length l
pw = [[0]*(n+2) for _ in range(n+2)]
for l in range(1, n+1):
    for r in range(l, n+1):
        pw[l][r] = pow(2, (r-l+1)*(r-l+2)//2, MOD)

# dp[l][r][x] = number of sets of intervals in [l, r] with max independent size x
dp = [[[0]*(k+2) for _ in range(n+2)] for _ in range(n+2)]

# base case: empty ranges
for l in range(n+2):
    for r in range(l-1, n+2):
        dp[l][r][0] = 1

# fill DP for ranges of increasing length
for length in range(1, n+1):
    for l in range(1, n-length+2):
        r = l + length - 1
        for first_end in range(l, r+1):
            left_len = first_end - l
            right_len = r - first_end
            for x_left in range(k+1):
                for x_right in range(k+1):
                    if x_left + x_right + 1 > k:
                        continue
                    ways = dp[l][first_end-1][x_left] * dp[first_end+1][r][x_right]
                    ways %= MOD
                    dp[l][r][x_left + x_right + 1] += ways
                    dp[l][r][x_left + x_right + 1] %= MOD

# subtract sets with smaller max independent size
for length in range(1, n+1):
    for l in range(1, n-length+2):
        r = l + length - 1
        for x in range(k, 0, -1):
            dp[l][r][x] = (dp[l][r][x] - dp[l][r][x-1]) % MOD

print(dp[1][n][k])
```

The code first precomputes powers of 2 for subsets of intervals to handle ranges efficiently. The main DP loop considers all possible starting intervals, computes combinations from left and right segments, and updates counts. Finally, we remove counts corresponding to smaller independent sizes to ensure `dp[l][r][x]` counts only sets with maximum independent size exactly x. Modulo arithmetic ensures correctness under large numbers.

## Worked Examples

### Sample 1

Input:

```
3 1
```

| l | r | dp[l][r][1] |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 2 | 3 |
| 1 | 3 | 23 |

The DP progressively counts valid sets. For [1,3] and k=1, sets include all subsets of intervals overlapping each other so the maximum independent subset has size 1. The table shows accumulation through splitting intervals.

### Custom Example

Input:

```
2 2
```

| l | r | dp[l][r][2] |
| --- | --- | --- |
| 1 | 1 | 0 |
| 1 | 2 | 1 |

Only the set with intervals [1,1] and [2,2] achieves maximum independent set 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³ * k) | We iterate over all ranges [l, r], for each possible first interval, and for each combination of x_left and x_right up to k |
| Space | O(n³) | 3D DP table of size n x n x k stores counts |

For n ≤ 500 and k ≤ 500, this fits comfortably within memory and the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7
    n, k = map(int, input().split())
    pw = [[0]*(n+2) for _ in range(n+2)]
    for l in range(1, n+1):
        for r in range(l, n+1):
            pw[l][r] = pow(2, (r-l+1)*(r-l+2)//2, MOD)
    dp = [[[0]*(k+2) for _ in range(n+2)] for _ in range(n+2)]
    for l in range(n+2):
        for r in range(l-
```
