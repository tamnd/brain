---
title: "CF 105383J - Just Round Down"
description: "We are given a single positive real number written as a string with a decimal point. The task is to compute its floor, meaning the greatest integer that does not exceed the value, and output that integer without any decimal part."
date: "2026-06-23T05:26:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105383
codeforces_index: "J"
codeforces_contest_name: "2024 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 105383
solve_time_s: 49
verified: true
draft: false
---

[CF 105383J - Just Round Down](https://codeforces.com/problemset/problem/105383/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive real number written as a string with a decimal point. The task is to compute its floor, meaning the greatest integer that does not exceed the value, and output that integer without any decimal part.

The input format is intentionally minimal, just one line like `1999.99`, `2.00000`, or potentially values such as `0.123`. The structure guarantees exactly one decimal point and at least one digit on both sides of it. The value is bounded above by 10^8, but since the input is a string, the real constraint that matters is that it fits comfortably in memory and can be processed character by character.

From a complexity standpoint, the input size is capped at 15 bytes, which immediately rules out any need for parsing libraries or high-performance numeric algorithms. Any solution that scans the string once is sufficient. Even an O(n) approach with constant work per character is trivially fast.

The main subtlety is that floating-point parsing in programming languages is not something we should rely on here. Converting to float and then applying a floor function risks precision errors for larger or awkward decimal representations. A string-based approach avoids this entirely.

Edge cases appear in two forms. First, numbers that are already integers but written with trailing zeros after the decimal point. For example, `2.00000` should output `2`. A naive float conversion might produce `1` if rounding errors occur, though in most languages this specific input is safe, but it is still unnecessary risk.

Second, numbers smaller than 1 such as `0.99999` or `0.12345`. In these cases, the floor is `0`. A naive approach that incorrectly extracts the integer part as a number and assumes it is nonzero would fail if it tries to interpret the string improperly.

A third subtle case is extremely large integer parts like `100000000.000`, where correctness depends on preserving the integer substring exactly without overflow or formatting changes.

## Approaches

The brute-force idea is to treat the input as a real number: convert the string into a floating-point value, apply a floor operation, and print the result. This works in the sense that it matches the mathematical definition, and for many typical cases it will pass.

However, this approach relies on binary floating-point representation. Numbers like `1999.99` are not exactly representable in binary, so intermediate rounding can introduce tiny errors. While these errors are usually invisible, floor operations are sensitive to them because a value like `1.99999999997` might be correctly interpreted as `1`, but a slightly misrepresented boundary case could shift unexpectedly.

More importantly, this problem does not require any arithmetic at all. The structure of the input already encodes the answer directly: everything before the decimal point is the integer part, and floor ignores everything after it.

The key observation is that for any positive decimal written in standard form, the floor is exactly the substring before the decimal point interpreted as an integer. No further computation is necessary.

This reduces the task from numeric computation to string parsing, eliminating precision risks entirely and reducing the solution to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (float conversion + floor) | O(n) | O(1) | Risky / unnecessary |
| Optimal (string parsing) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We construct the result directly from the input string.

1. Read the input string.
2. Scan the string until the decimal point is encountered.
3. Extract all characters before the decimal point.
4. Output this substring as an integer.

Each step is justified by the structure of decimal representation. The decimal point is the exact separator between integer and fractional parts, so everything after it is irrelevant for flooring.

### Why it works

The floor of a positive decimal number depends only on how many whole units are fully contained in the value. The digits before the decimal point encode exactly that quantity. The fractional part, regardless of magnitude, cannot increase the floor value, because it is always strictly less than 1. Therefore, discarding the fractional part preserves the correct integer result in all valid inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

i = 0
while i < len(s) and s[i] != '.':
    i += 1

print(int(s[:i]))
```

The solution reads the input as a string and scans until it finds the decimal point. Everything before that point is the integer part. Converting that substring to an integer automatically handles cases like leading zeros if they exist, although the problem guarantees no leading zeros for numbers greater than or equal to 1.

The important implementation detail is avoiding any floating-point conversion. Even though Python handles these safely for many inputs, the string approach is deterministic and aligns exactly with the definition of floor.

## Worked Examples

### Example 1: `1999.99`

We scan the string until the decimal point and isolate the prefix.

| Step | Index | Character | Prefix |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 9 | 19 |
| 3 | 2 | 9 | 199 |
| 4 | 3 | 9 | 1999 |
| 5 | 4 | . | stop |

The extracted prefix is `1999`, which is printed. The fractional part `.99` is irrelevant to the floor because it is strictly less than 1.

### Example 2: `2.00000`

| Step | Index | Character | Prefix |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 2 |
| 2 | 1 | . | stop |

The prefix is `2`, so the output is `2`. Even though the fractional part is long, it contributes nothing to the integer floor.

These examples confirm that the algorithm depends only on locating the decimal separator and ignoring everything after it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass until the decimal point is found |
| Space | O(1) | Only indices and substring reference are used |

The input size is at most 15 characters, so even a linear scan is effectively constant time. The solution is well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    i = 0
    while i < len(s) and s[i] != '.':
        i += 1
    return str(int(s[:i]))

# provided samples
assert run("1999.99\n") == "1999"
assert run("2.00000\n") == "2"

# custom cases
assert run("0.123\n") == "0", "fraction less than 1"
assert run("100.999\n") == "100", "normal rounding down behavior"
assert run("7.0\n") == "7", "integer represented as float"
assert run("99999999.999\n") == "99999999", "large integer part boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0.123 | 0 | values below 1 |
| 100.999 | 100 | fractional truncation |
| 7.0 | 7 | integer-like floats |
| 99999999.999 | 99999999 | large boundary integer |

## Edge Cases

One edge case is numbers less than 1 such as `0.123`. The algorithm scans until the decimal point and produces an empty prefix if the number starts with `0.`. Converting `0` correctly yields the floor, which is `0`.

Another case is inputs like `2.00000`, where the fractional part is non-empty but entirely zero. The scan stops at the decimal point and ignores all trailing zeros. The integer prefix `2` correctly represents the floor.

A larger integer boundary case such as `99999999.999` demonstrates that no overflow or floating-point conversion is needed. The prefix is safely extracted as a string and converted to an integer without precision loss.

Across all cases, the key invariant is that the substring before the decimal point always equals the mathematical floor of the number for all valid inputs in standard decimal representation.
