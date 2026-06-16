---
title: "CF 1003C - Intense Heat"
description: "We are given a sequence of daily temperatures and asked to evaluate all contiguous time intervals whose length is at least a given threshold. For each such interval, we compute its average temperature, meaning the sum of its values divided by its length."
date: "2026-06-16T23:30:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1003
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 494 (Div. 3)"
rating: 1300
weight: 1003
solve_time_s: 90
verified: false
draft: false
---

[CF 1003C - Intense Heat](https://codeforces.com/problemset/problem/1003/C)

**Rating:** 1300  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of daily temperatures and asked to evaluate all contiguous time intervals whose length is at least a given threshold. For each such interval, we compute its average temperature, meaning the sum of its values divided by its length. The task is to find the maximum possible average over all valid intervals.

So the object we are optimizing over is not a fixed window size, but every segment whose length starts from a minimum value and can extend up to the full array. This immediately makes the problem more subtle than fixed-window maximum average, because longer segments can trade a lower sum density for a longer span.

The input size constraint allows up to 5000 days. A naive cubic approach over all subarrays and recomputing sums would already be borderline. Even a double loop with recomputed sums would be too slow unless optimized with prefix sums. However, even with prefix sums, enumerating all O(n²) segments is still feasible at n = 5000, since about 25 million operations is acceptable in Python.

The hidden difficulty is that we are optimizing a ratio, not a linear function. This means the best segment is not necessarily one of the shortest or longest allowed segments, and there is no monotonic structure in segment length.

A few edge cases expose incorrect greedy ideas.

If all temperatures are equal, every segment has the same average, so any valid segment is optimal. A correct solution must not depend on picking a specific length.

If the array is strictly increasing, the best average might come from a short suffix segment rather than a long prefix, because including earlier low values drags the average down.

If k equals n, the answer is simply the average of the whole array. Any solution that assumes flexibility in choosing segment length must still handle this boundary cleanly.

## Approaches

The brute-force idea is straightforward. We consider every starting index, then extend the ending index, and only evaluate segments of length at least k. For each candidate segment, we compute its sum and divide by its length, tracking the maximum value.

With prefix sums, we can compute any segment sum in O(1). This reduces the total complexity to O(n²), since there are about n²/2 segments. At n = 5000, this is around 12.5 million evaluations, each consisting of a few arithmetic operations, which is acceptable.

The key observation is that while we cannot avoid checking many segments, we can avoid recomputing sums repeatedly. The ratio structure does not allow a faster pruning or binary search trick because the objective is not monotonic in segment length or endpoints.

Thus the optimal solution is essentially the brute-force idea made efficient with prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Prefix sums over all segments | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array where prefix[i] stores the sum of the first i elements. This allows any segment sum to be computed in constant time.
2. Iterate over all possible left endpoints l from 1 to n. Each choice fixes the start of a candidate segment.
3. For each l, iterate over all right endpoints r from l + k - 1 to n. This guarantees every segment has length at least k.
4. For each pair (l, r), compute the segment sum using prefix[r] − prefix[l − 1].
5. Compute the average by dividing the sum by (r − l + 1).
6. Track the maximum average seen across all valid segments.

The reason we start r from l + k − 1 is that shorter segments are disallowed and would only introduce invalid candidates without contributing to the answer.

### Why it works

Every valid segment is uniquely represented by a pair of endpoints (l, r) with r − l + 1 ≥ k. The algorithm enumerates all such pairs exactly once. Since the average is computed exactly for each segment, and the maximum is taken over a complete set of candidates, the result must match the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    best = 0.0

    for l in range(n):
        for r in range(l + k - 1, n):
            total = pref[r + 1] - pref[l]
            length = r - l + 1
            avg = total / length
            if avg > best:
                best = avg

    print(best)

if __name__ == "__main__":
    solve()
```

The prefix sum array is constructed so that each range sum query becomes a single subtraction. This is critical, because without it the inner loop would become O(n³). The nested loops then enumerate all valid segments while respecting the minimum length constraint directly in the index range.

The floating-point division is safe because the required precision is 1e-6, and Python’s double precision is sufficient for sums up to roughly 5000 × 5000.

## Worked Examples

### Example 1

Input:

```
4 3
3 4 1 2
```

We compute prefix sums:

| i | pref[i] |
| --- | --- |
| 0 | 0 |
| 1 | 3 |
| 2 | 7 |
| 3 | 8 |
| 4 | 10 |

Now we enumerate segments of length at least 3.

| l | r | sum | length | average |
| --- | --- | --- | --- | --- |
| 0 | 2 | 8 | 3 | 2.6667 |
| 0 | 3 | 10 | 4 | 2.5 |
| 1 | 3 | 7 | 3 | 2.3333 |

The maximum is 8/3 = 2.6667, achieved by the first three elements.

This confirms that the optimal segment is not necessarily the longest allowed one.

### Example 2

Input:

```
5 2
1 100 1 1 100
```

Prefix sums:

| i | pref[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 101 |
| 3 | 102 |
| 4 | 103 |
| 5 | 203 |

Consider key segments:

| l | r | sum | length | average |
| --- | --- | --- | --- | --- |
| 0 | 1 | 101 | 2 | 50.5 |
| 3 | 4 | 101 | 2 | 50.5 |
| 1 | 4 | 202 | 4 | 50.5 |

All optimal candidates tie at 50.5.

This shows that multiple segment lengths can produce identical optimal averages, so the algorithm must not assume uniqueness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Two nested loops over all valid segment endpoints |
| Space | O(n) | Prefix sum array |

With n up to 5000, the algorithm performs about 12.5 million iterations, which fits comfortably within time limits in Python when operations are simple arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    best = 0.0
    for l in range(n):
        for r in range(l + k - 1, n):
            total = pref[r + 1] - pref[l]
            best = max(best, total / (r - l + 1))

    return str(best)

assert run("4 3\n3 4 1 2\n")[:5] == "2.666", "sample 1"
assert run("3 3\n1 2 3\n") == "2.0", "whole array only"

assert run("5 1\n5 5 5 5 5\n") == "5.0", "all equal"

assert run("5 2\n1 100 1 1 100\n")[:4] == "50.5", "multiple peaks"

assert run("1 1\n7\n") == "7.0", "single element"

assert run("6 3\n1 2 3 4 5 6\n")[:4] == "4.5", "increasing array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 7 | minimal boundary |
| all equal | 5 | uniform stability |
| multiple peaks | 50.5 | non-unique optimum |
| increasing array | 4.5 | long vs short segment tradeoff |

## Edge Cases

When n equals k, the loop structure still works because for each l there is exactly one valid r. The algorithm effectively computes the average of the entire array in that case.

For a strictly increasing sequence like [1, 2, 3, 4, 5], the best segment of length at least k = 2 is not necessarily the full array. The enumeration checks segments like [4, 5] whose average is 4.5, which beats longer segments such as [1, 2, 3, 4, 5] with average 3. This confirms that restricting attention to full-range segments would be incorrect, and the exhaustive enumeration is necessary.
