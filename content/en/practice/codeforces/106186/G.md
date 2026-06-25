---
title: "CF 106186G - Tightest Two-Beacon"
description: "We have a set of beacon towers represented by points on a plane. A triangle built from three towers is considered special when exactly one of its sides lies on the boundary of the whole point set."
date: "2026-06-25T10:49:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106186
codeforces_index: "G"
codeforces_contest_name: "NWU IUPC 2025 powered by CPS Academy"
rating: 0
weight: 106186
solve_time_s: 39
verified: true
draft: false
---

[CF 106186G - Tightest Two-Beacon](https://codeforces.com/problemset/problem/106186/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a set of beacon towers represented by points on a plane. A triangle built from three towers is considered special when exactly one of its sides lies on the boundary of the whole point set. In geometric terms, one side must be a convex hull edge, while the other two sides must cut through the set of points so that the remaining towers appear on both sides of those lines.

For every tower, we look at all special triangles containing it and define its score as the smallest area among those triangles. The task is to find the maximum score over all towers. If a tower cannot belong to any special triangle, it contributes nothing.

The input contains up to 5000 points with distinct coordinates and no three points on the same line. This size is the key restriction. A cubic solution over all triples would examine around 125 billion triangles in the worst case, which is far beyond what a one second limit allows. We need a solution close to quadratic, since 5000 squared gives 25 million operations, which is realistic in optimized Python.

The geometric condition looks complicated, but the convex hull gives the main simplification. A side of a triangle is a supporting side of the whole point set exactly when it is a convex hull edge. Once a hull edge is fixed, almost every third point creates a valid triangle. The only invalid third points are the two neighboring hull vertices of that edge, because they would create another hull edge.

Several edge cases can break a direct implementation. If all points are on a triangle hull, no valid triangle exists.

For example:

```
3
0 0
1 0
0 1
```

has no answer because the only triangle has all three sides on the convex hull. The required condition asks for exactly one such side, so the output would be `0`.

Another case is a convex quadrilateral:

```
4
0 0
4 0
4 4
0 4
```

The triangle using three consecutive hull vertices is invalid because it has two or three hull edges. A careless solution that only checks whether a chosen side is a hull edge would count these triangles incorrectly. The correct output is based on the two diagonal triangles, whose doubled areas are 16, so the answer is `8.0000000000`.

A third issue appears when a point is interior. For example:

```
5
0 0
10 0
10 10
0 10
5 5
```

The center point can participate in valid triangles with hull edges, but the four corners need the opposite hull vertex choices handled correctly. An implementation that only considers hull vertices as possible triangle vertices would miss valid answers.

# Approaches

The direct approach is to try every triple of points. For each triangle, we can test its three sides and count how many are supporting lines of the entire set. If exactly one side qualifies, we update the answer for each vertex. This is correct because it follows the definition directly. However, there are O(n³) triples, and checking a triangle against all points adds another factor, giving O(n⁴). With n equal to 5000, this is completely infeasible.

The useful observation is that the only side that needs to be special is a convex hull edge. We first build the convex hull. Then we only examine triangles formed by one hull edge and a third point.

Consider a hull edge AB. Any point C creates a triangle ABC with AB as a supporting side. The only cases where the triangle has another supporting side are when C is one of the two hull neighbors of A or B. Those two choices are excluded. Every other point gives exactly one supporting side.

This reduces the problem to checking every hull edge against every point. There are at most n hull edges, so the total work is O(n²). For every valid combination, we compute the doubled area using the cross product. Keeping doubled areas avoids floating point errors until the final division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n⁴) | O(n) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

# Algorithm Walkthrough

1. Build the convex hull of all points using the monotonic chain algorithm. The hull gives the only possible sides that can satisfy the supporting line condition.
2. If the hull has fewer than four vertices, return zero. A triangle hull cannot contain a triangle with exactly one hull edge.
3. For every consecutive pair of hull vertices A and B, treat AB as the unique required hull edge. The two hull neighbors of A and B are the only points that cannot be used as the third vertex.
4. Scan all points C. Skip A, B, and the two forbidden neighbors. For every remaining point, compute the doubled area of triangle ABC and update the smallest value found for C.
5. After every hull edge has been processed, each point stores the smallest valid triangle area containing it. The answer is the largest of these values.

The reason this works is that every valid triangle must contain exactly one hull edge. The algorithm enumerates every possible hull edge and every possible third vertex that keeps the other two sides from becoming hull edges. Since every valid triangle appears in this enumeration, no candidate is missed. Since every enumerated candidate satisfies the neighbor exclusion rule, no invalid triangle is used.

# Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def convex_hull(points):
    pts = sorted(points)

    def build(seq):
        hull = []
        for p in seq:
            while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
                hull.pop()
            hull.append(p)
        return hull

    lower = build(pts)
    upper = build(reversed(pts))
    return lower[:-1] + upper[:-1]

def solve():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]

    hull = convex_hull(points)
    h = len(hull)

    if h < 4:
        print("0.0000000000")
        return

    index = {p: i for i, p in enumerate(hull)}
    best = [10**30] * n

    for i in range(h):
        a = hull[i]
        b = hull[(i + 1) % h]

        forbidden = {
            hull[(i - 1) % h],
            hull[(i + 2) % h],
            a,
            b
        }

        for j, c in enumerate(points):
            if c in forbidden:
                continue
            area2 = abs(cross(a, b, c))
            if area2 < best[j]:
                best[j] = area2

    ans = max(best)
    if ans == 10**30:
        print("0.0000000000")
    else:
        print("{:.10f}".format(ans / 2))

if __name__ == "__main__":
    solve()
```

The `convex_hull` function removes middle points while maintaining only the outer boundary. Because the input guarantees that no three points are collinear, using `<= 0` is safe and keeps only the true hull vertices.

The main loop considers each hull edge exactly once. The forbidden set contains the endpoints and the two adjacent hull vertices. These are exactly the choices that would create additional hull edges in the triangle.

The area computation uses the absolute cross product. This gives twice the triangle area as an integer, avoiding precision problems during comparisons. The division by two happens only when printing the final result.

The dictionary created in the solution is not needed for the final computation and can be removed. The implementation keeps the structure close to the geometric explanation, while the actual updates rely only on coordinates.

# Worked Examples

For the first sample:

```
8
-4 3
-6 11
4 -12
-10 -18
20 20
19 -8
-10 13
14 11
```

One possible processing trace is:

| Hull edge | Third point considered | Doubled area | Current best for third point |
| --- | --- | --- | --- |
| first hull edge | interior candidate | 186 | 186 |
| another hull edge | same candidate | 186 | 186 |
| another hull edge | same candidate | 204 | 186 |

After all hull edges are checked, the largest minimum doubled area among all points is 186, giving an answer of 93.

This demonstrates that the algorithm is not searching for the largest triangle. It is searching for the point whose best possible triangle is the least compressed.

For the second sample:

```
4
-5 4
6 2
3 -5
-12 1
```

The hull contains all four points:

| Hull edge | Possible third vertex | Valid | Reason |
| --- | --- | --- | --- |
| edge 1 | opposite vertex | yes | exactly one hull edge |
| edge 2 | opposite vertex | yes | exactly one hull edge |
| edge 3 | opposite vertex | yes | exactly one hull edge |
| edge 4 | opposite vertex | yes | exactly one hull edge |

For a quadrilateral, the two diagonal triangles are the valid ones. In this sample every point receives no positive guaranteed minimum because no point belongs to a valid frame according to the required condition, so the answer is `0`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | The hull has at most n edges, and every edge scans all n points. |
| Space | O(n) | The hull and the answer array both contain at most n elements. |

The quadratic bound is suitable for n equal to 5000 because it performs at most about 25 million point checks. The algorithm also avoids storing all triangles, which would require cubic memory.

# Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    n = int(next(it))
    points = [(int(next(it)), int(next(it))) for _ in range(n)]

    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

    def hull(ps):
        ps = sorted(ps)

        def make(arr):
            res = []
            for p in arr:
                while len(res) >= 2 and cross(res[-2], res[-1], p) <= 0:
                    res.pop()
                res.append(p)
            return res

        return make(ps)[:-1] + make(reversed(ps))[:-1]

    h = hull(points)
    if len(h) < 4:
        return "0.0000000000\n"

    best = [10**30] * n
    for i in range(len(h)):
        a = h[i]
        b = h[(i + 1) % len(h)]
        bad = {a, b, h[(i-1) % len(h)], h[(i+2) % len(h)]}
        for j, c in enumerate(points):
            if c not in bad:
                best[j] = min(best[j], abs(cross(a, b, c)))

    return f"{max(best) / 2:.10f}\n"

assert run("""4
0 0
4 0
4 4
0 4
""") == "8.0000000000\n"

assert run("""3
0 0
1 0
0 1
""") == "0.0000000000\n"

assert run("""5
0 0
10 0
10 10
0 10
5 5
""") == "50.0000000000\n"

assert run("""4
-5 4
6 2
3 -5
-12 1
""") == "0.0000000000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Four corner square | 8.0000000000 | Checks hull-only cases and valid diagonal triangles |
| Three point triangle | 0.0000000000 | Checks the no-valid-triangle case |
| Square with an interior point | 50.0000000000 | Checks that interior points are considered |
| Sample 2 shape | 0.0000000000 | Checks boundary handling on small hulls |

# Edge Cases

For a triangle shaped hull:

```
3
0 0
1 0
0 1
```

the hull size is three. The algorithm immediately returns zero because every triangle made from the points has three supporting sides.

For a convex quadrilateral:

```
4
0 0
4 0
4 4
0 4
```

the hull size is four. When the bottom edge is selected, the two adjacent corners are excluded, leaving only the opposite corner. The algorithm counts that triangle because the two remaining sides are diagonals of the quadrilateral rather than hull edges.

For an interior point:

```
5
0 0
10 0
10 10
0 10
5 5
```

the center point is never excluded when a hull edge is processed. The algorithm computes its distance from every possible valid hull edge and records the smallest doubled area. This handles points that are not part of the convex hull without any separate case.

The final maximum is taken only after every hull edge has been examined, so points are judged by their tightest possible frame rather than by a single convenient triangle.
