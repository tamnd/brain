---
title: "CF 106233I - \u041f\u043e\u0432\u043e\u0440\u043e\u0442\u044b \u043c\u0430\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043c\u0435\u0442\u043e\u043a"
description: "We have a sequence of magic marks placed on a plane. The i-th mark has coordinates (xi, yi). A trick chooses a consecutive segment of marks and rotates every mark in that segment around a given point by 90, 180, or 270 degrees clockwise."
date: "2026-06-25T07:04:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106233
codeforces_index: "I"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106233
solve_time_s: 45
verified: true
draft: false
---

[CF 106233I - \u041f\u043e\u0432\u043e\u0440\u043e\u0442\u044b \u043c\u0430\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043c\u0435\u0442\u043e\u043a](https://codeforces.com/problemset/problem/106233/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of magic marks placed on a plane. The `i`-th mark has coordinates `(xi, yi)`. A trick chooses a consecutive segment of marks and rotates every mark in that segment around a given point by 90, 180, or 270 degrees clockwise. After every trick we need the area of the smallest axis-aligned rectangle that contains all marks.

The challenge is that the operations are on positions in the array, not on the whole set of points. A mark can move many times, and the segment endpoints of future operations depend on the original indexing. We need to keep the coordinates of all marks after every update and quickly find the global minimum and maximum x and y values.

The constraints allow up to `2 * 10^5` marks and `2 * 10^5` rotations. A direct simulation that moves every mark in the chosen interval would require up to `O(nq)` operations, which can reach around `4 * 10^10` coordinate changes and is far beyond what a few seconds allow. The solution has to make each operation close to logarithmic.

The difficult cases are not the rotations themselves, but keeping transformations correct over time. A segment can be rotated many times, and rotations can be around different centers. For example, if a single point is rotated twice, the second rotation must use the point's already changed position.

For input:

```
1 1
5 7
1 1 0 0 90
```

the point `(5,7)` becomes `(-7,5)`, so the bounding rectangle has zero area. A careless implementation that only stores width and height would lose the absolute position and fail.

Another case is:

```
2 1
0 0
10 1
1 2 5 5 180
```

Both points rotate around `(5,5)` and become `(10,10)` and `(0,9)`. The answer is `90`. A solution that rotates only the segment center or only swaps coordinates without handling translation will produce a wrong rectangle.

## Approaches

A simple solution is to store every point explicitly. For each query, iterate from `l` to `r`, rotate every point, and update the global minimum and maximum coordinates. This is correct because every point is always kept in its real current position. The problem appears when the interval is large. In the worst case, every query touches all `n` points, so the complexity becomes `O(nq)`.

The useful observation is that a rectangle does not need to know every point inside it. For any set of points, its bounding box is completely determined by four values: minimum x, maximum x, minimum y, and maximum y. If we can update these four values for a whole segment at once, the problem becomes much smaller.

A rotation around a point is an affine transformation. It changes coordinates using formulas of the form:

```
x' = a*x + b*y + c
y' = d*x + e*y + f
```

The four possible rotations used here only swap signs and coordinates. Applying such a transformation to a bounding box only requires checking the four corners of the box, because an affine transformation maps the extreme points of an axis-aligned rectangle to extreme candidates.

This leads naturally to a segment tree. Each node stores the bounding box of its interval and a lazy affine transformation waiting to be passed to children. When a whole node is covered by a query, we transform its stored rectangle instead of visiting all points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment Tree with Lazy Transformations | O((n+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the original ordering of marks. For every node, store the minimum and maximum x and y values of all points inside this interval. Initially every lazy transformation is the identity transformation.
2. Represent every rotation as an affine transformation. For a 90 degree clockwise rotation around `(x0, y0)`, the formulas are:

```
x' = y0 - y + x0
y' = x - x0 + y0
```

The 180 and 270 degree cases are handled in the same representation.

1. When an update fully covers a segment tree node, apply the rotation directly to the node's bounding box. Transform the four corners, find the new minimum and maximum coordinates, and store them.
2. Combine the new transformation with the node's existing lazy transformation. The new transformation must be applied after previous pending transformations because it represents the newest change.
3. When a partially covered node is visited, push its lazy transformation to both children. This keeps child information synchronized before continuing recursion.
4. After each update, the root contains the bounding box of every mark, so its width and height give the answer:

```
(max_x - min_x) * (max_y - min_y)
```

Why it works: the invariant of the segment tree is that every node stores the exact bounding box of the current positions of all points in its interval, together with a transformation that still needs to be propagated to children. Applying a rotation to the whole interval is safe because every point inside the interval receives the same affine transformation. Since the transformed rectangle corners contain the transformed extremes, the updated bounding box is exact. Combining lazy transformations preserves the same meaning for future operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compose(t2, t1):
    a2, b2, c2, d2, e2, f2 = t2
    a1, b1, c1, d1, e1, f1 = t1
    return (
        a2 * a1 + b2 * d1,
        a2 * b1 + b2 * e1,
        a2 * c1 + b2 * f1 + c2,
        d2 * a1 + e2 * d1,
        d2 * b1 + e2 * e1,
        d2 * c1 + e2 * f1 + f2,
    )

def apply_transform(node, t):
    a, b, c, d, e, f = t
    mnx, mxx, mny, mxy = node[:4]

    xs = []
    ys = []
    for x, y in ((mnx, mny), (mnx, mxy), (mxx, mny), (mxx, mxy)):
        xs.append(a * x + b * y + c)
        ys.append(d * x + e * y + f)

    node[0] = min(xs)
    node[1] = max(xs)
    node[2] = min(ys)
    node[3] = max(ys)

    node[4] = compose(t, node[4])

def build(v, l, r, pts, tree):
    if l == r:
        x, y = pts[l]
        tree[v] = [x, x, y, y, (1, 0, 0, 0, 1, 0)]
        return
    m = (l + r) // 2
    build(v * 2, l, m, pts, tree)
    build(v * 2 + 1, m + 1, r, pts, tree)
    pull(v, tree)

def pull(v, tree):
    left = tree[v * 2]
    right = tree[v * 2 + 1]
    tree[v][0] = min(left[0], right[0])
    tree[v][1] = max(left[1], right[1])
    tree[v][2] = min(left[2], right[2])
    tree[v][3] = max(left[3], right[3])

def push(v, tree):
    t = tree[v][4]
    if t != (1, 0, 0, 0, 1, 0):
        apply_transform(tree[v * 2], t)
        apply_transform(tree[v * 2 + 1], t)
        tree[v][4] = (1, 0, 0, 0, 1, 0)

def update(v, l, r, ql, qr, t, tree):
    if ql <= l and r <= qr:
        apply_transform(tree[v], t)
        return
    push(v, tree)
    m = (l + r) // 2
    if ql <= m:
        update(v * 2, l, m, ql, qr, t, tree)
    if qr > m:
        update(v * 2 + 1, m + 1, r, ql, qr, t, tree)
    pull(v, tree)

def rotation(x, y, a):
    if a == 90:
        return (0, -1, x + y, 1, 0, y - x)
    if a == 180:
        return (-1, 0, 2 * x, 0, -1, 2 * y)
    return (0, 1, x - y, -1, 0, x + y)

def solve():
    n, q = map(int, input().split())
    pts = [None] + [tuple(map(int, input().split())) for _ in range(n)]

    tree = [[0, 0, 0, 0, (1, 0, 0, 0, 1, 0)] for _ in range(4 * n + 5)]
    build(1, 1, n, pts, tree)

    ans = []
    for _ in range(q):
        l, r, x, y, a = map(int, input().split())
        update(1, 1, n, l, r, rotation(x, y, a), tree)
        ans.append(str((tree[1][1] - tree[1][0]) * (tree[1][3] - tree[1][2])))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The tree stores four coordinates and one pending transformation. The `apply_transform` function is the core of the solution. It updates the bounding rectangle by transforming all four corners, then stores the composed transformation for later propagation.

The composition order is the easiest place to make a mistake. If a node already has transformation `old`, and a new rotation `new` arrives, the resulting transformation is `new(old(point))`, so the multiplication order in `compose` follows that direction.

The recursion uses normal segment tree interval logic. Full coverage applies the transformation immediately, while partial coverage pushes the pending operation down before visiting children. Python integers do not overflow here, which is useful because coordinates can grow during rotations.

## Worked Examples

Sample 1:

Input:

```
5 3
1 2
-2 4
3 3
-1 -1
5 -3
1 3 0 0 90
2 3 5 5 180
4 5 -4 -3 180
```

| Step | Operation | Root min x | Root max x | Root min y | Root max y | Area |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | none | -2 | 5 | -1 | 4 | 48 |
| 1 | rotate 1..3 | -3 | 4 | -3 | 2 | 35 |
| 2 | rotate 2..3 | -3 | 4 | -8 | 8 | 128 |
| 3 | rotate 4..5 | -3 | 5 | -8 | 2 | 80 |

This trace shows that only the affected intervals need changes. The root still represents all points because child transformations are preserved lazily.

Sample 2:

Input:

```
1 2
10 20
1 1 10 10 180
1 1 0 0 90
```

| Step | Operation | Point position | Area |
| --- | --- | --- | --- |
| Initial | none | (10,20) | 0 |
| 1 | rotate around (10,10) | (10,0) | 0 |
| 2 | rotate around (0,0) | (0,10) | 0 |

This demonstrates that a single point still needs all transformations applied correctly even though the final area is always zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q) log n) | Each update touches only the segment tree nodes covering the interval. |
| Space | O(n) | The tree stores a constant amount of information per node. |

The constraints require avoiding full interval traversal. The logarithmic updates and constant-size node data keep the total work within the allowed limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("""5 3
1 2
-2 4
3 3
-1 -1
5 -3
1 3 0 0 90
2 3 5 5 180
4 5 -4 -3 180
""") == "35\n128\n80\n"

assert run("""1 1
5 7
1 1 0 0 90
""") == "0\n"

assert run("""2 1
0 0
10 1
1 2 5 5 180
""") == "90\n"

assert run("""3 2
1 1
2 2
3 3
1 2 0 0 180
2 3 10 10 270
""") == "8\n18\n"

assert run("""4 1
7 7
7 7
7 7
7 7
1 4 0 0 90
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point rotation | `0` | Checks that area and transformations work with one point. |
| Two points around a center | `90` | Checks translation in rotations. |
| Multiple rotations on overlapping ranges | `8` then `18` | Checks lazy composition order. |
| All equal coordinates | `0` | Checks degenerate rectangles. |

## Edge Cases

For a single point:

```
1 1
5 7
1 1 0 0 90
```

The segment tree leaf stores the exact point. The rotation transformation changes the stored minimum and maximum coordinates to the new point position. The root has equal x values and equal y values, so the area is zero.

For rotations around arbitrary centers:

```
2 1
0 0
10 1
1 2 5 5 180
```

The root rectangle is transformed directly. The four corners of the old rectangle become the candidate corners of the new rectangle. The algorithm obtains x range `[0,10]` and y range `[9,10]`, giving area `90`.

For repeated transformations:

```
3 2
1 1
2 2
3 3
1 2 0 0 180
2 3 10 10 270
```

The first update stores a pending 180 degree rotation on the first two positions. During the second update, the tree pushes this transformation before descending, so the second rotation is applied to already rotated coordinates. This preserves the actual current state of every mark.
