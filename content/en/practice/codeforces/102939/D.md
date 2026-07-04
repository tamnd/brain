---
title: "CF 102939D - Robot Toss"
description: "Two robots stand at two fixed lattice points on a grid. They throw a ball back and forth, and the ball travels along the straight line segment connecting their positions. A third point, Eve, is trying to intercept the ball."
date: "2026-07-04T07:46:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102939
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 01-22-21 Div. 2 (Beginner)"
rating: 0
weight: 102939
solve_time_s: 43
verified: true
draft: false
---

[CF 102939D - Robot Toss](https://codeforces.com/problemset/problem/102939/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Two robots stand at two fixed lattice points on a grid. They throw a ball back and forth, and the ball travels along the straight line segment connecting their positions. A third point, Eve, is trying to intercept the ball. Eve succeeds exactly when the straight segment from Alice to Bob passes through her position.

For each candidate position of Eve, we must decide whether that point lies on the line segment between the two robots. This is a pure geometric membership test: does a point lie exactly on a given segment in the integer grid.

The input consists of two fixed points and then up to 100 query points. Each query is independent and asks whether that point lies on the segment. Coordinates are integers in the range roughly between minus ten thousand and ten thousand, which is small enough that any constant time arithmetic per query is sufficient.

The key constraint implication is that we can afford a direct geometric check per query without any preprocessing. Even an O(E) per query approach would be too slow, but here E is at most 100, so an O(1) test per query is sufficient.

A common mistake is to only check collinearity. That is not enough. For example, if Alice is at (0, 0) and Bob is at (2, 2), then the point (3, 3) is collinear with them but clearly lies beyond Bob and should not count as intercepting the segment. Another subtle edge case is when Eve coincides with Alice or Bob. In that case, the answer should still be positive because the segment passes through that endpoint.

## Approaches

The brute force idea is to model the line segment explicitly and check whether a point lies on it. One naive way is to parameterize the segment and test whether there exists a parameter t in [0, 1] such that the point equals Alice plus t times the vector from Alice to Bob. This reduces to solving two equations and checking consistency. While correct, it introduces floating point precision issues if implemented directly, and it is unnecessary given the integer nature of the coordinates.

A more robust observation is that a point lies on the segment if and only if two conditions hold. First, the three points must be collinear, which can be tested using the cross product of vectors AB and AE. Second, the point must lie within the bounding box formed by Alice and Bob, meaning its x coordinate is between the two x coordinates and its y coordinate is between the two y coordinates.

The key simplification is that collinearity ensures the point lies on the infinite line, while the bounding box constraint restricts it to the finite segment. Together these conditions fully characterize membership on a segment in integer geometry.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Parametric line solving with floats | O(E) | O(1) | Risky due to precision |
| Cross product + bounding box check | O(E) | O(1) | Accepted |

## Algorithm Walkthrough

We treat Alice as point A, Bob as point B, and each query as point C.

1. Compute the vector from A to B by subtracting coordinates, forming (dx, dy). This defines the direction of the segment.
2. For each query point C, compute the vector from A to C, forming (cx, cy).
3. Check collinearity by evaluating the cross product dx * cy − dy * cx. If this value is not zero, C is not on the line through A and B.
4. If collinear, check whether C lies within the axis-aligned bounding box of A and B by verifying min(xa, xb) ≤ xc ≤ max(xa, xb) and similarly for y.
5. If both conditions hold, output Yes, otherwise output No.

The cross product test replaces slope comparison and avoids division entirely, which eliminates precision issues and handles vertical lines naturally.

### Why it works

The cross product condition ensures that vectors AB and AC are linearly dependent, meaning C lies on the infinite line through A and B. The bounding box restriction then removes all points that lie on the same line but outside the segment endpoints. Together, these two conditions are both necessary and sufficient for a point to lie on a closed segment in the plane.

## Python Solution

```python
import sys
input = sys.stdin.readline

xa, ya = map(int, input().split())
xb, yb = map(int, input().split())
e = int(input())

dx = xb - xa
dy = yb - ya

def on_segment(xc, yc):
    cx = xc - xa
    cy = yc - ya

    if dx * cy != dy * cx:
        return False

    if min(xa, xb) <= xc <= max(xa, xb) and min(ya, yb) <= yc <= max(ya, yb):
        return True

    return False

out = []
for _ in range(e):
    x, y = map(int, input().split())
    out.append("Yes" if on_segment(x, y) else "No")

print("\n".join(out))
```

The code starts by fixing the direction vector between the two robots. Each query is handled independently by computing its relative vector from Alice. The cross product check is the central decision point, since it encodes collinearity without division.

The bounding box check is necessary because collinearity alone would accept points extending infinitely in both directions. The min and max comparisons ensure we only accept points that lie between the endpoints.

A subtle implementation detail is that all arithmetic stays in integers, so there is no risk of floating point error. Another important detail is that equality is inclusive, so endpoints are accepted automatically.

## Worked Examples

Consider Alice at (0, 0), Bob at (2, 2), and two queries (1, 1) and (-1, -1).

For the first query:

| Step | cx, cy | Cross product dx_cy − dy_cx | Collinear | In bounding box | Result |
| --- | --- | --- | --- | --- | --- |
| (1,1) | (1,1) | 2_1 − 2_1 = 0 | Yes | Yes | Yes |

This confirms that the point lies exactly halfway along the segment.

For the second query:

| Step | cx, cy | Cross product dx_cy − dy_cx | Collinear | In bounding box | Result |
| --- | --- | --- | --- | --- | --- |
| (-1,-1) | (-1,-1) | 2*(-1) − 2*(-1) = 0 | Yes | No | No |

This point lies on the same infinite line but is outside the segment endpoints, so it is rejected by the bounding box condition.

These two cases show the necessity of both checks: collinearity alone is insufficient, and bounding box alone is meaningless without ensuring the point lies on the line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(E) | Each query is processed with a constant number of arithmetic operations |
| Space | O(1) | Only a few integer variables are stored |

The constraints allow up to 100 queries, so a constant time geometric test per query is easily fast enough. All operations are simple integer multiplications and comparisons, which run comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    data = sys.stdin.read().strip().split()
    it = iter(data)

    xa, ya = int(next(it)), int(next(it))
    xb, yb = int(next(it)), int(next(it))
    e = int(next(it))

    dx = xb - xa
    dy = yb - ya

    def ok(xc, yc):
        cx = xc - xa
        cy = yc - ya
        if dx * cy != dy * cx:
            return False
        return min(xa, xb) <= xc <= max(xa, xb) and min(ya, yb) <= yc <= max(ya, yb)

    res = []
    for _ in range(e):
        x, y = int(next(it)), int(next(it))
        res.append("Yes" if ok(x, y) else "No")

    return "\n".join(res) + ("\n" if res else "")

# sample case
assert run("""0 0
2 2
2
1 1
-1 -1
""") == "Yes\nNo\n"

# collinear but outside segment
assert run("""0 0
2 2
1
3 3
""") == "No\n"

# endpoint case
assert run("""0 0
5 0
1
0 0
""") == "Yes\n"

# vertical line
assert run("""2 0
2 5
2
2 3
3 3
""") == "Yes\nNo\n"

# horizontal line
assert run("""0 7
4 7
2
2 7
5 7
""") == "Yes\nNo\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | Yes / No | basic correctness |
| (3,3) outside segment | No | collinearity vs segment membership |
| endpoint | Yes | boundary inclusion |
| vertical line | mixed | division-free handling of dx=0 |
| horizontal line | mixed | general axis-aligned correctness |

## Edge Cases

When Eve coincides with Alice or Bob, the cross product becomes zero automatically because the vectors are identical or zero. The bounding box condition also passes since the coordinate equals one endpoint. This ensures endpoints are accepted without special handling.

For vertical or horizontal segments, one of dx or dy is zero. The cross product formulation still works because it reduces correctly without requiring division. For example, if dx is zero, the condition becomes dy * cx = 0, which forces cx to be zero, meaning x must match Alice’s x-coordinate.

For points collinear but outside the segment, such as extending beyond Bob in the same direction, the cross product passes but the bounding box rejects them. This separation is what prevents false positives and ensures the segment is treated as a finite object rather than an infinite line.
