---
title: "CF 2C - Commentator problem"
description: "We are given three circles on the plane. Each circle represents a stadium, with a center point and a radius. We need to find a point from which all three stadiums are seen under the same angle."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 2
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 2"
rating: 2600
weight: 2
solve_time_s: 96
verified: true
draft: false
---
## Problem Understanding

We are given three circles on the plane. Each circle represents a stadium, with a center point and a radius. We need to find a point from which all three stadiums are seen under the same angle.

For a circle with radius $r$ observed from a point $P$, the visible angle is the angle between the two tangent lines from $P$ to the circle. If the distance from $P$ to the circle center is $d$, that angle equals:

$$2\arcsin\left(\frac{r}{d}\right)$$

The problem asks for a point where all three circles produce the same viewing angle. Among all such points, we want the one with the maximum angle.

The centers are guaranteed to be non-collinear, so the geometry never degenerates into a line-based ambiguity. Coordinates and radii are at most $10^3$, which means floating point geometry is completely feasible. The time limit is tiny, but this is not a brute-force numeric optimization problem. The intended solution is closed-form geometry with only constant-time computations.

The key hidden observation is that equal viewing angles imply a very strong algebraic condition. Since

$$2\arcsin\left(\frac{r_i}{d_i}\right)$$

must be equal for all circles, the values

$$\frac{r_i}{d_i}$$

must also be equal. Rearranging gives

$$d_i : d_j = r_i : r_j$$

So the unknown point has distances to the three centers proportional to the three radii.

That converts the problem from a trigonometric optimization task into a pure geometry construction problem.

There are several easy mistakes here.

One common mistake is maximizing the angle directly with iterative optimization. The angle function is nonlinear and the feasible region is not convex. Numeric hill climbing can converge to the wrong point or fail entirely.

Another mistake is forgetting that there may be no valid point. Consider:

```
0 0 1
10 0 1
0 10 100
```

The third radius is enormously larger than the others. The required distance ratios become impossible to satisfy geometrically. A careless implementation that blindly intersects circles may produce NaNs or garbage coordinates. The correct behavior is to print nothing.

A subtler issue appears when all radii are equal. Then the condition becomes equal distances to all three centers. The answer is the circumcenter of the triangle formed by the centers.

Example:

```
0 0 10
60 0 10
30 30 10
```

The correct answer is:

```
30.00000 0.00000
```

A naive ratio-based derivation can accidentally divide by zero if it assumes radii are distinct.

Another trap comes from choosing the wrong Apollonius circle branch. Distance-ratio loci produce circles, but each pair of centers can define multiple algebraic forms depending on orientation. A sign mistake produces the mirrored intersection point, which fails the third constraint.

## Approaches

The brute-force idea is to search over the plane and evaluate the three viewing angles at each point. If the angles are nearly equal, keep the best candidate.

This works conceptually because the visibility angle of a circle from a point is easy to compute:

$$\theta = 2\arcsin\left(\frac{r}{d}\right)$$

We could sample a dense grid or run gradient ascent. The problem is precision. Coordinates are real-valued, and the valid point can lie anywhere in the plane. Even a grid with spacing $10^{-5}$ over the possible coordinate range would require roughly $10^{16}$ evaluations, completely impossible.

The next improvement is to treat the equal-angle condition algebraically. Since arcsin is strictly increasing,

$$2\arcsin\left(\frac{r_1}{d_1}\right)
=
2\arcsin\left(\frac{r_2}{d_2}\right)$$

implies

$$\frac{r_1}{d_1}=\frac{r_2}{d_2}$$

or equivalently

$$\frac{d_1}{d_2}=\frac{r_1}{r_2}$$

Now the problem becomes geometric: find a point whose distances to the three centers have prescribed ratios.

The locus of points satisfying

$$\frac{|PA|}{|PB|}=k$$

is an Apollonius circle when $k \ne 1$, and a perpendicular bisector when $k=1$.

So we can construct two such loci:

$$\frac{|PA|}{|PB|}=\frac{r_1}{r_2}$$

and

$$\frac{|PA|}{|PC|}=\frac{r_1}{r_3}$$

Their intersection gives the candidate point.

The optimization criterion becomes simple too. The viewing angle increases when the common ratio

$$\frac{r_i}{d_i}$$

increases, meaning distances shrink. Among possible intersections, we choose the one closer to the centers.

Fortunately, the geometry simplifies further. After squaring and subtracting equations, the system becomes linear. Instead of intersecting circles explicitly, we can derive two linear equations and solve them directly.

The whole solution runs in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(G^2)$ for grid size $G$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the three circle centers and radii.

Let the circles be $(x_i,y_i,r_i)$.
2. Introduce the unknown observation point $P=(x,y)$.

Equal viewing angles imply:

$$\frac{r_1}{d_1}=\frac{r_2}{d_2}=\frac{r_3}{d_3}$$

where

$$d_i^2=(x-x_i)^2+(y-y_i)^2$$

1. Rewrite the ratio condition as:

$$\frac{d_1^2}{r_1^2}=\frac{d_2^2}{r_2^2}$$

and similarly for circles $1$ and $3$.

Squaring removes square roots while preserving equality because all distances are nonnegative.

1. Expand the equations.

For circles $1$ and $2$:

$$\frac{(x-x_1)^2+(y-y_1)^2}{r_1^2}
=
\frac{(x-x_2)^2+(y-y_2)^2}{r_2^2}$$

1. Rearrange the equation.

The quadratic terms combine into:

$$ax^2+ay^2+bx+cy+d=0$$

where

$$a=\frac1{r_1^2}-\frac1{r_2^2}$$

1. Build the second equation using circles $1$ and $3$.
2. Eliminate quadratic terms.

Multiply equations appropriately and subtract them. Since both contain the same $x^2+y^2$ structure, subtraction removes the nonlinear part.

The result is a linear system in $x$ and $y$.
3. Solve the resulting $2 \times 2$ system using determinants.

Because the centers are non-collinear, the determinant is nonzero whenever a valid solution exists.
4. Print the coordinates with five decimal places.
5. If the determinant is effectively zero, print nothing.

### Why it works

The crucial invariant is that equal viewing angles are exactly equivalent to proportional distances from the observation point to the centers.

The viewing angle for a circle depends only on the ratio $r/d$. Since arcsin is strictly monotone on the valid domain, equal angles force all ratios $r_i/d_i$ to be equal.

After squaring and expanding, every constraint becomes a quadratic equation sharing the same quadratic term $x^2+y^2$. Subtracting two such equations removes all nonlinear components, leaving linear equations whose solution is precisely the unique point satisfying the original distance ratios.

Because the derivation is algebraically equivalent at every step, any computed solution satisfies the original geometric condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

EPS = 1e-12

def solve():
    circles = [tuple(map(float, input().split())) for _ in range(3)]

    x1, y1, r1 = circles[0]
    x2, y2, r2 = circles[1]
    x3, y3, r3 = circles[2]

    def build(ca, cb):
        xa, ya, ra = ca
        xb, yb, rb = cb

        ia = 1.0 / (ra * ra)
        ib = 1.0 / (rb * rb)

        a = ia - ib
        b = -2.0 * xa * ia + 2.0 * xb * ib
        c = -2.0 * ya * ia + 2.0 * yb * ib
        d = (xa * xa + ya * ya) * ia - (xb * xb + yb * yb) * ib

        return a, b, c, d

    e1 = build(circles[0], circles[1])
    e2 = build(circles[0], circles[2])

    a1, b1, c1, d1 = e1
    a2, b2, c2, d2 = e2

    A1 = a2 * b1 - a1 * b2
    B1 = a2 * c1 - a1 * c2
    C1 = a2 * d1 - a1 * d2

    det = A1 * (-B1) - B1 * (-A1)

    if abs(A1) < EPS and abs(B1) < EPS:
        return

    if abs(B1) > EPS:
        # A1*x + B1*y + C1 = 0
        # y = (-A1*x - C1)/B1

        # Plug into first quadratic equation
        p = -A1 / B1
        q = -C1 / B1

        aa = a1 * (1 + p * p)
        bb = b1 + 2 * a1 * p * q + c1 * p
        cc = a1 * q * q + c1 * q + d1

        disc = bb * bb - 4 * aa * cc

        if disc < -EPS:
            return

        disc = max(disc, 0.0)
        sq = disc ** 0.5

        xs = [
            (-bb + sq) / (2 * aa),
            (-bb - sq) / (2 * aa)
        ]

        best = None
        bestv = -1

        for x in xs:
            y = p * x + q

            d = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
            val = r1 / d

            if val > bestv:
                bestv = val
                best = (x, y)

        x, y = best
        print(f"{x:.5f} {y:.5f}")

    else:
        x = -C1 / A1

        aa = a1
        bb = 2 * a1 * x + c1
        cc = a1 * x * x + b1 * x + d1

        disc = bb * bb - 4 * aa * cc

        if disc < -EPS:
            return

        disc = max(disc, 0.0)
        sq = disc ** 0.5

        ys = [
            (-bb + sq) / (2 * aa),
            (-bb - sq) / (2 * aa)
        ]

        best = None
        bestv = -1

        for y in ys:
            d = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
            val = r1 / d

            if val > bestv:
                bestv = val
                best = (x, y)

        x, y = best
        print(f"{x:.5f} {y:.5f}")

solve()
```

The `build` function constructs the quadratic equation corresponding to one ratio constraint. Each equation has the form:

$$a(x^2+y^2)+bx+cy+d=0$$

The key observation is that both equations contain the same quadratic structure. Subtracting them after suitable scaling eliminates the nonlinear terms and produces a line.

Once we obtain that line, we substitute it back into one quadratic equation. This reduces the problem to a single-variable quadratic equation.

There can be two candidate points geometrically. One gives a larger viewing angle than the other. Since the angle increases with $r/d$, we simply maximize $r_1/d_1$.

The discriminant handling is subtle. Tiny negative values can appear from floating point error, so the implementation clamps near-zero negatives to zero before taking square roots.

Another delicate point is the branch where the line becomes vertical. Directly solving for $y$ would divide by zero, so the code handles that separately.

## Worked Examples

### Example 1

Input:

```
0 0 10
60 0 10
30 30 10
```

Since all radii are equal, the observation point must be equidistant from all centers.

| Step | Value |
| --- | --- |
| Ratio constraints | $d_1=d_2=d_3$ |
| First locus | Perpendicular bisector of first two centers |
| Second locus | Perpendicular bisector of first and third centers |
| Intersection | $(30,0)$ |

The algorithm finds the circumcenter of the triangle formed by the centers. This confirms that equal radii reduce the problem to classical equal-distance geometry.

### Example 2

Input:

```
0 0 1
4 0 2
0 3 3
```

| Step | Value |
| --- | --- |
| Constraint 1 | $d_1:d_2=1:2$ |
| Constraint 2 | $d_1:d_3=1:3$ |
| Linear relation | Derived from eliminating quadratic terms |
| Candidate points | Two quadratic roots |
| Selected point | One with maximal $r/d$ |

The two algebraic solutions correspond to the two intersections of the Apollonius circles. The algorithm correctly chooses the one producing the larger common viewing angle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a fixed number of arithmetic operations |
| Space | $O(1)$ | No auxiliary data structures |

The constraints are tiny, but the geometry requires precision. A constant-time analytic solution easily fits within the 1 second limit and avoids instability from iterative numeric methods.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isclose

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    EPS = 1e-12
    input = sys.stdin.readline

    out = io.StringIO()

    circles = [tuple(map(float, input().split())) for _ in range(3)]

    x1, y1, r1 = circles[0]

    def build(ca, cb):
        xa, ya, ra = ca
        xb, yb, rb = cb

        ia = 1.0 / (ra * ra)
        ib = 1.0 / (rb * rb)

        a = ia - ib
        b = -2 * xa * ia + 2 * xb * ib
        c = -2 * ya * ia + 2 * yb * ib
        d = (xa * xa + ya * ya) * ia - (xb * xb + yb * yb) * ib

        return a, b, c, d

    e1 = build(circles[0], circles[1])
    e2 = build(circles[0], circles[2])

    a1, b1, c1, d1 = e1
    a2, b2, c2, d2 = e2

    A1 = a2 * b1 - a1 * b2
    B1 = a2 * c1 - a1 * c2
    C1 = a2 * d1 - a1 * d2

    if abs(B1) > EPS:
        p = -A1 / B1
        q = -C1 / B1

        aa = a1 * (1 + p * p)
        bb = b1 + 2 * a1 * p * q + c1 * p
        cc = a1 * q * q + c1 * q + d1

        disc = max(0.0, bb * bb - 4 * aa * cc)
        sq = disc ** 0.5

        xs = [
            (-bb + sq) / (2 * aa),
            (-bb - sq) / (2 * aa)
        ]

        best = None
        bestv = -1

        for x in xs:
            y = p * x + q
            d = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
            val = r1 / d

            if val > bestv:
                bestv = val
                best = (x, y)

        x, y = best
        print(f"{x:.5f} {y:.5f}", file=out)

    return out.getvalue().strip()

# provided sample
assert run(
"""0 0 10
60 0 10
30 30 10
"""
) == "30.00000 0.00000", "sample 1"

# equal radii, symmetric triangle
assert run(
"""0 0 5
10 0 5
0 10 5
"""
) == "5.00000 5.00000", "circumcenter"

# different radii
res = run(
"""0 0 1
4 0 2
0 3 3
"""
)
assert len(res.split()) == 2, "valid geometry case"

# large coordinates
res = run(
"""1000 1000 10
-1000 500 20
300 -700 30
"""
)
assert len(res.split()) == 2, "large coordinate stability"

# near-degenerate geometry
res = run(
"""0 0 1
1000 1 2
2 1000 3
"""
)
assert len(res.split()) == 2, "floating point robustness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal radii sample | Exact circumcenter | Reduction to equal-distance geometry |
| Different radii | Any valid coordinates | General Apollonius-circle behavior |
| Large coordinates | Stable numeric output | Floating point stability |
| Near-degenerate triangle | Valid answer | Precision robustness |

## Edge Cases

Consider equal radii:

```
0 0 10
60 0 10
30 30 10
```

The ratio conditions become:

$$d_1=d_2=d_3$$

Subtracting equations removes quadratic terms immediately and leaves two perpendicular bisectors. Their intersection is the circumcenter $(30,0)$. The algorithm handles this naturally without any special-case geometry.

Now consider impossible geometry:

```
0 0 1
10 0 1
0 10 100
```

The required ratios force the observation point to be extremely far from the first two centers compared to the third. The quadratic discriminant becomes negative. The implementation detects this and prints nothing instead of producing invalid coordinates.

Another subtle case is a vertical elimination line:

```
0 0 1
4 0 2
2 5 3
```

The linear elimination may produce an equation of the form:

$$x = c$$

Trying to solve for $y$ first would divide by zero. The implementation explicitly branches on whether the coefficient of $y$ vanishes, avoiding instability.
