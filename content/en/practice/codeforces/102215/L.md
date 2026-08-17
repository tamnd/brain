---
title: "CF 102215L - Inscribed Circle"
description: "We have two circles, each described by its center and radius. Their circumferences intersect at exactly two points, so neither circle contains the other and the two disks overlap in a proper lens-shaped region."
date: "2026-08-17T23:53:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "L"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 139
verified: false
draft: false
---

[CF 102215L - Inscribed Circle](https://codeforces.com/problemset/problem/102215/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have two circles, each described by its center and radius. Their circumferences intersect at exactly two points, so neither circle contains the other and the two disks overlap in a proper lens-shaped region. We need the largest circle that fits completely inside that overlap, and we must print its center and radius. The input bounds and required precision are those given in the original problem statement.

Let the centers be (O_1=(x_1,y_1)) and (O_2=(x_2,y_2)), with radii (r_1) and (r_2). Let

[
d=|O_1O_2|
]

be the distance between the centers. Having exactly two intersection points gives the strict inequalities

[
|r_1-r_2|<d<r_1+r_2.
]

The upper bound guarantees a positive overlap, while the lower bound prevents one disk from being completely inside the other. These strict inequalities are especially useful because they guarantee that the final radius is positive and that the two centers are distinct.

The coordinate bounds are only ([-1000,1000]), so there is no combinatorial input size here. The challenge is geometric precision, not running time. A solution that performs a constant number of floating-point operations is easily within the 2 second and 256 MB limits, while numerical searches or dense enumeration are unnecessary.

A careless implementation can fail when the circles have equal radii but are not centered on a horizontal line. For example,

```
0 0 5
3 4 5
```

has (d=5), so the answer is a circle of radius (2.5) centered at ((1.5,2)). A solution that only changes the (x)-coordinate, or assumes that the centers always lie on the (x)-axis, produces the wrong center.

Unequal radii are another common source of mistakes. Consider

```
0 0 5
6 0 9
```

Here (d=6), and the answer is centered at ((1,0)) with radius (4). The center is not the midpoint of the two original centers. Using the midpoint blindly would give radius (3), even though the smaller circle still has unused room on one side.

The nearly tangent case also matters numerically. For example,

```
-1000 0 1000
999 0 1000
```

has (d=1999), so the answer has radius (0.5) and center ((-0.5,0)). The required radius is small even though the input values are large, so calculations should be performed in floating point and printed with enough digits.

## Approaches

A literal brute-force method would try possible positions for the center and keep the largest circle that remains inside both disks. For a candidate center (P), the largest radius allowed by the first circle is (r_1-|PO_1|), and the largest radius allowed by the second is (r_2-|PO_2|). Thus the candidate radius is their minimum.

The problem is that the center is a continuous point, so brute force needs a discretization. If we tried to inspect every coordinate on a grid with spacing (10^{-9}) over the possible coordinate range ([-2000,2000]), there would be (4\cdot10^{12}) positions along each axis, or

[
(4\cdot10^{12})^2=1.6\cdot10^{25}
]

candidate centers. That is not merely too slow for 2 seconds, it is also an awkward way to guarantee the requested precision.

A more sophisticated numerical search could reduce the work substantially, but the geometry gives us an exact constant-time solution. The brute-force method works because the validity of a candidate center can be checked directly. The key observation is that the best center does not need two-dimensional search at all.

Take any candidate center (P) inside the lens. Project (P) onto the line (O_1O_2), obtaining (Q). The projection cannot increase the distance to either (O_1) or (O_2). Consequently,

[
r_1-|QO_1|\ge r_1-|PO_1|
]

and

[
r_2-|QO_2|\ge r_2-|PO_2|.
]

So moving the center onto the line joining the two original centers never makes the possible inscribed radius smaller. We can restrict the entire optimization to one dimension.

Now place the candidate center (P) between (O_1) and (O_2). If (t=|O_1P|), then (|PO_2|=d-t). The two circles allow radii

[
r_1-t
]

and

[
r_2-(d-t).
]

The maximum of their minimum occurs exactly when these two quantities are equal. Otherwise, if one is smaller, we can move (P) slightly toward the corresponding circle and increase the smaller quantity.

Solving

[
r_1-t=r_2-d+t
]

gives

[
t=\frac{d+r_1-r_2}{2}.
]

Substituting this into either radius expression gives

[
R=\frac{r_1+r_2-d}{2}.
]

Once (t) is known, the center is simply the point at distance (t) from (O_1) in the direction of (O_2).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(G^2)) for a (G\times G) coordinate grid | (O(1)) | Too slow and cannot naturally guarantee (10^{-9}) precision |
| Optimal | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the two circle centers and their radii. Compute

[
dx=x_2-x_1,\qquad dy=y_2-y_1
]

and

[
d=\sqrt{dx^2+dy^2}.
]

The guarantee of two intersection points means (d>0), so division by (d) is safe.
2. Compute the radius of the largest circle as

[
R=\frac{r_1+r_2-d}{2}.
]

This comes from making the distances from the new center to the two original circumferences equal to the same radius.
3. Compute the distance from (O_1) to the new center:

[
t=\frac{d+r_1-r_2}{2}.
]

This is the unique point on the segment (O_1O_2) for which both original circles leave exactly (R) units of radial clearance.
4. Convert that distance into a coordinate displacement. The unit vector from (O_1) toward (O_2) is

[
\left(\frac{dx}{d},\frac{dy}{d}\right).
]

Therefore the new center is

[
x=x_1+\frac{dx}{d}t,
\qquad
y=y_1+\frac{dy}{d}t.
]
5. Print (x), (y), and (R) with many digits. Fifteen digits after the decimal point give substantially more precision than the required (10^{-9}).

The key invariant is that the chosen center lies on (O_1O_2) and has exactly the same clearance from both circle boundaries. Any valid circle centered elsewhere can be projected onto this line without reducing its possible radius. Along the line, the first circle's available radius decreases as the center moves away from (O_1), while the second circle's available radius increases. Their minimum is maximized precisely at their crossing point. Thus the computed circle is both feasible and optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x2 - x1
    dy = y2 - y1

    d = (dx * dx + dy * dy) ** 0.5

    radius = (r1 + r2 - d) / 2.0
    dist_from_first = (d + r1 - r2) / 2.0

    x = x1 + dx * dist_from_first / d
    y = y1 + dy * dist_from_first / d

    print(f"{x:.15f} {y:.15f} {radius:.15f}")

if __name__ == "__main__":
    solve()
```

The first two lines of `solve` read the two circles exactly as given. All input values are integers, so `dx * dx + dy * dy` is also computed exactly before taking the square root.

The value `d` is the distance between the original centers. Because the circumferences have exactly two common points, the centers cannot coincide, so `d` is strictly positive. There is no need for an artificial epsilon check or a special case for coincident centers.

The expression `(r1 + r2 - d) / 2` is the final radius. The strict intersection condition guarantees that its numerator is positive.

The variable `dist_from_first` is the distance from the first center to the answer center. Multiplying the normalized vector `(dx / d, dy / d)` by this distance places the answer at the correct position along the line between the original centers.

No integer overflow is possible in Python, and even in fixed-width languages the squared coordinate differences here are tiny compared with 64-bit integer limits. The final calculations use floating point because the answer can be irrational.

## Worked Examples

### Sample 1

The input is

```
0 0 5
6 0 5
```

The important intermediate values are:

| Variable | Value |
| --- | --- |
| (dx) | (6) |
| (dy) | (0) |
| (d) | (6) |
| (R) | (2) |
| (t) | (3) |
| (x) | (3) |
| (y) | (0) |

Since the radii are equal, the crossing point of the two available-radius functions is the midpoint of the centers. The final circle is centered at ((3,0)) with radius (2), matching the sample output.

### Sample 2

The input is

```
-12 34 56
78 -90 123
```

The intermediate calculations are approximately:

| Variable | Value |
| --- | --- |
| (dx) | (90) |
| (dy) | (-124) |
| (d) | (153.21814\ldots) |
| (R) | (12.8906010988\ldots) |
| (t) | (43.1093989012\ldots) |
| (x) | (13.3222578219\ldots) |
| (y) | (-0.8884441101\ldots) |

Here the radii are different, so the answer center is not the midpoint. The new center is closer to the first circle because its radius is smaller. The computed values match the second sample within the required floating-point tolerance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | A constant number of arithmetic operations and one square root are performed |
| Space | (O(1)) | Only a fixed number of scalar variables are stored |

The input contains only two circles, so there is no dependence on an input size such as (N). The solution performs a few arithmetic operations and uses constant memory, leaving a very large margin under the 2 second and 256 MB limits.

## Test Cases

The assertions below compare floating-point values with a tolerance rather than comparing formatted strings. That reflects the actual judge condition, where many different decimal representations can be correct.

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
    d = (dx * dx + dy * dy) ** 0.5

    radius = (r1 + r2 - d) / 2.0
    t = (d + r1 - r2) / 2.0

    x = x1 + dx * t / d
    y = y1 + dy * t / d

    print(f"{x:.15f} {y:.15f} {radius:.15f}")

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

def check(inp: str, expected):
    out = run(inp).split()
    got = list(map(float, out))

    assert len(got) == 3
    for a, b in zip(got, expected):
        assert math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12), (
            f"got {got}, expected {expected}"
        )

# Provided samples
check(
    """0 0 5
6 0 5
""",
    (3.0, 0.0, 2.0),
)

check(
    """-12 34 56
78 -90 123
""",
    (13.322257821855908, -0.888444110112585, 12.890601098820779),
)

# Minimum radii, equal circles, simple horizontal placement
check(
    """0 0 1
1 0 1
""",
    (0.5, 0.0, 0.5),
)

# Equal circles with a non-horizontal center line
check(
    """0 0 5
3 4 5
""",
    (1.5, 2.0, 2.5),
)

# Unequal radii, catches the incorrect-midpoint solution
check(
    """0 0 5
6 0 9
""",
    (1.0, 0.0, 4.0),
)

# Maximum coordinate values while still having two intersections
check(
    """-1000 0 1000
999 0 1000
""",
    (-0.5, 0.0, 0.5),
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1` / `1 0 1` | `(0.5, 0, 0.5)` | Minimum radii and equal circles |
| `0 0 5` / `3 4 5` | `(1.5, 2, 2.5)` | Non-horizontal center line |
| `0 0 5` / `6 0 9` | `(1, 0, 4)` | Unequal radii and non-midpoint center |
| `-1000 0 1000` / `999 0 1000` | `(-0.5, 0, 0.5)` | Boundary coordinates and nearly tangent circles |

## Edge Cases

For the minimum-size case

```
0 0 1
1 0 1
```

we get (d=1). The radius is

[
R=\frac{1+1-1}{2}=0.5,
]

and the distance from the first center is also (0.5). The direction is ((1,0)), so the answer is exactly ((0.5,0,0.5)). The algorithm never needs a special branch for radius (1).

For the non-horizontal case

```
0 0 5
3 4 5
```

the center distance is (5). Equal radii give

[
R=\frac{5+5-5}{2}=2.5
]

and

[
t=\frac{5+5-5}{2}=2.5.
]

The unit direction from the first center to the second is ((3/5,4/5)), so the answer center is

[
(0,0)+2.5\left(\frac35,\frac45\right)=(1.5,2).
]

This catches implementations that incorrectly treat the geometry as one-dimensional along the (x)-axis.

For unequal radii,

```
0 0 5
6 0 9
```

we have (d=6). The radius is

[
R=\frac{5+9-6}{2}=4,
]

while

[
t=\frac{6+5-9}{2}=1.
]

Thus the center is ((1,0)). The two clearances are both (4):

[
5-1=4
]

and

[
9-(6-1)=4.
]

The equality of these two quantities is exactly the optimality condition.

For the near-tangent boundary case,

```
-1000 0 1000
999 0 1000
```

the centers are (1999) units apart. The final radius is

[
R=\frac{1000+1000-1999}{2}=0.5.
]

The answer center lies halfway between the two original centers, at

[
\frac{-1000+999}{2}=-0.5.
]

So the output is

```
-0.500000000000000 0.000000000000000 0.500000000000000
```

up to the permitted error. This case demonstrates why the implementation must not assume that the answer radius is comfortably separated from zero. The input guarantee gives a positive radius, but it can be arbitrarily small relative to the coordinate and radius magnitudes.
