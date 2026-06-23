---
title: "CF 105487A - Box"
description: "A rectangular box is placed in 3D space with its bottom face lying flat on a known horizontal plane. The height of the box is given, so the top face is just a vertical translation of the bottom face."
date: "2026-06-23T19:40:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105487
codeforces_index: "A"
codeforces_contest_name: "2024 China Collegiate Programming Contest (CCPC) Female Onsite (2024\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a)"
rating: 0
weight: 105487
solve_time_s: 80
verified: true
draft: false
---

[CF 105487A - Box](https://codeforces.com/problemset/problem/105487/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

A rectangular box is placed in 3D space with its bottom face lying flat on a known horizontal plane. The height of the box is given, so the top face is just a vertical translation of the bottom face. The bottom rectangle is specified indirectly: instead of giving all four corners, we are given two opposite corners on the same horizontal plane. From this, the full rectangle is determined, aligned with the x and y axes.

Each query gives a point in space, and we must determine whether this point lies inside or on the surface of the box.

The structure is therefore simple in geometry: a 3D axis-aligned box whose base is an axis-aligned rectangle in the xy-plane, and whose vertical extent is fixed by the height parameter.

The constraints are small, with at most one thousand queries. This immediately rules out anything beyond constant time processing per query. Any solution that attempts geometric decomposition per query or simulation over volume would be unnecessary overhead. The problem reduces to extracting interval boundaries once, then answering each query with a fixed number of comparisons.

A subtle edge case comes from how the base rectangle is specified. The two given points are opposite corners, but nothing guarantees ordering, so either coordinate can be smaller or larger. A naive implementation that assumes ordered endpoints will fail on swapped inputs. Another corner case is when the height is zero, which collapses the box into a flat rectangle in 3D space. Points exactly on that plane must still be considered inside.

## Approaches

A brute-force interpretation would try to reconstruct all eight vertices of the box and then test whether a point is inside by checking it against each face or performing a more general point-in-polyhedron test. This is correct but overkill. Even if implemented carefully, it introduces unnecessary geometric reasoning about faces and normals, while the structure of the box already guarantees axis alignment.

The key observation is that the box is fully described by independent intervals along each axis. The bottom rectangle defines an interval in x and an interval in y. The height defines an interval in z. Once these ranges are extracted, each query becomes a simple containment test in three independent one-dimensional segments.

The brute-force approach spends effort reconstructing geometry that is not needed. The optimized approach recognizes that the problem is separable along axes, reducing everything to three interval checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q) geometry per query, effectively O(q) with large constant | O(1) | Unnecessary but accepted |
| Optimal | O(q) | O(1) | Accepted |

## Algorithm Walkthrough

1. Extract the horizontal bounds of the box from the two given diagonal points by taking minimum and maximum of their x-coordinates and y-coordinates. This ensures correctness regardless of input order.
2. Compute the vertical bounds as the interval starting from the base plane z0 up to z0 + h. This defines the full height of the box.
3. For each query point, compare its x-coordinate against the precomputed x-interval. If it lies outside, the point cannot be inside the box.
4. If the x-coordinate is valid, compare the y-coordinate against the y-interval. If it fails here, it is outside as well.
5. If both horizontal checks pass, compare the z-coordinate against the vertical interval. If it lies within this range, the point is inside or on the boundary, otherwise it is outside.

The ordering of checks is not important for correctness, but doing horizontal checks first slightly reduces work in practice since many points are rejected early.

### Why it works

The box is axis-aligned, so membership in the 3D region is equivalent to simultaneous membership in three independent 1D intervals. There is no coupling between x, y, and z constraints. Any point inside must satisfy all three constraints, and any point failing even one constraint lies outside the Cartesian product of those intervals, which is exactly the box.

## Python Solution

```python
import sys
input = sys.stdin.readline

z0, h, u0, v0, u1, v1 = map(int, input().split())

x_min = min(u0, u1)
x_max = max(u0, u1)
y_min = min(v0, v1)
y_max = max(v0, v1)

z_min = z0
z_max = z0 + h

q = int(input())
out = []

for _ in range(q):
    x, y, z = map(int, input().split())

    if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
        out.append("YES")
    else:
        out.append("NO")

print("\n".join(out))
```

The implementation begins by normalizing the rectangle coordinates, since the two diagonal points may be given in any order. This step prevents incorrect interval construction when u0 is greater than u1 or v0 is greater than v1.

The vertical interval is constructed directly from the base height and box height. Since the box extends upward from the base plane, there is no ambiguity in ordering here.

Each query is answered by a direct three-way interval check. The comparisons are inclusive because boundary points are considered inside the box.

A common mistake in implementations of this type is forgetting that equality is allowed on all faces, which would incorrectly reject points lying exactly on edges or faces.

## Worked Examples

We use the sample input:

Input:

z0 = 1, h = 1, bottom corners (u0,v0)=(-1,-1), (u1,v1)=(1,1)

So:

x in [-1, 1]

y in [-1, 1]

z in [1, 2]

Query processing:

| Query (x,y,z) | x check | y check | z check | Result |
| --- | --- | --- | --- | --- |
| (-1,-1,1) | inside | inside | inside | YES |
| (0,0,2) | inside | inside | inside | YES |
| (1,2,2) | inside | outside | inside | NO |

The first query lies exactly on a corner of the base and at the bottom face, confirming that boundary inclusion is handled correctly. The second query is vertically at the top face center, still valid. The third query fails only in the y-coordinate, showing independence of axis constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each query is answered with constant-time comparisons across three axes |
| Space | O(1) | Only a fixed number of boundary variables are stored |

The constraints allow up to 1000 queries, so a linear scan with constant-time checks is easily within limits. The solution performs only simple integer comparisons per query and uses negligible memory.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    z0, h, u0, v0, u1, v1 = map(int, input().split())

    x_min = min(u0, u1)
    x_max = max(u0, u1)
    y_min = min(v0, v1)
    y_max = max(v0, v1)

    z_min = z0
    z_max = z0 + h

    q = int(input())
    out = []

    for _ in range(q):
        x, y, z = map(int, input().split())
        if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
            out.append("YES")
        else:
            out.append("NO")

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

assert run("""1 1 -1 -1 1 1
3
-1 -1 1
0 0 2
1 2 2
""") == "YES\nYES\nNO"

assert run("""0 0 5 5 5 5
2
5 5 0
5 5 1
""") == "YES\nNO"

assert run("""10 3 -2 -2 2 2
4
0 0 10
0 0 13
0 0 14
3 0 11
""") == "YES\nYES\nNO\nNO"

assert run("""-5 10 -1 -1 -1 -1
3
-1 -1 -5
-1 -1 5
-1 -1 6
""") == "YES\nYES\nNO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample case | YES YES NO | basic correctness |
| degenerate square | YES NO | h = 0 edge behavior |
| normal box | YES YES NO NO | interior vs boundary rejection |
| vertical shift | YES YES NO | negative z0 handling |

## Edge Cases

A key edge case occurs when the two diagonal points are given in reversed order. For example, if the input specifies (u0, v0) = (5, 5) and (u1, v1) = (-3, -2), the rectangle still spans from -3 to 5 in x and -2 to 5 in y. The algorithm handles this by taking minimum and maximum before comparison. Without this step, interval checks would fail and valid points would be rejected.

Another important case is when the height is zero. In this situation the box degenerates into a flat rectangle lying entirely on the plane z = z0. A point like (x, y, z0) must be accepted if it lies within the base rectangle. The algorithm naturally handles this because the vertical interval becomes [z0, z0], so only exact matches pass.

A final subtle case is boundary inclusion across all three axes. Points exactly on faces, edges, or vertices must be considered inside. The use of inclusive comparisons ensures that no valid boundary point is excluded, preserving correctness across all degenerate configurations.
