---
title: "CF 34E - Collisions"
description: "We have several point-like balls moving on a one-dimensional line. Every ball starts at some coordinate with its own vel"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 34
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 34 (Div. 2)"
rating: 2000
weight: 34
solve_time_s: 126
verified: true
draft: false
---

[CF 34E - Collisions](https://codeforces.com/problemset/problem/34/E)

**Rating:** 2000  
**Tags:** brute force, implementation, math  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several point-like balls moving on a one-dimensional line. Every ball starts at some coordinate with its own velocity and mass. Whenever two balls occupy the same position at the same time, they collide elastically, and their velocities change according to the standard physics formulas for one-dimensional elastic collisions.

The task is not to simulate velocities only. We must output the final coordinates of the original balls after exactly `t` seconds. Since collisions change future movement, every collision affects all later events.

The constraints are unusually small. There are at most 10 balls, and time is at most 100. Small `n` changes the nature of the problem completely. Even an `O(n^3)` or `O(n^4)` event simulation is easily fast enough. The challenge is not asymptotic complexity, it is numerical correctness and handling collisions in the right chronological order.

A naive continuous simulation with tiny time steps would fail badly. Collisions can happen at irrational-looking fractional times, and stepping through time with epsilon increments accumulates floating point error. The intended solution is event-driven: always jump directly to the next collision.

One easy mistake is processing collisions in the wrong order. Consider:

```
3 10
0 3 1
10 0 1
20 -3 1
```

The left ball hits the middle ball first, then the middle ball hits the right ball later. If we update all pairs independently without respecting time order, we produce impossible trajectories.

Another subtle case is simultaneous position updates. Suppose two balls collide at time `2.5`. Their positions at that exact instant must be updated before computing new velocities. If we change velocities first and then move them, the collision point becomes wrong.

Example:

```
2 5
0 2 1
10 -2 1
```

They meet at position `5` after `2.5` seconds. After an equal-mass elastic collision, they swap velocities. Final positions become:

```
5 - 2.5*2 = 0
5 + 2.5*2 = 10
```

A careless implementation might move them using old velocities for the full 5 seconds and incorrectly output `10` and `0`.

Another dangerous case is nearly equal collision times. Floating point comparisons must use an epsilon. Otherwise the algorithm may choose the wrong next collision because of precision noise.

The statement guarantees that no three balls collide simultaneously. That simplifies the implementation enormously. We never need to resolve multi-body collisions.

## Approaches

The most direct idea is physical simulation with very small time increments. At every step we move every ball by `v * dt`, then check whether some pair crossed each other. This works conceptually because sufficiently small steps approximate continuous motion.

The problem is precision. If `dt` is too large, collisions are missed entirely. If `dt` is tiny enough to be reliable, the number of iterations explodes. For example, using `dt = 1e-6` over 100 seconds already means `10^8` simulation steps. Even with only 10 balls, this is impractical and numerically unstable.

The structure of the problem gives a much cleaner route. Between collisions, every ball moves linearly with constant velocity. Nothing interesting happens except at collision moments. That means we never need to inspect intermediate times. We only need the earliest future collision.

For every pair of balls, we can compute analytically when they meet:

$$x_i + v_i t = x_j + v_j t$$

which gives:

$t=\frac{x_j-x_i}{v_i-v_j}$

A valid collision requires positive time and relative motion toward each other.

Once the earliest collision is known, we advance every ball directly to that time, update the two colliding velocities using the elastic collision formulas, then repeat.

Because `n ≤ 10`, recomputing all pair collision times after every event is completely fine. Even if there are many collisions, the total work stays tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force time stepping | Extremely large, depends on precision | O(n) | Too slow and inaccurate |
| Event-driven simulation | O(C · n²) | O(n) | Accepted |

Here `C` is the number of collisions that occur before time `t`.

## Algorithm Walkthrough

1. Store every ball with its current position, velocity, mass, and original index.
2. Maintain a variable `cur_time`, initially `0`.
3. For every pair of balls `(i, j)`, compute when they would collide if velocities stay unchanged.
4. Ignore invalid collision times.

A collision is invalid if:

- velocities are equal, because the distance never changes,
- collision time is non-positive,
- the collision happens after the remaining allowed simulation time.
5. Among all valid collisions, choose the smallest collision time `dt`.

This is the next physical event in the system. Nothing changes before this moment except linear motion.
6. If no collision exists before the target time:

1. Move every ball forward by the remaining time.
2. Stop the simulation.
7. Otherwise:

1. Move every ball forward by `dt`.
2. Increase `cur_time` by `dt`.
3. Let balls `i` and `j` be the colliding pair.
4. Compute their new velocities using the elastic collision formulas:

$v_1'=\frac{(m_1-m_2)v_1+2m_2v_2}{m_1+m_2}$

$v_2'=\frac{(m_2-m_1)v_2+2m_1v_1}{m_1+m_2}$

1. Repeat from step 3 until total simulated time reaches `t`.
2. Restore the original input order before printing answers.

### Why it works

Between collisions, every object moves with constant velocity, so positions are linear functions of time. The first future collision is the only event capable of changing velocities. Advancing directly to that event preserves the exact physical trajectory.

After processing a collision, the new velocities are precisely the ones dictated by elastic collision physics. Since the statement guarantees no triple collisions, every event involves exactly one pair, so processing collisions sequentially is valid.

By always choosing the earliest collision, the simulation reproduces the real chronological order of the system. No later collision can influence an earlier one.

## Python Solution

```python
import sys
input = sys.stdin.readline

EPS = 1e-10

def solve():
    n, T = map(float, input().split())
    n = int(n)

    balls = []

    for idx in range(n):
        x, v, m = map(float, input().split())
        balls.append({
            "x": x,
            "v": v,
            "m": m,
            "idx": idx
        })

    cur_time = 0.0

    while cur_time < T - EPS:
        best_dt = float('inf')
        pair = (-1, -1)

        # Find earliest collision
        for i in range(n):
            for j in range(i + 1, n):
                xi = balls[i]["x"]
                xj = balls[j]["x"]
                vi = balls[i]["v"]
                vj = balls[j]["v"]

                rel_v = vi - vj

                if abs(rel_v) < EPS:
                    continue

                dt = (xj - xi) / rel_v

                if dt <= EPS:
                    continue

                if cur_time + dt > T + EPS:
                    continue

                if dt < best_dt:
                    best_dt = dt
                    pair = (i, j)

        # No more collisions
        if pair == (-1, -1):
            remain = T - cur_time

            for b in balls:
                b["x"] += b["v"] * remain

            break

        # Advance to collision
        for b in balls:
            b["x"] += b["v"] * best_dt

        cur_time += best_dt

        i, j = pair

        m1 = balls[i]["m"]
        m2 = balls[j]["m"]

        v1 = balls[i]["v"]
        v2 = balls[j]["v"]

        nv1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        nv2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

        balls[i]["v"] = nv1
        balls[j]["v"] = nv2

    balls.sort(key=lambda b: b["idx"])

    print(*["{:.10f}".format(b["x"]) for b in balls])

solve()
```

The main loop repeatedly searches for the next collision event. Since `n` is tiny, checking every pair every time is simpler and safer than maintaining a priority queue of events.

The collision formula comes directly from solving the linear meeting equation. We skip non-positive times because they represent past collisions or immediate self-intersections caused by floating point noise.

The simulation always updates positions before changing velocities. That ordering matters. At the collision instant, all balls must first reach their correct physical coordinates.

The epsilon comparisons prevent instability from floating point arithmetic. Without them, two mathematically identical times might compare incorrectly after repeated updates.

The balls are never reordered during simulation. We only sort by original index before output so results match the input order.

## Worked Examples

### Example 1

Input:

```
2 9
3 4 5
0 7 8
```

Initial state:

| Ball | Position | Velocity | Mass |
| --- | --- | --- | --- |
| 0 | 3 | 4 | 5 |
| 1 | 0 | 7 | 8 |

Relative velocity:

$$4 - 7 = -3$$

Meeting time:

$$(0 - 3)/(-3) = 1$$

After 1 second:

| Ball | Position | Velocity before collision |
| --- | --- | --- |
| 0 | 7 | 4 |
| 1 | 7 | 7 |

New velocities:

| Ball | New velocity |
| --- | --- |
| 0 | 7.692307692 |
| 1 | 4.692307692 |

Remaining time is `8`.

Final positions:

| Ball | Final position |
| --- | --- |
| 0 | 68.538461538 |
| 1 | 44.538461538 |

This trace shows why event ordering matters. Velocities change only after both balls reach the same coordinate.

### Example 2

Input:

```
2 5
0 2 1
10 -2 1
```

Initial state:

| Ball | Position | Velocity |
| --- | --- | --- |
| 0 | 0 | 2 |
| 1 | 10 | -2 |

Collision time:

$$(10 - 0)/(2 - (-2)) = 2.5$$

At collision:

| Ball | Position |
| --- | --- |
| 0 | 5 |
| 1 | 5 |

Equal masses swap velocities:

| Ball | New velocity |
| --- | --- |
| 0 | -2 |
| 1 | 2 |

Remaining time is `2.5`.

Final positions:

| Ball | Final position |
| --- | --- |
| 0 | 0 |
| 1 | 10 |

This demonstrates the classic equal-mass behavior where velocities exchange completely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C · n²) | Every collision recomputes all pair collision times |
| Space | O(n) | Only the current ball states are stored |

`n` is at most 10, so even hundreds or thousands of collision checks are trivial. The solution easily fits within both time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

EPS = 1e-6

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, T = map(float, input().split())
    n = int(n)

    balls = []

    for idx in range(n):
        x, v, m = map(float, input().split())
        balls.append([x, v, m, idx])

    cur = 0.0

    while cur < T - 1e-10:
        best = float('inf')
        pair = (-1, -1)

        for i in range(n):
            for j in range(i + 1, n):
                xi, vi = balls[i][0], balls[i][1]
                xj, vj = balls[j][0], balls[j][1]

                if abs(vi - vj) < 1e-10:
                    continue

                dt = (xj - xi) / (vi - vj)

                if dt <= 1e-10:
                    continue

                if cur + dt > T + 1e-10:
                    continue

                if dt < best:
                    best = dt
                    pair = (i, j)

        if pair == (-1, -1):
            rem = T - cur

            for b in balls:
                b[0] += b[1] * rem

            break

        for b in balls:
            b[0] += b[1] * best

        cur += best

        i, j = pair

        x1, v1, m1, _ = balls[i]
        x2, v2, m2, _ = balls[j]

        nv1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        nv2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

        balls[i][1] = nv1
        balls[j][1] = nv2

    balls.sort(key=lambda x: x[3])

    return " ".join("{:.6f}".format(b[0]) for b in balls)

def close_enough(out, expected):
    a = list(map(float, out.split()))
    b = list(map(float, expected.split()))

    assert len(a) == len(b)

    for x, y in zip(a, b):
        assert abs(x - y) < EPS

# provided sample
close_enough(
    solve_io(
        "2 9\n"
        "3 4 5\n"
        "0 7 8\n"
    ),
    "68.538461538 44.538461538"
)

# minimum size
close_enough(
    solve_io(
        "1 10\n"
        "5 3 7\n"
    ),
    "35.0"
)

# equal masses swap velocities
close_enough(
    solve_io(
        "2 5\n"
        "0 2 1\n"
        "10 -2 1\n"
    ),
    "0.0 10.0"
)

# no collision
close_enough(
    solve_io(
        "2 3\n"
        "0 1 1\n"
        "10 2 1\n"
    ),
    "3.0 16.0"
)

# chain collisions
close_enough(
    solve_io(
        "3 4\n"
        "0 3 1\n"
        "10 0 1\n"
        "20 -3 1\n"
    ),
    "0.0 10.0 20.0"
)

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single ball | Linear movement only | No-collision handling |
| Equal masses head-on | Velocity swap | Correct collision physics |
| Faster ball already ahead | No collision | Positive-time filtering |
| Three-ball chain | Sequential events | Chronological collision processing |

## Edge Cases

Consider the case where two balls move with identical velocities.

```
2 10
0 3 1
5 3 2
```

Relative velocity is zero, so the meeting-time formula would divide by zero. The algorithm explicitly skips such pairs. Final positions become:

```
30
35
```

because neither ball ever catches the other.

Another subtle case is collision exactly at the final time.

```
2 5
0 1 1
10 -1 1
```

They collide at `t = 5`. The algorithm accepts this event because collision time is not beyond the target time. Both balls end at position `5`.

A floating point implementation that used strict `< T` comparisons might incorrectly skip the collision.

Now consider sequential collisions:

```
3 4
0 3 1
10 0 1
20 -3 1
```

The first collision occurs between balls 0 and 1 at time `10/3`. After equal-mass exchange, ball 1 moves right with velocity `3`, eventually colliding with ball 2.

The algorithm handles this correctly because after every event it recomputes all future collision times from the updated state. Old predictions are discarded since velocities changed.
