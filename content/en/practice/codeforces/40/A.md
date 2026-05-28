---
title: "CF 40A - Find Color"
description: "The plane is colored using concentric rings centered at the origin. Every ring between two consecutive integer distances alternates color. The borders themselves, meaning all points whose distance from the origin is an integer, are always black."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "geometry", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 40
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 39"
rating: 1300
weight: 40
solve_time_s: 84
verified: true
draft: false
---
[CF 40A - Find Color](https://codeforces.com/problemset/problem/40/A)

**Rating:** 1300  
**Tags:** constructive algorithms, geometry, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The plane is colored using concentric rings centered at the origin. Every ring between two consecutive integer distances alternates color. The borders themselves, meaning all points whose distance from the origin is an integer, are always black.

For a point `(x, y)`, we need to determine whether the point lies on a black boundary or inside a white region. The pattern alternates as the distance grows outward from the origin.

The key geometric quantity is the Euclidean distance from the origin:

$d = \sqrt{x^2 + y^2}$Drag the points to update the distance between two points.-10-8-6-4-2246810-10-5510A(6.0, 6.0)B(-6.0, -6.0)d = 16.97Delta x = 12Delta y = 12

If `d` is an integer, the answer is immediately `"black"` because the point lies exactly on a circle boundary.

Otherwise, the color depends on which annulus the point belongs to. The region between radius `0` and `1` is black, between `1` and `2` is white, between `2` and `3` is black again, and so on. In other words, the integer part of the distance determines the color parity.

The coordinate bounds are tiny, only up to `1000` in absolute value. Even an inefficient solution would run comfortably fast. Still, the problem is mainly about correctly interpreting the geometry and handling floating-point pitfalls.

The tricky part is detecting whether the distance is exactly an integer. A careless implementation using floating-point comparisons can fail because values like `sqrt(25)` may internally become `4.99999999997` or `5.00000000001`.

Consider the point:

```
3 4
```

The distance is exactly `5`, so the answer must be `"black"`. A floating-point comparison like `sqrt(x*x+y*y) == int(sqrt(...))` is unsafe.

Another subtle case is the origin:

```
0 0
```

Its distance is `0`, which is an integer, so the point is black. Some implementations accidentally classify it using parity logic and produce the wrong result.

One more easy-to-miss case is a point just inside a boundary:

```
2 2
```

The distance is about `2.828`, which lies between `2` and `3`. Since the interval `[2,3)` corresponds to a black region, the answer is `"black"`. Using rounding instead of flooring would incorrectly move it into the next ring.

## Approaches

A brute-force way to think about the problem is to imagine all concentric circles with integer radii. We could repeatedly increase the radius until we locate the first circle outside the point. Once we know the ring index, we can determine the color by parity.

That works because the coloring only changes when crossing an integer-radius circle. Since coordinates are at most `1000`, the maximum possible distance is roughly `1414`, so even scanning all radii would take only about `1400` iterations.

Still, the geometry gives a direct shortcut. The only information we actually need is:

1. Whether the distance is an integer.
2. Otherwise, the parity of `floor(distance)`.

The observation comes from how the coloring alternates ring by ring. Every annulus `[k, k+1)` has a fixed color determined entirely by `k`.

Instead of repeatedly checking circles, we can compute:

$r^2 = x^2 + y^2$$h$$k$$r$$(x)^2 + (y)^2 = 3.0^2$Sliders update the center and radius of the circle equation.-10-8-6-4-2246810-6-4-2246

If `r²` is a perfect square, the point is black.

Otherwise, let:

$k = \lfloor \sqrt{x^2+y^2} \rfloor$

When `k` is even, the region is black. When `k` is odd, the region is white.

This removes all iteration and avoids floating-point precision problems by using integer arithmetic wherever possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(R) | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coordinates `x` and `y`.
2. Compute the squared distance from the origin:

$s = x^2 + y^2$

Using the squared distance avoids unnecessary floating-point operations.
3. Compute the integer square root of `s`.

Let `r = isqrt(s)`.

This gives the largest integer such that `r² ≤ s`.
4. Check whether `r * r == s`.

If true, the point lies exactly on an integer-radius circle, so print `"black"`.
5. Otherwise, determine the ring index using `r`.

Since `r = floor(distance)`, the point belongs to the annulus `[r, r+1)`.
6. If `r` is even, print `"black"`.

If `r` is odd, print `"white"`.

The colors alternate starting from the center, where radius interval `[0,1)` is black.

### Why it works

Every integer-radius circle acts as a boundary between two regions. The interval `[0,1)` is black, `[1,2)` is white, `[2,3)` is black again, and the alternation continues forever.

For any point not on a boundary, its color depends only on the integer part of its distance from the origin. The value `floor(distance)` uniquely identifies the annulus containing the point. Even indices correspond to black regions, odd indices to white regions.

Checking whether the squared distance is a perfect square correctly detects boundary points without floating-point errors.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

x, y = map(int, input().split())

s = x * x + y * y
r = isqrt(s)

if r * r == s:
    print("black")
else:
    if r % 2 == 0:
        print("black")
    else:
        print("white")
```

The program begins by computing the squared distance instead of the actual distance. This is safer because integer arithmetic is exact.

The function `isqrt` returns the floor of the square root using pure integer operations. That avoids precision issues that can appear with `sqrt`.

The condition `r * r == s` checks whether the distance is an exact integer. Those points are always black because every boundary circle is black.

If the point is not on a boundary, the parity of `r` determines the ring color. The center region starts black, so even-numbered rings are black and odd-numbered rings are white.

A common mistake is using `round(sqrt(...))` instead of `floor`. Rings are defined by intervals, so flooring is the correct operation.

## Worked Examples

### Example 1

Input:

```
-2 1
```

| Step | Value |
| --- | --- |
| `x` | `-2` |
| `y` | `1` |
| `s = x² + y²` | `5` |
| `r = isqrt(5)` | `2` |
| `r*r == s` | `4 == 5` → false |
| `r % 2` | `0` |
| Answer | `black` |

The point lies between radius `2` and `3`, which is a black ring.

### Example 2

Input:

```
1 1
```

| Step | Value |
| --- | --- |
| `x` | `1` |
| `y` | `1` |
| `s = x² + y²` | `2` |
| `r = isqrt(2)` | `1` |
| `r*r == s` | `1 == 2` → false |
| `r % 2` | `1` |
| Answer | `white` |

This point lies inside the annulus `[1,2)`, which is white.

### Example 3

Input:

```
3 4
```

| Step | Value |
| --- | --- |
| `x` | `3` |
| `y` | `4` |
| `s = x² + y²` | `25` |
| `r = isqrt(25)` | `5` |
| `r*r == s` | `25 == 25` → true |
| Answer | `black` |

This example demonstrates the boundary rule. The point lies exactly on the circle of radius `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra memory proportional to input size is used |

The constraints are extremely small, so this solution easily fits within the limits. Even thousands of test cases would run instantly.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from math import isqrt

def solve():
    input = sys.stdin.readline

    x, y = map(int, input().split())

    s = x * x + y * y
    r = isqrt(s)

    if r * r == s:
        print("black")
    else:
        print("black" if r % 2 == 0 else "white")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("-2 1\n") == "black", "sample 1"

# custom cases
assert run("0 0\n") == "black", "origin is on integer-radius boundary"
assert run("1 1\n") == "white", "inside white ring"
assert run("3 4\n") == "black", "perfect-square distance"
assert run("2 2\n") == "black", "inside black ring"
assert run("1000 1000\n") == "black", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `black` | Origin handling |
| `1 1` | `white` | Odd-indexed ring |
| `3 4` | `black` | Exact integer distance |
| `2 2` | `black` | Flooring instead of rounding |
| `1000 1000` | `black` | Large coordinate values |

## Edge Cases

The first important edge case is a point exactly on a boundary circle.

Input:

```
3 4
```

The algorithm computes:

| Variable | Value |
| --- | --- |
| `s` | `25` |
| `r` | `5` |
| `r*r == s` | true |

Since the squared distance is a perfect square, the algorithm immediately prints `"black"`. This correctly handles the rule that every boundary is black.

The second edge case is the origin.

Input:

```
0 0
```

The execution becomes:

| Variable | Value |
| --- | --- |
| `s` | `0` |
| `r` | `0` |
| `r*r == s` | true |

The algorithm again returns `"black"` because the origin lies on the radius-0 boundary.

The third subtle case is a point near a boundary but not exactly on it.

Input:

```
2 2
```

The values are:

| Variable | Value |
| --- | --- |
| `s` | `8` |
| `r` | `2` |
| `r*r == s` | false |
| `r % 2` | `0` |

The point lies in the interval `[2,3)`, which is black. Using `floor(distance)` through `isqrt` produces the correct ring index. A buggy implementation using rounding could incorrectly classify this point as belonging to the next ring.
