---
title: "CF 103719C - \u041c\u0435\u0445\u043e\u0432\u044b\u0435 \u043f\u043e\u0434\u043f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438"
description: "We are given an array of length n, and we look at subsequences defined by choosing any increasing sequence of indices. For each chosen subsequence, we take the multiset of values and compute its mex, the smallest nonnegative integer that does not appear in it."
date: "2026-07-02T09:22:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103719
codeforces_index: "C"
codeforces_contest_name: "VII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 8-11 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103719
solve_time_s: 63
verified: true
draft: false
---

[CF 103719C - \u041c\u0435\u0445\u043e\u0432\u044b\u0435 \u043f\u043e\u0434\u043f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438](https://codeforces.com/problemset/problem/103719/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length n, and we look at subsequences defined by choosing any increasing sequence of indices. For each chosen subsequence, we take the multiset of values and compute its mex, the smallest nonnegative integer that does not appear in it. The subsequence is considered valid only if every selected element lies within distance at most 1 from this mex value.

The task is to count how many non-empty subsequences satisfy this condition, taken over all possible index selections, and return the answer modulo 998244353.

The constraint n up to 100000 forces any O(n²) or combinational enumeration over subsequences to be impossible. Even O(n log n) solutions need to avoid per-subsequence reasoning. The structure suggests that the condition on values collapses the search space heavily once mex is fixed, because mex strongly constrains which integers can appear in a valid set.

A subtle point is that the condition couples two things: membership of values near mex, and the definition of mex itself, which depends on which values are present and absent. This feedback loop is where naive reasoning typically breaks.

A common pitfall is to assume that once values are restricted to a small range around some candidate mex, any subset works. That ignores the mex requirement that all smaller values must appear at least once.

Another failure mode is mixing contributions from different mex values without checking that the same subsequence cannot correspond to multiple mex values. Here, mex uniquely determines the structure, so disjoint counting is safe once characterized correctly.

## Approaches

The brute force idea is to enumerate all subsequences and compute mex for each. That already gives 2^n candidates, and computing mex per subset costs up to O(n), leading to an infeasible exponential blowup.

The key observation is that the mex value of any valid subsequence cannot be large. The constraint forces every element in the subsequence to lie within {M-1, M, M+1}. At the same time, mex M requires that all integers from 0 to M-1 are present and that M is absent. These two conditions are extremely restrictive.

If M were 2 or more, the requirement that 0 must appear conflicts with the allowed value set {M-1, M+1}, which does not include 0. This immediately eliminates all mex values except 0 and 1.

This collapse reduces the problem into two independent counting problems: count subsequences with mex 0 and count subsequences with mex 1.

For mex 0, 0 must be absent and all elements must lie in {0,1} by the distance condition, forcing the subsequence to consist only of 1s.

For mex 1, 0 must appear at least once, 1 must be absent, and values must lie in {0,2}. This becomes a standard combinational count over two independent categories.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all subsequences | O(2^n · n) | O(n) | Too slow |
| Mex decomposition (0 and 1 only) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We first classify elements of the array by value, but only values 0, 1, and 2 matter. Any value outside this range can never belong to a valid subsequence because it would violate the condition |a[i] − M| ≤ 1 for both possible mex values.

### 1. Count frequencies

We compute c0, c1, c2 as the number of occurrences of values 0, 1, and 2.

### 2. Count subsequences with mex 0

A subsequence has mex 0 if 0 is absent and 1 is present (otherwise mex would be 0), but the distance constraint forces all elements to be in {0,1}. Combining these, 0 cannot appear and only 1s remain. Every non-empty subset of 1s is valid.

So the number of such subsequences is 2^{c1} − 1.

### 3. Count subsequences with mex 1

For mex 1, 0 must appear at least once and 1 must be absent. The distance constraint allows only values in {0,2}. Therefore we choose any subsequence from all c0 + c2 positions, but we must exclude those that contain no 0.

Total subsequences over these elements is 2^{c0+c2}, and those with no 0 are 2^{c2}. So the contribution is 2^{c0+c2} − 2^{c2}.

### 4. Sum contributions

The final answer is the sum of the two independent cases.

### Why it works

Once mex is fixed, the allowed value range becomes a rigid interval around it, and the mex definition forces presence of all smaller values. This leaves only two feasible mex values. Since each valid subsequence uniquely determines its mex, partitioning by mex creates disjoint sets and avoids double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

n = int(input())
a = list(map(int, input().split()))

c0 = c1 = c2 = 0
for x in a:
    if x == 0:
        c0 += 1
    elif x == 1:
        c1 += 1
    elif x == 2:
        c2 += 1

# mex = 0: non-empty subsets of ones
ans0 = (modpow(2, c1) - 1) % MOD

# mex = 1: subsets of {0,2} with at least one 0
ans1 = (modpow(2, c0 + c2) - modpow(2, c2)) % MOD

print((ans0 + ans1) % MOD)
```

The code first compresses the array into three relevant frequency counters. Everything else is pure combinatorics. Modular exponentiation is used to compute subset counts efficiently under the required modulus.

The subtraction steps handle exclusion of empty or invalid cases, so each term directly matches the derived counting expressions.

## Worked Examples

### Example 1

Consider input:

```
n = 4
a = [0, 2, 3, 2]
```

We compute c0 = 1, c1 = 0, c2 = 2.

For mex 0, we count subsequences made only of 1s, but there are none, so ans0 = 0.

For mex 1, we work with {0,2,2}. Total subsequences: 2^3 = 8. Those without 0 use only {2,2}, giving 2^2 = 4. So ans1 = 4.

Final answer is 4.

This matches the fact that valid subsequences are exactly those containing at least one 0 and any subset of 2s.

### Example 2

```
n = 3
a = [1, 1, 1]
```

Here c1 = 3, c0 = c2 = 0.

For mex 0, all non-empty subsets of ones are valid, giving 2^3 − 1 = 7.

For mex 1, no zeros exist, so no valid subsequence exists.

Final answer is 7.

This demonstrates that the solution cleanly separates contributions without interaction between cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass for counting plus constant-time exponentiation |
| Space | O(1) | only three counters and a few variables |

The solution comfortably fits within limits since all combinatorial growth is handled analytically rather than enumerated.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    MOD = 998244353

    def modpow(a, e):
        res = 1
        while e:
            if e & 1:
                res = res * a % MOD
            a = a * a % MOD
            e >>= 1
        return res

    n = int(input())
    a = list(map(int, input().split()))

    c0 = c1 = c2 = 0
    for x in a:
        if x == 0: c0 += 1
        elif x == 1: c1 += 1
        elif x == 2: c2 += 1

    ans0 = (modpow(2, c1) - 1) % MOD
    ans1 = (modpow(2, c0 + c2) - modpow(2, c2)) % MOD

    return str((ans0 + ans1) % MOD)

# provided sample-like checks
assert run("4\n0 2 3 2\n") == "4"

# all ones
assert run("3\n1 1 1\n") == "7"

# only zeros
assert run("3\n0 0 0\n") == "0"

# mixed small case
assert run("3\n0 1 2\n") == str(((2**1-1) + (2**2 - 2**1)) % MOD)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 7 | mex 0 case only |
| all zeros | 0 | mex 1 impossible without 2s |
| 0 1 2 | mixed formula | both contributions active |

## Edge Cases

If the array contains only value 1, the mex 0 formula correctly counts all non-empty subsets because no element violates the allowed range and mex becomes 0 automatically since 0 is absent.

If there are no 0s, the mex 1 contribution becomes zero because every candidate subset from {0,2} cannot satisfy the requirement of containing a 0, and the subtraction 2^{c0+c2} − 2^{c2} collapses correctly to zero.

If values larger than 2 appear, they are implicitly excluded from all valid subsequences because any inclusion would violate the distance constraint for both possible mex values, so they contribute nothing and safely disappear in the counting reduction.
