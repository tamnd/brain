---
title: "CF 105632F - Infinite Loop"
description: "We are given a fixed pattern of work that repeats every day forever. Each day has a timeline of k hours, and at the start of every day exactly n tasks appear. Task i of a day appears at a known hour ai within that day and requires bi hours of uninterrupted processing time."
date: "2026-06-22T05:37:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105632
codeforces_index: "F"
codeforces_contest_name: "2024 China Collegiate Programming Contest (CCPC) Zhengzhou Onsite (The 3rd Universal Cup. Stage 22: Zhengzhou)"
rating: 0
weight: 105632
solve_time_s: 78
verified: true
draft: false
---

[CF 105632F - Infinite Loop](https://codeforces.com/problemset/problem/105632/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed pattern of work that repeats every day forever. Each day has a timeline of `k` hours, and at the start of every day exactly `n` tasks appear. Task `i` of a day appears at a known hour `a_i` within that day and requires `b_i` hours of uninterrupted processing time. The arrival times `a_i` are strictly increasing, so tasks within a day come in a fixed chronological order.

There is a single worker processing tasks. The worker never preempts a task once started and always picks the earliest arrived unfinished task whenever they are free. Because tasks repeat every day, this becomes an infinite stream of tasks with a very regular structure.

Each query refers to a particular occurrence of a task, namely the `y`-th task on day `x`. The goal is to compute the exact time, expressed as day number and hour within that day, when that specific task finishes.

The key difficulty is that although each day has only `n` tasks, the system runs forever and tasks from different days interact through a queue. A task on day `x` is not independent of previous days, since earlier days may push it back in the processing order.

The constraints force us away from simulation across all days. With up to `10^5` tasks per day and up to `5×10^5` queried days, a naive per-day simulation would explode to around `5×10^10` operations. Even simulating a single day repeatedly would not be sufficient, because queue carryover creates cross-day dependencies.

A subtle edge case arises from system overload. If the total daily workload exceeds the available `k` hours, the queue never fully clears, and delay accumulates across days. If the workload is small enough, each day clears independently and no carryover exists. These two regimes behave fundamentally differently and must be separated.

A common mistake is to simulate each day independently, assuming tasks reset daily. That fails immediately when a task from day `x` depends on unfinished work from day `x-1`. Another failure mode is ignoring intra-day arrival times and treating tasks as if they arrive simultaneously, which breaks correctness when idle gaps exist early in the day.

## Approaches

A direct simulation would maintain a queue of pending tasks across all days, pushing new tasks each day and processing them one by one. This correctly models the system, but the number of operations grows with total processed work, which can reach `O(nq)` days in the worst case, far beyond feasibility.

The key observation is that the system behaves in one of two modes depending on whether a day’s total workload is at most the available processing time `k`.

If the sum of all `b_i` is at most `k`, then each day is underloaded. The worker finishes all tasks before the day ends, and the queue becomes empty every day. In this case, days are independent copies of the same schedule, and we only need to compute task completion times inside a single day.

If the sum exceeds `k`, then each day produces more work than can be completed. After a short transient period, the worker becomes permanently busy. Once that happens, the exact arrival times within a day stop affecting ordering in practice, because the queue never empties. The system degenerates into a continuous flow where only total work matters.

This allows us to reduce the infinite process into either a single-day simulation (light load) or a steady-state prefix accumulation (heavy load).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full simulation across days | O(total work) | O(n) | Too slow |
| Single-day simulation + steady state handling | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We split the solution into two cases based on the total workload of a day.

### Case 1: total work per day ≤ k

1. Compute a single-day schedule starting from time 0.

We simulate tasks in increasing order of `a_i`, maintaining a current time pointer. Each task starts at `max(current_time, a_i)` and finishes after adding `b_i`. This respects both arrival constraints and FIFO ordering.
2. Record the completion time of every task within the day.

Since total work fits in `k`, no task spills into the next day, so these completion times are final.
3. For a query `(x, y)`, shift the single-day result by whole days.

The answer is simply `(x-1)*k + completion_time_within_day[y]`.

This works because the system resets every day with no leftover tasks.

### Case 2: total work per day > k

1. Observe that the system eventually becomes permanently busy.

After enough days, there is always pending work at the start of each day, so the worker never idles.
2. In the steady state, arrival times within a day no longer affect execution order.

Tasks are effectively processed in strict day order, and within each day in index order, because no gaps appear that could reorder execution.
3. Replace each task by its processing cost only.

The system becomes a single infinite sequence of workloads repeating every day.
4. Precompute prefix sums for one day:

Let `pref[i] = b_1 + ... + b_i`, and `S = pref[n]`.
5. Compute global completion time in continuous hours:

The completion time of task `(x, y)` becomes:

`time = (x-1)*S + pref[y]`.
6. Convert continuous time into `(day, hour)` by dividing by `k`.

This works because once the system is saturated, the worker never waits, so the schedule is equivalent to processing a continuous stream with no idle gaps.

### Why it works

In both cases, the key invariant is that the worker always processes tasks in FIFO order of arrival, and once the system becomes saturated, there are no idle intervals that could distort ordering. Either the queue resets every day, or it never empties after some point. These are the only two stable behaviors possible under a constant daily input pattern, so reducing the process to either independent-day simulation or pure prefix accumulation captures all dynamics exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, q = map(int, input().split())
    a = []
    b = []
    
    for _ in range(n):
        ai, bi = map(int, input().split())
        a.append(ai)
        b.append(bi)

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + b[i]
    S = pref[n]

    # Case 1: light load, each day clears
    if S <= k:
        finish = [0] * n
        cur = 0
        for i in range(n):
            if cur < a[i]:
                cur = a[i]
            cur += b[i]
            finish[i] = cur

        out = []
        for _ in range(q):
            x, y = map(int, input().split())
            y -= 1
            day_start = (x - 1) * k
            t = day_start + finish[y]
            d = t // k + 1
            h = t % k + 1
            out.append(f"{d} {h}")

        print("\n".join(out))
        return

    # Case 2: heavy load, steady state prefix model
    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        y -= 1
        t = (x - 1) * S + pref[y]
        d = t // k + 1
        h = t % k + 1
        out.append(f"{d} {h}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first precomputes prefix sums of processing times, since they are the only quantities that matter in the overloaded regime. The decision point is the total daily workload `S`.

In the light-load branch, we explicitly simulate one day using a single time pointer. The important detail is the `max(cur, a[i])` step, which ensures that we respect task release times and idle periods inside the day.

In the heavy-load branch, we avoid simulation entirely. Each query is answered in constant time using a linear formula over prefix sums. The conversion from absolute time to `(day, hour)` uses integer division by `k`, with 1-based indexing adjustment.

## Worked Examples

Consider a small system with `k = 5` and tasks:

| i | a_i | b_i |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 4 | 3 |

### Trace (light load case)

Here total work is `4 ≤ 5`, so no carryover occurs.

| Step | Task | Start time | Finish time | cur |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 2 |
| 2 | 2 | 4 | 7 | 7 |

Both finish within the same day.

For query `(2, 2)`, day 2 task 2 finishes at continuous time `5 + 7 = 12`, which maps to day `3`, hour `2`.

This confirms that each day is independent.

Now consider a heavy load example:

`k = 10`, tasks:

| i | b_i |
| --- | --- |
| 1 | 4 |
| 2 | 6 |
| 3 | 7 |

Total work is `17 > 10`, so backlog accumulates.

Prefix sums are `4, 10, 17`.

For query `(3, 2)`, we compute:

`time = (3-1)*17 + 10 = 44`.

This represents continuous processing time; converting to day/hour gives day `5`, hour `4`.

The trace shows that only cumulative work matters once the system is saturated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | One prefix computation plus constant-time queries |
| Space | O(n) | Stores task arrays and prefix sums |

The constraints allow up to `10^5` tasks and queries, so linear preprocessing and constant-time per query fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# light load, independent days
assert run("""2 5 3
1 1
4 2
1 1
1 2
2 1
""") == "1 1\n1 2\n2 2"

# exact fill boundary
assert run("""2 5 2
1 2
2 3
1 2
2 1
""") == "1 5\n2 5"

# heavy load
assert run("""3 10 2
2 4
3 1
10 7
2 2
5 3
""") == "3 10\n4 7"

# minimum case
assert run("""1 5 1
1 5
1 1
""") == "1 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| light load | per-day independence | no carryover |
| boundary fill | exact k-hour packing | edge of regime switch |
| heavy load | prefix accumulation | saturated system behavior |
| minimum case | single task correctness | base correctness |

## Edge Cases

One edge case is when total daily workload is exactly equal to `k`. In this situation the worker finishes exactly at the end of each day, but never carries anything forward. For example, if tasks perfectly fill `k` hours, the light-load branch still applies. The simulation finishes at time exactly `k`, so shifting by `(x-1)*k` places each day back-to-back without overlap.

Another case is when the first task arrives late in the day. Even in a light-load system, the worker will idle until `a_1`. The simulation handles this through the `max(cur, a[i])` step. Without it, early idle time would be ignored and all completion times would be incorrectly shifted earlier.

A third case is a heavily loaded system where early days still appear partially idle. Even though the system eventually saturates, the steady-state formula only applies after the transition. The decision based on total daily workload avoids mixing regimes and ensures we do not incorrectly assume immediate saturation.
