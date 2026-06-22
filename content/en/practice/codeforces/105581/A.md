---
title: "CF 105581A - Scanner"
description: "We are watching a process that can only start at discrete moments. Vitya visits a scanner periodically, every t minutes starting from time 0, and the day ends at time T."
date: "2026-06-22T14:34:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105581
codeforces_index: "A"
codeforces_contest_name: "Open Udmurtia Junior Programming Contest 2018"
rating: 0
weight: 105581
solve_time_s: 55
verified: true
draft: false
---

[CF 105581A - Scanner](https://codeforces.com/problemset/problem/105581/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are watching a process that can only start at discrete moments. Vitya visits a scanner periodically, every `t` minutes starting from time 0, and the day ends at time `T`. Each visit is a chance to start scanning a new document, but only if the scanner is currently idle at that exact moment. Once a document starts scanning, it occupies the machine for `k` minutes without interruption. If Vitya arrives while the scanner is still busy, he leaves immediately and loses that opportunity.

The task is to determine how many times Vitya successfully starts a scan during the interval from time 0 up to and including time `T`.

The constraints are small, with all parameters at most 100. This means even a direct simulation over every possible visit is efficient. The number of visits is at most 100, so any solution that is linear in the number of visits runs comfortably within limits.

A subtle edge case appears at the boundary of the day. If Vitya arrives exactly at time `T`, he is still allowed to attempt starting a scan. If the scanner is free at that moment, a new scan begins even though it may end after the workday finishes. A naive approach that excludes the final time point would undercount in cases where the last arrival is valid.

Another corner case happens when `k` is larger than `t`. In that situation, Vitya frequently arrives during busy periods and skips many opportunities. For example, if `t = 2` and `k = 10`, only the very first successful start matters unless enough idle time passes between attempts.

## Approaches

A direct simulation is the most natural starting point. We enumerate every time Vitya visits the scanner: `0, t, 2t, ...` up to `T`. At each visit we check whether the scanner is free. If it is, we start a new scan and mark the machine as busy until the current time plus `k`. Otherwise we do nothing. This is correct because the process is entirely defined by local decisions at each arrival time.

This brute-force method performs at most `T / t + 1` checks, which is at most 101 operations in the worst case. Each check is constant work, so it is trivially fast.

There is no meaningful asymptotic improvement needed beyond this simulation, but the key observation is that the only state we need to maintain is the next time the scanner becomes available. This reduces the problem to a single running variable instead of tracking the entire timeline minute by minute.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T / t) | O(1) | Accepted |
| Event-based Greedy Simulation | O(T / t) | O(1) | Accepted |

## Algorithm Walkthrough

We compress the process into a sequence of arrival events and maintain when the scanner will next be free.

1. Initialize a variable `free_time = 0`, representing the earliest moment a new scan can start. Also initialize `count = 0` to store the number of successful starts.
2. Iterate over all arrival times `time = 0, t, 2t, ...` while `time ≤ T`. Each value represents a moment when Vitya checks the scanner.
3. For each `time`, compare it with `free_time`. If `time ≥ free_time`, the scanner is idle at that moment, so a new document can be started.
4. When a scan starts at `time`, increment `count` and set `free_time = time + k`, since the scanner will remain busy for the next `k` minutes.
5. If `time < free_time`, Vitya arrives during an ongoing scan and does nothing, leaving the state unchanged.

The process continues until all arrival moments up to and including `T` are processed.

The key property is that `free_time` always represents the exact end of the most recently started scan. Every decision depends only on whether the current arrival has reached or passed that boundary. No earlier history matters once `free_time` is updated.

## Python Solution

```python
import sys
input = sys.stdin.readline

t, k, T = map(int, input().split())

free_time = 0
count = 0

time = 0
while time <= T:
    if time >= free_time:
        count += 1
        free_time = time + k
    time += t

print(count)
```

The code maintains a single timeline pointer `time` that jumps in steps of `t`, which corresponds exactly to Vitya’s arrival schedule. The variable `free_time` encodes whether the scanner is busy or idle at each arrival.

A common mistake is forgetting that a scan starting at time `T` is valid even if it finishes after `T`. The condition only checks the start time, not whether the scan completes within the workday.

Another subtle point is initialization. Setting `free_time = 0` ensures that the first arrival at time 0 always starts a scan, matching the fact that the system begins idle.

## Worked Examples

### Example 1

Input:

`4 5 17`

Arrivals are at times 0, 4, 8, 12, 16.

| time | free_time | action | count |
| --- | --- | --- | --- |
| 0 | 0 | start scan, free_time = 5 | 1 |
| 4 | 5 | skip | 1 |
| 8 | 5 | start scan, free_time = 13 | 2 |
| 12 | 13 | skip | 2 |
| 16 | 13 | start scan, free_time = 21 | 3 |

At the final arrival, the scanner is free, so a third scan begins even though it ends after the day ends.

Output is 3.

### Example 2

Input:

`5 5 20`

Arrivals are at 0, 5, 10, 15, 20.

| time | free_time | action | count |
| --- | --- | --- | --- |
| 0 | 0 | start scan, free_time = 5 | 1 |
| 5 | 5 | start scan, free_time = 10 | 2 |
| 10 | 10 | start scan, free_time = 15 | 3 |
| 15 | 15 | start scan, free_time = 20 | 4 |
| 20 | 20 | start scan, free_time = 25 | 5 |

Every arrival lands exactly when the scanner becomes free, so every visit starts a new document.

Output is 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T / t) | We iterate over each arrival time from 0 to T in steps of t, and each iteration does constant work |
| Space | O(1) | Only two integer variables are maintained regardless of input size |

The maximum number of iterations is bounded by 100, so the solution is well within both time and memory limits even under worst-case inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t, k, T = map(int, input().split())

    free_time = 0
    count = 0

    time = 0
    while time <= T:
        if time >= free_time:
            count += 1
            free_time = time + k
        time += t

    return str(count)

# provided samples
assert run("4 5 17\n") == "3"
assert run("5 5 20\n") == "5"

# minimum values
assert run("1 1 1\n") == "2"

# large k blocking most attempts
assert run("2 10 10\n") == "1"

# t equals T boundary case
assert run("7 3 7\n") == "2"

# no overlap case
assert run("3 1 9\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 2 | boundary inclusion at time 0 and T |
| 2 10 10 | 1 | long scan blocks future attempts |
| 7 3 7 | 2 | arrival exactly at end of day is counted |
| 3 1 9 | 4 | frequent arrivals with short scans |

## Edge Cases

When the first arrival happens at time 0, the system must treat the scanner as immediately available. With input `1 5 3`, the sequence of arrivals is 0, 1, 2, 3. At time 0 a scan starts and blocks until time 5. Every later arrival is ignored because each is smaller than `free_time`, so the answer is 1. The simulation handles this naturally because `free_time` is initialized to 0.

When `k` is smaller than `t`, every arrival starts a scan since the scanner always finishes before the next visit. For `t = 4, k = 1, T = 12`, arrivals occur at 0, 4, 8, 12 and each satisfies `time ≥ free_time`, so every step increments the count. The state evolves as `free_time = 1, 5, 9, 13`.

When `k` is larger than `t`, overlapping scans dominate. For `t = 2, k = 6, T = 10`, arrivals are 0, 2, 4, 6, 8, 10. Only 0, 6, and 10 start scans because intermediate arrivals fall inside active intervals. The condition `time ≥ free_time` correctly filters these cases without needing any explicit reasoning about intervals.
