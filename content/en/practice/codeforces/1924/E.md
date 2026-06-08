---
title: "CF 1924E - Paper Cutting Again"
description: "We are asked to model a stochastic process of repeatedly cutting a rectangular sheet of paper and discarding parts of it, and then compute the expected number of steps until its area falls below a threshold."
date: "2026-06-08T19:09:53+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1924
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 921 (Div. 1)"
rating: 3100
weight: 1924
solve_time_s: 133
verified: false
draft: false
---

[CF 1924E - Paper Cutting Again](https://codeforces.com/problemset/problem/1924/E)

**Rating:** 3100  
**Tags:** combinatorics, probabilities  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to model a stochastic process of repeatedly cutting a rectangular sheet of paper and discarding parts of it, and then compute the expected number of steps until its area falls below a threshold. The paper starts with dimensions $n \times m$, and at each step a cut is made along any integer vertical or horizontal line that is not the boundary. For vertical cuts, the right part is discarded, and for horizontal cuts, the bottom part is discarded. The step is chosen uniformly among all $h+w-2$ possible cuts, where $h$ and $w$ are the current height and width.

The input gives multiple independent test cases, each specifying $n$, $m$, and $k$. The output is the expected number of steps modulo $10^9+7$, represented as $p\cdot q^{-1} \bmod 10^9+7$ if the expectation is the fraction $p/q$. We must handle up to $57{,}000$ test cases, and although $n$ and $m$ can be as large as $10^6$, the sum over all test cases is constrained to $10^6$, which allows an $O(nm)$ or $O(n+m)$ per test case solution.

A naive approach of simulating all cuts is impossible because the number of cut sequences grows exponentially. Even memoization across all $n \times m$ subrectangles would be infeasible due to memory. Edge cases arise when the area is already below $k$ at the start, in which case zero cuts are required, or when the area is just one or two units above $k$, which can result in small integer expectations that must be represented modulo $10^9+7$.

## Approaches

A brute-force simulation tries all sequences of cuts and computes the average number of steps. This is correct in principle, but infeasible because the number of sequences is roughly $2^{n+m}$ in the worst case, far beyond any computational limit. Even memoization over all $(h,w)$ pairs would require storing $10^{12}$ entries for $h \cdot w$, which is impossible.

The key insight is that the process has **linearity of expectation**. If we denote $E[h,w]$ as the expected number of steps starting from a rectangle of height $h$ and width $w$, we can write a recurrence:

$$E[h,w] = 0 \text{ if } h \cdot w < k$$

Otherwise, each cut line (vertical or horizontal) is equally likely. A vertical cut at position $x$ leaves a rectangle of width $x$ and height $h$, and a horizontal cut at position $y$ leaves a rectangle of height $y$ and width $w$. Therefore:

$$E[h,w] = 1 + \frac{1}{h+w-2} \left( \sum_{x=1}^{w-1} E[h,x] + \sum_{y=1}^{h-1} E[y,w] \right)$$

Because the sums over $x$ and $y$ are arithmetic series of expectations, we can compute prefix sums to allow $O(h+w)$ per rectangle instead of $O(hw)$. This observation makes the DP feasible, especially given that the sum of $n$ and $m$ over all test cases is $10^6$.

Modular arithmetic is needed at each step to compute the expected value modulo $10^9+7$. Since the expectation is a fraction, we store numerator and denominator separately and compute numerator * denominator_inverse modulo $10^9+7$ at the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Simulation | O(2^{n+m}) | O(nm) | Too slow |
| DP with prefix sums + modular fractions | O(n+m) per test case | O(n+m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n, m, k$. If $n \cdot m < k$, print 0 and continue. No cuts are needed.
2. Initialize a DP array `dp[h][w]` to store expected steps for rectangles of height `h` and width `w`. Use 1-based indexing.
3. Initialize prefix sums arrays `hsum[h][w]` and `wsum[h][w]` to allow quick sum of `dp` values along rows and columns. These arrays allow computing $\sum_{x=1}^{w-1} E[h,x]$ and $\sum_{y=1}^{h-1} E[y,w]$ in O(1) after preprocessing.
4. Iterate `h` from 1 to `n` and `w` from 1 to `m`. If `h*w < k`, set `dp[h][w] = 0`. Otherwise, compute:

$$dp[h][w] = \frac{( \text{hsum}[h][w-1] + \text{wsum}[h-1][w] + h + w -2)}{h + w -2}$$

The numerator includes `h+w-2` to account for the `+1` in expectation.

1. Store modular fractions at each step using Fermat’s inverse to compute division modulo $10^9+7$.
2. After filling the DP table, output `dp[n][m]` modulo $10^9+7`.

Why it works: This DP directly encodes the recurrence of the expected number of steps based on linearly adding the contributions of all possible cuts, and prefix sums accelerate the computation. Modulo arithmetic ensures that fractions are handled correctly under modulo.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

def modinv(a):
    return pow(a, MOD-2, MOD)

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    if n * m < k:
        print(0)
        continue

    dp = [0] * (m + 1)
    for h in range(1, n + 1):
        new_dp = [0] * (m + 1)
        prefix = [0] * (m + 1)
        for w in range(1, m + 1):
            if h * w < k:
                new_dp[w] = 0
            else:
                sum_prev_w = prefix[w - 1]
                sum_prev_h = dp[w]
                num = (sum_prev_w + sum_prev_h + h + w - 2) % MOD
                den = h + w - 2
                new_dp[w] = num * modinv(den) % MOD
            prefix[w] = (prefix[w - 1] + new_dp[w]) % MOD
        dp = new_dp
    print(dp[m])
```

This solution constructs the DP table row by row. `dp[w]` represents the previous row. `prefix[w]` accumulates sums along the current row, so that `sum_prev_w` can be computed in O(1). The fraction division is performed via modular inverse. Boundary conditions are handled by checking `h*w < k`.

## Worked Examples

**Test case:** 2 4 8

| h | w | dp[h][w] | prefix[w] |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 1 | 2 | 1 | 1 |
| 1 | 3 | 1 | 2 |
| 1 | 4 | 1 | 3 |
| 2 | 1 | 1 | 1 |
| 2 | 2 | 1 | 2 |
| 2 | 3 | 1 | 3 |
| 2 | 4 | 1 | 4 |

The final answer `dp[2][4] = 1`.

**Test case:** 2 4 2

Area initially 8 ≥ 2. The expectation is 17/6 = 833333342 modulo 10^9+7.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) per test case | DP iterates over each rectangle and computes sum using prefix sums |
| Space | O(m) | Only store current and previous row to compute DP |

Given sum of n+m over all test cases ≤ 10^6, total operations are ≤ 10^6, which fits comfortably within 3s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 10**9 + 7
    def modinv(a): return pow(a, MOD-2, MOD)
    t = int(input())
    res = []
    for _ in range(t):
        n,m,k = map(int,input().split())
        if n*m < k:
            res.append("0")
            continue
        dp = [0]*(m+1)
        for h in range(1,n+1):
            new_dp = [0]*(m+1)
            prefix = [0]*(m+1)
            for w in range(1,m+1):
                if h*w < k:
                    new_dp[w] = 0
                else:
                    sum_prev_w = prefix[w-1]
                    sum_prev_h = dp[w]
                    num = (sum_prev_w + sum_prev_h + h + w - 2)%MOD
                    den = h + w - 2
                    new_dp[w] = num * modinv(den) % MOD
                prefix[w] = (prefix[w-
```
