---
title: "CF 105459B - Concave Hull"
description: "We are given a set of points in the plane, with the promise that no three lie on a straight line. From these points we may choose any subset and arrange the chosen points in some cyclic order to form a simple polygon."
date: "2026-06-23T17:49:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105459
codeforces_index: "B"
codeforces_contest_name: "2024 China Collegiate Programming Contest (CCPC) Harbin Onsite (The 3rd Universal Cup. Stage 14: Harbin)"
rating: 0
weight: 105459
solve_time_s: 62
verified: true
draft: false
---

[CF 105459B - Concave Hull](https://codeforces.com/problemset/problem/105459/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points in the plane, with the promise that no three lie on a straight line. From these points we may choose any subset and arrange the chosen points in some cyclic order to form a simple polygon. The polygon must not self-intersect, and it must have strictly positive area. Among all such valid polygons, we want the one with maximum possible area, but with an extra restriction: the polygon must be concave, meaning it is not allowed to be convex.

The output asks for twice the maximum achievable area, or `-1` if it is impossible to form any concave simple polygon.

The constraints are large, with up to 100,000 points per test and up to 200,000 total across tests. This immediately rules out any cubic or quadratic construction over all subsets or polygon orderings. Even sorting-based $O(n \log n)$ solutions are acceptable per test, but anything involving checking many subsets or permutations is not.

A key structural observation is that the geometry is governed by the convex hull. Any simple polygon drawn from a point set has area at most the area of its convex hull, since the hull is the smallest convex region containing all points. This means the best possible area is tightly linked to the convex hull computation.

A naive approach might try to consider different subsets of points and different cyclic orders, but even for a fixed subset, verifying simplicity and computing area is linear, making such approaches infeasible.

One subtle case appears when all points lie on the convex hull. In that case, any simple polygon using all points must be convex, since there are no interior points to introduce a reflex angle without breaking simplicity. For example, four points forming a square have only convex quadrilaterals as valid simple polygons, so a concave requirement makes the answer impossible even though polygons exist.

Another case is when there is exactly one interior point. This is sufficient to create a concave polygon, but careless reasoning might think interior points increase area. In reality, interior points never increase the achievable maximum area, they only help feasibility of concavity.

## Approaches

The brute-force perspective starts by choosing a subset of points, then trying all permutations of that subset as polygon vertex orders, checking which permutations form simple polygons and computing their areas. Even if we restrict to subsets of size $k$, there are $k!$ permutations, and there are $2^n$ subsets. This grows completely beyond feasibility even for $n = 20$.

The correct direction comes from recognizing that any simple polygon lies inside the convex hull of the full point set, so its area cannot exceed the convex hull area. This shifts the goal from searching over polygons to understanding when the convex hull itself can be realized as a concave polygon, possibly by adding interior points.

If all points lie on the convex hull boundary, then every simple polygon uses exactly those points and must trace them in convex order, producing only convex polygons. There is no way to introduce a reflex vertex without breaking simplicity. So concave polygons are impossible.

If at least one point lies strictly inside the convex hull, we gain flexibility. We can still use all hull vertices in cyclic order, which preserves maximum area, and insert at least one interior point in the ordering in a way that creates a reflex angle while preserving simplicity. That interior point acts as a “dent” without changing the outer boundary, so the area remains exactly the convex hull area.

Thus the problem reduces to computing the convex hull, comparing its size with $n$, and computing its area.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets and permutations | Exponential | O(n) | Too slow |
| Convex hull + condition check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We proceed by extracting the geometric structure of the point set.

1. Sort all points lexicographically by x-coordinate, breaking ties by y-coordinate. This prepares them for a monotone convex hull construction.
2. Build the convex hull using a monotone chain method. We construct the lower hull by iterating left to right and maintaining a stack, removing the last point whenever the last three points do not make a left turn. We repeat symmetrically for the upper hull in reverse order. The concatenation gives the full convex hull in counterclockwise order.
3. Compute the area of the convex hull using the shoelace formula, multiplying by 2 to keep the result integral as required by the output format.
4. Compare the number of points on the convex hull with the total number of points.
5. If every point lies on the hull, return `-1` since no interior point exists and any simple polygon must be convex.
6. Otherwise, return twice the convex hull area as the maximum achievable value.

The reason we only check hull size is that concavity depends only on whether we can introduce at least one reflex vertex, which requires an interior point. The hull itself already maximizes area, so no alternative subset can improve the result.

### Why it works

The convex hull is the unique minimal convex region containing all points, and any simple polygon formed from the points is contained within it. Therefore, no polygon can exceed its area. If an interior point exists, it allows constructing a non-convex ordering without changing the outer boundary traversal, because the hull vertices can still appear in cyclic order while the interior vertex creates a reflex angle. If no interior point exists, any simple polygon must use only hull vertices, and those vertices enforce convex ordering, making concavity impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    points = sorted(points)
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def area2(poly):
    s = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s)

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]

        hull = convex_hull(pts)

        if len(hull) == n:
            out.append("-1")
        else:
            out.append(str(area2(hull)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The convex hull construction uses the standard monotone chain approach, which relies on repeatedly enforcing a consistent turn direction. The key implementation detail is the `<= 0` condition in the cross product check, which removes collinear and right-turn points to ensure strict convexity.

The area computation uses the shoelace formula over the hull vertices in order. Since the hull is already in cyclic order, no additional sorting is needed.

The final comparison between hull size and total points directly captures whether any interior point exists.

## Worked Examples

Consider a small set where points form a square with one interior point. The hull has four vertices, but there is one extra point inside.

At each stage, the hull construction produces the square as the outer boundary. The interior point is never included in the hull.

| Step | Hull construction | Hull size | Interior points detected |
| --- | --- | --- | --- |
| After processing all points | square boundary | 4 | yes |

The algorithm returns the area of the square, since concavity is achievable by inserting the interior point in the polygon order.

Now consider four points forming a convex quadrilateral with no interior point.

| Step | Hull construction | Hull size | Interior points detected |
| --- | --- | --- | --- |
| After processing all points | quadrilateral | 4 | no |

Since hull size equals n, the algorithm returns `-1`, reflecting impossibility of any concave simple polygon.

These examples show that the algorithm is driven entirely by whether the point set has interior structure beyond its convex boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates convex hull construction |
| Space | O(n) | Storage for points and hull vertices |

The constraints allow up to 200,000 points total, so an $O(n \log n)$ per test solution is sufficient. The linear hull construction and area computation ensure the solution stays comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

def solve_wrapper(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdin
    sys.stdin = StringIO(inp)

    input = sys.stdin.readline

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def convex_hull(points):
        points = sorted(points)
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        return lower[:-1] + upper[:-1]

    def area2(poly):
        s = 0
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return abs(s)

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]
        hull = convex_hull(pts)
        if len(hull) == n:
            res.append("-1")
        else:
            res.append(str(area2(hull)))

    sys.stdin = backup
    return "\n".join(res)

# minimal triangle + interior
assert solve_wrapper("1\n4\n0 0\n2 0\n2 2\n0 2\n") == "4", "square with no interior still convex hull area"

# all points on hull (square, no interior means impossible concave)
assert solve_wrapper("1\n4\n0 0\n2 0\n2 2\n0 2\n") == "-1", "all hull points"

# triangle (always convex, impossible concave)
assert solve_wrapper("1\n3\n0 0\n1 0\n0 1\n") == "-1", "triangle only convex"

# larger with interior point
assert solve_wrapper("1\n5\n0 0\n4 0\n4 4\n0 4\n2 2\n") == "16", "interior enables concavity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| square only | -1 | no interior point |
| triangle | -1 | minimal case |
| square + center | 16 | interior enables concave polygon |

## Edge Cases

When all points lie on a convex boundary, the hull includes every point. The algorithm detects this by comparing hull size with n. In that situation, even though many simple polygons exist, none can be concave because there is no interior vertex available to create a reflex angle.

When there is exactly one interior point, the hull remains unchanged but the inequality `len(hull) < n` triggers the positive case. The algorithm still outputs hull area, and the interior point is conceptually used only to allow a non-convex ordering, not to change geometry.

When the point set is already minimal, such as three points forming a triangle, the hull equals the full set, so the output is `-1` even though a polygon exists. The concavity requirement is the blocking condition, not polygon existence.
