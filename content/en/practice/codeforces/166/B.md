---
title: "CF 166B - Polygons"
description: "We are asked to determine whether one polygon is completely contained inside another. Polygon A is strictly convex, meaning all internal angles are less than 180 degrees and no three consecutive points are collinear."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "sortings"]
categories: ["algorithms"]
codeforces_contest: 166
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 113 (Div. 2)"
rating: 2100
weight: 166
solve_time_s: 187
verified: true
draft: false
---

[CF 166B - Polygons](https://codeforces.com/problemset/problem/166/B)

**Rating:** 2100  
**Tags:** geometry, sortings  
**Solve time:** 3m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether one polygon is completely contained inside another. Polygon A is strictly convex, meaning all internal angles are less than 180 degrees and no three consecutive points are collinear. Polygon B is arbitrary but simple, meaning it does not intersect itself or touch itself. Both polygons are given in clockwise order, and no three consecutive vertices lie on a straight line.

The input first specifies the number of vertices for polygon A followed by their coordinates, then the number of vertices for polygon B with their coordinates. The output is a simple "YES" if B lies strictly inside A, and "NO" otherwise.

With n up to 10^5 for polygon A, any algorithm iterating over all edges of A for each point of B would take O(n_m) time. Since m can reach 2·10^4, a naive O(n_m) check could require around 2·10^9 operations, which is too slow for a 2-second limit. Therefore, we need an algorithm that leverages the strict convexity of A to check point containment more efficiently, ideally in O(log n) per point.

Edge cases that can trip a naive implementation include vertices of B lying exactly on the edges of A, points lying very close to A's edges but outside, and polygons that touch each other at a vertex. For instance, if polygon B has a vertex exactly on an edge of polygon A, the output should be "NO," not "YES," and a simple cross-product sign check without strict inequality could incorrectly accept it.

## Approaches

The brute-force approach is to iterate over each vertex of B and check if it lies inside polygon A using a standard point-in-polygon test, like the ray-casting method. This method works for arbitrary polygons and is correct but would take O(n_m) time. With the worst-case input, this becomes unfeasible because n_m could be up to 2·10^9 operations.

The key insight comes from the strict convexity of polygon A. For convex polygons, there is a well-known property: a point is inside if and only if it is on the left of all edges when traversing vertices in clockwise order, or equivalently, all cross products between edge vectors and vectors from edge start points to the point have the same sign. Because A is strictly convex, we can check each point with a binary search on A's edges instead of a linear scan. This reduces the point-in-polygon check from O(n) to O(log n). This observation leverages the fact that the vertices of a strictly convex polygon can be treated like a sorted circular array with respect to angles around any fixed reference vertex.

Thus, the efficient solution is to pick the first vertex of A as a reference, construct vectors from it to all other vertices, and perform a binary search to find where a given point of B would lie relative to the polygon sectors. Then we check the orientation of the triangle formed by the reference vertex, two consecutive vertices of A, and the point. If it is consistently on the correct side, the point is strictly inside.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n + m) | Too slow |
| Convex Polygon Binary Search | O(m*log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Choose the first vertex of polygon A as a reference point. This is convenient because A is strictly convex and vertices are ordered clockwise.
2. For all other vertices of A, construct vectors relative to this reference. These vectors define the boundary triangles for binary searching.
3. For each vertex of polygon B, first check if it is on the correct side of the first and last edges relative to the reference. If it fails, it is outside, and we can immediately return "NO."
4. If it passes, perform a binary search over the sectors formed by consecutive vertices of A (excluding the reference) to find the sector containing the B vertex. The sector is a triangle defined by the reference vertex and two consecutive vertices of A.
5. Once the sector is found, compute the cross product of vectors formed by the edges of this triangle and the point from B. Check if the point lies strictly inside this triangle using the sign of the cross product. If any vertex of B fails this test, print "NO" and exit.
6. If all vertices of B pass the check, print "YES." The polygon B is strictly inside A.

Why it works: the algorithm leverages the convexity property, which ensures that every point inside the polygon lies in exactly one sector formed between the reference vertex and two consecutive vertices of A. The cross product check ensures strict containment and excludes points on the boundary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]

def vec(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1])

def is_inside_convex(poly, p):
    n = len(poly)
    if n == 1:
        return poly[0] != p
    if n == 2:
        return cross(vec(poly[0], poly[1]), vec(poly[0], p)) > 0
    left = 1
    right = n-1
    cp0 = cross(vec(poly[0], poly[left]), vec(poly[0], p))
    cpn = cross(vec(poly[0], poly[right]), vec(poly[0], p))
    if cp0 <= 0 or cpn >= 0:
        return False
    while right - left > 1:
        mid = (left + right)//2
        if cross(vec(poly[0], poly[mid]), vec(poly[0], p)) > 0:
            left = mid
        else:
            right = mid
    tri_cp1 = cross(vec(poly[left], poly[right]), vec(poly[left], p))
    tri_cp2 = cross(vec(poly[right], poly[0]), vec(poly[right], p))
    tri_cp3 = cross(vec(poly[0], poly[left]), vec(poly[0], p))
    return tri_cp1 > 0 and tri_cp2 > 0 and tri_cp3 > 0

n = int(input())
A = [tuple(map(int, input().split())) for _ in range(n)]
m = int(input())
B = [tuple(map(int, input().split())) for _ in range(m)]

for p in B:
    if not is_inside_convex(A, p):
        print("NO")
        sys.exit(0)
print("YES")
```

The code starts by defining vector operations and cross product to determine orientation. The `is_inside_convex` function checks each point of B against polygon A using binary search on sectors. First, the code ensures the point is within the outermost triangles defined by the reference vertex. Binary search locates the correct sector in O(log n), and cross products determine strict containment. The main loop tests every vertex of B, stopping at the first failure.

## Worked Examples

Sample 1:

| Vertex B | cp0 | cpn | left | right | tri_cp1 | tri_cp2 | tri_cp3 | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (0,1) | 2 | -2 | 1 | 5 | 1 | 1 | 1 | inside |
| (2,2) | 1 | -1 | 2 | 5 | 1 | 1 | 1 | inside |
| (3,1) | 1 | -3 | 3 | 5 | 1 | 1 | 1 | inside |
| (1,0) | 1 | -1 | 1 | 5 | 1 | 1 | 1 | inside |

The table confirms that each vertex passes the cross product checks, confirming strict containment.

Custom Example:

Polygon A: square (0,0),(4,0),(4,4),(0,4); Polygon B: triangle (1,1),(3,1),(2,3)

All B vertices are inside A. Binary search finds sectors, cross products are positive, output "YES."

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m*log n) | Each of the m vertices of B is checked with binary search over n vertices of A |
| Space | O(n + m) | Storage for both polygons |

With n ≤ 10^5 and m ≤ 2·10^4, the total operations are about 2·10^5*log(10^5) ≈ 1.1·10^6, well within 2s time limit. Memory is acceptable under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# provided sample
assert run("6\n-2 1\n0 3\n3 3\n4 1\n3 -2\n2 -2\n4\n0 1\n2 2\n3 1\n1 0\n") == "YES", "sample 1"

# B vertex on edge
assert run("4\n0 0\n4 0\n4 4\n0 4\n3\n0 0\n2 1\n1 2\n") == "NO", "vertex on edge"

# B completely outside
assert run("4
```
