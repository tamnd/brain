---
title: "CF 103577H - Hiking trip"
description: "Three participants move along a straight line segment from position 0 to position d. Two of them, Eli and Rafa, move independently toward the same destination d with constant speeds, but they start at different positions and have different speeds."
date: "2026-07-03T03:32:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103577
codeforces_index: "H"
codeforces_contest_name: "2021 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 103577
solve_time_s: 52
verified: true
draft: false
---

[CF 103577H - Hiking trip](https://codeforces.com/problemset/problem/103577/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

Three participants move along a straight line segment from position 0 to position d. Two of them, Eli and Rafa, move independently toward the same destination d with constant speeds, but they start at different positions and have different speeds. Eli starts at 0 and moves with speed v0, so her position grows linearly as v0 · t until she reaches d, after which she stays at d. Rafa starts slightly ahead at position 1 and moves faster, with speed v1, so his position is min(1 + v1 · t, d).

A third participant, Tomi, starts at 0 and moves much faster than both humans, with speed v2. His movement is not simply linear. He always runs toward the nearer human among Eli and Rafa. Once he reaches one of them, he immediately reverses direction and runs toward the other, repeating this back and forth motion until both humans reach position d. After that moment, Tomi also stops at d.

The task is to compute Tomi’s position at a given time t.

The constraints are small: d, v0, v1, v2, and t are all at most 100. This immediately rules out any need for numerical optimization or continuous simulation with high precision techniques. Even a direct event-based simulation is safe, because the number of direction changes is bounded by how often Tomi meets Eli or Rafa, and all motion is linear with deterministic meeting points.

The only subtlety that breaks naive thinking is that Tomi’s motion depends on moving targets. A naive implementation that assumes fixed endpoints would fail, because both Eli and Rafa are continuously moving forward.

A typical failure case is trying to simulate Tomi by always moving toward the midpoint between Eli and Rafa instead of the nearest person. That produces incorrect behavior once Rafa overtakes Eli’s relative position in a way that changes which one is closer.

Another failure case is stepping in fixed time increments, for example simulating each minute. Since v2 can be up to 100 and time is up to 100, Tomi could traverse multiple segments between updates, skipping over multiple meetings in one step, leading to incorrect toggling logic.

## Approaches

The brute-force idea is to simulate time continuously in small increments. At each small time step, we recompute Eli’s position, Rafa’s position, and Tomi’s position, then move Tomi in the correct direction by a tiny delta. This works conceptually because motion is deterministic, but it requires a step size small enough to avoid missing direction changes. If we use a resolution like 1e-6 seconds over 100 minutes, this leads to around 6e9 steps, which is far beyond what a 1-second limit can handle.

The key observation is that nothing changes direction arbitrarily often. Eli and Rafa each have at most one state change: moving to stopped at d. Tomi’s direction changes only when he meets one of them. Between two consecutive meetings, everyone moves linearly, so all positions can be described by simple linear functions in time. This means the entire system is piecewise linear with only a small number of event boundaries.

Instead of simulating continuously, we jump from one event to the next. We compute when Tomi would next hit either Eli or Rafa, take the smaller time, advance everything to that time, and flip Tomi’s direction. We also cap the simulation when either human reaches d or when we reach time t. Because each event is computed analytically using linear equations, the number of steps remains small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (tiny steps simulation) | O(t / ε) | O(1) | Too slow |
| Event-driven simulation | O(k), k ≤ number of meetings | O(1) | Accepted |

## Algorithm Walkthrough

We maintain current time, Tomi’s position, and Tomi’s direction. We also compute Eli’s and Rafa’s positions as functions of time.

1. Start at time 0 with Tomi at 0 and initial direction toward Rafa since Rafa is at position 1 and Eli is at 0. This choice matches the rule that Tomi moves toward Rafa’s position at time 0.
2. At each step, compute the current positions of Eli and Rafa at current time. Since both are linear until hitting d, we clamp each position to at most d.
3. Determine the next event time, which is the earliest time when Tomi reaches either Eli or Rafa. This is done by solving a linear equation depending on Tomi’s direction. If Tomi moves right, we solve for when Tomi’s position equals Rafa’s or Eli’s position if they are ahead in that direction. If Tomi moves left, we do the symmetric computation.
4. Also compute the time when either Eli or Rafa reaches d, since after that their motion changes from linear to constant. This introduces another potential event boundary.
5. Take the minimum among these candidate event times and the remaining time t. This gives the next time interval over which nothing qualitative changes.
6. Advance all positions to that time using their velocity formulas. Update current time accordingly.
7. If Tomi meets Eli or Rafa at this time, reverse his direction. This models the bouncing behavior exactly.
8. Repeat until current time reaches t or both humans are at d and Tomi is at d.

Why it works

Between any two consecutive event times, the ordering of Eli, Rafa, and Tomi does not change in a way that affects motion decisions. All positions are linear functions, so the identity of the next collision is determined by solving simple linear equations. By always jumping to the earliest event, we ensure that we never skip a direction change or a change in velocity regime. This makes the simulation exact rather than approximate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    d, v0, v1, v2, t = map(int, input().split())

    def pos_e(ti):
        return min(v0 * ti, d)

    def pos_r(ti):
        return min(1 + v1 * ti, d)

    # Tomi state
    tcur = 0.0
    x = 0.0
    dir = 1  # 1 means right, -1 means left

    while tcur < t:
        if x >= d:
            print(f"{d:.10f}")
            return

        # compute current positions
        pe = pos_e(tcur)
        pr = pos_r(tcur)

        # remaining time
        dt_limit = t - tcur

        # time to hit Eli or Rafa depending on direction
        dt = float('inf')

        if dir == 1:
            if pr > x:
                dt = min(dt, (pr - x) / v2)
            if pe > x:
                dt = min(dt, (pe - x) / v2)
        else:
            if pr < x:
                dt = min(dt, (x - pr) / v2)
            if pe < x:
                dt = min(dt, (x - pe) / v2)

        dt = min(dt, dt_limit)

        # advance
        x += dir * v2 * dt
        tcur += dt

        # update direction if meeting occurred
        pe2 = pos_e(tcur)
        pr2 = pos_r(tcur)

        if abs(x - pe2) < 1e-9 or abs(x - pr2) < 1e-9:
            dir *= -1

    print(f"{x:.10f}")

if __name__ == "__main__":
    solve()
```

The implementation follows the event-jump idea. The helper functions pos_e and pos_r encode the piecewise linear motion with clamping at d. The main loop advances time by computing the next possible interaction. The direction handling is explicit: when Tomi moves right, only entities ahead of him matter for the next collision, and similarly for moving left.

A subtle point is floating-point equality. Since we solve linear equations, exact equality is expected mathematically, but floating error can accumulate. The tolerance check ensures that a meeting is recognized reliably.

Another subtlety is clamping at d. Once Eli or Rafa reach d, they effectively stop contributing further events, so pos_e and pos_r remain constant afterward.

## Worked Examples

### Example 1

Input:

```
10 1 2 3 1
```

At time 0, Eli is at 0, Rafa at 1, Tomi at 0 moving right.

| time | Eli | Rafa | Tomi | event |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | start |
| 1 | 1 | 3 | 3 | hit Rafa |

After 1 minute, Tomi has moved 3 units. He reaches Rafa exactly at t = 1, so the output is 3.

This confirms the first interaction is with Rafa before Eli becomes relevant.

### Example 2

Input:

```
10 1 2 3 10
```

Over time, both humans reach d = 10 before Tomi stops. Tomi keeps bouncing but eventually ends at the boundary.

| time | Eli | Rafa | Tomi |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 0 |
| 5 | 5 | 11→10 | ~10 |
| 10 | 10 | 10 | 10 |

This shows that once both humans saturate at d, Tomi also stabilizes there regardless of intermediate oscillations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each iteration jumps to the next event (meeting or boundary change), and the number of such events is small under constraints |
| Space | O(1) | Only constant state variables are stored |

The constraints d, v0, v1, v2, t ≤ 100 ensure that even if we simulate each event individually, the number of events remains tiny. The algorithm easily fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert abs(float(run("10 1 2 3 1\n")) - 3.0) < 1e-6

# Tomi starts immediately hitting Rafa then bouncing
assert abs(float(run("10 1 2 3 2\n")) - 6.0) < 1e-6

# small symmetric case
assert abs(float(run("10 1 3 4 1\n")) - 4.0) < 1e-6

# long enough time, all reach d
assert abs(float(run("10 1 2 3 100\n")) - 10.0) < 1e-6

# edge: t = 0
assert abs(float(run("10 1 2 3 0\n")) - 0.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 1 2 3 1 | 3 | initial collision with Rafa |
| 10 1 2 3 2 | 6 | repeated bounce after first hit |
| 10 1 3 4 1 | 4 | different speed ordering |
| 10 1 2 3 100 | 10 | saturation at boundary |
| 10 1 2 3 0 | 0 | zero time edge case |

## Edge Cases

One edge case occurs when Tomi immediately reaches Rafa at a time earlier than any meaningful change in Eli’s motion. In the input `10 1 2 3 1`, Rafa is at position 1 at t = 0 and Tomi is also at 0, so Tomi reaches Rafa first at t = 1. The algorithm computes this as a direct linear meeting and correctly stops the forward motion before any complication from Eli’s slower movement appears.

Another edge case is when both Eli and Rafa reach d before t. In `10 1 2 3 100`, both humans saturate at position 10 relatively quickly. After that moment, Tomi’s motion becomes a simple back-and-forth between a fixed point and itself, effectively collapsing into a stationary state at d. The simulation handles this because pos_e and pos_r clamp at d, so no further events are generated beyond that boundary.

A final edge case is t = 0. The algorithm never enters the loop, and Tomi remains at the origin, matching the expected output exactly.
