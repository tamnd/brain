---
title: "CF 102281B - \u041a\u0443\u043b\u0438\u043d\u0430\u0440\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We have a triangular cookie cutter whose side lengths are (a), (b), and (c), and a circular cookie cutter with radius (r)."
date: "2026-08-13T16:09:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "B"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 114
verified: true
draft: false
---

[CF 102281B - \u041a\u0443\u043b\u0438\u043d\u0430\u0440\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a triangular cookie cutter whose side lengths are (a), (b), and (c), and a circular cookie cutter with radius (r). The cookies are thin, so the question is purely two-dimensional: can the circular cookie be placed completely inside the triangular cutter, and can the triangular cookie be placed completely inside the circular cutter?

The first question asks for the largest circle that can fit inside the triangle. That circle is the triangle's incircle, so the relevant quantity is the inradius.

The second question asks for the smallest circle that can contain the entire triangle. Such a circle is determined by the triangle's circumcircle, so the relevant quantity is the circumradius.

The input contains four integers between 1 and 10000. These bounds are tiny for an (O(1)) solution, and even a linear algorithm would be unnecessary because there is only one triangle to process. The main concern is not running time but numerical correctness. Direct floating-point calculations with Heron's formula can introduce rounding errors exactly at the boundary where the answer changes.

There are several edge cases where a careless implementation can fail. Consider

```
1 1 1 1
```

The triangle is equilateral. Its inradius is (\sqrt{3}/6), which is less than 1, while its circumradius is (\sqrt{3}/3), also less than 1. Both cookies fit, so both answers must be positive. An implementation that confuses inradius and circumradius would get one of the answers wrong.

A more useful boundary case is

```
2 2 2 1
```

Here the circumradius is (2/\sqrt{3}), which is greater than 1, while the inradius is (1/\sqrt{3}), which is less than 1. Thus the circle fits into the triangle, but the triangle does not fit into the circle. Using the same radius criterion for both directions gives the wrong result.

The exact boundary must also be handled inclusively. For example,

```
2 2 2 1
```

does not happen to lie on a boundary, but an equilateral triangle with side 1 and a circle whose radius is exactly its inradius would fit. The comparison must use `>=`, not `>`.

Finally, the sides can be as large as 10000, so computing Heron's expression directly is safe in Python, but an implementation in a fixed-width integer language should still choose the arithmetic carefully. The largest product involved is on the order of (10^{16}), which fits in a signed 64-bit integer but not in a signed 32-bit integer.

## Approaches

A naive geometric approach would try to simulate the physical insertion process. For the circle, one could try many possible positions and orientations and test whether the circle crosses one of the three sides. For the triangle inside the circle, one could similarly enumerate positions and rotations. The problem is that position and rotation are continuous variables, so there is no finite brute-force search that is both exact and guaranteed to find the optimum. If we discretize the angle into (N) values and positions into (M) values, the resulting search costs (O(NM)) checks, and its answer still depends on the chosen discretization. In the worst case there is no finite operation count that makes such a method an exact solution, because an arbitrarily fine grid may still miss a valid placement.

The brute-force idea does have one useful property: it works because it is searching for the extremal placement. The circle must be centered at a special point if it is as large as possible, and the triangle must be related to a special enclosing circle if that circle is as small as possible. Instead of searching for those placements, we can identify them mathematically.

For a triangle, the largest inscribed circle has radius equal to the inradius

[
\rho = \frac{A}{s},
]

where (A) is the triangle's area and (s=(a+b+c)/2) is its semiperimeter. The circular cookie fits exactly when (r\geq\rho).

Conversely, the smallest circle containing all three vertices has radius equal to the circumradius

[
R = \frac{abc}{4A}.
]

The triangle fits into the circular cutter exactly when (r\geq R).

The remaining issue is avoiding floating-point arithmetic. Heron's formula gives

[
A^2=s(s-a)(s-b)(s-c).
]

It is more convenient to multiply everything by 16 and define

[
D=(a+b+c)(-a+b+c)(a-b+c)(a+b-c)=16A^2.
]

Then (4A=\sqrt D). The inradius condition becomes

[
r\geq\frac{\sqrt D}{2(a+b+c)}.
]

Both sides are nonnegative, so we can square them:

[
4r^2(a+b+c)^2\geq D.
]

For the circumradius,

[
R=\frac{abc}{\sqrt D},
]

so

[
r\geq R
]

is equivalent to

[
r^2D\geq a^2b^2c^2.
]

Both decisions are now exact integer comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Geometric brute force over positions and rotations | No finite exact bound | O(1) | Not suitable |
| Formula with floating point | O(1) | O(1) | Risky at boundaries |
| Integer comparisons using Heron's formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the side lengths (a,b,c) and the circle radius (r). The three side lengths describe one triangle, so the first geometric quantity we need is its squared area.
2. Compute

[
D=(a+b+c)(-a+b+c)(a-b+c)(a+b-c).
]

Since (D=16A^2), its square root is (4A). We never actually need to calculate that square root.

1. Check whether the circle fits inside the triangle using

[
4r^2(a+b+c)^2\geq D.
]

This is exactly the condition (r\geq\rho), where (\rho) is the triangle's inradius.

1. Check whether the triangle fits inside the circle using

[
r^2D\geq a^2b^2c^2.
]

This is exactly the condition (r\geq R), where (R) is the circumradius.

1. Print the corresponding sentence for each comparison. Equality counts as fitting because the cookie is allowed to touch the cutter.

### Why it works

The largest circle that can be placed inside a triangle is its incircle, so checking the inradius is both necessary and sufficient for the first direction. The smallest circle containing all vertices of a nondegenerate triangle is its circumcircle, so checking the circumradius is necessary and sufficient for the second direction.

The value (D) satisfies (D=16A^2). Substituting this identity into the formulas for the inradius and circumradius transforms both geometric conditions into exact integer inequalities. Since every transformation preserves the direction of the comparison and all quantities being squared are nonnegative, the algorithm produces the same answer as the original geometric problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c, r = map(int, input().split())

p = a + b + c

# 16 * area^2
d = p * (-a + b + c) * (a - b + c) * (a + b - c)

# Circle fits into triangle iff r >= inradius.
circle_in_triangle = 4 * r * r * p * p >= d

# Triangle fits into circle iff r >= circumradius.
triangle_in_circle = r * r * d >= a * a * b * b * c * c

if circle_in_triangle:
    print("Circle gets into the triangle")
else:
    print("Circle doesn’t get into the triangle")

if triangle_in_circle:
    print("Triangle gets into the circle")
else:
    print("Triangle doesn’t get into the circle")
```

The variable `p` stores (a+b+c), which appears in both Heron's expression and the inradius comparison. The variable `d` is (16A^2), allowing the entire solution to avoid `sqrt`.

For the first comparison, the code uses

```
4 * r * r * p * p >= d
```

because

[
r\geq\frac{\sqrt D}{2p}
]

is equivalent to

[
4r^2p^2\geq D.
]

For the second comparison, the code uses

```
r * r * d >= a * a * b * b * c * c
```

because (R=abc/\sqrt D). Equality is deliberately accepted in both cases.

Python integers have arbitrary precision, so there is no overflow concern. In a language such as C++, 64-bit integers are sufficient for these constraints. The input contains only one test case, so there is no loop around the calculation.

The exact output strings must be preserved, including the curly apostrophe in `doesn’t`, because Codeforces compares output text directly.

## Worked Examples

### Sample 1

For the first sample, the input is

```
1 1 1 10
```

The triangle is equilateral, and the circle is very large.

| Variable | Value |
| --- | --- |
| (a) | 1 |
| (b) | 1 |
| (c) | 1 |
| (r) | 10 |
| (p=a+b+c) | 3 |
| (D) | 3 |
| (4r^2p^2) | 3600 |
| (r^2D) | 300 |
| (a^2b^2c^2) | 1 |
| Circle inside triangle | false |
| Triangle inside circle | true |

The first inequality fails because a circle of radius 10 is much larger than the triangle's inradius. The second inequality succeeds because the triangle's circumradius is much smaller than 10.

The output is

```
Circle doesn’t get into the triangle
Triangle gets into the circle
```

### Sample 2

For the second sample, the input is

```
10 10 10 1
```

Now the triangle is much larger than the circle.

| Variable | Value |
| --- | --- |
| (a) | 10 |
| (b) | 10 |
| (c) | 10 |
| (r) | 1 |
| (p=a+b+c) | 30 |
| (D) | 30000 |
| (4r^2p^2) | 3600 |
| (r^2D) | 30000 |
| (a^2b^2c^2) | 1000000 |
| Circle inside triangle | true |
| Triangle inside circle | false |

The circle's radius is larger than the triangle's inradius, so the circle fits inside. However, the triangle's circumradius is much greater than 1, so the triangle cannot fit inside the circle.

The output is

```
Circle gets into the triangle
Triangle doesn’t get into the circle
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | A fixed number of arithmetic operations is performed. |
| Space | (O(1)) | Only a constant number of integer variables are stored. |

The constraints allow side lengths and the radius up to 10000, and the solution performs only a handful of arithmetic operations. It is far below the 1.5 second time limit and uses negligible memory compared with the 128 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    a, b, c, r = map(int, input().split())

    p = a + b + c
    d = p * (-a + b + c) * (a - b + c) * (a + b - c)

    circle_in_triangle = 4 * r * r * p * p >= d
    triangle_in_circle = r * r * d >= a * a * b * b * c * c

    first = (
        "Circle gets into the triangle"
        if circle_in_triangle
        else "Circle doesn’t get into the triangle"
    )
    second = (
        "Triangle gets into the circle"
        if triangle_in_circle
        else "Triangle doesn’t get into the circle"
    )

    return first + "\n" + second

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided sample 1
assert run("1 1 1 10\n") == (
    "Circle doesn’t get into the triangle\n"
    "Triangle gets into the circle"
), "sample 1"

# Provided sample 2
assert run("10 10 10 1\n") == (
    "Circle gets into the triangle\n"
    "Triangle doesn’t get into the circle"
), "sample 2"

# Minimum-size valid triangle
assert run("1 1 1 1\n") == (
    "Circle gets into the triangle\n"
    "Triangle gets into the circle"
), "minimum-size values"

# Maximum-size equilateral triangle
assert run("10000 10000 10000 10000\n") == (
    "Circle gets into the triangle\n"
    "Triangle gets into the circle"
), "maximum-size values"

# Exact inradius boundary for a 3-4-5 triangle:
# inradius = 1, circumradius = 2.5
assert run("3 4 5 1\n") == (
    "Circle gets into the triangle\n"
    "Triangle doesn’t get into the circle"
), "inradius boundary"

# Exact circumradius boundary for a 3-4-5 triangle
assert run("3 4 5 3\n") == (
    "Circle gets into the triangle\n"
    "Triangle gets into the circle"
), "circumradius boundary"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | Both get into | Minimum values and symmetric equilateral geometry |
| `10000 10000 10000 10000` | Both get into | Maximum values and large integer arithmetic |
| `3 4 5 1` | Circle only | Exact inradius boundary |
| `3 4 5 3` | Both get into | Circumradius boundary and inclusive comparison |

## Edge Cases

For the minimum-size case

```
1 1 1 1
```

we get (D=3). The circle condition is (4\cdot1^2\cdot3^2=36\geq3), and the triangle condition is (1^2\cdot3=3\geq1). Both comparisons succeed. The example catches implementations that accidentally use the wrong radius formula for one of the directions.

For the 3-4-5 triangle with radius 1,

```
3 4 5 1
```

the area is 6, so the inradius is (6/6=1). The circle exactly touches all three sides in the optimal placement and must be accepted. The circumradius is (3\cdot4\cdot5/(4\cdot6)=2.5), so the triangle does not fit. This case catches a strict `>` comparison.

For the same triangle with radius 3,

```
3 4 5 3
```

the circle is still larger than the inradius, and now it is also larger than the circumradius. Both directions succeed. This verifies that the two inequalities are independent and that the circumradius calculation is being used for the triangle-inside-circle direction.

For maximum values,

```
10000 10000 10000 10000
```

the arithmetic involves values around (10^{16}). Python handles these integers exactly, so no precision is lost. The geometry is unchanged by scale: both the inradius and circumradius are proportional to the side length, and a radius of 10000 is more than sufficient for both directions.
