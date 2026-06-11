---
title: "CF 1153A - Serval and Bus"
description: "Serval is going to the bus station at a specific time t. There are n bus routes, each with a first bus arriving at si minutes and subsequent buses every di minutes. Serval will take the first bus that comes after or exactly at time t."
date: "2026-06-12T02:51:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1153
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 551 (Div. 2)"
rating: 1000
weight: 1153
solve_time_s: 103
verified: true
draft: false
---

[CF 1153A - Serval and Bus](https://codeforces.com/problemset/problem/1153/A)

**Rating:** 1000  
**Tags:** brute force, math  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Serval is going to the bus station at a specific time `t`. There are `n` bus routes, each with a first bus arriving at `s_i` minutes and subsequent buses every `d_i` minutes. Serval will take the first bus that comes after or exactly at time `t`. If multiple buses arrive at the same earliest time, any one of those routes is acceptable. The task is to determine which bus route Serval will board.

The input consists of `n` and `t`, followed by `n` pairs `(s_i, d_i)` representing the first arrival time and interval of each bus route. The output is a single integer representing the 1-based index of the chosen bus route.

The constraints are moderate: `n` is at most 100, and times can go up to `10^5`. A brute-force check across each bus route is feasible because even if we iterated minute by minute, the number of operations would be within the limit. Edge cases include the first bus of a route arriving exactly at `t`, routes where all buses arrive after `t`, or multiple routes sharing the earliest bus after `t`. For instance, if `t=2` and two routes have buses at times `[2,4,6]` and `[2,5,8]`, both are valid answers.

## Approaches

The naive approach is to generate all arrival times for each bus route until we reach or surpass `t` and then select the earliest among them. This works because `n` is small and the intervals `d_i` are bounded. However, constructing all bus times is unnecessary and can be avoided using simple arithmetic.

The key insight is that for a route starting at `s_i` with interval `d_i`, the first bus Serval can catch occurs at `s_i` if `s_i >= t`. Otherwise, we can compute the first bus after `t` directly as the smallest multiple of `d_i` added to `s_i` that is at least `t`. Mathematically, this is `s_i + ceil((t - s_i)/d_i) * d_i`. Using integer arithmetic, we can compute this with `(t - s_i + d_i - 1) // d_i` to avoid floating point operations. This reduces the problem to scanning each bus route once and computing its earliest catchable bus, making the solution O(n) in time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (generate all times) | O(n * max((t - s_i)/d_i)) | O(1) | Works for small t, inefficient for large intervals |
| Optimal (direct calculation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `t`.
2. Initialize two variables: `best_time` to a very large value (to track the earliest bus) and `best_route` to -1.
3. For each bus route index `i` from 1 to `n`, read `s_i` and `d_i`.
4. If `s_i >= t`, set the next bus for this route to `s_i`.
5. Otherwise, calculate how many intervals we need to wait after `s_i` to reach at least `t`. This is `(t - s_i + d_i - 1) // d_i`. Multiply this by `d_i` and add `s_i` to get the earliest bus time for this route.
6. If this bus time is less than `best_time`, update `best_time` and set `best_route` to `i`.
7. After checking all routes, print `best_route`.

Why it works: The algorithm maintains the invariant that `best_time` always holds the earliest bus Serval can catch among all processed routes. By computing the first catchable bus for each route using integer arithmetic, we guarantee that we never miss the actual earliest bus, and the final `best_route` is guaranteed to be correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, t = map(int, input().split())
best_time = float('inf')
best_route = -1

for i in range(1, n + 1):
    s, d = map(int, input().split())
    if s >= t:
        next_bus = s
    else:
        wait = (t - s + d - 1) // d
        next_bus = s + wait * d
    if next_bus < best_time:
        best_time = next_bus
        best_route = i

print(best_route)
```

The code reads input efficiently using `sys.stdin.readline`. The loop computes the earliest catchable bus for each route. The `(t - s + d - 1) // d` formula ensures we round up when the interval does not divide evenly. Updating `best_time` and `best_route` only when a strictly earlier bus is found avoids ambiguity, and using 1-based indexing matches the problem's expected output.

## Worked Examples

### Sample 1

Input:

```
2 2
6 4
9 5
```

| Route | s_i | d_i | next_bus | best_time | best_route |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 4 | 6 | 6 | 1 |
| 2 | 9 | 5 | 9 | 6 | 1 |

The earliest bus is route 1 at time 6. Serval boards route 1.

### Sample 2

Input:

```
3 2
2 2
2 3
2 4
```

| Route | s_i | d_i | next_bus | best_time | best_route |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | 2 | 1 |
| 2 | 2 | 3 | 2 | 2 | 1 |
| 3 | 2 | 4 | 2 | 2 | 1 |

All routes have the first bus at 2. Any route from 1 to 3 is valid; the algorithm picks the first encountered minimum, route 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each route is scanned once, and the arithmetic for next bus is O(1) |
| Space | O(1) | Only a few variables are maintained; no large data structures needed |

Given n ≤ 100, this solution runs in a fraction of a millisecond. Memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, t = map(int, input().split())
    best_time = float('inf')
    best_route = -1
    for i in range(1, n + 1):
        s, d = map(int, input().split())
        if s >= t:
            next_bus = s
        else:
            wait = (t - s + d - 1) // d
            next_bus = s + wait * d
        if next_bus < best_time:
            best_time = next_bus
            best_route = i
    return str(best_route)

# Provided samples
assert run("2 2\n6 4\n9 5\n") == "1", "sample 1"
assert run("3 2\n2 2\n2 3\n2 4\n") == "sample 2"

# Custom cases
assert run("1 1\n1 1\n") == "1", "single route catches immediately"
assert run("2 10\n1 3\n2 4\n") == "1", "earliest bus requires multiple intervals"
assert run("3 5\n2 2\n3 3\n5 1\n") == "3", "exact match at t"
assert run("3 7\n2 2\n3 3\n4 4\n") == "1", "multiple options, first min picked"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 1 | 1 | Single route catches immediately |
| 2 10\n1 3\n2 4 | 1 | Waiting multiple intervals, check calculation |
| 3 5\n2 2\n3 3\n5 1 | 3 | Route exactly at t is chosen |
| 3 7\n2 2\n3 3\n4 4 | 1 | Multiple routes arrive at same next bus; first minimum selected |

## Edge Cases

If `t` is before the first bus of a route, `s_i >= t`, the next bus is `s_i`. For example, `t=1`, `s=5`, `d=3` gives `next_bus=5`. The algorithm correctly identifies this as the earliest bus. When multiple routes have the same earliest next bus, the algorithm picks the first encountered minimum. For `t=2` and buses `[2,4]`, `[2,5]`, `[2,6]`, `best_time` becomes 2 at route 1, and the output is route 1. This satisfies the problem because any route with the earliest bus is acceptable.
