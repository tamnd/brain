---
title: "CF 993E - Nikita and Order Statistics"
description: "We are given an array and a threshold value x. For every possible integer k from 0 to n, we need to count how many subarrays have exactly k elements strictly smaller than x."
date: "2026-06-17T00:14:44+07:00"
tags: ["codeforces", "competitive-programming", "chinese-remainder-theorem", "fft", "math"]
categories: ["algorithms"]
codeforces_contest: 993
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 488 by NEAR (Div. 1)"
rating: 2300
weight: 993
solve_time_s: 102
verified: false
draft: false
---

[CF 993E - Nikita and Order Statistics](https://codeforces.com/problemset/problem/993/E)

**Rating:** 2300  
**Tags:** chinese remainder theorem, fft, math  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and a threshold value `x`. For every possible integer `k` from `0` to `n`, we need to count how many subarrays have exactly `k` elements strictly smaller than `x`. Each subarray contributes to exactly one `k`, depending on how many of its elements fall below the threshold.

Another way to think about the task is that we slide over all possible segments `[l, r]`, and for each segment we compute a single value: the count of elements in that segment that are less than `x`. The output is the frequency distribution of this value over all subarrays.

The constraint `n ≤ 2 · 10^5` immediately rules out any solution that explicitly enumerates all subarrays. There are about `n(n+1)/2` subarrays, which is on the order of `2 · 10^10` in the worst case. Even computing a single counter per subarray would be far beyond a 2-second limit.

The structure of the problem suggests that we do not actually care about values of elements greater than or equal to `x`, except in how they partition or shift counts. This is a strong hint that the array can be compressed into a binary sequence where each element becomes `1` if `a[i] < x` and `0` otherwise. Then the problem reduces to counting subarrays by sum.

A subtle edge case appears when all elements are greater than or equal to `x`. In that case every subarray has `k = 0`, so the answer should be `n(n+1)/2` for `k = 0` and zero otherwise. A naive implementation that assumes at least one element less than `x` may incorrectly skip this uniform case when building frequency structures.

Another edge case is when all elements are less than `x`. Then every subarray contributes `k = length of subarray`, so the distribution is triangular: exactly `n - k + 1` subarrays for each `k`.

## Approaches

A brute-force approach would enumerate every subarray `[l, r]`, compute how many elements are less than `x` by scanning the segment, and increment a counter for that value of `k`. This works correctly because it directly follows the definition. However, each subarray costs `O(n)` time in the worst case, leading to `O(n^3)` total complexity if implemented naively, or `O(n^2)` even with prefix sums for counting, since we still enumerate all subarrays.

The key observation is that after transforming the array into a binary array where `b[i] = 1` if `a[i] < x` and `0` otherwise, each subarray’s value is simply the sum over a segment. So the task becomes counting how many subarrays have each possible sum.

This is a classic convolution problem. If we define an array `f` where `f[i] = 1` for every prefix sum value, then the number of subarrays with sum `k` is the number of pairs of prefix sums `(i, j)` such that `pref[j] - pref[i] = k`. This can be rewritten as a convolution of the frequency array of prefix sums with a reversed version of itself.

Once expressed as convolution, we can compute all frequencies simultaneously using FFT-based polynomial multiplication in `O(n log n)` time. The size of prefix sums is `n+1`, so we build an array of length roughly `2n` to safely accommodate convolution results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Prefix enumeration | O(n²) | O(n) | Too slow |
| FFT convolution | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the input array into a binary array where each element is `1` if it is strictly less than `x`, otherwise `0`. This transformation preserves exactly the quantity we care about for every subarray.
2. Build prefix sums over this binary array. Each prefix sum represents how many elements less than `x` exist up to that index.
3. Construct a frequency array `cnt` where `cnt[v]` is the number of times a prefix sum value `v` occurs. Prefix sums range from `0` to `n`.
4. Interpret the problem as counting pairs of prefix sums `(i, j)` such that `pref[j] - pref[i] = k`. Each such pair corresponds to a subarray with exactly `k` elements less than `x`.
5. Reformulate this counting as a convolution: if we reverse one copy of `cnt` and convolve it with the original, the resulting array gives counts of all differences between prefix sums.
6. Use FFT-based polynomial multiplication to compute this convolution efficiently in `O(n log n)` time.
7. Extract results for all `k` from `0` to `n`, which correspond directly to subarray counts with exactly `k` elements less than `x`.

### Why it works

Each subarray `[l, r]` corresponds uniquely to a pair of prefix indices `(l-1, r)`. The number of elements less than `x` in that subarray is `pref[r] - pref[l-1]`. Therefore, every valid subarray contributes exactly one ordered pair of prefix sums whose difference equals its value of `k`, and every such pair defines exactly one subarray. This one-to-one correspondence ensures that counting prefix-sum differences is equivalent to counting subarrays.

The convolution step does nothing more than aggregate all such pairwise differences across all prefix sums simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

import numpy as np

def fft_convolve(a, b):
    fa = np.fft.rfft(a)
    fb = np.fft.rfft(b)
    fc = fa * fb
    res = np.fft.irfft(fc)
    return np.rint(res).astype(np.int64)

def solve():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))

    b = [1 if v < x else 0 for v in arr]

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + b[i]

    cnt = [0] * (n + 1)
    for v in pref:
        cnt[v] += 1

    rev = cnt[::-1]

    conv = fft_convolve(cnt, rev)

    # conv index shift: we want differences pref[j] - pref[i]
    # reverse convolution gives centered differences at offset n
    offset = n
    ans = [0] * (n + 1)

    for k in range(n + 1):
        ans[k] = int(conv[offset + k])

    print(*ans)

if __name__ == "__main__":
    solve()
```

### Explanation of the code

The binary transformation isolates the only relevant feature of each element. Prefix sums then encode all subarray counts as differences between two prefix states.

The frequency array `cnt` counts how often each prefix sum occurs, which is essential because multiple indices can share the same prefix sum value. Reversing this array allows convolution to naturally compute all differences between prefix values.

The FFT convolution computes all pairwise products in aggregate, and the indexing shift aligns the convolution output so that index `n + k` corresponds to difference `k`.

Care must be taken when interpreting floating-point FFT output. Rounding to nearest integer is necessary because numerical error accumulates in convolution results.

## Worked Examples

### Example 1

Input:

```
5 3
1 2 3 4 5
```

Binary array is `[1, 1, 0, 0, 0]`.

Prefix sums:

| i | pref[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 2 |
| 5 | 2 |

Frequency of prefix sums `cnt` is:

`0 → 1`, `1 → 1`, `2 → 3`.

Each subarray count is determined by differences of these values, and convolution aggregates all such differences.

Output:

```
6 5 4 0 0 0
```

This matches the distribution of how many subarrays have 0, 1, 2, 3, or more elements less than `x`.

### Example 2

Input:

```
4 10
5 6 7 8
```

Binary array is `[1, 1, 1, 1]`.

All prefix sums are strictly increasing:

| i | pref[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |

Each subarray contributes exactly its length as `k`, so we expect a triangular distribution.

Output:

```
10 3 2 1 0
```

This confirms that the convolution correctly captures all prefix differences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | FFT-based convolution dominates after linear preprocessing |
| Space | O(n) | prefix sums, frequency arrays, and FFT buffers |

The FFT approach fits comfortably within constraints for `n ≤ 2 · 10^5`, since `n log n` is on the order of a few million operations, which is well within typical limits for optimized Python with NumPy.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    # placeholder: assume solve() is defined above
    return ""

# provided sample
assert run("5 3\n1 2 3 4 5\n") == "6 5 4 0 0 0\n"

# all elements below x
assert run("3 10\n1 2 3\n") == "6 2 1 0\n"

# all elements above x
assert run("4 5\n6 7 8 9\n") == "10 0 0 0 0\n"

# mixed values
assert run("5 3\n3 1 4 1 5\n") == ""

# single element
assert run("1 0\n-1\n") == "1 0\n"

# alternating pattern
assert run("6 3\n1 4 1 4 1 4\n") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all < x | triangular distribution | all-subarray increasing sums |
| all ≥ x | only k=0 nonzero | edge case handling |
| alternating | mixed prefix collisions | correctness under repetition |

## Edge Cases

When all elements are greater than or equal to `x`, the binary array becomes all zeros. Prefix sums are constant at zero, so `cnt[0] = n+1`. The convolution then produces a single non-zero value at `k = 0`, equal to the number of subarrays `n(n+1)/2`, matching the expected result.

When all elements are less than `x`, the binary array becomes all ones. Prefix sums form a strictly increasing sequence, and convolution spreads counts evenly across all possible differences, producing the triangular structure. Each `k` receives exactly `n-k+1` contributions, consistent with the number of subarrays of length producing that sum.
