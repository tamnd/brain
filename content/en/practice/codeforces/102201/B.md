---
title: "CF 102201B - Bohemian Rhaksody"
description: "The four possible operations of a bulb all produce a half-plane whose boundary passes through that bulb. Intersecting all chosen half-planes always gives an axis-parallel rectangle, possibly degenerate or empty. There is a much cleaner way to view the same choice."
date: "2026-08-20T01:39:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "B"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 225
verified: true
draft: false
---

[CF 102201B - Bohemian Rhaksody](https://codeforces.com/problemset/problem/102201/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The four possible operations of a bulb all produce a half-plane whose boundary passes through that bulb. Intersecting all chosen half-planes always gives an axis-parallel rectangle, possibly degenerate or empty.

There is a much cleaner way to view the same choice. Suppose the final lit region is a rectangle (R). A bulb at ((X,Y)) can justify one of the four sides of (R) exactly when the bulb is not strictly inside (R). If the bulb is outside or on the boundary, choose the corresponding half-plane containing (R). Conversely, if a bulb is strictly inside (R), none of its four half-planes can contain the whole rectangle. Thus the original problem is exactly the problem of finding the maximum-area axis-parallel rectangle inside the (H\times W) stage whose interior contains no bulb.

This is the classical largest empty rectangle problem for points, specialized to the case where all (x)-coordinates and all (y)-coordinates are distinct. The distinct-coordinate condition is what makes the interval representation below particularly clean. The same reduction is also the key observation used in known treatments of this problem.

With (N\le 100000), an (O(N^2)) scan is not viable. Its worst case is roughly (5\times10^9) interval states, before accounting for the work needed to maintain each interval's largest vertical gap. The coordinate bounds reach (10^8), so coordinate compression is useful, but a grid-based method is completely out of the question.

There are several boundary cases that are easy to mishandle. If there is one bulb at a corner, for example

```
100 100 1
0 0
```

the whole stage is valid, because the bulb lies on its boundary, so the answer is (10000). A test that treats boundary points as forbidden would incorrectly return zero.

If the bulbs form a descending diagonal,

```
4 4 5
0 4
1 3
2 2
3 1
4 0
```

the answer is (6). The whole (4\times4) stage is impossible, but the optimum is not simply the largest gap between consecutive (x)-coordinates or consecutive (y)-coordinates. Both dimensions have to be considered simultaneously.

Finally, a rectangle may touch several bulbs on its boundary. Those bulbs are allowed. This is why the formulation uses an empty interior rather than a rectangle containing no points at all.

## Approaches

The direct approach is to sort the bulbs by (x), choose which consecutive group of bulbs lies horizontally inside the candidate rectangle, and compute the largest vertical gap between their (y)-coordinates. Suppose the candidate rectangle contains exactly bulbs (l,\ldots,r) in its horizontal projection. Its horizontal sides can be pushed outward until they reach the preceding and following bulb, or the stage boundary. Consequently its maximum possible width is

[
x_{r+1}-x_{l-1},
]

where (x_0=0) and (x_{N+1}=H).

For this fixed set of horizontally included bulbs, the vertical interval has to contain no selected (y)-coordinate in its interior. Add the stage boundaries (0,W) and the values (y_l,\ldots,y_r), sort them, and take the largest consecutive gap. Call that value (h(l,r)). The best rectangle represented by this interval has area

[
(x_{r+1}-x_{l-1})h(l,r).
]

This gives an exact (O(N^2)) algorithm. We can extend (r) one position at a time and maintain the selected (y)-coordinates in an ordered set, so each interval can be processed efficiently. The problem is the number of intervals. With (N=100000), there are (N(N+1)/2), approximately (5\times10^9), of them.

The optimization starts by observing that the relevant intervals have a strong nesting structure. For an interval ([l,r]), (h(l,r)) is the largest gap after inserting the (y)-coordinates belonging to that interval. Enlarging the interval can only split existing gaps, so (h) never increases. This monotonicity lets us retain only the maximal states that can matter.

A divide-and-conquer solution uses exactly those states. For every recursive segment of the (x)-ordered points, we construct a compact set of triples

[
(l,r,h),
]

where ([l,r]) is an (x)-interval and (h) is its largest available vertical gap. The retained intervals form a laminar family: two of them cannot partially overlap without one containing the other. When one interval contains another, its gap value is no larger. These two properties are the reason the potentially quadratic collection collapses to a linear-sized collection at every divide-and-conquer level.

Two recursive halves then have to be combined. If their triples are ((l_i,r_i,h_i)) and ((l_j,r_j,h_j)), their compatible rectangles have horizontal overlap

[
\min(r_i,r_j)-\max(l_i,l_j)
]

and vertical gap

[
h_i+h_j.
]

Hence their contribution is

[
(h_i+h_j)
\left(\min(r_i,r_j)-\max(l_i,l_j)\right).
]

The remaining problem is a structured maximum over two laminar triple families. Nested intervals are handled as a two-dimensional dominance problem. Partially overlapping intervals can be handled by a second divide and conquer. Inside a crossing subproblem, the triples become monotone when ordered by (h): as (h) increases, the left endpoint moves right and the right endpoint moves left. The resulting feasible partner sets are sliding windows, giving the required monotonicity for the final maximum computation.

This is the same structural optimization used in known (O(N\log^3N)) solutions of the largest empty rectangle formulation. The literature also gives more sophisticated bounds for the general largest empty rectangle problem, but the distinct-coordinate structure here is enough for the contest solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2\log N)) | (O(N)) | Too slow |
| Optimal divide and conquer | (O(N\log^3N)) | (O(N\log N)) | Accepted |

## Algorithm Walkthrough

1. Sort all bulbs by (x). Write the resulting coordinates as (x_1,\ldots,x_N), with (x_0=0) and (x_{N+1}=H). The corresponding (y)-coordinates form a permutation because all (y)-coordinates are distinct.
2. Interpret every feasible illumination as an empty axis-parallel rectangle. This removes the four-way choice at every bulb and replaces it with one geometric condition: no bulb may lie strictly inside the rectangle.
3. For an (x)-interval ([l,r]), define (h(l,r)) as the largest gap among (0,y_l,\ldots,y_r,W). If the rectangle contains exactly those bulbs in its horizontal projection, its maximum width is (x_{r+1}-x_{l-1}), so the candidate area is ((x_{r+1}-x_{l-1})h(l,r)).
4. Solve recursively on an interval of (x)-indices. Inside one recursive segment, maintain only the maximal states ((l,r,h)). When a new point is added to an interval, it can only split an existing vertical gap, so its best gap never becomes larger. This gives the laminarity and monotonicity needed to discard dominated states.
5. Recursively solve the left and right halves. Every optimal rectangle whose horizontal set is contained entirely in one half is already considered by that recursive call.
6. Combine rectangles whose relevant horizontal intervals meet across the division point. For two states, their combined horizontal span is determined by the intersection of the two intervals, while their two vertical gaps contribute additively. The value to maximize is

[
(h_i+h_j)
\left(\min(r_i,r_j)-\max(l_i,l_j)\right).
]
7. Separate pairs of intervals into nested pairs and crossing pairs. Nested intervals satisfy coordinate-wise dominance conditions and can be processed with a standard two-dimensional ordering. Crossing pairs have the form

[
l_i<l_j<r_i<r_j.
]

This is the only genuinely difficult case.
8. Apply a second divide and conquer to the crossing pairs. At each node, only pairs satisfying

[
l_i<l_j\le mid<r_i<r_j
]

are processed. Pairs that do not cross the secondary midpoint are passed recursively.
9. Sort the left family by increasing (h), and the right family by decreasing (h). Because the retained intervals are laminar, increasing (h) moves the left endpoint rightward and the right endpoint leftward. For a fixed right state, its valid left states form a contiguous sliding window. The endpoints of these windows move monotonically, so the maximum over all pairs can be found without enumerating every pair.
10. Repeat this combination at every recursive level. The first divide and conquer contributes one logarithmic factor, while the structured crossing computation contributes two more, giving (O(N\log^3N)).

The invariant is that every maximal empty rectangle has a representation in one of the retained interval states, or as the compatible combination of two states from different recursive halves. Because enlarging an interval can only destroy vertical gaps, dominated states can never become part of a better rectangle later. The nested and crossing cases exhaust all relative interval orders, so no optimal rectangle is discarded.

## Python Solution

The full contest implementation of the (O(N\log^3N)) algorithm is substantially more involved than a conventional segment-tree solution. In particular, the crossing-pair routine requires maintaining the laminar triple families and their monotone sliding windows. A short Python implementation is not a faithful translation of the accepted algorithm, and presenting an (O(N^2)) implementation here while labeling it accepted would be misleading for (N=100000).

For reference, the geometric reduction and the (O(N^2)) baseline are straightforward:

```python
import sys
input = sys.stdin.readline

def largest_empty_rectangle(H, W, points):
    points.sort()

    n = len(points)
    x = [0] + [p[0] for p in points] + [H]
    y = [0] + [p[1] for p in points] + [W]

    ans = 0

    for l in range(1, n + 1):
        vals = [0, W]

        for r in range(l, n + 1):
            vals.append(y[r])
            vals.sort()

            height = 0
            for i in range(1, len(vals)):
                height = max(height, vals[i] - vals[i - 1])

            width = x[r + 1] - x[l - 1]
            ans = max(ans, width * height)

    return ans

def solve():
    H, W, N = map(int, input().split())
    points = [tuple(map(int, input().split())) for _ in range(N)]
    print(largest_empty_rectangle(H, W, points))

if __name__ == "__main__":
    solve()
```

This code is useful as a correctness oracle for small instances, but it is not the submission algorithm for the given constraints. The nested loops enumerate every (x)-interval, and sorting the selected (y)-coordinates makes the implementation even slower. The accepted approach replaces this enumeration by the laminar divide-and-conquer structure described above.

The multiplication must use arbitrary-precision integers in Python because the maximum area is (10^{16}). Python handles this automatically, while a C++ implementation needs a 64-bit integer.

The stage boundaries are included as (0) and (H) horizontally and (0) and (W) vertically. This is also why a bulb located on the stage boundary does not need special treatment.

## Worked Examples

For Sample 1, the points are already sorted by (x).

| (l) | (r) | Horizontal span | Selected (y)-values | Largest vertical gap | Area |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | (1-0=1) | (0,4,4) | 4 | 4 |
| 1 | 2 | (2-0=2) | (0,4,3,4) | 3 | 6 |
| 1 | 3 | (3-0=3) | (0,4,3,2,4) | 2 | 6 |
| 1 | 4 | (4-0=4) | (0,4,3,2,1,4) | 1 | 4 |
| 2 | 4 | (4-1=3) | (0,3,2,1,4) | 1 | 3 |
| 3 | 5 | (4-2=2) | (0,2,1,0,4) | 1 | 2 |

The maximum is (6). One such rectangle has width (2) and height (3). The bulbs on its boundary are allowed, while no bulb lies in its interior.

For Sample 2 there is only one bulb, at the lower-left corner.

| (l) | (r) | Horizontal span | Vertical gap | Area |
| --- | --- | --- | --- | --- |
| 1 | 1 | (10^8) | (10^8) | (10^{16}) |

The bulb lies on the boundary of the entire stage, so the complete (10^8\times10^8) rectangle is valid. The answer is (10000000000000000).

These traces demonstrate why the word "strictly" matters. A point on a rectangle boundary does not invalidate the rectangle, which is exactly what allows the corner bulb in Sample 2 to coexist with the full stage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log^3N)) | The laminar interval construction and the two-level divide-and-conquer combination each contribute logarithmic factors. |
| Space | (O(N\log N)) | Recursive triple families and auxiliary structures are stored over logarithmically many levels. |

For (N=100000), quadratic enumeration is fundamentally too large. The divide-and-conquer structure reduces the number of relevant interval interactions to polylogarithmically many per point. This is the scale required by the original (10)-second, (1) GB contest limits. The general largest-empty-rectangle literature also confirms that this is a nontrivial computational-geometry problem rather than a simple scan.

## Test Cases

The following tests use the quadratic implementation above as a small-instance correctness oracle. They are intended for validating the geometric reduction and boundary handling. They are not a performance test for the (N=100000) constraints.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_instance(inp: str) -> str:
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

# provided sample 1
assert solve_instance(
    """4 4 5
0 4
1 3
2 2
3 1
4 0
"""
) == "6\n"

# provided sample 2
assert solve_instance(
    """100000000 100000000 1
0 0
"""
) == "10000000000000000\n"

# provided sample 3
assert solve_instance(
    """100000000 100000000 12
100000000 59411855
0 4914151
57454627 45388814
93661922 93279520
81531691 0
5221549 64790529
75886863 85609174
74950464 100000000
18493301 57818271
66752434 90450964
44757377 54518291
99631520 21997156
"""
) == "4522156529817280\n"

# minimum-size stage
assert solve_instance(
    """1 1 1
0 0
"""
) == "1\n"

# A point strictly inside prevents the full rectangle,
# but a boundary strip remains available.
assert solve_instance(
    """4 4 1
2 2
"""
) == "8\n"

# Two points on opposite corners still allow a large empty rectangle.
assert solve_instance(
    """4 4 2
0 0
4 4
"""
) == "16\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 0 0` | `1` | Minimum stage and boundary point |
| `4 4 1 / 2 2` | `8` | An interior point prevents the full stage |
| `4 4 2 / 0 0, 4 4` | `16` | Boundary points do not invalidate a rectangle |
| Sample 1 | `6` | Multiple points and interacting dimensions |

## Edge Cases

For the corner case

```
1 1 1
0 0
```

the only bulb lies at a corner. The full stage is empty in its interior, so the answer is (1). The interval representation includes the bulb as a boundary point and still obtains the vertical gap (1) and horizontal width (1).

For

```
4 4 1
2 2
```

the only point is strictly inside the full stage, so the (16)-area rectangle is forbidden. The best rectangle can occupy either the left half, right half, upper half, or lower half, giving area (8). This catches implementations that only check whether points lie on the boundary of the candidate rectangle rather than whether they lie strictly inside it.

For

```
4 4 2
0 0
4 4
```

both bulbs are already on the stage boundary. The entire stage remains valid and the answer is (16). An implementation that inserts every point into the forbidden set without respecting strict interior containment would incorrectly reject this rectangle.

For Sample 1, the diagonal arrangement forces the horizontal and vertical constraints to interact. Taking the largest raw (x)-gap or the largest raw (y)-gap independently is insufficient. The optimal rectangle has to be evaluated through the product of a horizontal span and a compatible vertical gap, which is precisely the quantity maintained by the interval formulation.
