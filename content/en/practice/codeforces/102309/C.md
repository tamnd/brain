---
title: "CF 102309C - Cai Xukun and Orz Pandas"
description: "We need to choose an initial velocity for a basketball thrown from (P=(x0,y0)) so that it reaches (Q=(x1,y1)) at some time (t), while the initial speed does not exceed (v{max}). The official problem uses the physical equation [ B(t)=P+v0t+frac12gt^2, ] where (g=(0,-9.80665))."
date: "2026-08-13T06:42:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "C"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 663
verified: true
draft: false
---

[CF 102309C - Cai Xukun and Orz Pandas](https://codeforces.com/problemset/problem/102309/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to choose an initial velocity for a basketball thrown from (P=(x_0,y_0)) so that it reaches (Q=(x_1,y_1)) at some time (t), while the initial speed does not exceed (v_{\max}).

The official problem uses the physical equation

[
B(t)=P+v_0t+\frac12gt^2,
]

where (g=(0,-9.80665)). The copied statement in the prompt omits the factor (1/2), but the official Codeforces statement contains it, and the sample output is consistent with that version.

For one test case, the four coordinates describe the starting point and target point in meters, while (v_{\max}) is the largest allowed magnitude of the initial velocity in meters per second. We must output (v_x), (v_y), and the hitting time (t). There may be arbitrarily many valid answers, so we only need to construct one.

The coordinates are bounded by (200) in absolute value, so the displacement in either direction is at most (400). There is no large array or graph hidden in the input, and each test case can be solved using a constant number of arithmetic operations. The real challenge is finding the algebraic construction rather than optimizing an asymptotically large computation. Multiple test cases continue until EOF, so the solution should use constant work per line.

There are two edge cases that deserve explicit treatment. If the starting and target points coincide, for example

```
0 0 0 0 0
```

then (v_0=(0,0)) and (t=0) is a valid answer. A formula that divides by the distance between the points would divide by zero. The fact that the problem guarantees a solution also means that (t=0) must be accepted in this case, because with (v_{\max}=0) there is no positive-time solution returning to the same point.

A second special case is a purely vertical downward throw, for example

```
0 10 0 0 0
```

A valid answer is

```
0 0 1.428...
```

because gravity alone moves the ball downward by (10) meters. A careless implementation might insist on a positive vertical initial velocity or divide by a horizontal displacement, neither of which is necessary.

## Approaches

A direct numerical approach would treat the flight time (t) as the unknown. For every candidate (t), the required velocity is determined uniquely:

[
v_x=\frac{dx}{t},
\qquad
v_y=\frac{dy}{t}+\frac{g_0t}{2},
]

where (dx=x_1-x_0), (dy=y_1-y_0), and (g_0=9.80665). We could scan possible values of (t), compute the corresponding speed, and look for one not exceeding (v_{\max}). The method is conceptually correct because every positive time determines exactly one velocity that reaches the target.

The problem is precision. If we scan the interval from (0) to (100) with a step of (10^{-8}), we already need (10^{10}) evaluations for one test case. A much coarser step can miss the narrow interval of valid times or produce a trajectory whose position error exceeds (10^{-6}). Numerical scanning is solving a problem that the algebra lets us solve exactly.

The key observation is that after expressing the velocity in terms of (t), its squared magnitude has a very simple form. Let

[
r=\sqrt{dx^2+dy^2}
]

be the distance between the two points, and let

[
k=\frac{9.80665}{2}=4.903325.
]

Then

[
v_x=\frac{dx}{t},
\qquad
v_y=\frac{dy}{t}+kt.
]

Squaring and adding gives

\frac{r^2}{t^2}+2kdy+k^2t^2.
]

The only variable part is

[
\frac{r^2}{t^2}+k^2t^2.
]

This expression is minimized when

[
t^2=\frac{r}{k}=\frac{2r}{9.80665}.
]

So instead of searching for a feasible time, we deliberately choose the time that gives the smallest possible initial speed. The problem guarantees that some feasible trajectory exists, so the minimum possible speed is also at most (v_{\max}). This gives us a valid trajectory immediately.

The minimum speed can also be written as

# 2kr+2kdy

9.80665(r+dy).
]

Since (r\ge |dy|), the expression is never negative. The horizontal displacement does not need a separate treatment, except for the degenerate case (r=0).

This is the entire optimization: minimize the required initial speed over the flight time, then use that minimizing time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(1/\varepsilon)) per test case | (O(1)) | Too slow for the required precision |
| Optimal | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Compute the displacement

[
dx=x_1-x_0,\qquad dy=y_1-y_0
]

and its Euclidean length

[
r=\sqrt{dx^2+dy^2}.
]

The displacement is the only geometric information needed after the starting point has been subtracted from the target.

1. If (r=0), output (v_x=v_y=t=0).

The ball already starts at the target, so no movement is required. This case must be separated because the general formula divides by (t).

1. Set (k=9.80665/2), corresponding to the magnitude of the gravitational acceleration divided by two in the trajectory equation.

For a chosen positive time (t), the required initial velocity is

[
v_x=\frac{dx}{t},
\qquad
v_y=\frac{dy}{t}+kt.
]

1. Choose

[
t=\sqrt{\frac{r}{k}}.
]

This minimizes the squared speed. To see why, the variable part of the squared speed is

[
\frac{r^2}{t^2}+k^2t^2.
]

The first term decreases as (t) grows, while the second increases. Their balance occurs when

[
\frac{r^2}{t^2}=k^2t^2,
]

which gives (t^2=r/k).

1. Compute

[
v_x=\frac{dx}{t}
]

and

[
v_y=\frac{dy}{t}+kt.
]

These values are constructed directly from the target equation, so substituting them back into the trajectory reaches (Q) at exactly the chosen time.

1. Print the three values with plenty of digits.

Although the statement describes the output as three decimals, the sample itself prints more digits, and the judge checks numerical validity rather than exact textual equality. Printing ten or twelve decimal places keeps the numerical error comfortably below the required tolerance.

Why it works: for every positive (t), the two velocity formulas are the unique initial velocity that reaches (Q) at time (t). Among all such velocities, the chosen (t=\sqrt{r/k}) minimizes the speed. Since the statement guarantees that at least one trajectory has speed at most (v_{\max}), this minimum-speed trajectory also satisfies the speed bound. The degenerate (P=Q) case is handled directly with the zero-time trajectory.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

G = 9.80665
K = G / 2.0

def solve():
    out = []

    for line in sys.stdin:
        if not line.strip():
            continue

        x0, y0, x1, y1, vmax = map(float, line.split())

        dx = x1 - x0
        dy = y1 - y0

        r = math.hypot(dx, dy)

        if r == 0.0:
            out.append("0.0000000000 0.0000000000 0.0000000000")
            continue

        t = math.sqrt(r / K)

        vx = dx / t
        vy = dy / t + K * t

        out.append(f"{vx:.12f} {vy:.12f} {t:.12f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The constants section stores (9.80665/2) as `K`, matching the (\frac12gt^2) term in the official trajectory equation.

The displacement is computed before anything involving time. This keeps the derivation independent of the absolute coordinates, which can be as large as (200) in either direction.

`math.hypot(dx, dy)` computes the distance without manually writing the square root expression. With the given bounds there is no overflow concern, but `hypot` is also a clean numerical implementation of the Euclidean distance.

The `r == 0.0` check is safe here because the input coordinates are integers. Thus (r=0) happens exactly when both points have identical coordinates, rather than because of a tiny floating-point approximation.

For every nonzero displacement, `t = sqrt(r / K)` is the minimizing time derived above. Once `t` is known, the velocity components follow directly from the two coordinate equations. There are no loops whose length depends on the coordinate values, and there is no binary search or iteration that could accumulate numerical error.

The code prints twelve digits after the decimal point. This is more precise than the nominal formatting requirement and gives the checker enough information to evaluate the trajectory with an error far below (10^{-6}).

## Worked Examples

The supplied sample is

```
0 0 10 0 15
```

Here the displacement is horizontal, so (dx=10), (dy=0), and (r=10).

| Variable | Value |
| --- | --- |
| (dx) | (10) |
| (dy) | (0) |
| (r) | (10) |
| (k) | (4.903325) |
| (t=\sqrt{r/k}) | approximately (1.428) |
| (v_x=dx/t) | approximately (7.002) |
| (v_y=dy/t+kt) | approximately (7.002) |

The resulting initial speed is approximately (9.903), which is below the allowed (15). The official sample prints a different valid trajectory, approximately ((6.342,7.732)) at time (1.577), because the problem accepts any trajectory satisfying the constraints.

For a second example, consider

```
0 10 0 0 0
```

The target is directly below the starting point.

| Variable | Value |
| --- | --- |
| (dx) | (0) |
| (dy) | (-10) |
| (r) | (10) |
| (k) | (4.903325) |
| (t=\sqrt{r/k}) | approximately (1.428) |
| (v_x) | (0) |
| (v_y) | approximately (0) |

Gravity alone moves the ball downward by

[
\frac12gt^2=4.903325\cdot\frac{10}{4.903325}=10.
]

Thus the ball reaches the target with zero initial velocity, exactly matching the (v_{\max}=0) constraint. This example also shows why the method does not need a special formula for vertical motion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) per test case | A fixed number of arithmetic operations and one square root are used |
| Space | (O(1)) excluding output storage | Only a constant number of floating-point variables are required |

The coordinate bounds make every arithmetic quantity small, and each test case takes constant time. Even a very large number of test cases is processed with only a few floating-point operations per line, so the method easily fits the one-second and 256 MB limits.

## Test Cases

Because the problem is special judged, the test harness should not compare the output text with one exact string. Instead, it should verify the mathematical conditions directly. This also correctly handles the fact that the sample output is only one of many valid answers.

```python
import sys
import io
import math

G = 9.80665
K = G / 2.0

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        out = []

        for line in sys.stdin:
            if not line.strip():
                continue

            x0, y0, x1, y1, vmax = map(float, line.split())

            dx = x1 - x0
            dy = y1 - y0
            r = math.hypot(dx, dy)

            if r == 0.0:
                out.append("0.0000000000 0.0000000000 0.0000000000")
                continue

            t = math.sqrt(r / K)
            vx = dx / t
            vy = dy / t + K * t

            out.append(f"{vx:.12f} {vy:.12f} {t:.12f}")

        print("\n".join(out))

        return output.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def check_case(inp: str):
    lines = inp.strip().splitlines()
    result = solve_data(inp).strip().splitlines()

    assert len(result) == len(lines)

    for original, produced in zip(lines, result):
        x0, y0, x1, y1, vmax = map(float, original.split())
        vx, vy, t = map(float, produced.split())

        assert t >= 0.0

        speed_sq = vx * vx + vy * vy
        assert vmax * vmax - speed_sq > -1e-6

        bx = x0 + vx * t
        by = y0 + vy * t - K * t * t

        assert abs(bx - x1) <= 1e-6
        assert abs(by - y1) <= 1e-6

# Provided sample.
check_case("0 0 10 0 15")

# Same starting and target point, including vmax = 0.
check_case("0 0 0 0 0")

# Pure vertical drop with zero initial velocity.
check_case("0 10 0 0 0")

# Pure vertical upward displacement.
check_case("0 0 0 10 20")

# Large coordinate differences and a generous speed limit.
check_case("-200 -200 200 200 200")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0 0` | `0 0 0` is valid | Coincident points and zero allowed speed |
| `0 10 0 0 0` | Approximately `0 0 1.428` | Gravity-only downward motion |
| `0 0 0 10 20` | Approximately `0 14.005 1.428` | Pure upward displacement |
| `-200 -200 200 200 200` | A valid nonzero trajectory | Maximum coordinate magnitude and diagonal displacement |

## Edge Cases

For coincident points, the exact input

```
0 0 0 0 0
```

gives (r=0). The general construction would try to use (t=\sqrt{r/k}=0) and then divide by (t), so the implementation returns the zero vector and zero time before performing those divisions. Substituting these values into the trajectory gives (B(0)=P=Q), and the speed is exactly zero.

For a gravity-only drop, consider

```
0 10 0 0 0
```

Here (r=10), so

[
t=\sqrt{\frac{10}{4.903325}}\approx1.428.
]

The vertical velocity becomes

[
v_y=\frac{-10}{t}+4.903325t\approx0.
]

The ball therefore reaches the point ten meters below it with no initial velocity. A method that assumes (v_y) must be positive would incorrectly reject this valid trajectory.

For an upward target,

```
0 0 0 10 20
```

the same time is approximately (1.428), but now

[
v_y=\frac{10}{t}+4.903325t\approx14.005.
]

The initial speed is about (14.005), comfortably below (20). The sign of (dy) naturally determines the sign and magnitude of the vertical component, so no separate upward-motion formula is needed.

Finally, the supplied sample

```
0 0 10 0 15
```

has a horizontal displacement of (10) meters. The minimizing trajectory produced by this solution uses approximately (v_x=v_y=7.002) and (t=1.428), with speed approximately (9.903<15). The sample's published answer uses another valid trajectory, which is why a test harness must verify the physics rather than compare the three printed numbers character by character.
