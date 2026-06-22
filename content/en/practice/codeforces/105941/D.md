---
title: "CF 105941D - 2025"
description: "We are given a single integer representing a year, and we need to decide whether it satisfies a very specific numeric property. The year is valid if two conditions hold simultaneously."
date: "2026-06-22T15:51:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105941
codeforces_index: "D"
codeforces_contest_name: "2025 National Invitational of CCPC (Zhengzhou), 2025 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105941
solve_time_s: 59
verified: true
draft: false
---

[CF 105941D - 2025](https://codeforces.com/problemset/problem/105941/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer representing a year, and we need to decide whether it satisfies a very specific numeric property. The year is valid if two conditions hold simultaneously. First, the year itself must be a perfect square, meaning there exists an integer whose square equals the year. Second, when we sum the decimal digits of the year, that sum must also be a perfect square.

The input size is extremely small, with the year bounded by 999,999. This immediately rules out anything like heavy preprocessing or advanced data structures. Any solution that repeatedly performs square checks or digit processing is still trivial to execute within limits because we only process one number, or at most a few test cases if extended.

The only subtle cases come from mismanaging perfect square checks. A common mistake is using floating-point square roots without correcting precision errors. Another is forgetting that digit sum can also be zero only in theoretical cases like 0, which is not relevant here because the year is at least 1. A third issue is assuming that if the number looks like a square pattern, it must be one, which fails for values like 999999 where rounding errors or incorrect integer checks may appear if implemented poorly.

A concrete edge case is the sample 999999. The digit sum is 54, which is not a perfect square, so the answer is No even though the number is close to a large square and might tempt incorrect heuristics. Another is 2025, which works cleanly since 2025 equals 45 squared and digit sum is 9 equals 3 squared.

## Approaches

The most direct approach is to compute whether the number is a perfect square, and separately compute the sum of its digits and check whether that sum is also a perfect square. This is straightforward because both operations are O(log y). The only nontrivial component is the square check.

A brute-force way to check if a number n is a perfect square is to try all integers i from 1 upward and test whether i squared equals n. This works correctly but is unnecessary because the maximum possible square root is at most 1000 since 1000 squared is 1,000,000, slightly above the constraint limit. Even though this brute-force is already small, it is conceptually inferior because it ignores the direct mathematical structure of square roots.

A better approach is to compute the integer square root of n using either built-in integer sqrt or binary search, then verify whether squaring it reproduces n. This avoids floating-point issues entirely and gives a deterministic check.

The digit sum is computed in a single pass over the decimal representation, and then the same square-check logic is applied again.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sqrt scan | O(√n) | O(1) | Accepted but unnecessary |
| Integer sqrt check + digit sum | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer y as input. This is the candidate year we evaluate directly.
2. Compute the digit sum of y by repeatedly extracting the last digit and accumulating it. This gives a secondary number s that captures the additive structure of the year.
3. Compute r = floor(sqrt(y)) using integer arithmetic. Then verify whether r * r equals y. If not, y is not a perfect square and we can immediately reject it. This step avoids floating-point precision issues.
4. Repeat the same square verification for s. Compute t = floor(sqrt(s)) and check whether t * t equals s. This ensures the digit sum is also structurally a perfect square.
5. Output Yes if both checks pass, otherwise output No.

### Why it works

The correctness rests on two independent characterizations. A number is a perfect square if and only if its integer square root, when squared back, reproduces the original value. This avoids approximation errors entirely because all operations are integer-based. The digit sum transformation is independent of the square property, so verifying it separately does not interfere with the first condition. Since both conditions are necessary and sufficient individually, their conjunction exactly matches the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_square(x: int) -> bool:
    if x < 0:
        return False
    r = int(x ** 0.5)
    return r * r == x or (r + 1) * (r + 1) == x

y = int(input().strip())

digit_sum = 0
tmp = y
while tmp > 0:
    digit_sum += tmp % 10
    tmp //= 10

if is_square(y) and is_square(digit_sum):
    print("Yes")
else:
    print("No")
```

The function `is_square` uses a floating-point square root but corrects possible rounding errors by checking both `r` and `r+1`. This is important because direct casting from float can occasionally truncate due to precision limits near large squares. The digit sum computation is done iteratively to avoid string conversion overhead, though either method would be acceptable given the constraints.

The final condition combines both checks directly, matching the logical requirement that both properties must hold simultaneously.

## Worked Examples

### Example 1: 2025

We compute digit sum and square status step by step.

| Step | y | digit sum | sqrt(y) check | sqrt(sum) check |
| --- | --- | --- | --- | --- |
| Start | 2025 | 0 | - | - |
| After digit scan | 2025 | 9 | - | - |
| Square check y | 2025 | 9 | True (45² = 2025) | - |
| Square check sum | 2025 | 9 | True | True (3² = 9) |

This confirms both conditions simultaneously, so the output is Yes.

### Example 2: 999999

| Step | y | digit sum | sqrt(y) check | sqrt(sum) check |
| --- | --- | --- | --- | --- |
| Start | 999999 | 0 | - | - |
| After digit scan | 999999 | 54 | - | - |
| Square check y | 999999 | 54 | False | - |

Since the first condition already fails, we stop early and return No. The digit sum being 54 is irrelevant once the first condition is violated, but even if checked, 54 is not a perfect square.

These traces show that rejection can happen at either condition independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log y) | digit extraction takes O(log y), square checks are constant time |
| Space | O(1) | only a few integer variables are used |

The constraints cap y at one million, so even a simple loop over digits and constant-time square checks are far below time limits. The solution is effectively instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main()

def main():
    import sys
    input = sys.stdin.readline

    def is_square(x: int) -> bool:
        if x < 0:
            return False
        r = int(x ** 0.5)
        return r * r == x or (r + 1) * (r + 1) == x

    y = int(input().strip())

    digit_sum = 0
    tmp = y
    while tmp > 0:
        digit_sum += tmp % 10
        tmp //= 10

    return "Yes" if is_square(y) and is_square(digit_sum) else "No"

# provided samples
assert run("2025\n") == "Yes"
assert run("999999\n") == "No"

# custom cases
assert run("1\n") == "Yes"   # 1 is 1^2, digit sum 1 is 1^2
assert run("2\n") == "No"    # not a square
assert run("16\n") == "No"   # 16 is square but digit sum 7 is not
assert run("81\n") == "Yes"  # 81=9^2, digit sum 9=3^2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | Yes | smallest valid square case |
| 2 | No | non-square rejection |
| 16 | No | square but invalid digit sum |
| 81 | Yes | both conditions satisfied |

## Edge Cases

The smallest meaningful input is 1. The algorithm computes digit sum as 1 and correctly identifies both conditions as true since 1 is a perfect square.

For 2, digit sum is 2 and the square check fails immediately. The square check uses integer comparison, so no floating-point error can incorrectly classify it as a square.

For 16, the number passes the square test since 4 squared is 16, but digit sum becomes 7. The second check correctly rejects it.

For 81, both checks pass cleanly. The square root is 9 and digit sum is also 9, and both reduce to 3 squared. This confirms that independent checks do not interfere and both must be satisfied simultaneously.
