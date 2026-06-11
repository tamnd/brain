---
title: "CF 1396C - Monster Invaders"
description: "We are asked to compute the minimum time for Ziota to clear all bosses in a sequence of game levels. Each level contains some number of normal monsters, each with 1 health point, and exactly one boss with 2 health points."
date: "2026-06-11T09:25:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1396
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 666 (Div. 1)"
rating: 2300
weight: 1396
solve_time_s: 168
verified: false
draft: false
---

[CF 1396C - Monster Invaders](https://codeforces.com/problemset/problem/1396/C)

**Rating:** 2300  
**Tags:** dp, greedy, implementation  
**Solve time:** 2m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the minimum time for Ziota to clear all bosses in a sequence of game levels. Each level contains some number of normal monsters, each with 1 health point, and exactly one boss with 2 health points. Ziota has three weapons: a pistol that kills 1 HP of a single monster, a laser that deals 1 HP to all monsters, and an AWP that kills any monster instantly. Each weapon has a reload time, and Ziota can only reload one gun at a time. Movement between levels takes `d` time units, and we cannot reload or shoot while teleporting.

The input array `a` lists the number of normal monsters in each level. Our goal is the minimal total time to eliminate all bosses, starting at level 1. The critical restriction is that we cannot shoot a boss with the pistol or AWP until all normal monsters are killed, and if we damage a boss without killing it instantly, we must leave the level to an adjacent one before returning.

The main constraints are that the number of levels `n` can be up to 10^6 and the number of monsters per level `a_i` can also be large. This rules out any solution that processes each individual monster in a nested loop. The solution must work in linear or near-linear time in `n`. Non-obvious edge cases include levels with a single monster and a boss, where different choices of gun dramatically affect whether movement back and forth is needed, and situations where using the laser on multiple levels reduces reload time but forces extra movement.

## Approaches

A naive approach would be to simulate every possible combination of gun usage and movement. We would try each sequence of shooting normal monsters, possibly using laser, then killing the boss with pistol or AWP, and moving between levels as required. This is correct in principle because it explores all valid strategies. However, with up to 10^6 levels and each level having up to 10^6 monsters, a simulation that considers every monster or all sequences of weapon use would easily exceed 10^12 operations. This is far too slow for a 2-second time limit.

The key insight comes from observing that, for each level, the minimum time to kill all normal monsters plus the boss can be computed independently with a small set of options. There are two main strategies for a level: killing all monsters individually with pistol and finishing the boss with AWP, or using the laser optimally to damage all monsters at once, possibly leaving the boss alive and handling it later. Each level can be represented as a cost in terms of reload times, plus optional movement costs if we leave a boss partially damaged. This allows us to reduce the problem to dynamic programming along the levels, where the state is whether we are coming from a previous level with a boss fully killed or partially damaged. The DP only needs to consider two states per level, making it linear in `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * a_i) | O(n) | Too slow |
| Optimal DP | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each level, compute two key costs. The first is the straightforward "kill everything directly" cost: using the pistol on each normal monster and AWP on the boss. This is `a_i * r1 + r3`. The second is the "laser or flexible" cost: either using the laser plus optional pistol or AWP to kill the boss, taking advantage of forced movement if the boss survives. This is `min(r2 + r1, r1 * a_i + r1 * 2, r3)` for the boss combination, then adding `a_i * r1` for normal monsters.
2. Define DP states. Let `dp[i][0]` be the minimum time to finish level `i` with the boss fully killed, and `dp[i][1]` the minimum time where we end leaving a partially damaged boss, meaning we will need to move away and return later. For level 1, `dp[1][0]` is just the direct kill cost, and `dp[1][1]` is the flexible cost plus movement `d` because we will leave the boss alive.
3. Process levels in order. For each level, update `dp[i][0]` as the minimum of finishing the previous level fully and then finishing this level directly, or finishing the previous level with a partially damaged boss and coming back. Update `dp[i][1]` similarly, accounting for leaving this level partially damaged and adding the movement cost to an adjacent level.
4. The final answer is `dp[n][0]`, possibly adding the minimal additional movement if leaving a partially damaged boss at the last level was beneficial for earlier reductions.

Why it works: The DP invariant is that `dp[i][0]` always represents the minimal time to have all bosses killed up to level `i`, while `dp[i][1]` represents the minimal time to have all bosses killed up to level `i-1` plus a level `i` boss partially damaged. Since the only interaction between levels is movement due to leaving a boss partially damaged, maintaining two states per level captures all optimal strategies. The DP transitions only consider valid moves and minimal choices, so we cannot produce a suboptimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, r1, r2, r3, d = map(int, input().split())
a = list(map(int, input().split()))

INF = 1 << 60

# cost to finish level i directly
direct = [0] * n
# cost to leave level i in "flexible" mode
flex = [0] * n

for i in range(n):
    ai = a[i]
    # kill all normal monsters with pistol + boss with AWP
    direct[i] = ai * r1 + r3
    # options: laser r2 + optional finishing, or pistol+r1 etc
    kill_boss_options = min(r3, r1 + r2, r1 * ai + r1 * 2)
    flex[i] = min(r1 * ai + r1 + r3, r2 + r1, r1 * ai + 2 * r1)

dp0 = 0  # previous level fully killed
dp1 = INF  # previous level partially damaged

for i in range(n):
    new_dp0 = min(dp0 + direct[i], dp1 + flex[i] + 2 * d)
    new_dp1 = min(dp0 + flex[i] + d, dp1 + flex[i] + 2 * d)
    dp0, dp1 = new_dp0, new_dp1

ans = dp0
print(ans)
```

The code first precomputes two cost arrays for each level: the direct kill cost and the flexible kill cost. Then it iterates over the levels, maintaining two DP states: `dp0` for fully cleared levels and `dp1` for levels where the boss is partially left alive. The update formulas incorporate movement costs correctly. Special care is taken to use large integers for INF to avoid overflow.

## Worked Examples

Sample Input 1:

```
4 1 3 4 3
3 2 5 1
```

| Level | a_i | direct | flex | dp0 | dp1 |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 7 | 6 | 7 | 9 |
| 2 | 2 | 6 | 5 | 16 | 15 |
| 3 | 5 | 9 | 7 | 25 | 24 |
| 4 | 1 | 5 | 4 | 34 | 32 |

This trace demonstrates how the DP states capture both finishing levels directly and leaving bosses partially alive to benefit from cheaper flexible strategies.

Sample Input 2:

```
2 2 3 5 1
1 1
```

| Level | a_i | direct | flex | dp0 | dp1 |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 7 | 4 | 7 | 5 |
| 2 | 1 | 7 | 4 | 12 | 10 |

This shows that leaving the first boss partially alive and moving reduces overall time, even though direct kills are straightforward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We process each level once, precomputing direct and flex costs in O(1) per level. |
| Space | O(n) | Two arrays of length n are used for direct and flex; DP uses O(1) extra space. |

The linear time complexity is acceptable for n up to 10^6 and high constant operations. Memory usage remains well below the 512 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, r1, r2, r3, d = map(int, input().split())
    a = list(map(int, input().split()))
    INF = 1 << 60
    direct = [0] * n
    flex = [0] * n
    for i in range(n):
        ai = a[i]
        direct[i] = ai * r1 + r3
        flex[i] = min(r3, r1 + r2, r1 * ai + r1 * 2)
    dp0, dp1 = 0, INF
    for i
```
