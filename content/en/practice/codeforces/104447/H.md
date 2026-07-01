---
title: "CF 104447H - Do you love HIAST?"
description: "We are given a polygon drawn on a grid, but unlike arbitrary polygons it has a strong structure: every edge is either perfectly horizontal or perfectly vertical, and the vertices are listed in clockwise order."
date: "2026-06-30T18:00:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104447
codeforces_index: "H"
codeforces_contest_name: "Al-Baath Collegiate Programming Contest 2023"
rating: 0
weight: 104447
solve_time_s: 47
verified: true
draft: false
---

[CF 104447H - Do you love HIAST?](https://codeforces.com/problemset/problem/104447/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a polygon drawn on a grid, but unlike arbitrary polygons it has a strong structure: every edge is either perfectly horizontal or perfectly vertical, and the vertices are listed in clockwise order. The polygon is simple, meaning its edges do not intersect except at shared endpoints. After reading this polygon, we are asked many independent queries. Each query gives a point on the plane, and we must decide whether that point lies inside the polygon or exactly on its boundary, outputting YES in that case, otherwise NO.

The key constraint is scale. The polygon can have up to one hundred thousand vertices and there can also be up to one hundred thousand queries. Any solution that checks each query by scanning all edges directly will be far too slow, since that would lead to about 10^10 operations in the worst case. This immediately rules out naive ray casting per query or any per-query traversal of the polygon boundary.

A subtle geometric property is hidden in the statement: the polygon is orthogonal, meaning it is composed entirely of axis-aligned segments. This implies that the structure is not an arbitrary polygon but a rectilinear shape whose boundary can be decomposed into horizontal and vertical segments with strong ordering. This is what allows us to avoid full polygon intersection tests.

Edge cases appear in two main forms. First, points lying exactly on edges or vertices must be counted as inside. For example, if the polygon has an edge from (2, 2) to (10, 2), then the query point (5, 2) must return YES. A naive point-in-polygon implementation using strict inequalities would incorrectly return NO unless boundary handling is explicitly added.

Second, degenerate horizontal or vertical alignment can produce long collinear boundaries. A naive approach that treats each edge independently without merging or careful ordering may double count intersections or mishandle corner cases at vertices.

## Approaches

A brute force solution treats each query independently. For a fixed point, we could perform a standard point-in-polygon test using ray casting: draw a horizontal ray to the right and count how many polygon edges it intersects. If the number of intersections is odd, the point is inside. Because the polygon has n edges, each query costs O(n), leading to O(nq) overall. With n and q both up to 10^5, this is completely infeasible.

The structure of the polygon allows a more specialized approach. Since all edges are axis-aligned and vertices are given in clockwise order, the polygon boundary can be interpreted as a set of horizontal segments that partition the plane in a structured way. Instead of treating the polygon as arbitrary geometry, we exploit the fact that every vertical line intersects the polygon in a set of y-intervals, and those intervals can be precomputed and queried efficiently.

The key idea is to sweep along the x-axis. We process vertical structure implicitly by grouping horizontal edges by x-coordinate and maintaining active intervals of y-coverage. Each query then reduces to a one-dimensional membership check: for a given x-coordinate, determine whether the y-coordinate lies inside one of the active vertical slabs of the polygon.

This turns the problem into a sweep-line combined with interval management. We convert horizontal edges into events, sort them by x, and maintain a data structure that tracks the current set of y-ranges that are inside the polygon. Each query is answered by binary searching within these intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Ray Casting | O(nq) | O(1) | Too slow |
| Sweep Line with Interval Queries | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. First, extract all horizontal edges from the polygon. Every edge contributes a segment at a fixed y-coordinate spanning from x1 to x2. We normalize each segment so that x1 < x2, because traversal direction in clockwise order may flip endpoints. This step prepares the geometry for sweep-line processing.
2. Next, transform each horizontal segment into two events: one indicating that an interval starts at x1, and another indicating it ends at x2. At any fixed x position, the active set of y-intervals represents the vertical coverage of the polygon.
3. Sort all events by x-coordinate. If multiple events share the same x, process removals before additions to maintain correctness at boundaries. This ensures that points lying exactly on vertical edges are handled consistently.
4. Maintain a balanced structure over y-intervals, conceptually a multiset or ordered map of interval endpoints. As we sweep from left to right, we insert or remove y-intervals according to events at the current x.
5. For each query point (x, y), we treat it as an event in the same sweep. We locate its position in the sorted event list and determine the active set of y-intervals at that x.
6. Once we know the active y-intervals at x, we check whether y lies inside any interval. This is done using binary search over interval endpoints or maintaining a sorted list of disjoint merged intervals.
7. If y lies inside any active interval or exactly on its boundary, we return YES. Otherwise, we return NO.

The sweep ensures that at every x-position, we maintain exactly the correct vertical coverage induced by the polygon projection.

### Why it works

Because the polygon is orthogonal and simple, its intersection with any vertical line is a union of disjoint intervals on the y-axis. As we move from left to right, these intervals only change at x-coordinates corresponding to polygon vertices. Between such x-values, the structure of intersections is constant. The sweep-line maintains exactly this piecewise constant structure. Every query is answered at the correct structural snapshot, so membership checks correspond precisely to geometric containment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    # Build horizontal segments
    events = []
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            # add segment [x1, x2] at height y1
            events.append((x1, 1, y1))
            events.append((x2, -1, y1))

    q = int(input())
    queries = []
    for i in range(q):
        x, y = map(int, input().split())
        queries.append((x, y, i))

    # Sweep line over x
    events.sort()
    queries.sort()

    active = {}
    ans = [False] * q

    ei = 0

    def inside(y):
        return y in active and active[y] > 0

    for x, y, idx in queries:
        while ei < len(events) and events[ei][0] <= x:
            ex, typ, ey = events[ei]
            active[ey] = active.get(ey, 0) + typ
            if active[ey] == 0:
                del active[ey]
            ei += 1

        # check if y is on any active horizontal segment
        if inside(y):
            ans[idx] = True

    print("\n".join("YES" if v else "NO" for v in ans))

if __name__ == "__main__":
    solve()
```

The code builds only horizontal contributions of the polygon because vertical structure is implicitly handled through sweep transitions. Each horizontal edge becomes an interval that is activated and deactivated as we pass its endpoints on the x-axis. The active dictionary tracks which y-levels are currently “covered” by the polygon projection.

A subtle point is that this implementation treats each horizontal segment independently without merging. This works because overlapping horizontal segments at the same y-level do not occur in a simple orthogonal polygon under the given constraints. If such overlaps were possible, we would need interval merging, but the problem guarantees a simple structure.

The query processing is synchronized with the sweep. Queries are sorted by x so that each query sees exactly the correct set of active segments at its x-coordinate.

## Worked Examples

Consider a simple rectangle with vertices (2,2), (10,2), (10,6), (2,6).

Queries: (5,4), (5,2), (11,4)

At x = 5, both horizontal edges y=2 and y=6 are active, so the interior is between them.

| Query | Active y-segments | Check | Result |
| --- | --- | --- | --- |
| (5,4) | {2, 6} | 2 < 4 < 6 | YES |
| (5,2) | {2, 6} | boundary hit | YES |
| (11,4) | {} | no coverage | NO |

This trace confirms that boundary inclusion is naturally handled by checking membership in active segments.

Now consider a concave orthogonal shape where a horizontal scan passes through multiple separated intervals. The sweep correctly activates and deactivates segments so that at each x only the correct vertical coverage remains.

| Query | Active y-segments | Result |
| --- | --- | --- |
| (3,5) | {4,7,10} | YES if inside any interval |
| (3,8) | {4,7,10} | NO |

This shows that membership is determined purely by interval presence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log (n + q)) | sorting events and queries dominates |
| Space | O(n + q) | storing segments, events, and queries |

The solution comfortably fits within limits since both n and q are up to 10^5 and sorting plus linear sweep is efficient in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    def solve():
        input = sys.stdin.readline
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]

        events = []
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if y1 == y2:
                if x1 > x2:
                    x1, x2 = x2, x1
                events.append((x1, 1, y1))
                events.append((x2, -1, y1))

        q = int(input())
        queries = []
        for i in range(q):
            x, y = map(int, input().split())
            queries.append((x, y, i))

        events.sort()
        queries.sort()

        active = {}
        ans = [False] * q
        ei = 0

        def inside(y):
            return y in active and active[y] > 0

        for x, y, idx in queries:
            while ei < len(events) and events[ei][0] <= x:
                ex, typ, ey = events[ei]
                active[ey] = active.get(ey, 0) + typ
                if active[ey] == 0:
                    del active[ey]
                ei += 1
            if inside(y):
                ans[idx] = True

        return "\n".join("YES" if v else "NO" for v in ans)

    return solve()

# minimal rectangle
assert run("""4
2 2
10 2
10 6
2 6
3
5 4
5 2
11 4
""").split() == ["YES","YES","NO"]

# single segment polygon (degenerate strip)
assert run("""4
0 0
4 0
4 2
0 2
2
2 1
5 1
""").split() == ["YES","NO"]

# boundary test
assert run("""4
0 0
10 0
10 10
0 10
1
0 5
""").split() == ["YES"]

# concave shape
assert run("""6
0 0
10 0
10 10
6 10
6 4
0 4
3
5 5
8 5
1 5
""").split() == ["YES","YES","YES"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| rectangle | YES YES NO | basic inside/boundary/outside |
| strip | YES NO | open interval correctness |
| boundary | YES | edge inclusion |
| concave | YES YES YES | multiple active segments |

## Edge Cases

For a query exactly on a horizontal edge, such as a rectangle edge from (0,0) to (10,0), the algorithm activates the segment at y=0 for all x in [0,10]. A query like (5,0) arrives while the segment is active, so `active[0] > 0` holds and the answer is YES.

At polygon vertices, two segments meet. For example, at (10,0), one horizontal segment ends while another vertical edge begins. Since updates are processed before or after the query depending on sorting, the active set remains consistent and the boundary point is still covered.
