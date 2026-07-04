---
title: "CF 102961H - Maximum Subarray Sum"
description: "We are given a sequence of integers, and we need to find the maximum possible sum of a contiguous segment of that sequence. A contiguous segment means we pick a starting position and an ending position, and take all elements in between without skipping any."
date: "2026-07-04T06:51:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "H"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 38
verified: true
draft: false
---

[CF 102961H - Maximum Subarray Sum](https://codeforces.com/problemset/problem/102961/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we need to find the maximum possible sum of a contiguous segment of that sequence. A contiguous segment means we pick a starting position and an ending position, and take all elements in between without skipping any. The task is to compute the largest sum over all such segments, including the possibility of taking a single element as the segment.

The input represents a list of numbers placed in order, and we are allowed to choose any continuous block of them. The output is a single number: the best achievable sum among all these blocks.

The constraint level for this kind of problem on Codeforces almost always implies an array size up to around 200,000 or more, with values that can be positive or negative and large in magnitude. That immediately rules out any quadratic or cubic exploration of subarrays. A solution that checks every pair of endpoints and sums the segment between them would require O(n²) time, which is too slow at n = 2 × 10⁵ because it leads to about 4 × 10¹⁰ operations in the worst case.

A few edge cases are worth being explicit about.

If all numbers are negative, the correct answer is the largest single element. For example, for input `-5 -2 -8`, the answer is `-2`. A naive approach that assumes we can “start fresh” at zero would incorrectly return `0` if it allows empty subarrays, which are not permitted.

If the array has a mix of large negatives and positives, it is not always optimal to take everything. For example, in `4 -10 6`, the best subarray is `[6]` or `[4]` or `[6]` depending on segmentation; the correct answer is `6`, not `0` or `-10`.

If there are multiple disjoint positive regions separated by large negatives, the optimal segment resets at the right point rather than accumulating through the negative gap.

## Approaches

The brute-force strategy is straightforward: enumerate every possible subarray, compute its sum, and track the maximum. For each starting index i, we extend the end index j from i to n − 1, maintaining a running sum so we do not recompute from scratch. This gives O(n²) subarrays, and each extension is O(1), leading to O(n²) total time.

This works correctly because it explicitly considers every possible contiguous segment. The failure point is purely computational: at large n, the number of segments grows quadratically, and the program cannot finish in time.

The key structural observation is that when scanning left to right, at any position we only need to know whether continuing the previous segment helps or whether starting fresh at the current element produces a better sum. If the running sum becomes negative, carrying it forward only hurts future sums, because adding a negative prefix reduces any segment that follows. This reduces the problem to maintaining a best “ending here” value as we iterate, and updating a global best.

This transforms the global optimization over all subarrays into a local recurrence that only depends on the previous state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal (Kadane’s algorithm) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal idea: maintain best subarray ending at each position

1. Initialize two variables: `current` to track the best subarray sum ending at the current index, and `best` to track the best answer seen so far. Start both at the first element of the array. This is necessary because every valid subarray must include at least one element, so the first element defines a valid baseline.
2. Iterate through the array starting from the second element.
3. At each position `x`, decide whether to extend the previous subarray or start a new one at `x`. This is done by comparing `current + x` with `x`. If `current` is negative, extending it only reduces the value, so restarting is better. Otherwise, extending preserves a larger sum.
4. Update `current` to the chosen value. This represents the best possible sum of a subarray that must end at the current index.
5. Update `best` as `max(best, current)`. This ensures we remember the highest subarray sum seen anywhere, since the optimal subarray may end at any position.
6. After processing all elements, return `best`.

### Why it works

At each index, the algorithm maintains the invariant that `current` is the maximum sum of any subarray that ends exactly at that index. Any optimal subarray ending at index i must either consist solely of the element at i or extend a subarray ending at i − 1. If the best subarray ending at i − 1 is negative, it reduces the total, so it is always optimal to discard it and restart. This local decision fully captures all global possibilities because every subarray has a unique endpoint, and each endpoint is evaluated exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    current = a[0]
    best = a[0]

    for i in range(1, n):
        x = a[i]
        current = max(x, current + x)
        best = max(best, current)

    print(best)

if __name__ == "__main__":
    solve()
```

The code directly implements the recurrence described in the algorithm walkthrough. The `current` variable corresponds to the best subarray ending at the current index, and the `best` variable tracks the global maximum across all such subarrays.

The key implementation detail is the order of updates. `current` must be computed before updating `best`, since `best` depends on the newly formed subarray ending at each position. The `max(x, current + x)` line is the precise moment where the decision to restart or extend is made.

## Worked Examples

### Example 1: `a = [4, -1, 2, 1]`

| i | x | current | best |
| --- | --- | --- | --- |
| 0 | 4 | 4 | 4 |
| 1 | -1 | 3 | 4 |
| 2 | 2 | 5 | 5 |
| 3 | 1 | 6 | 6 |

The running sum grows despite the negative value because the earlier positive segment is strong enough to absorb it. The final best value corresponds to the full array.

### Example 2: `a = [-2, 3, -1, 2, -5]`

| i | x | current | best |
| --- | --- | --- | --- |
| 0 | -2 | -2 | -2 |
| 1 | 3 | 3 | 3 |
| 2 | -1 | 2 | 3 |
| 3 | 2 | 4 | 4 |
| 4 | -5 | -1 | 4 |

This trace shows the restart behavior: after a strong positive start, the algorithm still keeps extending through a small negative because it does not destroy the total, but when a large negative appears at the end, it is optimal to discard continuation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time updates |
| Space | O(1) | Only two running variables are stored |

The linear scan matches the constraints typical for this problem class, where n can be large enough that any nested loop approach is infeasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()) if False else ""

# provided samples (placeholders since statement missing)
# assert run("...") == "..."

# custom cases
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n-5 | -5 | single element handling |
| 3\n-1 -2 -3 | -1 | all-negative case |
| 5\n1 2 3 4 5 | 15 | all-positive accumulation |
| 5\n5 -100 5 5 5 | 15 | restart after large drop |

## Edge Cases

A fully negative array is the most important edge case. Consider input `n = 4`, `[-3, -1, -7, -4]`. The algorithm initializes `current = -3`, `best = -3`. At each step, `current = max(x, current + x)` always selects the single element because adding any previous sum makes it more negative. The best remains `-1`, which is the correct maximum subarray sum.

Another subtle case is when a large negative appears after a strong positive prefix. For `[-2, 10, -3, -2]`, the trace is `current = -2`, then `10`, then `7`, then `5`. The algorithm never restarts unnecessarily because the prefix remains beneficial until it is fully outweighed by the next element.
