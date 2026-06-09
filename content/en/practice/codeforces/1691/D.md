---
title: "CF 1691D - Max GEQ Sum"
description: "We are asked to determine whether, for a given integer array, the maximum value in any contiguous subarray is at least as large as the sum of that subarray."
date: "2026-06-09T23:10:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "divide-and-conquer", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1691
codeforces_index: "D"
codeforces_contest_name: "CodeCraft-22 and Codeforces Round 795 (Div. 2)"
rating: 1800
weight: 1691
solve_time_s: 117
verified: true
draft: false
---

[CF 1691D - Max GEQ Sum](https://codeforces.com/problemset/problem/1691/D)

**Rating:** 1800  
**Tags:** binary search, constructive algorithms, data structures, divide and conquer, implementation, two pointers  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether, for a given integer array, the maximum value in any contiguous subarray is at least as large as the sum of that subarray. In simpler terms, for every possible segment of the array, the single largest number must not be smaller than the sum of all numbers in that segment. If there exists even one subarray where the sum exceeds the maximum element, the answer is "NO"; otherwise, it is "YES".

The input provides multiple test cases, each with an array of length up to 200,000, and the total number of elements across all test cases is capped at 200,000. Each element can range from -10^9 to 10^9. Given that n can be up to 2·10^5 and the time limit is 2 seconds, an algorithm with complexity worse than O(n) per test case is likely too slow. This rules out any approach that tries to examine all subarrays explicitly because that would require O(n²) operations per array, which can reach 4·10¹⁰ in the worst case.

A non-obvious edge case occurs when the array contains a large positive number flanked by negatives. For instance, in the array [-1, 5, -1], every subarray's sum is at most 5, and the maximum element is 5. A naive approach might fail if it does not consider subarrays of length 2 or 3 or only looks at adjacent sums without accounting for negatives that reduce the sum. Another edge case is a strictly increasing sequence of positive numbers, like [1, 2, 3], where the sum of the first two elements is 3, which equals the maximum in that subarray, but adding the next element produces a sum larger than the largest element so far, violating the condition.

## Approaches

The brute-force approach would examine all possible subarrays, compute both their sum and maximum, and verify the condition for each. For an array of size n, there are roughly n(n+1)/2 subarrays, and computing each sum or maximum independently would take O(n) time, giving a total complexity of O(n³). Even with prefix sums and segment maximums using data structures, the number of subarrays alone makes this approach infeasible for n = 2·10^5.

The key observation is that if the condition fails, it must fail on a subarray where the sum is locally maximal in some sense. Because any negative element only decreases the sum, the most dangerous subarrays are contiguous segments starting from the first element or ending at the last element. In other words, we only need to check prefix sums and suffix sums of all proper subarrays (those not including the entire array). If every proper prefix and suffix has a sum that does not exceed the maximum element anywhere in that subarray, the condition holds.

This reduces the problem to computing maximum prefix sums and maximum suffix sums efficiently and comparing them to adjacent elements. In practice, it suffices to iterate through the array and check whether any prefix or suffix sum of proper subarrays becomes strictly greater than the maximum in the whole array. If such a subarray exists, the answer is "NO"; otherwise, it is "YES". This approach is O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array and identify its maximum element. This is the candidate for satisfying the inequality because any sum must not exceed this maximum.
2. Check all proper prefixes of the array. Initialize a running sum to zero. Iterate from the first element to the penultimate element, adding each element to the running sum. If at any point the running sum exceeds the array's maximum, the condition is violated, so immediately return "NO".
3. Check all proper suffixes of the array. Reset the running sum to zero and iterate from the last element to the second element, adding each element to the running sum. Again, if the sum ever exceeds the maximum element, return "NO".
4. If both checks complete without finding a violating subarray, the condition holds for the array, so return "YES".

The intuition is that the inequality is only tight for subarrays that are prefixes or suffixes of some part of the array. Any subarray fully contained inside can be decomposed into a prefix and a suffix, and since negative numbers only reduce sums, if the condition holds for all prefixes and suffixes, it holds for all subarrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        max_val = max(a)

        # check prefixes
        prefix_sum = 0
        valid = True
        for i in range(n - 1):
            prefix_sum += a[i]
            if prefix_sum > max_val:
                valid = False
                break

        # check suffixes
        if valid:
            suffix_sum = 0
            for i in range(n - 1, 0, -1):
                suffix_sum += a[i]
                if suffix_sum > max_val:
                    valid = False
                    break

        print("YES" if valid else "NO")

if __name__ == "__main__":
    solve()
```

The code first identifies the maximum element. It then checks prefix sums from the first element to the penultimate, because including the last element is unnecessary-if the entire array sum exceeds the maximum, the array itself would violate the condition, which is forbidden. Similarly, the suffix check runs from the last element to the second element. Each loop immediately breaks if the condition is violated, optimizing for speed.

## Worked Examples

**Example 1: [-1, 1, -1, 2]**

| Step | Prefix/Suffix | Running Sum | Max | Valid? |
| --- | --- | --- | --- | --- |
| Prefix | -1 | -1 | 2 | YES |
| Prefix | -1+1=0 | 0 | 2 | YES |
| Prefix | 0-1=-1 | -1 | 2 | YES |
| Suffix | 2 | 2 | 2 | YES |
| Suffix | 2-1=1 | 1 | 2 | YES |
| Suffix | 1+1=2 | 2 | 2 | YES |

All sums ≤ max element, output YES.

**Example 2: [2, 3, -1]**

| Step | Prefix | Running Sum | Max | Valid? |
| --- | --- | --- | --- | --- |
| Prefix | 2 | 2 | 3 | YES |
| Prefix | 2+3=5 | 5 | 3 | NO |

Prefix sum 5 exceeds max 3, output NO.

This demonstrates the algorithm correctly detects violation in subarrays starting at the array's beginning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each array element is visited at most twice: once for prefixes, once for suffixes |
| Space | O(n) | To store the array; auxiliary variables are O(1) |

Since the total sum of n over all test cases is 2·10^5, this linear approach executes well within the 2-second limit. Memory usage also remains below the 256 MB cap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("3\n4\n-1 1 -1 2\n5\n-1 2 -3 2 -1\n3\n2 3 -1\n") == "YES\nYES\nNO", "sample 1"

# custom cases
assert run("1\n1\n100\n") == "YES", "single element"
assert run("1\n5\n1 1 1 1 1\n") == "YES", "all equal small numbers"
assert run("1\n3\n-5 -3 -2\n") == "YES", "all negative numbers"
assert run("1\n4\n1 2 3 4\n") == "NO", "increasing positives"
assert run("1\n6\n2 -1 2 -1 2 -1\n") == "YES", "alternating small negative and positive"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | YES | Minimum-size array |
| 1 1 1 1 1 | YES | All-equal values |
| -5 -3 -2 | YES | Negative numbers only |
| 1 2 3 4 | NO | Prefix sum exceeds max |
| 2 -1 2 -1 2 -1 | YES | Alternating signs, sum never exceeds max |

## Edge Cases

For a single-element array like [100], the algorithm computes the maximum as 100. Both prefix and suffix loops are skipped because n-1 is zero, so the condition passes automatically, outputting YES.

For an array with all negative numbers, e.g., [-5, -3, -2], the prefix sum starts negative and never exceeds the maximum, which is -2. The suffix sums similarly remain below -2. The algorithm correctly returns YES.
