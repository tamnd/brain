---
title: "CF 914A - Perfect Squares"
description: "We are given an array of integers and need to find the largest element that is not a perfect square. A perfect square is a number that can be expressed as the square of an integer. The input consists of a number n, the size of the array, followed by the array elements."
date: "2026-06-13T01:24:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 914
codeforces_index: "A"
codeforces_contest_name: "Codecraft-18 and Codeforces Round 458 (Div. 1 + Div. 2, combined)"
rating: 900
weight: 914
solve_time_s: 278
verified: true
draft: false
---

[CF 914A - Perfect Squares](https://codeforces.com/problemset/problem/914/A)

**Rating:** 900  
**Tags:** brute force, implementation, math  
**Solve time:** 4m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and need to find the largest element that is **not a perfect square**. A perfect square is a number that can be expressed as the square of an integer. The input consists of a number _n_, the size of the array, followed by the array elements. The output is a single integer: the largest element in the array which is not a perfect square.

The constraints are modest: _n_ can be up to 1000, and elements can range from -10^6 to 10^6. The negative numbers can never be perfect squares, so we immediately know they are candidates. The upper bound on _n_ means we can check each number individually in linear time without performance issues. The range of numbers also allows us to compute square roots safely with integer arithmetic.

An edge case arises when the array contains a mix of large perfect squares and smaller non-square numbers. For instance, the input `5\n1 4 9 16 2` has only 2 as the largest non-square. A naive approach that simply picks the largest number without checking for squares would return 16, which is incorrect. Negative numbers and zero require care: zero is a perfect square, and negative numbers are never perfect squares.

## Approaches

The brute-force approach is straightforward. We iterate through each element of the array and check if it is a perfect square. If it is not, we keep track of the maximum value seen so far. Checking if a number is a perfect square can be done by taking the integer square root and squaring it back to see if it equals the original number. Since there are at most 1000 elements, each requiring a constant-time square root check, the total operation count is around 1000, which is negligible. Therefore, brute force is acceptable in practice, though for larger arrays it could become inefficient.

The key insight is that we do not need to sort the array or store additional data structures. A single linear pass is enough. For each element, we compute the integer square root using the `math.isqrt` function, square it back, and compare with the original number. If they are unequal, the number is not a perfect square, and we compare it with the current maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

Since the optimal approach and brute force are effectively the same in this problem, the focus is on correctly identifying non-squares.

## Algorithm Walkthrough

1. Initialize a variable `best` to negative infinity. This will store the largest non-square found so far.
2. Iterate through each element `x` of the array.
3. If `x` is negative, it cannot be a perfect square. Compare it with `best` and update `best` if `x` is larger.
4. If `x` is non-negative, compute `y = int(sqrt(x))` using `math.isqrt(x)`. Check if `y * y == x`. If not, `x` is not a perfect square.
5. If `x` is not a perfect square, compare it with `best` and update `best` if `x` is larger.
6. After processing all elements, output `best`.

**Why it works:** At each step, we maintain the invariant that `best` is the largest number seen so far that is not a perfect square. Because we examine every element and correctly identify perfect squares, the final value of `best` is guaranteed to be the largest non-square.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

best = -float('inf')
for x in a:
    if x < 0:
        best = max(best, x)
    else:
        y = math.isqrt(x)
        if y * y != x:
            best = max(best, x)

print(best)
```

The solution first reads input efficiently using `sys.stdin.readline`. We initialize `best` to negative infinity to handle negative numbers correctly. For each element, negative numbers are automatically candidates. Non-negative numbers are tested for being perfect squares using integer square roots to avoid floating-point inaccuracies. Finally, `best` contains the largest non-square.

## Worked Examples

**Example 1**

Input:

```
2
4 2
```

| Step | x | is perfect square? | best |
| --- | --- | --- | --- |
| 1 | 4 | yes | -inf |
| 2 | 2 | no | 2 |

Output: `2`. This confirms the algorithm correctly ignores perfect squares and selects the largest non-square.

**Example 2**

Input:

```
5
1 4 9 16 2
```

| Step | x | is perfect square? | best |
| --- | --- | --- | --- |
| 1 | 1 | yes | -inf |
| 2 | 4 | yes | -inf |
| 3 | 9 | yes | -inf |
| 4 | 16 | yes | -inf |
| 5 | 2 | no | 2 |

Output: `2`. This demonstrates the algorithm correctly handles multiple squares and identifies the maximum non-square.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the n elements is checked once; `math.isqrt` is O(1) |
| Space | O(1) | Only a single variable `best` is used besides input storage |

With n ≤ 1000, this algorithm runs in well under 1 millisecond, far below the 1-second limit, and uses negligible memory.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    best = -float('inf')
    for x in a:
        if x < 0:
            best = max(best, x)
        else:
            y = math.isqrt(x)
            if y * y != x:
                best = max(best, x)
    return str(best)

# provided samples
assert run("2\n4 2\n") == "2", "sample 1"

# custom cases
assert run("5\n1 4 9 16 2\n") == "2", "all squares except one"
assert run("3\n-1 0 1\n") == "-1", "negative numbers handled"
assert run("4\n2 3 5 7\n") == "7", "all non-squares"
assert run("1\n0\n") == "-inf", "single element, square zero"  # would never happen due to guarantee
assert run("6\n-100 -36 0 1 2 3\n") == "3", "mixed negative and positive"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5\n1 4 9 16 2` | 2 | correctly ignores multiple perfect squares |
| `3\n-1 0 1` | -1 | handles negative numbers correctly |
| `4\n2 3 5 7` | 7 | largest non-square chosen among all non-squares |
| `6\n-100 -36 0 1 2 3` | 3 | mixed negatives, zeros, and squares |

## Edge Cases

For the input `-1 0 1`, `best` starts at negative infinity. `-1` is negative, so `best` becomes -1. `0` is a perfect square, skipped. `1` is a perfect square, skipped. Output is -1, which is correct. The algorithm never misclassifies negatives or zero.

For the input `2 3 5 7`, all numbers are non-squares. The algorithm updates `best` at each step, ending with 7. This confirms that sequences with no squares are handled naturally.

This confirms that the solution correctly identifies the largest non-square across all edge scenarios.
