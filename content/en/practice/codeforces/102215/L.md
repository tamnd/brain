---
title: "CF 102215L - Inscribed Circle"
description: "We have two disks, each described by a center and a positive radius. Their circumferences intersect at exactly two points, so neither disk contains the other and their intersection is a non-degenerate lens-shaped region."
date: "2026-08-18T22:13:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "L"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 525
verified: false
draft: false
---

[CF 102215L - Inscribed Circle](https://codeforces.com/problemset/problem/102215/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We have two disks, each described by a center and a positive radius. Their circumferences intersect at exactly two points, so neither disk contains the other and their intersection is a non-degenerate lens-shaped region.

We need to find the largest possible circle that fits completely inside this lens. The output is the center of that circle and its radius, with enough precision to satisfy an absolute or relative error of (10^{-9}).

The coordinates and radii are at most (1000) in magnitude, so all relevant distances are comfortably within ordinary floating-point range. There is also no large input size: the problem contains only two circles. The 2 second limit is therefore not a concern for an (O(1)) geometric solution. Even an iterative numerical method with a few hundred iterations would be fast enough, but the geometry lets us avoid iteration entirely.

The first subtle case is when the circles have equal radii. For example,

```
0 0 5
6 0 5
```

The answer is

```
3 0 2
```

A careless implementation might assume the optimal center is one of the original centers, but the correct center is halfway between them. More generally, symmetry places the answer on the line connecting the two circle centers, not necessarily at its midpoint.

Another case is when the radii differ:

```
0 0 5
7 0 3
```

Here the circles intersect because (2 < 7 < 8). The optimal center is at distance

[
\frac{7+5-3}{2}=4.5
]

from the first center, and the resulting radius is

[
\frac{5+3-7}{2}=0.5.
]

A common mistake is to use the midpoint of the centers regardless of the radii. That would give the wrong answer because the larger circle can accommodate the optimal center farther toward the smaller circle.

The final edge case concerns circles whose boundaries intersect very close to tangency. For example,

```
0 0 1
1.999999 0 1
```

The answer has a very small radius, approximately (5\times10^{-7}). Implementations that use integer arithmetic, insufficient precision, or formulas involving subtraction of nearly equal quantities carelessly can lose accuracy. The direct formula using the center distance remains stable enough with Python's double precision for the required error.

## Approaches

A naive geometric approach could search over possible center positions on a fine grid. For every candidate point, we would compute how much radius can be placed there, namely the smaller of its distances to the two circle boundaries. To reach (10^{-9}) positional precision over a coordinate range of roughly (2000), a uniform grid would require on the order of

[
2000^2 / 10^{-18} = 4\cdot10^{24}
]

candidate points. Even one constant-time calculation per point is hopeless.

A more reasonable numerical approach would reduce the search to one dimension and use ternary search. The symmetry of the lens means the optimal center lies on the line joining the two original centers. We could parameterize that line and maximize the feasible radius numerically. A few hundred iterations would already be enough, so this approach is actually fast enough, but it is unnecessary and introduces convergence and precision details that the exact geometry avoids.

The key observation is that for a point on the segment joining the centers, the distance to the first center increases exactly as the distance to the second center decreases. Suppose the centers are (C_1,C_2), their distance is (d), and the candidate center (P) is at distance (t) from (C_1). Then it is (d-t) from (C_2).

A circle centered at (P) fits inside the first disk with radius at most

[
r_1-t,
]

and it fits inside the second disk with radius at most

[
r_2-(d-t).
]

Hence its maximum feasible radius at (P) is

[
f(t)=\min(r_1-t,\ r_2-d+t).
]

The first expression decreases with (t), while the second increases with (t). The maximum of their minimum occurs exactly where they are equal. Solving

[
r_1-t=r_2-d+t
]

gives

[
t=\frac{d+r_1-r_2}{2}.
]

Substituting this value gives

[
r=\frac{r_1+r_2-d}{2}.
]

The problem's guarantee that the circumferences have exactly two common points gives

[
|r_1-r_2|<d<r_1+r_2.
]

Consequently, the computed (t) lies strictly between (0) and (d), and the computed radius is strictly positive. We can then place the answer at the corresponding point on the line between the two centers.

The brute-force search works because it directly evaluates the feasible radius of candidate centers, but it wastes almost all of its work exploring a two-dimensional continuous region. The observation that the optimal center must lie on the center-to-center axis reduces the problem to one dimension, and the fact that the two limiting radii are linear functions reduces that one-dimensional optimization to solving one equation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(1/\varepsilon^2)) grid samples | (O(1)) | Too slow |
| Numerical ternary search | (O(I)) | (O(1)) | Accepted but unnecessary |
| Geometric formula | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the centers (C_1=(x_1,y_1)), (C_2=(x_2,y_2)) and radii (r_1,r_2). The only geometric quantity we need initially is the distance between the two centers.
2. Compute

[
d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}.
]

Because the circles intersect at two points, (d>0), so the direction from (C_1) to (C_2) is well-defined.

1. Determine how far the desired center lies from (C_1):

[
t=\frac{d+r_1-r_2}{2}.
]

This comes from balancing the two available boundary distances. If the answer were closer to (C_1), the first circle would permit more radius while the second would be the limiting circle. If it were farther toward (C_2), the situation would reverse. The maximum is exactly at the balance point.

1. Convert the distance (t) into coordinates. The unit vector from (C_1) to (C_2) is

[
\left(\frac{x_2-x_1}{d},\frac{y_2-y_1}{d}\right).
]

Thus the answer center is

[
x=x_1+\frac{x_2-x_1}{d}t,
\qquad
y=y_1+\frac{y_2-y_1}{d}t.
]

1. Compute the radius using either limiting circle:

[
r=r_1-t.
]

After substituting the value of (t), this can also be written as

[
r=\frac{r_1+r_2-d}{2}.
]

1. Print the center and radius with many digits after the decimal point. Python's `float` is a 64-bit IEEE-754 double, which provides substantially more precision than the required (10^{-9}) error.

### Why it works

For any circle centered at a point (P) inside the lens, its radius cannot exceed the distance from (P) to either original circumference. The optimal center can be chosen on the line joining the original centers because reflecting any feasible circle across that line preserves both original disks, and the lens is symmetric about that line. On this axis, the two available radii are (r_1-t) and (r_2-d+t). One decreases as the center moves toward (C_2), while the other increases. Their minimum is maximized exactly at their intersection. The algorithm computes that intersection and places the center there, so no other point can admit a larger circle.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x2 - x1
    dy = y2 - y1

    d = math.hypot(dx, dy)

    t = (d + r1 - r2) / 2.0

    x = x1 + dx * t / d
    y = y1 + dy * t / d

    r = (r1 + r2 - d) / 2.0

    print(f"{x:.15f} {y:.15f} {r:.15f}")

if __name__ == "__main__":
    solve()
```

The first part reads the two circles and computes `dx` and `dy`, the displacement from the first center to the second. `math.hypot(dx, dy)` calculates the center distance without requiring us to write the square root explicitly.

The variable `t` is the distance from the first center to the optimal center. The guarantee about two intersection points means `t` is strictly positive and strictly smaller than `d`, so dividing by `d` is safe.

The coordinates are obtained by moving from the first center in the direction of the second center by exactly `t`. Writing the calculation as `dx * t / d` and `dy * t / d` avoids separately constructing a unit-vector tuple.

The radius uses the symmetric formula `(r1 + r2 - d) / 2`. Computing it directly is simpler than calculating `r1 - t`, and it avoids an unnecessary extra subtraction.

There are no integer-overflow concerns in Python because integers have arbitrary precision. The only floating-point operations involve values whose magnitude is at most a few thousand, so double precision comfortably handles them.

Printing fifteen digits after the decimal point gives much more precision than required. The judge compares the numerical values, not the formatting.

## Worked Examples

### Sample 1

The input is

```
0 0 5
6 0 5
```

The main variables evolve as follows.

| Variable | Value |
| --- | --- |
| (dx) | (6) |
| (dy) | (0) |
| (d) | (6) |
| (t=(d+r_1-r_2)/2) | (3) |
| (x= x_1+dx\cdot t/d) | (3) |
| (y= y_1+dy\cdot t/d) | (0) |
| (r=(r_1+r_2-d)/2) | (2) |

The radii available from the two original circles are equal at the midpoint, both being (5-3=2). Moving either direction would make one of them smaller, so the midpoint is optimal.

### Sample 2

The input is

```
-12 34 56
78 -90 123
```

The displacement and derived values are approximately

| Variable | Value |
| --- | --- |
| (dx) | (90) |
| (dy) | (-124) |
| (d) | (153.2239) |
| (t=(d+56-123)/2) | (43.1119) |
| (x) | (13.3222578218559) |
| (y) | (-0.8884441101126) |
| (r=(56+123-d)/2) | (12.8906010988208) |

Here the radii are quite different, so the optimal center is not halfway between the original centers. It lies closer to the smaller circle's center, exactly as the balancing equation predicts.

The two boundary distances from the resulting center are both approximately (12.8906011) after subtracting the appropriate center distance from the corresponding original radius. This confirms the central invariant that both original circles are tight at the optimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | A constant number of arithmetic operations and one square root are performed. |
| Space | (O(1)) | Only the two circles and a constant number of intermediate values are stored. |

The input contains only two circles, so an (O(1)) solution is far below the 2 second and 256 MB limits. More importantly, the formula avoids any iterative precision tuning, making the numerical behavior predictable.

## Test Cases

For floating-point output, comparing the complete output string is inappropriate because many different decimal representations can describe the same answer. The test helper below parses the three numbers and checks them with a strict absolute and relative tolerance.

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x2 - x1
    dy = y2 - y1

    d = math.hypot(dx, dy)

    t = (d + r1 - r2) / 2.0

    x = x1 + dx * t / d
    y = y1 + dy * t / d

    r = (r1 + r2 - d) / 2.0

    print(f"{x:.15f} {y:.15f} {r:.15f}")

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

def assert_answer(inp: str, expected, message: str):
    out = run(inp).split()
    got = list(map(float, out))

    assert len(got) == 3, message

    for a, b in zip(got, expected):
        assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9), (
            f"{message}: got {got}, expected {expected}"
        )

# Provided sample 1
assert_answer(
    "0 0 5\n6 0 5\n",
    (3.0, 0.0, 2.0),
    "sample 1"
)

# Provided sample 2
assert_answer(
    "-12 34 56\n78 -90 123\n",
    (13.322257821855908, -0.888444110112585, 12.890601098820779),
    "sample 2"
)

# Minimum radii, equal circles, center distance 1
assert_answer(
    "0 0 1\n1 0 1\n",
    (0.5, 0.0, 0.5),
    "minimum-size circles"
)

# Equal values and diagonal center displacement
# d = sqrt(2), so t = sqrt(2)/2 and the answer is (0.5, 0.5).
assert_answer(
    "0 0 1\n1 1 1\n",
    (0.5, 0.5, (2.0 - math.sqrt(2.0)) / 2.0),
    "equal circles on a diagonal"
)

# Very close to external tangency
assert_answer(
    "0 0 1\n1.999999 0 1\n",
    (0.9999995, 0.0, 0.0000005),
    "near-tangent circles"
)

# Unequal radii, catches midpoint assumptions
assert_answer(
    "0 0 5\n7 0 3\n",
    (4.5, 0.0, 0.5),
    "unequal radii"
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1` and `1 0 1` | `(0.5, 0, 0.5)` | Minimum radii and symmetric case |
| `0 0 1` and `1 1 1` | `(0.5, 0.5, (2-sqrt(2))/2)` | Diagonal direction and distance normalization |
| `0 0 1` and `1.999999 0 1` | `(0.9999995, 0, 0.0000005)` | Precision near tangency |
| `0 0 5` and `7 0 3` | `(4.5, 0, 0.5)` | Unequal radii and non-midpoint optimum |

## Edge Cases

The equal-radius case

```
0 0 1
1 0 1
```

has (d=1), so

[
t=\frac{1+1-1}{2}=0.5
]

and

[
r=\frac{1+1-1}{2}=0.5.
]

The center is `(0.5, 0)`. A midpoint-based implementation happens to work here, but the formula explains why it works and also generalizes to unequal radii.

The diagonal case

```
0 0 1
1 1 1
```

has (d=\sqrt2). The formula gives

[
t=\frac{\sqrt2}{2}.
]

The unit direction from the first center to the second is

[
\left(\frac1{\sqrt2},\frac1{\sqrt2}\right),
]

so multiplying by (t) gives `(0.5, 0.5)`. This catches implementations that accidentally use `dx` and `dy` directly as if the center distance were always horizontal.

The near-tangent case

```
0 0 1
1.999999 0 1
```

has

[
d=1.999999
]

and therefore

[
r=\frac{2-1.999999}{2}=0.0000005.
]

The optimal center is `(0.9999995, 0)`. The radius is positive but extremely small, which tests whether the implementation preserves enough floating-point precision.

Finally, the unequal-radius case

```
0 0 5
7 0 3
```

gives

[
t=\frac{7+5-3}{2}=4.5
]

and

[
r=\frac{5+3-7}{2}=0.5.
]

The center is `(4.5, 0)`, not `(3.5, 0)`. This is the most useful test against the common but incorrect assumption that symmetry always puts the answer at the midpoint of the two original centers.
