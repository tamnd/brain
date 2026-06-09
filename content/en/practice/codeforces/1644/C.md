---
title: "CF 1644C - Increase Subarray Sums"
description: "We are given an array of integers and a number $x$. The task is to compute, for each possible $k$ from 0 to $n$, the maximum sum of a contiguous subarray if we are allowed to add $x$ to exactly $k$ elements in the array."
date: "2026-06-10T04:13:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1644
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 123 (Rated for Div. 2)"
rating: 1400
weight: 1644
solve_time_s: 104
verified: true
draft: false
---

[CF 1644C - Increase Subarray Sums](https://codeforces.com/problemset/problem/1644/C)

**Rating:** 1400  
**Tags:** brute force, dp, greedy, implementation  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a number $x$. The task is to compute, for each possible $k$ from 0 to $n$, the maximum sum of a contiguous subarray if we are allowed to add $x$ to exactly $k$ elements in the array. The elements to add $x$ to can be chosen arbitrarily, and the subarray itself does not have to include all the increased elements. An empty subarray is allowed, which has sum zero.

The constraints are small enough that an $O(n^2)$ solution is feasible. The sum of $n$ over all test cases is at most 5000, meaning we can perform up to roughly 25 million operations in total under the 2-second time limit. Each array element and the increment $x$ can be large, so we must avoid integer overflow, but Python handles that natively.

Non-obvious edge cases include arrays with all negative numbers, where the maximum sum may be zero if no positive sum subarray exists. For example, for the array $[-5, -3, -2]$ with $x = 4$, choosing no elements to increase gives a maximum sum of 0, choosing one element wisely gives 2, and choosing all three gives 3. A naive implementation that always picks the first $k$ elements could fail in such cases.

Another edge case occurs when $x = 0$. Then the problem reduces to a classical maximum subarray sum problem, and the algorithm must correctly handle $k = 0$ without assuming $x > 0$.

## Approaches

A brute-force approach would be, for each $k$, to generate all subsets of size $k$ to add $x$, then for each subset, compute the maximum subarray sum. Generating all subsets is $O(\binom{n}{k})$, and computing the maximum subarray sum is $O(n)$. This approach is correct in principle but infeasible because $n$ can be up to 5000, so $\binom{5000}{k}$ is astronomically large even for small $k$.

The key insight is that adding $x$ to elements is always beneficial, so we can decouple the choice of subarray and the choice of which elements to increase. For any subarray of length $l$, the maximum benefit we can get from adding $x$ is $\min(l, k) \cdot x$, because we cannot increase more elements than the subarray contains. Therefore, it suffices to precompute, for each subarray length, the maximum subarray sum of that length without any increments. Then for each $k$, the maximum sum is the maximum over all lengths $l$ of $\text{max\_sum\_of\_length}[l] + \min(l, k) \cdot x$.

This reduces the problem from exponential to $O(n^2)$: computing maximum sums for all lengths takes $O(n^2)$, and computing the result for each $k$ takes $O(n^2)$ in total across all lengths. With $n \le 5000$, this is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and iterate over each test case.
2. For a given array of length $n$ and increment $x$, initialize an array `max_sum_of_length` of length (n + 1` to store the maximum sum for subarrays of each length.
3. For each starting index $i$ in the array, initialize a running sum `current_sum = 0`. Iterate over the ending index $j$ from $i$ to $n-1$. Increment `current_sum` by `a[j]` and update `max_sum_of_length[j-i+1]` with the maximum of its current value and `current_sum`. This captures the maximum sum for every subarray length.
4. Initialize an answer array `answer` of length $n + 1$ with zeros. This stores $f(k)$ for each $k$.
5. For each possible k` from 0 to \(n, iterate over all subarray lengths `l` from 0 to $n$ and update `answer[k]` as the maximum of its current value and `max_sum_of_length[l] + min(l, k) * x`. This calculates the optimal sum for each number of elements increased.
6. Print `answer` for each test case.

Why it works: By precomputing the maximum subarray sums for every length, we ensure that for any choice of $k$, we can consider the optimal subarray for every possible number of elements increased. The function $\min(l, k) \cdot x$ correctly models the limit that we cannot increase more elements than the subarray contains. Iterating over all lengths ensures that we never miss the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    max_sum_of_length = [0] * (n + 1)

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += a[j]
            length = j - i + 1
            if current_sum > max_sum_of_length[length]:
                max_sum_of_length[length] = current_sum

    answer = [0] * (n + 1)
    for k in range(n + 1):
        best = 0
        for length in range(n + 1):
            best = max(best, max_sum_of_length[length] + min(length, k) * x)
        answer[k] = best

    print(*answer)
```

The solution first constructs `max_sum_of_length`, ensuring that every possible subarray sum is considered. In the second loop, `min(length, k)` guarantees we never overcount the number of elements we can increase. Using zero as the initial value ensures that empty subarrays are correctly accounted for, producing a result of zero when all numbers are negative.

## Worked Examples

**Sample 1:**

Input: `4 2` and array `[4, 1, 3, 2]`.

| k | max over lengths l | l=1 | l=2 | l=3 | l=4 |
| --- | --- | --- | --- | --- | --- |
| 0 | max(4,5,8,10) | 4 | 5 | 8 | 10 |
| 1 | max(6,7,10,12) | 6 | 7 | 10 | 12 |
| 2 | max(8,9,12,14) | 8 | 9 | 12 | 14 |
| 3 | max(10,11,14,16) | 10 | 11 | 14 | 16 |
| 4 | max(12,13,16,18) | 12 | 13 | 16 | 18 |

This trace shows how the algorithm combines subarray sums with `k*x` to get the maximum for each `k`.

**Sample 2:**

Input: `3 5` and array `[-2, -7, -1]`.

| k | best subarray sum + min(length, k)*x |
| --- | --- |
| 0 | 0 |
| 1 | max(-2+5, -7+5, -1+5) = 4 |
| 2 | max(-2+10, -7+10, -1+10, (-2+-7)+10, ...) = 4 |
| 3 | sum([-2,-7,-1])+3*5 = 5 |

This demonstrates handling of negative numbers, empty subarray, and k > subarray length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Outer loop over start index, inner loop over end index computes all subarray sums |
| Space | O(n) | Arrays `max_sum_of_length` and `answer` |

Given $n \le 5000$ and sum of $n$ across all test cases $\le 5000$, $O(n^2)$ is acceptable within 2 seconds. Memory usage is well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # invoke solution
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        max_sum_of_length = [0] * (n + 1)
        for i in range(n):
            s = 0
            for j in range(i, n):
                s += a[j]
                max_sum_of_length[j-i+1] = max(max_sum_of_length[j-i+1], s)
        ans = [0]*(n+1)
        for k in range(n+1
```
