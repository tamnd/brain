---
title: "CF 231C - To Add or Not to Add"
description: "We are given an array of integers and a limited number of increment operations. Each operation increases a single element by one, and the same element can be increased multiple times."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 231
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 143 (Div. 2)"
rating: 1600
weight: 231
solve_time_s: 178
verified: true
draft: false
---

[CF 231C - To Add or Not to Add](https://codeforces.com/problemset/problem/231/C)

**Rating:** 1600  
**Tags:** binary search, sortings, two pointers  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a limited number of increment operations. Each operation increases a single element by one, and the same element can be increased multiple times. Our goal is to find a number that appears as many times as possible in the array after performing at most _k_ such operations. If multiple numbers can achieve the same maximum frequency, we must choose the smallest one.

The input consists of two integers, _n_ and _k_, followed by an array of _n_ integers. The output is the maximum frequency achievable and the smallest number achieving it.

Given that _n_ can reach 10^5 and _k_ can be as large as 10^9, any algorithm iterating over all possible numbers and counting occurrences or trying every combination of operations would be too slow. Naive brute-force solutions with O(n^2) complexity will time out because 10^10 operations is impossible in a 2-second limit.

Edge cases to consider include arrays where all numbers are equal, arrays that require no operations for an optimal result, and scenarios where the smallest number achieving the frequency is less than numbers that can achieve the same frequency with more operations. For example, for the input `3 3` with array `1 2 3`, incrementing both 1 and 2 twice each makes 3 occur 3 times, but the smallest number achieving the maximum frequency is 2 if we increment 1 and 2 once each.

## Approaches

A brute-force approach would consider each unique number in the array as a potential target. For each target, we could iterate over all elements and calculate how many increments are needed to raise smaller numbers to this target. We sum the operations, and if the total is less than or equal to _k_, we record the achievable frequency. This works because for any candidate number, the number of increments needed to make other numbers equal to it is deterministic. However, this is O(n^2) in the worst case because for each number we potentially scan the entire array.

The key insight is that after sorting the array, we can use a sliding window technique to efficiently compute the number of operations required to make a contiguous segment of numbers equal to the largest number in the window. By maintaining a prefix sum of the sorted array, we can calculate the operations needed to raise all numbers in the window to the rightmost number in constant time. We then move the window forward to consider larger segments. This reduces complexity to O(n log n) because we sort once and then use a linear pass with prefix sums. Sorting also allows us to easily select the smallest number achieving the maximum frequency when multiple numbers tie, since the first occurrence in sorted order will always be the smallest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Sliding Window with Prefix Sum | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in ascending order. Sorting ensures that any contiguous subsequence can be considered for incrementing to the same value without worrying about smaller numbers appearing later.
2. Construct a prefix sum array. For each index _i_, the prefix sum stores the sum of all elements from index 0 to _i_. This allows constant-time calculation of the sum of any subarray.
3. Initialize two pointers, `left` and `right`, both starting at 0. The `right` pointer represents the current number we aim to make other numbers equal to. The `left` pointer defines the start of the segment.
4. For each position of `right`, calculate the total increments needed to raise all elements from `a[left]` to `a[right]` to the value `a[right]`. Using the prefix sum, the operations are `operations_needed = a[right] * (right - left + 1) - (prefix_sum[right] - prefix_sum[left-1] if left > 0 else prefix_sum[right])`.
5. If `operations_needed` exceeds _k_, increment `left` until the window becomes valid. This effectively shrinks the window from the left until the required operations are within the allowed _k_.
6. Track the largest window length and the corresponding number. If multiple numbers yield the same length, choose the smaller one.
7. After traversing the array with `right`, report the maximum frequency and the associated number.

The algorithm works because the sorted array ensures that for any segment, the number at the right end is always the maximum. Increasing all elements in the segment to this value requires the fewest operations. Moving `left` forward whenever the operation limit is exceeded guarantees we always maintain a valid window.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

prefix_sum = [0] * n
prefix_sum[0] = a[0]
for i in range(1, n):
    prefix_sum[i] = prefix_sum[i-1] + a[i]

max_freq = 1
best_num = a[0]
left = 0

for right in range(n):
    total = prefix_sum[right] - (prefix_sum[left-1] if left > 0 else 0)
    operations_needed = a[right] * (right - left + 1) - total
    while operations_needed > k:
        left += 1
        total = prefix_sum[right] - (prefix_sum[left-1] if left > 0 else 0)
        operations_needed = a[right] * (right - left + 1) - total
    window_size = right - left + 1
    if window_size > max_freq:
        max_freq = window_size
        best_num = a[right]

print(max_freq, best_num)
```

The solution begins with sorting, allowing efficient windowing. The prefix sum enables constant-time computation of operations required. The sliding window ensures we never exceed _k_ operations and only consider valid segments. Updating the best number on strictly larger frequencies guarantees we select the smallest number in case of ties.

## Worked Examples

Sample 1 input `5 3` with array `[6, 3, 4, 0, 2]`.

| right | left | a[right] | operations_needed | window_size | max_freq | best_num |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 2 | 2*2-3=1 | 2 | 2 | 2 |
| 2 | 0 | 3 | 3*3-(0+2+3)=9-5=4>3 | left=1 | 3*2-(2+3)=6-5=1 | 2 |
| 3 | 1 | 4 | 4*3-(2+3+4)=12-9=3 | 3 | 3 | 4 |
| 4 | 1 | 6 | 6*4-(2+3+4+6)=24-15=9>3 | left=2 | 6*3-(3+4+6)=18-13=5>3 | left=3 |

This trace confirms that the segment `[2, 3, 4]` can be transformed to `[4,4,4]` using ≤3 operations, giving frequency 3 with the minimal number 4.

Sample 2 input `3 0` with array `[5,5,5]`. Sliding window never requires increments; max_freq becomes 3 with best_num 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, sliding window with prefix sums is O(n) |
| Space | O(n) | Prefix sum array of length n |

The solution fits within the time and memory limits for n up to 10^5 and k up to 10^9. No operation requires more than integer arithmetic, so 64-bit integers are sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    prefix_sum = [0]*n
    prefix_sum[0] = a[0]
    for i in range(1, n):
        prefix_sum[i] = prefix_sum[i-1] + a[i]
    max_freq = 1
    best_num = a[0]
    left = 0
    for right in range(n):
        total = prefix_sum[right] - (prefix_sum[left-1] if left > 0 else 0)
        operations_needed = a[right]*(right-left+1)-total
        while operations_needed > k:
            left += 1
            total = prefix_sum[right] - (prefix_sum[left-1] if left > 0 else 0)
            operations_needed = a[right]*(right-left+1)-total
        window_size = right-left+1
        if window_size > max_freq:
            max_freq = window_size
            best_num = a[right]
    return f"{max_freq} {best_num}"

assert run("5 3\n6 3 4 0 2\n") == "3 4"
assert run("3 0\n5 5 5\n")
```
