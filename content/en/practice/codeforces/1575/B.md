---
title: "CF 1575B - Building an Amusement Park"
description: "We want to place a circular amusement park so that it touches the origin. If the park has radius $r$, then its center must lie exactly $r$ units from the origin, because the origin lies on the boundary of the park. Each bird habitat is a point in the plane."
date: "2026-06-10T10:53:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "B"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2300
weight: 1575
solve_time_s: 318
verified: false
draft: false
---

[CF 1575B - Building an Amusement Park](https://codeforces.com/problemset/problem/1575/B)

**Rating:** 2300  
**Tags:** binary search, geometry  
**Solve time:** 5m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We want to place a circular amusement park so that it touches the origin. If the park has radius $r$, then its center must lie exactly $r$ units from the origin, because the origin lies on the boundary of the park.

Each bird habitat is a point in the plane. A habitat is considered covered if it lies inside or on the boundary of the chosen circle. Among all circles that touch the origin, we need the smallest radius that allows at least $k$ habitats to be covered.

The input contains up to $10^5$ habitats. Any algorithm that compares all pairs of points or explicitly searches over all possible circle centers is immediately ruled out. Even an $O(n^2)$ procedure would require around $10^{10}$ operations in the worst case. The target complexity has to be close to $O(n \log n)$ per major phase.

The geometric constraint is the interesting part. The center is not arbitrary. For a fixed radius $r$, the center is restricted to the circle centered at the origin with radius $r$. This converts the problem into a one dimensional angular problem.

Several edge cases are easy to mishandle.

Consider a habitat at the origin:

```
1 1
0 0
```

The correct answer is $0$. When $r=0$, the only possible center is also the origin, and the habitat is covered. A decision procedure that blindly divides by $r$ would crash or produce NaNs.

Consider a habitat exactly at distance $2r$ from the origin. For example:

```
1 1
2 0
```

The minimum radius is $1$. The corresponding angular interval collapses to a single angle. Using strict inequalities instead of inclusive ones would incorrectly reject this case.

Consider intervals that cross the $0$-angle boundary. Suppose a habitat generates an interval from $350^\circ$ to $10^\circ$. Treating angles as ordinary line segments would lose the wrapped portion and undercount overlaps.

## Approaches

A brute force viewpoint is to fix a radius $r$, enumerate candidate centers, count how many habitats are covered, and then binary search on $r$. The difficulty is that the center may be any point on a continuous circle, so there are infinitely many candidates. Even if we discretized aggressively, the result would not be exact.

The key observation is that for a fixed radius $r$, the center is constrained to the circle

$$|C| = r.$$

Take one habitat $P$. We ask which positions of $C$ cover it. The condition is

$$|P - C| \le r.$$

Since $C$ already lies on the circle $|C|=r$, the valid centers form an arc on that circle. Every habitat contributes one angular interval. We only need to know whether some angle is contained in at least $k$ intervals.

That transforms the geometric problem into a classic maximum overlap problem on a circle.

A fixed radius is either feasible or infeasible. If radius $r$ works, every larger radius also works. This monotonicity allows binary search on the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force center search | Exponential / Continuous state | Large | Impossible |
| Binary search + interval sweep | $O(\log A \cdot n \log n)$ | $O(n)$ | Accepted |

Here $A$ is the search range of the radius.

## Algorithm Walkthrough

### Geometry for one habitat

Let the habitat be $P=(x,y)$, and let

$$d = |P|.$$

For a fixed radius $r>0$, the center is

$$C = r(\cos\phi,\sin\phi).$$

The habitat is covered when

$$|P-C| \le r.$$

Squaring both sides:

$$d^2 + r^2 - 2rd\cos(\phi-a) \le r^2,$$

where $a$ is the polar angle of $P$.

After simplification:

$$\cos(\phi-a) \ge \frac{d}{2r}.$$

If $d>2r$, no angle satisfies this inequality.

Otherwise,

$$|\phi-a| \le \arccos\!\left(\frac{d}{2r}\right).$$

So the habitat contributes one angular interval centered at angle $a$.

### Binary Search Feasibility Check

1. If $r=0$, count how many habitats are exactly at the origin. The radius is feasible iff that count is at least $k$.
2. For every habitat, compute $d=\sqrt{x^2+y^2}$.
3. If $d>2r$, this habitat can never be covered and contributes nothing.
4. If $d=0$, the interval covers the entire circle. Increase a global base counter.
5. Otherwise compute

$$\alpha=\arccos\!\left(\frac{d}{2r}\right).$$

The valid center angles are

$$[a-\alpha,\ a+\alpha].$$

1. Convert every circular interval into sweep events. Intervals crossing $0$ radians are split into two ordinary intervals.
2. Sort all events by angle. Process start events before end events occurring at the same angle.
3. During the sweep, maintain the current overlap count plus the number of full circle intervals. If the maximum overlap reaches $k$, radius $r$ is feasible.
4. Binary search the smallest feasible radius.

### Why it works

For a fixed radius $r$, every habitat corresponds exactly to the set of center positions that cover it. The derivation above converts that set into an angular interval on the circle $|C|=r$. A center angle covers at least $k$ habitats if and only if that angle belongs to at least $k$ intervals. The sweep computes the maximum interval overlap exactly.

The feasibility predicate is monotone. Increasing the radius enlarges every feasible set of center positions, never shrinking it. Hence binary search over $r$ finds the minimum feasible radius.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    twopi = 2.0 * math.pi
    eps = 1e-12

    def check(r):
        if r < eps:
            cnt = 0
            for x, y in pts:
                if x == 0 and y == 0:
                    cnt += 1
            return cnt >= k

        base = 0
        events = []

        for x, y in pts:
            d = math.hypot(x, y)

            if d > 2.0 * r + 1e-10:
                continue

            if d < 1e-12:
                base += 1
                continue

            ratio = d / (2.0 * r)
            if ratio > 1.0:
                ratio = 1.0

            alpha = math.acos(ratio)
            a = math.atan2(y, x)

            l = a - alpha
            rr = a + alpha

            l %= twopi
            rr %= twopi

            if l <= rr:
                events.append((l, 1))
                events.append((rr, -1))
            else:
                events.append((0.0, 1))
                events.append((rr, -1))
                events.append((l, 1))
                events.append((twopi, -1))

        events.sort(key=lambda e: (e[0], -e[1]))

        cur = base
        best = cur

        for _, typ in events:
            cur += typ
            if cur > best:
                best = cur

        return best >= k

    lo = 0.0
    hi = 200000.0

    for _ in range(50):
        mid = (lo + hi) / 2.0
        if check(mid):
            hi = mid
        else:
            lo = mid

    print("{:.10f}".format(hi))

solve()
```

The binary search maintains an interval containing the optimal radius. Fifty iterations are far more than enough to achieve error below $10^{-4}$.

The function `check(r)` implements the geometric reduction. Each habitat becomes an angular interval. Habitats farther than $2r$ from the origin cannot contribute because the circle $|C|=r$ never enters their radius-$r$ coverage disk.

The most delicate implementation detail is handling intervals that wrap around $0$ radians. Such intervals are split into two ordinary intervals before the sweep. Another subtle point is event ordering. Start events are processed before end events at the same angle, which correctly handles intervals whose endpoints coincide.

## Worked Examples

### Sample 1

```
8 4
-3 1
-4 4
1 5
2 2
2 -2
-2 -4
-1 -1
-6 0
```

The optimal radius is approximately $\sqrt{10}$.

For that radius, the generated intervals have the following structure.

| Habitat | Distance from origin | Contributes interval? |
| --- | --- | --- |
| (-3,1) | 3.1623 | Yes |
| (-4,4) | 5.6569 | Yes |
| (1,5) | 5.0990 | Yes |
| (2,2) | 2.8284 | Yes |
| (2,-2) | 2.8284 | Yes |
| (-2,-4) | 4.4721 | Yes |
| (-1,-1) | 1.4142 | Yes |
| (-6,0) | 6.0000 | Yes |

The sweep discovers a point on the center circle where four intervals overlap. Any smaller radius drops the maximum overlap below four.

This example demonstrates the core idea: the problem is not about choosing a point in the plane, but about choosing an angle on the circle of possible centers.

### Custom Example

```
3 2
0 0
2 0
-2 0
```

The answer is $1$.

For $r=1$:

| Habitat | d | Interval |
| --- | --- | --- |
| (0,0) | 0 | Entire circle |
| (2,0) | 2 | Single angle $0$ |
| (-2,0) | 2 | Single angle $\pi$ |

The origin habitat contributes one permanent overlap everywhere. At angle $0$, the second habitat is also covered, giving overlap $2$. The radius is feasible.

This example exercises both full circle intervals and degenerate intervals of zero width.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log A \cdot n \log n)$ | Binary search, each check sorts $O(n)$ events |
| Space | $O(n)$ | Event list |

The search range is bounded by $2 \cdot 10^5$. Roughly fifty binary search iterations are sufficient for high precision. The resulting complexity fits comfortably within the problem limits.

## Test Cases

```python
# helper skeleton

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # paste solve() here and return captured output
    return ""

# sample from statement
# answer checked with tolerance in real judge

# minimum size
# 1 habitat at origin, answer = 0
inp = """\
1 1
0 0
"""

# single non-origin point
inp = """\
1 1
2 0
"""

# expected answer = 1

# all habitats at origin
inp = """\
5 5
0 0
0 0
0 0
0 0
0 0
"""

# expected answer = 0

# boundary case d = 2r
inp = """\
1 1
10 0
"""

# expected answer = 5

# wrap-around interval case
inp = """\
2 1
100 1
100 -1
"""

# should succeed with almost identical radii for both points
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One origin point | 0 | Radius zero handling |
| One point at (2,0) | 1 | Degenerate interval |
| All points at origin | 0 | Full circle intervals |
| Point at distance 10 | 5 | Boundary $d=2r$ |
| Points near angle wrap | Feasible | Circular interval splitting |

## Edge Cases

### Radius Zero

Input:

```
3 2
0 0
0 0
5 0
```

The only possible center is the origin. Two habitats are already covered, so the answer is exactly $0$.

The algorithm handles this in the special branch inside `check(r)`. No trigonometric calculations are performed.

### Habitat Exactly at Distance $2r$

Input:

```
1 1
10 0
```

For radius $5$, we get

$$\frac{d}{2r} = 1, \qquad \alpha = \arccos(1) = 0.$$

The interval collapses to a single angle. The sweep still counts it correctly because start events are processed before end events.

### Interval Crossing the Angle Boundary

Input:

```
2 1
100 1
100 -1
```

The valid angular interval for one of the points may cross from angles near $2\pi$ back to angles near $0$. The algorithm splits such intervals into

$$[l, 2\pi]$$

and

$$[0, r].$$

The sweep then sees the correct overlap structure. No coverage is lost at the boundary.
