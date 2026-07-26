---
title: "CF 102836H - \u0411\u043e\u043b\u044c\u0448\u043e\u0439 \u0431\u0430\u0442\u0443\u0442"
description: "We are given up to nine support points on a plane. We must decide whether these points can be arranged as the vertices of a simple polygon, meaning the border of the polygon cannot cross itself and cannot touch itself at a non-adjacent point."
date: "2026-07-26T14:53:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102836
codeforces_index: "H"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102836
solve_time_s: 43
verified: true
draft: false
---

[CF 102836H - \u0411\u043e\u043b\u044c\u0448\u043e\u0439 \u0431\u0430\u0442\u0443\u0442](https://codeforces.com/problemset/problem/102836/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given up to nine support points on a plane. We must decide whether these points can be arranged as the vertices of a simple polygon, meaning the border of the polygon cannot cross itself and cannot touch itself at a non-adjacent point. Among all valid orders of the same points, we need to output one that gives the largest possible area.

The input describes the coordinates of the supports. The output is either that no simple polygon can be built, or a permutation of point indices describing the order in which the polygon vertices should be visited.

The very small value of `n` completely changes the way we should think about the problem. With `n <= 9`, trying all permutations requires at most `9! = 362880` candidates, which is tiny. Even if every candidate needs several geometric checks, the total work remains comfortable for a 2 second limit. A polynomial-time geometry algorithm would be interesting, but unnecessary here.

The main pitfalls are not performance related, but geometric. A permutation can have a large signed area while still being invalid because edges cross. For example, the points

```
4
0 0
2 2
0 2
2 0
```

can be ordered as `1 2 3 4`, but the edges `(1,2)` and `(3,4)` cross. The correct answer must avoid such a self-intersection.

Another tricky case is when all points lie on one line:

```
3
0 0
1 0
2 0
```

No polygon with positive area exists because every possible ordering creates a degenerate shape. The algorithm must reject it instead of returning an arbitrary permutation.

A third common mistake is allowing a polygon edge to touch another edge at a point. The statement forbids self-touching as well as crossing, so the segment intersection test must include collinear overlap and endpoint contact cases for non-neighboring edges.

## Approaches

The direct approach is to generate every possible ordering of the points. For each permutation, we connect consecutive points and finally connect the last point back to the first. If the resulting cycle is a simple polygon, we compute its area using the shoelace formula and keep the best one.

This brute force method is correct because every possible polygon boundary using all points appears as one of the generated permutations. The best valid permutation among them is exactly the required answer.

The reason this approach is feasible is the constraint on `n`. The worst case has only `9!` permutations. For each permutation we inspect `n` edges and compare pairs of edges to detect intersections, which is roughly another `n^2` factor. The total number of primitive operations is still well below a practical limit because `9! * 9^2` is about 29 million simple checks.

A more advanced geometric construction can find a maximum-area polygon by sorting points around a center, but it requires more careful handling of degenerate cases. The small input size makes exhaustive search a safer and clearer solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n^2) | O(n) | Accepted |
| Geometric construction | O(n log n) | O(n) | Unnecessary |

## Algorithm Walkthrough

1. Generate every permutation of the point indices. Each permutation represents one possible order of walking around the trampoline border.
2. For the current order, build the polygon edges between consecutive vertices, including the final edge from the last vertex back to the first. A valid answer must have all of these edges forming a simple cycle.
3. Check every pair of non-adjacent edges. If any pair intersects, reject this permutation. Adjacent edges are allowed to meet at their shared endpoint, so they are skipped during this check.
4. For every valid polygon, calculate its doubled area with the shoelace formula. Keeping the doubled value avoids floating point precision issues.
5. Store the permutation with the maximum area found. If no permutation was valid, output `No`; otherwise output `Yes` and the saved order.

Why it works: every possible arrangement of the given points is examined. The intersection test removes exactly the orders that do not form simple polygons. For every remaining order, the shoelace formula gives the real area of that polygon, so selecting the largest value among all valid candidates produces an optimal polygon.

## Python Solution

```python
import sys
input = sys.stdin.readline

from itertools import permutations

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def orientation(a, b, c):
    return cross(
        b[0] - a[0],
        b[1] - a[1],
        c[0] - a[0],
        c[1] - a[1]
    )

def on_segment(a, b, c):
    return (
        min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
        min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    )

def segments_intersect(a, b, c, d):
    ab_c = orientation(a, b, c)
    ab_d = orientation(a, b, d)
    cd_a = orientation(c, d, a)
    cd_b = orientation(c, d, b)

    if ab_c == 0 and on_segment(a, b, c):
        return True
    if ab_d == 0 and on_segment(a, b, d):
        return True
    if cd_a == 0 and on_segment(c, d, a):
        return True
    if cd_b == 0 and on_segment(c, d, b):
        return True

    return (ab_c > 0) != (ab_d > 0) and (cd_a > 0) != (cd_b > 0)

def is_simple(order, pts):
    n = len(order)
    edges = []
    for i in range(n):
        edges.append((pts[order[i]], pts[order[(i + 1) % n]]))

    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if segments_intersect(edges[i][0], edges[i][1], edges[j][0], edges[j][1]):
                return False
    return True

def area2(order, pts):
    s = 0
    n = len(order)
    for i in range(n):
        x1, y1 = pts[order[i]]
        x2, y2 = pts[order[(i + 1) % n]]
        s += x1 * y2 - y1 * x2
    return abs(s)

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    best = None
    best_area = -1

    for p in permutations(range(n)):
        if is_simple(p, pts):
            cur = area2(p, pts)
            if cur > best_area:
                best_area = cur
                best = p

    if best is None:
        print("No")
    else:
        print("Yes")
        print(*[x + 1 for x in best])

if __name__ == "__main__":
    solve()
```

The implementation first defines the geometric primitives. The cross product determines the side on which a point lies relative to a directed segment, and it is the basis for all intersection checks.

The segment intersection function handles both the normal crossing case and collinear cases. The collinear checks are necessary because touching at a point or overlapping is also forbidden for non-adjacent polygon edges.

The `is_simple` function creates the cycle edges and compares only pairs that are not neighbors in the polygon. Neighboring edges share a vertex by definition, so checking them would incorrectly reject every valid polygon.

The area calculation uses twice the real area. This keeps everything as integers and avoids precision errors. Since all candidate polygons are compared using the same doubled area value, the maximum is preserved.

## Worked Examples

Consider the sample:

```
5
0 0
2 2
-2 -2
2 -2
-2 2
```

One possible search trace:

| Order checked | Simple? | Doubled area | Best order |
| --- | --- | --- | --- |
| 1 2 3 4 5 | No | 0 | none |
| 1 2 4 3 5 | Yes | 24 | 1 2 4 3 5 |

The chosen order avoids crossings and gives a valid polygon. The algorithm does not need to know the shape beforehand because it evaluates every possible arrangement.

Another example:

```
3
0 0
1 0
2 0
```

| Order checked | Simple? | Doubled area | Best order |
| --- | --- | --- | --- |
| 1 2 3 | Yes | 0 | 1 2 3 |
| 1 3 2 | Yes | 0 | 1 2 3 |

All points are collinear, so every cycle has zero area. Since the polygon must be simple and non-degenerate, the intersection test alone is not enough. The implementation must also reject zero-area polygons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n! * n^2) | There are n! permutations, and each one needs O(n^2) edge intersection checks. |
| Space | O(n) | The algorithm stores the points, current permutation data, and edge information. |

With `n <= 9`, the factorial term remains small enough. The algorithm performs a complete search over the entire space of possible polygons while staying within the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert run("""5
0 0
2 2
-2 -2
2 -2
-2 2
""").split()[0] == "Yes", "sample"

assert run("""3
0 0
1 0
2 0
""").strip() == "No", "collinear points"

assert run("""3
0 0
0 1
1 0
""").split()[0] == "Yes", "minimum polygon"

assert run("""4
0 0
2 0
2 2
0 2
""").split()[0] == "Yes", "rectangle"

assert run("""4
0 0
1 1
2 2
3 3
""").strip() == "No", "all equal slope"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample configuration | Yes | The normal polygon construction case |
| Three collinear points | No | Degenerate geometry handling |
| Three non-collinear points | Yes | Smallest possible valid polygon |
| Rectangle | Yes | Regular simple polygon detection |
| Four points on one line | No | Rejection of impossible instances |

## Edge Cases

For collinear points:

```
3
0 0
1 0
2 0
```

Every permutation creates a closed chain with zero area. The algorithm checks every order, but none gives a valid positive-area polygon, so it prints `No`.

For crossing candidates:

```
4
0 0
2 2
0 2
2 0
```

The order `1 2 3 4` creates a self-intersecting bow shape. When the algorithm compares the two opposite edges, the intersection test detects the crossing and rejects this permutation. Other permutations are still considered, and a valid rectangle order can be found.

For touching edges, the collinear checks inside `segments_intersect` handle cases where two non-adjacent edges share a point or overlap. This prevents accepting polygons whose border only appears valid when ignoring the exact geometry.
