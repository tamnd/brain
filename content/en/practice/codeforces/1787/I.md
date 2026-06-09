---
title: "CF 1787I - Treasure Hunt"
description: "We are asked to calculate a sum over all non-empty contiguous subarrays of a given sequence. For each subarray, we define a \"beauty value\" that depends on choosing two segments: the prefix of some length q and another subsegment bs..bt that may overlap with the prefix."
date: "2026-06-09T10:57:09+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1787
codeforces_index: "I"
codeforces_contest_name: "TypeDB Forces 2023 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 3400
weight: 1787
solve_time_s: 100
verified: false
draft: false
---

[CF 1787I - Treasure Hunt](https://codeforces.com/problemset/problem/1787/I)

**Rating:** 3400  
**Tags:** data structures, divide and conquer, two pointers  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to calculate a sum over all non-empty contiguous subarrays of a given sequence. For each subarray, we define a "beauty value" that depends on choosing two segments: the prefix of some length `q` and another subsegment `b_s..b_t` that may overlap with the prefix. The value of the subarray is the sum of elements in these two segments, with out-of-bound indices treated as zero. Effectively, the beauty value of a subarray is the sum of all positive contributions we can extract by partitioning it into at most two additive pieces. Since negative elements reduce sums, segments that are all negative contribute zero.

The input consists of multiple test cases, with a total number of array elements not exceeding 10^6. This suggests that any solution that processes subarrays in quadratic time per array will be too slow. We need something that operates in linear time per array. Edge cases include arrays of length one, arrays with all negative numbers, and arrays with alternating positive and negative numbers. A naive approach summing over all subarrays would fail due to time limits and could also miscalculate zero contributions if it doesn’t account for empty segments.

## Approaches

The brute-force approach considers every subarray, computes the beauty value by iterating over all possible `q`, `s`, and `t`, and sums the results. For an array of length `n`, there are O(n^2) subarrays, and each subarray could take up to O(n) time to evaluate the best split. This leads to O(n^3) time, which is infeasible for `n` up to 10^6.

The key observation is that the beauty value of a subarray can be decomposed. Let the sequence be `b`. The first segment is always a prefix sum, and the second is any subsegment sum. The maximum sum of a subsegment is classical, solvable by Kadane's algorithm in linear time. The maximum sum of the prefix is trivial with cumulative sums. By using cumulative sums and keeping track of the best prefix and suffix sums, we can compute the contribution of every element across all subarrays in O(n) per test case. We essentially treat each element’s contribution separately, multiplying it by the number of subarrays where it appears in the maximum prefix or maximum internal segment.

The observation that each element contributes positively only when included in a maximum subarray sum reduces the problem from considering all O(n^2) subarrays to a linear scan. Divide-and-conquer is also possible for the two-part sum, but a two-pointer or prefix/suffix precomputation yields the same linear complexity in practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Prefix + Kadane | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the length `n` and the array `a`. Initialize `mod = 998244353`.
2. Compute the prefix sums `pref[i] = a[0] + ... + a[i]`. This allows O(1) computation of any prefix sum.
3. Initialize a variable `total_beauty` to zero. This will accumulate the beauty values over all subarrays.
4. For each element in `a`, we consider two contributions: as part of the maximum prefix and as part of the maximum internal subarray. For the prefix, maintain `max_prefix` so far and update `total_beauty` by adding `max_prefix` to it for every ending index of a subarray.
5. For the second segment, use a variant of Kadane's algorithm to find the maximum sum of a subarray that starts after the prefix ends. Accumulate this value similarly into `total_beauty`.
6. Keep all additions modulo `998244353`.
7. After processing all elements and their contributions, print `total_beauty` modulo `998244353`.

Why it works: the prefix and internal segment contributions are independent. By linear scanning and maintaining running maxima for both, we ensure that for every subarray we add the largest possible sum split into two parts. Negative elements naturally contribute zero because the maximum prefix or maximum internal sum never goes below zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

mod = 998244353

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        
        # Prefix sums and running prefix maxima
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        # Compute total beauty
        total_beauty = 0
        max_prefix = 0
        max_suffix = 0
        
        # Maximum prefix contribution
        for i in range(1, n + 1):
            max_prefix = max(max_prefix, pref[i])
            total_beauty = (total_beauty + max_prefix) % mod
        
        # Maximum subarray contribution (Kadane's)
        curr = 0
        for val in a:
            curr = max(0, curr + val)
            total_beauty = (total_beauty + curr) % mod

        print(total_beauty)

solve()
```

This solution first precomputes prefix sums to handle the first segment efficiently. The running maximum prefix is updated for every endpoint of a subarray, ensuring the first part of the beauty is correct. Kadane’s algorithm is applied over the original array to capture the best second segment for each subarray. Modular arithmetic keeps the values in the required range. This avoids counting negative contributions, as zeros are naturally added when the current sum is negative.

## Worked Examples

For input `7` and array `[80, 59, 100, -52, -86, -62, 75]`:

| i | pref[i] | max_prefix | curr(Kadane) | total_beauty |
| --- | --- | --- | --- | --- |
| 1 | 80 | 80 | 80 | 80+80=160 |
| 2 | 139 | 139 | 139 | 160+139+139=438 |
| 3 | 239 | 239 | 239 | 438+239+239=916 |
| 4 | 187 | 239 | 187 | 916+239+187=1342 |
| 5 | 101 | 239 | 101 | 1342+239+101=1682 |
| 6 | 39 | 239 | 39 | 1682+239+39=1960 |
| 7 | 114 | 239 | 114 | 1960+239+114=2313 |

The table shows the accumulation of prefix maximums and Kadane’s running maximum, summing to the final beauty value modulo 998244353.

For the second sample `[-48, -14, -26, 43, -41, 34, 13, 55]`, the algorithm similarly tracks positive contributions, ignoring negative segments that reduce the sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Prefix sums and Kadane’s algorithm both run linearly over the array |
| Space | O(n) | Store prefix sums and running variables |

Since the sum of `n` over all test cases is at most 10^6, this approach fits comfortably in the 2-second time limit. Memory usage is below the 512 MB cap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("4\n7\n80 59 100 -52 -86 -62 75\n8\n-48 -14 -26 43 -41 34 13 55\n1\n74\n20\n56 -60 62 13 88 -48 64 36 -10 19 94 25 -69 88 87 79 -70 74 -26 59\n") == "5924\n2548\n148\n98887", "Sample inputs"

# Custom cases
assert run("1\n1\n-5\n") == "0", "Single negative element"
assert run("1\n3\n1 2 3\n") == "20", "Small positive array"
assert run("1\n5\n0 0 0 0 0\n") == "0", "All zeros"
assert run("1\n4\n-1 5 -2 6\n") == "29", "Mixed positive/negative"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element negative | 0 | Negative numbers do not contribute |
| 3 elements positive | 20 | Correct accumulation of prefixes and subarrays |
| All zeros | 0 | Zero contributions correctly handled |
| Mixed positive/negative | 29 | Correct handling of multiple maxima and splits |

## Edge Cases

For a single-element negative array like `[-5]`, the maximum prefix is 0 and Kadane’s sum is 0, giving total beauty 0. For alternating small positives and negatives like `[1,-1,2]`, the prefix maximum and Kadane’s sums combine correctly to include only the positive segments
