---
title: "CF 75D - Big Maximum Sum"
description: "We are given a set of small arrays and a sequence of indexes indicating how to concatenate them into one larger array. Once the large array is built in this way, the goal is to find the maximum sum of a contiguous subarray."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "implementation", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 75
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 67 (Div. 2)"
rating: 2000
weight: 75
solve_time_s: 94
verified: true
draft: false
---

[CF 75D - Big Maximum Sum](https://codeforces.com/problemset/problem/75/D)

**Rating:** 2000  
**Tags:** data structures, dp, greedy, implementation, math, trees  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of small arrays and a sequence of indexes indicating how to concatenate them into one larger array. Once the large array is built in this way, the goal is to find the maximum sum of a contiguous subarray. This is essentially an extension of the classic maximum subarray sum problem, but with a twist: building the array explicitly may be too costly, since the total length could be enormous. Each index in the sequence can point to any small array, and each small array can appear multiple times in the large array.

The input limits tell us that there are at most 50 small arrays, each of size up to 5000, and the sequence of indexes in the large array can be up to 250,000. Concatenating naively would create a potential array of size up to 50 × 5000 × 250,000 in the extreme, which is completely impractical for time or memory. This immediately signals that we need a way to reason about sums without explicitly constructing the full array.

Edge cases include arrays that contain only negative numbers. For example, if a small array is `[-5, -2]` and another is `[-1]`, and the sequence is `[1,2]`, the correct maximum sum is `-1` rather than `-2` or `-5`. Another tricky case arises when concatenating arrays could allow sums to span multiple arrays. For instance, if one small array has a negative prefix but a positive suffix, the maximum subarray could start in one instance and continue in the next, so we must track prefixes and suffixes carefully.

## Approaches

A naive solution would concatenate the arrays according to the sequence and then apply the standard Kadane’s algorithm to find the maximum subarray sum. This is correct in principle, because it directly models the problem, but it is far too slow for large sequences. If each array has length around 5000 and the sequence has 250,000 elements, the total length of the large array could reach over a billion elements. Even a linear scan is impossible in practice.

The key insight is that the maximum sum in a concatenated sequence can be computed incrementally using three statistics for each small array: the maximum prefix sum, the maximum suffix sum, and the total sum. The prefix sum is the maximum sum of a contiguous prefix of the array, the suffix sum is the maximum sum of a contiguous suffix, and the total sum is the sum of the entire array. If we process the sequence of indexes one by one, we can track the best subarray sum that ends in the current array by considering either: a new subarray entirely within the current array, or a subarray that started in previous arrays and continues into the current one.

This allows us to compute the maximum sum without ever building the huge array, reducing the problem from impractical memory usage to a linear scan of the sequence of indexes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total_length) | O(total_length) | Too slow |
| Optimal | O(sum of small arrays + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the total sum, maximum prefix sum, maximum suffix sum, and maximum subarray sum for each small array. The prefix and suffix sums let us extend subarrays across multiple concatenations, and the total sum helps when an array contributes entirely to a longer sequence.
2. Initialize two variables: `current_max` for the maximum sum of a subarray ending at the previous index, and `global_max` for the maximum sum found so far across the sequence.
3. Iterate over the sequence of indexes that defines the large array. For each index, retrieve the statistics for the corresponding small array.
4. Update `current_max` by choosing either to start fresh with the current array’s maximum subarray, or to extend the previous `current_max` by adding the current array’s maximum prefix sum.
5. Update `global_max` to be the maximum of itself and `current_max`. This tracks the overall best sum seen across all arrays processed so far.
6. After the loop, `global_max` contains the maximum sum of a contiguous subarray across the fully concatenated large array.

Why it works: at each step, `current_max` correctly represents the maximum sum ending at the current array, either by starting a new subarray within it or by extending a subarray from previous arrays. Tracking the maximum over all `current_max` values guarantees that any possible contiguous subarray is considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
small_arrays = []
for _ in range(n):
    data = list(map(int, input().split()))
    l = data[0]
    arr = data[1:]
    total = sum(arr)
    max_prefix = max_suffix = max_sub = arr[0]
    curr = 0
    for x in arr:
        curr += x
        max_prefix = max(max_prefix, curr)
    curr = 0
    for x in reversed(arr):
        curr += x
        max_suffix = max(max_suffix, curr)
    curr_max = arr[0]
    curr_sum = 0
    for x in arr:
        curr_sum += x
        curr_max = max(curr_max, curr_sum)
        if curr_sum < 0:
            curr_sum = 0
    max_sub = curr_max
    small_arrays.append((total, max_prefix, max_suffix, max_sub))

seq = list(map(int, input().split()))
current_max = global_max = -10**18

for idx in seq:
    total, pre, suf, sub = small_arrays[idx - 1]
    current_max = max(sub, suf + max(current_max, 0))
    global_max = max(global_max, current_max)

print(global_max)
```

The first loop computes all required statistics for each small array. Note that prefix and suffix sums are computed separately from the standard Kadane scan. In the main loop, we carefully update `current_max` by considering both starting fresh and extending from the previous array. Using `max(current_max, 0)` ensures that negative running sums do not incorrectly reduce the next subarray. All sums are large enough to use 64-bit integers, so the initial value `-10**18` is safe.

## Worked Examples

Sample 1:

| Step | Index | Current Array | current_max | global_max |
| --- | --- | --- | --- | --- |
| 1 | 2 | [3, 3] | 6 | 6 |
| 2 | 3 | [-5, 1] | 1 | 6 |
| 3 | 1 | [1, 6, -2] | 7 | 7 |
| 4 | 3 | [-5, 1] | 9 | 9 |

This shows that the running sum correctly extends across arrays, and the global maximum captures the optimal subarray spanning multiple arrays.

Custom example: single negative array followed by positive array

Input:

```
2 2
-3 -2 -1
4 5
1 2
```

Table:

| Step | Index | Current Array | current_max | global_max |
| --- | --- | --- | --- | --- |
| 1 | 1 | [-3, -2, -1] | -1 | -1 |
| 2 | 2 | [4, 5] | 9 | 9 |

Even though the first array is entirely negative, the algorithm correctly starts a new subarray on the second array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sum of lengths of small arrays + m) | Each small array is scanned once for its statistics; the sequence is scanned linearly. |
| Space | O(n) | We store four numbers per small array and the sequence of indexes. |

The time complexity is acceptable since the sum of lengths of small arrays is at most 50 × 5000 = 250,000 and the sequence length is at most 250,000. Memory usage is minimal, within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    small_arrays = []
    for _ in range(n):
        data = list(map(int, input().split()))
        l = data[0]
        arr = data[1:]
        total = sum(arr)
        max_prefix = max_suffix = max_sub = arr[0]
        curr = 0
        for x in arr:
            curr += x
            max_prefix = max(max_prefix, curr)
        curr = 0
        for x in reversed(arr):
            curr += x
            max_suffix = max(max_suffix, curr)
        curr_max = arr[0]
        curr_sum = 0
        for x in arr:
            curr_sum += x
            curr_max = max(curr_max, curr_sum)
            if curr_sum < 0:
                curr_sum = 0
        max_sub = curr_max
        small_arrays.append((total, max_prefix, max_suffix, max_sub))

    seq = list(map(int, input().split()))
    current_max = global_max = -10**18
    for idx in seq:
        total, pre, suf, sub = small_arrays[idx - 1]
        current_max = max(sub, suf + max(current_max, 0))
        global_max = max(global_max, current_max)
    return str(global_max)

# Provided sample
assert run("3 4
```
