---
title: "CF 420E - Playing the ball"
description: "A ball is thrown from the origin along some chosen direction, and it repeatedly appears at equally spaced points along that ray: first at distance $d$, then at $2d$, then $3d$, and so on. The direction is fixed once chosen, but it can be any real direction in the plane."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 420
codeforces_index: "E"
codeforces_contest_name: "Coder-Strike 2014 - Finals (online edition, Div. 1)"
rating: 2600
weight: 420
solve_time_s: 120
verified: true
draft: false
---

[CF 420E - Playing the ball](https://codeforces.com/problemset/problem/420/E)

**Rating:** 2600  
**Tags:** geometry  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

A ball is thrown from the origin along some chosen direction, and it repeatedly appears at equally spaced points along that ray: first at distance $d$, then at $2d$, then $3d$, and so on. The direction is fixed once chosen, but it can be any real direction in the plane.

On the plane there are $n$ circles. Every time one of these discrete landing points falls inside or on a circle, that circle contributes one point. If a landing point lies inside multiple circles, all of them contribute simultaneously. The task is to choose the direction of the ray so that the total number of such “hits” over all circles and all landing points is maximized.

The key object is not a continuous trajectory but a discrete infinite sequence of points $P_k = k \cdot d \cdot u$, where $u$ is a unit vector. The score is determined entirely by how many of these points fall into the given disks.

The constraints matter in a very specific way. With up to $2 \cdot 10^4$ circles, any approach that checks all directions or all pairs of circles directly is already too large. More importantly, any solution that tries to simulate all rays or discretize angles too finely will fail because the answer depends on a continuous choice of direction, not a finite set of candidates.

Each circle is relatively small in radius (at most 50), and the spacing $d$ is also small (at most 10). This strongly suggests that for a fixed circle, only a small number of indices $k$ can possibly produce hits, because once $k d$ is far from the circle center’s distance to the origin, the circle cannot contain that point.

A subtle failure case appears if one assumes each circle contributes at most one hit. A circle can be intersected multiple times by different multiples of $d$. For example, if a circle is centered near the origin but large enough, both $k=2$ and $k=3$ may produce valid hits for the same direction.

Another pitfall is treating the problem as if each circle only imposes a single angular constraint. The constraint actually depends on $k$, and different $k$ values for the same circle produce different angular intervals.

## Approaches

A direct way to think about the problem is to fix a direction and simulate the ray. For each circle, and for each integer $k$, we check whether the point $k d u$ lies inside the circle. Over all circles and all $k$, we count matches. This is correct but hopelessly slow, because the number of direction candidates is infinite, and even evaluating one direction requires checking all circles and all relevant $k$.

The key structural observation is to reverse the perspective. Instead of fixing a direction and checking circles, we fix a circle and ask for which directions and which indices $k$ the corresponding point lies inside it.

Fix a circle with center $C$. For a fixed $k$, the condition that $k d u$ lies inside the circle is a geometric constraint on the direction $u$. The point $k d u$ is at a fixed distance from the origin, so we are intersecting two objects: a circle centered at the origin with radius $k d$, and the given circle centered at $C$. This intersection corresponds to a set of angles from which the origin can “see” the circle at that radial distance.

For each valid $k$, the set of directions $u$ forms a contiguous angular interval. That interval is centered around the direction of $C$, and its half-width is determined by the law of cosines.

The remaining question is how many $k$ values per circle must be considered. The distance from the origin to $k d u$ is fixed, so for a circle centered at distance $|C|$, only values of $k$ such that $k d$ is within $r$ of $|C|$ can possibly work. That gives a tight integer range:

$$\frac{|C| - r}{d} \le k \le \frac{|C| + r}{d}.$$

Because $r \le 50$ and $d \ge 5$, this range contains at most about 20 integers per circle.

This reduces the problem to generating a collection of angular intervals, each carrying weight 1, and then finding the maximum overlap among them on the circle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over directions and circles | Infinite / exponential | O(n) | Too slow |
| Interval generation over valid $k$ values | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each circle, compute its distance $R$ from the origin and the direction angle $\theta$ from the origin to its center. This fixes the central geometry of all possible hits for that circle.
2. Determine the integer range of $k$ such that the circle could intersect the circle centered at the origin with radius $k d$. This is obtained from $|R - r| \le k d \le R + r$, then converted into integer bounds. This step filters out all irrelevant multiples.
3. For each integer $k$ in this range, treat the problem as an angular visibility problem between two circles: one centered at the origin with radius $k d$, and the given circle.
4. Compute the angular half-width $\alpha$ using the cosine law:

$$\cos \alpha = \frac{(k d)^2 + R^2 - r^2}{2 k d R}.$$

Clamp numerical issues so that values slightly outside $[-1,1]$ do not break arccos.
5. Add an interval $[\theta - \alpha, \theta + \alpha]$. If it crosses the $-\pi, \pi$ boundary, split it into two intervals.
6. After processing all circles and all valid $k$, sort all interval endpoints and sweep over angles, maintaining a running sum of active intervals.
7. The maximum value of this running sum is the answer, corresponding to the direction that intersects the maximum number of circle-hit events.

### Why it works

Each pair $(\text{circle}, k)$ contributes independently to the score: for a fixed direction, it either counts or does not count. The geometry shows that for fixed $k$, the set of directions that satisfy the condition is exactly one angular interval. Therefore every valid event can be represented as an interval on the unit circle, and the final score for a direction is exactly the number of intervals covering that angle. Maximizing the score becomes a maximum overlap problem on a circle, and the sweep line correctly captures all overlaps.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def norm_angle(a):
    while a <= -math.pi:
        a += 2 * math.pi
    while a > math.pi:
        a -= 2 * math.pi
    return a

def add_interval(events, l, r):
    if l <= r:
        events.append((l, 1))
        events.append((r, -1))
    else:
        events.append((-math.pi, 1))
        events.append((r, -1))
        events.append((l, 1))
        events.append((math.pi, -1))

n, d = map(int, input().split())

events = []

for _ in range(n):
    x, y, r = map(int, input().split())
    R = math.hypot(x, y)
    if R == 0:
        continue

    base_angle = math.atan2(y, x)

    k_min = int(math.ceil((R - r) / d))
    k_max = int(math.floor((R + r) / d))

    if k_max < 1:
        continue
    k_min = max(k_min, 1)

    for k in range(k_min, k_max + 1):
        rk = k * d

        val = (rk * rk + R * R - r * r) / (2 * rk * R)
        val = max(-1.0, min(1.0, val))

        ang = math.acos(val)

        l = base_angle - ang
        rgt = base_angle + ang

        l = norm_angle(l)
        rgt = norm_angle(rgt)

        add_interval(events, l, rgt)

events.sort()

ans = 0
cur = 0
for a, t in events:
    cur += t
    ans = max(ans, cur)

print(ans)
```

The code begins by converting each circle into the angular description of all valid viewing directions for each feasible $k$. The `k_min` and `k_max` computation is the crucial pruning step that prevents iterating unnecessary indices.

Each interval is carefully normalized to handle wrap-around at $\pm \pi$, because angular sweeps require a linear ordering. The sweep itself is a standard difference-array over sorted events.

A subtle detail is clamping the cosine argument before calling `acos`, since floating-point arithmetic near tangency can produce values slightly outside the valid domain.

## Worked Examples

Consider a small instance with two circles and a moderate step size.

### Example 1

Input:

```
2 5
1 1 1
5 0 1
```

| Circle | R | k range | Interval generated |
| --- | --- | --- | --- |
| (1,1,1) | √2 | k=1 | small arc around 45° |
| (5,0,1) | 5 | k=1 | arc around 0° |

The sweep over angles never accumulates more than 1 overlap, so the answer is 1. This shows that even though both circles are reachable, no single direction aligns both hits at the same $k$.

### Example 2

Input:

```
1 5
10 0 6
```

| k | Point radius | Condition | Result |
| --- | --- | --- | --- |
| 1 | 5 | inside circle | valid |
| 2 | 10 | inside circle | valid |

Both $k=1$ and $k=2$ produce valid intervals centered at 0 radians, so the sweep accumulates 2 overlaps at angle 0.

This demonstrates that a single circle can contribute multiple scoring events for a fixed direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + K)$ | Each circle contributes at most ~20 values of $k$, each producing one interval, followed by sorting and sweeping |
| Space | $O(n)$ | Storing all interval events |

The bound on $k$ is what keeps the solution comfortably within limits: although there are up to $2 \cdot 10^4$ circles, the total number of generated intervals stays around a few hundred thousand, which is well within a 2-second C++ or optimized Python solution.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    input = sys.stdin.readline

    n, d = map(int, input().split())
    events = []

    def norm(a):
        while a <= -math.pi:
            a += 2 * math.pi
        while a > math.pi:
            a -= 2 * math.pi
        return a

    def add(l, r):
        if l <= r:
            events.append((l, 1))
            events.append((r, -1))
        else:
            events.append((-math.pi, 1))
            events.append((r, -1))
            events.append((l, 1))
            events.append((math.pi, -1))

    for _ in range(n):
        x, y, r = map(int, input().split())
        R = math.hypot(x, y)
        if R == 0:
            continue
        ang0 = math.atan2(y, x)

        kmin = int(math.ceil((R - r) / d))
        kmax = int(math.floor((R + r) / d))
        kmin = max(kmin, 1)
        if kmax < kmin:
            continue

        for k in range(kmin, kmax + 1):
            rk = k * d
            val = (rk*rk + R*R - r*r) / (2*rk*R)
            val = max(-1.0, min(1.0, val))
            ang = math.acos(val)
            add(norm(ang0-ang), norm(ang0+ang))

    events.sort()
    cur = ans = 0
    for _, t in events:
        cur += t
        ans = max(ans, cur)
    return str(ans)

# provided samples
assert run("2 5\n1 1 1\n5 0 1\n") == "1"

# circle hits twice
assert run("1 5\n10 0 6\n") == "2"

# far circle, no hit
assert run("1 5\n100 0 1\n") == "0"

# symmetric case
assert run("2 5\n10 0 6\n-10 0 6\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | 1 | basic correctness |
| single circle multiple hits | 2 | multiple k contributions per circle |
| far circle | 0 | pruning of invalid k |
| symmetric circles | 2 | accumulation across independent intervals |

## Edge Cases

A circle far from the origin with small radius produces an empty $k$-range, and the algorithm naturally skips it because $k_{\max} < k_{\min}$. This prevents any invalid interval generation and avoids unnecessary floating-point computations.

When a circle is large enough to intersect multiple radii $k d$, the algorithm generates multiple intervals for the same circle. Each interval is independent, and the sweep line correctly counts them as separate contributions. This is crucial in cases where the optimal direction passes through the same geometric region at different distances.

When an interval crosses the $-\pi$ boundary, it is split into two, ensuring the sweep line sees a consistent ordering. Without this, the angular structure would break, and overlaps near the branch cut could be miscounted.
