---
title: "CF 106434A - \u0420\u043e\u0431\u043e\u0442-\u043f\u044b\u043b\u0435\u0441\u043e\u0441"
description: "A robot moves inside a one-dimensional corridor that can be thought of as a segment of integer points from 0 to L. The left wall is at position 0 and the right wall is at position L. The robot starts at position X and initially faces either left or right."
date: "2026-06-19T17:51:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106434
codeforces_index: "A"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421 2026, \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106434
solve_time_s: 49
verified: true
draft: false
---

[CF 106434A - \u0420\u043e\u0431\u043e\u0442-\u043f\u044b\u043b\u0435\u0441\u043e\u0441](https://codeforces.com/problemset/problem/106434/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

A robot moves inside a one-dimensional corridor that can be thought of as a segment of integer points from 0 to L. The left wall is at position 0 and the right wall is at position L. The robot starts at position X and initially faces either left or right. Every second it moves exactly one unit in the direction it is currently facing. When it tries to move past a wall, it first hits the boundary, immediately reverses direction, and then continues moving in the opposite direction.

The task is to determine the robot’s position after T seconds.

The constraints allow L and T up to 10^9, which immediately rules out any step-by-step simulation. A linear simulation would require up to 10^9 operations per test, which is too slow. The solution must compress the motion into a direct formula or an O(1) computation per test.

A common failure case for naive reasoning is to ignore the “bounce” behavior at boundaries and treat motion as simple linear movement. For example, with L = 10, X = 3, moving right for T = 4, a naive computation would give 7, which happens to be correct here. But if the robot hits a wall and reflects, the motion is not monotone, and linear extrapolation fails in general.

Another subtle failure arises when multiple reflections occur. For instance, if L = 5, X = 2, moving right for T = 10, the robot bounces repeatedly. Any approach that only considers the first collision breaks quickly.

## Approaches

The motion is essentially a straight-line walk with reflections at boundaries. A direct simulation tracks position and direction at each step, updating position and flipping direction at walls. This is correct but takes O(T) time, which is infeasible when T is large.

The key observation is that reflections can be removed by unfolding the corridor. Instead of bouncing, imagine that after reaching a wall, the robot continues into a mirrored copy of the corridor. This transforms the motion into a simple straight-line movement on an infinite line.

More concretely, we map positions in [0, L] into a periodic structure of length 2L. The robot moves as if it is on a line without walls, starting at X and moving ±1 per step depending on direction. After T steps, its “unfolded position” is X + d·T where d is +1 for right and −1 for left. We then map this position back into [0, L] using symmetry of period 2L.

If p = (X + d·T) mod (2L), then:

If p ≤ L, the answer is p.

If p > L, the answer is 2L − p.

This works because every full traversal from one wall to the other corresponds to a length L segment, and reflection is equivalent to reversing direction, which is exactly what the folding map encodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T) | O(1) | Too slow |
| Modular Reflection Mapping | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the direction into a numeric velocity d, where right becomes +1 and left becomes −1. This turns movement into arithmetic instead of branching logic.
2. Compute the raw position after T steps as p = X + d·T. This represents motion without walls, as if the corridor were extended infinitely.
3. Normalize p into the range [0, 2L] using modulo arithmetic: p = p mod (2L). This captures the repeating structure created by reflections.
4. If p is negative after modulo adjustment, shift it by adding 2L. This ensures consistency in the periodic representation.
5. Map the unfolded position back into the real corridor. If p is within [0, L], it already corresponds to a valid position. If p is in (L, 2L], reflect it as p = 2L − p.

The reflection step corresponds exactly to the robot having crossed the midpoint of a “virtual mirrored corridor” and coming back toward the original segment.

### Why it works

The invariant is that the robot’s motion on the unfolded line alternates between forward and mirrored segments of identical length L. Every time it crosses a boundary, its direction flip is equivalent to continuing motion into a reflected copy of the segment. The modulo operation compresses this infinite unfolding into a single periodic interval of length 2L, and the final reflection step selects the correct image of the robot within the original segment. Because every wall interaction corresponds exactly to a transition between symmetric halves of the period, no information is lost in the mapping.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    L = int(input().strip())
    X = int(input().strip())
    S = input().strip()
    T = int(input().strip())

    d = 1 if S == 'R' else -1

    p = X + d * T

    mod = 2 * L
    p %= mod
    if p < 0:
        p += mod

    if p <= L:
        print(p)
    else:
        print(2 * L - p)

if __name__ == "__main__":
    solve()
```

The implementation directly applies the unfolded-line model. The direction is encoded as ±1 so that movement becomes a single arithmetic expression. The modulo by 2L is the key step that compresses infinite reflections into a bounded periodic domain.

The final conditional handles the folding back into the original corridor. The threshold at L is critical: it separates the forward traversal from the mirrored traversal.

One subtle point is handling negative values after modulo. Python’s modulo already returns a non-negative result for positive modulus, but keeping the adjustment makes the logic robust under translation to other languages.

## Worked Examples

### Example 1

Let L = 10, X = 3, S = R, T = 4.

| Step | Expression | Value |
| --- | --- | --- |
| Direction d | R → +1 | 1 |
| Raw position p | 3 + 1·4 | 7 |
| Mod 2L | 7 mod 20 | 7 |
| Final position | 7 ≤ 10 | 7 |

This shows the simplest case where no reflection occurs. The unfolded model matches direct motion.

### Example 2

Let L = 10, X = 8, S = R, T = 5.

| Step | Expression | Value |
| --- | --- | --- |
| Direction d | R → +1 | 1 |
| Raw position p | 8 + 5 | 13 |
| Mod 2L | 13 mod 20 | 13 |
| Reflection | 13 > 10 ⇒ 20 − 13 | 7 |

This demonstrates a boundary crossing. After reaching the right wall at 10, the robot effectively reflects and moves left, which is captured by folding 13 back into 7.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All operations are arithmetic and a single modulo |
| Space | O(1) | Only a few integer variables are used |

The solution easily fits within constraints because it avoids simulating each second of movement. Even for T = 10^9, the computation remains constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# basic movement no bounce
assert run("10\n3\nR\n4\n") == "7"

# bounce at right wall
assert run("10\n8\nR\n5\n") == "7"

# bounce at left wall
assert run("10\n2\nL\n3\n") == "1"

# immediate reflection at boundary
assert run("5\n5\nR\n1\n") == "4"

# full oscillation cycle
assert run("5\n2\nR\n10\n") in ["2", "2"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 3 R 4 | 7 | simple linear motion |
| 10 8 R 5 | 7 | right wall reflection |
| 10 2 L 3 | 1 | left wall reflection |
| 5 5 R 1 | 4 | boundary immediate bounce |
| 5 2 R 10 | 2 | periodic oscillation stability |

## Edge Cases

One edge case is starting exactly at a wall and moving outward. For example, L = 5, X = 5, S = R, T = 1. The robot moves from 5 to 6 in unfolded space, which maps to 4 after reflection since 6 > 5 implies 10 − 6 = 4. The algorithm handles this naturally through the folding rule.

Another case is repeated full cycles. For L = 4, X = 1, S = R, T = 6, the unfolded position is 7, modulo 8 gives 7, and reflection gives 1. This matches the fact that after two full traversals the robot returns to its original position.

A third case is very large T. Since the computation only depends on T modulo 2L, values like T = 10^9 behave identically to their reduced remainder. The algorithm never depends on the absolute size of T, only its position in the cycle induced by reflections.
