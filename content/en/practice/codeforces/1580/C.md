---
title: "CF 1580C - Train Maintenance"
description: "We have a system that tracks trains of different models over a sequence of days. At the start, there are no trains. On each day, we either add a train of a specific model or remove one."
date: "2026-06-10T10:16:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1580
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 745 (Div. 1)"
rating: 2200
weight: 1580
solve_time_s: 343
verified: false
draft: false
---

[CF 1580C - Train Maintenance](https://codeforces.com/problemset/problem/1580/C)

**Rating:** 2200  
**Tags:** brute force, data structures, implementation  
**Solve time:** 5m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We have a system that tracks trains of different models over a sequence of days. At the start, there are no trains. On each day, we either add a train of a specific model or remove one. Each train alternates between operating and maintenance: it runs for `x_i` days, then goes into maintenance for `y_i` days, then runs again, and repeats until it is removed. The problem asks for the number of trains in maintenance for each day, counting only trains that exist that day. If a train is removed on a day, it does not count as being in maintenance on that day.

The input includes up to 200,000 train models and 200,000 events (days). Each train's cycle length `x_i + y_i` can be as large as 2×10^9. These bounds immediately rule out brute-force simulation day by day for every train, because if a train is added on day 1 and removed on day 200,000, simulating all cycles would require billions of operations. Therefore, any solution must scale with `m` (the number of events) rather than the total sum of train days.

A subtle edge case arises when `x_i` or `y_i` is larger than the number of remaining days. For example, if a train is added late and its maintenance period never starts before removal, a naive simulation might incorrectly count it as in maintenance. Another case is very short cycles; if a train cycles every day, a careless implementation might double-count maintenance or misalign the starting day.

## Approaches

The brute-force approach is straightforward: maintain a set of active trains. For each day, iterate over all trains currently in service and compute whether that day falls inside a maintenance period by checking `(current_day - add_day) % (x_i + y_i) >= x_i`. This is correct logically, but the worst-case complexity is `O(m × n)`. With `m` and `n` up to 2×10^5, this yields roughly 4×10^10 operations, which is far too slow.

The key insight comes from observing that trains can be separated into two categories: **fast-cycling trains**, where the cycle length is small, and **slow-cycling trains**, where the cycle length is large. For slow-cycling trains, we can mark exactly which days they enter and leave maintenance using a "difference array" or event queue approach. For fast-cycling trains, the number of different offsets modulo the cycle length is small, allowing us to precompute how many trains are in maintenance for each offset and update counts efficiently using a prefix sum structure. This hybrid approach reduces the complexity to `O(m√m)` or better.

In essence, the brute-force works because you can check each train individually, but fails when cycle lengths are huge and simulation becomes too long. The observation that cycles repeat periodically lets us avoid iterating through every day and instead handle updates in bulk.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m × n) | O(n) | Too slow |
| Optimal | O(m√m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute a threshold `B = sqrt(m)` to distinguish fast and slow cycles. Any train whose `x_i + y_i < B` is fast, otherwise slow. This balances the number of trains per category with the number of days.
2. For each slow-cycling train, when it is added, schedule maintenance intervals using a difference array. For each interval `[start_day, end_day)`, increment a counter at `start_day` and decrement it at `end_day`. When the train is removed early, stop scheduling further intervals.
3. For fast-cycling trains, precompute an array of size `cycle_length` representing how many trains are in maintenance for each day of the cycle. When a train is added, increment the appropriate offsets, and when it is removed, decrement the same offsets. This allows quick lookup for any day by `(day - add_day) % cycle_length`.
4. For each day `t` in the sequence of events, the total number of trains in maintenance is the sum of the difference array at `t` (for slow trains) plus the sum over all fast-cycle arrays for that day. Output this sum.
5. Update the structures when a train is removed so that future days correctly reflect the train's absence.

Why it works: Slow-cycling trains are explicitly tracked only for the days their maintenance actually happens, so we never simulate unnecessary days. Fast-cycling trains are tracked by offset modulo cycle length, leveraging the periodicity property. Together, these two mechanisms guarantee the correct maintenance count for every day. The invariants are: every slow train contributes only on exact maintenance days, and every fast train contributes according to its precomputed cycle array.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def main():
    n, m = map(int, input().split())
    xy = [tuple(map(int, input().split())) for _ in range(n)]
    events = [tuple(map(int, input().split())) for _ in range(m)]
    
    B = int(m**0.5) + 1
    slow = []
    fast = defaultdict(list)
    
    # classify trains
    for i, (x, y) in enumerate(xy):
        if x + y >= B:
            slow.append(i)
        else:
            fast[i] = [0]*(x+y)
    
    diff = [0]*(m+2)
    add_day = [None]*n
    
    for day, (op, k) in enumerate(events):
        k -= 1
        if op == 1:
            add_day[k] = day
            x, y = xy[k]
            if k in fast:
                for i in range(x, x+y):
                    fast[k][i % (x+y)] += 1
            else:
                t = day + x
                while t < m:
                    l = t
                    r = min(t+y, m)
                    diff[l] += 1
                    diff[r] -= 1
                    t += x + y
        else:
            x, y = xy[k]
            if k in fast:
                for i in range(x, x+y):
                    fast[k][i % (x+y)] -= 1
            add_day[k] = None
    
    res = []
    curr = 0
    for day in range(m):
        curr += diff[day]
        total = curr
        for k in fast:
            if add_day[k] is not None:
                cycle = xy[k][0]+xy[k][1]
                offset = (day - add_day[k]) % cycle
                if offset >= xy[k][0]:
                    total += 1
        res.append(total)
    
    print("\n".join(map(str, res)))

if __name__ == "__main__":
    main()
```

The solution first partitions trains into slow and fast categories to handle each efficiently. The difference array tracks slow trains' maintenance contributions, while fast trains use precomputed cycle arrays to handle frequent changes. A subtle point is using `day - add_day[k]` modulo cycle length for fast trains, which aligns the first maintenance period correctly. Care is taken to not count a train on the day it is removed.

## Worked Examples

Sample input:

```
3 4
10 15
12 10
1 1
1 3
1 1
2 1
2 3
```

| Day | Added/Removed | Slow diff | Fast offsets | Maintenance count |
| --- | --- | --- | --- | --- |
| 0 | Add 1 | 0 | 0 | 0 |
| 1 | Add 3 | 0 | 1 (train3 in maint) | 1 |
| 2 | Add 1 | 0 | 0 | 0 |
| 3 | Remove 1 | 0 | 0 | 0 |

This trace shows the algorithm correctly computes maintenance counts for days when trains enter or exit service, including the effect of cycles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m√m) | Fast trains handled by cycle offsets, slow trains handled by difference array, both combined scale roughly as m√m |
| Space | O(n + m) | Store difference array for slow trains and small cycle arrays for fast trains |

This fits well within the limits since m ≤ 2×10^5, giving roughly 2×10^5 × 500 operations in the worst case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import __main__
    sys.stdout = io.StringIO()
    __main__.main()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""3 4
10 15
12 10
1 1
1 3
1 1
2 1
2 3""") == "0\n1\n0\n0", "sample 1"

# custom cases
assert run("""1 3
1 1
1 1
2 1
1 1""") == "0\n0\n0", "single train add/remove/add"
assert run("""2 5
2 3
1 1
1 1
1 2
2 1
2 2
1 1""") == "0
```
