---
title: "CF 345C - Counting Fridays"
description: "We are given a small list of contest dates. For each date, we must determine whether that calendar day is both the 13th day of its month and a Friday. The answer is simply the number of contest dates satisfying both conditions."
date: "2026-06-07T15:45:28+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "C"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 2000
weight: 345
solve_time_s: 103
verified: true
draft: false
---

[CF 345C - Counting Fridays](https://codeforces.com/problemset/problem/345/C)

**Rating:** 2000  
**Tags:** *special  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small list of contest dates. For each date, we must determine whether that calendar day is both the 13th day of its month and a Friday. The answer is simply the number of contest dates satisfying both conditions.

The year range is from 1974 to 2030, and the number of dates is at most 10. These constraints are tiny. Even an algorithm that performs a substantial amount of calendar computation for every query would comfortably fit within the limits. The real challenge is not efficiency but correctly determining the weekday of a given date, including leap years and varying month lengths.

A common mistake is to check only whether the day number equals 13. Consider:

```
1
2013-09-13
```

The correct output is:

```
1
```

because September 13, 2013 was a Friday. Ignoring the weekday would count every 13th regardless of whether it was Friday.

Another easy mistake is mishandling leap years. Consider:

```
1
2012-02-13
```

The correct output is:

```
0
```

Any weekday computation that forgets that 2012 is a leap year may produce the wrong weekday and incorrectly count this date.

A third subtle case is duplicate contest dates:

```
3
2012-01-13
2012-01-13
2012-01-13
```

The correct output is:

```
3
```

Each contest must be counted independently. The statement explicitly allows multiple contests on the same day.

## Approaches

The most direct solution is to determine the weekday of every given date and count how many are Fridays occurring on the 13th day of a month.

A brute-force way to determine weekdays is to choose a known reference date and simulate day by day until reaching the target date. This works because weekdays repeat every seven days. If the reference date is decades away, each query may require traversing tens of thousands of days. The maximum span in this problem is roughly 56 years, or about 20,000 days. With only ten queries, this is still perfectly acceptable, but it is unnecessarily cumbersome.

The key observation is that weekday computation has well-known closed-form formulas. Since the date range is fixed and small, we can directly compute the weekday of a given date using Zeller's congruence. The formula automatically handles leap years and month lengths through arithmetic, avoiding any simulation.

For each input date, we first check whether the day component is 13. If not, the date cannot be a Friday the 13th. If it is 13, we compute its weekday using Zeller's congruence. The formula returns a code representing the weekday, and we count the date if the code corresponds to Friday.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · D) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

Here, $D$ is the number of days between the reference date and the queried date.

## Algorithm Walkthrough

1. Read the number of contest dates.
2. For each date string, extract the year, month, and day.
3. If the day is not 13, skip this date immediately.

No date can be a Friday the 13th unless its day-of-month equals 13.
4. Compute the weekday using Zeller's congruence.

For January and February, treat them as months 13 and 14 of the previous year. This is part of the formula's definition.
5. Let $K$ be the year within the century and $J$ be the zero-based century.
6. Evaluate Zeller's formula:

$$h =
\left(
q +
\left\lfloor \frac{13(m+1)}{5} \right\rfloor +
K +
\left\lfloor \frac{K}{4} \right\rfloor +
\left\lfloor \frac{J}{4} \right\rfloor +
5J
\right)
\bmod 7$$

where $q$ is the day of the month.
7. In Zeller's numbering, Friday corresponds to $h = 6$.
8. If $h = 6$, increment the answer.
9. After processing all dates, print the answer.

### Why it works

Zeller's congruence is a mathematically proven formula that maps every valid Gregorian calendar date to its weekday. The transformation of January and February into months 13 and 14 of the previous year is built into the derivation and guarantees correct leap-year handling.

The algorithm counts a date only when two conditions hold simultaneously: the day-of-month equals 13 and the computed weekday equals Friday. Since the weekday computation is correct for every valid input date, every counted date is a genuine Friday the 13th, and every Friday the 13th in the input is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_friday_13(year, month, day):
    if day != 13:
        return False

    if month <= 2:
        month += 12
        year -= 1

    q = day
    K = year % 100
    J = year // 100

    h = (
        q
        + (13 * (month + 1)) // 5
        + K
        + K // 4
        + J // 4
        + 5 * J
    ) % 7

    return h == 6  # Friday in Zeller's congruence

def solve():
    n = int(input())
    ans = 0

    for _ in range(n):
        s = input().strip()
        y, m, d = map(int, s.split('-'))

        if is_friday_13(y, m, d):
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates weekday computation into a helper function. The first check is whether the day equals 13. This avoids unnecessary arithmetic for dates that can never contribute to the answer.

The month adjustment for January and February is easy to overlook. Zeller's congruence treats them as months 13 and 14 of the previous year. Forgetting this transformation produces incorrect weekdays near the start of the year.

All arithmetic fits comfortably inside standard Python integers. No special handling for leap years is needed because the formula already incorporates the Gregorian calendar rules.

## Worked Examples

### Sample 1

Input:

```
5
2012-01-13
2012-09-13
2012-11-20
2013-09-13
2013-09-20
```

| Date | Day = 13? | Weekday | Counted? |
| --- | --- | --- | --- |
| 2012-01-13 | Yes | Friday | Yes |
| 2012-09-13 | Yes | Thursday | No |
| 2012-11-20 | No | Not checked | No |
| 2013-09-13 | Yes | Friday | Yes |
| 2013-09-20 | No | Not checked | No |

Final answer:

```
2
```

This trace shows that having day 13 is not sufficient. The weekday must also be Friday.

### Custom Example

Input:

```
4
2015-02-13
2015-03-13
2015-03-20
2015-11-13
```

| Date | Day = 13? | Weekday | Counted? |
| --- | --- | --- | --- |
| 2015-02-13 | Yes | Friday | Yes |
| 2015-03-13 | Yes | Friday | Yes |
| 2015-03-20 | No | Not checked | No |
| 2015-11-13 | Yes | Friday | Yes |

Final answer:

```
3
```

This example demonstrates that multiple Friday-the-13th dates can occur within the same year and all must be counted independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Constant-time weekday computation for each date |
| Space | O(1) | Only a few variables are stored |

With at most ten dates, the running time is effectively instantaneous. The memory usage is constant and far below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def is_friday_13(year, month, day):
    if day != 13:
        return False

    if month <= 2:
        month += 12
        year -= 1

    q = day
    K = year % 100
    J = year // 100

    h = (
        q
        + (13 * (month + 1)) // 5
        + K
        + K // 4
        + J // 4
        + 5 * J
    ) % 7

    return h == 6

def solve():
    n = int(input())
    ans = 0

    for _ in range(n):
        y, m, d = map(int, input().strip().split('-'))
        if is_friday_13(y, m, d):
            ans += 1

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""5
2012-01-13
2012-09-13
2012-11-20
2013-09-13
2013-09-20
"""
) == "2\n", "sample 1"

# minimum size input
assert run(
"""1
2012-01-13
"""
) == "1\n", "single Friday the 13th"

# duplicate dates
assert run(
"""3
2012-01-13
2012-01-13
2012-01-13
"""
) == "3\n", "duplicates counted separately"

# no date with day 13
assert run(
"""4
2012-01-12
2012-01-14
2012-09-20
2012-11-20
"""
) == "0\n", "day must equal 13"

# leap year related date
assert run(
"""1
2012-02-13
"""
) == "0\n", "correct leap-year weekday handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single date 2012-01-13 | 1 | Minimum input size |
| Three copies of 2012-01-13 | 3 | Duplicate contests are counted independently |
| No date has day 13 | 0 | Early rejection logic |
| 2012-02-13 | 0 | Leap-year handling and weekday computation |

## Edge Cases

### Duplicate Contest Dates

Input:

```
3
2012-01-13
2012-01-13
2012-01-13
```

The algorithm processes each line independently. Every occurrence has day 13 and evaluates to Friday. The counter increases three times, producing:

```
3
```

No deduplication is performed, which matches the problem requirements.

### Leap-Year Dates

Input:

```
1
2012-02-13
```

The day equals 13, so the algorithm computes the weekday. February is converted to month 14 of year 2011 before applying Zeller's formula. The computed weekday is Monday, not Friday, so the answer is:

```
0
```

This verifies that leap-year-sensitive dates are handled correctly.

### Dates That Are the 13th but Not Friday

Input:

```
1
2012-09-13
```

The day-of-month condition succeeds. The weekday computation returns Thursday. Since the weekday is not Friday, the counter remains zero:

```
0
```

This confirms that both conditions are required.

### Dates That Are Friday but Not the 13th

Input:

```
1
2013-09-20
```

The day-of-month is 20, so the algorithm immediately skips weekday checking. The answer is:

```
0
```

A Friday alone is insufficient. The date must specifically be Friday the 13th.
