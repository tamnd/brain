---
title: "CF 274A - k-Multiple Free Set"
description: "We are asked to find the largest subset of a given set of positive integers such that no element in the subset is exactly k times another element in the subset."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 274
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 168 (Div. 1)"
rating: 1500
weight: 274
solve_time_s: 74
verified: true
draft: false
---

[CF 274A - k-Multiple Free Set](https://codeforces.com/problemset/problem/274/A)

**Rating:** 1500  
**Tags:** binary search, greedy, sortings  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the largest subset of a given set of positive integers such that no element in the subset is exactly _k_ times another element in the subset. Formally, for a given integer _k_, we must ensure that for any two numbers _x_ and _y_ in the subset, the relationship _y_ = _x_·_k_ does not hold.

The input consists of a number of integers _n_ and the multiplier _k_, followed by _n_ distinct positive integers. The output is a single integer representing the maximum size of a subset that satisfies the k-multiple-free property.

The constraints indicate that _n_ can go up to 100,000 and each number as well as _k_ can be as large as 1,000,000,000. This implies that a brute-force approach checking every possible subset is infeasible, because there are exponentially many subsets. We need a solution that works in roughly linear or linearithmic time with respect to _n_.

Key edge cases to consider include inputs where the numbers form a geometric sequence with ratio _k_, because in that case careful selection is required to maximize the subset. Another important edge case is when _k_ = 1, because then any duplicate values cannot be in the same subset, even if the numbers themselves are distinct. We must also handle small sets like _n_ = 1.

## Approaches

A naive brute-force approach would attempt to generate all possible subsets of the input set and check for each subset whether any pair violates the k-multiple-free condition. This approach is correct in principle, because it examines all possible combinations. However, its time complexity is O(2^n) in the worst case, which is infeasible for n = 100,000.

The key insight to improve efficiency is to process the numbers in **sorted order**. By sorting the numbers ascendingly, we can greedily build the subset while ensuring the k-multiple-free property. For each number, we include it in our subset only if it is not a k-multiple of any previously included number. Using a hash set to track which numbers are included allows us to check the condition in constant time. This reduces the complexity to O(n log n) for sorting plus O(n) for the greedy selection, which is feasible under the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n·n^2) | O(n) | Too slow |
| Sorting + Greedy | O(n log n) | O(n) | Efficient and accepted |

## Algorithm Walkthrough

1. Sort the input array of integers in ascending order. Sorting allows us to process smaller numbers first and decide greedily whether to include them in the subset without violating the k-multiple-free condition.
2. Initialize an empty hash set `included` to keep track of numbers that are part of the k-multiple-free subset. This allows for O(1) lookup.
3. Initialize a counter `count` to 0, which will track the size of the valid subset.
4. Iterate through the sorted array. For each number `num`, check if `num` is divisible by _k_ and if `num // k` is already in `included`. If it is, skip `num` because including it would violate the k-multiple-free property. Otherwise, include `num` in `included` and increment `count`.
5. After processing all numbers, return `count`.

Why it works: Sorting ensures that we always consider smaller numbers first. This guarantees that when we check if `num // k` exists in the subset, we have already considered all smaller numbers. The invariant is that no two numbers in `included` will satisfy _y_ = _x_·_k_, so the final count is indeed the maximum possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

a.sort()
included = set()
count = 0

for num in a:
    if k != 1 and num % k == 0 and (num // k) in included:
        continue
    if k == 1 and num in included:
        continue
    included.add(num)
    count += 1

print(count)
```

This implementation sorts the array first, then greedily adds numbers to a set if they do not violate the k-multiple-free condition. We handle the edge case when k = 1 separately because division by k would always produce the number itself, so duplicates must be avoided. The counter keeps track of the number of elements included.

## Worked Examples

**Example 1:**

Input: `6 2` and `2 3 6 5 4 10`

After sorting: `[2, 3, 4, 5, 6, 10]`

`included = {}`

Iteration steps:

| num | num % k == 0? | num//k in included? | Action | included |
| --- | --- | --- | --- | --- |
| 2 | True | 1 not in included | Add | {2} |
| 3 | False | - | Add | {2,3} |
| 4 | True | 2 in included | Skip | {2,3} |
| 5 | False | - | Add | {2,3,5} |
| 6 | True | 3 in included | Skip | {2,3,5} |
| 10 | True | 5 in included | Skip | {2,3,5} |

Output: `3`

**Example 2:**

Input: `5 3` and `1 3 9 6 12`

After sorting: `[1, 3, 6, 9, 12]`

`included = {}`

| num | num % k == 0? | num//k in included? | Action | included |
| --- | --- | --- | --- | --- |
| 1 | False | - | Add | {1} |
| 3 | True | 1 in included | Skip | {1} |
| 6 | True | 2 not in included | Add | {1,6} |
| 9 | True | 3 not in included | Add | {1,6,9} |
| 12 | True | 4 not in included | Add | {1,6,9,12} |

Output: `4`

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates; iterating over it is O(n) |
| Space | O(n) | The `included` set can store up to n numbers |

The approach easily fits within the 2-second time limit for n ≤ 10^5.

## Test Cases

```python
# Sample and edge cases
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    included = set()
    count = 0
    for num in a:
        if k != 1 and num % k == 0 and (num // k) in included:
            continue
        if k == 1 and num in included:
            continue
        included.add(num)
        count += 1
    return str(count)

assert run("6 2\n2 3 6 5 4 10\n") == "3", "Sample 1"
assert run("5 3\n1 3 9 6 12\n") == "4", "Sample 2"
assert run("1 5\n10\n") == "1", "Single element"
assert run("5 1\n1 2 3 4 5\n") == "5", "k=1, no duplicates"
assert run("5 1\n1 1 2 2 3\n") == "3", "k=1, duplicates ignored"
assert run("6 2\n1 2 4 8 16 32\n") == "3", "Geometric progression"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 2\n2 3 6 5 4 10\n` | 3 | Basic sample input |
| `5 3\n1 3 9 6 12\n` | 4 | Mixed multiples |
| `1 5\n10\n` | 1 | Minimum-size input |
| `5 1\n1 2 3 4 5\n` | 5 | k = 1 with no duplicates |
| `5 1\n1 1 2 2 3\n` | 3 | k = 1 with duplicates |
| `6 2\n1 2 4 8 16 32\n` | 3 | Geometric progression |

## Edge Cases

The first edge case occurs when k = 1. Here, the naive approach of checking `num // k` would always refer to the number itself. Our implementation explicitly checks for duplicates in this scenario to avoid including the same value twice. For input `5 1\n1 1 2 2 3\n`, the algorithm correctly returns `3`.

The second edge case involves a geometric progression where each number is exactly k times the previous one, such as `1 2 4 8 16` with k = 2. The greedy
