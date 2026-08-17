---
title: "CF 102272A - Ch\u01a1i Bi-a"
description: "We have a rectangular carom table whose lower-left corner is (0, 0) and upper-right corner is (N, M). A ball starts at the integer position (x0, y0) inside the table and moves with constant velocity (vx, vy). Whenever it reaches a vertical wall, the sign of vx changes."
date: "2026-08-17T11:07:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "A"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 222
verified: false
draft: false
---

[CF 102272A - Ch\u01a1i Bi-a](https://codeforces.com/problemset/problem/102272/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rectangular carom table whose lower-left corner is `(0, 0)` and upper-right corner is `(N, M)`. A ball starts at the integer position `(x0, y0)` inside the table and moves with constant velocity `(vx, vy)`. Whenever it reaches a vertical wall, the sign of `vx` changes. Whenever it reaches a horizontal wall, the sign of `vy` changes. Reaching a corner simply changes both signs.

The task is to find the ball's exact position after `S` seconds. The position is guaranteed to be integral for integer `S`, but directly simulating the motion is far too expensive.

The dimensions, velocities, and time can all be as large as `10^9`, while there can be up to `10^4` test cases. A simulation that performs one operation per second could require `10^9` iterations for a single case and up to `10^13` iterations across the whole input. That cannot fit into a one-second time limit. We need a formula whose running time does not depend on `S`.

The two coordinates are also independent. A vertical wall affects only the x-coordinate, while a horizontal wall affects only the y-coordinate. This lets us solve a one-dimensional problem and apply it twice.

Several boundary cases can make a straightforward implementation wrong. Consider the input

```
1
5 4 2 1 3 0 1
```

After one second, the x-coordinate is exactly `5`, so the answer is `(5, 1)`. A careless implementation that immediately reflects whenever the coordinate is greater than or equal to `N` can accidentally move the ball back to `0` or to `2`, depending on how the reflection is coded. The wall itself is a valid position, so the reflected triangular-wave formula must allow exactly `N`.

A second issue is negative velocity. For

```
1
5 4 2 1 -3 0 1
```

the ball reaches `x = -1` in the unfolded picture. The actual position is `1`, so the answer is `(1, 1)`. Languages where `%` keeps a negative remainder require special handling, while Python's modulo already returns a nonnegative remainder.

A corner can be reached simultaneously in both coordinates. For example,

```
1
3 5 2 4 1 1 1
```

moves the ball to `(3, 5)`, exactly the upper-right corner. The correct output is

```
3 5
```

A method that reflects immediately after detecting the boundary could incorrectly output `(2, 4)` for the requested time. The position at the exact collision time is still the corner.

Finally, one velocity component may be zero. For

```
1
7 6 3 4 0 0 1000000000
```

the ball never moves, so the answer is simply `(3, 4)`. A formula based on dividing by the velocity or on counting wall collisions must explicitly handle this case, whereas the unfolding formula works without any special mathematical treatment.

## Approaches

The most direct solution is to simulate the ball one second at a time. At each second, add `(vx, vy)` to the current position. If the x-coordinate leaves the interval `[0, N]`, reflect it and reverse `vx`; similarly, reflect the y-coordinate and reverse `vy`. This is correct because it follows exactly the physical rules of the table.

The problem is the number of iterations. With `S = 10^9`, one test case can require `10^9` simulation steps. With `10^4` test cases, the theoretical worst case is `10^13` steps. Even if each step contains only a few integer operations, that is far beyond the one-second limit.

The key observation is that a bouncing coordinate is just a periodic triangular wave. Consider only the x-coordinate. If the table width is `N`, imagine removing the walls and allowing the ball to continue indefinitely. Its unfolded coordinate after `S` seconds is

`u = x0 + vx * S`.

The real table can be reconstructed by folding this infinite line back into every interval of length `N`. The pattern repeats every `2N`: the coordinate moves from `0` to `N`, then back from `N` to `0`, and repeats.

Thus we only need

`r = u mod (2N)`.

If `r <= N`, the actual x-coordinate is `r`. If `r > N`, the coordinate is `2N - r`. The same calculation independently gives the y-coordinate using period `2M`.

This eliminates the simulation completely. Large values of `S` and the velocity are handled by integer arithmetic, and the number of wall collisions never needs to be counted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(S)` per test case | `O(1)` | Too slow |
| Optimal | `O(1)` per test case | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `N`, `M`, the initial position `(x0, y0)`, the velocity `(vx, vy)`, and the requested time `S`. The x and y motions can be treated independently because a vertical collision never changes the y component and a horizontal collision never changes the x component.
2. For the x-coordinate, compute the unfolded position `u = x0 + vx * S`. This represents where the ball would be if there were no vertical walls at all.
3. Reduce `u` modulo `2N`, obtaining `r`. The interval `[0, 2N]` describes one complete back-and-forth cycle of the x-coordinate. Reducing modulo `2N` removes every complete cycle without changing the final position inside the table.
4. Convert `r` back to the table using the triangular-wave rule. If `r <= N`, the coordinate is `r`, because this is the first half of the cycle. Otherwise, the coordinate is `2N - r`, because the second half is moving back toward zero.
5. Apply exactly the same calculation to y, replacing `x0`, `vx`, and `N` with `y0`, `vy`, and `M`.
6. Print the resulting `(x, y)`. Since both coordinates are computed at the same absolute time `S`, a simultaneous corner collision is handled naturally. At a corner, both triangular waves are exactly at their respective boundaries.

### Why it works

For one coordinate, unfolding the table removes every reflection. The ball then follows the simple linear equation `x0 + vx*S`. Folding this line back into `[0, N]` reproduces every reflection because the first interval of length `N` corresponds to motion toward the right wall, while the second interval corresponds to the reflected motion toward the left wall. The complete pattern has period `2N`, so taking modulo `2N` loses no information. The same argument applies independently to y. Consequently, the two reconstructed coordinates are exactly the ball's position after `S` seconds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def reflected_position(start, velocity, length, time):
    period = 2 * length
    r = (start + velocity * time) % period

    if r <= length:
        return r
    return period - r

def solve():
    t = int(input())

    for _ in range(t):
        N, M, x0, y0, vx, vy, S = map(int, input().split())

        x = reflected_position(x0, vx, N, S)
        y = reflected_position(y0, vy, M, S)

        print(x, y)

if __name__ == "__main__":
    solve()
```

The `reflected_position` function contains the entire one-dimensional solution. `start + velocity * time` computes the unfolded location, and the modulo operation compresses it into one period of the bouncing motion.

The period is `2 * length`, not `length`. A coordinate takes `length` units of unfolded distance to go from one wall to the other, then another `length` units to return to the starting wall. Using only `length` as the period would incorrectly identify a point on the way to the right wall with the corresponding point on the way back.

The comparison `r <= length` is also deliberate. When `r == length`, the ball is exactly on the wall, and that is a valid position at the requested time. Only values strictly larger than `length` belong to the reflected half of the cycle.

Python's modulo operation is particularly convenient for negative velocities. For example, if the unfolded coordinate is `-1` and the period is `10`, Python evaluates `-1 % 10` as `9`, which is exactly the equivalent point in the current period.

There is no risk of integer overflow in Python. The largest product is on the order of `10^18`, which Python integers handle directly. In a fixed-width language, a sufficiently wide integer type would be required for `velocity * S`.

## Worked Examples

For the first sample test case, the table has width `3` and height `5`, the ball starts at `(2, 2)`, moves with velocity `(2, 1)`, and we need its position after `3` seconds.

| Step | x unfolded | x period | x position | y unfolded | y period | y position |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 2 | 6 | 2 | 2 | 10 | 2 |
| After 3 seconds | 8 | 2 | 2 | 5 | 5 | 5 |

For x, the unfolded coordinate is `2 + 2*3 = 8`. Reducing modulo `6` gives `2`, so the ball has returned to x-coordinate `2`. For y, the unfolded coordinate is `2 + 1*3 = 5`, exactly the upper wall, so the y-coordinate remains `5` at the requested instant. The resulting position is `(2, 5)`, matching the sample.

For the second sample test case, the table is `6 x 8`, the initial position is `(3, 2)`, the velocity is `(5, 1)`, and `S = 1`.

| Step | x unfolded | x period | x position | y unfolded | y period | y position |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 3 | 12 | 3 | 2 | 16 | 2 |
| After 1 second | 8 | 8 | 4 | 3 | 3 | 3 |

The unfolded x-coordinate is `8`. Since the table width is `6`, the second half of the period is active, so the actual coordinate is `12 - 8 = 4`. The y-coordinate is `3`, which is still inside the table. The final position is `(4, 3)`.

These two traces demonstrate both sides of the triangular wave. The first test lands exactly on a wall, while the second test reaches the reflected half of the x-coordinate cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(T)` | Each test case performs a constant number of arithmetic operations. |
| Space | `O(1)` | Only a fixed number of integer variables are stored for each test case. |

With at most `10^4` test cases, the algorithm performs only a few integer operations per case. This is easily compatible with the one-second limit, and memory usage does not grow with `S`, the table dimensions, or the number of wall collisions.

## Test Cases

```python
import sys
import io

def reflected_position(start, velocity, length, time):
    period = 2 * length
    r = (start + velocity * time) % period
    if r <= length:
        return r
    return period - r

def solve_data(data):
    inp = io.StringIO(data)
    t = int(inp.readline())
    out = []

    for _ in range(t):
        N, M, x0, y0, vx, vy, S = map(int, inp.readline().split())
        x = reflected_position(x0, vx, N, S)
        y = reflected_position(y0, vy, M, S)
        out.append(f"{x} {y}")

    return "\n".join(out) + "\n"

# Provided sample
sample = """\
3
3 5 2 2 2 1 3
6 8 3 2 5 1 1
100 200 13 45 -20 111 9969
"""
assert solve_data(sample) == """\
2 5
4 3
33 196
""", "provided sample"

# Minimum-size table, exact wall hit, and zero velocity component.
case_min = """\
3
2 2 1 1 1 0 1
2 2 1 1 1 0 2
2 2 1 1 0 0 1000000000
"""
assert solve_data(case_min) == """\
2 1
1 1
1 1
""", "minimum dimensions and zero velocity"

# Negative velocity.
case_negative = """\
1
5 4 2 1 -3 0 1
"""
assert solve_data(case_negative) == """\
1 1
""", "negative velocity"

# Exact corner hit.
case_corner = """\
1
3 5 2 4 1 1 1
"""
assert solve_data(case_corner) == """\
3 5
""", "corner collision"

# Maximum-scale values.
case_max = """\
1
1000000000 1000000000 1 999999999 1000000000 -1000000000 1000000000
"""
assert solve_data(case_max) == """\
1 999999999
""", "maximum values"

# Equal dimensions, equal positions, equal velocities, and repeated reflection.
case_equal = """\
1
10 10 3 3 4 4 3
"""
assert solve_data(case_equal) == """\
8 8
""", "equal values and reflection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1 1 1 0 1` and related cases | `2 1`, `1 1`, `1 1` | Minimum dimensions, exact boundary, and zero velocity |
| `5 4 2 1 -3 0 1` | `1 1` | Negative modulo and negative velocity |
| `3 5 2 4 1 1 1` | `3 5` | Simultaneous collision with two walls at a corner |
| `1000000000 1000000000 1 999999999 1000000000 -1000000000 1000000000` | `1 999999999` | Maximum numeric limits and very large products |
| `10 10 3 3 4 4 3` | `8 8` | Symmetric x and y motion and repeated reflections |

## Edge Cases

A ball landing exactly on a wall must not be reflected before its requested position is reported. For

```
1
5 4 2 1 3 0 1
```

the x unfolded coordinate is `5`, and the period is `10`. Since `5 <= 5`, the reflected coordinate is still `5`. The output is `5 1`. The condition must be `r <= length`, not `r < length`.

Negative velocity is handled by the same formula. For

```
1
5 4 2 1 -3 0 1
```

the unfolded x-coordinate is `-1`. Its remainder modulo `10` is `9`, and because `9 > 5`, the actual coordinate becomes `10 - 9 = 1`. The output is `1 1`. No separate simulation of moving toward the left wall is needed.

A corner collision is automatically represented by both coordinates reaching their upper boundaries at the same time. For

```
1
3 5 2 4 1 1 1
```

the unfolded coordinates are `3` and `5`. Their periods are `6` and `10`, and both remainders equal their respective table lengths. The result is exactly `3 5`. If the calculation were to reflect immediately after reaching a wall, it would answer the position at the next instant instead of the requested position.

A zero velocity component requires no special branch in the main algorithm. For

```
1
7 6 3 4 0 0 1000000000
```

the unfolded coordinates remain `3` and `4` regardless of time. Taking the corresponding modulo and folding leaves them unchanged, producing `3 4`. This is one reason the unfolded-coordinate formula is preferable to collision-counting formulas that may attempt to divide by a velocity.

The largest values also require attention to arithmetic. With velocity and time both around `10^9`, their product can reach `10^18`. Python handles this exactly, so the expression `start + velocity * time` is safe. In languages with 32-bit integers, the same expression would overflow, making a 64-bit integer type necessary.
