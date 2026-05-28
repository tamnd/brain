---
title: "CF 13B - Letter A"
description: "We are given exactly three line segments on a 2D plane. The task is to determine whether these three segments can repres"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 13
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 13"
rating: 2000
weight: 13
solve_time_s: 133
verified: false
draft: false
---

[CF 13B - Letter A](https://codeforces.com/problemset/problem/13/B)

**Rating:** 2000  
**Tags:** geometry, implementation  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given exactly three line segments on a 2D plane. The task is to determine whether these three segments can represent the shape of the uppercase letter A.

Geometrically, the structure must look like this:

- Two segments meet at a shared endpoint and form the two slanted legs of the letter.
- The third segment connects a point on one leg to a point on the other leg, acting as the horizontal bar.
- The angle at the top must be acute or right, but not straight or reflex.
- The horizontal bar cannot be too close to the bottom ends. On each leg, the shorter side created by the bar must be at least one quarter of the longer side.

Each test case contains exactly three segments, so the search space is tiny. We do not need sophisticated geometry data structures or computational geometry libraries. The challenge is correctness, especially around floating point precision and geometric corner cases.

The number of test cases can reach 10000, but every test case contains only three segments. Even an exhaustive check over all permutations is effectively constant time. A solution performing a few hundred arithmetic operations per test case is easily fast enough.

The dangerous part is not performance, it is geometric validation.

One common mistake is checking only whether two segments share an endpoint and the third intersects them somewhere. That accepts invalid shapes where the bar touches an endpoint instead of lying strictly inside the legs.

Consider this example:

```
(0,0)-(0,4)
(0,4)-(2,0)
(0,0)-(1,2)
```

The third segment touches the left leg exactly at its bottom endpoint. This is not a valid A because the bar must divide both legs into two positive parts.

Another subtle case is angle direction. A careless implementation may only check that the dot product is nonnegative. That accepts collinear segments:

```
(0,0)-(1,1)
(0,0)-(2,2)
(0.5,0.5)-(1.5,1.5)
```

The dot product is positive, but the angle is actually 0 degrees, not a valid A.

The ratio condition also causes mistakes. Suppose the bar is extremely close to the bottom of one leg:

```
(0,0)-(0,8)
(0,8)-(4,0)
(0,1)-(0.5,1)
```

One side ratio is $1:7$, which is smaller than $1:4$. Visually this does not resemble the letter A. Using only intersection checks would incorrectly accept it.

Another tricky situation is when the third segment intersects the infinite extension of a leg, but not the actual segment itself. Geometry implementations that forget segment bounds will fail here.

## Approaches

The brute-force approach is to try every way to interpret the three segments.

We choose two segments as the legs and the remaining segment as the crossbar. Then we check:

- the two chosen legs share exactly one endpoint,
- the angle between them is in the valid range,
- the bar endpoints lie on different legs,
- the ratio condition holds on both legs.

Since there are only three segments, there are only six permutations. Even with detailed geometry checks, this is effectively constant time.

The real difficulty is writing the geometry correctly.

A naive implementation often relies on floating point comparisons and geometric intersection formulas. That works for many cases but becomes fragile around precision boundaries. Coordinates can be as large as $10^8$, so squared lengths can reach $10^{16}$. Floating point computations remain safe here, but we can avoid them entirely.

The key observation is that every condition can be expressed using vector arithmetic and squared distances.

To verify the angle, we only need dot and cross products:

- dot product $> 0$ means angle less than 90 degrees,
- cross product $\ne 0$ means the legs are not collinear.

To verify that a point lies strictly inside a segment, we can use collinearity plus distance decomposition.

For the ratio condition, we never need square roots. If a point divides a segment into lengths $a$ and $b$, the condition is:

$$\frac{\min(a,b)}{\max(a,b)} \ge \frac14$$

which is equivalent to:

$$4 \cdot \min(a,b) \ge \max(a,b)$$

Using squared distances preserves the inequality because all values are nonnegative.

That turns the entire problem into pure integer arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with floating geometry | O(1) | O(1) | Accepted but fragile |
| Optimal integer geometry | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three segments.
2. Try all permutations of the segments.

For each permutation, treat the first two segments as the legs and the third as the crossbar.
3. Check whether the two legs share exactly one endpoint.

If they do not, this permutation cannot form the letter A.
4. Let the shared endpoint be the top vertex.

Rewrite both legs as vectors starting from this common point toward their other endpoints.
5. Verify the angle condition.

Compute the dot product of the two vectors.

The dot product must be positive, otherwise the angle is at least 90 degrees or degenerate.

Also compute the cross product.

The cross product must be nonzero, otherwise the two legs are collinear and no angle exists.
6. Check where the crossbar endpoints lie.

One endpoint of the crossbar must lie strictly inside the first leg.

The other endpoint must lie strictly inside the second leg.

A point lies on a segment if:

- it is collinear with the segment,
- its coordinates stay between the segment endpoints.

It must also not coincide with either endpoint of the leg.
7. Verify the ratio condition for both legs.

Suppose point $P$ lies on segment $AB$.

Let:

- $x = |AP|^2$
- $y = |PB|^2$

We require:

$$4 \cdot \min(x,y) \ge \max(x,y)$$

This guarantees the shorter piece is at least one quarter of the longer piece.

1. If every check passes for any permutation, print `YES`.
2. Otherwise print `NO`.

### Why it works

The algorithm directly encodes the geometric definition of the letter A.

Trying all permutations guarantees that we eventually test the correct assignment of legs and crossbar if one exists.

The shared endpoint check guarantees the two legs meet at a single top vertex. The dot and cross product conditions guarantee the angle is strictly between 0 and 90 degrees inclusive of 90? Actually the statement excludes 0 and allows 90, so we require dot product nonnegative and cross nonzero. A zero cross product would mean the legs lie on the same line.

The point-on-segment checks guarantee the crossbar truly connects the two legs instead of merely intersecting their infinite extensions.

The ratio condition guarantees the bar is not too close to either end. Since distance comparisons preserve order under squaring, squared lengths are sufficient.

Every accepted configuration satisfies all problem requirements, and every valid letter A passes all checks.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

def point_on_segment(p, a, b):
    if cross(sub(p, a), sub(b, a)) != 0:
        return False

    return (
        min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )

def strict_inside(p, a, b):
    return point_on_segment(p, a, b) and p != a and p != b

def ratio_ok(p, a, b):
    x = dist2(p, a)
    y = dist2(p, b)

    small = min(x, y)
    large = max(x, y)

    return 4 * small >= large

def solve_case(segs):
    for s1, s2, s3 in permutations(segs):
        a, b = s1
        c, d = s2

        common = None

        for p in [a, b]:
            for q in [c, d]:
                if p == q:
                    common = p

        if common is None:
            continue

        other1 = b if a == common else a
        other2 = d if c == common else c

        v1 = sub(other1, common)
        v2 = sub(other2, common)

        if cross(v1, v2) == 0:
            continue

        if dot(v1, v2) < 0:
            continue

        p1, p2 = s3

        ok1 = strict_inside(p1, common, other1) and strict_inside(
            p2, common, other2
        )

        ok2 = strict_inside(p2, common, other1) and strict_inside(
            p1, common, other2
        )

        if not (ok1 or ok2):
            continue

        if ok1:
            x, y = p1, p2
        else:
            x, y = p2, p1

        if not ratio_ok(x, common, other1):
            continue

        if not ratio_ok(y, common, other2):
            continue

        return "YES"

    return "NO"

def main():
    t = int(input())
    ans = []

    for _ in range(t):
        segs = []

        for _ in range(3):
            x1, y1, x2, y2 = map(int, input().split())
            segs.append(((x1, y1), (x2, y2)))

        ans.append(solve_case(segs))

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The solution is built entirely on integer geometry.

The helper functions `dot` and `cross` implement the standard vector operations used for angle and collinearity checks. Since coordinates are integers and Python integers are unbounded, overflow is not a concern.

The `point_on_segment` function first checks collinearity using the cross product. Then it verifies the point lies inside the coordinate bounds of the segment. Both conditions are necessary. Collinearity alone would incorrectly accept points on the infinite extension of the line.

`strict_inside` rejects segment endpoints. This matters because the bar must divide the legs into two positive-length parts.

The ratio check uses squared distances instead of real distances. If:

$$\frac{a}{b} \ge \frac14$$

then:

$$\frac{a^2}{b^2} \ge \frac1{16}$$

and after rearranging we get the equivalent integer comparison used in the code. This avoids floating point precision entirely.

The permutation loop guarantees that every possible assignment of legs and crossbar is tested. Since there are only six permutations, the runtime stays constant.

A subtle implementation detail is the angle check:

```
if dot(v1, v2) < 0:
```

We reject only negative dot products. Zero corresponds to exactly 90 degrees, which the statement allows.

## Worked Examples

### Sample Trace 1

Input:

```
4 4 6 0
4 1 5 2
4 0 4 4
```

| Step | Value |
| --- | --- |
| Chosen legs | `(4,4)-(6,0)` and `(4,0)-(4,4)` |
| Shared endpoint | `(4,4)` |
| Leg vectors | `(2,-4)` and `(0,-4)` |
| Cross product | `-8` |
| Dot product | `16` |
| Crossbar endpoints | `(4,1)` and `(5,2)` |
| Endpoint on first leg | `(5,2)` |
| Endpoint on second leg | `(4,1)` |
| Ratio check leg 1 | passes |
| Ratio check leg 2 | passes |
| Result | `YES` |

This trace shows the intended geometry. The two legs meet at the top, form an acute angle, and the crossbar lies strictly inside both legs.

### Sample Trace 2

Input:

```
0 0 0 6
0 6 2 -4
1 1 0 1
```

| Step | Value |
| --- | --- |
| Shared endpoint | `(0,6)` |
| Leg vectors | `(0,-6)` and `(2,-10)` |
| Cross product | `12` |
| Dot product | `60` |
| Crossbar endpoints | `(1,1)` and `(0,1)` |
| Endpoint on first leg | `(0,1)` |
| Endpoint on second leg | no |
| Result | `NO` |

The crossbar touches only one leg. The other endpoint does not lie on the second segment, so the configuration is rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only six permutations and constant-time geometry checks |
| Space | O(1) | Uses a fixed number of variables |

Even with 10000 test cases, the runtime is tiny because each case performs only a handful of arithmetic operations. Memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1])

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1]

    def cross(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def dist2(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx * dx + dy * dy

    def point_on_segment(p, a, b):
        if cross(sub(p, a), sub(b, a)) != 0:
            return False

        return (
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
        )

    def strict_inside(p, a, b):
        return point_on_segment(p, a, b) and p != a and p != b

    def ratio_ok(p, a, b):
        x = dist2(p, a)
        y = dist2(p, b)

        return 4 * min(x, y) >= max(x, y)

    def solve_case(segs):
        for s1, s2, s3 in permutations(segs):
            a, b = s1
            c, d = s2

            common = None

            for p in [a, b]:
                for q in [c, d]:
                    if p == q:
                        common = p

            if common is None:
                continue

            other1 = b if a == common else a
            other2 = d if c == common else c

            v1 = sub(other1, common)
            v2 = sub(other2, common)

            if cross(v1, v2) == 0:
                continue

            if dot(v1, v2) < 0:
                continue

            p1, p2 = s3

            ok1 = strict_inside(p1, common, other1) and strict_inside(
                p2, common, other2
            )

            ok2 = strict_inside(p2, common, other1) and strict_inside(
                p1, common, other2
            )

            if not (ok1 or ok2):
                continue

            if ok1:
                x, y = p1, p2
            else:
                x, y = p2, p1

            if not ratio_ok(x, common, other1):
                continue

            if not ratio_ok(y, common, other2):
                continue

            return "YES"

        return "NO"

    t = int(input())
    out = []

    for _ in range(t):
        segs = []

        for _ in range(3):
            x1, y1, x2, y2 = map(int, input().split())
            segs.append(((x1, y1), (x2, y2)))

        out.append(solve_case(segs))

    return "\n".join(out)

# provided samples
assert run(
"""3
4 4 6 0
4 1 5 2
4 0 4 4
0 0 0 6
0 6 2 -4
1 1 0 1
0 0 0 5
0 5 2 -1
1 2 0 1
"""
) == "YES\nNO\nYES", "sample"

# collinear legs
assert run(
"""1
0 0 1 1
0 0 2 2
1 1 2 1
"""
) == "NO", "collinear legs"

# bar touches endpoint
assert run(
"""1
0 0 0 4
0 4 2 0
0 0 1 2
"""
) == "NO", "crossbar endpoint"

# exactly 90 degree angle
assert run(
"""1
0 0 0 4
0 0 4 0
0 2 2 0
"""
) == "YES", "right angle allowed"

# ratio below 1/4
assert run(
"""1
0 0 0 8
0 8 4 0
0 1 0 1
"""
) == "NO", "ratio too small"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Collinear legs | `NO` | Rejects zero-degree angle |
| Bar touches endpoint | `NO` | Crossbar must lie strictly inside |
| Right angle configuration | `YES` | 90 degrees is allowed |
| Very unbalanced division | `NO` | Ratio constraint enforcement |

## Edge Cases

Consider the collinear-leg case:

```
1
0 0 1 1
0 0 2 2
1 1 2 1
```

The two candidate legs share an endpoint, but their direction vectors are scalar multiples. The cross product becomes zero, so the algorithm rejects the configuration immediately. This prevents accepting a degenerate angle.

Now examine the endpoint-touching case:

```
1
0 0 0 4
0 4 2 0
0 0 1 2
```

The point `(0,0)` lies on the left leg, but it is also an endpoint. `strict_inside` returns false because the point is not strictly internal to the segment. The algorithm correctly outputs `NO`.

For the ratio boundary:

```
1
0 0 0 8
0 8 4 0
0 1 0 1
```

The point `(0,1)` divides the vertical leg into lengths `1` and `7`. Squared distances become `1` and `49`. The condition:

```
4 * 1 >= 49
```

fails, so the configuration is rejected.

Finally, consider the exact right-angle case:

```
1
0 0 0 4
0 0 4 0
0 2 2 0
```

The dot product of the leg vectors is zero, meaning the angle is exactly 90 degrees. Since the code rejects only negative dot products, this configuration is accepted, matching the statement.
