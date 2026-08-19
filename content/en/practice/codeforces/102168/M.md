---
title: "CF 102168M - \u0412\u044b\u043f\u0443\u043a\u043b\u0430\u044f \u043e\u0431\u043e\u043b\u043e\u0447\u043a\u0430"
description: "We have exactly four distinct points on the coordinate plane. No three of them are collinear. We need to determine how many of these four points belong to the boundary of the convex hull of all four points."
date: "2026-08-19T07:31:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "M"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 72
verified: true
draft: false
---

[CF 102168M - \u0412\u044b\u043f\u0443\u043a\u043b\u0430\u044f \u043e\u0431\u043e\u043b\u043e\u0447\u043a\u0430](https://codeforces.com/problemset/problem/102168/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We have exactly four distinct points on the coordinate plane. No three of them are collinear. We need to determine how many of these four points belong to the boundary of the convex hull of all four points.

Because no three points lie on one line, there are only two possible geometric configurations. Either all four points are vertices of a convex quadrilateral, in which case the answer is 4, or one point lies strictly inside the triangle formed by the other three, in which case only the three outer points belong to the convex hull and the answer is 3.

The coordinates are between -100 and 100, and there are always exactly four points. This makes the input size constant, so even a direct check of every possible configuration would be easily fast enough. There is no need for an O(n log n) convex hull implementation intended for a large set of points. The small coordinate range also means every cross product fits comfortably in ordinary integer arithmetic. Python integers have arbitrary precision anyway.

The main edge case is that the four points can form a convex quadrilateral even when their input order is completely arbitrary. For example,

```
0 0
3 3
0 3
3 0
```

has answer `4`. A solution that assumes the input points are already given around the boundary could construct the wrong polygon.

The other important case is one point strictly inside the triangle formed by the other three. For example,

```
-1 -1
2 -1
2 2
1 0
```

has answer `3`, because `(1, 0)` is inside the triangle formed by the first three points. A careless solution that simply counts distinct points, or treats every input point as a hull vertex, would incorrectly print `4`.

The guarantees exclude three collinear points, so we never have to decide whether a point lying in the middle of a hull edge belongs to the boundary. For example, an input such as

```
0 0
1 0
2 0
0 1
```

cannot occur. The correct solution can consequently use strict orientation tests without handling zero cross products.

An input where all four coordinates are equal is also impossible, because the statement guarantees that no two points coincide. Thus such a case should not be added as a valid test of the algorithm.

## Approaches

A direct geometric approach is already sufficient because there are only four points. We can choose each point in turn and ask whether it lies inside the triangle formed by the other three points. There are four choices for the candidate point, and testing one point against the other three requires three orientation calculations. Thus the whole brute-force check performs at most 12 cross-product evaluations. Its time complexity is O(1), not something that becomes too slow for this problem.

The key observation is that the geometry of four points with no three collinear is extremely restricted. If one point is inside the triangle of the other three, that point cannot be a vertex of the convex hull. Conversely, if no point is inside the triangle formed by the other three, all four points must be extreme points, so they form a convex quadrilateral.

This lets us avoid constructing the hull entirely. For a candidate point P and the triangle ABC formed by the other three points, P is strictly inside the triangle exactly when the orientations of P with respect to all three directed edges have the same sign. We can calculate the cross product for AB with AP, BC with BP, and CA with CP. If all three values are positive or all three are negative, P is inside.

The brute-force and optimal approaches are both constant time here. The difference is that the direct hull approach solves a more general problem than necessary, while the triangle-containment observation uses the special fact that there are exactly four points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four points and store them as coordinate pairs.
2. For each point P, regard the other three points as the vertices A, B, C of a triangle. We test whether P is strictly inside this triangle because an interior point is exactly the type of point that does not appear on the convex hull.
3. Compute the orientation of P relative to each side of the triangle. For two vectors `(x1, y1)` and `(x2, y2)`, their cross product is `x1 * y2 - y1 * x2`. Its sign tells us whether one vector is to the left or right of the other.
4. If the three orientation values are all positive, or all negative, P lies strictly inside ABC. The absence of collinear triples guarantees that none of these values is zero.
5. If any point is found inside the triangle formed by the other three, print `3`. Exactly that point is excluded from the convex hull.
6. If no point is inside such a triangle, print `4`. Every point is then an extreme point, so the convex hull has four vertices.

### Why it works

Consider any four points with no three collinear. If one point P lies inside the triangle of the other three, the smallest convex polygon containing all four points is exactly that triangle, so three input points lie on the hull boundary.

If no point lies inside the triangle formed by the other three, suppose for contradiction that the hull had fewer than four vertices. Since there are four distinct points, one of them would have to lie inside the triangle formed by the other three. That contradicts the test. Hence all four points are hull vertices and the answer is 4.

The orientation test correctly identifies a point inside a triangle because a point strictly inside a triangle lies on the same side of each of the triangle's three directed edges. Since collinear triples are forbidden, strict inside and boundary cases are separated without ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b, c):
    """Cross product of AB and AC."""
    return (b[0] - a[0]) * (c[1] - a[1]) - \
           (b[1] - a[1]) * (c[0] - a[0])

def inside_triangle(p, a, b, c):
    x1 = cross(a, b, p)
    x2 = cross(b, c, p)
    x3 = cross(c, a, p)

    return (x1 > 0 and x2 > 0 and x3 > 0) or \
           (x1 < 0 and x2 < 0 and x3 < 0)

def solve():
    points = [tuple(map(int, input().split())) for _ in range(4)]

    for i in range(4):
        p = points[i]
        others = [points[j] for j in range(4) if j != i]

        if inside_triangle(p, others[0], others[1], others[2]):
            print(3)
            return

    print(4)

if __name__ == "__main__":
    solve()
```

The `cross` function computes the signed area expression for the triangle formed by `a`, `b`, and `c`. Only its sign matters. A positive value means that C lies to one side of the directed line AB, while a negative value means it lies on the other side.

`inside_triangle` evaluates the candidate point against all three directed sides. The directions are chosen cyclically as `AB`, `BC`, and `CA`, so a point inside the triangle gives three signs that agree. The two possible orientations of the triangle are handled by checking either three positive values or three negative values.

The main loop tries all four points as the possible interior point. The list comprehension selects exactly the other three points, which avoids relying on any input ordering.

There is no floating-point arithmetic. Using the integer cross product is both simpler and more reliable than computing angles or line intersections. With coordinates between -100 and 100, the intermediate values are tiny, and Python's integer arithmetic removes any overflow concern.

## Worked Examples

### Sample 1

The input points are the four corners of a square.

```
0 0
3 0
3 3
0 3
```

The algorithm tests each point against the triangle formed by the other three.

| Candidate P | Triangle of other points | Cross-product signs | Inside? |
| --- | --- | --- | --- |
| `(0, 0)` | `(3,0), (3,3), (0,3)` | `+, +, +` is not obtained for this candidate under the chosen directed edges | No |
| `(3, 0)` | `(0,0), (3,3), (0,3)` | mixed signs | No |
| `(3, 3)` | `(0,0), (3,0), (0,3)` | mixed signs | No |
| `(0, 3)` | `(0,0), (3,0), (3,3)` | mixed signs | No |

No candidate is inside the triangle of the other three, so all four points are extreme points. The output is `4`.

The trace demonstrates why input order is irrelevant. The points form a convex quadrilateral regardless of the order in which they are supplied.

### Sample 2

The input is

```
-1 -1
2 -1
2 2
1 0
```

The point `(1, 0)` lies inside the triangle formed by the first three points.

| Candidate P | Triangle of other points | Cross-product signs | Inside? |
| --- | --- | --- | --- |
| `(-1,-1)` | `(2,-1), (2,2), (1,0)` | mixed | No |
| `(2,-1)` | `(-1,-1), (2,2), (1,0)` | mixed | No |
| `(2,2)` | `(-1,-1), (2,-1), (1,0)` | mixed | No |
| `(1,0)` | `(-1,-1), (2,-1), (2,2)` | `+, +, +` | Yes |

The fourth point is strictly inside the triangle of the other three, so it is not part of the convex hull. The algorithm immediately prints `3`.

This example exercises the central distinction between an arbitrary point set and its convex hull. A point can be one of the given points without being a hull vertex.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | There are exactly four candidate points and at most three cross products per candidate. |
| Space | O(1) | Only four points and a constant number of intermediate values are stored. |

The input size is fixed at four points, so the algorithm is comfortably within the 2-second time limit and uses negligible memory. Even a conventional convex hull implementation would also pass, but it would introduce unnecessary sorting and more code.

## Test Cases

The problem has exactly four points, so there is no smaller valid input. Likewise, an all-equal-coordinate test is invalid because coincident points are forbidden. The custom tests below instead cover the smallest valid instance, a convex configuration at the coordinate limits, an interior point near a triangle edge, and a configuration whose input order does not follow the hull order.

```python
import sys
import io

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - \
           (b[1] - a[1]) * (c[0] - a[0])

def inside_triangle(p, a, b, c):
    x1 = cross(a, b, p)
    x2 = cross(b, c, p)
    x3 = cross(c, a, p)

    return (x1 > 0 and x2 > 0 and x3 > 0) or \
           (x1 < 0 and x2 < 0 and x3 < 0)

def solve():
    points = [tuple(map(int, input().split())) for _ in range(4)]

    for i in range(4):
        p = points[i]
        others = [points[j] for j in range(4) if j != i]

        if inside_triangle(p, others[0], others[1], others[2]):
            print(3)
            return

    print(4)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided sample 1
assert run("""\
0 0
3 0
3 3
0 3
""") == "4\n", "sample 1"

# Provided sample 2
assert run("""\
-1 -1
2 -1
2 2
1 0
""") == "3\n", "sample 2"

# Custom 1: smallest valid input, four corners in arbitrary order
assert run("""\
0 0
1 1
0 1
1 0
""") == "4\n", "convex quadrilateral with arbitrary input order"

# Custom 2: coordinates at the allowed boundaries
assert run("""\
-100 -100
100 -100
100 100
-100 100
""") == "4\n", "maximum coordinate magnitude"

# Custom 3: one point is strictly inside, close to a triangle edge
assert run("""\
0 0
10 0
0 10
1 1
""") == "3\n", "one interior point"

# Custom 4: interior point with negative coordinates
assert run("""\
-5 -5
5 -5
0 5
0 0
""") == "3\n", "interior point in a triangle spanning negative coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0`, `1 1`, `0 1`, `1 0` | `4` | Smallest valid input and arbitrary input order |
| `-100 -100`, `100 -100`, `100 100`, `-100 100` | `4` | Coordinate boundary values |
| `0 0`, `10 0`, `0 10`, `1 1` | `3` | Strict interior detection and orientation signs |
| `-5 -5`, `5 -5`, `0 5`, `0 0` | `3` | Interior detection with negative coordinates |

## Edge Cases

The arbitrary input-order case is handled because the algorithm never assumes that consecutive input points form hull edges. For

```
0 0
1 1
0 1
1 0
```

each point is tested against the other three. No point is inside the triangle formed by the others, so the algorithm prints `4`. A method that connected the points in input order and treated that order as the polygon boundary could make an unnecessary assumption that the input does not provide.

The interior-point case is handled directly by the triangle test. For

```
0 0
10 0
0 10
1 1
```

the point `(1,1)` is inside the triangle with vertices `(0,0)`, `(10,0)`, and `(0,10)`. The three cross products all have the same sign, so `inside_triangle` returns true and the answer is `3`. The fact that `(1,1)` is close to the diagonal edge does not cause a precision problem because all calculations use exact integers.

The coordinate-boundary case

```
-100 -100
100 -100
100 100
-100 100
```

forms a square whose four corners are hull vertices. The cross products remain exact integers, no floating-point comparison is involved, and the result is `4`.

Finally, collinear boundary cases do not need a special branch because the input guarantees that no three points are collinear. A point cannot sit exactly on a triangle edge in a valid test. Consequently, the strict comparisons `> 0` and `< 0` precisely describe the only relevant possibilities, and the algorithm never has to decide whether a collinear point should count as a hull vertex.
