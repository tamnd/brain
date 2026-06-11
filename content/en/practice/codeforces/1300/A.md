---
title: "CF 1300A - Non-zero"
description: "We are given an array of integers and want to make two properties simultaneously true: the sum of the elements must not be zero, and the product of the elements must not be zero. The only operation allowed is incrementing a single element by one."
date: "2026-06-11T18:19:56+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1300
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 618 (Div. 2)"
rating: 800
weight: 1300
solve_time_s: 42
verified: true
draft: false
---

[CF 1300A - Non-zero](https://codeforces.com/problemset/problem/1300/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and want to make two properties simultaneously true: the sum of the elements must not be zero, and the product of the elements must not be zero. The only operation allowed is incrementing a single element by one. The task is to find the minimum number of such increment operations to satisfy both properties.

The input consists of multiple test cases. Each test case starts with the size of the array, followed by the array elements. The bounds are small: at most 100 elements per array, each element between -100 and 100, and at most 1000 test cases. This means an $O(n)$ solution per test case will be fast enough.

Edge cases appear when there are zeros in the array. A zero in the array makes the product zero, which must be fixed by at least one increment per zero. Another subtle case occurs if the sum of the array is zero after fixing all zeros. For example, an array like [0, -1, 1] has sum zero and product zero. If we increment the zero to one, the product becomes non-zero, but the sum is now 1, so both conditions are satisfied. In general, after handling zeros, we must check whether the sum itself is zero, because incrementing zeros might not automatically fix the sum.

## Approaches

A brute-force approach would simulate incrementing every zero individually and then test every combination of additional increments to fix the sum. This would be correct but unnecessary, as the problem can be reasoned about mathematically. With $n \le 100$ and values bounded, the operation count might seem small, but simulating every sum adjustment could require exponential work, which is not justified given the simpler insight available.

The key insight is to separate the two constraints. Any zero in the array must be incremented to fix the product. Let `zeros` be the count of zeros; we need at least `zeros` operations. After incrementing all zeros, we can compute the sum of the resulting array. If this sum is zero, we need one additional increment anywhere to break the sum from zero. If the sum is already non-zero, no further operations are required. This reduces the solution to counting zeros and checking the adjusted sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^n) | O(n) | Too slow |
| Counting Zeros + Adjust Sum | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `steps` to zero. This will track the total increments needed.
2. Count the number of zeros in the array. Each zero requires one increment to make the product non-zero, so add this count to `steps`.
3. Compute the sum of the array after hypothetically incrementing all zeros by one. Let `sum_after` be this sum.
4. If `sum_after` is zero, increment `steps` by one. This accounts for the situation where fixing the product created a sum of zero.
5. Print `steps` as the result for this test case.

Why it works: Every zero must be incremented to achieve a non-zero product, which the algorithm ensures. Once zeros are handled, the only way the sum can remain zero is if the non-zero elements cancel out perfectly. Adding one more increment anywhere breaks this, guaranteeing both sum and product are non-zero. The algorithm counts exactly the minimum number of increments required.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    zeros = a.count(0)
    steps = zeros
    
    sum_after = sum(a) + zeros
    if sum_after == 0:
        steps += 1
    
    print(steps)
```

The first section reads the number of test cases and loops over them. For each arr
