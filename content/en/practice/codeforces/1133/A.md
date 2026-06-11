---
title: "CF 1133A - Middle of the Contest"
description: "The task is to find the exact midpoint of a contest given its start and end times in hours and minutes. The input gives the start time as h1:m1 and the end time as h2:m2."
date: "2026-06-12T04:03:52+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1133
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 544 (Div. 3)"
rating: 1000
weight: 1133
solve_time_s: 67
verified: true
draft: false
---

[CF 1133A - Middle of the Contest](https://codeforces.com/problemset/problem/1133/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to find the exact midpoint of a contest given its start and end times in hours and minutes. The input gives the start time as `h1:m1` and the end time as `h2:m2`. We are guaranteed that the contest lasts an even number of minutes, and that the contest happens within a single day. The output must be the midpoint in the same `hh:mm` format.

In practice, this means we need to compute the total duration of the contest in minutes, divide that by two, and add it to the start time. The constraints are small: hours are between 0 and 23 and minutes between 0 and 59. Because all operations are simple arithmetic on integers and we are only computing a single midpoint, performance is not a concern. A naive approach that calculates the time step by step will always be fast.

Subtle edge cases include contests that start or end on a half-hour boundary or near midnight, for example `23:58` to `23:59` is not allowed because the contest lasts at least 2 minutes, but `23:58` to `00:00` is valid if the day boundary were considered (but the problem guarantees a single day). Another potential trap is forgetting to carry over minutes into hours when the midpoint adds past 59 minutes.

## Approaches

A brute-force approach would simulate the contest minute by minute, counting halfway, and then print the corresponding hour and minute. This works because we are guaranteed a small fixed range of times (maximum 1440 minutes in a day). This approach is correct but unnecessarily slow for larger ranges or multiple queries because it performs a loop for every minute of the contest.

The key insight is that we can represent the time entirely in minutes from midnight. Convert the start time `h1:m1` to `start_minutes = h1 * 60 + m1` and the end time `h2:m2` to `end_minutes = h2 * 60 + m2`. The midpoint in minutes is `(start_minutes + end_minutes) // 2`. Finally, convert that back into hours and minutes with integer division and modulo. This works because all arithmetic is linear and we are guaranteed the total number of minutes is even, so integer division yields the correct midpoint without rounding issues.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(duration in minutes) | O(1) | Correct but unnecessary for this problem |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the start time `h1:m1` and end time `h2:m2`.
2. Convert both times into total minutes since midnight. Compute `start_minutes = h1 * 60 + m1` and `end_minutes = h2 * 60 + m2`. This allows linear arithmetic without worrying about hours wrapping.
3. Compute the midpoint in minutes as `(start_minutes + end_minutes) // 2`. Integer division works because the total contest duration is guaranteed to be even.
4. Convert the midpoint back to hours and minutes with `mid_h = mid_minutes // 60` and `mid_m = mid_minutes % 60`.
5. Print the result in two-digit format using zero-padding for hours and minutes to match the `hh:mm` requirement.

Why it works: Converting to total minutes ensures we handle any carryover from minutes to hours automatically. The integer division computes exactly half the duration, and modulo 60 and integer division by 60 correctly reconstruct the hours and minutes. The guarantees in the problem prevent rounding errors or day overflow.

## Python Solution

```python
import sys
input = sys.stdin.readline

h1, m1 = map(int, input().strip().split(':'))
h2, m2 = map(int, input().strip().split(':'))

start_minutes = h1 * 60 + m1
end_minutes = h2 * 60 + m2

mid_minutes = (start_minutes + end_minutes) // 2

mid_h = mid_minutes // 60
mid_m = mid_minutes % 60

print(f"{mid_h:02d}:{mid_m:02d}")
```

The solution first parses the input using `split(':')` and converts the hours and minutes into integers. Calculating total minutes simplifies all arithmetic. Dividing the sum of start and end minutes by two directly computes the midpoint. Finally, integer division and modulo convert the minutes back into hours and minutes, with formatting to maintain the two-digit requirement. The problem's guarantees mean no boundary checks are needed beyond zero-padding.

## Worked Examples

Sample Input 1:

```
10:00
11:00
```

| Variable | Value |
| --- | --- |
| h1, m1 | 10, 0 |
| h2, m2 | 11, 0 |
| start_minutes | 600 |
| end_minutes | 660 |
| mid_minutes | 630 |
| mid_h | 10 |
| mid_m | 30 |

The trace shows that converting to minutes simplifies finding the midpoint: 600 + 660 = 1260, divided by 2 gives 630 minutes, which corresponds to 10 hours 30 minutes.

Custom Input 2:

```
11:10
11:12
```

| Variable | Value |
| --- | --- |
| h1, m1 | 11, 10 |
| h2, m2 | 11, 12 |
| start_minutes | 670 |
| end_minutes | 672 |
| mid_minutes | 671 |
| mid_h | 11 |
| mid_m | 11 |

This shows the algorithm correctly handles minute-level precision, producing `11:11` for a two-minute contest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | Only a few integer variables are stored |

The approach is constant time and space, well within the limits. Since the input size is fixed to two times, there are no performance concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    h1, m1 = map(int, input().strip().split(':'))
    h2, m2 = map(int, input().strip().split(':'))
    start_minutes = h1 * 60 + m1
    end_minutes = h2 * 60 + m2
    mid_minutes = (start_minutes + end_minutes) // 2
    mid_h = mid_minutes // 60
    mid_m = mid_minutes % 60
    return f"{mid_h:02d}:{mid_m:02d}"

# provided sample
assert run("10:00\n11:00\n") == "10:30", "sample 1"

# minimum duration
assert run("00:00\n00:02\n") == "00:01", "minimum duration"

# even duration with minutes overflow
assert run("23:58\n23:59\n") == "23:58", "edge minutes overflow not allowed, guaranteed >=2 minutes"

# odd/even alignment
assert run("11:10\n11:12\n") == "11:11", "2-minute contest in mid hour"

# full day split
assert run("00:00\n23:58\n") == "11:59", "halfway through full day minus two minutes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10:00 11:00 | 10:30 | standard 1-hour contest |
| 00:00 00:02 | 00:01 | minimum contest duration |
| 11:10 11:12 | 11:11 | very short contest not on the hour |
| 00:00 23:58 | 11:59 | long contest spanning nearly whole day |

## Edge Cases

The algorithm correctly handles contests lasting exactly two minutes. For example, input `00:00` and `00:02` converts to minutes 0 and 2, midpoint is 1 minute, which converts back to `00:01`. It also handles times that require carrying over minutes to hours without any special cases. The guarantees about even durations prevent rounding errors, and the formatting ensures the output always has two digits for hours and minutes.
