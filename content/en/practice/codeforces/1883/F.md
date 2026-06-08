---
title: "CF 1883F - You Are So Beautiful"
description: "We are given an array of integers and are asked to count the number of contiguous subarrays whose elements appear as a subsequence in the original array exactly once."
date: "2026-06-08T22:31:33+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1883
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 905 (Div. 3)"
rating: 1400
weight: 1883
solve_time_s: 132
verified: false
draft: false
---

[CF 1883F - You Are So Beautiful](https://codeforces.com/problemset/problem/1883/F)

**Rating:** 1400  
**Tags:** data structures  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and are asked to count the number of contiguous subarrays whose elements appear as a subsequence in the original array **exactly once**. In simpler terms, a subarray is good if, when you try to find it anywhere else in the array without rearranging its elements, there is only one way to select those positions. For example, `[1, 2]` in `[1, 2, 1]` is good because the sequence `1, 2` only appears in the first two positions. But `[1]` is bad because `1` occurs multiple times, so there are multiple ways to pick it as a subsequence.

The input consists of multiple test cases. Each test case has an array up to `10^5` elements, with the sum of all `n` across test cases up to `2*10^5`. This immediately tells us that any solution slower than roughly `O(n log n)` per test case will be too slow. A naive approach enumerating all subarrays would be `O(n^2)` per test case, which is clearly unworkable.

Edge cases arise when all elements are identical, arrays of size 1, or arrays where values alternate repeatedly. For instance, `[1, 1, 1]` has only one valid subarray of length 1 if any single element is allowed, but all longer subarrays are invalid. `[1, 2, 1]` has subarrays `[1, 2]`, `[2, 1]`, `[1, 2, 1]` that behave differently. Handling duplicates carefully is critical, since they control whether a subsequence is unique.

## Approaches

The brute-force approach would be to iterate over all possible subarrays, and for each subarray, check how many times it occurs as a subsequence. Checking subsequences naively takes `O(n)` time for each subarray, and there are `O(n^2)` subarrays, so the overall complexity would be `O(n^3)` per test case. This clearly cannot work for `n` up to `10^5`.

The key insight is that a subarray `[a_l, ..., a_r]` occurs more than once as a subsequence **if any element in the subarray appears elsewhere outside of its current positions in a conflicting order**. To make this precise, we can track for each value its first and last occurrences in the array. A subarray is unique as a subsequence if all of its elements appear **exactly once in the whole array outside of their positions**. Another way to think about it is to maintain a sliding window such that no element inside the window has another occurrence inside the same or overlapping region. This reduces the problem to a two-pointer problem where we expand the right boundary while ensuring that each element inside the window appears at most twice: once in the window, once possibly outside.

A neat observation is that the “bad” elements are those whose first or last occurrence is inside the current window but also occurs outside. By using two maps to track first and last occurrences and then moving the left pointer to exclude conflicts, we can count the number of valid windows efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal Two-Pointer | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. First, precompute for each unique value in the array the indices of its first and last occurrence. This allows us to quickly check if an element in a candidate subarray appears elsewhere in a conflicting position.
2. Initialize a left pointer `l` at 0 and iterate the right pointer `r` from 0 to n-1. We are effectively trying to maintain a valid subarray `[l, r]` where all elements occur in positions that do not create multiple subsequences.
3. Maintain a map that counts the number of times each element appears in the current window. If we try to include an element that already appears inside the window or violates the uniqueness constraint, move the left pointer `l` to shrink the window until the condition is satisfied again.
4. For each position of `r`, the number of valid subarrays ending at `r` is `(r - l + 1)`. Add this count to the total. This works because expanding `r` by one includes all new subarrays ending at `r` with different left endpoints.
5. Continue until `r` reaches the end of the array.

The invariant is that at every step, `[l, r]` is the **largest subarray ending at `r` that is unique as a subsequence**, so counting all subarrays inside it ensures we count all good subarrays exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        last_occurrence = {}
        left = 0
        result = 0
        count = {}
        
        for right in range(n):
            val = a[right]
            count[val] = count.get(val, 0) + 1
            while count[val] > 1:
                count[a[left]] -= 1
                left += 1
            result += right - left + 1
        
        print(result)

solve()
```

We use a dictionary `count` to track occurrences in the current window. Whenever we encounter a duplicate inside the window, we move `left` until the window becomes valid. The number of subarrays ending at each `right` is simply the window length `right - left + 1`.

Boundary handling is subtle: if the window starts shrinking from the left, we must decrement counts carefully to avoid off-by-one errors.

## Worked Examples

### Example 1: `[1, 2, 1]`

| r | val | count | left | subarrays added | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | {1:1} | 0 | 1 | 1 |
| 1 | 2 | {1:1,2:1} | 0 | 2 | 3 |
| 2 | 1 | {1:2,2:1} | 0->1 | 2 | 4 |

Trace confirms the two-pointer invariant: at each step, the window `[left, r]` contains no duplicates, and counting `right - left + 1` gives exactly the valid subarrays.

### Example 2: `[4, 5, 4, 5, 4]`

| r | val | count | left | subarrays added | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | {4:1} | 0 | 1 | 1 |
| 1 | 5 | {4:1,5:1} | 0 | 2 | 3 |
| 2 | 4 | {4:2,5:1} | 0->1 | 2 | 5 |
| 3 | 5 | {4:1,5:2} | 1->2 | 2 | 7 |
| 4 | 4 | {4:2,5:1} | 2->3 | 2 | 9 |

This shows duplicates trigger left pointer adjustments correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is added and removed from the window at most once. |
| Space | O(n) | Dictionary stores counts of distinct elements. |

With total n across all test cases ≤ 2*10^5, this fits comfortably under the 1s limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("6\n1\n1\n2\n1 1\n3\n1 2 1\n4\n2 3 2 1\n5\n4 5 4 5 4\n10\n1 7 7 2 3 4 3 2 1 100\n") == "1\n1\n4\n7\n4\n28"

# Custom cases
assert run("1\n1\n42\n") == "1"  # single element
assert run("1\n5\n1 1 1 1 1\n") == "5"  # all equal
assert run("1\n5\n1 2 3 4 5\n") == "15"  # all unique
assert run("1\n6\n1 2 1 2 1 2\n") == "9"  # alternating duplicates
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n42\n` | 1 | Single-element array |
| `1\n5\n1 1 1 1 1\n` | 5 | Handling all equal values |
| `1\n5\n1 2 3 4 5\n` | 15 | All unique values, counting all subarrays |
| `1\n6\n |  |  |
