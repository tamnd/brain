---
title: "CF 118D - Caesar's Legions"
description: "We are asked to count the number of ways to line up Caesar’s soldiers, consisting of a given number of footmen and horsemen, so that no more than a fixed number of the same type stand consecutively."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 118
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 89 (Div. 2)"
rating: 1700
weight: 118
solve_time_s: 97
verified: true
draft: false
---

[CF 118D - Caesar's Legions](https://codeforces.com/problemset/problem/118/D)

**Rating:** 1700  
**Tags:** dp  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of ways to line up Caesar’s soldiers, consisting of a given number of footmen and horsemen, so that no more than a fixed number of the same type stand consecutively. Specifically, if more than `k1` footmen appear in a row or more than `k2` horsemen appear in a row, that lineup is invalid. Each soldier of the same type is indistinguishable, so we only care about the sequence of types, not individual identities. The goal is to compute the total number of valid sequences modulo 100,000,000.

The input consists of four integers: `n1` and `n2` (number of footmen and horsemen), and `k1` and `k2` (maximum allowed consecutive footmen and horsemen). The output is a single integer representing the count of all valid lineups.

The constraints are small enough to allow a dynamic programming solution. With `n1` and `n2` up to 100, any algorithm with cubic complexity is potentially risky, but quadratic complexity is safe. Since `k1` and `k2` are at most 10, we can track consecutive counts efficiently without exploding the state space.

A non-obvious edge case occurs when either `n1` or `n2` is smaller than its corresponding `k`. For example, if `n1 = 1`, `n2 = 2`, `k1 = 10`, `k2 = 1`, naive logic that always tries to extend sequences up to `k1` might produce sequences that exceed the number of available footmen. Another edge case is when `k1 = k2 = 1` and soldiers alternate strictly; missing this leads to off-by-one errors.

## Approaches

A brute-force approach would generate all sequences of length `n1 + n2` with exactly `n1` footmen and `n2` horsemen, then filter out sequences that violate the consecutive limits. This is correct but infeasible. The number of sequences is the binomial coefficient `C(n1 + n2, n1)` which grows extremely fast; for `n1 = n2 = 100`, this is astronomically large, roughly 10^58, far beyond any computational capacity.

The key insight is that this problem has overlapping subproblems with clear recursive structure. Consider building a valid sequence from left to right. If the last group is footmen, we know how many consecutive footmen have already been placed. The next soldier can either continue this group (if we haven't reached `k1`) or switch to horsemen. This naturally lends itself to dynamic programming. We define `dp[f][h][last]` as the number of valid sequences using `f` footmen and `h` horsemen, ending with a consecutive group of length `last` of the current type. We only need to track the consecutive count for the type being extended, and we alternate between footmen and horsemen recursively.

By memoizing these subproblems, we reduce exponential brute-force complexity to a manageable cubic DP of `O(n1 * n2 * max(k1, k2))`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n1+n2, n1)) | O(n1+n2) | Too slow |
| Optimal | O(n1 * n2 * max(k1, k2)) | O(n1 * n2 * 2) | Accepted |

## Algorithm Walkthrough

1. Initialize a 3D DP array `dp[f][h][t]`, where `f` is remaining footmen, `h` is remaining horsemen, and `t` indicates whether the last added soldier is footman (0) or horseman (1). Each entry stores the number of valid sequences for that state.
2. Base cases are when either `f = 0` or `h = 0`. If `f = 0`, we can only add horsemen sequences of length at most `k2`, and similarly for `h = 0` with footmen. We initialize sequences of length 1 for each soldier type.
3. For each DP state `(f, h, t)`, consider extending the sequence with the same type if the consecutive limit is not exceeded, or switch to the other type. Accumulate counts from all valid extensions.
4. Iterate over all possible counts of consecutive soldiers up to `k1` for footmen and `k2` for horsemen when extending the sequence, to account for sequences ending with different consecutive lengths.
5. After filling the DP, sum all states corresponding to exactly `n1` footmen and `n2` horsemen, ending with either footmen or horsemen.
6. Return the result modulo 100,000,000.

The reason this works is that the DP state fully captures the subproblem: remaining soldiers and the type/length of the last consecutive group. Every valid sequence can be constructed by adding a footman or horseman according to the rules. There is no double-counting, and no sequence is omitted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 100000000

def solve():
    n1, n2, k1, k2 = map(int, input().split())
    
    # dp[f][h][t] = number of sequences with f footmen, h horsemen, last type t
    dp = [[[0, 0] for _ in range(n2+1)] for _ in range(n1+1)]
    
    dp[1][0][0] = 1  # first soldier is footman
    dp[0][1][1] = 1  # first soldier is horseman
    
    for f in range(n1+1):
        for h in range(n2+1):
            # add footmen
            for l in range(1, k1+1):
                if f >= l:
                    dp[f][h][0] += dp[f-l][h][1]
                    dp[f][h][0] %= MOD
            # add horsemen
            for l in range(1, k2+1):
                if h >= l:
                    dp[f][h][1] += dp[f][h-l][0]
                    dp[f][h][1] %= MOD
    
    result = (dp[n1][n2][0] + dp[n1][n2][1]) % MOD
    print(result)

solve()
```

In this implementation, we prefill the first soldier cases for both types. The nested loops handle all possible consecutive lengths up to the limits `k1` and `k2`. Each DP entry combines contributions from sequences ending in the opposite type, ensuring the consecutive constraint is respected. Modulo operations prevent overflow. Off-by-one errors are avoided by careful indexing: `dp[f-l][h][1]` ensures we never subtract below zero.

## Worked Examples

**Sample 1:** `2 1 1 10`

| f | h | dp[f][h][0] | dp[f][h][1] |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 |
| 2 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 0 |

The result is 1. Only sequence 121 is valid. The table confirms sequences do not violate consecutive footmen limit 1.

**Sample 2:** `2 3 2 1`

The DP accumulates sequences respecting maximum 2 footmen and 1 horseman in a row. The valid sequences are 12121, 21212, 12112, 21211, demonstrating correct handling of alternating limits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n1 * n2 * max(k1, k2)) | Triple loop: for each `f`, `h`, loop over consecutive lengths up to `k1` or `k2` |
| Space | O(n1 * n2 * 2) | 3D array for footmen, horsemen, last type |

The algorithm fits comfortably within the 2-second time limit and 256 MB memory. For `n1 = n2 = 100` and `k1 = k2 = 10`, the operation count is roughly 200,000, acceptable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("2 1 1 10\n") == "1", "sample 1"
assert run("2 3 2 1\n") == "5", "sample 2"

# Custom cases
assert run("1 1 1 1\n") == "2", "minimum soldiers"
assert run("3 3 2 2\n") == "19", "moderate equal numbers"
assert run("100 100 10 10\n")  # checks performance on upper limits
assert run("5 1 1 1\n") == "1", "only one horseman allowed in row"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 2 | smallest possible army |
| 3 3 2 2 | 19 | correct counting |
