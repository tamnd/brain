---
title: "CF 102439A - Four minutes until BSUIR Open"
description: "We have a straight road from position 0 to the university at position (xn). Camera (i) is at position (xi), and when the car passes that point its speed must be at most (vi). The car starts at speed zero."
date: "2026-08-14T15:55:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "A"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 142
verified: true
draft: false
---

[CF 102439A - Four minutes until BSUIR Open](https://codeforces.com/problemset/problem/102439/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a straight road from position 0 to the university at position (x_n). Camera (i) is at position (x_i), and when the car passes that point its speed must be at most (v_i). The car starts at speed zero. It may accelerate with acceleration at most (a), brake with deceleration at most (b), and keep a constant speed.

The input gives the camera positions and their speed limits, together with the two acceleration parameters. The required output is the minimum possible travel time from position 0 to the last camera, which is also the university.

The main difficulty is that a camera restricts the speed only at one position. Between cameras the car may temporarily go much faster than either endpoint speed. For example, if the speed at two consecutive cameras is 1 and 1, the fastest motion does not necessarily stay at speed 1. The car can accelerate above 1, then brake back to 1 before the second camera.

With (n) up to (10^5), an (O(n^2)) algorithm would perform about

[
\frac{10^5(10^5-1)}2 \approx 5\cdot 10^9
]

pairwise checks in the worst case. That is far beyond what a one-second limit can handle. The solution must process every camera a constant number of times.

There are several edge cases that are easy to mishandle. If the only camera has speed limit zero, for example,

```
1 1 1
1 0
```

the correct answer is (2). The car must start from zero and return to zero after travelling one unit, so it accelerates to speed 1 and then brakes to zero. A solution that simply uses (x/v) breaks because the endpoint speed is zero.

An intermediate camera can also force the car to stop. For

```
2 1 1
1 0
2 1
```

the correct answer is approximately (3.4494897428). The first unit requires acceleration and braking back to zero, and only then can the car start accelerating again. Treating every segment as an independent constant-speed movement would fail badly here.

Equal camera limits are another subtle case. Consider

```
2 1 1
1 1
2 1
```

The answer is approximately (1.8989794856). On the second segment the car should accelerate above speed 1 and then brake back to speed 1. Simply travelling both segments at speed 1 gives a slower answer.

Finally, the last camera is the destination, so its speed limit is an endpoint constraint, not merely a restriction before continuing farther. If its limit is zero, the car must finish with speed zero. The backward pass handles that constraint naturally.

## Approaches

A direct approach is to determine, for every camera, how strongly each other camera constrains its speed. For a camera at (x_i), every later camera (j) gives a braking condition

[
u_i^2 \le v_j^2 + 2b(x_j-x_i).
]

A brute-force implementation could inspect every later camera for every (i), take the minimum allowed speed, and then do the analogous work for acceleration from the start. This is correct because every possible future camera is explicitly checked, but it performs (O(n^2)) operations, about (5\cdot10^9) checks when (n=10^5).

The useful observation is that these constraints have a local recurrence. Suppose the maximum speed that can legally be used at camera (i+1) is already known. Then the maximum speed at camera (i) that can still be reduced to that speed over distance (x_{i+1}-x_i) is

[
\sqrt{v_{i+1}^2+2b(x_{i+1}-x_i)}.
]

Any earlier camera has already been summarized by the value stored at (i+1). This means the complete braking restriction can be computed in one backward pass.

The same idea works from the start. If the maximum speed reachable at camera (i-1) is (u), then after travelling distance (d) with acceleration at most (a), the largest reachable speed is

[
\sqrt{u^2+2ad}.
]

Combining this with the camera's own limit gives the maximum speed allowed by all constraints to the left.

Let (F_i) be the maximum speed at camera (i) considering only the start and cameras before it. Let (B_i) be the maximum speed at camera (i) considering only cameras after it and the braking limit. Then the largest speed that is simultaneously compatible with both directions is

[
s_i=\min(F_i,B_i).
]

These speeds are exactly the endpoint speeds we need. Once two consecutive endpoint speeds are fixed, the fastest motion between them has a very simple shape: accelerate at rate (a) up to some peak speed (p), then brake at rate (b) down to the next endpoint speed.

For a segment of length (d), starting at speed (u) and ending at speed (v), the distance travelled during acceleration and braking is

[
d=\frac{p^2-u^2}{2a}+\frac{p^2-v^2}{2b}.
]

Solving for (p^2) gives

[
p^2=
\frac{2abd+bu^2+av^2}{a+b}.
]

The time for this segment is then

[
\frac{p-u}{a}+\frac{p-v}{b}.
]

The endpoint speeds produced by the two passes are mutually reachable, so the resulting (p) is always at least both endpoint speeds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all camera positions (x_i) and limits (v_i). Treat position 0 as an additional point whose speed is fixed at zero.
2. Compute the forward speed limit (F_i). Start with speed zero at position 0. For each camera, calculate the largest speed reachable from the previous forward speed using acceleration (a), then cap it by (v_i):

[
F_i=\min\left(v_i,\sqrt{F_{i-1}^2+2a(x_i-x_{i-1})}\right).
]

This captures every restriction coming from the start and all earlier cameras.

1. Compute the backward speed limit (B_i). Start at the last camera with (B_n=v_n). Move backwards and calculate how fast the car could be at the previous camera while still braking to (B_{i+1}):

[
B_i=\min\left(v_i,\sqrt{B_{i+1}^2+2b(x_{i+1}-x_i)}\right).
]

This compresses all future braking constraints into one value per camera.

1. Define the actual endpoint speed at each camera as

[
s_i=\min(F_i,B_i).
]

The forward value guarantees that the car can reach (s_i) from the start while respecting previous cameras. The backward value guarantees that it can continue from (s_i) to the destination while respecting future cameras.

1. Add position 0 with speed (s_0=0). For every consecutive pair of positions, let the distance be (d=x_i-x_{i-1}), the starting speed be (u=s_{i-1}), and the ending speed be (v=s_i).
2. Find the optimal peak speed from

[
p^2=
\frac{2abd+bu^2+av^2}{a+b}.
]

The car accelerates from (u) to (p), then brakes from (p) to (v). The segment time is

[
t_i=\frac{p-u}{a}+\frac{p-v}{b}.
]

1. Sum all segment times and print the result with sufficient precision.

### Why it works

The forward pass maintains the invariant that (F_i) is the greatest speed attainable at camera (i) while satisfying every camera from the start through (i). The recurrence follows directly from (v^2=u^2+2ad).

The backward pass maintains the symmetric invariant that (B_i) is the greatest speed permitted at camera (i) while still being able to satisfy every camera from (i) to the destination. Its recurrence follows from the braking relation (u^2=v^2+2bd).

Thus (s_i=\min(F_i,B_i)) is the greatest speed at every camera that is feasible in both directions. Using a larger endpoint speed would violate either a previous acceleration constraint or a future braking constraint. Using a smaller endpoint speed cannot improve the travel time, because the fastest segment between fixed positions has nondecreasing benefit from allowing larger feasible endpoint speeds.

For two fixed endpoint speeds, any time spent accelerating below (a) or braking below (b) can be replaced by faster acceleration or braking without violating the endpoint conditions. Hence an optimal segment consists of maximum acceleration followed by maximum braking. Solving the distance equation gives its unique peak speed, so the segment formula gives the minimum possible time. Summing these optimal segments produces the global optimum.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())

    x = [0] * n
    v = [0] * n

    for i in range(n):
        x[i], v[i] = map(int, input().split())

    # Maximum speed reachable from the start while
    # respecting all cameras seen so far.
    forward = [0.0] * n
    cur = 0.0
    prev_x = 0

    for i in range(n):
        d = x[i] - prev_x
        reachable = math.sqrt(cur * cur + 2.0 * a * d)
        cur = min(float(v[i]), reachable)
        forward[i] = cur
        prev_x = x[i]

    # Maximum speed allowed when looking from the destination backwards.
    backward = [0.0] * n
    backward[-1] = float(v[-1])

    for i in range(n - 2, -1, -1):
        d = x[i + 1] - x[i]
        reachable = math.sqrt(
            backward[i + 1] * backward[i + 1] + 2.0 * b * d
        )
        backward[i] = min(float(v[i]), reachable)

    # The actual feasible maximum speed at each camera.
    speed = [min(forward[i], backward[i]) for i in range(n)]

    ans = 0.0
    prev_speed = 0.0
    prev_x = 0.0

    for i in range(n):
        d = x[i] - prev_x
        cur_speed = speed[i]

        # During the optimal segment:
        #
        # d = (p^2 - u^2)/(2a) + (p^2 - v^2)/(2b)
        #
        # so:
        # p^2 = (2abd + bu^2 + av^2) / (a+b)
        p2 = (
            2.0 * a * b * d
            + b * prev_speed * prev_speed
            + a * cur_speed * cur_speed
        ) / (a + b)

        # Protect against a tiny negative value caused by floating point
        # rounding in cases where the exact value is zero.
        p = math.sqrt(max(0.0, p2))

        ans += (p - prev_speed) / a
        ans += (p - cur_speed) / b

        prev_speed = cur_speed
        prev_x = x[i]

    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The first pass uses `cur` as the best speed currently reachable from the start. The expression `cur * cur + 2.0 * a * d` is the standard constant-acceleration relation, and taking the minimum with the camera limit incorporates the new restriction immediately.

The backward pass starts with the final camera's actual speed limit. Since the destination is exactly the last camera, there is no later position after it, so its backward value is simply `v[-1]`. Every earlier camera is then restricted by how much braking distance is available before the next camera.

The third stage combines the two arrays. A camera can be reachable from the left but impossible to leave safely toward the right, or vice versa. Taking their minimum handles both conditions simultaneously.

The segment calculation is the most delicate part. The peak speed is not necessarily equal to either endpoint speed. Even if two cameras both require speed 1, the car can be faster than 1 between them. The quadratic expression for `p2` accounts for exactly that possibility.

There is no integer overflow issue in Python. The largest intermediate values are comfortably handled by Python integers before conversion to floating point, and the corresponding values are also well within the useful range of a double-precision floating-point number. The `max(0.0, p2)` guard only protects against a microscopic negative value caused by rounding.

## Worked Examples

### Sample 1

The input is

```
2 1 1
1 1
2 2
```

The forward pass starts at zero.

| Camera | Position | Limit | Forward (F_i) | Backward (B_i) | Final speed (s_i) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1.000000 | 1.000000 | 1.000000 |
| 2 | 2 | 2 | 1.732051 | 2.000000 | 1.732051 |

For the first segment, the start and endpoint speeds are 0 and 1. The optimal peak speed is

[
p=\sqrt{1.5}\approx1.224745.
]

The segment takes approximately (1.449490) time units.

For the second segment, the endpoint speeds are 1 and (\sqrt3). The car can accelerate throughout the entire segment, so its peak is (\sqrt3), and this segment takes approximately (0.732051).

| Segment | Distance | Start speed | End speed | Peak speed | Time |
| --- | --- | --- | --- | --- | --- |
| 0 to 1 | 1 | 0.000000 | 1.000000 | 1.224745 | 1.449490 |
| 1 to 2 | 1 | 1.000000 | 1.732051 | 1.732051 | 0.732051 |

The total is approximately (2.1815405), matching the sample output.

### Sample 2

The input is

```
4 1 5
2 3
4 5
7 3
9 5
```

The forward limits are

[
2,\quad 2.828427,\quad 3,\quad 3.605551.
]

The backward limits are

[
3,\quad 4.358899,\quad 3,\quad 5.
]

Taking the minimum gives the actual speeds

[
2,\quad2.828427,\quad3,\quad3.605551.
]

| Segment | Distance | Start speed | End speed | Peak speed | Time |
| --- | --- | --- | --- | --- | --- |
| 0 to 2 | 2 | 0.000000 | 2.000000 | 2.000000 | 2.000000 |
| 2 to 4 | 2 | 2.000000 | 2.828427 | 2.828427 | 0.828427 |
| 4 to 7 | 3 | 2.828427 | 3.000000 | 3.628590 | 0.925880 |
| 7 to 9 | 2 | 3.000000 | 3.605551 | 3.605551 | 0.605551 |

The sum is approximately (4.3598594), which matches the second sample.

The third segment is particularly useful because its peak speed is larger than both endpoint speeds. This is exactly the situation that a solution based only on average speeds or camera speeds would miss.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Two linear passes compute the forward and backward limits, followed by one linear pass for segment times. |
| Space | (O(n)) | The camera data and the forward, backward, and final speed arrays are stored. |

The algorithm performs only a constant number of operations per camera, so (10^5) cameras require only a few hundred thousand arithmetic operations. The memory usage is also linear and easily fits within 256 MB.

## Test Cases

```python
import sys
import io
import math

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, a, b = map(int, sys.stdin.readline().split())

    x = [0] * n
    v = [0] * n

    for i in range(n):
        x[i], v[i] = map(int, sys.stdin.readline().split())

    forward = [0.0] * n
    cur = 0.0
    prev_x = 0

    for i in range(n):
        d = x[i] - prev_x
        cur = min(float(v[i]), math.sqrt(cur * cur + 2.0 * a * d))
        forward[i] = cur
        prev_x = x[i]

    backward = [0.0] * n
    backward[-1] = float(v[-1])

    for i in range(n - 2, -1, -1):
        d = x[i + 1] - x[i]
        backward[i] = min(
            float(v[i]),
            math.sqrt(
                backward[i + 1] * backward[i + 1]
                + 2.0 * b * d
            )
        )

    speed = [min(forward[i], backward[i]) for i in range(n)]

    ans = 0.0
    prev_speed = 0.0
    prev_x = 0.0

    for i in range(n):
        d = x[i] - prev_x
        cur_speed = speed[i]

        p2 = (
            2.0 * a * b * d
            + b * prev_speed * prev_speed
            + a * cur_speed * cur_speed
        ) / (a + b)

        p = math.sqrt(max(0.0, p2))

        ans += (p - prev_speed) / a
        ans += (p - cur_speed) / b

        prev_speed = cur_speed
        prev_x = x[i]

    sys.stdin = old_stdin
    return f"{ans:.10f}"

def assert_close(inp: str, expected: float, eps: float = 1e-8):
    actual = float(solve_io(inp))
    assert abs(actual - expected) <= eps, (actual, expected)

# Provided sample 1
assert_close(
    """\
2 1 1
1 1
2 2
""",
    2.1815405,
    1e-7,
)

# Provided sample 2
assert_close(
    """\
4 1 5
2 3
4 5
7 3
9 5
""",
    4.3598594,
    1e-7,
)

# Minimum-size input, endpoint speed is zero.
assert_close(
    """\
1 1 1
1 0
""",
    2.0,
)

# One camera, endpoint speed is nonzero.
expected = 2.0 * math.sqrt(1.5) - 1.0
assert_close(
    """\
1 1 1
1 1
""",
    expected,
)

# All camera limits are equal.
p = math.sqrt(1.5)
expected = (2.0 * p - 1.0) + 2.0 * (p - 1.0)
assert_close(
    """\
3 1 1
1 1
2 1
3 1
""",
    expected,
)

# Intermediate camera forces a full stop.
expected = 2.0 + (2.0 * math.sqrt(1.5) - 1.0)
assert_close(
    """\
2 1 1
1 0
2 1
""",
    expected,
)

# Maximum-size input with a very simple exact answer.
# Every camera forces speed zero, so every unit segment takes exactly 2 time units.
n = 100000
parts = [f"{n} 1 1"]
parts.extend(f"{i} 0" for i in range(1, n + 1))
max_input = "\n".join(parts) + "\n"
assert_close(max_input, 2.0 * n, 1e-7)

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1 0` | `2` | Minimum input and zero endpoint speed |
| `1 1 1 / 1 1` | `1.4494897428...` | Starting from zero while ending at a positive speed |
| `3 1 1 / 1 1 / 2 1 / 3 1` | `2.3484692289...` | Equal limits and acceleration above the camera speed between cameras |
| `2 1 1 / 1 0 / 2 1` | `3.4494897428...` | An intermediate zero-speed camera |
| `100000 1 1` followed by positions `1..100000`, all with limit `0` | `200000` | Maximum (n), linear-time behavior, and repeated zero constraints |

## Edge Cases

For a final camera with speed limit zero, consider

```
1 1 1
1 0
```

The forward speed is zero because the camera forbids any positive endpoint speed. The backward speed is also zero because this is the destination. Thus the selected endpoint speed is zero. For the single segment,

[
p^2=\frac{2\cdot1\cdot1\cdot1}{2}=1,
]

so (p=1). The acceleration takes one time unit and the braking takes another, giving exactly (2).

For an intermediate zero-speed camera,

```
2 1 1
1 0
2 1
```

both passes select speed zero at the first camera. The first segment has peak speed 1 and takes 2 units of time. The second segment starts at zero and ends at speed 1, giving peak speed (\sqrt{1.5}) and time (2\sqrt{1.5}-1). The total is approximately (3.4494897428). The backward pass is what prevents the algorithm from carrying an illegal positive speed through the first camera.

For equal camera limits,

```
2 1 1
1 1
2 1
```

both camera speeds are selected as 1. On the first segment the peak is (\sqrt{1.5}), so the time is (2\sqrt{1.5}-1). On the second segment the same peak is used, but both endpoints already have speed 1, giving time (2(\sqrt{1.5}-1)). The total is approximately (1.8989794856). This demonstrates why the segment calculation must allow the car to exceed both camera speeds between the cameras.

For a destination with a high speed limit but an earlier restrictive camera, the forward pass can become the active constraint. In Sample 1, the second camera permits speed 2, but only (\sqrt3) is reachable from the first camera at speed 1 over the available distance. The final selected speed is consequently (\sqrt3), not 2. The forward pass prevents the algorithm from assuming that every camera's posted limit is independently attainable.
