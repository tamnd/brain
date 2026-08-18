---
title: "CF 102272A - Ch\u01a1i Bi-a"
description: "We have a rectangular carom table whose horizontal size is (N) and vertical size is (M). The ball starts at the integer position ((x0,y0)), strictly inside the table, and during every second its position changes according to its current velocity ((vx,vy))."
date: "2026-08-19T05:08:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "A"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 375
verified: false
draft: false
---

[CF 102272A - Ch\u01a1i Bi-a](https://codeforces.com/problemset/problem/102272/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We have a rectangular carom table whose horizontal size is (N) and vertical size is (M). The ball starts at the integer position ((x_0,y_0)), strictly inside the table, and during every second its position changes according to its current velocity ((v_x,v_y)). When the ball reaches a vertical wall, the sign of (v_x) changes. When it reaches a horizontal wall, the sign of (v_y) changes. If both happen at the same corner, both signs change.

The task is to find the ball's exact position after (S) seconds. The velocity components can be negative and can be as large as (10^9), while (S) can also be (10^9). There can be up to (10^4) test cases.

The large values immediately rule out simulating the ball one second at a time. A single test could require (10^9) iterations, and (10^4) such tests would give up to (10^{13}) iterations. Even though each iteration is simple, that is far beyond a one second time limit. We need a constant-time calculation for each coordinate.

The two coordinates are independent. The horizontal movement only depends on (N,x_0,v_x,S), and the vertical movement only depends on (M,y_0,v_y,S). So the main problem reduces to understanding one-dimensional motion between two reflecting walls at (0) and (L).

There are several edge cases that can silently break a direct implementation. The first is a ball that lands exactly on a wall. For example,

```
1
3 4 1 2 2 0 1
```

gives the position ((3,2)). The ball reaches the right wall exactly at time (1), so the answer is `3 2`. A careless implementation that immediately changes the position again after detecting a collision can accidentally return `1 2`.

A second case is negative velocity. For example,

```
1
5 4 2 2 -3 -2 1
```

gives the unfolded coordinates (-1) and (0). The reflected positions are (1) and (0), so the correct output is `1 0`. Implementations using a language where `%` keeps the sign of the dividend must normalize negative remainders. Python's `%` already returns a non-negative remainder, so the direct formula is safe.

A third case occurs when both coordinates reach walls at the same time. For example,

```
1
3 3 1 1 2 2 1
```

moves directly to the upper-right corner, giving `3 3`. The corner collision reverses both velocity components, but that reversal affects future movement, not the position at the collision time.

Finally, zero velocity in one coordinate must remain zero. For example,

```
1
2 5 1 3 0 2 3
```

keeps (x=1), while the vertical coordinate moves from (3) to (9) in the unfolded representation. Since (9\bmod 10=9), reflection gives (1), so the answer is `1 1`.

## Approaches

The straightforward solution is to simulate every second. At each step we add the current velocity to the position, check whether either coordinate reached a wall, and reverse the corresponding velocity component. This is correct because it follows exactly the physical rules of the problem.

The problem is the value of (S). In the worst case, one test requires (10^9) simulated seconds. With (10^4) tests, the worst-case operation count is on the order of (10^{13}), which cannot fit in the time limit.

The key observation is that reflection can be removed by imagining a larger, unfolded line. Consider only the (x)-coordinate and let the table width be (N). Instead of reflecting the ball at (0) and (N), imagine that the line continues forever:

[
\ldots,-2N,-N,0,N,2N,3N,\ldots
]

The ball simply travels along this infinite line with its original velocity. Every interval of length (2N) corresponds to one complete back-and-forth motion inside the real table.

After (S) seconds, the unfolded coordinate is

[
p=x_0+v_xS.
]

Only its position modulo (2N) matters. Let

[
r=p\bmod 2N,
]

with (0\le r<2N). If (r\le N), the real coordinate is (r). If (r>N), the ball is on the reflected half of the unfolded interval, so the real coordinate is (2N-r).

Thus the one-dimensional reflection can be calculated in constant time. The exact same formula works independently for (y), replacing (N) with (M).

This is essentially a periodic triangular wave. The bouncing motion has period (2N) in the unfolded coordinate, so modulo (2N) completely captures every possible number of wall collisions without explicitly simulating any of them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(S)) per test | (O(1)) | Too slow |
| Optimal | (O(1)) per test | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N,M,x_0,y_0,v_x,v_y,S). The final position can be calculated independently for the two coordinates, so no collision simulation between them is needed.
2. For the horizontal coordinate, compute the unfolded position

[
p_x=x_0+v_xS.
]

This represents where the ball would be after (S) seconds if the vertical walls did not reflect it.

1. Reduce this position modulo the full unfolded period:

[
r_x=p_x\bmod 2N.
]

Using (2N), rather than (N), is necessary because a movement from (0) to (N) and back to (0) forms the complete repeating pattern.

1. Reflect the reduced coordinate back into the actual table. If (r_x\le N), set (x_S=r_x). Otherwise set

[
x_S=2N-r_x.
]

The same value appears twice at the two ends of the unfolded interval, which correctly represents a wall position.

1. Repeat the same calculation vertically. Compute

[
p_y=y_0+v_yS,
]

then

[
r_y=p_y\bmod 2M,
]

and finally use (r_y) when (r_y\le M), otherwise use (2M-r_y).

1. Print (x_S) and (y_S). The two calculations are independent, including when both coordinates hit walls simultaneously.

### Why it works

For one coordinate, imagine replacing every reflected copy of the table by another copy placed next to it. The ball then travels forever in a straight line with constant velocity. Folding this infinite line back into the original interval exactly reproduces every reflection: crossing a multiple of (N) reverses the direction after folding.

The unfolded pattern repeats every (2N), so two unfolded positions that differ by a multiple of (2N) always fold to the same table coordinate. Taking the position modulo (2N) therefore removes an arbitrary number of complete back-and-forth trips. Folding the remaining value with (r) for the first half and (2N-r) for the second half gives exactly the physical position.

Since the horizontal and vertical coordinates obey the same independent argument, applying the transformation to both coordinates produces the ball's exact position after (S) seconds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def reflected_position(length, start, velocity, seconds):
    period = 2 * length
    pos = (start + velocity * seconds) % period

    if pos <= length:
        return pos
    return period - pos

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m, x0, y0, vx, vy, s = map(int, input().split())

        x = reflected_position(n, x0, vx, s)
        y = reflected_position(m, y0, vy, s)

        out.append(f"{x} {y}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `reflected_position` function contains the entire one-dimensional transformation from the algorithm. First it forms the unfolded position `start + velocity * seconds`. Python integers have arbitrary precision, so the product can safely reach around (10^{18}) without overflow.

The modulo is taken by `period = 2 * length`. Python guarantees that the result of `%` is in the interval from (0) through `period - 1`, even when the original position is negative. That is why the negative-velocity case needs no special branch.

The condition is `pos <= length`, not `pos < length`. If the ball lands exactly on a wall, that coordinate is already the correct physical position. For example, when `pos == length`, returning `length` is exactly right.

There is no need to update the velocity after finding a collision. We only need the position at one specified time, and the unfolded model has already encoded every velocity reversal through reflection.

The input is processed with `sys.stdin.readline`, and answers are accumulated before one final write. With up to (10^4) test cases, this keeps I/O overhead small.

## Worked Examples

For the first sample case,

```
3 5 2 2 2 1 3
```

the horizontal table size is (3), so the unfolded period is (6). The vertical table size is (5), so its period is (10).

| Coordinate | Start | Velocity | Time | Unfolded position | Modulo period | Reflected position |
| --- | --- | --- | --- | --- | --- | --- |
| (x) | 2 | 2 | 3 | 8 | 2 | 2 |
| (y) | 2 | 1 | 3 | 5 | 5 | 5 |

The answer is `2 5`. Physically, the ball moves horizontally from (2) to the right wall at (3), back to (1) at time (2), and then to (2) at time (3). The unfolded calculation gets the same result without simulating those collisions.

For the second sample case,

```
6 8 3 2 5 1 1
```

the horizontal period is (12), while the vertical period is (16).

| Coordinate | Start | Velocity | Time | Unfolded position | Modulo period | Reflected position |
| --- | --- | --- | --- | --- | --- | --- |
| (x) | 3 | 5 | 1 | 8 | 8 | 4 |
| (y) | 2 | 1 | 1 | 3 | 3 | 3 |

The horizontal unfolded position is (8). Since the table ends at (6), the reflected coordinate is (12-8=4). The vertical coordinate has not reached a wall, so it remains (3). The resulting answer is `4 3`.

These traces show why the reflection must happen after taking modulo (2L), rather than modulo (L). Modulo (L) would lose the distinction between travelling toward a wall and travelling back from it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case performs a constant number of arithmetic operations. |
| Space | (O(T)) | The output strings are stored before being written. The working space per test is (O(1)). |

With (T\le10^4), the algorithm performs only a few integer operations per test case. Even though (N,M,v_x,v_y,S) can make the intermediate product very large, Python handles these integers directly, and the number of arithmetic operations remains constant. The solution comfortably avoids the (10^9)-step simulation that the original bounds make impossible.

## Test Cases

```python
import sys
import io

def reflected_position(length, start, velocity, seconds):
    period = 2 * length
    pos = (start + velocity * seconds) % period

    if pos <= length:
        return pos
    return period - pos

def solve_input(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        output = io.StringIO()
        sys.stdout = output

        t = int(sys.stdin.readline())
        ans = []

        for _ in range(t):
            n, m, x0, y0, vx, vy, s = map(
                int, sys.stdin.readline().split()
            )

            x = reflected_position(n, x0, vx, s)
            y = reflected_position(m, y0, vy, s)

            ans.append(f"{x} {y}")

        sys.stdout.write("\n".join(ans))
        return output.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample = """\
3
3 5 2 2 2 1 3
6 8 3 2 5 1 1
100 200 13 45 -20 111 9969
"""
assert solve_input(sample) == "2 5\n4 3\n33 196", "provided sample"

# Minimum-size table, immediate hit on the right wall.
case_min = """\
1
2 2 1 1 1 0 1
"""
assert solve_input(case_min) == "2 1", "minimum-size table"

# Both coordinates move equally and hit a corner.
case_corner = """\
1
2 2 1 1 1 1 1
"""
assert solve_input(case_corner) == "2 2", "corner collision"

# Negative velocities, including a coordinate that lands exactly on a wall.
case_negative = """\
1
5 4 2 2 -3 -2 1
"""
assert solve_input(case_negative) == "1 0", "negative velocity"

# Zero velocity in one coordinate and multiple reflections in the other.
case_zero_velocity = """\
1
2 5 1 3 0 2 3
"""
assert solve_input(case_zero_velocity) == "1 1", "zero velocity"

# Maximum-scale values.
case_maximum = """\
1
1000000000 1000000000 999999999 999999999 1000000000 -1000000000 1000000000
"""
assert solve_input(case_maximum) == "999999999 999999999", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1 1 1 0 1` | `2 1` | Minimum table dimensions and an exact wall hit |
| `2 2 1 1 1 1 1` | `2 2` | Simultaneous collision at a corner |
| `5 4 2 2 -3 -2 1` | `1 0` | Negative velocities and negative unfolded positions |
| `2 5 1 3 0 2 3` | `1 1` | Zero velocity and repeated vertical reflections |
| `1000000000 1000000000 999999999 999999999 1000000000 -1000000000 1000000000` | `999999999 999999999` | Maximum-scale arithmetic and large periods |

## Edge Cases

An exact wall hit is handled by the `<= length` condition. Consider

```
1
3 4 1 2 2 0 1
```

For (x), the unfolded position is (1+2=3). The period is (6), so the reduced position is (3). Since (3\le3), the function returns (3). The vertical coordinate remains (2). The output is `3 2`. No extra reflection is applied at the instant of collision because the question asks for the position at that exact time.

Negative velocity requires the modulo operation to normalize the unfolded position. For

```
1
5 4 2 2 -3 -2 1
```

the horizontal unfolded position is (-1). Its normalized value modulo (10) is (9), so the reflected position is (10-9=1). Vertically, the unfolded position is (0), which stays (0). The output is `1 0`. The formula works even though the ball has crossed the left boundary in the unfolded model.

A corner collision does not require special handling. For

```
1
3 3 1 1 2 2 1
```

both unfolded coordinates become (3). Both periods are (6), and both reduced coordinates are exactly (3), so the answer is `3 3`. The fact that both velocity components reverse afterward has no effect on the position at time (1). The independence of the two one-dimensional transformations naturally handles the corner.

Zero velocity is also covered without a separate branch. For

```
1
2 5 1 3 0 2 3
```

the horizontal unfolded coordinate remains (1), while the vertical unfolded coordinate becomes (9). The vertical period is (10), so (9) folds to (1). The answer is `1 1`. A simulation might repeatedly inspect the horizontal coordinate even though nothing can happen there, while the formula simply calculates it once.

Finally, large values do not change the algorithm. With

```
1
1000000000 1000000000 999999999 999999999 1000000000 -1000000000 1000000000
```

the horizontal unfolded coordinate is (999999999+10^{18}), and the vertical one is (999999999-10^{18}). Since (10^{18}) is divisible by (2\cdot10^9), both coordinates reduce to (999999999) modulo their respective periods. Both are already in the first half of the unfolded interval, giving `999999999 999999999`. The example demonstrates why the solution must use arithmetic rather than simulation, while also exercising values close to the largest allowed limits.
