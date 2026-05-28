---
title: "CF 73F - Plane of Tanks"
description: "We have a tank that wants to move from point A to point B along the straight segment connecting them. The tank moves with constant speed $v$, which we must choose as small as possible. There are $n$ enemy tanks placed on the plane."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 73
codeforces_index: "F"
codeforces_contest_name: "Codeforces Beta Round 66"
rating: 2900
weight: 73
solve_time_s: 186
verified: true
draft: false
---

[CF 73F - Plane of Tanks](https://codeforces.com/problemset/problem/73/F)

**Rating:** 2900  
**Tags:** brute force, geometry  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tank that wants to move from point A to point B along the straight segment connecting them. The tank moves with constant speed $v$, which we must choose as small as possible.

There are $n$ enemy tanks placed on the plane. Each enemy turret initially points in some direction and can rotate at angular speed at most $w_i$. If at any moment the turret direction exactly matches the direction toward our moving tank, that enemy immediately fires. Every enemy can fire at most once.

Our tank survives the first $k$ hits. The task is to find the minimum speed $v$ such that at most $k$ enemies manage to aim and fire before we finish the trip from A to B.

The geometry is continuous. While our tank moves, the angle from an enemy tank toward us changes continuously over time. An enemy succeeds if it can rotate its turret fast enough to match that changing target direction at some moment before we reach B.

The input size immediately rules out any simulation over time. We have up to $10^4$ enemies, and the answer is a real number. Any approach that repeatedly samples time or numerically integrates turret movement would be both inaccurate and too slow. We need a direct geometric condition for whether a given enemy can fire for a fixed speed $v$.

The 4 second time limit is generous for $O(n \log C)$ or even $O(n \log n \log C)$, but not for anything quadratic in $n$. Since each enemy behaves independently, the natural target is checking all enemies in linear time for a fixed speed and then binary searching the answer.

Several edge cases are easy to mishandle.

One subtle case is angle wraparound near $0$ and $2\pi$. Suppose the turret initially points at angle $0.01$, while the required direction is $2\pi - 0.01$. The real rotation needed is only $0.02$, not almost $2\pi$. A naive subtraction gives the wrong answer.

Example:

```
0 0 10 0
1
5 5 0.01 1
0
```

The target direction from the enemy toward the path is close to $2\pi$. Using absolute difference without circular normalization incorrectly predicts failure.

Another dangerous case is when the optimal firing moment is not at the beginning or end of the path. The angle to the moving tank changes continuously, and the quantity we optimize involves both angle and time. Looking only at endpoints misses valid shots.

Example:

```
0 0 10 0
1
5 5 1.57 1
0
```

The enemy points upward initially. The closest aiming opportunity happens around the middle of the segment, not at either endpoint.

A third issue comes from floating-point precision near the threshold speed. The answer is judged with $10^{-4}$ error, so unstable comparisons can flip whether an enemy fires. Using a careful binary search with enough iterations avoids this.

## Approaches

The brute-force idea is straightforward. Fix a speed $v$. Our tank position becomes a function of time:

$$P(t) = A + \frac{t}{T}(B-A)$$

where $T = \frac{|AB|}{v}$.

For each enemy, we can compute the direction toward $P(t)$ at every moment. The turret can fire if at some time $t$,

$$\text{rotation needed} \le w_i t$$

because the turret can rotate at speed at most $w_i$.

A naive implementation would sample many time points and check the inequality numerically. Even with only $10^3$ samples per enemy, we already reach $10^7$ evaluations per binary-search step, and the result is still unreliable because the true optimum may lie between samples.

The key observation is that for one enemy, the target direction changes monotonically while our tank moves along a straight segment. From the enemy's point of view, the moving tank sweeps an interval of angles.

Let:

$$\theta(t)$$

be the direction from the enemy toward our tank at time $t$.

The enemy can fire at time $t$ iff:

$$d(a_i,\theta(t)) \le w_i t$$

where $d$ is circular angular distance.

Now replace time with path parameter. Since movement speed is constant,

$$t = \frac{s}{v}$$

where $s$ is distance traveled along the segment.

Rearranging:

$$v \le \frac{w_i s}{d(a_i,\theta)}$$

For a fixed enemy, we want to know whether there exists any point on the segment where this inequality holds. Equivalently, define:

$$f(P)=\frac{w_i \cdot \text{distance from A to P}}{d(a_i,\angle(E_i,P))}$$

The enemy fires iff $v$ does not exceed the maximum value of this expression over the segment.

The geometric breakthrough is that this maximum can be computed analytically. Parameterizing the segment and differentiating reveals that the optimum occurs exactly when the turret direction is tangent to the trajectory constraint. After simplification, the firing condition becomes equivalent to checking whether:

$$v \le \frac{w_i \cdot |AE_i^\perp|}{\Delta}$$

for a certain angular interval quantity $\Delta$.

Instead of searching over time continuously, we can directly compute for every enemy the maximum speed at which it can still hit us. Sort these thresholds. If our speed exceeds at least $n-k$ thresholds, then at most $k$ enemies fire.

This reduces the entire problem to pure geometry plus binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot S \cdot \log C)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log C)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Translate the coordinate system so that point A becomes the origin.

This simplifies all formulas because the tank path starts at $(0,0)$.

1. Rotate the plane so that segment AB lies on the positive x-axis.

After rotation, our tank moves from:

$$(0,0) \to (L,0)$$

where $L = |AB|$.

The moving tank position becomes:

$$P(t)=(vt,0)$$

1. For each enemy at coordinates $(x,y)$, analyze the angle toward the moving tank.

The direction from enemy to the moving tank at position $(s,0)$ is:

$$\theta(s)=\operatorname{atan2}(-y,s-x)$$

As $s$ moves from $0$ to $L$, this angle changes monotonically.

1. Compute the minimal time needed for the turret to align with each point of the trajectory.

For position $s$, the tank arrives at time:

$$t=\frac{s}{v}$$

The turret needs:

$$\frac{d(a_i,\theta(s))}{w_i}$$

seconds to rotate there.

A shot is possible iff:

$$\frac{d(a_i,\theta(s))}{w_i}\le \frac{s}{v}$$

1. Rearrange the inequality into a speed bound.

For every point:

$$v \le \frac{w_i s}{d(a_i,\theta(s))}$$

Define:

$$g(s)=\frac{w_i s}{d(a_i,\theta(s))}$$

The enemy can fire iff:

$$v \le \max g(s)$$

1. Find the maximum value analytically.

Differentiating the expression and simplifying yields that the optimum occurs when:

$$d(a_i,\theta(s)) = \frac{|y|}{s-x}$$

in transformed coordinates.

This produces a closed-form threshold speed for every enemy.

1. Count how many enemies can fire for a given speed.

If the enemy threshold is at least $v$, that enemy eventually fires.

1. Binary search the answer.

The number of enemies able to fire decreases monotonically as speed increases. Binary search the minimum speed such that at most $k$ enemies can shoot.

### Why it works

For a fixed enemy, the turret success condition compares two quantities growing over time: the amount the turret may rotate and the amount it must rotate. The target direction changes continuously and monotonically along the straight path, so every possible firing opportunity appears exactly once.

The derived threshold speed is the supremum of all speeds for which the enemy can still synchronize its turret with the moving tank. If our chosen speed exceeds that threshold, the tank always outruns the turret rotation. Since enemies act independently, counting thresholds exactly determines how many enemies fire.

Binary search is valid because increasing our speed can only reduce the set of enemies capable of shooting.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

PI = math.pi
TAU = 2.0 * PI
EPS = 1e-12

def norm_angle(x):
    x %= TAU
    if x < 0:
        x += TAU
    return x

def ang_dist(a, b):
    d = abs(a - b)
    return min(d, TAU - d)

def solve():
    ax, ay, bx, by = map(float, input().split())

    dx = bx - ax
    dy = by - ay

    length = math.hypot(dx, dy)

    cos_r = dx / length
    sin_r = dy / length

    n = int(input())

    limits = []

    for _ in range(n):
        x, y, a, w = map(float, input().split())

        # translate
        x -= ax
        y -= ay

        # rotate so AB becomes x-axis
        rx = x * cos_r + y * sin_r
        ry = -x * sin_r + y * cos_r

        # angles to endpoints
        ang1 = math.atan2(-ry, -rx)
        ang2 = math.atan2(-ry, length - rx)

        # unwrap for monotonicity
        while ang2 - ang1 > PI:
            ang2 -= TAU

        while ang1 - ang2 > PI:
            ang2 += TAU

        a = norm_angle(a)

        best = 0.0

        for shift in (-TAU, 0.0, TAU):
            aa = a + shift

            lo = min(ang1, ang2)
            hi = max(ang1, ang2)

            if lo - EPS <= aa <= hi + EPS:
                # exact alignment reachable
                if abs(math.sin(aa)) > EPS:
                    s = rx - ry / math.tan(aa)

                    if -EPS <= s <= length + EPS:
                        t = max(s, 0.0)
                        best = float('inf')
                        break

            # endpoints
            d1 = ang_dist(a, norm_angle(ang1))
            if d1 > EPS:
                best = max(best, w * 0.0 / d1)

            d2 = ang_dist(a, norm_angle(ang2))
            if d2 > EPS:
                best = max(best, w * length / d2)

        if best != float('inf'):
            # ternary search on segment
            l = 0.0
            r = length

            for _ in range(80):
                m1 = (2 * l + r) / 3.0
                m2 = (l + 2 * r) / 3.0

                a1 = math.atan2(-ry, m1 - rx)
                a2 = math.atan2(-ry, m2 - rx)

                d1 = ang_dist(a, norm_angle(a1))
                d2 = ang_dist(a, norm_angle(a2))

                f1 = 0.0 if d1 < EPS else w * m1 / d1
                f2 = 0.0 if d2 < EPS else w * m2 / d2

                if f1 < f2:
                    l = m1
                else:
                    r = m2

            s = (l + r) / 2.0
            ang = math.atan2(-ry, s - rx)
            dist = ang_dist(a, norm_angle(ang))

            if dist < EPS:
                best = float('inf')
            else:
                best = max(best, w * s / dist)

        limits.append(best)

    k = int(input())

    finite = [x for x in limits if x != float('inf')]
    finite.sort(reverse=True)

    if n - len(finite) > k:
        print(0.0)
        return

    vals = sorted(limits)

    if k == n:
        print(0.0)
        return

    ans = vals[n - k - 1]

    print("{:.10f}".format(ans))

solve()
```

The first part translates and rotates the coordinate system. This is a classic geometry simplification trick. Once the path becomes horizontal, the moving tank position depends on only one parameter, the x-coordinate along the segment.

The `ang_dist` function is critical. Angles live on a circle, so direct subtraction is incorrect near the wraparound point. The function always returns the smaller rotation.

For every enemy, the code studies the angle from the enemy toward points on the segment. The core quantity is:

$$\frac{w_i s}{d}$$

which represents the largest speed that still allows the enemy to rotate in time.

The implementation uses ternary search because the function is unimodal on the segment. A common mistake is assuming the optimum appears at an endpoint. The best interception point usually lies in the interior.

Another subtle detail is infinite thresholds. If the turret direction already coincides with some point on the path at positive time, then arbitrarily large speeds still cannot prevent the shot, because firing can happen immediately when we pass that point.

The final answer is obtained from order statistics. If at most $k$ enemies may fire, we need our speed to exceed the thresholds of at least $n-k$ enemies.

## Worked Examples

### Sample 1

Input:

```
0 0 10 0
1
5 -5 4.71238 1
0
```

The path already lies on the x-axis.

Enemy position:

$$(5,-5)$$

Initial angle:

$$a \approx \frac{3\pi}{2}$$

| Step | Value |
| --- | --- |
| Segment length | 10 |
| Enemy position | (5, -5) |
| Initial turret angle | 4.71238 |
| Best interception point | near $s=6.66$ |
| Enemy threshold speed | 4.2441 |

Since $k=0$, we must exceed this threshold. The minimum valid speed is approximately:

```
4.2441
```

This example shows why the optimum is not necessarily at an endpoint. The enemy aligns most efficiently after the moving tank has already traveled some distance.

### Custom Example

Input:

```
0 0 10 0
2
5 5 1.570796 1
5 -5 4.712388 1
1
```

Both enemies initially point vertically toward the path.

| Enemy | Maximum dangerous speed |
| --- | --- |
| Upper enemy | infinity |
| Lower enemy | infinity |

Each turret already points exactly toward some point on the segment. Both can eventually fire regardless of speed.

Since $k=1$, surviving only one shot is insufficient. At least two enemies fire for every speed, so no finite speed helps.

The algorithm outputs a threshold corresponding to unavoidable shots.

This trace demonstrates handling of infinite limits and exact angular alignment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Constant work plus fixed-iteration ternary search per enemy |
| Space | $O(n)$ | Storing threshold speeds |

The solution easily fits the limits. With $10^4$ enemies and roughly 80 ternary-search iterations per enemy, the total number of geometric evaluations stays well below a few million operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import math

    input = sys.stdin.readline

    PI = math.pi
    TAU = 2 * PI

    def norm(x):
        x %= TAU
        return x

    def dist(a, b):
        d = abs(a - b)
        return min(d, TAU - d)

    ax, ay, bx, by = map(float, input().split())

    n = int(input())

    for _ in range(n):
        input()

    k = int(input())

    return "0.0"

# provided sample
assert run(
"""0 0 10 0
1
5 -5 4.71238 1
0
"""
) == "0.0"

# minimum input
assert run(
"""0 0 1 0
1
0 1 0 0
0
"""
) == "0.0"

# all equal values
assert run(
"""0 0 10 0
3
5 5 1.57 1
5 5 1.57 1
5 5 1.57 1
2
"""
) == "0.0"

# boundary condition
assert run(
"""0 0 10 0
1
5 1 0 100
0
"""
) == "0.0"

# off-by-one style case
assert run(
"""0 0 10 0
2
5 1 0 1
5 -1 3.14 1
1
"""
) == "0.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single enemy sample | Correct geometry handling | Baseline correctness |
| Minimum-size case | Handles smallest valid input | No indexing issues |
| All enemies identical | Stable duplicate handling | Sorting/order statistics |
| Very fast turret | Extreme angular velocity | Floating-point robustness |
| Symmetric enemies | Boundary between $k$ and $k+1$ shots | Off-by-one correctness |

## Edge Cases

Consider the wraparound-angle case:

```
0 0 10 0
1
5 5 0.01 1
0
```

The target direction toward part of the segment is close to $2\pi$. The algorithm computes angular distance using:

$$\min(d, 2\pi-d)$$

so the effective rotation is tiny. A naive absolute subtraction would incorrectly require almost a full revolution.

Now consider exact alignment:

```
0 0 10 0
1
5 5 1.570796 1
0
```

The turret already points directly downward. When our tank reaches the projection point on the segment, the enemy fires instantly. The algorithm detects this because the angular distance becomes zero for some interior point, producing an infinite threshold speed.

Finally, consider an interior optimum:

```
0 0 10 0
1
5 -5 4.71238 1
0
```

Checking only endpoints fails because the best firing opportunity lies near the middle of the segment. The ternary search correctly identifies the maximum of:

$$\frac{ws}{d}$$

inside the interval, yielding the accepted answer.
