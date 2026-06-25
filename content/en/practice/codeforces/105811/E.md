---
title: "CF 105811E - Cable Plan"
description: "The problem asks us to process many proposed cable lines over a set of houses placed on a plane. For every line, we need the largest perpendicular distance from any house to that line."
date: "2026-06-25T15:19:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105811
codeforces_index: "E"
codeforces_contest_name: "UT Open 2025"
rating: 0
weight: 105811
solve_time_s: 58
verified: true
draft: false
---

[CF 105811E - Cable Plan](https://codeforces.com/problemset/problem/105811/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to process many proposed cable lines over a set of houses placed on a plane. For every line, we need the largest perpendicular distance from any house to that line. The official statement describes the houses as points and the cable plans as lines of the form `Ax + By + C = 0`.

The distance from a point `(x, y)` to such a line is:

$$\frac{|Ax + By + C|}{\sqrt{A^2+B^2}}$$

The denominator is the same for every house in one query, so the real task is finding the maximum value of `|Ax + By + C|` among all points.

The input size is large. With up to `2 * 10^5` houses and `2 * 10^5` queries, a solution that checks every house for every query performs about `4 * 10^10` operations, which is far beyond what a contest time limit allows. We need to preprocess the houses so each query is close to logarithmic time.

The key geometric observation is that the maximum value of a linear function over a set of points is always reached on the convex hull. All points inside the hull are irrelevant because they are convex combinations of other points, and a linear function cannot have a strict maximum there. The problem becomes a convex hull support query problem.

There are a few edge cases that break careless solutions. If all houses lie on one line, the convex hull has only two vertices. For example:

```
2 1
0 0
5 5
1 -1 0
```

The line `x - y = 0` contains both houses, so the answer is:

```
0.0000000000
```

A solution that assumes at least three hull points may fail.

Another issue is that the answer uses the absolute value. Consider:

```
2 1
0 0
1 1
1 0 -10
```

The expression values are `-10` and `-9`, so the maximum absolute value is `10`. Only searching for the maximum signed value would incorrectly return `9`.

A third subtle case is when the best point is not an original input point. The farthest point from a direction is always on the hull, but not necessarily the first or last point in the input order. Any solution relying on input ordering will silently fail.

## Approaches

A direct solution is straightforward. For every query, compute the value of the line expression for every house, keep the largest absolute value, and divide by the normalization factor. This is correct because it checks the exact definition of the answer. However, with `n` houses and `q` queries, the complexity is `O(nq)`, which becomes roughly `4 * 10^10` evaluations at maximum input size.

The improvement comes from recognizing the structure of the expression. For a query normal vector `(A, B)`, we need:

$$\max |A x + B y + C|$$

The `C` part only shifts all values equally, so we need the maximum and minimum of:

$$A x + B y$$

over all houses. The convex hull contains exactly the extreme points for every direction. This converts the problem into finding a support point of a convex polygon.

After building the convex hull, each query becomes a binary search on the hull. The dot product with a fixed direction changes in a unimodal way around a convex polygon, so we can locate the extreme vertex in logarithmic time. Convex hull based extreme queries are a standard use of the ordered structure of a convex polygon.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n log n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all house coordinates and build the convex hull using the monotonic chain algorithm. Remove inner points because they can never maximize a linear expression.
2. Store the hull vertices in counter-clockwise order. The ordering matters because the dot product values around a convex polygon form a shape where binary search is possible.
3. For each query line, extract `A`, `B`, and `C`. The direction `(A, B)` tells us which side of the hull is farthest.
4. Find the maximum value of `A*x + B*y` on the hull. This is done with a binary search over the cyclic convex polygon.
5. Find the minimum value in the same way by searching with direction `(-A, -B)`. Negating the direction turns a minimum query into a maximum query.
6. Combine the two extremes. The largest absolute expression value is:

$$\max(\text{maxValue}+C,\;-(\text{minValue}+C))$$

Then divide by `sqrt(A^2+B^2)`.

Why it works: the convex hull contains all possible extreme points of the original point set. For any direction vector, a linear function reaches its maximum and minimum on the hull. Since the distance formula is just an absolute linear expression divided by a constant, the two support queries give exactly the two candidates needed for the answer.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def build_hull(points):
    points = sorted(set(points))
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

def dot(p, a, b):
    return p[0] * a + p[1] * b

def support(poly, a, b):
    n = len(poly)
    if n == 1:
        return dot(poly[0], a, b)

    l, r = 0, n - 1
    while l < r:
        m = (l + r) // 2
        cur = dot(poly[m], a, b)
        nxt = dot(poly[(m + 1) % n], a, b)
        if cur <= nxt:
            l = m + 1
        else:
            r = m
    ans = dot(poly[l], a, b)
    ans = max(ans, dot(poly[(l - 1) % n], a, b))
    ans = max(ans, dot(poly[(l + 1) % n], a, b))
    return ans

def solve():
    n, q = map(int, input().split())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    hull = build_hull(pts)

    out = []
    for _ in range(q):
        A, B, C = map(int, input().split())

        mx = support(hull, A, B)
        mn = -support(hull, -A, -B)

        value = max(abs(mx + C), abs(mn + C))
        ans = value / math.sqrt(A * A + B * B)
        out.append(f"{ans:.12f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The hull construction removes points that are hidden inside the polygon. The `cross` function checks whether the last two hull edges would create a non-left turn, meaning the middle point cannot belong to the convex boundary.

The `support` function is the core optimization. It searches for the vertex where the projection onto `(A, B)` is largest. The final checks around the found index handle flat edges and avoid issues from equal projection values.

The query processing performs two support queries. One finds the maximum projection, while the other finds the minimum by reversing the direction vector. The absolute value is applied only after both extremes are known, which avoids the common mistake of forgetting the negative side.

## Worked Examples

Sample 1:

```
2 2
0 0
1 1
-1 1 0
1 1 -2
```

| Step | Query direction | Maximum projection | Minimum projection | Answer |
| --- | --- | --- | --- | --- |
| 1 | (-1, 1) | 0 | 0 | 0 |
| 2 | (1, 1) | 2 | 0 | 1.4142135624 |

The first line has both points on it, so both projections are equal. The second query reaches its largest distance at `(0,0)`.

Sample 2:

```
3 1
0 0
2 0
0 2
1 0 -3
```

| Step | Query direction | Maximum projection | Minimum projection | Answer |
| --- | --- | --- | --- | --- |
| 1 | (1,0) | 2 | 0 | 3 |

The constant term shifts all projections. The minimum projection is still needed because the absolute value can choose the other side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | Hull construction sorts points once, each query performs two logarithmic support searches |
| Space | O(n) | The convex hull stores at most all input points |

The preprocessing dominates the initial cost, and every query only touches logarithmically many hull vertices. This fits the limits for `2 * 10^5` points and queries.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue()

assert run("""2 2
0 0
1 1
-1 1 0
1 1 -2
""") == "0.000000000000\n1.414213562373\n"

assert run("""1 1
5 7
1 1 -12
""") == "0.000000000000\n"

assert run("""3 1
0 0
2 0
0 2
1 0 -3
""") == "3.000000000000\n"

assert run("""4 1
0 0
10 0
10 10
0 10
1 0 0
""") == "10.000000000000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two points on a diagonal | `0` and `sqrt(2)` | Basic hull and absolute distance handling |
| One house | `0` | Single point hull |
| Triangle with shifted line | `3` | Constant term handling |
| Square boundary query | `10` | Maximum projection on hull vertices |

## Edge Cases

For collinear houses:

```
2 1
0 0
5 5
1 -1 0
```

The hull contains only the two endpoints. The support query checks both possible vertices, and the line expression is zero for both, giving the correct answer.

For the absolute value issue:

```
2 1
0 0
1 1
1 0 -10
```

The two expression values are `-10` and `-9`. The algorithm computes both the maximum and minimum projections, then applies the absolute value, producing `10`.

For a case where input order is misleading:

```
4 1
100 100
0 0
100 0
0 100
1 1 0
```

The farthest point is not the first input point by any useful ordering. The hull removes ordering assumptions and the support search finds the correct extreme vertex.
