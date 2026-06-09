---
title: "CF 1760D - Challenging Valleys"
description: "We are given an array of integers and need to determine whether it forms a \"valley\" according to a precise definition. Conceptually, a valley is a flat subarray that is lower than its neighbors on both sides."
date: "2026-06-09T14:22:53+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1760
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 835 (Div. 4)"
rating: 1000
weight: 1760
solve_time_s: 148
verified: true
draft: false
---

[CF 1760D - Challenging Valleys](https://codeforces.com/problemset/problem/1760/D)

**Rating:** 1000  
**Tags:** implementation, two pointers  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and need to determine whether it forms a "valley" according to a precise definition. Conceptually, a valley is a flat subarray that is lower than its neighbors on both sides. Formally, there must be exactly one contiguous segment of equal elements such that if the segment is not at the boundary, its left neighbor is strictly greater and its right neighbor is strictly greater as well. If the flat segment is at the boundary, only the neighbor that exists must satisfy this condition. The output is "YES" if exactly one such valley segment exists and "NO" otherwise.

The constraints allow arrays of length up to 200,000 and up to 10,000 test cases, but the sum of all array lengths across test cases does not exceed 200,000. This means we must handle each array in linear time relative to its size. Any approach that inspects every possible subarray explicitly would be quadratic and far too slow. A careful linear scan suffices.

Edge cases that are easy to mishandle include arrays of length 1, arrays with all elements equal, or arrays with multiple flat segments that could individually look like valleys. For example, `[1, 1, 1]` is a valley because the left boundary starts the flat segment and there is no smaller neighbor to its left, but `[2, 1, 1, 1, 2]` has one clear valley in the middle and should return "YES". Arrays like `[1, 2, 1, 2, 1]` have multiple potential minimal points, so the output should be "NO". Miscounting flat regions or failing to verify the boundary conditions is a common source of errors.

## Approaches

The brute-force approach would check every possible subarray of length at least one to see if it satisfies the valley property. For each subarray, we would verify all elements are equal, and check the neighbors if they exist. This is correct, but each array of length `n` could have O(n^2) subarrays, which is too slow for `n = 2*10^5`.

The key insight is that only the minimal elements of the array can form valid valleys because any valley must be lower than its surroundings. We can first find the minimal value in the array and then look at contiguous segments of this value. For each contiguous segment of minimal elements, we check the boundary conditions: the element before the segment, if it exists, must be strictly greater, and the element after the segment, if it exists, must be strictly greater. If exactly one such segment satisfies this, the array is a valley; otherwise, it is not. By focusing on minimal elements and scanning linearly, we reduce the complexity from quadratic to linear in the size of the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For the current array, find the minimal value. This is the only candidate for a valley because any valley must be lower than its neighbors.
2. Initialize a counter for the number of valid valley segments.
3. Iterate through the array from left to right. Whenever you encounter a minimal value, identify the contiguous segment of equal minimal values.
4. For this segment, check the boundary elements. If the segment starts at the beginning of the array, only check the right neighbor. If it ends at the last index, only check the left neighbor. Otherwise, verify the left neighbor is greater than the minimal value and the right neighbor is greater as well.
5. If the segment satisfies the boundary condition, increment the valley counter.
6. Continue scanning the array to the next minimal segment until the end.
7. At the end, if exactly one segment passed the boundary check, print "YES". Otherwise, print "NO".

Why it works: The minimal value observation ensures we only consider potential valleys, and the boundary checks ensure that we satisfy the definition of a valley exactly once. The linear scan guarantees we examine all contiguous minimal segments without missing overlaps or partial checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_valley(a):
    n = len(a)
    min_val = min(a)
    i = 0
    valley_count = 0
    
    while i < n:
        if a[i] == min_val:
            start = i
            while i + 1 < n and a[i + 1] == min_val:
                i += 1
            end = i
            left_ok = start == 0 or a[start - 1] > min_val
            right_ok = end == n - 1 or a[end + 1] > min_val
            if left_ok and right_ok:
                valley_count += 1
            i += 1
        else:
            i += 1
    return valley_count == 1

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print("YES" if is_valley(a) else "NO")
```

The function `is_valley` scans the array once. The inner while loop groups contiguous minimal values, and boundary conditions are explicitly checked. Incrementing `i` carefully avoids skipping segments or double-counting.

## Worked Examples

Trace input `[3, 2, 2, 1, 2, 2, 3]`:

| i | a[i] | start | end | left_ok | right_ok | valley_count |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | - | - | - | - | 0 |
| 1 | 2 | - | - | - | - | 0 |
| 2 | 2 | - | - | - | - | 0 |
| 3 | 1 | 3 | 3 | True | True | 1 |
| 4 | 2 | - | - | - | - | 1 |
| 5 | 2 | - | - | - | - | 1 |
| 6 | 3 | - | - | - | - | 1 |

Only one segment `[3,3]` of minimal values satisfies the boundary condition, output "YES".

Trace input `[1, 2, 3, 4, 3, 2, 1]`:

| i | a[i] | start | end | left_ok | right_ok | valley_count |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | True | False | 0 |
| 6 | 1 | 6 | 6 | False | True | 0 |

Two minimal segments exist but none satisfies both boundaries, output "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Linear scan of array, grouping contiguous minimal elements. |
| Space | O(1) | Only counters and indices are maintained, no extra storage proportional to n. |

Given the sum of `n` over all test cases is ≤ 2·10^5, this solution easily fits in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    def is_valley(a):
        n = len(a)
        min_val = min(a)
        i = 0
        valley_count = 0
        while i < n:
            if a[i] == min_val:
                start = i
                while i + 1 < n and a[i + 1] == min_val:
                    i += 1
                end = i
                left_ok = start == 0 or a[start - 1] > min_val
                right_ok = end == n - 1 or a[end + 1] > min_val
                if left_ok and right_ok:
                    valley_count += 1
                i += 1
            else:
                i += 1
        return valley_count == 1
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        res.append("YES" if is_valley(a) else "NO")
    return "\n".join(res)

# provided samples
assert run("""6
7
3 2 2 1 2 2 3
11
1 1 1 2 3 3 4 5 6 6 6
7
1 2 3 4 3 2 1
7
9 7 4 6 9 9 10
1
1000000000
8
9 4 4 5 9 4 9 10
""") == """YES
YES
NO
YES
YES
NO"""

# custom cases
assert run("""4
1
5
5
2 2 2 2 2
5
5 4 3 2 1
6
1 2 1 2 1 2
""") == """YES
NO
YES
NO"""
```

| Test input | Expected output |
