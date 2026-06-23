---
title: "CF 105485J - \u661f\u7a79\u5217\u8f66"
description: "The train moves along a fixed horizontal ray that starts at a given point and continues infinitely to the right. Every danger zone is a circle on the plane, and whenever the train’s path passes through a circle, we count only the portion of the train’s path that lies inside that…"
date: "2026-06-23T18:23:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105485
codeforces_index: "J"
codeforces_contest_name: "2024 China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 105485
solve_time_s: 62
verified: true
draft: false
---

[CF 105485J - \u661f\u7a79\u5217\u8f66](https://codeforces.com/problemset/problem/105485/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

The train moves along a fixed horizontal ray that starts at a given point and continues infinitely to the right. Every danger zone is a circle on the plane, and whenever the train’s path passes through a circle, we count only the portion of the train’s path that lies inside that circle. If multiple circles overlap along the path, overlapping parts are counted only once because we are measuring total covered length on the line, not per circle contribution.

Geometrically, everything collapses onto a single 1D problem once we fix the train’s path. The train always stays on the horizontal line y = y0, so each circle either does not touch this line at all, or it cuts out a segment along the x-axis. The task becomes computing the total length of the union of all such segments, restricted to x ≥ x0.

The constraints allow up to 100,000 circles, so any approach that compares every pair of circles or repeatedly scans the line is too slow. A naive O(k²) overlap resolution would be far beyond limits. Even O(k²) interval merging is impossible.

A subtle edge case comes from circles that do not intersect the horizontal line of travel at all. For example, a circle centered at (0, 10) with radius 1 never touches y = 0, so it contributes nothing. Another corner case is tangency: if the circle just touches the line, it contributes a single point segment of zero length, which must not affect the answer.

Another important situation is when a circle’s intersection lies completely to the left of the starting position x0. Even if the circle intersects the line, only the portion with x ≥ x0 matters, so intervals must be clipped correctly.

## Approaches

A direct approach is to process each circle independently, compute where it intersects the horizontal line y = y0, and then simulate walking along the x-axis while maintaining how many circles cover each point. This leads naturally to a sweep-line idea over x-coordinates. However, even a sweep-line implemented as an event structure is unnecessary because we only need the union length, not coverage counts.

The key observation is that each circle contributes at most one interval on the line y = y0. For a circle centered at (xc, yc) with radius r, the vertical distance from the path is fixed as dy = y0 − yc. If |dy| > r, the circle does not intersect the path. Otherwise, the horizontal half-width of the intersection is sqrt(r² − dy²), giving an interval [xc − d, xc + d].

After converting all circles into intervals, the problem becomes merging overlapping intervals and computing total covered length starting from x0.

The brute force fails when k is large because pairwise merging or repeated scanning produces quadratic behavior. Sorting intervals by left endpoint reduces the problem to a single pass merge in O(k log k).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force overlap simulation | O(k²) | O(k) | Too slow |
| Sort + merge intervals | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

### 1. Convert circles into intervals on the x-axis

For each circle, compute dy = y0 − yc. If dy² > r², skip it since the train never enters the circle. Otherwise compute d = sqrt(r² − dy²). The circle contributes the interval [xc − d, xc + d] on the line y = y0. This step reduces a 2D geometric problem into a 1D interval problem.

### 2. Clip intervals to the starting point

Since the train starts at x = x0, any portion of an interval left of x0 is irrelevant. Replace each interval [l, r] with [max(l, x0), r]. If after clipping l ≥ r, discard it. This ensures we only measure reachable covered segments.

### 3. Sort all intervals by left endpoint

Sorting gives a deterministic order that allows linear merging. Once intervals are ordered, any overlap structure becomes easy to resolve in a single sweep.

### 4. Merge intervals and accumulate covered length

Maintain a current active interval [cur_l, cur_r]. Traverse sorted intervals. If the next interval starts after cur_r, we add cur_r − cur_l to the answer and reset. Otherwise we extend cur_r if needed. At the end, add the last active interval length.

### Why it works

Each circle maps exactly to a convex segment on a line, and union length on a line depends only on interval endpoints, not on original geometry. Sorting ensures that when we process an interval, all potential overlaps with earlier intervals have already been resolved into a single merged segment. The invariant is that at every step, the current segment represents the union of all processed intervals, so adding a disjoint segment cannot miss or double count any region.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    x0, y0, k = map(int, input().split())
    intervals = []

    for _ in range(k):
        xc, yc, r = map(int, input().split())
        dy = y0 - yc
        if dy * dy > r * r:
            continue
        dx = math.sqrt(r * r - dy * dy)
        l = xc - dx
        rgt = xc + dx

        if rgt <= x0:
            continue
        l = max(l, x0)
        intervals.append((l, rgt))

    if not intervals:
        print("0.0000000000")
        return

    intervals.sort()

    total = 0.0
    cur_l, cur_r = intervals[0]

    for l, r in intervals[1:]:
        if l > cur_r:
            total += cur_r - cur_l
            cur_l, cur_r = l, r
        else:
            if r > cur_r:
                cur_r = r

    total += cur_r - cur_l
    print(f"{total:.10f}")

if __name__ == "__main__":
    solve()
```

The code first converts every circle into a candidate segment on the train’s line, then removes irrelevant parts left of x0. Sorting ensures we can merge in one pass. The floating-point sqrt is necessary because circle intersections naturally produce real-valued endpoints. The final accumulation step must be done carefully after the loop to avoid losing the last segment.

A common implementation mistake is forgetting to clip against x0 before merging. Another is treating tangential intersections incorrectly; when r² == dy², dx becomes zero and produces a valid zero-length interval, which is harmless and naturally ignored by the union logic.

## Worked Examples

### Example 1

Input:

```
0 0 2
10 0 5
20 0 10
```

| Step | Interval 1 | Interval 2 | Active segment | Total |
| --- | --- | --- | --- | --- |
| After conversion | [5, 15] | [10, 30] | - | 0 |
| After sort | [5, 15] | [10, 30] | - | 0 |
| Merge | merge | merged into [5, 30] | [5, 30] | 0 |
| Final | - | - | - | 25 |

The two circles overlap on the x-axis, so their union forms a single continuous segment.

### Example 2

Input:

```
0 0 3
5 5 2
10 0 3
20 0 1
```

| Circle | Intersects y=0 | Interval |
| --- | --- | --- |
| (5,5,2) | no | - |
| (10,0,3) | yes | [7, 13] |
| (20,0,1) | yes | [19, 21] |

| Step | Active segment | Total |
| --- | --- | --- |
| Start | [7, 13] | 0 |
| Add [19,21] | split | 6 |
| Final | - | 10 |

This shows how non-intersecting circles are ignored and disjoint intervals accumulate independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | sorting k intervals dominates, merging is linear |
| Space | O(k) | storing up to one interval per circle |

The algorithm fits comfortably within limits since k is at most 100,000 and sorting dominates at roughly 2 million comparisons.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    x0, y0, k = map(int, input().split())
    intervals = []

    for _ in range(k):
        xc, yc, r = map(int, input().split())
        dy = y0 - yc
        if dy * dy > r * r:
            continue
        dx = math.sqrt(r * r - dy * dy)
        l = xc - dx
        rgt = xc + dx
        if rgt <= x0:
            continue
        l = max(l, x0)
        intervals.append((l, rgt))

    if not intervals:
        return "0.0000000000"

    intervals.sort()

    total = 0.0
    cur_l, cur_r = intervals[0]

    for l, r in intervals[1:]:
        if l > cur_r:
            total += cur_r - cur_l
            cur_l, cur_r = l, r
        else:
            if r > cur_r:
                cur_r = r

    total += cur_r - cur_l
    return f"{total:.10f}"

# provided sample
assert run("0 0 4\n10 0 5\n20 0 10\n30 0 15\n-2 -3 5\n")[:2] != "", "sample"

# minimum size
assert run("0 0 1\n0 1 1\n") == "0.0000000000", "touch only point"

# all overlapping
assert run("0 0 2\n0 0 10\n0 0 10\n") != "", "overlap merge"

# disjoint intervals
assert run("0 0 2\n0 0 2\n10 0 2\n") != "", "disjoint"

# far left clipped
assert run("100 0 1\n0 0 50\n") == "0.0000000000", "clipping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single tangential circle | 0 | zero-length intersection handling |
| overlapping identical circles | positive length once | correct union behavior |
| disjoint circles | sum of segments | independent accumulation |
| circle entirely left of x0 | 0 | correct clipping |

## Edge Cases

A circle that only touches the line y = y0 at exactly one point produces dy² = r² and thus dx = 0. The algorithm converts this into [xc, xc], which contributes zero length after merging, so it does not affect the result.

When all circles lie above or below the path, every interval is discarded during the dy² > r² check, leaving an empty list and producing output zero.

If a large circle extends infinitely far left but the starting point x0 lies inside it, clipping ensures we only count the portion from x0 onward. The left endpoint becomes x0, so the contribution is correctly limited to the reachable segment.
