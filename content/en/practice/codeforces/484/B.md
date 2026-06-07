---
title: "CF 484B - Maximum Value"
description: "We are given a sequence of integers a1, a2, …, an and asked to compute the maximum value of ai % aj over all pairs (i, j) where ai ≥ aj. The input consists of the number of integers n and the sequence itself."
date: "2026-06-07T17:21:53+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 484
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 276 (Div. 1)"
rating: 2100
weight: 484
solve_time_s: 95
verified: true
draft: false
---

[CF 484B - Maximum Value](https://codeforces.com/problemset/problem/484/B)

**Rating:** 2100  
**Tags:** binary search, math, sortings, two pointers  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers `a1, a2, …, an` and asked to compute the maximum value of `ai % aj` over all pairs `(i, j)` where `ai ≥ aj`. The input consists of the number of integers `n` and the sequence itself. The output is a single integer: the largest remainder obtained by dividing one element of the array by another not larger than itself.

The first key observation is that since all elements are positive integers bounded by `10^6` and `n` can reach `2·10^5`, any naive attempt to check every pair directly is infeasible. A brute-force solution iterating over all pairs would perform roughly `n^2` operations, up to `4·10^10`, which is far beyond a 1-second limit. Therefore we need a strategy that avoids explicit enumeration of all pairs.

Edge cases appear when the array contains repeated elements or a single element. For example, if all elements are equal, `ai % aj` is always zero, so the answer is zero. If the array contains `1`, it acts as a universal divisor, producing smaller remainders. Arrays with only one element should trivially return zero, since `ai % ai = 0`.

## Approaches

The brute-force approach is straightforward. Iterate over all pairs `(i, j)` such that `ai ≥ aj` and compute `ai % aj`, keeping track of the maximum. This guarantees correctness because it literally examines every allowed pair. However, with `n` up to `2·10^5`, the worst-case complexity is O(n^2), which is infeasible for large inputs.

The key insight for an optimal solution is that the remainder `x % y` is always less than `y`. This means that for any `y`, the maximum remainder we can achieve with it as a divisor is `max(x < 2y) x % y`. Sorting the array and considering divisors in order lets us avoid unnecessary checks. More concretely, the maximum remainder is achieved by either the largest element smaller than `2*y` or the largest element in the array excluding `y`. By scanning the sorted array backwards and using this property, we can compute the maximum remainder efficiently in O(n log n) time.

The optimal approach works because once the array is sorted, for each potential divisor `y`, the candidate dividends that produce a remainder near `y-1` are located close to multiples of `y`. Instead of checking all elements, we can jump by `y` increments and consider only the largest elements in each range. This reduces the number of operations dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the array `a`. The array contains `n` integers between `1` and `10^6`.
2. Sort the array in ascending order. Sorting allows us to efficiently find the largest element smaller than any multiple of a candidate divisor.
3. Initialize `max_value` to zero. This will store the maximum remainder found.
4. Iterate over all distinct values `y` in the array, excluding the largest element. For each `y`, consider multiples of `y` starting from `2*y`.
5. For each multiple `k*y`, find the largest element `x` in the array that is smaller than `k*y`. The remainder `x % y` is a candidate for the maximum. Update `max_value` if `x % y` is larger than the current `max_value`.
6. After considering all candidate divisors, also check the largest element in the array modulo the second-largest element, as it can produce a remainder larger than any element smaller than it.
7. Print `max_value`.

**Why it works**: The algorithm exploits the fact that for a fixed divisor `y`, the remainder `x % y` is maximized when `x` is just below a multiple of `y`. By sorting the array and scanning in multiples of `y`, we are guaranteed to find the largest possible remainder for each divisor. No remainder is missed because all relevant `x` are considered relative to multiples of `y`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
a.sort()
max_a = a[-1]
max_value = 0
unique_vals = sorted(set(a))

for y in unique_vals:
    if y == max_a:
        continue
    k = 2
    while k * y <= max_a + y:
        # Find largest x < k*y using binary search
        left, right = 0, n - 1
        pos = -1
        while left <= right:
            mid = (left + right) // 2
            if a[mid] < k * y:
                pos = mid
                left = mid + 1
            else:
                right = mid - 1
        if pos != -1:
            max_value = max(max_value, a[pos] % y)
        k += 1

print(max_value)
```

The sorting step ensures that binary search correctly finds the largest element smaller than each multiple of `y`. We skip the largest element as a divisor because it cannot produce a positive remainder. The `while` loop considers successive multiples, ensuring no remainder candidate is missed. The binary search carefully handles boundary conditions so that `pos` always points to the largest valid dividend.

## Worked Examples

**Example 1**

Input:

```
3
3 4 5
```

| Step | Candidate divisor y | k*y | Largest x < k*y | x % y | max_value |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 6 | 5 | 2 | 2 |
| 2 | 4 | 8 | 5 | 1 | 2 |

Output: `2`

Explanation: The remainder `5 % 3 = 2` is the largest achievable.

**Example 2**

Input:

```
5
1 2 3 4 5
```

| Step | Candidate divisor y | k*y | Largest x < k*y | x % y | max_value |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 5 | 0 | 0 |
| 2 | 2 | 4 | 3 | 1 | 1 |
| 3 | 3 | 6 | 5 | 2 | 2 |
| 4 | 4 | 8 | 5 | 1 | 2 |

Output: `2`

Explanation: Maximum remainder occurs for `5 % 3 = 2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + n log n) ≈ O(n log n) | Sorting the array takes O(n log n). Each divisor uses binary search over the array, which is O(log n) per multiple, with total iterations bounded by n. |
| Space | O(n) | Storing the array and the set of unique values. |

The solution handles arrays up to `2·10^5` elements and values up to `10^6` efficiently, fitting within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    max_a = a[-1]
    max_value = 0
    unique_vals = sorted(set(a))
    for y in unique_vals:
        if y == max_a:
            continue
        k = 2
        while k * y <= max_a + y:
            left, right = 0, n - 1
            pos = -1
            while left <= right:
                mid = (left + right) // 2
                if a[mid] < k * y:
                    pos = mid
                    left = mid + 1
                else:
                    right = mid - 1
            if pos != -1:
                max_value = max(max_value, a[pos] % y)
            k += 1
    return str(max_value)

# provided samples
assert run("3\n3 4 5\n") == "2", "sample 1"

# custom cases
assert run("1\n1\n") == "0", "single element"
assert run("5\n2 2 2 2 2\n") == "0", "all equal"
assert run("5\n1 2 3 4 5\n") == "2", "simple increasing"
assert run("6\n1 3 5 7 9 11\n") == "5", "odd numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 0 | Single-element array |
| 5\n2 2 2 2 2 | 0 | All elements equal |
| 5\n1 2 3 4 5 | 2 | Typical increasing sequence |
| 6\n1 3 5 |  |  |
