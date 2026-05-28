---
title: "CF 153D - Date Change"
description: "We are asked to manipulate dates by adding or subtracting a number of days. The input consists of a date string in the \"DD.MM.YYYY\" format and an integer representing a shift in days, which can be positive or negative."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 153
codeforces_index: "D"
codeforces_contest_name: "Surprise Language Round 5"
rating: 2000
weight: 153
solve_time_s: 76
verified: true
draft: false
---

[CF 153D - Date Change](https://codeforces.com/problemset/problem/153/D)

**Rating:** 2000  
**Tags:** *special  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to manipulate dates by adding or subtracting a number of days. The input consists of a date string in the "DD.MM.YYYY" format and an integer representing a shift in days, which can be positive or negative. The output is a date string in the same format representing the original date shifted by that many days. Conceptually, the problem reduces to moving forward or backward along a calendar while respecting month lengths and leap years.

The constraints are relatively small: the shift is limited to ±1000 days, and the input year is always between 1980 and 2020. This means we do not need to optimize for extremely large ranges; operations proportional to the number of days are feasible. However, naive implementations often fail on boundary cases like month-end transitions, leap days in February, and negative shifts. For example, starting at "28.02.2012" with a shift of 1 should yield "29.02.2012", and a shift of 2 should give "01.03.2012". A careless approach that ignores leap years would produce "01.03.2012" for both.

Negative shifts also require careful handling. If the input is "01.03.2012" and the shift is -1, the correct output is "29.02.2012", not "28.02.2012" as a naive calculation might produce. These edge cases show that month lengths and leap year rules must be applied explicitly or via a reliable date library.

## Approaches

The brute-force approach is straightforward: convert the date string into separate day, month, and year integers, then increment or decrement the day one at a time, adjusting the month and year whenever the day exceeds the number of days in the month or drops below one. This approach is correct because it explicitly simulates the calendar, but it has a worst-case time complexity of O(|shift|), which is acceptable here since |shift| ≤ 1000, but would be too slow if shifts were, for example, millions.

The optimal approach leverages Python's built-in `datetime` module, which internally handles leap years, month boundaries, and negative shifts. This removes the need for manual date arithmetic and edge-case handling. The key insight is that `datetime.date` objects can be safely combined with `datetime.timedelta` objects representing a number of days. Adding a positive or negative `timedelta` automatically computes the resulting day, month, and year correctly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | shift | ) |
| Optimal | O(1) | O(1) | Accepted, concise, handles all edge cases |

## Algorithm Walkthrough

1. Read the input date string and split it into day, month, and year integers using string slicing or splitting on the period character. This converts "DD.MM.YYYY" into three integers for computation.
2. Read the shift value as an integer. This value can be positive or negative, representing forward or backward movement on the calendar.
3. Create a `datetime.date` object using the parsed year, month, and day. This object represents the exact input date.
4. Create a `datetime.timedelta` object with the number of days equal to the shift. `timedelta` supports negative values natively.
5. Add the `timedelta` to the `date` object. Python internally calculates the resulting date, correctly handling month transitions, leap years, and negative shifts.
6. Format the resulting date object back into a string in "DD.MM.YYYY" format, ensuring two digits for day and month and four digits for year. This preserves the required output format.

The reason this works is that Python's `datetime` module guarantees that arithmetic on `date` objects respects all calendar rules, including leap years. There is no need to manually track days in a month or adjust for February 29, which eliminates potential off-by-one errors.

## Python Solution

```python
import sys
import datetime
input = sys.stdin.readline

date_str = input().strip()
shift = int(input().strip())

day, month, year = map(int, date_str.split('.'))
current_date = datetime.date(year, month, day)
shifted_date = current_date + datetime.timedelta(days=shift)

print(shifted_date.strftime('%d.%m.%Y'))
```

The first section parses the input. We use `strip()` to remove trailing newlines. `map(int, ...)` converts the split strings into integers. The `datetime.date` constructor ensures the input is a valid date. `datetime.timedelta` handles the shift and allows negative values, removing manual error-prone arithmetic. Finally, `strftime` guarantees the output format matches exactly "DD.MM.YYYY" with leading zeros.

## Worked Examples

Sample Input 1:

```
10.02.2012
12
```

| Variable | Value |
| --- | --- |
| day | 10 |
| month | 2 |
| year | 2012 |
| current_date | 2012-02-10 |
| shifted_date | 2012-02-22 |

The algorithm correctly adds 12 days, accounting for February having 29 days in 2012.

Sample Input 2 (negative shift):

```
01.03.2012
-1
```

| Variable | Value |
| --- | --- |
| day | 1 |
| month | 3 |
| year | 2012 |
| current_date | 2012-03-01 |
| shifted_date | 2012-02-29 |

This demonstrates handling of negative shifts and the leap day correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All operations use Python's built-in date arithmetic and string parsing, independent of shift size. |
| Space | O(1) | Only a few integer and date objects are created, no extra data structures. |

The solution easily fits within the 2-second time limit and 256 MB memory limit for any valid input.

## Test Cases

```python
import sys, io
import datetime

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    date_str = input().strip()
    shift = int(input().strip())
    day, month, year = map(int, date_str.split('.'))
    current_date = datetime.date(year, month, day)
    shifted_date = current_date + datetime.timedelta(days=shift)
    return shifted_date.strftime('%d.%m.%Y')

# Provided samples
assert run("10.02.2012\n12\n") == "22.02.2012", "sample 1"
assert run("01.03.2012\n-1\n") == "29.02.2012", "sample 2"

# Custom cases
assert run("28.02.2011\n1\n") == "01.03.2011", "non-leap year feb"
assert run("28.02.2012\n1\n") == "29.02.2012", "leap year feb"
assert run("31.12.2019\n1\n") == "01.01.2020", "year change forward"
assert run("01.01.1980\n-1\n") == "31.12.1979", "year change backward"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 28.02.2011 1 | 01.03.2011 | Normal February to March transition in non-leap year |
| 28.02.2012 1 | 29.02.2012 | Leap day handling |
| 31.12.2019 1 | 01.01.2020 | End-of-year increment |
| 01.01.1980 -1 | 31.12.1979 | Negative shift across year boundary |

## Edge Cases

Starting on February 29 in a leap year and shifting by one year minus one day is a subtle edge. For input "29.02.2012" with shift 365, Python calculates the correct output as "28.02.2013" because 2013 is not a leap year. Similarly, negative shifts that cross month or year boundaries are handled automatically, such as "01.03.2012" with shift -1 producing "29.02.2012". Using the `datetime` module eliminates manual tracking errors that typically occur in these edge cases.
