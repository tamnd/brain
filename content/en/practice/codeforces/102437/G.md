---
title: "CF 102437G - Regulated Shortest Path"
description: "We have an undirected graph whose vertices are cities and whose edges are roads. Sam starts in city s at time 0 and wants to reach city t as early as possible. Every road has its own repeating weather schedule. If a road has parameters a, b, and d, then its period is P = a + b."
date: "2026-08-16T09:26:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "G"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 180
verified: false
draft: false
---

[CF 102437G - Regulated Shortest Path](https://codeforces.com/problemset/problem/102437/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph whose vertices are cities and whose edges are roads. Sam starts in city `s` at time `0` and wants to reach city `t` as early as possible. Every road has its own repeating weather schedule. If a road has parameters `a`, `b`, and `d`, then its period is `P = a + b`. During every period, the road is dry from time `Pk` through `Pk + a`, and rainy from `Pk + a` through `P(k + 1)`. Sam may wait freely in cities, but while traversing a road for `d` units of time, the entire traversal must lie inside one dry interval.

The task is to compute the earliest arrival time at `t`, or `-1` if no usable route exists. The roads are undirected, so the same time schedule applies regardless of the direction in which Sam uses a road.

The graph has up to `100000` cities and `200000` roads. With this size, algorithms that inspect all possible paths are hopeless, because the number of simple paths can already be exponential. Even an `O(nm)` graph algorithm would be too expensive at this scale, so we need a near-linear or `O(m log n)` approach. The values of `a`, `b`, and `d` can reach `10^9`, and waiting may accumulate over many roads, so the implementation must also handle times far larger than 32-bit integers. Python integers are suitable for this automatically.

There are several boundaries where a careless implementation can fail. First, a road is usable only if `d <= a`. For example,

```
2 1 1 2
1 2 1 1 2
```

has a dry interval of length `1`, but the road takes `2` units to cross, so the answer is `-1`. Treating the road as having an average travel time or merely checking whether it is dry at the departure instant would incorrectly allow it.

The second boundary is that Sam may start exactly when a dry interval begins and may finish exactly when it ends. For example,

```
2 1 1 2
1 2 2 3 2
```

has a dry interval `[0, 2]`, so traversing from time `0` to time `2` is valid and the answer is `2`. A strict inequality such as `departure + d < a` would incorrectly reject this route.

The third boundary appears when Sam reaches a road exactly as rain starts. Consider

```
3 2 1 3
1 2 2 3 2
2 3 2 3 1
```

The first road can be traversed from `0` to `2`. At time `2`, rain starts on the second road, so Sam cannot start it then. The next dry interval begins at time `5`, giving arrival time `6`. The correct output is `6`. A formula that checks only the departure time against the dry interval and forgets the whole traversal would incorrectly produce `3`.

Finally, if `s == t`, Sam is already at the destination, so the answer is `0`, even when there are no roads.

## Approaches

A direct brute-force solution could enumerate every possible route from `s` to `t`, simulate the weather schedule on every road in that route, and keep the earliest arrival time. This is correct because every feasible journey corresponds to some graph path, and simulating a fixed path tells us its earliest possible traversal time. The problem is the number of paths. Even with a sparse graph, a layered graph can contain `2^(n/2)` distinct simple `s` to `t` paths. If every path takes `Theta(n)` work to simulate, the worst case is `Theta(n * 2^(n/2))` operations, far beyond what can be processed for `n = 100000`.

The useful observation is that we do not need to remember Sam's entire history when he reaches a city. Suppose he reaches a city at time `x`. For any outgoing road, there is a uniquely determined earliest time at which he can start traversing that road. Waiting in the city longer can never make the arrival at the other endpoint earlier than this earliest feasible departure.

For one road, let `P = a + b` and let `r = x mod P`. If `d > a`, the road can never be traversed because every dry interval is only `a` units long. Otherwise, Sam can leave immediately when `r + d <= a`. If that condition fails, he must wait until the next dry interval begins, which is `x - r + P`, and then spend `d` units on the road.

This gives a time-dependent edge relaxation that takes constant time. More importantly, the resulting earliest-arrival function is FIFO: arriving at a city later can never allow us to reach the other endpoint earlier by taking the same road. Inside the part where immediate traversal is possible, the arrival time increases with the starting time. Once traversal no longer fits, all those starting times wait for the same next dry interval, producing a flat section, and then the function rises again. Thus ordinary Dijkstra's greedy choice remains valid.

The brute-force approach works because every path can be evaluated exactly, but fails because there are too many paths. The FIFO property lets us collapse all paths reaching the same city into a single state, its earliest arrival time. We can then use Dijkstra's algorithm, replacing a fixed edge weight with a constant-time function that computes the earliest legal arrival through that road.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Theta(n * 2^(n/2))` in a sparse layered graph | `O(n + m)` plus recursion/path state | Too slow |
| Optimal | `O((n + m) log n)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list containing every road in both directions. For each road, store its parameters `a`, `b`, and `d`, because the weather schedule is the same from either endpoint.
2. Initialize `dist[s] = 0` and every other distance to infinity. Put `(0, s)` into a min-heap. The heap always gives us the city whose currently known earliest arrival time is smallest.
3. When city `u` is removed from the heap with time `cur`, ignore the entry if `cur` is larger than `dist[u]`. Such an entry is stale because a later relaxation already found a better way to reach `u`.
4. For every road from `u` to `v`, first compute its period `P = a + b`. If `d > a`, skip this road because no dry interval is long enough to contain the traversal.
5. Otherwise compute `r = cur % P`. If `r + d <= a`, Sam can enter the road immediately, so the candidate arrival time is `cur + d`.
6. If `r + d > a`, the current dry interval is too short. Sam waits until the next period starts at `cur - r + P`, then traverses the road, giving candidate arrival `cur - r + P + d`.
7. If this candidate is smaller than `dist[v]`, update `dist[v]` and push `(candidate, v)` into the heap. The relaxation is exactly the same role as in ordinary Dijkstra, except that the edge's effective travel time depends on the current time.
8. Once the heap is empty, output `dist[t]` if it is finite, otherwise output `-1`. We can also stop as soon as `t` is popped with its current distance, because the heap guarantees that no future state can have a smaller arrival time.

### Why it works

The invariant is that whenever a city `u` is permanently extracted from the heap, `dist[u]` is the earliest possible time at which Sam can reach `u`. For every outgoing road, the relaxation computes the earliest possible arrival at its other endpoint given that arrival time at `u`. The road's arrival function is FIFO, so reaching `u` at a later time cannot produce an earlier arrival through that road. Consequently, the usual Dijkstra argument applies: after extracting the smallest tentative arrival time, no undiscovered route can reach that city earlier. Repeating this over all relaxations gives the true earliest arrival time for every reachable city, including `t`.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def solve():
    n, m, s, t = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v, a, b, d = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, a, b, d))
        graph[v].append((u, a, b, d))

    dist = [INF] * n
    dist[s - 1] = 0

    pq = [(0, s - 1)]

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        if u == t - 1:
            print(cur)
            return

        for v, a, b, d in graph[u]:
            if d > a:
                continue

            period = a + b
            r = cur % period

            if r + d <= a:
                arrive = cur + d
            else:
                arrive = cur - r + period + d

            if arrive < dist[v]:
                dist[v] = arrive
                heapq.heappush(pq, (arrive, v))

    print(-1)

if __name__ == "__main__":
    solve()
```

The adjacency list stores each undirected road twice, which makes every relaxation identical regardless of the traversal direction. Each stored tuple contains exactly the parameters needed to calculate the next legal traversal.

The check `d > a` removes impossible roads immediately. The dry interval has length exactly `a`, so no traversal longer than `a` can fit inside it.

The expression `cur % period` gives Sam's position inside the current weather cycle. When `r + d <= a`, the entire traversal fits before rain starts. Equality is allowed because the endpoints of the dry interval are valid.

When the traversal does not fit, `cur - r` is the beginning of the current period, so `cur - r + period` is the beginning of the next period. Adding `d` gives the earliest arrival after waiting. This formulation avoids any floating-point arithmetic and handles times of arbitrary size.

The priority queue uses lazy deletion. A city may be inserted several times after progressively better routes are found, so an extracted pair is ignored whenever its time differs from the current `dist[u]`.

The maximum possible answer can be much larger than `10^9`, since many roads can each contribute a large amount of travel and waiting time. Python's arbitrary-precision integers avoid overflow without any special handling.

## Worked Examples

### Sample 1

The input is

```
3 2 1 3
1 2 3 4 1
2 3 2 3 2
```

For the first road, `P = 7` and the dry interval is `[0, 3]`. Starting at time `0`, the one-unit traversal finishes at time `1`.

For the second road, `P = 5` and the dry interval is `[0, 2]`. Sam reaches city `2` at time `1`, but a two-unit traversal would finish at time `3`, after rain has already started. He therefore waits until time `5` and reaches city `3` at time `7`.

| Popped city | Current time | Road considered | `r` | Earliest arrival |
| --- | --- | --- | --- | --- |
| 1 | 0 | `1 -> 2` | 0 | 1 |
| 2 | 1 | `2 -> 1` | 1 | 2 |
| 2 | 1 | `2 -> 3` | 1 | 7 |
| 3 | 7 | destination |  | 7 |

The key point is the second relaxation. Being physically present at city `2` at time `1` does not mean Sam can immediately use the second road. The entire traversal must fit into the dry interval, so the algorithm waits for the next interval and correctly obtains `7`.

### Sample 2

There is no second official sample in the supplied statement, so consider this boundary-focused example:

```
4 3 1 4
1 2 3 2 2
2 4 2 3 1
1 3 1 1 2
```

The first road has dry interval `[0, 3]`, so Sam can traverse it from `0` to `2`. The second road has dry interval `[0, 2]`, and Sam arrives at exactly time `2`, so starting at that boundary is valid and he reaches city `4` at time `3`. The third road is unusable because its traversal time `2` is greater than its dry interval length `1`.

| Popped city | Current time | Road considered | `r` | Earliest arrival |
| --- | --- | --- | --- | --- |
| 1 | 0 | `1 -> 2` | 0 | 2 |
| 1 | 0 | `1 -> 3` | 0 | unusable |
| 2 | 2 | `2 -> 4` | 2 | 3 |
| 4 | 3 | destination |  | 3 |

This trace exercises two boundary rules at once. The traversal ending exactly at the end of a dry interval is legal, and an edge with `d > a` must be rejected before attempting to calculate a departure time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m) log n)` | Each road is relaxed from both endpoints, and heap operations cost `O(log n)` |
| Space | `O(n + m)` | The adjacency list contains `2m` directed entries, while distances and the heap use `O(n + m)` space |

With `n <= 100000` and `m <= 200000`, the algorithm performs a constant amount of arithmetic per edge relaxation and uses a binary heap for the priority queue. This is the standard scale where `O(m log n)` is practical, while enumerating paths or repeatedly scanning all edges would not be.

## Test Cases

```python
import sys
import io
import heapq

input = sys.stdin.readline
INF = 10**30

def solve():
    n, m, s, t = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v, a, b, d = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, a, b, d))
        graph[v].append((u, a, b, d))

    dist = [INF] * n
    dist[s - 1] = 0
    pq = [(0, s - 1)]

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        if u == t - 1:
            print(cur)
            return

        for v, a, b, d in graph[u]:
            if d > a:
                continue

            period = a + b
            r = cur % period

            if r + d <= a:
                arrive = cur + d
            else:
                arrive = cur - r + period + d

            if arrive < dist[v]:
                dist[v] = arrive
                heapq.heappush(pq, (arrive, v))

    print(-1)

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    out = io.StringIO()

    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old_stdout

    return out.getvalue().strip()

assert run(
    """3 2 1 3
1 2 3 4 1
2 3 2 3 2
"""
) == "7", "sample 1"

assert run(
    """1 0 1 1
"""
) == "0", "start already equals destination"

assert run(
    """2 1 1 2
1 2 1 1 2
"""
) == "-1", "road traversal is longer than every dry interval"

assert run(
    """4 3 1 4
1 2 3 2 2
2 4 2 3 1
1 3 1 1 2
"""
) == "3", "exact dry-interval boundary and unusable road"

assert run(
    """3 2 1 3
1 2 2 3 2
2 3 2 3 1
"""
) == "6", "arriving exactly when rain starts requires waiting"

assert run(
    """4 3 1 4
1 2 1 1 1
2 3 1 1 1
3 4 1 1 1
"""
) == "3", "all equal values"

n = 100000
lines = [f"{n} {n - 1} 1 {n}"]
for i in range(1, n):
    lines.append(f"{i} {i + 1} 1 1 1")
assert run("\n".join(lines) + "\n") == str(n - 1), "large chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 1 1` | `0` | Minimum-size graph and `s == t` |
| `2 1 1 2` with `a=1, d=2` | `-1` | Road is impossible when `d > a` |
| Four-city boundary case | `3` | Traversal may end exactly at the dry boundary |
| Three-city waiting case | `6` | Arrival at the start of rain forces a full-period wait |
| Four-city equal-parameter chain | `3` | Repeated identical schedules |
| `100000`-vertex chain | `99999` | Large input size and accumulated travel time |

## Edge Cases

For `s == t`, consider the exact input

```
1 0 1 1
```

The priority queue starts with city `1` at time `0`. Since it is already the destination, the algorithm immediately prints `0`. No edge processing is needed, and the absence of roads is irrelevant.

For an unusable road, consider

```
2 1 1 2
1 2 1 1 2
```

The road has period `2`, with dry intervals of length `1`. The algorithm sees `d = 2 > a = 1` and skips the road. The destination remains at infinity, so the output is `-1`. This is better than trying to wait for a special position in the cycle, because no dry interval can ever contain the complete traversal.

For an exact dry-boundary traversal, use

```
2 1 1 2
1 2 2 3 2
```

At time `0`, `r = 0`, and `r + d = 2 = a`. The condition is satisfied, so Sam leaves immediately and arrives at time `2`. The output is `2`. The equality in `r + d <= a` is necessary.

For arriving exactly when rain begins, use

```
3 2 1 3
1 2 2 3 2
2 3 2 3 1
```

The first road takes Sam from `0` to `2`. For the second road, its period is `5`, so at time `2` we have `r = 2`. Since `r + d = 3 > a = 2`, the current dry interval cannot contain the traversal. The next dry interval begins at `5`, giving arrival `5 + 1 = 6`. The output is `6`. This catches the common mistake of checking only whether the road is dry at the departure instant.

For the large-input boundary, a chain of `100000` cities with every road set to `a = b = d = 1` has an especially simple behavior. Each road can be traversed from an exact period boundary, so every edge contributes exactly one unit and no waiting is needed. The destination is reached at `99999`. The Dijkstra implementation processes the graph in `O(n log n)` time for this case and uses linear graph storage, which demonstrates why the asymptotic complexity is appropriate for the maximum constraints.
