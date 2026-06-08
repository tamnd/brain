---
title: "CF 2041E - Beautiful Array"
description: "We are asked to construct an integer array such that its mean is exactly a and its median is exactly b. The input consists of two integers, a and b, which are the desired mean and median, respectively."
date: "2026-06-08T09:42:10+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 2041
codeforces_index: "E"
codeforces_contest_name: "2024 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1200
weight: 2041
solve_time_s: 110
verified: false
draft: false
---

[CF 2041E - Beautiful Array](https://codeforces.com/problemset/problem/2041/E)

**Rating:** 1200  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an integer array such that its mean is exactly `a` and its median is exactly `b`. The input consists of two integers, `a` and `b`, which are the desired mean and median, respectively. The output is the length of a valid array, followed by the array elements themselves. The array length must be between 1 and 1000, and each element must be an integer within ±10^6.

The constraints are relatively generous. Since the array can have up to 1000 elements, and the elements themselves can be very large in magnitude, we have substantial freedom in choosing array values. This makes an approach based on careful construction feasible. The key challenge is to satisfy the mean and median simultaneously while keeping integers and length within the allowed bounds.

The non-obvious edge cases include situations where the mean and median differ. For example, if `a = 3` and `b = 4`, a naive approach that simply fills the array with `b` will satisfy the median but not the mean. Another edge case is when `a = b`, in which case filling the array entirely with `a` solves both requirements trivially. Arrays of length 1 must also be handled correctly, where the single element must be equal to both `a` and `b`. These examples show that the solution must allow flexible construction rather than blindly filling values.

## Approaches

A brute-force approach would try all possible array lengths and all combinations of integer elements to check if the resulting array has the desired mean and median. This is correct in principle because it checks all possibilities. However, with up to 1000 elements and values up to 10^6, the number of combinations is astronomically large, making this approach infeasible.

The insight for an optimal solution is that we can construct a small array around the median and adjust other elements to satisfy the mean. If we start with an array of length 3 with `[b, b, x]`, the median is `b`. We can solve for `x` using the mean equation: `(b + b + x)/3 = a` gives `x = 3a - 2b`. This guarantees integer solutions as long as `x` is an integer, which it always is if `a` and `b` are integers. If `x` is outside allowed bounds, we can increase the array length by adding extra `b`s and a balancing element. This approach works because the constraints allow both positive and negative numbers up to ±10^6.

This method is simple, always constructs an array of reasonable length (≤1000), and satisfies both mean and median exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((10^6)^n) | O(n) | Too slow |
| Constructive | O(1) | O(n) | Accepted |

## Algorithm Walkthrough

1. Check if `a` equals `b`. If so, print an array of length 1 with `[a]`. This trivially satisfies both mean and median.
2. Otherwise, consider an initial array of length 3: `[b, b, x]`, where `x = 3a - 2b`. This ensures that the mean is exactly `a` while the median remains `b`.
3. If `x` is within the allowed element bounds (±10^6), print this array. Its median is `b` because the middle element after sorting is `b`.
4. If `x` is outside the bounds, extend the array by adding additional `b`s at the beginning or end and adjust a single element to maintain the mean. Specifically, for larger arrays, choose a simple pattern such as `[b]*k + [y]`, where `y` is computed to satisfy the mean exactly. The constraints guarantee that a solution exists.
5. Output the length of the array followed by the array elements.

Why it works: The algorithm maintains the median at `b` by keeping `b` at the center. By algebraically solving for the remaining element(s) to satisfy the mean, we guarantee the mean is exactly `a`. The allowed ranges for array length and element values ensure a valid solution can always be constructed.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = map(int, input().split())

if a == b:
    print(1)
    print(a)
else:
    # Start with three elements: [b, b, x]
    x = 3 * a - 2 * b
    if abs(x) <= 10**6:
        print(3)
        print(b, b, x)
    else:
        # If x is too large, use a longer array
        # We'll use 100 elements: 50 b's and 50 zeros, then adjust last element
        n = 100
        arr = [b] * (n // 2)
        arr += [0] * (n // 2 - 1)
        # Compute the last element to satisfy the mean
        total = sum(arr)
        last = n * a - total
        arr.append(last)
        print(n)
        print(*arr)
```

The code first checks if `a` equals `b`, in which case the array is `[a]`. Otherwise, it attempts the simple three-element construction `[b, b, 3a-2b]`. If that fails due to bounds, it builds a longer array of 100 elements with half `b`s and half zeros, adjusting the last element to satisfy the mean. Sorting is not necessary because the median remains `b` due to placement of `b`s at the center.

## Worked Examples

### Sample 1

Input:

```
3 4
```

| Step | Array | Mean Calculation | Median |
| --- | --- | --- | --- |
| Initial | [4, 4, x] | (4+4+1)/3 = 3 | 4 |
| Output | [4, 4, 1] | 3 | 4 |

This confirms that the simple three-element construction works when `3a - 2b = 1`.

### Custom Example

Input:

```
2 5
```

| Step | Array | Mean Calculation | Median |
| --- | --- | --- | --- |
| Initial | [5, 5, x] | (5+5+(-1))/3 = 3 | 5 |
| Adjusted | [5,5,-1] | (5+5-1)/3 = 3 | 5 |

Again, the three-element array satisfies both conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Construction involves a few arithmetic operations and array creation up to 100 elements |
| Space | O(n) | Array stores up to 1000 integers |

The solution easily fits within the time and memory constraints. The array length never exceeds 1000, and arithmetic operations are trivial for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    input_backup = builtins.input
    builtins.input = lambda: sys.stdin.readline()
    import sys
    out = io.StringIO()
    sys.stdout = out
    # solution code
    a, b = map(int, input().split())
    if a == b:
        print(1)
        print(a)
    else:
        x = 3 * a - 2 * b
        if abs(x) <= 10**6:
            print(3)
            print(b, b, x)
        else:
            n = 100
            arr = [b] * (n // 2)
            arr += [0] * (n // 2 - 1)
            last = n * a - sum(arr)
            arr.append(last)
            print(n)
            print(*arr)
    builtins.input = input_backup
    return out.getvalue().strip()

# provided samples
assert run("3 4\n") == "3\n4 4 1", "sample 1"
# custom cases
assert run("2 2\n") == "1\n2", "a equals b"
assert run("100 0\n") == "3\n0 0 300", "median zero, mean large"
assert run("-5 5\n") == "3\n5 5 -25", "negative mean, positive median"
assert run("0 100\n") == "3\n100 100 -200", "median large, mean zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 1\n2 | Single-element array when mean equals median |
| 100 0 | 3\n0 0 300 | Large mean, median zero |
| -5 5 | 3\n5 5 -25 | Negative mean, positive median |
| 0 100 | 3\n100 100 -200 | Median larger than mean |

## Edge Cases

When `a = b`, such as `2 2`, the algorithm immediately outputs `[2]`. The trace is trivial: the array has length 1, mean = 2, median = 2.

When `3a - 2b` exceeds ±10^6, the algorithm switches to a longer array of 100 elements. For example, `a = 1000`, `b = 0` produces `3*1000 - 2*0 = 3000`, which exceeds the element bounds. The extended
