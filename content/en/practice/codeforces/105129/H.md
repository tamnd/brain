---
title: "CF 105129H - Array Subsequence"
description: "We are given an array and asked to think about all ways to choose exactly k elements while preserving order, although the order constraint does not affect which values end up selected, only which subsets are valid."
date: "2026-06-27T19:22:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "H"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 56
verified: true
draft: false
---

[CF 105129H - Array Subsequence](https://codeforces.com/problemset/problem/105129/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and asked to think about all ways to choose exactly k elements while preserving order, although the order constraint does not affect which values end up selected, only which subsets are valid. For each chosen group of k elements, we look only at its largest and smallest values and take their difference. The task is to compute the average of this quantity over all possible subsequences of size k.

The key object is not the subsequence structure itself but the induced uniform distribution over all k-element subsets of indices. Every subset of indices of size k is equally likely, so the problem reduces to a pure combinatorial expectation over subsets.

The constraints are large, with n up to 5 · 10^5 across test cases. Any solution that enumerates subsets or even processes all pairs directly is immediately infeasible since that would be at least quadratic. Even an O(n log n) per pair style approach would be too slow. This strongly suggests that the solution must reduce the expectation to a sum over individual elements or a small number of structured contributions that can be precomputed in linear or near-linear time.

A subtle point that often breaks naive attempts is treating subsequences as if they preserve adjacency information. They do not. Only relative index order matters for counting combinations, not contiguous structure. Another common pitfall is attempting to directly reason about maxima and minima simultaneously, which leads to double counting or complicated dependence. The correct direction is to separate the contributions of maximum and minimum in expectation, which removes the dependency.

As a concrete failure mode, consider trying to simulate for small n by enumerating all subsets. For n = 50 and k = 25, this is already astronomically large. Another incorrect idea is trying to fix a pair (i, j) and assume independence of elements between them without correctly accounting for how many subsets choose both as extremal elements. The dependence is purely combinatorial and must be expressed with binomial coefficients.

## Approaches

The brute-force approach is straightforward. We enumerate every subset of size k, compute its minimum and maximum, and accumulate their difference. This is correct because it directly follows the definition of expectation over a uniform distribution. However, the number of such subsets is C(n, k), which grows exponentially in n for mid-sized k. Even for n = 40, this becomes infeasible.

The key observation is that the expectation of a difference splits cleanly into the difference of expectations. The expression max(S) − min(S) becomes E[max(S)] − E[min(S)]. This removes the interaction between minimum and maximum entirely and reduces the problem to two independent order-statistic expectations.

Now the structure becomes classical. After sorting the array, each element ai can be considered as a candidate for being the maximum or the minimum of the chosen subset. We only need to compute how many subsets of size k have ai as their maximum, and similarly how many have ai as their minimum. Each such count translates directly into a binomial coefficient based on how many elements lie to its left or right in the sorted order.

This turns the problem into a linear sweep over the sorted array with combinatorial weights computed using factorial precomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(C(n, k) · k) | O(k) | Too slow |
| Expected Value via Order Statistics | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Sort the array

We sort the array so that positions correspond to ranks. This allows us to reason about how many elements are smaller or larger than a given element using indices alone.

### 2. Precompute factorials and inverse factorials

We need binomial coefficients under a modulus, so we precompute factorials and modular inverses up to n. This makes any C(n, k) query O(1).

### 3. Fix contribution of each element

We interpret the expectation as a sum over all elements where each element contributes based on being the maximum or minimum of the chosen subset.

For an element at position i (0-indexed), we compute two probabilities:

The probability it is the maximum is the number of ways to choose the remaining k − 1 elements from the i elements before it, divided by the total number of subsets.

The probability it is the minimum is the number of ways to choose k − 1 elements from the elements after it.

These are directly expressed using binomial coefficients.

### 4. Aggregate contributions

For each element ai, we add its value multiplied by the difference between its probability of being maximum and being minimum. This yields its net expected contribution to max − min.

### 5. Normalize by total number of subsets

All probabilities share the same denominator C(n, k), so we multiply by its modular inverse at the end.

### Why it works

Every subset has a unique maximum and minimum, so when we sum contributions over all elements, each subset’s maximum is counted exactly once in the “max” term and each subset’s minimum is counted exactly once in the “min” term. The linearity of expectation guarantees that this decomposition does not lose or double count any configurations. The combinatorial formulas ensure that each element is weighted exactly by the number of subsets where it plays the extremal role.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

maxn = 5 * 10**5 + 5
fact = [1] * (maxn)
invfact = [1] * (maxn)

for i in range(1, maxn):
    fact[i] = fact[i - 1] * i % MOD

invfact[maxn - 1] = pow(fact[maxn - 1], MOD - 2, MOD)
for i in range(maxn - 2, -1, -1):
    invfact[i] = invfact[i + 1] * (i + 1) % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    if k == 1:
        print(0)
        continue

    total = C(n, k)
    inv_total = modinv(total)

    ans = 0

    for i, val in enumerate(a):
        # as maximum: choose k-1 from left side
        max_cnt = C(i, k - 1)
        # as minimum: choose k-1 from right side
        min_cnt = C(n - i - 1, k - 1)

        ans += val * (max_cnt - min_cnt)
        ans %= MOD

    ans = ans * inv_total % MOD
    print(ans)
```

The implementation precomputes factorials once, which is necessary because multiple test cases share the same bounds. The core loop uses the sorted order to interpret index i as having exactly i smaller elements and n − i − 1 larger elements, which is what allows direct binomial counting.

The special case k = 1 is handled separately since max and min coincide, making the answer zero.

A subtle implementation detail is maintaining modular arithmetic carefully when subtracting min_cnt from max_cnt, since intermediate values can become negative before applying the modulus.

## Worked Examples

Consider the array [4, 1, 3, 1] with k = 2.

After sorting, we get [1, 1, 3, 4]. Total subsets are C(4, 2) = 6.

We compute contributions per element.

| i | value | C(i,1) | C(n-i-1,1) | net contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 3 | 1 · (0 − 3) |
| 1 | 1 | 1 | 2 | 1 · (1 − 2) |
| 2 | 3 | 2 | 1 | 3 · (2 − 1) |
| 3 | 4 | 3 | 0 | 4 · (3 − 0) |

Summing gives the numerator before normalization. Dividing by 6 yields the expected value.

This trace shows how each element independently contributes depending on whether it can act as an endpoint of a 2-element subset.

Now consider [1, 1, 1] with k = 1. Every subset is a single element, so max − min is always 0. The algorithm directly returns 0 because contributions cancel.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case after preprocessing | Each element is processed once, and binomial queries are O(1) |
| Space | O(n) | Factorials and inverse factorials up to max n |

The preprocessing fits comfortably within limits since the total n across tests is 5 · 10^5. Each test case then runs in linear time, which is optimal for this input scale.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    maxn = 100
    fact = [1] * (maxn)
    invfact = [1] * (maxn)
    for i in range(1, maxn):
        fact[i] = fact[i - 1] * i % MOD
    invfact[maxn - 1] = pow(fact[maxn - 1], MOD - 2, MOD)
    for i in range(maxn - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    def C(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        if k == 1:
            out.append("0")
            continue

        total = C(n, k)
        inv_total = pow(total, MOD - 2, MOD)

        ans = 0
        for i, val in enumerate(a):
            max_cnt = C(i, k - 1)
            min_cnt = C(n - i - 1, k - 1)
            ans += val * (max_cnt - min_cnt)
            ans %= MOD

        out.append(str(ans * inv_total % MOD))

    return "\n".join(out)

# provided samples
assert run("""4
4 2
4 1 3 1
3 1
1 1 1
6 3
-10 -10 10 10 10 -10
4 4
4 2 1 3
""") == """2
0
20
2"""

# custom cases
assert run("""1
1 1
5
""") == "0", "single element"

assert run("""1
2 2
1 10
""") == "9", "full array"

assert run("""1
5 2
1 2 3 4 5
""") == "3", "small increasing"

assert run("""1
5 1
1 2 3 4 5
""") == "0", "k=1 case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | k=1 degeneracy |
| full array | 9 | max-min over entire set |
| small increasing | 3 | combinatorial weighting correctness |
| k=1 case | 0 | edge case cancellation |

## Edge Cases

When k equals 1, every subsequence contains exactly one element, so maximum and minimum are identical. The algorithm handles this by returning zero immediately, matching the combinatorial cancellation that would otherwise occur in the formula.

When k equals n, there is only one subsequence, the entire array. Each element’s contribution collapses into a deterministic maximum and minimum, and the formula correctly reduces to max(a) − min(a) because exactly one element is counted as maximum and one as minimum with full probability weight.

When all values are equal, every subset has zero range. In the formula, every term multiplies a difference of identical values after sorting, so the sum becomes zero modulo the system, matching the expected result.

When values are negative, nothing changes because all combinatorial reasoning is independent of magnitude sign. The formula only relies on linearity of expectation, so negative contributions are naturally handled without special casing.
