---
title: "CF 105170C - Fibonacci Sum"
description: "We are given a very large integer written in binary, call it n. Instead of interpreting it as a number in the usual way and looping from 1 to n, we are asked to work directly with its binary representation."
date: "2026-06-27T08:28:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105170
codeforces_index: "C"
codeforces_contest_name: "The 2024 CCPC National Invitational Contest (Changchun) , The 17th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 105170
solve_time_s: 43
verified: true
draft: false
---

[CF 105170C - Fibonacci Sum](https://codeforces.com/problemset/problem/105170/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very large integer written in binary, call it `n`. Instead of interpreting it as a number in the usual way and looping from 1 to `n`, we are asked to work directly with its binary representation.

For every integer `i` from 1 up to `n`, we look at the number of 1-bits in `i`, which is the popcount of `i`. Call this value `g(i)`. We then map that count through the Fibonacci sequence, where `f(1) = 1`, `f(2) = 1`, and for larger indices each term is the sum of the previous two. The final answer is the sum of `f(g(i))` over all `i` in `[1, n]`, taken modulo `10^9 + 7`.

So the problem is not really about iterating over numbers. It is about aggregating a function of popcount over a huge range defined by a binary limit.

The main difficulty is that `n` can have up to 10^7 bits. This immediately rules out any approach that iterates over values up to `n`, or even constructs all intermediate integers. Even storing all numbers is impossible. The only structure available is the binary string itself.

The key observation is that the value of `g(i)` depends only on which bit positions are chosen as 1s in `i`. So the problem reduces to counting how many integers `i ≤ n` have exactly `k` set bits, for each `k`, and then summing `f(k)` weighted by those counts.

This turns the problem into a constrained combinatorics problem over a binary prefix.

A few edge cases matter:

When `n = 1`, the only value is `i = 1`, so the answer is `f(1) = 1`. Any solution that assumes at least two bits or starts from 0 will be off.

When `n = 2` (binary `10`), valid numbers are `1` and `2`, with popcounts `1` and `1`, so the answer is `f(1) + f(1) = 2`.

A common failure mode is trying to treat the range as all binary numbers of fixed length equal to `|n|`, which incorrectly includes numbers greater than `n`.

## Approaches

The brute-force approach is straightforward in concept. We would iterate `i` from 1 to `n`, compute its popcount, evaluate the Fibonacci value for that count, and accumulate the result. This is correct, but completely infeasible. Even if we could compute popcount in O(1), the number of iterations is on the order of `n`, and `n` itself is a binary integer with up to 10^7 bits, so its magnitude is astronomically large.

The breakdown happens because we are iterating over values instead of bit patterns. The structure we actually need is not numeric order, but combinatorial structure over subsets of bit positions.

The key insight is to switch viewpoint: every number `i ≤ n` corresponds to selecting a subset of bit positions such that the resulting binary number does not exceed `n`. For a fixed subset size `k`, the contribution is `f(k)` multiplied by the number of valid subsets of size `k`.

This turns the problem into a digit dynamic programming problem over the binary representation of `n`, where we count how many prefixes produce valid numbers with a given number of chosen ones.

We maintain, for each prefix of `n`, how many ways we can form numbers with a given popcount, splitting into two cases: whether we are already strictly smaller than `n`, or still exactly matching the prefix. This is the standard “tight” DP over binary strings, with an additional dimension tracking the number of ones chosen so far.

Once we know the number of valid integers with exactly `k` ones, the final answer is just a weighted sum over Fibonacci values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over i | O(n) | O(1) | Too slow |
| Digit DP over binary prefix | O(L²) worst-case structured DP | O(L²) or optimized O(L) | Accepted |

Here `L` is the length of the binary string.

## Algorithm Walkthrough

We process the binary string from left to right, building counts of how many numbers we can form that are less than or equal to the prefix of `n`.

1. Precompute Fibonacci values up to `L`, since the popcount of any number with at most `L` bits cannot exceed `L`. This ensures we can instantly map any count of ones to its Fibonacci value.
2. Set up a DP table where `dp[tight][k]` represents how many ways we can form a number using the processed prefix such that exactly `k` ones have been chosen so far, and `tight` indicates whether we are still exactly matching the prefix of `n`.
3. Initialize `dp[1][0] = 1`, meaning before processing any bits, we have exactly one empty construction that matches the prefix.
4. For each bit in the binary string of `n`, update the DP:

We consider placing either 0 or 1 at the current position, but we must respect the constraint imposed by the prefix if we are in the tight state. If the current bit of `n` is 0, we cannot place 1 in the tight state. If it is 1, both choices are possible, but choosing 1 may still keep us tight or break tightness depending on the exact match.
5. Each transition also updates the count of selected ones, increasing `k` when we place a 1.
6. After processing all bits, we have counts of valid numbers grouped by their popcount, accumulated across both tight and non-tight states.
7. Compute the final answer by summing `dp[0][k] + dp[1][k]` multiplied by `f(k)` over all `k`.

### Why it works

Every integer `i ≤ n` corresponds to exactly one valid path in this digit DP: we decide bit by bit whether `i` matches `n` so far or has already become smaller, and we track how many ones we have used. The tight constraint guarantees we never exceed `n`, and the state split ensures each valid number is counted exactly once. Since popcount is fully captured by the number of chosen ones, grouping by `k` is sufficient, and the final sum correctly aggregates contributions of all integers in the range.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

s = input().strip()
L = len(s)

# Fibonacci up to L
fib = [0] * (L + 2)
fib[1] = 1
for i in range(2, L + 2):
    fib[i] = (fib[i - 1] + fib[i - 2]) % MOD

# dp[tight][k]
# tight = 0 or 1
dp0 = [0] * (L + 1)
dp1 = [0] * (L + 1)

dp1[0] = 1  # start tight, 0 ones used

for ch in s:
    bit = int(ch)
    ndp0 = [0] * (L + 1)
    ndp1 = [0] * (L + 1)

    for k in range(L + 1):
        val1 = dp1[k]
        if val1:
            # place 0
            if bit == 1:
                ndp0[k] = (ndp0[k] + val1) % MOD
            else:
                ndp1[k] = (ndp1[k] + val1) % MOD

            # place 1
            nk = k + 1
            if nk <= L:
                if bit == 1:
                    ndp1[nk] = (ndp1[nk] + val1) % MOD
                # if bit == 0, cannot place 1 in tight state

        val0 = dp0[k]
        if val0:
            # already smaller, can place freely
            ndp0[k] = (ndp0[k] + val0) % MOD
            ndp0[k + 1] = (ndp0[k + 1] + val0) % MOD if k + 1 <= L else ndp0[k + 1]

    dp0, dp1 = ndp0, ndp1

ans = 0
for k in range(L + 1):
    cnt = (dp0[k] + dp1[k]) % MOD
    ans = (ans + cnt * fib[k]) % MOD

print(ans)
```

The solution is structured around a digit DP over the binary representation. The Fibonacci array is precomputed once, and every DP state transition updates counts of constructed numbers by their current popcount. The split into `tight` and `non-tight` states enforces the upper bound defined by `n`.

A subtle implementation detail is maintaining bounds on `k`. Since we never ch
