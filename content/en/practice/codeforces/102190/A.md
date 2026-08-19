---
title: "CF 102190A - standard input/output"
description: "The input is a compact representation of a weekly work schedule. It consists of three integers written consecutively: s, the hour when work starts in the morning, t, the hour when work ends in the afternoon, and d, the number of working days in a week."
date: "2026-08-20T00:42:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102190
codeforces_index: "A"
codeforces_contest_name: "2019 ECNU Campus Invitational Contest"
rating: 0
weight: 102190
solve_time_s: 93
verified: true
draft: false
---

[CF 102190A - standard input/output](https://codeforces.com/problemset/problem/102190/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a compact representation of a weekly work schedule. It consists of three integers written consecutively: `s`, the hour when work starts in the morning, `t`, the hour when work ends in the afternoon, and `d`, the number of working days in a week. Since both `s` and `t` are guaranteed to be between 2 and 11, they each occupy exactly two decimal digits, while `d` is a single digit.

For example, `996` represents starting at 9 a.m., finishing at 9 p.m., and working 6 days a week. A workday then lasts `t - s + 12` hours, because the starting time is in the morning and the ending time is in the afternoon. The required output is this daily duration multiplied by the number of working days.

The bounds are deliberately tiny. There is only one input line and the three values have fixed lengths, so there is no large input size to optimize around. Even a solution that tried every possible value of `s`, `t`, and `d` would examine at most `10 * 10 * 7 = 700` combinations, which is effectively constant time. The direct parsing solution is even simpler and performs only a handful of arithmetic operations.

The main edge case is when the starting and ending clock numbers are equal. An input such as `996` does not mean zero hours per day. It means 9 a.m. to 9 p.m., which is 12 hours. A careless solution using only `t - s` would output `0`, while the correct weekly total is `12 * 6 = 72`.

Another boundary case is the smallest permitted hours. For `221`, the schedule is 2 a.m. to 2 p.m. for one day. The duration is 12 hours, so the answer is `12`. Again, simply computing `t - s` would incorrectly produce zero.

At the other end, `1117` means 11 a.m. to 11 p.m. for 7 days. The daily duration is still 12 hours, giving `84` hours per week. The fact that the hour is 11 rather than 2 does not change the calculation when the two clock values are equal.

## Approaches

A brute-force solution could generate every valid triple `(s, t, d)`, construct its decimal representation, and compare it with the input. There are at most 10 choices for `s`, 10 choices for `t`, and 7 choices for `d`, so the worst case contains exactly 700 candidate triples. Once the matching triple is found, its weekly duration can be calculated directly. This approach is correct because the constraints guarantee that the input corresponds to exactly one valid interpretation.

The brute-force approach is already fast enough for these constraints, but it performs unnecessary work. The structure of the input gives us a direct way to recover the three values. Since `s` and `t` are always two digits and `d` is always one digit, the first two characters are `s`, the next two are `t`, and the final character is `d`.

The key observation is how to calculate the length of a workday. The interval starts in the morning and ends in the afternoon. From `s` a.m. to 12 p.m. takes `12 - s` hours, followed by `t` hours from 12 p.m. to `t` p.m. Their sum is

`(12 - s) + t = 12 + t - s`.

Multiplying this duration by `d` gives the total number of working hours in the week. The brute-force solution works because the search space is tiny, but the fixed-width encoding lets us reduce the entire problem to constant-time parsing and arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(700) = O(1) | O(1) | Accepted |
| Direct Parsing | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input as a string. Keeping it as a string makes the fixed positions of `s`, `t`, and `d` explicit.
2. Convert the first two characters to an integer and call it `s`. These are exactly the two digits representing the morning starting hour.
3. Convert the next two characters to an integer and call it `t`. These are exactly the two digits representing the afternoon ending hour.
4. Convert the final character to an integer and call it `d`. It represents the number of working days.
5. Compute the duration of one working day as `12 + t - s`. This accounts for crossing noon, so equal hour values correctly produce a 12-hour workday.
6. Multiply the daily duration by `d` and print the result, because the same schedule is used on every working day.

The correctness follows from the fixed-width encoding and the time interval formula. The first four characters uniquely determine `s` and `t`, while the last character determines `d`. For any valid `s` and `t`, the elapsed time from `s` a.m. to `t` p.m. is exactly `12 + t - s`. Thus the algorithm computes the exact duration of each working day and multiplies it by exactly the number of working days, so its output is the required weekly working time.

## Python Solution

```python
import sys
input = sys.stdin.readline

std = input().strip()

s = int(std[:2])
t = int(std[2:4])
d = int(std[4])

daily_hours = 12 + t - s
weekly_hours = daily_hours * d

print(weekly_hours)
```

The input is kept as a string because its format is positional. Slicing `std[:2]` extracts the two digits of `s`, while `std[2:4]` extracts the two digits of `t`. The final character is converted directly into `d`.

The expression `12 + t - s` is preferable to trying to reason about separate cases such as `s == t` or `s < t`. The noon crossing is always present because the starting time is in the morning and the ending time is in the afternoon. With `s = 9` and `t = 9`, for example, the formula gives `12`, exactly as required.

There is no integer overflow concern in Python, and the largest possible answer is only `84`. There are also no off-by-one issues because the calculation deals with elapsed hours rather than counting clock labels.

## Worked Examples

The statement as provided does not contain actual sample input and output pairs, so the following two traces use representative valid inputs.

For `996`, the schedule is 9 a.m. to 9 p.m. for 6 days.

| `std` | `s` | `t` | `d` | `daily_hours` | `weekly_hours` |
| --- | --- | --- | --- | --- | --- |
| `996` | 9 | 9 | 6 | 12 | 72 |

The equal values of `s` and `t` exercise the most common mistake. The workday is not zero hours because the two values refer to different halves of the day.

For `251`, the schedule is 2 a.m. to 11 p.m. for 1 day.

| `std` | `s` | `t` | `d` | `daily_hours` | `weekly_hours` |
| --- | --- | --- | --- | --- | --- |
| `251` | 2 | 5 | 1 | 15 | 15 |

Here the input is parsed as `s = 2`, `t = 5`, `d = 1`, so the daily duration is `12 + 5 - 2 = 15`. The trace also confirms that the final digit belongs entirely to `d` and is not part of the ending hour.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The input always contains exactly five characters, followed by a constant number of arithmetic operations. |
| Space | O(1) | Only the input string and a few integer variables are stored. |

The constraints make the constant-time solution more than sufficient. Even the brute-force search has only 700 possible triples, but direct parsing avoids that unnecessary enumeration and matches the structure of the input exactly.

## Test Cases

Because the original statement contains no visible sample pairs, the test suite below uses the examples from the explanation together with boundary cases.

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    std = input().strip()

    s = int(std[:2])
    t = int(std[2:4])
    d = int(std[4])

    daily_hours = 12 + t - s
    print(daily_hours * d)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("996\n") == "72", "equal start and end hour"
assert run("251\n") == "15", "representative schedule"
assert run("221\n") == "12", "minimum hour values"
assert run("1117\n") == "84", "maximum values"
assert run("231\n") == "13", "off-by-one check"
assert run("1187\n") == "84", "equal maximum hour values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `996` | `72` | Equal morning and afternoon clock values |
| `251` | `15` | Ordinary non-equal schedule |
| `221` | `12` | Minimum permitted `s` and `t` |
| `1117` | `84` | Maximum permitted values and maximum `d` |
| `231` | `13` | Difference calculation and boundary around the hour values |
| `1187` | `84` | Equal maximum clock values with seven working days |

## Edge Cases

For `996`, the algorithm reads `s = 9`, `t = 9`, and `d = 6`. It computes `daily_hours = 12 + 9 - 9 = 12`, then outputs `12 * 6 = 72`. This handles the distinction between 9 a.m. and 9 p.m. without any special case.

For `221`, the algorithm reads `s = 2`, `t = 2`, and `d = 1`. The duration becomes `12 + 2 - 2 = 12`, so the output is `12`. This confirms that the lower boundary does not require separate handling.

For `1117`, the algorithm parses `s = 11`, `t = 11`, and `d = 7`. The daily duration is `12 + 11 - 11 = 12`, and the weekly total is `12 * 7 = 84`. This covers the upper bounds and also confirms that the final digit is correctly treated as the number of working days.

The input `231` is useful for catching an implementation that accidentally counts the endpoint as an extra hour. Here `s = 2` and `t = 3`, so the elapsed time is `12 + 3 - 2 = 13`, not 14. The program consequently prints `13`, matching the actual interval from 2 a.m. to 3 p.m.
