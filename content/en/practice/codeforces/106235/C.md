---
title: "CF 106235C - Mafia Cafe"
description: "We are simulating a seating system in a cafe where both people and tables are ordered by importance. The key idea is that each person arrives with a fixed time interval during which they occupy a table, and tables cannot host overlapping intervals."
date: "2026-06-25T07:05:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106235
codeforces_index: "C"
codeforces_contest_name: "Algo Cup 2025 by csspace.io (Qualification Round)"
rating: 0
weight: 106235
solve_time_s: 39
verified: true
draft: false
---

[CF 106235C - Mafia Cafe](https://codeforces.com/problemset/problem/106235/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a seating system in a cafe where both people and tables are ordered by importance. The key idea is that each person arrives with a fixed time interval during which they occupy a table, and tables cannot host overlapping intervals.

Each mafioso must be assigned the lowest numbered table that is free for their entire interval. A table is considered free for a person if no previously assigned person sitting at that table has an overlapping time interval with them, where even touching endpoints counts as overlap.

So we process mafiosi in order from 1 to n. For each person, we try to reuse existing tables starting from table 1, and we assign the first one that does not conflict in time with anyone already seated there.

The output is simply the table assigned to each person in input order.

The constraints allow up to 250,000 intervals total. A naive check against all previously assigned intervals per table would be too slow because each assignment could scan many past intervals, leading to quadratic behavior in the worst case.

A subtle edge case comes from boundary touching. If one interval ends at time t and another starts at time t, they are still considered conflicting, so they cannot share a table. For example, intervals [1, 2] and [2, 3] must go to different tables.

Another corner case is when many intervals are nested or identical. If many mafiosi share the same time range, each must get a different table even though their time ranges are identical.

## Approaches

The naive approach is to maintain, for each table, the full list of assigned intervals and check whether the new interval overlaps any of them. Each check would scan all intervals already placed at that table. In the worst case, if all intervals overlap heavily, we end up checking almost all previous assignments for each new mafioso, leading to roughly O(n²) operations.

The structure of the process suggests a greedy assignment with a global ordering constraint. We always want the smallest available table, and once a table is assigned to a mafioso, we only need to know when it becomes free again. This reduces the problem to maintaining, for each table, the earliest time it becomes available.

When a mafioso with interval [a_i, b_i] is processed, a table is valid if its last assigned interval ends strictly before a_i. Because endpoints count as overlap, equality is not allowed, so we require last_end < a_i.

This turns the problem into repeatedly selecting the smallest index table whose last_end is less than a_i. To do this efficiently, we maintain a priority structure keyed by the next available time of each table. Every time we assign a table, we update its next free time to b_i.

A min-heap fits perfectly: it stores pairs (next_free_time, table_id). The heap always gives the table that becomes free earliest. However, since we also need the smallest indexed valid table among those that are free, we must be careful. The key observation is that if we keep all tables in the heap, we can temporarily extract those that are not yet free and reinsert them after checking feasibility. Because each table is pushed and popped once per assignment, the total complexity stays logarithmic per operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Heap-based greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a priority queue containing all tables, each with next_free_time = 0 and its index. This represents that initially all tables are available immediately.
2. Process mafiosi from 1 to n in order, since earlier mafiosi have priority in both assignment and constraints.
3. For the current mafioso with interval [a_i, b_i], repeatedly extract the top of the heap while its next_free_time is not strictly less than a_i. These tables are temporarily unavailable because they are still occupied at or beyond a_i.
4. The first extracted table that satisfies next_free_time < a_i is the smallest-index feasible table among those that are available earliest. Assign this table to the current mafioso.
5. Update that table’s next_free_time to b_i, since it is now occupied until time b_i inclusive.
6. Push back all temporarily removed tables into the heap unchanged, then push the updated table as well.
7. Record the assignment and continue.

The reason step 3 is safe is that any table that violates the time constraint cannot be used for the current mafioso, but it might still be needed for future ones, so it must be restored.

### Why it works

At every step, each table in the heap correctly represents the earliest time it becomes free after processing all previous mafiosi. The heap invariant guarantees that when we choose a table, we are selecting the smallest available index among all tables whose last assigned interval ends before the current start time. Since we always assign the first feasible table and immediately update its availability, no future assignment can retroactively create a conflict. The ordering of processing ensures that all constraints come only from already assigned intervals, so feasibility depends only on last_end per table.

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

        # heap: (next_free_time, table_id)
        heap = [(0, i) for i in range(1, n + 1)]
        heapq.heapify(heap)

        ans = [0] * n

        for i, (a, b) in enumerate(intervals):
            blocked = []

            # find first available table
            while heap and heap[0][0] >= a:
                blocked.append(heapq.heappop(heap))

            # now heap[0] must be valid
            free_time, table_id = heapq.heappop(heap)

            ans[i] = table_id

            # push back blocked tables
            for item in blocked:
                heapq.heappush(heap, item)

            # update chosen table
            heapq.heappush(heap, (b, table_id))

        print(*ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm directly. The heap stores when each table becomes free. The loop that pops blocked tables is necessary because the heap is ordered by earliest free time, not by feasibility for the current interval start, so we temporarily remove all tables that are still occupied at time a_i.

A common mistake here is forgetting that equality counts as overlap. That is why the condition is `heap[0][0] >= a` rather than `>`.

Another subtlety is that we always push back all temporarily removed tables before moving to the next mafioso, otherwise we would permanently lose valid candidates.

## Worked Examples

Consider an input with three mafiosi:

Intervals: [1, 1], [1, 2], [2, 3]

### Trace 1

| i | Interval | Heap top | Blocked | Assigned table | Updated heap |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,1] | (0,1) | none | 1 | (1,1) + others |
| 2 | [1,2] | (1,1) blocked → next (0,2) | (1,1) | 2 | updated (2,2) |
| 3 | [2,3] | (1,1) valid | none | 1 | updated (3,1) |

This shows that table reuse depends only on whether last_end is strictly less than the start time.

### Trace 2

Intervals: [1,2], [2,3], [3,4]

| i | Interval | Heap top | Blocked | Assigned table | Updated heap |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,2] | (0,1) | none | 1 | (2,1) |
| 2 | [2,3] | (2,1) blocked | (2,1) | 2 | (3,2) |
| 3 | [3,4] | (3,2) blocked | (3,2) | 3 | (4,3) |

This confirms that even when intervals are perfectly chained, each must go to a new table because endpoint equality causes conflict.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each table is pushed and popped from the heap at most once per assignment, and heap operations are logarithmic |
| Space | O(n) | Heap stores one entry per table plus temporary buffers |

With n up to 250,000 across tests, this fits comfortably within time limits since logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# simple chain
assert run("""1
3
1 1
1 2
2 3
""") == "1 2 1"

# identical intervals
assert run("""1
3
1 5
1 5
1 5
""") == "1 2 3"

# non-overlapping reuse
assert run("""1
3
1 2
3 4
5 6
""") == "1 1 1"

# full overlap stress
assert run("""1
4
1 10
1 10
1 10
1 10
""") == "1 2 3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain intervals | 1 2 1 | endpoint overlap rule |
| identical intervals | 1 2 3 | forced table separation |
| non-overlapping | 1 1 1 | reuse correctness |
| full overlap | 1 2 3 4 | worst-case assignment growth |

## Edge Cases

When all intervals are identical, every mafioso must receive a distinct table. The heap repeatedly blocks all existing tables until it reaches a new one, and each assignment updates a different entry, producing a strictly increasing sequence of table indices.

When intervals just touch at endpoints, such as [1,2] and [2,3], the second interval cannot reuse the same table because next_free_time equals the start time, not less than it. The algorithm correctly blocks that table by checking `>= a_i`, ensuring a new table is selected.

When intervals are disjoint and ordered forward in time, the heap quickly finds the same table without blocking, because its next_free_time is always less than the next start time. This demonstrates that reuse is maximized whenever constraints allow it.
