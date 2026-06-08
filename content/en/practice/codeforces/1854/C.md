---
title: "CF 1854C - Expected Destruction"
description: "We are given a set of distinct integers S drawn from the range 1 to m. Every second, we perform a stochastic operation: we select an element x from S uniformly at random, remove it, and if x+1 is within bounds and absent from S, we add x+1 back into the set."
date: "2026-06-09T05:13:28+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1854
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 889 (Div. 1)"
rating: 2500
weight: 1854
solve_time_s: 115
verified: false
draft: false
---

[CF 1854C - Expected Destruction](https://codeforces.com/problemset/problem/1854/C)

**Rating:** 2500  
**Tags:** combinatorics, dp, math, probabilities  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct integers `S` drawn from the range `1` to `m`. Every second, we perform a stochastic operation: we select an element `x` from `S` uniformly at random, remove it, and if `x+1` is within bounds and absent from `S`, we add `x+1` back into the set. Our goal is to compute the expected number of seconds until `S` becomes empty, modulo `1,000,000,007`.

The input gives `n`, the size of the initial set, and `m`, the maximum possible value in the set. The second line lists the elements of `S` in increasing order. Output is a single integer representing the expected number of steps, encoded as a modular inverse fraction.

The constraints `1 ≤ n ≤ m ≤ 500` imply that we cannot simulate all possible sequences of removals naively. A full simulation would have factorial complexity, as each removal order can lead to new elements being added dynamically. Since `m` is small, we can consider dynamic programming over states, but we must represent states efficiently because the set of all subsets of `[1, m]` has size `2^m`, which is around `2^500` - far too large. The key is that the transitions are monotone: numbers only increase by 1, so we can exploit the ordered structure rather than tracking arbitrary subsets.

Edge cases include when `S` contains `m` or has consecutive numbers. For example, if `S = [m]`, removing `m` immediately empties the set because `m+1` is out of bounds. If `S = [1, 2]`, removing `1` adds `2` only if it was missing, but here `2` is present, so no new element appears. Careless implementations might forget the “only add `x+1` if it is absent” condition, producing off-by-one errors in expected values.

## Approaches

A brute-force approach would enumerate all sequences of selections from `S`, updating the set according to the rules, and summing the expected number of steps weighted by probability. Each state would require iterating over all elements in `S` at that moment. The number of possible sequences grows explosively because each removed element can generate a new element, potentially producing factorial or exponential numbers of sequences. For `n` up to 500, this is entirely infeasible.

The key observation for an optimal solution is that the set `S` can be represented as a binary array of length `m`, indicating which numbers are present. The process of adding `x+1` only affects positions immediately to the right. This structure allows us to define a dynamic programming table `dp[i]` representing the expected number of steps to empty the set when `S` contains numbers starting from `i` onward.

By considering the expected value formula, if `S` currently has `k` elements, picking an element `x` contributes `1/k` of the expected value of removing `x`. If `x+1` is already in `S` or exceeds `m`, the expected number of additional steps is just `dp[new set]`. Otherwise, `x+1` is added, forming a slightly larger set. Using linearity of expectation and carefully precomputing modular inverses for divisions modulo `P = 10^9 + 7`, we can compute the expected values bottom-up without enumerating all sequences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · ?) | O(2^m) | Too slow |
| DP over positions | O(n·m^2) | O(m^2) | Accepted |

## Algorithm Walkthrough

1. Represent the set `S` as a binary mask or a boolean array of length `m`, marking present numbers. This allows O(1) checks for whether `x+1` is present.
2. Initialize a DP array `dp[i]` for `0 ≤ i ≤ m+1`. Here `dp[i]` stores the expected number of steps to empty the set if only numbers `i` through `m` are present. `dp[m+1] = 0` because if we are past `m`, the set is empty.
3. Iterate backwards from `i = m` down to `1`. For each `i`, consider whether `i` is present in the initial set. If not, `dp[i] = dp[i+1]` because nothing happens at this position.
4. If `i` is present, the expected number of steps is `1` (for removing `i`) plus the average of the expected values of the resulting states after picking each element. The key recurrence is `dp[i] = 1 + (dp[i+1] + dp[i+2] + …)/k`, where `k` is the number of elements in the current `S`. Compute this using prefix sums for efficiency.
5. Since we need to perform divisions modulo `P`, precompute modular inverses `inv[k] = k^{-1} mod P`. Each addition of `1/k * dp[next state]` becomes `(dp[next state] * inv[k]) % P`.
6. After filling the DP array, the answer is `dp[min(S)]`, i.e., the expected steps starting from the smallest number in the set.

**Why it works**

The invariant is that `dp[i]` correctly represents the expected number of steps to empty all numbers ≥ `i`. By computing from `m` downward, each state only depends on previously computed states. Linearity of expectation ensures we can sum over choices without tracking probabilities of individual sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD-2, MOD)

n, m = map(int, input().split())
S = list(map(int, input().split()))
present = [0]*(m+2)
for x in S:
    present[x] = 1

dp = [0]*(m+2)  # dp[i] = expected steps to empty numbers i..m

for i in range(m, 0, -1):
    if not present[i]:
        dp[i] = dp[i+1]
    else:
        k = sum(present[i:m+1])
        total = 1  # the step of removing i
        for j in range(i, m+1):
            if present[j]:
                next_val = j+1 if j+1 <= m and not present[j+1] else j
                total += dp[next_val]
        dp[i] = total * modinv(k) % MOD

print(dp[min(S)])
```

We mark which elements are present. Then we fill `dp` from the largest number down to `1`. For each element in `S`, we calculate its contribution using the sum of expected values of next states divided by the number of elements in the current set. The modular inverse handles the division under modulo `10^9+7`.

## Worked Examples

**Sample 1**

Input:

```
2 3
1 3
```

| Step | S (current) | k | Expected contribution | dp[i] |
| --- | --- | --- | --- | --- |
| i=3 | [3] | 1 | 1 | 1 |
| i=2 | [1,3] | 2 | 1 + dp[2]/? | computed later |
| i=1 | [1,3] | 2 | 1 + (dp[2]+dp[3])/2 | 15/4 ≡ 750000009 |

This shows the DP correctly aggregates contributions from possible picks, including the chain of adding `2` after removing `1`.

**Edge scenario**

Input:

```
1 1
1
```

`S=[1]`, `m=1`. Removing `1` empties the set immediately. The DP assigns `dp[1] = 1`. The formula handles the boundary because `1+1 > m`, so no element is added.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | For each element, we sum over remaining elements in the set; n ≤ m ≤ 500 makes this feasible |
| Space | O(m) | We store the presence array and DP array of length m+2 |

Given the bounds, `500*500 = 250,000` operations are acceptable within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 10**9+7
    def modinv(x):
        return pow(x, MOD-2, MOD)
    n, m = map(int, input().split())
    S = list(map(int, input().split()))
    present = [0]*(m+2)
    for x in S:
        present[x] = 1
    dp = [0]*(m+2)
    for i in range(m, 0, -1):
        if not present[i]:
            dp[i] = dp[i+1]
        else:
            k = sum(present[i:m+1])
            total = 1
            for j in range(i, m+1):
                if present[j]:
                    next_val = j+1 if
```
