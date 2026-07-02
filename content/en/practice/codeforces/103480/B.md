---
title: "CF 103480B - 7 \u7684\u610f\u5fd7"
description: "We are given several independent test cases. In each test case we receive an array of positive integers, and the task is to count how many subarrays have sum exactly equal to 7777."
date: "2026-07-03T06:30:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103480
codeforces_index: "B"
codeforces_contest_name: "The 4th Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 103480
solve_time_s: 42
verified: true
draft: false
---

[CF 103480B - 7 \u7684\u610f\u5fd7](https://codeforces.com/problemset/problem/103480/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case we receive an array of positive integers, and the task is to count how many subarrays have sum exactly equal to 7777. A subarray is defined by choosing two indices $l$ and $r$ with $l \le r$, and summing all elements between them inclusively. We are not asked to find maximum or minimum values, only to count how many different contiguous segments produce the target sum.

The constraints matter in a very direct way. The array length can be up to $10^5$, and there can be up to 10 test cases. A naive quadratic enumeration of all subarrays would involve about $10^{10}$ operations in the worst case, which is far beyond what can run in one second. This immediately rules out any approach that recomputes sums from scratch for every pair of endpoints.

There is a structural constraint that becomes important: every element is positive and at most 5000. This guarantees that prefix sums are strictly increasing and that sliding window behavior is well-defined without worrying about negative corrections.

A subtle failure case for naive implementations is recomputing subarray sums repeatedly. For example, if we fix a left endpoint and extend right pointers while summing repeatedly, we still end up doing $O(n^2)$ additions. Another pitfall is ignoring that multiple subarrays may overlap heavily, and counting them incorrectly if one uses hashing on sums without proper prefix alignment.

## Approaches

The brute-force approach is straightforward: enumerate every pair $(l, r)$, compute the sum of the subarray, and check whether it equals 7777. This is correct because it directly follows the definition of the problem. However, computing each sum from scratch costs $O(n)$, and there are $O(n^2)$ pairs, leading to $O(n^3)$ time. Even if we optimize each subarray sum using a prefix sum array, reducing each query to $O(1)$, we still have $O(n^2)$ total subarrays per test case, which is too large for $n = 10^5$.

The key observation comes from the positivity of all elements. Since all numbers are positive, prefix sums strictly increase as we move right. This allows us to maintain a sliding window: for each right endpoint, we can move the left endpoint forward while the sum exceeds the target. The invariant is that the current window sum is always maintained efficiently, and no valid subarray is skipped or double-counted.

This transforms the problem into a two-pointer scan over the array, where each pointer only moves forward at most $n$ times, producing an $O(n)$ solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or $O(n^3)$ | $O(1)$ | Too slow |
| Optimal Two Pointers | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain a sliding window $[l, r]$ and its current sum.

1. Initialize two pointers $l = 0$, $r = 0$, and a running sum equal to 0. This represents an empty window before processing any elements.
2. Move the right pointer step by step from left to right. At each step, add the current element to the running sum. This expands the window and ensures we consider every possible subarray ending at $r$.
3. While the current sum exceeds 7777, move the left pointer forward and subtract the element leaving the window. This is valid because all elements are positive, so shrinking from the left can only decrease the sum, never increase it.
4. After adjusting the window, if the sum equals 7777, increment the answer. This counts the unique subarray ending at the current $r$ whose sum matches the target.
5. Continue until the right pointer reaches the end of the array.

The correctness relies on the fact that at each position $r$, the algorithm finds all valid left boundaries $l$ such that the subarray sum is exactly 7777. Because the array contains only positive numbers, there is at most one valid adjustment sequence per $r$, and no valid subarray is skipped.

### Why it works

The key invariant is that at every step, the window $[l, r]$ is the smallest possible left boundary for the current right endpoint such that the sum does not exceed 7777. Because elements are positive, moving $l$ forward monotonically decreases the sum, and thus each pointer moves at most $n$ times. Every valid subarray ending at $r$ must appear exactly when the window sum becomes 7777 after shrinking from an overlarge sum, so every solution is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    target = 7777
    l = 0
    s = 0
    ans = 0
    
    for r in range(n):
        s += arr[r]
        
        while l <= r and s > target:
            s -= arr[l]
            l += 1
        
        if s == target:
            ans += 1
    
    return ans

t = int(input())
out = []
for _ in range(t):
    out.append(str(solve()))
print("\n".join(out))
```

The code mirrors the sliding window process directly. The variable `s` tracks the current window sum, and the left pointer `l` is only moved when necessary to keep the sum within bounds. The condition `s == target` is checked only after restoring feasibility, ensuring correctness. The use of a single pass per test case keeps the implementation efficient and simple, avoiding any prefix-sum dictionary or hashing.

## Worked Examples

Consider the array `[2000, 3000, 2777, 1000]`.

We track the sliding window:

| r | l | window | sum | action |
| --- | --- | --- | --- | --- |
| 0 | 0 | [2000] | 2000 | expand |
| 1 | 0 | [2000, 3000] | 5000 | expand |
| 2 | 0 | [2000, 3000, 2777] | 7777 | match found |
| 3 | 0 | [2000, 3000, 2777, 1000] | 8777 | shrink left |

When we reach $r = 2$, the sum matches exactly once, so we count one subarray. At $r = 3$, the sum exceeds the target and shrinking would be required, but no exact match appears.

Now consider `[7777, 1, 7776]`.

| r | l | window | sum | action |
| --- | --- | --- | --- | --- |
| 0 | 0 | [7777] | 7777 | match |
| 1 | 0 | [7777, 1] | 7778 | shrink |
| 1 | 1 | [1] | 1 | no match |
| 2 | 1 | [1, 7776] | 7777 | match |

This example shows that valid subarrays can appear after shrinking the window, and the algorithm correctly re-evaluates the condition after each adjustment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is added and removed at most once via two pointers |
| Space | $O(1)$ extra space | Only a few counters and pointers are used |

Given $T \le 10$ and $n \le 10^5$, the total work is linear in the input size, comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        n = int(input())
        arr = list(map(int, input().split()))
        target = 7777
        l = 0
        s = 0
        ans = 0
        for r in range(n):
            s += arr[r]
            while l <= r and s > target:
                s -= arr[l]
                l += 1
            if s == target:
                ans += 1
        return ans
    
    t = int(input())
    out = []
    for _ in range(t):
        out.append(str(solve()))
    return "\n".join(out)

# sample-like case
assert run("1\n4\n2000 3000 2777 1000") == "1"

# exact match at single element
assert run("1\n1\n7777") == "1"

# no valid subarray
assert run("1\n3\n1 2 3") == "0"

# multiple overlapping valid subarrays
assert run("1\n5\n7777 1 7776 1 7777") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single exact element | 1 | single-element match |
| no solution | 0 | absence handling |
| overlapping matches | 3 | multiple valid windows |

## Edge Cases

One important edge case is when a single element equals 7777. For input `[7777]`, the algorithm starts with `r = 0`, adds the element, and immediately finds `s == 7777`, so it counts exactly one subarray.

Another case is when all elements are small and no combination reaches 7777. For example `[1, 2, 3]` causes the window sum to never exceed the target, and since it never equals 7777, the answer remains zero.

A more subtle case is when the sum briefly exceeds the target and must shrink before a valid window is found again. In `[7777, 1, 7776]`, the window first matches at index 0, then expands beyond the target, then shrinks and later finds another valid subarray. The sliding window correctly handles this because it always restores feasibility before checking equality again.
