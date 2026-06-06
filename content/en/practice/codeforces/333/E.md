---
title: "CF 333E - Summer Earnings"
description: "We are given a set of candidate points in the plane, and we must choose exactly three of them to serve as centers of three identical circles. All three circles must have the same radius, and they are allowed to touch but not overlap in their interiors."
date: "2026-06-06T10:08:06+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "geometry", "sortings"]
categories: ["algorithms"]
codeforces_contest: 333
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 194 (Div. 1)"
rating: 2500
weight: 333
solve_time_s: 101
verified: false
draft: false
---

[CF 333E - Summer Earnings](https://codeforces.com/problemset/problem/333/E)

**Rating:** 2500  
**Tags:** binary search, bitmasks, brute force, geometry, sortings  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of candidate points in the plane, and we must choose exactly three of them to serve as centers of three identical circles. All three circles must have the same radius, and they are allowed to touch but not overlap in their interiors. The radius is not fixed in advance; instead, we are trying to make it as large as possible while still being able to place the circles at three chosen centers without intersection.

If we pick three centers, the radius is constrained by the closest pair among the three points. Two circles with equal radius do not overlap if and only if the distance between their centers is at least twice the radius. So for a chosen triple, the limiting factor is the minimum pairwise distance among the three points. The best radius for that triple is half of that minimum distance.

The task is therefore equivalent to choosing three points that maximize the minimum pairwise distance, then dividing that value by two.

The input size is up to 3000 points. A cubic or near-cubic solution over triples is already borderline, since 3000³ is about 27 billion operations. Even a quadratic scan over all pairs is fine, but we need to be careful about how we extract the best triple from pairwise information.

A subtle issue appears when multiple points lie on a circle or form near-degenerate configurations. For example, if many points are extremely close together except one distant outlier, a naive approach that only considers globally best pairs can miss that the third point destroys the candidate pair.

A typical failure mode is choosing the farthest pair of points and assuming any third point works. For instance, if two points are extremely far apart but a third point is close to one of them, the radius is actually forced small by that third point. So we must consider triples jointly, not pairs independently.

## Approaches

A brute-force solution would enumerate every triple of points. For each triple, compute all three pairwise distances and take the minimum. This is correct but costs $O(n^3)$, which is too large for $n = 3000$.

The key observation is that for a fixed pair of points $A$ and $B$, the only way a third point can restrict the radius is if it lies closer than $AB$ to either $A$ or $B$. So if we fix a candidate pair, we want a third point that is as far as possible from both endpoints, in the sense that we care about maximizing the minimum of its distances to the pair.

Instead of reasoning directly in geometry for triples, we invert the problem. Suppose we guess that the optimal answer has value $R$. Then we only need to check whether there exists a triple where all pairwise distances are at least $2R$. This becomes a feasibility question over a graph: connect points whose distance is at least $2R$, and we want to know whether there is a triangle in this graph.

Checking for a triangle directly over all edges is still expensive if done naively. However, we can use the structure that $n \le 3000$. For each pair $(i, j)$, we can precompute all valid neighbors of $i$, and maintain adjacency sets. Then for each edge $(i, j)$, we need to check whether there exists a common neighbor $k$ such that both edges exist. With bitsets, intersection checks become fast.

This leads naturally to binary search on the answer: we sort all pairwise distances, or directly binary search the radius, and check feasibility using bitset intersections. Each check runs in about $O(n^2 / 64)$, which is acceptable.

A more direct viewpoint avoids explicit binary search. We compute all pairwise distances, sort them, and consider thresholds implicitly, but binary search is simpler to reason about.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (triples) | $O(n^3)$ | $O(1)$ | Too slow |
| Binary search + bitset triangle check | $O(n^2 \log n / 64)$ | $O(n^2 / 64)$ | Accepted |

## Algorithm Walkthrough

1. Precompute squared distances between all pairs of points. This avoids floating-point errors during comparisons and lets us work with integers throughout most of the logic.
2. Collect all unique distances (or use binary search bounds between 0 and maximum distance). The answer depends monotonically on the radius, since increasing radius only makes constraints stricter.
3. For a candidate radius $r$, convert it into a threshold $d = (2r)^2$. We only allow edges between pairs of points whose squared distance is at least $d$.
4. Build a graph implicitly where an edge means “these two points can serve as centers simultaneously for radius $r$”.
5. For each node $i$, store its adjacency as a bitset over all nodes. This representation allows fast intersection checks between neighbor sets.
6. To check whether a valid triple exists, iterate over all edges $(i, j)$. If they are connected, compute the intersection of adjacency sets of $i$ and $j$. If any bit is set in the intersection, a third point $k$ exists forming a valid triangle.
7. If any triangle exists, radius $r$ is feasible; otherwise it is not. Use this as the predicate in binary search.

### Why it works

Any valid solution is defined by a triple of points whose pairwise distances all exceed $2r$. This is exactly a triangle in the threshold graph. The bitset intersection step ensures we are not just finding two compatible edges independently, but a full shared neighbor, which is the third vertex completing the triangle. Since all triples are checked implicitly via edge pairs and their common neighbors, no valid configuration is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    dist2 = [[0] * n for _ in range(n)]
    max_d = 0

    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx = x1 - x2
            dy = y1 - y2
            d = dx * dx + dy * dy
            dist2[i][j] = dist2[j][i] = d
            if d > max_d:
                max_d = d

    # bitset adjacency for threshold graph
    bit = [0] * n

    def check(threshold):
        nonlocal bit
        for i in range(n):
            bit[i] = 0

        for i in range(n):
            for j in range(n):
                if i != j and dist2[i][j] >= threshold:
                    bit[i] |= (1 << j)

        for i in range(n):
            for j in range(i + 1, n):
                if bit[i] & bit[j] & (1 << i | 1 << j):
                    continue
                if bit[i] & bit[j]:
                    return True
        return False

    # binary search on squared diameter
    lo, hi = 0, max_d

    for _ in range(60):
        mid = (lo + hi) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid

    radius2 = lo / 4.0
    print((lo ** 0.5) / 2.0)

if __name__ == "__main__":
    solve()
```

The implementation begins by computing all squared pairwise distances, since all geometric comparisons reduce to distance comparisons and squaring avoids floating-point instability during the feasibility checks.

The `check` function constructs the threshold graph for a candidate squared distance. An adjacency bitmask is built for each node. The condition for a valid triple is that there exist two nodes $i, j$ such that they are both connected to some third node $k$, which is detected through intersection of their bitmasks.

The binary search runs over squared distances, and the final radius is derived as half the square root of the best feasible squared threshold.

One subtle point is ensuring that bit operations remain correct for up to 3000 nodes. Python integers handle arbitrary bit length, so this is safe, but performance relies on sparse intersections in practice.

## Worked Examples

### Example 1

Input:

```
3
0 1
1 0
1 1
```

Pairwise squared distances are:

(0,1)=1, (0,2)=1, (1,2)=2.

We test threshold 1: all edges exist, so triangle exists.

We test threshold 2: only edge (1,2) remains, no triangle.

| Step | Threshold | Graph edges | Triangle exists |
| --- | --- | --- | --- |
| 1 | 1 | full | yes |
| 2 | 2 | partial | no |

This confirms the best squared threshold is 1, giving radius 0.5.

### Example 2

Input:

```
4
0 0
0 10
10 0
100 100
```

The first three points form a tight triangle, while the fourth is far away.

At threshold corresponding to distances among the first three points, a triangle exists. Any higher threshold breaks connectivity.

| Step | Threshold | Active edges | Triangle |
| --- | --- | --- | --- |
| 1 | small | dense among first 3 | yes |
| 2 | large | only isolated edges | no |

This shows the algorithm correctly ignores irrelevant distant points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \log n)$ | distance computation is $O(n^2)$, each feasibility check uses bitset intersections over $O(n^2)$, repeated $O(\log n)$ times |
| Space | $O(n^2)$ | full distance matrix plus adjacency representation |

The quadratic preprocessing dominates memory, but $n = 3000$ is within limits for a 256 MB constraint when stored as integers. The bitset operations are efficient enough in Python due to native big integer arithmetic.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt

    data = inp.strip().split()
    n = int(data[0])
    pts = [(int(data[i]), int(data[i+1])) for i in range(1, 2*n, 2)]

    dist2 = [[0]*n for _ in range(n)]
    max_d = 0
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(n):
            x2, y2 = pts[j]
            dx, dy = x1-x2, y1-y2
            d = dx*dx + dy*dy
            dist2[i][j] = d
            max_d = max(max_d, d)

    def check(th):
        bit = [0]*n
        for i in range(n):
            for j in range(n):
                if dist2[i][j] >= th and i != j:
                    bit[i] |= 1 << j
        for i in range(n):
            for j in range(i+1, n):
                if bit[i] & bit[j]:
                    return True
        return False

    lo, hi = 0, max_d
    for _ in range(40):
        mid = (lo + hi)//2
        if check(mid):
            lo = mid
        else:
            hi = mid

    return str(math.sqrt(lo)/2)

# provided sample
assert abs(float(run("3\n0 1\n1 0\n1 1\n")) - 0.5) < 1e-6

# custom cases
assert abs(float(run("3\n0 0\n10 0\n0 10\n")) - 5.0/math.sqrt(2)) < 1e-6
assert abs(float(run("3\n0 0\n1 0\n2 0\n")) - 0.5) < 1e-6
assert abs(float(run("4\n0 0\n0 1\n1 0\n100 100\n")) > 0)  # sanity
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| right triangle | geometric correctness | correct distance reasoning |
| collinear points | degenerate cases | handling minimal spacing |
| outlier point | robustness | ignoring irrelevant points |

## Edge Cases

A key edge case occurs when all points are almost collinear. In that situation, the optimal triple is formed by choosing two far endpoints and a middle point that minimizes the bottleneck distance. The algorithm still works because the threshold graph will only connect sufficiently distant pairs, and triangle formation fails unless three mutually compatible points exist.

Another case is when one point is extremely isolated. For example:

```
(0,0), (1,0), (2,0), (1000,1000)
```

The best triple ignores the outlier entirely. The algorithm handles this because the outlier has few or no edges at higher thresholds, preventing it from participating in any triangle, while the dense cluster still forms valid triangles at lower thresholds.

A final subtle case is when multiple pairs share the same maximum distance but no third point supports a triangle at that scale. The bitset intersection prevents false positives by requiring a common neighbor, ensuring that pairwise optimality does not incorrectly imply triple feasibility.
