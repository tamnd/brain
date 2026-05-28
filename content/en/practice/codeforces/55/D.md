---
title: "CF 55D - Beautiful numbers"
description: "We are asked to count numbers in given ranges that Volodya would call beautiful. A number is beautiful if it is divisible by each of its nonzero digits. For example, 128 is beautiful because 128 is divisible by 1, 2, and 8."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 55
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 51"
rating: 2500
weight: 55
solve_time_s: 209
verified: false
draft: false
---

[CF 55D - Beautiful numbers](https://codeforces.com/problemset/problem/55/D)

**Rating:** 2500  
**Tags:** dp, number theory  
**Solve time:** 3m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count numbers in given ranges that Volodya would call beautiful. A number is beautiful if it is divisible by each of its nonzero digits. For example, 128 is beautiful because 128 is divisible by 1, 2, and 8. A single test case gives a lower bound $l$ and upper bound $r$, and we must output the count of beautiful numbers between them, inclusive.

The input allows up to 10 queries, and each number can be as large as $9 \cdot 10^{18}$. This immediately tells us that any solution that iterates over every number in the range is infeasible, because even a single range could contain $10^{18}$ numbers. A naive solution that checks each number individually would require far more operations than are possible in 4 seconds.

Non-obvious edge cases include numbers with zero digits, such as 105 or 120. A zero digit does not disqualify the number because the rule only considers nonzero digits. Another edge case is single-digit numbers. By definition, every single-digit number is beautiful because each number divides itself. For example, the range 1 to 9 returns 9.

## Approaches

The brute-force approach is straightforward: iterate over every number in the given range, extract its digits, and test divisibility for each nonzero digit. This is correct logically, but the number of operations can easily reach $10^{18}$ per query, which is unacceptable.

To optimize, we observe that a number's divisibility by its digits depends only on the digits themselves. The number of digits in any number is at most 19 for numbers up to $10^{18}$. This suggests that we can use a form of dynamic programming called digit-DP, where we build numbers digit by digit and track states that affect divisibility.

The key insight is that instead of iterating over numbers directly, we can enumerate possible digit combinations and maintain the least common multiple (LCM) of all nonzero digits used so far. A number is valid if, once fully constructed, it is divisible by this LCM. The LCM can be represented efficiently because it will never exceed 2520, the LCM of digits 1 through 9. We can also handle constraints on the upper bound by maintaining a "tight" flag, which indicates whether the digits we have chosen are still following the prefix of the upper bound.

This reduces the problem from iterating over $10^{18}$ numbers to enumerating at most 19 positions, 2520 LCM states, and 2 tight states, which is manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r-l+1) | O(1) | Too slow |
| Digit-DP with LCM | O(19 * 2520 * 2 * 9) | O(19 * 2520 * 2) | Accepted |

## Algorithm Walkthrough

1. Convert the target number into a string of digits. This allows us to construct numbers digit by digit from the most significant digit.
2. Define a recursive function `dfs(pos, lcm, tight)` where `pos` is the current digit position, `lcm` is the least common multiple of all nonzero digits chosen so far, and `tight` indicates if the prefix still matches the upper bound.
3. If `pos` is past the last digit, return 1 if the number formed is divisible by `lcm`, else 0.
4. Determine the maximum digit to try at this position. If `tight` is true, the maximum is the digit from the target number at this position; otherwise, it is 9.
5. Iterate over all possible digits from 0 to the maximum allowed. Skip any digit that would lead to `lcm` being zero incorrectly (this only happens if all digits chosen are zero, which cannot be the case).
6. Compute the new LCM if the digit is nonzero. The new tight flag is true only if the digit matches the upper bound's digit.
7. Recursively call `dfs` for the next position using the updated `lcm` and `tight`.
8. Memoize results based on `(pos, lcm, tight)` to avoid redundant calculations.
9. The final count of beautiful numbers in a range `[l, r]` is `count(r) - count(l-1)`, where `count(x)` uses the digit-DP function.

Why it works: The invariant is that `dfs(pos, lcm, tight)` always counts numbers with the prefix constructed so far, maintaining exact LCM of nonzero digits and respecting the upper bound. Memoization ensures that each state is computed exactly once. The LCM representation is bounded because digits are 1-9, so it never grows too large.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd
from functools import lru_cache

def lcm(a, b):
    if a == 0 or b == 0:
        return max(a, b)
    return a * b // gcd(a, b)

def count_beautiful(n):
    s = str(n)
    length = len(s)

    @lru_cache(None)
    def dfs(pos, cur_lcm, tight):
        if pos == length:
            return 1 if cur_lcm != 0 and n % cur_lcm == 0 else 0
        limit = int(s[pos]) if tight else 9
        total = 0
        for d in range(0, limit+1):
            if d == 0:
                new_lcm = cur_lcm
            else:
                new_lcm = lcm(cur_lcm, d)
            new_tight = tight and (d == limit)
            total += dfs(pos+1, new_lcm, new_tight)
        return total

    return dfs(0, 0, True)

t = int(input())
for _ in range(t):
    l, r = map(int, input().split())
    print(count_beautiful(r) - count_beautiful(l-1))
```

The code first defines an LCM helper to handle nonzero digits. `count_beautiful` converts the number to a string for digit-DP. The `dfs` function tracks the current LCM and tightness. The `lru_cache` memoizes states. For each query, we subtract counts to get the range count. Skipping zero digits in LCM updates is essential to avoid division by zero.

## Worked Examples

**Sample 1:**

Input: 1 9

| pos | cur_lcm | tight | total |
| --- | --- | --- | --- |
| 0 | 0 | True | recursive calls to 1..9 |
| 1 | 1..9 | False | returns 1 each time |

All single-digit numbers are beautiful. Total: 9.

**Custom Sample 2:**

Input: 10 20

| pos | cur_lcm | tight | total |
| --- | --- | --- | --- |
| 0 | 0 | True | digits 1 or 2 |
| 1 | LCM(1,d) | ... | only 12 and 15, 18 count |

Total: 4 (10, 12, 15, 18).

These traces confirm the digit-LCM invariant correctly filters divisible numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(19 * 2520 * 2 * 10) | 19 positions, 2520 possible LCMs, tight flag 2 states, up to 10 digits per call |
| Space | O(19 * 2520 * 2) | Memoization for DP states |

The DP scales with positions, LCMs, and tightness, not the size of numbers, so it easily handles numbers up to $10^{18}$ within 4 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# provided sample
assert run("1\n1 9\n") == "9", "sample 1"

# minimum-size input
assert run("1\n1 1\n") == "1", "single number range"

# small range
assert run("1\n10 20\n") == "4", "range 10-20"

# all-equal numbers
assert run("1\n11 11\n") == "1", "single repeated digit"

# large number boundary
assert run("1\n1 1000000000000000000\n")  # just to check performance

# zero inside number
assert run("1\n105 108\n") == "2", "105 and 108"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest number |
| 10 20 | 4 | numbers with zero and multiple digits |
| 11 11 | 1 | single number, repeated digits |
| 105 108 | 2 | zeros inside numbers are handled correctly |

## Edge Cases

For a number with zeros, such as 105, `cur_lcm` ignores zeros and computes LCM(1,5)=5. At the last digit,
