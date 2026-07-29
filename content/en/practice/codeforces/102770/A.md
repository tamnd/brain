---
title: "CF 102770A - AD 2020"
description: "We need count how many calendar days inside a given inclusive interval have the property that their YYYYMMDD representation contains the three consecutive digits 202. A date is not compared as a number with the property. The actual eight-character representation matters."
date: "2026-07-30T04:31:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "A"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 90
verified: true
draft: false
---

[CF 102770A - AD 2020](https://codeforces.com/problemset/problem/102770/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We need count how many calendar days inside a given inclusive interval have the property that their `YYYYMMDD` representation contains the three consecutive digits `202`.

A date is not compared as a number with the property. The actual eight-character representation matters. For example, `22020101` contains `202` because the substring starts at the second digit of the year, while `20190202` contains it because the substring crosses from the year into the month.

The input contains up to `10^5` independent date intervals. The years are limited to `2000` through `9999`, so there are only 8000 possible years. This rules out scanning every day for every query because the whole range contains almost three million days, and doing that for `10^5` cases would approach `3 * 10^11` date checks. The small fixed year range suggests preprocessing all years once and answering each query using prefix sums.

The tricky parts are the boundaries and the different places where `202` can appear. A careless solution may only check whether the year contains `202` and miss cases involving the month and day. For example, the interval `2111 02 01` to `2111 02 03` has only one valid date, `21110202`, because the substring is formed by the month and day part. Another mistake is excluding the ending date. For `2020 01 01` to `2020 01 02`, both dates are valid because both full strings contain `202`, so the answer is `2`.

Leap years also matter. For example, the interval `2200 02 28` to `2200 03 01` contains two days, not three, because 2200 is not a leap year.

## Approaches

The direct solution is to iterate through every date in the interval, convert it to `YYYYMMDD`, and check whether `"202"` appears. This is easy to prove correct because every day is inspected exactly once. However, the largest possible interval spans the years 2000 to 9999, which contains about 2.9 million days. Repeating that work for `10^5` queries is far beyond the limit.

The key observation is that the calendar range is tiny compared with the number of queries. There are only 8000 possible years. We can preprocess each year by counting how many valid dates inside it contain `202`, and also store prefix information inside the year.

For a query, the answer becomes:

`number of valid days in years before Y2` plus `number of valid days from January 1 to the ending date`, minus the same value calculated for the day before the starting date.

This turns every query into a constant amount of work after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of days in range) per query | O(1) | Too slow |
| Optimal | O(1) per query after O(8000 * 366) preprocessing | O(8000 * 13 * 32) | Accepted |

## Algorithm Walkthrough

1. Precompute information for every year from 2000 to 9999. For each year, simulate all valid months and days, create the eight-digit date string, and count whether it contains `202`.

The number of years is fixed and small, so this preprocessing is cheap and removes repeated work from the queries.
2. Store a prefix array where `prefix[y]` is the number of valid dates from 2000 up to the end of year `y`.

This allows complete years before a query boundary to be answered instantly.
3. For every year, also store cumulative counts by month and day. This lets us count only the beginning part of a year when a query ends in the middle of that year.
4. Define a function that returns the number of valid dates from `2000-01-01` to any given date.

It combines the precomputed full years with the partial year information.
5. Answer each query with:

`count(end_date) - count(day_before_start_date)`

Subtracting the previous day handles the inclusive interval correctly.

Why it works:

The prefix function always counts exactly the days from the fixed starting point to a requested date. For a query interval, removing everything before the first day leaves exactly the days inside the interval. Since every date is counted according to its complete `YYYYMMDD` representation during preprocessing, no possible occurrence of `202` is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

year_pref = [0] * 10001
inside = {}

for y in range(2000, 10000):
    cur = [[0] * 32 for _ in range(13)]
    total = 0
    for m in range(1, 13):
        limit = days_in_month[m - 1]
        if m == 2 and leap(y):
            limit += 1
        for d in range(1, limit + 1):
            if "202" in f"{y:04d}{m:02d}{d:02d}":
                total += 1
            cur[m][d] = total
    inside[y] = cur
    year_pref[y] = year_pref[y - 1] + total

def count_to(y, m, d):
    if y < 2000:
        return 0
    ans = year_pref[y - 1]
    if m:
        ans += inside[y][m][d]
    return ans

def previous_day(y, m, d):
    d -= 1
    if d == 0:
        m -= 1
        if m == 0:
            return y - 1, 12, 31
        d = days_in_month[m - 1]
        if m == 2 and leap(y):
            d += 1
    return y, m, d

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        y1, m1, d1, y2, m2, d2 = map(int, input().split())
        py, pm, pd = previous_day(y1, m1, d1)
        out.append(str(count_to(y2, m2, d2) - count_to(py, pm, pd)))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The preprocessing loop builds two kinds of information. `year_pref` stores completed years, while `inside[y]` stores cumulative answers inside one particular year. The latter avoids iterating over months and days during every query.

The query function first takes all complete years before the target year and then adds the partial count inside the target year. The previous-day function is used because the prefix function is inclusive. Without it, the starting date would be counted twice.

Python integers do not overflow here because the total number of days in the whole supported range is only a few million. The main implementation detail to avoid is handling February correctly when moving backwards across a month boundary.

## Worked Examples

For the first sample:

`2111 02 01` to `2111 02 03`

| Step | Date | Prefix result |
| --- | --- | --- |
| End boundary | 2111-02-03 | Counts all valid days before and including this date |
| Start minus one day | 2111-01-31 | Removes all earlier days |
| Difference | 2111-02-01 to 2111-02-03 | 1 |

The only counted date is `21110202`, which contains `202`.

For the second sample:

`2202 01 01` to `2202 12 31`

| Step | Date | Prefix result |
| --- | --- | --- |
| End boundary | 2202-12-31 | Includes the whole year |
| Start minus one day | 2201-12-31 | Excludes everything before 2202 |
| Difference | Entire year 2202 | 365 |

Every date in 2202 contains `202` in the year part.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(8000 * 366 + T) | Preprocessing checks every possible supported date once, then each query is constant time |
| Space | O(8000 * 13 * 32) | Stores cumulative information for each year |

The preprocessing cost is roughly three million date checks, which is small. After that, even `10^5` queries only require simple arithmetic operations.

## Test Cases

```python
import sys, io

# paste the solution above here and expose solve()

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    result = sys.stdout.getvalue()
    sys.stdin = old
    return result

assert run("""3
2111 2 1 2111 2 3
2202 1 1 2202 12 31
2000 1 1 9999 12 31
""") == "1\n365\n44294\n"

assert run("""1
2000 1 1 2000 1 1
""") == "0\n"

assert run("""1
2020 1 1 2020 1 2
""") == "2\n"

assert run("""1
2202 2 28 2202 3 1
""") == "2\n"

assert run("""1
9999 12 31 9999 12 31
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2000-01-01` to `2000-01-01` | `0` | Minimum boundary and dates without `202` |
| `2020-01-01` to `2020-01-02` | `2` | Year substring detection and inclusive ranges |
| `2202-02-28` to `2202-03-01` | `2` | Leap year transition handling |
| `9999-12-31` to `9999-12-31` | `0` | Maximum year boundary |

## Edge Cases

A substring can cross the year boundary into the month or day. For the input `2111 02 01 2111 02 03`, the algorithm does not only inspect the year. During preprocessing it checks the complete string `21110202`, so the answer is correctly `1`.

A year containing `202` makes every day in that year valid. For `2202 01 01 2202 12 31`, the substring appears in the year digits themselves. The preprocessing value for year 2202 is the number of days in that year, which is `365`, and the query returns that complete-year count.

Leap years affect the number of dates that can exist. For `2200 02 28 2200 03 01`, the backward date calculation uses the Gregorian rule and recognizes that 2200 is not a leap year. February has 28 days, so no invalid February 29 is introduced.
