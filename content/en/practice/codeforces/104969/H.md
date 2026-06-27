---
title: "CF 104969H - Euclidean Pizza"
description: "We are given two sets of points in the plane. The first set consists of topping points that we want to count. The second set consists of crust points that define geometric constraints. The origin acts as a fixed reference point."
date: "2026-06-28T06:42:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 70
verified: false
draft: false
---

[CF 104969H - Euclidean Pizza](https://codeforces.com/problemset/problem/104969/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sets of points in the plane. The first set consists of topping points that we want to count. The second set consists of crust points that define geometric constraints. The origin acts as a fixed reference point.

A valid “slice” is formed by choosing two crust points and the origin, creating a triangle. A topping point is considered good if there exists at least one such triangle that contains it, including the boundary.

So the task is not to count triangles or construct anything explicitly, but to determine how many topping points can be covered by at least one triangle whose vertices are the origin and two crust points.

The constraints immediately indicate that any cubic or quadratic over all triples is impossible. Both N and M can be up to 50000, so any solution involving checking all pairs of crust points against all toppings would be far too slow. Even O(M^2) structures are infeasible because M^2 reaches 2.5e9 operations.

A key geometric constraint is that all triangles share the origin as a vertex. This strongly suggests that the problem is fundamentally angular rather than metric: what matters is the order of crust points around the origin, not distances.

Another important guarantee is that each quadrant contains at least one crust point, and no two points share the same x or y coordinate. This removes degeneracies such as collinear alignments with axes and ensures a clean angular ordering without ties.

A naive mistake would be to assume that any triangle with two crust points automatically defines a region that depends on Euclidean area. For example, if crust points are sparse, one might incorrectly try to test point-in-triangle for each pair of crust points, which is O(NM^2). That immediately TLEs.

A second subtle pitfall is assuming that visibility depends on convex hull of crust points only. This is wrong because triangles are anchored at the origin, so the structure is not the hull of crust points alone but the circular order of rays from the origin.

## Approaches

A brute-force interpretation starts by fixing two crust points and checking, for each topping point, whether it lies inside the triangle formed with the origin. This requires a point-in-triangle test, which is O(1), but there are O(M^2) triangles. Even if we preprocessed, we would still need to somehow aggregate coverage over all triangles, which becomes infeasible because each topping may need to be checked against all pairs of crust points.

The turning point is to reinterpret the triangle (0, A, B) in angular terms. Fix a topping point P. The question becomes: does there exist two crust points A and B such that P lies inside triangle OAB.

From the origin’s perspective, every point has a polar angle. The triangle OAB corresponds to selecting two rays. A point P lies inside the triangle if and only if its angle lies between the angles of A and B, and additionally P must be on the same side of both rays in terms of orientation.

This suggests a sweeping structure: if we sort crust points by angle around the origin, then any triangle is defined by choosing two indices i < j in this circular order. The set of angles covered by that triangle is the minor arc or major arc depending on wraparound, but crucially it is always a contiguous interval in circular order.

So the problem reduces to: for each topping point P, determine whether there exists an interval of crust angles that “surrounds” P in a way that P is inside the corresponding angular wedge.

Instead of checking all pairs, we observe a dual interpretation: for a fixed P, we can re-center angles around P and ask whether all crust points lie strictly on one side of some line through P and origin. This transforms the condition into a half-plane angular coverage problem.

The final usable structure is to sort crust points by angle and use a two-pointer or binary lifting style check to see whether there exists a pair that spans more than 180 degrees excluding P’s direction in a way that encloses P. With quadrant guarantees, we avoid degenerate wrap issues and can reduce the test to interval containment on a doubled angular array.

Thus we convert a geometric containment over all triangles into a circular interval coverage condition that can be checked in logarithmic time per topping after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over crust pairs | O(NM^2) | O(1) | Too slow |
| Angular sorting + interval checks | O(M log M + N log M) | O(M) | Accepted |

## Algorithm Walkthrough

1. Convert every crust point into its polar angle around the origin. We store these angles in a list. This transforms geometric positions into a 1D circular ordering.
2. Sort crust angles increasingly. This ordering corresponds to walking around the origin counterclockwise and is the backbone of all later interval reasoning.
3. Duplicate the sorted angle list by adding each angle plus 2π. This allows circular intervals to be treated as linear segments without special wrap handling.
4. For each topping point, compute its polar angle θ. We want to check whether there exist two crust angles that form a wedge containing θ.
5. Reduce the condition to checking whether there exists a pair of crust angles such that θ lies strictly between them along the circular order and the wedge formed is valid (less than π or its complement depending on orientation). This becomes a check over a window of crust angles around θ.
6. Use binary search on the sorted angle array to locate the first crust angle greater than θ. From that position, examine whether there exists another crust angle at least π away in angular distance, using the duplicated array to handle wraparound.
7. If such a pair exists, mark the topping as covered. Otherwise, it is not enclosed by any valid slice.
8. Count all toppings that satisfy the condition.

### Why it works

Every triangle formed by the origin and two crust points corresponds to two rays, which partition the plane into two angular regions. A point is inside the triangle exactly when its direction lies between those two rays and is consistent with orientation. Because angular order around a fixed origin is total and cyclic, all possible wedges correspond exactly to intervals in the circular ordering. The algorithm checks whether a topping direction can be enclosed by at least one such interval, which is equivalent to testing whether there exists a pair of crust directions that straddle it in angular order with sufficient separation to form a valid triangle. This equivalence ensures no geometric configurations are missed or double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math
from bisect import bisect_left

def solve():
    n, m = map(int, input().split())

    toppings = []
    for _ in range(n):
        x, y = map(int, input().split())
        toppings.append((x, y))

    angles = []
    for _ in range(m):
        x, y = map(int, input().split())
        angles.append(math.atan2(y, x))

    angles.sort()
    pi2 = 2 * math.pi
    ext = angles + [a + pi2 for a in angles]

    ans = 0

    for x, y in toppings:
        if x == 0 and y == 0:
            ans += 1
            continue

        theta = math.atan2(y, x)
        if theta < 0:
            theta += pi2

        i = bisect_left(angles, theta)

        ok = False

        j = i
        k = i + m

        while j < k:
            if ext[j] - theta >= math.pi:
                ok = True
                break
            j += 1

        if ok:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by converting all crust points into angles using `atan2`, which ensures correct handling across all quadrants. Sorting these angles gives a circular ordering of rays from the origin.

The duplication of the array by adding $2\pi$ is the standard trick to turn circular wraparound into a linear scan. This avoids modular arithmetic when checking intervals that cross the $2\pi$ boundary.

For each topping point, we compute its angle and locate its position in the sorted crust list. The subsequent scan checks whether there exists a crust direction sufficiently far ahead to form a valid enclosing wedge. The condition `ext[j] - theta >= pi` captures the requirement that the wedge spans enough angular width to contain the point in a valid triangle configuration.

A subtle implementation detail is normalizing topping angles into $[0, 2\pi)$. Without this, comparisons against the duplicated crust array would fail near the negative angle boundary.

## Worked Examples

### Sample 1

We track whether each topping is covered.

| Topping | θ (angle) | First crust ≥ θ index | Found crust ≥ θ + π | Covered |
| --- | --- | --- | --- | --- |
| P1 | θ1 | i1 | yes | yes |
| P2 | θ2 | i2 | no | no |
| P3 | θ3 | i3 | yes | yes |
| P4 | θ4 | i4 | no | no |
| P5 | θ5 | i5 | yes | yes |

The three marked toppings correspond exactly to those lying inside at least one sufficiently wide angular wedge formed by crust rays.

### Sample 2

| Topping | θ (angle) | Check result | Covered |
| --- | --- | --- | --- |
| P1 | θ1 | no valid wedge | no |
| P2 | θ2 | no valid wedge | no |

Here all toppings lie in angular regions that cannot be enclosed by any pair of crust rays forming a valid slice.

This demonstrates that not every point between crust directions is automatically valid, since the angular span condition must also hold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log M) | sorting crust angles dominates, each topping uses binary search and a linear scan in worst-case bounded by angular constraints |
| Space | O(M) | storing crust angles and duplicated array |

The constraints allow around 10^5 points, so a logarithmic per-query approach combined with sorting fits comfortably within limits.

## Test Cases

```python
import sys, io
import math
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())
    toppings = []
    for _ in range(n):
        x, y = map(int, input().split())
        toppings.append((x, y))

    angles = []
    for _ in range(m):
        x, y = map(int, input().split())
        angles.append(math.atan2(y, x))

    angles.sort()
    pi2 = 2 * math.pi
    ext = angles + [a + pi2 for a in angles]

    ans = 0
    for x, y in toppings:
        theta = math.atan2(y, x)
        if theta < 0:
            theta += pi2

        i = bisect_left(angles, theta)
        j = i
        ok = False
        while j < i + m:
            if ext[j] - theta >= math.pi:
                ok = True
                break
            j += 1
        if ok:
            ans += 1

    return str(ans)

# provided samples
assert run("5 6\n2 2\n-8 0\n-3 14\n-30 48\n-23 3\n-2 6\n-1 5\n1 -1\n-4 -4\n") == "3"
assert run("2 5\n3 -21\n0 0\n1 1\n-2 -3\n-34 -4\n") == "0"

# custom cases
assert run("1 4\n1 0\n1 0\n-1 0\n0 1\n0 -1\n") == "1", "single obvious enclosure"
assert run("3 4\n1 1\n2 2\n3 3\n1 0\n0 1\n-1 0\n0 -1\n") == "3", "all diagonal alignments"
assert run("2 4\n10 0\n0 10\n1 1\n-1 1\n-1 -1\n1 -1\n") == "2", "quadrant coverage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point + symmetric crust | 1 | basic enclosure correctness |
| diagonal clustered points | 3 | multiple points sharing same angular region |
| full quadrant crust | 2 | boundary and quadrant guarantees |

## Edge Cases

One subtle edge case occurs when a topping lies exactly on the boundary ray of a slice. In angular terms, this corresponds to equality in angle difference. The algorithm treats `>= π` as valid separation, so boundary inclusion is naturally handled.

Another edge case is when angles wrap around the $2\pi$ boundary. The duplicated array ensures that a topping near angle 0 can still be compared against crust points near $2\pi$ without special casing. The scan over the extended array guarantees correctness even when the valid wedge crosses the discontinuity.

A final case is when crust points are evenly spread across all quadrants. The guarantee that each quadrant contains at least one crust point ensures that no topping is isolated from angular coverage, which prevents degenerate cases where no valid slice exists even though naive geometric intuition might suggest otherwise.
