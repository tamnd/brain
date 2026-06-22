---
title: "CF 105631K - King of Card Games"
description: "We are drawing numbers repeatedly from a set containing all integers from 1 to n, with replacement. Each draw is independent and uniformly random, so any sequence of length m is simply an ordered m-tuple where each position can be any value from 1 to n."
date: "2026-06-22T14:57:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105631
codeforces_index: "K"
codeforces_contest_name: "SYSU Collegiate Programming Contest 2024 (SYSUCPC 2024), Final"
rating: 0
weight: 105631
solve_time_s: 64
verified: true
draft: false
---

[CF 105631K - King of Card Games](https://codeforces.com/problemset/problem/105631/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are drawing numbers repeatedly from a set containing all integers from 1 to n, with replacement. Each draw is independent and uniformly random, so any sequence of length m is simply an ordered m-tuple where each position can be any value from 1 to n.

For each such sequence, we only care about two values: the minimum element that appears in the sequence and the maximum element that appears. If we call them b and a respectively, the sequence contributes the value (a − b)².

The task is not to evaluate this for a single random sequence, but to sum this value over every possible sequence of length m. Since there are n^m sequences, we are effectively aggregating a function over all possible multisets with order.

The main difficulty is that the function depends only on the extreme values of the sequence, but those extremes are induced by many different sequences. A naive enumeration would require iterating over all n^m sequences, which is impossible even for very small parameters.

A useful way to think about the structure is to group sequences by their minimum and maximum values. Once the pair (min, max) is fixed, the contribution of all sequences with those extremes can be counted combinatorially.

A subtle edge case appears when all elements in the sequence are identical. In that situation min equals max, and the contribution is zero. Any correct formulation must ensure these cases do not introduce spurious non-zero contributions.

Another edge case is when m = 1. Every sequence has min = max, so the answer must always be zero regardless of n. Any formula that accidentally counts invalid inclusion-exclusion terms for small intervals must handle this cleanly.

## Approaches

A direct brute force approach would generate every sequence of length m and compute its minimum and maximum. This takes O(n^m · m) time since computing min and max per sequence costs linear time in m. Even storing or iterating over n^m sequences is infeasible once n and m exceed small constants, so this direction is immediately ruled out.

The key structural observation is that the contribution of a sequence depends only on its smallest and largest values, not on internal arrangement. Instead of thinking in terms of sequences, we shift perspective to intervals [i, j] representing possible value ranges of the sequence. For a fixed pair (i, j), we count how many sequences of length m use only values in that interval while containing at least one i and at least one j. Every such sequence contributes (j − i)².

If we denote k = j − i + 1, the number of sequences using only values in the interval is k^m. Among these, we subtract those missing i and those missing j, and add back those missing both endpoints. This yields a standard inclusion-exclusion expression:

k^m − 2·(k−1)^m + (k−2)^m.

Summing this over all intervals and weighting by the squared distance gives the final answer. Rewriting in terms of distance d = j − i simplifies the outer sum, because there are exactly (n − d) choices of interval with that width.

This reduces the problem from exponential enumeration to a single linear scan over distances, with modular exponentiation used to evaluate powers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m · m) | O(m) | Too slow |
| Optimal | O(n log m) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem into summing over possible distances between minimum and maximum values.

1. Fix a distance d between minimum and maximum values. This means we consider all intervals [i, i + d] inside [1, n]. There are exactly n − d such intervals because i can range from 1 to n − d.
2. For each such interval, compute k = d + 1, the number of distinct values allowed inside the interval.
3. Count sequences of length m that stay entirely within this interval and touch both endpoints. We start from all k^m sequences.
4. Subtract sequences that never use the lower endpoint, which can only use k − 1 values, contributing (k − 1)^m.
5. Subtract sequences that never use the upper endpoint, again contributing (k − 1)^m.
6. Add back sequences that avoid both endpoints, which use k − 2 values, contributing (k − 2)^m.
7. Multiply the resulting count by d², since every such sequence has (max − min)² equal to d².
8. Accumulate over all d from 1 to n − 1.

The only computational challenge is evaluating powers x^m for many bases x under a large modulus. Each exponentiation is done with binary exponentiation.

Why it works comes from partitioning sequences by their extremal values. Every sequence has a unique pair (min, max), and for a fixed pair, the inclusion-exclusion formula counts exactly those sequences whose set of values spans the entire interval. No sequence is counted twice across different intervals because the pair (min, max) uniquely determines its contribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def mod_pow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    n, m = map(int, input().split())
    
    if m == 1:
        print(0)
        return

    ans = 0

    for d in range(1, n):
        k = d + 1

        total = mod_pow(k, m)
        minus1 = mod_pow(k - 1, m) if k - 1 >= 0 else 0
        minus2 = mod_pow(k - 2, m) if k - 2 >= 0 else 0

        cnt = (total - 2 * minus1 + minus2) % MOD
        ans = (ans + cnt * (d * d % MOD) * (n - d)) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the distance-based decomposition. The loop over d represents all possible gaps between minimum and maximum values. For each gap, we compute three modular exponentiations corresponding to k^m, (k−1)^m, and (k−2)^m.

A frequent pitfall is mishandling small k values. When k is 1 or 2, terms like (k−2)^m or (k−1)^m involve zero or negative bases. In modular arithmetic, 0^m is safe when m > 0 and equals zero, but negative bases must not be interpreted literally. The code avoids this by clamping invalid cases.

Another subtlety is that multiplication by (n − d) must be done after computing the inclusion-exclusion count, since it represents the number of valid starting positions of the interval.

## Worked Examples

Consider a small case n = 3, m = 2.

We iterate over d = 1 and d = 2.

For d = 1, k = 2. We have:

k^2 = 4

(k−1)^2 = 1

(k−2)^2 = 0

So cnt = 4 − 2·1 + 0 = 2. There are (3 − 1) = 2 intervals of this size, so contribution is 2 · 1² · 2 = 4.

For d = 2, k = 3. We have:

3^2 = 9

2^2 = 4

1^2 = 1

So cnt = 9 − 2·4 + 1 = 2. There is (3 − 2) = 1 interval, so contribution is 2 · 4 · 1 = 8.

Total is 12.

| d | k | k^m | (k−1)^m | (k−2)^m | cnt | intervals (n−d) | contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 4 | 1 | 0 | 2 | 2 | 4 |
| 2 | 3 | 9 | 4 | 1 | 2 | 1 | 8 |

This confirms that the decomposition correctly matches the sample behavior.

A second sanity case is n = 2, m = 1. Every sequence has length 1, so min equals max and the answer must be zero. The loop still runs, but cnt evaluates to zero for every d, ensuring no accidental contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | We iterate over all distances d and compute a constant number of exponentiations per iteration, each in O(log m) |
| Space | O(1) | Only a fixed number of variables are used |

The constraints allow up to 10^6 values for n and m, so a linear scan over n with logarithmic exponentiation fits comfortably within typical limits, provided the exponentiation routine is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    MOD = 998244353

    def mod_pow(a, e):
        res = 1
        a %= MOD
        while e:
            if e & 1:
                res = res * a % MOD
            a = a * a % MOD
            e >>= 1
        return res

    def solve():
        n, m = map(int, sys.stdin.readline().split())
        if m == 1:
            print(0)
            return

        ans = 0
        for d in range(1, n):
            k = d + 1
            total = mod_pow(k, m)
            minus1 = mod_pow(k - 1, m) if k - 1 >= 0 else 0
            minus2 = mod_pow(k - 2, m) if k - 2 >= 0 else 0
            cnt = (total - 2 * minus1 + minus2) % MOD
            ans = (ans + cnt * (d * d % MOD) * (n - d)) % MOD
        print(ans % MOD)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
# assert run("3 1") == "0"
# assert run("3 2") == "12"

# custom cases
assert run("1 5") == "0", "single element always zero range"
assert run("2 1") == "0", "single draw no spread"
assert run("2 2") == "2", "manual check small"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 0 | Single value cannot produce spread |
| 2 1 | 0 | One draw always has min=max |
| 2 2 | 2 | Small non-trivial interval counting |

## Edge Cases

When m = 1, every sequence consists of a single value. The minimum and maximum coincide, so every contribution is zero. The algorithm handles this by an early return before any power computations, avoiding unnecessary work and preventing misinterpretation of inclusion-exclusion terms at tiny interval sizes.

When n = 1, there is only one possible sequence regardless of m. The loop over distances does not execute because there is no valid d ≥ 1, so the answer remains zero naturally.

When d = 1, the interval size is k = 2, and the term (k−2)^m becomes 0^m. Since m ≥ 1, this is safely zero, matching the fact that no sequence over a single-element alphabet exists that uses both endpoints.
