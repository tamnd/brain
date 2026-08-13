---
title: "CF 102284B - \u0411\u043e\u043b\u044c\u0448\u0438\u0435 \u0447\u0430\u0441\u044b \u0438 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0430\u044f \u043e\u043a\u0440\u0443\u0436\u043d\u043e\u0441\u0442\u044c"
description: "The archived Codeforces contest lists problem B as «Большие часы и маленькая окружность», with a 2 second time limit and 512 MB of memory. The geometric setup consists of one small circle in the center and (n) identical larger circles arranged symmetrically around it."
date: "2026-08-13T16:15:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "B"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 141
verified: true
draft: false
---

[CF 102284B - \u0411\u043e\u043b\u044c\u0448\u0438\u0435 \u0447\u0430\u0441\u044b \u0438 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u0430\u044f \u043e\u043a\u0440\u0443\u0436\u043d\u043e\u0441\u0442\u044c](https://codeforces.com/problemset/problem/102284/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

The archived Codeforces contest lists problem B as «Большие часы и маленькая окружность», with a 2 second time limit and 512 MB of memory.

The geometric setup consists of one small circle in the center and (n) identical larger circles arranged symmetrically around it. The small circle has radius (r). Every large circle touches the small circle externally, and every pair of neighboring large circles also touches each other. The task is to determine the radius (R) of each large circle.

The key point is that the centers of the large circles form a regular (n)-gon. The distance from the common center to every large-circle center is (R+r), because the two circles are externally tangent. At the same time, two neighboring large-circle centers are exactly (2R) apart, because those large circles touch each other.

The constraints are small, with (3 \le n \le 100) and (1 \le r \le 100). This means even a complicated constant-time geometric calculation is easily fast enough, and there is no need for iteration over the circles. The real issue is numerical precision, not running time. The required answer is a real number, so the implementation should use floating-point arithmetic and print enough digits.

There are several edge cases where a seemingly reasonable implementation can go wrong. When (n=6) and (r=1), the answer is exactly (1). The six large circles form a regular hexagon around the small one, and their centers lie at distance (2) from the center. A formula using the full central angle (2\pi/n) where the half-angle (\pi/n) is needed gives the wrong radius.

For input

```
6 1
```

the correct output is

```
1.0000000000
```

A second boundary case is (n=3), (r=1). The three large circles form an equilateral arrangement. The answer is approximately (6.4641016151). A careless implementation that assumes the outer radius is close to (r) fails badly here, because with only three outer circles there is a large amount of space between the center and their points of tangency.

For input

```
3 1
```

the correct output is approximately

```
6.4641016151
```

A third precision-sensitive case is (n=100), (r=1). The answer is only about (0.032429391). An implementation that prints too few digits can lose the required precision, especially because the answer is much smaller than one.

For input

```
100 1
```

the correct output is approximately

```
0.0324293910
```

## Approaches

A direct brute-force approach could search for (R) numerically. Since (n\ge3) and (r\le100), the actual answer is below (647). If we tried every candidate with a step of (10^{-6}), we would inspect roughly (647,000,000) candidates in the worst case. Each candidate would require checking the geometric tangency condition, so this approach is far beyond what is sensible for a 2 second limit. A larger step is not safe because the required answer is continuous and the checker expects a small absolute or relative error.

A binary search is already much better. For a chosen (R), we can calculate the distance between neighboring large-circle centers and compare it with (2R). Since that condition is monotonic in (R), around 60 to 100 binary-search iterations are enough for double precision. Such a solution would be accepted, but it is still solving a numerical equation iteratively when the geometry gives us the equation directly.

The useful observation is that the centers of the large circles form a regular (n)-gon. Consider the center of the small circle, the centers of two neighboring large circles, and the midpoint of the segment joining those two large-circle centers. This creates a right triangle. Its hypotenuse is (R+r), because it connects the common center to a large-circle center. The opposite side is (R), because the full distance between neighboring large-circle centers is (2R), so half of it is (R).

The angle at the common center is half of the central angle between neighboring vertices of the regular (n)-gon, namely

[
\frac{\pi}{n}.
]

Thus

\frac{R}{R+r}.
]

Let

[
s=\sin\left(\frac{\pi}{n}\right).
]

Then

[
s(R+r)=R,
]

so

[
sR+sr=R,
]

and consequently

[
R(1-s)=sr.
]

The required radius is therefore

[
\boxed{
R=\frac{r\sin(\pi/n)}
{1-\sin(\pi/n)}
}.
]

The brute-force works because every candidate can be checked against the same geometric condition, but fails because a continuous value cannot sensibly be enumerated at the required precision. The observation that the centers form a regular polygon turns the entire problem into one trigonometric expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^9)) in a (10^{-6}) grid | (O(1)) | Too slow |
| Optimal | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the number (n) of large circles and the radius (r) of the small circle. There is only one test case, so no outer test-case loop is needed.
2. Compute the half-angle

[
\theta=\frac{\pi}{n}.
]

Neighboring centers are separated by an angle (2\pi/n), and the right-triangle construction uses half of that angle.
3. Compute

[
s=\sin(\theta).
]

In the right triangle, (R) is opposite (\theta) and (R+r) is the hypotenuse, giving (s=R/(R+r)).
4. Rearrange the equation to obtain

[
R=\frac{rs}{1-s}.
]

The denominator is positive because (n\ge3), so (0<\pi/n\le\pi/3) and consequently (0<s<1).
5. Print (R) with enough decimal places. Ten digits after the decimal point provide considerably more precision than the required tolerance.

Why it works: the centers of all large circles must lie at the same distance (R+r) from the center of the small circle, and neighboring centers must be (2R) apart. Those two facts uniquely determine the isosceles triangle formed by the three centers. Splitting that triangle in half gives a right triangle whose sine relation is exactly (R/(R+r)=\sin(\pi/n)). The algorithm solves this equation algebraically, so the printed value is the unique radius satisfying both tangency requirements.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, r = map(float, input().split())

    s = math.sin(math.pi / n)
    R = r * s / (1.0 - s)

    print(f"{R:.10f}")

if __name__ == "__main__":
    solve()
```

The first line reads the two geometric parameters. Although (n) is mathematically an integer, reading it as a floating-point value is harmless and lets the expression `math.pi / n` be written directly.

The variable `s` stores (\sin(\pi/n)), which is the only nontrivial geometric quantity required by the formula. The radius is then obtained from `r * s / (1.0 - s)`.

The denominator must be `1.0 - s`, not `s - 1.0`. The latter would produce a negative radius. The half-angle must be `math.pi / n`, not `2 * math.pi / n`, because the right triangle contains half of the angle between neighboring circle centers.

There is no integer overflow issue because Python integers have arbitrary precision and the actual computation uses floating-point values. The possible values are also small enough that ordinary double precision has ample accuracy.

The output uses ten digits after the decimal point. Printing seven or eight digits would usually be enough, but ten gives a comfortable margin for the required error tolerance.

## Worked Examples

### Sample 1

Consider

```
3 1
```

The three large-circle centers form an equilateral triangle. The following trace shows the values used by the formula.

| (n) | (r) | (\theta=\pi/n) | (s=\sin(\theta)) | (1-s) | (R=rs/(1-s)) |
| --- | --- | --- | --- | --- | --- |
| 3 | 1 | 1.04719755 | 0.86602540 | 0.13397460 | 6.46410162 |

The angle between neighboring centers is (2\pi/3), so the right triangle uses (\pi/3). Its hypotenuse is (R+1), while its opposite side is (R). The equation (R/(R+1)=\sqrt3/2) gives (R\approx6.46410162).

This example demonstrates why the answer can be much larger than the radius of the small circle. With only three outer circles, their centers have to be far away to make the circles touch both the central circle and their two neighbors.

### Sample 2

Consider

```
6 1
```

The trace becomes particularly simple.

| (n) | (r) | (\theta=\pi/n) | (s=\sin(\theta)) | (1-s) | (R=rs/(1-s)) |
| --- | --- | --- | --- | --- | --- |
| 6 | 1 | 0.52359878 | 0.50000000 | 0.50000000 | 1.00000000 |

Here the half-angle is (30^\circ), whose sine is exactly (1/2). The equation becomes (R/(R+1)=1/2), giving (R=1).

This example is useful for checking the half-angle. Using (2\pi/n=60^\circ) instead would use (\sin60^\circ) and produce an incorrect result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Only a constant number of arithmetic and trigonometric operations are performed. |
| Space | (O(1)) | Only a few floating-point variables are stored. |

The constraints are tiny compared with what an (O(1)) solution can handle. The calculation performs no loops proportional to (n), so the maximum value (n=100) has no meaningful performance impact. The 512 MB memory limit is also far above the constant amount of memory used by the program.

## Test Cases

```python
import sys
import io
import math

def solve():
    n, r = map(float, input().split())

    s = math.sin(math.pi / n)
    R = r * s / (1.0 - s)

    print(f"{R:.10f}")

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue() if False else ""
    finally:
        input = old_input
        sys.stdin = old_stdin

def solve_for_test(inp: str) -> float:
    n, r = map(float, inp.split())
    s = math.sin(math.pi / n)
    return r * s / (1.0 - s)

# Provided samples.
assert abs(solve_for_test("3 1") - 6.464101615137754) < 1e-9, "sample 1"
assert abs(solve_for_test("6 1") - 1.0) < 1e-9, "sample 2"
assert abs(solve_for_test("100 100") - 3.2429391) < 1e-7, "sample 3"

# Minimum n, small r.
assert abs(solve_for_test("3 1") - 6.464101615137754) < 1e-9, "minimum n"

# Maximum n and maximum r.
assert abs(solve_for_test("100 100") - 3.2429391) < 1e-7, "maximum values"

# Equal input values n = r = 4.
assert abs(
    solve_for_test("4 4") - 9.65685424949238
) < 1e-9, "equal values"

# Large n with the smallest radius, testing a small answer.
assert abs(
    solve_for_test("100 1") - 0.032429391
) < 1e-9, "small answer"

# n = 5 catches confusion between pi/n and 2*pi/n.
assert abs(
    solve_for_test("5 1") - 1.42532540417602
) < 1e-9, "half-angle boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1` | `6.4641016151` | Minimum (n), large resulting radius |
| `100 100` | `3.2429391` | Maximum values and floating-point precision |
| `4 4` | `9.6568542495` | Equal input values |
| `100 1` | `0.0324293910` | Very small answer and precision |
| `5 1` | `1.4253254042` | Correct use of the half-angle |

The test helper evaluates the same mathematical expression as the submitted solution and compares numerical values rather than requiring an exact textual representation. That is appropriate for a floating-point output problem, where many different decimal representations can satisfy the checker.

## Edge Cases

For (n=6) and (r=1), the input is

```
6 1
```

The algorithm computes (\sin(\pi/6)=1/2), so

[
R=\frac{1\cdot(1/2)}{1-1/2}=1.
]

The output is

```
1.0000000000
```

This catches the most common geometric mistake, using the full angle between neighboring centers instead of half of it.

For (n=3) and (r=1), the input is

```
3 1
```

The algorithm gets (\sin(\pi/3)=\sqrt3/2), giving

[
R=
\frac{\sqrt3/2}{1-\sqrt3/2}
\approx6.4641016151.
]

The output is

```
6.4641016151
```

This is the smallest possible number of outer circles and produces the largest ratio between the outer and inner radii.

For (n=100) and (r=1), the input is

```
100 1
```

The angle (\pi/100) is small, so its sine is about (0.0314108). The formula gives

[
R\approx
\frac{0.0314108}{0.9685892}
\approx0.032429391.
]

The output is

```
0.0324293910
```

This case checks that the implementation does not accidentally round a small positive answer to zero.

For (n=4) and (r=4), the input is

```
4 4
```

Here (\sin(\pi/4)=\sqrt2/2), so

[
R=
\frac{4(\sqrt2/2)}{1-\sqrt2/2}
\approx9.6568542495.
]

The output is

```
9.6568542495
```

This case has equal input values but does not create any special mathematical case. The same formula applies without modification, which is exactly what a robust implementation should do.
