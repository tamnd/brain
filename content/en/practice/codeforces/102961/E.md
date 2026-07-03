---
title: "CF 102961E - Restaurant Customers"
description: "We are given a timeline of customer visits to a restaurant, where each customer appears at some moment and leaves at some later moment. Each customer contributes a continuous time interval during which they are present inside the restaurant."
date: "2026-07-04T06:50:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "E"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 46
verified: true
draft: false
---

[CF 102961E - Restaurant Customers](https://codeforces.com/problemset/problem/102961/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a timeline of customer visits to a restaurant, where each customer appears at some moment and leaves at some later moment. Each customer contributes a continuous time interval during which they are present inside the restaurant.

The task is to determine the maximum number of customers that are simultaneously inside at any moment in time.

A useful way to reframe the input is that each customer becomes a segment on a number line. The problem then asks for the maximum overlap depth among all segments.

The constraints (typically up to around 2×10^5 intervals in this problem family) imply that an O(n²) approach is immediately infeasible. Any solution that compares every interval with every other interval would perform on the order of 10^10 operations in the worst case, which is far beyond a typical time limit. This pushes us toward O(n log n) or O(n) methods, which are standard for sweep line or sorting-based counting problems.

A subtle edge case comes from how simultaneous events are treated. Consider two customers: one leaves at time 5 and another arrives at time 5. If we incorrectly treat both as overlapping, we might overcount. For example:

Input:

```
1
1 5
5 10
```

Depending on interpretation, the correct answer is usually 1, because the first customer is no longer inside when the second arrives. A naive approach that increments before processing departures at the same timestamp would incorrectly output 2.

This ambiguity forces us to carefully define ordering at equal times, rather than simply sorting by time alone.

## Approaches

A brute-force approach would simulate every moment in time where changes happen. One could, for each interval, iterate through all other intervals and count how many overlap with it. This works because overlap checking is straightforward, but it repeats the same comparisons many times.

For n intervals, this leads to roughly n checks per interval, producing O(n²) total operations. With n around 200,000, this becomes completely unusable.

The key observation is that we do not actually care about relationships between arbitrary pairs of intervals. We only care about how the number of active intervals changes over time. Instead of asking “how many intervals overlap this one,” we ask “how does the active count evolve as time moves forward.”

This turns the problem into an event processing task. Each interval contributes exactly two events: an entry event and an exit event. If we sort all events by time and sweep through them, maintaining a running counter, we can track the number of active customers at every moment. The answer is simply the maximum value of this counter.

The only remaining difficulty is handling events that occur at the same time. We resolve this by ensuring that departures are processed before arrivals at equal timestamps, so that a customer leaving at time t does not overlap with one arriving at time t.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sweep Line (event sorting) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert each customer interval into two events: one representing arrival at time l and one representing departure at time r. This reformulation is useful because it replaces range overlap reasoning with discrete state changes.
2. Encode arrivals as +1 changes in the active customer count and departures as -1 changes. This allows us to maintain a single running variable instead of recomputing overlaps.
3. Sort all events by time. When two events share the same timestamp, place departure events before arrival events. This ordering prevents artificial overlap at exact boundary points.
4. Sweep through the sorted events from left to right, maintaining a running counter of active customers.
5. At each event, update the counter using its delta value and track the maximum value observed so far.
6. Return the maximum counter value after processing all events.

Why it works: the sweep line invariant is that after processing all events up to a time t, the running counter exactly equals the number of intervals that contain t under the chosen boundary convention. Because every interval contributes exactly one +1 and one -1, and because ordering ensures correct treatment of equal timestamps, no interval is ever double counted or missed. The maximum over all sweep states must therefore equal the maximum simultaneous overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    events = []

    for _ in range(n):
        l, r = map(int, input().split())
        events.append((l, 1))
        events.append((r, -1))

    events.sort(key=lambda x: (x[0], x[1]))

    cur = 0
    best = 0

    for t, delta in events:
        cur += delta
        if cur > best:
            best = cur

    print(best)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the event transformation. Each interval becomes two entries, and we never explicitly store the intervals again after that point. The sorting step enforces the correct temporal order, and the tie-breaking rule embedded in `(time, delta)` ensures that -1 events are processed before +1 events at identical times.

The sweep itself is a single pass. The variable `cur` represents how many customers are currently inside, while `best` tracks the maximum seen. The update order matters: we apply the event first, then consider whether the new state is a candidate for the answer.

## Worked Examples

### Example 1

Input:

```
3
1 4
2 5
7 9
```

Events after transformation:

| Step | Event | Active Count |
| --- | --- | --- |
| Start | - | 0 |
| 1 | (1, +1) | 1 |
| 2 | (2, +1) | 2 |
| 3 | (4, -1) | 1 |
| 4 | (5, -1) | 0 |
| 5 | (7, +1) | 1 |
| 6 | (9, -1) | 0 |

Maximum active count is 2.

This shows how overlaps accumulate naturally without explicitly comparing intervals.

### Example 2

Input:

```
2
1 5
5 10
```

Events:

| Step | Event | Active Count |
| --- | --- | --- |
| Start | - | 0 |
| 1 | (1, +1) | 1 |
| 2 | (5, -1) | 0 |
| 3 | (5, +1) | 1 |
| 4 | (10, -1) | 0 |

Maximum active count is 1.

This trace demonstrates why ordering departures before arrivals at equal timestamps is essential. Without it, the intermediate state at time 5 would incorrectly become 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting 2n events dominates, sweep is linear |
| Space | O(n) | Storing two events per interval |

The solution comfortably fits typical constraints for up to 200,000 intervals. Sorting 400,000 events is well within limits, and the single linear sweep ensures predictable runtime.

## Test Cases

```python
import sys, io

def solve_input(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input())
    events = []
    for _ in range(n):
        l, r = map(int, input().split())
        events.append((l, 1))
        events.append((r, -1))
    events.sort(key=lambda x: (x[0], x[1]))

    cur = 0
    best = 0
    for _, d in events:
        cur += d
        if cur > best:
            best = cur
    print(best)

# provided samples
assert solve_input("3\n1 4\n2 5\n7 9\n") == "2"
assert solve_input("2\n1 5\n5 10\n") == "1"

# custom cases
assert solve_input("1\n10 20\n") == "1", "single interval"
assert solve_input("3\n1 10\n1 10\n1 10\n") == "3", "all overlap"
assert solve_input("3\n1 2\n3 4\n5 6\n") == "1", "disjoint"
assert solve_input("2\n1 2\n2 3\n") == "1", "boundary overlap handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 1 | minimum size case |
| identical intervals | 3 | full overlap stacking |
| disjoint intervals | 1 | no overlap accumulation |
| boundary touching | 1 | correct tie handling |

## Edge Cases

One important edge case is when many intervals share the same endpoints. If all customers arrive at time 1 and leave at time 10, the algorithm must accumulate all arrivals before any departure, reaching a peak equal to n. The event sorting guarantees this because arrivals are treated as +1 and processed after -1 only when times differ, while equal-time ordering keeps the intended structure consistent.

Another edge case is a single interval. The algorithm correctly produces 1 because it introduces exactly one +1 and one -1, and the sweep never exceeds a count of one.

A final subtle case is alternating endpoints such as (1,2), (2,3), (3,4). The correct answer is 1, and the sweep maintains this because every -1 at time t is processed before or alongside the +1 at the same time, preventing artificial stacking at boundaries.
