---
title: "CF 105006F - Walk in the Park"
description: "Each dog-walking job can be seen as an item that Alice may choose at most once. A job comes with two pieces of information: a 7-day requirement pattern and a payment value. The pattern is a length-7 binary vector indicating on which days of the week the dog must be walked."
date: "2026-06-28T03:12:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105006
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-01-24 Div. 1 (Advanced)"
rating: 0
weight: 105006
solve_time_s: 36
verified: true
draft: false
---

[CF 105006F - Walk in the Park](https://codeforces.com/problemset/problem/105006/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

Each dog-walking job can be seen as an item that Alice may choose at most once. A job comes with two pieces of information: a 7-day requirement pattern and a payment value. The pattern is a length-7 binary vector indicating on which days of the week the dog must be walked. If Alice accepts a job, she commits to walking that dog on every day marked 1 in its pattern, and each such commitment consumes one of her daily capacities.

The weekly schedule is fixed: on each of the 7 days, Alice can walk at most 2 dogs, so each day has capacity 2. The constraint is global across all selected jobs, since a job may consume capacity on multiple days simultaneously.

The task is to select a subset of jobs maximizing total payment while ensuring that on every day, the number of chosen jobs requiring that day does not exceed 2.

The input size is small in terms of N, at most 100 jobs, but the constraint coupling across 7 days is strong. This immediately suggests that brute force over subsets of jobs is conceptually possible since there are at most $2^{100}$ subsets, but clearly infeasible. However, the real structure is that each job interacts only with 7 shared resources, meaning the state space is fundamentally governed by the per-day loads rather than by N itself.

A naive greedy approach fails because choosing a high-paying job early can block multiple smaller jobs that together exceed its value. For example, a job that requires all 7 days with reward 100 might look optimal locally, but two jobs requiring disjoint subsets of days could yield 200 total while still respecting the per-day capacity constraints.

Another subtle failure case occurs when multiple jobs overlap heavily on one day. Selecting too many moderate-value jobs that all include a single busy day can violate feasibility only at the very end, making greedy selection hard to correct retroactively.

## Approaches

A direct brute-force method enumerates every subset of jobs, checks feasibility by simulating the weekly capacity usage, and computes total profit. Feasibility checking costs $O(7N)$ per subset since we count how many selected jobs require each day. With $2^N$ subsets, this becomes $O(2^N \cdot N)$, which is astronomically large for $N = 100$.

The key observation is that the only shared resource constraints are the 7 days of the week, each with capacity 2. This means the system state is fully described by how many slots are used on each of the 7 days, i.e. a 7-dimensional vector where each entry is in $\{0,1,2\}$. The total number of such states is $3^7 = 2187$, which is small enough for dynamic programming.

Each job transitions the system by adding a fixed binary vector to the current state, provided no coordinate exceeds 2. This transforms the problem into a classic knapsack-style DP over a small multidimensional capacity space, where items are jobs and dimensions are days of the week.

We therefore perform DP over all feasible load configurations, updating states by considering whether to take each job or skip it. The compression from 100 jobs into a state space of size 2187 is what makes the solution efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N \cdot N)$ | $O(7)$ | Too slow |
| Optimal DP over day-load states | $O(N \cdot 3^7)$ | $O(3^7)$ | Accepted |

## Algorithm Walkthrough

We represent each DP state as a 7-tuple of integers, where each entry records how many dogs are already assigned to that day. Each entry ranges from 0 to 2.

1. Initialize a dictionary or array `dp` where the key is the 7-day state and the value is the maximum profit achievable. Start with the all-zero state having value 0. This represents choosing no jobs.
2. Process jobs one by one. For each job, extract its 7-day requirement vector and its payment.
3. For each existing DP state, consider two possibilities: skip the job, which keeps the state unchanged, or take the job, which adds its requirement vector to the state.
4. When attempting to take a job, verify feasibility by ensuring that for every day, the resulting count does not exceed 2. This ensures we respect Alice’s capacity constraint.
5. If the resulting state is valid, update the DP table entry for that state with the maximum of its current value and the previous state value plus the job’s payment.
6. After processing all jobs, the answer is the maximum value across all DP states.

The crucial idea is that DP never needs to remember which jobs were chosen, only the induced load configuration. This is valid because all future constraints depend solely on current load, not on job identity.

### Why it works

At any point, every DP state encodes exactly the set of achievable load configurations after processing a prefix of jobs, along with the best profit obtainable for each configuration. When processing a new job, transitions consider all ways of extending previously valid configurations by either excluding or including the job. Since feasibility depends only on cumulative day loads and these are fully represented in the state, no information needed for future decisions is lost. Therefore, the DP invariant holds: after processing i jobs, all reachable valid states with their optimal profits are correctly recorded.

## Python Solution

```python
import sys
input = sys.stdin.readline

def encode(state):
    # base-3 encoding of 7 digits
    res = 0
    for x in state:
        res = res * 3 + x
    return res

def decode(x):
    state = [0] * 7
    for i in range(6, -1, -1):
        state[i] = x % 3
        x //= 3
    return state

def add_state(state, req):
    new_state = state[:]
    for i in range(7):
        new_state[i] += req[i]
        if new_state[i] > 2:
            return None
    return new_state

def solve():
    n = int(input())
    jobs = []
    for _ in range(n):
        *days, val = map(int, input().split())
        jobs.append((days, val))

    dp = {encode([0]*7): 0}

    for days, val in jobs:
        cur_items = list(dp.items())
        for mask, profit in cur_items:
            state = decode(mask)

            new_state = add_state(state, days)
            if new_state is not None:
                new_mask = encode(new_state)
                if new_mask not in dp or dp[new_mask] < profit + val:
                    dp[new_mask] = profit + val

    print(max(dp.values()))

if __name__ == "__main__":
    solve()
```

The DP table is stored as a dictionary keyed by a base-3 encoding of the 7-day load vector. This avoids repeatedly copying 7-element lists in inner loops while still keeping the state compact.

Each job is processed by iterating over a snapshot of current states. This is essential because updates for the current job must not immediately influence other transitions of the same job, which would otherwise overcount selections.

The base-3 encoding ensures fast hashing and comparison of states, and decoding is only done when we need to apply transitions. Since the state space is small, this overhead is negligible.

## Worked Examples

### Example 1

Input:

```
2
1 0 0 0 0 0 0 10
1 0 0 0 0 0 0 20
```

Only day 1 is used, capacity is 2.

| Step | State (day1) | Action | Profit |
| --- | --- | --- | --- |
| Start | 0 | none | 0 |
| Job 1 | 1 | take | 10 |
| Job 2 | 2 | take | 30 |

The DP shows both jobs can be taken because capacity is 2, giving total 30.

### Example 2

Input:

```
3
1 1 1 0 0 0 0 0 50
1 1 1 0 0 0 0 0 60
1 1 1 0 0 0 0 0 40
```

All jobs use the same two days, capacity per day is 2.

| Step | State (d1,d2) | Action | Profit |
| --- | --- | --- | --- |
| Start | (0,0) | none | 0 |
| Job 1 | (1,1) | take | 50 |
| Job 2 | (2,2) | take | 110 |
| Job 3 | skipped | invalid (would exceed 2) | 110 |

This confirms that DP correctly enforces shared capacity across jobs.

## Complexity Analysis

| Measure | Co
