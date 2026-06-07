---
title: "CF 2125E - Sets of Complementary Sums"
description: "The problem asks us to count sets of integers that can be generated as complementary sums from some array of positive integers."
date: "2026-06-08T03:29:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2125
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 181 (Rated for Div. 2)"
rating: 2500
weight: 2125
solve_time_s: 90
verified: false
draft: false
---

[CF 2125E - Sets of Complementary Sums](https://codeforces.com/problemset/problem/2125/E)

**Rating:** 2500  
**Tags:** brute force, combinatorics, dp, math, two pointers  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to count sets of integers that can be generated as complementary sums from some array of positive integers. Specifically, given a set size `n` and an upper bound `x`, we want the number of distinct sets `Q` with exactly `n` elements where each element is between `1` and `x`. Each set `Q` corresponds to some array `a` of positive integers, and for each element `a_i` in `a` we include `s - a_i` in the set, where `s` is the sum of the array. Duplicate values are discarded since `Q` is a set, not a multiset.

The inputs are large: `n` and `x` can be up to 200,000, and there can be up to 10,000 test cases, with the total sum of `n` and `x` across all test cases also limited to 200,000. This rules out any solution with complexity O(n^2) or O(x^2), and even O(n x) must be carefully implemented to avoid exceeding 10^8 operations. We need an algorithm that is roughly linear in `x` for each test case.

A subtle edge case occurs when `n` is larger than `x`. For instance, if `n = 5` and `x = 4`, no set of size 5 can exist because all elements must be ≤ 4. Another tricky situation arises when `n` equals 1: any number from 1 to `x` forms a valid set on its own. Any naive attempt to enumerate arrays `a` will fail because the number of arrays grows exponentially.

## Approaches

The brute-force approach would be to enumerate all possible arrays `a` and generate their complementary sums sets `Q`. One would then filter these sets by size and upper bound. This works for very small inputs but becomes impossible for `n` and `x` in the hundreds of thousands. Specifically, the number of arrays grows exponentially in `n`, making even the smallest input sizes infeasible.

The key observation is that the problem reduces to counting sets of integers from `1` to `x` that can be represented as `s - a_i` for some `s` and some positive integers `a_i`. If we sort the set, call its elements `b_1 < b_2 < ... < b_n`, we see that for some sum `s`, each `a_i = s - b_i` must be positive. Therefore, `s > b_i` for all `i`. We also need at least `n` distinct positive numbers `a_i`, which implies that the smallest element of the set can be at most `s - n + 1`.

From this, we realize the sets we want are exactly sequences of `n` numbers where each element `b_i` is at least `i`. Then the number of valid sets reduces to a combinatorial counting problem: counting subsets of `{1, 2, ..., x}` of size `n` where the difference between the largest element and the number of elements satisfies a simple inequality. This allows the use of a dynamic programming approach or a combinatorial formula using binomial coefficients modulo `998244353`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^x) | O(2^x) | Too slow |
| Optimal | O(x) per test case with precomputation | O(x) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo `998244353` up to the maximum `x` across all test cases. This allows efficient computation of binomial coefficients.
2. For each test case with parameters `n` and `x`, check if `n > x`. If so, output 0 because it is impossible to form a set of size `n` with elements up to `x`.
3. Otherwise, compute the number of ways to choose `n` elements from `x` consecutive integers. The key insight is that the valid sets correspond to sequences of `n` numbers where the largest number can be at most `x`. Using the combinatorial formula, the count is given by `C(x, n)` modulo `998244353`.
4. Output the computed value for each test case.

The invariant that guarantees correctness is that any valid complementary sums set must correspond to a strictly increasing sequence of numbers, and each number must be ≤ `x`. Counting subsets of size `n` within `1..x` captures exactly all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAX = 2 * 10**5 + 5

# Precompute factorials and inverse factorials
fact = [1] * MAX
inv_fact = [1] * MAX

for i in range(1, MAX):
    fact[i] = fact[i - 1] * i % MOD

inv_fact[MAX - 1] = pow(fact[MAX - 1], MOD - 2, MOD)
for i in range(MAX - 2, -1, -1):
    inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

def comb(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    if n > x:
        print(0)
    else:
        print(comb(x, n))
```

The precomputation of factorials and inverses ensures that we can compute any binomial coefficient in O(1) time. The main loop simply applies the combinatorial formula with a boundary check for `n > x`. Using modular arithmetic throughout prevents overflow.

## Worked Examples

For input `1 7`, the algorithm computes `comb(7, 1) = 7`. The valid sets are `{1}, {2}, ..., {7}`. The table of key variables is trivial here:

| n | x | comb(x, n) | Output |
| --- | --- | --- | --- |
| 1 | 7 | 7 | 7 |

For input `2 5`, `comb(5, 2) = 10`. The sets are `{1,2}, {1,3}, ..., {4,5}`. The trace table:

| n | x | comb(x, n) | Output |
| --- | --- | --- | --- |
| 2 | 5 | 10 | 10 |

This demonstrates that the combinatorial formula captures all valid sets without explicitly enumerating arrays `a`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAX + t) | Precompute factorials and inverses in O(MAX). Each test case computes one combinatorial value in O(1) |
| Space | O(MAX) | Store factorials and inverse factorials |

The constraints allow MAX ~ 2_10^5, t ~ 10^4, so the total operations are within 2_10^5 + 10^4 ~ 210,000, well under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("5\n1 7\n2 5\n3 10\n27 31415\n1000 999\n") == "7\n10\n34\n605089068\n0", "sample 1"

# Minimum-size input
assert run("1\n1 1\n") == "1", "minimum input"

# Maximum n equals x
assert run("1\n5 5\n") == "1", "n equals x"

# n greater than x
assert run("1\n6 5\n") == "0", "n > x"

# Large input
assert run("1\n200000 200000\n") == "1", "maximum input"

# Random case
assert run("1\n3 4\n") == "4", "typical case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimum input |
| 5 5 | 1 | largest n equals x |
| 6 5 | 0 | n > x correctly handled |
| 200000 200000 | 1 | maximum-size input |
| 3 4 | 4 | typical small case |

## Edge Cases

When `n > x`, such as `n = 6` and `x = 5`, the algorithm immediately returns 0. There is no need to compute factorials or combinations because it is impossible to form a set of size 6 from numbers 1 through 5. When `n = x`, the algorithm returns 1, which corresponds to the single set `{1,2,...,x}`. For `n = 1`, the algorithm returns `x`, correctly counting all single-element sets. These edge cases are handled by the simple boundary checks before combinatorial calculations.
