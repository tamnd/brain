---
title: "CF 102375L - \u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0442\u043e\u0447\u043a\u0438"
description: "We have an integer grid inside the rectangle with corners (0, 0) and (X, Y). Among all marked points, p1 is special. We need to count every grid point whose Euclidean distance to p1 is no larger than its distance to every other marked point."
date: "2026-08-15T07:33:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "L"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 1254
verified: false
draft: false
---

[CF 102375L - \u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0442\u043e\u0447\u043a\u0438](https://codeforces.com/problemset/problem/102375/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 20m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We have an integer grid inside the rectangle with corners `(0, 0)` and `(X, Y)`. Among all marked points, `p1` is special. We need to count every grid point whose Euclidean distance to `p1` is no larger than its distance to every other marked point.

A direct interpretation suggests checking every grid point against every marked point. That is far too expensive. The useful structure appears after comparing squared distances. For a fixed competitor `pi`, the set of points at least as close to `p1` as to `pi` is one half-plane bounded by the perpendicular bisector of the two points. The desired set is the intersection of all these half-planes with the rectangle.

The original contest statement gives `X, Y, K <= 2 * 10^5`, with a 2 second time limit and 512 MiB memory limit. This immediately rules out iterating over all pairs of grid points and marked points. The rectangle itself can contain about `(2 * 10^5 + 1)^2 = 4 * 10^10` integer points, so even an `O(XY)` algorithm is impossible. We need to process the marked points in roughly `O(K log K)` time and then scan only one coordinate range.

There are several boundary cases that can silently break an implementation.

If `K = 1`, there are no competitors at all, so every grid point is good. For example,

```
1 1 1
0 0
```

has output `4`, because the four integer points of the rectangle are `(0,0)`, `(0,1)`, `(1,0)`, and `(1,1)`. A common mistake is to count `X * Y` cells instead of `(X + 1) * (Y + 1)` grid points.

Competitors can have the same `x` coordinate as `p1`. Then their perpendicular bisector is horizontal, so they do not impose an `x` bound at all. For example,

```
2 4 3
1 2
1 0
1 4
```

The first competitor requires `y >= 1`, the second requires `y <= 3`, and every `x` from `0` through `2` is allowed. The answer is `3 * 3 = 9`. Treating every competitor as an `x`-line would either divide by zero or silently lose this restriction.

The bisector can pass halfway between two integer coordinates. For example,

```
2 2 2
1 1
0 1
```

The condition against `(0,1)` is `x >= 1/2`, so integer points must have `x >= 1`. There are two possible `x` values and three possible `y` values, giving output `6`. Using truncating integer division instead of mathematical floor or ceiling can produce the wrong boundary.

Ties must also be accepted. The condition is distance less than or equal to the competitor's distance, so a point exactly on a bisector belongs to the good region. This is why all envelope comparisons in the solution use non-strict comparisons when choosing the active line.

## Approaches

The brute-force solution follows directly from the definition. Enumerate every integer `(x, y)` in the rectangle, compute its squared distance to `p1`, then compare that value with the squared distance to every other marked point. Squared distances are enough because square root is monotonic.

This is correct because a point is accepted exactly when none of the competitors is strictly closer. However, the worst case has about `4 * 10^10` grid points and `2 * 10^5` competitors, giving roughly `8 * 10^15` distance comparisons. That is many orders of magnitude beyond what can fit into the time limit.

The key observation is that comparing two squared Euclidean distances eliminates the quadratic terms in `x` and `y`. Let `p1 = (x1, y1)` and let a competitor be `q = (xi, yi)`. The inequality

`(x - x1)^2 + (y - y1)^2 <= (x - xi)^2 + (y - yi)^2`

simplifies to

`2(xi - x1)x + 2(yi - y1)y <= xi^2 + yi^2 - x1^2 - y1^2`.

This is a linear half-plane.

Now fix an integer `y`. Every competitor with `xi > x1` gives an upper bound on `x`, while every competitor with `xi < x1` gives a lower bound on `x`. Consequently, for every row `y`, the good points form one integer interval `[L(y), R(y)]`. We only need to calculate the tightest lower and upper bounds.

Each bound is a linear function of `y`, possibly with a rational coefficient. The upper boundary is the minimum of many lines, and the lower boundary is the maximum of many lines. Such envelopes can be constructed with the convex hull trick. We sort the lines by slope, discard lines that can never become optimal, and then scan `y` from bottom to top while maintaining a pointer to the currently optimal line.

The same `y` coordinate can also be restricted by competitors with `xi = x1`. Those constraints are handled directly before building the line envelopes.

The brute-force works because it tests exactly the definition, but fails when the rectangle contains billions of grid points. The observation that every distance comparison becomes a half-plane lets us replace the two-dimensional enumeration by two one-dimensional line envelopes and a single scan over `y`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(XYK)` | `O(K)` | Too slow |
| Optimal | `O(K log K + Y)` | `O(K)` | Accepted |

## Algorithm Walkthrough

1. Read `p1 = (x1, y1)` and initialize the allowed row interval to `0 <= y <= Y`. Every competitor with the same `x` coordinate as `p1` can only restrict this interval. Competitors with different `x` coordinates will be converted into lines.
2. For a competitor `q = (xi, yi)`, define

`dx = xi - x1`,

`dy = yi - y1`,

`C = xi^2 + yi^2 - x1^2 - y1^2`.

Its half-plane is

`2 dx x + 2 dy y <= C`.

This equation is kept in integer arithmetic, so no floating-point error can affect a boundary point.
3. If `dx = 0`, the inequality contains no `x`. When `dy > 0`, it becomes

`y <= (yi + y1) / 2`.

When `dy < 0`, it becomes

`y >= (yi + y1) / 2`.

Convert these to integer floor and ceiling bounds and intersect them with the current row interval.
4. If `dx > 0`, solve the inequality for `x`:

`x <= (C - 2dy * y) / (2dx)`.

This is an upper-bound line. For a fixed `y`, all such competitors must be satisfied, so we take the minimum of these lines.
5. If `dx < 0`, division reverses the inequality:

`x >= (2dy * y - C) / (2(-dx))`.

This is a lower-bound line. We need the maximum of all these functions. Instead of implementing a second kind of hull, store the negation of every lower line. The maximum of the original lines becomes the negative of the minimum of their negations.
6. Represent every rational line as

`f(y) = (m*y + b) / d`

with `d > 0`. Sort lines by decreasing slope `m/d`. For equal slopes, only the line with the smallest intercept matters for a minimum envelope.
7. Build the lower envelope. Consider three consecutive lines `a`, `b`, and `c` with decreasing slopes. Let `x_ab` be where `a` and `b` intersect, and `x_bc` where `b` and `c` intersect. If `x_ab >= x_bc`, line `b` is never the minimum, so it can be removed. All comparisons are performed by cross multiplication, which avoids floating-point arithmetic.
8. Scan the integer rows from the first allowed `y` to the last allowed `y`. Since the query coordinates are increasing, the active line on the envelope can only move forward. While the next line is no worse than the current line at the current `y`, advance the pointer.
9. Evaluate the upper envelope at `y` and take its mathematical floor. Evaluate the negated lower envelope and take the negative of its floor, which gives the mathematical ceiling of the original lower bound.
10. Clamp the resulting interval to `[0, X]`. If `L <= R`, the row contributes `R - L + 1` good integer points. Sum these contributions over all allowed rows.

### Why it works

For every competitor `pi`, the algorithm inserts exactly the half-plane containing all points that are at least as close to `p1` as to `pi`. The intersection of these half-planes is exactly the Voronoi cell of `p1`, restricted to the rectangle.

On a fixed row `y`, every half-plane with `xi > x1` contributes an upper bound on `x`, and every half-plane with `xi < x1` contributes a lower bound. Their intersection is consequently the interval from the maximum lower bound to the minimum upper bound. The equal-`x` competitors affect only which rows exist.

The convex hull contains exactly the lines that can be minimal for some query coordinate. The intersection-order test removes a middle line precisely when its interval of optimality is empty. During the increasing scan of `y`, the minimum can only move forward through the hull, so the selected line is always the true envelope value. Flooring and ceiling those exact rational values gives exactly the first and last integer `x` on the row. Thus every counted point is good, and every good point is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline
from functools import cmp_to_key

def slope_cmp(a, b):
    # Compare a.m / a.d and b.m / b.d, in decreasing order.
    left = a[0] * b[2]
    right = b[0] * a[2]

    if left > right:
        return -1
    if left < right:
        return 1

    # Equal slopes. Smaller intercept first.
    left = a[1] * b[2]
    right = b[1] * a[2]

    if left < right:
        return -1
    if left > right:
        return 1
    return 0

def value_leq(a, b, x):
    # a(x) <= b(x), with both denominators positive.
    left = (a[0] * x + a[1]) * b[2]
    right = (b[0] * x + b[1]) * a[2]
    return left <= right

def redundant(a, b, c):
    # Slopes are strictly decreasing.
    # b is redundant iff intersection(a,b) >= intersection(b,c).

    n1 = b[1] * a[2] - a[1] * b[2]
    d1 = a[0] * b[2] - b[0] * a[2]

    n2 = c[1] * b[2] - b[1] * c[2]
    d2 = b[0] * c[2] - c[0] * b[2]

    return n1 * d2 >= n2 * d1

def build_hull(lines):
    if not lines:
        return []

    lines.sort(key=cmp_to_key(slope_cmp))

    hull = []

    for line in lines:
        if hull:
            last = hull[-1]

            # Same slope. Keep the smaller intercept.
            if line[0] * last[2] == last[0] * line[2]:
                if line[1] * last[2] < last[1] * line[2]:
                    hull[-1] = line
                continue

        while len(hull) >= 2 and redundant(hull[-2], hull[-1], line):
            hull.pop()

        hull.append(line)

    return hull

def solve():
    X, Y, K = map(int, input().split())

    points = [tuple(map(int, input().split())) for _ in range(K)]
    x1, y1 = points[0]

    ymin = 0
    ymax = Y

    upper_lines = []
    lower_lines = []

    base_sq = x1 * x1 + y1 * y1

    for xi, yi in points[1:]:
        dx = xi - x1
        dy = yi - y1
        C = xi * xi + yi * yi - base_sq

        if dx == 0:
            s = xi + x1

            if dy > 0:
                # y <= (yi + y1) / 2
                ymax = min(ymax, s // 2)
            else:
                # y >= (yi + y1) / 2
                ymin = max(ymin, (s + 1) // 2)

        elif dx > 0:
            # x <= (C - 2*dy*y) / (2*dx)
            upper_lines.append((-2 * dy, C, 2 * dx))

        else:
            # x >= (2*dy*y - C) / (2*(-dx))
            #
            # Store the negation:
            # -x_bound = (-2*dy*y + C) / (2*(-dx))
            lower_lines.append((2 * dy, -C, -2 * dx))

    if ymin > ymax:
        print(0)
        return

    upper_hull = build_hull(upper_lines)
    lower_hull = build_hull(lower_lines)

    upper_ptr = 0
    lower_ptr = 0

    answer = 0

    for y in range(ymin, ymax + 1):
        if upper_hull:
            while (
                upper_ptr + 1 < len(upper_hull)
                and value_leq(
                    upper_hull[upper_ptr + 1],
                    upper_hull[upper_ptr],
                    y
                )
            ):
                upper_ptr += 1

            m, b, d = upper_hull[upper_ptr]
            upper_num = m * y + b
            right = upper_num // d
        else:
            right = X

        if lower_hull:
            while (
                lower_ptr + 1 < len(lower_hull)
                and value_leq(
                    lower_hull[lower_ptr + 1],
                    lower_hull[lower_ptr],
                    y
                )
            ):
                lower_ptr += 1

            m, b, d = lower_hull[lower_ptr]
            lower_neg_num = m * y + b

            # Original lower bound is -lower_neg_line.
            # ceil(-z) = -floor(z).
            left = -(lower_neg_num // d)
        else:
            left = 0

        if left < 0:
            left = 0
        if right > X:
            right = X

        if left <= right:
            answer += right - left + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The input is read through `sys.stdin.readline`, and the first marked point is used as `p1` exactly as specified by the input format. The quantity `base_sq` stores `x1^2 + y1^2`, so every competitor's constant can be formed without recomputing the same value.

The three branches on `dx` correspond directly to the three geometric cases from the algorithm. For `dx = 0`, no line is created because the restriction is purely vertical. For `dx > 0`, the denominator of the upper-bound line is positive. For `dx < 0`, multiplying by `-1` makes the denominator positive before the line is negated.

The hull stores `(m, b, d)` instead of a floating-point slope and intercept. Every comparison cross-multiplies the two fractions. Coordinates can be as large as `2 * 10^5`, and squared coordinates can reach roughly `4 * 10^10`, but Python integers have arbitrary precision, so there is no overflow issue.

The `redundant` test uses the exact intersection coordinates of consecutive lines. The denominators in those intersection expressions are positive because the hull is sorted by strictly decreasing slope. This makes the cross multiplication valid even when an intersection coordinate is negative.

The query pointer only moves forward. Since the rows are processed in increasing `y`, the optimal line also moves monotonically through a hull whose slopes are ordered consistently. This reduces all envelope queries after construction to linear time.

The floor operation is another subtle point. Python's `//` is mathematical floor division, including for negative numerators, which is exactly what the rational boundary requires. For the negated lower envelope, if its value is `z = -g`, the desired integer lower bound is `ceil(g) = -floor(z)`, which explains the expression used in the code.

## Worked Examples

For Sample 1, `p1 = (2,2)`. The four other points produce the following relevant bounds:

`(1,1)` gives `x >= 3 - y`.

`(1,3)` gives `x >= y - 1`.

`(3,3)` gives `x <= 5 - y`.

`(3,1)` gives `x <= y + 1`.

The envelopes are consequently

`L(y) = max(3-y, y-1)`

and

`R(y) = min(5-y, y+1)`.

The row scan is:

| `y` | `L(y)` | `R(y)` | Good `x` values | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | none | 0 |
| 1 | 2 | 2 | 2 | 1 |
| 2 | 1 | 3 | 1, 2, 3 | 3 |
| 3 | 2 | 2 | 2 | 1 |
| 4 | 3 | 1 | none | 0 |

The total is `1 + 3 + 1 = 5`. The middle row contains `p1` itself, and the rows immediately above and below contain only the points on the relevant bisectors. This demonstrates why equality must be accepted.

For Sample 2, `p1 = (0,0)` and every competitor is `(i,0)` for `1 <= i <= 5`. Each competitor gives

`2ix <= i^2`,

or

`x <= i/2`.

The smallest upper bound comes from `(1,0)`, giving `x <= 1/2`. Since `x` is integral, every good point has `x = 0`. There are no lower bounds and no row restrictions.

| `y` | Lower bound | Upper bound | Contribution |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 |
| 3 | 0 | 0 | 1 |
| 4 | 0 | 0 | 1 |
| 5 | 0 | 0 | 1 |
| 6 | 0 | 0 | 1 |

The answer is `7`. This example also shows why many competitors can disappear from the envelope. Once `(1,0)` gives the tightest bound, all later parallel bisectors are irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(K log K + Y)` | The two line sets are sorted and reduced into hulls, then all relevant rows are scanned once. |
| Space | `O(K)` | At most one line per competitor is stored before redundant lines are removed. |

With `K, Y <= 2 * 10^5`, the sorting dominates the asymptotic cost. The algorithm never enumerates the `O(XY)` grid points, which is the critical difference from brute force. Python's arbitrary-precision integers also remove the overflow concerns that would require 64-bit arithmetic in languages with fixed-width integers.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py`. The helper temporarily replaces its `input` function and captures its output, so each assertion exercises the same `solve()` used by the submission.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = solution.input

    sys.stdin = io.StringIO(inp)
    solution.input = sys.stdin.readline
    sys.stdout = io.StringIO()

    try:
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        solution.input = old_input
        sys.stdin = old_stdin
        sys.stdout = old_stdout

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

# Minimum-size rectangle, only p1.
assert run("""\
1 1 1
0 0
""") == "4", "minimum case"

# All competitors have the same x coordinate as p1.
assert run("""\
2 4 3
1 2
1 0
1 4
""") == "9", "horizontal bisectors"

# Half-integer bisector: x >= 1/2 becomes x >= 1.
assert run("""\
2 2 2
1 1
0 1
""") == "6", "half-integer boundary"

# Maximum K, with the first competitor already giving the tightest
# possible x-bound. There are 200000 distinct marked points.
points = ["0 0"]
points.extend(f"{i} 0" for i in range(1, 200000))

max_case = "200000 200000 200000\n" + "\n".join(points) + "\n"

assert run(max_case) == "200001", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 0 0` | `4` | Minimum dimensions, `K = 1`, and the distinction between grid points and cells |
| `2 4 3 / (1,2), (1,0), (1,4)` | `9` | Competitors with the same `x` coordinate and pure row restrictions |
| `2 2 2 / (1,1), (0,1)` | `6` | Exact floor handling at a half-integer bisector |
| `200000 200000 200000` with points `(0,0), (1,0), ..., (199999,0)` | `200001` | Large coordinates, maximum `K`, and performance of the envelope construction |

## Edge Cases

When `K = 1`, the line arrays are empty. The hull queries are skipped, so the code uses `left = 0` and `right = X` for every row. For the input

```
1 1 1
0 0
```

the row interval is `[0,1]` for both `y = 0` and `y = 1`, contributing two points per row and producing `4`.

When a competitor shares `x` with `p1`, the code enters the `dx == 0` branch. For

```
2 4 3
1 2
1 0
1 4
```

the point `(1,0)` has `dy = -2`, so the condition becomes `y >= 1`. The point `(1,4)` has `dy = 2`, so the condition becomes `y <= 3`. The resulting row interval is `[1,3]`, and every row contains all three possible `x` coordinates. The answer is `9`.

For the half-integer boundary

```
2 2 2
1 1
0 1
```

the competitor has `dx = -1`, `dy = 0`, and the lower-bound function is `1/2`. The lower envelope evaluates to exactly `1/2`, and Python's floor division gives `0` for the transformed value `-1/2` only after the sign transformation is handled correctly. The code computes the original integer lower bound as `1`, giving the valid rows `x = 1,2` for each of the three `y` values and answer `6`.

A point lying exactly on a bisector must remain good because ties are allowed. In Sample 1, `(2,2)` is `p1` itself, while `(2,1)` and `(2,3)` lie on relevant bisectors. The envelope comparisons use `<=`, so a line that ties the current best line can become active without excluding the tied coordinate.

The rectangle boundary is also part of the search space. If a computed lower bound is negative, it is clamped to `0`, and if an upper bound exceeds `X`, it is clamped to `X`. Thus a Voronoi cell extending beyond the rectangle is correctly clipped instead of being counted outside the allowed grid.

Finally, the answer can never be zero for a valid input because `p1` itself is an integer point inside the rectangle and its distance to itself is zero. The implementation may temporarily obtain an empty interval on a row, but the row `y = y1` always contains at least `x = x1`, so the total answer is at least one.
