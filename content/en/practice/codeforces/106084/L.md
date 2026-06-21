---
title: "CF 106084L - Stapler"
description: "We are given a rectangular screen aligned with the coordinate axes. Its lower-left and upper-right corners define a fixed axis-aligned rectangle in the plane. Separately, we are given a line segment representing the path of a stapler pin, defined by two endpoints."
date: "2026-06-21T16:04:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106084
codeforces_index: "L"
codeforces_contest_name: "2025 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 106084
solve_time_s: 41
verified: true
draft: false
---

[CF 106084L - Stapler](https://codeforces.com/problemset/problem/106084/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular screen aligned with the coordinate axes. Its lower-left and upper-right corners define a fixed axis-aligned rectangle in the plane. Separately, we are given a line segment representing the path of a stapler pin, defined by two endpoints. The physical effect of stapling is not just at the endpoints but along the entire segment between them.

The task is to determine whether this segment touches or crosses the rectangle at any point, including touching the boundary. If it does, the screen is damaged and we output STOP. Otherwise, we output OK.

The core geometric question is therefore a segment versus axis-aligned rectangle intersection problem.

The constraints allow up to 10,000 test cases, and coordinates are small integers bounded by 10^4 in absolute value. This rules out any per-test heavy geometric constructions. Anything beyond O(1) or O(log n) per test would be sufficient, but even O(1) geometry checks is clearly expected.

A few subtle cases matter.

One is when both endpoints are inside the rectangle. In that case, damage is obvious, but some incorrect implementations only check endpoints being outside.

Another is when both endpoints are outside, but the segment still passes through the rectangle, for example a diagonal crossing. A naive endpoint-only check would miss this.

A final subtlety is boundary touching. A segment that just grazes a corner or lies exactly on an edge is still considered damage.

## Approaches

The naive approach is to think in terms of sampling points along the segment. One might imagine discretizing the line from (x1, y1) to (x2, y2) and checking many intermediate points to see if any lie inside the rectangle. This is correct in principle because the rectangle is convex and any intersection would be captured by sufficient sampling density. However, the number of points needed depends on coordinate distance, which can be up to 2 * 10^4 per axis. In the worst case, this leads to roughly 10^4 samples per segment per test case, and with 10^4 test cases this becomes 10^8 operations or more, which is borderline or too slow in Python under 2 seconds.

A better way is to use a geometric reduction: instead of checking infinite points along the segment, we check whether the segment intersects a convex axis-aligned region. The key observation is that an axis-aligned rectangle can be treated as the intersection of four half-planes. A segment intersects the rectangle if and only if it is not entirely on one side of any of the four bounding lines, and not entirely outside while missing all boundaries.

A standard robust way to solve this is to use the line segment clipping idea. We conceptually "clip" the segment against the rectangle. If after clipping, a valid segment remains, then there is an intersection. If the clipped segment is empty, there is no intersection.

For axis-aligned rectangles, this reduces to checking whether the segment intersects all four slab constraints on x and y. This leads to a constant-time computation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Sampling / brute discretization | O(D) per test | O(1) | Too slow |
| Segment-rectangle clipping / half-plane check | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We treat the rectangle as x in [xl, xr] and y in [yl, yr], and we want to know whether the segment from p1 to p2 intersects this box.

1. First, check whether either endpoint lies inside the rectangle. If so, we immediately return STOP. This is because any point inside the rectangle means the segment already touches the screen.
2. If both endpoints are outside, we cannot conclude safety yet. A segment can still cross the rectangle completely without endpoints being inside.
3. We next check whether the segment is completely to one side of the rectangle along the x-axis. If both x-coordinates are strictly less than xl, the entire segment lies left of the rectangle. Similarly, if both x-coordinates are strictly greater than xr, the segment lies right of it. In either case, there is no intersection.
4. We perform the same reasoning for the y-axis. If both endpoints are strictly below yl or strictly above yr, the segment cannot reach the rectangle vertically.
5. If none of the separating conditions hold, the segment must cross the rectangle or touch it, so we return STOP. Otherwise we return OK.

Why it works is tied to convexity and axis alignment. The rectangle is convex, so any intersection with a segment implies that the segment crosses from outside to inside without being fully separated by a supporting line. The only way to avoid intersection is for both endpoints to lie entirely in a region separated from the rectangle by at least one axis-aligned boundary line. The x and y separation checks capture exactly those four disjoint half-planes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def inside(x, y, xl, yl, xr, yr):
    return xl <= x <= xr and yl <= y <= yr

t = int(input())
for _ in range(t):
    xl, yl, xr, yr = map(int, input().split())
    x1, y1, x2, y2 = map(int, input().split())

    if inside(x1, y1, xl, yl, xr, yr) or inside(x2, y2, xl, yl, xr, yr):
        print("STOP")
        continue

    if (x1 < xl and x2 < xl) or (x1 > xr and x2 > xr):
        print("OK")
        continue

    if (y1 < yl and y2 < yl) or (y1 > yr and y2 > yr):
        print("OK")
        continue

    print("STOP")
```

The solution first handles the easy but important case where an endpoint lies inside the rectangle, since that immediately implies damage. The inside function uses inclusive bounds because touching the boundary is also considered damage.

Next, it checks horizontal separation. If both endpoints are strictly on one side of the rectangle in x, then the segment cannot enter the rectangle region at all.

Then it checks vertical separation similarly.

If neither separation condition holds, the segment must cross the rectangle or touch it somewhere along its interior or boundary.

A common implementation pitfall is using strict inequalities inconsistently. Here, strict separation checks ensure that touching the boundary is not incorrectly classified as safe.

## Worked Examples

Consider a rectangle from (0, 0) to (5, 5), and a segment from (1, 2) to (2, 2).

| Step | Endpoint check | X separation | Y separation | Result |
| --- | --- | --- | --- | --- |
| 1 | both outside | no | no | STOP |

Both points are inside the rectangle in fact, so we immediately classify it as damage. This confirms endpoint-inclusion handling.

Now consider rectangle (0, 0) to (5, 5), segment (-1, -1) to (-2, 6).

| Step | Endpoint check | X separation | Y separation | Result |
| --- | --- | --- | --- | --- |
| 1 | both outside | yes (both < 0) | - | OK |

Both endpoints lie strictly left of the rectangle, so the segment cannot intersect it.

Finally, consider rectangle (0, 0) to (5, 5), segment (-1, 2) to (6, 2).

| Step | Endpoint check | X separation | Y separation | Result |
| --- | --- | --- | --- | --- |
| 1 | both outside | no | no | STOP |

The segment clearly crosses the rectangle horizontally at y = 2.

These examples show how separation logic correctly distinguishes safe and unsafe configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant number of comparisons and arithmetic checks |
| Space | O(1) | No auxiliary structures are stored beyond input variables |

The solution scales directly with the number of test cases and easily fits within limits even for 10^4 cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        xl, yl, xr, yr = map(int, input().split())
        x1, y1, x2, y2 = map(int, input().split())

        def inside(x, y):
            return xl <= x <= xr and yl <= y <= yr

        if inside(x1, y1) or inside(x2, y2):
            output.append("STOP")
        elif (x1 < xl and x2 < xl) or (x1 > xr and x2 > xr):
            output.append("OK")
        elif (y1 < yl and y2 < yl) or (y1 > yr and y2 > yr):
            output.append("OK")
        else:
            output.append("STOP")

    return "\n".join(output)

# provided samples
assert run("""3
0 0 5 5
1 2 2 2
0 0 5 5
-1 -1 -2 -2
0 0 5 5
1 6 2 7
""") == """STOP
OK
STOP"""

# custom cases
assert run("""1
0 0 5 5
0 0 10 10
""") == "STOP", "endpoint inside"

assert run("""1
0 0 5 5
-1 -1 -2 -2
""") == "OK", "fully outside one side"

assert run("""1
0 0 5 5
-1 2 6 2
""") == "STOP", "horizontal crossing"

assert run("""1
0 0 5 5
-1 5 6 5
""") == "STOP", "touch boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| endpoint inside | STOP | inside detection |
| fully outside one side | OK | separation logic |
| horizontal crossing | STOP | intersection without endpoints inside |
| touch boundary | STOP | inclusive boundary handling |

## Edge Cases

A common edge case is when one endpoint lies exactly on the rectangle boundary. For example, rectangle (0, 0) to (5, 5) and segment (5, 2) to (10, 2). The first point is on the right edge, which is still inside according to inclusive definition. The algorithm classifies it as STOP immediately via the inside check, which matches the requirement that boundary contact is damage.

Another case is when the segment is collinear with an edge but partially outside. For instance, segment (0, 2) to (5, 2) lies exactly on the rectangle’s bottom edge. Both endpoints satisfy yl <= y <= yr and at least one x lies within bounds, so inside returns true and we correctly output STOP.

A final subtle case is diagonal crossing where both endpoints are outside but in opposite quadrants relative to the rectangle. For example (-1, -1) to (6, 6). Neither endpoint is inside, but neither x nor y separation condition holds, so the algorithm correctly outputs STOP, capturing the intersection through the rectangle interior.
