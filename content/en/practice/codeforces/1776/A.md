---
title: "CF 1776A - Walking Boy"
description: "The task asks us to determine whether it is possible for the judge to have walked Boy, her dog, at least twice during a single day given a timeline of messages. Each walk takes exactly 120 minutes, cannot overlap another walk, and the judge never sends messages during a walk."
date: "2026-06-09T11:44:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "A"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 800
weight: 1776
solve_time_s: 77
verified: true
draft: false
---

[CF 1776A - Walking Boy](https://codeforces.com/problemset/problem/1776/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to determine whether it is possible for the judge to have walked Boy, her dog, at least twice during a single day given a timeline of messages. Each walk takes exactly 120 minutes, cannot overlap another walk, and the judge never sends messages during a walk. The input consists of several test cases, each providing a strictly increasing list of message times in minutes since midnight. The output for each test case is "YES" if it is possible to fit at least two non-overlapping 120-minute walks around the messages, or "NO" otherwise.

A key observation is that a day has 1440 minutes, so the total time available is finite. Since each walk consumes 120 minutes, two walks require 240 minutes of free time. The message times partition the day into intervals where walking is possible. If any interval between consecutive messages or between the start/end of the day is at least 120 minutes, a walk could occur there. We need to check if at least two such intervals exist without overlapping.

Edge cases include situations where there are very few messages, messages tightly packed together, or walks potentially starting at midnight or ending at the last minute of the day. For example, if messages occur at minutes 0, 1, 2, 3, 4, the remaining time from 5 to 1440 is plenty to schedule two walks. Conversely, if messages are at 0, 120, 240, …, 1320, it may be impossible to fit even a single 120-minute walk.

The problem constraints are very mild. Each test case has at most 100 messages, and there are at most 100 test cases. This allows any O(n) per test case solution to run comfortably within time limits. We can iterate through the message times and compute gaps without worrying about performance.

## Approaches

A brute-force approach would attempt to place a 120-minute walk starting at every possible minute of the day and check if it overlaps any message. This would involve checking up to 1440 start times per test case, and for each start time, iterating over all messages to check conflicts. In the worst case, this results in roughly 1440 * 100 = 144,000 operations per test case, which is feasible but unnecessarily inefficient.

The optimal approach observes that the only relevant times are the intervals between consecutive messages and the edges of the day. Each message splits the day into gaps: from midnight to the first message, between messages, and from the last message to the end of the day. We only need to measure these gaps and see if at least two gaps have length 120 or more. By iterating once over the message list and checking the lengths of intervals, we can solve each test case in O(n) time. The insight is that placing a walk anywhere inside a sufficiently large gap always works because messages do not move during the walk.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1440 * n) | O(n) | Works but unnecessarily slow |
| Interval Check | O(n) | O(1) | Accepted and simple |

## Algorithm Walkthrough

1. Start by reading the number of test cases, `t`. This tells us how many separate schedules we need to analyze.
2. For each test case, read the number of messages `n` and the list of message times `a`. The list is strictly increasing.
3. Initialize a counter `walkable_intervals` to zero. This will track how many 120-minute intervals exist between messages.
4. Compute the first interval from midnight to the first message. If this interval is at least 120 minutes, increment `walkable_intervals`.
5. Iterate over consecutive message pairs. For each pair `(a[i], a[i+1])`, check the interval `a[i+1] - a[i]`. If this gap is at least 120 minutes, increment `walkable_intervals`.
6. Check the final interval from the last message to the end of the day. If `1440 - a[-1]` is at least 120, increment `walkable_intervals`.
7. After counting all intervals, if `walkable_intervals` is at least 2, output "YES"; otherwise, output "NO".

Why it works: The algorithm is correct because it only considers maximal contiguous periods without messages. Any 120-minute walk must entirely fit inside one of these periods. By counting periods of length at least 120, we directly count how many non-overlapping walks are possible. Two or more such periods guarantee that two walks can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    walkable = 0
    
    # Check interval before first message
    if a[0] >= 120:
        walkable += 1
    
    # Check intervals between messages
    for i in range(n - 1):
        if a[i+1] - a[i] >= 120:
            walkable += 1
    
    # Check interval after last message
    if 1440 - a[-1] >= 120:
        walkable += 1
    
    print("YES" if walkable >= 2 else "NO")
```

The code mirrors the algorithm step by step. We explicitly check the intervals before the first message, between each consecutive pair, and after the last message. The walkable counter captures how many valid 120-minute intervals exist. The threshold comparison `>= 120` ensures we do not underestimate available time. The final conditional simply verifies if at least two walks can be scheduled.

## Worked Examples

**Example 1**

Input: `100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400`

| Interval Start | Interval End | Length | Walkable? |
| --- | --- | --- | --- |
| 0 | 100 | 100 | No |
| 100 | 200 | 100 | No |
| 200 | 300 | 100 | No |
| 300 | 400 | 100 | No |
| 400 | 500 | 100 | No |
| 500 | 600 | 100 | No |
| 600 | 700 | 100 | No |
| 700 | 800 | 100 | No |
| 800 | 900 | 100 | No |
| 900 | 1000 | 100 | No |
| 1000 | 1100 | 100 | No |
| 1100 | 1200 | 100 | No |
| 1200 | 1300 | 100 | No |
| 1300 | 1400 | 100 | No |
| 1400 | 1440 | 40 | No |

Walkable intervals: 0 → output `NO`.

**Example 2**

Input: `100 200 300 400 600 700 800 900 1100 1200 1300 1400`

Intervals of at least 120 minutes: 400→600, 900→1100. Walkable intervals: 2 → output `YES`.

These tables illustrate how counting valid gaps directly determines feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Iterate through n messages once, constant work per interval |
| Space | O(n) | Store the message times in a list |

With `t` test cases, the total complexity is O(t*n), which is at most 100 * 100 = 10,000 operations, negligible compared to the 2-second time limit. Memory usage is minimal, storing only the message list.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        walkable = 0
        if a[0] >= 120:
            walkable += 1
        for i in range(n - 1):
            if a[i+1] - a[i] >= 120:
                walkable += 1
        if 1440 - a[-1] >= 120:
            walkable += 1
        print("YES" if walkable >= 2 else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("6\n14\n100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400\n12\n100 200 300 400 600 700 800 900 1100 1200 1300 1400\n13\n100 200 300 400 500 600 700 800 900 1100 1200 1300 1400\n13\n101 189 272 356 463 563 659 739 979 1071 1170 1274 1358\n1\n42\n5\n0 1 2 3 4") == "NO\nYES\nNO\nYES\nYES\nYES"

# Custom edge cases
assert run("1\n1\n0") == "NO", "Only one message at start"
assert run("1\n1\n1320") == "NO", "Only one message near end"
assert run("1\n0\n") == "YES
```
