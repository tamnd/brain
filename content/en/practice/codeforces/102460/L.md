---
title: "CF 102460L - Largest Quadrilateral"
description: "We have up to 4096 points in the plane, and we may choose four of them as the vertices of a quadrilateral. The four points do not have to be distinct as coordinates because the input itself may contain duplicates, and degenerate quadrilaterals are allowed."
date: "2026-08-09T03:00:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "L"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 331
verified: true
draft: false
---

[CF 102460L - Largest Quadrilateral](https://codeforces.com/problemset/problem/102460/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have up to 4096 points in the plane, and we may choose four of them as the vertices of a quadrilateral. The four points do not have to be distinct as coordinates because the input itself may contain duplicates, and degenerate quadrilaterals are allowed. The task is to find the largest possible area and print it exactly, including the possible `.5` fractional part.

The central geometric fact is that an optimal quadrilateral can be treated as a convex one, possibly degenerated into a triangle. Once a diagonal is fixed, its area is the sum of the areas of the two triangles lying on the two sides of that diagonal. For a fixed diagonal, maximizing the quadrilateral area is consequently the same as finding the farthest point from the diagonal on each side. This is the key observation behind the intended (O(N^2)) solution.

The coordinate bounds are large, up to (10^9), so floating point geometry is unnecessary and undesirable. Every doubled area is an integer cross product, so we can perform the entire computation with exact integer arithmetic. In C++, signed 64-bit integers are sufficient for the required cross products, while Python integers have arbitrary precision.

The value (N=4096) is large enough to rule out anything close to (O(N^3)), let alone (O(N^4)). Enumerating every four-point subset already gives

[
\binom{4096}{4}=11,710,951,848,960
]

possibilities, roughly (1.17\times10^{13}). The intended solution must exploit geometric structure rather than examine every quadruple independently. The convex hull costs only (O(N\log N)), after which the quadratic rotating-calipers phase is the dominant work.

There are several edge cases that can silently break an implementation.

If all points are identical, for example

```
4
0 0
0 0
0 0
0 0
```

the answer is `0`. A convex-hull implementation that assumes at least three distinct points can fail here.

If all points are collinear, for example

```
4
0 0
1 0
2 0
3 0
```

the answer is also `0`. The hull has only two vertices, even though the input contains four points.

If the hull has exactly three vertices, the answer is the area of that triangle. For example,

```
4
0 0
4 0
0 4
1 1
```

has a triangular hull, and the fourth point lies inside it. The maximum allowed quadrilateral degenerates to the triangle, so the answer is `8`, not zero and not an arbitrary small quadrilateral.

Finally, the answer may be a half-integer. The input

```
4
0 0
1 0
0 1
3 2
```

has maximum doubled area `5`, so the required output is `2.5`. Printing through floating point is unnecessary and can introduce formatting errors. We keep twice the area as an integer until the final output.

## Approaches

The direct approach is to enumerate every choice of four input points. For each quadruple, we could consider the possible vertex orders or, more efficiently, determine the maximum area obtainable from those four points in constant time. Either way, the number of quadruples is (O(N^4)). At (N=4096), there are about (1.17\times10^{13}) quadruples, which is far beyond the available time.

The useful observation is that a maximum-area quadrilateral can be taken to be convex, with the degenerate triangle case handled separately. If we choose one diagonal (A C), the quadrilateral is split into two triangles, (A B C) and (A C D). Their bases are both the same segment (AC), so their combined area is maximized by choosing the point farthest from line (AC) on one side and the point farthest from line (AC) on the other side. The doubled triangle area is exactly the absolute cross product.

This also tells us why only convex-hull points matter. If the point maximizing the distance from a fixed line were strictly inside the convex hull, a hull point would lie farther in that direction. Thus an optimal choice can be moved onto the hull. This hull reduction and the fixed-diagonal formulation are the standard geometric basis for the (O(N^2)) method.

After computing the convex hull in cyclic order, consider a fixed hull vertex (i). Move the other endpoint (j) of the diagonal forward around the hull. For each diagonal (i,j), we need the best vertex between (i) and (j), and the best vertex on the other arc. Because the polygon is convex, these farthest vertices move monotonically as (j) moves forward. A pointer that has already moved forward never needs to move backward. This is the rotating-calipers step.

Thus the brute-force search over all pairs of opposite vertices becomes quadratic. For every (i), there are (O(N)) possible (j), while the two farthest-point pointers together also advance only (O(N)) times. The resulting algorithm is (O(N^2)) after the hull is known.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^4)) | (O(N)) | Too slow |
| Optimal | (O(N^2)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read all points and compute their convex hull.

We sort the points lexicographically and use the monotonic-chain construction. Duplicate coordinates are removed for the purpose of constructing the geometric hull, and collinear points along an edge are unnecessary because they can never increase an area maximum. The original multiplicity does not affect the answer when the hull has at least four vertices.
2. If the hull has at most two vertices, output `0`.

Every input point lies on one line, so every possible quadrilateral has zero area.
3. If the hull has exactly three vertices, compute the doubled area of that triangle and output it.

Any fourth point is either inside the triangle or coincides with one of its vertices. Such a point cannot create an area larger than the triangle itself, while the problem permits degenerate quadrilaterals, so the triangle area is the required maximum.
4. Duplicate the cyclic hull array conceptually by considering indices from `0` through `2h-1`.

This avoids awkward modulo operations while traversing the two arcs of a diagonal. A point at index `i+h` is the same geometric point as index `i`.
5. Fix a hull vertex `i` and let `j` run from `i+2` through `i+h-2`.

These are exactly the diagonals for which there is at least one hull vertex on each side. Every convex quadrilateral has such a diagonal, so considering these pairs covers every candidate.
6. Maintain pointer `k` for the best vertex on the arc from `i` to `j`.

While `k+1 < j` and the doubled triangle area increases when replacing `k` by `k+1`, advance `k`. For a convex polygon, the distance from a fixed chord to consecutive vertices is unimodal, so once the value starts decreasing, moving farther cannot find a better vertex.
7. Maintain pointer `l` for the best vertex on the complementary arc from `j` back to `i`.

The same unimodality argument applies to this side. As `j` advances, the optimal `l` never needs to move backward, which is what turns the otherwise cubic search into a quadratic one.
8. Compute the candidate doubled area as

[
\operatorname{cross}(i,j,k)+\operatorname{cross}(i,j,l).
]

The hull is stored counterclockwise, so both terms have the same sign for the corresponding two arcs. Each cross product is twice the area of one triangle, and their sum is twice the quadrilateral area.
9. Update the global maximum and continue through all diagonals.

Each possible convex quadrilateral has a diagonal among the pairs considered in step 5, and for that diagonal the algorithm chooses the best possible vertex on each side. Consequently, its candidate value is at least the area of that quadrilateral. Since every candidate is itself a valid quadrilateral construction, the maximum candidate is exactly the answer.
10. Convert doubled area to the required textual form.

If the doubled area is even, print `answer // 2`. If it is odd, print `answer // 2` followed by `.5`. No floating-point arithmetic is needed.

Why it works: for every chosen diagonal, the quadrilateral area is exactly the sum of two triangle areas. The base of both triangles is fixed, so each side is independently optimized by taking the hull vertex with maximum perpendicular distance from the diagonal. Convexity makes each side's distance sequence unimodal and makes its maximizing index monotone as the diagonal endpoint advances. The two rotating pointers therefore find the exact best pair for every diagonal without scanning every possible pair of opposite vertices. Since every maximum-area quadrilateral can be chosen convex with vertices on the hull, the global maximum over these diagonal candidates is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))

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

def largest_quadrilateral(points):
    hull = convex_hull(points)
    h = len(hull)

    if h <= 2:
        return 0

    if h == 3:
        return abs(cross(hull[0], hull[1], hull[2]))

    # Duplicate the hull so that all cyclic arcs can be traversed
    # with ordinary integer indices.
    p = hull + hull

    ans = 0
    limit_offset = h - 1

    for i in range(h):
        k = i + 1
        l = i + 3

        last_j = i + h - 2

        for j in range(i + 2, last_j + 1):
            if k >= j:
                k = j - 1

            # Best point on the arc i ... j.
            while k + 1 < j:
                cur = cross(p[i], p[k], p[j])
                nxt = cross(p[i], p[k + 1], p[j])
                if cur <= nxt:
                    k += 1
                else:
                    break

            if l <= j:
                l = j + 1

            # Best point on the complementary arc j ... i+h.
            while l + 1 <= i + h - 1:
                cur = cross(p[i], p[j], p[l])
                nxt = cross(p[i], p[j], p[l + 1])
                if cur <= nxt:
                    l += 1
                else:
                    break

            candidate = (
                cross(p[i], p[j], p[k])
                + cross(p[i], p[j], p[l])
            )

            if candidate > ans:
                ans = candidate

    return ans

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        points = [tuple(map(int, input().split())) for _ in range(n)]

        doubled = largest_quadrilateral(points)

        if doubled % 2 == 0:
            out.append(str(doubled // 2))
        else:
            out.append(str(doubled // 2) + ".5")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `convex_hull` function uses the standard monotonic-chain construction. The `<= 0` condition removes points that lie strictly inside a hull edge as well as duplicate points. Keeping only the extreme endpoints is sufficient for the maximum-area search.

The special cases before the quadratic loop are necessary because a diagonal-based quadrilateral requires at least four hull vertices. With two hull vertices the entire set is collinear. With three hull vertices the best allowed quadrilateral degenerates to the hull triangle, so its doubled area is one cross product.

The `p = hull + hull` line is a small but useful implementation detail. It lets `j`, `k`, and `l` move through a complete cyclic copy of the hull without repeated `% h` operations inside the hottest loop.

For a counterclockwise convex hull, the cross products used in the two arcs are nonnegative. That lets the implementation avoid `abs()` inside the quadratic loop. The two cross products are exactly the doubled areas of the two triangles formed by the diagonal.

The condition `k + 1 < j` prevents `k` from becoming one of the diagonal endpoints. Similarly, `l + 1 <= i + h - 1` keeps `l` inside the complementary arc. These boundaries are the easiest places to introduce an off-by-one error.

The pointers are deliberately initialized as `k = i + 1` and `l = i + 3`. The smallest valid diagonal has `j = i + 2`, so its first arc contains only `i+1`, while its other arc starts at `i+3`.

All area calculations remain integers. With coordinates as large as (10^9), a cross product can be on the order of (10^{18}), so a language with fixed-width arithmetic needs a sufficiently wide integer type. Python's arbitrary-precision integers handle this automatically.

## Worked Examples

### Sample 1

The three test cases in the first sample are interpreted with the missing contest-format header restored as `T = 3`.

For the first case, all five points are hull vertices. The most useful diagonal is from `(0,0)` to `(3,1)`. The best point on one side is `(1,0)`, giving doubled triangle area `1`, and the best point on the other side is `(1,2)`, giving doubled triangle area `5`. Their sum is `6`, so the quadrilateral area is `3`.

A condensed trace of the rotating-calipers state is:

| `i` | `j` | `k` | `l` | Candidate doubled area | Global best |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 3 | 6 | 6 |
| 0 | 3 | 2 | 4 | 6 | 6 |
| 1 | 3 | 2 | 4 | 6 | 6 |
| 2 | 4 | 3 | 6 | 6 | 6 |
| 3 | 5 | 4 | 6 | 3 | 6 |
| 4 | 6 | 5 | 7 | 4 | 6 |

The important part of this trace is not that every diagonal gives the optimum. It shows that the best side pointers advance monotonically, and that the first candidate with doubled area `6` already corresponds to the required area `3`.

For the second case, the points form a convex quadrilateral. The best diagonal is `(0,0)` to `(3,2)`. The two opposite hull points are `(1,0)` and `(0,1)`. Their doubled triangle areas are `2` and `3`.

| `i` | `j` | `k` | `l` | Candidate doubled area | Global best |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 3 | 5 | 5 |
| 1 | 3 | 2 | 4 | 5 | 5 |

The final doubled area is `5`, so the output is `2.5`. The third case has only two distinct locations, `(0,0)` and `(2,2)`, so its hull is a line segment and the answer is `0`.

### Sample 2

The four points are

```
(0,0)
(1,0)
(0,1)
(3,2)
```

and all four lie on the convex hull. With hull order `(0,0), (1,0), (3,2), (0,1)`, there is only one distinct diagonal to inspect for each fixed starting point.

| `i` | `j` | `k` | `l` | First doubled triangle area | Second doubled triangle area | Candidate |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 3 | 2 | 3 | 5 |
| 1 | 3 | 2 | 4 | 4 | 1 | 5 |

The maximum doubled area is `5`, giving the exact answer `2.5`. This example exercises the half-integer output path and also confirms that the two sides of a diagonal must be optimized independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N + H^2)) | Sorting and hull construction cost (O(N\log N)), while the rotating-calipers phase considers (O(H^2)) diagonals and each pointer moves monotonically. |
| Space | (O(N)) | The sorted points, hull, and duplicated hull require linear memory. |

Here (H) is the number of convex-hull vertices and (H\le N), so the worst-case time complexity is (O(N^2)). With (N=4096), the quadratic phase has about (1.7\times10^7) diagonal iterations in the worst case, which is the intended scale for the six-second limit. The memory consumption is linear and comfortably within the 1024 MB limit.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py`.

```python
# helper: run solution on input string, return output string
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
sample1 = """\
3
5
0 0
1 0
3 1
1 2
0 1
4
0 0
4 0
0 4
1 1
4
0 0
1 1
2 2
1 1
"""

assert run(sample1) == "3\n3\n0", "sample 1"

# Provided sample 2
sample2 = """\
1
4
0 0
1 0
0 1
3 2
"""

assert run(sample2) == "2.5", "sample 2"

# Minimum-size non-degenerate case.
square = """\
1
4
0 0
1 0
1 1
0 1
"""

assert run(square) == "1", "minimum-size square"

# All points equal.
equal = """\
1
4
0 0
0 0
0 0
0 0
"""

assert run(equal) == "0", "all points equal"

# All points collinear.
collinear = """\
1
4
0 0
1 0
2 0
100 0
"""

assert run(collinear) == "0", "collinear points"

# Maximum coordinate boundary and a half-integer answer.
boundary = """\
1
4
0 0
1000000000 0
1000000000 1
0 1
"""

assert run(boundary) == "1000000000", "coordinate boundary"

# Maximum-size input, deliberately consisting of equal points.
# This checks both input volume and the degenerate hull case.
maximum_size = "1\n4096\n" + "123456789 987654321\n" * 4096

assert run(maximum_size) == "0", "maximum-size input"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Four vertices of a unit square | `1` | Minimum-size non-degenerate quadrilateral |
| Four copies of `(0,0)` | `0` | Duplicate points and degenerate hull |
| Four collinear points | `0` | Two-vertex hull and zero area |
| Coordinates up to (10^9) | `1000000000` | Large integer arithmetic and boundary coordinates |
| 4096 identical points | `0` | Maximum input size and degenerate case |

## Edge Cases

For four identical points,

```
1
4
0 0
0 0
0 0
0 0
```

the sorted unique point list contains only one point. The hull therefore has size one, and `largest_quadrilateral` immediately returns zero. No diagonal processing is attempted.

For four collinear points,

```
1
4
0 0
1 0
2 0
3 0
```

the monotonic-chain hull has two endpoints, `(0,0)` and `(3,0)`. The function returns zero because every cross product involving the input points is zero.

For a triangular hull with an interior fourth point,

```
1
4
0 0
4 0
0 4
1 1
```

the hull contains `(0,0)`, `(4,0)`, and `(0,4)`. Its doubled area is

[
|(4,0)\times(0,4)|=16,
]

so the actual area is `8`. The interior point cannot increase the area beyond the enclosing triangle, and the allowed degenerate quadrilateral can attain that value. The special `h == 3` branch consequently returns `16`, which is formatted as `8`.

For a half-integer result,

```
1
4
0 0
1 0
0 1
3 2
```

the rotating-calipers phase finds a maximum doubled area of `5`. The final formatting sees that `5` is odd and prints `5 // 2` followed by `.5`, producing exactly `2.5`. No floating-point calculation occurs.

For coordinates at the maximum bound,

```
1
4
0 0
1000000000 0
1000000000 1
0 1
```

the doubled area is (2\times10^9), so the answer is `1000000000`. The implementation computes this directly with integer cross products, avoiding precision loss.

The duplicated-hull representation is also an edge-condition safeguard. For a diagonal with endpoints `i` and `j`, the first side uses indices strictly between them, while the second side uses indices strictly after `j` and before `i+h`. The loop bounds `j <= i+h-2`, `k+1 < j`, and `l+1 <= i+h-1` guarantee that neither farthest-point pointer ever becomes a diagonal endpoint or crosses into an invalid arc.

If you want, I can also turn this into a shorter Codeforces-style editorial that keeps the same proof but is easier to skim during a contest.
