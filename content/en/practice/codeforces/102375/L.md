---
title: "CF 102375L - \u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0442\u043e\u0447\u043a\u0438"
description: "We have a rectangle whose integer lattice points are all candidates. Among the marked points, the first point (p1) is special. We need to count every integer point ((x,y)) inside the rectangle for which (p1) is at least as close as every other marked point."
date: "2026-08-14T03:38:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "L"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 214
verified: false
draft: false
---

[CF 102375L - \u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0442\u043e\u0447\u043a\u0438](https://codeforces.com/problemset/problem/102375/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rectangle whose integer lattice points are all candidates. Among the marked points, the first point (p_1) is special. We need to count every integer point ((x,y)) inside the rectangle for which (p_1) is at least as close as every other marked point.

The square root in the Euclidean distance is unnecessary. Comparing squared distances gives, for another marked point (q=(u,v)) and (p_1=(a,b)),

[
(x-a)^2+(y-b)^2 \le (x-u)^2+(y-v)^2.
]

After expanding and cancelling (x^2) and (y^2), this becomes

[
2(u-a)x+2(v-b)y \le u^2+v^2-a^2-b^2.
]

So every other marked point contributes one linear inequality. The set of good points is exactly the intersection of these half-planes with the rectangle.

The dimensions and the number of marked points are all at most (2\cdot10^5). The rectangle itself can contain about (4\cdot10^{10}) integer points, so enumerating all candidate points is impossible. Checking every candidate against every marked point would require roughly

[
(2\cdot10^5)^2\cdot2\cdot10^5 \approx 8\cdot10^{15}
]

distance comparisons. We need something close to (O(K\log K+X)) or (O(K\log K+Y)).

There are several boundary cases that matter because the inequalities are non-strict. First, (p_1) itself is always good, so the answer can never be zero. For example,

```
1 1 1
0 0
```

has answer (4), because all four lattice points belong to the rectangle. A solution that considers only the interior of the rectangle would incorrectly return zero.

Equal distances must also be accepted. Consider

```
2 1 2
0 0
2 0
```

The perpendicular bisector is (x=1). Both (x=0) and (x=1) belong to (p_1)'s Voronoi cell, so the answer is (4). Replacing the required `<=` by `<` would incorrectly discard the two points with (x=1).

A bisector can be vertical, so dividing by the coefficient of (y) without handling the zero case is unsafe. For example,

```
3 3 2
1 0
1 1
```

gives the condition (y\le\frac12), so only (y=0) is allowed and the answer is (4). A sign error when dividing the inequality would reverse the allowed half-plane.

Finally, many marked points can have the same (y)-coordinate. This produces many vertical bisectors and is not a special geometric exception that can be ignored. Sample 2 is exactly such a case: all marked points lie on (y=0), and only the column (x=0) belongs to the cell of (p_1).

## Approaches

The direct approach is to iterate over every integer (x) and (y) in the rectangle and compare the squared distance to (p_1) with the squared distance to every other marked point. The method is correct because the definition of a good point is checked literally. Its problem is the size of the search space. In the worst case it performs about (8\cdot10^{15}) comparisons, far beyond what is possible.

The useful observation is that after expanding the squared distances, every condition is linear. We do not need to construct the whole two-dimensional Voronoi polygon. Instead, fix an integer (x). Every non-vertical boundary can be written as either

[
y\le f(x)
]

or

[
y\ge g(x),
]

where (f) and (g) are rational linear functions. Thus for a fixed column (x), all good integer (y) form one interval:

[
\left[\left\lceil\max g(x)\right\rceil,
\left\lfloor\min f(x)\right\rfloor\right].
]

The rectangle itself supplies (0\le y\le Y).

Now the problem has become a lower-envelope and upper-envelope problem for lines. We can construct the lower envelope with the Convex Hull Trick. The slopes are rational rather than necessarily integral, so every comparison is performed by cross multiplication. We also process integer (x)-coordinates from left to right, which lets us store the first integer coordinate where each line becomes optimal and answer all columns in linear time after building the hull.

A constraint with (v=b) does not give a line in (y). It gives a vertical restriction on (x), so these constraints can be processed separately and shrink the interval of columns we have to inspect.

The brute-force method works because it checks every half-plane at every lattice point. It fails because there are too many lattice points. The observation that each half-plane becomes a line bound on (y) for a fixed (x) lets us replace the two-dimensional enumeration with two one-dimensional envelopes and a sweep over at most (X+1) columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(XYK)) | (O(K)) | Too slow |
| Optimal | (O(K\log K+X)) | (O(K)) | Accepted |

## Algorithm Walkthrough

1. Read (p_1=(a,b)), initialize the allowed column interval as (L=0) and (R=X), and prepare two collections of lines. The first collection will represent upper bounds on (y), while the second will represent negated lower bounds.
2. For every other marked point (q=(u,v)), define

[
dx=u-a,\qquad dy=v-b,
]

and

[
C=u^2+v^2-a^2-b^2.
]

The corresponding condition is

[
2dx,x+2dy,y\le C.
]

This is obtained directly by cancelling the quadratic terms from the two squared distances.

1. If (dy=0), the inequality contains no (y). Since the two points are distinct, (dx\ne0), and the condition simplifies to

[
2dx,x\le dx(u+a).
]

For (dx>0), this gives

[
x\le\left\lfloor\frac{u+a}{2}\right\rfloor.
]

For (dx<0), it gives

[
x\ge\left\lceil\frac{u+a}{2}\right\rceil.
]

Update (L) or (R) accordingly.

1. If (dy>0), divide the inequality by the positive value (2dy). The result is

[
y\le\frac{-2dx,x+C}{2dy}.
]

Store this rational line in the upper-envelope collection.

1. If (dy<0), division reverses the inequality:

[
y\ge\frac{2dx,x-C}{-2dy}.
]

For convenience, negate this bound. Then

[
-y\le\frac{-2dx,x+C}{-2dy}.
]

So we store the line with numerator (-2dx,x+C) and positive denominator (-2dy) in the second collection. The minimum of these negated lines is exactly the negative of the maximum lower bound.

1. Add the rectangle constraints (y\le Y) and (y\ge0). The first is the constant upper line (Y). The second becomes the constant negated lower line (0). This means the envelopes automatically include the rectangle's horizontal sides.
2. If (L>R), no integer column can satisfy all vertical restrictions, so the answer is zero. In fact this cannot happen for a valid geometric Voronoi cell containing (p_1), but handling it makes the implementation complete.
3. Sort each collection by decreasing rational slope. Two slopes (a_1/d_1) and (a_2/d_2) are compared by cross multiplication, so no floating point arithmetic is used. For equal slopes, keep only the line with the smaller value.
4. Build the lower envelope. Suppose the previous hull line is (f) and the new line is (g), with (g) having the smaller slope. The new line eventually becomes better as (x) increases. Its first integer winning coordinate is the ceiling of their intersection.

For lines

[
f(x)=\frac{a_f x+b_f}{d_f},
\qquad
g(x)=\frac{a_g x+b_g}{d_g},
]

the intersection satisfies

[
(a_gd_f-a_fd_g)x=b_fd_g-b_gd_f.
]

Because the slopes are sorted decreasingly, the coefficient on the left is negative. We compute the exact ceiling with integer arithmetic. If the new line starts no later than the previous line started, the previous line is redundant and is removed.

1. Store, together with every hull line, the first integer (x) where it is optimal. Since these starting coordinates are increasing, a single pointer can answer all queries for (x=L,L+1,\ldots,R). When the next line's starting coordinate is reached, advance the pointer.
2. For every integer column (x), query the upper hull and obtain a rational upper bound (U(x)). Its largest valid integer (y) is

[
\left\lfloor U(x)\right\rfloor.
]

Query the second hull and obtain the minimum value of (-g(x)). If this value is (Q(x)), then the largest original lower bound is (-Q(x)), and the smallest valid integer (y) is

[
\left\lceil-Q(x)\right\rceil=-\left\lfloor Q(x)\right\rfloor.
]

1. The number of good points in this column is the upper integer bound minus the lower integer bound plus one, provided the interval is non-empty. Add that number to the answer.

### Why it works

For every other marked point, the condition that (p_1) is no farther away is exactly one linear half-plane. At a fixed (x), a non-vertical half-plane gives one upper or lower bound on (y). Their intersection is consequently an integer interval, whose endpoints are determined by the minimum upper line and maximum lower line.

The Convex Hull Trick keeps exactly those lines that can attain the required minimum. The stored starting coordinate is the first integer column where a hull line is no worse than its predecessor, so the hull pointer always identifies an optimal line for the current (x). Exact cross multiplication and exact floor or ceiling division preserve the non-strict inequalities, including points lying exactly on bisectors.

Thus every integer point counted by the sweep satisfies every original distance inequality, and every integer point satisfying all those inequalities appears in exactly one swept column and is counted.

## Python Solution

```python
import sys
from functools import cmp_to_key

input = sys.stdin.readline

def ceil_div(a, b):
    return -((-a) // b)

def slope_cmp(p, q):
    # Lines are sorted by decreasing slope p[0] / p[2].
    left = p[0] * q[2]
    right = q[0] * p[2]

    if left != right:
        return -1 if left > right else 1

    # For equal slopes, smaller intercept first.
    left = p[1] * q[2]
    right = q[1] * p[2]

    if left != right:
        return -1 if left < right else 1

    return 0

def build_hull(lines, left, right):
    lines.sort(key=cmp_to_key(slope_cmp))

    # Remove equal slopes. Because of the comparator, the first
    # line among equal slopes has the smallest intercept.
    unique = []
    for line in lines:
        if unique:
            p = unique[-1]
            if line[0] * p[2] == p[0] * line[2]:
                continue
        unique.append(line)

    hull = []
    start = []

    for line in unique:
        if not hull:
            hull.append(line)
            start.append(left)
            continue

        while hull:
            old = hull[-1]

            # Intersection coordinate of old and line:
            #
            # (line.a / line.d) * x + line.b / line.d
            # =
            # (old.a / old.d) * x + old.b / old.d
            #
            # The denominator below is negative because slopes are
            # strictly decreasing.
            numerator = old[1] * line[2] - line[1] * old[2]
            denominator = line[0] * old[2] - old[0] * line[2]
            first_integer = ceil_div(numerator, denominator)

            if first_integer <= start[-1]:
                hull.pop()
                start.pop()
            else:
                break

        if not hull:
            hull.append(line)
            start.append(left)
        else:
            if first_integer > right:
                break
            hull.append(line)
            start.append(first_integer)

    return hull, start

def query_hull(hull, start, x, ptr):
    while ptr + 1 < len(hull) and start[ptr + 1] <= x:
        ptr += 1

    line = hull[ptr]
    numerator = line[0] * x + line[1]
    denominator = line[2]

    return numerator, denominator, ptr

def solve():
    X, Y, K = map(int, input().split())
    points = [tuple(map(int, input().split())) for _ in range(K)]

    a, b = points[0]

    left = 0
    right = X

    # Upper lines have the form
    #     y <= (A*x+B)/D
    #
    # Lower lines are stored after negating the lower bound, so they
    # also have the form
    #     -y <= (A*x+B)/D.
    upper = [(0, Y, 1)]
    lower = [(0, 0, 1)]

    aa = a * a + b * b

    for u, v in points[1:]:
        dx = u - a
        dy = v - b
        c = u * u + v * v - aa

        if dy == 0:
            # 2*dx*x <= dx*(u+a)
            if dx > 0:
                right = min(right, (u + a) // 2)
            else:
                left = max(left, ceil_div(u + a, 2))
            continue

        if dy > 0:
            # y <= (-2*dx*x + c) / (2*dy)
            upper.append((-2 * dx, c, 2 * dy))
        else:
            # y >= (2*dx*x - c) / (-2*dy)
            #
            # Equivalently:
            # -y <= (-2*dx*x + c) / (-2*dy)
            lower.append((-2 * dx, c, -2 * dy))

    if left > right:
        print(0)
        return

    upper_hull, upper_start = build_hull(upper, left, right)
    lower_hull, lower_start = build_hull(lower, left, right)

    up_ptr = 0
    low_ptr = 0
    answer = 0

    for x in range(left, right + 1):
        un, ud, up_ptr = query_hull(
            upper_hull, upper_start, x, up_ptr
        )
        upper_y = un // ud

        ln, ld, low_ptr = query_hull(
            lower_hull, lower_start, x, low_ptr
        )

        # ln / ld is the minimum value of -lower_bound(x).
        # Hence lower_bound(x) = -ln / ld, and
        # ceil(lower_bound(x)) = -(ln // ld).
        lower_y = -(ln // ld)

        lower_y = max(lower_y, 0)
        upper_y = min(upper_y, Y)

        if lower_y <= upper_y:
            answer += upper_y - lower_y + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation converts every distance comparison into a line. The constant `aa` stores (a^2+b^2), so the right side of every inequality can be formed without recomputing it.

The `dy == 0` branch is separate because the corresponding bisector is vertical. Dividing by `dy` in that case would be invalid. The formulas use integer floor and ceiling operations so that the boundary point is retained when equality holds.

The `build_hull` function first orders lines by decreasing rational slope. Cross multiplication is used for every comparison, which avoids floating-point errors near almost coincident slopes. Equal slopes need special treatment because only the line with the smaller intercept can ever be part of a minimum envelope.

The intersection calculation also stays entirely in integer arithmetic. The denominator is negative because the new line has a smaller slope than the previous one. `ceil_div` works with negative denominators as well, which matters because intersection coordinates can be negative even though our actual queries are inside the rectangle.

The hull stores `start[i]`, the first integer (x) at which line `i` becomes optimal. Since these values are increasing, the sweep does not need binary search. The pointer only moves forward, so all (X+1) column queries together take (O(X)).

The lower hull stores the negative of every lower bound. This turns the required maximum into another minimum problem, allowing the same hull implementation to be reused. The expression `-(ln // ld)` is the exact ceiling of the original lower bound and correctly handles negative rational values.

Python integers have arbitrary precision, so all cross products are exact. With the given coordinate bounds, the products are already within the range that a 64-bit signed integer can almost cover, but using Python integers removes any overflow concern.

## Worked Examples

### Sample 1

The first point is (p_1=(2,2)). The four other points produce the following bounds:

[
y\ge3-x,\qquad y\le x+1,\qquad
y\le5-x,\qquad y\ge x-1.
]

The rectangle contributes (0\le y\le4).

| (x) | Lower bound | Upper bound | Good integer (y) | Added |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | none | 0 |
| 1 | 2 | 2 | 2 | 1 |
| 2 | 1 | 3 | 1, 2, 3 | 3 |
| 3 | 2 | 2 | 2 | 1 |
| 4 | 3 | 1 | none | 0 |

The sweep counts (1+3+1=5) points, giving the required output `5`. The trace shows the central Voronoi cell as a discrete diamond. The equality cases on its boundary are included.

### Sample 2

Here (p_1=(0,0)), while every other point is on the same horizontal line (y=0). The first competitor ((1,0)) already gives

[
x\le0
]

for (p_1)'s cell. The remaining points only strengthen this restriction. Thus the valid column interval becomes (L=0,R=0).

| (x) | Vertical interval after processing sites | Lower (y) | Upper (y) | Added |
| --- | --- | --- | --- | --- |
| 0 | only valid column | 0 | 6 | 7 |

Every (y) from (0) through (6) is good at (x=0), so the answer is (7). This demonstrates why vertical bisectors must be handled independently from the line envelopes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(K\log K+X)) | Each of the two line sets is sorted once, hull construction is linear after sorting, and the column sweep is (O(X)). |
| Space | (O(K)) | The two line collections and their hulls contain (O(K)) lines. |

With (K,X\le2\cdot10^5), the sorting dominates the running time and the final sweep examines only (2\cdot10^5+1) possible columns. The algorithm never enumerates the potentially (4\cdot10^{10}) lattice points of the rectangle, so it fits the stated limits.

## Test Cases

The following harness is intended to be appended to the solution above. It temporarily replaces standard input and output and calls the same `solve()` function.

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    sys.stdout = io.StringIO()

    try:
        solve()
        result = sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

    return result

# Provided sample 1
assert run("""\
4 4 5
2 2
1 1
1 3
3 3
3 1
""") == "5", "sample 1"

# Provided sample 2
assert run("""\
6 6 6
0 0
1 0
2 0
3 0
4 0
5 0
""") == "7", "sample 2"

# Minimum-size case. With only p1, every lattice point is good.
assert run("""\
1 1 1
0 0
""") == "4", "minimum size"

# Equality on a perpendicular bisector must be accepted.
assert run("""\
2 1 2
0 0
2 0
""") == "4", "tie boundary"

# All marked points have the same x-coordinate, producing a horizontal
# bisector. Only y=0 is good.
assert run("""\
3 3 2
1 0
1 1
""") == "4", "horizontal bisector"

# All marked points have the same y-coordinate. The first point is
# in the middle, so its Voronoi cell is x in [1, 3], with all three
# possible y values.
assert run("""\
4 2 3
2 1
0 1
4 1
""") == "9", "same y coordinates"

# Maximum-size stress case.
# X = Y = K = 200000.
# All sites lie on y=0 and p1=(0,0), so only x=0 is good,
# while every y from 0 to 200000 is allowed.
points = "\n".join(f"{i} 0" for i in range(200000))
max_case = f"200000 200000 200000\n{points}\n"
assert run(max_case) == "200001", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 0 0` | 4 | Minimum dimensions, (K=1), rectangle boundaries |
| `2 1 2 / 0 0 / 2 0` | 4 | Non-strict equality on a bisector |
| `3 3 2 / 1 0 / 1 1` | 4 | Horizontal bisector and inequality direction |
| `4 2 3 / 2 1 / 0 1 / 4 1` | 9 | Multiple vertical bisectors and equal coordinates |
| (200000\times200000), (200000) points on (y=0) | 200001 | Maximum input sizes and large integer arithmetic |

## Edge Cases

The case with only (p_1) is handled by the initial constant lines. For

```
1 1 1
0 0
```

the upper hull contains (y\le1), the lower hull contains (y\ge0), and the sweep visits (x=0) and (x=1). Each column contributes two points, giving (4). The implementation never relies on the existence of a competitor.

The equality case

```
2 1 2
0 0
2 0
```

produces the vertical condition (x\le1). The sweep therefore examines (x=0) and (x=1). At both columns the vertical restriction is satisfied, and the horizontal bounds give (y=0,1). The result is (4). The use of `<=` in the original inequality is preserved by the integer floor and ceiling calculations.

For a horizontal bisector,

```
3 3 2
1 0
1 1
```

the comparison is

[
y^2+x'^2\le y-1)^2+x'^2,
]

which simplifies to (y\le\frac12). Integer (y) can only be (0). Since (x) has four possible values, the answer is (4). In the implementation, this competitor becomes the upper line (y\le\frac12), and the hull returns `1 // 2 = 0` for every column.

When all marked points have the same (y)-coordinate,

```
4 2 3
2 1
0 1
4 1
```

the first point is equidistant from the two outer sites at (x=1) and (x=3). Its cell is

[
1\le x\le3,
]

and every (y\in{0,1,2}) has the same horizontal displacement comparison. The sweep counts three columns with three points each, giving (9).

The maximum-size case uses

```
200000 200000 200000
0 0
1 0
2 0
...
199999 0
```

The first competitor already forces (x\le0), so only (x=0) survives. Every (y) from (0) through (200000) is equally good because all marked points have (y=0). The answer is (200001). This test exercises the largest allowed (X), (Y), and (K) simultaneously while also checking that the algorithm does not accidentally scale with the number of lattice points.
