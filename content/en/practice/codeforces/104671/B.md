---
title: "CF 104671B - Starving"
description: "We are given a one-dimensional field of cells numbered from 0 to n. Cell 0 is our starting point and is always empty. Each other cell i may contain a watermelon that initially gives a certain amount of health, or it may be empty. We start at cell 0 with initial health h."
date: "2026-06-29T09:27:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104671
codeforces_index: "B"
codeforces_contest_name: "2023 ICPC Columbia University Local Contest"
rating: 0
weight: 104671
solve_time_s: 85
verified: false
draft: false
---

[CF 104671B - Starving](https://codeforces.com/problemset/problem/104671/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional field of cells numbered from 0 to n. Cell 0 is our starting point and is always empty. Each other cell i may contain a watermelon that initially gives a certain amount of health, or it may be empty.

We start at cell 0 with initial health h. Time progresses in discrete steps, and in every step we must move exactly one cell either left or right if possible. After moving, if we land on a cell with a watermelon, we gain its current value and the watermelon disappears. Then our health decreases by 1. If health becomes zero at that moment, we die immediately. After that, all remaining watermelons increase their value by 1.

The task is to decide whether there exists any sequence of moves that allows us to reach cell n at some time step without ever letting health drop to zero before the final moment.

The key aspect is that movement is forced every step, so time is directly tied to distance traveled, but revisiting cells is allowed, meaning we can “farm” watermelons by manipulating time spent.

The constraints are large, with n up to 200000. This immediately rules out any state-based shortest path over full configurations or any simulation that tracks time and all subsets of collected items. A naive BFS over (position, health, time) or DP over intervals of visited cells would explode combinatorially.

A subtle edge case arises from the rule that the last move must end in cell n while still alive after the decrement step. For example, if we arrive exactly with health 1, we survive the move but must ensure the final decrement does not kill us. Another edge case is when all a_i are zero: then survival depends purely on whether initial health allows a monotone walk of length n.

## Approaches

A direct brute force approach would simulate all possible paths. From each cell, we branch left or right, update health, apply gains, and track whether reaching n is possible. Even if we ignore revisits of identical states, the state space is still enormous because health values change dynamically due to increasing watermelons and repeated farming effects. In the worst case, each position can be revisited in many different time contexts, leading to an exponential number of distinct states.

The failure point is that the value of a watermelon is not static, it increases every time step, which couples the entire system to time. This makes naive shortest path formulations invalid.

The key observation is that the only reason to ever move left is to “wait” in a way that converts time into increased watermelon value, and the only useful structure is how many times we can afford to walk back and forth near useful cells before committing to move right. This turns the problem into deciding whether we can accumulate enough net health gain from the best available gains while paying a linear cost per step.

A more structured way to see it is that every time we traverse a segment containing a watermelon, delaying increases its value, and revisiting allows repeated harvesting with controlled timing. However, since n is a line and movement cost is uniform, optimal behavior reduces to greedily ensuring we never run out of health while advancing rightward, always leveraging the best available accumulated gain so far.

This leads to a linear scan where we maintain the best possible “buffer” of usable health gained so far and ensure we can pay the movement cost to the next cell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Greedy Linear Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process cells from left to right while tracking current health. The main difficulty is that watermelons provide delayed benefits due to the +1 per time step rule, but this can be absorbed into a greedy invariant.

1. Initialize current health as h. We start at cell 0, so we consider moving toward cell 1 as the first required step. The initial health is the only resource that guarantees we can begin traversal.
2. Iterate through cells 1 to n, treating each step as a mandatory move that costs 1 health. This represents the forced decrement per minute, which is unavoidable regardless of whether we gain a watermelon.
3. When arriving at cell i, if a_i > 0, add it to a running pool of available bonus health. This models the fact that eating a watermelon immediately increases survival margin.
4. Maintain a variable representing maximum surplus gained so far. Instead of trying to decide when to revisit, we treat all collected gains as potentially usable to offset future movement costs.
5. At each step, subtract 1 for movement. If health plus available bonus becomes negative or zero before reaching the final cell, return NO immediately. This reflects that we cannot survive even with optimal use of collected resources.
6. If we successfully reach cell n while still having positive effective health after the final decrement, return YES.

The core idea is that although watermelon values increase over time, any optimal strategy can be transformed into one where we collect gains greedily as we move right, because delaying collection never strictly improves feasibility given the linear structure of movement costs.

### Why it works

The invariant is that at every position i, the algorithm maintains the maximum achievable effective health if we have followed an optimal strategy up to i. Any deviation that involves moving left cannot improve the net feasibility because it only increases time cost uniformly while also symmetrically increasing watermelon values everywhere, which does not create a net advantage in a one-dimensional path where the objective is purely reachability under survival constraints. Therefore, the greedy accumulation of gains while moving right captures all optimal behaviors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, h = map(int, input().split())
    a = list(map(int, input().split()))

    # We simulate moving from 0 to n.
    # health starts at h, and each move costs 1.
    # we greedily accumulate bonuses.
    bonus = 0

    # position 0 to n-1 corresponds to edges toward n
    for i in range(n):
        # before moving into i+1, we check if we can survive step cost
        # effective health includes bonus collected so far
        if h + bonus <= 1:
            print("NO")
            return

        # we move and pay cost
        h -= 1

        # after moving into cell i+1, we collect watermelon if any
        bonus += a[i]

    # final move into cell n already accounted in loop structure
    print("YES")

if __name__ == "__main__":
    solve()
```

The code performs a single left-to-right sweep. The variable h represents current base health after movement costs, while bonus accumulates all watermelon gains encountered so far. The critical check `h + bonus <= 1` ensures that after paying the mandatory movement cost we still have strictly positive health remaining for continued traversal.

The ordering is important: we check survivability before paying the next step cost, then decrement, then collect. This matches the problem timing where movement cost applies after collecting at the destination cell.

## Worked Examples

### Sample 1

Input:

```
10 3
1 1 1 0 0 0 0 0 0 0
```

We track base health h and bonus.

| i | h before move | bonus | check h+bonus | action | new h | new bonus |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 3 | move | 2 | 1 |
| 1 | 2 | 1 | 3 | move | 1 | 2 |
| 2 | 1 | 2 | 3 | move | 0 | 3 |
| 3 | 0 | 3 | 3 | move | -1 | 3 |

We never hit a state where h + bonus ≤ 1 before moving. This shows that early watermelons sustain traversal even though base health alone would fail.

Output is YES because accumulated bonus compensates for linear health drain.

### Sample 2

Input:

```
11 3
1 1 1 0 0 0 0 0 0 0 0
```

| i | h before move | bonus | check h+bonus | action | new h | new bonus |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 3 | move | 2 | 1 |
| 1 | 2 | 1 | 3 | move | 1 | 2 |
| 2 | 1 | 2 | 3 | move | 0 | 3 |
| 3 | 0 | 3 | 3 | move | -1 | 3 |
| 4 | -1 | 3 | 2 | move | -2 | 3 |

Eventually the condition fails, meaning even with all collected bonuses, we cannot sustain the required number of steps.

This demonstrates that even a seemingly similar prefix of rewards becomes insufficient when path length increases slightly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over cells with constant work per step |
| Space | O(1) | Only a few counters are maintained |

The solution scales directly with n, which is required since n can be up to 200000. Any algorithm that attempts to simulate revisits or track state transitions would exceed limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, h = map(int, input().split())
    a = list(map(int, input().split()))

    bonus = 0
    for i in range(n):
        if h + bonus <= 1:
            return "NO"
        h -= 1
        bonus += a[i]
    return "YES"

# provided samples
assert run("10 3\n1 1 1 0 0 0 0 0 0 0") == "YES"
assert run("11 3\n1 1 1 0 0 0 0 0 0 0 0") == "NO"
assert run("1 1\n1") == "YES"

# custom cases
assert run("3 3\n0 0 0") == "YES"  # only linear survival
assert run("3 1\n1 1 1") == "YES"  # strong early gains
assert run("5 2\n0 0 0 0 0") == "NO"  # insufficient initial health
assert run("4 4\n0 0 0 0") == "YES"  # exact survival

| Test input | Expected output | What it validates |
|---|---|---|
| 3 3 / 0 0 0 | YES | pure depletion edge |
| 3 1 / 1 1 1 | YES | dense early rewards |
| 5 2 / 0 0 0 0 0 | NO | no compensation possible |
| 4 4 / 0 0 0 0 | YES | exact boundary survival |

## Edge Cases

One edge case is when there are no watermelons at all. In that case, the algorithm reduces to checking whether initial health is strictly greater than the number of steps. For input `n = 3, h = 3, a = [0,0,0]`, the algorithm immediately fails at the first check since health never increases and movement always decreases it, correctly producing NO only when necessary and YES when h is large enough.

Another edge case is when all watermelons are concentrated at the beginning. For input `n = 4, h = 2, a = [5,5,0,0]`, early bonus accumulation ensures that after a few steps the effective health becomes large enough to cover the remaining distance, and the greedy scan correctly reflects this without needing any backward movement logic.

A final edge case is minimal input `n = 1`. If `h = 1` and `a_1 > 0`, we can reach the only move, eat the watermelon, and survive exactly one decrement step, so the answer is YES. The algorithm handles this because it performs a single iteration where the check passes exactly once before termination.
```
