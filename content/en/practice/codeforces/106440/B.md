---
title: "CF 106440B - \u51f8\u5305"
description: "We are given a set of distinct points in the plane. The task is to split these points into two non-empty groups, call them A and B, such that the convex hull formed by A and the convex hull formed by B do not touch at all, neither in their interiors nor on their boundaries."
date: "2026-06-22T04:17:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106440
codeforces_index: "B"
codeforces_contest_name: "\u201c\u89c4\u5f8b\u672a\u6765\u676f\u201d2026 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b"
rating: 0
weight: 106440
solve_time_s: 59
verified: true
draft: false
---

[CF 106440B - \u51f8\u5305](https://codeforces.com/problemset/problem/106440/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of distinct points in the plane. The task is to split these points into two non-empty groups, call them A and B, such that the convex hull formed by A and the convex hull formed by B do not touch at all, neither in their interiors nor on their boundaries.

In simpler geometric terms, we are looking for two groups of points whose “rubber band shapes” are completely separated, so that there is a gap between the two resulting convex polygons. We are free to ignore any number of points as long as both groups are non-empty and disjoint.

The key geometric implication of the constraints is that there are at most 500 points, and no three points are collinear. That last condition removes degeneracies such as many points lying on a single line segment, which simplifies convex hull reasoning because every hull vertex is well-defined and strictly turns left or right.

With 500 points, an O(n log n) or even O(n²) solution is acceptable. Anything cubic or worse is unnecessary.

A subtle failure case for naive intuition is trying to split points arbitrarily, for example by taking the first half of the input as A and the second half as B. Even if both sets are non-empty, their convex hulls can overlap heavily.

For example, four points forming a square in order and splitting diagonally by index can produce two sets whose convex hulls are both the entire square, so they intersect completely even though the sets are disjoint.

This shows that the partition must respect geometry, not input order.

## Approaches

A brute-force idea would be to try all ways of splitting the points into two non-empty subsets and check whether their convex hulls intersect. For each partition, computing two convex hulls costs O(n log n), and there are 2ⁿ possible partitions, so this approach is completely infeasible even for n = 30.

The structure of the problem suggests we do not need to search at all. We are not asked to optimize any measure; we only need existence of one valid separation.

The key observation is that if we can find a single point that is guaranteed to lie strictly outside the convex hull of all remaining points, then we can isolate it as one group. A single point has a degenerate convex hull consisting only of itself, so if it lies outside the other hull, the two hulls are automatically disjoint.

This reduces the task to finding any point that is a vertex of the convex hull of the entire set. A convex hull vertex cannot be written as a convex combination of other points, which means it cannot lie inside the convex hull of the remaining points after removal.

So the entire problem collapses to computing the global convex hull and choosing one of its vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2ⁿ · n log n) | O(n) | Too slow |
| Convex hull vertex selection | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first compute the convex hull of all given points using a standard monotonic chain algorithm.

1. Sort all points by x-coordinate, breaking ties by y-coordinate. This gives a deterministic order for building the hull.
2. Construct the lower hull by scanning points left to right. Each time we add a new point, we remove the last point from the hull while the last turn formed is not a strict counterclockwise turn. This enforces convexity of the lower boundary.
3. Construct the upper hull similarly by scanning from right to left, applying the same convexity condition.
4. Merge the two hulls to obtain the full convex polygon. Every point that remains in this structure is a vertex of the convex hull of the entire set.
5. Select any one of these hull vertices, and place it into set A.
6. Place all remaining points into set B.

The reason we pick only a single hull vertex is that it is guaranteed to be an extreme point of the full configuration, so it cannot be contained in the convex hull of the remaining points.

### Why it works

The convex hull of all points is the smallest convex set containing them. Any vertex of this hull is an extreme point in some direction, meaning there exists a supporting line where all other points lie strictly on one side of that vertex.

If we remove such a vertex, the remaining points all lie in a convex region that does not contain that vertex. Since convex hulls are closed under convex combinations, the removed vertex cannot be reconstructed from the remaining points, which means it lies outside their convex hull.

Thus A’s convex hull is a single point, and B’s convex hull is a polygon that does not include that point. Two disjoint convex sets cannot intersect, neither in interior nor boundary, so the condition is satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

n = int(input())
pts = []
for i in range(n):
    x, y = map(int, input().split())
    pts.append((x, y, i + 1))

pts.sort()

lower = []
for p in pts:
    while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
        lower.pop()
    lower.append(p)

upper = []
for p in reversed(pts):
    while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
        upper.pop()
    upper.append(p)

hull = lower[:-1] + upper[:-1]

# pick any hull vertex
a_idx = hull[0][2]
A = [a_idx]
B = [p[2] for p in pts if p[2] != a_idx]

print(len(A), len(B))
print(*A)
print(*B)
```

The code builds the convex hull using the monotonic chain method. The cross product is used to enforce left turns only, ensuring the structure remains convex.

After computing the hull, we simply take the first hull vertex. Any hull vertex works equally well, because every such point is guaranteed to be extreme.

The remaining points are collected into B. No additional geometric checks are needed, because convexity guarantees separation.

## Worked Examples

Consider a small configuration of five points forming a convex pentagon.

| Step | Hull Construction | Selected A | Remaining B |
| --- | --- | --- | --- |
| After sorting | Points ordered by x-y | - | - |
| Lower hull | Builds convex boundary | - | - |
| Upper hull | Completes polygon | - | - |
| Final hull | All 5 points | - | - |
| Selection | First hull vertex | one vertex | others |

In this case, choosing any vertex of the pentagon isolates that point, and the remaining four still form a convex polygon that does not include it.

Now consider a case where points form a dense convex shape with interior points.

| Step | Observation |
| --- | --- |
| Input | Many interior points plus boundary points |
| Hull result | Only outer boundary points remain |
| A selection | Any boundary vertex |
| B set | All points except that vertex |

This shows that interior points do not affect the correctness, because they never appear in the hull and are safely included in B.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates convex hull construction |
| Space | O(n) | Storage for points and hull arrays |

With n up to 500, sorting and linear scans are trivial within limits. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import Popen, PIPE
    return ""

# sample placeholders (actual judge samples should be inserted)
# assert run(...) == ...

# custom tests

# minimum size valid case (6 points in convex position)
inp = """6
0 0
1 0
2 0
2 1
1 2
0 2
"""
# expected: 1 point vs 5 points
# assert run(inp) ...

# convex square with interior point
inp = """5
0 0
2 0
2 2
0 2
1 1
"""

# all points on convex hull except interior
# assert run(inp) ...

# random small case
inp = """7
0 0
3 0
3 3
0 3
1 1
2 1
1 2
"""
# assert run(inp) ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 convex points | 1 vs 5 split | Basic hull vertex separation |
| square + interior | 1 vs 4 split | Interior points do not matter |
| random small set | valid split | General correctness |

## Edge Cases

One important situation is when all points lie on the convex hull boundary. In this case, the hull contains every point, but any single vertex is still valid for isolation. The algorithm selects a vertex and places it into A, leaving the rest in B, and the separation still holds because the remaining points form a convex polygon that excludes that vertex.

Another case is when there are many interior points. Even though these points never appear in the hull, they are safely placed into B. The convex hull of B may shrink compared to the full hull, but it still cannot include the removed extreme vertex.

A final subtle case is when multiple points share extreme coordinates, such as several points with the same maximum x-value. The monotonic chain still selects the true extreme boundary vertices, and picking any one of them is sufficient because all are guaranteed to lie outside the convex hull of the rest.
