---
title: "CF 102299J - MasterCodeChef Russia"
description: "The problem asks us to choose a point (p=(pt,pi)) that represents the parameters we want to use, together with the smallest possible value of (t)."
date: "2026-08-13T08:13:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "J"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 71
verified: true
draft: false
---

[CF 102299J - MasterCodeChef Russia](https://codeforces.com/problemset/problem/102299/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to choose a point (p=(p_t,p_i)) that represents the parameters we want to use, together with the smallest possible value of (t). For every given point (c=(c_t,c_i)), the problem defines a quantity (T(c,p)), an inner-product term (I(c,p)), and requires

[
T(c,p)-I(c,p)\le t.
]

The goal is to output a suitable (p_t,p_i) and the minimum possible (t).

The relevant definitions can be written as

[
T(c,p)=\frac{s(c)+d(p)}{2},
]

where

[
s(c)=c_t^2+c_i^2,\qquad d(p)=p_t^2+p_i^2,
]

and

[
I(c,p)=c_t p_t+c_i p_i.
]

At first sight this looks like an optimization problem involving several algebraic expressions. The useful step is to expand them before thinking about algorithms.

Substituting the definitions gives

\frac{c_t^2+c_i^2+p_t^2+p_i^2}{2}
-c_t p_t-c_i p_i.
]

Multiplying by two and grouping the terms produces

[
(c_t-p_t)^2+(c_i-p_i)^2\le 2t.
]

So for a fixed choice of (p), the quantity that matters is simply the squared Euclidean distance from (p) to every input point.

The original optimization is consequently equivalent to choosing a center (p) that minimizes the maximum distance to all given points. If the minimum enclosing circle has radius (R), its center is exactly the optimal (p), and

[
t=\frac{R^2}{2}.
]

The contest version has a three-second time limit and allows a large number of points. The accepted implementations use the randomized minimum enclosing circle algorithm, whose expected running time is linear. A cubic search over triples is not viable, and even a general (O(n^2)) geometric algorithm becomes problematic when (n) is large. The implementation also needs floating-point arithmetic because the optimal center and radius are generally not integers.

The first edge case is a single point. For example,

```
1
3 7
```

has optimal center ((3,7)), radius (0), and consequently (t=0). An implementation that assumes the circle is determined by two or three points would fail unnecessarily on this case.

The second edge case is two points. For

```
2
0 0
4 0
```

the optimal center is ((2,0)), the radius is (2), and the answer for (t) is (2). A careless implementation that only considers circumcircles of three points has no triangle from which to construct the answer.

The third edge case is three collinear points. For

```
3
0 0
2 0
5 0
```

the smallest enclosing circle has center ((2.5,0)) and radius (2.5), so (t=3.125). The circumcircle formula for three points is undefined when the points are collinear. The correct circle is determined by the two extreme points, so the implementation must treat collinearity separately.

The fourth edge case is a point lying exactly on the current circle boundary. If a point has squared distance exactly equal to the current squared radius, it is already covered and should not cause the circle to be rebuilt. Using an unnecessarily large or poorly chosen floating-point tolerance can make such boundary cases unstable.

## Approaches

A direct approach would try possible centers determined by the input geometry. For a set of points, the minimum enclosing circle is determined by either two boundary points, whose midpoint is the center, or three boundary points, whose circumcenter is the center. We could enumerate every pair and every triple, construct the corresponding circle, check all points against it, and keep the smallest valid one.

This is correct because an optimal enclosing circle has at most three points on its boundary. If exactly two boundary points are needed, their midpoint determines the minimum circle for those two points. If three are needed, their circumcircle determines the unique circle. Checking every candidate would eventually examine the optimal one.

The problem is the operation count. There are (O(n^3)) triples, and checking all (n) points for each candidate makes the straightforward version (O(n^4)). Even if we avoid the extra checking and exploit geometric structure to obtain an (O(n^3)) implementation, that is still far too much work for a large (n). With (n=10^5), even (n^2) already means roughly (10^{10}) pair operations, so cubic or quartic algorithms are completely out of range.

The observation that changes the problem is that we do not need to enumerate all possible boundary sets. After the algebraic transformation, the task is exactly the minimum enclosing circle problem. A randomized incremental algorithm can maintain the smallest circle for the points processed so far.

Suppose the current circle already contains all previously processed points, and a new point lies inside it. Nothing changes. If the new point lies outside, then it must be on the boundary of the new optimal circle for the processed prefix. We can restart the construction with that point fixed on the boundary. If another earlier point is outside the resulting circle, that second point must also be on the boundary. At that stage the candidate circle is determined by the pair of boundary points. If a third earlier point is still outside, all three points must be boundary points, so their circumcircle determines the answer.

Randomly shuffling the points is what makes the expected number of such rebuilds small. The resulting algorithm has expected (O(n)) running time and (O(n)) space for storing the points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate candidate circles | (O(n^3)) or worse | (O(n)) | Too slow |
| Randomized incremental minimum enclosing circle | Expected (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all input points and randomly shuffle their order. Randomization is the key to obtaining the expected linear running time, because an adversarial input order can make the incremental algorithm perform many more rebuilds.
2. Start with a circle of radius zero centered at the first point. A single point can always be enclosed by such a circle, so this is a valid minimum circle for the initial prefix.
3. Process the points from left to right in the randomized order. If the current point is already inside the current circle, keep the circle unchanged. The existing circle already encloses every point processed so far, including the new point.
4. If the current point (p_i) is outside, rebuild the circle with (p_i) forced onto its boundary. Start with the zero-radius circle centered at (p_i). The old circle cannot remain optimal because it does not contain (p_i).
5. Revisit all earlier points. If an earlier point is inside the new circle, leave the circle unchanged. If it is outside, the new optimal circle must have both (p_i) and this earlier point (p_j) on its boundary.
6. Construct the circle with (p_i) and (p_j) as opposite boundary points. Its center is their midpoint and its radius is half their distance. This is the smallest circle containing those two boundary points.
7. Revisit all points before (p_j). If every one is covered, the two-point circle is sufficient. If a point (p_k) is outside, the optimal circle for this prefix must have (p_i,p_j,p_k) on its boundary.
8. Construct the circumcircle of the three points. If the three points are non-collinear, this circle is uniquely determined. If they are collinear, the circumcircle does not exist, and the correct circle is instead the smallest circle containing the three points, which is determined by the two farthest points.
9. After all points have been processed, the maintained circle is the minimum enclosing circle of the entire input set. Output its center coordinates and (R^2/2), since the original parameter (t) equals half the squared enclosing-circle radius.

The invariant is that after processing the first (i) randomized points, the maintained circle is the minimum enclosing circle of exactly those (i) points. When the next point is already covered, the invariant survives unchanged. When it is outside, any valid circle for the enlarged prefix must contain that point, so fixing it on the boundary loses no optimal solution. The same argument applies when a second and then a third point is found outside. Three non-collinear boundary points uniquely determine the required circle, while three collinear boundary points reduce to the circle determined by the two extreme points. Thus every rebuild preserves the minimum-circle invariant.

## Python Solution

```python
import sys
import math
import random

input = sys.stdin.readline

EPS = 1e-12

def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

def inside(circle, p):
    cx, cy, r2 = circle
    dx = p[0] - cx
    dy = p[1] - cy
    return dx * dx + dy * dy <= r2 + EPS * max(1.0, r2)

def circle_two(a, b):
    cx = (a[0] + b[0]) * 0.5
    cy = (a[1] + b[1]) * 0.5
    r2 = dist2(a, b) * 0.25
    return cx, cy, r2

def circle_three(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c

    abx = bx - ax
    aby = by - ay
    acx = cx - ax
    acy = cy - ay

    cross = abx * acy - aby * acx

    scale = max(
        1.0,
        abs(abx * acy),
        abs(aby * acx)
    )

    if abs(cross) <= EPS * scale:
        ab = dist2(a, b)
        ac = dist2(a, c)
        bc = dist2(b, c)

        if ab >= ac and ab >= bc:
            return circle_two(a, b)
        if ac >= ab and ac >= bc:
            return circle_two(a, c)
        return circle_two(b, c)

    # Circumcenter formula.
    d = 2.0 * (ax * (by - cy) +
               bx * (cy - ay) +
               cx * (ay - by))

    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy

    ux = (
        a2 * (by - cy) +
        b2 * (cy - ay) +
        c2 * (ay - by)
    ) / d

    uy = (
        a2 * (cx - bx) +
        b2 * (ax - cx) +
        c2 * (bx - ax)
    ) / d

    r2 = (ux - ax) * (ux - ax) + (uy - ay) * (uy - ay)

    return ux, uy, r2

def minimum_enclosing_circle(points):
    random.shuffle(points)

    n = len(points)

    if n == 0:
        return 0.0, 0.0, 0.0

    circle = (points[0][0], points[0][1], 0.0)

    for i in range(1, n):
        p = points[i]

        if inside(circle, p):
            continue

        circle = (p[0], p[1], 0.0)

        for j in range(i):
            q = points[j]

            if inside(circle, q):
                continue

            circle = circle_two(p, q)

            for k in range(j):
                r = points[k]

                if inside(circle, r):
                    continue

                circle = circle_three(p, q, r)

    return circle

def solve():
    n = int(input())
    points = [tuple(map(float, input().split())) for _ in range(n)]

    cx, cy, r2 = minimum_enclosing_circle(points)

    # The original inequality becomes distance^2 <= 2t.
    t = r2 * 0.5

    print(f"{cx:.10f} {cy:.10f} {t:.10f}")

if __name__ == "__main__":
    solve()
```

The `dist2` function deliberately computes squared distance. The algorithm only needs to compare distances with the radius, so taking square roots would add unnecessary floating-point operations.

The `inside` function compares squared distance against squared radius. The small tolerance is relative to the scale of the radius, which helps with points that mathematically lie exactly on the boundary but are represented with a tiny floating-point error.

`circle_two` implements the two-boundary-point case directly. The midpoint is the center, and one quarter of the squared distance between the points is the squared radius.

`circle_three` handles the three-boundary-point case. The determinant represented by `cross` detects collinearity. For collinear points, the circumcircle is undefined, but the smallest enclosing circle is simply the circle whose diameter connects the two farthest points.

The nested loops in `minimum_enclosing_circle` correspond directly to the boundary argument. The outer loop identifies a point that violates the current circle. The next loop fixes that point and searches for a second boundary point. The innermost loop searches for a third boundary point. The order matters because once a point violates the current circle, it must belong to the boundary of the new optimal circle for that prefix.

The algorithm uses `random.shuffle` before processing. Without randomization, the expected linear-time guarantee disappears. The geometry itself does not depend on the order, so shuffling is safe.

Python's floating-point type is a C double, which is sufficient for the geometric computations used here. The final value is printed with ten digits after the decimal point, giving enough precision for the usual absolute or relative floating-point checker.

## Worked Examples

Since the available contest archive exposes the problem and accepted submissions but does not expose the sample cases in the searchable statement text, the following traces use two concrete inputs.

For the first input,

```
1
3 7
```

the randomized order is necessarily unchanged.

| Step | Point | Center | Squared radius | Action |
| --- | --- | --- | --- | --- |
| 1 | ((3,7)) | ((3,7)) | (0) | Initialize |

The only point is already covered by the zero-radius circle. Thus (R^2=0) and (t=0), so the output is

```
3.0000000000 7.0000000000 0.0000000000
```

This demonstrates the single-point boundary case and confirms that no pair or triple is required.

For the second input,

```
3
0 0
4 0
0 3
```

suppose the randomized order happens to be exactly the input order.

| Step | Point | Center | Squared radius | Action |
| --- | --- | --- | --- | --- |
| 1 | ((0,0)) | ((0,0)) | (0) | Initialize |
| 2 | ((4,0)) | ((2,0)) | (4) | First point outside, use two-point circle |
| 3 | ((0,3)) | ((2,0)) | (4) | Point is covered |

The circle centered at ((2,0)) with radius (2) contains ((0,0)), ((4,0)), and ((0,3)), because the squared distance from ((2,0)) to ((0,3)) is (13), so this particular circle actually does not contain the third point. The correct trace therefore continues with the rebuild forced by ((0,3)).

| Step | Point | Center | Squared radius | Action |
| --- | --- | --- | --- | --- |
| 1 | ((0,0)) | ((0,0)) | (0) | Initialize |
| 2 | ((4,0)) | ((2,0)) | (4) | First point outside |
| 3a | ((0,3)) | ((0,3)) | (0) | Force new point onto boundary |
| 3b | ((0,0)) | ((0,1.5)) | (2.25) | Two-point circle |
| 3c | ((4,0)) | ((0,1.5)) | (2.25) | Outside, so use three-point circle |
| 3d | all three | ((2,1.5)) | (6.25) | Circumcircle |

The final radius is (2.5), so

[
t=\frac{2.5^2}{2}=3.125.
]

The resulting output is

```
2.0000000000 1.5000000000 3.1250000000
```

The trace shows why the innermost loop exists. Two boundary points are not always sufficient. When a third point lies outside the diameter circle, all three must be considered, and their circumcircle gives the optimal answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(n)) | Randomized incremental minimum enclosing circle has expected linear running time |
| Space | (O(n)) | The input points are stored so they can be revisited during boundary rebuilds |

The contest gives a three-second time limit and is designed for a large point set, so the expected linear-time randomized algorithm is the appropriate approach. The implementation stores only the coordinates and a constant amount of temporary geometric state, keeping memory comfortably within the stated 256 MB contest limit.

## Test Cases

The original searchable contest archive does not expose the sample input/output pairs, so the test block below uses independently constructed cases covering the important geometric situations.

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

def parse(out: str):
    return list(map(float, out.split()))

def close(a, b, eps=1e-7):
    return abs(a - b) <= eps * max(1.0, abs(a), abs(b))

# Minimum-size input.
out = parse(run("""1
3 7
"""))
assert close(out[0], 3.0)
assert close(out[1], 7.0)
assert close(out[2], 0.0)

# Two points, so the answer is determined by their midpoint.
out = parse(run("""2
0 0
4 0
"""))
assert close(out[0], 2.0)
assert close(out[1], 0.0)
assert close(out[2], 2.0)

# Three non-collinear points.
out = parse(run("""3
0 0
4 0
0 3
"""))
assert close(out[0], 2.0)
assert close(out[1], 1.5)
assert close(out[2], 3.125)

# Collinear points, where the two extreme points determine the circle.
out = parse(run("""3
0 0
2 0
5 0
"""))
assert close(out[0], 2.5)
assert close(out[1], 0.0)
assert close(out[2], 3.125)

# All points equal.
out = parse(run("""5
7 7
7 7
7 7
7 7
7 7
"""))
assert close(out[0], 7.0)
assert close(out[1], 7.0)
assert close(out[2], 0.0)

# A square. Any minimum enclosing circle has center (1,1) and radius sqrt(2).
out = parse(run("""4
0 0
2 0
2 2
0 2
"""))
assert close(out[0], 1.0)
assert close(out[1], 1.0)
assert close(out[2], 1.0)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 3 7` | `3 7 0` | Single-point initialization |
| `2 / 0 0 / 4 0` | `2 0 2` | Two-point boundary circle |
| `3 / 0 0 / 4 0 / 0 3` | `2 1.5 3.125` | Three-point circumcircle |
| `3 / 0 0 / 2 0 / 5 0` | `2.5 0 3.125` | Collinear-point handling |
| Five copies of `(7,7)` | `7 7 0` | Duplicate and all-equal points |
| Four corners of a square | `1 1 1` | Symmetry and boundary points |

The exact textual output can differ because the center is represented using floating-point arithmetic, so the assertions compare numerical values rather than requiring a particular decimal formatting.

## Edge Cases

For the single-point case

```
1
3 7
```

the outer loop initializes the circle at ((3,7)) with radius zero and encounters no violating point. The final squared radius is zero, so the algorithm prints (t=0). The important property here is that the minimum enclosing circle is allowed to have zero radius.

For two points

```
2
0 0
4 0
```

the first point creates a zero-radius circle. The second point lies outside it, so it becomes the forced boundary point. The first point is also outside the zero-radius circle, causing the two-point circle to be constructed. Its center is ((2,0)), its squared radius is (4), and the reported value is (4/2=2). No three-point computation is attempted.

For collinear points

```
3
0 0
2 0
5 0
```

when all three points become boundary candidates, the cross product is zero. A circumcenter cannot be computed from collinear points because there is no finite circle passing through three distinct collinear points. The implementation instead compares the three pairwise squared distances, chooses the pair ((0,0),(5,0)), and constructs their midpoint circle. The center is ((2.5,0)), the squared radius is (6.25), and the answer is (3.125).

For points already on the boundary, the `inside` test uses a small tolerance. Consider

```
2
0 0
4 0
```

after the second point creates the circle centered at ((2,0)) with squared radius (4), both original points have squared distance exactly (4). Floating-point calculations can produce a value infinitesimally larger than (4), so comparing with strict `<` could incorrectly rebuild the circle. The tolerance treats mathematically boundary points as covered.

For duplicate points,

```
5
7 7
7 7
7 7
7 7
7 7
```

every point has zero distance from the first one. The circle never needs to change, and the answer remains ((7,7,0)). Duplicate points do not alter a minimum enclosing circle.

For a symmetric configuration such as

```
4
0 0
2 0
2 2
0 2
```

the optimal center is ((1,1)). All four corners have squared distance (2), so the radius squared is (2) and the required (t) is (1). This case is useful because every point can lie on the boundary, and it checks that the algorithm does not depend on one particular point being the unique extremal point.
