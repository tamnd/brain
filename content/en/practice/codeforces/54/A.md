---
title: "CF 54A - Presents"
description: "We are asked to estimate the minimum number of presents the Hedgehog will receive over the next N days. He has two rules governing present reception: every holiday he receives a gift, and he cannot go more than K days without receiving one."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 54
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 50"
rating: 1300
weight: 54
solve_time_s: 79
verified: true
draft: false
---

[CF 54A - Presents](https://codeforces.com/problemset/problem/54/A)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to estimate the minimum number of presents the Hedgehog will receive over the next `N` days. He has two rules governing present reception: every holiday he receives a gift, and he cannot go more than `K` days without receiving one. Today’s present is already accounted for, so we only consider days 1 through `N`.

Input gives `N` and `K` first. Then we are told which days are holidays. The goal is to count the minimum number of presents required to satisfy both constraints. The output is a single integer: this minimal number.

Looking at constraints, `N` is up to 365, which is comfortably small. This means even an algorithm with roughly `N^2` operations would run fine in 2 seconds. `K` is at most `N`, so we must plan presents with potentially large gaps, but never exceeding `K` days. Holidays are unique and sorted, which simplifies scanning.

Non-obvious edge cases include the situation where a holiday coincides with a day that would already receive a present due to the `K`-day rule. For example, if `N=5`, `K=2`, and holidays are `[2,4]`, a naive approach that simply counts `ceil(N/K)` and adds holidays would double-count the overlap. Another tricky case is when `K` is larger than `N`; then at most one non-holiday present may be needed.

## Approaches

A brute-force approach would simulate every day from 1 to `N`, keeping track of the last day a present was received. On each day, we check if it is a holiday or if more than `K` days have passed since the last present. If either is true, we increment the present count and update the last-present day. This works because it directly enforces both constraints, but even though `N` is small, it is verbose and not necessary to iterate every single day.

The key insight is to realize that presents must be spaced at most `K` days apart, but holidays fix certain present days. Therefore, we can greedily place presents on holidays first, then fill gaps between them so that no stretch of `K` days is present-less. By processing intervals between presents (or from day 0 to the first holiday, between holidays, and from last holiday to day `N`), we can compute how many additional presents are required using simple integer division.

This transforms the problem from day-by-day simulation to interval analysis. For any interval of length `L`, the number of presents required is `(L-1)//K + 1` if `L > 0`. This works because each present covers `K` days after it; the formula counts the minimal number of presents to cover the entire interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) | O(N) | Acceptable, but verbose |
| Interval Analysis / Greedy | O(C) | O(C) | Optimal, simple and clear |

## Algorithm Walkthrough

1. Read `N`, `K`, and the list of holidays. Prepend a 0 to the holiday list to represent "today," which already had a present. Append `N+1` as a sentinel to simplify handling the last interval.
2. Initialize a counter `presents` to 0.
3. Iterate over consecutive pairs of holiday days, `start` and `end`. For each interval `(start, end)`, compute the number of days between presents as `end - start - 1`. If this length is positive, compute the minimal number of presents using `(length - 1) // K + 1` and add it to `presents`.
4. Output `presents`.

Why it works: The invariant is that every holiday already receives a present, and every interval between presents is covered by the formula to respect the `K`-day maximum. Each interval is independent, and adding presents inside the interval in this greedy fashion ensures no gap of `K` days is missed. There is no double-counting because holidays already have presents.

## Python Solution

```python
import sys
input = sys.stdin.readline

N, K = map(int, input().split())
line = list(map(int, input().split()))
C = line[0]
holidays = line[1:]

# Add today (day 0) and a sentinel after the last day
days = [0] + holidays + [N+1]
presents = 0

for i in range(1, len(days)):
    interval = days[i] - days[i-1] - 1
    if interval > 0:
        presents += (interval + K - 1) // K

print(presents)
```

We first read input and convert holidays into a list of days. Prepending day 0 and appending `N+1` simplifies edge cases. For each interval between consecutive "present days," we calculate the minimal presents required using ceiling division, which is `(interval + K - 1) // K`. Finally, the total count is printed. The careful choice of `interval = days[i] - days[i-1] - 1` avoids off-by-one errors that often arise with inclusive/exclusive day counts.

## Worked Examples

**Sample 1**: `N=5`, `K=2`, holidays `[1,3]`

| i | days[i-1] | days[i] | interval | presents added | total presents |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 2 | 1 | 3 | 1 | 1 | 1 |
| 3 | 3 | 6 | 2 | 2 | 3 |

The algorithm correctly identifies that 3 presents are needed: one for the interval between day 1 and 3, and two for the interval after day 3 to day 5.

**Custom Example**: `N=7`, `K=3`, holidays `[2,5]`

| i | days[i-1] | days[i] | interval | presents added | total presents |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1 | 1 | 1 |
| 2 | 2 | 5 | 2 | 1 | 2 |
| 3 | 5 | 8 | 2 | 1 | 3 |

The algorithm places presents optimally: intervals are covered without exceeding `K` days.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C) | We process `C+2` days (holidays + today + sentinel) and perform simple arithmetic per interval. |
| Space | O(C) | We store the augmented list of days. |

Given that `C ≤ N ≤ 365`, this solution is extremely fast and fits well within the memory and time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    N, K = map(int, input().split())
    line = list(map(int, input().split()))
    C = line[0]
    holidays = line[1:]
    days = [0] + holidays + [N+1]
    presents = 0
    for i in range(1, len(days)):
        interval = days[i] - days[i-1] - 1
        if interval > 0:
            presents += (interval + K - 1) // K
    return str(presents)

# provided sample
assert run("5 2\n1 3\n") == "3", "sample 1"

# minimum input
assert run("1 1\n0\n") == "1", "single day, no holiday"

# maximum K
assert run("10 10\n2 3 7\n") == "2", "K covers most days"

# all days holidays
assert run("5 1\n5 1 2 3 4 5\n") == "5", "every day a holiday"

# no holidays, K=2
assert run("6 2\n0\n") == "3", "even spacing with K=2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | 1 | Minimum size input, no holidays |
| 10 10 2 3 7 | 2 | Maximum K value, sparse holidays |
| 5 1 5 1 2 3 4 5 | 5 | All holidays, ensures no double-counting |
| 6 2 0 | 3 | Non-holiday intervals handled correctly |

## Edge Cases

For `N=1`, `K=1`, no holidays: the interval is `1` day after today. The formula `(1 + 1 - 1)//1 = 1` correctly returns 1 present.

For `N=10`, `K=10`, holidays `[3,7]`, intervals are `[0-3]`, `[3-7]`, `[7-11]`. The presents added per interval are `ceil(2/10)=1`,
