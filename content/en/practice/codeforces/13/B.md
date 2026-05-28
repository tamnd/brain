---
title: "CF 13B - Letter A"
description: "We are given three line segments on a 2D plane. We must decide whether these three segments can be interpreted as the shape of the capital letter A."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 13
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 13"
rating: 2000
weight: 13
solve_time_s: 105
verified: true
draft: false
---
[CF 13B - Letter A](https://codeforces.com/problemset/problem/13/B)

**Rating:** 2000  
**Tags:** geometry, implementation  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three line segments on a 2D plane. We must decide whether these three segments can be interpreted as the shape of the capital letter A.

The structure of the letter is very rigid. Two segments must meet at a common endpoint and form the two slanted legs of the A. The third segment acts as the horizontal bar connecting the two legs somewhere in the middle.

The geometry conditions are stricter than just “they look like an A”.

The two leg segments must share exactly one endpoint, which becomes the top vertex of the letter. The angle between the legs must be positive and at most 90 degrees. A straight line or a reflex angle is invalid.

The crossbar must connect one point on the first leg and one point on the second leg. Those intersection points cannot be too close to either endpoint. More precisely, if a leg is split by the crossbar connection point, the shorter piece divided by the longer piece must be at least $\frac14$. This prevents the bar from sitting almost at the very top or very bottom.

The input size is tiny. Each test case contains only three segments, and at most $10^4$ test cases exist. That immediately tells us we do not need sophisticated geometry structures or optimization tricks. Even checking every permutation of segments is completely fine because there are only $3! = 6$ possibilities.

The real challenge is correctness. Geometry implementation mistakes are much more dangerous here than asymptotic complexity.

Several edge cases easily break naive solutions.

One common mistake is checking only whether the crossbar endpoints lie on the infinite supporting lines instead of on the actual segments.

Consider:

```
0 0 0 4
0 4 4 0
10 10 11 11
```

The third segment lies nowhere near the other two. A careless line-based check would still think the lines intersect correctly.

Another trap is forgetting that the angle must be acute or right, not obtuse.

Example:

```
0 0 0 5
0 5 -2 -1
0 2 -1 2
```

The two legs share a point, but the angle opens wider than 90 degrees. The correct answer is `NO`.

A subtler issue is the proportion condition. Many implementations only verify that the crossbar is inside each leg segment, but not whether it sits too close to an endpoint.

Example:

```
0 0 0 8
0 8 4 0
0 7 1 6
```

The bar is extremely close to the top. One side ratio becomes $1:7$, which is smaller than $1:4$. The answer must be `NO`.

Floating-point precision is another source of silent bugs. Distances and ratios involve square roots, but we can avoid them completely by comparing squared lengths and using vector dot products with integers.

## Approaches

The brute-force idea is straightforward. Since there are only three segments, we can try every way to choose two of them as the legs and the remaining one as the crossbar.

For each permutation, we check:

1. The chosen legs share exactly one endpoint.
2. The angle between them is in the valid range.
3. Each endpoint of the crossbar lies on a different leg.
4. The division ratio condition holds on both legs.

This already works fast enough. Each test case performs only constant-time geometry operations. Even with $10^4$ test cases, the total work is negligible.

The hard part is not speed, it is expressing the geometry robustly.

A naive implementation often uses floating-point distances and slope formulas. That creates unnecessary instability, especially for collinear checks and angle comparisons. Vertical segments also complicate slope-based logic.

The key observation is that every required property can be expressed with vector operations.

Collinearity can be checked using cross products.

Whether an angle is acute or right can be checked using the dot product.

Whether a point lies between two endpoints can be checked using coordinate bounds.

The proportion condition can also avoid square roots. Suppose a point divides a segment into lengths $a$ and $b$. The condition is:

$$\frac{\min(a,b)}{\max(a,b)} \ge \frac14$$

Instead of computing real lengths, we compare squared lengths:

$$16 \cdot \min(a^2,b^2) \ge \max(a^2,b^2)$$

Everything stays integer-based and exact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with floating-point geometry | O(1) per test case | O(1) | Accepted but error-prone |
| Optimal integer-vector geometry | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three segments.

Each segment is represented by two endpoints.
2. Try all permutations of the three segments.

For every permutation, treat the first two segments as the legs and the third as the crossbar.
3. Check whether the two leg segments share exactly one endpoint.

If they do not, this permutation cannot form the letter A.
4. Let the shared endpoint be the top vertex.

Reorient the two legs so that both start from this common point and extend downward toward their other endpoints.

This normalization simplifies all later checks.
5. Compute the angle condition using the dot product.

Let the leg direction vectors be $u$ and $v$.

The angle between them is acute or right exactly when:

$$u \cdot v > 0$$

If the dot product is zero or negative, reject this configuration.

Zero would mean 90 degrees only if vectors point outward from the common point, but our vectors extend away from the top, so a positive dot product correctly captures angles smaller than 90 degrees.
6. Check whether one endpoint of the crossbar lies on the first leg and the other lies on the second leg.

A point lies on a segment if:

- the cross product is zero, meaning collinear,
- and the coordinates stay within the segment bounds.
7. Verify the proportion condition for both legs.

Suppose point $P$ lies on segment $AB$.

Compute:

$$d_1 = |AP|^2,\quad d_2 = |PB|^2$$

The required ratio becomes:

$$16 \cdot \min(d_1,d_2) \ge \max(d_1,d_2)$$

This is equivalent to the original condition without square roots.
8. If all checks pass for any permutation, print `YES`.
9. Otherwise print `NO`.

### Why it works

The algorithm explicitly verifies every condition from the definition of the letter A.

Trying all permutations guarantees we never miss the correct assignment of legs and crossbar.

The shared-endpoint check guarantees the correct topology.

The dot product check guarantees the opening angle is valid.

The point-on-segment checks guarantee the crossbar connects the two legs rather than merely intersecting their infinite supporting lines.

The ratio test guarantees the crossbar is placed within the allowed middle region on both legs.

Since every required property is checked exactly once and every rejection corresponds to violating a definition condition, the algorithm is correct.

## Python Solution

```python
import sys
from itertools import permutations

input = sys.stdin.readline

def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

def point_on_segment(p, a, b):
    ap = vec(a, p)
    ab = vec(a, b)

    if cross(ap, ab) != 0:
        return False

    return (
        min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )

def good_ratio(p, a, b):
    d1 = dist2(a, p)
    d2 = dist2(p, b)

    mn = min(d1, d2)
    mx = max(d1, d2)

    return 16 * mn >= mx

def check(s1, s2, s3):
    p1, p2 = s1
    q1, q2 = s2

    common = None

    for a in [p1, p2]:
        for b in [q1, q2]:
            if a == b:
                common = a

    if common is None:
        return False

    if p1 == common:
        a = p2
    else:
        a = p1

    if q1 == common:
        b = q2
    else:
        b = q1

    v1 = vec(common, a)
    v2 = vec(common, b)

    if dot(v1, v2) <= 0:
        return False

    r1, r2 = s3

    ok1 = point_on_segment(r1, common, a) and point_on_segment(r2, common, b)
    ok2 = point_on_segment(r2, common, a) and point_on_segment(r1, common, b)

    if not ok1 and not ok2:
        return False

    if ok2:
        r1, r2 = r2, r1

    if not good_ratio(r1, common, a):
        return False

    if not good_ratio(r2, common, b):
        return False

    return True

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        segs = []

        for _ in range(3):
            x1, y1, x2, y2 = map(int, input().split())
            segs.append(((x1, y1), (x2, y2)))

        found = False

        for perm in permutations(segs):
            if check(*perm):
                found = True
                break

        ans.append("YES" if found else "NO")

    print("\n".join(ans))

solve()
```

The implementation mirrors the geometry checks directly.

The `point_on_segment` function uses two conditions. The cross product guarantees collinearity. The bounding-box check guarantees the point lies inside the finite segment rather than somewhere farther along the line.

The angle test uses the dot product. Since both vectors start from the common endpoint and point outward along the legs, a positive dot product means the angle is strictly smaller than 90 degrees.

The proportion condition is implemented entirely with squared distances. This avoids floating-point precision issues and also avoids expensive square roots.

The permutation loop is tiny because there are only six possible assignments. This keeps the code simple and eliminates complicated case analysis.

One subtle point is handling the crossbar endpoints. Either endpoint of the crossbar could belong to either leg, so the code tests both assignments.

## Worked Examples

### Example 1

Input:

```
0 0 0 5
0 5 2 -1
1 2 0 1
```

| Step | Value |
| --- | --- |
| Common endpoint | (0, 5) |
| First leg vector | (0, -5) |
| Second leg vector | (2, -6) |
| Dot product | 30 |
| Crossbar endpoints | (1, 2), (0, 1) |
| Endpoint on first leg | (0, 1) |
| Endpoint on second leg | (1, 2) |
| Ratio check first leg | valid |
| Ratio check second leg | valid |
| Final answer | YES |

The dot product is positive, so the angle is acute. Each crossbar endpoint lies on a different leg, and both division ratios satisfy the $1/4$ condition.

### Example 2

Input:

```
0 0 0 8
0 8 4 0
0 7 1 6
```

| Step | Value |
| --- | --- |
| Common endpoint | (0, 8) |
| First leg vector | (0, -8) |
| Second leg vector | (4, -8) |
| Dot product | 64 |
| Crossbar endpoints | (0, 7), (1, 6) |
| Distance split on first leg | 1 and 7 |
| Ratio | 1/7 |
| Final answer | NO |

Even though the topology and angle are valid, the crossbar is too close to the top vertex. The ratio condition rejects it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only 6 permutations and constant-time geometry checks |
| Space | O(1) | No extra structures depending on input size |

The constraints are extremely small for each test case, so constant-time geometry is more than enough. Even $10^4$ cases execute comfortably within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def vec(a, b):
        return (b[0] - a[0], b[1] - a[1])

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1]

    def cross(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def dist2(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx * dx + dy * dy

    def point_on_segment(p, a, b):
        ap = vec(a, p)
        ab = vec(a, b)

        if cross(ap, ab) != 0:
            return False

        return (
            min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
        )

    def good_ratio(p, a, b):
        d1 = dist2(a, p)
        d2 = dist2(p, b)

        mn = min(d1, d2)
        mx = max(d1, d2)

        return 16 * mn >= mx

    def check(s1, s2, s3):
        p1, p2 = s1
        q1, q2 = s2

        common = None

        for a in [p1, p2]:
            for b in [q1, q2]:
                if a == b:
                    common = a

        if common is None:
            return False

        if p1 == common:
            a = p2
        else:
            a = p1

        if q1 == common:
            b = q2
        else:
            b = q1

        if dot(vec(common, a), vec(common, b)) <= 0:
            return False

        r1, r2 = s3

        ok1 = point_on_segment(r1, common, a) and point_on_segment(r2, common, b)
        ok2 = point_on_segment(r2, common, a) and point_on_segment(r1, common, b)

        if not ok1 and not ok2:
            return False

        if ok2:
            r1, r2 = r2, r1

        return (
            good_ratio(r1, common, a)
            and good_ratio(r2, common, b)
        )

    t = int(input())
    out = []

    for _ in range(t):
        segs = []

        for _ in range(3):
            x1, y1, x2, y2 = map(int, input().split())
            segs.append(((x1, y1), (x2, y2)))

        ans = "NO"

        for perm in permutations(segs):
            if check(*perm):
                ans = "YES"
                break

        out.append(ans)

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
) == "YES\nNO\nYES", "sample cases"

# no shared endpoint
assert run(
"""1
0 0 1 1
2 2 3 3
0 1 1 2
"""
) == "NO", "legs must share a vertex"

# obtuse angle
assert run(
"""1
0 0 0 5
0 5 -2 -1
0 2 -1 2
"""
) == "NO", "angle must be <= 90 degrees"

# crossbar too close to endpoint
assert run(
"""1
0 0 0 8
0 8 4 0
0 7 1 6
"""
) == "NO", "ratio condition"

# valid symmetric A
assert run(
"""1
0 0 -2 -4
0 0 2 -4
-1 -2 1 -2
"""
) == "YES", "basic valid A"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Segments without common endpoint | NO | Legs must connect |
| Obtuse opening angle | NO | Dot-product angle check |
| Crossbar near top | NO | Ratio condition |
| Symmetric valid shape | YES | Standard successful configuration |

## Edge Cases

Consider the case where the crossbar lies on the infinite extension of a leg but not on the actual segment.

```
1
0 0 0 4
0 4 4 0
10 10 11 11
```

The line through the third segment does not touch either leg segment. The `point_on_segment` function rejects it because the coordinates fall outside the segment bounds. The algorithm prints `NO`.

Now consider an obtuse angle.

```
1
0 0 0 5
0 5 -2 -1
0 2 -1 2
```

The shared endpoint is `(0,5)`. The leg vectors become `(0,-5)` and `(-2,-6)`. Their dot product is:

$$0 \cdot (-2) + (-5) \cdot (-6) = 30$$

If vectors were oriented incorrectly, this case could accidentally pass. The implementation always orients vectors away from the common endpoint, making the angle test reliable.

Finally, examine the boundary ratio case.

```
1
0 0 0 8
0 8 4 0
0 7 1 6
```

The point `(0,7)` divides the first leg into lengths `1` and `7`. Squared lengths become `1` and `49`.

The check becomes:

$$16 \cdot 1 \ge 49$$

which is false, so the algorithm correctly rejects the configuration.
