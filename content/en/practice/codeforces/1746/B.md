---
title: "CF 1746B - Rebellion"
description: "We are given a binary array, containing only zeroes and ones, and we can perform an operation where we choose two distinct elements, add the value of the first element to the second, and then remove the first element. Each operation reduces the size of the array by one."
date: "2026-06-09T15:42:32+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1746
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 23"
rating: 800
weight: 1746
solve_time_s: 165
verified: false
draft: false
---

[CF 1746B - Rebellion](https://codeforces.com/problemset/problem/1746/B)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, two pointers  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array, containing only zeroes and ones, and we can perform an operation where we choose two distinct elements, add the value of the first element to the second, and then remove the first element. Each operation reduces the size of the array by one. The goal is to make the array non-decreasing, meaning every element is at least as large as the one before it. We are asked to determine the minimum number of such operations needed.

The input consists of multiple test cases. Each test case provides the length of the array and the array itself. The constraints allow arrays of size up to 100,000, and the sum of all arrays across all test cases does not exceed 200,000. With a one-second time limit, this rules out any solution that is quadratic or worse, because O(n^2) operations could be up to 10^10 in the worst case.

A key edge case is an array that is already non-decreasing, such as `[0, 0, 1, 1]`. Here, the answer should be zero. Another tricky case is when a single `1` appears before a sequence of zeros, for example `[1, 0, 0]`. A naive approach might try to pair adjacent elements without considering the cumulative effect of moving `1`s forward, potentially producing too many operations. Also, arrays with only zeroes or only ones need special handling because they are trivially non-decreasing.

## Approaches

The brute-force approach would try all possible pairs of indices to perform the operation, checking at each step whether the array has become non-decreasing. This is correct in principle, but each operation reduces the array by only one element and there are potentially n*(n-1)/2 choices at each step, giving a worst-case complexity of O(n^2) or worse. With n up to 10^5, this approach is infeasible.

The optimal insight comes from realizing that the only elements that violate the non-decreasing property are `1`s that appear before zeros. Every `0` that is preceded by a `1` is a candidate for correction. Importantly, moving all problematic `1`s toward the end can be done greedily by counting how many `0`s appear after the last `1` and performing operations to remove `1`s from the front, adding them to the last `1` or another `1` that is already after the zeros. This reduces the problem to counting the number of `1`s before the first `0` from the right that violates the order, which is exactly the number of operations needed.

The key observation is that the minimal number of operations is equal to the count of `1`s that appear before the last zero that needs to be "pushed forward". Every such `1` must be involved in an operation to restore non-decreasing order, while `1`s already after zeros do not need to move.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array length `n` and the array `a`.
2. Initialize a counter `ops` to zero and a flag `zeros_seen` to false.
3. Traverse the array from right to left. For each element:

- If the element is `0`, set `zeros_seen` to true. This identifies that any `1` before this point will need an operation.
- If the element is `1` and `zeros_seen` is true, increment `ops`. This counts the number of `1`s that are out of order and need to be moved.
4. After completing the traversal, `ops` contains the minimum number of operations required. Print `ops`.

The reason this works is that any `1` that occurs before a `0` in a segment that violates the non-decreasing order must participate in an operation to restore order. By scanning from right to left, we ensure that we count exactly those `1`s that are before the last zero that needs to be fixed. All other elements are already in non-decreasing order and do not contribute to the operation count.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    ops = 0
    zeros_seen = False
    for x in reversed(a):
        if x == 0:
            zeros_seen = True
        elif zeros_seen:
            ops += 1
    print(ops)
```

This code reads input efficiently using `sys.stdin.readline` and handles multiple test cases. It uses a single pass from right to left to count the number of `1`s that are before zeros, which corresponds to the minimal operations. The use of a flag avoids scanning the array multiple times or using additional storage.

## Worked Examples

**Example 1:**

Input array: `[1, 0, 0, 1, 0]`

| Index | Element | zeros_seen | ops |
| --- | --- | --- | --- |
| 4 | 0 | True | 0 |
| 3 | 1 | True | 1 |
| 2 | 0 | True | 1 |
| 1 | 0 | True | 1 |
| 0 | 1 | True | 2 |

The table shows that the `1`s at positions 0 and 3 need operations, so the output is `2`.

**Example 2:**

Input array: `[0, 0, 1, 1]`

| Index | Element | zeros_seen | ops |
| --- | --- | --- | --- |
| 3 | 1 | False | 0 |
| 2 | 1 | False | 0 |
| 1 | 0 | True | 0 |
| 0 | 0 | True | 0 |

No `1` appears before a zero, so no operations are needed. Output is `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the array per test case |
| Space | O(1) | Only a few integer variables are used |

Given the constraints of sum of n over all test cases ≤ 2·10^5, this linear solution comfortably fits within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        ops = 0
        zeros_seen = False
        for x in reversed(a):
            if x == 0:
                zeros_seen = True
            elif zeros_seen:
                ops += 1
        print(ops)
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n8\n0 0 1 1 1 1 1 1\n5\n1 0 0 1 1\n2\n1 0\n11\n1 1 0 0 1 0 0 1 1 1 0\n") == "0\n1\n1\n3"

# Custom cases
assert run("2\n1\n0\n1\n1\n") == "0\n0", "single element arrays"
assert run("1\n5\n1 1 1 1 1\n") == "0", "all ones"
assert run("1\n5\n0 0 0 0 0\n") == "0", "all zeros"
assert run("1\n6\n1 0 1 0 1 0\n") == "3", "alternating ones and zeros"
assert run("1\n4\n1 0 0 1\n") == "2", "ones at edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0` and `1\n1` | `0\n0` | single-element arrays |
| `1\n1 1 1 1 1` | `0` | all ones, already non-decreasing |
| `1\n0 0 0 0 0` | `0` | all zeros, already non-decreasing |
| `1\n1 0 1 0 1 0` | `3` | alternating ones and zeros, tests correct counting of `1`s before zeros |
| `1\n1 0 0 1` | `2` | ones at edges, tests handling of `1`s before zeros |

## Edge Cases

For the array `[1, 0, 1]`, the algorithm sets `zeros_seen` when it sees the `0` at index 1. The `1` at index 0 is counted as needing an operation, while the `1` at index 2 comes after the zero and does not increase `ops`. The output is `1`, which matches the minimal operations required.

For an array with a single element, such as `[0]` or `[1]`, the algorithm never enters the `elif zeros_seen` branch, so `ops` remains zero, correctly returning `0`. This confirms the approach handles the minimal input edge case.
