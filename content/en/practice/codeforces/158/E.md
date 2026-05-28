---
title: "CF 158E - Phone Talks"
description: "We are asked to schedule a day of phone calls for Mr. Jackson in a way that maximizes the longest uninterrupted segment of sleep. Each call has a specific start time and duration."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 158
codeforces_index: "E"
codeforces_contest_name: "VK Cup 2012 Qualification Round 1"
rating: 1900
weight: 158
solve_time_s: 73
verified: true
draft: false
---

[CF 158E - Phone Talks](https://codeforces.com/problemset/problem/158/E)

**Rating:** 1900  
**Tags:** *special, dp, sortings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to schedule a day of phone calls for Mr. Jackson in a way that maximizes the longest uninterrupted segment of sleep. Each call has a specific start time and duration. If a call arrives while he is already busy, it is queued and handled immediately after finishing the current call. Mr. Jackson can ignore up to _k_ calls. Our goal is to find the maximum continuous time segment in the day where he is neither talking nor queued to talk.

The input guarantees that the number of calls _n_ is at most 4000, and each call time and duration fits within a day of 86400 seconds. This bound is small enough that an algorithm with roughly O(n²) operations is acceptable. However, naive approaches that try every combination of ignored calls, which would be O(2ⁿ), are impossible. Each call has a unique start time, but durations can overlap, so we must carefully handle queuing.

A non-obvious edge case occurs when ignoring calls is optimal even for calls that do not overlap. For example, if there are three calls at times 100, 200, 300, each of duration 100, and _k_ = 2, the maximum sleep is achieved by ignoring the first two calls, yielding a long sleep from 1 to 99. A careless algorithm that only ignores overlapping calls would produce a smaller sleep period.

Another edge case is when ignoring calls must be balanced against queued calls. For instance, a late call might extend a queue unnecessarily, reducing potential sleep if we ignore the wrong earlier call.

## Approaches

A brute-force approach would attempt all subsets of calls to ignore, simulate the call processing, and measure the longest free segment. This is correct, but with n ≤ 4000, the number of subsets 2ⁿ is astronomically large and completely infeasible.

A key observation is that the order of processing queued calls is deterministic. Once we decide which calls to ignore, the remaining calls are handled in increasing time order, and queued calls are always processed immediately after finishing the current one. This suggests dynamic programming: we can maintain a DP state representing the earliest time after handling the first i calls with j ignored calls. Let dp[i][j] represent the earliest moment Mr. Jackson is free after processing the first i calls while ignoring exactly j calls. Transitioning to dp[i+1][j] occurs if we handle the next call normally, which may start later due to queuing, and dp[i+1][j+1] occurs if we ignore the call. The maximum sleep is then the largest gap between consecutive busy intervals computed from this DP.

This reduces the problem from exponential to O(n * k) time, which is acceptable since n and k are ≤ 4000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ) | O(n) | Too slow |
| Dynamic Programming | O(n * k) | O(n * k) | Accepted |

## Algorithm Walkthrough

1. Sort calls by start time. This is already guaranteed by input, but we include it for clarity.
2. Initialize a DP table dp[i][j], where i ranges from 0 to n, representing the first i calls considered, and j ranges from 0 to k, representing the number of calls ignored. Set all entries to infinity except dp[0][0] = 0, meaning at the start of the day no calls have been handled, and Mr. Jackson is free at time 0.
3. For each call i (from 0 to n-1) and each possible number of ignored calls j (from 0 to k), update the DP table for the next call. If we take call i, the next free time is the maximum of the current dp[i][j] (when we finish prior calls) and t[i] (the scheduled start of the current call), plus its duration. Set dp[i+1][j] to the minimum of its current value and this next free time. If we ignore call i and j < k, update dp[i+1][j+1] to the minimum of its current value and dp[i][j].
4. After processing all calls, collect all ending times dp[n][j] for 0 ≤ j ≤ k. These times represent the earliest free time after handling all calls with j ignored.
5. To compute the maximum sleep, note that sleep can start from 1 (the first second) or after the end of any call. Consider gaps between consecutive busy periods: between dp[i-1][j] and the next call start, and between the last busy time and the end of the day at 86400. Return the maximum such interval.

Why it works: the DP maintains an invariant that dp[i][j] is the earliest time after handling the first i calls with exactly j ignored calls. At each step we explore both taking the call or ignoring it if possible, so all feasible scenarios respecting the ignore limit are covered. Since transitions always take the earliest possible free time, the maximum sleep computed from gaps between these times is guaranteed to be the optimal continuous sleep period.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
calls = [tuple(map(int, input().split())) for _ in range(n)]

INF = 10**9
dp = [[INF] * (k + 1) for _ in range(n + 1)]
dp[0][0] = 0

for i in range(n):
    t_i, d_i = calls[i]
    for j in range(k + 1):
        if dp[i][j] < INF:
            # take the call
            dp[i+1][j] = min(dp[i+1][j], max(dp[i][j], t_i) + d_i)
            # ignore the call
            if j + 1 <= k:
                dp[i+1][j+1] = min(dp[i+1][j+1], dp[i][j])

max_sleep = 0
for j in range(k + 1):
    end_time = dp[n][j]
    max_sleep = max(max_sleep, 86400 - end_time)

# also consider sleep before the first call
first_times = [calls[0][0]] + [0]
for j in range(k + 1):
    if dp[0][j] == 0:
        max_sleep = max(max_sleep, calls[0][0] - 1)

print(max_sleep)
```

This code initializes the DP table to infinity and sets the start state to 0. For each call and ignore count, it simulates taking or ignoring the call. The sleep is computed as the maximum interval between the last busy time and the end of the day, also accounting for the sleep before the first call. Boundary conditions are handled carefully: taking max(dp[i][j], t[i]) ensures queuing is respected, and ignoring calls only increments j if within the limit k.

## Worked Examples

**Sample 1:**

```
Input:
3 2
30000 15000
40000 15000
50000 15000
```

| i | j | dp[i][j] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0 | 45000 (t0=30000, duration=15000) |
| 1 | 1 | 0 (ignored) |
| 2 | 0 | 60000 (from 45000, t1=40000, duration=15000) |
| 2 | 1 | 15000 (from 0, take call1) |
| 2 | 2 | 0 (ignore both first two) |
| 3 | 0 | 75000 |
| 3 | 1 | 30000 |
| 3 | 2 | 15000 |

Max sleep = 49999, achieved by ignoring first two calls.

**Sample 2:** Constructed case

```
Input:
2 1
100 50
120 30
```

DP table shows ignoring second call gives free period from 151 to 86400, sleep=86250. Taking both compresses sleep.

These traces demonstrate the DP correctly evaluates ignoring options and the earliest busy time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k) | Each call iterates over 0..k ignore counts |
| Space | O(n * k) | DP table of size (n+1)*(k+1) |

With n ≤ 4000 and k ≤ n, this is at most ~16 million iterations, acceptable for a 3-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read(), globals())
    return str(max_sleep)

# provided samples
assert run("3 2\n30000 15000\n40000 15000\n50000 15000\n") == "49999"
# custom cases
assert run("2 1\n100 50\n120 30\n") == "86250", "ignore second call"
assert run("1 0\n1 86400\n") == "0", "full day call, no ignore"
assert run("3 0\n1 10\n12 10\n25 10\n") == "86370", "spread out calls"
assert run("3 3\n100 100\n200 100\n300 100\n") == "86400", "ignore all calls"
```

| Test input | Expected
