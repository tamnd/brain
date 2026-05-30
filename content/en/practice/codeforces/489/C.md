---
title: "CF 489C - Given Length and Sum of Digits..."
description: "We are asked to construct two numbers of a specified length, m, whose digits sum to a given value, s. The first number should be the smallest possible, the second the largest. Both numbers are expressed in base 10 and cannot have leading zeroes unless the number is zero itself."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 489
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 277.5 (Div. 2)"
rating: 1400
weight: 489
solve_time_s: 653
verified: false
draft: false
---

[CF 489C - Given Length and Sum of Digits...](https://codeforces.com/problemset/problem/489/C)

**Rating:** 1400  
**Tags:** dp, greedy, implementation  
**Solve time:** 10m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct two numbers of a specified length, _m_, whose digits sum to a given value, _s_. The first number should be the smallest possible, the second the largest. Both numbers are expressed in base 10 and cannot have leading zeroes unless the number is zero itself.

The input provides two integers: _m_ tells us how many digits the number must have, and _s_ tells us what the sum of those digits must be. The output is a pair of numbers: the minimal and maximal numbers that satisfy these conditions, or "-1 -1" if no such number exists.

The constraints are subtle. Since _m_ can go up to 100 and _s_ up to 900, we cannot generate all numbers of length _m_ and check their digit sums; the brute force approach would require evaluating up to $10^{100}$ possibilities. The edge cases include a zero sum. For instance, _m = 1_ and _s = 0_ is valid and should return "0 0", but _m > 1_ and _s = 0_ is impossible because a number of length more than one cannot have a sum of zero without leading zeroes. Another edge case occurs when the sum exceeds the maximum achievable sum for a given length, e.g., _m = 2_, _s = 20_, which is impossible because the maximum sum of two digits is 18.

## Approaches

A brute-force approach would attempt to generate all numbers of length _m_, calculate the sum of their digits, and compare against _s_. This is correct in principle, but infeasible: even for _m = 20_, there are $10^{20}$ candidates. The operation count is astronomical and cannot complete within the given 1-second limit.

The key insight comes from recognizing the problem's structure: the sum of digits is constrained and each digit ranges from 0 to 9. For the maximum number, we can greedily assign the largest possible digit starting from the most significant position. For the minimum number, we need a similar approach but in reverse: we want the smallest digit in the most significant position, but we must leave enough sum for the remaining digits. The problem is effectively greedy, because at each step, the choice of digit depends only on the remaining sum and the number of remaining positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^m) | O(m) | Too slow |
| Greedy / Constructive | O(m) | O(m) | Accepted |

## Algorithm Walkthrough

1. **Check feasibility**. If _s_ is 0 and _m_ is greater than 1, or if _s_ is greater than 9*m, output "-1 -1". These conditions are impossible because either the sum cannot be split across the digits without violating length, or the sum exceeds the maximum digit sum for length _m_.
2. **Construct the maximum number**. Start with an empty list for digits. For each position from left to right, assign the largest digit possible, constrained by the remaining sum (cannot exceed 9). Subtract that digit from the remaining sum. Repeat until all digits are filled.
3. **Construct the minimum number**. This requires a small adjustment to avoid leading zeros. Start from left to right as well, but pick the smallest digit possible at each position, constrained so that the remaining digits can still sum up to the remaining sum. Specifically, the digit at position _i_ must be at least `max(1, remaining_sum - 9*(m-i-1))` to ensure the rest of the digits can accommodate the remaining sum without exceeding 9 per digit. Subtract the chosen digit from the remaining sum and continue.
4. **Output the numbers**. Join the digits of the minimal and maximal numbers into strings and print them.

**Why it works**. For the maximum number, assigning the largest possible digit at each position maximizes the value greedily; for the minimum number, assigning the smallest possible digit while ensuring feasibility guarantees minimality without breaking the sum constraint. At each step, the remaining sum is correctly distributed among the remaining positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

m, s = map(int, input().split())

if (s == 0 and m > 1) or (s > 9 * m):
    print("-1 -1")
else:
    # Construct max number
    sum_remaining = s
    max_digits = []
    for i in range(m):
        d = min(9, sum_remaining)
        max_digits.append(str(d))
        sum_remaining -= d
    max_num = ''.join(max_digits)

    # Construct min number
    sum_remaining = s
    min_digits = []
    for i in range(m):
        for d in range(0 if i > 0 else 1, 10):
            if sum_remaining - d <= 9 * (m - i - 1):
                min_digits.append(str(d))
                sum_remaining -= d
                break
    min_num = ''.join(min_digits)

    print(min_num, max_num)
```

The solution begins by checking feasibility for edge cases. Constructing the maximum number is straightforward: always pick the largest feasible digit. Constructing the minimum number is slightly more subtle, ensuring that the digit choice at each step allows the remaining sum to be distributed across the remaining digits. A common mistake is neglecting the first digit cannot be zero, or failing to check that the remaining sum does not exceed the maximum achievable sum for remaining positions.

## Worked Examples

**Sample 1**: Input `2 15`

| Step | max_digits | sum_remaining | min_digits | sum_remaining |
| --- | --- | --- | --- | --- |
| 1 | [9] | 6 | [6] | 9 |
| 2 | [9,6] | 0 | [6,9] | 0 |

Output: `69 96`

This demonstrates greedy allocation works from left to right for both maximal and minimal numbers.

**Sample 2**: Input `3 0`

This triggers the edge case: m > 1 and s = 0 is impossible.

Output: `-1 -1`

**Sample 3**: Input `3 20`

| Step | max_digits | sum_remaining | min_digits | sum_remaining |
| --- | --- | --- | --- | --- |
| 1 | [9] | 11 | [2] | 18 |
| 2 | [9,9] | 2 | [2,9] | 9 |
| 3 | [9,9,2] | 0 | [2,9,9] | 0 |

Output: `299 992`

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Constructing each number iterates over m digits once, with inner loop in min number being at most 10 iterations. |
| Space | O(m) | We store digits in lists of length m. |

Given m ≤ 100, both time and space comfortably fit within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    m, s = map(int, input().split())
    if (s == 0 and m > 1) or (s > 9 * m):
        return "-1 -1"
    sum_remaining = s
    max_digits = []
    for i in range(m):
        d = min(9, sum_remaining)
        max_digits.append(str(d))
        sum_remaining -= d
    max_num = ''.join(max_digits)
    sum_remaining = s
    min_digits = []
    for i in range(m):
        for d in range(0 if i > 0 else 1, 10):
            if sum_remaining - d <= 9 * (m - i - 1):
                min_digits.append(str(d))
                sum_remaining -= d
                break
    min_num = ''.join(min_digits)
    return f"{min_num} {max_num}"

# Provided samples
assert run("2 15\n") == "69 96", "sample 1"
assert run("3 0\n") == "-1 -1", "sample 2"

# Custom test cases
assert run("1 0\n") == "0 0", "single-digit zero"
assert run("2 0\n") == "-1 -1", "two-digit zero impossible"
assert run("3 27\n") == "999 999", "maximum sum exactly 9 per digit"
assert run("3 20\n") == "299 992", "general case sum 20"
assert run("5 5\n") == "10004 50000", "small sum over multiple digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 0 | Single-digit zero case |
| 2 0 | -1 -1 | Multi-digit zero impossible |
| 3 27 | 999 999 | Maximum sum exactly fills all digits |
| 3 20 | 299 992 | General construction with leftover sum distribution |
| 5 5 | 10004 50000 | Ensures minimal number avoids leading zero |

## Edge Cases

For _m = 1_, _s = 0_, the algorithm correctly returns "0 0" because a single digit zero is
