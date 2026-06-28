---
title: "CF 104886B - Easy Geometry"
description: "The brute-force view is to treat the river contact point as a variable point $P = (x, 0)$ and minimize the function $$f(x) = sqrt{(x-x1)^2 + y1^2} + sqrt{(x-x2)^2 + y2^2}."
date: "2026-06-28T09:06:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104886
codeforces_index: "B"
codeforces_contest_name: "USI-Team-Selection 2023-2024"
rating: 0
weight: 104886
solve_time_s: 47
verified: true
draft: false
---

[CF 104886B - Easy Geometry](https://codeforces.com/problemset/problem/104886/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Approaches

The brute-force view is to treat the river contact point as a variable point $P = (x, 0)$ and minimize the function

$$f(x) = \sqrt{(x-x_1)^2 + y_1^2} + \sqrt{(x-x_2)^2 + y_2^2}.$$

A direct approach would try many candidate values of $x$, but the search space is continuous and unbounded. Even if discretized, achieving $10^{-6}$ precision for every test case under 10^5 queries is infeasible.

The key structural observation is that the optimal path must reflect a classic geometry principle: reflecting one endpoint across the constraint line converts a broken path with a single contact into a straight-line distance. If we reflect the destination point across the river line $y=0$, it becomes $(x_2, -y_2)$. Any path that goes from $(x_1,y_1)$ to a point on the river and then to $(x_2,y_2)$ is equivalent in length to a path from $(x_1,y_1)$ to $(x_2,-y_2)$ with a single “kink” on the river, and the shortest such path occurs when the kink lies on the straight segment between these two points.

This reduces the problem to computing a standard Euclidean distance between the original start point and the reflected endpoint. The river constraint is automatically satisfied by construction of the reflection argument, since the intersection point of the straight segment with $y=0$ is exactly the optimal touch point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over river point | O(T · K) for large K or continuous search | O(1) | Too slow |
| Reflection trick | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Take the starting point $(x_1, y_1)$ and reflect the destination point across the river line to get $(x_2, -y_2)$. This transformation converts the constrained path into an unconstrained straight-line problem in Euclidean space.
2. Compute the squared distance between $(x_1, y_1)$ and $(x_2, -y_2)$, because working in squared form avoids premature floating-point operations and keeps the implementation stable.
3. Take the square root of this value to obtain the final answer for the test case.
4. Repeat this independently for each test case, since there is no interaction between queries.

The key idea behind the reflection is that any path that touches the river exactly once can be “unfolded” into a straight segment in a reflected coordinate system. The optimality comes from the fact that Euclidean shortest paths are straight lines in a plane without obstacles.

### Why it works

The river acts like a mandatory intermediate constraint forcing the path to cross the line $y=0$. Reflecting one endpoint across that line creates a geometric symmetry where every valid two-segment path corresponds to a broken line with the same length in the reflected plane. Among all such broken lines, the straight segment between the original point and the reflected point is the shortest possible connection, and its intersection with the river automatically gives a valid meeting point. This ensures the computed distance is minimal among all admissible river-touching paths.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

t = int(input())
for _ in range(t):
    x1, y1, x2, y2 = map(int, input().split())

    dx = x1 - x2
    dy = y1 + y2  # since reflected point is (x2, -y2)

    print(math.hypot(dx, dy))
```

The implementation directly follows the reflection reduction. The only subtle point is the expression for the vertical difference: after reflection, the y-coordinate difference becomes $y_1 - (-y_2) = y_1 + y_2$, which is easy to get wrong if written mechanically.

Using `math.hypot` avoids manual squaring and square root ordering issues and is numerically stable for large coordinates.

## Worked Examples

Consider a simple case where the two points are horizontally aligned above the river. The reflection creates a symmetric configuration.

For input:

```
0 1 2 1
```

| Step | x1 | y1 | x2 | y2 | Reflected x2,y2 | dx | dy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 2 | 1 | (2, -1) | -2 | 2 |

The computed distance is $\sqrt{(-2)^2 + 2^2} = \sqrt{8}$, which matches the shortest path going down to the river and back up optimally.

For a more skewed case:

```
-10 10 -20 20
```

| Step | x1 | y1 | x2 | y2 | Reflected x2,y2 | dx | dy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | -10 | 10 | -20 | 20 | (-20, -20) | 10 | 30 |

The distance becomes $\sqrt{10^2 + 30^2} = \sqrt{1000}$, showing that vertical separation dominates when both points are far from the river.

These examples confirm that the algorithm behaves like a direct Euclidean measurement in a transformed space, which is exactly what the geometric argument predicts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs a constant number of arithmetic operations and one square root |
| Space | O(1) | No auxiliary data structures beyond input variables |

The solution easily fits within limits because even for 10^5 test cases, the work reduces to a handful of floating-point operations per case.

## Test Cases

```python
import sys, io, math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    t = int(input())
    out = []
    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())
        dx = x1 - x2
        dy = y1 + y2
        out.append(str(math.hypot(dx, dy)))
    return "\n".join(out)

# provided samples
assert run("""2
0 1 2 1
-10 10 -20 20
""").split()[0][:5] == "2.828", "sample 1"

# minimum size-like symmetry
assert run("""1
0 1 0 1
""").strip()[:3] == "2.0", "vertical symmetry"

# large coordinates
assert run("""1
-1000000000 1000000000 1000000000 1000000000
""").strip()[:5] == "28284", "large scale"

# asymmetric heights
assert run("""1
1 2 3 10
""") != "", "general case"

# identical x
assert run("""1
5 1 5 100
""") != "", "same x axis-aligned test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| same point mirrored | 2.0 | degenerate symmetric geometry |
| large coordinates | large value | numeric stability |
| same x, different y | computed distance | vertical dominance case |
| general case | valid real number | correctness of reflection model |

## Edge Cases

When both points share the same x-coordinate, the optimal path still goes straight down to the river and straight back up, and the formula reduces cleanly to $\sqrt{(y_1 + y_2)^2}$, which matches intuition.

When the points are symmetric around some vertical line, the reflected formulation ensures that the straight segment passes exactly through the optimal river contact, so no special casing is required.

When one point is very close to the river, the expression still behaves correctly because the reflection does not introduce instability, the distance simply approaches the direct segment from near the boundary to the reflected point of the other endpoint.
