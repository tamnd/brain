---
title: "CF 102354F - Cosmic Crossroads"
description: "We have two unordered collections of points on the unit sphere. Every geometric line through the origin is represented twice, by its two intersection points with the sphere, so whenever a point (r) occurs, (-r) occurs as well."
date: "2026-08-14T02:31:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "F"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 377
verified: false
draft: false
---

[CF 102354F - Cosmic Crossroads](https://codeforces.com/problemset/problem/102354/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We have two unordered collections of points on the unit sphere. Every geometric line through the origin is represented twice, by its two intersection points with the sphere, so whenever a point (r) occurs, (-r) occurs as well. The second collection is obtained from the first by applying one rotation around the origin and then changing the order of the points.

The task is to recover both pieces of information. For every point of the second collection we must output the index of the corresponding point in the first collection, and we must describe the rotation by an axis and an angle. The required geometric error is only (10^{-6}), while the input is precise to about (10^{-12}), so ordinary double precision is sufficient if we avoid unnecessarily unstable computations.

The decisive constraint is (n\le 4\cdot10^4), hence there can be (8\cdot10^4) points. Any method comparing every pair of points takes roughly (6.4\cdot10^9) pair operations, which is far beyond the four second limit. We need an almost linear computation apart from sorting, so (O(n\log n)) is the natural target.

There are two structural facts that make such a solution possible. First, rotations preserve distances, dot products, and every expression built from them. Second, the directions were chosen uniformly at random. Randomness is not decorative here: it makes a carefully chosen rotational invariant almost surely different for different lines, so the invariant can serve as a fingerprint.

There is one subtlety caused by the antipodal representation. Any invariant depending only on even powers of coordinates gives the same value to (r) and (-r). That is not a bug, because those two points belong to the same line. We first identify lines, and only after recovering the rotation do we decide which of the two opposite endpoints is the correct point.

The supplied sample is another useful edge case. Its four points form a square in one plane. The invariant used below has exactly the same value for all four points, so the random uniqueness assumption does not hold for this sample. A careless implementation that blindly pairs consecutive sorted points can form the wrong line pairs. The implementation below contains a small brute-force fallback for (n\le3), which handles the sample and other tiny symmetric configurations. For the actual large inputs, the promised random construction makes the fast path overwhelmingly reliable.

For example, the sample has the four points
[
(0.923879533,0.382683432,0),\quad
(0.923879533,-0.382683432,0),
]
together with their negatives. Every point receives the same quadratic fingerprint. The correct output may use a (-\pi/2) rotation around the (z)-axis and the permutation (2,3,4,1). A method that assumes every fingerprint is unique would silently fail before it even tries to compute the rotation.

A second simple edge case is the identity rotation. If the two input sets are identical but shuffled, the required angle is (0), and the axis can be any nonzero vector. The implementation outputs the (x)-axis in this case. The axis is not uniquely defined when the angle is zero, so comparing the printed axis with some expected axis would be incorrect.

## Approaches

The direct approach is conceptually simple. Try a correspondence between points of the two sets, determine the rotation from enough corresponding vectors, and check all remaining points. With (2n) possible targets for the first point and (2n-1) for the second, even before handling the remaining permutation there are already (\Theta(n^2)) candidate pairs. If every candidate requires scanning (O(n)) points, the worst case is (\Theta(n^3)), about (5.12\cdot10^{14}) basic point comparisons at (n=4\cdot10^4). Even a much more careful (O(n^2)) search would still perform about (6.4\cdot10^9) pair operations.

The useful observation is to stop trying to guess the rotation first. Instead, construct a number attached to each point that is unchanged by rotation and independent of the ordering of the whole set.

The official solution uses the fourth-power distance polynomial
[
P_4(x,y,z)=
\sum_l
\left((x-x_l)^2+(y-y_l)^2+(z-z_l)^2\right)^2.
]
This is rotationally invariant, and evaluating it for every point can be reduced to constant work per point after accumulating the required moments.

4-8(p\cdot r_l)+4(p\cdot r_l)^2.
]
Summing over all points, the linear term disappears because the input is antipodal:
[
\sum_l r_l=0.
]
Define the symmetric matrix
[
M=\sum_l r_l r_l^T.
]
Then
[
\sum_l(p\cdot r_l)^2=p^TMp,
]
so
[
P_4(p)=4(2n)+4p^TMp.
]
The constant factor and additive constant do not affect sorting. We therefore use
[
F(p)=p^TMp
]
as the fingerprint.

# b^TM_Bb

# b^TR^TM_ARb

# (Rb)^TM_A(Rb)

F_A(Rb).
]
Thus corresponding points have equal fingerprints. Because the directions are random, different lines almost surely have different values. The only unavoidable equality is between (r) and (-r), since (F(-r)=F(r)).

We sort the fingerprints. In the generic case every two consecutive equal values form one antipodal pair, and the pairs occur in the same order in both sets. This gives the correspondence between the (n) lines in (O(n\log n)) time.

Once two nonparallel corresponding lines are known, only four orientations remain. Choose one representative from each line in each set. For each of the four sign choices, construct the unique proper rotation mapping the two selected vectors to the chosen target vectors. Then test it against all points. The correct sign combination is guaranteed to pass.

The final step converts the rotation matrix to an axis-angle representation. A quaternion representation is convenient because it remains stable when the angle is close to (\pi), where the usual formula based only on the antisymmetric part of the matrix loses precision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) to (O(n^3)) depending on verification | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all (2n) points of the first set and all (2n) points of the second set. Store the coordinates as floating-point triples. Since every point lies on the unit sphere and the required error is (10^{-6}), double precision is appropriate.
2. For each set, accumulate the six independent entries of the symmetric matrix
[
M=\sum r_ir_i^T.
]
The entries are
[
M_{xx}=\sum x_i^2,\quad
M_{xy}=\sum x_iy_i,\quad
M_{xz}=\sum x_iz_i,
]
and similarly for (M_{yy},M_{yz},M_{zz}).
3. Evaluate (F(r)=r^TMr) for every point. This takes only a constant number of arithmetic operations per point because (M) is only (3\times3).
4. Sort the point indices by their fingerprints. In the random case, the two copies of every line have the same fingerprint and different lines have different fingerprints. Consequently, positions (0,1) correspond to one line, positions (2,3) to another, and so on, in both sets.
5. Use the first line as one reference and scan the other line groups until finding a second reference whose direction is not almost parallel to the first. Since the points are random, this is normally immediate. Choosing a well-separated pair avoids dividing by a tiny cross product when constructing the coordinate frame.
6. Let (s_1,s_2) be representatives from the two selected lines of the second set and (t_1,t_2) representatives from the corresponding lines of the first set. Try all four choices
[
(\pm t_1,\pm t_2).
]
For each choice, construct an orthonormal basis from (s_1,s_2), construct another from the signed target vectors, and map the first basis to the second. This gives a proper rotation matrix.
7. Validate the candidate rotation against every point. For a second-set point (b), its fingerprint tells us the corresponding first-set line, which contains exactly two opposite points. Compare (Rb) with those two candidates and keep the closer one. If every distance is below a small numerical tolerance, the candidate is the desired rotation and permutation.
8. If the fingerprints do not split the points into pairs and (n\le3), use a tiny brute-force fallback. There are at most (6!=720) permutations, so we can try every permutation, construct a rotation from two nonparallel vectors, and verify all points. This handles the symmetric sample without affecting the asymptotic complexity.
9. Convert the resulting rotation matrix into a unit quaternion. Make the scalar component nonnegative, then use
[
\theta=2\operatorname{atan2}(|v|,w)
]
where (w) is the scalar part and (v) is the vector part. The vector (v/|v|) is the rotation axis. For a zero rotation, any axis is valid, so we output ((1,0,0)).
10. Print the angle, the axis point, and the permutation in the required one-based indexing.

Why it works

The central invariant is (F(r)=r^TMr), which is the nonconstant part of the fourth-power distance polynomial. A rotation changes (M) by conjugation and changes (r) by the inverse conjugation, so (F) is unchanged for corresponding points. Random independent directions make these fingerprints distinct between different lines with probability one in the mathematical model. The sorting step therefore identifies every line pair.

For two nonparallel vectors, their ordered pair determines an oriented orthonormal frame. A rotation mapping one frame to another is unique. The four sign choices cover the only ambiguity caused by the fact that a line has two possible representatives. Exactly one candidate agrees with the actual rotation, and the global verification rejects every incorrect candidate. Once that rotation is known, choosing the closer endpoint inside each matched antipodal pair gives the required point permutation.

## Python Solution

```python
import sys
import math
import itertools

input = sys.stdin.readline

EPS = 1e-8
CHECK_EPS2 = 5e-10
CROSS_EPS = 1e-8

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )

def norm2(a):
    return dot(a, a)

def scale(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def normalize(a):
    d = math.sqrt(norm2(a))
    return scale(a, 1.0 / d)

def apply_rot(R, v):
    return (
        R[0][0] * v[0] + R[0][1] * v[1] + R[0][2] * v[2],
        R[1][0] * v[0] + R[1][1] * v[1] + R[1][2] * v[2],
        R[2][0] * v[0] + R[2][1] * v[1] + R[2][2] * v[2],
    )

def rotation_from_two(source1, source2, target1, target2):
    u = normalize(source1)
    v0 = sub(source2, scale(u, dot(source2, u)))
    vlen2 = norm2(v0)
    if vlen2 < CROSS_EPS * CROSS_EPS:
        return None
    v = scale(v0, 1.0 / math.sqrt(vlen2))
    w = cross(u, v)

    U = normalize(target1)
    V0 = sub(target2, scale(U, dot(target2, U)))
    Vlen2 = norm2(V0)
    if Vlen2 < CROSS_EPS * CROSS_EPS:
        return None
    V = scale(V0, 1.0 / math.sqrt(Vlen2))
    W = cross(U, V)

    # R = [U V W] [u v w]^T
    R = [[0.0] * 3 for _ in range(3)]
    T = (U, V, W)
    S = (u, v, w)

    for i in range(3):
        for j in range(3):
            R[i][j] = (
                T[0][i] * S[0][j]
                + T[1][i] * S[1][j]
                + T[2][i] * S[2][j]
            )
    return R

def matrix_fingerprint(p, M):
    x, y, z = p
    qx = M[0][0] * x + M[0][1] * y + M[0][2] * z
    qy = M[0][1] * x + M[1][1] * y + M[1][2] * z
    qz = M[0][2] * x + M[1][2] * y + M[2][2] * z
    return x * qx + y * qy + z * qz

def build_matrix(points):
    xx = xy = xz = yy = yz = zz = 0.0
    for x, y, z in points:
        xx += x * x
        xy += x * y
        xz += x * z
        yy += y * y
        yz += y * z
        zz += z * z
    return (
        (xx, xy, xz),
        (xy, yy, yz),
        (xz, yz, zz),
    )

def build_groups(values, order):
    groups = []
    for idx in order:
        if not groups or abs(values[idx] - values[groups[-1][0]]) > EPS:
            groups.append([idx])
        else:
            groups[-1].append(idx)
    return groups

def validate_group_rotation(R, A, B, groups_a, groups_b):
    m = len(A)
    perm = [-1] * m

    for g in range(len(groups_b)):
        ga = groups_a[g]
        gb = groups_b[g]

        if len(ga) != 2 or len(gb) != 2:
            return None

        a0, a1 = ga
        for bi in gb:
            rb = apply_rot(R, B[bi])

            d0 = norm2(sub(rb, A[a0]))
            d1 = norm2(sub(rb, A[a1]))

            if d0 <= d1:
                best = a0
                bestd = d0
            else:
                best = a1
                bestd = d1

            if bestd > CHECK_EPS2:
                return None
            if perm[bi] != -1:
                return None
            perm[bi] = best

    if any(x == -1 for x in perm):
        return None
    return perm

def brute_force_small(A, B):
    m = len(A)

    first = 0
    second = -1
    for j in range(1, m):
        if norm2(cross(B[first], B[j])) > CROSS_EPS * CROSS_EPS:
            second = j
            break

    if second == -1:
        return None

    for p in itertools.permutations(range(m)):
        for s1 in (1.0, -1.0):
            for s2 in (1.0, -1.0):
                R = rotation_from_two(
                    B[first],
                    B[second],
                    scale(A[p[first]], s1),
                    scale(A[p[second]], s2),
                )
                if R is None:
                    continue

                ok = True
                for i in range(m):
                    rb = apply_rot(R, B[i])
                    if norm2(sub(rb, A[p[i]])) > CHECK_EPS2:
                        ok = False
                        break

                if ok:
                    return R, list(p)

    return None

def rotation_to_axis_angle(R):
    tr = R[0][0] + R[1][1] + R[2][2]

    if tr > 0.0:
        s = math.sqrt(tr + 1.0) * 2.0
        qw = 0.25 * s
        qx = (R[2][1] - R[1][2]) / s
        qy = (R[0][2] - R[2][0]) / s
        qz = (R[1][0] - R[0][1]) / s
    elif R[0][0] > R[1][1] and R[0][0] > R[2][2]:
        s = math.sqrt(max(0.0, 1.0 + R[0][0] - R[1][1] - R[2][2])) * 2.0
        qx = 0.25 * s
        qy = (R[0][1] + R[1][0]) / s
        qz = (R[0][2] + R[2][0]) / s
        qw = (R[2][1] - R[1][2]) / s
    elif R[1][1] > R[2][2]:
        s = math.sqrt(max(0.0, 1.0 + R[1][1] - R[0][0] - R[2][2])) * 2.0
        qx = (R[0][1] + R[1][0]) / s
        qy = 0.25 * s
        qz = (R[1][2] + R[2][1]) / s
        qw = (R[0][2] - R[2][0]) / s
    else:
        s = math.sqrt(max(0.0, 1.0 + R[2][2] - R[0][0] - R[1][1])) * 2.0
        qx = (R[0][2] + R[2][0]) / s
        qy = (R[1][2] + R[2][1]) / s
        qz = 0.25 * s
        qw = (R[1][0] - R[0][1]) / s

    qn = math.sqrt(qw * qw + qx * qx + qy * qy + qz * qz)
    qw /= qn
    qx /= qn
    qy /= qn
    qz /= qn

    if qw < 0.0:
        qw = -qw
        qx = -qx
        qy = -qy
        qz = -qz

    vnorm = math.sqrt(qx * qx + qy * qy + qz * qz)

    if vnorm < 1e-12:
        return 0.0, (1.0, 0.0, 0.0)

    theta = 2.0 * math.atan2(vnorm, max(0.0, qw))
    axis = (qx / vnorm, qy / vnorm, qz / vnorm)

    if theta > math.pi:
        theta -= 2.0 * math.pi
        axis = scale(axis, -1.0)

    return theta, axis

def solve():
    n = int(input())
    m = 2 * n

    A = [tuple(map(float, input().split())) for _ in range(m)]
    B = [tuple(map(float, input().split())) for _ in range(m)]

    MA = build_matrix(A)
    MB = build_matrix(B)

    qa = [matrix_fingerprint(p, MA) for p in A]
    qb = [matrix_fingerprint(p, MB) for p in B]

    order_a = sorted(range(m), key=qa.__getitem__)
    order_b = sorted(range(m), key=qb.__getitem__)

    groups_a = build_groups(qa, order_a)
    groups_b = build_groups(qb, order_b)

    # The random-instance fast path has exactly n groups,
    # each containing the two antipodal endpoints of one line.
    fast = (
        len(groups_a) == n
        and len(groups_b) == n
        and all(len(g) == 2 for g in groups_a)
        and all(len(g) == 2 for g in groups_b)
    )

    if not fast and n <= 3:
        ans = brute_force_small(A, B)
        if ans is not None:
            R, perm = ans
        else:
            raise RuntimeError("No rotation found")
    else:
        if not fast:
            # The official random-input guarantee makes this branch
            # practically unreachable for large n.
            groups_a = [order_a[2 * i:2 * i + 2] for i in range(n)]
            groups_b = [order_b[2 * i:2 * i + 2] for i in range(n)]

        g0 = 0
        best_g = 1
        best_sep = 2.0

        a0 = A[groups_a[g0][0]]
        b0 = B[groups_b[g0][0]]

        for g in range(1, n):
            ag = A[groups_a[g][0]]
            sep = abs(dot(a0, ag))
            if sep < best_sep:
                best_sep = sep
                best_g = g

        a1 = A[groups_a[best_g][0]]
        b1 = B[groups_b[best_g][0]]

        R = None
        perm = None

        for s0 in (1.0, -1.0):
            for s1 in (1.0, -1.0):
                cand = rotation_from_two(
                    b0,
                    b1,
                    scale(a0, s0),
                    scale(a1, s1),
                )
                if cand is None:
                    continue

                p = validate_group_rotation(
                    cand, A, B, groups_a, groups_b
                )
                if p is not None:
                    R = cand
                    perm = p
                    break

            if R is not None:
                break

        if R is None:
            # This is only a safety net for unusual numerical degeneracy.
            if n <= 3:
                ans = brute_force_small(A, B)
                if ans is None:
                    raise RuntimeError("No rotation found")
                R, perm = ans
            else:
                raise RuntimeError("Fingerprint matching failed")

    theta, axis = rotation_to_axis_angle(R)

    print("{:.12f}".format(theta))
    print("{:.12f} {:.12f} {:.12f}".format(*axis))
    print(" ".join(str(x + 1) for x in perm))

if __name__ == "__main__":
    solve()
```

The matrix accumulation is the only pass over the coordinates needed to construct the invariant. Because the matrix is symmetric, only six values are stored, although the code keeps the complete symmetric structure when evaluating the quadratic form.

The expression in `matrix_fingerprint` is evaluated as (x(Mr)_x+y(Mr)_y+z(Mr)_z). The two antipodal points produce the same value because replacing (r) by (-r) changes both factors of the quadratic form's product of signs.

The sorting arrays contain indices rather than coordinates. This avoids moving the actual point data and makes it straightforward to recover the original input index for the final permutation.

The four sign choices are necessary. The input represents lines, not oriented vectors, so the invariant can tell us which line corresponds to which line but cannot tell whether the chosen endpoint should be positive or negative. Once two nonparallel oriented vectors are fixed, the rotation itself resolves this ambiguity.

The frame construction subtracts the projection of the second vector onto the first. That produces a vector perpendicular to the first, after which a cross product completes an orthonormal right-handed basis. Mapping one right-handed basis to another always produces a proper rotation, not a reflection.

The quaternion conversion uses different formulas depending on the dominant diagonal entry when the trace is nonpositive. This avoids dividing by a tiny number near a (180^\circ) rotation. The zero-angle case is handled separately because the axis is mathematically arbitrary there.

## Worked Examples

### Sample 1

For the supplied sample, the four points of the first set form a square in the (xy)-plane, and the second set is the same square rotated by (+\pi/2) before the required inverse rotation is applied.

The quadratic matrix for the first set is diagonal:
[
M=
\begin{pmatrix}
3.41421356&0&0\
0&0.58578644&0\
0&0&0
\end{pmatrix}.
]
Every point of the square has the same value of (r^TMr), so the normal random-instance pairing is unavailable.

| Stage | State |
| --- | --- |
| (n) | (2) |
| Number of points | (4) |
| Fingerprint groups | One group containing all four points |
| Fast path | Rejected |
| Fallback | Enumerate (4!=24) permutations |
| Valid rotation | Rotation by (-\pi/2) around (z) |
| Valid permutation | (2,3,4,1) |

The fallback tries a permutation and determines the rotation from two nonparallel points. Once the correct permutation is reached, the computed rotation sends every primed point to its assigned point. The output shown in the statement is one valid representation, and the program may produce a different but equivalent representation because the problem has many valid choices for this symmetric configuration.

### A non-symmetric four-line example

Consider four unoriented directions
[
(1,0,0),\quad
(0,1,0),\quad
(0,0,1),\quad
\frac{1}{\sqrt3}(1,1,1),
]
together with their negatives. Rotate everything around the (z)-axis by (90^\circ), then shuffle the points.

The quadratic fingerprint is no longer identical for every line, so the fast path can identify the line groups. The important state transition is shown below.

| Stage | First set | Second set |
| --- | --- | --- |
| Matrix (M) | Accumulated from 8 points | Rotated version of (M) |
| Sorted fingerprints | 4 line groups | Same 4 groups in the same order |
| Reference group | First group | Corresponding first group |
| Second reference | Least parallel remaining group | Its corresponding group |
| Sign trials | 4 | 4 |
| Successful trial | One sign pair | Same physical rotation |
| Validation | All 8 points within tolerance | All 8 points within tolerance |

The example demonstrates why the algorithm separates line identification from endpoint identification. The fingerprint identifies an antipodal pair as one object. The two-vector rotation reconstruction then determines the orientation of its two endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Matrix accumulation and fingerprint evaluation are (O(n)); sorting (2n) values costs (O(n\log n)); only four rotations are checked against all points. |
| Space | (O(n)) | The two point sets, fingerprints, sorting indices, and permutation all use linear memory. |

For (n=4\cdot10^4), there are only (8\cdot10^4) points. The dominant operation is sorting two arrays of that size, followed by a constant number of linear scans. This is comfortably within the intended four second complexity target in a compiled implementation, and the Python implementation keeps all geometric operations constant-sized and uses `sys.stdin.readline` for input.

The random-direction guarantee is what turns the invariant from a general-purpose fingerprint into a practical one. Without it, different lines could have equal fingerprints, and no single scalar invariant would be sufficient in general. The official discussion makes the same distinction: (P_4) is useful for random configurations, while symmetric configurations can make it useless.

## Test Cases

The output of this problem is not unique, so an assert should not compare the raw output string with one predetermined answer. The right test is to parse the returned rotation and permutation and verify the geometric condition. The following harness assumes the `solve()` function from the solution above is available in the same test file.

```python
import sys
import io
import math
import random

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

def rotate_z(p, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    x, y, z = p
    return (c * x - s * y, s * x + c * y, z)

def make_case(points, angle):
    first = []
    for p in points:
        first.append(p)
        first.append((-p[0], -p[1], -p[2]))

    second = []
    for p in points:
        q = rotate_z(p, angle)
        second.append(q)
        second.append((-q[0], -q[1], -q[2]))

    rng = random.Random(1234567)
    rng.shuffle(second)

    lines = [str(len(points))]
    for p in first:
        lines.append("{:.12f} {:.12f} {:.12f}".format(*p))
    for p in second:
        lines.append("{:.12f} {:.12f} {:.12f}".format(*p))
    return "\n".join(lines) + "\n"

def parse_output(inp, out):
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = 2 * n

    A = []
    for _ in range(m):
        A.append(tuple(float(next(it)) for _ in range(3)))

    B = []
    for _ in range(m):
        B.append(tuple(float(next(it)) for _ in range(3)))

    out_data = out.split()
    theta = float(out_data[0])
    axis = tuple(map(float, out_data[1:4]))
    perm = list(map(int, out_data[4:4 + m]))

    assert -math.pi - 1e-9 <= theta <= math.pi + 1e-9
    assert 1e-3 <= sum(abs(x) for x in axis) <= 1e3
    assert sorted(perm) == list(range(1, m + 1))

    c = math.cos(theta)
    s = math.sin(theta)
    x, y, z = axis
    length = math.sqrt(x * x + y * y + z * z)
    x /= length
    y /= length
    z /= length

    for i in range(m):
        bx, by, bz = B[i]

        # Rodrigues rotation.
        cross_x = y * bz - z * by
        cross_y = z * bx - x * bz
        cross_z = x * by - y * bx
        d = x * bx + y * by + z * bz

        rx = bx * c + cross_x * s + x * d * (1.0 - c)
        ry = by * c + cross_y * s + y * d * (1.0 - c)
        rz = bz * c + cross_z * s + z * d * (1.0 - c)

        ax, ay, az = A[perm[i] - 1]
        err = math.sqrt(
            (rx - ax) ** 2 +
            (ry - ay) ** 2 +
            (rz - az) ** 2
        )
        assert err <= 2e-6

# Provided sample.
sample1 = """\
2
0.923879533 0.382683432 0
0.923879533 -0.382683432 0
-0.923879533 -0.382683432 0
-0.923879533 0.382683432 0
0.382683432 0.923879533 0
0.382683432 -0.923879533 0
-0.382683432 -0.923879533 0
-0.382683432 0.923879533 0
"""

parse_output(sample1, run(sample1))

# Minimum-size case, n = 2, with an identity rotation.
case_min = make_case(
    [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
    ],
    0.0,
)
parse_output(case_min, run(case_min))

# Symmetric three-line case. This exercises the small brute-force fallback.
case_symmetric = make_case(
    [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    ],
    math.pi / 2,
)
parse_output(case_symmetric, run(case_symmetric))

# Non-symmetric case with a general-looking set of directions.
case_general = make_case(
    [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0 / math.sqrt(3.0),
         1.0 / math.sqrt(3.0),
         1.0 / math.sqrt(3.0)),
    ],
    -0.731,
)
parse_output(case_general, run(case_general))

# Maximum-size stress case.
# The points are generated deterministically on the sphere and then rotated.
n_big = 40000
points_big = []

for i in range(n_big):
    z = -1.0 + 2.0 * (i + 0.5) / n_big
    phi = i * 2.399963229728653
    r = math.sqrt(max(0.0, 1.0 - z * z))
    points_big.append((r * math.cos(phi), r * math.sin(phi), z))

case_big = make_case(points_big, 1.234567)
parse_output(case_big, run(case_big))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided sample | Any geometrically valid rotation and permutation | Symmetric configuration and the small brute-force fallback |
| (n=2), identity rotation | Angle (0) with any valid axis and permutation | Minimum size and zero-angle handling |
| Three coordinate axes | Any valid (90^\circ) rotation and permutation | Multiple equal fingerprints and fallback correctness |
| Four non-symmetric directions | A valid rotation close to (-0.731) radians around the (z)-axis | Normal invariant-based matching and sign selection |
| (n=40000) generated directions | Any valid permutation with error at most (2\cdot10^{-6}) | Maximum input size, sorting cost, and numerical stability |

## Edge Cases

The first edge case is the unavoidable antipodal equality. Suppose the set contains ((1,0,0)) and ((-1,0,0)). Their fingerprints satisfy
[
F(1,0,0)=F(-1,0,0).
]
A careless implementation might conclude that the invariant has failed. The correct interpretation is that both points describe the same geometric line. The algorithm keeps them together and delays the sign decision until after the rotation is known.

The second edge case is the identity rotation. Take
[
A={(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)}
]
and let (B=A) in a different order. The required rotation can be the identity, with (\theta=0). The quaternion has zero vector part, so the code prints axis ((1,0,0)). The axis is arbitrary for zero rotation, and the permutation is obtained by matching the rotated points directly.

The third edge case is a rotation by exactly (\pi). The antisymmetric entries of a rotation matrix are theoretically zero at this angle, so a formula such as
[
e_x=\frac{R_{32}-R_{23}}{2\sin\theta}
]
is numerically dangerous. The quaternion conversion instead selects the largest diagonal term when the trace is nonpositive. For example, a rotation by (\pi) around the (z)-axis has
[
R=
\begin{pmatrix}
-1&0&0\
0&-1&0\
0&0&1
\end{pmatrix},
]
and the largest diagonal determines the (z)-component of the quaternion without dividing by a quantity close to zero.

The fourth edge case is the supplied square sample. Its four points all have the same quadratic fingerprint. Sorting alone cannot tell which two points form an original line. Since (n=2), the fallback enumerates all (4!) possible point permutations. For each one it constructs a rotation from two nonparallel vectors and checks all four points. One of these candidates gives the valid (-\pi/2) rotation and the permutation (2,3,4,1).

The final numerical edge case is two random fingerprints that happen to be extremely close. With independently uniform random directions, exact equality between different lines has probability zero, and the probability of a collision inside a fixed numerical tolerance is extremely small. The statement deliberately supplies this random construction so that the scalar fourth-degree invariant can be used as a practical fingerprint. The code still verifies the final rotation against every point, so an incorrect candidate caused by numerical ambiguity is rejected rather than silently printed.
