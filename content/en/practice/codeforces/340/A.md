---
title: "CF 340A - The Wall"
description: "We are asked to count the number of bricks that get painted by both Iahub and Floyd in a specific range. The bricks are numbered with consecutive integers starting from 1."
date: "2026-06-06T17:15:38+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 340
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 198 (Div. 2)"
rating: 1200
weight: 340
solve_time_s: 80
verified: true
draft: false
---

[CF 340A - The Wall](https://codeforces.com/problemset/problem/340/A)

**Rating:** 1200  
**Tags:** math  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of bricks that get painted by both Iahub and Floyd in a specific range. The bricks are numbered with consecutive integers starting from 1. Iahub paints every _x_-th brick, starting from brick _x_, while Floyd paints every _y_-th brick, starting from brick _y_. We are interested only in bricks numbered between _a_ and _b_, inclusive, that are painted by both.

The input consists of four integers: _x_, _y_, _a_, and _b_. The output is a single integer representing the count of bricks painted by both.

The constraints tell us that _x_ and _y_ are at most 1000, so any algorithm using these as direct step sizes is feasible. The range [_a_, _b_] can go up to 2·10⁹, which makes a brute-force simulation over the entire interval impractical. A naive loop over every brick in [_a_, _b_] would require potentially 2·10⁹ iterations, which is far beyond 1-second execution time.

An edge case arises when _a_ is smaller than both _x_ and _y_. For example, if _x_ = 5, _y_ = 7, _a_ = 1, _b_ = 10, we must correctly include the first multiple of 5 and 7 that falls in [1, 10]. Careless floor division or rounding might exclude it. Another edge case is when _a_ equals _b_, such as _x_ = 3, _y_ = 3, _a_ = 6, _b_ = 6. The algorithm must correctly count a single brick if it is painted by both.

## Approaches

The brute-force approach is simple to describe. We iterate over every brick numbered from _a_ to _b_. For each brick, we check if it is divisible by both _x_ and _y_. If it is, we increment a counter. This is correct because a brick is painted by both if and only if its number is divisible by both step sizes. The problem with this approach is the worst case: if _b - a_ is on the order of 2·10⁹, the loop performs billions of iterations, which is far too slow.

The key insight for an optimal solution is that a brick is painted by both if and only if it is a multiple of the least common multiple (LCM) of _x_ and _y_. Once we know the LCM, say _z_, the problem reduces to counting multiples of _z_ in the interval [_a_, _b_]. This can be done mathematically without iterating over each brick. To count multiples of _z_ in a range, we compute the number of multiples up to _b_, subtract the number of multiples strictly less than _a_, and the difference gives the count in [_a_, _b_]. This approach avoids any per-brick simulation and runs in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(b - a + 1) | O(1) | Too slow for large b-a |
| Optimal | O(log(max(x, y))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the greatest common divisor (GCD) of _x_ and _y_. This is necessary to calculate the LCM efficiently. Using the formula `LCM(x, y) = x * y // GCD(x, y)` ensures we avoid integer overflow by dividing before multiplying.
2. Compute the LCM of _x_ and _y_, which we call _z_. A brick is painted by both painters if and only if its number is a multiple of _z_.
3. Count how many multiples of _z_ are less than or equal to _b_. This is done by `b // z`.
4. Count how many multiples of _z_ are strictly less than _a_. This is done by `(a - 1) // z`. Subtracting these two counts gives the number of multiples of _z_ within [_a_, _b_].
5. Print the result.

The invariant is that every multiple of _z_ in the interval [_a_, _b_] is counted exactly once. No other numbers in the interval are multiples of both _x_ and _y_, so the count is exact. The algorithm never needs to examine individual bricks, making it efficient even for very large ranges.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

x, y, a, b = map(int, input().split())

def lcm(u, v):
    return u * v // gcd(u, v)

z = lcm(x, y)
count = b // z - (a - 1) // z
print(count)
```

The first part reads the input and imports the `gcd` function from Python's math library. The `lcm` function computes the least common multiple efficiently. The calculation `b // z - (a - 1) // z` counts multiples of `z` in the desired range, taking care to include _a_ if it itself is a multiple. The subtraction `(a - 1) // z` ensures we do not undercount when _a_ is itself a multiple.

## Worked Examples

**Sample 1**

Input: 2 3 6 18

| Step | z (LCM) | Multiples ≤ b | Multiples < a | Count |
| --- | --- | --- | --- | --- |
| Compute z | 6 | 3 | 0 | 3 |

Multiples of 6 in [6, 18] are 6, 12, 18. The algorithm correctly counts 3.

**Sample 2**

Input: 5 7 1 10

| Step | z (LCM) | Multiples ≤ b | Multiples < a | Count |
| --- | --- | --- | --- | --- |
| Compute z | 35 | 0 | 0 | 0 |

No brick numbered 1 to 10 is a multiple of both 5 and 7. Count is 0.

These traces demonstrate the method works both when the range contains multiples and when it contains none.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(x, y))) | GCD computation dominates, which is logarithmic in smaller of x or y |
| Space | O(1) | Only a few integer variables are used |

Given the constraints, this method executes in constant time for the input limits, easily under 1 second and within memory limits.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, y, a, b = map(int, input().split())
    z = x * y // gcd(x, y)
    return str(b // z - (a - 1) // z)

# Provided sample
assert run("2 3 6 18\n") == "3", "sample 1"

# Custom cases
assert run("5 7 1 10\n") == "0", "no overlap"
assert run("3 3 6 6\n") == "1", "single brick"
assert run("1 1 1 1000000000\n") == "1000000000", "every brick"
assert run("2 3 1 1\n") == "0", "range below first multiple"
assert run("2 3 1 6\n") == "1", "include first multiple only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 7 1 10 | 0 | No brick painted by both in the range |
| 3 3 6 6 | 1 | Single brick equal to a multiple |
| 1 1 1 1000000000 | 1000000000 | All bricks painted by both |
| 2 3 1 1 | 0 | Range below first multiple |
| 2 3 1 6 | 1 | Include first multiple at boundary |

## Edge Cases

When the range starts below the first multiple, the subtraction `(a - 1) // z` ensures no undercounting. For example, x = 2, y = 3, a = 1, b = 5, z = 6. Multiples ≤ b = 0, multiples < a = 0, count = 0. If _a_ itself is a multiple, like a = 6, b = 6, then multiples ≤ b = 1, multiples < a = 0, count = 1, correctly including the brick. The algorithm naturally handles ranges of length 1, ranges starting at multiples, and large ranges, thanks to the arithmetic counting method.
