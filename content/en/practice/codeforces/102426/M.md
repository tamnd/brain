---
title: "CF 102426M - \u957f\u5b89\u8857\u7684\u534e\u706f"
description: "We have (N) identical circular lighting regions. Their centers lie on one straight street, with consecutive centers exactly (L) units apart, and every circle has radius (R). The task is to compute the area covered by at least one light."
date: "2026-08-12T19:44:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "M"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 72
verified: true
draft: false
---

[CF 102426M - \u957f\u5b89\u8857\u7684\u534e\u706f](https://codeforces.com/problemset/problem/102426/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (N) identical circular lighting regions. Their centers lie on one straight street, with consecutive centers exactly (L) units apart, and every circle has radius (R). The task is to compute the area covered by at least one light.

The circles are arranged in a one-dimensional chain, which is the key structural property. Although the illuminated regions are two-dimensional, their centers have only one degree of freedom, so the overlap pattern is much simpler than it would be for arbitrary circles.

There can be as many as (10^5) test cases, while (N), (R), and (L) can each be as large as (10^9). An algorithm that iterates over the (N) lamps for every test case could require (10^{14}) operations in the worst case, which is far beyond the time limit. We need a constant amount of arithmetic per test case. The large values of (R) and (L) also mean that intermediate geometric expressions should be evaluated with floating-point arithmetic carefully, although Python's integers themselves do not overflow.

Several boundary cases are easy to mishandle. If there are no lamps, for example (N=0,R=10,L=3), the illuminated area is exactly (0), regardless of the other parameters. A formula that starts with (N\pi R^2) handles this naturally, but code that assumes at least one circle may fail.

If (N=1), for example (N=1,R=2,L=100), there is only one circle, so the answer is (4\pi). The distance between consecutive lamps is irrelevant because there is no consecutive pair.

If (L\ge 2R), neighboring circles do not overlap. For example, (N=2,R=1,L=2) gives an area of (2\pi). Using the overlap formula without treating the boundary carefully can introduce a tiny negative square-root argument because of floating-point arithmetic, or incorrectly count a zero-area intersection.

At the other extreme, (L=0) means that every lamp is at exactly the same position. For example, (N=5,R=3,L=0) has area (9\pi), not (45\pi). A correct overlap formula must recognize that the intersection of two coincident circles is the entire circle.

Finally, (R=0) makes every illuminated region a point with zero area. For example, (N=10,R=0,L=7) has answer (0). This case should be handled before evaluating an expression such as (L/(2R)), since division by zero would otherwise occur.

## Approaches

A direct approach would process the lamps from left to right and explicitly maintain which parts of the new circle have already been illuminated. Geometrically, this can be done by computing intersections with previously placed circles. The method is correct because the union area can be obtained by adding the part of each new circle that was not covered before.

The problem is that there can be (N) circles, and a naive implementation may compare each new circle with all earlier circles. One test case can then require (\Theta(N^2)) pair checks, which is (10^{18}) operations when (N=10^9), although the input itself limits the number of test cases rather than making such an iteration practical. Even an (O(N)) algorithm per case is too expensive when (10^5) cases contain large (N).

The useful observation is that we do not actually need to compare a circle with all earlier circles. Consider three consecutive centers at positions (0,L,2L). Take a point that belongs to both the first and third circles. Since the middle center is closer to every point lying between the two outer centers, that point also belongs to the middle circle. More generally, when the circles are added from left to right, every point of the new circle that was already covered by any earlier circle is also covered by the immediately preceding circle.

Thus the new circle overlaps the entire previous union in exactly the same area as it overlaps its immediate predecessor. This remains true even when several circles overlap simultaneously. Triple and higher-order overlaps do not need separate inclusion-exclusion terms because they are already accounted for when each new circle is added.

So the union area has a very simple form. Start with (N) individual circle areas, (N\pi R^2), and subtract the same adjacent-pair overlap (N-1) times. When (L\ge 2R), there is no overlap and nothing needs to be subtracted.

For two equal circles of radius (R), whose centers are (L) apart, their intersection area for (0\le L<2R) is

## 2R^2\arccos\left(\frac{L}{2R}\right)

\frac{L}{2}\sqrt{4R^2-L^2}.
]

Consequently, for (N>0),

[
S=
N\pi R^2-(N-1)S_{\text{overlap}},
]

with (S_{\text{overlap}}=0) when (L\ge 2R).

The important part is not merely recognizing the standard circle-intersection formula. The real simplification is proving that every new circle intersects the entire previous union in only the same region that it shares with its immediate predecessor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) per test case | (O(N)) | Too slow |
| Optimal | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N), (R), and (L). If (N=0) or (R=0), output (0), because there is no positive-area illuminated region.
2. Compute the area of one circle as (\pi R^2), then initialize the total as (N\pi R^2). This represents the area before removing overlaps.
3. Check whether (L<2R). If not, consecutive circles are disjoint or tangent, so the overlap area is zero and the initial total is already the answer.
4. When (L<2R), compute the intersection area of two neighboring circles with

\frac{L}{2}\sqrt{4R^2-L^2}.
]

The first term consists of two circular sectors, while the square-root term removes the two triangular pieces between the chord and the centers.

1. Subtract this overlap exactly (N-1) times. There are (N-1) adjacent pairs, and adding a new circle increases the union by its full area minus exactly its overlap with the preceding circle.
2. Print the resulting floating-point value with enough digits, for example using `:.10f`. Ten digits after the decimal point give substantially more precision than the required (10^{-6}).

Why it works: when the (i)-th circle is added, suppose a point in it also belongs to an earlier circle. The center of the immediately preceding circle lies between the new circle's center and that earlier center. For any point inside both endpoint circles, its distance to the middle center is no greater than its distance to the farther endpoint center. Hence the point also belongs to the preceding circle. Therefore the intersection between the new circle and the entire existing union is exactly its intersection with the preceding circle. The same overlap area is subtracted once for every one of the (N-1) additions, so every point covered by multiple circles is counted exactly once in the final union.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, r, l = map(int, input().split())

        if n == 0 or r == 0:
            out.append("0.0000000000")
            continue

        circle_area = math.pi * r * r
        area = n * circle_area

        if l < 2 * r:
            x = l / (2.0 * r)

            # Protect acos from a possible tiny floating-point drift.
            x = max(-1.0, min(1.0, x))

            overlap = (
                2.0 * r * r * math.acos(x)
                - 0.5 * l * math.sqrt(4.0 * r * r - l * l)
            )

            area -= (n - 1) * overlap

        out.append(f"{area:.10f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first branch handles the two zero-area cases before any division or square root. This is necessary because the overlap formula contains (L/(2R)).

The initial `area` is the sum of the areas of all (N) circles. When (L\ge2R), the circles are disjoint or tangent, so the overlap is zero and the value is already correct.

For overlapping circles, `x` is (L/(2R)), the cosine of half of the angle subtended by the common chord. The `max` and `min` clamp protects `math.acos` from a floating-point value such as `1.0000000000000002`, although the mathematical value is exactly within the valid interval.

The expression under `sqrt` is nonnegative whenever (L<2R). The comparison is done using the original integers, so there is no ambiguity at the boundary (L=2R).

Python integers can represent the products involving values up to (10^9) without overflow. The final geometric calculations use `float`, whose precision is sufficient for the required (10^{-6}) tolerance. Printing ten digits after the decimal point gives additional safety against formatting error.

## Worked Examples

The provided sample represents one test case with (N=4), (R=1), and (L=1). The input as displayed in the statement has lost its line break, so it corresponds to:

```
1
4 1 1
```

For this case, neighboring circles overlap because (1<2).

| Step | (N) | (R) | (L) | Initial area | Pair overlap | Final area |
| --- | --- | --- | --- | --- | --- | --- |
| Input | 4 | 1 | 1 | (4\pi) | (1.2283697\ldots) | (8.8812621\ldots) |

The overlap of two unit circles whose centers are one unit apart is

\frac{2\pi}{3}-\frac{\sqrt3}{2}.
]

There are three adjacent pairs, so the union area is

# 3\left(\frac{2\pi}{3}-\frac{\sqrt3}{2}\right)

2\pi+\frac{3\sqrt3}{2}
\approx8.881262.
]

This demonstrates why simply subtracting the pairwise overlap is still correct even though four circles can participate in regions where several circles overlap. Each circle is added only once, and its newly covered area is determined entirely by the preceding circle.

For a second example, consider two tangent circles:

```
1
2 3 6
```

Here (2R=6=L), so the circles touch at exactly one point. A point has zero area, meaning there is no area to subtract.

| Step | (N) | (R) | (L) | Condition | Overlap | Final area |
| --- | --- | --- | --- | --- | --- | --- |
| Input | 2 | 3 | 6 | (L\ge2R) | 0 | (18\pi) |

The answer is (18\pi\approx56.5486677646). This trace exercises the exact tangency boundary and shows why the overlap branch must use `L < 2 * R`, not `L <= 2 * R`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case performs a constant number of arithmetic, square-root, and trigonometric operations. |
| Space | (O(T)) | The output strings are stored before being written, while the working memory per test case is (O(1)). |

With (T\le10^5), the algorithm performs only a constant amount of work for each test case, so it scales linearly with the input size. There is no dependence on (N), which is essential because (N) can be as large as (10^9). The arithmetic uses only a few scalar variables, and even storing all formatted outputs is small enough for the stated memory limit.

## Test Cases

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, r, l = map(int, input().split())

        if n == 0 or r == 0:
            out.append("0.0000000000")
            continue

        circle_area = math.pi * r * r
        area = n * circle_area

        if l < 2 * r:
            x = l / (2.0 * r)
            x = max(-1.0, min(1.0, x))

            overlap = (
                2.0 * r * r * math.acos(x)
                - 0.5 * l * math.sqrt(4.0 * r * r - l * l)
            )

            area -= (n - 1) * overlap

        out.append(f"{area:.10f}")

    sys.stdout.write("\n".join(out))

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

def check(inp: str, expected: list[float], eps: float = 1e-6):
    actual = list(map(float, run(inp).split()))
    assert len(actual) == len(expected)

    for a, e in zip(actual, expected):
        assert abs(a - e) <= eps * max(1.0, abs(e)), (a, e)

# Provided sample.
check(
    "1\n4 1 1\n",
    [2 * math.pi + 3 * math.sqrt(3) / 2]
)

# Minimum-size input: no lamps.
check(
    "1\n0 1000000000 1000000000\n",
    [0.0]
)

# One circle: L is irrelevant.
check(
    "1\n1 7 0\n",
    [49 * math.pi]
)

# Coincident circles: all N circles occupy exactly the same region.
check(
    "1\n5 3 0\n",
    [9 * math.pi]
)

# Tangency boundary: L = 2R, so there is no positive-area overlap.
check(
    "1\n2 3 6\n",
    [18 * math.pi]
)

# Completely separated circles.
check(
    "1\n4 2 5\n",
    [16 * math.pi]
)

# Several strongly overlapping circles.
check(
    "1\n10 10 1\n",
    [
        10 * math.pi * 100
        - 9 * (
            200 * math.acos(1 / 20)
            - 0.5 * math.sqrt(399)
        )
    ]
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 1000000000 1000000000` | `0` | No lamps, the empty union |
| `1 / 1 7 0` | (49\pi) | Single circle and irrelevant spacing |
| `1 / 5 3 0` | (9\pi) | All circles coincident |
| `1 / 2 3 6` | (18\pi) | Exact tangency at (L=2R) |
| `1 / 4 2 5` | (16\pi) | Completely disjoint circles |
| `1 / 10 10 1` | Formula value | Strong overlap and repeated subtraction |

The tests compare floating-point results numerically rather than comparing formatted strings. This is the correct way to test a geometry solution because mathematically equivalent calculations can differ by a few units in the last several decimal places.

## Edge Cases

For (N=0), consider

```
1
0 1000000000 1000000000
```

The algorithm enters the first condition immediately and returns `0.0000000000`. No circle exists, so there is no illuminated area. A careless implementation that assumes (N\ge1) might still return a nonzero expression if it uses the radius without checking the number of lamps.

For (N=1), consider

```
1
1 2 100
```

The algorithm computes one circle area, (4\pi), and never needs the overlap formula because (N-1=0). The spacing value does not describe any actual pair of lamps in this case. The output is approximately `12.5663706144`.

For coincident circles, consider

```
1
5 3 0
```

The overlap formula gives

[
2\cdot9\arccos(0)-0=9\pi.
]

The initial sum is (5\cdot9\pi), and four overlaps of (9\pi) are removed:

[
45\pi-4(9\pi)=9\pi.
]

Thus the algorithm correctly treats all five lamps as one illuminated disk. This case also confirms that the method handles the extreme of maximum possible overlap without requiring a special formula beyond the general intersection expression.

For tangent circles, consider

```
1
2 3 6
```

Since (L=2R), the overlap branch is skipped. The answer is

[
2\pi\cdot3^2=18\pi.
]

The circles share only one boundary point, whose area is zero. Using a strict `<` comparison avoids unnecessarily evaluating the square root at zero and makes the geometric meaning of the boundary explicit.

For separated circles, consider

```
1
4 2 5
```

Here (2R=4<L=5), so every circle is disjoint from the next one and consequently from every other circle. The answer is simply

[
4\cdot\pi\cdot2^2=16\pi.
]

The algorithm never calls `acos` or `sqrt` in this branch, so there is no risk of evaluating the intersection formula outside its geometric domain.

For many heavily overlapping circles, consider (N=10,R=10,L=1). Every newly added circle overlaps the previous union, but the amount that needs to be removed is still exactly the two-circle overlap. The algorithm performs that subtraction nine times rather than attempting to enumerate triple, quadruple, or higher-order intersections. This is the central invariant of the solution and is what reduces the entire geometry problem to (O(1)) work per test case.
