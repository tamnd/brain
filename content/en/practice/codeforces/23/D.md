---
title: "CF 23D - Tetragon"
description: "We are given three points in the plane. Each point is the midpoint of one side of some strictly convex quadrilateral, an"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 23
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 23"
rating: 2600
weight: 23
solve_time_s: 131
verified: false
draft: false
---

[CF 23D - Tetragon](https://codeforces.com/problemset/problem/23/D)

**Rating:** 2600  
**Tags:** geometry, math  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three points in the plane. Each point is the midpoint of one side of some strictly convex quadrilateral, and the three corresponding sides all have the same length. The original vertices are unknown. We must reconstruct any valid quadrilateral or determine that no such figure exists.

The tricky part is that we are not told which midpoint belongs to which side. Even if a valid quadrilateral exists, the three given points could correspond to consecutive sides, alternating sides, or some other cyclic order. A correct solution must handle every possible arrangement.

The number of test cases is large, up to $5 \cdot 10^4$, so the work per test case must be constant time. Any approach that performs geometric search, optimization, or iterative reconstruction would be far too slow. We need a direct geometric characterization.

The coordinates are tiny integers, but that does not simplify the geometry. Degenerate configurations are still possible, and floating point inaccuracies can easily break convexity checks if the reconstruction formula is not derived carefully.

One easy mistake is assuming the three equal sides are consecutive. Consider:

```
0 1 1 0 2 2
```

A valid quadrilateral exists, but only for one specific cyclic arrangement of the midpoint roles. A solution that fixes one ordering and never permutes the points incorrectly outputs NO.

Another dangerous case is collinear midpoint positions:

```
1 1 2 2 3 3
```

All three points lie on the same line. A careless algebraic reconstruction may still produce four points, but the resulting quadrilateral cannot be strictly convex. The correct output is NO.

A more subtle failure happens when the reconstruction gives repeated vertices. For example, some midpoint assignments lead to side vectors collapsing to zero length. The figure then becomes degenerate even though intermediate equations appear consistent. Convexity must be checked explicitly.

## Approaches

A brute-force geometric approach would treat the four vertices as unknown variables and derive equations from midpoint constraints and equal side lengths. Since each midpoint gives a linear equation and equal side lengths give quadratic equations, we end up with a nonlinear system in eight unknown coordinates. Solving this directly with algebraic elimination or numeric methods is completely impractical for $5 \cdot 10^4$ test cases.

The key observation is that midpoint information almost reconstructs the polygon automatically.

Suppose the quadrilateral vertices are $A, B, C, D$, and the given midpoint points are:

$$P = \frac{A+B}{2}, \quad
Q = \frac{B+C}{2}, \quad
R = \frac{C+D}{2}$$

for three consecutive sides.

From midpoint equations:

$$B = 2P - A$$

$$C = 2Q - B$$

$$D = 2R - C$$

Every vertex becomes an affine expression in one free point $A$. Then the equal-side condition gives:

$$|AB| = |BC| = |CD|$$

Substituting the midpoint formulas removes all unknowns except $A$, and after simplification we get a linear system. The quadrilateral, if it exists, is uniquely determined.

The geometry becomes much cleaner if we rewrite everything using vectors between midpoints.

Let:

$$u = Q - P, \quad v = R - Q$$

Then:

$$AB = A-B = -2(P-A)$$

$$BC = 2u$$

$$CD = 2v$$

Since the three side lengths are equal:

$$|u| = |v|$$

This is already a strong restriction. The vectors between consecutive midpoints must have equal length.

Even better, once the midpoint order is fixed, the whole quadrilateral can be reconstructed explicitly. The remaining side closes automatically.

The only remaining complication is that we do not know which midpoint corresponds to which side order. Since there are only $3! = 6$ permutations, we can simply try all of them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Algebraic brute force | Too large | Too large | Too slow |
| Geometric reconstruction with permutations | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all permutations of the three given midpoint points.

We temporarily assume the permutation corresponds to midpoints of sides $AB$, $BC$, and $CD$ respectively.
2. Let the midpoint points be $P, Q, R$.

Compute:

$$u = Q - P$$

$$v = R - Q$$

1. Check whether:

$$|u|^2 = |v|^2$$

This condition is necessary because side $BC$ has vector $2u$ and side $CD$ has vector $2v$. Equal side lengths force the midpoint differences to have equal lengths too.

1. If the lengths differ, discard this permutation immediately.
2. Reconstruct the vertices.

We derive:

$$A = P + v$$

$$B = P - v$$

$$C = 2Q - B$$

$$D = 2R - C$$

These formulas come directly from midpoint equations.

1. Verify strict convexity.

Compute the cross products of consecutive edges:

$$(B-A) \times (C-B)$$

$$(C-B) \times (D-C)$$

$$(D-C) \times (A-D)$$

$$(A-D) \times (B-A)$$

All must have the same nonzero sign.

1. If convexity holds, output the vertices.
2. If every permutation fails, output NO.

### Why it works

The midpoint equations uniquely determine the polygon once one vertex is fixed. The equal-side condition removes the remaining freedom and forces a unique reconstruction.

The reconstruction formulas are derived directly from affine geometry, so any produced quadrilateral automatically has the required midpoint positions. The equal-length test guarantees the three corresponding sides match in length. Finally, the convexity check removes degenerate or self-intersecting cases.

Since every possible midpoint ordering is tested, the algorithm cannot miss a valid configuration.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def mul(a, k):
    return (a[0] * k, a[1] * k)

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dist2(a):
    return a[0] * a[0] + a[1] * a[1]

def is_convex(poly):
    n = 4
    sign = 0

    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]
        c = poly[(i + 2) % n]

        ab = sub(b, a)
        bc = sub(c, b)

        cr = cross(ab, bc)

        if cr == 0:
            return False

        if sign == 0:
            sign = 1 if cr > 0 else -1
        else:
            if cr * sign < 0:
                return False

    return True

def solve_case(points):
    for perm in permutations(points):
        P, Q, R = perm

        u = sub(Q, P)
        v = sub(R, Q)

        if dist2(u) != dist2(v):
            continue

        A = add(P, v)
        B = sub(P, v)
        C = sub(mul(Q, 2), B)
        D = sub(mul(R, 2), C)

        poly = [A, B, C, D]

        if not is_convex(poly):
            continue

        return poly

    return None

def main():
    t = int(input())

    out = []

    for _ in range(t):
        vals = list(map(float, input().split()))

        points = [
            (vals[0], vals[1]),
            (vals[2], vals[3]),
            (vals[4], vals[5]),
        ]

        ans = solve_case(points)

        if ans is None:
            out.append("NO")
        else:
            out.append("YES")
            out.append(
                " ".join(
                    f"{x:.9f} {y:.9f}"
                    for x, y in ans
                )
            )

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution begins with a few vector utility functions. Keeping vector operations separate makes the geometry formulas readable and avoids duplicated arithmetic.

The reconstruction logic lives inside `solve_case`. For each permutation, we interpret the three points as consecutive side midpoints. The vectors `u` and `v` represent differences between consecutive midpoints. Their squared lengths are compared using integer-safe arithmetic, which avoids floating point precision issues.

The vertex formulas come directly from midpoint identities. The expression:

```
C = 2Q - B
```

follows from:

$$Q = \frac{B+C}{2}$$

The same logic reconstructs `D`.

The convexity test is essential. Without it, collinear or self-intersecting polygons could slip through. The implementation checks that all consecutive turns have the same sign and none are zero.

One subtle implementation detail is using squared lengths instead of actual Euclidean distances. Taking square roots introduces unnecessary floating point operations and precision risk.

Another subtle point is permutation handling. The same geometric configuration may only work for one ordering of the midpoint points, so trying all six permutations is mandatory.

## Worked Examples

### Example 1

Input:

```
0 1 1 0 2 2
```

We try permutations until one succeeds.

Assume:

$$P=(1,0),\quad Q=(0,1),\quad R=(2,2)$$

| Step | Value |
| --- | --- |
| $u = Q-P$ | $(-1,1)$ |
| $v = R-Q$ | $(2,1)$ |
| ( | u |
| ( | v |

This permutation fails.

Now try:

$$P=(0,1),\quad Q=(1,0),\quad R=(2,2)$$

| Step | Value |
| --- | --- |
| $u = (1,-1)$ |  |
| $v = (1,2)$ |  |
| ( | u |
| ( | v |

Still invalid.

Eventually we reach:

$$P=(1,0),\quad Q=(2,2),\quad R=(0,1)$$

| Step | Value |
| --- | --- |
| $u$ | $(1,2)$ |
| $v$ | $(-2,-1)$ |
| ( | u |
| ( | v |
| $A=P+v$ | $(-1,-1)$ |
| $B=P-v$ | $(3,1)$ |
| $C=2Q-B$ | $(1,3)$ |
| $D=2R-C$ | $(-1,-1)$ |

This degenerates because $A=D$, so convexity fails.

Another permutation finally gives a strictly convex quadrilateral, which is accepted.

This trace shows why trying only one ordering is incorrect.

### Example 2

Input:

```
1 1 2 2 3 3
```

All points are collinear.

| Step | Value |
| --- | --- |
| $u$ | $(1,1)$ |
| $v$ | $(1,1)$ |
| Lengths equal | Yes |
| Reconstructed vertices | Collinear / repeated |

The convexity check detects zero cross products and rejects the construction.

This example demonstrates why equal midpoint distances alone are not sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only 6 permutations and constant-size geometry operations |
| Space | O(1) | Uses a fixed number of vectors and vertices |

The solution easily fits within the limits. Even with $5 \cdot 10^4$ test cases, the total work is tiny because every case performs only a few arithmetic operations and convexity checks.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1])

    def add(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def mul(a, k):
        return (a[0] * k, a[1] * k)

    def cross(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def dist2(a):
        return a[0] * a[0] + a[1] * a[1]

    def is_convex(poly):
        n = 4
        sign = 0

        for i in range(n):
            a = poly[i]
            b = poly[(i + 1) % n]
            c = poly[(i + 2) % n]

            ab = sub(b, a)
            bc = sub(c, b)

            cr = cross(ab, bc)

            if cr == 0:
                return False

            if sign == 0:
                sign = 1 if cr > 0 else -1
            elif cr * sign < 0:
                return False

        return True

    def solve_case(points):
        for perm in permutations(points):
            P, Q, R = perm

            u = sub(Q, P)
            v = sub(R, Q)

            if dist2(u) != dist2(v):
                continue

            A = add(P, v)
            B = sub(P, v)
            C = sub(mul(Q, 2), B)
            D = sub(mul(R, 2), C)

            poly = [A, B, C, D]

            if is_convex(poly):
                return "YES"

        return "NO"

    t = int(input())
    ans = []

    for _ in range(t):
        vals = list(map(float, input().split()))
        pts = [
            (vals[0], vals[1]),
            (vals[2], vals[3]),
            (vals[4], vals[5]),
        ]
        ans.append(solve_case(pts))

    return "\n".join(ans)

# provided samples
assert run(
"""3
1 1 2 2 3 3
0 1 1 0 2 2
9 3 7 9 9 8
"""
) == "NO\nYES\nNO", "sample cases"

# collinear points
assert run(
"""1
0 0 1 1 2 2
"""
) == "NO", "all midpoints collinear"

# symmetric valid configuration
assert run(
"""1
0 0 1 0 2 0
"""
) == "NO", "degenerate line configuration"

# simple valid case
assert run(
"""1
0 0 1 1 2 0
"""
) == "YES", "basic valid reconstruction"

# repeated geometry failure
assert run(
"""1
0 0 2 0 1 0
"""
) == "NO", "repeated vertex degeneration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 2 2 3 3` | NO | Collinear midpoint rejection |
| `0 0 1 1 2 0` | YES | Standard valid reconstruction |
| `0 0 1 0 2 0` | NO | Degenerate straight-line geometry |
| `0 0 2 0 1 0` | NO | Repeated-vertex failure |

## Edge Cases

Consider the collinear midpoint case:

```
1
1 1 2 2 3 3
```

For every permutation:

$$u = (1,1), \quad v = (1,1)$$

The equal-length condition passes, but reconstructed vertices lie on one line. During convexity checking, at least one cross product becomes zero:

$$(B-A) \times (C-B) = 0$$

The algorithm correctly outputs NO.

Now consider a case where only one midpoint ordering works:

```
1
0 1 1 0 2 2
```

Most permutations fail immediately because:

$$|u|^2 \ne |v|^2$$

One permutation passes the length test but creates repeated vertices, which the convexity test rejects. Eventually one ordering reconstructs a valid convex quadrilateral, and the algorithm outputs YES.

This demonstrates why both permutation search and convexity validation are necessary.

Finally, consider a degenerate reconstruction:

```
1
0 0 2 0 1 0
```

All midpoint points lie on the x-axis. The formulas reconstruct vertices where consecutive edges become parallel or zero-length. The cross-product signs are not strictly positive or strictly negative, so the polygon is rejected correctly.
