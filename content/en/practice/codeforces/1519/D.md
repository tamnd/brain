---
title: "CF 1519D - Maximum Sum of Products"
description: "We are given two arrays of integers, a and b, both of the same length n. The task is to maximize the sum of element-wise products, $sum ai cdot bi$, by reversing at most one contiguous subarray of a."
date: "2026-06-10T18:12:35+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1519
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 108 (Rated for Div. 2)"
rating: 1600
weight: 1519
solve_time_s: 124
verified: true
draft: false
---

[CF 1519D - Maximum Sum of Products](https://codeforces.com/problemset/problem/1519/D)

**Rating:** 1600  
**Tags:** brute force, dp, implementation, math, two pointers  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of integers, `a` and `b`, both of the same length `n`. The task is to maximize the sum of element-wise products, $\sum a_i \cdot b_i$, by reversing at most one contiguous subarray of `a`. Reversing a subarray means picking a segment of `a` and flipping the order of its elements, while `b` remains unchanged.

The constraints give us `n` up to 5000. This means an O(n^3) solution is impractical, as it could require around 125 billion operations. An O(n^2) solution may be feasible with careful implementation. Values in `a` and `b` can be up to 10^7, so we must use a data type capable of storing sums up to roughly `5000 * 10^7 * 10^7 = 5 * 10^18`. Python's `int` handles this without overflow.

Edge cases include small arrays of length 1 or 2, where reversing may not improve the sum. Another subtle case occurs when the optimal subarray is the entire array, or when no reversal is needed because the array is already aligned with `b` for maximum sum. For example, `a = [1, 2, 3]`, `b = [3, 2, 1]`. Reversing the entire `a` gives `[3, 2, 1]` and maximum sum `3*3 + 2*2 + 1*1 = 14`.

## Approaches

The brute-force method is straightforward: iterate over all possible subarrays `(l, r)` of `a`, reverse the subarray, compute the sum $\sum a_i \cdot b_i$, and track the maximum. This works because every valid reversal is considered. However, this requires O(n^3) operations: O(n^2) for all subarrays and O(n) to compute each sum. With `n` up to 5000, this is far too slow.

The key insight is that reversing a subarray changes only the contributions of that subarray to the total sum. The parts of `a` outside the reversed segment remain aligned with `b`. We can therefore precompute the total sum without reversal and focus only on the "gain" from reversing subarrays.

We can exploit symmetry: consider a subarray from `l` to `r`. If we reverse it, the contribution of elements `a[l+i] * b[l+i]` changes to `a[r-i] * b[l+i]`. By expanding from the center of the subarray outward, we can compute the gain incrementally in O(n^2) time. This two-pointers or dynamic expansion technique reduces the complexity from O(n^3) to O(n^2), which is feasible for `n=5000`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n^2) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the initial sum of products without any reversal. Call this `base_sum`.
2. Initialize `max_gain = 0` to track the maximum increase from reversing any subarray.
3. Consider every possible center for a subarray. For odd-length subarrays, a single element can be the center; for even-length subarrays, the center is between two elements.
4. Expand symmetrically around the center. Let `l` and `r` be the indices being swapped in this expansion. Compute the gain `gain = a[r] * b[l] + a[l] * b[r] - a[l] * b[l] - a[r] * b[r]`. This is the net increase in sum if we reverse this pair.
5. Accumulate `gain` as we expand outward, and update `max_gain` whenever the accumulated gain exceeds it.
6. After checking all possible centers, the answer is `base_sum + max_gain`.

Why it works: reversing a subarray affects only the positions inside it. By expanding from the center outward and calculating the incremental gain at each step, we ensure every possible subarray is considered exactly once. Since the gain is computed relative to the original sum, the sum outside the subarray remains unchanged, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

base_sum = sum(a[i] * b[i] for i in range(n))
max_gain = 0

# Odd-length centers
for center in range(n):
    gain = 0
    l, r = center - 1, center + 1
    while l >= 0 and r < n:
        gain += a[r] * b[l] + a[l] * b[r] - a[l] * b[l] - a[r] * b[r]
        if gain > max_gain:
            max_gain = gain
        l -= 1
        r += 1

# Even-length centers
for center in range(n - 1):
    gain = 0
    l, r = center, center + 1
    while l >= 0 and r < n:
        gain += a[r] * b[l] + a[l] * b[r] - a[l] * b[l] - a[r] * b[r]
        if gain > max_gain:
            max_gain = gain
        l -= 1
        r += 1

print(base_sum + max_gain)
```

The code first computes the sum without any reversal. Then it examines all odd-length and even-length subarrays by expanding from a center. The incremental gain formula ensures we only account for swapped contributions, avoiding recomputing the sum from scratch. Boundary handling for `l` and `r` guarantees no index errors.

## Worked Examples

**Sample 1:**

Input: `a = [2,3,2,1,3], b = [1,3,2,4,2]`

| l | r | a[l]*b[l]+a[r]*b[r] | a[r]*b[l]+a[l]*b[r] | gain | max_gain |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 1_4+3_2=10 | 3_4+1_2=14 | 4 | 4 |
| 2 | 5 | ... | ... | ... | 4 |

The optimal subarray to reverse is `[1, 3]` (indices 3 to 4), giving a gain of 4. Base sum is 25, so maximum sum is 29.

**Sample 2:**

Input: `a = [1,2,3], b = [3,2,1]`

| l | r | gain | max_gain |
| --- | --- | --- | --- |
| 0 | 2 | (3_1 +1_3)-(1_3 +3_1)=0 | 0 |

Reversing the full array gives no additional gain in this expansion, base sum is 10, maximum sum remains 10.

This demonstrates the gain computation correctly identifies when no reversal improves the sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each possible center (O(n)), we expand outward up to n/2 times |
| Space | O(1) | Only a few variables to track sums and gains; no extra arrays |

O(n^2) operations with n=5000 is approximately 25 million, acceptable under a 2-second limit in Python. Memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    base_sum = sum(a[i] * b[i] for i in range(n))
    max_gain = 0

    for center in range(n):
        gain = 0
        l, r = center - 1, center + 1
        while l >= 0 and r < n:
            gain += a[r] * b[l] + a[l] * b[r] - a[l] * b[l] - a[r] * b[r]
            if gain > max_gain:
                max_gain = gain
            l -= 1
            r += 1

    for center in range(n - 1):
        gain = 0
        l, r = center, center + 1
        while l >= 0 and r < n:
            gain += a[r] * b[l] + a[l] * b[r] - a[l] * b[l] - a[r] * b[r]
            if gain > max_gain:
                max_gain = gain
            l -= 1
            r += 1

    return str(base_sum + max_gain)

# provided samples
assert run("5\n2 3 2 1 3\n1 3 2 4 2\n") == "29", "sample 1"
assert run("2\n13 37\n2 4\n") == "174", "sample 2"

# custom cases
assert run("3\n1 2 3\n3
```
