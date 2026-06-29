---
title: "CF 104619A - Advance to Taoyuan Regional"
description: "We are given a single calendar date in the year 2023, written as YYYY-MM-DD. This date represents when a programming contest (TOPC) is planned to be held."
date: "2026-06-29T17:25:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104619
codeforces_index: "A"
codeforces_contest_name: "2023 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 104619
solve_time_s: 47
verified: true
draft: false
---

[CF 104619A - Advance to Taoyuan Regional](https://codeforces.com/problemset/problem/104619/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single calendar date in the year 2023, written as `YYYY-MM-DD`. This date represents when a programming contest (TOPC) is planned to be held. The task is to decide whether this date is too late or not, based on a fixed cutoff rule derived from the ICPC Taoyuan Regional schedule.

The key condition is tied to October 21, 2023. Any TOPC contest date must be at least 35 days before that regional contest date; otherwise, it is considered too late. So the problem reduces to a calendar comparison: given a date in 2023, determine whether it is strictly earlier than or equal to the cutoff date (October 21 minus 35 days), or after it.

The input constraints simplify the problem significantly. The year is always 2023, and the month-day range is small and bounded (months 1 to 12, days 1 to 28). This removes concerns about invalid dates or leap years. We only need correct date arithmetic within a fixed year.

A naive mistake would be to compare month and day lexicographically as strings. For example, comparing `"2023-09-30"` and `"2023-10-01"` as strings works, but comparing `"2023-10-01"` and a computed cutoff incorrectly as strings without normalization could fail in general reasoning. Another subtle edge case is misunderstanding the 35-day subtraction: it is not enough to assume “September is safe, October is not”, because the boundary lies in early September.

A concrete edge scenario: if the cutoff is around early September 2023, then dates like `2023-09-16` are still valid, but `2023-10-01` becomes too late even though it is close in time. This shows that month-based heuristics are insufficient.

So the problem is fundamentally a date comparison against a fixed threshold date.

## Approaches

A brute-force approach would simulate day-by-day subtraction from October 21, 2023, going back 35 days. Since the date range is small and fixed, this is trivial to compute manually or via simple loops over a calendar representation. The cost is constant time in practice, since the year and range are fixed.

A cleaner approach is to convert every date into an integer representing “days since a fixed origin”, then compare integers. Since all dates are in 2023 and months are bounded, we can predefine month lengths and compute day-of-year values.

Once we convert the input date into a day index, we compute the cutoff date similarly and compare.

The key observation is that we do not need full date libraries. A fixed-year conversion is sufficient, and comparison becomes a single integer comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Calendar Simulation | O(1) | O(1) | Accepted |
| Day-of-Year Conversion | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We first compute the cutoff date by subtracting 35 days from October 21, 2023. Since all dates are within a single year and months are small, we precompute cumulative days for each month.

We then convert both the input date and the cutoff date into day-of-year values.

### Steps

1. Parse the input string `YYYY-MM-DD` into integers year, month, and day. We only care about month and day since the year is fixed.
2. Build a static array representing the number of days in each month of 2023. Since the problem guarantees validity and does not include leap years, February has 28 days.
3. Construct a prefix sum array where `prefix[m]` gives total days up to the end of month `m - 1`. This allows fast conversion of a date into a single integer day index.
4. Convert the input date into a day-of-year value using `prefix[month] + day`.
5. Compute the cutoff date as October 21, 2023, then subtract 35 days. Convert that result into another day-of-year value.
6. Compare the two values. If the input day index is greater than the cutoff index, the date is too late; otherwise it is valid.

The reasoning behind converting to a linear index is that it removes all calendar structure. Once flattened, the problem reduces to a simple integer comparison.

### Why it works

The algorithm relies on the invariant that the day-of-year mapping preserves chronological order: if date A occurs before date B in the calendar, then its day index is smaller. Because we compute both values using the same month-length structure, no distortion is introduced. Subtracting 35 days from a known date in the same representation yields the correct boundary, and comparison in this space is equivalent to real date comparison.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_day(month, day):
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    prefix = [0] * 13
    for i in range(1, 13):
        prefix[i] = prefix[i - 1] + days_in_month[i - 1]
    return prefix[month] + day

def solve():
    s = input().strip()
    year, month, day = map(int, s.split("-"))

    # input date as day index
    d = to_day(month, day)

    # cutoff: 2023-10-21 minus 35 days
    cutoff = to_day(10, 21) - 35

    if d > cutoff:
        print("TOO LATE")
    else:
        print("GOOD")

if __name__ == "__main__":
    solve()
```

The parsing step directly extracts month and day from the ISO format string. We ignore the year since it is fixed.

The function `to_day` converts a date into a linear position in the year using a prefix sum of month lengths. This ensures constant-time comparison after conversion.

The cutoff is computed by converting October 21 into a day index and subtracting 35, which is safe because all computations stay within the same linearized calendar space.

Finally, we compare directly and print the required label.

## Worked Examples

### Example 1

Input: `2023-09-16`

We compute day-of-year values.

| Step | Month | Day | Day index |
| --- | --- | --- | --- |
| Input date | 9 | 16 | 31+28+31+30+31+30+31+31 + 16 = 259 |
| Cutoff base | 10 | 21 | 294 |
| Cutoff after -35 | - | - | 259 |

The input equals the cutoff boundary, so it is not later than it. The output is `GOOD`.

This confirms that equality is treated as valid, matching the “at least 35 days before” condition.

### Example 2

Input: `2023-10-01`

| Step | Month | Day | Day index |
| --- | --- | --- | --- |
| Input date | 10 | 1 | 273 |
| Cutoff | - | - | 259 |

Since 273 > 259, the date is after the cutoff boundary, so the output is `TOO LATE`.

This shows how early October dates exceed the allowable window even though they are close to the regional contest date.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All computations involve fixed-size arrays and constant arithmetic |
| Space | O(1) | Only a small fixed array for month lengths and prefix sums |

The solution comfortably fits within constraints since it performs constant-time computation per test case and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("2023-09-16\n") == "GOOD"
assert run("2023-10-01\n") == "TOO LATE"

# boundary: exactly cutoff
assert run("2023-09-16\n") == "GOOD"

# just after cutoff
assert run("2023-09-17\n") == "TOO LATE"

# earliest date
assert run("2023-01-01\n") == "GOOD"

# late year boundary
assert run("2023-10-28\n") == "TOO LATE"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2023-09-16 | GOOD | boundary equality case |
| 2023-09-17 | TOO LATE | first invalid day after cutoff |
| 2023-01-01 | GOOD | minimum date handling |
| 2023-10-28 | TOO LATE | far beyond cutoff |

## Edge Cases

A subtle case is the exact cutoff boundary. If the input date converts to the same day index as the computed cutoff, it must still be accepted. The algorithm handles this correctly because it uses `>` for rejection, not `>=`.

Another case is late October dates. For example, `2023-10-28` converts to a significantly larger day index than the cutoff, so it is correctly classified as too late without needing month-specific logic.

A final case is early-year dates like `2023-01-01`. These map to very small day indices and are always safely before the cutoff, which confirms that the prefix sum representation preserves ordering across the entire year.
