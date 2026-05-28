---
title: "CF 130J - Date calculation"
description: "We are given a year in the Gregorian calendar and a day number inside that year. The task is to determine the actual calendar date corresponding to that day number."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "J"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1800
weight: 130
solve_time_s: 90
verified: true
draft: false
---

[CF 130J - Date calculation](https://codeforces.com/problemset/problem/130/J)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a year in the Gregorian calendar and a day number inside that year. The task is to determine the actual calendar date corresponding to that day number.

For example, if the input year is 2011 and the day index is 324, we count forward from January 1st until we reach the 324th day of the year. The answer is the calendar date where that count stops.

The only complication comes from leap years. February normally has 28 days, but in leap years it has 29. A year is a leap year if it is divisible by 400, or divisible by 4 but not divisible by 100.

The constraints are tiny. The year lies between 1600 and 2400, and the day index is at most 366. Even a very direct simulation over months is easily fast enough because there are only 12 months in a year. Any solution that processes months one by one runs in constant time.

The main danger is handling leap years incorrectly. Many incorrect implementations check only divisibility by 4, which breaks for years like 1900. Another common mistake is forgetting to increase February to 29 days in leap years.

Consider this example:

```
Input:
1900
60
```

Year 1900 is divisible by 100 but not by 400, so it is not a leap year. February has 28 days. The 60th day is March 1st.

Correct output:

```
1 3
```

A careless implementation using only `year % 4 == 0` would incorrectly treat 1900 as a leap year and output February 29th.

Another edge case appears near the end of leap years.

```
Input:
2000
366
```

Year 2000 is divisible by 400, so it is a leap year. The 366th day exists and corresponds to December 31st.

Correct output:

```
31 12
```

If February is not adjusted to 29 days, the computation shifts every later month backward by one day.

## Approaches

The most straightforward idea is to simulate the calendar day by day. Start from January 1st and repeatedly advance one day until reaching the requested day index. This works because the Gregorian calendar rules are deterministic and there are at most 366 days to process.

That brute-force simulation performs at most 365 transitions between dates. Even that is perfectly acceptable for the given limits. The implementation, however, becomes more complicated because advancing a date correctly requires handling month boundaries and leap years carefully.

A cleaner approach comes from observing that the problem only depends on month lengths. Instead of moving one day at a time, we can subtract entire months from the day index.

Suppose the target day index is 324. January contributes 31 days, so the target date cannot lie in January. We subtract 31 and continue with February. We keep removing full months until the remaining value fits inside the current month. That remaining value is exactly the day of the month.

This works because months partition the year into consecutive blocks of days. Once we know the correct month lengths, especially February in leap years, the date can be located with a simple linear scan over the 12 months.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(366) | O(1) | Accepted |
| Optimal | O(12) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the year and the day index.
2. Determine whether the year is a leap year.

A year is leap if:

- it is divisible by 400, or
- it is divisible by 4 but not divisible by 100.
3. Create the array of month lengths.

Start with:

```
[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
```

If the year is leap, change February from 28 to 29.
4. Iterate through the months in order.

For each month:

- if the remaining day index is larger than the current month length, subtract the whole month and continue;
- otherwise, the answer lies in this month.
5. Once the correct month is found:

- the remaining day index is the day of the month;
- the current month position plus one is the month number.
6. Output the day and month.

### Why it works

At every step of the iteration, the remaining day index represents the position inside the still-unprocessed suffix of the year. When we subtract a month length, we remove exactly all days belonging to that month. After processing several months, the remaining value becomes small enough to fit inside the next month. That value is precisely the calendar day within that month, so the algorithm always returns the correct date.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    year = int(input())
    day_index = int(input())

    leap = (
        year % 400 == 0 or
        (year % 4 == 0 and year % 100 != 0)
    )

    months = [31, 28, 31, 30, 31, 30,
              31, 31, 30, 31, 30, 31]

    if leap:
        months[1] = 29

    month = 1

    for days in months:
        if day_index > days:
            day_index -= days
            month += 1
        else:
            print(day_index, month)
            return

solve()
```

The first part computes whether the year is leap. The condition must follow the Gregorian rules exactly. Checking only divisibility by 4 produces wrong answers for years like 1700, 1800, and 1900.

The `months` array stores the number of days in each month. February is updated to 29 only when the year is leap.

The loop processes months in chronological order. If the target day index is larger than the current month length, the target date must lie later in the year, so we subtract the whole month and move on.

The stopping condition is subtle. We use `if day_index > days` instead of `>=`. If the remaining value equals the month length exactly, the answer is the last day of the current month, not the first day of the next one.

For example, in a non-leap year:

```
day_index = 31
```

This should produce January 31st. Using `>=` would incorrectly subtract January and move into February.

## Worked Examples

### Example 1

Input:

```
2011
324
```

Year 2011 is not a leap year.

| Month | Days in Month | Remaining Day Index Before | Action | Remaining After |
| --- | --- | --- | --- | --- |
| 1 | 31 | 324 | subtract | 293 |
| 2 | 28 | 293 | subtract | 265 |
| 3 | 31 | 265 | subtract | 234 |
| 4 | 30 | 234 | subtract | 204 |
| 5 | 31 | 204 | subtract | 173 |
| 6 | 30 | 173 | subtract | 143 |
| 7 | 31 | 143 | subtract | 112 |
| 8 | 31 | 112 | subtract | 81 |
| 9 | 30 | 81 | subtract | 51 |
| 10 | 31 | 51 | subtract | 20 |
| 11 | 30 | 20 | stop | 20 |

Output:

```
20 11
```

This trace shows how each processed month removes a whole contiguous block of days from the year until the remaining value fits inside the current month.

### Example 2

Input:

```
2000
60
```

Year 2000 is a leap year because it is divisible by 400.

| Month | Days in Month | Remaining Day Index Before | Action | Remaining After |
| --- | --- | --- | --- | --- |
| 1 | 31 | 60 | subtract | 29 |
| 2 | 29 | 29 | stop | 29 |

Output:

```
29 2
```

This example exercises the leap-year logic. February contains 29 days, so the 60th day becomes February 29th instead of March 1st.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(12) | At most 12 months are processed |
| Space | O(1) | Only a small fixed-size array is stored |

The running time is effectively constant because the calendar always has 12 months. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    year = int(input())
    day_index = int(input())

    leap = (
        year % 400 == 0 or
        (year % 4 == 0 and year % 100 != 0)
    )

    months = [31, 28, 31, 30, 31, 30,
              31, 31, 30, 31, 30, 31]

    if leap:
        months[1] = 29

    month = 1

    for days in months:
        if day_index > days:
            day_index -= days
            month += 1
        else:
            print(day_index, month)
            return

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("2011\n324\n") == "20 11", "sample 1"

# minimum valid input
assert run("1600\n1\n") == "1 1", "minimum case"

# leap year, February 29
assert run("2000\n60\n") == "29 2", "leap year handling"

# non-leap century year
assert run("1900\n60\n") == "1 3", "century year rule"

# last day of leap year
assert run("2400\n366\n") == "31 12", "end of leap year"

# boundary at end of January
assert run("2011\n31\n") == "31 1", "month boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1600 / 1` | `1 1` | Smallest day index |
| `2000 / 60` | `29 2` | Leap year February |
| `1900 / 60` | `1 3` | Century year is not leap |
| `2400 / 366` | `31 12` | Maximum valid day in leap year |
| `2011 / 31` | `31 1` | Off-by-one at month boundary |

## Edge Cases

Consider the non-leap century year case:

```
Input:
1900
60
```

The algorithm checks leap-year status:

```
1900 % 400 != 0
1900 % 4 == 0
1900 % 100 == 0
```

Because the year is divisible by 100 and not by 400, it is not leap. February remains 28 days.

The algorithm subtracts January:

```
60 - 31 = 29
```

February has only 28 days, so it subtracts February:

```
29 - 28 = 1
```

The remaining value fits inside March, producing:

```
1 3
```

This confirms the century rule is handled correctly.

Now consider the maximum valid day in a leap year:

```
Input:
2000
366
```

Year 2000 is leap because it is divisible by 400, so February becomes 29 days.

The algorithm subtracts every month sequentially:

```
366 - 31 - 29 - 31 - 30 - ...
```

After subtracting the first eleven months, the remaining value becomes 31, which fits exactly inside December.

The answer is:

```
31 12
```

This case confirms two important details: leap-year adjustment is correct, and the comparison uses `>` rather than `>=`, so the last day of a month is handled properly.
