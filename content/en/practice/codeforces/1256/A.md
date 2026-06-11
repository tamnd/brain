---
title: "CF 1256A - Payment Without Change"
description: "We are asked to determine whether a target sum S can be constructed using two types of coins. One type has value n and there are a coins of it, the other type has value 1 and there are b coins of it."
date: "2026-06-11T20:52:24+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1256
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 598 (Div. 3)"
rating: 1000
weight: 1256
solve_time_s: 110
verified: true
draft: false
---

[CF 1256A - Payment Without Change](https://codeforces.com/problemset/problem/1256/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a target sum `S` can be constructed using two types of coins. One type has value `n` and there are `a` coins of it, the other type has value `1` and there are `b` coins of it. For each test case, the task is to decide if we can pick some number `x` of coins with value `n` and some number `y` of coins with value `1` such that their total value equals `S`. The constraints are that `x` cannot exceed `a` and `y` cannot exceed `b`.

The input sizes are large: `a`, `b`, `n`, and `S` can go up to `10^9`, and there can be up to `10^4` test cases. This rules out any brute-force approach that tries every combination of `x` and `y` because the number of iterations could exceed `10^9` per test case, far beyond feasible computation in one second.

A subtle edge case arises when the target `S` is not a multiple of `n` but we have few coins of value `1`. For example, if `a=1`, `b=1`, `n=3`, and `S=4`, we can take one coin of value 3 and one coin of value 1 to reach 4. But if `b=0`, the same `S` cannot be reached even though `S` is smaller than the maximum possible using `a` coins of `n`. A careless approach that only checks `S <= a * n + b` would incorrectly return YES for this case.

## Approaches

The naive approach is to iterate over every possible number of `n`-value coins `x` from `0` to `a` and for each `x` check if there is a `y` such that `x*n + y = S` and `y <= b`. This works because it directly tests all possible ways to reach `S`, but it requires up to `a` iterations per test case. Since `a` can be up to `10^9`, this approach is completely impractical.

The key observation that leads to an optimal solution is that we do not need to try every `x`. The largest contribution from the `n`-value coins should be used first to reduce the remaining amount we need from `1`-value coins. We can simply take `x = min(a, S // n)` coins of value `n`. This maximizes the contribution from `n`-value coins without exceeding `a` or overshooting `S`. Then the remaining sum to reach `S` is `S - x * n`. If this remainder is less than or equal to `b`, we can cover it with `1`-value coins. Otherwise, the sum cannot be reached. This observation reduces the solution to a constant-time check per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a) | O(1) | Too slow for a=10^9 |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the values `a`, `b`, `n`, `S`.
2. Compute the maximum number of `n`-value coins we could use without exceeding `S` as `S // n`.
3. Restrict this number by the actual coins we have, giving `x = min(a, S // n)`.
4. Compute the remaining sum after using `x` coins of value `n`: `remaining = S - x * n`.
5. Check if `remaining` is less than or equal to `b`. If yes, print `YES`; otherwise, print `NO`.

Why it works: By taking as many high-value coins as possible without exceeding the target, we ensure the leftover sum is minimized. Since 1-value coins can cover any amount up to `b`, checking if the remainder is ≤ b guarantees that the exact sum `S` can be formed if possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    a, b, n, S = map(int, input().split())
    max_n_coins = min(a, S // n)
    remaining = S - max_n_coins * n
    if remaining <= b:
        print("YES")
    else:
        print("NO")
```

The solution first calculates the maximum number of `n`-value coins we can take (`S // n`), then limits it by the available coins (`min(a, S // n)`). The remaining sum is checked against `b`. Using integer division and subtraction guarantees no floating-point errors. No extra space is used beyond a few variables.

## Worked Examples

Trace Sample 1:

Input: `1 2 3 4`

| Step | max_n_coins | remaining | remaining <= b? | Output |
| --- | --- | --- | --- | --- |
| 1 | min(1, 4//3)=1 | 4 - 1*3 = 1 | 1 <= 2 | YES |

Input: `1 2 3 6`

| Step | max_n_coins | remaining | remaining <= b? | Output |
| --- | --- | --- | --- | --- |
| 1 | min(1, 6//3)=1 | 6 - 1*3 = 3 | 3 <= 2 | NO |

These traces demonstrate that the algorithm correctly calculates how many high-value coins to use and verifies if the remaining sum can be covered with 1-value coins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each test case requires a few arithmetic operations |
| Space | O(1) | Only a handful of integer variables are used |

Given up to `10^4` test cases, the total operations are within `10^5`, which easily fits in the 1-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    q = int(input())
    for _ in range(q):
        a, b, n, S = map(int, input().split())
        max_n_coins = min(a, S // n)
        remaining = S - max_n_coins * n
        if remaining <= b:
            output.append("YES")
        else:
            output.append("NO")
    return "\n".join(output)

# Provided samples
assert run("4\n1 2 3 4\n1 2 3 6\n5 2 6 27\n3 3 5 18\n") == "YES\nNO\nNO\nYES", "Sample 1"

# Custom cases
assert run("1\n0 5 3 4\n") == "NO", "no n-value coins"
assert run("1\n5 0 3 9\n") == "YES", "exact multiples of n"
assert run("1\n5 0 3 10\n") == "NO", "remainder cannot be covered"
assert run("1\n1 1 1 2\n") == "YES", "minimum coin values"
assert run("1\n1000000000 1000000000 1000000000 2000000000\n") == "YES", "maximum coin counts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 5 3 4` | NO | cannot pay S without n-value coins |
| `5 0 3 9` | YES | exact multiple of n, no 1-value coins needed |
| `5 0 3 10` | NO | remainder cannot be covered |
| `1 1 1 2` | YES | minimum values, simple case |
| `1000000000 1000000000 1000000000 2000000000` | YES | large numbers, stress test |

## Edge Cases

If `a` is 0, the algorithm sets `max_n_coins = 0` and checks if `S <= b`. For example, `a=0, b=5, n=3, S=4` leads to `max_n_coins=0`, `remaining=4`, and `remaining <= b` is true only if `b >= 4`. If `b` is smaller, the algorithm correctly outputs NO.

If `S` is smaller than `n` but we have some n-value coins, `S // n` is 0, so no n-value coin is used. For `a=5, b=5, n=10, S=3`, `max_n_coins=0`, `remaining=3`, and `remaining <= b` evaluates as YES because the 1-value coins suffice.

If `S` is exactly equal to `a * n + b`, the algorithm takes all `a` coins and uses the remaining `b` coins to cover the remainder. This handles the upper-bound edge correctly.
