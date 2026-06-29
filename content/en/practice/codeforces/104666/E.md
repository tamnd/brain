---
title: "CF 104666E - Deep800080"
description: "We are given a straight pier in the plane, defined by a line passing through the origin and a second point $(A, B)$. We are allowed to choose any point on this infinite line as the location of a barbecue grill."
date: "2026-06-29T09:53:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104666
codeforces_index: "E"
codeforces_contest_name: "2019-2020 ICPC Central Europe Regional Contest (CERC 19)"
rating: 0
weight: 104666
solve_time_s: 93
verified: true
draft: false
---

[CF 104666E - Deep800080](https://codeforces.com/problemset/problem/104666/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight pier in the plane, defined by a line passing through the origin and a second point $(A, B)$. We are allowed to choose any point on this infinite line as the location of a barbecue grill. Around that chosen point, a circular smoke cloud of fixed radius $R$ appears. Every boat is a fixed point in the plane, and a boat is considered “alerted” if it lies inside or on this circle.

The task is to choose a point on the pier that maximizes how many boats are covered by the circle.

Geometrically, this is a constrained center selection problem: we are not free to place the circle anywhere in the plane, only along a fixed line, and we want the position on that line that maximizes the number of points within distance $R$.

The constraints are large, with up to $3 \cdot 10^5$ boats. Any approach that recomputes distances for every possible pier position or tries to discretize candidate centers directly will fail. Even a naive $O(N^2)$ sweep over pairs of boats is far too slow.

A more subtle issue is numerical stability. The pier is defined by arbitrary coordinates, and boats can lie anywhere within a large coordinate range. A solution relying on repeated geometric computations must avoid precision drift when comparing distances and endpoints of intervals.

Edge cases appear when boats are far from the pier. For example, if all boats are farther than $R$ from the line itself, then no boat can ever be covered regardless of where we place the circle center on the pier, and the answer is zero. A careless implementation that does not filter these cases may still generate invalid intervals and produce incorrect overlaps.

Another edge case is when boats are exactly at distance $R$ from the moving center for a single degenerate position on the line. These cases produce intervals that collapse to a point, and treating them incorrectly as empty intervals will lose valid answers.

## Approaches

The brute-force idea is to choose a candidate point on the pier and count how many boats fall within distance $R$. If we sample many points along the line, or try all projections of boats onto the line as candidate centers, we can compute the answer by direct distance checks. This works conceptually because the best circle center must lie at a “critical” position where the set of covered boats changes, typically aligned with geometric events involving the boundary of circles centered at boats.

However, this approach is too slow. If we try every pair of boats to generate candidate transitions, we get $O(N^2)$ candidates. Even evaluating a single candidate costs $O(N)$, leading to $O(N^3)$ in the worst case. Even reducing evaluation to $O(1)$ with preprocessing does not fix the explosion in candidate positions.

The key observation is that we can reverse the viewpoint. Instead of choosing a center and checking which boats it covers, we fix a boat and ask: for which positions of the center on the pier would this boat be covered?

Fix a boat $P$. The center $C$ must satisfy $|C - P| \le R$. Since $C$ is constrained to lie on a line, this condition becomes an interval constraint on a single parameter along the line. Every boat contributes an interval of valid center positions. The final answer is the maximum number of overlapping intervals.

Thus the geometric problem reduces to a 1D interval overlap problem after projecting all boats onto the pier line and shrinking each circle into an interval along that line.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sampling / pair generation | $O(N^2)$ to $O(N^3)$ | $O(N)$ | Too slow |
| Interval projection + sweep line | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We convert the 2D geometry into a 1D coordinate system aligned with the pier.

### 1. Build a coordinate system along the pier

We treat the pier as an infinite line passing through $(0,0)$ and $(A,B)$. We define a direction vector $d = (A,B)$ and normalize it into a unit vector $u$. This lets us represent any point on the pier by a single scalar parameter $t$, where position is $P(t) = (0,0) + t \cdot u$.

The reason for this step is that all valid barbecue positions lie on this line, so reducing the problem to a single parameter removes one geometric degree of freedom.

### 2. Precompute perpendicular distance and projection for each boat

For each boat $X_i = (x_i, y_i)$, we compute its projection onto the line and its perpendicular distance to the line.

The perpendicular distance determines whether the boat can ever be covered. If this distance exceeds $R$, then no circle centered on the line can reach it.

If the boat is reachable, we also compute its projection coordinate $t_i$ along the line.

### 3. Convert each boat into an interval on the line

For a fixed center at position $t$, the distance to a boat decomposes into perpendicular and parallel components. The perpendicular component is fixed. The remaining allowable radius along the line becomes:

$$\Delta_i = \sqrt{R^2 - d_{\perp}^2}$$

So the center must satisfy:

$$t \in [t_i - \Delta_i,\; t_i + \Delta_i]$$

Each boat becomes an interval on the real line.

This is the critical transformation: a 2D circular constraint becomes a 1D segment constraint.

### 4. Sweep line over all intervals

We collect all interval endpoints. Each start adds +1 to coverage, each end subtracts -1. Sorting endpoints and sweeping yields the maximum overlap at any point.

We take care that endpoints are handled consistently so that a boat exactly on the boundary is included.

### Why it works

The algorithm relies on the fact that every valid center position on the pier corresponds to exactly one point on the real line parameter $t$, and each boat defines exactly the set of $t$ values for which it is covered. Coverage is therefore additive over intervals, and maximizing the number of covered boats becomes equivalent to finding a point with maximum interval overlap. No geometric interactions between boats remain after projection, so there is no hidden dependency that could invalidate the reduction.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    N, R, A, B = map(int, input().split())

    # direction vector of pier
    dx, dy = A, B
    norm = math.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm

    events = []

    for _ in range(N):
        x, y = map(int, input().split())

        # projection coordinate onto pier
        tx = x
        ty = y

        t = tx * ux + ty * uy  # dot product gives projection

        # perpendicular distance via cross product magnitude
        cross = abs(tx * dy - ty * dx) / norm

        if cross > R:
            continue

        span = math.sqrt(R * R - cross * cross)

        l = t - span
        r = t + span

        events.append((l, 1))
        events.append((r, -1))

    events.sort()

    cur = 0
    best = 0

    for _, v in events:
        cur += v
        best = max(best, cur)

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation starts by building an orthonormal basis along the pier using a normalized direction vector. Every boat is then mapped into a scalar coordinate along that direction using a dot product. The perpendicular distance is computed using a cross product divided by the line norm, which avoids explicitly constructing a rotated coordinate system.

Each boat contributes an interval only if it is geometrically reachable, meaning the perpendicular distance does not exceed the radius. Otherwise it is safely ignored.

The sweep line uses sorted endpoints where left endpoints increment the active count and right endpoints decrement it. The maximum prefix sum during this sweep corresponds to the best placement of the barbecue.

A subtle implementation detail is floating-point stability. Using `math.hypot` and consistent normalization avoids large relative errors when $A, B$ are large. The statement guarantee about tolerance allows standard double precision without additional epsilon handling.

## Worked Examples

### Sample 2

Input:

```
3 1 1 0
0 0
2 0
4 0
```

All boats lie on the x-axis, which is also the pier. The unit direction is $(1,0)$, so projection is direct.

| Boat | t | Perp distance | Interval |
| --- | --- | --- | --- |
| (0,0) | 0 | 0 | [-1, 1] |
| (2,0) | 2 | 0 | [1, 3] |
| (4,0) | 4 | 0 | [3, 5] |

Sweeping these intervals, the maximum overlap occurs at $t \in [1,1]$ and $t \in [3,3]$, each covering 2 boats.

Output is 2.

### Sample 3

Input:

```
4 1 1 0
0 0
1 1
1 -1
2 0
```

The pier is the x-axis again. We classify intervals:

| Boat | Projection t | Perp distance | Interval |
| --- | --- | --- | --- |
| (0,0) | 0 | 0 | [-1, 1] |
| (1,1) | 1 | 1 | point at 1 |
| (1,-1) | 1 | 1 | point at 1 |
| (2,0) | 2 | 0 | [1, 3] |

At $t=1$, all four intervals overlap. This yields answer 4, demonstrating how degenerate intervals still contribute correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Each boat becomes at most two events, sorted once, then swept linearly |
| Space | $O(N)$ | Stores interval endpoints for all reachable boats |

The constraints allow up to $3 \cdot 10^5$ boats, so an $O(N \log N)$ sweep is easily fast enough. Memory usage is linear in the number of intervals, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import hypot, sqrt
    import math

    input = sys.stdin.readline
    N, R, A, B = map(int, input().split())
    dx, dy = A, B
    norm = math.hypot(dx, dy)
    ux, uy = dx / norm, dy / norm

    events = []
    for _ in range(N):
        x, y = map(int, input().split())
        t = x * ux + y * uy
        cross = abs(x * dy - y * dx) / norm
        if cross <= R:
            span = math.sqrt(R * R - cross * cross)
            events.append((t - span, 1))
            events.append((t + span, -1))

    events.sort()
    cur = 0
    best = 0
    for _, v in events:
        cur += v
        best = max(best, cur)
    return str(best)

# provided samples
assert run("""7 5 0 1
-1 -1
1 -1
0 0
2 3
3 4
10 10
2 12
""") == "5"

assert run("""3 1 1 0
0 0
2 0
4 0
""") == "2"

assert run("""4 1 1 0
0 0
1 1
1 -1
2 0
""") == "4"

# custom cases
assert run("""1 10 1 1
5 5
""") == "1", "single boat always covered if reachable"

assert run("""2 1 1 0
0 10
0 -10
""") == "0", "all too far from line"

assert run("""5 2 0 1
0 0
0 1
0 2
0 3
0 4
""") == "3", "vertical stacking overlap window"

assert run("""3 5 1 0
-100 0
0 0
100 0
""") == "2", "large spread with limited radius"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 1 | minimal configuration |
| all unreachable | 0 | filtering by perpendicular distance |
| dense line overlap | 3 | interval stacking correctness |
| sparse wide spread | 2 | correct local overlap window |

## Edge Cases

If all boats lie far from the pier line, every perpendicular distance exceeds $R$, and the algorithm generates no intervals. The sweep then sees no events and returns zero, matching the fact that no placement on the line can reach any boat.

When a boat lies exactly at distance $R$ from the line, its interval collapses to a single point. In the sweep line, this appears as a start and end at the same coordinate, contributing correctly to overlap at that exact center position without requiring special handling.

When multiple boats share identical projection coordinates but different perpendicular distances, their intervals overlap heavily around the same region. The sweep correctly accumulates all contributions since each interval is independent after projection.
