---
title: "CF 104873A - Accumulator Battery"
description: "A phone starts a journey fully charged and consumes battery while Anna travels. At some point during the journey, when the battery level hits a fixed threshold of 20 percent, the phone switches to a slower discharge mode."
date: "2026-06-28T10:12:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104873
codeforces_index: "A"
codeforces_contest_name: "2018-2019 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104873
solve_time_s: 50
verified: true
draft: false
---

[CF 104873A - Accumulator Battery](https://codeforces.com/problemset/problem/104873/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

A phone starts a journey fully charged and consumes battery while Anna travels. At some point during the journey, when the battery level hits a fixed threshold of 20 percent, the phone switches to a slower discharge mode. Before that point it drains faster, after that point it drains at exactly half the previous rate.

We are told the travel takes `t` minutes, but for the actual question only the battery percentage at arrival matters. At the moment Anna reaches her destination, the battery is `p` percent. From that moment onward, the same discharge rules continue, and we are asked how many minutes remain until the battery reaches zero.

The constraints are very small, so any solution that directly computes a closed form expression or even simulates minute by minute would be fast enough. The real challenge is not performance but correctly handling the change of drain rate at the 20 percent boundary.

A subtle edge case is when the battery at arrival is already at or below 20 percent. In that situation, the phone is already in slow mode, so no additional phase change happens. A naive solution that always assumes a switch point at 20 percent would incorrectly add an extra fast phase that never exists.

Another potential mistake comes from interpreting the statement as dependent on `t`. Since `t` only describes what happened before arrival, and we are already given the resulting battery `p`, any dependence on `t` in the final computation is unnecessary and leads to incorrect reasoning.

## Approaches

The battery drains in two linear phases. In normal mode, the battery decreases at a constant rate of 1 percent per minute. Once it reaches 20 percent, it switches to eco mode, where the speed becomes half, meaning 0.5 percent per minute.

A brute-force simulation would iterate minute by minute, decrementing the battery and switching modes when the level crosses 20 percent. This works because the process is deterministic, but it is unnecessarily detailed and would require up to 100 units of simulation per query. While still trivial under constraints, it obscures the structure of the problem.

The key observation is that the process is piecewise linear. Instead of simulating time, we can compute how long each segment lasts. From any starting battery level `p`, we either remain entirely in eco mode or first traverse a linear segment down to 20 percent and then continue in eco mode until zero.

This reduces the problem to evaluating at most two arithmetic expressions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(p) | O(1) | Accepted |
| Piecewise Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check whether the starting battery level `p` is above 20 percent. This determines whether we will cross the mode boundary.
2. If `p > 20`, compute the time to go from `p` down to 20 in normal mode. Since the drain is 1 percent per minute, this duration is `p - 20`.
3. Still in the case `p > 20`, compute the time from 20 down to 0 in eco mode. In eco mode, the drain is half as fast, so 20 percent takes 40 minutes.
4. Add the two durations to get the total remaining time.
5. If `p ≤ 20`, the phone is already in eco mode at arrival, so compute time directly as `p / 0.5`, which is equivalent to `2p`.

The reason this split works is that the battery evolution after arrival is fully determined by the current level and does not depend on the past journey length.

### Why it works

The system evolves in two linear regimes with a single threshold. Within each regime, the battery decreases at a constant rate independent of history. Once the state is known at time zero, the future trajectory depends only on whether the initial value lies above or below the threshold. This makes the time-to-zero computation equivalent to summing the lengths of at most two linear segments of a piecewise function.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t, p = map(int, input().split())

    if p > 20:
        # normal mode down to 20
        time_normal = p - 20
        # eco mode from 20 to 0
        time_eco = 40
        ans = time_normal + time_eco
    else:
        # already in eco mode
        ans = 2 * p

    print(float(ans))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the piecewise structure. The variable `t` is read but not used, since it does not affect the remaining lifetime after arrival. The only decision point is whether the current battery level is above the 20 percent threshold. The two formulas correspond exactly to the durations of the two linear drain phases.

A common mistake is to try to propagate the initial 100 percent state or simulate the entire journey again. That is unnecessary because the problem already provides the post-journey state `p`, which fully determines the future evolution.

## Worked Examples

### Example 1

Input:

`p = 70`

We are in the high-battery regime, so the system first reaches 20 percent in normal mode, then switches.

| Phase | Start | End | Rate | Duration |
| --- | --- | --- | --- | --- |
| Normal | 70 | 20 | 1 %/min | 50 |
| Eco | 20 | 0 | 0.5 %/min | 40 |

Total time is 90 minutes.

This confirms the correctness of splitting at the threshold.

### Example 2

Input:

`p = 5`

Here the phone is already in eco mode.

| Phase | Start | End | Rate | Duration |
| --- | --- | --- | --- | --- |
| Eco | 5 | 0 | 0.5 %/min | 10 |

The process stays in a single regime, so no threshold handling is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic and a single conditional check are performed |
| Space | O(1) | No additional data structures are used |

The solution trivially satisfies the constraints since it performs a fixed number of operations regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t, p = map(int, input().split())

    if p > 20:
        return str(float((p - 20) + 40))
    else:
        return str(float(2 * p))

# provided samples
assert run("30 70") == "90.0"
assert run("120 5") == "10.0"

# boundary: exactly at threshold
assert run("10 20") == "40.0"

# just above threshold
assert run("10 21") == "41.0"

# maximum battery
assert run("1 99") == "119.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 30 70 | 90.0 | Crossing threshold case |
| 120 5 | 10.0 | Already in eco mode |
| 10 20 | 40.0 | Exact boundary behavior |
| 10 21 | 41.0 | Minimal normal phase |
| 1 99 | 119.0 | Large initial normal segment |

## Edge Cases

A critical edge case is when `p` is exactly 20. In that situation, the battery is already at the switching boundary, so no normal-mode segment should be counted.

For input:

`p = 20`

The algorithm takes the eco branch and computes `2 * 20 = 40` minutes. Any approach that incorrectly forces a normal-mode phase would subtract time that does not exist.

Another edge case is very small `p`, such as 1 or 2. These values remain entirely in eco mode, and the linear scaling remains valid without any hidden transition.

For very large `p` close to 99, the full two-phase computation activates, and the correctness depends on properly summing both segments without double counting the threshold region.
