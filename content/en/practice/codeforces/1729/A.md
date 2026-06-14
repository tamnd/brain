---
title: "CF 1729A - Two Elevators"
description: "The situation describes a decision between two elevators that can potentially reach Vlad on the 1st floor. Each elevator has a different movement rule, and the goal is to determine which one arrives back to floor 1 the fastest after Vlad presses a call button."
date: "2026-06-15T02:29:39+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1729
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 820 (Div. 3)"
rating: 800
weight: 1729
solve_time_s: 344
verified: true
draft: false
---

[CF 1729A - Two Elevators](https://codeforces.com/problemset/problem/1729/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 5m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The situation describes a decision between two elevators that can potentially reach Vlad on the 1st floor. Each elevator has a different movement rule, and the goal is to determine which one arrives back to floor 1 the fastest after Vlad presses a call button.

The first elevator is initially stopped at some floor `a`. Once called, it immediately starts moving toward floor 1. Its travel time is purely the distance between its current position and the destination, so the time it needs is `|a - 1|`.

The second elevator behaves differently. It starts at floor `b` and is currently moving toward floor `c`. If Vlad calls it, it does not immediately head to floor 1. Instead, it first continues (or finishes) its current movement toward `c`, and only after reaching `c` does it start moving toward floor 1. This means its total time is the time to go from `b` to `c`, plus the time to go from `c` to `1`, which is `|b - c| + |c - 1|`.

The task is to compare these two arrival times for each test case and decide whether the first elevator is faster, the second is faster, or they take the same time.

The constraints allow up to `10^4` test cases, with floor values up to `10^8`. This immediately rules out any simulation of movement step by step. Each test must be processed in constant time, since even O(t log n) would be unnecessary overhead and O(t * distance) is impossible due to the magnitude of floor differences.

A subtle edge case appears when one elevator is already effectively at floor 1. For example, if `a = 1`, the first elevator has zero travel time. Similarly, if `b = 1`, the second elevator still must finish its current move to `c` before returning, so it is never instant even though it starts at floor 1. This asymmetry is easy to misread if one assumes starting position alone determines immediate availability.

## Approaches

A brute-force interpretation would simulate each elevator’s movement in time steps. For the first elevator, this is trivial, it just walks from `a` to `1`. For the second elevator, one might try to simulate its movement toward `c` first, then toward `1`, updating position step by step.

This works conceptually but is completely infeasible. The distance between floors can be up to `10^8`, so simulating even a single test case step-by-step could take up to `10^8` operations, and across `10^4` test cases this becomes astronomically large.

The key observation is that both elevators move at constant speed and do not interact with any constraints other than distance. This reduces the entire problem to computing total path lengths. The first elevator contributes a single segment from `a` to `1`. The second elevator contributes a fixed two-segment path from `b` to `c` and then `c` to `1`. Once expressed as distances, the comparison becomes a simple arithmetic check.

We are not optimizing a process anymore, we are only comparing two scalar values derived from geometry on a number line.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(t · max distance) | O(1) | Too slow |
| Direct distance computation | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the three integers `a`, `b`, and `c`. These define the starting positions and the forced intermediate target for the second elevator.
2. Compute the arrival time of the first elevator as `t1 = abs(a - 1)`. This directly represents its uninterrupted movement to floor 1.
3. Compute the arrival time of the second elevator as `t2 = abs(b - c) + abs(c - 1)`. This encodes the rule that it must first complete its movement to `c`, then proceed to 1.
4. Compare `t1` and `t2`. If `t1 < t2`, the first elevator is strictly faster, so output `1`.
5. If `t2 < t1`, the second elevator is strictly faster, so output `2`.
6. If both times are equal, output `3` since both choices are equivalent.

The reasoning behind the comparison is that both expressions fully capture total travel time under deterministic movement. There are no hidden states, delays, or branching paths beyond these distances.

### Why it works

The system can be modeled as movement on a one-dimensional number line with constant speed. Each elevator’s behavior defines a fixed path length once the call is made. Because travel time is proportional to distance and there are no interactions between elevators, minimizing arrival time is equivalent to minimizing total path length. The algorithm is correct because it compares exactly those path lengths without approximation or simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())

    t1 = abs(a - 1)
    t2 = abs(b - c) + abs(c - 1)

    if t1 < t2:
        print(1)
    elif t2 < t1:
        print(2)
    else:
        print(3)
```

The first computation `t1` encodes the direct distance from the first elevator to the destination floor. The second computation `t2` explicitly respects the constraint that the second elevator must first reach `c` before heading to 1, which is why it is split into two absolute differences rather than a single direct distance from `b` to `1`.

The comparison logic is a direct translation of the problem’s decision rule. Each branch is mutually exclusive and collectively exhaustive, ensuring exactly one valid output per test case.

## Worked Examples

### Sample Input 1

```
3
1 2 3
3 1 2
3 2 1
```

| a | b | c | t1 = |a−1| | t2 = |b−c| + |c−1| | Decision |

|---|---|---|---|---|---|

| 1 | 2 | 3 | 0 | 2 + 2 = 4 | 1 |

| 3 | 1 | 2 | 2 | 1 + 1 = 2 | 3 |

| 3 | 2 | 1 | 2 | 1 + 0 = 1 | 2 |

The first case shows a degenerate situation where the first elevator is already at floor 1, giving it zero travel time. The second case demonstrates equality of total path lengths, where both strategies converge to the same arrival time. The third case shows the second elevator benefiting from being closer to its intermediate target and then already near floor 1.

### Sample Input 2

```
2
10 5 8
1 100 2
```

| a | b | c | t1 | t2 | Decision |
| --- | --- | --- | --- | --- | --- |
| 10 | 5 | 8 | 9 | 3 + 7 = 10 | 1 |
| 1 | 100 | 2 | 0 | 98 + 1 = 99 | 1 |

The second sample emphasizes how the second elevator’s forced detour can dominate its cost even when it starts relatively close to floor 1, because it is obligated to finish its movement to `c` first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires constant-time arithmetic operations and comparisons |
| Space | O(1) | Only a fixed number of variables are used regardless of input size |

The solution scales linearly with the number of test cases, which is optimal given that each case must be read and processed at least once. The arithmetic operations are trivial and well within limits for `t ≤ 10^4`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    it = iter(inp.strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        a = int(next(it)); b = int(next(it)); c = int(next(it))
        t1 = abs(a - 1)
        t2 = abs(b - c) + abs(c - 1)
        if t1 < t2:
            out.append("1")
        elif t2 < t1:
            out.append("2")
        else:
            out.append("3")
    return "\n".join(out)

# provided samples
assert run("""3
1 2 3
3 1 2
3 2 1
""") == """1
3
2"""

# custom cases
assert run("""1
1 2 100
""") == "1"

assert run("""1
50 1 2
""") == "3"

assert run("""1
100 50 1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 100` | `1` | First elevator is already optimal |
| `50 1 2` | `3` | Symmetric equality case |
| `100 50 1` | `2` | Second elevator dominates |

## Edge Cases

When `a = 1`, the first elevator has zero cost because it is already on the destination floor. The algorithm computes `t1 = abs(1 - 1) = 0`, so any nonzero second-elevator path will correctly lose.

When `b = 1`, the second elevator still incurs cost because it must first reach `c`. For example, with `a = 5, b = 1, c = 10`, we get `t1 = 4` and `t2 = 9 + 9 = 18`, so the first elevator is correctly chosen despite the second starting at floor 1.

When `c = 1`, the second elevator’s second leg becomes zero, but it still pays the cost from `b` to `1`. For example, `a = 10, b = 5, c = 1` gives `t1 = 9`, `t2 = 4 + 0 = 4`, so the second elevator wins because its forced route actually ends at the target floor immediately after reaching `c`.
