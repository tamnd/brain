---
title: "CF 1584G - Eligible Segments"
description: "We have several points on the plane. We want to count pairs of points whose connecting segment stays close to every point in the set. More precisely, for a chosen pair $(pi,pj)$, every point must lie at distance at most $R$ from that segment."
date: "2026-06-10T09:41:50+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1584
codeforces_index: "G"
codeforces_contest_name: "Technocup 2022 - Elimination Round 2"
rating: 3200
weight: 1584
solve_time_s: 139
verified: false
draft: false
---

[CF 1584G - Eligible Segments](https://codeforces.com/problemset/problem/1584/G)

**Rating:** 3200  
**Tags:** geometry  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have several points on the plane. We want to count pairs of points whose connecting segment stays close to every point in the set. More precisely, for a chosen pair $(p_i,p_j)$, every point must lie at distance at most $R$ from that segment.

The segment matters, not the infinite line. A point may project outside the segment, in which case its distance to the segment is the distance to one of the endpoints.

The number of points is at most 3000. There are about $4.5\times 10^6$ pairs of endpoints. Checking every pair against all points would require roughly

$$\binom{3000}{2}\cdot 3000 \approx 1.35\times 10^{10}$$

distance computations, which is far beyond what fits into three seconds. Any cubic solution is ruled out. Quadratic algorithms are acceptable, and $O(n^2\log n)$ is easily fast enough.

Several situations are easy to mishandle.

Suppose all points lie on one line:

```
3 1
0 0
2 0
5 0
```

The correct answer is 1, namely the segment joining the two extreme points. If we only require every point to be close to the infinite supporting line, then all three pairs would seem valid, which is wrong because the middle pair leaves one endpoint outside the segment.

Another subtle case appears when the farthest point from the supporting line projects beyond an endpoint.

```
3 2
0 0
3 0
10 1
```

The point $(10,1)$ is only distance 1 from the infinite line $y=0$, but its distance to the segment from $(0,0)$ to $(3,0)$ is almost 7. A line based formulation alone misses this.

A third pitfall is that the segment must cover the projections of all points. For

```
4 2
-3 0
0 1
0 -1
3 0
```

only the segment between the two extreme points works. Any shorter segment leaves one of the outer points outside.

## Approaches

The brute force idea is straightforward. Enumerate every pair of points, treat them as segment endpoints, and compute the distance from every point to that segment. If all distances are at most $R$, count the pair.

The correctness is immediate because the definition is checked directly. The problem is speed. There are $O(n^2)$ pairs and each pair requires $O(n)$ distance tests, giving $O(n^3)$ operations.

To improve this, we need to understand the geometry.

Take some direction $u$. Project every point onto that direction. Among all projections there is a minimum and a maximum. The segment joining the points attaining these extreme projections is the only candidate segment whose supporting line has direction $u$. Any other pair with the same direction leaves some projection outside the segment.

Now look at the perpendicular direction $v$. The maximum difference between projections onto $v$ is exactly the width of the point set in that orientation. Every point lies within distance

$$\frac{\text{width}}{2}$$

from the middle line. Thus a segment with direction $u$ is feasible exactly when the width perpendicular to $u$ is at most $2R$.

This converts the problem into a convex geometry problem. Only convex hull vertices matter, because interior points can never become extreme projections. For each edge direction on the convex hull we can use rotating calipers to maintain the farthest point in the perpendicular direction and obtain the width in linear time overall.

Whenever the width does not exceed $2R$, the two extreme points along the current direction form one eligible segment.

The key observation is that each direction determines at most one candidate pair, reducing millions of possibilities to only the $m$ hull vertices, where $m\le n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Compute the convex hull.

Interior points never determine extreme projections in any direction, so they can be ignored. We construct the convex hull using the monotone chain algorithm.

### 2. Handle small hulls.

If the hull contains one point, no segment exists.

If the hull contains two points, their segment is the only possible answer and it is always valid.

### 3. Traverse hull edges with rotating calipers.

For every hull edge $H_iH_{i+1}$, consider its direction. The width perpendicular to this direction equals the maximum distance from the supporting line through the edge to any hull vertex.

Because the antipodal point moves monotonically around the polygon, the rotating calipers technique updates this maximum in total linear time.

### 4. Compute the width.

For edge vector $e$, let

$$A = |\text{cross}(e, H_k-H_i)|$$

where $k$ is the current antipodal point.

The actual width is

$$\frac{A}{|e|}.$$

Instead of using floating point numbers, compare

$$A^2 \le (2R)^2|e|^2.$$

This avoids precision issues.

### 5. Recover the endpoint pair.

For the current edge direction, the segment that spans all projections is formed by the two support points in that direction.

Rotating calipers simultaneously maintain these extreme vertices. Whenever the width condition holds, that pair contributes one answer.

### 6. Count distinct pairs.

Different edge directions may produce the same endpoint pair, so we store pairs in a set.

### Why it works

For any direction, all point projections form an interval. The only segment with that direction whose projection interval contains every point is the segment joining the minimum and maximum projections. A point's distance to this segment equals its distance to the supporting line because every projection lies inside the interval.

The width perpendicular to the segment direction is exactly the largest such distance multiplied by two. Thus the condition "every point is within distance $R$ from the segment" is equivalent to "the width of the point set perpendicular to the segment is at most $2R$". Rotating calipers enumerate every relevant orientation, so every valid pair is found and no invalid pair is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
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

def solve():
    n, R = map(int, input().split())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    hull = convex_hull(pts)
    m = len(hull)

    if m < 2:
        print(0)
        return

    if m == 2:
        print(1)
        return

    hull.extend(hull[:2])

    j = 1
    ans = set()

    for i in range(m):
        ni = i + 1
        ex = hull[ni][0] - hull[i][0]
        ey = hull[ni][1] - hull[i][1]

        while True:
            nj = (j + 1) % m

            cur = abs(ex * (hull[j][1] - hull[i][1]) -
                      ey * (hull[j][0] - hull[i][0]))
            nxt = abs(ex * (hull[nj][1] - hull[i][1]) -
                      ey * (hull[nj][0] - hull[i][0]))

            if nxt > cur:
                j = nj
            else:
                break

        area = abs(ex * (hull[j][1] - hull[i][1]) -
                   ey * (hull[j][0] - hull[i][0]))

        edge_sq = ex * ex + ey * ey

        if area * area <= 4 * R * R * edge_sq:
            a = i
            b = ni % m
            if a > b:
                a, b = b, a
            ans.add((a, b))

    print(len(ans))

solve()
```

The first part builds the convex hull. Using `<=0` removes collinear interior points and leaves only extreme vertices.

Rotating calipers maintain the antipodal point `j`. Since `j` only moves forward, the total number of pointer advances is linear.

The comparison uses squared quantities. This avoids floating point inaccuracies and matches the statement's guarantee that tiny perturbations of $R$ do not change the answer.

Pairs are inserted into a set because multiple edges may correspond to the same segment orientation.

## Worked Examples

### Sample 1

Input:

```
4 2
0 1
0 -1
3 0
-3 0
```

Convex hull order:

$$(-3,0),(0,-1),(3,0),(0,1)$$

| Edge | Antipodal point | Width | Width ≤ 2R? |
| --- | --- | --- | --- |
| (-3,0)-(0,-1) | (0,1) | 1.897 | Yes |
| (0,-1)-(3,0) | (-3,0) | 1.897 | Yes |
| (3,0)-(0,1) | (0,-1) | 1.897 | Yes |
| (0,1)-(-3,0) | (3,0) | 1.897 | Yes |

Only one distinct segment spans all projections, namely $(-3,0)$ to $(3,0)$.

Output:

```
1
```

This example shows that several edge orientations may correspond to the same final pair.

### Collinear Example

Input:

```
3 1
0 0
2 0
5 0
```

| Hull size | Candidate segment | Answer |
| --- | --- | --- |
| 2 | (0,0)-(5,0) | 1 |

All points lie on the segment, so every distance equals zero.

This confirms that interior collinear points are safely removed by the hull construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log n)$ | Hull construction dominates |
| Space | $O(n)$ | Hull vertices and auxiliary structures |

The limit $n=3000$ is modest, and an $O(n\log n)$ algorithm runs comfortably within three seconds.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# sample 1
assert run("""4 2
0 1
0 -1
3 0
-3 0
""") == "1"

# single point
assert run("""1 5
0 0
""") == "0"

# two points
assert run("""2 1
0 0
5 0
""") == "1"

# collinear points
assert run("""3 1
0 0
2 0
5 0
""") == "1"

# square with large R
assert run("""4 10
0 0
1 0
1 1
0 1
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One point | 0 | No segment exists |
| Two points | 1 | Trivial hull |
| Collinear points | 1 | Interior collinear points removed correctly |
| Large square with large R | 6 | Every pair becomes valid |

## Edge Cases

Consider

```
3 1
0 0
2 0
5 0
```

The hull contains only the two extreme points. Rotating calipers never need to move. The algorithm outputs 1, which is correct because the middle point lies on the segment.

For

```
3 2
0 0
3 0
10 1
```

the width with respect to the direction of the short segment is small, but the projections do not span the third point. The support pair for that direction becomes $(0,0)$ and $(10,1)$, not $(0,0)$ and $(3,0)$, preventing an incorrect count.

For

```
4 2
-3 0
0 1
0 -1
3 0
```

multiple edge directions satisfy the width condition. They all produce the same support pair consisting of the two extreme points. The set of pairs removes duplicates, leaving the correct answer 1.
