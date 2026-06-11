---
title: "CF 1343C - Alternating Subsequence"
description: "We are given a sequence of integers, both positive and negative, and need to construct a subsequence whose elements strictly alternate in sign. Among all subsequences that achieve the maximum possible length, we are asked to find the one with the largest sum."
date: "2026-06-11T15:09:21+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1343
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 636 (Div. 3)"
rating: 1200
weight: 1343
solve_time_s: 79
verified: true
draft: false
---

[CF 1343C - Alternating Subsequence](https://codeforces.com/problemset/problem/1343/C)

**Rating:** 1200  
**Tags:** dp, greedy, two pointers  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, both positive and negative, and need to construct a subsequence whose elements strictly alternate in sign. Among all subsequences that achieve the maximum possible length, we are asked to find the one with the largest sum. The output for each test case is that sum.

Each test case provides the number of elements followed by the sequence itself. The constraints are substantial: the sum of all sequence lengths across test cases does not exceed 200,000, so any solution must run in linear time per test case. Quadratic solutions, such as checking every possible subsequence, are infeasible.

A subtle edge case arises when consecutive elements have the same sign. For example, if the input is `[1, 2, 3, -1, -2]`, the maximal alternating subsequence will pick the largest positive before switching to negative, then the largest negative before switching again. Simply alternating every element would fail to maximize the sum. Another tricky case occurs when all elements are of the same sign, such as `[-1, -2, -3]`, where the longest alternating subsequence has length one, and the correct answer is the largest element `-1`.

## Approaches

The brute-force approach is to generate all possible subsequences, check which alternate in sign, and select the one with the largest length and then maximum sum. This is correct but completely impractical: generating subsequences is O(2^n), and n can be up to 2 × 10^5.

The key observation that enables an efficient solution is that within a contiguous segment of numbers with the same sign, we only ever want the largest number. Including smaller numbers would reduce the sum without extending the length of the alternating subsequence. Therefore, the sequence can be compressed into "blocks" of consecutive numbers with the same sign, and for each block we select the maximum element. Once compressed, simply summing these maximum elements in alternating order achieves the optimal solution.

The optimal approach therefore works in linear time by iterating through the sequence, maintaining the maximum of the current sign block, and adding it to the total sum whenever a sign change occurs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `sum_total` to zero. This will store the sum of the chosen alternating subsequence.
2. Set `current_max` to the first element of the sequence. This tracks the largest element in the current sign block.
3. Iterate through the sequence from the second element. For each element:

1. If its sign matches `current_max`, update `current_max` to the larger of the two. This ensures we only keep the largest number in the current sign block.
2. If its sign differs, add `current_max` to `sum_total` and set `current_max` to this new element, starting a new sign block.
4. After the iteration, add the last `current_max` to `sum_total`. This handles the final block.
5. Print `sum_total`.

Why it works: the invariant is that at any point, `current_max` holds the maximum element of the current consecutive-sign block. Since alternating subsequences require switching sign for each element, choosing the largest in each block maximizes the sum without reducing the subsequence length. This guarantees that the result is the maximum sum for the maximum-length alternating subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    sum_total = 0
    current_max = a[0]
    
    for i in range(1, n):
        if (a[i] > 0) == (current_max > 0):
            current_max = max(current_max, a[i])
        else:
            sum_total += current_max
            current_max = a[i]
    
    sum_total += current_max
    print(sum_total)
```

Each part follows directly from the algorithm. `current_max` keeps the largest value of the current sign block. The comparison `(a[i] > 0) == (current_max > 0)` checks whether the current element has the same sign as the previous block. Adding `current_max` at the end ensures the last block is accounted for. This avoids off-by-one errors and works for sequences entirely positive or negative.

## Worked Examples

Sample Input 1:

```
5
1 2 3 -1 -2
```

| i | a[i] | current_max |_
