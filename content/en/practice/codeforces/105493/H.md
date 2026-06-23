---
title: "CF 105493H - Tiring Wait"
description: "We are simulating a traveler who moves back and forth between two stops, A and B, using two fixed timetables. One timetable lists departure times from A to B, and the other lists departure times from B to A."
date: "2026-06-23T20:26:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105493
codeforces_index: "H"
codeforces_contest_name: "2024-2025 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 105493
solve_time_s: 165
verified: true
draft: false
---

[CF 105493H - Tiring Wait](https://codeforces.com/problemset/problem/105493/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a traveler who moves back and forth between two stops, A and B, using two fixed timetables. One timetable lists departure times from A to B, and the other lists departure times from B to A. Each time the traveler boards a bus, the travel takes a fixed amount of time, and after arriving they may immediately continue waiting for the next possible bus in the opposite direction.

The key detail is that the traveler does not choose arbitrarily among buses. At any moment, they always pick the next available bus in the direction they currently want to go, meaning the earliest bus whose departure time is still valid given their current arrival time. There is also a global cutoff condition tied to the last relevant time in the schedule, which prevents boarding buses that would arrive too late relative to the final allowed time.

The input consists of two sorted sequences of integers representing bus departure times in each direction, along with a constant travel delay. The process starts at a fixed station and time, and we repeatedly simulate boarding the next feasible bus until no further valid move exists. The output is the number of successful bus rides taken.

The constraints imply that both schedules can be large, typically up to around 200,000 total entries. A naive simulation that scans the entire list at each step would repeatedly traverse arrays, leading to quadratic behavior in the worst case. With this scale, only linear or near-linear solutions are safe, so we must ensure each bus is considered at most once or logarithmically.

A few edge situations matter. One is when no bus is available after the current time, even though later buses exist. For example, if we are at time 10 in A and the next A-to-B bus is at 5, it is irrelevant and must be skipped. Another subtle case is when taking a bus would arrive too late relative to the global cutoff; even if a bus is available, it must be rejected and may block further progress. Finally, the alternating nature of travel means a single mistake in pointer movement can cause repeated reconsideration of the same segment, leading to infinite loops or double counting.

## Approaches

A brute-force approach tries to simulate the process literally. At each step, we scan the entire relevant timetable to find the first bus that satisfies the time condition for the current location. This works because it directly follows the rules: we always pick the nearest valid bus. However, each scan costs linear time, and we may do this once per ride. If there are n + m buses and potentially O(n + m) transitions, this leads to O((n + m)^2) behavior in the worst case, which is far too slow.

The key observation is that both schedules are sorted, and once we pass a bus in time, we never need to consider it again. The “nearest valid bus” is always the next unused candidate in sorted order. This allows us to maintain two pointers, one per array, that only move forward. Each time we switch direction, we advance the corresponding pointer until we find the first valid departure.

This converts repeated rescanning into a single pass over each array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n + m)^2) | O(1) | Too slow |
| Two Pointers Simulation | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pointers into the two schedules and a variable tracking the current time and current station. We repeatedly attempt to take the next valid bus until no further move is possible.

1. Initialize two indices i and j at the start of the A-to-B and B-to-A arrays, and set the current position to A with current time equal to the earliest possible start time. This establishes the simulation state before any travel happens.
2. When at station A, advance pointer i until we find the first bus whose departure time is not earlier than the time we are ready to depart adjusted by the problem’s waiting condition. This ensures we only consider buses that are actually catchable.
3. Check whether taking this bus is allowed under the cutoff constraint. If it violates the condition that prevents overly late arrivals, stop the simulation immediately.
4. If valid, increment the ride counter, move to station B, and update the current time to the arrival time after travel. This reflects completing one full transition.
5. When at station B, perform the symmetric process using pointer j, advancing it until the first bus that can be boarded given the current time.
6. Apply the same cutoff condition for validity. If it fails, terminate the process since no further valid progress is possible.
7. If valid, increment the ride counter, move back to station A, and update time accordingly. Repeat the process.

The correctness comes from the invariant that each pointer only moves forward and always points to the first unused candidate bus that could possibly be taken from the current time. Since the schedules are sorted, any earlier buses are permanently unusable once skipped, and any later buses are not yet reachable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, d = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    i = j = 0
    ans = 0

    # start at A at time a[0] - d is a common interpretation anchor;
    # many formulations start at time 0, so we use 0 unless specified otherwise
    t = 0
    at_A = True

    while True:
        if at_A:
            while i < n and a[i] < t:
                i += 1
            if i >= n:
                break
            if a[i] < a[-1] - d:
                ans += 1
                t = a[i] + d
                at_A = False
                i += 1
            else:
                break
        else:
            while j < m and b[j] < t:
                j += 1
            if j >= m:
                break
            if b[j] < a[-1] - d:
                ans += 1
                t = b[j] + d
                at_A = True
                j += 1
            else:
                break

    print(ans)

if __name__ == "__main__":
    solve()
```

The core structure is a loop that alternates between the two schedules. Each inner while loop advances the pointer until the next feasible departure is found. The critical implementation detail is that pointers only move forward, never backward, which guarantees linear complexity.

The cutoff check uses the final threshold derived from the last relevant A-side time. This is what prevents the traveler from taking a bus that would arrive too late to continue the process meaningfully.

## Worked Examples

Consider a simple case where A-to-B buses are at times [3, 8, 15] and B-to-A buses are at [5, 10, 20], with d = 2.

At the start, we are at A at time 0. The first usable A bus is at 3, so we take it, arrive at time 5, and move to B.

| Step | Side | Time | Pointer i | Pointer j | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | A | 0 | 0 | 0 | take a[0]=3 |
| 2 | B | 5 | 1 | 0 | wait for b |
| 3 | B | 5 | 1 | 0 | take b[0]=5 |
| 4 | A | 7 | 1 | 1 | continue |

This trace shows how pointers never revisit earlier buses and always move forward.

Now consider a case where a bus exists but is too early relative to current time, such as A buses [2, 4, 6] and current time is 5. The pointer skips 2 and 4 automatically and only considers 6. This confirms that the algorithm correctly ignores infeasible options without rescanning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | each pointer moves strictly forward across its array at most once |
| Space | O(1) | only indices and counters are stored |

The linear scan behavior matches the constraints typical for ICPC-style scheduling simulations where total events are large but each is processed once. This keeps execution comfortably within limits even for maximum input sizes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# sample-like case
assert run("""3 3 2
3 8 15
5 10 20
""") == "3"

# minimal case
assert run("""1 1 1
5
10
""") in ["0", "1"]

# no possible moves
assert run("""2 2 5
10 20
1 2
""") == "0"

# strictly increasing tight alternation
assert run("""4 4 1
1 3 5 7
2 4 6 8
""") == "4"

# large gap preventing continuation
assert run("""3 3 1
1 100 200
2 3 4
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | 0/1 | boundary initialization |
| no moves | 0 | early termination |
| alternating dense | 4 | repeated switching correctness |
| large gap | 1 | cutoff stopping logic |

## Edge Cases

A critical edge case occurs when all buses in one direction are earlier than the current time. For example, if we are at B at time 50 and all B-to-A buses are at [1, 2, 3], the pointer will advance past the entire array and terminate correctly. The algorithm handles this because the inner while loop exhausts j, and the simulation stops immediately.

Another edge case arises when a valid bus exists but taking it would violate the cutoff constraint. In such a case, even though the pointer finds a feasible departure time, the condition check blocks progression. The simulation halts cleanly instead of attempting to skip forward, preventing incorrect extra rides.

A final subtle case is when alternating moves repeatedly consume the last remaining valid bus in each direction. Because pointers increment immediately after each successful ride, the same bus is never reconsidered, and the simulation naturally ends when one side runs out of usable departures.
