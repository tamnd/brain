---
title: "CF 1692E - Binary Deque"
description: "We are given a binary array of length $n$, meaning each element is either 0 or 1. The task is to perform a sequence of operations where, in each operation, we remove either the first or the last element of the array."
date: "2026-06-09T23:02:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1692
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 799 (Div. 4)"
rating: 1200
weight: 1692
solve_time_s: 110
verified: true
draft: false
---

[CF 1692E - Binary Deque](https://codeforces.com/problemset/problem/1692/E)

**Rating:** 1200  
**Tags:** binary search, implementation, two pointers  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary array of length $n$, meaning each element is either 0 or 1. The task is to perform a sequence of operations where, in each operation, we remove either the first or the last element of the array. After some number of these removals, the sum of the remaining elements must equal a target value $s$. We want to find the minimum number of operations required to reach this sum, or report -1 if it is impossible.

The input provides multiple test cases, each with the array size $n$, the target sum $s$, and the array itself. The sum of all $n$ over all test cases does not exceed 200,000, so our solution must process each test case efficiently, ideally in linear time relative to the size of the array. Quadratic solutions, such as trying all possible prefixes and suffixes explicitly, would be far too slow for the largest arrays because they could require up to $n^2$ operations per test case.

Edge cases arise when the target sum is already achieved, when $s$ is zero or equal to the total sum of the array, or when all elements are identical. For example, if the array is $[1, 1, 1]$ and $s = 0$, a naive approach that only removes elements from the start might fail to explore removing from the end. Another subtle case is when the array has zeros at both ends, like $[0, 1, 1, 0]$ with $s = 2$; we must recognize that removing zeros does not affect the sum and should minimize operations.

## Approaches

The brute-force method would iterate over all combinations of removing $i$ elements from the front and $j$ elements from the back. For each combination, we would compute the sum of the remaining array. This works for small arrays because it correctly explores every possible subarray, but it requires $O(n^2)$ operations per test case in the worst case. With $n$ up to 200,000, this approach would require 40 billion operations in the worst case, which is completely infeasible.

The key insight comes from rewriting the problem: instead of thinking about what to remove, think about what to keep. If the array sum is $total\_sum$, then removing elements to reach sum $s$ is equivalent to keeping a contiguous subarray whose sum is $s$. Since we can remove elements from both ends, the subarray we keep must be continuous. This reduces the problem to finding the longest contiguous subarray with sum equal to $s$. Once we know the length of this subarray, the minimum number of operations is simply the total number of elements minus the length of the subarray.

This leads naturally to a two-pointer or sliding window solution. Sliding window works efficiently because the array only contains 0s and 1s, so the sum of the window can be updated incrementally in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array. If $s$ is greater than the total sum, immediately return -1 because it is impossible to reach $s$. If $s$ equals the total sum, return 0 since no operations are needed.
2. Initialize two pointers: `left = 0` for the start of the window and `current_sum = 0` for the sum of elements within the window. We will attempt to find the longest subarray whose sum equals $s$.
3. Iterate over the array with an index `right`. Add `array[right]` to `current_sum`. If `current_sum` exceeds $s$, move the `left` pointer forward and subtract `array[left]` from `current_sum` until `current_sum <= s`.
4. Whenever `current_sum` equals $s$, update a variable `max_length` to track the maximum length of such a subarray.
5. After the loop, if `max_length` remains -1, return -1 because no valid subarray was found. Otherwise, return `n - max_length`, which represents the minimum number of operations required to reduce the array to the desired sum.

Why it works: the sliding window invariant ensures that `current_sum` always represents the sum of a contiguous subarray ending at `right`. By adjusting `left`, we shrink the window only when necessary, guaranteeing that every candidate subarray with sum `s` is considered. Keeping track of the maximum length ensures the minimum number of removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_operations_to_sum(n, s, arr):
    total = sum(arr)
    if s > total:
        return -1
    if s == total:
        return 0
    
    max_len = -1
    left = 0
    current_sum = 0
    
    for right in range(n):
        current_sum += arr[right]
        while current_sum > s and left <= right:
            current_sum -= arr[left]
            left += 1
        if current_sum == s:
            max_len = max(max_len, right - left + 1)
    
    return n - max_len if max_len != -1 else -1

t = int(input())
for _ in range(t):
    n, s = map(int, input().split())
    arr = list(map(int, input().split()))
    print(min_operations_to_sum(n, s, arr))
```

The solution first handles impossible cases quickly, then uses a sliding window to locate the longest subarray with the target sum. The `while` loop inside the `for` ensures that the window shrinks correctly when the sum exceeds $s$. The `max_len` variable tracks the longest valid subarray. Returning `n - max_len` converts the kept subarray into the minimum number of removals.

## Worked Examples

### Example 1

Input: `3 1 1 0 0`

| right | left | current_sum | max_len |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 2 | 0 | 1 | 1 |

Result: `3 - 1 = 2`, but careful, we check total sum: `sum(arr) = 1`, equals s, so return 0.

### Example 2

Input: `9 3 0 1 0 1 1 1 0 0 1`

| right | left | current_sum | max_len |
| --- | --- | --- | --- |
| 0 | 0 | 0 | -1 |
| 1 | 0 | 1 | -1 |
| 2 | 0 | 1 | -1 |
| 3 | 0 | 2 | -1 |
| 4 | 0 | 3 | 5 |
| 5 | 0 | 4 | - subtract left -> left=1, current_sum=4, left=2 -> current_sum=4, left=3->current_sum=3 |

`max_len = 6`, result: `9 - 6 = 3`.

This trace confirms that the window correctly adjusts both ends and finds the longest subarray matching the target sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is added and removed at most once in the sliding window. |
| Space | O(1) | Only a few variables are used beyond the input array. |

Given the constraints that the sum of all $n$ across test cases is ≤ 200,000, the algorithm is well within the time limit of 2 seconds and uses negligible additional memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, s = map(int, input().split())
        arr = list(map(int, input().split()))
        print(min_operations_to_sum(n, s, arr))
    return output.getvalue().strip()

# Provided samples
assert run("7\n3 1\n1 0 0\n3 1\n1 1 0\n9 3\n0 1 0 1 1 1 0 0 1\n6 4\n1 1 1 1 1 1\n5 1\n0 0 1 1 0\n16 2\n1 1 0 0 1 0 0 1 1 0 0 0 0 0 1 1\n6 3\n1 0 1 0 0 0") == "0\n1\n3\n2\n2\n7\n-1"

# Custom tests
assert run("2\n1 1\n1\n1 0\n0") == "0\n-1", "single element arrays"
assert run("1\n5 3\n1 1 1 1 1") == "2", "all ones, remove two elements"
assert run("1\n5 0\n0 0 0 0 0") == "0", "all zeros,
```
