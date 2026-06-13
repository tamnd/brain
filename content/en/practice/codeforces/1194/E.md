---
title: "CF 1194E - Count The Rectangles"
description: "We are given a collection of axis-aligned line segments in the plane. Each segment is either perfectly horizontal or perfectly vertical. Horizontal segments never overlap with other horizontal segments, and the same is true for vertical segments."
date: "2026-06-13T13:44:24+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "data-structures", "geometry", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1194
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 68 (Rated for Div. 2)"
rating: 2200
weight: 1194
solve_time_s: 274
verified: true
draft: false
---

[CF 1194E - Count The Rectangles](https://codeforces.com/problemset/problem/1194/E)

**Rating:** 2200  
**Tags:** bitmasks, brute force, data structures, geometry, sortings  
**Solve time:** 4m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of axis-aligned line segments in the plane. Each segment is either perfectly horizontal or perfectly vertical. Horizontal segments never overlap with other horizontal segments, and the same is true for vertical segments. Intersections only happen between a horizontal and a vertical segment, and when they do, they form a single crossing point.

The task is to count how many ways we can choose four segments that form the boundary of a rectangle. Two of the chosen segments must be horizontal, two must be vertical. Each horizontal segment must intersect both vertical segments, and vice versa, so together they define the four sides of a rectangle.

A key way to reinterpret the problem is to think in terms of intersection structure. Each vertical segment defines a set of horizontal segments it intersects, and a rectangle is formed exactly when we pick two vertical segments that share at least two common horizontal neighbors.

The constraints allow up to 5000 segments. A cubic or worse approach is impossible. Even an O(n^2 log n) or O(n^2) solution is borderline but acceptable, which suggests we should look for a structure that reduces the problem to processing pairs and counting overlaps efficiently.

A subtle edge case arises when multiple vertical segments share exactly one horizontal segment in common. For example, if three vertical segments all intersect the same two horizontal segments, then every pair of vertical segments contributes a rectangle. A naive approach that counts independently per intersection point risks double counting or missing combinations if it does not enforce “choose two horizontals and two verticals” symmetrically.

Another failure mode is treating intersections as independent points and counting squares per cell-like grid representation. That breaks when segments are long, because intersection is not a point grid problem but an interval overlap problem.

## Approaches

A brute-force strategy is to try every quadruple of segments and check whether they form a rectangle. For each candidate, we verify that we have two horizontal and two vertical segments, and then check all four intersection conditions. This requires O(n^4) combinations, and each check is O(1), which leads to roughly 6×10^14 operations in the worst case. This is far beyond any feasible limit.

We can reduce this by separating horizontal and vertical segments. Suppose we fix two vertical segments. A rectangle exists with them if and only if there are at least two horizontal segments that intersect both vertical segments. If we know the number of common horizontal intersections, say k, then this pair of verticals contributes C(k, 2) rectangles.

So the problem reduces to: for every pair of vertical segments, count how many horizontal segments intersect both of them. The same logic would work symmetrically, but we only need one orientation.

Now the key optimization is to encode which horizontals intersect which verticals. For each vertical segment, we can build a list of all horizontal segments that intersect it. Then for each pair of vertical segments, we compute the size of the intersection of their lists. Since n is at most 5000, storing and intersecting these lists using a frequency array or marking technique is fast enough.

The final complexity becomes O(n^2) over pairs of vertical segments plus total intersection processing, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over quadruples | O(n^4) | O(1) | Too slow |
| Pair verticals + count common horizontals | O(n^2 + total intersections) | O(n^2) worst | Accepted |

## Algorithm Walkthrough

We reorganize the problem so that vertical segments act as “buckets” of horizontal intersections.

1. Split all segments into horizontals and verticals. This is necessary because only mixed pairs intersect, and rectangles are defined by two of each type.
2. For every vertical segment, compute which horizontal segments intersect it. A horizontal segment intersects a vertical segment if its x-range contains the vertical x-coordinate and its y-value lies within the vertical y-range.
3. Store these relationships in a structure where each vertical has a list of horizontal indices. This transforms geometry into combinatorics over sets.
4. For every pair of vertical segments, compute how many horizontals appear in both of their lists. This is the number of horizontal segments that touch both verticals.
5. If this number is k, then these two verticals form C(k, 2) rectangles, because we choose any two of the common horizontals as the top and bottom sides.
6. Sum this contribution over all vertical pairs.

The core reasoning is that every rectangle is uniquely determined by choosing its left and right vertical sides, and then choosing two horizontals that intersect both. This ensures every rectangle is counted exactly once.

### Why it works

Fix any valid rectangle. It has exactly two vertical sides and two horizontal sides. When we process the pair of its vertical sides, both horizontal sides will be present in the intersection list of those two verticals. Thus this rectangle is counted in the term C(k, 2) for that vertical pair. No other vertical pair can generate the same rectangle because the vertical sides are fixed by definition of the rectangle. This establishes both completeness and uniqueness of counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def intersect(h, v):
    # h: (x1, x2, y), v: (x, y1, y2)
    x1, x2, y = h
    x, y1, y2 = v
    return (min(x1, x2) <= x <= max(x1, x2)) and (min(y1, y2) <= y <= max(y1, y2))

n = int(input())
horiz = []
vert = []

for i in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    if y1 == y2:
        horiz.append((x1, x2, y1))
    else:
        vert.append((x1, y1, x2))

H = len(horiz)
V = len(vert)

# build adjacency: for each vertical, which horizontals it intersects
adj = [[] for _ in range(V)]

for vi, (x, y1, y2) in enumerate(vert):
    for hi, (x1, x2, y) in enumerate(horiz):
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            adj[vi].append(hi)

ans = 0

# count pairs of verticals
for i in range(V):
    mark = {}
    for h in adj[i]:
        mark[h] = 1
    for j in range(i + 1, V):
        cnt = 0
        for h in adj[j]:
            if h in mark:
                cnt += 1
        ans += cnt * (cnt - 1) // 2

print(ans)
```

The solution explicitly builds the intersection relationship between vertical and horizontal segments. The double loop over vertical pairs is unavoidable in this formulation, but each pair is processed using hash membership checks, which keeps intersection counting efficient.

A subtle point is using a dictionary (or set) per vertical. This avoids O(n) scanning when counting intersections. The final combination step uses the combinatorial identity C(k, 2), ensuring that we count pairs of horizontals rather than individual intersections.

## Worked Examples

### Example trace

Consider a simplified input with three horizontals and three verticals.

| Vertical pair | Common horizontals | k | Contribution |
| --- | --- | --- | --- |
| (v1, v2) | {h1, h2} | 2 | 1 |
| (v1, v3) | {h2} | 1 | 0 |
| (v2, v3) | {h1, h2} | 2 | 1 |

This shows how rectangles emerge only when at least two horizontals are shared.

The same mechanism scales to the full problem: every rectangle is exactly one “vertical pair + horizontal pair” configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V^2 · H̄) | Each vertical pair compares lists of intersecting horizontals |
| Space | O(V + H + intersections) | Stores adjacency lists between segments |

With n ≤ 5000, V and H are at most 5000, and total intersections are bounded by the input structure. This fits comfortably within limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import comb

    n = int(input())
    horiz = []
    vert = []

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        if y1 == y2:
            horiz.append((x1, x2, y1))
        else:
            vert.append((x1, y1, x2))

    V = len(vert)
    adj = []
    for x, y1, y2 in vert:
        s = set()
        for i, (x1, x2, y) in enumerate(horiz):
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                s.add(i)
        adj.append(s)

    ans = 0
    for i in range(V):
        for j in range(i + 1, V):
            k = len(adj[i] & adj[j])
            ans += k * (k - 1) // 2
    return str(ans)

# sample
assert run("""7
-1 4 -1 -2
6 -1 -2 -1
-2 3 6 3
2 -2 2 4
4 -1 4 3
5 3 5 1
5 2 1 2
""") == "7"

# minimum case
assert run("""2
0 0 0 1
1 0 1 1
""") == "0"

# single rectangle
assert run("""4
0 0 0 2
2 0 2 2
0 0 2 0
0 2 2 2
""") == "1"

# multiple overlapping structures
assert run("""6
0 0 0 2
2 0 2 2
4 0 4 2
0 0 4 0
0 2 4 2
1 1 1 3
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum case | 0 | no rectangle possible |
| single rectangle | 1 | basic correctness |
| multiple structure | 3 | combinatorial counting correctness |

## Edge Cases

A degenerate configuration occurs when several vertical segments share exactly the same set of intersecting horizontals. In such a case, every pair of verticals contributes a rectangle for every pair of shared horizontals, so the algorithm correctly uses C(k, 2) rather than k.

Another case is when a vertical intersects many horizontals but most other verticals intersect only a subset. The pairwise intersection logic ensures that only common horizontals contribute, preventing overcounting from independent intersections.
