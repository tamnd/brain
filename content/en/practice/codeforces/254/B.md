---
title: "CF 254B - Jury Size"
description: "Each Olympiad happens on a fixed calendar date in 2013. Before that date, a group of jury members must work continuously for several days. If an Olympiad needs p people and t preparation days, then exactly p people are busy on each of the t days immediately before the Olympiad."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 254
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 155 (Div. 2)"
rating: 1500
weight: 254
solve_time_s: 892
verified: true
draft: false
---

[CF 254B - Jury Size](https://codeforces.com/problemset/problem/254/B)

**Rating:** 1500  
**Tags:** brute force, implementation  
**Solve time:** 14m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

Each Olympiad happens on a fixed calendar date in 2013. Before that date, a group of jury members must work continuously for several days. If an Olympiad needs `p` people and `t` preparation days, then exactly `p` people are busy on each of the `t` days immediately before the Olympiad.

The same person cannot prepare two different Olympiads on the same day. We need the minimum total number of jury members so that every preparation schedule can exist simultaneously.

The whole problem reduces to one question:

For every calendar day, how many people are required at the same time?

The answer is the maximum of those daily requirements.

The constraints are very small. There are at most 100 Olympiads, and every preparation length is at most 100 days. Even if we simulate every preparation day explicitly, the total work is around `100 * 100 = 10,000` operations, which is tiny.

The main difficulty is not performance, it is handling dates correctly.

A few edge cases easily create off-by-one mistakes.

Suppose an Olympiad is on March 10 and requires 3 preparation days. The work happens on March 7, March 8, and March 9. March 10 itself is not included. A careless implementation might accidentally count the Olympiad day too.

Example:

```
1
3 10 5 3
```

Correct answer:

```
5
```

The occupied days are only March 7 to March 9.

Another tricky case is preparation crossing into 2012.

Example:

```
1
1 3 4 5
```

Preparation days are December 29 to January 2. If we only store days inside 2013, we lose part of the interval.

Correct answer:

```
4
```

Several Olympiads can happen on the same day, and their preparation intervals may fully overlap.

Example:

```
2
5 20 3 2
5 20 4 2
```

Both require work on May 18 and May 19.

Correct answer:

```
7
```

A buggy solution that processes events independently without accumulating daily load would fail here.

## Approaches

The most direct idea is to simulate every preparation day for every Olympiad.

For each Olympiad, we determine the exact days on which its jury members work. Then we add `p[i]` to the workload of each of those days. After processing all Olympiads, we scan all days and take the maximum workload.

This works because jury conflicts are completely local to a single day. If 12 people are simultaneously needed on some day, then at least 12 jury members must exist. Conversely, if the maximum simultaneous requirement is 12, we can reuse the same 12 people across different days.

A naive implementation could represent dates as `(month, day)` pairs and repeatedly move backward one day at a time using calendar logic. That is already fast enough here because the total number of simulated days is small.

There is an even cleaner approach. Convert every date into a single integer day index. For example, January 1 becomes day 1, February 1 becomes day 32, and so on. Once dates become integers, every preparation interval is simply a contiguous segment on a number line.

Then we only need an array storing how many jury members are busy on each day.

For an Olympiad occurring on day `D` with preparation length `t`, the occupied interval is:

```
[D - t, D - 1]
```

We add `p` to every day in that interval.

Since the calendar has only 365 days and preparation may extend about 100 days into the previous year, even a direct range update by iteration is trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with manual date stepping | O(n · t) | O(365) | Accepted |
| Optimal with day-index conversion | O(n · t) | O(500) | Accepted |

## Algorithm Walkthrough

1. Create an array containing the number of days in each month of 2013.
2. Build a helper function that converts a calendar date `(month, day)` into its day number inside the year.

For example:

```
Jan 1  -> 1
Feb 1  -> 32
Mar 1  -> 60
```
3. Create an array `cnt` large enough to store workloads for days before January 1 as well.

We use an offset so negative day indices never appear.
4. For each Olympiad:

Convert its date into an integer `D`.
5. The preparation interval is from `D - t` to `D - 1`.

These are exactly the days before the Olympiad.
6. For every day in that interval, add `p` to `cnt[day]`.

This means `p` jury members are occupied on each of those days.
7. After processing all Olympiads, scan the array and find the maximum value.
8. Print that maximum.

### Why it works

For every day, `cnt[d]` equals the total number of jury members simultaneously required on that day.

Any valid schedule must contain at least `cnt[d]` people for every day `d`, because those preparations overlap in time and cannot share people.

If the maximum daily requirement is `M`, then `M` people are also sufficient. We can simply assign distinct people to all active tasks on each day, reusing them freely on different days.

So the minimum possible jury size is exactly the maximum daily workload.

## Python Solution

```python
import sys
input = sys.stdin.readline

MONTHS = [31, 28, 31, 30, 31, 30,
          31, 31, 30, 31, 30, 31]

def day_number(month, day):
    total = 0
    for i in range(month - 1):
        total += MONTHS[i]
    return total + day

def solve():
    n = int(input())

    OFFSET = 200
    cnt = [0] * 1000

    for _ in range(n):
        m, d, p, t = map(int, input().split())

        D = day_number(m, d)

        start = D - t
        end = D - 1

        for day in range(start, end + 1):
            cnt[day + OFFSET] += p

    print(max(cnt))

solve()
```

The helper function converts dates into sequential day numbers. This removes all calendar complications from the main logic.

The array uses an offset because preparation may start before January 1. For example, January 3 with `t = 5` needs days `-2, -1, 0, 1, 2` relative to the year's numbering. Python lists do not allow negative logical indices in the way we want here, so we shift everything by a constant offset.

The interval boundaries are the most delicate part of the implementation.

If the Olympiad happens on day `D`, preparation occupies:

```
[D - t, D - 1]
```

The day `D` itself must not be included.

The loop:

```
for day in range(start, end + 1):
```

correctly includes both ends of the preparation interval.

The array size is intentionally much larger than necessary. The maximum day number is 365, and preparation length is at most 100, so an array of size 1000 is comfortably safe.

## Worked Examples

### Sample 1

Input:

```
2
5 23 1 2
3 13 2 3
```

The Olympiad on May 23 needs 1 person on May 21 and May 22.

The Olympiad on March 13 needs 2 people on March 10, March 11, and March 12.

| Olympiad | Preparation Days | Added People |
| --- | --- | --- |
| May 23 | May 21, May 22 | +1 |
| March 13 | March 10, 11, 12 | +2 |

Daily workloads become:

| Day | Workload |
| --- | --- |
| March 10 | 2 |
| March 11 | 2 |
| March 12 | 2 |
| May 21 | 1 |
| May 22 | 1 |

The maximum is `2`.

Output:

```
2
```

This example shows that non-overlapping preparation periods can reuse the same jury members.

### Custom Example

Input:

```
3
1 5 3 3
1 6 2 2
1 7 4 1
```

Preparation intervals:

| Olympiad | Preparation Days | Added People |
| --- | --- | --- |
| Jan 5 | Jan 2, 3, 4 | +3 |
| Jan 6 | Jan 4, 5 | +2 |
| Jan 7 | Jan 6 | +4 |

Accumulated workloads:

| Day | Total |
| --- | --- |
| Jan 2 | 3 |
| Jan 3 | 3 |
| Jan 4 | 5 |
| Jan 5 | 2 |
| Jan 6 | 4 |

The maximum is `5`.

Output:

```
5
```

This trace demonstrates how overlapping intervals accumulate their jury requirements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · t) | Each Olympiad updates at most 100 days |
| Space | O(1) | The workload array has fixed size |

The worst case performs about 10,000 updates, which is tiny for a 1 second limit. Memory usage is also negligible because the array size does not depend on input magnitude in any meaningful way.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MONTHS = [31, 28, 31, 30, 31, 30,
          31, 31, 30, 31, 30, 31]

def solve_io(inp: str) -> str:
    input = io.StringIO(inp).readline

    def day_number(month, day):
        total = 0
        for i in range(month - 1):
            total += MONTHS[i]
        return total + day

    n = int(input())

    OFFSET = 200
    cnt = [0] * 1000

    for _ in range(n):
        m, d, p, t = map(int, input().split())

        D = day_number(m, d)

        for day in range(D - t, D):
            cnt[day + OFFSET] += p

    return str(max(cnt))

def run(inp: str) -> str:
    return solve_io(inp).strip()

# provided sample
assert run(
"""2
5 23 1 2
3 13 2 3
"""
) == "2", "sample 1"

# minimum input
assert run(
"""1
1 1 1 1
"""
) == "1", "minimum case"

# fully overlapping intervals
assert run(
"""2
5 20 3 2
5 20 4 2
"""
) == "7", "complete overlap"

# crossing into previous year
assert run(
"""1
1 3 4 5
"""
) == "4", "cross-year preparation"

# no overlap at all
assert run(
"""3
1 10 2 1
2 10 3 1
3 10 4 1
"""
) == "4", "independent schedules"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single Olympiad on Jan 1 | 1 | Correct handling of earliest date |
| Two identical intervals | 7 | Proper accumulation of overlaps |
| Preparation starting in 2012 | 4 | Negative-relative day handling |
| Completely separate intervals | 4 | Jury reuse across different days |

## Edge Cases

Consider preparation crossing into the previous year.

Input:

```
1
1 3 4 5
```

January 3 corresponds to day 3. The preparation interval is:

```
[3 - 5, 3 - 1] = [-2, 2]
```

The algorithm stores these values safely using the offset:

| Relative Day | Stored Index | Workload |
| --- | --- | --- |
| -2 | 198 | 4 |
| -1 | 199 | 4 |
| 0 | 200 | 4 |
| 1 | 201 | 4 |
| 2 | 202 | 4 |

The maximum becomes `4`, which is correct.

Now consider the off-by-one boundary around the Olympiad day itself.

Input:

```
1
3 10 5 3
```

Day number for March 10 is 69.

The preparation interval is:

```
[66, 68]
```

Only three days are updated:

| Day | Calendar Date |
| --- | --- |
| 66 | March 7 |
| 67 | March 8 |
| 68 | March 9 |

March 10 is never counted. The answer is correctly `5`.

Finally, consider overlapping preparations with different ranges.

Input:

```
2
1 10 3 5
1 12 4 3
```

Intervals:

```
Jan 5 to Jan 9
Jan 9 to Jan 11
```

The overlap occurs only on January 9.

| Day | Total Jury Needed |
| --- | --- |
| Jan 5 | 3 |
| Jan 6 | 3 |
| Jan 7 | 3 |
| Jan 8 | 3 |
| Jan 9 | 7 |
| Jan 10 | 4 |
| Jan 11 | 4 |

The algorithm accumulates both contributions on the shared day and outputs `7`.
