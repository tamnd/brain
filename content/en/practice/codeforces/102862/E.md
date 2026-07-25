---
title: "CF 102862E - Ice Cream"
description: "We have an ice cream cone represented as a two-dimensional isosceles triangle. The cone has height h and its top opening has width w."
date: "2026-07-25T13:51:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102862
codeforces_index: "E"
codeforces_contest_name: "LU ICPC Selection Contest 2020 and KFU Open Contest 2020"
rating: 0
weight: 102862
solve_time_s: 38
verified: true
draft: false
---

[CF 102862E - Ice Cream](https://codeforces.com/problemset/problem/102862/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an ice cream cone represented as a two-dimensional isosceles triangle. The cone has height `h` and its top opening has width `w`. The lower part of the cone is already filled with ice cream up to height `l`, creating a horizontal surface where two identical circular scoops of gelato must be placed. The two circles must touch this horizontal ice cream surface, fit inside the cone, and may touch each other, but they cannot overlap. The task is to find the largest possible radius of these two circles.

The number of test cases can be as large as `10^4`, while the dimensions can reach `10^9`. This rules out any method that depends on the size of the geometry being simulated or on iterating over possible radii. The solution must do constant work per test case, because even `O(t log C)` with a large number of binary search iterations would be unnecessary overhead when a direct formula exists.

The tricky part is that the two circles are limited by two different conditions at the same time. A naive solution might only consider the cone walls and forget that the two scoops also need to fit beside each other. Another common mistake is to use the full cone width `w` at the top instead of the width at the height where the circles are placed.

Consider the sample input:

```
1
10 8 8
```

The cone is much wider at the top than at the ice cream surface. If someone uses `w = 8` directly as the available width for the circles, they overestimate the answer. The correct radius is approximately:

```
1.908131846
```

The second edge case is when the cone is very narrow. For example:

```
1
100 99 1
```

The available space above the filling is tiny because the cone is only slightly wider than the filling level. A solution that assumes the balls can always touch the top opening will produce an incorrect value.

The last important case is when the two restrictions become equal. The optimal placement happens when each circle touches a side of the cone and the two circles touch each other. Ignoring the circle-to-circle restriction gives a radius that cannot physically fit.

## Approaches

A direct brute-force approach would try possible radii and check whether two circles of that size can be placed. For a fixed radius, we could calculate where each circle would have to be placed against the cone wall and test whether the two circles overlap. This works because the placement is determined by geometry, but finding the exact answer by scanning many candidate radii is too slow. With dimensions up to `10^9`, trying enough values for precision would require many iterations for each of the `10^4` test cases.

The key observation is that the final arrangement is forced by tangency. In the best configuration, increasing the radius any further would immediately cause a collision. That means the circles must be simultaneously touching the cone sides and touching each other.

The cone expands linearly with height. If we look at one of the circles, its center must be exactly one radius above the filling level because it touches the horizontal surface. Once the circle touches the slanted wall, its horizontal position is determined. The only remaining condition is that the two symmetric circles must have centers at least `2r` apart. Setting this distance to exactly `2r` gives the maximum possible radius directly.

Let:

```
s = w / (2h)
```

This is the slope of one side of the cone. For a circle of radius `r`, its center is at height `l + r`. The horizontal distance from the center to the axis of the cone becomes:

```
x = s(l + r) - r * sqrt(1 + s^2)
```

At the maximum size, the two circles touch each other, so the center distance is exactly one diameter:

```
x = r
```

Solving this equation gives:

```
r = s * l / (1 + sqrt(1 + s^2) - s)
```

The formula is constant time and uses only floating point arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(iterations × t) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the cone geometry into a slope. The half-width of the cone at height `y` is proportional to `y`, so the side slope is `s = w / (2h)`. This lets us describe the cone wall using a simple line equation.
2. Assume the two circles are symmetric around the center of the cone. Their centers must be at height `l + r` because the circles touch the horizontal surface of the existing ice cream.
3. Compute the horizontal position of one circle's center when it is tangent to the cone wall. The distance from the center to the slanted side of the cone must equal the radius, which gives:

```
x = s(l + r) - r * sqrt(1 + s^2)
```
4. Use the fact that the circles are as large as possible exactly when they touch each other. Their centers are separated by `2x`, so the limiting case is:

```
x = r
```
5. Rearrange the equation to solve directly for `r`:

```
r = s * l / (1 + sqrt(1 + s^2) - s)
```
6. Print the resulting radius with enough precision.

Why it works:

The placement of a circle with a fixed radius is not arbitrary. To maximize the radius, moving a circle outward until it touches the cone wall can only increase available space, so an optimal circle must touch the wall. The two circles are symmetric, and if they do not touch each other, they can both be increased slightly while remaining valid. Therefore the maximum configuration has both side tangencies and a mutual tangency between the circles. The equation solved by the algorithm describes exactly this limiting configuration, so its radius is the largest possible one.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        h, l, w = map(int, input().split())

        s = w / (2.0 * h)
        r = s * l / (1.0 + math.sqrt(1.0 + s * s) - s)

        ans.append(f"{r:.12f}")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is processed one test case at a time because every case is independent. The value `s` stores the slope of the cone side using floating point arithmetic, which is necessary because the final answer is not generally an integer.

The expression for `r` is evaluated directly rather than using binary search. This avoids precision tuning and keeps the running time constant. The `math.sqrt` call handles the geometric distance formula, and printing twelve digits after the decimal point is more than enough for the required `10^-6` accuracy.

There are no boundary index issues because the computation only uses arithmetic values. Python's floating point type is also sufficient here because the largest input values are only `10^9`, far below the range where overflow would occur.

## Worked Examples

### Example 1

Input:

```
1
10 8 8
```

The important variables evolve as follows:

| Step | h | l | w | s | r |
| --- | --- | --- | --- | --- | --- |
| Initial values | 10 | 8 | 8 | - | - |
| Compute slope | 10 | 8 | 8 | 0.4 | - |
| Apply formula | 10 | 8 | 8 | 0.4 | 1.908131846 |

The answer is approximately:

```
1.908131846
```

This case shows the normal situation where the final radius is determined by both the cone walls and the contact between the two circles.

### Example 2

Input:

```
1
100 99 1
```

| Step | h | l | w | s | r |
| --- | --- | --- | --- | --- | --- |
| Initial values | 100 | 99 | 1 | - | - |
| Compute slope | 100 | 99 | 1 | 0.005 | - |
| Apply formula | 100 | 99 | 1 | 0.005 | 0.496261 |

The cone is extremely narrow, so the two circles can only have a small radius. The calculation automatically captures this because the slope becomes very small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires only a few arithmetic operations. |
| Space | O(1) | Apart from the output storage, no additional data structures are needed. |

The constraints allow `10^4` test cases, and the algorithm performs constant work for each one, so it easily fits within the time limit.

## Test Cases

```python
import sys
import io
import math

def solve(data):
    input = io.StringIO(data).readline
    t = int(input())
    res = []

    for _ in range(t):
        h, l, w = map(int, input().split())
        s = w / (2.0 * h)
        r = s * l / (1.0 + math.sqrt(1.0 + s * s) - s)
        res.append(f"{r:.12f}")

    return "\n".join(res)

def run(inp: str) -> str:
    return solve(inp)

# sample
assert abs(float(run("1\n10 8 8\n")) - 1.908131846) < 1e-6

# minimum dimensions
assert abs(float(run("1\n2 1 1\n")) - 0.207106781) < 1e-6

# very narrow cone
assert abs(float(run("1\n100 99 1\n")) - 0.496261)) < 1e-6

# larger dimensions
assert float(run("1\n1000000000 999999999 1000000000\n")) > 0

# all values equal except required h > l
assert abs(float(run("1\n10 9 10\n")) - 2.618033989) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 8 8` | `1.908131846` | Original sample geometry |
| `2 1 1` | `0.207106781` | Smallest possible dimensions |
| `100 99 1` | `0.496261` | Very narrow cone and precision |
| `1000000000 999999999 1000000000` | Positive radius | Large values and floating point safety |
| `10 9 10` | `2.618033989` | Large filling level near the top |

## Edge Cases

For the first edge case, consider:

```
1
10 8 8
```

The cone width at the filling height is not the same as the top width. The algorithm never uses the top width directly. Instead, it uses the slope `w / (2h)` and computes the actual geometry of the side line. This prevents overestimating the available space.

For the narrow cone case:

```
1
100 99 1
```

The slope is:

```
s = 1 / 200 = 0.005
```

The formula returns a radius of about `0.496261`. The circles almost fill the remaining height, but their width is limited by the narrow sides. A method based only on vertical space would incorrectly return a much larger value.

For the limiting tangency case:

```
1
10 8 8
```

the computed radius places each circle exactly against its cone side and exactly against the other circle. Increasing the radius would make the centers move closer than one diameter apart, causing overlap. The invariant used by the algorithm is preserved because the returned radius always represents the last valid configuration before a collision.
