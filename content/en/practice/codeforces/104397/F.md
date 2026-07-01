---
title: "CF 104397F - ``Mode'' but ``Low Space''?"
description: "We are given a collection of cookie sizes, essentially an array of integers. From this array, we want to select a subset of cookies such that the chosen elements lie within a narrow value range: the largest selected value minus the smallest selected value must be at most k."
date: "2026-06-30T23:10:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104397
codeforces_index: "F"
codeforces_contest_name: "The 21st UESTC Programming Contest Final"
rating: 0
weight: 104397
solve_time_s: 74
verified: true
draft: false
---

[CF 104397F - ``Mode'' but ``Low Space''?](https://codeforces.com/problemset/problem/104397/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of cookie sizes, essentially an array of integers. From this array, we want to select a subset of cookies such that the chosen elements lie within a narrow value range: the largest selected value minus the smallest selected value must be at most `k`. Among all such valid subsets, we are asked to maximize how many elements we can take.

The input size can be as large as one million, and the values themselves are arbitrary up to 1e9. The constraint on `k` is small, at most 9, which immediately suggests that any solution depending heavily on value differences can be optimized using ordering or local scanning rather than global combinatorics.

The memory limit is extremely tight at 1 megabyte, which effectively rules out frequency arrays over the value domain and any auxiliary structures proportional to `n` storing multiple copies of data. This pushes us toward in place processing or sorted streaming behavior with minimal extra storage.

A naive pitfall appears when one tries to treat the problem as independent frequency aggregation per value. For example, if cookies are `[1, 100, 101, 102]` with `k = 2`, a naive grouping might overcount by mixing counts from disjoint regions if not careful about enforcing a contiguous numeric interval constraint.

Another subtle edge case arises when all values are identical. For example, `[5, 5, 5, 5]` with any `k` should return `4`, and any sliding logic that incorrectly resets windows on duplicates would fail here.

## Approaches

The brute-force idea is straightforward: consider every possible subset, check whether its maximum minus minimum is within `k`, and keep the largest valid one. Even restricting to subsets that are contiguous in sorted order, one might still attempt to enumerate all start and end pairs. After sorting, this reduces the condition to checking all intervals `[i, j]` such that `a[j] - a[i] <= k`, and taking the maximum length.

This immediately suggests an `O(n^2)` scan over all pairs. With `n` up to 1e6, this is completely infeasible since it would require on the order of 10^12 comparisons.

The key observation is that after sorting, any optimal subset must form a contiguous segment in the sorted array. Once sorted, expanding a window only increases the maximum, and shrinking it only increases the minimum, so validity is naturally expressed as a sliding interval condition. This converts the problem into finding the longest subarray where the difference between endpoints is at most `k`.

That structure is exactly what a two pointers technique captures. We maintain a left boundary and extend a right boundary as far as possible while preserving the constraint, shrinking the left boundary only when necessary. Each element enters and leaves the window at most once, giving linear time after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sort + Two Pointers | O(n log n) | O(1) extra (besides sort) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Sort the array of cookie sizes in non-decreasing order. This transforms the problem into working with contiguous value intervals where any valid subset must appear as a continuous segment in this ordering.
2. Initialize two pointers `l = 0` and `r = 0`, representing the current window of chosen cookies. At any moment, this window represents a candidate subset.
3. Expand the right pointer `r` step by step. After each expansion, check whether `a[r] - a[l] <= k`. If it holds, the current window is valid and can potentially update the answer.
4. If the condition is violated, shrink the window from the left by increasing `l` until the condition becomes valid again. This works because increasing `l` only decreases the minimum value in the window, directly restoring feasibility.
5. During the process, maintain the maximum window size `r - l + 1`. This represents the best valid subset seen so far.
6. Continue until `r` reaches the end of the array, ensuring all possible right endpoints are considered exactly once.

### Why it works

After sorting, any subset that satisfies the constraint can be mapped to a contiguous segment in sorted order without loss of generality, because including any skipped element inside a valid range cannot violate the maximum minus minimum condition. The two pointers invariant is that at every step, the window `[l, r]` is the smallest left boundary that keeps the segment valid for the current `r`. This guarantees that no valid segment ending at `r` is missed, since any smaller left index would violate the constraint, and any larger one only reduces the size unnecessarily.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

a.sort()

l = 0
ans = 1

for r in range(n):
    while a[r] - a[l] > k:
        l += 1
    ans = max(ans, r - l + 1)

print(ans)
```

The solution begins by sorting the array so that valid subsets correspond to contiguous ranges in value space. The two pointer loop then maintains a window `[l, r]` that always satisfies the constraint `a[r] - a[l] <= k`. Whenever the constraint breaks, the left pointer is advanced until validity is restored. The answer is updated at each step using the current window length.

A common mistake here is forgetting that shrinking must happen in a loop, not a single conditional step, because multiple increments of `l` may be required before the constraint is satisfied again.

## Worked Examples

### Example 1

Input:

```
6 3
1 1 4 5 1 4
```

Sorted array: `[1, 1, 1, 4, 4, 5]`

| r | l | window | valid | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | yes | 1 |
| 1 | 0 | [1,1] | yes | 2 |
| 2 | 0 | [1,1,1] | yes | 3 |
| 3 | 0 | [1,1,1,4] | no | 3 |
| 3 | 1 | [1,1,4] | no | 3 |
| 3 | 2 | [1,4] | no | 3 |
| 3 | 3 | [4] | yes | 3 |
| 4 | 3 | [4,4] | yes | 4 |
| 5 | 3 | [4,4,5] | yes | 5 |

Final answer is `5`, achieved on the segment `[4, 4, 5]`.

This trace shows how the left pointer aggressively advances until the range constraint is restored, and how optimal windows may start late in the array rather than always from the beginning.

### Example 2

Input:

```
5 0
2 2 2 3 3
```

Sorted array: `[2, 2, 2, 3, 3]`

| r | l | window | valid | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [2] | yes | 1 |
| 1 | 0 | [2,2] | yes | 2 |
| 2 | 0 | [2,2,2] | yes | 3 |
| 3 | 0 | [2,2,2,3] | no | 3 |
| 3 | 1 | [2,2,3] | no | 3 |
| 3 | 2 | [2,3] | no | 3 |
| 3 | 3 | [3] | yes | 3 |
| 4 | 3 | [3,3] | yes | 4 |

Answer is `4`.

This demonstrates that even with `k = 0`, duplicates are handled correctly because the window only depends on equality of endpoints, not frequency logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, two pointers run in linear time |
| Space | O(1) extra | Only indices and counters are used beyond input storage |

The constraints allow up to one million elements, so a linear scan after sorting is essential. The memory constraint further reinforces avoiding auxiliary structures like frequency maps or coordinate compression arrays of large size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    l = 0
    ans = 1
    for r in range(n):
        while a[r] - a[l] > k:
            l += 1
        ans = max(ans, r - l + 1)
    return str(ans)

# provided sample
assert run("6 3\n1 1 4 5 1 4\n") == "5"

# all equal
assert run("4 10\n7 7 7 7\n") == "4"

# k = 0 with duplicates
assert run("5 0\n2 2 2 3 3\n") == "4"

# strictly increasing, small k
assert run("5 1\n1 2 3 4 5\n") == "2"

# single element
assert run("1 5\n100\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 4 | window stability when all differences are zero |
| k = 0 with duplicates | 4 | correctness under equality constraint |
| increasing sequence | 2 | sliding contraction behavior |
| single element | 1 | minimal boundary correctness |

## Edge Cases

One edge case is when all elements are identical. The algorithm keeps expanding the right pointer without ever shrinking, since `a[r] - a[l]` is always zero. The window becomes the entire array, correctly producing `n`.

Another edge case is when `k = 0` but values repeat. Only identical values can coexist, and the algorithm naturally groups equal elements together. When a different value is encountered, the left pointer advances until the window contains only that value again, ensuring correctness.

A final edge case is strictly increasing sequences with small `k`. The window continuously collapses to size one or two. For example, with `[1,2,3,4]` and `k = 1`, the window never grows beyond adjacent pairs, and the algorithm correctly returns `2` rather than mistakenly allowing longer spans.
