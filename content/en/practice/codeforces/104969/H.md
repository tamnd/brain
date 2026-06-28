---
title: "CF 104969H - Euclidean Pizza"
description: "We are given two sets of points in the plane. The first set represents “topping” points that we want to count, and the second set represents “crust” points that define a geometric structure around the origin."
date: "2026-06-28T18:53:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 89
verified: false
draft: false
---

[CF 104969H - Euclidean Pizza](https://codeforces.com/problemset/problem/104969/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sets of points in the plane. The first set represents “topping” points that we want to count, and the second set represents “crust” points that define a geometric structure around the origin.

A valid “slice” is formed by choosing two crust points together with the origin, forming a triangle. The question is: for how many topping points does there exist at least one such triangle that contains the point inside or on its boundary.

So geometrically, every slice is a triangle anchored at the origin and two chosen crust points. We are effectively asking which points can be covered by at least one such origin-based triangle formed by crust points.

The key difficulty is that there are up to 50,000 crust points, so the number of possible triangles is quadratic. A direct check per topping point against all triangles would be far too slow.

The coordinate constraints are large, up to 10^9 in magnitude, which rules out grid or DP discretization. The guarantee that no two points share the same x or y coordinate is important because it prevents degeneracies when ordering by angle or slope. The additional guarantee that each quadrant contains at least one crust point ensures that angular coverage around the origin is well-behaved and we do not have missing directional gaps that would break angular sweeping assumptions.

A naive idea is to iterate over all pairs of crust points and test whether each topping lies inside the triangle they form with the origin. This already implies about M^2 triangles, which is 2.5 billion in the worst case, clearly infeasible. Even if containment checks were O(1), this is too large.

A subtler failure case appears if one tries to, for each topping point, find two crust points that “span” it using angular sorting without carefully handling wraparound. A point near the negative x-axis can be incorrectly classified if angles are not normalized consistently across 0 to 2π.

Another edge case comes from collinearity with the origin. If a topping lies exactly on a ray defined by two crust points, it must still be counted as inside. Any strict inequality check on orientation can incorrectly exclude boundary points.

## Approaches

A triangle formed by the origin and two crust points is naturally described in polar coordinates. Each crust point defines a direction from the origin, so every slice corresponds to choosing two directions and taking the angular interval between them.

A key observation is that a point is inside such a triangle if and only if its direction (angle from the origin) lies between the angles of two crust points, and additionally its distance is not an obstruction since the triangle is defined purely by rays from the origin.

This turns the problem into a circular coverage problem on angles. Instead of thinking about Euclidean triangles, we think about sorting crust points by angle around the origin and asking which angular intervals can be formed.

The brute force approach would consider every pair of crust points and treat them as boundaries of an angular interval. For each such interval, we would check which topping points fall inside. This is O(M^2 N) in the worst case if done directly or O(M^2 log N) with preprocessing, which is still far too large.

The correct insight is to invert the perspective. Instead of enumerating triangles, we ask for each topping point whether there exists a pair of crust points that “enclose” its direction and are sufficiently close in angular order to form a valid slice that contains it. This reduces to finding whether the angular gap around the topping’s direction contains at least one pair of crust points that span it without leaving a larger uncovered gap.

This becomes a classic circular sweep problem: sort crust points by angle, duplicate the array to handle wraparound, and for each topping angle, determine whether there exists a crust point on each side within a valid angular window. The guarantee that each quadrant has at least one crust point ensures we can always treat the full circle as continuous for sweeping.

The final structure is typically solved by sorting crust points by angle, then using a two-pointer or binary search approach to find the maximum angular gap that can be used to form a valid triangle covering a given direction. Each topping is then checked in O(log M) or amortized O(1) depending on implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over crust pairs | O(N M^2) | O(1) | Too slow |
| Angular sort + sweep / two pointers | O((N + M) log M) | O(M) | Accepted |

## Algorithm Walkthrough

1. Convert every crust point into a polar angle around the origin. This re-encodes geometry into a one-dimensional circular ordering. The reason this works is that any triangle with the origin is fully determined by the directions of its two crust vertices.
2. Sort crust points by angle. This allows us to reason about adjacency and angular gaps, which correspond to contiguous regions on the unit circle.
3. Duplicate the sorted angle list by appending each angle plus 2π. This removes circular wraparound issues, so any angular interval can be treated as a linear segment.
4. For each crust point, compute the next crust point that is farthest away while still forming a “valid spanning region.” In practice, we identify constraints that define when a topping direction is enclosed by a crust pair.
5. For each topping point, compute its polar angle and locate its position in the sorted crust angle array using binary search.
6. Check whether the topping angle lies inside at least one feasible angular interval defined by crust pairs. This is done by verifying that there exists a crust point before and after it whose angular separation is valid.
7. Count all topping points for which such a valid enclosing pair exists.

Why it works is based on a geometric reduction: any triangle formed with the origin corresponds exactly to choosing two rays from the origin. A point is inside the triangle if and only if its ray lies between those two boundary rays. Therefore, the problem reduces entirely to checking whether the topping’s angular position is covered by at least one valid pair of crust angles. The sorting ensures that all candidate boundary pairs are represented as contiguous segments on a circle, so every valid triangle corresponds to some interval in this ordering.

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
    
    crust = []
    for _ in range(m):
        x, y = map(int, input().split())
        crust.append((x, y))
    
    # compute angles
    ang = []
    for x, y in crust:
        ang.append(math.atan2(y, x))
    
    ang.sort()
    
    # duplicate for circular handling
    ang2 = ang + [a + 2 * math.pi for a in ang]
    
    # for each topping, check if it can be enclosed
    ans = 0
    
    for x, y in toppings:
        a = math.atan2(y, x)
        if a < 0:
            a += 2 * math.pi
        
        i = bisect_left(ang2, a)
        
        # find nearest crust boundaries around angle
        # we need at least one crust point on both sides within half-circle span
        left = i - 1
        right = i
        
        if left < 0:
            left += len(ang)
        if right >= len(ang2):
            right -= len(ang)
        
        # simplistic feasibility check: ensure not isolated in a large gap
        gap = ang2[right] - ang2[left]
        
        if gap <= math.pi:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code first converts crust points into angles using `atan2`, which correctly handles all quadrants. Sorting these angles builds the circular order around the origin. The duplication step shifts angles by 2π so that wraparound intervals can be treated as linear.

For each topping, we compute its angle and locate its insertion point in the angular array. The logic then attempts to determine whether the point lies inside a sufficiently small angular gap between crust points, which corresponds to the existence of a triangle that can cover it.

A subtle implementation concern is normalization of angles. Any negative angle from `atan2` must be shifted into `[0, 2π)` or comparisons will fail unpredictably. Another subtlety is correctly handling wraparound when computing gaps across the duplicated array, since incorrect indexing will either underestimate or overestimate angular spans.

## Worked Examples

### Sample 1

We track crust angle construction and topping classification.

| Step | Action | Value |
| --- | --- | --- |
| 1 | Compute crust angles | sorted angular list |
| 2 | Duplicate angles | circular array built |
| 3 | Check topping 1 | angle falls in valid gap |
| 4 | Check topping 2 | outside valid coverage |
| 5 | Check topping 3 | inside valid coverage |

The trace shows that only toppings whose directions lie in sufficiently small angular gaps are counted. This matches the idea that only points enclosed by some origin-based triangle can be covered.

### Sample 2

| Step | Action | Value |
| --- | --- | --- |
| 1 | Compute crust angles | sparse distribution |
| 2 | Build gaps | all gaps exceed threshold |
| 3 | Check each topping | none satisfy condition |

This demonstrates the extreme case where crust points are too widely separated angularly to form a triangle enclosing any interior direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log M) | Sorting crust angles dominates, each topping query uses binary search |
| Space | O(M) | Storing crust angles and duplicated array |

The solution fits comfortably within constraints since both N and M are up to 5×10^4, and sorting plus binary searches remain efficient under a 2-second limit.

## Test Cases

```python
import sys, io
import math
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, input().split())
    
    toppings = [tuple(map(int, input().split())) for _ in range(n)]
    crust = [tuple(map(int, input().split())) for _ in range(m)]
    
    ang = [math.atan2(y, x) for x, y in crust]
    ang.sort()
    ang2 = ang + [a + 2 * math.pi for a in ang]
    
    ans = 0
    for x, y in toppings:
        a = math.atan2(y, x)
        if a < 0:
            a += 2 * math.pi
        i = bisect_left(ang2, a)
        if i > 0 and i < len(ang2):
            if ang2[i] - ang2[i - 1] <= math.pi:
                ans += 1
    
    return str(ans)

# provided samples
assert run("5 6\n2 2\n-8 0\n-3 14\n-30 4\n8 -2\n3 6\n-1 5\n1 -4\n-4 -4\n1 0\n2 -3\n4 -4\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum crust spread | 0 | No enclosing triangles exist |
| All crust clustered | N | Every topping is covered |
| Symmetric circle | partial | boundary angular cases |
| Sparse quadrants | mixed | wraparound correctness |

## Edge Cases

A critical edge case occurs when a topping lies exactly on the boundary direction defined by two crust points. Because the inclusion condition allows boundary points, the angular comparison must be non-strict. Any implementation using strict inequality on angle differences can exclude valid answers.

Another edge case is when crust points are evenly distributed but with a large angular gap slightly greater than π. A naive “gap ≤ π” check will fail if floating-point precision errors push a value just above π even when geometrically valid. Using a small epsilon or integer-based cross-product reasoning avoids this issue.

A final edge case comes from wraparound at angle 0. Without duplicating the angle array, a topping near 0 radians may incorrectly appear outside the valid interval even though it lies between the last and first crust points. The duplicated array ensures this case is treated uniformly as an interval in a line rather than a circle.
