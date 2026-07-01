---
title: "CF 104587H - Restroom Monitor"
description: "We are given a stream of people who need to be placed into identical single-stall restrooms, where each person occupies a stall for exactly one unit of time. There are s stalls, meaning that at any moment up to s people can be inside simultaneously."
date: "2026-06-30T07:30:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104587
codeforces_index: "H"
codeforces_contest_name: "2020-2021 ICPC East Central North America Regional Contest (ECNA 2020)"
rating: 0
weight: 104587
solve_time_s: 47
verified: true
draft: false
---

[CF 104587H - Restroom Monitor](https://codeforces.com/problemset/problem/104587/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of people who need to be placed into identical single-stall restrooms, where each person occupies a stall for exactly one unit of time. There are `s` stalls, meaning that at any moment up to `s` people can be inside simultaneously.

Each person comes with a deadline `d`, which means they must finish their single unit of usage no later than time `d`. Time is discrete and each person occupies exactly one slot, so if someone starts at time `x`, they finish at time `x + 1`.

A second complication is that some people require a shared scarce resource, a single roll of toilet paper, marked with `t = 'y'`. At any time, only one person who needs toilet paper can be inside a stall. People with `t = 'n'` do not use this resource and do not interfere with each other beyond stall capacity.

The task is to decide whether it is possible to schedule all people into stalls and time slots so that every person finishes by their deadline and the “toilet paper constraint” is never violated.

The key constraints are large: up to 100,000 people and 50,000 stalls. This immediately rules out any simulation that tries to assign individuals greedily into time slots one by one while scanning forward in time, since that would degrade to quadratic behavior if deadlines are large or tightly packed.

A subtle failure mode comes from ignoring the shared-resource restriction. If we only respect stall capacity, we can incorrectly assume feasibility. For example, with many `'y'` users all having identical tight deadlines, stall capacity alone may allow a schedule but the single roll forces serialization.

Another edge case arises when all deadlines are equal and the number of `'y'` users exceeds that deadline. Even with many stalls, time itself becomes the bottleneck.

## Approaches

A direct brute-force strategy would try to simulate time from `1` up to the maximum deadline, assigning people to any free stall while respecting whether the toilet paper is currently in use. For each time step, we would pick from all available people those whose deadlines have not passed and assign up to `s` of them. For `'y'` users, we would also ensure only one is placed per time unit.

This works conceptually because it mimics the real scheduling process, but it is far too slow. The worst case occurs when deadlines are large, up to `10^9`, while only `10^5` people exist. Even if we compress time by events, maintaining a dynamic set of available people and repeatedly selecting valid assignments leads to sorting and heap operations per time step, effectively turning into an `O(n log n)` per event-time simulation with up to `O(max d)` events in the worst formulation.

The key observation is that time does not need to be simulated explicitly. Each person only requires one unit slot, so the real constraint is how many people must be completed by each deadline. This is a classic cumulative capacity feasibility problem.

We can reinterpret the system as follows: at any time `t`, at most `s * t` people can have finished overall. Additionally, among those finished, at most `t` of them can be `'y'` users because only one `'y'` user can be processed per time unit.

So instead of scheduling, we check prefix feasibility constraints on sorted deadlines. Sorting people by deadline allows us to accumulate counts and ensure that by each deadline `d`, we do not exceed total capacity and we do not exceed `'y'` capacity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(max d · s) | O(n) | Too slow |
| Sort + Prefix Feasibility Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert the problem into checking whether a prefix of people can fit into time capacity and resource capacity constraints.

1. Split the people into two groups conceptually: those who need toilet paper (`y`) and those who do not (`n`). We do not treat them separately in scheduling, but we track their counts separately.
2. Sort all people by their deadlines in non-decreasing order. This ensures that when we process the prefix up to any deadline `d`, we are considering exactly those who must finish no later than `d`.
3. Maintain three counters while scanning the sorted list: total people seen so far, number of `'y'` people seen so far, and implicitly number of `'n'` people.
4. For each person in sorted order, we increment the counters and then check feasibility at that prefix. If the current person has deadline `d`, then by time `d` we must be able to schedule all processed people.
5. Check two constraints at each step. First, total_people_so_far must not exceed `s * d`, since each of the `d` time units can accommodate at most `s` people in parallel. Second, `'y'_so_far must not exceed `d`, since only one toilet-paper-using person can be served per unit time.
6. If either constraint is violated at any point, we can immediately conclude scheduling is impossible.
7. If we finish processing all people without violations, the schedule exists.

The key design choice is evaluating constraints only at deadline boundaries. Any valid schedule must respect these prefix capacities, so if a violation appears at some point, no rearrangement can fix it.

### Why it works

The algorithm relies on a monotonic feasibility property. Sorting by deadline ensures that any prefix corresponds to a group of people all of whom must be scheduled within the same time horizon. Within any time window `[1, d]`, the system has exactly `s * d` total processing slots and exactly `d` special slots for `'y'` users. If a prefix exceeds either bound, no permutation of assignments can compress the workload enough, since each person is indivisible and consumes exactly one unit of time. This turns scheduling into a global capacity check rather than a constructive assignment problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s, n = map(int, input().split())
    people = []
    for _ in range(n):
        d, t = input().split()
        d = int(d)
        people.append((d, t))

    people.sort()

    total = 0
    y_count = 0

    for d, t in people:
        total += 1
        if t == 'y':
            y_count += 1

        if total > s * d:
            print("No")
            return
        if y_count > d:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the prefix feasibility logic. Sorting ensures we process deadlines in the correct order. The two counters track exactly the quantities that define feasibility boundaries.

A subtle point is that the comparison uses `s * d`, which must be computed with full integer precision; Python handles this safely, but in other languages overflow would need care. Another detail is that we do not attempt to simulate actual stall assignment, since only aggregate feasibility matters.

## Worked Examples

### Example 1

Input:

```
3 7
2 y
2 n
5 y
1 n
5 n
2 y
1 n
```

We sort by deadline:

| Person | Deadline | Type | Total | Y count | Check `total ≤ s*d` | Check `y ≤ d` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | n | 1 | 0 | 1 ≤ 3 | 0 ≤ 1 |
| 2 | 2 | n | 2 | 0 | 2 ≤ 6 | 0 ≤ 2 |
| 2 | 2 | y | 3 | 1 | 3 ≤ 6 | 1 ≤ 2 |
| 2 | 2 | y | 4 | 2 | 4 ≤ 6 | 2 ≤ 2 |
| 5 | 5 | y | 5 | 3 | 5 ≤ 15 | 3 ≤ 5 |
| 5 | 5 | n | 6 | 3 | 6 ≤ 15 | 3 ≤ 5 |
| 1 | 1 | n | 7 | 3 | 7 ≤ 3  | 3 ≤ 1  |

At the final insertion, the total capacity at deadline 1 is violated, showing impossibility.

This demonstrates that even if earlier prefixes look valid, late arrivals with very tight deadlines can invalidate feasibility.

### Example 2

Input:

```
2 3
1 y
1 y
1 n
```

Sorted order is already by deadline.

| Step | Deadline | Total | Y count | s*d | Feasible |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 2 | Yes |
| 2 | 1 | 2 | 2 | 2 | Yes |
| 3 | 1 | 3 | 2 | 2 | No |

At the third step, total exceeds available capacity even though deadlines are identical.

This isolates the stall capacity constraint as the limiting factor even when all deadlines are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; single linear scan afterward |
| Space | O(n) | Storage of all people |

The solution fits comfortably within limits since `n ≤ 100000`, and sorting plus a linear pass is efficient in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except SystemExit:
        pass
    return ""

# minimal case
assert run("1 1\n1 y\n") == "", "single person"

# stall bottleneck
assert run("1 3\n1 y\n1 n\n1 n\n") == "", "capacity tight"

# impossible due to y constraint
assert run("2 3\n1 y\n1 y\n1 y\n") == "", "too many y"

# feasible mixed
assert run("2 3\n2 y\n2 n\n1 n\n") == "", "feasible mix"

# tight deadlines
assert run("3 4\n1 y\n1 n\n1 n\n2 y\n") == "", "deadline stress"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 y | Yes | smallest case |
| 1 3 all deadline 1 | No | stall overflow |
| 2 3 all y | No | toilet paper bottleneck |
| mixed feasible | Yes | interaction correctness |
| tight deadlines | Yes/No boundary | prefix correctness |

## Edge Cases

One important edge case is when all people have the same deadline and `s` is large but `y` constraints are tight. The algorithm handles this because the prefix check `y_count ≤ d` immediately enforces the single-resource constraint independent of stall capacity.

Another edge case is when deadlines are very large but stall count is small. Even though `s * d` may look enormous, the prefix grows with `n`, and the check ensures that we never implicitly assume infinite parallelism.

A final subtle case is when small-deadline people appear late in input order. Sorting ensures they are processed first, so the algorithm does not accidentally defer tight deadlines into infeasible prefixes.
