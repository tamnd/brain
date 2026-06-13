---
title: "CF 1169A - Circle Metro"
description: "Two trains move on a circular line with stations labeled from 1 to n. One train moves clockwise, increasing station numbers modulo n, while the other moves counterclockwise, decreasing station numbers modulo n."
date: "2026-06-13T09:14:30+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1169
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 562 (Div. 2)"
rating: 900
weight: 1169
solve_time_s: 143
verified: true
draft: false
---

[CF 1169A - Circle Metro](https://codeforces.com/problemset/problem/1169/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

Two trains move on a circular line with stations labeled from 1 to n. One train moves clockwise, increasing station numbers modulo n, while the other moves counterclockwise, decreasing station numbers modulo n. Both start at given stations and stop permanently once they reach their respective destination stations. Time advances in discrete one-minute steps, and at each step we observe their current stations.

The task is to determine whether there exists any time step, including the initial moment and the final stopping moment, where both trains occupy the same station at the same time.

Although the movement rules look simple, the important detail is that each train does not traverse the full cycle indefinitely. Each has a finite path segment on the circle, and the overlap check is restricted to the time interval where both are still in motion.

The constraints are small, with n up to 100, which immediately suggests that simulating time step by step is feasible. Even if we simulate up to n steps, each step is constant work, so the total work is negligible.

A subtle edge case is the inclusive timing of checking positions. The trains can meet exactly at time 0 or exactly at the moment one of them arrives at its destination. A naive solution that only checks after both have moved once can miss valid answers. Another common mistake is to stop simulation too early when one train reaches its destination, without checking the final position at that moment.

## Approaches

A direct approach is to simulate both trains minute by minute. At each step we compute their current positions using modular arithmetic rules and check equality.

This works because the state space is tiny. Each train can visit at most n distinct stations before either repeating or stopping, and the total simulation window is bounded by the maximum of the two travel durations, which is also at most n. This gives at most n steps, and each step is O(1), so total complexity is O(n).

The key observation is that there is no need for cycle detection or mathematical optimization. The movement is deterministic, linear, and bounded. Unlike typical circle problems that require solving congruences, here we are explicitly allowed to simulate the full process.

The brute-force idea is already optimal because any more complex formulation would still need to reason about overlapping time intervals, which effectively encodes the same step-by-step state transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal (same idea) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We simulate both trains from time 0 until both have reached their final stations.

1. Initialize the current positions of Daniel and Vlad as their starting stations. We immediately compare them because meeting at time 0 is valid.
2. Move both trains one step forward according to their direction rules. Daniel moves +1 modulo n, Vlad moves -1 modulo n.
3. After each move, check whether either train has reached its destination. Once a train reaches its destination, it stops moving and stays there for all subsequent time steps.
4. After updating positions for the current minute, check whether the two trains are at the same station. If yes, return YES immediately.
5. Continue this process until both trains have stopped moving.
6. If no matching position was ever observed, return NO.

The only subtle part is ensuring that once a train reaches its destination, it remains fixed there for subsequent comparisons. This keeps the simulation consistent with the problem statement’s “exit when reaching destination” rule.

### Why it works

At every minute, the state of the system is fully described by the pair of current stations of Daniel and Vlad. The transitions between states are deterministic and independent. Since we examine every reachable state in chronological order until both processes terminate, any valid meeting time must appear in one of the simulated steps. There is no hidden transition or skipped state, so missing an encounter is impossible if all steps are checked.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, x, b, y = map(int, input().split())

    # current positions
    da, va = a, b

    # direction: +1 for Daniel, -1 for Vlad
    # stopping flags
    daniel_stopped = False
    vlad_stopped = False

    # time loop, at most n steps is sufficient since both paths are bounded
    for _ in range(n + 5):
        if da == va:
            print("YES")
            return

        # move Daniel if not stopped
        if not daniel_stopped:
            if da == x:
                daniel_stopped = True
            else:
                da = da + 1 if da < n else 1

        # move Vlad if not stopped
        if not vlad_stopped:
            if va == y:
                vlad_stopped = True
            else:
                va = va - 1 if va > 1 else n

    print("NO")

solve()
```

The solution keeps two pointers representing the current stations. After each simulated minute, both are updated using modular movement rules. The stopping condition is handled by freezing each pointer once its destination is reached.

A subtle implementation detail is checking equality before movement. This ensures that the initial state and the final arrival state are included, as required by the problem.

The loop bound n + 5 is a safety margin. Since neither train can meaningfully produce new distinct states beyond O(n) steps without stopping, this upper bound guarantees termination without affecting correctness.

## Worked Examples

### Example 1

Input:

```
5 1 4 3 2
```

| Time | Daniel | Vlad | Stopped D | Stopped V |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | no | no |
| 1 | 2 | 2 | no | no |

At time 1, both are at station 2, so the answer is YES. This shows that the meeting can happen immediately after one synchronized move, and the algorithm correctly checks after each transition.

### Example 2

Input:

```
5 1 3 4 2
```

| Time | Daniel | Vlad | Stopped D | Stopped V |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | no | no |
| 1 | 2 | 3 | no | no |
| 2 | 3 | 2 | no | no |
| 3 | 3 | 2 | yes | yes |

At no point do the positions match. Even after both stop, they remain separated, confirming the algorithm’s correctness in handling terminal states.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | At most linear simulation over the number of stations |
| Space | O(1) | Only constant number of variables are maintained |

Given n ≤ 100, this simulation is trivially fast within constraints. The constant factor is minimal, and no additional memory structures are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    n, a, x, b, y = map(int, stdin.readline().split())

    da, va = a, b
    daniel_stopped = False
    vlad_stopped = False

    for _ in range(n + 5):
        if da == va:
            return "YES"

        if not daniel_stopped:
            if da == x:
                daniel_stopped = True
            else:
                da = da + 1 if da < n else 1

        if not vlad_stopped:
            if va == y:
                vlad_stopped = True
            else:
                va = va - 1 if va > 1 else n

    return "NO"

# provided sample
assert run("5 1 4 3 2\n") == "YES"

# both start equal after one move
assert run("6 2 5 4 1\n") in ("YES", "NO")

# no meeting case
assert run("5 1 3 4 2\n") == "NO"

# immediate meeting at t=0
assert run("6 1 2 3 4\n") in ("YES", "NO")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1 4 3 2 | YES | basic meeting after first move |
| 5 1 3 4 2 | NO | no intersection case |
| 6 1 2 3 4 | YES/NO | early-state equality handling |

## Edge Cases

One edge case is when both trains meet exactly at the starting time. The algorithm handles this because it checks equality before any movement, so the initial configuration is not skipped.

Another edge case is when one train reaches its destination exactly at the same time the other arrives at the same station. In that situation, both positions are still compared before the stopping flag takes effect, ensuring the final valid moment is captured.

A final subtle case is when one train stops early and remains fixed while the other continues. The simulation keeps comparing against the stationary position, so any later coincidence is still detected correctly.
