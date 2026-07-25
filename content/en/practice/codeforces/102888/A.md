---
title: "CF 102888A - \u4e09\u89d2\u5f62\u5207\u534a"
description: "The triangle is always a right triangle with its right angle at $(x0, y0)$. Its other two vertices are $(x0 + a, y0)$ and $(x0, y0 + b)$."
date: "2026-07-25T12:24:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102888
codeforces_index: "A"
codeforces_contest_name: "The 15-th Beihang University Collegiate Programming Contest (BCPC 2020) - Preliminary"
rating: 0
weight: 102888
solve_time_s: 56
verified: true
draft: false
---

[CF 102888A - \u4e09\u89d2\u5f62\u5207\u534a](https://codeforces.com/problemset/problem/102888/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The triangle is always a right triangle with its right angle at $(x_0, y_0)$. Its other two vertices are $(x_0 + a, y_0)$ and $(x_0, y_0 + b)$. We must choose a vertical line $x = c$, where $x_0 \le c \le x_0 + a$, so that the part of the triangle on the left of the line and the part on the right have exactly the same area.

The input gives the position of the triangle and its dimensions. The output is a single floating point value $c$. Any answer within the required floating point tolerance is accepted.

The bounds are extremely small. Every coordinate is at most 1000 in magnitude and both side lengths are at most 1000. Since there is only one triangle, even an iterative numerical method would comfortably fit within the limits. Even so, the geometry has a closed-form solution, so the problem can be solved in constant time without any iteration.

The main difficulty is that the area on the left does not grow linearly with the cutting position. Assuming that the halfway point along the base also halves the area is incorrect.

Consider the input

```
0 0 1 1
```

The correct answer is approximately

```
0.292893218...
```

Cutting at $x = 0.5$ leaves a larger area on the left because the triangle becomes shorter as we move to the right.

Another easy mistake is forgetting that the triangle may not start at the origin.

For example,

```
100 200 4 5
```

The answer is not computed directly from the interval $[0,4]$. After solving in local coordinates, the result must be shifted back by adding $x_0$.

A third common error is using integer arithmetic.

For example,

```
0 0 3 2
```

The answer is irrational. Integer division or premature truncation produces a visibly incorrect cut position.

## Approaches

A direct numerical approach is to binary search the cutting position. For any candidate $c$, we compute the area on the left, compare it with half of the total area, and adjust the search interval. Since the left area increases continuously as the cut moves right, binary search is correct. Around sixty iterations already give far more precision than required, so this approach runs in constant time.

The interesting part is deriving the area formula. Let

$$t = c - x_0,$$

so that $t$ measures the horizontal distance from the left side of the triangle.

The hypotenuse joins $(0,b)$ and $(a,0)$ in local coordinates, so its equation is

$$y = b\left(1-\frac{x}{a}\right).$$

The portion of the triangle left of $x=t$ is a trapezoid whose parallel sides have heights

$$b,\qquad b\left(1-\frac{t}{a}\right).$$

Its area is

$$S_{\text{left}}
=
\frac{
b+b\left(1-\frac{t}{a}\right)
}{2}
\cdot t
=
bt-\frac{bt^2}{2a}.$$

The total triangle area is

$$\frac{ab}{2},$$

so setting the left area equal to half the total area gives

$$bt-\frac{bt^2}{2a}
=
\frac{ab}{4}.$$

Dividing by $b$ and rearranging,

$$2t-\frac{t^2}{a}
=
\frac{a}{2},$$

or

$$t^2-2at+\frac{a^2}{2}=0.$$

The valid root inside the interval $[0,a]$ is

$$t=a\left(1-\frac{1}{\sqrt2}\right).$$

Finally,

$$c=x_0+t.$$

This produces the answer immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (binary search on the answer) | O(log Precision) | O(1) | Accepted |
| Optimal (closed-form geometry) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $x_0$, $y_0$, $a$, and $b$. Only $x_0$ and $a$ influence the answer because every vertical cross section scales proportionally with $b$.
2. Compute the horizontal offset

$$t=a\left(1-\frac{1}{\sqrt2}\right).$$

This is obtained by solving the quadratic equation that makes the left area exactly half of the total area.
3. Compute

$$c=x_0+t.$$

This converts the local coordinate back into the original coordinate system.
4. Print the result as a floating point number.

### Why it works

The height of the triangle decreases linearly from left to right, so the accumulated area is the integral of a linear function, which is a quadratic expression. Solving that quadratic for exactly half of the total area gives a unique solution inside the interval $[0,a]$. Since every derivation is exact, the computed value always divides the triangle into two equal-area regions.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

x0, y0, a, b = map(int, input().split())

c = x0 + a * (1.0 - 1.0 / math.sqrt(2.0))

print(c)
```

The program first reads the four integers. Although the input includes both coordinates and both side lengths, only the horizontal position and horizontal length appear in the final formula.

The computation uses the closed-form expression derived from the area equation. Using `math.sqrt` keeps the calculation in floating point, which easily satisfies the required error tolerance.

Finally, the program prints the answer directly. No special formatting is needed because Python's default floating point output already provides sufficient precision.

## Worked Examples

### Sample 1

Input

```
0 0 1 1
```

| Step | Variable | Value |
| --- | --- | --- |
| Read input | $x_0$ | 0 |
| Read input | $a$ | 1 |
| Compute offset | $t$ | $1-\frac1{\sqrt2}\approx0.2928932188$ |
| Compute answer | $c$ | 0.2928932188 |

The cut lies noticeably closer to the left edge than the midpoint. This confirms that equal width does not imply equal area because the triangle becomes shorter toward the right.

### Sample 2

Input

```
347 -685 868 194
```

| Step | Variable | Value |
| --- | --- | --- |
| Read input | $x_0$ | 347 |
| Read input | $a$ | 868 |
| Compute offset | $t$ | 254.23131393 |
| Compute answer | $c$ | 601.23131393 |

This example demonstrates that the vertical side length and vertical position have no effect on the answer. Only the base length and horizontal translation matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed. |
| Space | O(1) | No additional data structures are allocated. |

The algorithm performs a constant amount of work regardless of the input values. It easily fits within any reasonable time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import math
import sys

def solve():
    input = sys.stdin.readline
    x0, y0, a, b = map(int, input().split())
    print(x0 + a * (1 - 1 / math.sqrt(2)))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue().strip()

def check(inp, expected):
    ans = float(run(inp))
    assert abs(ans - expected) <= 1e-6

# provided samples
check("0 0 1 1\n", 0.2928932188134524)
check("347 -685 868 194\n", 601.2313139300767)
check("-110 -319 376 122\n", 0.12785027385811532)

# custom cases
check("0 0 1000 1000\n", 292.89321881345245)
check("100 200 4 5\n", 101.17157287525382)
check("-1000 0 1 7\n", -999.7071067811865)
check("0 500 10 1\n", 2.9289321881345245)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1000 1000` | `292.89321881345245` | Largest side lengths |
| `100 200 4 5` | `101.17157287525382` | Horizontal translation |
| `-1000 0 1 7` | `-999.7071067811865` | Negative coordinates |
| `0 500 10 1` | `2.9289321881345245` | Independence from `y0` and `b` |

## Edge Cases

Consider the smallest possible triangle:

```
0 0 1 1
```

The algorithm computes

$$t=1-\frac1{\sqrt2},$$

so the answer is approximately `0.2928932188`. This matches the exact equal-area cut instead of the incorrect midpoint at `0.5`.

Now consider a translated triangle:

```
100 200 4 5
```

The local solution is

$$4\left(1-\frac1{\sqrt2}\right)\approx1.171572875.$$

Adding the horizontal offset gives

```
101.171572875...
```

The translation affects only the final addition, leaving the geometry unchanged.

Finally, consider a case with an irrational answer:

```
0 0 3 2
```

The algorithm computes

$$3\left(1-\frac1{\sqrt2}\right)\approx0.878679656.$$

Using floating point arithmetic preserves the required precision, while integer arithmetic would incorrectly round the result and fail the judge.
