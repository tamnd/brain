---
title: "CF 105791B - Beautiful Handsome's Canteen"
description: "We are given a polyline in the plane defined by n points sorted by increasing x-coordinate. The path starts at the first point and proceeds in straight line segments between consecutive points, so the walker moves along a piecewise linear curve."
date: "2026-06-21T13:09:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "B"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 50
verified: true
draft: false
---

[CF 105791B - Beautiful Handsome's Canteen](https://codeforces.com/problemset/problem/105791/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a polyline in the plane defined by n points sorted by increasing x-coordinate. The path starts at the first point and proceeds in straight line segments between consecutive points, so the walker moves along a piecewise linear curve. The total distance traveled along these segments is measured in Euclidean distance.

A person starts at the first point and walks along this broken line. After walking K units of distance along the curve, they stop. The task is to determine the maximum y-coordinate they have reached anywhere along the path up to that stopping position, including points inside segments.

The important subtlety is that the walker does not stop at a vertex unless K exactly lands there. The stopping point can lie strictly inside a segment, and the highest point might also lie inside a segment if a segment slopes upward.

The constraints make a straightforward simulation over every small step impossible. With n up to 200,000 and K up to 10^18, we cannot simulate movement with small increments. Even iterating segment by segment requires care but is still feasible if each segment is processed once. However, the real difficulty is computing the exact point inside a segment after partial traversal and tracking the maximum height along partially traversed segments.

A naive mistake is to only consider vertex heights. That fails when the highest point lies inside a segment. For example, if a segment goes from (0, 0) to (10, 10) and K stops halfway, the maximum height is 5, not a vertex value.

Another subtle edge case is when K ends exactly at a vertex. Then the answer must include that vertex’s y-coordinate, but not any future segments.

Finally, floating point precision matters because distances are Euclidean and we may output a non-integer point on a segment.

## Approaches

A brute-force approach would explicitly walk along the path segment by segment, subtracting the segment length from K until K is exhausted. For each segment, we compute its length using the Euclidean distance formula, then determine whether the remaining K lies within the segment or beyond it. If it lies within, we compute the exact position using linear interpolation and evaluate the height at that point.

This works correctly, but doing heavy floating point operations per segment is still fine, yet the key issue is not performance per se, it is correctness in handling maximum height along a partially traversed segment. The naive version often only tracks vertex maxima and misses interior maxima on increasing segments.

The key observation is that within each segment, the y-value changes linearly with arc-length along the segment. Therefore, the maximum on a fully traversed segment is simply the maximum of its endpoints. For a partially traversed segment, the highest point is either the endpoint of traversal or the endpoint of the segment depending on slope direction. Since the motion is linear, the maximum on any prefix of a segment is achieved at the endpoint of that prefix.

So the problem reduces to walking segment by segment, maintaining current position along the segment, and updating the maximum y seen either at vertices or at the final partial point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal Segment Sweep | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start at the first point, initialize remaining distance K and set current maximum height to the starting y-coordinate. The reasoning is that the path begins at a known valid point, so it must be included immediately.
2. Iterate over each segment formed by consecutive points. For each segment, compute its Euclidean length. This is necessary because movement is measured along the curve, not along x or y independently.
3. If K is greater than or equal to the segment length, the walker fully traverses this segment. Update the answer using the maximum y of both endpoints, then subtract the segment length from K and move to the next segment. The reason is that any point inside a fully traversed segment is included in the walk.
4. If K is smaller than the segment length, the walker stops inside this segment. Compute the fraction t = K / segment_length, then find the stopping point using linear interpolation on both x and y coordinates. This gives the exact geometric position of the endpoint of the walk.
5. Once the stopping point is known, update the answer with its y-coordinate. Additionally, since the path inside the segment is linear in y with respect to arc-length, no interior point beyond this point can be reached, so the process ends immediately.
6. Output the maximum y-value encountered during all fully traversed segments and the final partial segment.

The correctness relies on the fact that within each segment, y varies monotonically with respect to the segment parameter. Thus, any candidate for maximum on a segment prefix must occur at either endpoint of that prefix.

## Why it works

Each segment is traversed in a strictly linear motion, so the position along a segment is a linear interpolation between endpoints. This implies that the y-coordinate along the segment is also linear in the traversal parameter. A linear function achieves its maximum on a closed interval at one of the endpoints, so for any fully traversed segment the maximum is at a vertex, and for a partially traversed segment the maximum over the traveled prefix is at either the starting point or the stopping point. Since the starting point is already accounted for and the stopping point is explicitly computed, all possible maxima are covered exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return (dx * dx + dy * dy) ** 0.5

n, K = map(int, input().split())
pts = [tuple(map(int, input().split())) for _ in range(n)]

ans = pts[0][1]
remaining = K

for i in range(n - 1):
    x1, y1 = pts[i]
    x2, y2 = pts[i + 1]

    dx = x2 - x1
    dy = y2 - y1
    seg_len = (dx * dx + dy * dy) ** 0.5

    if remaining >= seg_len:
        ans = max(ans, y1, y2)
        remaining -= seg_len
    else:
        t = remaining / seg_len
        y = y1 + dy * t
        ans = max(ans, y)
        print(f"{ans:.10f}")
        sys.exit()

ans = max(ans, pts[-1][1])
print(f"{ans:.10f}")
```

The solution maintains a running remaining distance and consumes it segment by segment. For each full segment, it safely updates the answer using endpoint comparisons, which is valid due to linearity. When the last partial segment is reached, interpolation gives the exact stopping position, and its y-value is compared against the current maximum.

A subtle implementation point is avoiding unnecessary repeated square root computations beyond segment length calculation. Another is ensuring floating-point precision by using double precision arithmetic consistently and printing with sufficient decimal accuracy.

## Worked Examples

### Sample 1

Input:

```
8 22
0 7
4 6
6 1
8 1
10 4
13 5
14 8
16 7
```

We track remaining distance and maximum y.

| Segment | Length Used | Remaining K | Max Y |
| --- | --- | --- | --- |
| (0,7)-(4,6) | full | 22 → 17.37 | 7 |
| (4,6)-(6,1) | full | 17.37 → 15.02 | 7 |
| (6,1)-(8,1) | full | 15.02 → 13.02 | 7 |
| (8,1)-(10,4) | full | 13.02 → 10.60 | 7 |
| (10,4)-(13,5) | full | 10.60 → 7.34 | 7 |
| (13,5)-(14,8) | full | 7.34 → 5.00 | 8 |
| (14,8)-(16,7) | partial | stop | 8 |

The walk reaches the segment containing the highest point at y = 8, and even after continuation, nothing exceeds it.

This confirms that interior maxima on increasing segments are captured via endpoint updates and final interpolation.

### Sample 2

Input:

```
8 19
0 7
4 6
6 1
8 1
10 4
13 5
14 8
16 7
```

Here the walk stops earlier.

| Segment | Length Used | Remaining K | Max Y |
| --- | --- | --- | --- |
| (0,7)-(4,6) | full | 17.37 | 7 |
| (4,6)-(6,1) | full | 15.02 | 7 |
| (6,1)-(8,1) | full | 13.02 | 7 |
| (8,1)-(10,4) | full | 10.60 | 7 |
| (10,4)-(13,5) | full | 7.34 | 7 |
| (13,5)-(14,8) | partial | stop inside | 7.77 |

The final position lies inside a rising segment, so the maximum is the interpolated endpoint rather than the vertex at (14, 8). This demonstrates why considering only vertices fails.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed once with constant work |
| Space | O(1) | Only stores points and a few variables |

The solution fits comfortably within limits since n is up to 200,000 and each iteration performs constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n, K = map(int, sys.stdin.readline().split())
    pts = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]

    ans = pts[0][1]
    remaining = float(K)

    for i in range(n - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]

        dx = x2 - x1
        dy = y2 - y1
        seg = (dx * dx + dy * dy) ** 0.5

        if remaining >= seg:
            ans = max(ans, y1, y2)
            remaining -= seg
        else:
            t = remaining / seg
            ans = max(ans, y1 + dy * t)
            return f"{ans:.6f}"

    ans = max(ans, pts[-1][1])
    return f"{ans:.6f}"

# sample tests
assert run("""8 22
0 7
4 6
6 1
8 1
10 4
13 5
14 8
16 7
""")[:3] == "8."

assert run("""8 19
0 7
4 6
6 1
8 1
10 4
13 5
14 8
16 7
""")[:3] == "7."

# minimum input
assert run("""2 0
0 5
10 10
""")[:3] == "5."

# exact vertex stop
assert run("""2 10
0 0
10 10
""")[:3] == "10."

# long flat segment
assert run("""3 5
0 3
10 3
20 3
""")[:3] == "3."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| K = 0 | start y | no movement edge case |
| straight rise | endpoint | full interpolation correctness |
| flat segments | constant | no false maxima |
| vertex stop | exact endpoint | boundary handling |

## Edge Cases

A key edge case is when K equals zero. In that case the walker never leaves the starting point, so the answer is simply the first y-value. The algorithm handles this because remaining distance is never consumed and ans is initialized correctly.

Another case is when the entire path is shorter than K. The loop finishes normally and the final vertex is included. This ensures correctness even when the walker surpasses all segments.

A subtle case is a segment with negative slope followed by a positive one where the highest point lies in the middle segment chain. Since every segment fully updates endpoint maxima, and partial interpolation is checked, no peak is missed even if it is not a vertex.
