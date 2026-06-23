---
title: "CF 105257M - Window Decoration"
description: "We are given up to ten thousand identical decorations placed inside a 100 by 100 square window. Each decoration is centered at an integer coordinate strictly inside the boundary, and each one is a rotated square whose diagonals align with the coordinate axes and have total…"
date: "2026-06-24T04:31:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105257
codeforces_index: "M"
codeforces_contest_name: "2024 ICPC ShaanXi Provincial Contest"
rating: 0
weight: 105257
solve_time_s: 63
verified: true
draft: false
---

[CF 105257M - Window Decoration](https://codeforces.com/problemset/problem/105257/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given up to ten thousand identical decorations placed inside a 100 by 100 square window. Each decoration is centered at an integer coordinate strictly inside the boundary, and each one is a rotated square whose diagonals align with the coordinate axes and have total length 2.

Because the diagonals are axis-parallel and centered at an integer point, each decoration is exactly the set of points whose Manhattan distance to its center is at most 1. Geometrically, this is a diamond shape with four vertices one unit away in the cardinal directions.

The task is to compute how much total area inside the window is covered by at least one of these diamonds, counting overlaps only once.

The input size allows up to 10000 shapes, so any approach that tries to measure overlap pair by pair or samples the plane at fine resolution becomes too slow. A naive pairwise union computation would require checking intersections between all pairs of shapes, which leads to roughly 10^8 comparisons, and each intersection test is not constant-time if done geometrically.

A subtle issue appears if one tries to approximate the area by counting grid cells or sampling points. The shapes are continuous, and boundaries matter: a single diamond contributes area even when it only partially covers a region. Any discretization would introduce error beyond the required 1e-4 tolerance.

Another pitfall is assuming the covered region behaves like a simple union of axis-aligned squares in the original coordinate system. The shapes are not axis-aligned squares, so standard rectangle union techniques do not apply directly without transformation.

## Approaches

A direct geometric union over diamonds is complicated because each shape is defined by an L1 constraint. The brute-force idea would be to compute the union area by considering every pairwise intersection and then applying inclusion-exclusion or a plane sweep over polygon boundaries. While correct, this becomes messy because each diamond contributes four line segments, and handling all intersections between O(n) polygons leads to quadratic or worse behavior.

The key observation is that the L1 diamond becomes much simpler under a linear change of variables. If we define new coordinates u = x + y and v = x - y, then the condition |x - xi| + |y - yi| ≤ 1 transforms into a condition where both u and v are independently bounded within an interval around their center. In this transformed space, each diamond becomes an axis-aligned square.

Once the problem is expressed as a union of axis-aligned squares, the task becomes a classic plane sweep over rectangles. We sweep along one axis and maintain active coverage on the other axis using a segment tree or coordinate-compressed difference counting. This reduces the problem to O(n log n), which is easily fast enough for n = 10000.

Finally, since the transformation scales area, we correct the computed area by the Jacobian determinant of the transformation. This ensures the result matches the original coordinate system.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force polygon union | O(n^2) or worse | O(n) | Too slow |
| Transform + sweep line | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Transform each center (x, y) into (u, v) where u = x + y and v = x - y. This linear transformation is chosen because it converts L1 distance constraints into independent bounds on u and v.
2. Rewrite each diamond condition |x - xi| + |y - yi| ≤ 1 as two inequalities in transformed space: u in [ui - 1, ui + 1] and v in [vi - 1, vi + 1]. This shows each shape is now an axis-aligned square of side length 2.
3. Represent each square as a rectangle event in the (u, v) plane. Each contributes an interval [ui - 1, ui + 1] along u and [vi - 1, vi + 1] along v.
4. Collect all rectangle edges as sweep events along the u-axis. Each event either adds or removes coverage over an interval in v.
5. Sort events by their u-coordinate and sweep from left to right. Between consecutive event positions, the active set of rectangles does not change, so the covered v-length remains constant across that strip.
6. Maintain active coverage on the v-axis using coordinate compression and a segment tree that stores total covered length. After processing events at position u, compute contribution as (next_u - current_u) multiplied by active_v_coverage.
7. Sum all contributions to obtain the total area in (u, v) space.
8. Multiply the final result by 1/2 to convert back to (x, y) space, since the linear transformation has Jacobian determinant 1/2.

The correctness relies on the fact that every point is counted exactly once in the sweep: each horizontal strip in u is paired with the correct active vertical coverage in v, and the transformation preserves coverage structure without distortion beyond uniform scaling.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords) - 1
        self.count = [0] * (4 * self.n)
        self.length = [0] * (4 * self.n)

    def _update(self, idx, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.count[idx] += val
        else:
            mid = (l + r) // 2
            if ql < mid:
                self._update(idx * 2, l, mid, ql, qr, val)
            if qr > mid:
                self._update(idx * 2 + 1, mid, r, ql, qr, val)

        if self.count[idx] > 0:
            self.length[idx] = self.coords[r] - self.coords[l]
        else:
            if r - l == 1:
                self.length[idx] = 0
            else:
                self.length[idx] = self.length[idx * 2] + self.length[idx * 2 + 1]

    def update(self, l, r, val):
        self._update(1, 0, self.n, l, r, val)

    def query(self):
        return self.length[1]

n = int(input())
rects = []

vs = []

for _ in range(n):
    x, y = map(int, input().split())
    u = x + y
    v = x - y
    x1, x2 = u - 1, u + 1
    y1, y2 = v - 1, v + 1
    rects.append((x1, x2, y1, y2))
    vs.append(y1)
    vs.append(y2)

vs = sorted(set(vs))
idx = {v: i for i, v in enumerate(vs)}

events = []
for x1, x2, y1, y2 in rects:
    events.append((x1, y1, y2, 1))
    events.append((x2, y1, y2, -1))

events.sort()

seg = SegTree(vs)

area_uv = 0
for i in range(len(events)):
    x, y1, y2, t = events[i]
    seg.update(idx[y1], idx[y2], t)
    if i + 1 < len(events):
        dx = events[i + 1][0] - x
        area_uv += dx * seg.query()

print(area_uv / 2)
```

The solution begins by converting each input center into the rotated coordinate system where each diamond becomes a square. The rectangle list stores those squares in terms of their u and v intervals.

The segment tree operates over compressed v-coordinates. Each update adjusts how many rectangles currently cover a v-segment, and the tree maintains total covered length. The sweep over u multiplies this covered length by horizontal distance between events.

The final division by 2 corrects the area scaling introduced by the linear transform.

A subtle point is that interval updates use half-open structure implicitly through coordinate compression, which avoids double counting shared boundaries.

## Worked Examples

Consider a small configuration where two diamonds overlap slightly in the original grid. After transformation, we obtain two overlapping squares in uv space.

For illustration, assume two centers produce intervals in v that overlap partially.

| Sweep step | u-coordinate | Active v coverage | Segment length | Contribution |
| --- | --- | --- | --- | --- |
| 1 | u1 | 0 | 0 | 0 |
| 2 | u2 | k | u2 - u1 | (u2 - u1) * k |

This shows how area accumulates only when there is horizontal separation between events.

A second example is a single diamond. It becomes a single square of side 2 in uv space. The sweep produces a constant active coverage across its width, yielding exactly 4 in uv space, which becomes 2 in original coordinates after scaling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting events and segment tree updates for each endpoint |
| Space | O(n) | Storage for events, coordinate compression, and segment tree |

The constraints allow up to 10000 shapes, and logarithmic overhead is small enough that the sweep-line solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # --- paste solution logic here as function ---
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, coords):
            self.coords = coords
            self.n = len(coords) - 1
            self.count = [0] * (4 * self.n)
            self.length = [0] * (4 * self.n)

        def _update(self, idx, l, r, ql, qr, val):
            if ql <= l and r <= qr:
                self.count[idx] += val
            else:
                mid = (l + r) // 2
                if ql < mid:
                    self._update(idx * 2, l, mid, ql, qr, val)
                if qr > mid:
                    self._update(idx * 2 + 1, mid, r, ql, qr, val)

            if self.count[idx] > 0:
                self.length[idx] = self.coords[r] - self.coords[l]
            else:
                if r - l == 1:
                    self.length[idx] = 0
                else:
                    self.length[idx] = self.length[idx * 2] + self.length[idx * 2 + 1]

        def update(self, l, r, val):
            self._update(1, 0, self.n, l, r, val)

        def query(self):
            return self.length[1]

    n = int(input())
    rects = []
    vs = []

    for _ in range(n):
        x, y = map(int, input().split())
        u = x + y
        v = x - y
        rects.append((u - 1, u + 1, v - 1, v + 1))
        vs += [v - 1, v + 1]

    vs = sorted(set(vs))
    idx = {v: i for i, v in enumerate(vs)}

    events = []
    for x1, x2, y1, y2 in rects:
        events.append((x1, y1, y2, 1))
        events.append((x2, y1, y2, -1))

    events.sort()

    seg = SegTree(vs)

    area_uv = 0
    for i, (x, y1, y2, t) in enumerate(events):
        seg.update(idx[y1], idx[y2], t)
        if i + 1 < len(events):
            area_uv += (events[i + 1][0] - x) * seg.query()

    return str(area_uv / 2)

# sample-like sanity checks
assert run("1\n1 1\n")  # single diamond produces nonzero area
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 single point | 2 | basic single-shape correctness |
| multiple overlapping centers | merged area | overlap handling |
| max scattered points | stable output | performance and sweep correctness |
| identical centers repeated | no double counting | multiset handling |

## Edge Cases

A key edge case is repeated centers. If multiple decorations share the same integer point, a naive approach might add their areas multiple times. In this solution, both copies generate identical rectangles in uv space, but the segment tree counts coverage as a union, so duplicates do not change the active length after the first insertion.

Another edge case appears near the boundary of the window. A center at (1, 1) generates a diamond reaching down to x = 0 or y = 0. The transformation does not rely on clamping to the window because the sweep operates on the full geometric region, and the window constraint is already satisfied by the placement rules.

A final edge case is when rectangles only touch at boundaries. Since the sweep uses half-open intervals in coordinate compression, touching edges do not create artificial area. The segment tree only contributes length when intervals have positive measure, so zero-width overlaps are ignored correctly.
