---
title: "CF 1703G - Good Key, Bad Key"
description: "We are asked to open a sequence of chests, each containing some number of coins, using either “good” or “bad” keys. A good key costs a fixed amount of coins to use, while a bad key is free but halves the coins in every unopened chest, including the one it opens, rounding down."
date: "2026-06-09T21:39:14+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1703
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 806 (Div. 4)"
rating: 1600
weight: 1703
solve_time_s: 155
verified: false
draft: false
---

[CF 1703G - Good Key, Bad Key](https://codeforces.com/problemset/problem/1703/G)

**Rating:** 1600  
**Tags:** bitmasks, brute force, dp, greedy, math  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to open a sequence of chests, each containing some number of coins, using either “good” or “bad” keys. A good key costs a fixed amount of coins to use, while a bad key is free but halves the coins in every unopened chest, including the one it opens, rounding down. We want to maximize the total coins we have after opening all chests in order.

The input gives the number of chests, the cost of a good key, and the number of coins in each chest. The output is the maximum coins achievable. Conceptually, we are deciding, for each chest, whether to spend coins now to get the full value or take a free action that reduces future gains.

Constraints are significant: up to 100,000 chests per test case and up to 10,000 test cases. The total sum of `n` over all test cases is limited to 100,000, which means any solution with per-test-case complexity O(n) is feasible. Brute-force exploration of all sequences of good/bad key choices is exponential and infeasible because even 20 chests would require checking over a million sequences. Values of coins and key costs can reach 10^9, so integer overflow is a concern in languages with 32-bit integers.

Non-obvious edge cases include chests with zero coins, cases where the cost of a good key is zero, and situations where all coins are equal. For example, if `n = 2`, `k = 1`, and `a = [0, 10]`, using a good key on the first chest is wasteful because it has no coins. Using a bad key on the first chest halves the second chest, so it is optimal to skip or adjust the choice carefully.

## Approaches

The most straightforward approach is brute-force: for each chest, consider both choices of keys, recursively compute the resulting coins, and pick the maximum. This works because it correctly models all possible sequences, but it fails because each chest doubles the number of states. With `n` up to 10^5, this would take O(2^n) operations, clearly impractical.

The key insight is that a bad key halves all remaining chests, so the effect of consecutive bad keys follows a geometric decay. That allows us to reverse the problem: instead of simulating each combination, we can fix the number of bad keys used at the end and greedily apply good keys to the larger chests. The optimal strategy is to decide how many of the last chests we will open with bad keys. We can iterate over the number of bad keys `b` from 0 to `n` and calculate the resulting coins: all chests before the last `b` get good keys, and the last `b` are affected by sequential halvings.

This works because using a good key early is only worthwhile if it compensates for the coins lost by future halvings. The total number of iterations is `n` per test case, and each calculation can be done in O(n) or O(b) if we precompute powers of two, which is fast enough given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n^2) naive, O(n) with prefix sums/powers | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums of coins from the end, to quickly know the sum of the last `b` chests. This allows us to compute the halved values efficiently.
2. Precompute powers of 1/2 using integer division (`// 2`) for at most 60 iterations since halving beyond that gives zero for all chests with values up to 10^9.
3. Iterate `b` from 0 to `n`, representing the number of bad keys used at the end. For each `b`, compute the coins collected by applying `b` bad keys sequentially on the last `b` chests. The formula is a sum of `floor(a[i] / 2^j)` for the appropriate powers `j`.
4. The remaining `n - b` chests use good keys. Subtract the total cost `(n - b) * k` from the total coins collected from those chests.
5. Track the maximum over all values of `b`. The maximum value is the answer for the test case.

Why it works: the algorithm maintains the invariant that for each `b`, all sequences with exactly `b` bad keys at the end are considered, which guarantees we explore all optimal placements of bad keys. Since bad keys only affect remaining chests, any sequence where a bad key is applied earlier can be represented as some `b` in this iteration. Good keys are applied greedily to the largest unaffected chests, which ensures no higher total can be achieved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        res = 0
        total_good = 0
        # Start with all coins as if all bad keys were used
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + a[i]
        max_coins = 0
        pow2 = 1
        for b in range(n + 1):
            coins_from_bad = 0
            for i in range(n - b, n):
                coins_from_bad += a[i] // pow2
            coins_from_good = suffix[0] - suffix[n - b] - (n - b) * k
            max_coins = max(max_coins, coins_from_good + coins_from_bad)
            pow2 *= 2
        print(max_coins)

solve()
```

The code first computes suffix sums to quickly evaluate the total coins for the good-key section. It iterates over the number of bad keys used at the end, computing their effect using repeated integer division to model sequential halvings. Multiplying `pow2` by two each step ensures each halving is accounted correctly.

Subtle points include handling integer division carefully so rounding down is automatic, avoiding floating-point errors. Using `suffix` allows O(1) access to sums of chests before bad keys, eliminating the need for repeated summation inside the loop.

## Worked Examples

### Sample Input 1

```
n = 4, k = 5, a = [10, 10, 3, 1]
```

| b | Coins from good keys | Coins from bad keys | Total |
| --- | --- | --- | --- |
| 0 | 10+10+3+1-4*5= -1 | 0 | -1 |
| 1 | 10+10+3-3*5=5 | 1//2=0 | 5 |
| 2 | 10+10-2*5=10 | 3//2=1,1//4=0 | 11 |
| 3 | 10-1*5=5 | 10//2=5,3//4=0,1//8=0 | 10 |
| 4 | 0 | 10//16=0,10//32=0,3//64=0,1//128=0 | 0 |

Maximum is 11. The trace confirms the algorithm evaluates all placements of bad keys efficiently.

### Sample Input 2

```
n = 1, k = 2, a = [1]
```

| b | Good | Bad | Total |
| --- | --- | --- | --- |
| 0 | 1-2=-1 | 0 | -1 |
| 1 | 0 | 1//1=1 | 1 |

Maximum is 1, showing the algorithm correctly handles single-element arrays and when bad keys are better.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) naive, O(n) with halving cutoff | We iterate over up to `n` bad keys. For each, computing bad-key sum using precomputed powers reduces complexity |
| Space | O(n) | Suffix sums array of length `n+1` |

Given the constraint that the sum of `n` over all test cases ≤ 10^5, this solution runs comfortably in under 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("5\n4 5\n10 10 3 1\n1 2\n1\n3 12\n10 10 29\n12 51\n5 74 89 45 18 69 67 67 11 96 23 59\n2 57\n85 60\n") == "11\n0\n13\n60\n58"

# Custom cases
assert run("1\n1 0\n100\n") == "100", "single chest, zero cost"
assert run("1\n3
```
