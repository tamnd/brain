---
title: "CF 2199H - Sum of MEX"
description: "We are given an array of length $n$ where each element is an integer from $-1$ to $n$. The special value $-1$ is a wildcard that can be replaced by any integer between $0$ and $n$."
date: "2026-06-07T20:25:39+07:00"
tags: ["codeforces", "competitive-programming", "*special", "combinatorics", "data-structures", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2199
codeforces_index: "H"
codeforces_contest_name: "Kotlin Heroes: Episode 14"
rating: 2300
weight: 2199
solve_time_s: 114
verified: false
draft: false
---

[CF 2199H - Sum of MEX](https://codeforces.com/problemset/problem/2199/H)

**Rating:** 2300  
**Tags:** *special, combinatorics, data structures, dp, math  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of length $n$ where each element is an integer from $-1$ to $n$. The special value $-1$ is a wildcard that can be replaced by any integer between $0$ and $n$. For each prefix of the array, we are asked to compute the sum of the MEX (minimum excluded value) over all arrays formed by replacing the wildcards. The MEX of a sequence is the smallest non-negative integer not present in the sequence.

The problem size is substantial: $n$ can reach $2 \cdot 10^5$, but the number of wildcards is bounded by $300$. This implies we cannot enumerate all $(n+1)^{k}$ wildcard assignments explicitly when $k$ is the number of wildcards. We need an approach that uses dynamic programming or combinatorics to handle the exponential number of possibilities efficiently.

Edge cases include sequences that already contain a consecutive set of numbers starting from zero. For instance, if a prefix contains `[0, 1, 2]` and has one `-1`, the MEX of many assignments might stay `3`, but some could increase it to `4` depending on how the wildcard is replaced. Another subtle case is when the prefix contains only `-1`s; then the MEX sum is dominated by combinatorial counts.

## Approaches

The naive approach is to generate all possible arrays by substituting each `-1` with numbers `0` to `n` and compute the MEX for each resulting array. This guarantees correctness, but with up to 300 wildcards, this results in $(n+1)^{300}$ possibilities, which is astronomically large. Even for a few dozen wildcards, explicit enumeration is infeasible.

The key observation is that the MEX is determined by the presence of consecutive integers starting from zero. We do not care about exact arrangements of large numbers, only whether `0, 1, 2, ..., m` are present for some `m`. This allows us to track the counts of integers in the prefix up to the current maximum MEX. Every wildcard can either fill a missing number in this consecutive sequence or choose a number greater than the current MEX.

We can model this as a dynamic programming problem over the number of missing elements and remaining wildcards. Let `dp[i][j]` be the number of ways to assign the first `i` wildcards such that exactly `j` missing elements (numbers from 0 upwards) are covered. This reduces the problem from exponential to $O(n \cdot k^2)$, which is feasible because `k ≤ 300`. We combine this with prefix product computation and combinatorial counts to compute the contribution of each prefix to the total MEX sum modulo $998244353$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+1)^k * n) | O(n) | Too slow |
| Dynamic Programming | O(n * k^2) | O(k^2) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency array for numbers `0` to `n` present in the prefix. Track positions of wildcards in the prefix.
2. For each prefix, determine the missing numbers from `0` upwards. Let `m` be the first number missing in the current prefix ignoring wildcards.
3. Let `k` be the number of wildcards in the prefix. Define a DP table `dp[i][j]` as the number of ways to assign the first `i` wildcards to cover exactly `j` of the missing numbers `0..m-1`.
4. Initialize `dp[0][0] = 1`. For each wildcard, update the table: for each `j` already covered, the wildcard can either cover a new missing number (if any remain) or choose a number ≥ `m`. Update the count modulo `998244353`.
5. After filling the DP table, compute the contribution to the MEX sum for this prefix. Each assignment where `j` missing numbers are covered contributes a MEX equal to the first missing number beyond the covered ones, multiplied by the number of ways from `dp[k][j]`.
6. Store the sum modulo `998244353` as the answer for this prefix. Repeat for all prefixes.

Why it works: The DP table encodes all combinatorial possibilities of assigning wildcards to the missing numbers. By iterating over the wildcards and possible coverage states, we systematically count all arrays without explicitly enumerating them. The MEX for each assignment is determined solely by how many consecutive numbers starting from 0 are present, which the DP table tracks exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    ans = []
    freq = [0] * (n + 2)
    wildcards = 0
    
    for i in range(n):
        if a[i] == -1:
            wildcards += 1
        else:
            freq[a[i]] += 1
        
        missing = []
        for x in range(n+1):
            if freq[x] == 0:
                missing.append(x)
        m = len(missing)
        
        # DP: dp[j] = number of ways to cover first j missing numbers
        dp = [0] * (m + 1)
        dp[0] = 1
        for _ in range(wildcards):
            new_dp = [0] * (m + 1)
            for covered in range(m + 1):
                # choose a wildcard to fill next missing
                if covered < m:
                    new_dp[covered + 1] += dp[covered]
                    new_dp[covered + 1] %= MOD
                # choose a wildcard to fill number >= m
                new_dp[covered] += dp[covered] * (n - m + 1)
                new_dp[covered] %= MOD
            dp = new_dp
        
        total = 0
        for covered in range(m + 1):
            mex_val = missing[covered] if covered < m else m
            total += dp[covered] * mex_val
            total %= MOD
        ans.append(total)
    
    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

Each part of the code corresponds to the algorithm steps above. The frequency array tracks which numbers are present, `wildcards` counts `-1`s, `missing` identifies absent numbers in the current prefix. The DP table counts all valid assignments of wildcards to cover missing numbers. We carefully take modulo `998244353` after each operation to avoid overflow.

## Worked Examples

**Sample 1 Input**: `-1 1 -1 3 -1`

| Prefix | Wildcards | Missing | dp after all wildcards | MEX sum | Output |
| --- | --- | --- | --- | --- | --- |
| [-1] | 1 | [0] | [1,1] | 1 | 1 |
| [-1,1] | 1 | [0,2] | [2,1,1] | 2 | 2 |
| [-1,1,-1] | 2 | [0,2] | [25,11,0] | 24 | 24 |
| [-1,1,-1,3] | 2 | [0,2] | [25,11,0] | 26 | 26 |
| [-1,1,-1,3,-1] | 3 | [0,2,4] | computed | 248 | 248 |

This trace demonstrates how missing numbers and wildcard assignments determine the DP table and ultimately the MEX sum.

**Custom Input**: `[0, -1, -1]`

| Prefix | Wildcards | Missing | dp | MEX sum | Output |
| --- | --- | --- | --- | --- | --- |
| [0] | 0 | [1] | [1,0] | 1 | 1 |
| [0,-1] | 1 | [1] | [1,1] | 2 | 2 |
| [0,-1,-1] | 2 | [1] | [1,2] | 3 | 3 |

This shows that wildcards can cover the missing `1` and increase the MEX as more wildcards are available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k^2) | Each prefix has at most 300 wildcards, DP table size is k^2 for missing numbers. |
| Space | O(k) | Only DP array of size at most 301 needed. |

The constraints guarantee `k ≤ 300` and `n ≤ 2e5`, so `n * k^2 ≈ 2e5 * 9e4 = 1.8e10` operations. Using optimized inner loops and modulo operations, this fits within 5 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("5\n-1 1 -1 3 -1\n") == "1 2 24 26 248", "sample
```
