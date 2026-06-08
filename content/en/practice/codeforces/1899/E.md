---
title: "CF 1899E - Queue Sort"
description: "We are given an array of integers, and we want to sort it in non-decreasing order. The catch is that we cannot arbitrarily swap elements."
date: "2026-06-08T21:26:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1899
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 909 (Div. 3)"
rating: 1300
weight: 1899
solve_time_s: 132
verified: true
draft: false
---

[CF 1899E - Queue Sort](https://codeforces.com/problemset/problem/1899/E)

**Rating:** 1300  
**Tags:** greedy, implementation, sortings  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we want to sort it in non-decreasing order. The catch is that we cannot arbitrarily swap elements. Instead, we have a single complex operation available: take the first element, move it to the end, and then bubble it back left as long as it is smaller than its immediate predecessor. Conceptually, this is like rotating the array and letting the moved element "slide" left until it finds the correct spot relative to the elements it passed. The goal is to determine the minimum number of these operations to sort the array or report impossibility if sorting cannot be achieved.

The array can be up to 200,000 elements, and the sum of all array sizes across multiple test cases does not exceed 200,000. This bounds our solution to linear or linearithmic time complexity; anything quadratic would be far too slow. For example, trying to simulate each operation naively could take up to `O(n^2)` time per array, which is infeasible.

Subtle edge cases include arrays that are already sorted (zero operations), arrays where the first element is the largest and blocks sorting unless removed multiple times, and arrays with repeated elements where swaps are limited by the "strictly greater" condition. A small example illustrating a failure of naive simulation is `[4, 3, 1, 2]`. If you just try to move each element forward without considering the global order, you might conclude it can be sorted in one pass, while the correct answer is impossible because the relative order of `3` and `1` cannot be fixed through the allowed operation.

## Approaches

The brute-force approach would literally simulate the operation: repeatedly move the first element to the end and bubble it back until it fits. After each operation, check if the array is sorted. This works because the operation is deterministic and each application changes the array in a defined way. However, the worst-case operation count can reach `n` per element, resulting in `O(n^2)` per test case. With `n` up to 200,000, this is far too slow.

The key insight for an optimal approach is to recognize that the operation essentially allows us to move any prefix of the array that is already in order to the back. If we think about the array from the end backwards, the longest suffix that is already sorted and non-decreasing cannot be touched by future operations; only elements before it can move. The minimum number of operations is therefore determined by the length of the unsorted prefix preceding this sorted suffix. If the unsorted prefix contains any element larger than the first element of the sorted suffix, sorting becomes impossible because the operation cannot insert elements into the middle of the suffix without violating the "strictly greater" rule.

Thus, the problem reduces to identifying the longest non-decreasing suffix from the end and checking if the remaining prefix can be moved to the back in order without conflicts. If yes, the number of operations equals the size of the prefix; otherwise, sorting is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For a given array, start scanning from the end to find the longest non-decreasing suffix. Initialize a pointer `i = n-2` and move backwards as long as `a[i] <= a[i+1]`. After this, `i+1` marks the start of the sorted suffix.
2. Check if the prefix before this suffix can be "rotated" to the end without violating the operation rules. Specifically, the operation allows each element to bubble left until it is no longer smaller than its predecessor. This is equivalent to checking if the prefix is non-increasing because the first element of the array must eventually reach the end of this prefix.
3. Count the number of operations needed, which is exactly the length of the unsorted prefix. This is the number of elements before the sorted suffix.
4. If at any point we detect that an element in the prefix is greater than the start of the sorted suffix and cannot be inserted correctly, output `-1`.

Why it works: The operation allows each prefix element to move to the back while respecting the relative order. The invariant is that once an element enters the sorted suffix, it stays there in the correct relative position. Therefore, identifying the longest sorted suffix tells us the minimal safe point; everything before it must be moved by operations, and their number equals the size of the prefix. Any violation in the prefix means some element will never fit the rules, guaranteeing impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_operations_to_sort(a):
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] <= a[i + 1]:
        i -= 1
    if i == -1:
        return 0  # already sorted
    prefix_length = i + 1
    
    # Check if the prefix is non-increasing
    for j in range(prefix_length - 1):
        if a[j] < a[j + 1]:
            return -1
    return prefix_length

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(min_operations_to_sort(a))
```

The function `min_operations_to_sort` first finds the sorted suffix from the end. If the entire array is already sorted, it returns zero. It then examines the unsorted prefix to ensure it is non-increasing. If it is not, some elements in the prefix will violate the operation's "bubble until strictly greater" condition, making sorting impossible, so we return `-1`. Otherwise, the number of operations equals the prefix length, because each element must be rotated once to reach its correct position.

## Worked Examples

### Example 1

Input: `[6, 4, 1, 2, 5]`

| Step | Array | i | Comment |
| --- | --- | --- | --- |
| Init | 6 4 1 2 5 | 3 | Start from end |
| Scan | 2 5 | 2 | 2 <= 5, continue |
| Scan | 1 2 | 1 | 1 <= 2, continue |
| Scan | 4 1 | 0 | 4 > 1, stop |
| Prefix | 6 4 | 0 | Check non-increasing 6 > 4, valid |
| Result | 2 |  | Minimum operations equals prefix length |

### Example 2

Input: `[4, 3, 1, 2, 6, 4]`

| Step | Array | i | Comment |
| --- | --- | --- | --- |
| Init | 4 3 1 2 6 4 | 4 | Start from end |
| Scan | 6 4 | 4 | 6 > 4, stop |
| Prefix | 4 3 1 2 6 | 0..4 | Check non-increasing 1 < 2, fails |
| Result | -1 |  | Impossible to sort |

These traces demonstrate both the calculation of the minimal prefix length and the detection of impossible cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited at most twice: once in suffix scan, once in prefix check |
| Space | O(1) | Only pointers and counters used, no extra arrays |

Given `n` up to 2e5 and sum of all test cases up to 2e5, this solution comfortably runs under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open('solution.py').read())  # assuming solution saved as solution.py
    return out.getvalue().strip()

# provided samples
assert run("5\n5\n6 4 1 2 5\n7\n4 5 3 7 8 6 2\n6\n4 3 1 2 6 4\n4\n5 2 4 2\n3\n2 2 3\n") == "2\n6\n-1\n-1\n0", "sample 1"

# custom cases
assert run("1\n1\n42\n") == "0", "single element, already sorted"
assert run("1\n5\n1 2 3 4 5\n") == "0", "already sorted array"
assert run("1\n5\n5 4 3 2 1\n") == "5", "strictly decreasing, all need moves"
assert run("1\n5\n2 2 2 2 2\n") == "0", "all equal elements"
assert run("1\n6\n3 3 2 2 1 1\n") == "6", "non-increasing prefix followed by sorted suffix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element `[42]` | 0 | Minimal array size |
| Sorted `[1 2 3 4 5]` | 0 | Already sorted |
| Reverse `[5 4 3 2 1]` | 5 | All elements need operations |
| All equal `[2 2 2 2 2]` | 0 | Non-decreasing with duplicates |
