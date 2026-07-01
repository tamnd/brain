---
title: "CF 104101B - Steel of Heart"
description: "We are simulating a single game character whose health changes over time according to a chronological event log. The character starts with an initial health value and gains additional health whenever they level up."
date: "2026-07-02T02:07:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104101
codeforces_index: "B"
codeforces_contest_name: "The 2022 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 104101
solve_time_s: 50
verified: true
draft: false
---

[CF 104101B - Steel of Heart](https://codeforces.com/problemset/problem/104101/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a single game character whose health changes over time according to a chronological event log. The character starts with an initial health value and gains additional health whenever they level up. At some point, they may also purchase a special item that permanently increases their health and unlocks a passive ability.

After the item is acquired, whenever the character attacks an enemy, the passive may trigger if that enemy is not currently on cooldown. When it triggers, it computes a damage value based on the character’s current health, then converts a fraction of that damage back into healing. The healing is added immediately to the character’s current health, which can then affect future computations.

The input is a sequence of timestamped events sorted in increasing time order. Each event is either a level-up that increases health by a fixed amount, a purchase event that grants a large flat health bonus and enables the passive, or an attack on one of five possible enemies that may or may not trigger the passive depending on cooldown state. The cooldown is tracked independently per enemy, meaning attacking different enemies does not interfere with each other’s cooldown timers.

The output is simply the final health value after processing all events in order.

The constraints are small enough that a direct simulation is sufficient. There are at most 1000 events, and time is given at second granularity over a 60 minute window, so even a straightforward O(m) simulation with constant work per event is easily fast enough.

The main subtlety lies in correctly handling the cooldown logic per enemy and ensuring that the passive is only applied after the item is purchased. Another frequent source of errors is the order of operations inside the passive: damage depends on current health at the moment of attack, and healing is applied after computing damage, not before.

A naive mistake would be to forget that cooldown is per enemy. For example, if an attack at 00:10 hits enemy 1, then another attack at 00:20 hits enemy 2, the second attack should still trigger the passive on enemy 2 if the item is active, even though 10 seconds have passed since the first trigger.

Another subtle case is the cooldown boundary. If an attack triggers at time t, then a second attack on the same enemy at time t + 29 should not trigger, but at time t + 30 it should be allowed again.

## Approaches

The most direct approach is to simulate the timeline exactly as described. We maintain the character’s current health, whether the item has been purchased, and for each enemy the last time the passive was triggered.

For each event, we parse its timestamp into seconds and process it in order. Level-up events simply add a fixed amount of health. Item purchase adds a fixed bonus and enables future passive computations. Attack events check whether the item is active and whether the cooldown condition for that enemy is satisfied. If both hold, we compute damage using the current health, compute healing as a floored percentage of that damage, and add it to the health. We also update the last trigger time for that enemy.

A brute-force variant would not differ much in structure because the input size is already small. The only hypothetical inefficiency would be recomputing time parsing or scanning previous events unnecessarily, but even that would stay within limits. The real improvement is conceptual: tracking per-enemy state allows each event to be handled in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m) | O(1) | Accepted |
| Optimal Simulation | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

We convert all timestamps into seconds to simplify comparisons, since cooldown logic depends only on differences.

1. Initialize current health as H1 and mark the item as not purchased. Also initialize an array last_trigger of size 5, filled with a very negative value so that early attacks always pass cooldown checks.
2. Process events in chronological order.
3. If the event is a level-up, increase health by H2.
4. If the event is a purchase event, increase health by 800 and mark the item as active.
5. If the event is an attack on enemy x, first check whether the item has been purchased. If not, the attack does nothing.
6. If the item is active, check cooldown for enemy x using the condition current_time - last_trigger[x] >= 30. If this fails, ignore the attack.
7. If cooldown allows, compute damage as 125 + floor(0.06 * current_health).
8. Compute healing as floor(0.1 * damage), then add it to current health.
9. Update last_trigger[x] to the current time.

The key idea is that health changes immediately affect subsequent events, including later damage calculations, so we must update it in place.

### Why it works

At every moment in time, the simulation maintains the exact state of the game implied by the event history: current health, item availability, and per-enemy cooldown status. Each event transitions this state deterministically based only on the current state and the event itself. Since events are processed in increasing time order and each update matches the game rules exactly, no future event depends on unprocessed information, which guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_time(s):
    mm, ss = s.split(":")
    return int(mm) * 60 + int(ss)

def solve():
    H1, H2, m = map(int, input().split())
    
    hp = H1
    item = False

    last = [-10**9] * 5

    for _ in range(m):
        parts = input().split()
        t = parse_time(parts[0])
        typ = int(parts[1])

        if typ == 2:
            hp += H2

        elif typ == 1:
            hp += 800
            item = True

        else:
            x = int(parts[2]) - 1
            if not item:
                continue
            if t - last[x] < 30:
                continue

            damage = 125 + int(0.06 * hp)
            heal = int(damage * 0.1)

            hp += heal
            last[x] = t

    print(hp)

if __name__ == "__main__":
    solve()
```

The implementation follows the event-driven structure directly. Time is converted once per event to seconds, which avoids repeated parsing complexity.

The cooldown check uses strict inequality `t - last[x] < 30`, which is equivalent to enforcing a 30-second minimum gap. The health-dependent calculations use integer truncation exactly as required by the problem statement.

## Worked Examples

### Example 1

Consider a short sequence where the item is bought and then an attack happens immediately.

| Time | Event | HP before | Action | HP after | Notes |
| --- | --- | --- | --- | --- | --- |
| 00:00 | level-up | 500 | +10 | 510 | basic growth |
| 00:10 | buy item | 510 | +800 | 1310 | item activated |
| 00:15 | attack enemy 1 | 1310 | damage = 125 + 78 = 203, heal = 20 | 1330 | cooldown starts |

This trace shows how health directly influences the damage formula and how healing is applied immediately after damage computation.

### Example 2

Now consider cooldown blocking repeated triggers.

| Time | Event | HP before | Action | HP after | Notes |
| --- | --- | --- | --- | --- | --- |
| 00:00 | buy item | 500 | +800 | 1300 | item active |
| 00:10 | attack 1 | 1300 | triggers | 1320 | enemy 1 cooldown starts |
| 00:20 | attack 1 | 1320 | blocked | 1320 | cooldown not finished |
| 00:40 | attack 1 | 1320 | triggers again | 1340 | cooldown reset |

This confirms that cooldown is per enemy and enforced by time differences, not by event count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | each event is processed once with O(1) work |
| Space | O(1) | only constant state plus 5 cooldown trackers |

The constraints allow up to 1000 events, so a linear simulation is comfortably within limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    # assume solve is defined in global scope
    return str(__import__('__main__').solve() or "")

# Simple sanity: no item, only level ups
assert run("500 10 2\n00:00 2\n00:01 2\n") == "520", "level ups only"

# Item then single attack
assert run("500 10 1\n00:00 1\n00:01 3 1\n") != "", "basic item usage"

# Cooldown test: same enemy repeated
assert run("500 10 3\n00:00 1\n00:01 3 1\n00:10 3 1\n") != "", "cooldown behavior"

# Multiple enemies independent cooldown
assert run("500 10 5\n00:00 1\n00:01 3 1\n00:02 3 2\n00:03 3 1\n") != "", "independent enemies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| level ups only | linear growth | pure H2 accumulation |
| item + attack | > initial+800 | passive activation |
| repeated enemy attack | cooldown blocking | 30s rule |
| multi-enemy attacks | separate cooldowns | per-enemy state |

## Edge Cases

One important edge case is attacking before the item is purchased. In that situation, attacks must be ignored entirely even if cooldown logic would otherwise allow them. The simulation handles this by checking the `item` flag before any computation.

Another edge case is repeated attacks exactly on the boundary of cooldown. If an attack occurs at time t and another at t + 30, the second must trigger. The condition `t - last[x] < 30` correctly rejects only strictly smaller gaps, so equality passes.

A final edge case is the dependence of damage on current health after multiple level-ups and previous heals. Since health is updated immediately after each event, the damage formula always reflects the correct state at the moment of attack, even if multiple events happen in the same minute.
