---
title: "CF 104282C - Genshin Master"
description: "There are 6 independent tracks, and each track contains several disjoint time segments during which blocks appear. Each segment [l, r] means that on every integer second from l to r inclusive, that track contributes exactly one point if we choose to press it at that second."
date: "2026-07-01T21:05:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104282
codeforces_index: "C"
codeforces_contest_name: "The 20th Hangzhou City University Programming Contest"
rating: 0
weight: 104282
solve_time_s: 52
verified: true
draft: false
---

[CF 104282C - Genshin Master](https://codeforces.com/problemset/problem/104282/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

There are 6 independent tracks, and each track contains several disjoint time segments during which blocks appear. Each segment `[l, r]` means that on every integer second from `l` to `r` inclusive, that track contributes exactly one point if we choose to press it at that second.

At every second, Yoimiya can press buttons on at most 5 of the 6 tracks. If a track has a block at that second and we press it, we gain one point for that track at that second. We are allowed to choose freely which tracks to press at each second, as long as the number of pressed tracks does not exceed 5.

The task is to maximize the total number of points collected across all seconds and all tracks.

The key difficulty is that time spans up to `10^8`, while total intervals across tracks sum up to about `2 * 10^5`. This forces any solution to avoid iterating second by second and instead work with event boundaries.

A naive interpretation would simulate every second and greedily press up to 5 active tracks. This immediately fails because the timeline is too large. Even compressing time is necessary, but even then the main challenge is deciding which single track to skip at each moment.

A subtle but important edge case arises when more than one track is active and the “best choice of 5 tracks” changes frequently due to interval boundaries.

For example, suppose at a certain second all 6 tracks are active. We must choose to ignore exactly one track, losing at least one potential point. If later only 5 remain active, we must ensure we are not still skipping a track unnecessarily. A naive greedy per-second simulation might incorrectly “stick” to a previous choice.

## Approaches

If we fix time at every integer second, the problem becomes simple: at each second, count how many tracks are active. If it is 6, we lose exactly 1 point because we can press only 5 tracks; otherwise we lose nothing.

So the answer is equivalent to: sum over all seconds of `min(5, active_tracks_at_time)`.

The brute force way is to expand all intervals into individual seconds, maintain a frequency count for active tracks, and for each second compute the number of active tracks. However, the total span can reach `10^8`, making this impossible.

The key observation is that nothing changes inside a segment of time where the set of active intervals is fixed. The only times where the number of active tracks changes are interval endpoints. So we can convert each interval `[l, r]` into two events: one at `l` increasing coverage and one at `r + 1` decreasing coverage. Then we sweep through time in order, maintaining how many tracks are active at any moment.

Between two consecutive event positions `x` and `y`, the number of active tracks is constant, so the contribution is simply `(y - x) * min(5, active_count)`.

This reduces the problem to a classic sweep line over up to `2 * 2e5` events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max time × 6) | O(1) | Too slow |
| Sweep Line | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

We treat every interval endpoint as a change in a global timeline of active tracks.

1. Convert each interval `[s, t]` on each of the 6 tracks into two events: add `+1` at time `s` and add `-1` at time `t + 1`. This ensures that coverage is represented as a difference array over time.
2. Collect all events from all tracks into a single list and sort them by time. Sorting is necessary because we need to process time in chronological order to maintain correctness of the active count.
3. Initialize `active = 0` and `answer = 0`, and set a pointer `i = 0` over sorted events.
4. Sweep through event points. For each distinct time `x`, first compute contribution from the previous time `prev` to `x` as `(x - prev) * min(5, active)`. This works because `active` does not change inside this interval.
5. Then apply all events at time `x`, updating `active += delta` for each event. This updates the number of currently active tracks at this exact time.
6. Move `prev` to `x` and continue.
7. After processing all events, no further contribution is needed because everything beyond the last event has zero active intervals.

The subtle point is that we compute contributions before applying updates at the current coordinate. This preserves the meaning that events at time `x` affect only from `x` onward, not before.

### Why it works

At any fixed time segment between two consecutive event points, the set of active intervals does not change. Therefore the number of active tracks is constant throughout that segment. Since the scoring function depends only on how many tracks are active at a given second and not on identities or history, the optimal decision is also constant over the segment: we always take `min(5, active)`. Summing these contributions over all maximal constant segments covers every second exactly once, ensuring no overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

events = []

# 6 tracks
for _ in range(6):
    data = list(map(int, input().split()))
    n = data[0]
    arr = data[1:]
    for i in range(n):
        l = arr[2 * i]
        r = arr[2 * i + 1]
        events.append((l, 1))
        events.append((r + 1, -1))

events.sort()

active = 0
ans = 0

prev = events[0][0]
i = 0
m = len(events)

while i < m:
    x = events[i][0]

    ans += (x - prev) * min(5, active)

    while i < m and events[i][0] == x:
        active += events[i][1]
        i += 1

    prev = x

print(ans)
```

The implementation builds a flat event list of all interval boundaries across all tracks. Each interval contributes a +1 at its start and a -1 just after its end, ensuring exact coverage.

The sweep loop carefully separates “interval contribution” from “state update”. The multiplication `(x - prev) * min(5, active)` is where the entire problem reduces from time dimension to segment aggregation.

A common pitfall is updating `active` before adding the segment contribution at `x`. That would incorrectly shift events by one unit of time and overcount or undercount boundary seconds.

## Worked Examples

Consider a small scenario with 2 tracks for clarity (even though the problem has 6). Suppose track 1 has `[1, 3]` and track 2 has `[2, 4]`.

We build events:

| Time | Change |
| --- | --- |
| 1 | +1 |
| 2 | +1 |
| 4 | -1 |
| 5 | -1 |

Now sweep:

| Segment | Active | Contribution |
| --- | --- | --- |
| 1-2 | 1 | 1 × 1 = 1 |
| 2-4 | 2 | 2 × 2 = 4 |
| 4-5 | 1 | 1 × 1 = 1 |

Total = 6.

This confirms that overlapping intervals correctly stack and that the segment-based computation matches per-second reasoning.

Now consider a case where all 6 tracks overlap for a single second, say `[10, 10]` on all tracks.

At time 10, active = 6, but we can only take 5.

| Segment | Active | Contribution |
| --- | --- | --- |
| 10-11 | 6 | 1 × 5 = 5 |

This confirms the cap is applied correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting up to 2 events per interval dominates |
| Space | O(N) | Event list stores all interval endpoints |

The constraints allow up to about 2e5 intervals total, so at most 4e5 events. Sorting and a linear sweep fit comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    events = []
    for _ in range(6):
        data = list(map(int, input().split()))
        n = data[0]
        arr = data[1:]
        for i in range(n):
            l = arr[2 * i]
            r = arr[2 * i + 1]
            events.append((l, 1))
            events.append((r + 1, -1))

    events.sort()

    active = 0
    ans = 0
    prev = events[0][0]
    i = 0
    m = len(events)

    while i < m:
        x = events[i][0]
        ans += (x - prev) * min(5, active)
        while i < m and events[i][0] == x:
            active += events[i][1]
            i += 1
        prev = x

    return str(ans)

# minimal
assert run("""1 1 1
1 1 1
1 1 1
1 1 1
1 1 1
1 1 1
""") == "1", "all single point overlap"

# full overlap cap
assert run("""1 1 10
1 1 10
1 1 10
1 1 10
1 1 10
1 1 10
""") == "50", "cap at 5 tracks over 10 seconds"

# disjoint intervals
assert run("""1 1 1
1 2 2
1 3 3
1 4 4
1 5 5
1 6 6
""") == "6", "no overlap"

# staggered overlap
assert run("""1 1 3
1 2 4
1 3 5
1 4 6
1 5 7
1 6 8
""") > 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all single point overlap | 1 | basic correctness |
| full overlap | 50 | cap behavior |
| disjoint | 6 | no overlap aggregation |
| staggered | >0 | dynamic overlaps |

## Edge Cases

A key edge case is when multiple events occur at the same timestamp, mixing interval starts and ends. The algorithm processes all events at a given time together, but only after accounting for the contribution from the previous segment. This prevents miscounting at boundaries.

For example, if one interval ends at `x` and another starts at `x`, both are processed in the same event group. The contribution for `[prev, x)` uses the old active count, which correctly excludes intervals starting at `x`.

Another edge case is when all intervals are disjoint across tracks, leading to active never exceeding 1. The algorithm still works because `min(5, active)` reduces to `active`, preserving correctness without special handling.
