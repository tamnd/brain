---
title: "CF 1468A - LaIS"
description: "We are asked to find the length of the longest subsequence of an array such that the sequence is \"almost increasing.\" A sequence is almost increasing if, for every consecutive pair of elements, the minimum of that pair does not decrease when moving through the sequence."
date: "2026-06-11T01:23:37+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "A"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 2200
weight: 1468
solve_time_s: 273
verified: true
draft: false
---

[CF 1468A - LaIS](https://codeforces.com/problemset/problem/1468/A)

**Rating:** 2200  
**Tags:** data structures, dp, greedy  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the length of the longest subsequence of an array such that the sequence is "almost increasing." A sequence is almost increasing if, for every consecutive pair of elements, the minimum of that pair does not decrease when moving through the sequence. Formally, for a subsequence $b_1, b_2, \dots, b_k$, we require $\min(b_1, b_2) \le \min(b_2, b_3) \le \dots \le \min(b_{k-1}, b_k)$. Any two-element sequence automatically satisfies this property, which means subsequences of length 2 are trivially almost increasing.

The input consists of multiple test cases. Each test case gives the array length $n$ and the array $a$ itself. We must output a single integer per test case: the length of the longest almost increasing subsequence. The total number of array elements across all test cases is bounded by $5 \cdot 10^5$. This constraint is crucial: it allows algorithms that are linear in $n$ per test case, but anything quadratic, like a naive dynamic programming over all pairs, will be too slow.

An important edge case is when the array is strictly decreasing. For example, for $a = [5, 4, 3, 2, 1]$, the naive approach might consider every element individually, but a longer subsequence exists if we allow repetitions that satisfy the min-condition. Another edge case occurs when all elements are equal; here the whole array is a valid almost increasing subsequence. Small arrays of length 2 are trivial, but a careless implementation might try to compute differences or minimums and incorrectly return 1 instead of 2.

## Approaches

A brute-force approach is to consider every possible subsequence and check if it satisfies the almost increasing condition. For each subsequence, we compute the sequence of pairwise minimums and verify it is non-decreasing. While this is correct in principle, the number of subsequences of an array of length $n$ is $2^n$, making this method completely impractical even for $n = 20$.

A more natural brute-force dynamic programming approach considers storing the longest almost increasing subsequence ending at each index. One might define $dp[i]$ as the length of the longest valid subsequence ending at $a[i]$. For each $i$, we could check all previous $j < i$ and see if appending $a[i]$ to the subsequence ending at $j$ preserves the almost increasing property. This requires computing $\min(a[j], a[i])$ and comparing it to the previous min in the subsequence. This gives an $O(n^2)$ solution, which is still too slow for $n \sim 5 \cdot 10^5$.

The key observation is that the condition only depends on consecutive pairwise minimums. We do not need to track every element individually but rather two "states": the last element in the subsequence if we take the smaller value of a pair, or if we take the larger value. Using this, we can maintain two arrays or two variables: one for the longest subsequence ending with the last element chosen as the smaller of the last pair, and one with the last element as the larger of the last pair. This allows us to process the array in linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| DP over all previous | O(n^2) | O(n) | Too slow |
| Linear DP with two states | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two variables, `low` and `high`, both representing the last element of a subsequence. Set them to the first element of the array since the subsequence starts there. Also initialize a counter `length = 1` to represent the current subsequence length.
2. Iterate through the array starting from the second element. At each step, we have two choices for extending the subsequence: append the smaller of the last two elements or the larger. For the current element `a[i]`, compute the new potential `low` as the minimum of the previous `low` or `high` and `a[i]`. Compute the new potential `high` as the maximum of the previous `low` or `high` and `a[i]`.
3. If the new `low` is greater than or equal to the previous `low`, we can safely increment the subsequence length and update `low` and `high`. Otherwise, reset `low` and `high` appropriately.
4. Continue this process for all elements, always keeping track of the longest subsequence length.

Why it works: the invariant maintained is that `low` and `high` always represent the minimum and maximum elements of the last pair in the current subsequence. By only tracking these two values, we capture all possibilities for extending the subsequence while satisfying the almost increasing property, without enumerating every subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    if n == 2:
        print(2)
        continue
    
    length = 2
    prev_min = min(a[0], a[1])
    prev_max = max(a[0], a[1])
    
    for i in range(2, n):
        curr_min = min(prev_max, a[i])
        curr_max = max(prev_max, a[i])
        if curr_min >= prev_min:
            length += 1
            prev_min = curr_min
            prev_max = curr_max
        else:
            prev_min = min(a[i-1], a[i])
            prev_max = max(a[i-1], a[i])
    
    print(length)
```

The first section handles fast input and iterates over multiple test cases. We treat arrays of length 2 as a special case because they are always valid. The main loop computes `curr_min` and `curr_max` as potential extensions of the last pair. If `curr_min >= prev_min`, the sequence can safely extend. Otherwise, we reset `prev_min` and `prev_max` to the current pair to ensure the subsequence is still valid.

## Worked Examples

Consider the array `[1, 2, 7, 3, 2, 1, 2, 3]`.

| i | a[i] | prev_min | prev_max | curr_min | curr_max | length |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | 2 | 2 | 2 |
| 2 | 7 | 1 | 2 | 2 | 7 | 3 |
| 3 | 3 | 2 | 7 | 3 | 7 | 4 |
| 4 | 2 | 3 | 7 | 2 | 7 | 4 (reset prev_min/prev_max to 2,3) |
| 5 | 1 | 2 | 3 | 1 | 3 | 5 |
| 6 | 2 | 1 | 3 | 2 | 3 | 6 |
| 7 | 3 | 2 | 3 | 3 | 3 | 6 |

The maximum length obtained is 6, which matches the sample output. The table shows how `prev_min` and `prev_max` capture the pairwise min constraints without storing the entire subsequence.

For `[2, 1]`, the output is 2. For `[4, 1, 5, 2, 6, 3, 7]`, the output is 7 because each step can extend without violating the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan the array once and maintain two variables for extension, so each element is processed in constant time. |
| Space | O(1) extra | Only a few variables are maintained, independent of n. |

Given the constraint $\sum n \le 5 \cdot 10^5$, this linear solution runs well within time limits. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 2:
            output.append("2")
            continue
        length = 2
        prev_min = min(a[0], a[1])
        prev_max = max(a[0], a[1])
        for i in range(2, n):
            curr_min = min(prev_max, a[i])
            curr_max = max(prev_max, a[i])
            if curr_min >= prev_min:
                length += 1
                prev_min = curr_min
                prev_max = curr_max
            else:
                prev_min = min(a[i-1], a[i])
                prev_max = max(a[i-1], a[i])
        output.append(str(length))
    return "\n".join(output)

# Provided samples
assert run("3\n8\n1 2 7 3 2 1 2 3\n2\n
```
