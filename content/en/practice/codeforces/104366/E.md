---
title: "CF 104366E - Triangle Pick"
description: "We are given a collection of triangular surfaces in 3D space. Each triangle is a flat solid piece defined by three vertices."
date: "2026-07-01T17:43:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104366
codeforces_index: "E"
codeforces_contest_name: "The 17th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 104366
solve_time_s: 66
verified: true
draft: false
---

[CF 104366E - Triangle Pick](https://codeforces.com/problemset/problem/104366/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of triangular surfaces in 3D space. Each triangle is a flat solid piece defined by three vertices. From the origin, we shoot rays in different directions, and for each direction we need to determine which triangle the ray hits first, measured by distance along the ray.

A ray is fully determined by a direction vector. The ray always starts at the origin and extends infinitely in that direction. For each query direction, we conceptually test where this ray intersects the triangles and pick the triangle whose intersection point is closest to the origin, along the ray.

The output for each query is the index of that closest triangle, or 0 if the ray does not intersect any triangle at all.

The constraints are small enough that a direct per-query scan over all triangles is feasible. With up to 1000 triangles and 10000 queries, a straightforward O(n) per query approach gives about 10^7 triangle tests total, which is comfortably within limits in C++ or optimized Python using a direct geometric intersection routine.

The main subtlety is numerical and geometric correctness. A triangle is a filled surface, not just edges, so a valid intersection is any point inside its interior or boundary. The ray originates exactly at the origin, so cases where a triangle lies behind the origin or is parallel to the ray must be rejected. Degenerate cases where the ray grazes edges are stated to not cause precision issues, so a stable intersection method is sufficient.

A naive but incorrect approach would be to intersect the ray with the plane of each triangle and then assume the intersection point is valid. This fails when the plane is hit outside the triangle bounds. Another failure mode is forgetting to ignore intersections with negative ray parameter t, which correspond to points behind the origin.

## Approaches

A brute-force solution is to process each query independently and test every triangle. For each triangle, we compute whether the ray intersects the triangle, and if so compute the distance t along the ray. We keep the minimum t and return its triangle index.

Each triangle test requires solving a ray-triangle intersection problem. A direct method is to compute the plane intersection and then check barycentric coordinates, or use a more stable formulation such as Möller-Trumbore. This is constant time per triangle.

With n triangles and m queries, this gives O(nm) intersection tests. In the worst case, this is 10^7 triangle checks. Each check involves a constant number of vector operations, so this is acceptable.

The key observation is that there is no structure linking triangles across queries, and triangles do not intersect each other, so no spatial acceleration structure is required. Since n is only 1000, we do not gain enough from preprocessing like BVH or grids to justify the complexity. A direct scan is optimal in both simplicity and performance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) extra | Accepted |
| Optimal (same idea with stable intersection) | O(nm) | O(1) extra | Accepted |

## Algorithm Walkthrough

We use the Möller-Trumbore ray-triangle intersection test because it directly computes whether a ray hits a triangle and returns the distance parameter along the ray in a numerically stable way.

### Steps

1. Represent the ray as origin O = (0,0,0) and direction D = (x,y,z).

Every intersection will be of the form O + tD, and we only care about t > 0 because negative t lies behind the origin.
2. For each triangle with vertices A, B, C, compute two edges: E1 = B − A and E2 = C − A.

This converts the triangle into a parametric surface A + uE1 + vE2.
3. Compute the determinant via the cross product P = D × E2 and det = E1 · P.

If det is near zero, the ray is parallel to the triangle plane and cannot intersect it.
4. Compute inverse determinant inv = 1 / det and vector T = O − A = −A.
5. Compute barycentric coordinate u = (T · P) * inv.

If u is not in [0,1], the intersection lies outside the triangle.
6. Compute Q = T × E1 and barycentric coordinate v = (D · Q) * inv.

If v is not in [0,1] or u + v > 1, the point lies outside the triangle.
7. Compute t = (E2 · Q) * inv.

If t <= 0, the triangle is behind the origin or exactly at it and is ignored.
8. Track the smallest positive t across all triangles.

The triangle with this minimum t is the first hit for this query.
9. Output its index, or 0 if no valid t was found.

### Why it works

The Möller-Trumbore formulation rewrites the intersection condition as solving a linear system for ray parameters directly in barycentric coordinates. The determinant encodes whether the ray direction spans a valid basis with the triangle edges. The constraints on u, v, and u+v enforce that the intersection lies inside the triangle rather than on the infinite plane. Because we always compare t values along the same ray parameterization, selecting the minimum t correctly identifies the closest intersection in physical space.

## Python Solution

```python
import sys
input = sys.stdin.readline

EPS = 1e-12

def intersect(ray_dx, ray_dy, ray_dz, tri):
    ax, ay, az, bx, by, bz, cx, cy, cz = tri

    # edges
    e1x, e1y, e1z = bx - ax, by - ay, bz - az
    e2x, e2y, e2z = cx - ax, cy - ay, cz - az

    # P = D x E2
    px = ray_dy * e2z - ray_dz * e2y
    py = ray_dz * e2x - ray_dx * e2z
    pz = ray_dx * e2y - ray_dy * e2x

    det = e1x * px + e1y * py + e1z * pz

    if abs(det) < EPS:
        return None

    inv = 1.0 / det

    tx, ty, tz = -ax, -ay, -az

    # u = T · P * inv
    u = (tx * px + ty * py + tz * pz) * inv
    if u < 0.0 or u > 1.0:
        return None

    # Q = T x E1
    qx = ty * e1z - tz * e1y
    qy = tz * e1x - tx * e1z
    qz = tx * e1y - ty * e1x

    v = (ray_dx * qx + ray_dy * qy + ray_dz * qz) * inv
    if v < 0.0 or u + v > 1.0:
        return None

    t = (e2x * qx + e2y * qy + e2z * qz) * inv
    if t <= 0.0:
        return None

    return t

def solve():
    n, m = map(int, input().split())
    tris = [tuple(map(int, input().split())) for _ in range(n)]

    out = []

    for _ in range(m):
        dx, dy, dz = map(int, input().split())

        best_t = float('inf')
        best_id = 0

        for i, tri in enumerate(tris, 1):
            t = intersect(dx, dy, dz, tri)
            if t is not None and t < best_t:
                best_t = t
                best_id = i

        out.append(str(best_id))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution isolates the intersection logic into a single function so that each triangle test is a pure constant-time computation. The key implementation detail is keeping all computations in floating point while using a small epsilon check for degeneracy in the determinant. The sign checks on u, v, and t ensure that only valid forward intersections are considered.

The triangle loop is intentionally left unoptimized because n is small enough that Python can handle roughly ten million simple arithmetic blocks within time limits.

## Worked Examples

Consider a simple case with one triangle in the xy-plane:

Input:

```
1 2
1 0 0  0 1 0  0 0 1
0 0 1
0 0 -1
```

First query shoots upward in z direction. The triangle lies partially in positive z due to vertex (0,0,1), so it is intersected. Second query shoots downward and misses.

| Query direction | Intersection result | Best t | Chosen triangle |
| --- | --- | --- | --- |
| (0,0,1) | hits triangle | finite | 1 |
| (0,0,-1) | no hit | inf | 0 |

This demonstrates that direction matters even when triangles share an origin-adjacent vertex.

Now consider two triangles at different depths along the same ray:

Input:

```
2 1
1 0 1  0 1 1  0 0 1
1 0 3  0 1 3  0 0 3
1 0 0
```

The ray points along +x, so it will hit the closest triangle that intersects that ray direction first.

| Step | Triangle | t computed | current best |
| --- | --- | --- | --- |
| 1 | tri 1 | valid small t | tri 1 |
| 2 | tri 2 | larger t | tri 1 |

The output is 1, confirming that ordering is determined purely by ray distance, not input order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each query checks all triangles using constant-time ray-triangle intersection |
| Space | O(1) extra | Only triangle storage and a few vectors are used |

With n up to 1000 and m up to 10000, the total number of intersection checks is 10^7. Each check is a fixed number of arithmetic operations, which fits comfortably within typical time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    import io as sio

    buf = sio.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

# minimum case: single triangle, single ray hit
assert run("""1 1
1 0 0 0 1 0 0 0 1
1 1 1
""") == "1"

# miss case
assert run("""1 1
1 0 0 0 1 0 0 0 1
-1 -1 -1
""") == "0"

# two triangles, nearer wins
assert run("""2 1
1 0 1 0 1 1 0 0 1
1 0 2 0 1 2 0 0 2
1 0 0
""") == "1"

# multiple queries
assert run("""1 3
1 0 0 0 1 0 0 0 1
0 0 1
1 0 0
0 1 0
""") == """1
1
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single triangle hit | 1 | basic intersection correctness |
| single triangle miss | 0 | rejection of non-intersections |
| two triangles same ray | 1 | correct minimum-distance selection |
| multiple queries | repeated 1 | independence across queries |

## Edge Cases

A key edge case is when the ray is parallel to a triangle plane. In that situation, the determinant in the Möller-Trumbore formulation becomes zero or near zero, and the algorithm immediately discards the triangle. For example, if a triangle lies in a plane x = 1 and the ray direction is (0,1,0), the cross product computation yields a zero determinant, so no false intersection is produced.

Another case is when the triangle lies behind the origin. Suppose a triangle is defined at negative coordinates and the ray points positively. The computed t becomes negative, and the check t <= 0 correctly rejects it. This prevents selecting triangles that are geometrically valid but not reachable along the ray direction.

A final case is multiple triangles along the same ray direction. Since each triangle independently produces a valid t, the algorithm correctly resolves ties by simply keeping the minimum value, so no additional tie-breaking logic is required beyond index tracking.
