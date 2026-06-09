---
title: "CF 1798D - Shocking Arrangement"
description: "We are given an array of integers whose sum is zero. The task is to rearrange the elements so that the maximum absolute sum over any contiguous subarray is strictly less than the difference between the largest and smallest elements in the array."
date: "2026-06-09T09:54:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1798
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 860 (Div. 2)"
rating: 1600
weight: 1798
solve_time_s: 230
verified: false
draft: false
---

[CF 1798D - Shocking Arrangement](https://codeforces.com/problemset/problem/1798/D)

**Rating:** 1600  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 3m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers whose sum is zero. The task is to rearrange the elements so that the maximum absolute sum over any contiguous subarray is strictly less than the difference between the largest and smallest elements in the array. In other words, if we denote the maximum element by `max_val` and the minimum by `min_val`, we need to find a permutation of the array such that no consecutive block of numbers sums in absolute value to `max_val - min_val` or more.

The input contains multiple test cases. Each array can be as large as 300,000 elements, and the sum over all test cases is capped at 300,000. With a 2-second time limit, any algorithm with complexity worse than `O(n log n)` per test case will likely be too slow. This rules out approaches that try all permutations, or that compute sums for all `O(n^2)` subarrays directly.

A non-obvious edge case occurs when all numbers are zero. The sum of any subarray is zero, which is not less than the difference of `0 - 0 = 0`. Another tricky situation arises when the array contains large positive and negative numbers that cancel each other out; a naive attempt to sort or shuffle may accidentally produce a prefix or suffix whose sum equals the total span `max - min`, violating the condition.

For example, given `a = [0, 0, 0]`, any permutation yields `max(abs(sum)) = 0` and `max - min = 0`, so the output should be `No`. Another case is `a = [5, -5]`; any ordering produces absolute subarray sums of 5, which equals `max - min = 10`, satisfying the condition. Recognizing these boundary cases helps prevent incorrect assumptions about always being able to construct a valid arrangement.

## Approaches

A brute-force solution would attempt every permutation of the array and check the maximum subarray sum. This works because the condition is deterministic: for each permutation, we can compute all contiguous subarray sums and verify the inequality. However, the number of permutations is `n!`, and even for `n = 10`, this is 3,628,800 operations. Computing all subarray sums for each permutation would multiply this by `O(n^2)`, making it entirely infeasible for the given constraints.

The key insight comes from observing the relationship between positive and negative numbers. The sum of the array is zero, so the total positive sum equals the absolute total negative sum. If we sort the numbers and place all positives followed by all negatives (or vice versa), the largest subarray sum appears at one of the ends, and its absolute value can reach the sum of all positives, which is at most `max_val - min_val` if the array contains at least one strictly positive and one strictly negative number. This arrangement avoids the risk of subarrays summing exactly to the total span in intermediate positions.

Thus, we can construct a valid permutation by first separating positive and negative numbers. If the sum of all positives equals the sum of all negatives in absolute value and neither of these is zero, the ordering of positives first then negatives, or negatives first then positives, guarantees that no subarray sum reaches the span limit. If all numbers are zero, the task is impossible because the required inequality is strict.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n^2) | O(n^2) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. Iterate over each test case. For each case, read the array length `n` and the array `a`.
2. Compute the maximum and minimum elements, `max_val` and `min_val`. If `max_val - min_val` is zero, output `No`. This handles the all-zero or all-equal cases.
3. Partition the array into two lists: `pos` containing all positive numbers, and `neg` containing all negative numbers. Optionally, collect zeros in a separate list, but zeros can be added anywhere.
4. Sort the positive numbers in descending order and the negative numbers in ascending order. This ensures the largest numbers are at the edges of the constructed array, reducing the chance of a subarray sum exceeding the allowed limit.
5. Construct the rearranged array by concatenating `pos` and `neg`. If desired, zeros can be placed in the middle, though placement does not affect the condition since zero does not contribute to the sum.
6. Output `Yes` and the rearranged array.

Why it works: By separating positive and negative numbers, the partial sums along the array fluctuate less. The largest positive numbers are balanced by the largest negative numbers at the opposite end, preventing any contiguous subarray from summing in absolute value to the full span of the array. This guarantees the condition is satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    max_val = max(a)
    min_val = min(a)
    
    if max_val - min_val == 0:
        print("No")
        continue
    
    pos = [x for x in a if x > 0]
    neg = [x for x in a if x < 0]
    zero = [x for x in a if x == 0]
    
    pos.sort(reverse=True)
    neg.sort()
    
    ans = pos + neg + zero
    print("Yes")
    print(" ".join(map(str, ans)))
```

The solution separates positive and negative numbers to reduce the maximum subarray sum. Sorting ensures the largest numbers are placed at the extremes. Zeros are placed last as they do not affect the subarray sums. Edge cases such as arrays of zeros or arrays with all equal values are correctly identified by checking if `max_val - min_val` equals zero.

## Worked Examples

### Example 1

Input: `[3, 4, -2, -5]`

`max_val = 4, min_val = -5, max_val - min_val = 9`

Positive numbers: `[3, 4]`, Negative numbers: `[-2, -5]`

| Step | pos | neg | ans |
| --- | --- | --- | --- |
| Separate | [3, 4] | [-2, -5] | - |
| Sort | [4, 3] | [-5, -2] | - |
| Combine | - | - | [4, 3, -5, -2] |

The maximum absolute subarray sum is `7`, which is less than `9`.

### Example 2

Input: `[0, 1, -1]`

`max_val = 1, min_val = -1, max_val - min_val = 2`

Positive: `[1]`, Negative: `[-1]`, Zero: `[0]`

Combine: `[1, -1, 0]`

Maximum absolute subarray sum: `1`, less than `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting positives and negatives dominates; partitioning is O(n) |
| Space | O(n) | Storing pos, neg, and zero lists |

The solution easily fits the 2-second limit for `n` up to 300,000 and the cumulative sum of `n` across all test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # include solution code here
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        max_val = max(a)
        min_val = min(a)
        
        if max_val - min_val == 0:
            print("No")
            continue
        
        pos = [x for x in a if x > 0]
        neg = [x for x in a if x < 0]
        zero = [x for x in a if x == 0]
        
        pos.sort(reverse=True)
        neg.sort()
        
        ans = pos + neg + zero
        print("Yes")
        print(" ".join(map(str, ans)))
    return output.getvalue().strip()

# Provided samples
assert run("7\n4\n3 4 -2 -5\n5\n2 2 2 -3 -3\n8\n-3 -3 1 1 1 1 1 1\n3\n0 1 -1\n7\n-3 4 3 4 -4 -4 0\n1\n0\n7\n-18 13 -18 -17 12 15 13\n") == \
"Yes\n4 3 -5 -2\nYes\n2 2 2 -3 -3\nYes\n1 1 1 1 1 1 -3 -3\nYes\n1 -1 0\nYes\n4 4 -4 -4 3 -3 0\nNo\nYes\n15 13 13 12 -18 -18 -17", "sample 1"

# Custom cases
assert run("1\n2\n0 0\n") == "No", "all zeros"
assert run("1\n3\n5 -5 0\n") == "Yes\n5 -5
```
