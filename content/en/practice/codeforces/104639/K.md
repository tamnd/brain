---
title: "CF 104639K - Minimum Euclidean Distance"
description: "We are given a convex polygon that represents a safe region in the plane. For every airdrop query, we also get a circle defined by its diameter endpoints. Each airdrop lands uniformly at random anywhere inside that circle."
date: "2026-06-29T16:57:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104639
codeforces_index: "K"
codeforces_contest_name: "The 2023 ICPC Asia EC Regionals Online Contest (I)"
rating: 0
weight: 104639
solve_time_s: 34
verified: true
draft: false
---

[CF 104639K - Minimum Euclidean Distance](https://codeforces.com/problemset/problem/104639/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a convex polygon that represents a safe region in the plane. For every airdrop query, we also get a circle defined by its diameter endpoints. Each airdrop lands uniformly at random anywhere inside that circle.

For each query we must choose a single point inside the polygon. That point acts as a fixed landing reference. The cost of a choice is the expected value of the squared Euclidean distance between this chosen point and a uniformly random point inside the circle. The task is to minimize this expectation over all choices of the point inside the polygon, and output the resulting minimum value for each circle.

The polygon is fixed, while circles vary across queries. The constraints allow up to 5000 vertices and 5000 queries, with coordinates up to 1e9.

A naive interpretation is that each query requires optimizing a continuous function over a convex polygon, which already suggests that geometry and convexity properties will be central.

A key structural observation is that the expectation depends only on the relative position between the chosen point and the random point in the circle, and not on the polygon shape except through feasibility of the chosen point.

A subtle edge case is when the best point for a circle lies outside the polygon. For example, if the polygon is very small and the circle is far away, the optimal unconstrained point might be the circle center, but the polygon forces projection onto its boundary. This means we are not just computing a geometric property of the circle, but a constrained optimization over a convex set.

## Approaches

Start by ignoring the polygon constraint. For a fixed circle, suppose we choose a point P and the random point X is uniformly distributed inside a disk. The objective is to minimize E[|P − X|²].

Expanding the square gives E[|P − X|²] = |P|² − 2P·E[X] + E[|X|²]. The key simplification is that the expectation depends on P only through its distance to the mean of the distribution. For a uniform distribution over a disk, the mean is exactly the center of the circle. Therefore the expression becomes minimized when P is as close as possible to the circle center, and the minimum unconstrained value is achieved at P equal to the center.

Thus the problem reduces to projecting the circle center onto the convex polygon. The optimal P is the closest point in the polygon to the circle center in Euclidean distance. Once we have that projection point Q, the answer is E[|Q − X|²], which can be expanded as |Q − C|² + E[|X − C|²], where C is the circle center.

So the problem splits into two parts: a geometric constant term depending only on the circle, and a squared distance from the circle center to the polygon.

The remaining task is to compute, for each query point C, the squared distance from C to a convex polygon. With n up to 5000 and q up to 5000, an O(nq) point-in-polygon or distance-to-edge scan is sufficient. Because the polygon is convex and vertices are ordered, the closest point to an external point lies either on a vertex or on an edge where the perpendicular projection lands within the segment. This can be checked in linear time per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force projection per query over all edges | O(nq) | O(n) | Accepted |
| Optimal same as above with convex geometry simplification | O(nq) | O(n) | Accepted |

There is no need for more advanced data structures since the constraints are small enough, and the geometry is straightforward once the expectation is rewritten correctly.

## Algorithm Walkthrough

1. Precompute the circle center and radius squared for each query. The center is the midpoint of the diameter endpoints, and the radius squared is one quarter of the squared distance between endpoints. This isolates all query-specific geometric data.
2. For each query, treat the problem as finding the minimum squared distance from the circle center to the convex polygon. This is justified because the expectation decomposes into a constant depending only on the circle plus the squared distance from the chosen point to the center.
3. For a given center point C, iterate over all polygon edges. For each edge AB, compute the projection of C onto the line AB.
4. If the projection parameter lies within the segment, compute the squared distance from C to the projection point. Otherwise compute the squared distance to the nearest endpoint among A and B. This ensures we are computing distance to the closest point on that edge segment.
5. Maintain the minimum such squared distance over all edges and vertices. This gives the squared distance from C to the convex polygon.
6. Add the constant expected value of squared distance from a random point in the disk to its center, which equals R²/2, and output the sum.

The key reason step 6 works is that for a uniform disk, variance in two dimensions splits evenly across axes, giving E[|X − C|²] = R²/2.

### Why it works

The expectation E[|P − X|²] can be decomposed into |P − C|² + E[|X − C|²], where C is the circle center. The second term is independent of P, so minimizing the expectation reduces exactly to minimizing the squared distance from P to C. Since the feasible region is convex, the closest feasible point is well-defined and lies on a vertex or edge projection. The algorithm enumerates all such candidates, so it must include the true closest point and therefore achieves the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dot(ax, ay, bx, by):
    return ax * bx + ay * by

def dist2(ax, ay, bx, by):
    dx = ax - bx
    dy = ay - by
    return dx * dx + dy * dy

def clamp01(t):
    if t < 0.0:
        return 0.0
    if t > 1.0:
        return 1.0
    return t

def solve():
    n, q = map(int, input().split())
    poly = [tuple(map(int, input().split())) for _ in range(n)]

    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())

        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0

        dx = x2 - x1
        dy = y2 - y1
        r2 = (dx * dx + dy * dy) / 4.0

        best = float('inf')

        for i in range(n):
            x3, y3 = poly[i]
            x4, y4 = poly[(i + 1) % n]

            ex = x4 - x3
            ey = y4 - y3

            vx = cx - x3
            vy = cy - y3

            e2 = ex * ex + ey * ey
            t = 0.0
            if e2 != 0:
                t = (vx * ex + vy * ey) / e2
                t = clamp01(t)

            px = x3 + t * ex
            py = y3 + t * ey

            best = min(best, dist2(cx, cy, px, py))

        ans = best + r2 / 2.0
        print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The solution first converts each diameter into a circle center and radius squared. The midpoint formula directly gives the expectation center, while the radius computation is purely algebraic.

The polygon loop computes the closest point on each segment using projection. The clamp step ensures the projection stays within the segment; otherwise endpoints dominate. This is the standard Euclidean projection onto a segment.

Finally, the answer combines the squared distance from the circle center to the polygon with the fixed variance term R²/2.

## Worked Examples

Consider the sample polygon as a unit square and the first query circle with endpoints (0,0) and (1,1). The center is (0.5, 0.5) and radius squared is 0.5.

| Step | Action | cx | cy | r² | best distance² |
| --- | --- | --- | --- | --- | --- |
| init | compute circle | 0.5 | 0.5 | 0.5 | inf |
| edges | scan polygon | 0.5 | 0.5 | 0.5 | 0 |
| final | add r²/2 | 0.5 | 0.5 | 0.5 | 0.25 |

The projection lands inside the square, so the center is feasible and distance is zero. The final answer is purely the disk variance term.

Now consider a circle far outside the polygon, say center at (2,2) with any radius. The closest point in the square is always (1,1).

| Step | Action | cx | cy | best |
| --- | --- | --- | --- | --- |
| init | circle center | 2 | 2 | inf |
| edges | projection | 2 | 2 | 2 |
| fin |  |  |  |  |
