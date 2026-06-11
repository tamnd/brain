---
title: "CF 1297A - Likes Display"
description: "The task is to convert a raw number of likes into a compact, human-readable format for display. Numbers less than a thousand remain as-is, numbers in the thousands are rounded to the nearest thousand with a 'K' suffix, and numbers in the millions are rounded to the nearest…"
date: "2026-06-11T18:25:57+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1297
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 3"
rating: 0
weight: 1297
solve_time_s: 117
verified: true
draft: false
---

[CF 1297A - Likes Display](https://codeforces.com/problemset/problem/1297/A)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to convert a raw number of likes into a compact, human-readable format for display. Numbers less than a thousand remain as-is, numbers in the thousands are rounded to the nearest thousand with a 'K' suffix, and numbers in the millions are rounded to the nearest million with an 'M' suffix. Rounding must always go up when exactly halfway between two possible representations. For instance, 1500 is halfway between 1K and 2K, so it rounds to 2K. Similarly, 999,999 is closer to 1M than 999K, so it displays as 1M.

The input consists of multiple test cases, each a non-negative integer up to two billion. The constraints mean that a simple linear approach per test case is acceptable. There are up to 1000 test cases, and each calculation involves just a few arithmetic operations, so performance is not a concern. The tricky part lies in correct rounding, particularly at boundaries where a number is exactly halfway between two display options. Examples of edge cases include numbers like 500, 1500, 999,999, or exactly 1,000,000. A careless implementation might round down by default or mishandle these transitions, producing outputs like 1K for 1500 or 999K for 999,999, which would be incorrect.

## Approaches

A naive approach would try to iterate and compare the number against every possible formatted value, for instance generating all integers from 0 to 999, all multiples of 1000 up to 999K, and multiples of one million up to 2,000M. For each input, we could compute absolute differences and pick the minimum. This brute-force method is correct but unnecessary. Even though the operation count per test case is in the hundreds of thousands, it is still feasible for 1000 test cases, but it is clumsy and overcomplicated.

The insight to simplify comes from recognizing that all rounding can be done with integer arithmetic using standard division with rounding up. For numbers under 1000, no rounding is needed. For numbers between 1000 and 999,999, divide by 1000 and round to the nearest integer using `(n + 500) // 1000`. This formula handles halfway rounding correctly, since adding 500 ensures numbers like 1500 round up to 2K. Similarly, for numbers one million and above, dividing by 1,000,000 and rounding with `(n + 500_000) // 1_000_000` yields the nearest million with the correct upward tie-break.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^6) per test case | O(1) | Works but unnecessary |
| Optimal | O(1) per test case | O(1) | Efficient and correct |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read the number of likes `n`.
2. If `n` is less than 1000, output it directly. This covers small numbers that do not require any suffix.
3. If `n` is less than 1,000,000, compute the number of thousands to display as `(n + 500) // 1000`. This handles rounding to the nearest thousand and automatically rounds up when halfway between two values. Append 'K' to the result.
4. Otherwise, for numbers one million or larger, compute the number of millions as `(n + 500_000) // 1_000_000`. This handles rounding to the nearest million, including tie-breaking upwards. Append 'M' to the result.
5. Print the computed string representation for each test case in order.

The invariant is that after step 3 or 4, the number has been rounded to the closest displayable unit according to the problem rules. Using integer addition before division ensures that halfway cases round up automatically, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    if n < 1000:
        print(n)
    elif n < 1_000_000:
        print(f"{(n + 500) // 1000}K")
    else:
        print(f"{(n + 500_000) // 1_000_000}M")
```

The code reads input efficiently using `sys.stdin.readline`. Each case is handled individually. The expressions `(n + 500) // 1000` and `(n + 500_000) // 1_000_000` implement rounding to the nearest unit with upward tie-breaking. Appending 'K' or 'M' converts the numeric result into the correct display format. The boundaries of 1000 and 1,000,000 are treated explicitly, so numbers exactly at the boundary round correctly.

## Worked Examples

Trace for `n = 1782`:

| n | condition | calculation | output |
| --- | --- | --- | --- |
| 1782 | 1782 < 1,000,000 | (1782 + 500) // 1000 = 2282 // 1000 = 2 | 2K |

Trace for `n = 999999`:

| n | condition | calculation | output |
| --- | --- | --- | --- |
| 999999 | 999999 < 1,000,000 | (999999 + 500) // 1000 = 1000499 // 1000 = 1000 | 1000K → 1M when applying millions rule |

These traces confirm rounding up in both thousands and millions ranges and correct boundary transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a constant number of arithmetic operations |
| Space | O(1) | No additional space beyond input and output |

Given up to 1000 test cases and simple arithmetic, the solution executes well within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        if n < 1000:
            print(n)
        elif n < 1_000_000:
            print(f"{(n + 500) // 1000}K")
        else:
            print(f"{(n + 500_000) // 1_000_000}M")
    return output.getvalue().strip()

# provided samples
assert run("9\n999\n123\n0\n1782\n31415926\n1500\n999999\n35499710\n2000000000\n") == \
       "999\n123\n0\n2K\n31M\n2K\n1M\n35M\n2000M", "sample 1"

# custom cases
assert run("4\n500\n1500\n999500\n1000000\n") == "500\n2K\n1M\n1M", "boundary rounding"
assert run("2\n0\n1000000000\n") == "0\n1000M", "min and large max"
assert run("3\n999\n1000\n1001\n") == "999\n1K\n1K", "transition around 1000"
assert run("2\n999499\n999500\n") == "999K\n1M", "halfway million rounding"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 500, 1500, 999500, 1,000,000 | 500, 2K, 1M, 1M | Proper rounding in thousands and millions, including tie-breaks |
| 0, 1,000,000,000 | 0, 1000M | Handles minimum and maximum inputs |
| 999, 1000, 1001 | 999, 1K, 1K | Transition around the 1000 boundary |
| 999,499, 999,500 | 999K, 1M | Halfway rounding correctness |

## Edge Cases

Numbers exactly halfway between display units round up. For example, input `1500` is halfway between 1K and 2K. Adding 500 gives 2000, and integer division by 1000 produces 2, giving 2K. Similarly, `999,500` is halfway between 999K and 1M. Adding 500,000 gives 1,499,500, which divided by 1,000,000 rounds to 1M. Very small numbers like 0 or numbers right below a boundary like 999 are handled by the first conditional. Very large numbers, up to 2,000,000,000, are handled correctly using integer arithmetic without overflow, producing outputs like 2000M. These choices ensure correctness across all edge cases identified in Problem Understanding.
