---
title: "CF 102272A - Ch\u01a1i Bi-a"
description: "We have a rectangular carom table whose horizontal extent is from (x=0) to (x=N), and whose vertical extent is from (y=0) to (y=M). A ball starts at the integer position ((x0,y0)) strictly inside the rectangle."
date: "2026-08-21T10:14:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "A"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 1451
verified: true
draft: false
---

[CF 102272A - Ch\u01a1i Bi-a](https://codeforces.com/problemset/problem/102272/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 24m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular carom table whose horizontal extent is from (x=0) to (x=N), and whose vertical extent is from (y=0) to (y=M). A ball starts at the integer position ((x_0,y_0)) strictly inside the rectangle. During every second it moves by the current velocity vector ((v_x,v_y)). When it reaches a vertical wall, the sign of (v_x) changes. When it reaches a horizontal wall, the sign of (v_y) changes. Hitting a corner changes both signs.

The task is to find the ball's exact integer position after (S) seconds. The input contains up to (10^4) independent simulations. The table dimensions, coordinates, velocities, and time can all be as large as (10^9).

The large value of (S) rules out simulating the motion one second at a time. A single test case could require (10^9) updates, and across (10^4) test cases that would reach (10^{13}) updates. Even a very small amount of work per simulated second would be far beyond a 1 second time limit. We need a computation whose cost does not depend linearly on (S).

The most useful structural fact is that the horizontal and vertical motions are independent. A vertical wall changes only (v_x), while a horizontal wall changes only (v_y). We can solve the one-dimensional motion on ([0,N]) and ([0,M]) separately, then combine the two coordinates.

There are several boundary cases that can expose mistakes in a naive implementation. First, the velocity can be negative. For example, with

```
1
5 5 2 2 -3 0 1
```

the correct position is

```
4 2
```

because the ball moves from (x=2) to (x=-1), reaches the wall at (x=0), and reflects to (x=1) only after the actual continuous trajectory reaches the wall. Since the requested position is at time (1), the correct interpretation is obtained by the unfolded trajectory: (2-3=-1), whose reflected position is (1). A formula that uses an ordinary remainder without normalizing negative values can produce a negative coordinate.

A second trap is reaching a wall exactly at the requested time. Consider

```
1
2 3 1 1 1 2 1
```

At time (1), the ball is exactly at the upper-right corner, so the answer is

```
2 3
```

The velocity changes after the collision, but that does not move the ball away from the corner before the requested time. An implementation that reflects as soon as it sees the endpoint and then immediately applies another movement can introduce an off-by-one error.

A third case is a corner collision. For

```
1
2 3 1 2 1 1 1
```

the ball reaches ((2,3)), so the output is

```
2 3
```

Both coordinates must use their own reflection rules. Treating a corner as only one wall collision would leave one velocity component incorrectly oriented, which becomes visible on later queries.

Finally, zero velocity is valid for either coordinate. For example,

```
1
2 2 1 1 0 1 3
```

has output

```
1 2
```

because the horizontal coordinate never changes, while the vertical coordinate reaches (2) at the first second and then reflects.

## Approaches

The direct simulation follows the physical description exactly. Starting from ((x_0,y_0)), we add ((v_x,v_y)) once per second. Whenever a coordinate reaches one of its two boundaries, we reverse the corresponding velocity component. This is correct because it performs precisely the same transitions as the billiard model.

The problem is the number of iterations. In the worst case (S=10^9), so one test case can require (10^9) simulated seconds. With (T=10^4), the theoretical total reaches (10^{13}) iterations. The simulation is correct but fundamentally incompatible with the constraints.

The key observation is that a reflected one-dimensional trajectory can be unfolded into a straight line. Imagine replacing the interval ([0,N]) by an infinite sequence of copies:

[
[0,N], [N,2N], [2N,3N], \ldots
]

and continuing them in alternating orientation. Instead of reflecting at a wall, the ball keeps moving straight through the boundary into the next copy. Folding that straight trajectory back into the original interval gives exactly the same physical position.

The unfolded horizontal coordinate after (S) seconds is simply

[
p_x=x_0+v_xS.
]

The actual table coordinate depends only on where (p_x) lies within a period of length (2N). Define

[
r_x=p_x\bmod 2N.
]

For (0\le r_x\le N), the folded position is (r_x). For (N<r_x<2N), it is (2N-r_x). This creates the familiar triangular wave of a bouncing particle.

The vertical coordinate has exactly the same form with (M). This reduces the whole simulation to a few integer additions, modulo operations, and comparisons. Negative velocities require no special physical case because Python's modulo operation already returns a value in the range ([0,2N-1]) for a positive modulus.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(S)) per test case | (O(1)) | Too slow |
| Optimal | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Compute the unfolded horizontal position (p_x=x_0+v_xS). We deliberately ignore reflections here because the unfolded model lets the ball continue through every wall in a straight line.
2. Reduce (p_x) modulo (2N), obtaining (r_x=p_x\bmod 2N). A complete back-and-forth trip from one wall to the other and back has length (2N), so positions separated by (2N) fold to the same physical coordinate.
3. Fold (r_x) back into the table. If (r_x\le N), the physical coordinate is (r_x). Otherwise the trajectory is in the mirrored half of the period, so the physical coordinate is (2N-r_x).
4. Perform the same computation vertically using (p_y=y_0+v_yS), period (2M), and the folding boundary (M).
5. Print the resulting (x) and (y) coordinates. The two dimensions are independent, so their separately computed positions form the ball's final position.

### Why it works

Consider only the horizontal coordinate. In the real table, every collision with (x=0) or (x=N) reverses the horizontal velocity. In the unfolded representation, instead of reversing velocity, we continue into a reflected copy of the table. Folding those copies back into ([0,N]) reverses the apparent direction exactly when the real ball would hit a wall. One full pair of reflections corresponds to a distance of (2N), so taking the unfolded coordinate modulo (2N) preserves all information needed to determine the current physical position. The same argument applies independently to (y). Thus the two folded coordinates are exactly the position of the real ball after (S) seconds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def position(start, velocity, length, seconds):
    unfolded = start + velocity * seconds
    period = 2 * length
    r = unfolded % period

    if r <= length:
        return r
    return period - r

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m, x0, y0, vx, vy, s = map(int, input().split())

        x = position(x0, vx, n, s)
        y = position(y0, vy, m, s)

        out.append(f"{x} {y}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `position` function contains the entire one-dimensional reflection logic. It first constructs the unfolded coordinate after (S) seconds. There is no need to simulate individual collisions because all of them are represented by the periodic folding operation.

The modulo divisor is twice the table length, not the table length itself. Using (N) would incorrectly identify the two directions of travel, since reaching (x=0) and reaching (x=N) are different points of the trajectory.

The condition `r <= length` includes the exact wall position. This matters because a ball can be exactly on a wall at the requested time. At that instant its position is still the wall coordinate, regardless of the velocity reversal that happens after collision.

Python integers have arbitrary precision, so products such as (v_xS) do not overflow. In languages with fixed-width integer types, a 64-bit integer should be used because the product can reach roughly (10^{18}).

Negative velocities require no separate branch. For example, if the unfolded coordinate is (-1) and the period is (10), Python computes (-1\bmod 10=9). Folding (9) gives (10-9=1), exactly the physical position obtained by reflecting the point (-1) across (x=0).

## Worked Examples

### Sample 1, first test case

The first test case is

```
3 5 2 2 2 1 3
```

The horizontal table length is (3), so its period is (6). The vertical table length is (5), so its period is (10).

| Coordinate | Start | Velocity | Time | Unfolded | Period | Remainder | Final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (x) | 2 | 2 | 3 | 8 | 6 | 2 | 2 |
| (y) | 2 | 1 | 3 | 5 | 10 | 5 | 5 |

The horizontal unfolded coordinate (8) is equivalent to (2) modulo (6), so the ball is at (x=2). The vertical coordinate is exactly (5), which is the upper wall, giving the final position ((2,5)).

This demonstrates that the formula naturally handles a trajectory that reaches a wall exactly at the requested time.

### Sample 1, second test case

The second test case is

```
6 8 3 2 5 1 1
```

Here the horizontal period is (12), and the vertical period is (16).

| Coordinate | Start | Velocity | Time | Unfolded | Period | Remainder | Final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (x) | 3 | 5 | 1 | 8 | 12 | 8 | 4 |
| (y) | 2 | 1 | 1 | 3 | 16 | 3 | 3 |

For (x), the remainder (8) lies in the mirrored half of the period, so it folds to (12-8=4). The vertical coordinate remains (3). The output is consequently ((4,3)).

This trace shows why the second half of the period must be reflected rather than used directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case performs constant-time arithmetic for two coordinates. |
| Space | (O(T)) for output storage, (O(1)) auxiliary space | The computation itself uses only a constant number of integers per test case. |

With at most (10^4) test cases, the algorithm performs only a constant amount of arithmetic for each case. The value (S=10^9) has no effect on the number of iterations, so the solution easily fits the 1 second limit. The memory usage is also tiny apart from the output strings.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        input = sys.stdin.readline

        def position(start, velocity, length, seconds):
            unfolded = start + velocity * seconds
            period = 2 * length
            r = unfolded % period
            if r <= length:
                return r
            return period - r

        t = int(input())
        out = []

        for _ in range(t):
            n, m, x0, y0, vx, vy, s = map(int, input().split())
            x = position(x0, vx, n, s)
            y = position(y0, vy, m, s)
            out.append(f"{x} {y}")

        print("\n".join(out))
        return output.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def run(inp: str) -> str:
    return solve_data(inp)

assert run("""3
3 5 2 2 2 1 3
6 8 3 2 5 1 1
100 200 13 45 -20 111 9969
""") == """2 5
4 3
33 196
""", "provided sample"

assert run("""1
2 2 1 1 0 1 1
""") == """1 2
""", "minimum-size table and zero velocity"

assert run("""1
1000000000 1000000000 1 1 1 1 1000000000
""") == """999999999 999999999
""", "maximum-size values"

assert run("""1
5 5 2 2 3 3 4
""") == """4 4
""", "equal dimensions and equal coordinates"

assert run("""1
2 3 1 2 1 1 1
""") == """2 3
""", "exact corner collision"

assert run("""1
5 5 2 2 -3 0 1
""") == """1 2
""", "negative velocity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1 1 0 1 1` | `1 2` | Minimum dimensions and a zero velocity component |
| `1000000000 1000000000 1 1 1 1 1000000000` | `999999999 999999999` | Maximum numerical values and large time |
| `5 5 2 2 3 3 4` | `4 4` | Equal dimensions, equal coordinates, and repeated reflections |
| `2 3 1 2 1 1 1` | `2 3` | Reaching a corner exactly at the requested time |
| `5 5 2 2 -3 0 1` | `1 2` | Negative velocity and a stationary coordinate |

## Edge Cases

The first tricky case is negative velocity. For

```
1
5 5 2 2 -3 0 1
```

the horizontal unfolded coordinate is (2-3=-1). With period (10), the normalized remainder is (9). Since (9>5), the folded coordinate is (10-9=1). The vertical coordinate is unchanged at (2), so the answer is `1 2`. No special branch for negative velocity is necessary.

The second case is a wall reached exactly at the requested time. For

```
1
2 3 1 1 1 2 1
```

the unfolded coordinates are (2) and (3). Their remainders are also (2) and (3), both equal to their respective table lengths. Because the folding condition uses `<=`, the result is exactly `2 3`. The velocity reversal affects subsequent motion, not the position at the collision instant.

The third case is a corner collision:

```
1
2 3 1 2 1 1 1
```

Both unfolded coordinates reach their maximum values simultaneously. The horizontal result is (2), and the vertical result is (3), giving `2 3`. Since each coordinate is handled independently, there is no need for a special corner case in the implementation. Both velocity components are implicitly reflected by their respective triangular-wave formulas.

The fourth case is zero velocity:

```
1
2 2 1 1 0 1 3
```

For (x), the unfolded coordinate remains (1), so the horizontal result is always (1). For (y), the unfolded coordinate is (4), and the period is (4), giving remainder (0). The vertical result is consequently (0), so the exact output is `1 0`. This illustrates why zero velocity does not require special handling, although it also shows that the ball may be on a boundary at the requested time.

A final source of bugs is confusing the table length with the full reflection period. For a table of width (5), the sequence of positions in one horizontal cycle has the form

[
0,1,2,3,4,5,4,3,2,1,0.
]

The cycle length is (10=2N). If an implementation reduced modulo (N), it would incorrectly map positions from the return journey onto the outward journey and lose the direction information encoded by the reflection.
