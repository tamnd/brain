---
title: "CF 39B - Company Income Growth"
description: "We are given a sequence of integers representing the yearly income of a company starting from 2001. The first number is the income in 2001, the second in 2002, and so on. These values may be negative if the company incurred a loss that year."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "B"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 1300
weight: 39
solve_time_s: 207
verified: true
draft: false
---
[CF 39B - Company Income Growth](https://codeforces.com/problemset/problem/39/B)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers representing the yearly income of a company starting from 2001. The first number is the income in 2001, the second in 2002, and so on. These values may be negative if the company incurred a loss that year. Petya wants to present a "perfect" growth scenario in which the income grows linearly by 1 billion each year: 1 billion in the first year, 2 billion in the second year, 3 billion in the third, and so on. Since the real incomes may not follow this perfect pattern, he wants to extract a subsequence of years whose income exactly matches 1, 2, 3, … in order.

Our goal is to select the longest such subsequence. We then output its length and the corresponding years (2000 + year index).

The input constraint is small: `n` is at most 100. This means an algorithm with O(n^2) operations is feasible because even 10,000 operations are trivial for modern processors under a 2-second limit. The incomes can be negative, so a naive approach that stops at the first mismatch would fail. We also need to handle the possibility that no year matches the perfect growth at all, in which case the answer is 0.

Non-obvious edge cases include sequences where multiple matching years exist for the same target value. For example, in `[1, 1, 2, 2, 3]`, the perfect sequence could take either the first 1 or the second 1. Another edge case is when all numbers are negative, e.g., `[-1, -2, -3]`, producing an output of 0. A careless approach might return indices without checking the actual value against the expected perfect growth.

## Approaches

The brute-force approach is to try every subsequence of the income array, checking whether its elements form the perfect growth. Since the number of subsequences of length k is combinatorial, the total operation count grows exponentially, roughly O(2^n). For `n = 100`, this is completely infeasible.

The key insight is that this problem is equivalent to finding the longest subsequence that matches a given increasing sequence `1, 2, 3, …`. This is exactly a variation of the Longest Increasing Subsequence (LIS) problem, but instead of arbitrary comparisons, each element must match a specific expected value. Because `n` is small, a dynamic programming approach works efficiently.

We iterate through the array while maintaining a DP array where `dp[i]` is the length of the longest perfect sequence ending at position `i`. For each position, we check all previous positions to see if we can extend the sequence. This reduces the problem from exponential to O(n^2), which is acceptable given the constraints. We also store a `prev` array to reconstruct the actual sequence of years.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Dynamic Programming | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `dp` of length `n` with zeros. `dp[i]` will store the length of the longest perfect subsequence ending at index `i`.
2. Initialize an array `prev` of length `n` with `-1` to store the previous index in the sequence for reconstruction.
3. Loop over the array using index `i` from 0 to n-1. For each element `a[i]`, calculate its target value in the perfect sequence as `dp[i] + 1`. If `a[i]` equals `dp[i] + 1` and it can extend any previous subsequence, update `dp[i]` to `dp[j] + 1` for some `j < i` where `dp[j]` is maximized, and record `prev[i] = j`. If no previous element can extend it, set `dp[i] = 1`.
4. After filling `dp`, find the index `max_index` with the largest `dp[max_index]`. This gives the length of the longest perfect sequence.
5. Reconstruct the sequence by following the `prev` array from `max_index` backwards. Convert each array index to the actual year by adding 2001.
6. Print the length of the sequence and the reconstructed years. If no element ever matched the perfect growth, output 0.

Why it works: At each step, `dp[i]` accurately represents the longest perfect sequence ending at `i` because it only considers valid extensions. The `prev` array ensures we can reconstruct the subsequence in order. The algorithm systematically considers all possibilities for ending a perfect sequence at each position, so it cannot miss the longest one.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

dp = [0] * n
prev = [-1] * n

for i in range(n):
    if a[i] == 1:
        dp[i] = 1
    for j in range(i):
        if dp[j] > 0 and a[i] == dp[j] + 1:
            if dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

# Find the index of the maximum length
max_len = 0
max_index = -1
for i in range(n):
    if dp[i] > max_len:
        max_len = dp[i]
        max_index = i

if max_len == 0:
    print(0)
else:
    sequence = []
    idx = max_index
    while idx != -1:
        sequence.append(2001 + idx)
        idx = prev[idx]
    sequence.reverse()
    print(max_len)
    print(*sequence)
```

We first initialize `dp` and `prev` to track the longest sequences and their reconstruction paths. We loop over every pair `(j, i)` with `j < i` to check if we can extend a sequence. This is where careful handling of the expected perfect growth is crucial; without `a[i] == dp[j] + 1`, the subsequence would be invalid. The final reconstruction uses `prev` to build the sequence backward and then reverses it for chronological order.

## Worked Examples

**Sample 1:**

Input:

```
10
-2 1 1 3 2 3 4 -10 -2 5
```

| i | a[i] | dp[i] | prev[i] |
| --- | --- | --- | --- |
| 0 | -2 | 0 | -1 |
| 1 | 1 | 1 | -1 |
| 2 | 1 | 1 | -1 |
| 3 | 3 | 0 | -1 |
| 4 | 2 | 2 | 1 |
| 5 | 3 | 3 | 4 |
| 6 | 4 | 4 | 5 |
| 7 | -10 | 0 | -1 |
| 8 | -2 | 0 | -1 |
| 9 | 5 | 5 | 6 |

Sequence reconstructed: 2002, 2005, 2006, 2007, 2010

This demonstrates that the algorithm correctly tracks subsequences and skips irrelevant years.

**Custom Input:**

```
5
-1 -2 -3 -4 -5
```

All `dp[i]` remain 0, so output is 0. This confirms the edge case of no valid years is handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Two nested loops over n elements, feasible for n ≤ 100 |
| Space | O(n) | Two arrays `dp` and `prev` of size n, plus the reconstructed sequence |

The algorithm fits well within the constraints: 10,000 operations in a 2-second window is trivial, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    dp = [0] * n
    prev = [-1] * n
    for i in range(n):
        if a[i] == 1:
            dp[i] = 1
        for j in range(i):
            if dp[j] > 0 and a[i] == dp[j] + 1:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = j
    max_len = 0
    max_index = -1
    for i in range(n):
        if dp[i] > max_len:
            max_len = dp[i]
            max_index = i
    if max_len == 0:
        return "0"
    sequence = []
    idx = max_index
    while idx != -1:
        sequence.append(2001 + idx)
        idx = prev
```
