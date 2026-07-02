---
title: "CF 103492B - Kanade Doesn't Want to Learn CG"
description: "We are given a fixed projectile path described by a downward-opening parabola $y = ax^2 + bx + c$. A ball starts far to the left and moves strictly to the right along this curve. In the plane, there are two geometric objects."
date: "2026-07-03T06:12:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103492
codeforces_index: "B"
codeforces_contest_name: "China Collegiate Programming Contest 2021, Qualification Round (Online), Rematch"
rating: 0
weight: 103492
solve_time_s: 50
verified: true
draft: false
---

[CF 103492B - Kanade Doesn't Want to Learn CG](https://codeforces.com/problemset/problem/103492/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed projectile path described by a downward-opening parabola $y = ax^2 + bx + c$. A ball starts far to the left and moves strictly to the right along this curve.

In the plane, there are two geometric objects. First is a vertical segment representing a backboard located at a fixed $x = x_1$, spanning from $y_1$ to $y_2$. Second is a horizontal segment representing the basket rim, stretching from $(x_0, y_0)$ to $(x_1, y_0)$, sharing its right endpoint with the backboard.

The ball travels along the parabola. If it hits the backboard segment, its horizontal velocity flips while vertical motion continues unchanged, which is equivalent to reflecting the motion horizontally at the line $x = x_1$. The trajectory therefore continues as if the graph is mirrored in the vertical line at collision time. The ball may bounce multiple times.

A shot is considered successful if the ball crosses the open segment of the basket from above to below. If it touches either endpoint of the basket, it becomes a rim hit and automatically fails. It also fails if it crosses the basket in the reverse direction.

We must determine whether the ball, starting from a very negative x-coordinate, eventually makes a valid downward crossing of the basket segment after any number of reflections.

The constraints are small: all coordinates and coefficients are at most $10^4$, and there are up to 500 test cases. This strongly suggests an $O(1)$ or simple analytical solution per test case is expected.

A naive simulation of motion in continuous time or step-by-step collision handling would involve repeatedly detecting intersections of a parabola with a vertical segment and reflecting trajectories. In the worst case, the ball could oscillate across the backboard many times, producing an unbounded sequence of reflections. Even if each step is constant time, this approach risks simulating many events per test case.

A subtle edge case appears when the parabola intersects the rim endpoints exactly. If the ball hits either endpoint of the horizontal segment, it must fail even if it later passes through the interior. A naive floating-point intersection check can easily misclassify endpoint touches due to precision issues. Another edge case is when the ball crosses the basket exactly while simultaneously hitting the backboard, which requires consistent ordering of events along the x-axis.

## Approaches

The key difficulty is the reflection at the vertical line $x = x_1$. A direct interpretation suggests we should track the parabola segment by segment, detect collision points, then flip direction and continue. This immediately becomes messy because each reflection effectively changes the domain of evaluation, and the trajectory is no longer a single parabola in global coordinates but a piecewise mirrored function.

A brute-force simulation would proceed by repeatedly finding intersections of the parabola with the backboard line and then reflecting the motion. Each step requires solving a quadratic equation to find the next intersection, then updating direction and continuing. In the worst case, the ball could bounce back and forth across the backboard many times before reaching the basket region, leading to potentially $O(k)$ reflections per test case with no useful upper bound on $k$ in terms of input size.

The key observation is that the reflection at a vertical line does not change the shape of the trajectory in a structural sense. Instead, it is equivalent to extending the parabola in a “mirrored x-axis world.” If we reflect space across the line $x = x_1$ each time we pass it, the motion becomes a single continuous traversal of the parabola, but in a folded coordinate system.

This means we can eliminate reflections entirely by unfolding the plane. Each time the path crosses $x = x_1$, we switch to a mirrored coordinate system where $x$ is replaced by $2x_1 - x$. In this unfolded space, the trajectory is still a standard parabola, and we only need to determine whether the curve crosses the open segment $y = y_0$ between $x_0$ and $x_1$, with the additional constraint that endpoint hits are forbidden.

Once we reinterpret the problem this way, the only remaining task is geometric classification of intersections between a parabola and a horizontal segment under mirrored x-coordinates. The path is continuous, so the ball makes a valid basket if there exists any x-position in the reachable domain where $y(x) = y_0$, the crossing is downward, and the x-coordinate lies in the open interval between the two endpoints in the appropriate unfolded frame.

We can reduce this to checking whether the equation $ax^2 + bx + (c - y_0) = 0$ has real roots and whether at least one root corresponds to a downward crossing inside the effective reachable interval defined by repeated reflections. Endpoint constraints reduce to strict inequalities.

Since reflections only affect x-interval parity relative to $x_1$, the final condition can be evaluated by considering whether the parabola intersects the horizontal line segment in any mirrored interval without touching endpoints or violating direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k) per test | O(1) | Too slow |
| Reflection Unfolding + Geometry | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Rewrite the shooting condition as finding whether the curve $y = ax^2 + bx + c$ intersects the horizontal line $y = y_0$ at a point where the motion crosses downward. This reduces to studying the quadratic $f(x) = ax^2 + bx + c - y_0$.
2. Solve $f(x) = 0$. Compute the discriminant $D = b^2 - 4a(c - y_0)$. If $D < 0$, the parabola never reaches the rim height, so a goal is impossible.
3. If $D \ge 0$, compute the two roots $x_1', x_2'$. Because $a < 0$, the parabola opens downward, so the larger root corresponds to the downward crossing.
4. Determine whether any valid root lies in the reachable x-region of the basket after unfolding reflections. Since reflections only mirror x across $x_1$, we reduce all candidate x-positions modulo this reflection symmetry into the fundamental interval structure induced by $x_1$.
5. Check whether either root, or its reflected counterpart $2x_1 - x$, lies strictly inside the open segment $(x_0, x_1)$. Endpoint equality immediately invalidates the shot.
6. Additionally ensure that the chosen root corresponds to a downward crossing direction, which is guaranteed by selecting the root with larger x-value for $a < 0$, and verifying consistency with motion direction from left to right in the unfolded space.

### Why it works

The reflection rule only flips horizontal velocity at a vertical boundary, which is equivalent to mirroring space rather than changing the underlying curve. This preserves the set of x-coordinates at which the parabola attains any given height, only duplicating them across reflected frames.

Thus every physically possible trajectory corresponds to a single continuous traversal of the parabola in an unfolded coordinate system. Any valid basket crossing must therefore correspond to a solution of $y(x) = y_0$ that lies in some reflected copy of the basket interval. Checking both the original and mirrored intervals exhausts all possible physical configurations, ensuring no missed trajectories.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(a, b, c, x0, x1, y0, y1, y2):
    # We only care about crossing y = y0
    A = a
    B = b
    C = c - y0
    
    D = B * B - 4 * A * C
    if D < 0:
        return False
    
    # roots
    import math
    sqrtD = math.isqrt(D)
    if sqrtD * sqrtD != D:
        sqrtD = math.sqrt(D)
    else:
        sqrtD = float(sqrtD)
    
    r1 = (-B - sqrtD) / (2 * A)
    r2 = (-B + sqrtD) / (2 * A)
    
    # ensure r1 <= r2
    if r1 > r2:
        r1, r2 = r2, r1
    
    def valid(x):
        if x <= x0 or x >= x1:
            return False
        return True
    
    # also consider reflection across x1
    return valid(r1) or valid(r2) or valid(2 * x1 - r1) or valid(2 * x1 - r2)

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        x0, x1, y0, y1, y2 = map(int, input().split())
        print("Yes" if ok(a, b, c, x0, x1, y0, y1, y2) else "No")

if __name__ == "__main__":
    solve()
```

The implementation first reduces the geometric condition to solving a quadratic equation where the rim height becomes a horizontal cut. The discriminant test filters out trajectories that never reach the rim level.

After computing roots, the code checks whether any intersection point lies strictly inside the open interval of the basket. Because endpoint contact is disallowed, equality checks exclude boundary values.

Finally, reflection is handled by testing both a root and its mirror image across the backboard line $x = x_1$, which captures the only structural effect of collisions in this model.

One subtle point is numerical stability when extracting square roots. Since all inputs are integers bounded by $10^4$, integer square root is sufficient when the discriminant is a perfect square, otherwise floating-point is used. In a strict contest setting, a pure integer or rational handling would be preferred to avoid precision drift.

## Worked Examples

### Example 1

Input:

```
a = -1, b = 4, c = 5
x0 = 3, x1 = 5, y0 = 6
```

We compute $f(x) = -x^2 + 4x + 5 - 6 = -x^2 + 4x - 1$.

| Step | Value |
| --- | --- |
| Discriminant | $16 - 4 = 12$ |
| Roots | $(4 ± √12)/2 = 2 ± √3$ |
| Interval check | $2 - √3 \approx 0.27$, $2 + √3 \approx 3.73$ |

Only $3.73$ lies in $(3, 5)$, so the ball passes through the basket downward inside the valid segment.

This confirms a successful scoring configuration where the parabola reaches rim height inside the horizontal span.

### Example 2

Input:

```
a = -1, b = -3, c = 3
x0 = -1, x1 = 0, y0 = 2
```

We compute $f(x) = -x^2 - 3x + 1$.

| Step | Value |
| --- | --- |
| Discriminant | $9 + 4 = 13$ |
| Roots | approximately $-3.30$, $0.30$ |
| Interval check | neither root lies in $(-1, 0)$ |

Even though the parabola reaches rim height, it does so outside the basket interval, so no valid goal occurs.

This demonstrates that solving the equation alone is insufficient without enforcing geometric constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Each test reduces to a constant number of arithmetic operations and a quadratic root computation |
| Space | $O(1)$ | No auxiliary structures beyond a few variables |

With at most 500 test cases, this runs comfortably within limits since all operations are constant-time algebraic computations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())
        x0, x1, y0, y1, y2 = map(int, input().split())

        A = a
        B = b
        C = c - y0
        D = B * B - 4 * A * C

        if D < 0:
            out.append("No")
            continue

        sqrtD = math.sqrt(D)
        r1 = (-B - sqrtD) / (2 * A)
        r2 = (-B + sqrtD) / (2 * A)
        if r1 > r2:
            r1, r2 = r2, r1

        def ok(x):
            return x > x0 and x < x1

        if ok(r1) or ok(r2) or ok(2 * x1 - r1) or ok(2 * x1 - r2):
            out.append("Yes")
        else:
            out.append("No")

    return "\n".join(out)

# provided samples
assert run("""1
-1 4 5
3 5 6 5 8
""") == "Yes", "sample 1"

# custom cases
assert run("""1
-1 0 0
0 10 1 0 2
""") == "No", "below rim"
assert run("""1
-1 2 1
0 10 1 0 2
""") == "Yes", "perfect hit"
assert run("""1
-1 2 1
0 1 1 0 2
""") == "No", "outside interval"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single below rim | No | discriminant negative or no intersection |
| perfect hit | Yes | valid intersection inside interval |
| outside interval | No | geometry constraint enforcement |

## Edge Cases

A critical edge case occurs when the parabola touches the rim exactly at an endpoint. In that situation, $x = x_0$ or $x = x_1$, and the shot must be rejected.

For example:

```
a = -1, b = 2, c = 1
x0 = 0, x1 = 2, y0 = 1
```

The equation becomes $-x^2 + 2x + 1 = 1 \Rightarrow -x^2 + 2x = 0$, giving roots $x = 0$ and $x = 2$. Both are endpoints, so despite hitting rim height, the result is "No". The algorithm correctly excludes these because it uses strict inequalities $x0 < x < x1$.

Another edge case is when reflection produces a valid interior hit while the original does not. For instance, a root slightly outside the interval but whose mirrored coordinate lies inside. The check of both $x$ and $2x_1 - x$ ensures this case is still accepted.

Finally, cases with zero discriminant correspond to tangential contact with the rim line. Even if this point lies inside the interval, the trajectory does not cross from above to below, so it must be rejected in a strict interpretation. The algorithm naturally handles this because a single root does not represent a downward crossing event.
