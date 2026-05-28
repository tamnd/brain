---
title: "CF 190B - Surrounded"
description: "We are given two circles on the plane. Each circle represents an enemy ring surrounding a city. A radar can be placed at any point, and it detects everything within distance r from its position. The radar must be able to detect at least one point from each circle."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 190
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 120 (Div. 2)"
rating: 1800
weight: 190
solve_time_s: 94
verified: true
draft: false
---

[CF 190B - Surrounded](https://codeforces.com/problemset/problem/190/B)

**Rating:** 1800  
**Tags:** geometry  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two circles on the plane. Each circle represents an enemy ring surrounding a city. A radar can be placed at any point, and it detects everything within distance `r` from its position.

The radar must be able to detect at least one point from each circle. We want the smallest possible detection radius.

Geometrically, each enemy ring is the circumference of a circle. If the radar is placed at point `P`, then its distance to a circle is the minimum distance from `P` to any point on that circumference. The radar works if that minimum distance is at most `r` for both circles.

The input gives the centers and radii of the two circles. The output is the minimum possible radius of the radar.

The coordinates and radii are at most `10^4`, so every computation easily fits inside standard floating point arithmetic. The problem only involves two circles, which means we do not need complicated optimization or search structures. A constant time geometric formula is enough.

The tricky part is understanding what it means for a point to be within distance `r` from a circle. Many incorrect solutions treat the whole disk as the target instead of only the circumference.

Consider this example:

```
0 0 5
20 0 5
```

The centers are 20 units apart. The closest points of the circles are 10 units apart, so the optimal radar radius is `5`.

A careless solution might think the answer is half the distance between centers, which gives `10`, but the radar only needs to touch the circumferences, not the centers.

Another important case happens when one circle lies inside the other:

```
0 0 10
1 0 1
```

The smaller circle is completely inside the larger one. The optimal radar can sit at the common center `(0,0)`. Its distance to the large circumference is `10`, and to the small circumference is `1`, so the answer is `10`.

A naive formula like `(d + r1 + r2) / 2` would produce `(1 + 10 + 1)/2 = 6`, which is impossible because any point detecting the outer circle needs radius at least `10`.

The most subtle case is when the circles intersect:

```
0 0 5
6 0 5
```

The circumferences already share points. We can place the radar at an intersection point and use radius `0`.

Any approach that assumes the answer must always be positive would fail here.

## Approaches

A brute force approach would try many candidate radar positions and compute the smallest radius needed from each one.

For a fixed point `P`, the minimum distance to a circle with center `C` and radius `R` is:

```
|PC - R|
```

This works because every point on the circumference is exactly distance `R` from the center. If `P` lies outside the circle, the closest boundary point is along the segment toward the center. If `P` lies inside, the closest boundary point is outward along the radius.

So the required radar radius at point `P` is:

```
max(|PC1 - R1|, |PC2 - R2|)
```

The brute force idea is correct, but the plane contains infinitely many points. Even discretizing the plane finely enough would be far too slow and numerically unstable.

The key observation is that this is really a one-dimensional optimization problem.

Suppose the radar center is at point `P`. Let:

```
a = distance(P, C1)
b = distance(P, C2)
d = distance(C1, C2)
```

By the triangle inequality:

```
|a - b| ≤ d
```

The required radius is:

```
max(|a - R1|, |b - R2|)
```

We want to minimize this value.

The important geometric fact is that an optimal point always lies on the line connecting the two centers. Once we move onto that line, the distances become easy to express.

Let the radar be placed on the line, between or beyond the centers. If its distance from `C1` is `x`, then its distance from `C2` is `|d - x|`.

Now the problem becomes minimizing:

```
max(|x - R1|, ||d - x| - R2|)
```

Instead of solving this with calculus, we can reason geometrically.

The closest possible distance between points on the two circumferences is:

```
gap = max(0, d - R1 - R2, R1 - d - R2, R2 - d - R1)
```

This expression covers all configurations:

If the circles overlap or touch, the gap is `0`.

If they are disjoint externally, the gap is `d - R1 - R2`.

If one lies completely inside the other, the gap is the difference between the larger radius and `(d + smaller radius)`.

Once we know the minimum distance between the two circumferences, the radar only needs to cover half of that gap, because we can place it midway between the two closest circumference points.

So the answer is:

```
gap / 2
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Impossible to bound meaningfully | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the centers and radii of the two circles.
2. Compute the Euclidean distance `d` between the centers.
3. Determine how far apart the circumferences are.

There are three geometric configurations.

If the circles are externally disjoint, the gap is:

```
d - r1 - r2
```

If one circle lies completely inside the other, the gap is:

```
max(r1, r2) - d - min(r1, r2)
```

If the circles intersect or touch, the gap is `0`.
4. Combine all cases into one formula:

```
gap = max(0, d - r1 - r2, r1 - d - r2, r2 - d - r1)
```
5. The optimal radar radius is half of this gap.

The radar can always be placed at the midpoint of the shortest segment connecting the two circumferences.
6. Print `gap / 2`.

### Why it works

Let `A` and `B` be the closest pair of points, one on each circumference. Their distance is exactly `gap`.

Any radar that detects both circles must be within radius `r` of both `A` and `B`. By triangle inequality, that requires:

```
2r ≥ distance(A, B) = gap
```

So every valid radar satisfies:

```
r ≥ gap / 2
```

Now place the radar at the midpoint of segment `AB`. Its distance to both `A` and `B` is exactly `gap / 2`, so it detects both circles with radius `gap / 2`.

Since we constructed a solution matching the lower bound, the value is optimal.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

x1, y1, r1 = map(float, input().split())
x2, y2, r2 = map(float, input().split())

d = math.hypot(x1 - x2, y1 - y2)

gap = max(
    0.0,
    d - r1 - r2,
    r1 - d - r2,
    r2 - d - r1
)

print(gap / 2.0)
```

The first part reads the two circles and computes the distance between their centers using `math.hypot`, which avoids manual squaring and square roots.

The variable `gap` stores the minimum possible distance between points on the two circumferences.

The expression:

```
d - r1 - r2
```

handles externally separated circles.

The expression:

```
r1 - d - r2
```

means circle 2 lies completely inside circle 1 with remaining clearance.

The symmetric expression handles the opposite containment case.

If none of these quantities are positive, the circles overlap or touch, so the minimum gap is zero.

Finally, the answer is half the gap because the radar can stand at the midpoint between the closest circumference points.

Floating point precision is sufficient because the required error tolerance is `1e-6`.

## Worked Examples

### Sample 1

Input:

```
0 0 1
6 0 3
```

The center distance is:

```
d = 6
```

| Variable | Value |
| --- | --- |
| r1 | 1 |
| r2 | 3 |
| d | 6 |
| d - r1 - r2 | 2 |
| r1 - d - r2 | -8 |
| r2 - d - r1 | -4 |
| gap | 2 |
| answer | 1 |

The circles are externally disjoint. Their closest points are 2 units apart, so the radar only needs radius 1 by standing midway between them.

### Example 2

Input:

```
0 0 5
6 0 5
```

| Variable | Value |
| --- | --- |
| r1 | 5 |
| r2 | 5 |
| d | 6 |
| d - r1 - r2 | -4 |
| r1 - d - r2 | -6 |
| r2 - d - r1 | -6 |
| gap | 0 |
| answer | 0 |

The circles overlap. Since the circumferences intersect, we can place the radar directly on an intersection point and use radius 0.

### Example 3

Input:

```
0 0 10
1 0 1
```

| Variable | Value |
| --- | --- |
| r1 | 10 |
| r2 | 1 |
| d | 1 |
| d - r1 - r2 | -10 |
| r1 - d - r2 | 8 |
| r2 - d - r1 | -10 |
| gap | 8 |
| answer | 4 |

The smaller circle lies completely inside the larger one. The closest boundary points are still 8 units apart, so the radar needs radius 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations |
| Space | O(1) | No extra memory proportional to input size |

The problem contains only two circles, so a direct geometric formula is enough. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    x1, y1, r1 = map(float, input().split())
    x2, y2, r2 = map(float, input().split())

    d = math.hypot(x1 - x2, y1 - y2)

    gap = max(
        0.0,
        d - r1 - r2,
        r1 - d - r2,
        r2 - d - r1
    )

    print(gap / 2.0)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert abs(float(run("0 0 1\n6 0 3\n")) - 1.0) < 1e-9

# intersecting circles
assert abs(float(run("0 0 5\n6 0 5\n")) - 0.0) < 1e-9

# one circle inside another
assert abs(float(run("0 0 10\n1 0 1\n")) - 4.0) < 1e-9

# externally tangent circles
assert abs(float(run("0 0 2\n4 0 2\n")) - 0.0) < 1e-9

# large coordinates
assert abs(float(run("10000 10000 1\n-10000 -10000 1\n")) - (math.hypot(20000, 20000) - 2) / 2) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 5 / 6 0 5` | `0` | Overlapping circles |
| `0 0 10 / 1 0 1` | `4` | Containment case |
| `0 0 2 / 4 0 2` | `0` | Exact tangency |
| Large coordinates | Correct floating result | Numerical stability |

## Edge Cases

Consider externally tangent circles:

```
0 0 2
4 0 2
```

The center distance is `4`, exactly equal to `r1 + r2`.

The algorithm computes:

```
d - r1 - r2 = 0
```

All other expressions are negative, so `gap = 0`.

The answer becomes `0`, which is correct because the circumferences touch at one point.

Now consider strict containment:

```
0 0 8
1 0 2
```

The center distance is `1`.

The algorithm computes:

```
r1 - d - r2 = 5
```

This means the closest points on the circumferences are still 5 units apart. The answer is `2.5`.

A naive solution using only external separation would incorrectly produce `0`.

Finally, consider intersecting circles:

```
0 0 5
8 0 5
```

The center distance is `8`, while `r1 + r2 = 10`.

All three gap expressions are negative, so the gap becomes `0`.

The circles intersect, so placing the radar at an intersection point gives radius `0`.
