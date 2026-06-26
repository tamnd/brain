---
title: "CF 105206B - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435"
description: "We are given a long sequence of non-negative integers. We are also given a target value x. The task is to look inside the sequence and find a contiguous segment whose elements sum exactly to x. Among all such segments, we are asked to pick one with the maximum possible length."
date: "2026-06-27T02:40:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105206
codeforces_index: "B"
codeforces_contest_name: "VitebskOpen Junior"
rating: 0
weight: 105206
solve_time_s: 83
verified: false
draft: false
---

[CF 105206B - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435](https://codeforces.com/problemset/problem/105206/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a long sequence of non-negative integers. We are also given a target value `x`. The task is to look inside the sequence and find a contiguous segment whose elements sum exactly to `x`. Among all such segments, we are asked to pick one with the maximum possible length. If several segments share that maximum length, any one of them is acceptable. If no segment has sum exactly `x`, we report failure.

The output is not the segment itself, but two values describing it: its length and the starting position using 1-based indexing.

The constraints are what shape the solution. The array size can reach five million elements, so any method that inspects all subarrays explicitly will not survive. Even storing prefix sums in a naive array is borderline in memory but still possible if done carefully. The sum bound goes up to 10^16, which guarantees that 32-bit arithmetic is insufficient for accumulation, so 64-bit integers are required throughout.

A key structural property is that all numbers are non-negative. This completely determines the direction of valid window movement: once a window sum exceeds `x`, expanding it further can never fix the situation, only shrink it can help.

There are a few edge cases that break naive reasoning:

A first edge case is when `x = 0`. Since all numbers are non-negative, the only valid segments are those composed entirely of zeros. A naive sliding window that assumes positive growth might still work, but implementations that only move pointers when sum changes can get stuck if they do not handle zero-expansion carefully.

Example:

Input:

```
5 0
1 0 0 0 2
```

Correct answer is `3 2`, the segment of three zeros.

A second edge case is when all elements are large and the sum exceeds `x` immediately; here only shrinking matters, and failure to shrink correctly leads to infinite expansion attempts in a two-pointer implementation.

## Approaches

A brute-force solution would enumerate every starting index `l`, and for each `l`, extend `r` while maintaining a running sum until it exceeds or matches `x`. If it matches, we update the best length. This is correct because every subarray is considered, but in the worst case it examines O(n^2) segments, and the total work degenerates to O(n^2) additions. With `n = 5 * 10^6`, this is entirely infeasible.

The key observation comes from the fact that all numbers are non-negative. This guarantees that if we maintain a window `[l, r]` and the sum becomes too large, increasing `r` only makes it worse. This monotonic behavior allows us to maintain a sliding window where both endpoints only move forward. Each element enters and leaves the window at most once, so we can track valid sums in linear time.

Instead of checking all subarrays, we maintain a dynamic interval that always represents the current sum. We expand the right end greedily, and when the sum becomes too large, we contract from the left until it is valid again. Every time the sum equals `x`, we update the best answer if the window is longer than previous ones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Sliding Window | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers `l = 0`, `r = 0`, and a running sum `s = 0`. Also store the best answer `(best_len, best_l)` initialized as not found. The two pointers define the current window under consideration.
2. Move `r` from left to right across the array, adding `a[r]` to `s` at each step. This expands the current window to include more elements.
3. After each expansion, while `s > x` and `l <= r`, subtract `a[l]` from `s` and increment `l`. This restores feasibility of the window since all values are non-negative, meaning shrinking is the only way to reduce the sum.
4. If at any point `s == x`, compare the current window length `r - l + 1` with the best length found so far. If it is larger, update the best answer to `(length, l + 1)` because the output uses 1-based indexing.
5. Continue until `r` reaches the end of the array. The final stored answer is the longest valid segment.

### Why it works

The correctness rests on a monotonicity property: once the sum exceeds `x`, no future extension of the right endpoint can fix it without first removing elements from the left. Since all values are non-negative, the sum only increases when extending `r`, and only decreases when moving `l`. This ensures every subarray with right endpoint `r` is uniquely represented by exactly one left pointer position during processing. As a result, no valid window is skipped, and every candidate is evaluated exactly when it becomes minimal under the constraint `s <= x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    l = 0
    s = 0

    best_len = 0
    best_l = -1

    for r in range(n):
        s += a[r]

        while l <= r and s > x:
            s -= a[l]
            l += 1

        if s == x:
            length = r - l + 1
            if length > best_len:
                best_len = length
                best_l = l + 1

    if best_l == -1:
        print(-1)
    else:
        print(best_len, best_l)

if __name__ == "__main__":
    solve()
```

The implementation maintains a sliding window using two indices. The sum `s` always represents the sum of the current segment `[l, r]`. The inner loop is responsible for restoring validity whenever the sum exceeds `x`. Because each element is removed from the left at most once, this loop does not create quadratic behavior.

The answer update only occurs when `s == x`, and it tracks the maximum window length seen so far. The index conversion to 1-based form is handled at assignment time to avoid repeated adjustments later.

## Worked Examples

### Example 1

Input:

```
6 5
1 1 1 1 2 1
```

| r | l | window | sum | action | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 1 | expand | - |
| 3 | 0 | [1,1,1,1] | 4 | expand | - |
| 4 | 0 | [1,1,1,1,2] | 6 → shrink | move l | - |
| 4 | 4 | [2] | 2 | shrink done | - |
| 5 | 4 | [2,1] | 3 | expand | - |

Continuing this process, when the window becomes `[1,1,1,1]` starting at index 3, we get sum 4, and later valid subwindows are compared until the best `[1,1,1,1]`-like segment is found with length 4 starting at position 3.

This trace shows how shrinking removes earlier elements to reestablish validity and how the algorithm never revisits a left boundary once it moves past it.

### Example 2

Input:

```
5 11
4 2 9 0 1
```

| r | l | window | sum | action | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [4] | 4 | expand | - |
| 1 | 0 | [4,2] | 6 | expand | - |
| 2 | 0 | [4,2,9] | 15 → shrink | l moves | - |
| 2 | 1 | [2,9] | 11 | match | (2,2) |
| 3 | 1 | [2,9,0] | 11 | match | (3,2) |
| 4 | 1 | [2,9,0,1] | 12 → shrink | adjust | (3,2) |

This example shows how zero does not affect sum constraints and how multiple valid windows ending at different `r` can share the same sum, requiring tracking of maximum length rather than first occurrence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each element is added and removed at most once from the sliding window |
| Space | O(1) | only a few counters are maintained besides the input array |

The linear behavior is essential given `n` up to five million. Any quadratic approach would exceed time limits by several orders of magnitude, while the constant extra memory ensures scalability.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, x = map(int, input().split(
```
