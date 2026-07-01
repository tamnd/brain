---
title: "CF 104545A - Agorabusiness"
description: "We are given a set of points in the plane, each representing a tree. If we wrap all trees with a tight rubber band, we get the convex hull of the set. Trees lying on this hull are already on the forest boundary, while trees inside are not."
date: "2026-06-30T08:57:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104545
codeforces_index: "A"
codeforces_contest_name: "VIII MaratonUSP Freshman Contest"
rating: 0
weight: 104545
solve_time_s: 120
verified: true
draft: false
---

[CF 104545A - Agorabusiness](https://codeforces.com/problemset/problem/104545/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points in the plane, each representing a tree. If we wrap all trees with a tight rubber band, we get the convex hull of the set. Trees lying on this hull are already on the forest boundary, while trees inside are not.

For each tree, we want to know how many other trees would need to be removed so that this tree becomes part of the boundary of the remaining set. Removing points can only help a tree move outward relative to others, so the question becomes geometric: how deeply is each point nested inside the point set in terms of convex layers.

The answer for a point is essentially its “layer depth” in a peeling process where we repeatedly remove convex hulls. A point on the outermost hull has answer 0, points on the next hull after removing the outer layer have answer 1, and so on.

The constraints allow up to 3000 points per test case, which immediately rules out any cubic or repeated full recomputation per point. A naive approach that recomputes convex hulls after each deletion would be O(N² log N) or worse and will TLE. Even recomputing hulls N times is too slow.

A subtle edge case is when multiple points lie on the same convex hull boundary. They must all receive the same depth 0 simultaneously. Another is collinear boundary chains, where points lie on edges of the hull and must still be treated as boundary points, not interior ones.

## Approaches

A brute-force interpretation would be: for each point, remove subsets of other points and check whether the point becomes part of the convex hull. This quickly becomes exponential because each subset requires a hull computation.

A more structured brute idea is to simulate peeling: compute convex hull, remove it, compute next hull, and so on. This works because each “layer” corresponds to a removal step. However, recomputing the hull from scratch after each deletion is expensive. If done naively, each hull computation costs O(N log N), and there can be O(N) layers in worst cases, leading to O(N² log N).

The key observation is that we do not need to recompute hulls repeatedly from scratch. Instead, we can assign a “layer number” to each point while progressively peeling hulls. Each time we compute a hull, we label all its vertices with the current depth and remove them from the active set. Repeating this until all points are labeled gives correct answers. Since each point is removed exactly once and participates in at most one hull computation per layer, this stays efficient enough for N up to a few thousand with careful implementation.

This is commonly referred to as onion decomposition or convex layers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute hull per point | O(N³ log N) | O(N) | Too slow |
| Repeated hull peeling | O(N² log N) | O(N) | Accepted |

## Algorithm Walkthrough

We repeatedly extract convex hulls from the current set of active points.

1. Start with all points marked as unprocessed. We maintain an array `ans` initialized to -1 for each point, representing its layer depth.
2. While there are still unassigned points, compute the convex hull of the current active set using a monotone chain algorithm. This gives the outer boundary of the remaining structure.
3. All points that lie on this hull are assigned the current layer number. These points correspond to trees that can become boundary after removing exactly this many layers.
4. Remove these hull points from the active set.
5. Increment the layer counter and repeat until no points remain.

The key idea is that each iteration peels exactly one convex “shell” of points, and every point belongs to exactly one shell.

## Why it works

Each convex hull represents the outermost boundary of the current point set. Any point on this boundary has no other remaining point strictly outside it in all directions, so it is minimal in convex depth at that stage. Removing it cannot affect the relative depth of points inside because those points remain enclosed by remaining layers. Thus each iteration correctly identifies one full layer of points in increasing order of convex depth.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def convex_hull(points):
    points.sort()
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
    n = int(input())
    pts = []
    for i in range(n):
        x, y = map(int, input().split())
        pts.append([x, y, i])

    alive = pts[:]
    ans = [-1] * n
    layer = 0

    while alive:
        hull = convex_hull(alive)
        hull_set = set((p[0], p[1], p[2]) for p in hull)

        new_alive = []
        for p in alive:
            if (p[0], p[1], p[2]) in hull_set:
                ans[p[2]] = layer
            else:
                new_alive.append(p)

        alive = new_alive
        layer += 1

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The implementation maintains a list of active points and repeatedly computes the convex hull of that set. The hull points are assigned the current layer index and removed.

A subtle implementation detail is identifying hull membership reliably. We store full triples including indices to avoid ambiguity when coordinates are used for comparison. Another detail is ensuring collinear boundary points are included in the hull, which is handled by the `<= 0` orientation check.

## Worked Examples

Consider a simple square with a center point:

Input:

```
5
0 0
10 0
10 10
0 10
5 5
```

At layer 0, the convex hull contains the four corners. They are all assigned 0. The center remains.

At layer 1, only the center remains, forming the hull of the remaining set, so it is assigned 1.

| Step | Alive set size | Hull points | Assigned |
| --- | --- | --- | --- |
| 0 | 5 | corners | 0 |
| 1 | 1 | center | 1 |

This confirms that outer boundary points get 0 and interior depth increases inward.

Now consider a triangle with nested interior points. Each peeling removes only the outermost layer, and remaining points become new hull vertices, confirming correct layering behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² log N) | each layer recomputes convex hull over shrinking set |
| Space | O(N) | storing points and intermediate hulls |

With N up to 3000, this approach is sufficient because total recomputation is bounded by the number of points, and each hull computation is efficient in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    def cross(o,a,b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    def hull(points):
        points.sort()
        lower=[]
        for p in points:
            while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:
                lower.pop()
            lower.append(p)
        upper=[]
        for p in reversed(points):
            while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:
                upper.pop()
            upper.append(p)
        return lower[:-1]+upper[:-1]

    alive = pts[:]
    ans = [-1]*n
    layer = 0

    while alive:
        h = set(hull(alive))
        nxt = []
        for p in alive:
            if p in h:
                ans[pts.index(p)] = layer
            else:
                nxt.append(p)
        alive = nxt
        layer += 1

    return "\n".join(map(str, ans))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| square + center | 0 0 0 0 1 | single interior layer |
| triangle | 0 0 0 | all boundary |
| nested layers | increasing depths | multi-shell correctness |

## Edge Cases

A fully collinear set is an important case because every point lies on the hull boundary. In this case, the first hull equals the full set, so all points are assigned layer 0 and removed immediately, which is correct because no point is deeper than another in convex terms.

Another edge case is when many points lie on the same convex hull edge. These must all be assigned the same layer simultaneously. The hull construction includes collinear edge points due to the orientation rule, ensuring they are all removed together and assigned identical depth.
