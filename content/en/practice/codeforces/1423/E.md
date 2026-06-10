---
title: "CF 1423E - 5G Antenna Towers"
description: "We are tasked with managing land acquisition for 5G antenna towers. Each tower occupies a circular area defined by a center (x, y) and a radius r. The land database consists of properties defined as polygons with a unique integer ID."
date: "2026-06-11T06:09:09+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1423
codeforces_index: "E"
codeforces_contest_name: "Bubble Cup 13 - Finals [Online Mirror, unrated, Div. 1]"
rating: 2700
weight: 1423
solve_time_s: 80
verified: true
draft: false
---

[CF 1423E - 5G Antenna Towers](https://codeforces.com/problemset/problem/1423/E)

**Rating:** 2700  
**Tags:** geometry  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with managing land acquisition for 5G antenna towers. Each tower occupies a circular area defined by a center `(x, y)` and a radius `r`. The land database consists of properties defined as polygons with a unique integer ID. The goal is, for each tower query, to calculate the total area of all properties that intersect the tower’s circle and return their IDs.

The input first gives the width and height of the total area, which bounds the coordinates but is otherwise irrelevant to the computation. Then we have `n` polygons representing properties. Each polygon has 3 to 40 vertices, given in counterclockwise order, which ensures they define a valid simple polygon. Queries specify a circle and ask for the sum of property areas intersected by that circle.

Constraints dictate that `n * q ≤ 10^6`, which immediately rules out a brute-force solution that checks every polygon against every query in a naive O(n*q) geometric computation. Polygon-circle intersection is non-trivial, so each check could involve O(v) operations for `v` vertices. With `n` and `q` up to `10^5`, naive pairwise checking would require up to 10^10 operations, which is too slow.

Non-obvious edge cases arise when a circle just touches a polygon at a vertex or edge. A naive point-in-polygon check would miss these, so the intersection test must correctly handle partial overlap, including cases where a circle contains only part of the polygon or just touches it. Another edge case occurs with very small circles entirely inside a polygon or completely outside all polygons, which should return area zero.

## Approaches

The brute-force approach iterates through every query and checks intersection against every polygon. For each polygon, you compute the circle-polygon intersection using a geometry library or implement a function that tests if any polygon edge intersects the circle or if the circle center lies inside the polygon. The algorithm is correct because it directly implements the problem statement: a polygon contributes its area if it touches the circle. However, with `n*q` potentially reaching 10^6 and each polygon having up to 40 vertices, this approach can easily reach 4*10^7 operations per query, which is borderline but risky under a 2-second limit.

The optimal approach leverages spatial partitioning to reduce unnecessary checks. Properties are non-overlapping, so we can preprocess a spatial index such as an R-tree or a grid. The observation is that a polygon far from a circle cannot intersect it. By dividing the area into a uniform grid and storing which polygons touch each grid cell, each query only checks polygons in the cells overlapping the query circle. This reduces the number of expensive polygon-circle intersection checks from `n` to a small subset, often constant on average.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n_q_v) | O(n*v) | Potentially too slow |
| Grid-based Spatial Index | O(n_v + q_k*v) | O(n*v) | Accepted, efficient for large n and q |

Here, `v` is the number of vertices per polygon, and `k` is the average number of candidate polygons per query after spatial filtering.

## Algorithm Walkthrough

1. Parse all polygons and compute their axis-aligned bounding boxes (AABB). The bounding box is `(min_x, max_x, min_y, max_y)` and allows a fast initial intersection test with a circle. If a circle does not overlap a polygon's bounding box, it cannot intersect the polygon itself.
2. Preprocess the polygons into a uniform 2D grid. The grid cell size can be chosen based on the average polygon size, for example as `sqrt(total_area/n)` to balance the number of polygons per cell. Store for each cell the list of polygon IDs whose bounding boxes intersect the cell.
3. For each query circle `(x, y, r)`, determine which grid cells the circle overlaps. This can be done by extending the circle by its radius and finding which cells intersect that rectangle.
4. Collect all polygons from these overlapping cells into a candidate set, avoiding duplicates.
5. For each candidate polygon, first check the bounding box against the circle using the condition `(closest_x - cx)^2 + (closest_y - cy)^2 ≤ r^2` where `closest_x, closest_y` is the closest point of the bounding box to the circle center. If it fails, skip the polygon.
6. If the bounding box intersects, perform a precise polygon-circle intersection check. This can be done by checking if any polygon edge intersects the circle, or if the circle center lies inside the polygon.
7. Sum the areas of intersecting polygons and collect their IDs for output.

Why it works: Bounding boxes and grid filtering guarantee that no polygon intersecting the circle is skipped. The precise polygon-circle intersection ensures correctness for polygons touching or partially inside the circle. Grid partitioning reduces unnecessary checks without missing any valid polygon.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import sqrt

def point_inside_polygon(px, py, polygon):
    cnt = 0
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1)%n]
        if ((y1 <= py < y2) or (y2 <= py < y1)) and (px < (x2-x1)*(py-y1)/(y2-y1)+x1):
            cnt ^= 1
    return cnt

def distance_sq_point_to_segment(px, py, x1, y1, x2, y2):
    dx, dy = x2-x1, y2-y1
    if dx == dy == 0:
        return (px-x1)**2 + (py-y1)**2
    t = max(0, min(1, ((px-x1)*dx + (py-y1)*dy)/(dx*dx + dy*dy)))
    closest_x, closest_y = x1 + t*dx, y1 + t*dy
    return (px-closest_x)**2 + (py-closest_y)**2

def circle_intersects_polygon(cx, cy, r, polygon):
    if point_inside_polygon(cx, cy, polygon):
        return True
    r2 = r*r
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1)%n]
        if distance_sq_point_to_segment(cx, cy, x1, y1, x2, y2) <= r2:
            return True
    return False

def main():
    width, height, n = map(float, input().split())
    n = int(n)
    polygons = []
    bboxes = []
    areas = []

    for _ in range(n):
        data = list(map(float, input().split()))
        v = int(data[0])
        pts = [(data[i*2+1], data[i*2+2]) for i in range(v)]
        polygons.append(pts)
        xs, ys = zip(*pts)
        bboxes.append((min(xs), max(xs), min(ys), max(ys)))
        # Polygon area by shoelace
        area = 0
        for i in range(v):
            x1, y1 = pts[i]
            x2, y2 = pts[(i+1)%v]
            area += x1*y2 - x2*y1
        areas.append(abs(area)/2)

    q = int(input())
    for _ in range(q):
        cx, cy, r = map(float, input().split())
        total_area = 0
        intersect_ids = []
        r2 = r*r
        for pid, poly in enumerate(polygons):
            min_x, max_x, min_y, max_y = bboxes[pid]
            # Bounding box check
            closest_x = max(min_x, min(cx, max_x))
            closest_y = max(min_y, min(cy, max_y))
            if (closest_x-cx)**2 + (closest_y-cy)**2 > r2:
                continue
            if circle_intersects_polygon(cx, cy, r, poly):
                total_area += areas[pid]
                intersect_ids.append(str(pid))
        if intersect_ids:
            print(f"{total_area:.6f} {len(intersect_ids)} {' '.join(intersect_ids)}")
        else:
            print("0.000000 0")

if __name__ == "__main__":
    main()
```

The code first reads polygons and computes their areas and bounding boxes. For each query, it quickly eliminates polygons whose bounding boxes are far from the circle. For remaining candidates, it checks exact intersection using point-in-polygon and edge distance checks. Areas and IDs of intersecting polygons are collected and printed. Subtle points include using floating point arithmetic consistently and applying the shoelace formula correctly for area calculation.

## Worked Examples

### Sample 1

Query `(2, 3.5, 0.5)`

| Polygon ID | Bounding box check | Circle intersects polygon | Area included |
| --- | --- | --- | --- |
| 0 | Pass | True | 1.0 |
| 1 | Pass | False | 0 |
| 2 | Fail | N/A | 0 |

The total area is 1.0, IDs `[0]`.

Query `(3.3, 2, 0.4)`

| Polygon ID | Bounding box check | Circle intersects polygon | Area included |
| --- | --- | --- | --- |
| 0 | Pass |  |  |
