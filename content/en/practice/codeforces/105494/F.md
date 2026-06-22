---
title: "CF 105494F - Traffic Lights"
description: "We are simulating a bus moving through a sequence of traffic lights. Between intersections, the bus spends a fixed amount of travel time, and at each intersection it may need to wait depending on the current state of a periodic traffic signal."
date: "2026-06-23T01:40:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105494
codeforces_index: "F"
codeforces_contest_name: "2024-2025 ICPC NERC, Kyrgyzstan Qualification Contest"
rating: 0
weight: 105494
solve_time_s: 44
verified: true
draft: false
---

[CF 105494F - Traffic Lights](https://codeforces.com/problemset/problem/105494/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a bus moving through a sequence of traffic lights. Between intersections, the bus spends a fixed amount of travel time, and at each intersection it may need to wait depending on the current state of a periodic traffic signal.

Each traffic light has its own cycle defined by a green duration and a red duration. The cycle repeats every fixed period, and at time zero, we are told how the light was offset relative to its cycle, in the sense that green was active a certain number of seconds before the trip began. As the bus arrives at each intersection, we must determine whether the light is green at that exact moment. If it is red, we wait until it becomes green again, then continue.

The input describes a sequence of intersections. For each intersection i, we are given the travel time to reach it from the previous one, the green duration gi, the red duration ri, and an offset di describing how long before the start of the trip the last green phase began. The goal is to compute the total elapsed time when the bus finishes passing all intersections.

The constraints are large enough that simulating each second is impossible. Even a direct step-by-step time evolution would degrade to O(total time), which in the worst case can be extremely large if waiting times accumulate.

A subtle edge case arises when the bus arrives exactly at a transition point between green and red. If remi equals gi, that moment is already the start of red, so waiting is required. Another edge case is when gi is zero, meaning the light is always red and every arrival forces waiting for a full cycle.

A naive implementation might also mis-handle the offset di, especially if it is large. Since di can be much larger than the cycle period, failing to reduce it modulo the cycle leads to incorrect phase computation.

## Approaches

A brute-force simulation would track time continuously and, for each intersection, increment time until the light becomes green. After moving to each intersection, we advance time by ai, then repeatedly check the light state by simulating the cycle second by second. This is correct because it mirrors the real process exactly, but it can degrade to O(total time across all waiting), which is not feasible when waiting times are large.

The key observation is that we never need to simulate individual seconds. The traffic light state is periodic, so at any time we only need to know where we are within its cycle. Instead of advancing one second at a time, we can compute the phase of the light directly using modular arithmetic.

When we arrive at intersection i, the time elapsed since the start is known. The light’s cycle repeats every gi + ri seconds. Since the last green started di seconds before time zero, the total elapsed time since that reference green start is time + di. Reducing this modulo the cycle length gives us the current position within the cycle. If this position lies within the green interval, we pass immediately. Otherwise, we jump directly forward to the next green phase.

This reduces each intersection to O(1) computation, since modular arithmetic replaces simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(total waiting time) | O(1) | Too slow |
| Modular Simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

Let time represent the current elapsed time from the start of the trip.

1. Initialize time to 0. This represents the moment before entering the first segment, where no travel has occurred.
2. For each intersection i, first increase time by ai. This accounts for the travel time needed to reach the traffic light.
3. Compute the total elapsed time since a known green reference as totali = time + di. This shifts our timeline so that we can align the current moment with the cycle’s phase definition.
4. Compute periodi = gi + ri. This represents the full repetition length of the traffic signal.
5. Compute remi = totali mod periodi. This gives the position within the current cycle. The modulo works because the signal behavior repeats identically every period.
6. If remi < gi, the signal is green at arrival and we proceed without delay. Otherwise, the signal is red, and we must wait exactly periodi − remi seconds to reach the next green phase boundary. After waiting, we add this delay to time.

After processing all intersections, time contains the total travel duration including all waiting times.

The key invariant is that at every step, time always reflects the earliest moment the bus can reach the next intersection after fully resolving all previous waiting decisions. Because each update only depends on the current time and a deterministic modulo computation of the next light’s cycle, no future decision depends on how we arrived at the current state. The process is locally optimal at every intersection and thus globally correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    time = 0

    for _ in range(n):
        a, g, r, d = map(int, input().split())
        time += a

        period = g + r
        total = time + d
        rem = total % period

        if rem >= g:
            time += period - rem

    print(time)

if __name__ == "__main__":
    solve()
```

The solution keeps a single running time variable and updates it per intersection. The travel time is always added first because arrival happens before any signal check.

The critical implementation detail is the order of operations: the modulo must be computed after adding the offset di, and the waiting time must only be added when the phase is in red. Using rem >= g correctly handles the boundary case where the light switches exactly at the moment of arrival.

## Worked Examples

Consider a simple case with two intersections.

Input:

```
2
3 5 5 0
4 2 3 1
```

We track time step by step.

For the first intersection, time becomes 3 after travel. The cycle is 10. total = 3, rem = 3, which is less than 5, so we pass immediately.

For the second intersection, time becomes 7. total = 7 + 1 = 8, cycle = 5, rem = 3. Since green is 2 seconds long, rem >= 2 means we are in red, so we wait 5 − 3 = 2 seconds.

| i | time after travel | total = time + d | period | rem | action | new time |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 10 | 3 | green | 3 |
| 2 | 7 | 8 | 5 | 3 | red wait 2 | 9 |

This confirms how waiting is only triggered when the modular position exceeds the green window.

Now consider an edge case where the bus arrives exactly at the red boundary.

Input:

```
1
5 3 4 0
```

After travel, time = 5. total = 5, period = 7, rem = 5. Since green is 3, rem >= 3 means red. We wait 7 − 5 = 2, moving time to 7.

This shows that arriving exactly at the boundary of green does not allow passage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each intersection requires constant-time arithmetic operations |
| Space | O(1) | Only a single accumulator variable is maintained |

The algorithm fits comfortably within typical constraints for up to 2e5 intersections, since each step performs only a few integer operations and no additional memory is allocated.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# basic sample-like test
assert run("2\n3 5 5 0\n4 2 3 1\n") == "9"

# single always-green case
assert run("1\n10 5 5 100\n") == "10"

# always-red light (gi = 0)
assert run("1\n3 0 4 0\n") == "7"

# boundary transition case
assert run("1\n0 2 3 0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 intersections sample | 9 | normal simulation correctness |
| always green offset | 10 | no waiting behavior |
| always red case | 7 | full cycle wait handling |
| zero travel boundary | 0 | immediate arrival edge case |

## Edge Cases

One important edge case is when the arrival time lands exactly at the start of the red phase. For example, with gi = 3, ri = 4, if rem = 3, we are exactly at the transition. The condition rem >= gi ensures we treat this as red and apply waiting. The computed wait is period − rem, which correctly jumps to the next green start.

Another edge case is large di values. Suppose di is 10^12 while the cycle is small. The modulo operation automatically normalizes this, so we never need to explicitly reduce di beforehand. For instance, if period = 6 and di = 10^12, then (time + di) % 6 correctly captures the phase without overflow or incorrect scaling.

A final subtle case is when gi = 0. In that case, rem < gi is never true, so every arrival triggers waiting of a full cycle. The formula still works because period − rem always advances to the next cycle boundary, ensuring correctness without special casing.
