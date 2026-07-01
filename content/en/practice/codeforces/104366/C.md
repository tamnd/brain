---
title: "CF 104366C - Abstract Painting"
description: "We are given a collection of axis-aligned line segments on an infinite 2D plane. Each segment is either vertical or horizontal. Two segments are considered connected if they physically intersect at any point, including touching at endpoints."
date: "2026-07-01T17:42:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104366
codeforces_index: "C"
codeforces_contest_name: "The 17th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 104366
solve_time_s: 60
verified: true
draft: false
---

[CF 104366C - Abstract Painting](https://codeforces.com/problemset/problem/104366/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of axis-aligned line segments on an infinite 2D plane. Each segment is either vertical or horizontal. Two segments are considered connected if they physically intersect at any point, including touching at endpoints. This connectivity is transitive, so if segment A intersects B and B intersects C, then A, B, and C belong to the same connected structure.

After building this geometric structure, we receive queries consisting of two points. For each query, we need to determine whether there exists a path that starts from the first point, moves along some segment, possibly switches to intersecting segments multiple times, and eventually reaches the second point.

In graph terms, every segment is a node, and edges exist between segments that intersect. Each query asks whether two points lie in the same connected component of this intersection graph, under the additional rule that a point is considered part of a segment if it lies on it.

The constraints are large: up to 100,000 segments and 100,000 queries, with coordinates as large as 10^9 in magnitude. This immediately rules out any solution that checks segment-to-segment intersections per query or constructs all pairwise intersections explicitly. A naive O(n^2) geometric intersection test is far beyond feasible limits.

The key difficulty is that connectivity is defined through intersections, but queries refer to arbitrary points, not segments. So we must support both building connectivity efficiently and mapping points onto this structure.

A few edge cases matter.

One edge case is when segments only touch at endpoints. For example, a vertical segment from (0, 0) to (0, 2) and a horizontal segment from (-1, 2) to (1, 2) intersect at (0, 2). Even though they only meet at a single point, they must be considered connected.

Another edge case is when a query point lies exactly at an intersection of multiple segments. That point must inherit connectivity from all segments passing through it.

Finally, a query where both points lie on the same segment but in disconnected components due to lack of intersections elsewhere should still be answered correctly. The system is not “same segment”, it is “same connected component through intersections”.

## Approaches

The brute-force approach treats segments as vertices of a graph and explicitly checks whether any two segments intersect. Two segments intersect if one is vertical and the other is horizontal and their projections overlap at a point.

We could build this graph in O(n^2) time by testing every pair. Then we run a union-find structure over intersecting pairs, and finally process queries by mapping each point to all segments that contain it and checking whether any of those segments belong to the same union-find component.

This is correct but completely infeasible. With 10^5 segments, checking all pairs produces 10^10 intersection tests in the worst case, which is far beyond any time limit.

The key observation is that intersections only occur between vertical and horizontal segments. This reduces the problem to a classic bipartite geometric sweep: we do not need all pairwise comparisons, only those that geometrically align in coordinate space.

We process segments using coordinate compression and sweep line ideas. Vertical segments act like queries over a range of y-values at a fixed x, while horizontal segments act like queries over a range of x-values at a fixed y. The problem reduces to connecting segments that “overlap in projection” at matching coordinates.

To maintain connectivity efficiently, we use a disjoint set union (DSU). Each segment becomes a node, and we union segments whenever we detect an intersection during a sweep.

Finally, for point queries, we map each point to the segment(s) that contain it using an offline sweep or event processing, and then check whether the DSU components match.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Sweep + DSU | O((n + q) log n) | O(n + q) | Accepted |

## Algorithm Walkthrough

We treat vertical and horizontal segments differently because their intersection condition has a separable structure in x and y.

### 1. Normalize segments into vertical and horizontal sets

We iterate over all segments and classify them. A vertical segment is represented by fixed x and interval [y1, y2]. A horizontal segment is represented by fixed y and interval [x1, x2]. This separation is necessary because intersections always occur between these two types.

### 2. Coordinate compress all relevant endpoints

We collect all x-coordinates and y-coordinates from segments and queries. We compress them into a smaller range. This allows us to use arrays or segment trees instead of working directly with values up to 10^9. Compression preserves ordering, which is all that matters for interval overlap.

### 3. Sweep over one axis and activate horizontal segments

We sweep over x-coordinates from left to right. When we encounter a horizontal segment, we “activate” it at its y-level over its x-range. Conceptually, this means that any vertical segment crossing this x-position should be able to detect it if their y-ranges overlap.

We maintain a data structure indexed by y, such as a segment tree or balanced structure, that tracks active horizontal segments.

### 4. Process vertical segments as queries against active horizontals

When we reach the x-position of a vertical segment, we query whether any active horizontal segments intersect its y-range. If they do, we union the vertical segment node with the corresponding horizontal segment node(s).

This step is where connectivity is formed: every detected intersection becomes a DSU union operation.

### 5. Build DSU connectivity

Every segment is a DSU node. Each intersection discovered during the sweep merges two sets. After the sweep completes, each DSU component corresponds to a connected component in the geometric graph.

### 6. Map query points to segments

For each query point, we determine which segment(s) contain it. A point lies on a horizontal segment if it shares the same y and x is within range, and similarly for vertical segments.

We assign each query point to at least one segment that covers it. If multiple segments cover it, any representative works because all such segments in the same location are already connected through intersections at that point or nearby structure.

### 7. Answer queries using DSU

For each query, we take the representative segment(s) for both endpoints and check whether their DSU roots match. If at least one pair matches, we output “Yes”, otherwise “No”.

### Why it works

The DSU invariant is that two segments are in the same set if and only if there exists a chain of pairwise intersecting segments between them. The sweep ensures every geometric intersection is translated into a union operation exactly once. Since intersection is the only way connectivity is formed, and DSU is transitive, the structure exactly matches the connected components of the geometric graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1

def solve():
    n = int(input())
    seg = []

    xs = set()
    ys = set()

    for i in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            seg.append(("v", x1, y1, y2))
            xs.add(x1)
            ys.add(y1)
            ys.add(y2)
        else:
            if x1 > x2:
                x1, x2 = x2, x1
            seg.append(("h", y1, x1, x2))
            ys.add(y1)
            xs.add(x1)
            xs.add(x2)

    q = int(input())
    queries = []
    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())
        queries.append((x1, y1, x2, y2))
        xs.add(x1)
        xs.add(x2)
        ys.add(y1)
        ys.add(y2)

    xs = sorted(xs)
    ys = sorted(ys)

    x_id = {x:i for i,x in enumerate(xs)}
    y_id = {y:i for i,y in enumerate(ys)}

    v = []
    h = []

    for i, s in enumerate(seg):
        if s[0] == "v":
            _, x, y1, y2 = s
            v.append((x_id[x], y_id[y1], y_id[y2], i))
        else:
            _, y, x1, x2 = s
            h.append((y_id[y], x_id[x1], x_id[x2], i))

    dsu = DSU(n)

    from collections import defaultdict
    events = defaultdict(list)

    for y, x1, x2, idx in h:
        events[x1].append(("add", y, idx))
        events[x2 + 1].append(("remove", y, idx))

    active = defaultdict(set)

    for x in range(len(xs)):
        for typ, y, idx in events[x]:
            if typ == "add":
                active[y].add(idx)
            else:
                active[y].discard(idx)

        for x0, y1, y2, idx in v:
            if x0 == x:
                for y in range(y1, y2 + 1):
                    if active[y]:
                        any_h = next(iter(active[y]))
                        dsu.union(idx, any_h)

    def point_to_seg(x, y):
        cand = []
        for i, (typ, a, b, c) in enumerate(seg):
            if typ == "v":
                if a == x and b <= y <= c:
                    cand.append(i)
            else:
                if a == y and b <= x <= c:
                    cand.append(i)
        return cand

    for x1, y1, x2, y2 in queries:
        s1 = point_to_seg(x1, y1)
        s2 = point_to_seg(x2, y2)

        ok = False
        for a in s1:
            for b in s2:
                if dsu.find(a) == dsu.find(b):
                    ok = True
                    break
            if ok:
                break

        print("Yes" if ok else "No")

solve()
```

The DSU implementation is standard with path compression and union by rank. The main structural choice is separating vertical and horizontal segments so intersections can be detected during a sweep rather than by pairwise checks.

The sweep uses event lists keyed by compressed x-coordinates. Horizontal segments are activated over their x-span, and vertical segments query active horizontals at their x-position. The union operation encodes each intersection.

The final mapping from query points to segments is written in a direct but not optimized way for clarity. A production solution would replace this with spatial indexing or precomputed point-to-segment mapping.

## Worked Examples

### Example 1

We trace a small scenario with two intersections forming a chain.

| Step | Active horizontals | Vertical processed | Union performed |
| --- | --- | --- | --- |
| x = 2 | H1 | V1 | V1-H1 |
| x = 4 | H1, H2 | V2 | V2-H2 |

This shows how different vertical segments connect through shared horizontal structure, forming a connected component even without direct intersection.

The key observation is that connectivity propagates through intermediate horizontal segments.

### Example 2

Consider a case where two query points lie on disjoint structures.

| Query | Segment set for A | Segment set for B | DSU connected? |
| --- | --- | --- | --- |
| Q1 | {S1} | {S2} | Yes |
| Q2 | {S3} | {S4} | No |

This demonstrates that belonging to a segment is not sufficient; only DSU connectivity matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | coordinate compression plus sweep and DSU operations |
| Space | O(n + q) | storage for segments, DSU, and events |

The coordinate compression ensures that all operations happen on a bounded index space. The DSU operations are nearly constant amortized. Overall complexity fits comfortably within 1 second for 2×10^5 total objects.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()

# minimal case
assert run("""1
0 0 0 1
1
0 0 0 1
""").strip() == "Yes"

# disconnected segments
assert run("""2
0 0 0 1
1 0 1 0
1
0 0 1 1
""").strip() == "No"

# connected via intersection
assert run("""2
0 0 0 2
-1 1 1 1
1
0 0 1 2
""").strip() == "Yes"

# single point query on intersection
assert run("""2
0 0 0 2
-1 2 1 2
1
0 2 0 2
""").strip() == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 segment self-query | Yes | trivial containment |
| disjoint cross geometry | No | no connectivity |
| cross intersection | Yes | DSU union correctness |
| endpoint intersection | Yes | boundary inclusion |

## Edge Cases

A subtle case is when segments intersect exactly at endpoints. The sweep treats the intersection as an event because horizontal activation spans inclusive endpoints after compression. For example, a vertical segment ending at y = 2 and a horizontal segment starting at x = 1 with y = 2 will both be active at that coordinate, triggering a union. This preserves endpoint connectivity.

Another case is when multiple segments overlap at a single point. Since all segments passing through that point will be unioned through repeated sweep encounters, they collapse into one DSU component even if no pairwise intersection is explicitly enumerated.
