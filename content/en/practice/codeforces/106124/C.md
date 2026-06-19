---
title: "CF 106124C - Crochet Competition"
description: "We are given two timestamps that describe when a crochet competition started and when it ended. Each timestamp contains a weekday together with a clock time in hours and minutes. The goal is to compute how long the competition lasted, measured in days, hours, and minutes."
date: "2026-06-19T20:02:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106124
codeforces_index: "C"
codeforces_contest_name: "2025-2026 ICPC Nordic Collegiate Programming Contest (NCPC 2025)"
rating: 0
weight: 106124
solve_time_s: 50
verified: true
draft: false
---

[CF 106124C - Crochet Competition](https://codeforces.com/problemset/problem/106124/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two timestamps that describe when a crochet competition started and when it ended. Each timestamp contains a weekday together with a clock time in hours and minutes. The goal is to compute how long the competition lasted, measured in days, hours, and minutes.

The subtlety is that the time is cyclic over weeks. If the end time appears earlier in the week than the start time, the competition must have wrapped around into the next week or even several weeks later. The only special rule is that if the two timestamps are exactly identical, the duration is defined to be exactly one week.

The output must express the difference in a normalized form: days, hours, and minutes, omitting any zero-valued component, and formatting the remaining components in a natural English style.

The input size is constant, so the constraints are extremely small. This immediately rules out any complexity concerns beyond constant-time parsing and arithmetic. The main difficulty is not performance but correct normalization of time differences across a repeating weekly cycle.

The most common mistakes happen when treating weekdays independently from clock time. For example, interpreting “Mon 23:00 to Mon 01:00” as a negative duration instead of wrapping to the next week leads to incorrect results. Another edge case is identical timestamps, which must produce exactly 7 days rather than zero duration.

## Approaches

A brute-force mindset would try to simulate time minute by minute, advancing from the start timestamp until reaching the end timestamp. This is conceptually correct because time is discrete in minutes, and each step moves forward by one minute. However, in the worst case, the gap could be multiple weeks, meaning up to about 10,000 minutes or more of unnecessary iteration. While still small in practice, this approach is unnecessary and hides the real structure of the problem.

The key observation is that both timestamps live in a single periodic cycle of 7 days × 24 hours × 60 minutes. If we map each timestamp into an absolute minute index inside a week, we can compute differences directly. Once both times are converted into “minutes since the start of a week”, the only ambiguity is whether the end lies before the start in that modular space. If it does, we simply add one full week to the end time. This converts the problem into a straightforward subtraction.

From there, the remaining task is to decompose the total difference into days, hours, and minutes using integer division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force minute simulation | O(D) where D is duration in minutes | O(1) | Accepted but unnecessary |
| Modular conversion | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We treat each timestamp as an absolute minute offset from the beginning of a reference week, such as Monday 00:00.

1. Map weekdays to integers from 0 to 6, where Monday is 0 and Sunday is 6. This gives a consistent ordering of days in the week.
2. Convert each timestamp into total minutes from the start of the week using the formula:

`total = weekday * 1440 + hour * 60 + minute`.

This works because each day has 1440 minutes.
3. Compare the two values. If the end value is strictly less than the start value, we interpret this as wrapping into the next week, so we add 7 × 1440 minutes to the end value.
4. If both timestamps are identical, return exactly one week, which is 7 × 1440 minutes, without further decomposition. This rule overrides normal subtraction.
5. Compute the difference in minutes: `diff = end - start`.
6. Decompose the result into days, hours, and minutes:

`days = diff // 1440`,

`hours = (diff % 1440) // 60`,

`minutes = diff % 60`.
7. Build the output string by including only non-zero components in the order days, hours, minutes, and format them with correct singular or plural forms.

### Why it works

The correctness comes from representing all timestamps in a linearized time axis over a fixed cyclic period. Any real-world timestamp in this problem is equivalent to a unique position in a 10080-minute cycle. By converting everything into this linear space and only applying a single wrap correction when necessary, we preserve the true temporal order. The decomposition step is exact because integer division over fixed unit sizes cleanly partitions minutes into days, hours, and minutes without overlap or ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

days_map = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6
}

def parse(line):
    d, t = line.strip().split()
    h, m = map(int, t.split(":"))
    return days_map[d] * 1440 + h * 60 + m

a = parse(input())
b = parse(input())

WEEK = 7 * 1440

if a == b:
    diff = WEEK
else:
    if b < a:
        b += WEEK
    diff = b - a

days = diff // 1440
diff %= 1440
hours = diff // 60
minutes = diff % 60

parts = []
if days:
    parts.append(f"{days} day" + ("s" if days != 1 else ""))
if hours:
    parts.append(f"{hours} hour" + ("s" if hours != 1 else ""))
if minutes:
    parts.append(f"{minutes} minute" + ("s" if minutes != 1 else ""))

print(", ".join(parts))
```

The parsing step converts the weekday and clock time into a single integer representing minutes since the start of the week. The wrap handling is crucial: when the end time is earlier in the week, we explicitly shift it forward by one full week so subtraction remains valid.

The formatting logic builds the output incrementally and ensures that zero components are omitted entirely, which is required by the statement’s output rules.

## Worked Examples

### Example 1

Input:

Mon 08:00

Mon 15:00

We map both times into minutes:

| Step | Start | End |
| --- | --- | --- |
| Weekday index | 0 | 0 |
| Hour/min conversion | 480 | 900 |
| Total minutes | 480 | 900 |

Difference is 420 minutes.

| Step | Value |
| --- | --- |
| diff | 420 |
| days | 0 |
| hours | 7 |
| minutes | 0 |

Output becomes:

7 hours

This confirms the algorithm correctly handles same-day differences without any wrap logic.

### Example 2

Input:

Mon 10:00

Wed 08:59

| Step | Start | End |
| --- | --- | --- |
| Weekday index | 0 | 2 |
| Hour/min conversion | 600 | 2×1440 + 539 = 3419 |
| Total minutes | 600 | 3419 |

No wrap is needed since end ≥ start.

| Step | Value |
| --- | --- |
| diff | 2819 |
| days | 1 |
| hours | 22 |
| minutes | 59 |

Output:

1 day, 22 hours, 59 minutes

This shows correct decomposition across multiple units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time parsing and arithmetic on two timestamps |
| Space | O(1) | Fixed mapping and a few integers |

The computation is purely arithmetic and independent of any input size growth. It comfortably fits within any reasonable constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    # assume solution is wrapped in main logic below
    return _sys.stdout.getvalue().strip()

# Since the solution is script-style, we instead test logic directly:

def solve(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdin
    sys.stdin = StringIO(inp)

    days_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}

    def parse(line):
        d,t=line.strip().split()
        h,m=map(int,t.split(":"))
        return days_map[d]*1440+h*60+m

    a=parse(sys.stdin.readline())
    b=parse(sys.stdin.readline())

    WEEK=7*1440

    if a==b:
        diff=WEEK
    else:
        if b<a:
            b+=WEEK
        diff=b-a

    d=diff//1440
    diff%=1440
    h=diff//60
    m=diff%60

    parts=[]
    if d:
        parts.append(f"{d} day"+("s" if d!=1 else ""))
    if h:
        parts.append(f"{h} hour"+("s" if h!=1 else ""))
    if m:
        parts.append(f"{m} minute"+("s" if m!=1 else ""))

    sys.stdin = backup
    return ", ".join(parts)

# provided samples
assert solve("Mon 08:00\nMon 15:00\n") == "7 hours"
assert solve("Mon 10:00\nWed 08:59\n") == "1 day, 22 hours, 59 minutes"

# custom cases
assert solve("Mon 00:00\nMon 00:00\n") == "7 days", "exact same time"
assert solve("Sun 23:59\nMon 00:00\n") == "1 minute", "wrap across week boundary"
assert solve("Fri 10:00\nFri 10:01\n") == "1 minute", "minute precision"
assert solve("Sat 12:00\nSun 11:00\n") == "23 hours", "less than a day"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Mon 00:00 → Mon 00:00 | 7 days | identical timestamps rule |
| Sun 23:59 → Mon 00:00 | 1 minute | week wrap handling |
| Fri 10:00 → Fri 10:01 | 1 minute | minute-level correctness |
| Sat 12:00 → Sun 11:00 | 23 hours | no-day boundary case |

## Edge Cases

One important edge case is when the timestamps are identical. For example:

Input:

Mon 00:00

Mon 00:00

The algorithm detects equality before any arithmetic. It directly assigns a full week of 10080 minutes. This avoids incorrectly producing zero duration, which would violate the problem specification.

Another case is wrap-around at the end of the week:

Input:

Sun 23:59

Mon 00:00

Here the end timestamp converts to a smaller numeric value than the start. The algorithm adds 10080 minutes to the end, producing a 1-minute difference. This demonstrates that ordering is preserved only after normalization into a linear weekly cycle.

A final subtle case is when the duration is less than one hour or one day. The decomposition step handles this cleanly because integer division naturally produces zero higher components, which are then omitted during formatting.
