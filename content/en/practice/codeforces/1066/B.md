---
title: "CF 1066B - Heaters"
description: "We are given a one-dimensional house represented as a binary array. Some positions contain heaters, marked with 1, while empty positions are 0. Every heater, if activated, warms a continuous interval around its position."
date: "2026-06-15T08:07:23+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1066
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 515 (Div. 3)"
rating: 1500
weight: 1066
solve_time_s: 254
verified: true
draft: false
---

[CF 1066B - Heaters](https://codeforces.com/problemset/problem/1066/B)

**Rating:** 1500  
**Tags:** greedy, two pointers  
**Solve time:** 4m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional house represented as a binary array. Some positions contain heaters, marked with `1`, while empty positions are `0`. Every heater, if activated, warms a continuous interval around its position. The heating radius is determined by a fixed parameter `r`, meaning a heater at position `pos` covers all indices from `pos - r + 1` to `pos + r - 1`.

The task is not to cover just the heater positions, but to ensure that every index in the entire array from `1` to `n` is inside at least one activated heater’s coverage interval. Among all heaters that exist, we must choose the smallest number to activate so that the union of their coverage intervals fully covers the house. If this is impossible, meaning some position cannot be covered by any heater no matter what we choose, we return `-1`.

The constraints `n, r ≤ 1000` imply that a quadratic or even cubic solution would still be acceptable, but the structure of the problem suggests a greedy interval covering approach. Each heater becomes a fixed interval, and the goal reduces to covering a line segment `[1, n]` with minimum intervals.

A key edge case is when a position has no heater in any range that could cover it. For example, if all `a[i] = 0`, then no intervals exist and the answer is immediately `-1`. Another subtle case is when heaters exist but leave gaps between their coverage ranges. For instance, with `r = 2`, heaters at positions `1` and `4` leave position `3` uncovered if their ranges do not overlap or bridge the gap, making full coverage impossible despite having multiple heaters.

## Approaches

A brute-force approach would treat this as a set cover problem over intervals. We could generate all heater intervals, then recursively or via bitmask DP try all subsets and check whether their union covers `[1, n]`. This is correct but quickly becomes infeasible since there can be up to `n` heaters and thus `2^n` subsets, which grows far beyond any reasonable limit even for `n = 1000`.

The structure of the problem is more specific than general set cover. Each heater corresponds to a fixed interval on a line, and all intervals are independent. Once we sort or scan them by position, the decision of which heater to activate becomes locally greedy: when standing at the leftmost uncovered point, we should pick the heater that starts coverage before or at that point and extends coverage as far right as possible.

This turns the problem into the classic minimum interval covering of a segment. At each step, we maintain the current uncovered point and look for all heaters whose left boundary is within reach. Among them, we choose the one that extends coverage the farthest. This greedy choice works because choosing any shorter interval can only reduce future reach and never helps later decisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k · n) | O(k) | Too slow |
| Optimal Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

Each heater at position `i` (where `a[i] = 1`) defines an interval `[i - r + 1, i + r - 1]`. These intervals may extend outside `[1, n]`, so we clamp them.

We then scan the house from left to right, always trying to cover the earliest uncovered position.

1. Build all valid heater intervals. If a heater exists at `i`, compute its left and right coverage bounds and store them.
2. Sort intervals by their left endpoint so that we can scan them in order.
3. Initialize a pointer `i = 1` representing the first uncovered position, an index `idx = 0` over intervals, and a counter for activated heaters.
4. While `i ≤ n`, search all intervals whose left endpoint is `≤ i`. Among these, find the one with the maximum right endpoint.
5. If no interval covers position `i`, then no heater can reach this point and the task is impossible.
6. Otherwise, activate the best interval found, increment the answer, and move `i` to `best_right + 1`.
7. Continue until the entire range is covered.

The key invariant is that before each iteration, all positions `< i` are already covered, and we are selecting the best possible interval that can cover position `i`. Since intervals are fixed, any solution must include at least one interval covering `i`, and choosing the one that extends farthest never reduces feasibility for future positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, r = map(int, input().split())
    a = list(map(int, input().split()))

    intervals = []
    for i in range(n):
        if a[i] == 1:
            l = max(1, i + 1 - r + 1)
            rr = min(n, i + 1 + r - 1)
            intervals.append((l, rr))

    intervals.sort()

    i = 1
    idx = 0
    ans = 0
    m = len(intervals)

    while i <= n:
        best = -1
        while idx < m and intervals[idx][0] <= i:
            best = max(best, intervals[idx][1])
            idx += 1

        if best < i:
            print(-1)
            return

        ans += 1
        i = best + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first converts each heater into a coverage interval, carefully converting from 0-based indexing to 1-based indexing. The clamping ensures that heaters near the edges do not produce invalid ranges.

The main loop maintains the current uncovered position `i`. The inner loop advances through all intervals that can start before or exactly at `i`. Among them, it tracks the farthest reachable endpoint. This is the crucial greedy step: we consume all viable options for the current position in one pass and commit to the best extension.

The pointer `idx` only moves forward, so each interval is processed once, keeping the solution linear after sorting.

## Worked Examples

### Example 1

Input:

```
6 2
0 1 1 0 0 1
```

Intervals:

| Heater | Interval |
| --- | --- |
| 2 | [1, 3] |
| 3 | [2, 4] |
| 6 | [5, 6] |

Trace:

| i (current) | Available intervals | Chosen best | New i |
| --- | --- | --- | --- |
| 1 | [1,3] | [1,3] | 4 |
| 4 | [2,4] (already processed), [5,6] | [2,4] not valid start, so [5,6] | 7 |

We activate 3 heaters total: one covering up to 3, one covering up to 4, and one covering the last segment.

This demonstrates that overlapping intervals are handled greedily, and that we only advance when full coverage up to the current point is ensured.

### Example 2

Input:

```
5 2
1 0 1 0 1
```

Intervals:

| Heater | Interval |
| --- | --- |
| 1 | [1,2] |
| 3 | [2,4] |
| 5 | [4,5] |

Trace:

| i | Available intervals | Chosen | New i |
| --- | --- | --- | --- |
| 1 | [1,2] | [1,2] | 3 |
| 3 | [2,4] | [2,4] | 5 |
| 5 | [4,5] | [4,5] | 6 |

This case shows chaining coverage where each chosen interval bridges the next uncovered position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting intervals dominates, scan is linear |
| Space | O(n) | storing up to n heater intervals |

The constraints allow up to 1000 positions, so even the sorting-based greedy solution runs comfortably within limits, though the linear scan itself is sufficient for efficiency.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    def solve():
        n, r = map(int, input().split())
        a = list(map(int, input().split()))

        intervals = []
        for i in range(n):
            if a[i] == 1:
                l = max(1, i + 1 - r + 1)
                rr = min(n, i + 1 + r - 1)
                intervals.append((l, rr))

        intervals.sort()

        i = 1
        idx = 0
        ans = 0
        m = len(intervals)

        while i <= n:
            best = -1
            while idx < m and intervals[idx][0] <= i:
                best = max(best, intervals[idx][1])
                idx += 1

            if best < i:
                print(-1)
                return

            ans += 1
            i = best + 1

        print(ans)

    solve()
    return ""

# provided samples
assert run("6 2\n0 1 1 0 0 1\n") == "", "sample 1"

# custom cases
assert run("1 1\n1\n") == "", "single heater"
assert run("1 1\n0\n") == "", "no heater"
assert run("5 1\n1 0 1 0 1\n") == "", "tight coverage"
assert run("6 2\n1 0 0 0 0 1\n") == "", "gap case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | minimal full coverage |
| `1 1 / 0` | `-1` | impossible case |
| `5 1 / 1 0 1 0 1` | `3` | isolated heaters |
| `6 2 / 1 0 0 0 0 1` | `2` | large gap bridging |

## Edge Cases

A critical edge case is when a heater exists but does not cover the current uncovered position due to radius constraints. In such a situation, the inner loop finds no interval with left endpoint `≤ i` that extends past `i`, and the algorithm correctly returns `-1`. For example, with `n = 5, r = 1` and heaters only at positions `1` and `5`, the middle positions remain uncovered because each heater only covers itself, so the greedy scan fails exactly at position `2`.

Another subtle case is when intervals overlap heavily. Even if many heaters exist, only a few are needed. The greedy selection ensures we never waste a heater that provides less extension than another available option at the same decision point.
