---
title: "CF 339B - Xenia and Ringroad"
description: "We have a circular city with n houses arranged clockwise along a ringroad. Each house has a unique number from 1 to n, and traffic flows only clockwise. Xenia starts at house 1 and has m tasks to complete in a specific order, each task located at a house number a[i]."
date: "2026-06-06T17:08:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 339
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 197 (Div. 2)"
rating: 1000
weight: 339
solve_time_s: 115
verified: false
draft: false
---

[CF 339B - Xenia and Ringroad](https://codeforces.com/problemset/problem/339/B)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We have a circular city with `n` houses arranged clockwise along a ringroad. Each house has a unique number from 1 to `n`, and traffic flows only clockwise. Xenia starts at house 1 and has `m` tasks to complete in a specific order, each task located at a house number `a[i]`. The time it takes to move from one house to its immediate clockwise neighbor is 1 unit. The goal is to compute the total time Xenia will spend traveling to complete all tasks in the given order.

The input consists of two integers `n` and `m`, followed by `m` integers representing the sequence of houses Xenia must visit. The output is a single integer, the total time to finish all tasks.

Given the constraints (`2 ≤ n ≤ 10^5` and `1 ≤ m ≤ 10^5`) and a 2-second time limit, any algorithm must run in roughly linear time. Nested loops or quadratic approaches, which would perform up to `10^10` operations in the worst case, are too slow. Each move can be computed in constant time, so we can aim for an `O(m)` solution.

Non-obvious edge cases include scenarios where the next task is at a house with a smaller number than the current one. For instance, if Xenia is at house 3 in a ring of 4 houses and the next task is at house 2, she must traverse houses 4 and then 1 before reaching 2. A naive approach that only subtracts indices would incorrectly give a negative travel time. Another edge case is consecutive tasks in the same house, which should take zero additional time. For example, in `n = 5`, tasks `[3, 3, 2]`, the time to reach the second task at 3 is zero, then she moves from 3 to 2 along the ring, taking 4 units, not 2.

## Approaches

The brute-force approach would simulate Xenia moving from house to house step by step along the ringroad. For each task, we would increment a counter for each house traversed. While this is conceptually correct, the worst-case scenario occurs when Xenia has to traverse almost the entire ring for each task, leading to `O(m * n)` operations, which is around `10^10` for maximum constraints and far too slow.

The key observation is that moving along a one-way circular road allows us to compute the travel time between two houses using simple arithmetic rather than simulating each step. If Xenia is at house `current` and needs to reach `next`, the distance along the ring is `next - current` if `next >= current`, or `n - (current - next)` if `next < current`. This accounts for wrapping around the ring. This transforms the simulation into a single linear pass over the task list, computing distances in constant time per task.

By summing these distances, we can calculate the total time in `O(m)` with no extra space apart from variables tracking the current house and the total time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate step by step) | O(m * n) | O(1) | Too slow |
| Optimal (compute distances arithmetically) | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `current` to 1, representing Xenia’s starting house, and `total_time` to 0. We track `current` because the next task depends on the house Xenia is currently at.
2. Iterate over each task `task` in the given sequence. For each `task`, determine the time to move from `current` to `task`. If `task >= current`, the distance is `task - current`. Otherwise, she must wrap around the ring, so the distance is `n - (current - task)`. Add this distance to `total_time`.
3. Update `current` to `task` to reflect Xenia’s new location.
4. After processing all tasks, print `total_time`.

Why it works: the invariant maintained is that `current` always accurately reflects Xenia’s current house before moving to the next task. The distance calculation correctly handles the circular nature of the road by differentiating the cases where the next task is ahead or behind in terms of house numbering. Summing these distances in order guarantees that all travel time is accounted for exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
tasks = list(map(int, input().split()))

current = 1
total_time = 0

for task in tasks:
    if task >= current:
        total_time += task - current
    else:
        total_time += n - (current - task)
    current = task

print(total_time)
```

The first line reads the city size and number of tasks. The second line reads the sequence of tasks. We initialize `current` to 1, the starting house, and `total_time` to 0. The loop iterates over tasks and calculates the distance depending on whether the task house number is ahead or requires wrapping around. Updating `current` ensures the next iteration uses the correct starting point. This approach avoids off-by-one errors since house numbers start at 1.

## Worked Examples

**Sample 1**

Input:

```
4 3
3 2 3
```

| Task | Current | Distance | Total_time |
| --- | --- | --- | --- |
| 3 | 1 | 2 | 2 |
| 2 | 3 | 3 | 5 |
| 3 | 2 | 1 | 6 |

Xenia moves 1→2→3 (2 units), wraps around 3→4→1→2 (3 units), then 2→3 (1 unit). The total time is 6.

**Sample 2**

Input:

```
5 4
2 2 4 1
```

| Task | Current | Distance | Total_time |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 1 |
| 2 | 2 | 0 | 1 |
| 4 | 2 | 2 | 3 |
| 1 | 4 | 2 | 5 |

This demonstrates consecutive tasks in the same house take zero time and wrap-around logic from 4→1 is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each task is processed once with constant-time arithmetic. |
| Space | O(m) | We store the task list; no additional structures needed. |

This fits comfortably within the constraints: `m` and `n` up to 10^5, and each arithmetic operation is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    tasks = list(map(int, input().split()))
    current = 1
    total_time = 0
    for task in tasks:
        if task >= current:
            total_time += task - current
        else:
            total_time += n - (current - task)
        current = task
    return str(total_time)

# provided sample
assert run("4 3\n3 2 3\n") == "6", "sample 1"

# custom tests
assert run("5 4\n2 2 4 1\n") == "5", "consecutive tasks & wrap"
assert run("2 5\n1 2 1 2 1\n") == "5", "small n, alternating"
assert run("10 1\n10\n") == "9", "single task at last house"
assert run("3 3\n3 3 3\n") == "2", "all tasks same house"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 4\n2 2 4 1 | 5 | Consecutive tasks and wrap-around logic |
| 2 5\n1 2 1 2 1 | 5 | Small ring, alternating tasks, full traversal |
| 10 1\n10 | 9 | Single task at last house |
| 3 3\n3 3 3 | 2 | Repeated tasks in same house, zero distance for repeats |

## Edge Cases

For tasks in decreasing order across the ring, the algorithm correctly wraps. Input `n=4, tasks=[4,1,2]` results in `3+1+1=5` units: 1→2→3→4 (3 units), wrap 4→1 (1 unit), 1→2 (1 unit). For repeated tasks in the same house, distance is zero, e.g., `n=5, tasks=[2,2]` yields `1` unit. In both cases, the arithmetic distance calculation ensures correct travel time without simulating each house step-by-step.
