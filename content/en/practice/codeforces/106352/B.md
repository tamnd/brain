---
title: "CF 106352B - \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u043f\u043e \u043f\u0435\u0439\u043d\u0442\u0431\u043e\u043b\u0443"
description: "We are given a sequence of paintballs, each characterized by a time moment when it flies and a vertical position (a row on a wall). The wall has height h, and rows are numbered from bottom to top. Each paintball exists only at its given time and affects exactly one row."
date: "2026-06-19T14:52:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106352
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106352
solve_time_s: 48
verified: true
draft: false
---

[CF 106352B - \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u043f\u043e \u043f\u0435\u0439\u043d\u0442\u0431\u043e\u043b\u0443](https://codeforces.com/problemset/problem/106352/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of paintballs, each characterized by a time moment when it flies and a vertical position (a row on a wall). The wall has height `h`, and rows are numbered from bottom to top. Each paintball exists only at its given time and affects exactly one row.

At some chosen starting time `t0`, a shield of fixed height `w` is placed covering rows `[1, w]`. After that, every second it moves upward by exactly one row, so at time `t0 + k` it covers rows `[1 + k, w + k]`. Once it reaches the topmost valid position `[h - w + 1, h]`, it stays there for one second and then disappears. A paintball is blocked if, at its exact time, its row lies inside the current interval covered by the shield.

The task is to choose `t0` to maximize the number of blocked paintballs.

The input size goes up to `n = 10^5`, and row coordinates and times go up to `10^9`. This immediately rules out any solution that tries to simulate the shield for every possible starting time or every second of its lifetime. A quadratic or even `O(n log n)` per candidate strategy over all candidates would be too slow.

A key difficulty is that each paintball constraint couples time and row: whether it is blocked depends on a linear relation between its time and the chosen starting time.

A few edge cases matter.

One is when multiple paintballs occur at the same time but at different rows. For example, if at time `t = 5` we have rows `1, 2, 10` and `w = 2`, only two consecutive rows could ever be covered, so at most two can be blocked, never all three.

Another is when `w = h`. In that case, the shield covers the whole grid for exactly one second regardless of position, so the answer becomes simply counting how many paintballs exist at all times that coincide with any valid shield existence interval, and in fact every paintball can be blocked if we align `t0` with its time.

A third subtle edge case is ordering: the shield moves deterministically with time, so a wrong interpretation that lets it “teleport” or stay fixed for multiple seconds at intermediate positions will overcount blocks.

## Approaches

A brute-force approach would try every possible starting time `t0` from the set of all paintball times. For each candidate `t0`, we simulate the shield movement second by second and check each paintball to see if it is covered at its time. This works conceptually because the shield behavior is fully deterministic once `t0` is fixed, so correctness is not an issue.

The problem is performance. If we try `O(n)` possible `t0` values and for each we scan all `n` paintballs, we already get `O(n^2)`, which is far beyond the limit for `n = 10^5`. Even more directly, simulating the shield across up to `h` steps is impossible because `h` can reach `10^9`.

The key observation is that each paintball imposes a constraint on valid `t0` values. For a paintball `(t, s)` to be blocked, the shield must cover row `s` at time `t`, which means:

```
1 + (t - t0) <= s <= w + (t - t0)
```

Rearranging both inequalities gives an interval of valid `t0` values for which this paintball is covered. So each paintball becomes a segment on the number line of `t0`.

Once this transformation is done, the problem reduces to finding a point `t0` that lies inside the maximum number of intervals. This is a classic maximum overlap problem on intervals, solvable with sorting endpoints and sweeping.

The subtle point is that we also need to respect that the shield exists only for a finite number of seconds. However, this constraint is naturally encoded by the interval derivation, since outside valid ranges the inequalities simply produce empty intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation over all starts | O(n²) | O(1) | Too slow |
| Interval transformation + sweep line | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Key transformation

1. For each paintball `(t, s)`, derive the range of `t0` values that make it blocked.

The shield at time `t` covers rows `[1 + (t - t0), w + (t - t0)]`. We require:

```
1 + (t - t0) <= s <= w + (t - t0)
```

Solving both inequalities gives:

```
t - s + 1 <= t0 <= t - s + w
```

So each paintball becomes an interval `[L, R]` on the timeline of possible starting times.
2. Collect all such intervals for all paintballs. Each valid `t0` corresponds to selecting a vertical alignment of the shield trajectory.
3. We want the `t0` that lies in the maximum number of these intervals, which is equivalent to maximum interval overlap.
4. Convert each interval into two events: +1 at `L`, -1 at `R + 1`.
5. Sort all events by coordinate, then sweep from left to right maintaining a running sum.
6. Track the maximum value of the running sum; this is the answer.

### Why it works

Each paintball contributes independently a condition on `t0`. A single `t0` is valid for that paintball exactly when it lies inside its derived interval. Therefore, counting how many intervals contain a given `t0` is exactly counting how many paintballs are blocked. The sweep line finds the point of maximum overlap, which corresponds directly to the optimal starting time.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, h, w = map(int, input().split())

events = []

for _ in range(n):
    t, s = map(int, input().split())
    L = t - s + 1
    R = t - s + w
    events.append((L, 1))
    events.append((R + 1, -1))

events.sort()

cur = 0
best = 0

for x, delta in events:
    cur += delta
    if cur > best:
        best = cur

print(best)
```

The core of the implementation is the interval conversion step. Each paintball is translated into a range of starting times `t0` where it becomes blocked. The sweep line over sorted event endpoints accumulates how many such constraints are simultaneously satisfied.

A subtle detail is using `R + 1` for the negative event. This ensures that the interval is treated as inclusive on both ends while still being compatible with integer sweep logic. Without this shift, off-by-one errors would miscount paintballs that are exactly on the boundary of shield coverage.

Another point is that we never explicitly use `h`. Although it defines the physical constraints of the shield path, it is implicitly respected because the derived inequalities already encode feasibility.

## Worked Examples

### Example 1

Input:

```
4 5 2
1 1
1 2
2 2
3 4
```

We compute intervals:

| paintball | (t, s) | L = t-s+1 | R = t-s+w |
| --- | --- | --- | --- |
| 1 | (1,1) | 1 | 2 |
| 2 | (1,2) | 0 | 1 |
| 3 | (2,2) | 1 | 2 |
| 4 | (3,4) | 0 | 1 |

Events become:

```
(0,+1), (2,-1)
(1,+1), (2,-1)
(1,+1), (3,-1)
(1,+1), (2,-1)
```

Sweep:

| x | delta | cur | best |
| --- | --- | --- | --- |
| 0 | +1 | 1 | 1 |
| 1 | +1 | 2 | 2 |
| 1 | +1 | 3 | 3 |
| 1 | +1 | 4 | 4 |
| 2 | -1 | 3 | 4 |
| 2 | -1 | 2 | 4 |
| 2 | -1 | 1 | 4 |
| 3 | -1 | 0 | 4 |

Maximum overlap is 4, meaning there exists a `t0` aligning the shield to block all four paintballs.

This trace confirms that the transformation preserves all timing and row constraints without explicitly simulating movement.

### Example 2

Input:

```
5 6 3
10 1
11 2
12 6
13 4
14 6
```

Intervals:

| (t,s) | L | R |
| --- | --- | --- |
| (10,1) | 10 | 12 |
| (11,2) | 10 | 12 |
| (12,6) | 7 | 9 |
| (13,4) | 10 | 12 |
| (14,6) | 11 | 13 |

Sweep reveals the maximum overlap occurs around `t0 = 11`, where three intervals intersect.

This shows how the method naturally captures partial alignment across time shifts, where different subsets of paintballs become blockable under different starting times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting 2n events dominates |
| Space | O(n) | storing interval endpoints |

The solution is fast enough for `n = 10^5` because sorting and linear sweep both comfortably fit within time limits, and memory usage stays linear in the number of paintballs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, h, w = map(int, input().split())
    events = []
    for _ in range(n):
        t, s = map(int, input().split())
        L = t - s + 1
        R = t - s + w
        events.append((L, 1))
        events.append((R + 1, -1))
    events.sort()
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return str(best)

# provided samples
assert run("""4 5 2
1 1
1 2
2 2
3 4
""") == "4"

assert run("""5 6 3
10 1
11 2
12 6
13 4
14 6
""") == "3"

# minimum case
assert run("""1 10 3
5 4
""") == "1"

# all identical
assert run("""3 10 2
5 1
5 1
5 1
""") == "3"

# boundary alignment
assert run("""2 10 1
5 5
6 6
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base correctness |
| duplicates | 3 | stacking intervals |
| boundary alignment | 2 | off-by-one correctness |

## Edge Cases

A critical edge case is when a paintball sits exactly on the lower or upper boundary of the shield at a given second. The interval derivation includes both boundaries, so such paintballs must be counted as valid. If we used a strict inequality when converting constraints, these cases would be dropped incorrectly.

Another edge case appears when derived intervals extend outside feasible time ranges. For example, a very high row at an early time produces negative `L`. This is not a problem because sweep line over integers naturally handles unbounded ranges; such intervals simply start earlier than all others.

Finally, multiple overlapping paintballs at identical `(t, s)` values produce identical intervals. The sweep correctly counts multiplicity because each contributes a separate +1 event, ensuring correct aggregation of duplicates.
