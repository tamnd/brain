---
title: "CF 102452F - Falling Objects"
description: "Each object is one of three convex solids: a cube, a sphere, or a regular tetrahedron. Its size, orientation, and horizontal release position are given. The objects are released one at a time, and each one falls only vertically."
date: "2026-08-12T08:28:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102452
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ICPC Asia Hong Kong Regional Contest"
rating: 0
weight: 102452
solve_time_s: 179
verified: true
draft: false
---

[CF 102452F - Falling Objects](https://codeforces.com/problemset/problem/102452/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

Each object is one of three convex solids: a cube, a sphere, or a regular tetrahedron. Its size, orientation, and horizontal release position are given. The objects are released one at a time, and each one falls only vertically. Once it first touches the ground or any object that has already landed, it stops permanently.

The rotation is a proper z-X-Z Euler rotation. After applying it, we only need the resulting fixed geometry. The question for object (i) is not where it was released, but the final (z)-coordinate of its highest point after the vertical fall.

The key difficulty is that an object can touch another object at an arbitrary point. A cube, for example, can first touch another cube along a face, at an edge, or at a vertex. A sphere can touch a face or edge of a polyhedron at a non-obvious point. Treating each solid as a single bounding box loses exactly the geometric information that determines the landing height.

The constraints make a quadratic simulation feasible. There are at most (1000) objects in total over all test cases, so considering every earlier object for every new object gives only about (5\cdot10^5) object pairs. The time limit is 5.5 seconds and the memory limit is 512 MB. We consequently want an (O(n^2)) simulation, but each pair must be handled with carefully chosen constant-time geometric operations rather than numerical falling simulation. The official problem page gives the same (n\le1000) bound and 5.5 second limit.

There are several subtle cases that expose careless implementations. A sphere released above the ground with radius (1) must have center height (1), so its highest point is (2). An implementation that interprets the radius as the highest point would print (1), which is wrong.

```
1
1
1 0 0 0 0 0 1
```

The answer is (2).

A second trap is tangency. Two unit spheres whose centers are horizontally (2) units apart touch exactly at one point. The second sphere still stops there, even though their horizontal projections only touch at the boundary.

```
1
2
1 0 0 0 0 0 1
1 0 0 0 2 0 1
```

Both highest points are (2). A strict intersection test that requires positive-area overlap would incorrectly let the second sphere fall through to the ground.

A third trap is rotation. A tetrahedron is not symmetric under arbitrary rotations, so its highest and lowest vertical offsets depend on the Euler angles. Using only its unrotated height gives the wrong landing position.

```
1
1
2 191 98 10 25 25 2
```

The correct highest point is approximately (1.9504473433), not the height of an unrotated tetrahedron.

## Approaches

A tempting brute-force simulation is to lower an object by small increments, test whether it intersects an earlier object, and stop when an intersection is detected. This is conceptually easy, but it cannot provide the required (10^{-4}) accuracy efficiently. If the vertical step is (10^{-5}), an object of height around (10^4) needs roughly (10^9) iterations. Even one such fall is already too expensive, and there can be (1000) falls.

A more respectable numerical approach is binary search on the center height. For every earlier object, we could test whether the two solids intersect at a proposed height and perform around 50 to 60 binary-search iterations. In the worst case this means roughly (60\cdot n(n-1)/2), or about 30 million pair tests for (n=1000), with every pair test itself requiring a substantial three-dimensional intersection computation. The constant becomes particularly unpleasant for cubes and tetrahedra.

The useful observation is that the first contact of two convex solids can always be represented by a small number of feature combinations. A polyhedron consists of vertices, edges, and triangular faces. When one polyhedron falls vertically onto another, the first contact is represented by a moving vertex touching a static face, a moving face touching a static vertex, or two edges whose horizontal projections meet. For spheres, the analogous cases are point-sphere, line-sphere, plane-sphere, and sphere-sphere. This feature decomposition is also the standard geometric organization used in detailed solutions of this problem.

That changes the problem completely. We do not have to search over the falling height. For every possible contact feature, we calculate directly the center height at which that contact happens, then take the maximum. The maximum is the first contact because the object starts at (+\infty) and moves downward.

For a point falling onto a triangular face, the horizontal coordinates are fixed, so the point reaches the face at the unique height obtained from the plane equation. For two edges, their horizontal projections determine the contact point, and the difference between their vertical coordinates gives the required center height. For a line and a sphere, the height function is a square root of a quadratic plus a linear term, which has a single maximum because it is concave. We can solve its derivative explicitly instead of performing numerical optimization.

The three-dimensional geometry is thus reduced to a fixed collection of elementary formulas. The official detailed geometry write-up describes the same ten primitive collision types and explains why cube and tetrahedron collisions can be reduced to them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Vertical step simulation | Unbounded for required precision | (O(n)) | Too slow |
| Binary search on height | (O(n^2\log \varepsilon^{-1})) | (O(n)) | Too much geometric work |
| Feature-based collision | (O(n^2)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Represent every cube or tetrahedron by its rotated vertices, its edges, and its triangular faces. A cube has 8 vertices, 12 edges, and 12 triangular faces after splitting each square face into two triangles. A tetrahedron has 4 vertices, 6 edges, and 4 faces. A sphere is represented by its center and radius. The tetrahedron coordinates can be chosen with side length one and then scaled by the input size. The coordinates used below are centered at the geometric center.
2. Construct the z-X-z rotation matrix from the three input angles and rotate every polyhedron vertex. The rotation matrix is applied before translating the object to its given (x,y) position. The resulting (x,y) coordinates stay fixed during the fall, while every vertex receives the same unknown vertical translation. The standard z-X-z matrix used here is the one described in the detailed solution.
3. Before processing object (i), initialize its center height using the ground. If the lowest rotated vertex or point relative to the center has coordinate (z_{\min}), then the ground contact occurs at center height (-z_{\min}). For a sphere this is simply its radius.
4. Consider every earlier object as a possible obstacle. If the horizontal distance between the two centers is larger than the sum of their bounding radii, their horizontal projections cannot meet, so the pair can be skipped immediately. This is an exact rejection test, not an approximation.
5. For a polyhedron-polyhedron pair, test moving vertex against static face, moving face against static vertex, and moving edge against static edge. A vertex-face contact is obtained from a plane equation and a point-in-triangle test. A face-vertex contact is the same calculation with the roles reversed. An edge-edge contact is found from the intersection of the two horizontal line segments.
6. For a sphere-polyhedron pair, test sphere-vertex, sphere-edge, and sphere-face contacts. For the edge case, maximize the vertical contact height along the edge. For the face case, use the normal of the face, because the first sphere-plane contact occurs along a normal direction.
7. For two spheres, enlarge the static sphere radius by the moving sphere radius. The moving sphere then behaves like a point falling onto this enlarged sphere. If the horizontal distance is (d), the center height is
[
z_{\text{static}}+\sqrt{(r_1+r_2)^2-d^2}.
]
8. For every valid feature pair, update the current landing height with the largest candidate. A higher candidate means the moving object would touch that feature earlier during its downward motion.
9. Once the landing center height is known, translate all of the object's vertices by that height and store its final highest point. The next object sees this object as a completely static obstacle.
10. Process objects in chronological order and print the highest final vertex of every object. The previous objects never move again, so no later simulation can change an already computed answer.

### Why it works

At every stage, the current object moves only by a vertical translation. Consider its first contact with a previous convex object. A contact point lies on the boundary of each solid. For a polyhedron, a boundary point belongs to a vertex, edge, or face. If the contact is between interiors of two faces, their supporting planes coincide at the first contact and a vertex-face calculation captures the same height. If the contact involves an edge, the two horizontal edge projections intersect and the edge-edge calculation captures it. Sphere contacts reduce to the corresponding point, edge, or face cases because the sphere's surface point responsible for first contact is uniquely determined by the vertical direction or the face normal.

Thus every possible first contact is represented by one of the tested feature pairs. Each feature routine calculates the exact center height at which that contact occurs. Taking their maximum gives the highest possible contact height, which is exactly the first collision encountered while falling from (+\infty). The invariant is that after processing object (i), its stored center height is the true height at which it first touches the already frozen sculpture, and all of its stored geometry is at its final position.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

EPS = 1e-9
NEG = -1e100

def cross2(ax, ay, bx, by):
    return ax * by - ay * bx

def inside_triangle(p, a, b, c):
    abx, aby = b[0] - a[0], b[1] - a[1]
    bcx, bcy = c[0] - b[0], c[1] - b[1]
    cax, cay = a[0] - c[0], a[1] - c[1]

    apx, apy = p[0] - a[0], p[1] - a[1]
    bpx, bpy = p[0] - b[0], p[1] - b[1]
    cpx, cpy = p[0] - c[0], p[1] - c[1]

    x1 = cross2(abx, aby, apx, apy)
    x2 = cross2(bcx, bcy, bpx, bpy)
    x3 = cross2(cax, cay, cpx, cpy)

    scale = max(
        1.0,
        math.hypot(abx, aby) * math.hypot(apx, apy),
        math.hypot(bcx, bcy) * math.hypot(bpx, bpy),
        math.hypot(cax, cay) * math.hypot(cpx, cpy),
    )
    tol = EPS * scale

    return (x1 >= -tol and x2 >= -tol and x3 >= -tol) or (
        x1 <= tol and x2 <= tol and x3 <= tol
    )

def plane_of(tri):
    a, b, c = tri
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]

    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    d = nx * a[0] + ny * a[1] + nz * a[2]
    return nx, ny, nz, d

def point_plane(moving_p, static_tri):
    a, b, c = static_tri
    if not inside_triangle(moving_p, a, b, c):
        return NEG

    nx, ny, nz, d = plane_of(static_tri)
    if abs(nz) < EPS:
        return NEG

    z = (d - nx * moving_p[0] - ny * moving_p[1]) / nz
    return z - moving_p[2]

def plane_point(moving_tri, static_p):
    if not inside_triangle(static_p, moving_tri[0], moving_tri[1], moving_tri[2]):
        return NEG

    nx, ny, nz, d = plane_of(moving_tri)
    if abs(nz) < EPS:
        return NEG

    z = (d - nx * static_p[0] - ny * static_p[1]) / nz
    return static_p[2] - z

def line_line(moving_l, static_l):
    a, b = moving_l
    c, d = static_l

    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]

    den = cross2(rx, ry, sx, sy)
    qx, qy = c[0] - a[0], c[1] - a[1]

    if abs(den) > EPS:
        t = cross2(qx, qy, sx, sy) / den
        u = cross2(qx, qy, rx, ry) / den

        if t < -EPS or t > 1.0 + EPS or u < -EPS or u > 1.0 + EPS:
            return NEG

        zm = a[2] + t * (b[2] - a[2])
        zs = c[2] + u * (d[2] - c[2])
        return zs - zm

    if abs(cross2(qx, qy, rx, ry)) > EPS:
        return NEG

    rr = rx * rx + ry * ry
    if rr < EPS:
        return NEG

    tc = ((c[0] - a[0]) * rx + (c[1] - a[1]) * ry) / rr
    td = ((d[0] - a[0]) * rx + (d[1] - a[1]) * ry) / rr

    lo = max(0.0, min(tc, td))
    hi = min(1.0, max(tc, td))

    if lo > hi + EPS:
        return NEG

    ans = NEG

    for t in (lo, hi):
        x = a[0] + rx * t
        y = a[1] + ry * t

        ss = sx * sx + sy * sy
        if ss < EPS:
            continue

        u = ((x - c[0]) * sx + (y - c[1]) * sy) / ss
        if u < -EPS or u > 1.0 + EPS:
            continue

        zm = a[2] + t * (b[2] - a[2])
        zs = c[2] + u * (d[2] - c[2])
        ans = max(ans, zs - zm)

    return ans

def point_sphere(moving_p, sphere_center, radius):
    dx = moving_p[0] - sphere_center[0]
    dy = moving_p[1] - sphere_center[1]
    q = radius * radius - dx * dx - dy * dy

    if q < -EPS:
        return NEG

    return sphere_center[2] + math.sqrt(max(0.0, q)) - moving_p[2]

def sphere_point(sphere_center_xy, radius, static_p):
    dx = sphere_center_xy[0] - static_p[0]
    dy = sphere_center_xy[1] - static_p[1]
    q = radius * radius - dx * dx - dy * dy

    if q < -EPS:
        return NEG

    return static_p[2] + math.sqrt(max(0.0, q))

def line_sphere(moving_l, sphere_center, radius, moving_line=True):
    a, b = moving_l

    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]

    ax = a[0] - sphere_center[0]
    ay = a[1] - sphere_center[1]

    B = dx * dx + dy * dy

    if B < EPS:
        q = radius * radius - ax * ax - ay * ay
        if q < -EPS:
            return NEG
        top = math.sqrt(max(0.0, q))

        if moving_line:
            return sphere_center[2] + top - a[2]
        return a[2] + top

    t0 = -(ax * dx + ay * dy) / B
    min_d2 = ax * ax + ay * ay - B * t0 * t0

    if min_d2 > radius * radius + EPS:
        return NEG

    D = max(0.0, radius * radius - min_d2)
    width = math.sqrt(D / B)

    left = max(0.0, t0 - width)
    right = min(1.0, t0 + width)

    if left > right + EPS:
        return NEG

    def value(t):
        px = ax + dx * t
        py = ay + dy * t
        q = radius * radius - px * px - py * py
        if q < -EPS:
            return NEG

        root = math.sqrt(max(0.0, q))

        if moving_line:
            return sphere_center[2] + root - (a[2] + dz * t)
        return a[2] + dz * t + root

    ans = max(value(left), value(right))

    if D > EPS:
        if moving_line:
            qlinear = -dz
        else:
            qlinear = dz

        if abs(qlinear) > EPS:
            t = t0 + qlinear * math.sqrt(
                D / (B * (B + qlinear * qlinear))
            )
            if left - EPS <= t <= right + EPS:
                ans = max(ans, value(t))

    return ans

def plane_sphere(moving_tri, sphere_center, radius):
    nx, ny, nz, d = plane_of(moving_tri)
    norm = math.sqrt(nx * nx + ny * ny + nz * nz)

    if norm < EPS:
        return NEG

    ans = NEG

    for sign in (-1.0, 1.0):
        qx = sphere_center[0] + sign * radius * nx / norm
        qy = sphere_center[1] + sign * radius * ny / norm
        qz = sphere_center[2] + sign * radius * nz / norm

        p = (qx, qy, qz)

        if not inside_triangle(p, moving_tri[0], moving_tri[1], moving_tri[2]):
            continue

        nx2, ny2, nz2, d2 = plane_of(moving_tri)
        if abs(nz2) < EPS:
            continue

        plane_z = (d2 - nx2 * qx - ny2 * qy) / nz2
        ans = max(ans, qz - plane_z)

    return ans

def sphere_plane(center_xy, radius, static_tri):
    nx, ny, nz, d = plane_of(static_tri)
    norm = math.sqrt(nx * nx + ny * ny + nz * nz)

    if norm < EPS:
        return NEG

    ans = NEG

    for sign in (-1.0, 1.0):
        qx = center_xy[0] + sign * radius * nx / norm
        qy = center_xy[1] + sign * radius * ny / norm

        if not inside_triangle(
            (qx, qy, 0.0),
            static_tri[0],
            static_tri[1],
            static_tri[2],
        ):
            continue

        if abs(nz) < EPS:
            continue

        plane_z = (d - nx * qx - ny * qy) / nz
        center_z = plane_z - sign * radius * nz / norm
        ans = max(ans, center_z)

    return ans

class Cloud:
    __slots__ = (
        "typ", "x", "y", "r", "rel", "pts", "edges", "faces",
        "bound", "vmax", "minz", "top", "z"
    )

    def __init__(self, typ, alpha, beta, gamma, x, y, r):
        self.typ = typ
        self.x = float(x)
        self.y = float(y)
        self.r = float(r)
        self.z = 0.0

        if typ == 1:
            self.rel = []
            self.pts = []
            self.edges = []
            self.faces = []
            self.bound = float(r)
            self.vmax = float(r)
            self.minz = -float(r)
            self.top = 0.0
            return

        if typ == 0:
            h = 0.5
            base = [
                (-h, -h, -h),
                ( h, -h, -h),
                ( h,  h, -h),
                (-h,  h, -h),
                (-h, -h,  h),
                ( h, -h,  h),
                ( h,  h,  h),
                (-h,  h,  h),
            ]
            self.edges = [
                (0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 4),
                (0, 4), (1, 5), (2, 6), (3, 7),
            ]
            self.faces = [
                (0, 1, 2), (0, 2, 3),
                (4, 6, 5), (4, 7, 6),
                (0, 4, 5), (0, 5, 1),
                (1, 5, 6), (1, 6, 2),
                (2, 6, 7), (2, 7, 3),
                (3, 7, 4), (3, 4, 0),
            ]
        else:
            s3 = math.sqrt(3.0)
            s6 = math.sqrt(6.0)
            base = [
                (-0.5 / s3,  0.5, -0.5 / s6),
                (-0.5 / s3, -0.5, -0.5 / s6),
                ( 1.0 / s3,  0.0, -0.5 / s6),
                ( 0.0,       0.0,  1.5 / s6),
            ]
            self.edges = [
                (0, 1), (0, 2), (0, 3),
                (1, 2), (1, 3), (2, 3),
            ]
            self.faces = [
                (0, 1, 2),
                (0, 1, 3),
                (0, 2, 3),
                (1, 2, 3),
            ]

        a = math.radians(alpha)
        b = math.radians(beta)
        g = math.radians(gamma)

        ca, sa = math.cos(a), math.sin(a)
        cb, sb = math.cos(b), math.sin(b)
        cg, sg = math.cos(g), math.sin(g)

        # Active z-X-z rotation.
        m00 = ca * cg - cb * sa * sg
        m01 = -ca * sg - cb * cg * sa
        m02 = sa * sb

        m10 = cg * sa + ca * cb * sg
        m11 = ca * cb * cg - sa * sg
        m12 = -ca * sb

        m20 = sb * sg
        m21 = cg * sb
        m22 = cb

        scale = float(r)
        rel = []

        for px, py, pz in base:
            px *= scale
            py *= scale
            pz *= scale

            rx = m00 * px + m01 * py + m02 * pz
            ry = m10 * px + m11 * py + m12 * pz
            rz = m20 * px + m21 * py + m22 * pz

            rel.append((self.x + rx, self.y + ry, rz))

        self.rel = rel
        self.pts = list(rel)

        self.bound = 0.0
        self.vmax = 0.0
        self.minz = float("inf")

        for p in rel:
            dx = p[0] - self.x
            dy = p[1] - self.y
            self.bound = max(self.bound, math.hypot(dx, dy))
            self.vmax = max(self.vmax, abs(p[2]))
            self.minz = min(self.minz, p[2])

        self.top = self.z + max(p[2] for p in self.pts)

    def set_height(self, z):
        self.z = z
        if self.typ == 1:
            self.top = z + self.r
            return

        self.pts = [
            (p[0], p[1], p[2] + z)
            for p in self.rel
        ]
        self.top = z + max(p[2] for p in self.rel)

def collision(moving, static):
    if moving.typ == 1 and static.typ == 1:
        dx = moving.x - static.x
        dy = moving.y - static.y
        rr = moving.r + static.r
        q = rr * rr - dx * dx - dy * dy
        if q < -EPS:
            return NEG
        return static.z + math.sqrt(max(0.0, q))

    ans = NEG

    if moving.typ == 1:
        sc = (static.x, static.y, static.z)

        for p in static.pts:
            ans = max(
                ans,
                sphere_point((moving.x, moving.y), moving.r, p)
            )

        for i, j in static.edges:
            ans = max(
                ans,
                line_sphere(
                    (static.pts[i], static.pts[j]),
                    (moving.x, moving.y, 0.0),
                    moving.r,
                    moving_line=False,
                )
            )

        for f in static.faces:
            tri = (static.pts[f[0]], static.pts[f[1]], static.pts[f[2]])
            ans = max(ans, sphere_plane((moving.x, moving.y), moving.r, tri))

        return ans

    if static.typ == 1:
        sc = (static.x, static.y, static.z)

        for p in moving.rel:
            ans = max(ans, point_sphere(p, sc, static.r))

        for i, j in moving.edges:
            ans = max(
                ans,
                line_sphere(
                    (moving.rel[i], moving.rel[j]),
                    sc,
                    static.r,
                    moving_line=True,
                )
            )

        for f in moving.faces:
            tri = (
                moving.rel[f[0]],
                moving.rel[f[1]],
                moving.rel[f[2]],
            )
            ans = max(ans, plane_sphere(tri, sc, static.r))

        return ans

    # Polyhedron versus polyhedron.
    for p in moving.rel:
        for f in static.faces:
            tri = (
                static.pts[f[0]],
                static.pts[f[1]],
                static.pts[f[2]],
            )
            ans = max(ans, point_plane(p, tri))

    for f in moving.faces:
        tri = (
            moving.rel[f[0]],
            moving.rel[f[1]],
            moving.rel[f[2]],
        )
        for p in static.pts:
            ans = max(ans, plane_point(tri, p))

    for i, j in moving.edges:
        ml = (moving.rel[i], moving.rel[j])
        for k, l in static.edges:
            sl = (static.pts[k], static.pts[l])
            ans = max(ans, line_line(ml, sl))

    return ans

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        n = int(input())

        clouds = []

        for _ in range(n):
            typ, alpha, beta, gamma, x, y, r = map(int, input().split())

            cur = Cloud(typ, alpha, beta, gamma, x, y, r)

            # Ground contact.
            if typ == 1:
                ground_z = r
            else:
                ground_z = -cur.minz

            best = ground_z

            # Higher static objects are more likely to determine the answer.
            previous = sorted(
                clouds,
                key=lambda c: c.top,
                reverse=True,
            )

            for old in previous:
                # No point of old can force the center above this bound.
                if old.top + cur.vmax <= best + 1e-10:
                    break

                dx = cur.x - old.x
                dy = cur.y - old.y

                if dx * dx + dy * dy > (
                    cur.bound + old.bound
                ) ** 2 + 1e-8:
                    continue

                h = collision(cur, old)
                if h > best:
                    best = h

            cur.set_height(best)
            clouds.append(cur)
            out.append(f"{cur.top:.15f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `Cloud` constructor first creates the canonical geometry and then applies the z-X-z rotation. Keeping the vertices relative to the center is useful because the unknown quantity during collision detection is exactly the common vertical translation.

For polyhedra, `rel` stores the rotated vertices with the requested (x,y) translation but with center height zero. Once an object lands, `set_height` adds the final center height to every vertex. The `top` field then directly gives the required answer.

The three elementary planar routines are `point_plane`, `plane_point`, and `line_line`. A point-face contact is valid only when the point's horizontal projection belongs to the triangular face. The plane's (z)-coordinate at that horizontal position follows directly from its equation. The edge routine handles both ordinary crossing and collinear overlap, which matters because touching at a boundary is a valid collision.

The sphere routines use the same vertical-contact idea. A point touching a sphere uses the upper hemisphere for a falling point and the lower hemisphere for a falling sphere. The line-sphere routine deserves special attention. After parameterizing the line by (t), the horizontal distance squared is quadratic in (t), so the vertical contact height has the form
[
\sqrt{D-B(t-t_0)^2}+qt+c.
]
This function is concave on its valid interval. Its stationary point can be written directly as
[
t=t_0+q\sqrt{\frac{D}{B(B+q^2)}}.
]
Checking that point together with the interval endpoints gives the exact maximum without a ternary search.

The face-sphere routines use the face normal. At the first sphere-plane contact, the radius vector is parallel to the plane normal, so only the two points obtained by moving the sphere center by one radius along the normal need to be considered. This is the same geometric reduction described in the detailed solution.

The processing loop also contains two exact pruning rules. The horizontal bounding-radius test rejects objects whose projections cannot meet. The vertical test stops scanning older objects once `old.top + cur.vmax` is no higher than the current best answer. Since the previous objects are processed in decreasing top height, every later object is no higher and can also be rejected.

Python uses double-precision floating point through its `float` type. No integer overflow is involved because the geometry is evaluated with floating-point arithmetic, and the input coordinates are small enough that the squared distances remain comfortably representable.

## Worked Examples

### Sample 1

The first test case contains a cube followed by a sphere.

```
2
0 45 90 270 0 0 2
1 11 45 14 0 0 1
```

For the cube, the ground is the only obstacle.

| Object | Shape | Ground center height | Best collision | Final center height | Highest point |
| --- | --- | --- | --- | --- | --- |
| 1 | Cube, side 2 | 1.000000 | none | 1.000000 | 2.000000 |
| 2 | Sphere, radius 1 | 1.000000 | 3.000000 | 3.000000 | 4.000000 |

The first cube has vertical offsets (-1) and (1), so its center stops at (z=1). Its highest point is (2). The sphere's horizontal position is the same as the cube's center. The highest point of the cube is (2), and the sphere has radius (1), so its center must reach (3) before touching the cube. Its highest point is consequently (4).

This demonstrates the invariant that the answer for an object is the maximum valid contact height, not the minimum height at which any geometric feature could intersect.

### Sample 2

The second test case places a rotated cube at the origin and a very large sphere at ((8,9)).

```
2
0 45 90 0 0 0 2
1 112 345 67 8 9 99
```

The trace is:

| Object | Shape | Ground center height | Previous-object candidate | Final center height | Highest point |
| --- | --- | --- | --- | --- | --- |
| 1 | Cube, side 2 | 2.000000 | none | 2.000000 | 2.000000 |
| 2 | Sphere, radius 99 | 99.000000 | about 100.384662 | about 100.384662 | about 199.384662 |

The first cube has a rotated vertical extent of (2), so its highest point is (2). The second object is large enough that its horizontal projection reaches the cube. The sphere's center therefore stops above the cube rather than at the ground. Adding its radius gives the reported highest point, approximately (199.3846615614).

The example also demonstrates why a simple radius-only vertical approximation is insufficient. The exact horizontal distance to the previous object determines the sphere's contact height through a square root.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | Every object considers earlier objects, and each solid has only a constant number of vertices, edges, and faces |
| Space | (O(n)) | We store the final geometry of all landed objects |

The nominal worst case still examines every pair, but each pair contains only a constant number of geometric feature checks. The horizontal and vertical pruning rules substantially reduce the practical number of feature checks, especially when objects are separated or the current object has already found a high support. With (n\le1000) in total, the quadratic outer simulation is appropriate for the 5.5 second limit. The original contest page confirms these constraints.

## Test Cases

The following tests use the `solve()` function from the solution above. Floating-point output is checked numerically rather than by comparing formatted strings.

```python
# Save the solution above as solution.py before running these tests.

import io
import sys
import math
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def values(inp: str):
    return [float(x) for x in run(inp).split()]

def assert_close(actual, expected, eps=1e-6):
    assert len(actual) == len(expected)
    for a, b in zip(actual, expected):
        assert abs(a - b) <= eps * max(1.0, abs(b)), (a, b)

# Provided sample.
sample = """\
3
2
0 45 90 270 0 0 2
1 11 45 14 0 0 1
2
0 45 90 0 0 0 2
1 112 345 67 8 9 99
1
2 191 98 10 25 25 2
"""

assert_close(
    values(sample),
    [
        2.000000000000001,
        4.000000000000001,
        2.000000000000001,
        199.384661561446364,
        1.950447343314250,
    ],
    1e-5,
)

# Minimum-size object, a unit sphere on the ground.
assert_close(
    values("""\
1
1
1 0 0 0 0 0 1
"""),
    [2.0],
)

# All equal values, three identical unit spheres stacked vertically.
assert_close(
    values("""\
1
3
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
"""),
    [2.0, 4.0, 6.0],
)

# Boundary tangency. The second sphere touches the first at exactly
# one point because their centers are two radii apart.
assert_close(
    values("""\
1
2
1 0 0 0 0 0 1
1 0 0 0 2 0 1
"""),
    [2.0, 2.0],
)

# Single tetrahedron with side length 2 and no rotation.
# Its height is 2*sqrt(2/3).
expected_tetra_top = 2.0 * math.sqrt(2.0 / 3.0)

assert_close(
    values("""\
1
1
2 0 0 0 0 0 2
"""),
    [expected_tetra_top],
)

# Maximum n. The spheres are far apart, so every one lands directly
# on the ground. This also exercises the horizontal-distance pruning.
n = 1000
parts = ["1", str(n)]
for i in range(n):
    parts.append(f"1 0 0 0 {3 * i} 0 1")

inp = "\n".join(parts) + "\n"
got = values(inp)

assert len(got) == n
assert all(abs(x - 2.0) < 1e-6 for x in got)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided three-case sample | `2, 4, 2, 199.3846615614, 1.9504473433` | Rotation, sphere contact, tetrahedron geometry, multiple cases |
| One unit sphere | `2` | Minimum-size object and ground contact |
| Three identical spheres at one position | `2, 4, 6` | Repeated stacking and chronological processing |
| Two unit spheres at distance 2 | `2, 2` | Exact tangency and non-strict intersection |
| Unrotated tetrahedron of side 2 | (2\sqrt{2/3}) | Tetrahedron coordinates and vertical extent |
| 1000 separated unit spheres | 1000 copies of `2` | Maximum input size and horizontal pruning |

## Edge Cases

The unit sphere case

```
1
1
1 0 0 0 0 0 1
```

starts with `best = 1`, because the lowest point of the sphere is one radius below its center. There are no previous objects, so the final center height remains (1), and the highest point is (1+1=2). This directly checks that the stored answer is the highest point rather than the center height.

The tangent-sphere case

```
1
2
1 0 0 0 0 0 1
1 0 0 0 2 0 1
```

first places the sphere center at (z=1). For the second sphere, the horizontal center distance is exactly (2), equal to the sum of the radii. The sphere-sphere formula has square-root term zero, so its center height is also (1). Its highest point is (2). The use of `<=` through the tolerance checks is what allows a single-point tangency to count as contact.

For repeated stacking,

```
1
3
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
```

the first sphere has center height (1). The second sees a static sphere at height (1), so its center reaches (3). The third sees the second sphere as the highest relevant obstacle and reaches center height (5). Their highest points are consequently (2,4,6). The vertical pruning rule also illustrates the ordering invariant, because once a higher object already determines the answer, sufficiently lower objects cannot improve it.

For the unrotated tetrahedron,

```
1
1
2 0 0 0 0 0 2
```

the lowest vertex is at
[
-\frac{2}{2\sqrt6}=-\frac1{\sqrt6},
]
so the center stops at (1/\sqrt6). The highest vertex is at
[
\frac{3}{\sqrt6},
]
and the final highest point is
[
\frac1{\sqrt6}+\frac3{\sqrt6}
=\frac4{\sqrt6}
=2\sqrt{\frac23}
\approx1.6329931619.
]
The result comes from the actual tetrahedron vertices, so no assumption about an axis-aligned bounding box is involved.

Finally, the maximum-size test uses (1000) spheres whose centers are three units apart. Their radii are one, so adjacent horizontal projections do not even touch. The bounding-radius test rejects every previous object before any expensive geometric calculation. Each sphere consequently lands at center height (1) and has highest point (2). This validates both the quadratic storage structure and the spatial pruning that keeps the constant factor manageable.
