---
title: "CF 1768A - Greatest Convex"
description: "The problem asks us to find the largest integer x less than a given integer k such that the sum of x! and (x-1)! is divisible by k. In plain language, we want a number just below k where adding its factorial to the factorial of the previous number gives a multiple of k."
date: "2026-06-09T12:42:24+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1768
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 842 (Div. 2)"
rating: 800
weight: 1768
solve_time_s: 105
verified: true
draft: false
---

[CF 1768A - Greatest Convex](https://codeforces.com/problemset/problem/1768/A)

**Rating:** 800  
**Tags:** greedy, math, number theory  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to find the largest integer `x` less than a given integer `k` such that the sum of `x!` and `(x-1)!` is divisible by `k`. In plain language, we want a number just below `k` where adding its factorial to the factorial of the previous number gives a multiple of `k`. Each test case is a single integer `k`, and we need to output the corresponding `x` or `-1` if no such number exists.

Looking at the constraints, `k` can be as large as a billion, and we may have up to ten thousand test cases. This means any solution that explicitly computes factorials for numbers approaching `k` is completely infeasible. Factorials grow extremely fast, and `100!` already exceeds `10^157`, far beyond standard integer operations in practice. Therefore, an approach that tries to compute factorials directly for large `k` will not work.

A subtle edge case arises with very small values of `k`. For example, if `k = 3`, the largest `x` is `2` because `2! + 1! = 2 + 1 = 3`, divisible by 3. If we naively attempted `x = k - 1` without checking, it might work, but we have to understand why this pattern holds.

## Approaches

The brute-force approach would iterate over `x` from `k-1` down to `1`, compute `x! + (x-1)!`, and check divisibility by `k`. This is correct mathematically but fails computationally. Calculating factorials up to `10^9` is impossible. Even using modular arithmetic, the factorial sequence quickly exceeds any feasible integer size, so this approach is too slow and memory-intensive.

The key observation is that the sum `x! + (x-1)!` can be rewritten as `(x-1)! * (x + 1)`. We want this expression divisible by `k`. If `x >= k`, `(x-1)!` already contains `k` as a factor when `k > 2`, but we are limited to `x < k`. So the largest `x` that works is `k-1`. This is because `(k-1)! + (k-2)!` simplifies to `(k-2)! * k`, which is always divisible by `k` for `k > 2`. For `k = 2`, the only candidate is `x = 1`.

We can summarize: for any `k >= 3`, the answer is `k-1`. For `k = 2`, the answer is `1`. There is no need to compute factorials explicitly, which reduces the problem to simple arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per test case | O(1) | Too slow for large k |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, `t`.
2. For each test case, read the integer `k`.
3. If `k` equals 2, output 1. This is the only case where the largest `x` is not `k-1`.
4. Otherwise, output `k-1`. This works because `(k-1)! + (k-2)! = (k-2)! * k`, which is divisible by `k`.
5. Repeat for all test cases.

Why it works: the crucial property is the factorial factorization. For any integer `k > 2`, `(k-2)!` multiplied by `k` guarantees divisibility. By always taking `x = k-1`, we ensure we are maximizing `x` while keeping it less than `k`. The special case `k = 2` handles the smallest bound where the factorial pattern still holds.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k = int(input())
    if k == 2:
        print(1)
    else:
        print(k - 1)
```

The code first reads the number of test cases. For each test case, it checks the special case `k = 2` because the general formula `k-1` would produce `1`, which coincidentally matches, but we handle it explicitly for clarity. For all other `k`, it prints `k-1`, using the mathematical simplification. Fast input with `sys.stdin.readline` ensures the solution runs efficiently for up to 10,000 test cases.

## Worked Examples

**Input:** `3`

**k = 3**

| k | x | (x-1)! | x! | x! + (x-1)! | Divisible by k? |
| --- | --- | --- | --- | --- | --- |
| 3 | 2 | 1 | 2 | 3 | Yes |

Here `x = 2` gives `2! + 1! = 3`, divisible by 3. The algorithm outputs `2`.

**Input:** `6`

| k | x | (x-1)! | x! | x! + (x-1)! | Divisible by k? |
| --- | --- | --- | --- | --- | --- |
| 6 | 5 | 24 | 120 | 144 | Yes |

`x = 5` gives `(5! + 4!) = 144`, divisible by `6`. The algorithm outputs `5`.

The traces confirm that picking `x = k-1` maximizes `x` while guaranteeing divisibility through the factorial factorization property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is handled in O(1), t ≤ 10^4 |
| Space | O(1) | Only a few integers are stored per test case |

With these constraints, the solution executes well under 1 second, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        k = int(input())
        if k == 2:
            print(1)
        else:
            print(k - 1)
    return output.getvalue().strip()

# provided samples
assert run("4\n3\n6\n8\n10\n") == "2\n5\n7\n9", "sample 1"

# custom cases
assert run("1\n2\n") == "1", "minimum k"
assert run("1\n1000000000\n") == "999999999", "maximum k"
assert run("3\n4\n5\n6\n") == "3\n4\n5", "small consecutive k"
assert run("1\n7\n") == "6", "prime k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | Handles the minimum k edge case |
| 1000000000 | 999999999 | Handles very large k efficiently |
| 4,5,6 | 3,4,5 | Correctness for small consecutive numbers |
| 7 | 6 | Correctness for prime k |

## Edge Cases

For `k = 2`, the algorithm explicitly returns `1`. Even though `1! + 0! = 2` is divisible by `2`, handling it separately ensures the code is clear and avoids misinterpretation of the formula `k-1`. For `k = 10^9`, the algorithm does not compute any factorial and directly outputs `999999999`, avoiding overflow and running in constant time. For all primes or composite numbers greater than 2, the choice `x = k-1` is valid, because the factorization `(x-1)! * (x+1)` guarantees divisibility. This covers every possible input within the constraints.

This completes the editorial. It shows the reasoning from factorial manipulation, highlights the key insight, and delivers a fully efficient, correct solution.
