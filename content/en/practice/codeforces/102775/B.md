---
title: "CF 102775B - \u041a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u0438"
description: "The task is about comparing two calendar systems for the same moment in time. The input gives a valid date written according to the Gregorian calendar, with a day, month, and year. We need to determine how many days earlier the Julian calendar shows for that same date."
date: "2026-07-27T20:36:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 56
verified: true
draft: false
---

[CF 102775B - \u041a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u0438](https://codeforces.com/problemset/problem/102775/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about comparing two calendar systems for the same moment in time. The input gives a valid date written according to the Gregorian calendar, with a day, month, and year. We need to determine how many days earlier the Julian calendar shows for that same date. In other words, we need the number of days by which the Julian calendar falls behind the Gregorian one.

The years in the input range are from 1582 to 2500. This is a very small range for a date simulation, but the challenge is not the number of dates. The challenge is handling the exact moments when leap year rules differ. A solution that checks every day would perform hundreds of thousands of operations, which is still acceptable here, but it hides the actual idea and is easier to get wrong around calendar transitions. A formula-based solution only needs to inspect a few centuries and is constant time.

The main source of mistakes is assuming that the difference is always a fixed number. For example, on 15 November 1582 the difference is 10 days, because the Gregorian calendar had just replaced the Julian calendar with a ten-day correction. However, by 1 March 1700 the difference is 11 days. The Julian calendar treats 1700 as a leap year, while the Gregorian calendar does not, so the Julian calendar has gained one extra day.

Another boundary case is the exact day before a leap difference appears. For input `28 2 1700`, the output is `10`. A careless implementation that increments the difference for the whole year 1700 would incorrectly print `11`.

The year 2000 is another common trap. For input `1 3 2000`, the output is still `13`, because 2000 is a leap year in both calendars. A solution that only checks whether a year is divisible by 100 would incorrectly add an extra day.

The final boundary is near the maximum year. For input `17 3 2500`, the output is `17`. The Julian calendar considers 2500 a leap year, while the Gregorian calendar does not, and the extra day appears after February ends.

## Approaches

A straightforward approach is to simulate the calendars day by day. Starting from the first Gregorian date where the calendars differ, we could move forward one day at a time and maintain the Julian and Gregorian dates separately. Whenever one calendar reaches a leap day and the other does not, the difference changes. This works because every individual date transition can be modeled exactly.

The problem with this method is that it solves a much larger problem than necessary. The input range covers more than nine hundred years, which is over three hundred thousand days. While this specific range is not huge, the simulation approach performs unnecessary work and makes the calendar transition logic more complicated.

The key observation is that the calendars differ only because of leap year rules. Both calendars have the same number of days in normal years, so the offset changes only after years where one calendar contains an extra February day and the other does not.

The initial offset after the Gregorian reform is 10 days. From there, we only need to count the Gregorian century years that are leap years in the Julian calendar but not in the Gregorian calendar. These years are 1700, 1800, 1900, 2100, 2200, 2300, and 2500. Each contributes one extra day to the Julian calendar, but only if the given date is after February of that year.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of days between dates) | O(1) | Works in this range, but unnecessary |
| Optimal | O(year range) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the historical offset of 10 days. Every valid input date is after 15 October 1582, so the Gregorian calendar is already ten days ahead of the Julian calendar.
2. Go through every year from 1583 up to the given year. Check whether this year creates an additional difference between the calendars.
3. For each year, verify whether the Julian calendar has a leap day while the Gregorian calendar does not. This happens when the year is divisible by 100 but not by 400. These are exactly the century years that Gregorian rules remove but Julian rules keep.
4. If such a year has already passed its February leap day, add one to the answer. If the input date is still in January or February of that year, the extra day has not appeared yet, so it must not be counted.
5. Print the accumulated offset.

Why it works: the only possible difference between the calendars comes from leap days. Normal years contribute exactly the same number of days to both systems. The starting offset accounts for the Gregorian reform, and every later adjustment corresponds to one missing Gregorian leap day that still exists in the Julian calendar. Since we count every such leap day exactly when it becomes part of the elapsed time, the final value is precisely the calendar difference.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    d, m, y = map(int, input().split())

    ans = 10

    for year in range(1583, y + 1):
        if year % 100 == 0 and year % 400 != 0:
            if year < y or (year == y and m > 2):
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The program begins with `ans = 10` because every input date is after the Gregorian calendar was introduced, and the initial correction from the Julian calendar is always ten days.

The loop checks only century years. A normal leap year appears in both calendars, so it cannot affect the difference. A year divisible by 100 is special because the Gregorian calendar removes its leap day unless it is also divisible by 400.

The condition `year < y or (year == y and m > 2)` handles the exact boundary of February. A leap day on 29 February changes the offset only after that day has passed. For a date in February or earlier, that year's missing Gregorian leap day has not yet affected the difference.

The range is tiny, so iterating through the years is simpler and safer than trying to compress the century calculations into a single formula.

## Worked Examples

For the first sample, the input is `15 11 1582`.

| Year checked | Current offset | Reason |
| --- | --- | --- |
| Start | 10 | Gregorian reform difference |
| No later years | 10 | No extra leap differences yet |

The date is shortly after the Gregorian correction, before any century leap-year mismatch occurs. The result remains 10 days.

For the second sample, the input is `31 1 1918`.

| Year checked | Current offset | Reason |
| --- | --- | --- |
| Start | 10 | Gregorian reform difference |
| 1700 | 11 | Julian has an extra leap day |
| 1800 | 12 | Julian has an extra leap day |
| 1900 | 13 | Julian has an extra leap day |
| Final | 13 | January 1918 is after all previous changes |

This trace shows why the answer depends on the date's year and month, not just the year. The leap difference from 1900 already exists because the input date is much later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(y - 1582) | The algorithm checks each year once |
| Space | O(1) | Only the current answer and loop variables are stored |

The maximum year is 2500, so the loop runs fewer than one thousand iterations. This easily fits within the limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    d, m, y = map(int, input().split())

    ans = 10
    for year in range(1583, y + 1):
        if year % 100 == 0 and year % 400 != 0:
            if year < y or (year == y and m > 2):
                ans += 1

    return str(ans)

# provided samples
assert solution("15 11 1582\n") == "10", "sample 1"
assert solution("31 1 1918\n") == "13", "sample 2"

# custom cases
assert solution("15 10 1582\n") == "10", "first valid Gregorian date"
assert solution("1 3 1700\n") == "11", "first century leap mismatch"
assert solution("1 3 2000\n") == "13", "Gregorian 400-year leap rule"
assert solution("17 3 2500\n") == "17", "maximum boundary date"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `15 10 1582` | 10 | The starting Gregorian reform boundary |
| `1 3 1700` | 11 | The first year where the calendars diverge again |
| `1 3 2000` | 13 | The special Gregorian rule for divisible-by-400 years |
| `17 3 2500` | 17 | The maximum year and final possible offset increase |

## Edge Cases

For `15 10 1582`, the algorithm starts with an offset of 10 and finds no completed mismatching century leap years. The output is 10, matching the immediate Gregorian correction.

For `28 2 1700`, the loop detects that 1700 is a century year where Julian has a leap day and Gregorian does not, but the condition `m > 2` is false. The answer stays 10 because February 29 has not affected the calendar difference yet.

For `1 3 1700`, the same year is now past February. The algorithm adds one day for 1700, changing the answer from 10 to 11. This handles the exact transition point correctly.

For `1 3 2000`, the year is divisible by 400, so it is a leap year in both calendars. The algorithm does not count it, leaving the accumulated difference at 13.

For `17 3 2500`, the algorithm counts all previous mismatching century years and also counts 2500 because the date is after February. The final answer becomes 17, which is the largest possible difference in the input range.
