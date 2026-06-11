---
title: "CF 1238A - Prime Subtraction"
description: "We are given two integers, x and y, with x y. The task is to determine whether it is possible to choose a single prime number p and repeatedly subtract it from x until we reach y. Importantly, once a prime is chosen, it must be used exclusively; we cannot switch primes mid-way."
date: "2026-06-11T22:09:09+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1238
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 74 (Rated for Div. 2)"
rating: 900
weight: 1238
solve_time_s: 83
verified: true
draft: false
---

[CF 1238A - Prime Subtraction](https://codeforces.com/problemset/problem/1238/A)

**Rating:** 900  
**Tags:** math, number theory  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `x` and `y`, with `x > y`. The task is to determine whether it is possible to choose a single prime number `p` and repeatedly subtract it from `x` until we reach `y`. Importantly, once a prime is chosen, it must be used exclusively; we cannot switch primes mid-way. Each test case is independent, and the values of `x` and `y` can be extremely large, up to $10^{18}$.

The problem reduces to checking whether the difference `x - y` can be expressed as a multiple of some prime number. If such a prime exists, the answer is "YES"; otherwise, "NO".

Constraints suggest we cannot iterate over all primes up to `x - y` because the difference itself can be as large as $10^{18}$, and we have up to 1000 test cases. A naive approach attempting trial division for every potential prime would be far too slow.

Edge cases include scenarios where `x - y = 1`. Since 1 is not a prime, it is impossible to subtract any prime to reach `y`. Another case is when `x - y` is even and greater than 2: we can always use 2 to bridge the gap. Similarly, if `x - y` itself is prime, we can use that prime directly. These insights lead to the optimal approach.

## Approaches

A brute-force solution would attempt to generate all prime numbers less than `x - y` and check for each whether it divides the difference. While correct for small inputs, this fails because generating primes up to $10^{18}$ is infeasible. The operation count would be astronomical, easily exceeding $10^{15}$, making it impractical.

The key observation is that we only need to check the smallest prime, 2, and whether the difference itself is prime. If `x - y = 1`, no prime works and the answer is "NO". For `x - y >= 2`, there is always a prime `p` that divides the difference. Specifically, if the difference is even, 2 works; if the difference is greater than 2 and odd, then the difference itself is prime or has a prime factor smaller than itself. Therefore, the problem simplifies to a constant-time check per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (trial division / sieve up to x-y) | O(sqrt(x-y)) per test case | O(1) | Too slow for x-y ~ 1e18 |
| Optimal (difference analysis) | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `x` and `y`.
3. Compute the difference `d = x - y`.
4. If `d == 1`, print "NO" because no prime can bridge a difference of 1.
5. Otherwise, print "YES". Any difference greater than 1 can always be expressed as multiples of some prime.

The reasoning is that every integer greater than 1 has at least one prime factor. Thus, either `d` is prime itself, or it can be decomposed into multiples of a prime number, which satisfies the problem's requirements.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    if x - y == 1:
        print("NO")
    else:
        print("YES")
```

The code follows the algorithm directly. We use fast input via `sys.stdin.readline` to handle multiple test cases efficiently. The difference `x - y` is computed as a single integer subtraction. We check for the only failing edge case where the difference is 1, and otherwise return "YES".

## Worked Examples

Sample Input 1:

```
100 98
```

| x | y | d = x-y | Output |
| --- | --- | --- | --- |
| 100 | 98 | 2 | YES |

Explanation: `d = 2`. The difference is greater than 1, so we can subtract the prime 2 exactly once.

Sample Input 2:

```
41 40
```

| x | y | d = x-y | Output |
| --- | --- | --- | --- |
| 41 | 40 | 1 | NO |

Explanation: `d = 1`. No prime number can be subtracted to reach `y` because all primes are greater than 1.

These traces demonstrate that the only case requiring careful handling is when the difference is exactly 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | We perform constant-time operations for each of the t test cases. |
| Space | O(1) | Only a few integer variables are used, independent of input size. |

This fits comfortably within the 2-second time limit even for the maximum t = 1000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        x, y = map(int, input().split())
        if x - y == 1:
            print("NO")
        else:
            print("YES")
    return output.getvalue().strip()

# Provided samples
assert run("4\n100 98\n42 32\n1000000000000000000 1\n41 40\n") == "YES\nYES\nYES\nNO", "sample 1"

# Custom cases
assert run("2\n2 1\n3 2\n") == "NO\nNO", "difference 1 edge case"
assert run("1\n1000000000000000000 999999999999999998\n") == "YES", "large even difference"
assert run("1\n1000000000000000000 999999999999999999\n") == "NO", "large difference of 1"
assert run("1\n17 2\n") == "YES", "odd difference greater than 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | NO | Difference of 1 cannot be bridged by primes |
| 3 2 | NO | Another difference of 1 |
| 1e18 1e18-2 | YES | Very large even difference works |
| 1e18 1e18-1 | NO | Very large difference of 1 |
| 17 2 | YES | Odd difference greater than 1 is valid |

## Edge Cases

For the difference of 1, the algorithm correctly outputs "NO". Input `x = 41`, `y = 40` yields `d = 1`, triggering the specific condition and avoiding the incorrect assumption that any prime works.

For maximum-size inputs, like `x = 10^18`, `y = 1`, the difference `d = 10^18 - 1` is much larger than 1, so the algorithm outputs "YES" efficiently without iterating or generating primes. This confirms correctness and performance across the entire input space.
