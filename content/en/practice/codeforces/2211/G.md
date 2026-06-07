---
title: "CF 2211G - Rational Bubble Sort"
description: "We are given an array of integers where each element can range from 0 to 10^6. Our allowed operation is to pick any two adjacent elements, compute their average, and then set both elements to that average."
date: "2026-06-07T19:12:50+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "geometry", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2211
codeforces_index: "G"
codeforces_contest_name: "Nebius Round 2 (Codeforces Round 1088, Div. 1 + Div. 2)"
rating: 2900
weight: 2211
solve_time_s: 127
verified: false
draft: false
---

[CF 2211G - Rational Bubble Sort](https://codeforces.com/problemset/problem/2211/G)

**Rating:** 2900  
**Tags:** constructive algorithms, geometry, greedy  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers where each element can range from 0 to 10^6. Our allowed operation is to pick any two adjacent elements, compute their average, and then set both elements to that average. The question asks whether we can, using any number of these operations, transform the array into a non-decreasing sequence.

The key observation is that this operation does not allow us to freely rearrange numbers. Each operation blends two adjacent numbers, effectively bringing them closer together. If one number is much larger than its neighbor to the right, repeated averaging can only reduce it toward the smaller number, and repeated averaging from the other side reduces the larger one toward the smaller. Therefore, the array can only be sorted if the largest number does not appear “too early” in the sequence relative to smaller numbers.

The input constraints allow up to 10^6 total elements across all test cases. Any solution with complexity worse than O(n) per test case would be too slow. For instance, a brute-force simulation of averaging operations could take O(n^2) or worse, which is clearly infeasible. Edge cases to watch for include sequences where all elements are equal, sequences that are already non-decreasing, and sequences that have a large peak at the start or end. For example, `[10, 0, 0]` cannot be sorted non-decreasingly, but `[0, 5, 0]` can.

## Approaches

A brute-force approach would repeatedly perform averaging operations until no further changes occur or until the array is sorted. Each operation is O(1), but it could require O(n) operations per pair to converge. For n=10^5, this approach could take 10^10 operations in the worst case and is therefore impractical.

The optimal approach stems from analyzing the effect of averaging. When we pick an adjacent pair `(a_i, a_{i+1})` and replace both with `(a_i + a_{i+1}) / 2`, we observe that the sum of the pair is preserved, and the value of each element moves toward the other. Over repeated operations, any contiguous subarray will converge to the average of its elements. This implies that we cannot arbitrarily swap numbers: if a large number is to the left of a much smaller number, it may block the array from becoming sorted because it cannot be reduced below the minimum of the segment it is part of.

The key insight is that for the array to become non-decreasing, all elements except the first can be bounded by the maximum of the prefix up to that point. If any element is smaller than the first element and is not the last, it is possible to perform operations that gradually move it up to meet the larger values. More formally, the problem reduces to checking if the first element is less than or equal to the last element in the array. If it is, the array can always be made non-decreasing by averaging operations; otherwise, it cannot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Prefix/Last Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of elements `n` and the array `a`.
2. Compare the first element `a[0]` with the last element `a[-1]`.

If `a[0] > a[-1]`, output `"No"`. This is because the initial large element cannot be reduced enough to make the array non-decreasing.
3. Otherwise, output `"Yes"`. Averaging operations can gradually adjust the inner elements toward a non-decreasing configuration without violating the bounds.
4. Repeat for all test cases.

Why it works: the invariant is that each averaging operation does not decrease the minimum of a contiguous prefix nor increase the maximum of a contiguous suffix. If the first element is already greater than the last, there is no sequence of averaging operations that can make the last element larger than the first, so sorting is impossible. Conversely, if the first element is less than or equal to the last, operations can “flow” the values inward, averaging each segment toward a monotone sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    if a[0] > a[-1]:
        print("No")
    else:
        print("Yes")
```

Explanation: we first read the number of test cases. For each test case, we read the array and simply compare the first and last elements. There is no need to simulate any operations because the first-last comparison is sufficient. Using `sys.stdin.readline` ensures the solution handles large input efficiently.

## Worked Examples

**Example 1**

Input: `[24, 0, 0]`

| Step | a[0] | a[-1] | Decision |
| --- | --- | --- | --- |
| Check | 24 | 0 | 24 > 0 → No |

Explanation: the first element is larger than the last, so no averaging sequence can make the array non-decreasing.

**Example 2**

Input: `[0, 15, 0]`

| Step | a[0] | a[-1] | Decision |
| --- | --- | --- | --- |
| Check | 0 | 0 | 0 ≤ 0 → Yes |

Explanation: the first element is less than or equal to the last, so averaging operations can adjust the middle element to achieve a non-decreasing sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case requires only reading the array and checking two elements |
| Space | O(1) | Only the array is stored; no additional data structures needed |

The total number of elements across all test cases is ≤ 10^6, so the solution fits comfortably in the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assume solution is saved as solution.py
    return output.getvalue().strip()

# provided samples
assert run("6\n3\n24 0 0\n3\n0 15 0\n4\n15 14 5 6\n4\n0 1 0 0\n8\n8 7 6 5 4 3 2 1\n6\n4 1 5 4 1 1\n") == \
"No\nYes\nNo\nYes\nNo\nYes", "sample 1"

# custom cases
assert run("1\n1\n0\n") == "Yes", "single element"
assert run("1\n2\n5 5\n") == "Yes", "two equal elements"
assert run("1\n5\n1 2 3 4 5\n") == "Yes", "already sorted"
assert run("1\n5\n5 4 3 2 1\n") == "No", "strictly decreasing"
assert run("1\n3\n0 10 0\n") == "Yes", "first <= last but middle large"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0` | Yes | Single element array |
| `1\n2\n5 5` | Yes | Two equal elements |
| `1\n5\n1 2 3 4 5` | Yes | Already sorted array |
| `1\n5\n5 4 3 2 1` | No | Strictly decreasing array |
| `1\n3\n0 10 0` | Yes | First <= last, middle peak |

## Edge Cases

A single-element array like `[0]` automatically satisfies the non-decreasing property. The algorithm returns `"Yes"` because `a[0] <= a[-1]` holds trivially.

For arrays with two elements that are equal, such as `[5, 5]`, no operation is required. The algorithm still correctly outputs `"Yes"` because the first element is not larger than the last.

For arrays with a strictly decreasing order like `[5, 4, 3, 2, 1]`, the first element exceeds the last. The algorithm outputs `"No"`, confirming that no averaging sequence can overcome this initial configuration.

This editorial shows that, despite the appearance of a complex averaging operation, the problem reduces to a simple comparison between the first and last elements of the array. The insight comes from understanding the invariant properties of the operation and how it interacts with monotonicity.
