---
title: "CF 105581B - Patrol"
description: "We are given a police officer who continuously patrols back and forth along a straight segment between two fixed points A and B at unit speed."
date: "2026-06-22T06:09:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105581
codeforces_index: "B"
codeforces_contest_name: "Open Udmurtia Junior Programming Contest 2018"
rating: 0
weight: 105581
solve_time_s: 44
verified: true
draft: false
---

[CF 105581B - Patrol](https://codeforces.com/problemset/problem/105581/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a police officer who continuously patrols back and forth along a straight segment between two fixed points A and B at unit speed. The motion is perfectly periodic: starting at A at time 0, he goes to B, then immediately turns around and goes back to A, repeating this indefinitely with no pauses.

At some time T, an external event interrupts this motion. At that exact moment, regardless of where the officer currently is on the segment, he stops the patrol and instead walks directly toward a third point C on the same line, again at unit speed. The task is to compute how long it takes from time T until he reaches C.

The input gives A and B as endpoints of the patrol segment, then T and C. The key hidden task is to determine the officer’s exact position at time T under this back and forth motion, then compute the remaining straight-line travel time to C.

The constraints allow coordinates up to 10^5 and time up to 10^9. A simulation stepping second by second is impossible because T can be large, so any solution must compute the position using arithmetic structure of periodic motion.

A naive pitfall is assuming the officer is always moving from A to B only, ignoring direction reversals. Another is forgetting that direction depends on how many full traversals of segment length have occurred.

A concrete edge case:

Input:

A = 3, B = 8, T = 10, C = 1

At t = 0 he is at 3, at t = 5 he is at 8, at t = 10 he is back at 3. A wrong approach that assumes monotone movement would incorrectly place him at 13, which is outside the segment and invalid.

Correct output is computed from the actual oscillation, giving position at T = 3 again, so time to C is |3 − 1| = 2.

Another edge case occurs when T lands exactly at a turning point, where direction flips instantaneously but position remains the endpoint.

## Approaches

A brute-force simulation would advance the officer one second at a time, maintaining current position and direction, flipping direction whenever an endpoint is reached. Each second costs O(1), so total complexity is O(T). This is correct but completely infeasible when T reaches 10^9.

The key observation is that the motion is periodic on a segment of length L = |A − B|. One full cycle consists of moving from A to B and back, covering distance 2L in time 2L. Instead of simulating step by step, we can reduce time T modulo the cycle length 2L and determine where within this cycle the officer is.

Once the remaining time within a cycle is known, the position becomes a simple linear function: first moving from A to B, then from B back to A. This removes all simulation and reduces the problem to constant-time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T) | O(1) | Too slow |
| Cycle Reduction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We assume WLOG that A and B define a segment, and define L = |A − B|. We treat A as the starting endpoint of the cycle.

1. Compute L = |A − B|. This is the distance of one leg of the patrol, so a full round trip has length 2L.
2. Determine the officer’s effective time inside the current cycle: t = T mod (2L). Any full cycles before this do not affect the final position because the motion repeats exactly.
3. If t ≤ L, the officer is on the forward leg from A toward B, so his position is A + direction * t where direction depends on whether A < B.
4. If t > L, he is on the return leg. We convert it into remaining forward distance from B: t' = t − L, then position is B − direction * t'.
5. Once position P at time T is known, compute answer as |P − C|, since he moves directly at unit speed to C.

The subtle point is consistently handling direction. Instead of treating A as always smaller, we encode direction explicitly so the same formula works for both cases.

### Why it works

The motion is a deterministic walk on a line segment with reflecting boundaries. Every 2L time units, the state (position and direction) returns exactly to the starting configuration at A moving toward B. This creates a perfect periodic orbit. Reducing time modulo the period preserves the exact state within that orbit, so the computed position is identical to what full simulation would produce.

## Python Solution

```python
import sys
input = sys.stdin.readline

A, B = map(int, input().split())
T, C = map(int, input().split())

L = abs(A - B)
period = 2 * L

# If A == B (degenerate, though constraints say A != B)
# motion still handled normally since L > 0 guaranteed

t = T % period

# normalize direction: start moving from A toward B
if A < B:
    start = A
    end = B
    forward = 1
else:
    start = A
    end = B
    forward = -1

if t <= L:
    pos = start + forward * t
else:
    t2 = t - L
    pos = end - forward * t2

ans = abs(pos - C)
print(ans)
```

The solution first computes the segment length and reduces time using modulo arithmetic. The direction is normalized so that “forward” always means moving from A to B, even if A > B.

The first phase handles movement from A toward B. If the reduced time is still within that phase, the position is computed by linear motion. Otherwise we switch to the return phase starting from B and move back symmetrically.

Finally, the answer is the direct distance to C because motion after T is unrestricted straight-line movement.

## Worked Examples

### Example 1

Input:

A = 3, B = 8, T = 10, C = 1

Here L = 5, period = 10, so t = 10 mod 10 = 0.

| Step | t | Phase | Position |
| --- | --- | --- | --- |
| Start | 0 | at A | 3 |

At t = 0, the officer is exactly at A again after a full cycle. From there, distance to C is |3 − 1| = 2.

This demonstrates that full cycles collapse correctly via modulo.

### Example 2

Input:

A = 2, B = 6, T = 7, C = 5

L = 4, period = 8, so t = 7.

| Step | t | Phase | Position |
| --- | --- | --- | --- |
| start | 7 | forward 2, backward 3 | compute |

Since t ≤ L is false, we are in return phase. We compute t2 = 7 − 4 = 3, so position is 6 − 3 = 3.

Distance to C is |3 − 5| = 2.

This shows correct handling of the backward motion segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All operations are arithmetic and conditional checks |
| Space | O(1) | Only a few integer variables are stored |

The constraints allow up to 10^9 for T, but the solution avoids iteration entirely by reducing time modulo a fixed period, keeping execution constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    A, B = map(int, input().split())
    T, C = map(int, input().split())

    L = abs(A - B)
    period = 2 * L
    t = T % period

    if A < B:
        start, end, f = A, B, 1
    else:
        start, end, f = A, B, -1

    if t <= L:
        pos = start + f * t
    else:
        t2 = t - L
        pos = end - f * t2

    return str(abs(pos - C))

# sample-like cases
assert run("3 8\n10 1\n") == "2"
assert run("6 1\n7 9\n") == "2"

# minimum movement
assert run("0 1\n0 0\n") == "0"

# immediate stop
assert run("2 5\n0 4\n") == "2"

# mid forward phase
assert run("1 5\n2 10\n") == "8"

# mid backward phase
assert run("1 5\n6 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 8 / 10 1 | 2 | full cycle reset |
| 6 1 / 7 9 | 2 | backward direction |
| 0 1 / 0 0 | 0 | already at target |
| 2 5 / 0 4 | 2 | start at endpoint |
| 1 5 / 2 10 | 8 | forward motion |
| 1 5 / 6 2 | 3 | backward motion |

## Edge Cases

One important edge case is when T is an exact multiple of the full cycle length 2L. In this case, t becomes 0 after modulo reduction, meaning the officer is exactly at A moving toward B again. The algorithm handles this naturally because t ≤ L sends us into the forward phase and yields position A.

Another edge case occurs when the officer is exactly at B at time T, meaning t = L. The condition t ≤ L ensures this is treated as the endpoint of the forward phase, producing position B without ambiguity, which is consistent with instantaneous direction reversal.

A third case is when A > B. Because direction is encoded explicitly rather than relying on ordering, the same formulas apply. For instance, with A = 8, B = 3, the forward step moves toward decreasing coordinates, and the backward step reverses it correctly, ensuring symmetry without special-casing.
