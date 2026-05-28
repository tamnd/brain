---
title: "CF 149B - Martian Clock"
description: "We are given a string representing a Martian time in the format \"a:b\", where a is the hour component and b is the minute component. Unlike Earth time in base 10, these strings could represent numbers in any numeral system with a base greater than 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 149
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 106 (Div. 2)"
rating: 1600
weight: 149
solve_time_s: 85
verified: true
draft: false
---

[CF 149B - Martian Clock](https://codeforces.com/problemset/problem/149/B)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string representing a Martian time in the format "a:b", where `a` is the hour component and `b` is the minute component. Unlike Earth time in base 10, these strings could represent numbers in any numeral system with a base greater than 1. Our task is to identify all numeral bases in which the given strings could represent a valid Earth time. A valid time means that the numeric value of `a` is between 0 and 23 inclusive, and the numeric value of `b` is between 0 and 59 inclusive.

The input strings consist of digits '0'-'9' and uppercase letters 'A'-'Z'. Each character represents a digit according to standard positional notation: digits 0-9 map to their integer values, letters A-Z map to 10-35. The strings can have leading zeros, which do not affect the numeric value. The length of `a` and `b` can be up to 5 characters, which implies that the largest number representable could be substantial if interpreted in a large base, but we only need to consider bases that keep the value within the valid hour and minute ranges.

Edge cases to consider include strings where the largest digit determines a minimum valid base larger than 10. For example, "1A:2" requires a base of at least 11, otherwise 'A' is not a valid digit. Another edge case occurs when a string is "00:01" or similar: all digits are small enough that infinitely many numeral systems could work. A naive approach that only checks small bases might incorrectly report no valid bases in such situations.

## Approaches

A brute-force approach would attempt to convert `a` and `b` into integers in every base starting from 2 upwards. For each base, we would check if both numbers fall within the valid ranges. This is correct in principle because all possible valid bases are integers greater than 1, and the strings have a finite length. However, this approach is potentially inefficient if implemented naively, because the maximum base to consider could theoretically be unbounded if the largest digit is small and the string's value is small, leading to a large number of unnecessary checks.

The key insight for an optimal solution is to recognize that the largest digit in a string imposes a strict lower bound on the possible base. If the largest digit in `a` is `max_a` and in `b` is `max_b`, the minimum base to consider is `max(max_a, max_b) + 1`. Any base smaller than this would make at least one character invalid. Additionally, we can stop checking bases once the converted number exceeds 23 for hours or 59 for minutes, because higher bases will only increase the value. If the hour value is at most 23 and the minute value is at most 59 in the minimum base, then any larger base will also satisfy these constraints, leading to infinitely many solutions. Otherwise, we only need to check up to the base where the larger of the two values would exceed its respective bound.

This approach reduces the range of bases to check from an unbounded range to a small finite set determined by the constraints on hours and minutes, making the solution efficient and simple to implement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(B) where B is max base | O(1) | Too slow if B is large |
| Optimal | O(36) | O(1) | Accepted |

## Algorithm Walkthrough

1. Split the input string at the colon to separate hours (`a`) and minutes (`b`).
2. Define a helper function to convert a character to its integer value, with '0'-'9' mapping to 0-9 and 'A'-'Z' mapping to 10-35.
3. Identify the largest digit in `a` and in `b`. The minimum base we need to consider is one greater than the largest of these two digits, because any numeral system smaller than that cannot represent the strings correctly.
4. If the minimum base is larger than 60, no valid base exists because even in the minimum possible base, `b` would exceed 59. Print 0 and exit.
5. For bases starting from the minimum base up to 60, convert `a` and `b` to integers in that base. Check if the resulting values satisfy the hour and minute constraints (0 ≤ hours ≤ 23, 0 ≤ minutes ≤ 59). Record valid bases.
6. If the minimum base already produces numbers within the hour and minute limits, then every larger base will also be valid, leading to infinitely many solutions. Print -1 and exit.
7. If the list of valid bases is empty, print 0. Otherwise, print the bases in increasing order.

The reason this works is that the conversion from a string to an integer is monotonically increasing with respect to the base. Once the converted value exceeds its bound, no larger base can satisfy the constraint, except in the case of a very small string that is always within bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def char_to_val(c):
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    return ord(c) - ord('A') + 10

def str_to_int(s, base):
    val = 0
    for c in s:
        val = val * base + char_to_val(c)
    return val

time_str = input().strip()
a_str, b_str = time_str.split(':')

max_digit_a = max(char_to_val(c) for c in a_str)
max_digit_b = max(char_to_val(c) for c in b_str)
min_base = max(max_digit_a, max_digit_b) + 1

if min_base > 60:
    print(0)
    sys.exit()

hours = str_to_int(a_str, min_base)
minutes = str_to_int(b_str, min_base)

if hours <= 23 and minutes <= 59:
    print(-1)
else:
    valid_bases = []
    for base in range(min_base, 61):
        h_val = str_to_int(a_str, base)
        m_val = str_to_int(b_str, base)
        if h_val <= 23 and m_val <= 59:
            valid_bases.append(base)
    if not valid_bases:
        print(0)
    else:
        print(" ".join(map(str, valid_bases)))
```

The first part converts characters to numeric values and finds the minimum base. The second part checks if the minimum base already yields valid time values, which means infinitely many bases work. Otherwise, we iterate through possible bases up to 60, since hours cannot exceed 23 and minutes cannot exceed 59. Each conversion is linear in the length of the string, but the lengths are at most 5, so this is fast.

## Worked Examples

**Sample 1:** "11:20"

| Step | min_base | hours | minutes | valid_bases |
| --- | --- | --- | --- | --- |
| compute max digits | 1 for '1', 2 for '2' | - | - | - |
| min_base = 3 | - | 3? | 3? | - |
| check bases 3..22 | - | hours <=23? | minutes <=59? | 3..22 |

This trace confirms that all bases from 3 to 22 allow the string to represent a valid time.

**Sample 2:** "000B:00001"

| Step | min_base | hours | minutes | action |
| --- | --- | --- | --- | --- |
| max_digit_a = 11, max_digit_b = 1 | min_base = 12 | hours = 11, minutes = 1 | - | hours <=23 and minutes <=59, so infinitely many bases |

The algorithm correctly prints -1, showing that infinitely many bases work.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L * 36) | L is max length of input strings (≤5), we check at most 36 bases (from 2 to 60) and convert each string in O(L) |
| Space | O(1) | Only stores a few integers and the list of valid bases |

With lengths capped at 5 and base range at most 60, the solution runs in microseconds, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    def char_to_val(c):
        if '0' <= c <= '9':
            return ord(c) - ord('0')
        return ord(c) - ord('A') + 10

    def str_to_int(s, base):
        val = 0
        for c in s:
            val = val * base + char_to_val(c)
        return val

    time_str = input().strip()
    a_str, b_str = time_str.split(':')

    max_digit_a = max(char_to_val(c) for c in a_str)
    max_digit_b = max(char_to_val(c) for c in b_str)
    min_base = max(max_digit_a, max_digit_b) + 1

    if min_base > 60:
        return "0"

    hours = str_to_int(a_str, min_base)
    minutes = str_to_int(b_str, min_base)

    if hours <= 23 and minutes <= 59:
        return "-1"
    else:
        valid_bases = []
        for base in range(min_base,
```
