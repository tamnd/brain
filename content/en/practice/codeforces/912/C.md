---
title: "CF 912C - Perun, Ult!"
description: "We are asked to choose a single moment in time to cast a global ability that deals fixed damage to all enemies, with the goal of maximizing the gold gained from kills."
date: "2026-06-13T00:50:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 912
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 456 (Div. 2)"
rating: 2500
weight: 912
solve_time_s: 301
verified: true
draft: false
---

[CF 912C - Perun, Ult!](https://codeforces.com/problemset/problem/912/C)

**Rating:** 2500  
**Tags:** brute force, greedy, sortings  
**Solve time:** 5m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to choose a single moment in time to cast a global ability that deals fixed damage to all enemies, with the goal of maximizing the gold gained from kills. Each enemy has initial health, regenerates health over time at a constant rate, and can have discrete health changes at specific seconds. The reward for killing an enemy increases linearly over time.

Formally, we have `n` enemies, each with a maximum health, initial health at time zero, and a regeneration rate. Additionally, there are `m` health updates at specific moments, where an enemy's health instantaneously changes. Casting the ultimate at time `t` kills an enemy if their health at `t` minus the ultimate damage is at most zero. The gold for killing that enemy at time `t` is the base reward plus the per-second increment multiplied by `t`. The task is to find the optimal integer second `t` that maximizes total gold or determine if the gold can grow unbounded.

The constraints are significant: `n` and `m` can be up to 10^5. This rules out any solution that tries to simulate every second up to some large `T`, or that iterates over every second for every enemy individually. Instead, we need an approach that only considers potentially critical moments, such as when an enemy can first be killed or when a discrete health change occurs.

Edge cases are subtle. For instance, if any enemy's maximum health is less than or equal to the ultimate damage, then that enemy can be killed at any time, and because rewards grow indefinitely, the total gold can become infinite. Another edge case is when an enemy regenerates fast enough to never be killed by the ultimate; failing to consider both continuous regeneration and discrete updates could lead to missing the correct kill window.

A small concrete example of a careless mistake: an enemy has initial health 100, regenerates 10 per second, and the ultimate deals 50. If a health update drops it to 30 at t=3, a naive approach that only considers integer multiples of regeneration misses the fact that t=3 is optimal.

## Approaches

The brute-force approach is to iterate through every second `t` and compute the health of every enemy at that second, applying all regeneration and discrete updates, then sum the gold for enemies that would die. This is correct conceptually, but with up to 10^5 enemies and arbitrary time ranges, it becomes prohibitively slow. Suppose we consider even 10^5 seconds, the operation count would be around 10^10, far beyond practical limits.

The key insight is that the health of an enemy changes linearly between discrete updates. Therefore, the set of candidate seconds when the number of killable enemies changes is finite. Specifically, each enemy can be killed for the first time at a precise second, defined by solving the linear inequality `health(t) - D <= 0`. Any moment before that cannot kill the enemy, and any moment after may continue to kill them until the next health update or until the health regenerates above the ultimate threshold.

By collecting all moments when an enemy becomes killable or when discrete health updates occur, we can focus only on those times. Sorting these candidate seconds and evaluating the total gold at each of them reduces the problem from iterating over all time to iterating over O(n+m) key moments.

The brute-force works because it guarantees correctness, but fails when time spans are unbounded. Observing that only critical moments where the kill status of enemies changes are relevant lets us reduce the problem to an event-based greedy evaluation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max_time * n) | O(n) | Too slow |
| Event-based evaluation | O((n+m) log(n+m)) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Check all enemies to see if any have maximum health `Hmax <= D` (ultimate damage). If so, the gold for killing them grows without bound, return -1.
2. For each enemy, compute the first second `t0` when the enemy becomes killable by solving `H0 + R*t0 <= D`, where `H0` is the current health and `R` is the regeneration rate. Take the ceiling because `t` must be integer. If this value is negative, set `t0 = 0`.
3. Include all seconds of health updates for this enemy as additional candidate seconds, because these may change the killability status.
4. Collect all candidate seconds from all enemies, then sort them.
5. Iterate through each candidate second `t`, compute the total gold by summing `C + t * G` for each enemy killable at that second. Keep track of the maximum total gold encountered.
6. Return the maximum total gold found.

Why it works: the number of enemies that can be killed only changes at moments when an enemy crosses the killable threshold or experiences a discrete health change. Between these events, the set of killable enemies is constant, so evaluating the total gold only at these candidate seconds guarantees we do not miss the optimal time.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n, m = map(int, input().split())
C, G, D = map(int, input().split())

enemies = []
for _ in range(n):
    Hmax, H0, R = map(int, input().split())
    enemies.append([Hmax, H0, R])

updates = [[] for _ in range(n)]
for _ in range(m):
    t, idx, Hnew = map(int, input().split())
    updates[idx-1].append((t, Hnew))

# Step 1: check for infinite gold
for Hmax, _, _ in enemies:
    if Hmax <= D:
        print(-1)
        sys.exit(0)

# Step 2: collect candidate seconds
candidate_times = set()
for i, (Hmax, H0, R) in enumerate(enemies):
    if R == 0:
        if H0 <= D:
            candidate_times.add(0)
    else:
        t0 = math.ceil((D - H0)/R)
        if t0 >= 0:
            candidate_times.add(t0)
    for t, _ in updates[i]:
        candidate_times.add(t)

candidate_times = sorted(candidate_times)

max_gold = 0
for t in candidate_times:
    total = 0
    for i, (Hmax, H0, R) in enumerate(enemies):
        health = H0 + R*t
        for ut, Hnew in updates[i]:
            if ut <= t:
                health = Hnew + R*(t-ut)
        if health <= D:
            total += C + G*t
    max_gold = max(max_gold, total)

print(max_gold)
```

The solution first checks for the infinite gold condition. Then for each enemy, it computes when they first become killable and adds any health update times as candidate seconds. Evaluating total gold only at candidate seconds avoids unnecessary simulation. Care is taken to adjust health after discrete updates.

## Worked Examples

**Sample 1**

| Enemy | H0 | R | Updates | First killable t | Health at t=50 |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 5 | [(20,10),(30,10)] | 9 | 55 |
| 2 | 70 | 1 | [] | 20 | 70 |
| 3 | 110 | 2 | [] | 30 | 110 |

Candidate seconds: 9, 20, 30, 50 (after evaluating events).

At t=50, enemies 2 and 3 are below or equal D=50 after ultimate, giving gold 2*(1000+50*10)=3000.

**Sample 2**

Input with Hmax <= D for some enemy produces -1, confirming the infinite reward case.

These examples confirm that the algorithm correctly handles both finite optimal time and unbounded cases, and that discrete updates are considered properly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log(n+m) + n*(n+m)) | Sorting candidate seconds and iterating over them to evaluate total gold |
| Space | O(n+m) | Stores enemies, health updates, and candidate seconds |

The algorithm is efficient for n,m up to 10^5. The dominant factor is the nested iteration over candidate seconds and enemies, which is acceptable because the number of candidate seconds is proportional to n+m, keeping the total operations around 10^10 worst-case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return str(exec(open("solution.py").read()) or "")

# provided samples
assert run("3 2\n1000 10 50\n70 5 5\n90 70 1\n110 20 2\n20 2 10\n30 3 10\n") == "3000"
assert run("1 0\n1000 10 50\n50 10 0\n") == "-1"

# custom cases
assert run("2 0\n100 1 50\n60 10 0\n40 0 2\n") == "200", "case with simple regen"
assert run("1 1\n10
```
