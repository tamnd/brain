---
title: "CF 1282A - Temporarily unavailable"
description: "We are given a person moving along a straight line segment from position a to position b at constant speed 1 unit per minute. Independently, there is a network base station at position c that covers everything within distance r."
date: "2026-06-11T19:26:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1282
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 610 (Div. 2)"
rating: 900
weight: 1282
solve_time_s: 119
verified: true
draft: false
---

[CF 1282A - Temporarily unavailable](https://codeforces.com/problemset/problem/1282/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a person moving along a straight line segment from position `a` to position `b` at constant speed 1 unit per minute. Independently, there is a network base station at position `c` that covers everything within distance `r`. While the person moves, at every moment they are either inside coverage or outside it. The task is to compute how long, in total time, they spend outside the covered region during the whole trip.

Since speed is 1, time equals distance traveled. So the problem reduces to measuring how much of the segment from `a` to `b` lies outside the interval of coverage.

The key geometric observation is that the coverage area on the number line is itself a segment centered at `c`, extending `r` units in both directions. So the covered region is the interval `[c - r, c + r]`. The movement is also an interval, but it may go left or right depending on whether `a < b` or `a > b`.

The constraints allow up to 1000 test cases with coordinates up to 10^8 in magnitude. This immediately suggests an O(1) per test solution is required, since anything involving scanning or simulation over distance is impossible.

A naive interpretation would simulate movement minute by minute or unit by unit, but the range of coordinates makes this infeasible. Even a single test case could span up to 2⋅10^8 steps.

Edge cases that typically break incorrect approaches include reversing direction (when `a > b`), full coverage (entire segment inside `[c-r, c+r]`), and no overlap at all (segment completely disjoint from coverage). Another subtle case is when the segment only partially overlaps the coverage interval, requiring careful handling of intersection endpoints.

For example, if `a = 1, b = 10, c = 7, r = 1`, the coverage is `[6, 8]`. The traveled segment overlaps only in `[6, 8]`, so uncovered parts are `[1, 6]` and `[8, 10]`, giving total uncovered length 7. A mistake here is forgetting to clamp overlap properly or assuming direction does not matter.

## Approaches

The brute-force idea is to simulate Polycarp’s movement at unit resolution, checking for each integer point or each small step whether it lies inside `[c - r, c + r]`. This works conceptually because coverage is easy to test per position. However, the path length can be up to 2⋅10^8 per test, and with up to 1000 tests, this becomes completely infeasible.

The structure of the problem removes the need for simulation. Both the movement and the coverage are continuous intervals on a line. Instead of tracking positions over time, we only need to compute how much of the travel segment intersects the coverage segment. Once we recognize this, the problem becomes a pure interval intersection task.

We compute the overlap between the travel interval `[min(a,b), max(a,b)]` and the coverage interval `[c-r, c+r]`. The length of this overlap is the time spent in coverage. Subtracting it from total travel distance gives the time spent outside coverage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(distance) | O(1) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We reformulate everything in terms of intervals.

1. Convert the movement into a normalized segment `[l1, r1]` where `l1 = min(a, b)` and `r1 = max(a, b)`. This removes direction entirely so we only deal with lengths.
2. Convert the coverage into `[l2, r2]` where `l2 = c - r` and `r2 = c + r`. This represents all points where the signal is available.
3. Compute the intersection of these two segments by taking `left = max(l1, l2)` and `right = min(r1, r2)`.
4. If `right > left`, the intersection has positive length, so coverage time is `right - left`. If `right <= left`, there is no overlap and coverage time is zero.
5. Compute total travel time as `r1 - l1`, then subtract coverage time to get uncovered time.

The reason this works is that movement at speed 1 turns time into geometric length. The problem is reduced to measuring how much of one interval lies outside another, which is exactly total length minus intersection length.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, r = map(int, input().split())

    l1, r1 = min(a, b), max(a, b)
    l2, r2 = c - r, c + r

    left = max(l1, l2)
    right = min(r1, r2)

    overlap = max(0, right - left)
    total = r1 - l1

    print(total - overlap)
```

The code directly implements the interval view of the problem. The first step normalizes direction, which avoids any special casing for `a > b`. The second step builds the coverage interval explicitly.

The intersection logic relies on the standard formula for overlapping segments. The `max(0, right - left)` ensures that non-overlapping intervals contribute zero, avoiding negative lengths.

Finally, subtracting overlap from total gives exactly the time spent outside coverage.

## Worked Examples

### Example 1

Input:

`a = 1, b = 10, c = 7, r = 1`

| Step | l1,r1 | l2,r2 | left | right | overlap | total | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| init | [1,10] | [6,8] | - | - | - | - | - |
| compute | [1,10] | [6,8] | 6 | 8 | 2 | 9 | 7 |

The overlap `[6,8]` contributes 2 units of covered time. The full journey is 9 units long, so uncovered time is 7, matching the sample.

### Example 2

Input:

`a = 8, b = 2, c = 10, r = 4`

| Step | l1,r1 | l2,r2 | left | right | overlap | total | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| init | [2,8] | [6,14] | - | - | - | - | - |
| compute | [2,8] | [6,14] | 6 | 8 | 2 | 6 | 4 |

The segment partially overlaps the coverage from 6 to 8. Total travel is 6, so uncovered time is 4.

These examples confirm that direction reversal and partial overlap are handled uniformly by interval normalization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant-time arithmetic operations |
| Space | O(1) | No auxiliary structures beyond a few variables |

The constraints allow up to 1000 test cases, and each is processed in constant time, so the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        a, b, c, r = map(int, input().split())
        l1, r1 = min(a, b), max(a, b)
        l2, r2 = c - r, c + r
        overlap = max(0, min(r1, r2) - max(l1, l2))
        print((r1 - l1) - overlap)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("""9
1 10 7 1
3 3 3 0
8 2 10 4
8 2 10 100
-10 20 -17 2
-3 2 2 0
-3 1 2 0
2 3 2 3
-1 3 -2 2
""") == """7
0
4
0
30
5
4
0
3"""

# custom cases
assert run("""1
0 10 5 0
""") == "10", "no coverage anywhere"

assert run("""1
0 10 5 100
""") == "0", "full coverage"

assert run("""1
5 5 0 0
""") == "0", "zero-length movement"

assert run("""1
-5 5 0 2
""") == "6", "partial symmetric overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no coverage everywhere | 10 | disjoint intervals |
| full coverage | 0 | complete containment |
| zero movement | 0 | degenerate segment |
| symmetric overlap | 6 | correct partial intersection |

## Edge Cases

When `a == b`, the movement interval collapses to a single point. In this case `r1 - l1` is zero, so the answer is automatically zero regardless of coverage. For input `a = 5, b = 5, c = 0, r = 0`, the interval view gives `[5,5]` and `[0,0]`, producing zero overlap and zero total length, matching the correct result.

When there is no overlap at all, such as `a = 0, b = 10, c = 100, r = 1`, the intersection computation yields `min(r1,r2) < max(l1,l2)`, so overlap becomes zero. The answer reduces to the full segment length, which is 10.

When coverage fully contains the movement segment, such as `a = 2, b = 5, c = 3, r = 10`, the intersection equals the entire segment, so overlap equals total length and the result becomes zero.
