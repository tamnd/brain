---
title: "CF 2126A - Only One Digit"
description: "The task asks us to find the smallest non-negative integer that shares at least one decimal digit with a given number. For every test case, we are provided a number x, and we need to produce a number y such that some digit in y also appears in x."
date: "2026-06-08T03:21:27+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2126
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1037 (Div. 3)"
rating: 800
weight: 2126
solve_time_s: 70
verified: true
draft: false
---

[CF 2126A - Only One Digit](https://codeforces.com/problemset/problem/2126/A)

**Rating:** 800  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to find the smallest non-negative integer that shares at least one decimal digit with a given number. For every test case, we are provided a number `x`, and we need to produce a number `y` such that some digit in `y` also appears in `x`. The number `y` should be as small as possible.

The input consists of multiple test cases, up to 1000, and each number `x` is between 1 and 1000. These bounds are modest, which means we can afford simple operations like converting numbers to strings, iterating over their digits, or trying all single-digit numbers directly. Since `x` is at most four digits long, storing its digits in a set or array is trivial in terms of memory.

Edge cases to consider include numbers that are themselves single digits. For instance, if `x = 7`, the smallest `y` is `7` itself. A careless approach might try to loop over numbers starting from zero and check each one; this would work, but it is overkill and ignores the fact that `y` must always be one of the digits present in `x`. Another subtle case is numbers containing zeros, like `x = 102`, where the minimal `y` is `0`, not `1` or `2` necessarily, but whatever is smallest among the digits of `x`.

## Approaches

A brute-force approach would be to start at `y = 0` and incrementally check every number to see if it shares a digit with `x`. To implement this, we could convert both numbers to strings, then check each pair of digits for equality. In the worst case, `y` could reach 1000 before finding a match, and doing string comparisons repeatedly would make this approach slower than necessary. Although for the given constraints it still passes, it is not elegant or conceptually minimal.

The key insight is that `y` only needs to be a single-digit number because if any digit of `x` exists in 0-9, that digit is already the minimal possible `y`. The problem reduces to extracting the digits of `x` and returning the smallest one. This works because single-digit numbers are the smallest non-negative integers, so the minimal solution is simply the minimum digit present in `x`. This insight avoids any unnecessary iteration and provides a direct, constant-time solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1000) per test case | O(log x) | Accepted but unnecessary |
| Optimal | O(log x) per test case | O(log x) | Accepted |

## Algorithm Walkthrough

1. Read the integer `t`, the number of test cases.
2. For each test case, read the integer `x`.
3. Convert `x` to a string so that we can iterate over its digits.
4. Extract all digits from `x` and convert them into integers.
5. Find the smallest digit among these integers. This is the minimal `y` that shares a digit with `x`.
6. Print this smallest digit for the current test case.

Why it works: Any number `y` that shares a digit with `x` must contain one of the digits present in `x`. Since digits 0-9 are the smallest building blocks of integers, the minimal `y` is guaranteed to be the smallest digit from `x`. This invariant is always true because we never consider numbers outside the digits of `x`, so no smaller valid `y` can exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x = input().strip()
    digits = [int(d) for d in x]
    print(min(digits))
```

The solution first reads the number of test cases. For each test case, it converts the number to a string to easily extract digits, then converts each digit back to an integer for comparison. The minimal digit is printed immediately. This avoids unnecessary loops, handles leading zeros correctly, and works for both single- and multi-digit numbers.

## Worked Examples

**Example 1**

Input `x = 6`

| Variable | Value |
| --- | --- |
| x | '6' |
| digits | [6] |
| min(digits) | 6 |

The output is 6. Here, the smallest number sharing a digit with 6 is 6 itself.

**Example 2**

Input `x = 122`

| Variable | Value |
| --- | --- |
| x | '122' |
| digits | [1, 2, 2] |
| min(digits) | 1 |

The output is 1. The smallest number sharing a digit with 122 is 1, the smallest of its digits. This demonstrates handling of repeated digits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log x) per test case | We iterate over each digit in x, which has at most 4 digits. |
| Space | O(log x) per test case | We store the list of digits from x. |

Given the constraints, 1000 test cases with numbers up to 1000 results in at most 4000 digit operations. This fits comfortably within the 1-second time limit. Memory use is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        x = input().strip()
        digits = [int(d) for d in x]
        output.append(str(min(digits)))
    return "\n".join(output)

# Provided samples
assert run("5\n6\n96\n78\n122\n696\n") == "6\n6\n7\n1\n6", "sample 1"

# Custom cases
assert run("3\n7\n102\n1000\n") == "7\n0\n0", "single digits and zero handling"
assert run("2\n999\n111\n") == "9\n1", "all-equal digits"
assert run("2\n10\n20\n") == "0\n0", "numbers containing zero"
assert run("1\n321\n") == "1", "descending digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7, 102, 1000 | 7, 0, 0 | Single-digit numbers and presence of 0 |
| 999, 111 | 9, 1 | All-equal digits |
| 10, 20 | 0, 0 | Handling of zero digits |
| 321 | 1 | Descending digits, correct min selection |

## Edge Cases

For `x = 102`, the digits are `[1, 0, 2]`. The algorithm extracts these digits, finds the minimum (0), and returns it. Even though `y` could be larger numbers like 10 or 12, the minimal non-negative integer sharing a digit is 0, and the algorithm produces this correctly.

For `x = 1000`, the digits `[1, 0, 0, 0]` yield 0 as the smallest. This confirms the solution handles multiple zeros properly.

For a single-digit `x`, like 7, the digits `[7]` directly produce 7, confirming that the algorithm works without additional conditions for small numbers.

This editorial provides a clear path from the problem to a constant-time solution per test case. It avoids unnecessary iteration and uses the properties of digits to guarantee correctness.
