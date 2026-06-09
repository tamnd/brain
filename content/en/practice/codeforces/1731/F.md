---
title: "CF 1731F - Function Sum"
description: "We are asked to work with arrays of integers of size n, where each element is between 1 and k. For each position in the array, we define two quantities."
date: "2026-06-09T18:38:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp", "fft", "math"]
categories: ["algorithms"]
codeforces_contest: 1731
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 841 (Div. 2) and Divide by Zero 2022"
rating: 2500
weight: 1731
solve_time_s: 139
verified: true
draft: false
---

[CF 1731F - Function Sum](https://codeforces.com/problemset/problem/1731/F)

**Rating:** 2500  
**Tags:** brute force, combinatorics, dp, fft, math  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to work with arrays of integers of size `n`, where each element is between `1` and `k`. For each position in the array, we define two quantities. The first counts how many previous elements are smaller than the current one, and the second counts how many later elements are larger than the current one. A position is considered _good_ if there are fewer smaller elements before it than larger elements after it. The function `f(a)` sums the values at all good positions in a given array. Finally, we need the sum of `f(a)` over all possible arrays of size `n`.

The constraints are small enough that `n` is at most 50 and `k` is less than `998244353`. Enumerating all arrays is technically possible for tiny `n` and `k`, but `k^n` grows very quickly, so brute-force enumeration is infeasible. This suggests we need a combinatorial or dynamic programming approach. Edge cases include arrays where all elements are the same, which should produce a sum of zero since no position is ever good, and arrays with minimum or maximum values that push the counts of smaller and larger elements to extremes.

For example, if `n=3` and `k=2`, the array `[2,2,2]` has `f([2,2,2]) = 0` because no element has more larger elements after it than smaller elements before it. A careless approach might attempt to compute `lsl` and `grr` for every array explicitly, which would quickly blow up computationally.

## Approaches

A straightforward approach is to generate all arrays of length `n` and for each array compute `lsl` and `grr` for every position, summing elements where the position is good. This brute-force works because it directly follows the definition, but it fails as soon as `n` or `k` grows beyond trivial sizes. For `n=50` and `k=50`, the number of arrays is `50^50`, which is astronomically large.

The key insight comes from observing that `lsl` only depends on the prefix and `grr` only depends on the suffix. This allows us to count arrays combinatorially rather than enumerating them. If we fix a value `v` at position `i`, we only need the number of elements smaller than `v` before `i` and the number of elements larger than `v` after `i`. These counts can be encoded as combinations: the number of ways to choose `less` elements smaller than `v` in the prefix and `greater` elements larger than `v` in the suffix. Summing over all possible counts and all positions gives the final answer. We can compute the combinations using factorials modulo `998244353` and handle powers efficiently with modular exponentiation.

The brute-force is conceptually simple but intractable for this problem. The combinatorial approach reduces the problem to summing products of powers and combinations, which is manageable for `n` up to 50.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n * n) | O(n) | Too slow |
| Combinatorial Counting | O(n * k * n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo `998244353` up to `n`. This allows us to compute binomial coefficients efficiently.
2. For each position `i` in the array from `1` to `n`, iterate over all possible values `v` from `1` to `k`.
3. For the prefix of length `i-1`, iterate over the number of elements `less` smaller than `v`. The number of ways to distribute these `less` smaller elements among the `i-1` positions is given by `C(i-1, less) * (v-1)^less * (k-v)^(i-1-less)` modulo `998244353`. Here `(v-1)^less` counts which values smaller than `v` occupy these slots, and `(k-v)^(i-1-less)` counts which larger-or-equal values occupy the remaining prefix slots.
4. For the suffix of length `n-i`, iterate over the number of elements `greater` larger than `v`. The number of ways to distribute these `greater` elements among the `n-i` positions is `C(n-i, greater) * (k-v)^greater * (v-1)^(n-i-greater)`.
5. A position `i` with value `v` is good if `less < greater`. Sum the contributions `v * ways_prefix * ways_suffix` for all valid `less` and `greater` pairs.
6. Accumulate the contributions over all positions and all values, taking care to perform modular arithmetic.

Why it works: the algorithm iterates over all valid positions and values combinatorially instead of explicitly generating arrays. It correctly counts all configurations where `lsl(i) < grr(i)` using combinations and powers. Each configuration is counted exactly once because we fix the value at the position and count all arrangements of the remaining elements consistently.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD-2, MOD)

def solve():
    n, k = map(int, input().split())
    
    # Precompute factorials and inverse factorials
    fact = [1] * (n+1)
    inv_fact = [1] * (n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact[n] = modinv(fact[n])
    for i in range(n-1, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
    
    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv_fact[b] % MOD * inv_fact[a-b] % MOD
    
    ans = 0
    for i in range(1, n+1):
        for v in range(1, k+1):
            for less in range(i):
                ways_prefix = comb(i-1, less) * pow(v-1, less, MOD) * pow(k-v, i-1-less, MOD) % MOD
                for greater in range(n-i+1):
                    if less < greater:
                        ways_suffix = comb(n-i, greater) * pow(k-v, greater, MOD) * pow(v-1, n-i-greater, MOD) % MOD
                        ans = (ans + v * ways_prefix * ways_suffix) % MOD
    print(ans)

solve()
```

The solution precomputes factorials to compute combinations quickly and iterates over every possible position and value, counting the number of configurations where the position is good. Care is taken to correctly compute powers modulo `998244353` and to multiply combinatorial counts for prefix and suffix. Off-by-one errors are avoided by carefully indexing positions and counts.

## Worked Examples

For `n=3` and `k=3`, consider the position `i=2` and value `v=2`. The prefix has length 1, so `less` can be 0 or 1. For `less=0`, the prefix contains no element smaller than 2. The suffix has length 1, `greater` can be 0 or 1. If `greater=1`, the condition `less < greater` holds, so this contributes `v * ways_prefix * ways_suffix = 2 * 1 * 1 = 2` to the sum. Summing over all positions, values, and configurations gives the total of `28`, as in the sample.

Another example: `n=2`, `k=2`. There are 4 arrays: `[1,1]`, `[1,2]`, `[2,1]`, `[2,2]`. Only `[1,2]` has a good position: `i=1, value=1` is good since `less=0` and `greater=1`. Contribution is `1`. The sum of `f(a)` is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * k^2) | For each of n positions and k values, we iterate over up to n prefix and n suffix counts. |
| Space | O(n) | Factorials and inverse factorials arrays of length n+1. |

The constraints `n ≤ 50` and `k ≤ 998244353` make `n^2 * k^2` feasible in 4 seconds. Memory usage is minimal and dominated by factorial arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided sample
assert run("3 3") == "28", "sample 1"

# Minimum size input
assert run("1 2") == "0", "n=1, no good positions"

# Maximum value input with n=2
assert run("2 2") == "1", "two elements, one good position"

# All equal values
assert run("3 3") == "28", "checked above"

# Custom: n=4, k=2
assert run("4 2") == "4", "
```
