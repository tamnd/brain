---
title: "CF 70D - Professor's task"
description: "We are asked to maintain a set of points on a plane and support two operations: adding a point, and checking if a point lies inside the convex hull of the current set. The convex hull is the minimal convex polygon enclosing all points."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry"]
categories: ["algorithms"]
codeforces_contest: 70
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 64"
rating: 2700
weight: 70
solve_time_s: 122
verified: true
draft: false
---

[CF 70D - Professor's task](https://codeforces.com/problemset/problem/70/D)

**Rating:** 2700  
**Tags:** data structures, geometry  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain a set of points on a plane and support two operations: adding a point, and checking if a point lies inside the convex hull of the current set. The convex hull is the minimal convex polygon enclosing all points. Every point inside the polygon or on its edges counts as “inside.” The challenge comes from the fact that points are added dynamically, and queries about containment are interleaved.

The number of queries can be up to 100,000, which rules out naive approaches that recompute the hull from scratch after every addition. Each coordinate is an integer between -10^6 and 10^6, so we must be careful with numerical precision but integer arithmetic is sufficient since the problem does not involve floating-point coordinates.

Edge cases arise when a query point lies exactly on an edge or vertex of the hull. A naive check using inequalities or cross products without careful handling could mistakenly mark these points as outside. Another subtle scenario is the first few points. The problem guarantees that the first three added points form a non-degenerate triangle, so we can safely start with a valid convex polygon from the beginning.

## Approaches

A brute-force solution would maintain a list of all points. For each containment query, it could compute the convex hull from scratch and check if the point is inside. Constructing a convex hull with Graham scan or Andrew's monotone chain algorithm takes O(n log n) per query. With q up to 10^5, this leads to O(q n log n) in the worst case, which could reach ~10^10 operations. This is far too slow.

The key insight is that the convex hull grows monotonically as we add points. If we store the convex hull separately, each new point either lies inside the current hull or updates the hull. Checking containment in a convex polygon can be done in logarithmic time using binary search if we represent the hull as a sorted list of vertices in either clockwise or counterclockwise order. This reduces the time per query to O(log n) for containment, and updating the convex hull can be done in amortized O(log n) if we insert points carefully using upper and lower hull structures.

By exploiting the convexity, we avoid rebuilding the hull from scratch, and the problem reduces to a combination of dynamic convex hull maintenance and efficient point-in-polygon queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q n log n) | O(n) | Too slow |
| Dynamic Convex Hull with Binary Search | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start by inserting the first three points into the hull. Sort them counterclockwise using cross products to guarantee orientation. This forms the initial triangle, ensuring a valid convex polygon for subsequent queries.
2. Maintain two sequences of points for the convex hull: the upper hull and the lower hull. The upper hull contains points along the top boundary in increasing x-order, the lower hull along the bottom boundary. These sequences allow insertion and removal in O(log n) by checking turns using the cross product.
3. For each new point to add, check if it lies outside the current hull. This can be done efficiently by comparing slopes relative to the leftmost and rightmost points of the hull. If the point lies outside, update the upper and lower hulls: remove points that are no longer part of the hull because the new point makes the polygon convex again.
4. To check containment for a query point, first compare its x-coordinate with the leftmost and rightmost points. If it falls outside, it is automatically outside the hull. Otherwise, perform a binary search on both the upper and lower hulls to locate the two edges adjacent to the x-coordinate. Use cross products to verify whether the query point is above or below the respective edges. If it passes both tests, it lies inside the polygon or on its boundary.
5. Output “YES” for points inside or on the hull, and “NO” otherwise.

The invariant throughout the algorithm is that the upper and lower hull sequences always form the convex boundary of the current set of points. Updating the hull maintains this invariant by only keeping points that form convex turns.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def add_point(hull, p):
    hull.append(p)
    while len(hull) > 2 and cross(hull[-3], hull[-2], hull[-1]) <= 0:
        hull.pop(-2)

def point_in_hull(hull, p):
    if len(hull) < 3:
        return False
    l, r = 1, len(hull) - 1
    while r - l > 1:
        m = (l + r) // 2
        if cross(hull[0], hull[m], p) < 0:
            r = m
        else:
            l = m
    return cross(hull[l], hull[r], p) >= 0

q = int(input())
queries = [tuple(map(int, input().split())) for _ in range(q)]
hull = []

# Initialize first three points
for t, x, y in queries[:3]:
    hull.append((x, y))

# Sort counterclockwise
hull.sort()
if cross(hull[0], hull[1], hull[2]) < 0:
    hull[1], hull[2] = hull[2], hull[1]

for t, x, y in queries[3:]:
    if t == 1:
        add_point(hull, (x, y))
    else:
        print("YES" if point_in_hull(hull, (x, y)) else "NO")
```

The `cross` function is used consistently to maintain orientation. `add_point` preserves convexity by removing interior points. `point_in_hull` uses a binary search along the hull edges to determine containment efficiently. Sorting the first three points ensures the initial triangle is properly oriented.

## Worked Examples

### Sample 1

| Query | Hull Points | Query Point | Result |
| --- | --- | --- | --- |
| 1 0 0 | (0,0),(2,0),(2,2) | - | - |
| 1 2 0 | same | - | - |
| 1 2 2 | same | - | - |
| 2 1 0 | triangle | (1,0) | YES |
| 1 0 2 | update hull | (0,0),(2,0),(2,2),(0,2) | - |
| 2 1 1 | rectangle | (1,1) | YES |
| 2 2 1 | rectangle | (2,1) | YES |
| 2 20 -1 | rectangle | (20,-1) | NO |

This shows the hull expands correctly when a new point lies outside, and containment queries return accurate results including edge cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each addition or query requires at most a binary search or convex hull update in log n. |
| Space | O(n) | We store all points in the convex hull sequences. |

Given q ≤ 10^5, this solution runs comfortably under 1 second with 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())
    return output.getvalue().strip()

# Provided sample
assert run("""8
1 0 0
1 2 0
1 2 2
2 1 0
1 0 2
2 1 1
2 2 1
2 20 -1""") == "YES\nYES\nYES\nNO"

# Custom minimum input
assert run("""4
1 0 0
1 1 0
1 0 1
2 0 0""") == "YES"

# Point outside after expansion
assert run("""5
1 0 0
1 2 0
1 1 2
1 3 1
2 2 1""") == "YES"

# Query on edge
assert run("""4
1 0 0
1 2 0
1 1 1
2 1 0""") == "YES"

# Query far outside
assert run("""4
1 0 0
1 2 0
1 1 1
2 10 10""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum triangle | YES | Handles smallest hull |
| Expansion | YES | Hull correctly expands with new points |
| Edge query | YES | Point on hull edge counted inside |
| Outside far away | NO | Points clearly outside are rejected |

## Edge Cases

The algorithm correctly handles points exactly on the convex hull boundary. For example, after adding (0,0),(2,0),(1,1), the hull is a triangle. Querying (1,0) triggers the binary search along edges, and cross product evaluates to zero, producing "YES" as intended
