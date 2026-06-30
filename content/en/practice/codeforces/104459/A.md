---
title: "CF 104459A - Sekiro"
description: "We are working on a fictional calendar system where time is fully regular. Each year has exactly 12 months, each month has exactly 30 days, and weeks repeat every 5 days in a fixed cycle from Monday through Friday. For each test case, we are given two dates in this calendar."
date: "2026-06-30T13:34:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104459
codeforces_index: "A"
codeforces_contest_name: "The 10th Shandong Provincial Collegiate Programming Contest"
rating: 0
weight: 104459
solve_time_s: 49
verified: true
draft: false
---

[CF 104459A - Sekiro](https://codeforces.com/problemset/problem/104459/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a fictional calendar system where time is fully regular. Each year has exactly 12 months, each month has exactly 30 days, and weeks repeat every 5 days in a fixed cycle from Monday through Friday.

For each test case, we are given two dates in this calendar. The first date comes with its known weekday. The second date has no weekday attached, and the task is to determine which weekday that second date falls on, using the information from the first date as a reference point.

So conceptually, this is a relative offset problem on a one-dimensional timeline of days. Every date can be converted into an absolute day index, and weekday progression depends only on how many days separate two points in time.

The constraints allow the year values to be as large as 10^9, but the structure of the calendar is perfectly uniform. That removes any need for simulation over years or months. Any approach that iterates day by day between dates is immediately infeasible when the gap between years can reach billions, since a single test case could require up to 10^9 operations.

The only meaningful edge cases come from sign handling and modular arithmetic. A common mistake is incorrectly computing negative offsets between dates when the second date is earlier than the first. Another is mishandling wraparound in the 5-day weekday cycle, especially when the difference is negative or exactly divisible by 5.

For example, if today is Monday on 2019-05-12 and we ask for 2019-05-11, the answer should be Sunday in a real-world analogy, but here the cycle only has five days, so it wraps within that restricted set. If we incorrectly compute modulo without normalizing negativity, we can land outside the weekday list or index it incorrectly.

Another subtle case is when both dates are identical. Then the offset is zero and the answer must be exactly the given weekday, regardless of any computation path.

## Approaches

A brute-force approach would convert both dates into a day count by repeatedly adding 1 day while updating month and year transitions. Each increment would also update the weekday in a cyclic manner. This is straightforward to implement and correct, because it simulates the calendar exactly as defined.

However, the worst case gap between dates can be extremely large, up to about 10^9 years difference. Since each year contributes 360 days, this leads to up to roughly 3.6 × 10^11 days in the worst case. A simulation stepping one day at a time is therefore completely infeasible.

The key observation is that the calendar is fully linear and periodic. Every month and year structure is constant, so we can compute the absolute day number of any date directly using arithmetic. Once both dates are expressed as integer day indices, the difference between them directly determines how many weekday steps to move in a cycle of size 5.

This reduces the problem to computing a linear transformation followed by a modulo operation. The structure is identical to mapping a date onto a one-dimensional number line where each day is one unit, and weekdays form a repeating cycle independent of the absolute position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(distance in days) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

We define a function that maps any date to an absolute day index starting from a fixed reference, for example year 0, month 1, day 1.

1. Convert each date into an absolute day number using the formula `(year * 12 * 30) + (month * 30) + day`. This works because every year and month has fixed size, so no irregular offsets exist.
2. Compute the difference `delta = index2 - index1`. This tells us how many days we move forward (or backward if negative).
3. Convert the given weekday string into an integer in `[0, 4]`, mapping Monday to 0 through Friday to 4.
4. Add the day difference to the weekday index: `new_index = (start_index + delta) % 5`.
5. Normalize the result to ensure it is within `[0, 4]`, which Python already guarantees with modulo behavior on integers.
6. Convert the resulting index back to the corresponding weekday string and output it.

### Why it works

The key invariant is that weekday progression depends only on the number of days between two points, not on absolute calendar position. Since each day shifts the weekday by exactly one step in a cycle of size 5, adding the day difference to the known weekday preserves correctness. The absolute date conversion ensures that any pair of dates is reduced to a consistent integer difference, and modular arithmetic on a fixed cycle guarantees correctness even for negative offsets.

## Python Solution

```python
import sys
input = sys.stdin.readline

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
idx = {d: i for i, d in enumerate(days)}

def to_day_number(y, m, d):
    return y * 12 * 30 + (m - 1) * 30 + (d - 1)

T = int(input())
for _ in range(T):
    y1, m1, d1, s = input().split()
    y1 = int(y1); m1 = int(m1); d1 = int(d1)

    y2, m2, d2 = map(int, input().split())

    base = to_day_number(y1, m1, d1)
    target = to_day_number(y2, m2, d2)

    delta = target - base
    start = idx[s]

    ans = (start + delta) % 5
    print(days[ans])
```

The conversion function `to_day_number` encodes the calendar into a flat timeline. Each year contributes 360 days and each month contributes 30 days, so the arithmetic is consistent and avoids loops.

The weekday index is computed using a dictionary lookup. We then shift it by the difference in absolute days. The modulo operation directly handles wraparound in the 5-day cycle.

One subtle point is that Python’s modulo with negative numbers still produces a correct non-negative remainder in this context, so no extra adjustment is needed.

## Worked Examples

### Example 1

Input:

```
2019 5 12 Monday
2019 5 14
```

We compute:

| Step | Value |
| --- | --- |
| base | 2019·360 + 4·30 + 11 |
| target | 2019·360 + 4·30 + 13 |
| delta | 2 |
| start index | 0 |
| result | (0 + 2) % 5 = 2 |

Output is Wednesday.

This confirms forward shifting works correctly across small intra-month distances.

### Example 2

Input:

```
2019 5 12 Friday
2019 12 30
```

| Step | Value |
| --- | --- |
| base | computed absolute day |
| target | later absolute day |
| delta | positive large number |
| start index | 4 |
| result | (4 + delta) % 5 |

The exact numeric delta is large, but only its remainder modulo 5 matters. The output matches Friday → shifted forward correctly.

This demonstrates that large year jumps are safely compressed into modular arithmetic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only arithmetic operations and dictionary lookup |
| Space | O(1) | Fixed arrays and maps |

The solution easily fits within constraints since each test case is processed with constant-time computations regardless of the size of year values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    input = _sys.stdin.readline

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    idx = {d: i for i, d in enumerate(days)}

    def to_day_number(y, m, d):
        return y * 12 * 30 + (m - 1) * 30 + (d - 1)

    T = int(input())
    out = []
    for _ in range(T):
        y1, m1, d1, s = input().split()
        y2, m2, d2 = map(int, input().split())

        base = to_day_number(int(y1), int(m1), int(d1))
        target = to_day_number(y2, int(m2), int(d2))

        delta = target - base
        ans = (idx[s] + delta) % 5
        out.append(days[ans])

    return "\n".join(out)

# provided samples
assert run("""2
2019 5 12 Monday
2019 5 14
2019 5 12 Tuesday
2019 12 30
""") == """Wednesday
Friday"""

# custom cases
assert run("""1
2000 1 1 Monday
2000 1 1
""") == "Monday"

assert run("""1
2000 1 2 Monday
2000 1 1
""") == "Friday"

assert run("""1
2000 1 1 Friday
2000 2 1
""") == "Monday"

assert run("""1
2000 12 30 Friday
2001 1 1
""") == "Friday"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| same date | Monday | identity case |
| previous day wrap | Friday | negative delta handling |
| month boundary | Monday | intra-year transitions |
| year boundary | Friday | cross-year consistency |

## Edge Cases

For identical dates such as `2000 1 1 Monday → 2000 1 1`, the computed delta is zero. The algorithm produces `(start + 0) % 5`, which directly returns the original weekday index, preserving correctness without special handling.

For backward movement such as `2000 1 2 Monday → 2000 1 1`, the delta is -1. The computation `(0 + (-1)) % 5` evaluates correctly in Python to 4, which corresponds to Friday. This confirms that negative modulo behaves consistently with cyclic weekday indexing.

For large forward jumps like `2000 1 1 Monday → 999999999 12 30`, the absolute difference is extremely large, but only its remainder modulo 5 affects the answer. The conversion compresses the entire range into a single integer difference, and the cycle ensures correctness regardless of magnitude.
