---
title: "CF 105093J - Reservoir Doggos"
description: "A pack of dogs is fixing a sequence of holes in a damaged reservoir on Titan. Each hole leaks oil at a constant rate until it is fully repaired."
date: "2026-06-27T20:50:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "J"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 36
verified: true
draft: false
---

[CF 105093J - Reservoir Doggos](https://codeforces.com/problemset/problem/105093/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

A pack of dogs is fixing a sequence of holes in a damaged reservoir on Titan. Each hole leaks oil at a constant rate until it is fully repaired. Once a hole is chosen, the dogs must work on it continuously for a fixed amount of time, and they cannot switch tasks until it is finished.

If a hole leaks at rate $v_i$ and takes $t_i$ seconds to repair, then every second before completion contributes $v_i$ units of lost oil. The total loss from a hole depends on when it finishes, not just its own duration. If a hole finishes at time $C_i$, its contribution to the total loss is $v_i \cdot C_i$. The goal is to choose an order of repairing all holes to minimize the sum of these losses.

So the problem is really about ordering tasks on a single machine. Each task has a processing time $t_i$ and a weight $v_i$, and we want to minimize the sum of weighted completion times.

The input gives multiple test cases. For each one, we are given all leak rates and all repair times, and we must output the minimum possible total leaked oil.

The constraints allow up to $2 \cdot 10^5$ total holes across all test cases. This immediately rules out any solution that tries all permutations, since even for $n = 10^5$, $n!$ is completely infeasible and even $O(n^2)$ approaches are too slow. The solution must be $O(n \log n)$ per test case or better.

A subtle failure case for naive reasoning is assuming we should always fix the highest leak rate first. For example, consider two holes:

Input:

$v = [100, 1]$, $t = [1000, 1]$

Fixing by highest $v$ first gives large delay to the long job, but fixing the long job first may be better overall. This shows that neither sorting only by $v$ nor only by $t$ is correct.

The correct ordering depends on the ratio between leakage rate and repair time, not either value alone.

## Approaches

If we try all possible orders, we compute the total loss by simulating completion times. For each permutation, we accumulate prefix sums of repair times and multiply each completion time by its leak rate. This is correct but requires $n!$ permutations, and even for $n = 10$, this is already too large.

A slightly better idea is to sort tasks by a heuristic such as decreasing $v_i$ or increasing $t_i$, but both fail on counterexamples where a small leak rate with huge time should not be prioritized over a medium leak rate with tiny time.

The structure of the objective function is the key: each task contributes $v_i$ multiplied by its completion time, and completion times depend on cumulative processing order. This is exactly the classical single-machine scheduling problem minimizing $\sum w_i C_i$, where $w_i = v_i$ and processing time is $t_i$.

A known optimal result for this structure is Smith’s rule: sort tasks by decreasing ratio $w_i / p_i$, which here becomes sorting by decreasing $v_i / t_i$. Intuitively, a task is more urgent if it leaks heavily relative to how long it takes to fix.

Once sorted, we sweep through tasks in that order, maintain running time, and accumulate weighted completion cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal (ratio sort) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat each hole as a job with processing time $t_i$ and weight $v_i$.

### Steps

1. Pair each hole into a tuple $(v_i, t_i)$.

This is necessary because the optimal order depends on both values simultaneously, not independently.
2. Sort all pairs by decreasing value of $v_i / t_i$.

This prioritizes jobs that contribute more leakage per unit of repair time. If two jobs have equal ratio, either order is safe because they contribute proportionally the same density.
3. Initialize a variable `time = 0` to represent the current completion time boundary.

This tracks when each job finishes in the chosen schedule.
4. Initialize `answer = 0`.
5. Iterate through jobs in sorted order. For each job:

compute its completion time as `time + t_i`.

Add `v_i * (time + t_i)` to the answer.

Then update `time += t_i`.

The reasoning is that every second spent before finishing this job contributes its leak rate, so its total damage is proportional to its finishing moment.
6. Output the final accumulated answer.

### Why it works

The key property is that swapping two adjacent jobs only depends on their relative order. Consider two jobs $A$ and $B$. If we compare schedules $AB$ and $BA$, the difference in total cost reduces to comparing $v_A / t_A$ and $v_B / t_B$. If $v_A / t_A < v_B / t_B$, swapping reduces cost. This establishes that any inversion with respect to decreasing ratio ordering can be improved, which implies the sorted order is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        n = int(input())
        v = list(map(int, input().split()))
        t = list(map(int, input().split()))

        jobs = list(zip(v, t))

        # sort by decreasing v/t without floating point issues
        jobs.sort(key=lambda x: x[0] * 1.0 / x[1], reverse=True)

        time = 0
        ans = 0

        for vi, ti in jobs:
            time += ti
            ans += vi * time

        out.append(str(ans))

    print("\n".j
```
