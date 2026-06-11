---
title: "CF 1348B - Phoenix and Beauty"
description: "Phoenix has an array of integers ranging from 1 to $n$, and he wants it to be \"beautiful.\" A beautiful array is one where every consecutive block of $k$ elements sums to the same value."
date: "2026-06-11T14:48:06+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1348
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 638 (Div. 2)"
rating: 1400
weight: 1348
solve_time_s: 165
verified: false
draft: false
---

[CF 1348B - Phoenix and Beauty](https://codeforces.com/problemset/problem/1348/B)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy, sortings  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

Phoenix has an array of integers ranging from 1 to $n$, and he wants it to be "beautiful." A beautiful array is one where every consecutive block of $k$ elements sums to the same value. The task is to determine whether it's possible to insert additional numbers (also between 1 and $n$) into the array so that it becomes beautiful, and if so, produce one such array. We do not need to minimize the number of insertions, only ensure the resulting array is valid and does not exceed a length of $10^4$.

The input provides multiple test cases. Each test case gives the current array and the subarray length $k$. We must output either $-1$ if it is impossible, or a constructed array of length $m$ that meets the beautiful array criteria.

Constraints are small: $n \le 100$ and $t \le 50$, which means any solution with complexity roughly $O(n^2)$ per test case will run comfortably in the time limit. However, the array construction may require replicating a sequence to reach up to $10^4$, so we need a method that can repeat elements efficiently.

Edge cases include situations where $k = n$, in which case the entire array itself must form a single sum block, and when $k = 1$, where any array is automatically beautiful. Another subtle case occurs when the array has more distinct elements than $k$ - this may make it impossible to form a repeating block that satisfies the subarray sum constraint.

For example, given $a = [1, 2, 3]$ and $k = 2$, there is no way to insert elements to make all consecutive pairs sum to the same value because there are three distinct numbers and only pairs of size 2, so we would need more than 2 distinct numbers in a repeating pattern.

## Approaches

A brute-force approach might attempt to consider all possible insertions and all possible values for those insertions, checking if the resulting array is beautiful. This would involve generating all sequences up to length $10^4$, which is clearly infeasible. Even with $n \le 100$, the number of possibilities grows combinatorially because each position can be filled with any number from 1 to $n$.

The key insight is that to satisfy the beautiful array property, the array can be constructed as repetitions of a block containing all distinct numbers present in the original array. If the number of distinct elements in the original array exceeds $k$, there is no block of length $k$ that can capture all distinct elements, so the array cannot be made beautiful. If the number of distinct elements is at most $k$, we can construct a block of length exactly $k$ by adding arbitrary numbers (within bounds) to fill the block, then repeat this block enough times to cover the original array. This guarantees that every subarray of length $k$ will have the same sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * n^k) | O(n^2) | Too slow |
| Optimal | O(n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and $k$ and the array $a$.
2. Identify the distinct elements in $a$. If the number of distinct elements exceeds $k$, output $-1$ because it is impossible to create a repeating block of length $k$ that contains all distinct elements.
3. Otherwise, construct a block of length $k$ by taking all distinct elements and appending arbitrary elements (1 is convenient) until the block length reaches $k$. This block ensures that every subarray of length $k$ contains all original distinct elements.
4. Repeat this block enough times to cover the original array $a$. The repetition can be done as many times as necessary to reach a length not exceeding $10^4$. The final length $m$ can be chosen as $k \times \text{ceil}(n / k)$ and then repeat the block until $m \le 10^4$.
5. Print $m$ and the resulting array.

Why it works: By repeating a fixed block of length $k$ containing all distinct elements, every consecutive subarray of length $k$ is identical to the block, which ensures all subarrays of length $k$ have the same sum. This satisfies the beautiful array property.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = lis
```
