---
title: "CF 105206F - ROAD TO BE LEGEND"
description: "We are given several independent test cases. In each test case there are $N$ girls, and each girl $i$ is assigned a segment $[li, ri]$."
date: "2026-06-27T02:40:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105206
codeforces_index: "F"
codeforces_contest_name: "VitebskOpen Junior"
rating: 0
weight: 105206
solve_time_s: 56
verified: true
draft: false
---

[CF 105206F - ROAD TO BE LEGEND](https://codeforces.com/problemset/problem/105206/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case there are $N$ girls, and each girl $i$ is assigned a segment $[l_i, r_i]$. The task is to decide whether we can assign each girl a distinct integer “shop number” such that girl $i$ receives a shop inside her allowed segment, and no two girls share the same shop.

Although shops are labeled from 1 to $10^9$, only relative ordering matters, since we never actually need to construct all available shops. What matters is whether we can place $N$ points, one per interval, without collisions.

The constraints are large: the total number of intervals across all test cases is up to $2 \cdot 10^5$. This immediately rules out any quadratic reasoning per test case. Any approach that repeatedly scans all remaining intervals or tries all assignments greedily with nested loops will fail. We need something closer to $O(N \log N)$ per test case or amortized linear over all test cases.

A common failure mode here comes from greedy strategies that ignore interval structure.

One incorrect idea is to always assign the smallest possible available shop to each interval in arbitrary order. Consider intervals:

$[1, 100]$, $[1, 1]$, $[2, 2]$.

If we process in input order and assign greedily, we might assign 1 to the first interval, blocking the second, even though a valid assignment exists: assign 1 to $[1,1]$, 2 to $[2,2]$, and 100 to $[1,100]$. The mistake is treating intervals independently without respecting urgency.

Another failure is sorting by left endpoint and greedily assigning increasing positions. That also fails because intervals that start early are not necessarily the most constrained.

The key difficulty is that each interval has a “deadline-like” structure imposed by its right endpoint.

## Approaches

The brute-force approach would attempt to assign shops recursively or via backtracking. At each step, we pick a girl and try every available shop in her interval. In the worst case, this explores exponential configurations, since each assignment reduces availability by one but branching remains large. Even with pruning, the worst case degenerates quickly when intervals heavily overlap.

The structure of the problem suggests a scheduling interpretation: each girl must be assigned a unique integer within a range, which is equivalent to placing unit-length jobs on a number line with constraints. This is closely related to interval scheduling with deadlines.

The key insight is to process intervals in increasing order of their right endpoint. Once we are at a position $x$, we want to assign it to the most constrained interval available at that moment, specifically the interval that ends earliest among those that can still accept $x$. This avoids wasting small endpoints on flexible intervals.

We simulate sweeping possible shop positions from left to right, but we do not iterate all integers. Instead, we maintain a set of active intervals whose left endpoint has been reached, and we always assign the next available position to the interval with the smallest right endpoint. If at some point the smallest right endpoint is smaller than the current position, it means that interval can no longer be satisfied.

This reduces the problem to a classic greedy feasibility check using a min-heap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Backtracking | Exponential | O(N) | Too slow |
| Sort + Min Heap Greedy | $O(N \log N)$ | O(N) | Accepted |

## Algorithm Walkthrough

We interpret each interval as becoming available at $l_i$ and expiring at $r_i$. We simulate assigning increasing shop indices.

1. Sort all intervals by their left endpoint. This allows us to activate intervals exactly when they become eligible to receive a position.
2. Maintain a pointer over the sorted intervals and a min-heap ordered by right endpoints. The heap represents all intervals currently eligible for assignment.
3. Sweep a variable `x` representing the next shop index we are trying to assign. Instead of iterating all integers up to $10^9$, we only move `x` when there is at least one active interval. If there are no active intervals, we jump `x` to the next interval’s left endpoint.
4. Before assigning `x`, insert into the heap all intervals with $l_i \le x$. These are the intervals that can potentially use this position.
5. If the heap is empty after activation, we jump `x` forward again because no interval can use this position. This ensures we only process meaningful positions.
6. Take the interval with the smallest $r_i$ from the heap. This interval is the most urgent because it has the tightest constraint on future assignments.
7. If $r_i < x$, this interval cannot be assigned any valid shop anymore, so the answer is impossible. Otherwise, assign $x$ to it and remove it from the heap.
8. Increment `x` and repeat until all intervals are assigned or a contradiction occurs.

The ordering choice in step 6 is the critical decision: always satisfying the earliest-ending interval prevents blocking later feasibility.

### Why it works

At any point, all active intervals have $l_i \le x$, so they are eligible to receive position $x$ or later. Among them, if we ever choose an interval with a larger right endpoint while ignoring a smaller one, we risk postponing the tighter constraint and losing feasibility later. Any feasible assignment can be transformed so that at each position $x$, the interval assigned is one with minimum $r_i$ among those still available, because swapping assignments between a loose and tight interval never breaks validity but can only improve slack. This exchange argument ensures the greedy choice preserves feasibility whenever a solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        intervals = [tuple(map(int, input().split())) for _ in range(n)]
        intervals.sort()

        heap = []
        i = 0
        x = 1
        ok = True

        while i < n or heap:
            if not heap and i < n and x < intervals[i][0]:
                x = intervals[i][0]

            while i < n and intervals[i][0] <= x:
                heapq.heappush(heap, intervals[i][1])
                i += 1

            if not heap:
                continue

            r = heapq.heappop(heap)
            if r < x:
                ok = False
                break

            x += 1

        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The core structure is a sweep line over possible assignments. The sorted array ensures intervals are introduced at the correct time. The heap stores only right endpoints because left endpoints are already satisfied when inserted. The variable `x` advances only when we successfully assign or when we must jump over empty regions.

A subtle point is the jump when there are no active intervals. Without it, the algorithm may unnecessarily iterate through huge gaps up to $10^9$, causing timeout. The jump preserves correctness because no interval can be assigned within that gap anyway.

## Worked Examples

### Sample 1

Input:

```
3
1 2
2 3
3 3
```

| Step | x | Active intervals (r values) | Chosen r | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | [2] | 2 | assign |
| 2 | 2 | [3,3] | 3 | assign |
| 3 | 3 | [3] | 3 | assign |

All intervals are matched exactly once, so the assignment succeeds.

This trace shows how the heap always picks the tightest constraint, but feasibility is maintained because each interval has enough slack.

### Sample 2

Input:

```
4
1 2
2 3
3 3
1 4
```

| Step | x | Active intervals (r values) | Chosen r | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | [2,4] | 2 | assign |
| 2 | 2 | [3,4] | 3 | assign |
| 3 | 3 | [3,4] | 3 | assign |
| 4 | 4 | [4] | 4 | assign |

All intervals can be assigned distinct positions.

This demonstrates that even though the long interval $[1,4]$ exists, it does not interfere with feasibility because tighter intervals are prioritized first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ per test case | sorting plus each interval pushed and popped once from heap |
| Space | $O(N)$ | heap and storage for intervals |

The total $N$ across test cases is bounded by $2 \cdot 10^5$, so the solution runs comfortably within limits. The logarithmic factor from heap operations remains small enough for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""2
3
1 2
2 3
3 3
5
1 2
2 3
3 3
1 3
999999999 1000000000
""") == """Yes
No"""

# sample 2
assert run("""1
4
1 2
2 3
3 3
1 4
""") == "Yes"

# minimum case
assert run("""1
1
5 5
""") == "Yes"

# impossible small overlap
assert run("""1
2
1 1
1 1
""") == "No"

# disjoint intervals
assert run("""1
3
1 1
3 3
2 2
""") == "Yes"

# large gap test
assert run("""1
3
100 100
1 1
200 200
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point interval | Yes | minimal correctness |
| identical tight intervals | No | collision detection |
| disjoint order shuffle | Yes | ordering robustness |
| sparse large gaps | Yes | correctness across jumps |

## Edge Cases

A first edge case is when all intervals collapse to single points. For input $[1,1], [1,1]$, the heap contains only a single valid assignment at $x=1$, and the second interval fails immediately because no second position is available.

Another case is when intervals are widely separated. For $[1,1], [100,100], [200,200]$, the algorithm repeatedly jumps `x` to the next available left endpoint. Each interval is isolated, so heap emptiness triggers correct skipping without wasting iterations.

A final case is heavy overlap such as $[1,10]$ repeated many times. The heap grows with all intervals, and the algorithm assigns consecutive integers starting from 1. If the number of intervals exceeds the length of the union of ranges, the heap eventually produces an interval with $r < x$, causing rejection exactly when capacity is exhausted.
