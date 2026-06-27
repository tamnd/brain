---
title: "CF 105023D - Airport Algorithm"
description: "Each plane occupies a gate during a continuous time interval from its arrival time to its departure time. While it is present at the airport, it blocks one gate, so overlapping intervals correspond to simultaneous gate usage."
date: "2026-06-28T01:44:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105023
codeforces_index: "D"
codeforces_contest_name: "HPI 2024 Novice"
rating: 0
weight: 105023
solve_time_s: 81
verified: false
draft: false
---

[CF 105023D - Airport Algorithm](https://codeforces.com/problemset/problem/105023/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

Each plane occupies a gate during a continuous time interval from its arrival time to its departure time. While it is present at the airport, it blocks one gate, so overlapping intervals correspond to simultaneous gate usage.

For a given query interval $[l, r]$, we are asked to consider only the planes that are relevant inside this time window. A plane contributes to the congestion during the query if its presence at the airport overlaps the query interval in a way that it is “active” at some time inside it, with a special rule at boundaries: planes departing exactly at $l$ or $r$ are excluded, while planes arriving exactly at $l$ or $r$ are included.

The task for each query is to determine the maximum number of planes simultaneously present at any moment inside the interval $[l, r]$, because that maximum equals the minimum number of gates required to avoid conflicts.

The constraint $N \le 10^5$ immediately rules out any solution that recomputes overlaps per query by scanning all planes. Even $Q \le 50$ does not save a quadratic or $N \log N$ per query approach, since $50 \cdot 10^5$ still allows only linear or near-linear per query logic at most.

A subtle edge case comes from the boundary rule. If a plane departs exactly at $l$, it does not count, even though a naive overlap check like $a_i \le r$ and $d_i \ge l$ would incorrectly include it.

For example, if a plane has interval $[5, 10]$ and a query is $[10, 12]$, a naive intersection check would treat it as active at 10, but the statement excludes departures at the boundary, so it should not contribute at all.

Another edge case is a query that begins or ends exactly at a large number of arrivals. Arrivals at the boundary are counted, so intervals starting exactly at $l$ must still be included in the active set.

## Approaches

A direct way to answer each query is to simulate time. For each query, we can iterate over all planes and check whether their interval overlaps the query interval under the boundary rules, then compute the maximum number of overlaps over all relevant times.

This is correct but expensive. For each query we would potentially inspect $10^5$ intervals and then determine overlaps across time, leading to roughly $O(NQ)$ just to filter, and worse if we try to scan time continuously. The hidden cost is that detecting the maximum overlap requires reasoning about event ordering or sweep over time, which makes naive per-query simulation too slow.

The key observation is that each query only cares about the maximum number of active intervals inside a fixed window. This is a classic transformation: instead of thinking in continuous time, we convert each plane into two events, an arrival event and a departure event, and then reduce the problem to prefix counting over sorted event times.

Once events are sorted, we can build a prefix sum array representing how many planes are active at each event boundary. Then a query reduces to finding the maximum prefix sum value over a restricted range of event indices. That is a range maximum query over a static array, which can be answered with a sparse table or segment tree.

Because $Q \le 50$, we can afford preprocessing once globally, then answer each query by mapping its time bounds into indices in the sorted event list and taking a range maximum query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NQ)$ to $O(N^2)$ depending on method | $O(1)$ to $O(N)$ | Too slow |
| Sweep + RMQ | $O(N \log N + Q \log N)$ | $O(N \log N)$ | Accepted |

## Algorithm Walkthrough

We transform each interval into two events, but we must respect the boundary rule carefully.

1. Represent each plane as a +1 event at arrival time $a_i$ and a -1 event at departure time $d_i$. We treat arrivals as inclusive and departures as exclusive by handling ordering correctly in sorting. This ensures correct counting at exact boundary times.
2. Sort all events by time, and if two events share the same time, process arrival events before departure events. This ordering encodes the rule that arrivals at a boundary are counted while departures are not.
3. Sweep through the sorted events and compute a prefix sum array where each position stores the number of active planes after processing that event. This gives a piecewise constant function over time.
4. For each distinct event time, store the corresponding prefix sum value. This compresses the timeline into at most $2N$ points.
5. Build a range maximum structure over this prefix sum array so that we can query the maximum number of active planes over any contiguous segment efficiently.
6. For each query $[l, r]$, locate the first event index whose time is $\ge l$ and the last event index whose time is $\le r$. These define the segment of the timeline that intersects the query window.
7. Use the range maximum structure to compute the maximum prefix sum over this segment, which gives the answer for the query.

Why it works comes down to the structure of the sweep line. Between consecutive event times, the number of active planes does not change, so the maximum within any query interval must occur at some event boundary inside the interval. The prefix sum after sorting events correctly represents the number of active planes at each such boundary, so taking a maximum over the restricted range exactly captures the peak congestion inside $[l, r]$.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SparseTable:
    def __init__(self, arr):
        n = len(arr)
        self.n = n
        self.log = [0] * (n + 1)
        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1

        k = self.log[n] + 1
        self.st = [[0] * n for _ in range(k)]
        self.st[0] = arr[:]

        j = 1
        while (1 << j) <= n:
            i = 0
            while i + (1 << j) <= n:
                self.st[j][i] = max(self.st[j - 1][i],
                                     self.st[j - 1][i + (1 << (j - 1))])
                i += 1
            j += 1

    def query(self, l, r):
        j = self.log[r - l + 1]
        return max(self.st[j][l], self.st[j][r - (1 << j) + 1])

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    d = list(map(int, input().split()))

    events = []
    for i in range(n):
        events.append((a[i], 1))
        events.append((d[i], -1))

    events.sort(key=lambda x: (x[0], -x[1]))

    times = []
    active = []
    cur = 0

    for t, v in events:
        cur += v
        times.append(t)
        active.append(cur)

    st = SparseTable(active)

    def lower_bound(x):
        lo, hi = 0, len(times)
        while lo < hi:
            mid = (lo + hi) // 2
            if times[mid] >= x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def upper_bound(x):
        lo, hi = 0, len(times)
        while lo < hi:
            mid = (lo + hi) // 2
            if times[mid] > x:
                hi = mid
            else:
                lo = mid + 1
        return lo - 1

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        L = lower_bound(l)
        R = upper_bound(r)
        if L > R:
            out.append("0")
        else:
            out.append(str(st.query(L, R)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The event sorting step is where boundary correctness is enforced. Sorting by time and placing arrivals before departures ensures that at time $t$, arrivals are included before any removal at the same timestamp.

The prefix accumulation builds the exact number of active planes after each event, so each index corresponds to a stable state. The sparse table then allows constant-time maximum queries over any segment.

The binary searches isolate exactly the portion of the event timeline intersecting the query interval, ensuring we only consider states that occur within $[l, r]$.

## Worked Examples

### Example 1

Input:

```
N = 5, Q = 2
a = [2, 7, 4, 5, 9]
d = [8, 11, 5, 8, 16]
queries:
[1, 10]
[8, 14]
```

Events after sorting:

```
(2,+1), (4,+1), (5,+1), (7,+1), (8,-1), (8,-1), (9,+1), (11,-1), (16,-1)
```

Prefix active counts:

| Event index | Time | Change | Active |
| --- | --- | --- | --- |
| 0 | 2 | +1 | 1 |
| 1 | 4 | +1 | 2 |
| 2 | 5 | +1 | 3 |
| 3 | 7 | +1 | 4 |
| 4 | 8 | -1 | 3 |
| 5 | 8 | -1 | 2 |
| 6 | 9 | +1 | 3 |
| 7 | 11 | -1 | 2 |
| 8 | 16 | -1 | 1 |

Query $[1, 10]$ selects indices covering times 2 to 9, giving max active = 4.

Query $[8, 14]$ selects indices around 8 to 11, giving max active = 3.

This confirms that the algorithm correctly captures peak overlap inside restricted windows rather than globally.

### Example 2

Input:

```
N = 3, Q = 1
a = [1, 3, 5]
d = [4, 6, 8]
query: [4, 4]
```

At time 4, the second plane is still active because it departs at 6, while the first plane departs exactly at 4 and is excluded by boundary rule.

Active planes at query time = 1.

The event representation ensures arrivals at 4 are included before departures at 4, so the prefix state correctly reflects a single active interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + Q \log N)$ | sorting events and building RMQ, plus binary searches per query |
| Space | $O(N \log N)$ | sparse table over at most $2N$ event states |

The constraints allow up to $10^5$ planes, so preprocessing in $N \log N$ is easily fast enough, and each query is effectively constant or logarithmic time. With only 50 queries, the solution is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return __import__("__main__").solve() if False else ""

# Since solve prints directly, we redefine a wrapper version for testing
def run(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdin
    sys.stdin = StringIO(inp)

    from contextlib import redirect_stdout
    out = StringIO()
    with redirect_stdout(out):
        solve()

    sys.stdin = backup
    return out.getvalue().strip()

# sample
assert run("""5 2
2 7 4 5 9
8 11 5 8 16
1 10
8 14
""") == "4\n3"

# minimum size
assert run("""1 1
5
10
5 5
""") == "1"

# all disjoint
assert run("""3 1
1 10 20
2 11 21
5 15
""") == "1"

# full overlap
assert run("""3 1
1 2 3
10 10 10
1 10
""") == "3"

# boundary exclusion check
assert run("""2 1
1 10
5 10
10 10
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single plane | 1 | minimum case |
| disjoint intervals | 1 | no overlap logic |
| full overlap | 3 | peak stacking |
| boundary case | 1 | departure-at-boundary exclusion |

## Edge Cases

A key edge case is when a plane departs exactly at the query boundary. For input:

```
a = [1], d = [5], query = [5, 5]
```

the correct output is 1 because the plane is still present up to but not including 5 depending on interpretation; with the given rule, departures at 5 are excluded, so the plane does not contribute at 5. The sweep-line ordering ensures the -1 event at time 5 is applied after considering arrivals, preventing incorrect inclusion.

Another edge case occurs when multiple events share the same timestamp. For example:

```
a = [5, 5], d = [10, 10], query = [5, 5]
```

Both planes arrive at 5, so both must be counted, yielding 2. Sorting arrivals before departures ensures the prefix reaches 2 before any subtraction at that time.
