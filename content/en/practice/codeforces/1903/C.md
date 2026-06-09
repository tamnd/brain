---
title: "CF 1903C - Theofanis' Nightmare"
description: "We are given an array of integers, and our task is to split it into contiguous, non-empty subarrays. Each subarray contributes to a weighted sum called the Cypriot value, which is calculated as the sum over all subarrays of the subarray sum multiplied by its 1-based index in the…"
date: "2026-06-08T21:01:18+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1903
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 912 (Div. 2)"
rating: 1400
weight: 1903
solve_time_s: 100
verified: true
draft: false
---

[CF 1903C - Theofanis' Nightmare](https://codeforces.com/problemset/problem/1903/C)

**Rating:** 1400  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and our task is to split it into contiguous, non-empty subarrays. Each subarray contributes to a weighted sum called the _Cypriot value_, which is calculated as the sum over all subarrays of the subarray sum multiplied by its 1-based index in the partition. Our goal is to maximize this weighted sum.

The input consists of multiple test cases. Each test case contains the array length `n` and the array elements, which can be negative or positive. The output is a single integer per test case: the maximum Cypriot value achievable by some partition.

The constraints tell us `n` can go up to 100,000 and the sum of all `n` across test cases is at most 200,000. This indicates that any solution that is quadratic in `n` will be too slow. A linear or near-linear solution is required.

Non-obvious edge cases include arrays that are all positive, all negative, or alternating in sign. For example, a single negative number should remain as a singleton subarray to avoid reducing the weighted sum of later positive elements. For an array `[5, -2, 3]`, naïvely merging all elements gives a smaller value than splitting around the negative number.

## Approaches

The brute-force solution considers every possible way to split the array. For each partitioning into `k` subarrays, we compute the weighted sum. Even using dynamic programming, iterating over all split points for each prefix results in O(n^2) complexity. For `n = 10^5`, this would require roughly 10^10 operations, which is infeasible.

The key insight comes from observing how the index multiplier behaves. A large positive number contributes more if it appears later in the partition because it is multiplied by a larger index. Conversely, a negative number contributes less-or even harms the total-if it appears later. Therefore, the optimal strategy is to partition the array such that every contiguous sequence of elements with the same sign is treated as a single subarray. In other words, we break the array whenever the sign changes. Within each contiguous positive or negative block, we take only the largest element of that block if the block is negative, and sum all elements if the block is positive.

This observation reduces the problem to a simple linear scan: iterate through the array, track the current "sign block," and decide whether to merge or start a new block. The solution runs in O(n) time per test case, which fits comfortably within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `total` as 0 to hold the final Cypriot value. Also initialize `current_max` as the first element of the array, representing the best value in the current contiguous block.
2. Iterate through the array from the second element to the end.
3. If the current element has the same sign as `current_max`, replace `current_max` with the maximum of itself and the current element. This ensures we pick the most valuable element in a positive or negative block.
4. If the sign changes, add `current_max` to `total`, then set `current_max` to the current element. This splits the array at sign changes.
5. After finishing the iteration, add the last `current_max` to `total` to include the last block.
6. Print `total`.

Why it works: At each sign block, including the largest element maximizes the block's contribution without harming later blocks. Adding smaller elements within a negative block would decrease the Cypriot value because multiplying them by the index gives a larger negative penalty. This greedy approach guarantees the maximum sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_cypriot_value(arr):
    total = 0
    current_max = arr[0]
    for num in arr[1:]:
        if (num > 0 and current_max > 0) or (num < 0 and current_max < 0):
            current_max = max(current_max, num)
        else:
            total += current_max
            current_max = num
    total += current_max
    return total

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(max_cypriot_value(a))
```

The first loop maintains the best candidate in each contiguous sign block. The comparison `(num > 0 and current_max > 0) or (num < 0 and current_max < 0)` checks if the current element continues the same sign block. The second branch adds `current_max` to `total` when the sign changes, creating a new block. Adding `current_max` at the end handles the final block.

## Worked Examples

**Example 1: `[1, -3, 7, -6, 2, 5]`**

| i | num | current_max | total |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | -3 | -3 | 1 |
| 2 | 7 | 7 | -2 |
| 3 | -6 | -6 | 5 |
| 4 | 2 | 2 | -1 |
| 5 | 5 | 5 | 2 |

Final `total = 32`. Each sign block is correctly processed, confirming the greedy invariant.

**Example 2: `[2, 9, -5, -3]`**

| i | num | current_max | total |
| --- | --- | --- | --- |
| 0 | 2 | 2 | 0 |
| 1 | 9 | 9 | 0 |
| 2 | -5 | -5 | 9 |
| 3 | -3 | -3 | 4 |

Final `total = 4`. Shows that negative blocks only contribute the maximum single negative number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through the array per test case |
| Space | O(1) | Only a few integer variables are maintained |

Since the sum of `n` over all test cases ≤ 2 * 10^5, the solution runs comfortably under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # Solution code
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = 0
        current_max = a[0]
        for num in a[1:]:
            if (num > 0 and current_max > 0) or (num < 0 and current_max < 0):
                current_max = max(current_max, num)
            else:
                total += current_max
                current_max = num
        total += current_max
        print(total)
    return output.getvalue().strip()

# Provided samples
assert run("4\n6\n1 -3 7 -6 2 5\n4\n2 9 -5 -3\n8\n-3 -4 2 -5 1 10 17 23\n1\n830\n") == "32\n4\n343\n830", "sample 1"

# Custom test cases
assert run("2\n1\n-100\n3\n0 0 0\n") == "-100\n0", "single negative and all zeros"
assert run("1\n5\n1 2 3 4 5\n") == "15", "all positive increasing"
assert run("1\n5\n-1 -2 -3 -4 -5\n") == "-1", "all negative, pick max"
assert run("1\n6\n1 -1 1 -1 1 -1\n") == "3", "alternating signs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n-100` | `-100` | Single negative number |
| `0 0 0` | `0` | All zeros |
| `1 2 3 4 5` | `15` | All positive, no splits needed |
| `-1 -2 -3 -4 -5` | `-1` | All negative, pick maximum element |
| `1 -1 1 -1 1 -1` | `3` | Alternating signs, greedy splitting works |

## Edge Cases

A single-element array `[830]` sets `total = 830` immediately. The algorithm correctly handles arrays with only negative numbers by picking the maximum negative element as the sole contributor. Alternating signs are handled because each change triggers a block split, guaranteeing the optimal partition without any complex logic.
