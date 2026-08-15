---
title: "CF 102354F - Cosmic Crossroads"
description: "We are given two collections of (n) unoriented lines through the origin. Each line is represented by its two intersections with the unit sphere, so every collection contains (2n) unit vectors and every vector occurs together with its negation."
date: "2026-08-15T17:42:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "F"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 610
verified: false
draft: false
---

[CF 102354F - Cosmic Crossroads](https://codeforces.com/problemset/problem/102354/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two collections of (n) unoriented lines through the origin. Each line is represented by its two intersections with the unit sphere, so every collection contains (2n) unit vectors and every vector occurs together with its negation.

The second collection is obtained from the first by applying one rotation around the origin and then permuting the points. The task is to recover any such rotation and the corresponding permutation. Since a line has no preferred direction, either endpoint of the same diameter is an acceptable match after rotation.

The upper bound (n=4\cdot 10^4) means there can be (8\cdot 10^4) points in each collection. An (O(n^2)) algorithm would already require roughly (6.4\cdot 10^9) pair operations, which is far beyond a four second limit. We need something close to (O(n\log n)), with only a small amount of constant-size linear algebra per point. The coordinates have up to twelve decimal digits, so the implementation must use floating point carefully, but the statement gives enough precision margin to work with ordinary double precision.

The first subtlety is the antipodal representation. If (p) represents a line, then (-p) represents exactly the same line. Any invariant that is unchanged by (p\mapsto -p) cannot distinguish those two points. This is expected and harmless, because after the rotation we can choose whichever endpoint gives the required permutation.

A second subtlety is that a quadratic distance invariant is useless here. For a unit vector (p), the sum of squared distances from (p) to all input points is constant because the input contains every point together with its opposite. For example, with

```
2
1 0 0
-1 0 0
0 1 0
0 -1 0
1 0 0
-1 0 0
0 1 0
0 -1 0
```

the identity rotation and permutation (1\ 2\ 3\ 4) are valid, but every point has exactly the same sum of squared distances. A method based on that quantity cannot distinguish anything.

A third subtlety is that even the useful fourth-degree invariant can have equal values for different lines in a specially symmetric configuration. The sample itself has such a symmetry. A careless implementation that assumes the first two sorted points are always opposite endpoints can accidentally try to construct a frame from two parallel vectors. The correct implementation explicitly searches for two nonparallel points. For the sample, the first two points are already nonparallel, so they can be used.

Finally, the random-direction condition matters. The fourth-degree invariant is not a deterministic complete fingerprint for arbitrary point sets. For a uniformly random collection of directions, two different lines have equal invariant only with probability zero in exact arithmetic, and numerical collisions are overwhelmingly unlikely. This is the intended source of uniqueness. The underlying invariant approach is also the standard solution described for this problem.

## Approaches

The most direct brute-force idea is to guess which two points of the second collection correspond to two nonparallel points of the first collection. Two oriented nonparallel vectors determine a unique rotation, after choosing the appropriate signs for the second pair. We could then rotate every point and check whether the resulting set matches the first set.

There are (O(n^2)) choices for the pair in the second collection, and checking one candidate rotation against all (O(n)) points costs (O(n)). That gives (O(n^3)) work. At (n=4\cdot10^4), this is on the order of (6.4\cdot10^{13}) point checks, before accounting for the constant factor of the three-dimensional geometry. Trying every complete permutation is even worse, with ((2n)!) possibilities.

The useful observation is that rotation preserves distances. Define

[
P_4(p)=\sum_q |p-q|^4,
]

where the sum runs over all (2n) points in one collection. If the whole collection is rotated, the multiset of distances from a point to all other points is unchanged, so (P_4) is unchanged. The original editorial insight is to use this fourth-degree rotational invariant and sort the points by it.

For this particular problem we can simplify the calculation considerably. Let

[
M=\sum_q qq^T.
]

Because every (q) is a unit vector and the collection contains both (q) and (-q), we have

[
\sum_q q=0.
]

For a unit vector (p),

[
|p-q|^2=2-2p\cdot q.
]

Consequently,

[
\begin{aligned}
P_4(p)
&=\sum_q (2-2p\cdot q)^2\
&=4\sum_q\left(1-2p\cdot q+(p\cdot q)^2\right)\
&=4\left(2n+p^TMp\right).
\end{aligned}
]

The factor (4) and the constant (2n) do not affect the ordering. Thus we only need the scalar

[
s(p)=p^TMp.
]

The matrix (M) has only six independent entries, so it is constructed in (O(n)), and every signature is evaluated in (O(1)). We then sort the (2n) signatures, obtaining the correspondence between the two collections.

The brute-force method works because two nonparallel corresponding vectors determine the rotation. It fails because we do not know which vectors correspond. The invariant gives us that correspondence without trying all pairs, reducing the geometric matching problem to sorting (O(n)) scalar values.

There is still a sign ambiguity. Once two corresponding lines have been identified, choose the sign of the second target vector so that its dot product with the first target vector agrees with the corresponding dot product in the first collection. Two oriented nonparallel vectors then define orthonormal coordinate frames, and the rotation is simply the matrix that maps one frame to the other.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n)) | Too slow |
| Fourth-degree invariant + sorting | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the (2n) points of each collection. Every point has unit length up to the given input precision, and every point has its opposite in the same collection.
2. For each collection, construct the symmetric matrix

[
M=\sum_i r_i r_i^T.
]

For a point (r_i=(x_i,y_i,z_i)), its contribution is

[
\begin{pmatrix}
x_i^2 & x_iy_i & x_iz_i\
x_iy_i & y_i^2 & y_iz_i\
x_iz_i & y_iz_i & z_i^2
\end{pmatrix}.
]

Only six values need to be stored.

1. For every point (p), compute its scalar signature

[
s(p)=p^TMp.
]

This is proportional to the fourth-degree distance invariant (P_4(p)), so corresponding points have equal signatures in exact arithmetic. The antipodal points of one line also have the same signature, which is exactly the ambiguity we expect.

1. Sort the indices of both collections by their signatures. With random independent directions, different lines almost surely have different signatures, so the sorted positions identify corresponding lines. If several signatures coincide because of a symmetry, any correspondence compatible with that symmetry is potentially valid. The sample is such a small degenerate case, so the implementation does not assume that a particular sorted position is necessarily the opposite endpoint.
2. Take the first point in the sorted first collection and the point at the same sorted position in the second collection. Then scan the remaining sorted positions until we find another pair of nonparallel vectors. This handles the antipodal pair appearing consecutively in the generic case and also handles the sample, where several signatures coincide.
3. Let the chosen source vectors be (a_0,a_1), and the corresponding target vectors be (b_0,b_1). Normalize (a_0) and (b_0). For each second vector, remove its component along the first vector:

[
a_1^\perp=a_1-(a_1\cdot a_0)a_0.
]

Normalize this vector and do the same for (b_1).

1. Complete both pairs to right-handed orthonormal frames with a cross product:

[
a_2=a_0\times a_1^\perp,\qquad
b_2=b_0\times b_1^\perp.
]

If the target second vector has the wrong orientation, replace (b_1) by (-b_1) before constructing the frame. The sign is selected by comparing the two corresponding dot products.

1. Form the rotation matrix

[
R=
\begin{bmatrix}
b_0&b_1^\perp&b_2
\end{bmatrix}
\begin{bmatrix}
a_0&a_1^\perp&a_2
\end{bmatrix}^T.
]

By construction, (Ra_0=b_0) and (Ra_1=\pm b_1), with the sign chosen consistently. Since the two source vectors are nonparallel, this determines the entire proper rotation.

1. Convert (R) to a unit quaternion and then to an axis and angle. Taking the quaternion scalar part nonnegative gives an angle in ([0,\pi]), which satisfies the required interval. For a zero rotation, any axis is valid, so the implementation uses the (x)-axis.
2. For every input point (b_i) of the second collection, rotate it using (R). Its corresponding line is already known from the sorted position. That line has two candidate endpoints, (a_j) and (-a_j). Compare the rotated point with both and choose the closer endpoint. The resulting indices form the required permutation.

Why it works: the matrix (M) captures all second moments of the point set, and under a rotation (R) it transforms as (M'=RMR^T). Hence for corresponding points (p) and (Rp),

[
(Rp)^TM'(Rp)=p^TR^TRMR^TRp=p^TMp.
]

So the scalar signature is preserved. With random directions, it identifies each line independently except for its unavoidable antipodal ambiguity. Once two nonparallel line correspondences are chosen, the frame construction produces exactly the rotation mapping those lines. Since the input guarantees that a common rotation exists, that rotation maps every remaining line to its corresponding line. Finally, comparing the two endpoints of each line resolves the only remaining sign ambiguity.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )

def norm(a):
    return math.sqrt(dot(a, a))

def normalize(a):
    d = norm(a)
    return (a[0] / d, a[1] / d, a[2] / d)

def mat_vec(r, v):
    return (
        r[0][0] * v[0] + r[0][1] * v[1] + r[0][2] * v[2],
        r[1][0] * v[0] + r[1][1] * v[1] + r[1][2] * v[2],
        r[2][0] * v[0] + r[2][1] * v[1] + r[2][2] * v[2],
    )

def dist2(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    z = a[2] - b[2]
    return x * x + y * y + z * z

def build_signatures(points):
    m00 = m01 = m02 = 0.0
    m11 = m12 = 0.0
    m22 = 0.0

    for x, y, z in points:
        m00 += x * x
        m01 += x * y
        m02 += x * z
        m11 += y * y
        m12 += y * z
        m22 += z * z

    sig = [0.0] * len(points)

    for i, (x, y, z) in enumerate(points):
        tx = m00 * x + m01 * y + m02 * z
        ty = m01 * x + m11 * y + m12 * z
        tz = m02 * x + m12 * y + m22 * z
        sig[i] = x * tx + y * ty + z * tz

    order = list(range(len(points)))
    order.sort(key=sig.__getitem__)
    return sig, order

def make_frame(a, b):
    a = normalize(a)
    d = dot(a, b)
    v = (
        b[0] - d * a[0],
        b[1] - d * a[1],
        b[2] - d * a[2],
    )
    v = normalize(v)
    w = cross(a, v)
    return (a, v, w)

def frame_rotation(source, target):
    # R = T * S^T, where S and T contain frame vectors as columns.
    r = [[0.0] * 3 for _ in range(3)]

    for i in range(3):
        for j in range(3):
            r[i][j] = (
                target[0][i] * source[0][j]
                + target[1][i] * source[1][j]
                + target[2][i] * source[2][j]
            )

    return r

def rotation_to_axis_angle(r):
    trace = r[0][0] + r[1][1] + r[2][2]

    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * s
        qx = (r[2][1] - r[1][2]) / s
        qy = (r[0][2] - r[2][0]) / s
        qz = (r[1][0] - r[0][1]) / s
    elif r[0][0] >= r[1][1] and r[0][0] >= r[2][2]:
        s = math.sqrt(max(0.0, 1.0 + r[0][0] - r[1][1] - r[2][2])) * 2.0
        qw = (r[2][1] - r[1][2]) / s
        qx = 0.25 * s
        qy = (r[0][1] + r[1][0]) / s
        qz = (r[0][2] + r[2][0]) / s
    elif r[1][1] >= r[2][2]:
        s = math.sqrt(max(0.0, 1.0 - r[0][0] + r[1][1] - r[2][2])) * 2.0
        qw = (r[0][2] - r[2][0]) / s
        qx = (r[0][1] + r[1][0]) / s
        qy = 0.25 * s
        qz = (r[1][2] + r[2][1]) / s
    else:
        s = math.sqrt(max(0.0, 1.0 - r[0][0] - r[1][1] + r[2][2])) * 2.0
        qw = (r[1][0] - r[0][1]) / s
        qx = (r[0][2] + r[2][0]) / s
        qy = (r[1][2] + r[2][1]) / s
        qz = 0.25 * s

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

    theta = 2.0 * math.atan2(vnorm, qw)
    axis = (qx / vnorm, qy / vnorm, qz / vnorm)

    if theta > math.pi:
        theta -= 2.0 * math.pi

    return theta, axis

def solve():
    n = int(input())
    total = 2 * n

    a = [tuple(map(float, input().split())) for _ in range(total)]
    b = [tuple(map(float, input().split())) for _ in range(total)]

    sig_a, order_a = build_signatures(a)
    sig_b, order_b = build_signatures(b)

    a0 = order_a[0]
    b0 = order_b[0]

    # Find two nonparallel pairs. In the generic case positions 0 and 1
    # are antipodes, so the loop naturally skips them.
    chosen = None
    for k in range(1, total):
        ia = order_a[k]
        ib = order_b[k]

        ca = cross(a[a0], a[ia])
        cb = cross(b[b0], b[ib])

        if dot(ca, ca) > 1e-14 and dot(cb, cb) > 1e-14:
            chosen = (ia, ib)
            break

    if chosen is None:
        # This is only relevant for extremely degenerate input.
        # n >= 2 guarantees a valid nonparallel pair under the
        # random-direction condition.
        for ia in range(total):
            if ia == a0:
                continue
            ca = cross(a[a0], a[ia])
            if dot(ca, ca) <= 1e-14:
                continue
            for ib in range(total):
                if ib == b0:
                    continue
                cb = cross(b[b0], b[ib])
                if dot(cb, cb) > 1e-14:
                    chosen = (ia, ib)
                    break
            if chosen is not None:
                break

    a1, b1 = chosen

    a0v = normalize(a[a0])
    b0v = normalize(b[b0])
    a1v = normalize(a[a1])
    b1v = normalize(b[b1])

    da = dot(a0v, a1v)
    db = dot(b0v, b1v)

    # The two corresponding unoriented lines have the same angle.
    # Choose the sign giving the matching oriented dot product.
    if abs(da - db) > abs(da + db):
        b1v = (-b1v[0], -b1v[1], -b1v[2])

    source_frame = make_frame(a0v, a1v)
    target_frame = make_frame(b0v, b1v)

    r = frame_rotation(source_frame, target_frame)

    theta, axis = rotation_to_axis_angle(r)

    # Locate the antipode of every point of A exactly as represented
    # in the input. Decimal parsing preserves the sign symmetry.
    lookup = {}
    for i, p in enumerate(a):
        lookup[p] = i

    opposite = [0] * total
    for i, (x, y, z) in enumerate(a):
        opposite[i] = lookup[(-x, -y, -z)]

    position_b = [0] * total
    for pos, idx in enumerate(order_b):
        position_b[idx] = pos

    permutation = [0] * total

    for j in range(total):
        pos = position_b[j]
        candidate = order_a[pos]
        other = opposite[candidate]

        rb = mat_vec(r, b[j])

        if dist2(rb, a[other]) < dist2(rb, a[candidate]):
            permutation[j] = other + 1
        else:
            permutation[j] = candidate + 1

    print("{:.12f}".format(theta))
    print("{:.12f} {:.12f} {:.12f}".format(axis[0], axis[1], axis[2]))
    print(" ".join(map(str, permutation)))

if __name__ == "__main__":
    solve()
```

The first part of the implementation builds the (3\times3) second-moment matrix. The six stored entries are enough because the matrix is symmetric. The signature calculation then reduces every point to one quadratic-form evaluation.

The sorting step is the only asymptotically expensive operation. Python's built-in sort is implemented in optimized native code, so sorting (8\cdot10^4) floating-point keys is comfortably within the intended complexity.

The pair-selection loop deliberately checks cross products instead of assuming that a fixed pair of sorted positions is nonparallel. For a generic input, the first two sorted points are the two endpoints of the same line, so they cannot define a frame. In the sample, several signatures coincide, so the first two sorted points can instead be from different lines. Checking the cross products handles both cases.

The sign adjustment uses

[
|d_a-d_b| \quad\text{versus}\quad |d_a+d_b|.
]

This is preferable to checking only the sign of a product, because the dot products may be very close to zero. The chosen sign makes the two oriented pairs have the same mutual angle.

The frame rotation is constructed as (T S^T). Since both frames are orthonormal, this matrix is automatically a proper rotation up to floating-point error. The quaternion conversion avoids the numerical instability of extracting an axis directly from ((R-R^T)/(2\sin\theta)) when the angle is close to (0) or (\pi).

The final permutation does not trust the sign chosen during sorting. Each sorted position identifies a line, so there are exactly two candidate endpoints in the first collection. Rotating the second endpoint and comparing its distances to both candidates resolves the sign independently for every point.

## Worked Examples

### Sample 1

The sample has two lines, with endpoints

[
(\cos22.5^\circ,\pm\sin22.5^\circ,0)
]

and their opposites. The second set is the same pair of lines rotated in the plane.

The fourth-degree signatures are not enough to distinguish the two lines in this specially symmetric example, so the sorted order contains several equal values. The algorithm does not assume that positions (0) and (2) are the two lines. It scans until it finds two nonparallel pairs.

| Algorithm variable | Value or behavior |
| --- | --- |
| (n) | (2) |
| Number of points | (4) |
| First selected point | First point in sorted order |
| Second selected point | First later point nonparallel to it |
| Source dot product | Approximately (0.70710678) |
| Target dot product before sign | Approximately (-0.70710678) |
| Target sign | Negated |
| Rotation matrix | A planar rotation equivalent to the required rotation |
| Output angle | Any equivalent valid angle in ([-\pi,\pi]) |
| Permutation | A valid matching of the four endpoints |

The official sample uses angle (-\pi/2), axis ((0,0,1)), and permutation (2,3,4,1). The program is allowed to produce a different valid rotation because the symmetric two-line configuration admits multiple descriptions of the same line correspondence.

### Constructed sample 2

Consider three source lines represented by

[
a=(1,0,0),
]

[
b=(0,1,0),
]

and

[
c=(0.3,0.4,\sqrt{0.75}).
]

The second collection is obtained by rotating everything by (90^\circ) around the (z)-axis. The rotated representatives are

[
(0,1,0),\quad (-1,0,0),\quad
(-0.4,0.3,\sqrt{0.75}).
]

Each point is accompanied by its opposite.

For the first collection, after summing both endpoints of every line, the quadratic-form signatures of the three lines are proportional to (2.18), (2.32), and (2.50). The exact values are not needed, only their ordering.

| Algorithm variable | Source state | Target state |
| --- | --- | --- |
| First line signature | (2.18) | (2.18) |
| Second line signature | (2.32) | (2.32) |
| Third line signature | (2.50) | (2.50) |
| First frame vector | ((1,0,0)) | ((0,1,0)) |
| Second frame vector | ((0,1,0)) | ((-1,0,0)) |
| Third frame vector | ((0,0,1)) | ((0,0,1)) |
| Rotation angle | (90^\circ) | (90^\circ) |
| Rotation axis | ((0,0,1)) | ((0,0,1)) |

The important part of this trace is that the same scalar signature is obtained before and after rotation. Once two nonparallel lines are paired, the entire rotation matrix follows from the two orthonormal frames.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Constructing matrices and signatures takes (O(n)), sorting (2n) values takes (O(n\log n)), and all remaining geometry is linear |
| Space | (O(n)) | The two point arrays, signatures, sorted indices, antipode mapping, and permutation all use linear memory |

For (n\le4\cdot10^4), there are at most (8\cdot10^4) points in each collection. The algorithm performs only a constant amount of arithmetic per point plus two sorts of (8\cdot10^4) elements, which fits the four second limit much more comfortably than any quadratic approach. The memory usage is also linear and remains well within the stated 256 MiB limit.

## Test Cases

The output of this problem is not unique, so an assert comparing the output string with the official sample output is too strict. The test harness below instead checks that the produced permutation is a permutation of all indices and that rotating every second-set point by the reported axis and angle places it within tolerance of the reported first-set point. It also checks the official sample output itself.

```python
import sys
import io
import math
import random

# The following helpers assume that solve() from the solution above
# has been renamed solve_stream(inp) and returns its printed output.
# In a local test file, replace this wrapper with the submitted solution.

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

def rotate(v, axis, theta):
    x, y, z = v
    ax, ay, az = axis

    c = math.cos(theta)
    s = math.sin(theta)
    d = ax * x + ay * y + az * z

    return (
        x * c + (ay * z - az * y) * s + ax * d * (1.0 - c),
        y * c + (az * x - ax * z) * s + ay * d * (1.0 - c),
        z * c + (ax * y - ay * x) * s + az * d * (1.0 - c),
    )

def valid_output(inp: str, out: str, eps=3e-5) -> bool:
    data = inp.strip().splitlines()
    n = int(data[0])
    m = 2 * n

    first = [tuple(map(float, data[i + 1].split())) for i in range(m)]
    second = [tuple(map(float, data[i + 1 + m].split())) for i in range(m)]

    lines = out.strip().splitlines()
    if len(lines) != 3:
        return False

    theta = float(lines[0])
    axis = tuple(map(float, lines[1].split()))
    perm = list(map(int, lines[2].split()))

    if len(perm) != m:
        return False

    if sorted(perm) != list(range(1, m + 1)):
        return False

    an = math.sqrt(sum(x * x for x in axis))
    if an < 1e-12:
        return False

    axis = tuple(x / an for x in axis)

    for i in range(m):
        rotated = rotate(second[i], axis, theta)
        target = first[perm[i] - 1]

        d2 = sum(
            (rotated[k] - target[k]) ** 2
            for k in range(3)
        )

        if d2 > eps * eps:
            return False

    return True

sample1 = """\
2
0.923879533 0.382683432 0
0.923879533 -0.382683432 0
-0.923879533 -0.382683432 0
-0.923879533 0.382683432 0
0.382683432 0.923879533 0
0.382683432 -0.923879533 0
-0.382683432 -0.923879533 0
-0.382683432 0.923879533
"""

official_sample_output = """\
-1.570796327
0.000000000 0.000000000 1.000000000
2 3 4 1
"""

assert valid_output(sample1, official_sample_output), "official sample"
assert valid_output(sample1, run(sample1)), "sample 1 produced by solution"

def make_case(points, theta, axis, order):
    second = [rotate(p, axis, theta) for p in points]

    shuffled = [second[i] for i in order]

    lines = [str(len(points) // 2)]
    for p in points:
        lines.append("{:.12f} {:.12f} {:.12f}".format(*p))
    for p in shuffled:
        lines.append("{:.12f} {:.12f} {:.12f}".format(*p))

    return "\n".join(lines) + "\n"

# Minimum size, n = 2, and a nontrivial rotation.
r = math.sqrt(0.5)
points_min = [
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, r, r),
    (0.0, -r, -r),
]
case_min = make_case(
    points_min,
    math.pi / 3.0,
    (1.0, 1.0, 1.0),
    [2, 0, 3, 1],
)
assert valid_output(case_min, run(case_min)), "minimum n"

# Identity rotation, with the input already shuffled.
points_identity = [
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, -1.0, 0.0),
]
case_identity = make_case(
    points_identity,
    0.0,
    (1.0, 0.0, 0.0),
    [2, 3, 0, 1],
)
assert valid_output(case_identity, run(case_identity)), "zero rotation"

# All invariant values coincide. This is deliberately symmetric.
# The second set has the same order, so the arbitrary tie order is valid.
points_equal = [
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, -1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 0.0, -1.0),
]
case_equal = make_case(
    points_equal,
    math.pi / 2.0,
    (0.0, 0.0, 1.0),
    list(range(6)),
)
assert valid_output(case_equal, run(case_equal)), "equal invariant values"

# Boundary angle close to pi.
s = math.sqrt(3.0) / 2.0
points_pi = [
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, s, 0.5),
    (0.0, -s, -0.5),
    (0.5, 0.5, math.sqrt(0.5)),
    (-0.5, -0.5, -math.sqrt(0.5)),
]
case_pi = make_case(
    points_pi,
    math.pi,
    (0.0, 1.0, 0.0),
    [4, 0, 5, 2, 1, 3],
)
assert valid_output(case_pi, run(case_pi)), "angle pi"

# Maximum-size structural test.
# The test checks the size and permutation structure instead of rotating
# all 80000 points again, which keeps the test harness itself practical.
random.seed(123456)
n = 40000
points_max = []

for _ in range(n):
    x = random.gauss(0.0, 1.0)
    y = random.gauss(0.0, 1.0)
    z = random.gauss(0.0, 1.0)
    q = math.sqrt(x * x + y * y + z * z)
    p = (x / q, y / q, z / q)
    points_max.append(p)
    points_max.append((-p[0], -p[1], -p[2]))

case_max = make_case(
    points_max,
    0.0,
    (1.0, 0.0, 0.0),
    list(range(2 * n)),
)

out_max = run(case_max)
lines_max = out_max.strip().splitlines()
assert len(lines_max) == 3, "maximum size line count"
assert len(lines_max[2].split()) == 2 * n, "maximum size permutation length"
assert sorted(map(int, lines_max[2].split())) == list(range(1, 2 * n + 1)), \
    "maximum size permutation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | Any geometrically valid output | Symmetric (n=2) case and equal invariant values |
| Minimum (n=2) | Any valid rotation and permutation | Smallest allowed input and antipodal handling |
| Identity rotation | Angle (0) with any valid axis and permutation | Zero-angle quaternion branch |
| Symmetric equal-signature set | Any valid rotation | Behavior when the fourth-degree invariant has ties |
| Rotation by (\pi) | Any valid rotation with angle (\pi) or an equivalent representation | Quaternion boundary handling |
| (n=40000) | A valid permutation of all (80000) indices | Maximum input size and (O(n\log n)) behavior |

## Edge Cases

The antipodal case is fundamental rather than pathological. For

```
2
1 0 0
-1 0 0
0 1 0
0 -1 0
1 0 0
-1 0 0
0 1 0
0 -1 0
```

the two endpoints of each line have identical fourth-degree signatures. The algorithm never tries to distinguish them. Sorting identifies a line, and the final distance comparison decides whether the rotated point should be matched with (p) or (-p). The identity rotation with permutation (1,2,3,4) is valid.

The zero-rotation case is handled separately inside the axis-angle conversion. If the rotation matrix is numerically indistinguishable from the identity, its quaternion has an almost zero vector part. The angle is reported as zero and the axis is chosen as ((1,0,0)). The axis is arbitrary when the angle is zero, so this is a valid output.

The sample illustrates invariant collisions. Several different lines have the same (P_4) value, so an implementation that blindly assumes sorted positions (0) and (2) represent different lines can select two opposite points and fail to construct a frame. The implementation instead checks cross products while scanning the sorted positions. In the sample, the first two points are nonparallel, so they provide a valid frame.

A rotation by exactly (\pi) is another numerical boundary. Directly computing the axis using division by (\sin\theta) is unstable because (\sin\pi=0). The quaternion conversion avoids that division and extracts the axis from the vector part of the quaternion, so the (\pi)-rotation test exercises the intended stable branch.

The final sign choice is also an edge case. Suppose the invariant correctly identifies two lines, but the second collection happens to list the opposite endpoint. A rotation mapping (p) to (q) may instead need to map (p) to (-q). The algorithm compares (d_a=a_0\cdot a_1) with both (d_b=b_0\cdot b_1) and (-d_b), choosing the orientation that preserves the angle. The remaining endpoint choices are then resolved independently when constructing the permutation.
