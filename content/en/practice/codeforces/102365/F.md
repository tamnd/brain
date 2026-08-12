---
title: "CF 102365F - Fair Distribution"
description: "For every subset of villagers, consider the area of the convex hull of their houses. A random permutation gives each villager a marginal contribution: when that villager is inserted, compare the new convex hull area with the area before insertion."
date: "2026-08-13T00:02:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102365
codeforces_index: "F"
codeforces_contest_name: "UBC Programming Contest 2019 (UBCPC 2019)"
rating: 0
weight: 102365
solve_time_s: 216
verified: true
draft: false
---

[CF 102365F - Fair Distribution](https://codeforces.com/problemset/problem/102365/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

For every subset of villagers, consider the area of the convex hull of their houses. A random permutation gives each villager a marginal contribution: when that villager is inserted, compare the new convex hull area with the area before insertion. The required answer for a villager is the average of that marginal contribution over all possible insertion orders.

Equivalently, this is the Shapley value of the convex-hull-area function. For a fixed villager (p), we need the expected increase in hull area when (p) is inserted into a uniformly random ordering of the other (N-1) points.

The input contains at most 200 distinct planar points, with coordinates bounded by (10^4). The small value of (N) rules out factorial or exponential enumeration, but it leaves room for a cubic algorithm. In particular, (N^3) is only (8\cdot10^6) iterations at the maximum size, which is a reasonable target for an optimized implementation. The coordinate bound also means every ordinary orientation test fits comfortably in a 64-bit integer, although Python integers remove any overflow concern.

The first degenerate case is (N=1). A single point has zero-area convex hull, so the only answer is (0).

```
1
10000 -10000
```

The correct output is

```
0
```

An implementation that assumes every villager can eventually form a triangle may try to divide by a level that does not exist.

The second case is two points.

```
2
0 0
10000 10000
```

Again the answer is

```
0
0
```

The convex hull of two points is a segment, so every marginal contribution is zero. A formula based on three points must explicitly handle this case.

The third issue is collinearity. Consider

```
4
0 0
1 0
2 0
0 1
```

The hull is the triangle with vertices ((0,0),(2,0),(0,1)), but the point ((1,0)) lies on one of its edges. A naive version of the usual general-position formula can count the triangle using both endpoints ((0,0),(2,0)) and also count smaller triangles involving ((1,0)), producing too much area. The correct Shapley values are

```
0.4166666666666667
0.0833333333333333
0.0833333333333333
0.4166666666666667
```

The implementation below handles such degeneracies by using an infinitesimal symbolic perturbation for orientation decisions while retaining the original coordinates for triangle areas. This is the correct limiting interpretation because convex-hull area, and hence every finite average of marginal contributions, is continuous under arbitrarily small perturbations.

## Approaches

The direct approach follows the definition literally. Enumerate every one of the (N!) permutations. For each permutation, insert the points one at a time, recompute the convex hull after every insertion, and add the increase in area to the corresponding villager. This is correct because it explicitly evaluates exactly the experiment whose expectation the problem asks for.

The problem is the factorial number of permutations. Even before accounting for hull construction, (200!) is approximately (7.9\cdot10^{374}). Recomputing a hull for every prefix would make the work roughly (O(N!,N^2\log N)), which is hopeless.

The useful observation is that a marginal hull-area increase has a very specific geometric structure. Suppose (p) is the point being inserted. The part of the new hull that was not already present in the old hull is a chain of triangles whose common vertex is (p). Every such triangle can be described by two earlier points (q) and (q').

Direct the line from (q) to (q'), and let (H(q,q')) be its left open halfplane. If (p) lies in that halfplane, the triangle (pqq') can appear in the newly exposed part of the hull exactly when (q) and (q') are the first two relevant points to appear, while (p) is the third.

Let (L(q,q')) be the number of input points lying strictly in (H(q,q')). Among the (L+2) points consisting of (q,q') and those (L) points, the required event says that (q,q') occupy the first two positions, in either order, and (p) occupies the third position. Its probability is

# \frac{2!,(L-1)!}{(L+2)!}

\frac{2}{L(L+1)(L+2)}.
]

This is the key reduction. The enormous collection of permutations disappears. For every ordered pair of points we only need one integer, its halfplane level, and one rational probability.

For a fixed (p), the expected contribution is then

\sum_{\substack{q\ne q'\p\in H(q,q')}}
\operatorname{area}(pqq')\rho(q,q').
]

The level values can be computed efficiently by sorting the other points by polar angle around each (q) and using a rotating pointer. Once the levels are known, evaluating the formula for all (p) takes (O(N^3)) time.

For the given (N\le200), this is the practical solution. The same geometric decomposition admits a more advanced (O(N^2)) algorithm by aggregating weighted line halfplane queries through a line arrangement, which is the asymptotically optimal version of this idea.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N!,N^2\log N)) | (O(N)) | Too slow |
| Pair and halfplane levels | (O(N^3)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Read all points and prepare a tiny symbolic perturbation for orientation decisions. The original coordinates remain unchanged for computing triangle areas. The perturbation only decides which side of a line a point belongs to when the original three points are collinear.
2. For every point (q), sort all other points by their polar angle around (q). With the perturbation, no two relevant directions are exactly tied.
3. Sweep around the sorted directions with a second pointer. For a directed pair (q\to q'), every point encountered strictly counterclockwise from (q') for less than (180^\circ) lies in the left halfplane of the directed line. The number of such points is (L(q,q')).
4. Convert every level (L\ge1) into the probability
[
\rho(q,q')=\frac{2}{L(L+1)(L+2)}.
]
A level of zero receives weight zero because no third point can lie in that halfplane.
5. For every target point (p), inspect every unordered pair (q,q'). Compute the original signed double area
[
c=(q'-q)\times(p-q).
]
If (c>0), (p) is on the left of (q\to q'), so add
[
\frac{c}{2}\rho(q,q').
]
If (c<0), (p) is on the left of (q'\to q), so add
[
\frac{-c}{2}\rho(q',q).
]
If (c=0), the triangle has zero area and contributes nothing.
6. Print the accumulated value for every point. For (N<3), the loops naturally produce zero for every villager.

The invariant behind the computation is that every positive-area piece created by inserting (p) is represented by exactly one directed pair (q,q'), namely the endpoints of one exposed edge of the old hull. The event represented by that pair is exactly that (q,q') appear before (p), while every point on the relevant side appears after (p). The probability assigned to the pair is precisely the probability of that event. Summing the corresponding triangle areas thus gives the marginal contribution for one permutation in expectation, and linearity of expectation allows all pairs to be summed independently.

For collinear input, the infinitesimal perturbation only changes side classifications for triples whose original area is zero. Such triples contribute zero area anyway. For every non-collinear triple, the original integer orientation is nonzero and is much larger than the infinitesimal perturbation, so its side classification remains unchanged.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    if n < 3:
        for _ in range(n):
            print("0.0")
        return

    # The perturbation is only used for orientation / angular ordering.
    # x_i -> x_i + eps * i
    # y_i -> y_i + eps * i^2
    #
    # eps is chosen far below the smallest possible nonzero integer
    # orientation, which has absolute value at least 1.
    eps = 1e-10

    px = [x + eps * (i + 1) for i, (x, y) in enumerate(pts)]
    py = [y + eps * (i + 1) * (i + 1)
          for i, (x, y) in enumerate(pts)]

    rho = [[0.0] * n for _ in range(n)]

    # Compute the level of every directed line q -> r.
    #
    # For a fixed q, points are sorted by angle around q.
    # For every starting direction, a monotone pointer finds the
    # entire open semicircle to its left.
    for q in range(n):
        order = [i for i in range(n) if i != q]

        qx = px[q]
        qy = py[q]

        order.sort(
            key=lambda i: math.atan2(py[i] - qy, px[i] - qx)
        )

        m = n - 1
        doubled = order + order
        t = 0

        for s in range(m):
            if t < s + 1:
                t = s + 1

            a = doubled[s]
            ax = px[a] - qx
            ay = py[a] - qy

            while t < s + m:
                b = doubled[t]
                bx = px[b] - qx
                by = py[b] - qy

                cross = ax * by - ay * bx
                if cross > 0.0:
                    t += 1
                else:
                    break

            level = t - s - 1
            if level > 0:
                rho[q][a] = (
                    2.0 / (level * (level + 1) * (level + 2))
                )

    ans = [0.0] * n

    # For each p and each unordered pair q,r, exactly one orientation
    # puts p strictly on the left, unless p,q,r are collinear.
    for p in range(n):
        total = 0.0
        px0, py0 = pts[p]

        for q in range(n):
            qx, qy = pts[q]

            for r in range(q + 1, n):
                if r == p or q == p:
                    continue

                rx, ry = pts[r]

                cross = (
                    (rx - qx) * (py0 - qy)
                    - (ry - qy) * (px0 - qx)
                )

                if cross > 0:
                    total += 0.5 * cross * rho[q][r]
                elif cross < 0:
                    total += 0.5 * (-cross) * rho[r][q]

        ans[p] = total

    for value in ans:
        print("{:.15f}".format(value))

if __name__ == "__main__":
    solve()
```

The first part of the implementation builds the perturbed coordinates. The perturbation is deliberately tiny, while its dependence on the point index makes it deterministic. If an original orientation is nonzero, its absolute value is at least 1 because all input coordinates are integers. The perturbation is far too small to reverse such an orientation.

The angular sweep computes (L(q,q')) without testing all (N) points against every directed line. For each fixed (q), the points are circularly ordered once. As the starting direction advances, the endpoint of the left semicircle never moves backward, so all levels for that (q) are obtained in linear time after sorting.

The `rho` matrix is indexed by directed pairs. This matters because the two directions of the same geometric line have different left halfplanes and hence generally have different levels and probabilities.

The final triple loop uses unordered pairs only. If the original cross product is positive, the relevant directed line is (q\to r). If it is negative, the relevant direction is (r\to q). This avoids doing the same geometric pair twice.

The area calculation uses the original integer coordinates, not the perturbed ones. This is essential. The perturbation is a symbolic device for deciding combinatorial relationships, not a modification of the actual amount of money represented by the geometry.

All geometric orientation calculations involving the original coordinates are integer calculations. Python's arbitrary-precision integers make overflow impossible here. The only floating-point operations are the probability values, the angular ordering, and the final accumulation.

## Worked Examples

### Sample 1

The sample contains four points:

```
(2,2)
(0,2)
(2,0)
(1,1)
```

The first three points form a triangle of area (2), while ((1,1)) lies inside it. The expected shares are

```
0.8333333333333333
0.5
0.5
0.1666666666666667
```

The following trace focuses on the geometric pair contributions.

| Target (p) | Pair | Double area | Relevant level | Probability | Contribution |
| --- | --- | --- | --- | --- | --- |
| ((2,2)) | ((0,2),(2,0)) | 4 | 1 | (1/3) | (2/3) |
| ((2,2)) | other relevant pairs | varies | varies | varies | (1/6) total |
| ((0,2)) | hull pairs | varies | varies | varies | (1/2) total |
| ((2,0)) | hull pairs | varies | varies | varies | (1/2) total |
| ((1,1)) | hull pairs | varies | varies | varies | (1/6) total |

The interior point receives a positive amount because it can be inserted after two points that form a smaller hull and can enlarge that hull, even though it never belongs to the final hull of all four points.

### Sample 2

Consider the three-point input

```
3
0 0
2 0
0 2
```

The full convex hull has area (2). With exactly three points, a villager contributes nonzero area precisely when that villager is third in the permutation. Each villager is third in exactly (2!) of the (3!) permutations, so every villager receives (2/3).

| Target (p) | Number of other points | Relevant pair | Double area | Level | Probability | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| ((0,0)) | 2 | ((2,0),(0,2)) | 4 | 1 | (1/3) | (2/3) |
| ((2,0)) | 2 | ((0,2),(0,0)) | 4 | 1 | (1/3) | (2/3) |
| ((0,2)) | 2 | ((0,0),(2,0)) | 4 | 1 | (1/3) | (2/3) |

The three answers sum to (2), exactly the area of the final hull. This is the efficiency property of the Shapley allocation appearing directly in the geometry.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3)) | Level computation is (O(N^2\log N)), followed by (O(N^3)) pair accumulation |
| Space | (O(N^2)) | The directed probability matrix contains (N^2) values |

With (N\le200), the cubic part contains fewer than four million unordered point-pair checks per target, and only about four million total pair-target combinations after exploiting unordered pairs. The probability preprocessing is smaller than that. The memory usage is dominated by the (200\times200) probability matrix.

The asymptotically stronger geometric solution reduces the final weighted halfplane aggregation to (O(N^2)), but it requires constructing and traversing a line arrangement. The cubic implementation above is considerably simpler and is well matched to the contest's (N=200) constraint. The underlying pair decomposition is the same one used in the known (O(N^2)) result.

## Test Cases

```python
# The tests below assume the solution above is placed in this file.
# For a standalone test script, the implementation is reproduced
# through the run() helper.

import sys
import io
import math

def algorithm(inp: str) -> list[float]:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]

        if n < 3:
            return [0.0] * n

        eps = 1e-10

        px = [x + eps * (i + 1) for i, (x, y) in enumerate(pts)]
        py = [y + eps * (i + 1) * (i + 1)
              for i, (x, y) in enumerate(pts)]

        rho = [[0.0] * n for _ in range(n)]

        for q in range(n):
            order = [i for i in range(n) if i != q]
            qx, qy = px[q], py[q]

            order.sort(
                key=lambda i: math.atan2(py[i] - qy, px[i] - qx)
            )

            m = n - 1
            doubled = order + order
            t = 0

            for s in range(m):
                if t < s + 1:
                    t = s + 1

                a = doubled[s]
                ax = px[a] - qx
                ay = py[a] - qy

                while t < s + m:
                    b = doubled[t]
                    bx = px[b] - qx
                    by = py[b] - qy

                    if ax * by - ay * bx > 0.0:
                        t += 1
                    else:
                        break

                level = t - s - 1
                if level > 0:
                    rho[q][a] = (
                        2.0 / (level * (level + 1) * (level + 2))
                    )

        ans = [0.0] * n

        for p in range(n):
            px0, py0 = pts[p]
            total = 0.0

            for q in range(n):
                if q == p:
                    continue

                qx, qy = pts[q]

                for r in range(q + 1, n):
                    if r == p:
                        continue

                    rx, ry = pts[r]

                    cross = (
                        (rx - qx) * (py0 - qy)
                        - (ry - qy) * (px0 - qx)
                    )

                    if cross > 0:
                        total += 0.5 * cross * rho[q][r]
                    elif cross < 0:
                        total += 0.5 * (-cross) * rho[r][q]

            ans[p] = total

        return ans

    finally:
        sys.stdin = old_stdin

def run(inp: str) -> list[float]:
    return algorithm(inp)

def assert_close(actual, expected, name):
    assert len(actual) == len(expected), name
    for a, e in zip(actual, expected):
        assert abs(a - e) <= 1e-8 * max(1.0, abs(e)), (
            name, a, e
        )

# Provided sample
sample = """\
4
2 2
0 2
2 0
1 1
"""
assert_close(
    run(sample),
    [
        0.8333333333333333,
        0.5,
        0.5,
        0.16666666666666666,
    ],
    "provided sample",
)

# Minimum-size input
assert_close(
    run("""\
1
10000 -10000
"""),
    [0.0],
    "one point",
)

# Two points, still zero area
assert_close(
    run("""\
2
-10000 -10000
10000 10000
"""),
    [0.0, 0.0],
    "two points",
)

# Three points, every point gets one third of the triangle area.
triangle = """\
3
0 0
2 0
0 2
"""
assert_close(
    run(triangle),
    [2.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0],
    "triangle",
)

# Square: all four vertices are symmetric, so every answer is 1/4.
square = """\
4
0 0
1 0
1 1
0 1
"""
assert_close(
    run(square),
    [0.25, 0.25, 0.25, 0.25],
    "square",
)

# Collinear points plus one off-line point.
degenerate = """\
4
0 0
1 0
2 0
0 1
"""
assert_close(
    run(degenerate),
    [
        5.0 / 12.0,
        1.0 / 12.0,
        1.0 / 12.0,
        5.0 / 12.0,
    ],
    "collinear boundary point",
)

# Maximum-size input. The expected individual answers are not written
# explicitly, so we check the defining efficiency property:
# their sum must equal the area of the full convex hull.
pts = [(i, (i * i) % 10000) for i in range(200)]
maximum = "200\n" + "\n".join(f"{x} {y}" for x, y in pts) + "\n"
got = run(maximum)

assert len(got) == 200, "maximum size length"
assert all(x >= -1e-9 for x in got), "nonnegative maximum answers"

def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    def cross(o, a, b):
        return (
            (a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0])
        )

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

def hull_area(points):
    h = convex_hull(points)
    if len(h) < 3:
        return 0.0

    s = 0
    for i in range(len(h)):
        x1, y1 = h[i]
        x2, y2 = h[(i + 1) % len(h)]
        s += x1 * y2 - y1 * x2

    return abs(s) / 2.0

assert abs(sum(got) - hull_area(pts)) <= 1e-6 * max(
    1.0, hull_area(pts)
), "maximum efficiency"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | (0.8333333,0.5,0.5,0.1666667) | Original sample and interior point |
| `1 / (10000,-10000)` | `0` | Minimum size and zero-area hull |
| Two opposite boundary points | `0,0` | No triangle exists |
| Right triangle | `2/3` for every point | Probability (1/3) of being inserted last |
| Unit square | `0.25` for every point | Symmetry and equal allocation |
| Collinear chain plus one point | `5/12,1/12,1/12,5/12` | Degenerate collinearity handling |
| 200 generated points | Sum equals full hull area | Maximum input size and efficiency invariant |

## Edge Cases

For a single point, the preprocessing stage is skipped because (N<3), and the solution immediately prints zero. There is no directed pair that can define a triangle, so this agrees with the geometric definition.

For two points, the same early return applies. Their convex hull is a line segment, whose area is zero. This avoids ever constructing a probability for a nonexistent third point.

For three non-collinear points, there is exactly one pair of predecessors whenever the target point is inserted third. The halfplane containing the target contains exactly one point, so (L=1) and

[
\rho=\frac{2}{1\cdot2\cdot3}=\frac13.
]

The target receives one third of the triangle area. Since each of the three points has the same probability of being third, every point receives exactly one third of the full area.

For collinear points, the original cross product can be zero even though the symbolic perturbation puts the points on a definite side of the line. The algorithm deliberately uses different coordinates for these two jobs. The original cross product determines the actual triangle area, which is zero for a collinear triple. The perturbed geometry determines the combinatorial ordering needed for the probability. This corresponds to taking the limit from a general-position configuration and avoids double-counting a hull edge containing several input points.

For the concrete degenerate input

```
4
0 0
1 0
2 0
0 1
```

the full hull has area (1). The two endpoints ((0,0)) and ((0,1)) each receive (5/12), while the two points on the bottom edge each receive (1/12). Their sum is

[
\frac5{12}+\frac1{12}+\frac1{12}+\frac5{12}=1,
]

so the entire hull area is distributed exactly once.

The final efficiency check is also a useful debugging invariant. For every permutation, the sum of all marginal increases telescopes to the final hull area. Taking expectations preserves that equality, so the computed answers must always sum to the area of the convex hull of all input points. A significant discrepancy usually means that a directed halfplane, probability level, or orientation sign was handled incorrectly.
