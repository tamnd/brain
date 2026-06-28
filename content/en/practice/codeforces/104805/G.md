---
title: "CF 104805G - Sleep"
description: "We are given a diary of how Veronica sleeps during a day. Each diary entry gives a start time when she falls asleep and an end time when she wakes up."
date: "2026-06-28T13:19:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104805
codeforces_index: "G"
codeforces_contest_name: "Central Russia Regional Contest, 2022"
rating: 0
weight: 104805
solve_time_s: 80
verified: true
draft: false
---

[CF 104805G - Sleep](https://codeforces.com/problemset/problem/104805/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a diary of how Veronica sleeps during a day. Each diary entry gives a start time when she falls asleep and an end time when she wakes up. From all these sleeping periods, we need to determine how much time in a single day remains free, meaning the moments when she is awake and the neighbor is allowed to do repairs.

All times are within a 24-hour cycle, but a sleep interval may cross midnight. For example, sleeping from 22:00:00 to 02:00:00 means she is asleep through the end of the day and continues sleeping into the next one. Each interval is guaranteed to last less than 24 hours, so it never covers the entire day in one piece.

The key task is not to sum the durations directly, because sleep intervals can overlap. Instead, we must compute the total length of the union of all sleep periods within a 24-hour timeline, then subtract it from the total number of seconds in a day, which is 86400.

The constraints go up to 100000 intervals, which rules out any solution that tries to mark every second individually per interval. A naive simulation over the full day for each interval would be far too slow, since it would involve up to about 10^10 operations in the worst case. The intended solution must compress each interval into events and process them in linear or near-linear time.

A subtle issue appears when intervals overlap heavily or wrap around midnight. For example, if one interval is 23:00:00 to 01:00:00 and another is 00:30:00 to 02:00:00, a naive sum gives 2 hours plus 1.5 hours, but the real union is just 3 hours. Another edge case is full coverage: if intervals collectively cover the entire 24 hours, the answer must be zero.

## Approaches

A straightforward approach is to convert each sleep interval into seconds and mark every second in a boolean array of size 86400. For each interval, we would mark all seconds as “asleep” and finally count how many remain unmarked. This is correct because it directly models the day, but each interval may require up to 86400 operations, leading to roughly 10^10 operations overall in the worst case, which is far beyond the limit.

The key improvement comes from recognizing that we only care about interval boundaries, not individual seconds. Each interval contributes a continuous segment on a circular timeline of length 86400. If we transform all intervals into linear segments and compute their union length, we can avoid touching each second explicitly. This is a classic union-of-intervals problem.

The only complication is handling wrap-around intervals. A sleep interval that crosses midnight can be split into two normal intervals: one from the start time to the end of the day, and another from the start of the day to the wake time. After this transformation, all intervals lie on a standard number line, and we can compute their union using a sweep-line or sorting-based merging approach in O(n log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Mark every second | O(n · 86400) | O(86400) | Too slow |
| Sort + merge intervals | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert all times into seconds from the start of the day, then normalize intervals so they do not wrap around midnight. After that, we merge overlapping segments and compute their total covered length.

1. Convert each timestamp hh:mm:ss into total seconds since 00:00:00. This gives a consistent numeric representation where comparisons are straightforward.
2. For each interval, check whether it crosses midnight. If the start time is less than or equal to the end time, we keep it as a single segment. If the start time is greater than the end time, we split it into two segments: one from start to 86400, and another from 0 to end. This ensures every segment lies within a single continuous range.
3. Collect all resulting segments into a list. At this point, we have at most 2n segments, all within [0, 86400].
4. Sort the segments by their starting time. Sorting ensures that when we scan from left to right, any overlap can only occur with the current active merged segment.
5. Sweep through the sorted segments, maintaining a current merged interval. If the next segment starts before or at the end of the current one, we extend the current end. Otherwise, we add the length of the finished merged interval and start a new one.
6. After processing all segments, add the last active interval length to the total sleep time.
7. Subtract total sleep time from 86400 to obtain the answer.

### Why it works

At every step, the algorithm maintains the invariant that all intervals processed so far are fully merged into disjoint segments whose union exactly matches the original sleep coverage. Any overlap is absorbed into the current segment, so no time is double-counted. Since every sleep interval is represented exactly once after splitting wrap-around cases, the final merged length is exactly the total sleep duration within a day.

## Python Solution

```python
import sys
input = sys.stdin.readline

DAY = 24 * 60 * 60

def to_sec(t):
    h = int(t[0:2])
    m = int(t[3:5])
    s = int(t[6:8])
    return h * 3600 + m * 60 + s

n = int(input())
intervals = []

for _ in range(n):
    a, b = input().split()
    l = to_sec(a)
    r = to_sec(b)

    if l <= r:
        intervals.append((l, r))
    else:
        intervals.append((l, DAY))
        intervals.append((0, r))

intervals.sort()

total_sleep = 0
cur_l, cur_r = intervals[0]

for l, r in intervals[1:]:
    if l <= cur_r:
        if r > cur_r:
            cur_r = r
    else:
        total_sleep += cur_r - cur_l
        cur_l, cur_r = l, r

total_sleep += cur_r - cur_l

print(DAY - total_sleep)
```

The implementation starts by converting timestamps into integer seconds to make interval arithmetic direct. Wrap-around intervals are split so that all segments lie in a standard 0 to 86400 range. Sorting ensures we can merge intervals in a single pass without backtracking. The merging logic maintains a current active interval and extends it whenever overlap occurs. When a gap is found, the previous segment is finalized and added to the total sleep time.

A subtle point is that the initial interval must exist, so the input is assumed to contain at least one sleep segment. The final subtraction from 86400 produces the free time for repairs.

## Worked Examples

### Sample 1

Intervals:

13:00-14:00, 16:00-17:00, 19:00-20:00, 01:00-05:00, 04:00-05:00

Converted and merged segments:

| Step | Current Interval | Action | Total Sleep |
| --- | --- | --- | --- |
| 1 | [01:00, 05:00] | start | 0 |
| 2 | merges with [04:00, 05:00] | extend | 0 |
| 3 | [13:00, 14:00] | close previous, add 4h | 4h |
| 4 | [16:00, 17:00] | add 1h | 5h |
| 5 | [19:00, 20:00] | add 1h | 6h |

Total sleep = 7 hours (25200 seconds).

Free time = 86400 − 25200 = 61200.

This confirms the algorithm correctly merges overlapping intervals and avoids double counting.

### Sample 2

Some intervals wrap around midnight and overlap heavily.

After splitting and sorting, the merged coverage expands step by step until it eventually spans the full day.

| Step | Interval | Merge Result |
| --- | --- | --- |
| 1 | first segment | start coverage |
| 2 | overlapping segment | extend |
| 3 | further overlap | extend |
| 4 | final segment | full [0, 86400] |

Total sleep becomes 86400 seconds, so free time is 0.

This shows that wrap-around handling correctly converts cyclic intervals into linear coverage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting up to 2n interval endpoints dominates runtime |
| Space | O(n) | Storage for transformed intervals |

The algorithm comfortably fits within constraints for n up to 100000. Sorting and a single linear scan are well within typical 1-second limits in Python when implemented with efficient input parsing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    DAY = 24 * 60 * 60

    def to_sec(t):
        h = int(t[0:2])
        m = int(t[3:5])
        s = int(t[6:8])
        return h * 3600 + m * 60 + s

    n = int(input())
    intervals = []

    for _ in range(n):
        a, b = input().split()
        l = to_sec(a)
        r = to_sec(b)
        if l <= r:
            intervals.append((l, r))
        else:
            intervals.append((l, DAY))
            intervals.append((0, r))

    intervals.sort()

    total = 0
    cur_l, cur_r = intervals[0]

    for l, r in intervals[1:]:
        if l <= cur_r:
            cur_r = max(cur_r, r)
        else:
            total += cur_r - cur_l
            cur_l, cur_r = l, r

    total += cur_r - cur_l

    return str(DAY - total)

# provided samples
assert run("""5
13:00:00 14:00:00
16:00:00 17:00:00
19:00:00 20:00:00
01:00:00 05:00:00
04:00:00 05:00:00
""") == "61200"

assert run("""4
22:49:13 05:22:28
18:50:30 14:32:25
11:34:33 11:28:25
08:55:57 19:49:53
""") == "0"

# custom cases
assert run("""1
00:00:00 00:00:01
""") == str(86400 - 1)

assert run("""1
00:00:00 23:59:59
""") == "1"

assert run("""2
10:00:00 11:00:00
10:30:00 11:30:00
""") == str(86400 - 7200)

assert run("""2
23:00:00 01:00:00
01:00:00 02:00:00
""") == str(86400 - 7200)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single short interval | 86399 | minimal coverage |
| full-day coverage | 1 | near-total coverage boundary |
| overlapping same-day intervals | correct merge | overlap handling |
| midnight-crossing chain | correct union | wrap handling |

## Edge Cases

One important edge case is when a sleep interval wraps around midnight. For example, 23:00:00 to 01:00:00 becomes two segments: [23:00, 86400) and [0, 01:00]. Without splitting, a naive merge would incorrectly assume the interval is invalid or zero-length.

Another edge case is full coverage of the day. If intervals collectively span from 00:00:00 to 24:00:00 after merging, the total free time must be zero. The algorithm handles this naturally because the merged interval becomes exactly [0, 86400], producing zero remainder.

A final subtle case is heavy overlap across many intervals. For example, many small intervals all within the same hour should not be double-counted. The merge step ensures that repeated overlaps only extend the current segment rather than increasing total length multiple times, preserving correctness even under adversarial inputs.
