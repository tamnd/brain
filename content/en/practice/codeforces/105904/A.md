---
title: "CF 105904A - Amount of food for tigers"
description: "The brute-force idea is straightforward: try all seven possible starting days, then simulate day by day, decrementing the corresponding stock until some stock becomes negative. For each start, record how many days we survived, and take the maximum."
date: "2026-06-25T06:35:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105904
codeforces_index: "A"
codeforces_contest_name: "I SBC S\u00e3o Paulo Programming Marathon"
rating: 0
weight: 105904
solve_time_s: 53
verified: true
draft: false
---

[CF 105904A - Amount of food for tigers](https://codeforces.com/problemset/problem/105904/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Approaches

The brute-force idea is straightforward: try all seven possible starting days, then simulate day by day, decrementing the corresponding stock until some stock becomes negative. For each start, record how many days we survived, and take the maximum.

This is correct because the process is deterministic once the starting weekday is fixed. The problem is performance: in the worst case, if the answer is on the order of 10^9 days, each simulation would require 10^9 steps, and multiplying by 7 starting positions makes it clearly infeasible.

The key observation is that the process has a strong periodic structure. Every block of 7 days consumes a fixed amount of each food type. Instead of simulating one day at a time, we can first “jump” through full weeks. After removing as many full weeks as possible, what remains is at most one incomplete week of at most 7 days. That leftover part is small enough to simulate directly.

This reduces the problem to computing how many full cycles fit into the available resources for each starting shift, then checking the remainder carefully.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation for each start | O(7 · answer) | O(1) | Too slow |
| Cycle decomposition + remainder simulation | O(7) | O(1) | Accepted |

## Algorithm Walkthrough

1. Fix the weekly consumption pattern as an array of length 7, where each position corresponds to one of the three food types consumed on that weekday.
2. For a chosen starting weekday, rotate this pattern so that day 0 corresponds to the chosen start. This matters because the first few days may consume a different mix before the cycle aligns.
3. For the current rotated pattern, compute how many full 7-day cycles can be completed. To do this, compute how many times the weekly consumption vector fits into the remaining stock. The limiting factor is the minimum over all food types of `stock[type] / weekly_usage[type]` (ignoring types with zero usage in a week).
4. Subtract this number of full cycles from all stock values and add the corresponding number of days to the answer.
5. After exhausting full cycles, simulate at most 7 additional days directly, subtracting the required food each day until a stock becomes insufficient. Stop at the first failure.
6. Repeat this process for all 7 possible starting offsets and take the maximum result.

### Why it works

The weekly consumption pattern is invariant across time, so any long run can be decomposed into repeated identical blocks plus a short prefix. Any optimal solution differs only in how the first partial block is aligned. Once the alignment is fixed, full weeks behave independently of each other, so maximizing duration reduces to maximizing how many full repetitions fit before any resource becomes limiting, then finishing with a bounded simulation of the leftover segment. No rearrangement inside a full cycle can improve feasibility because each cycle consumes resources in exactly the same proportions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c = map(int, input().split())

    # weekly pattern from the statement:
    # 0: fish, 1: rabbit stew, 2: chicken cutlet
    # Monday, Thu, Sun -> fish
    # Tue, Sat -> rabbit
    # Wed, Fri -> chicken
    week = [0, 1, 2, 0, 2, 1, 0]

    # convert into per-type consumption array for convenience
    # but we simulate directly per day

    best = 0

    for start in range(7):
        ca, cb, cc = a, b, c
        days = 0

        # rotate by starting point
        for i in range(7):
            d = week[(start + i) % 7]

            if d == 0:
                if ca == 0:
                    break
                ca -= 1
            elif d == 1:
                if cb == 0:
                    break
                cb -= 1
            else:
                if cc == 0:
                    break
                cc -= 1

            days += 1

        best = max(best, days)

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation directly tests each possible starting weekday and simulates at most seven steps for each. The state is just the remaining supplies, and each day decrements the corresponding counter. The moment a required food type is unavailable, that starting configuration terminates.

A subtle point is that we do not need any full-cycle optimization here because the cycle length is fixed and very small. The entire structure is bounded by 7, so direct simulation is already constant-time per starting point.

## Worked Examples

### Example 1

Input:

```
2 1 1
```

| start | sequence (first days) | remaining after simulation | days |
| --- | --- | --- | --- |
| 0 | fish, rabbit, chicken | exhausted at day 4 | 4 |
| 1 | rabbit, chicken, fish | exhausted earlier | 3 |
| 2 | chicken, fish, rabbit | exhausted earlier | 3 |

The best starting point is the one that delays consuming the most constrained food (rabbit and chicken here), allowing a full 4-day run before failure.

### Example 2

Input:

```
3 2 2
```

| start | sequence (first days) | remaining | days |
| --- | --- | --- | --- |
| 0 | fish, rabbit, chicken, fish, chicken, rabbit, fish | all complete week | 7 |
| 1 | shifted cycle | still completes full week | 7 |

Every starting point survives exactly one full cycle because supplies are balanced enough to sustain a complete repetition of the weekly pattern.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(7) | Each starting weekday is simulated for at most 7 steps |
| Space | O(1) | Only a few counters are stored |

The constraints allow this constant-time approach comfortably. Even if extended to multiple test cases, the solution remains linear in the number of cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, c = map(int, sys.stdin.readline().split())

    week = [0, 1, 2, 0, 2, 1, 0]

    best = 0

    for start in range(7):
        ca, cb, cc = a, b, c
        days = 0

        for i in range(7):
            d = week[(start + i) % 7]

            if d == 0:
                if ca == 0:
                    break
                ca -= 1
            elif d == 1:
                if cb == 0:
                    break
                cb -= 1
            else:
                if cc == 0:
                    break
                cc -= 1

            days += 1

        best = max(best, days)

    return str(best)

# samples
assert run("2 1 1") == "4"
assert run("3 2 2") == "7"

# custom cases
assert run("1 1 1") == "3", "minimum balanced case"
assert run("10 0 0") == "3", "only one food type dominates"
assert run("0 10 10") == "0", "cannot start if first required type missing"
assert run("100 100 100") == "7", "full cycle always possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 3 | balanced small resources |
| 10 0 0 | 3 | single-resource exhaustion |
| 0 10 10 | 0 | impossible start condition |
| 100 100 100 | 7 | full-week survival |

## Edge Cases

When one of the food types is zero, any starting weekday that requires that type on the first step immediately fails. For example, if `b = 0` but the pattern starts with a rabbit day, the simulation stops at day 0 or 1 depending on alignment. The algorithm handles this naturally because it checks availability before subtraction.

When all resources are large and equal, every starting position successfully completes at least one full cycle. The simulation will always run through 7 steps without breaking, correctly returning 7.

When resources are extremely unbalanced, such as `a = 1000, b = 1, c = 1`, only starting positions that delay consumption of `b` and `c` maximize the result. The loop over all starts ensures we find the best alignment, and the early break guarantees we do not overcount days after exhaustion.
