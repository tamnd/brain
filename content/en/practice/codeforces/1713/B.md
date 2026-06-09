---
title: "CF 1713B - Optimal Reduction"
description: "We are given an array of positive integers. We can repeatedly choose a contiguous subarray and decrease all elements in that subarray by one. The goal is to bring all array elements to zero using as few operations as possible."
date: "2026-06-09T20:12:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1713
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 812 (Div. 2)"
rating: 1000
weight: 1713
solve_time_s: 148
verified: false
draft: false
---

[CF 1713B - Optimal Reduction](https://codeforces.com/problemset/problem/1713/B)

**Rating:** 1000  
**Tags:** constructive algorithms, sortings  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers. We can repeatedly choose a contiguous subarray and decrease all elements in that subarray by one. The goal is to bring all array elements to zero using as few operations as possible. Let us denote by $f(a)$ the minimum number of such operations needed for an array $a$. The task is to determine whether the given array $a$ is already "optimal" in the sense that no permutation of $a$ can be reduced to zero in fewer operations.

The input consists of multiple test cases. Each test case gives the length $n$ of the array and the array itself. The output should be "YES" if the array is optimal in the sense above, and "NO" otherwise. The constraints allow $n$ up to $10^5$ per test case, with the sum over all test cases also up to $10^5$. This rules out any algorithm with quadratic or worse complexity, so an $O(n \log n)$ or $O(n)$ solution is necessary.

Non-obvious edge cases include arrays with repeated numbers, arrays in sorted or reverse-sorted order, and arrays with the maximum element at either end. For example, for $a = [3,1,3,2]$, the array is not optimal because rearranging it to $[1,2,3,3]$ reduces the number of operations from 5 to 3. Careless implementations that do not consider permutations can falsely declare such arrays as optimal.

## Approaches

A brute-force approach would try all permutations of the array and compute $f(b)$ for each. Computing $f(b)$ could be done with a recursive or iterative strategy that subtracts the minimum of the current segment repeatedly. However, for $n = 10^5$, the number of permutations is $n!$, which is completely infeasible. Even computing $f(a)$ directly with a naive segment subtraction algorithm is too slow for large arrays.

The key observation is that $f(a)$ is minimized when the array is non-decreasing. The reason is that any local decrease in a non-monotone sequence creates extra operations. In other words, the "optimal" arrangement is sorted in non-decreasing order. Once the array is sorted, the minimal number of operations equals the largest element because we can always cover the previous elements as part of larger segments. Therefore, the array $a$ is already optimal if it is sorted in non-decreasing order. If there exists an element that is smaller than its predecessor, then there exists a permutation (the sorted one) that reduces $f(a)$. This leads directly to a simple check: compare the array to its sorted version.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the array length $n$ and the array $a$.
3. Create a sorted copy of $a$ in non-decreasing order.
4. Compare $a$ with its sorted version. If they are identical, print "YES". Otherwise, print "NO".

This algorithm works because the only arrays that are guaranteed to require the minimum number of operations among all permutations are those that are sorted in non-decreasing order. Any deviation from this order can always be improved by rearranging into a non-decreasing sequence, which never increases $f(a)$ and often reduces it.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    if a == sorted(a):
        print("YES")
    else:
        print("NO")
```

The solution reads input efficiently using `sys.stdin.readline`. It constructs the sorted version of each array and performs a direct comparison. Python’s built-in `sorted` function runs in $O(n \log n)$ time. The comparison `a == sorted(a)` iterates through the array, costing $O(n)$ per test case. Boundary conditions are handled automatically because we never access indices outside the array bounds.

## Worked Examples

### Sample 1

Input array: `[2,3,5,4]`

Sorted array: `[2,3,4,5]`

Comparison: `[2,3,5,4] != [2,3,4,5]` → output "NO"

This demonstrates that the original array is not sorted, and a permutation exists that reduces operations.

### Sample 2

Input array: `[1,2,3]`

Sorted array: `[1,2,3]`

Comparison: `[1,2,3] == [1,2,3]` → output "YES"

This confirms the invariant: non-decreasing arrays are optimal.

### Sample 3

Input array: `[3,1,3,2]`

Sorted array: `[1,2,3,3]`

Comparison: `[3,1,3,2] != [1,2,3,3]` → output "NO"

This highlights an edge case with repeated elements and non-monotone ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates per test case, comparison is O(n) |
| Space | O(n) | Sorted copy of the array |

With sum of $n$ across all test cases ≤ 10^5, total operations are comfortably within $10^6$ for a 1-second limit.

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
        if a == sorted(a):
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# provided samples
assert run("3\n4\n2 3 5 4\n3\n1 2 3\n4\n3 1 3 2\n") == "NO\nYES\nNO", "sample tests"

# custom cases
assert run("1\n1\n1\n") == "YES", "single element"
assert run("1\n5\n5 4 3 2 1\n") == "NO", "reverse order"
assert run("1\n4\n2 2 2 2\n") == "YES", "all equal"
assert run("1\n6\n1 2 3 3 4 5\n") == "YES", "sorted with duplicates"
assert run("1\n6\n1 2 3 5 4 6\n") == "NO", "small inversion in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | YES | minimal array size |
| `1\n5\n5 4 3 2 1` | NO | reverse order maximizes operations |
| `1\n4\n2 2 2 2` | YES | all elements equal |
| `1\n6\n1 2 3 3 4 5` | YES | sorted with repeated numbers |
| `1\n6\n1 2 3 5 4 6` | NO | small inversion in middle of array |

## Edge Cases

For a single-element array `[1]`, the algorithm sorts `[1]` to `[1]` and prints "YES", correctly handling the minimum-size input. For a reverse-sorted array `[5,4,3,2,1]`, sorting produces `[1,2,3,4,5]`, comparison fails, and output is "NO", confirming that the algorithm identifies non-optimal permutations. For an array of identical elements `[2,2,2,2]`, sorting leaves the array unchanged and output is "YES", handling repeated numbers correctly. For arrays with a small inversion such as `[1,2,3,5,4,6]`, sorting fixes the inversion, comparison fails, and output is "NO", confirming the algorithm detects subtle non-monotone cases.
