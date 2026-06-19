---
title: "CF 106484D - Locks"
description: "We are given an array of positions from 1 to n. Each position behaves like a lock that can be either free or already locked by some query. Initially every position is free."
date: "2026-06-19T17:21:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106484
codeforces_index: "D"
codeforces_contest_name: "2026 GBA International Programming Contest"
rating: 0
weight: 106484
solve_time_s: 60
verified: true
draft: false
---

[CF 106484D - Locks](https://codeforces.com/problemset/problem/106484/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positions from 1 to n. Each position behaves like a lock that can be either free or already locked by some query. Initially every position is free.

Each query describes a segment of positions from l to r and two starting times, one for locking and one for unlocking. During the locking phase of a query, we scan its segment from left to right, one position per unit time starting at ts. When we reach a position, if it is currently free, we lock it and assign it to this query. If it is already locked by any other query, we leave it unchanged. The unlocking phase starts later at time te and again scans the same segment in the same order. During this phase, a position is only unlocked if it is currently owned by this query; otherwise nothing happens.

All operations from all queries are placed on a shared time axis. If multiple operations happen at the same time on the same position, they are executed in increasing order of query index.

For each query, we only care about how many positions it successfully locks during its locking phase.

The key difficulty is that locking is global and persistent until explicitly removed, so earlier or later queries can block each other depending on time overlap.

The constraints n, q ≤ 1000 mean that the total number of operations is on the order of q times segment length, which is at most about one million updates for locking and one million for unlocking. This rules out any solution that tries to recompute interactions per query pair or per position pair in a quadratic-in-events way. A simulation over explicitly generated events is feasible, but anything that tries to repeatedly scan time steps or recompute full timelines per query would be too slow.

A subtle case comes from simultaneous operations at the same time. Since multiple queries may operate on different positions at identical timestamps, ordering by query index becomes critical. If this ordering is ignored, a later query could incorrectly steal or override a lock that should have been taken earlier in the same time step.

## Approaches

A direct interpretation simulates time step by time step. For each integer time, we would check all queries, see which positions are being processed, and update the state. However, time ranges go up to 10^9, so iterating over time is impossible.

The more useful perspective is to observe that nothing depends on absolute time, only on the relative ordering of events. Each query generates a sequence of independent operations: a lock attempt for each position in its segment, and later an unlock attempt for the same positions. Each such operation can be represented as a single event with a timestamp.

This converts the problem into a global ordering problem over all events. Each event is either a lock attempt or an unlock attempt on a specific position. The system state only changes when we process these events in increasing time order, breaking ties by query index as required.

Once events are sorted, we simulate them in order. A lock event succeeds only if the position is free at that moment. An unlock event succeeds only if the position is currently owned by that query. We track ownership per position.

This reduces the problem from reasoning about continuous time to a discrete sweep over at most 2qn events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (time simulation) | O(max time × q × segment) | O(n) | Too slow |
| Event sorting + simulation | O(E log E) where E ≤ 2qn | O(n + E) | Accepted |

## Algorithm Walkthrough

We turn each query into explicit events.

1. For every query, generate lock events for all positions in its interval. The event time for position k in [l, r] is ts + (k - l). This models the sequential scanning exactly.
2. For every query, generate unlock events for all positions in its interval. The event time is te + (k - l). This mirrors the same left-to-right traversal but at a later starting time.
3. Store each event as a tuple (time, query_id, type, position), where type distinguishes lock and unlock. We include query_id because tie-breaking requires processing smaller indexed queries first when times match.
4. Sort all events lexicographically by time, then by query_id. The type does not affect ordering because the rule only specifies query order at equal time.
5. Maintain an array owner[pos], initially empty. Also maintain an answer array ans[q], initially zero.
6. Process events in sorted order. If the event is a lock attempt and owner[pos] is empty, assign owner[pos] = query_id and increment ans[query_id]. If it is a lock attempt and the position is already owned, do nothing.
7. If the event is an unlock attempt and owner[pos] equals query_id, clear owner[pos]. Otherwise do nothing.

The key reason this works is that every action affecting a position is represented exactly once in time order. No later event can retroactively change earlier decisions because ownership is only updated when processing events in chronological sequence. The tie-breaking by query index ensures consistency when multiple events share the same timestamp.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    
    events = []
    
    queries = []
    for i in range(q):
        ts, te, l, r = map(int, input().split())
        queries.append((ts, te, l, r))
        
        for k in range(l, r + 1):
            t_lock = ts + (k - l)
            t_unlock = te + (k - l)
            
            events.append((t_lock, i, 0, k))
            events.append((t_unlock, i, 1, k))
    
    events.sort()
    
    owner = [0] * (n + 1)
    ans = [0] * q
    
    for t, i, typ, pos in events:
        if typ == 0:
            if owner[pos] == 0:
                owner[pos] = i + 1
                ans[i] += 1
        else:
            if owner[pos] == i + 1:
                owner[pos] = 0
    
    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The code constructs a full event list for both phases of each query. Lock events are marked with type 0, unlock events with type 1. The sorting step enforces global chronological processing with correct tie-breaking.

The array owner stores which query currently holds each position. Using 0 as “unlocked” simplifies checks. The answer array is incremented only when a lock transition succeeds, which exactly matches the definition of a successful lock during the locking phase.

A subtle point is that unlock events only apply if the current owner matches the query, otherwise they are ignored. This prevents one query from unlocking another query’s lock.

## Worked Examples

Consider a small scenario with n = 3 and two queries.

Query 1: ts = 1, te = 5, l = 1, r = 2

Query 2: ts = 2, te = 4, l = 2, r = 3

We generate events and sort them.

| time | query | type | pos | owner before | action | owner after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | lock | 1 | none | lock | 1 |
| 2 | 1 | lock | 2 | none | lock | 1 |
| 2 | 2 | lock | 2 | 1 | skip | 1 |
| 3 | 2 | lock | 3 | none | lock | 2 |

After processing lock events, query 1 successfully locked 2 positions and query 2 locked 1 position.

This trace shows how query ordering at equal time prevents query 2 from stealing position 2 at time 2, since query 1 is processed first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(qn log(qn)) | Each query produces O(n) events and sorting dominates |
| Space | O(qn + n) | Event storage plus ownership array |

With n, q ≤ 1000, the total number of events is at most 2 × 10^6, and sorting this comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal case
assert run("""1 1
1 2 1 1
""") == "1"

# non-overlapping segments
assert run("""3 2
1 2 1 2
3 4 3 3
""") == "2\n1"

# overlapping conflict
assert run("""3 2
1 5 1 3
2 6 2 3
""") == "3\n0"

# full overlap same segment
assert run("""4 2
1 5 1 4
2 6 1 4
""") == "4\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | basic lock correctness |
| disjoint ranges | 2 1 | independent queries |
| overlapping competition | 3 0 | ownership blocking |
| full overlap | 4 0 | strict priority in time order |

## Edge Cases

A key edge case is simultaneous events at the same timestamp. For example, if query 1 and query 2 both act on the same position at time 2, query order determines the outcome. The sorting by query index ensures query 1 is processed first, so if it locks the position, query 2 will correctly see it as already taken.

Another edge case is unlock not affecting foreign ownership. If query 2 unlocks a position currently owned by query 1, the operation must be ignored. This is handled explicitly by checking owner[pos] == query_id before clearing ownership, preventing accidental cross-query interference.

A final edge case is repeated access to the same position by the same query during its lock phase. Since ownership is only assigned once and subsequent lock attempts do nothing, the increment to ans happens exactly once per successful acquisition, not per visit.
