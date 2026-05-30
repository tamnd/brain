---
title: "CF 1950C - Clock Conversion"
description: "We are given times expressed in the 24-hour clock format, for example 00:00 for midnight, 13:45 for one forty-five in the afternoon, or 23:59 for one minute before midnight. Our task is to convert each time into the 12-hour clock format, which uses the familiar AM and PM labels."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1950
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 937 (Div. 4)"
rating: 800
weight: 1950
solve_time_s: 51
verified: true
draft: false
---

[CF 1950C - Clock Conversion](https://codeforces.com/problemset/problem/1950/C)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given times expressed in the 24-hour clock format, for example `00:00` for midnight, `13:45` for one forty-five in the afternoon, or `23:59` for one minute before midnight. Our task is to convert each time into the 12-hour clock format, which uses the familiar AM and PM labels. In this system, midnight corresponds to `12:00 AM`, noon corresponds to `12:00 PM`, and hours from 1 to 11 are simply labeled AM in the morning or PM in the afternoon. The minutes remain unchanged.

The input provides up to 1440 test cases, each consisting of a single string in the format `hh:mm`. Each `hh` is between `00` and `23` and `mm` is between `00` and `59`. Because each operation on a single string is constant time, the maximum number of operations is roughly linear in the number of test cases. This is manageable under a 1-second time limit, so we do not need any advanced optimizations.

Non-obvious edge cases appear when the hour is at the boundaries of the AM/PM split. Specifically, `00:mm` must become `12:mm AM` and `12:mm` must become `12:mm PM`. Naive approaches that simply subtract 12 from hours above 12 or leave hours unchanged will misclassify these cases. For example, `00:59` must convert to `12:59 AM`, not `00:59 AM`, and `12:14` must convert to `12:14 PM`, not `00:14 PM`.

## Approaches

The brute-force approach reads each input time, splits the hour and minute, and applies a series of conditional rules. We would check if the hour is zero, twelve, or greater than twelve, and adjust both the hour and the AM/PM suffix accordingly. Each time conversion is constant time, so even with the maximum of 1440 test cases, this brute-force method will run efficiently. There is no algorithmic bottleneck.

The key insight that simplifies the implementation is that the conversion rules for the hour are straightforward arithmetic. For hours 1 through 11, the AM/PM label depends only on whether the original hour is less than 12 (AM) or 12 or greater (PM). Midnight and noon are the only special cases where we need to output 12 instead of 0 or leave the hour unchanged. Once we identify these two cases explicitly, all other hours follow the simple formula `hour % 12` for 1-11 PM and no change for AM.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t) | O(1) | Accepted |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, `t`, from input. Each test case represents one time string.
2. For each test case, read the string `s` in format `hh:mm`. Split it into `hh` and `mm` as integers.
3. Check if the hour is zero. If so, set the 12-hour hour to 12 and label it AM.
4. Check if the hour is exactly 12. If so, leave the hour as 12 and label it PM.
5. If the hour is greater than 12, subtract 12 from the hour to convert it to the 12-hour equivalent and label it PM.
6. If the hour is between 1 and 11 inclusive, leave it unchanged and label it AM.
7. Format the hour and minute as two-digit strings to preserve leading zeros.
8. Print the formatted string with the appropriate AM or PM suffix.

Why it works: At each step, the conversion follows the explicit definition of the 12-hour clock. Midnight and noon are handled as exceptions, while other hours are simply mapped using arithmetic modulo 12. This guarantees that all valid 24-hour times are converted correctly and consistently.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    hh, mm = map(int, s.split(":"))
    if hh == 0:
        period = "AM"
        hh_12 = 12
    elif hh == 12:
        period = "PM"
        hh_12 = 12
    elif hh > 12:
        period = "PM"
        hh_12 = hh - 12
    else:
        period = "AM"
        hh_12 = hh
    print(f"{hh_12:02d}:{mm:02d} {period}")
```

The solution reads each test case, converts the string hours and minutes into integers, and applies the AM/PM conversion rules. We explicitly handle `hh = 0` and `hh = 12` to avoid off-by-one mistakes. The format string `"{hh_12:02d}:{mm:02d}"` ensures that leading zeros are preserved, which is critical for 12-hour clock notation.

## Worked Examples

Consider the input `00:59`:

| hh | mm | hh_12 | period | Output |
| --- | --- | --- | --- | --- |
| 0 | 59 | 12 | AM | 12:59 AM |

The conversion correctly maps midnight to 12 AM.

For input `18:06`:

| hh | mm | hh_12 | period | Output |
| --- | --- | --- | --- | --- |
| 18 | 6 | 6 | PM | 06:06 PM |

The hour 18 is greater than 12, so subtracting 12 gives 6, and the label is PM.

These traces confirm that boundary conditions and general cases are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time |
| Space | O(1) | Only a few variables per test case are needed; no extra data structures are used |

With up to 1440 test cases, this is well within the 1-second time limit and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        s = input().strip()
        hh, mm = map(int, s.split(":"))
        if hh == 0:
            period = "AM"
            hh_12 = 12
        elif hh == 12:
            period = "PM"
            hh_12 = 12
        elif hh > 12:
            period = "PM"
            hh_12 = hh - 12
        else:
            period = "AM"
            hh_12 = hh
        print(f"{hh_12:02d}:{mm:02d} {period}")
    return out.getvalue().strip()

# Provided samples
assert run("11\n09:41\n18:06\n12:14\n00:59\n00:00\n14:34\n01:01\n19:07\n11:59\n12:00\n21:37\n") == \
"""09:41 AM
06:06 PM
12:14 PM
12:59 AM
12:00 AM
02:34 PM
01:01 AM
07:07 PM
11:59 AM
12:00 PM
09:37 PM"""

# Custom cases
assert run("3\n00:00\n12:00\n23:59\n") == "12:00 AM\n12:00 PM\n11:59 PM", "boundary times"
assert run("2\n01:05\n13:05\n") == "01:05 AM\n01:05 PM", "simple AM/PM mapping"
assert run("2\n11:11\n22:22\n") == "11:11 AM\n10:22 PM", "before noon and evening"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 00:00, 12:00, 23:59 | 12:00 AM, 12:00 PM, 11:59 PM | Midnight, noon, and last minute edge cases |
| 01:05, 13:05 | 01:05 AM, 01:05 PM | AM vs PM for same numerical hour |
| 11:11, 22:22 | 11:11 AM, 10:22 PM | Hours just before noon and evening conversion |

## Edge Cases

For `00:00`, the algorithm sets `hh_12` to 12 and period to AM. The formatted string becomes `12:00 AM`. For `12:00`, `hh_12` remains 12 and the period is PM, giving `12:00 PM`. These cases would fail if we naively applied `hh % 12` without handling zero. For `23:59`, subtracting 12 produces 11 and period PM, giving `11:59 PM`, confirming correct afternoon-to-evening mapping. The traces show the algorithm consistently produces correct 12-hour outputs for all boundary times.
