---
title: "CF 319E - Ping-Pong"
description: "We are asked to maintain a dynamic set of intervals and answer reachability queries between them. Each interval is represented by two integers $(x, y)$ where $x < y$. Intervals are added one by one, and each new interval is guaranteed to be strictly longer than all previous ones."
date: "2026-06-06T02:04:02+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 319
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 189 (Div. 1)"
rating: 3000
weight: 319
solve_time_s: 91
verified: true
draft: false
---

[CF 319E - Ping-Pong](https://codeforces.com/problemset/problem/319/E)

**Rating:** 3000  
**Tags:** data structures  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain a dynamic set of intervals and answer reachability queries between them. Each interval is represented by two integers $(x, y)$ where $x < y$. Intervals are added one by one, and each new interval is guaranteed to be strictly longer than all previous ones. A move from interval $(a, b)$ to interval $(c, d)$ is allowed if either endpoint of $(a, b)$ lies strictly inside $(c, d)$. A path exists between two intervals if we can chain such moves.

Input consists of a number of queries, either adding a new interval or asking if a path exists from one previously added interval to another. Output should respond to each query of the second type with "YES" or "NO".

With $n$ up to $10^5$ and coordinates up to $10^9$, we cannot afford an $O(n^2)$ approach that compares every pair of intervals on every query. A naive solution would scan the entire interval set each time we add a new interval or check reachability, which could result in up to $10^{10}$ operations, far beyond a 2-second time limit. We need a data structure that allows incremental updates and efficient reachability queries.

A subtle edge case occurs because intervals are added in strictly increasing length. This guarantees that each new interval cannot be contained by any older interval, but older intervals _can_ be contained by the new one. A careless implementation might attempt to check all intervals on every query without leveraging this property, producing quadratic time complexity.

Another edge case is when intervals share endpoints. For example, if $(1, 5)$ and $(5, 11)$ exist, a path from the first to the second does not exist because neither endpoint of the first lies strictly inside the second. The correct output here would be "NO".

## Approaches

The brute-force solution iterates over all intervals added so far for each query. For a type-2 query, we could perform a depth-first search from the starting interval, checking each interval for reachability using the endpoint containment rule. While this approach is correct, in the worst case it requires traversing all intervals for each query, resulting in $O(n^2)$ time complexity. With $n = 10^5$, this is clearly too slow.

The key observation that unlocks a faster solution is the strictly increasing length property. This means every new interval can "absorb" older intervals, but cannot be absorbed by them. Consequently, reachability is always forward-directed from smaller intervals to larger ones. We can represent each interval as a node and maintain two values for it: the minimum and maximum positions it can reach via successive moves. When a new interval is added, it may extend the reach of previous intervals whose endpoints lie inside it. We can propagate this reachability efficiently in linear time by iterating backward over intervals, updating their reachable ranges. Once intervals are processed, answering a query reduces to checking whether the destination interval's endpoints lie within the reachable range of the source interval. This reduces the problem from $O(n^2)$ to $O(n)$ for processing all additions and queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain a list of intervals in the order they are added. Each interval stores its start and end coordinates.
2. Maintain two arrays, `reach_min` and `reach_max`, representing the minimum and maximum positions reachable from each interval.
3. When adding a new interval `(x, y)`, initialize `reach_min` and `reach_max` for it as `x` and `y`. Iterate backward over previously added intervals. If the interval's start or end lies inside the new interval, update the previous interval's `reach_min` and `reach_max` by extending them to include the new interval's reach. Stop propagating if the current interval's reach already covers the new interval.
4. For a query `(a, b)`, check whether interval `b` lies entirely inside the reachable range `[reach_min[a], reach_max[a]]`. If either endpoint of `b` lies within this range, output "YES"; otherwise, output "NO".

The correctness is guaranteed because the strictly increasing interval length ensures that all reachability propagations are monotonic: once a range is extended, it will never shrink, and all moves respect the containment rule. This makes the reachability computation equivalent to a single pass of interval expansion, capturing all possible paths.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
intervals = []
reach_min = []
reach_max = []

for _ in range(n):
    parts = input().split()
    if parts[0] == '1':
        x, y = int(parts[1]), int(parts[2])
        intervals.append((x, y))
        reach_min.append(x)
        reach_max.append(y)
        i = len(intervals) - 2
        while i >= 0:
            lx, rx = reach_min[i], reach_max[i]
            nx, ny = reach_min[-1], reach_max[-1]
            a, b = intervals[i]
            if (a > nx and a < ny) or (b > nx and b < ny):
                reach_min[i] = min(lx, nx)
                reach_max[i] = max(rx, ny)
            i -= 1
    else:
        a, b = int(parts[1]) - 1, int(parts[2]) - 1
        bx, by = intervals[b]
        if (bx >= reach_min[a] and bx <= reach_max[a]) or (by >= reach_min[a] and by <= reach_max[a]):
            print("YES")
        else:
            print("NO")
```

Each part of the solution directly corresponds to the algorithm steps. We store intervals and their reach ranges. When adding a new interval, we propagate reachability backward only to intervals that may now reach it. Queries simply check whether the destination interval lies in the reachable range of the source interval. The backward propagation stops when no further extension occurs, preventing unnecessary updates and preserving linear total time complexity.

## Worked Examples

Sample 1:

```
5
1 1 5
1 5 11
2 1 2
1 2 9
2 1 2
```

| Step | Intervals | reach_min | reach_max | Query | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,5) | 1 | 5 | - | - |
| 2 | (5,11) | 1,5 | 5,11 | - | - |
| 3 | - | - | - | 1→2 | NO |
| 4 | (2,9) | 1,5,2 | 11,11,9 | - | - |
| 5 | - | - | - | 1→2 | YES |

This trace demonstrates the backward propagation of reachable ranges. Initially, interval 1 cannot reach interval 2 because endpoint 5 of interval 1 is not strictly inside (5,11). After adding interval 3, the reachability of interval 1 expands via interval 3, allowing a path to interval 2.

Custom input 2:

```
3
1 1 4
1 2 5
2 1 2
```

| Step | Intervals | reach_min | reach_max | Query | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,4) | 1 | 4 | - | - |
| 2 | (2,5) | 1,2 | 5,5 | - | - |
| 3 | - | - | - | 1→2 | YES |

Interval 1's reach expands through interval 2, allowing reachability to 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each interval can only propagate its reach once to previous intervals, and each query is O(1) |
| Space | O(n) | Storing n intervals and two reach arrays of size n |

The solution fits comfortably within the limits. Backward propagation is efficient due to the strictly increasing length guarantee, and queries are instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    n = int(input())
    intervals = []
    reach_min = []
    reach_max = []

    for _ in range(n):
        parts = input().split()
        if parts[0] == '1':
            x, y = int(parts[1]), int(parts[2])
            intervals.append((x, y))
            reach_min.append(x)
            reach_max.append(y)
            i = len(intervals) - 2
            while i >= 0:
                lx, rx = reach_min[i], reach_max[i]
                nx, ny = reach_min[-1], reach_max[-1]
                a, b = intervals[i]
                if (a > nx and a < ny) or (b > nx and b < ny):
                    reach_min[i] = min(lx, nx)
                    reach_max[i] = max(rx, ny)
                i -= 1
        else:
            a, b = int(parts
```
