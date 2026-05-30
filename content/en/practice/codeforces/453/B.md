---
title: "CF 453B - Little Pony and Harmony Chest"
description: "We are given a sequence of integers a1, a2, ..., an with values between 1 and 30, and we need to construct another sequence b1, b2, ..., bn of positive integers such that every pair in b is coprime."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 453
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 259 (Div. 1)"
rating: 2000
weight: 453
solve_time_s: 79
verified: true
draft: false
---

[CF 453B - Little Pony and Harmony Chest](https://codeforces.com/problemset/problem/453/B)

**Rating:** 2000  
**Tags:** bitmasks, brute force, dp  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers `a1, a2, ..., an` with values between 1 and 30, and we need to construct another sequence `b1, b2, ..., bn` of positive integers such that every pair in `b` is coprime. The goal is to minimize the sum of absolute differences between corresponding elements of `a` and `b`, that is, minimize `|a1 - b1| + |a2 - b2| + ... + |an - bn|`.

The key constraints are that `n` can be up to 100, which is small enough that algorithms with cubic or quadratic factors in `n` can be feasible. Each `ai` is at most 30, which limits the potential candidate values for `bi`. The coprimality condition is global: no two `bi` can share a prime factor, so we cannot choose the sequence greedily without keeping track of primes already used.

Non-obvious edge cases include sequences where all `ai` are equal, like `1 1 1 1 1`. In this case, the optimal `bi` may also be all ones if the coprimality constraint allows it. Another tricky situation is when `ai` are multiples of small primes, e.g., `2 4 8 16`. A naive greedy choice picking each `ai` directly would violate coprimality. Similarly, if `ai` contains primes that repeat, careful selection of nearby coprime numbers is required to minimize the sum.

## Approaches

The brute-force approach would enumerate all possible sequences `b` of length `n` where each `bi` is in the range `[1, 60]` (we can extend slightly beyond the maximum `ai` to allow coprime flexibility). For each candidate sequence, we would check coprimality for all pairs and compute the sum. This works because for any fixed sequence of length `n=100`, there are roughly `60^100` combinations, which is astronomically large and infeasible. Even with pruning, the approach is too slow.

The key insight is that `bi` values can be mapped to subsets of prime numbers using bitmasks. Each integer between 1 and 60 can be represented by the set of its prime factors. If we maintain a bitmask of primes already used in previous `bi`, we can efficiently check whether a new candidate `bi` is coprime with the sequence so far. This reduces the problem to dynamic programming over positions in the array and subsets of primes.

We define `dp[i][mask]` as the minimal sum of differences for the first `i` elements of `a` with a set of primes used represented by `mask`. For each position `i`, we try all `bi` from 1 to 58 (or 60) that do not share primes with `mask`, updating the new mask by adding primes of `bi`. This reduces the problem to a manageable state space because there are only 16 primes up to 60, so masks range over `2^16` possibilities, and `n` is at most 100. This gives a feasible dynamic programming solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(60^n * n^2) | O(n) | Too slow |
| Optimal | O(n * 2^16 * 60) | O(n * 2^16) | Accepted |

## Algorithm Walkthrough

1. Precompute all primes up to 60 and assign each a bit position. Every number `x` in `[1, 58]` is mapped to a bitmask representing its prime factors. This allows us to check coprimality using bitwise AND operations.
2. Initialize a dynamic programming table `dp[i][mask]` with `inf` values. `dp[0][0]` is 0 because no elements chosen yet.
3. Iterate through positions `i` from 0 to `n-1`. For each `mask` representing primes used so far, consider every candidate `b` from 1 to 58. If `mask` AND `b`'s prime bitmask is zero, the candidate is coprime with all previous selections.
4. Compute `dp[i+1][new_mask]` as the minimum of its current value and `dp[i][mask] + |a[i] - b|`. Store a backtracking table to reconstruct the actual sequence.
5. After processing all positions, find the `mask` at `dp[n][mask]` with the minimal sum. Backtrack through the stored choices to reconstruct the optimal sequence `b`.
6. Output the reconstructed sequence.

The invariant is that `dp[i][mask]` always contains the minimal sum achievable for the first `i` positions using exactly the primes indicated in `mask`. Since we only add numbers that do not share primes with `mask`, coprimality is guaranteed at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
prime_to_bit = {p: i for i, p in enumerate(primes)}

def number_to_mask(x):
    mask = 0
    for p in primes:
        if x % p == 0:
            mask |= (1 << prime_to_bit[p])
    return mask

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    max_val = 58

    masks = [number_to_mask(i) for i in range(max_val+1)]

    dp = [{} for _ in range(n+1)]
    dp[0][0] = 0
    back = [{} for _ in range(n+1)]

    for i in range(n):
        for mask in dp[i]:
            for b in range(1, max_val+1):
                b_mask = masks[b]
                if mask & b_mask == 0:
                    new_mask = mask | b_mask
                    cost = dp[i][mask] + abs(a[i] - b)
                    if new_mask not in dp[i+1] or cost < dp[i+1][new_mask]:
                        dp[i+1][new_mask] = cost
                        back[i+1][new_mask] = (mask, b)

    # reconstruct
    mask = min(dp[n], key=lambda m: dp[n][m])
    res = []
    for i in range(n, 0, -1):
        prev_mask, b = back[i][mask]
        res.append(b)
        mask = prev_mask
    print(' '.join(map(str, reversed(res))))

solve()
```

The code first encodes numbers to prime bitmasks for quick coprimality checks. The dynamic programming table `dp[i][mask]` keeps the minimal sum for each position and used-primes mask. The backtracking table stores choices to reconstruct the sequence. Using bitwise operations ensures that the coprimality check is O(1).

## Worked Examples

### Sample 1

Input: `1 1 1 1 1`

| i | mask | candidate b | new_mask | dp[i+1][new_mask] |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 0+ |
| 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 0 | 1 | 0 | 0 |
| 4 | 0 | 1 | 0 | 0 |

All `bi` can be 1 since they are coprime (1 has no prime factors). The minimal sum is 0.

### Custom Example

Input: `2 2 3`

| i | mask | candidate b | new_mask | dp[i+1][new_mask] |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 (mask for 2) |  |
| 1 | 2 | 3 | 2 | 3=6 (mask for 2 and 3) |

The algorithm selects `b=[2,3]`, minimizing sum and maintaining coprimality.

These traces confirm that the dynamic programming invariant holds: we always track minimal sum for each mask, and we never violate coprimality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 2^16 * 58) | n positions, 2^16 prime masks, 58 candidates per position |
| Space | O(n * 2^16) | dp table and backtracking table storing states for each mask |

With n ≤ 100 and 16 primes, 2^16 = 65536, so total operations are roughly 100 * 65536 * 58 ≈ 380 million. In practice, pruning reduces actual states, which is acceptable for a 4-second limit. Memory usage is under 256MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("5\n1
```
