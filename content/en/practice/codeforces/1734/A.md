---
title: "CF 1734A - Select Three Sticks"
description: "We are given a collection of sticks, each with a positive integer length. Our goal is to adjust the lengths using the minimum number of operations so that three of them can form an equilateral triangle."
date: "2026-06-09T18:18:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1734
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 822 (Div. 2)"
rating: 800
weight: 1734
solve_time_s: 145
verified: true
draft: false
---

[CF 1734A - Select Three Sticks](https://codeforces.com/problemset/problem/1734/A)

**Rating:** 800  
**Tags:** brute force, greedy, sortings  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of sticks, each with a positive integer length. Our goal is to adjust the lengths using the minimum number of operations so that three of them can form an equilateral triangle. An operation is either increasing or decreasing a stick’s length by exactly one unit, and no stick can have length zero or less after an operation.

The input consists of multiple test cases. Each test case provides the number of sticks and their lengths. The output is the minimum number of operations required to ensure that some triplet of sticks can be made equal, which is equivalent to forming an equilateral triangle.

Looking at the constraints, we have up to 300 sticks in total across all test cases. This is small enough to consider solutions that are quadratic in the number of sticks per test case. The stick lengths themselves can be very large (up to $10^9$), so any solution that tries to iterate over all possible lengths explicitly will be infeasible. The challenge lies not in iterating over sticks but in calculating differences efficiently.

Non-obvious edge cases include situations where the sticks are already equal, where the minimal number of operations requires bringing the middle stick to match the extremes, or where the three closest lengths are consecutive numbers. For instance, given sticks `[1, 2, 3]`, the optimal equilateral triangle has side length `2` with two operations: increase `1` to `2` and decrease `3` to `2`. A careless solution might try to always pick the smallest or largest stick as the target, which would produce suboptimal answers.

## Approaches

The brute-force approach would be to consider every possible triplet of sticks, compute the minimum number of operations needed to equalize them, and take the minimum among all triplets. With up to 300 sticks per test case, there are $\binom{300}{3} \approx 4.5 \times 10^6$ triplets. For each triplet, we would need a few arithmetic operations, which is technically feasible given the constraints, but unnecessarily slow and cumbersome.

The key insight is to sort the sticks. Once sorted, the closest three sticks will always give the optimal solution because equalizing sticks that are far apart will cost more operations than equalizing nearby lengths. After sorting, we only need to consider each group of three consecutive sticks. For any triplet `(x, y, z)` with `x ≤ y ≤ z`, the minimal operations to make all three equal is `abs(y-x) + abs(z-y)`. This formula arises because moving `y` to match `x` or `z` is never better than moving each stick towards the median. Sorting reduces the problem from cubic to linear scanning after sorting, which is much faster.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow for n=300 |
| Sorting + Sliding Triplet | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n` and the array of stick lengths.
3. Sort the array in non-decreasing order. Sorting ensures that the minimal adjustments are always found among consecutive sticks.
4. Initialize a variable `min_ops` to infinity. This will track the minimum number of operations for this test case.
5. Iterate over the array from index `0` to `n-3`. For each index `i`, consider the triplet `(a[i], a[i+1], a[i+2])`.
6. Compute the number of operations needed to make the triplet equal: `a[i+2] - a[i]`. This is because the minimal moves to equalize three numbers is achieved by making them all equal to the median, which in a sorted triplet is always `a[i+1]`. Moving `a[i]` and `a[i+2]` to `a[i+1]` costs `(a[i+1]-a[i]) + (a[i+2]-a[i+1]) = a[i+2]-a[i]`.
7. Update `min_ops` if this value is smaller.
8. After scanning all triplets, output `min_ops`.

Why it works: Sorting guarantees that we consider the smallest spread between three sticks. Using the median minimizes the sum of absolute differences. By iterating through consecutive triplets, we ensure that we do not miss a smaller number of operations, because any triplet with a larger spread would require strictly more operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    min_ops = float('inf')
    for i in range(n - 2):
        ops = a[i+2] - a[i]
        if ops < min_ops:
            min_ops = ops
    print(min_ops)
```

The solution first reads the number of test cases and iterates through them. Sorting is done for each array to line up sticks for minimal adjustment. The key subtlety is realizing that `a[i+2] - a[i]` is enough; attempting to move all sticks to either extreme would be suboptimal. Boundary handling (`n-2`) ensures no out-of-range errors.

## Worked Examples

**Example 1:**

Input: `[1, 2, 3]` (sorted already)

| i | Triplet | ops = a[i+2]-a[i] | min_ops |
| --- | --- | --- | --- |
| 0 | (1,2,3) | 2 | 2 |

Output: `2`. This matches the minimal operations by moving `1 → 2` and `3 → 2`.

**Example 2:**

Input: `[7, 3, 7, 3]` → sorted `[3, 3, 7, 7]`

| i | Triplet | ops | min_ops |
| --- | --- | --- | --- |
| 0 | (3,3,7) | 4 | 4 |
| 1 | (3,7,7) | 4 | 4 |

Output: `4`. The minimal adjustment comes from equalizing `(3,3,7)` by moving `3 → 7` and `7 → 7`.

These examples show that the algorithm correctly picks the minimal spread among consecutive sticks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates; scanning triplets is linear |
| Space | O(n) | Storage of the array for each test case |

With `n` up to 300 per test case and sum of `n` ≤ 300, this fits well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n1 2 3\n4\n7 3 7 3\n5\n3 4 2 1 1\n8\n3 1 4 1 5 9 2 6\n") == "2\n4\n1\n1", "sample 1"

# Custom cases
assert run("1\n3\n5 5 5\n") == "0", "all equal sticks"
assert run("1\n3\n1 1 10\n") == "9", "one long stick"
assert run("1\n4\n1 2 2 3\n") == "1", "multiple minimal triplets"
assert run("1\n5\n1 2 3 4 5\n") == "2", "consecutive numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 5 5 5` | `0` | Already equilateral, zero operations |
| `3 1 1 10` | `9` | One extreme stick, needs large adjustment |
| `4 1 2 2 3` | `1` | Multiple candidate triplets |
| `5 1 2 3 4 5` | `2` | Closest triplets minimize operations |

## Edge Cases

For `[1, 2, 3]`, the algorithm selects `(1,2,3)` and calculates `3-1=2`. Moving `1 → 2` and `3 → 2` achieves the equilateral triangle, showing that the method correctly targets the median, not an extreme. For `[1, 1, 10]`, the triplet `(1,1,10)` yields `10-1=9`, correctly indicating the number of moves to bring all sticks to `1` or `10`. The sorted scan ensures no better combination is missed.
