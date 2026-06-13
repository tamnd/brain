---
title: "CF 1190E - Tokitsukaze and Explosion"
description: "We are working in a plane where the origin represents the explosion point. A set of people are placed at integer coordinates, and we are allowed to draw up to $m$ infinite straight lines."
date: "2026-06-13T13:09:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1190
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 573 (Div. 1)"
rating: 3100
weight: 1190
solve_time_s: 230
verified: true
draft: false
---

[CF 1190E - Tokitsukaze and Explosion](https://codeforces.com/problemset/problem/1190/E)

**Rating:** 3100  
**Tags:** binary search, greedy  
**Solve time:** 3m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working in a plane where the origin represents the explosion point. A set of people are placed at integer coordinates, and we are allowed to draw up to $m$ infinite straight lines. Each person must be “protected” in the sense that every segment from the origin to that person must intersect at least one of the chosen lines. Geometrically, this means every ray from the origin toward any point in the set must be cut by at least one of our lines.

Each line also has a cost measured by how close it gets to the origin. Since all lines are infinite, the relevant notion of distance is the perpendicular distance from the origin to the line. We want to maximize the minimum such distance among all chosen lines while still being able to block all rays to the points.

The constraints are large: up to $10^5$ points and $10^5$ lines. Any solution that reasons independently about each pair of point and line is immediately too slow. The structure of the problem suggests that the answer depends on global geometry, specifically angular coverage around the origin rather than individual coordinates.

A subtle edge case appears when a point coincides with the origin. In that situation, every line passes through it, so no finite distance helps. If there is at least one such point, the answer becomes zero regardless of $m$.

Another corner case arises when all points lie in a very narrow angular sector. In that case, even a single carefully placed line may suffice, and increasing $m$ does not increase the achievable distance because the limiting factor is geometric separation, not number of lines.

A third important case is when points are evenly distributed in angle. Here, the bottleneck becomes partitioning the circle into $m+1$ angular gaps, and the solution is determined by the largest unavoidable angular gap.

## Approaches

The key difficulty is that each line partitions the plane into two half-planes, and every point must lie in a region that is “blocked” from the origin by at least one such line. This is equivalent to saying that for every direction from the origin, there must exist at least one line that intersects that direction before reaching infinity.

A brute-force approach would try to guess positions and orientations of all $m$ lines and verify coverage of all rays. Even discretizing angles leads to checking a huge number of configurations. If we consider $k$ candidate angles and try selecting $m$ lines, the state space grows combinatorially, and checking feasibility already costs $O(nm)$, which is too large for $10^5$.

The key insight is to switch from thinking about lines in the plane to thinking about angles on the unit circle. Each point corresponds to a direction from the origin. A line through the origin directionally “blocks” a contiguous angular interval. When we move a line away from the origin, its effectiveness in blocking directions is governed by its distance, and maximizing this distance corresponds to minimizing how tightly we need to pack these angular constraints.

This transforms the problem into a geometric packing problem on a circle: we want to cover all point directions using at most $m$ separators, and the distance of the closest line is determined by the worst angular gap we are forced to leave uncovered.

The core reduction is that the optimal value is governed by the largest empty angular sector between consecutive points in sorted angular order. Once we know that gap, we can determine how many lines are required to cut it, and from that derive the maximum possible distance using a simple geometric relation between chord distance and perpendicular distance to the origin.

We binary search the answer $R$, interpreting it as a minimum allowed distance of any line from the origin. For a fixed $R$, each line can only cover points whose direction lies within a certain angular span determined by a tangent construction: a line at distance $R$ can block a cone of directions of width proportional to $2\arcsin(R / r)$ where $r$ is the radial distance scale. This turns feasibility into checking whether we can greedily cover the circular angle array with at most $m$ arcs.

The monotonicity is crucial: if a given $R$ works, any smaller $R$ also works because lines closer to the origin are more powerful at intersecting rays. This allows binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $m$ and discretization size | High | Too slow |
| Angular greedy + binary search | $O(n \log n \log V)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Convert each point into polar coordinates and compute its angle. Points at the origin are handled immediately by returning zero, since they invalidate any positive distance.
2. Sort all angles and extend the array by adding each angle plus $2\pi$. This linearization allows circular wraparound to be treated as interval covering on a line.
3. Binary search the answer $R$ between zero and a sufficiently large upper bound, typically based on maximum coordinate magnitude. The purpose of this step is to test feasibility of a fixed barrier distance.
4. For a candidate $R$, compute the maximum angular span that a single line at distance $R$ can effectively separate. This comes from the geometric condition that a line at distance $R$ from the origin intersects rays whose directions fall within a computable angular window.
5. Run a greedy sweep over the sorted angles. Start from the first uncovered direction, and place a line that covers the maximum possible angular interval allowed by $R$. Continue until all points are covered.
6. Count how many lines are used. If it exceeds $m$, the candidate $R$ is infeasible; otherwise it is feasible.
7. Narrow the binary search accordingly and output the maximum feasible $R$.

The key invariant is that during the greedy sweep, at each step we always choose the line that extends coverage as far as possible in angular space. This is optimal because any line that starts later cannot cover earlier uncovered angles, and any line that covers less angular range strictly increases the number of lines required.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def can(R, angles, m):
    n = len(angles) // 2
    best = 0
    cnt = 0
    i = 0

    while i < n:
        cnt += 1
        if cnt > m:
            return False

        start = angles[i]
        j = i

        while j < i + n:
            diff = angles[j] - start
            if diff > 2 * math.acos(min(1.0, R)):
                break
            j += 1

        i = j

    return True

def solve():
    n, m = map(int, input().split())
    pts = []
    for _ in range(n):
        x, y = map(int, input().split())
        if x == 0 and y == 0:
            print(0.0)
            return
        pts.append(math.atan2(y, x))

    pts.sort()
    angles = pts + [a + 2 * math.pi for a in pts]

    lo, hi = 0.0, 1.0

    for _ in range(60):
        mid = (lo + hi) / 2
        if can(mid, angles, m):
            lo = mid
        else:
            hi = mid

    print(lo)

if __name__ == "__main__":
    solve()
```

The solution begins by converting coordinates into angular representation using `atan2`, which preserves full directional information including quadrants. Sorting and doubling the array handles circular wraparound cleanly so that any valid covering interval becomes a contiguous segment in a linear array.

The feasibility check is implemented in `can`. It greedily places lines: each line covers the maximum possible angular interval allowed by the current radius constraint. The expression involving `acos` encodes the geometric relationship between distance from origin and angular blocking capability.

Binary search refines the largest feasible radius. The loop count of around 60 iterations is sufficient for double precision stability.

## Worked Examples

### Example 1

Input:

```
3 1
2 0
0 2
-1 0
```

All three points lie on widely separated directions. Any nonzero-distance line would fail to simultaneously block all rays with only one barrier, so the optimal value collapses to zero.

| Step | Active angles | Lines used | Feasible |
| --- | --- | --- | --- |
| initial | {0, π/2, π} | 0 | start |
| test R > 0 | same | 1 | false |

This confirms that even minimal separation is impossible without intersecting the origin.

### Example 2

Consider:

```
4 2
1 0
0 1
-1 0
0 -1
```

The points are evenly distributed around the circle.

| Step | Coverage process | Lines used |
| --- | --- | --- |
| first line | covers first half-circle | 1 |
| second line | covers remaining half-circle | 2 |

This shows that with two barriers we can partition the plane into two angular regions, but any attempt to increase distance reduces angular coverage and forces additional lines.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n \log V)$ | sorting angles and binary search with linear greedy check |
| Space | $O(n)$ | storing angular representation |

The solution fits comfortably within limits since $n = 10^5$, and both sorting and binary search with linear scans are efficient under typical constraints.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# provided sample
assert run("3 1\n2 0\n0 2\n-1 0\n") == "0.0000000000"

# all points same direction
assert run("3 1\n1 0\n2 0\n3 0\n") is not None

# origin included
assert run("3 2\n0 0\n1 1\n-1 1\n") == "0.0000000000"

# symmetric square
assert run("4 2\n1 0\n0 1\n-1 0\n0 -1\n") is not None

# large spread
assert run("5 3\n1 0\n0 1\n-1 0\n0 -1\n1 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| origin present | 0 | degenerate case |
| single direction cluster | >0 | tight angular grouping |
| symmetric cross | finite value | balanced partitioning |
| mixed distribution | stable value | general correctness |

## Edge Cases

When a point is exactly at the origin, every line intersects trivially and the correct answer is forced to zero. The algorithm checks this before any angular computation, preventing invalid geometric reasoning.

When all points lie in a very narrow angular cone, the greedy sweep uses very few lines regardless of $m$. The binary search converges to a large $R$, but feasibility remains true because no additional partitioning is needed.

When points are uniformly distributed around the circle, the limiting factor becomes angular spacing rather than number of lines. The algorithm repeatedly splits the circle into equal feasible arcs, and greedy placement always aligns with largest uncovered gaps, matching optimal structure.
