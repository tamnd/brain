---
title: "CF 940A - Points on the line"
description: "We are given several points placed on a number line. Each point is just a single integer coordinate. We want to keep a subset of these points such that the spread of the remaining points is controlled, specifically the difference between the largest and smallest kept point must…"
date: "2026-06-17T02:34:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 940
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 466 (Div. 2)"
rating: 1200
weight: 940
solve_time_s: 181
verified: true
draft: false
---

[CF 940A - Points on the line](https://codeforces.com/problemset/problem/940/A)

**Rating:** 1200  
**Tags:** brute force, greedy, sortings  
**Solve time:** 3m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several points placed on a number line. Each point is just a single integer coordinate. We want to keep a subset of these points such that the spread of the remaining points is controlled, specifically the difference between the largest and smallest kept point must not exceed a given limit `d`.

The task is not to choose the subset directly, but instead to determine the minimum number of points that must be removed so that the remaining points fit inside some interval of length at most `d`.

The key observation is that once we decide the leftmost and rightmost points of the remaining set, everything in between them in sorted order can potentially be kept. This makes the structure inherently one-dimensional and ordering becomes the central tool.

The constraints are small: `n ≤ 100` and coordinates are also bounded by 100. This immediately tells us that even quadratic solutions are acceptable, and sorting followed by scanning is easily fast enough. Anything beyond that, like exponential subsets, is unnecessary but still technically feasible due to small input size.

A subtle edge case occurs when all points already lie within a range ≤ `d`. In this case, no removals are needed. Another edge case is when `d = 0`. Then only identical coordinates can remain together, meaning we are effectively looking for the maximum frequency of a single value. For example, input `3 0` with points `1 2 1` should keep the two `1`s and remove one point.

A naive mistake would be to try removing extreme points greedily without sorting or without considering all valid windows. For example, removing the current min or max iteratively can fail because removing one extreme might make another previously valid window suboptimal.

## Approaches

The brute-force way to think about this problem is to try every possible subset of points and check whether its diameter is at most `d`. For each subset, compute minimum and maximum values and verify the constraint. This is correct because it explores all possibilities, but it is computationally infeasible since there are `2^n` subsets. With `n = 100`, this explodes completely.

The structure of the problem becomes much simpler once we sort the points. After sorting, any valid set of points with diameter ≤ `d` must correspond to a contiguous segment in this sorted array after removing some elements. Instead of choosing arbitrary subsets, we only need to find the largest contiguous block where `a[r] - a[l] ≤ d`. This reduces the problem to finding the longest window satisfying a difference constraint, which is a classic two-pointer pattern.

We slide a left pointer and expand the right pointer as far as possible while maintaining the constraint. Whenever the constraint is violated, we move the left pointer forward. The largest valid window gives the maximum number of points we can keep, and the answer is `n - best_window_size`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(1) | Too slow |
| Sorting + Two Pointers | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the array of point coordinates in non-decreasing order. Sorting is essential because it allows diameter checks to be reduced to simple differences between endpoints of intervals.
2. Initialize two pointers `l = 0` and iterate `r` from left to right. The idea is to treat `r` as the expanding endpoint of a candidate valid segment.
3. For each position `r`, check whether the current segment `[l, r]` satisfies `a[r] - a[l] ≤ d`. This directly represents the diameter of the current subset.
4. If the condition is violated, move `l` forward until the condition becomes valid again. Each increment of `l` removes the smallest element in the current window, which is the only way to reduce the diameter in a sorted array.
5. At each step, compute the size of the valid window `r - l + 1` and track the maximum such size. This represents the largest subset we can keep.
6. After processing all `r`, compute the answer as `n - best_window_size`, since everything not in the optimal window must be removed.

### Why it works

Sorting guarantees that any subset achieving minimum and maximum values corresponds to a contiguous range in sorted order. The two-pointer process maintains a window that always satisfies the diameter constraint. Whenever the constraint is violated, the only way to restore validity is to move the left boundary rightward, because removing internal elements does not affect the maximum-minimum gap unless the extremes change. This ensures that every valid candidate window is considered without missing any optimal configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d = map(int, input().split())
a = list(map(int, input().split()))

a.sort()

l = 0
best = 0

for r in range(n):
    while a[r] - a[l] > d:
        l += 1
    best = max(best, r - l + 1)

print(n - best)
```

The sorting step is what transforms the problem into a sliding window over a monotonic sequence. Without sorting, the diameter condition would not correspond to a simple left-right difference, and the two-pointer method would fail.

The `while` loop ensures the invariant that the current window is always valid before updating the best answer. Importantly, `l` only moves forward, so the total number of pointer movements is linear.

## Worked Examples

### Example 1

Input:

```
3 1
2 1 4
```

Sorted array: `[1, 2, 4]`

| r | l | window | a[r] - a[l] | valid | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 0 | yes | 1 |
| 1 | 0 | [1,2] | 1 | yes | 2 |
| 2 | 1 | [2,4] | 2 | no → adjust l | 2 |

When `r = 2`, the window `[1,2,4]` is invalid because `4 - 1 = 3 > 1`. We move `l` until the window becomes `[2,4]`, which still violates, so we move again to `[4]`.

Final best window size is `2`, so answer is `3 - 2 = 1`.

This shows that the optimal solution does not necessarily include the smallest element; removing it can unlock a valid larger segment.

### Example 2

Input:

```
5 0
1 2 2 3 2
```

Sorted array: `[1, 2, 2, 2, 3]`

| r | l | window | a[r] - a[l] | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 0 | 1 |
| 1 | 1 | [2,2] | 0 | 2 |
| 3 | 1 | [2,2,2] | 0 | 3 |
| 4 | 2 | [2,3] | 1 > 0 → shift l | 3 |

Best window is `3`, so answer is `5 - 3 = 2`.

This confirms the `d = 0` case behaves like selecting the most frequent value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, two-pointer scan is linear |
| Space | O(1) | Only pointers and counters used |

The constraints allow up to 100 elements, so even simpler quadratic approaches would pass. The chosen solution is optimal and generalizes cleanly to larger constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, d = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    l = 0
    best = 0

    for r in range(n):
        while a[r] - a[l] > d:
            l += 1
        best = max(best, r - l + 1)

    return str(n - best)

# provided samples
assert run("3 1\n2 1 4\n") == "1"

# custom cases
assert run("1 0\n5\n") == "0"
assert run("4 0\n1 2 3 4\n") == "3"
assert run("5 2\n1 2 3 4 5\n") == "2"
assert run("6 10\n1 2 3 4 5 6\n") == "0"
assert run("5 1\n1 100 101 102 103\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimum boundary |
| all distinct, d=0 | n-1 | frequency constraint behavior |
| sliding window needed | 2 | general case correctness |
| large enough d | 0 | no removals needed |
| outlier extreme | 4 | effect of distant element |

## Edge Cases

When all points are identical, sorting produces a constant array and the window always satisfies the condition regardless of `d`. The algorithm expands the window to full size and correctly returns zero removals.

When `d = 0`, only equal values can coexist. The sliding window naturally collapses to blocks of identical numbers, and the maximum window corresponds exactly to the maximum frequency of any coordinate.

When one value is far outside the rest, sorting places it at one end. The window will temporarily include it and then shrink as soon as it violates the constraint, ensuring it is excluded unless it can fit within a valid segment.
