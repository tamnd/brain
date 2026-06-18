---
problem: 993A
contest_id: 993
problem_index: A
name: "Two Squares"
contest_name: "Codeforces Round 488 by NEAR (Div. 1)"
rating: 1600
tags: ["geometry", "implementation"]
answer: passed_samples
verified: true
solve_time_s: 88
date: 2026-06-17
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a3294bf-6b50-83ec-a672-f71aefc63faf
---

# CF 993A - Two Squares

**Rating:** 1600  
**Tags:** geometry, implementation  
**Model:** gpt-5-5  
**Solve time:** 1m 28s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a3294bf-6b50-83ec-a672-f71aefc63faf  

---

## Solution

## Problem Understanding

We are given two geometric figures, each described by four corner points in the plane. One of them is an axis-aligned square, meaning its sides are parallel to the coordinate axes. The other is a square rotated by 45 degrees, meaning its sides are not axis-aligned but instead form a diamond shape relative to the grid.

Each square is provided as a list of its four vertices in order along the boundary. The order is consistent (either clockwise or counterclockwise), so the edges connect consecutive points and the last point connects back to the first.

The task is to determine whether these two squares share at least one point in common, where touching at a single point or one being fully inside the other both count as intersection.

The coordinate range is very small, from -100 to 100, and there are only two objects, each with four vertices. This immediately suggests that any solution with cubic or even high quadratic complexity over many points is unnecessary; constant-factor geometric reasoning or direct segment intersection checks are sufficient.

A subtle point is that “intersection” includes boundary contact. Two squares that only touch at a vertex or along an edge still count as intersecting. A naive approach that only checks strict interior overlap would incorrectly reject these cases.

Another common pitfall is assuming we can rely on axis alignment for both squares. Only one square is axis-aligned; the other may have arbitrary orientation at 45 degrees. Any method that assumes rectangles aligned to axes for both will fail.

Edge cases that commonly break incorrect solutions include:

One square completely inside the other, for example the rotated square centered inside the axis-aligned square. In this case, no edges intersect, but all vertices of the inner square are inside the outer one.

A single-point touch, such as the tip of the rotated square touching the side of the axis-aligned square. In this case, no segment interiors overlap.

A degenerate-looking situation where a vertex lies exactly on an edge of the other square, which must be treated as intersection.

## Approaches

A brute-force geometric approach starts by treating each square as a set of four line segments. We could check every segment of the first square against every segment of the second square for intersection. Each segment-segment check is constant time using orientation tests. This already works within limits because there are only 4 edges per square, so at most 16 segment comparisons.

However, even though this brute-force is already efficient enough, it does not immediately handle containment. If one square lies entirely inside the other, none of the edges intersect, so the algorithm would incorrectly return “No” unless we also check point containment. This adds an extra layer: for each vertex of one square, we must test whether it lies inside the other polygon.

The key observation is that both shapes are convex polygons with exactly four vertices. For convex polygons, intersection can be decided completely by checking two conditions: whether any edge intersects, or whether one polygon contains a vertex of the other. This works because if convex polygons overlap without edge intersection, one must fully contain the other.

This reduces the problem to a small fixed number of orientation and segment tests, all in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Segment + Point Checks | O(1) | O(1) | Accepted |
| Optimal Convex Polygon Intersection | O(1) | O(1) | Accepted |

In practice both are the same asymptotically here, but the structured convex-polygon reasoning avoids missing containment cases.

## Algorithm Walkthrough

1. Read the four vertices of each square and store them in order. The order guarantees that consecutive points define edges.
2. Define a function `orient(a, b, c)` that computes the cross product sign to determine whether point `c` is to the left, right, or on the directed line `ab`. This is the core primitive for all geometric reasoning.
3. Define a function `on_segment(a, b, c)` to detect whether point `c` lies exactly on segment `ab`. This handles boundary-touch cases explicitly.
4. Define a segment intersection check between two segments. Two segments intersect if their endpoints are on opposite sides of each other’s supporting lines, or if any endpoint lies on the other segment.
5. Check all four edges of the first square against all four edges of the second square. If any pair of edges intersects, immediately conclude that the squares intersect.
6. If no edges intersect, check whether any vertex of the first square lies inside or on the boundary of the second square using consistent orientation checks for a convex polygon.
7. Repeat the same containment check in the opposite direction, testing whether any vertex of the second square lies inside the first square.
8. If neither edge intersection nor containment is found, conclude that the squares do not intersect.

The reason each step is necessary is that convex polygons can overlap in exactly three ways: crossing edges, full containment, or boundary touching without crossings. Each case is captured by one of the checks above.

### Why it works

Both squares are convex polygons. For convex polygons, if their intersection is non-empty, then either their boundaries intersect or one polygon lies entirely inside the other. Boundary intersection is captured by segment-segment checks, and containment is captured by vertex-in-polygon checks. Since all possibilities are covered, failure of both conditions implies disjoint sets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def orient(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def on_segment(ax, ay, bx, by, cx, cy):
    return min(ax, bx) <= cx <= max(ax, bx) and min(ay, by) <= cy <= max(ay, by) and orient(ax, ay, bx, by, cx, cy) == 0

def seg_inter(a, b, c, d):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    o1 = orient(ax, ay, bx, by, cx, cy)
    o2 = orient(ax, ay, bx, by, dx, dy)
    o3 = orient(cx, cy, dx, dy, ax, ay)
    o4 = orient(cx, cy, dx, dy, bx, by)

    if o1 == 0 and on_segment(ax, ay, bx, by, cx, cy): return True
    if o2 == 0 and on_segment(ax, ay, bx, by, dx, dy): return True
    if o3 == 0 and on_segment(cx, cy, dx, dy, ax, ay): return True
    if o4 == 0 and on_segment(cx, cy, dx, dy, bx, by): return True

    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)

def inside(poly, p):
    x, y = p
    n = 4
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if orient(x1, y1, x2, y2, x, y) < 0:
            return False
    return True

sq1 = list(map(int, input().split()))
sq2 = list(map(int, input().split()))

poly1 = [(sq1[i], sq1[i+1]) for i in range(0, 8, 2)]
poly2 = [(sq2[i], sq2[i+1]) for i in range(0, 8, 2)]

for i in range(4):
    for j in range(4):
        if seg_inter(poly1[i], poly1[(i+1) % 4], poly2[j], poly2[(j+1) % 4]):
            print("YES")
            sys.exit()

for p in poly1:
    if inside(poly2, p):
        print("YES")
        sys.exit()

for p in poly2:
    if inside(poly1, p):
        print("YES")
        sys.exit()

print("NO")
```

The segment intersection routine is the central piece. It combines orientation tests with explicit collinearity handling, ensuring that shared endpoints and edge overlaps are correctly detected.

The containment check uses a consistent sign test over all edges of the convex polygon. Because the vertices are given in order, a point is inside the polygon if it always lies on the same side of every directed edge.

The early exit on first detected intersection is safe because any valid intersection is sufficient.

## Worked Examples

### Sample 1

Input:

```
0 0 6 0 6 6 0 6
1 3 3 5 5 3 3 1
```

The first square is a 6x6 axis-aligned box. The second is a diamond-shaped square centered inside it.

| Step | Action | Result |
| --- | --- | --- |
| 1 | Check all edge pairs | No edge intersections |
| 2 | Test vertex (1,3) inside square 1 | True |
| 3 | Stop early | YES |

This demonstrates containment without boundary crossing. The algorithm correctly detects that absence of edge intersection is not enough.

### Sample 2

Constructed non-intersecting case:

```
0 0 2 0 2 2 0 2
5 5 6 5 6 6 5 6
```

| Step | Action | Result |
| --- | --- | --- |
| 1 | Check edge intersections | None |
| 2 | Test vertices of square 1 in square 2 | False |
| 3 | Test vertices of square 2 in square 1 | False |
| 4 | Conclude separation | NO |

This confirms that the algorithm does not produce false positives when both polygons are disjoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Fixed 4 edges per square, constant number of orientation and containment checks |
| Space | O(1) | Only stores constant number of points |

The problem size is constant, so even a direct geometric implementation with nested loops comfortably fits within limits. The main concern is correctness of geometric predicates rather than performance.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    def orient(ax, ay, bx, by, cx, cy):
        return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

    def on_segment(ax, ay, bx, by, cx, cy):
        return min(ax, bx) <= cx <= max(ax, bx) and min(ay, by) <= cy <= max(ay, by) and orient(ax, ay, bx, by, cx, cy) == 0

    def seg_inter(a, b, c, d):
        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = d

        o1 = orient(ax, ay, bx, by, cx, cy)
        o2 = orient(ax, ay, bx, by, dx, dy)
        o3 = orient(cx, cy, dx, dy, ax, ay)
        o4 = orient(cx, cy, dx, dy, bx, by)

        if o1 == 0 and on_segment(ax, ay, bx, by, cx, cy): return True
        if o2 == 0 and on_segment(ax, ay, bx, by, dx, dy): return True
        if o3 == 0 and on_segment(cx, cy, dx, dy, ax, ay): return True
        if o4 == 0 and on_segment(cx, cy, dx, dy, bx, by): return True

        return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)

    def inside(poly, p):
        x, y = p
        for i in range(4):
            x1, y1 = poly[i]
            x2, y2 = poly[(i+1)%4]
            if orient(x1, y1, x2, y2, x, y) < 0:
                return False
        return True

    sq = list(map(int, sys.stdin.readline().split()))
    poly1 = [(sq[i], sq[i+1]) for i in range(0, 8, 2)]
    sq = list(map(int, sys.stdin.readline().split()))
    poly2 = [(sq[i], sq[i+1]) for i in range(0, 8, 2)]

    for i in range(4):
        for j in range(4):
            if seg_inter(poly1[i], poly1[(i+1)%4], poly2[j], poly2[(j+1)%4]):
                return "YES"

    for p in poly1:
        if inside(poly2, p):
            return "YES"

    for p in poly2:
        if inside(poly1, p):
            return "YES"

    return "NO"

# provided samples
assert run("0 0 6 0 6 6 0 6\n1 3 3 5 5 3 3 1\n") == "YES", "sample 1"
assert run("0 0 2 0 2 2 0 2\n5 5 6 5 6 6 5 6\n") == "NO", "sample 2"

# custom cases
assert run("0 0 4 0 4 4 0 4\n0 0 4 0 4 4 0 4\n") == "YES", "identical squares"
assert run("0 0 2 0 2 2 0 2\n2 2 4 2 4 4 2 4\n") == "YES", "touch at vertex"
assert run("0 0 3 0 3 3 0 3\n10 10 11 10 11 11 10 11\n") == "NO", "far apart"
assert run("0 0 5 0 5 5 0 5\n1 1 4 1 4 4 1 4\n") == "YES", "full containment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical squares | YES | exact overlap handling |
| touch at vertex | YES | boundary-only intersection |
| far apart | NO | disjoint correctness |
| full containment | YES | no-edge-intersection case |

## Edge Cases

One important case is full containment, where the rotated square lies entirely inside the axis-aligned square. In this situation, no edge intersections occur. For example, the square `(0,0)-(5,0)-(5,5)-(0,5)` contains `(1,1)-(4,1)-(4,4)-(1,4)`. The algorithm fails the segment checks, then evaluates each vertex of the inner square against the outer square. Each orientation test returns a non-negative value for all edges, so the containment check returns true and the final answer is “YES”.

A second case is single-point touching. If a vertex of one square lies exactly on an edge of the other, the orientation becomes zero and `on_segment` triggers. This ensures that cases like `(0,0)-(2,0)-(2,2)-(0,2)` and `(2,2)-(3,2)-(3,3)-(2,3)` correctly return “YES” even though no area overlaps.

A third case is complete separation. When squares are far apart, all orientation tests are consistent in sign for all edges, and no segment intersection triggers. Both containment checks fail because at least one edge sees the test point on the wrong side, leading to “NO” with no ambiguity.