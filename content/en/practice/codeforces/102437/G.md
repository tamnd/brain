---
title: "CF 102437G - Regulated Shortest Path"
description: "We have an undirected graph of cities and roads. Sam starts in city s at time 0 and wants the earliest possible arrival at city t. Each road has three parameters. Its traversal time is d. The weather on that road is periodic, with period [ P=a+b."
date: "2026-08-14T15:44:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "G"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 227
verified: false
draft: false
---

[CF 102437G - Regulated Shortest Path](https://codeforces.com/problemset/problem/102437/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph of cities and roads. Sam starts in city `s` at time `0` and wants the earliest possible arrival at city `t`.

Each road has three parameters. Its traversal time is `d`. The weather on that road is periodic, with period

[
P=a+b.
]

During every period, the road is dry from time `kP` through `kP+a`, and it rains from `kP+a` through `(k+1)P`. Sam may wait freely in cities, so when he reaches an endpoint of a road, he only needs to choose a suitable future dry interval.

A traversal of duration `d` is possible only if the whole interval spent on the road is dry. If Sam enters the road at time `x`, he needs

[
x+d\le kP+a
]

for the appropriate period. Entering exactly when rain stops is allowed, and arriving exactly when rain starts is also allowed.

The task is to find the minimum possible arrival time at `t`, or `-1` if no usable sequence of roads exists.

The graph can contain `100000` vertices and `200000` edges. With this size, algorithms such as enumerating paths or performing `O(nm)` graph relaxations are far beyond a practical time limit. In the worst case, `nm` is about `2\cdot10^{10}` edge examinations. We need a near-linear graph algorithm, typically around `O((n+m)\log n)`.

There are several boundary cases that can make an otherwise plausible implementation wrong. First, a road can have traversal time longer than its entire dry interval. For example,

```
2 1 1 2
1 2 3 5 4
```

Here the dry interval lasts only `a=3`, while crossing takes `d=4`. The road can never be used, so the correct output is `-1`. A careless implementation that merely waits for the next dry period and adds `d` would incorrectly claim that the road is traversable.

A second boundary case occurs when the traversal ends exactly when rain starts. For example,

```
2 1 1 2
1 2 3 5 3
```

The road is dry from time `0` through time `3`. Sam can enter at `0`, spend `3` units on the road, and arrive at time `3`, exactly when rain begins. The correct output is `3`. The condition must consequently be `remaining_dry >= d`, not `remaining_dry > d`.

A third case is arriving during rain. Consider

```
2 1 1 2
1 2 3 5 2
```

The first dry interval is `[0,3]`, so Sam can cross immediately and arrive at `2`. But if some previous road brought him to this road at time `4`, he cannot enter immediately because time `4` is inside the rain interval `[3,8]`. He has to wait until time `8`, then cross and arrive at `10`. Using only `time % period` without distinguishing the dry and rainy portions would produce an invalid departure.

Finally, a road can be perfectly usable while the current arrival time is exactly at the beginning of a new dry interval. With `a=3`, `b=5`, arriving at time `8` gives remainder `0`, so departure is immediately possible. The formula must treat remainder `0` as dry rather than waiting for another period.

## Approaches

A direct brute-force solution can use repeated graph relaxation. Suppose `dist[v]` is the earliest known time at which Sam can reach city `v`. For every edge, we can calculate the earliest arrival through that edge and repeatedly relax all edges until no value changes. This is essentially Bellman-Ford adapted to the time-dependent edge costs.

The relaxation itself is correct because once the arrival time at an endpoint is known, the edge has a well-defined earliest possible arrival time. Repeating the relaxations eventually propagates information along paths containing many edges.

The problem is the number of repetitions. In the worst case, Bellman-Ford needs `n-1` full passes, and every pass examines all `m` roads. With `n=100000` and `m=200000`, that is up to

[
(n-1)m\approx2\cdot10^{10}
]

edge examinations. This is much too large.

The key observation is that every road behaves like a time-dependent edge with the FIFO property. If Sam reaches a road endpoint later, the earliest possible arrival at the other endpoint can never become earlier. Waiting is always allowed, and the earliest feasible departure is simply the first dry interval that can contain the entire traversal.

That property lets us use Dijkstra's algorithm. The usual Dijkstra argument still applies: when the currently smallest tentative arrival time is extracted, no later route can reach that city earlier. The only additional work is replacing a fixed edge weight with a function that computes the earliest legal arrival time from the current time.

Suppose the current time is `x` and the road has period `P=a+b`. Let

[
r=x\bmod P.
]

If `r <= a-d`, the road has enough dry time remaining in the current dry interval, so Sam can leave immediately and arrive at `x+d`.

If `r > a-d`, the current dry interval is already too short. Sam must wait until the next period begins, at time `x-r+P`, and then spend `d` time crossing. This gives the candidate arrival time

[
x-r+P+d.
]

When `d>a`, no period contains enough dry time for the traversal, so the edge is unusable in both directions.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` | `O(n+m)` | Too slow |
| Optimal | `O((n+m) log n)` | `O(n+m)` | Accepted |

## Algorithm Walkthrough

1. Store every road in the adjacency list of both endpoints. Each stored edge contains the other endpoint and its values `a`, `b`, and `d`, because the road is bidirectional and has the same weather schedule in either direction.
2. If `d > a`, ignore the road during relaxation. Its dry interval has length `a`, so there is no possible continuous traversal of length `d`.
3. Initialize `dist[s] = 0` and every other distance to infinity. Put `(0, s)` into a min-heap. The heap always gives us the city with the smallest currently known arrival time.
4. When city `u` is extracted with time `cur`, discard the entry if it is stale, meaning `cur != dist[u]`. Otherwise, `cur` is the earliest known arrival time at `u`.
5. For every road from `u` to `v`, calculate its period `P = a+b` and the remainder `r = cur % P`. The current dry interval can be used exactly when

[
r+d\le a,
]

which is equivalent to `r <= a-d`.

1. If the road can be used immediately, its candidate arrival time is `cur+d`. Otherwise, compute the beginning of the next dry interval as `cur-r+P`, and use candidate arrival time `cur-r+P+d`.
2. If this candidate is smaller than `dist[v]`, update `dist[v]` and push the new pair into the heap. This is the same relaxation operation as in ordinary Dijkstra, except that the effective edge cost depends on the current time.
3. When city `t` is extracted from the heap, return its distance. If the heap becomes empty first, `t` is unreachable and the answer is `-1`.

The correctness invariant is that every stored `dist[v]` is the earliest arrival time found so far, and every relaxation computes the true earliest possible arrival through that particular road from the current time. Because the earliest-arrival function of every road is nondecreasing, reaching a city later can never create an earlier opportunity downstream. Thus, when the minimum-distance heap entry for a city is finalized, no unexplored route can beat it. This is exactly the property Dijkstra needs, so the final distance of `t` is optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, s, t = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v, a, b, d = map(int, input().split())

        # If d > a, there is no dry interval long enough
        # to traverse this road.
        if d <= a:
            graph[u].append((v, a, b, d))
            graph[v].append((u, a, b, d))

    INF = 10**30
    dist = [INF] * (n + 1)
    dist[s] = 0

    pq = [(0, s)]

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        if u == t:
            print(cur)
            return

        for v, a, b, d in graph[u]:
            period = a + b
            rem = cur % period

            if rem <= a - d:
                # Enough dry time remains in the current period.
                nd = cur + d
            else:
                # Wait for the next period to start.
                nd = cur - rem + period + d

            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    print(-1)

if __name__ == "__main__":
    solve()
```

The adjacency list contains only usable roads. Removing roads with `d > a` is safe because every dry interval has exactly length `a`, regardless of which period it belongs to.

For a usable road, `period = a + b` describes one complete weather cycle. The expression `cur % period` tells us where the current time lies inside that cycle. The road is dry while the remainder is at most `a`, but crossing requires `d` consecutive units, so the actual condition is `rem + d <= a`, implemented as `rem <= a - d`.

The waiting calculation deserves particular attention. If the current remainder is `rem`, the current period began at `cur - rem`. Its next beginning is consequently `cur - rem + period`. Adding `d` gives the earliest arrival after waiting. This avoids any loop over individual time units or periods.

Python integers have arbitrary precision, so the potentially large arrival times do not overflow. The maximum answer can be much larger than `32`-bit integer limits because many roads and waiting periods can accumulate.

The early return when `t` is popped is valid for Dijkstra because heap entries are processed in nondecreasing distance order. At that moment the popped distance is final.

## Worked Examples

The supplied example is

```
3 2 1 3
1 2 3 4 1
2 3 2 3 2
```

For the first road, `a=3`, `b=4`, so its period is `7`. Sam starts at time `0`, where the remainder is `0`, and the road can be crossed immediately.

| Popped city | Current time | Edge | Remainder | Action | New arrival |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | `1 -> 2` | `0 mod 7 = 0` | Cross immediately | `1` |
| 2 | 1 | `2 -> 3` | `1 mod 5 = 1` | Cross immediately | `3` |
| 3 | 3 | destination |  | Stop | `3` |

This direct trace appears to give `3`, but it exposes a crucial detail in the interpretation of the intervals. The rain intervals are `[a+k(a+b), (k+1)(a+b)]`, so the dry interval is `[k(a+b), a+k(a+b)]`. For the second road, `a=2`, `b=3`, `d=2`, so starting at time `1` and finishing at time `3` is not valid because rain starts at time `2`. Sam must wait until time `5`, then cross and arrive at `7`.

The correct trace is consequently:

| Popped city | Current time | Edge | Remainder | Action | New arrival |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | `1 -> 2` | `0` | Cross immediately | `1` |
| 2 | 1 | `2 -> 3` | `1` | Wait until `5` | `7` |
| 3 | 7 | destination |  | Stop | `7` |

The answer is `7`, matching the sample. The example demonstrates why checking only whether the road is currently dry is insufficient. The entire traversal must fit inside the remaining dry portion.

For a second example, consider a road whose traversal exactly fills the dry interval:

```
2 1 1 2
1 2 3 5 3
```

Here the period is `8`, the road is dry from `0` through `3`, and crossing takes exactly `3`.

| Popped city | Current time | Remainder | Condition | Arrival |
| --- | --- | --- | --- | --- |
| 1 | 0 | `0` | `0 <= 3-3` | `3` |
| 2 | 3 | destination |  | `3` |

The result is `3`. The equality in `rem <= a-d` is what permits arrival exactly when rain starts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n+m) log n)` | Each usable edge is relaxed from each endpoint, and heap operations take logarithmic time |
| Space | `O(n+m)` | The graph, distance array, and priority queue require linear space |

With `100000` cities and `200000` roads, the algorithm performs only a logarithmic number of heap operations per relaxation rather than repeatedly scanning the entire graph. The graph itself is linear in the input size, so this fits the intended scale of the constraints.

## Test Cases

```python
# The implementation under test is the solve() function from the solution above.
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n, m, s, t = map(int, input().split())
    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v, a, b, d = map(int, input().split())
        if d <= a:
            graph[u].append((v, a, b, d))
            graph[v].append((u, a, b, d))

    INF = 10**30
    dist = [INF] * (n + 1)
    dist[s] = 0
    pq = [(0, s)]

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        if u == t:
            print(cur)
            return

        for v, a, b, d in graph[u]:
            period = a + b
            rem = cur % period

            if rem <= a - d:
                nd = cur + d
            else:
                nd = cur - rem + period + d

            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    print(-1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""\
3 2 1 3
1 2 3 4 1
2 3 2 3 2
""") == "7", "sample 1"

# Minimum-size graph, source equals destination.
assert run("""\
1 0 1 1
""") == "0", "source equals destination"

# Road is impossible because d > a.
assert run("""\
2 1 1 2
1 2 3 5 4
""") == "-1", "traversal longer than dry interval"

# Traversal ends exactly when rain begins.
assert run("""\
2 1 1 2
1 2 3 5 3
""") == "3", "exact dry-interval boundary"

# Arrive during rain and wait for the next dry interval.
assert run("""\
3 2 1 3
1 2 1 2 1
2 3 2 3 2
""") == "6", "waiting for next dry interval"

# Large values, checking that integer arithmetic does not overflow.
assert run("""\
3 2 1 3
1 2 1000000000 1000000000 1000000000
2 3 1000000000 1000000000 1000000000
""") == "2000000000", "large values"

# Maximum-size vertex count with no edges.
# This exercises memory handling and the unreachable case.
n = 100000
max_input = f"{n} 0 1 {n}\n"
assert run(max_input) == "-1", "maximum number of vertices"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `7` | Waiting for a later dry interval |
| `1 0 1 1` | `0` | Source and destination are the same |
| One road with `d > a` | `-1` | Permanently unusable road |
| One road with `d = a` | `3` | Exact dry-interval boundary |
| Two roads requiring a wait | `6` | Correct modulo and waiting calculation |
| Large `a`, `b`, and `d` | `2000000000` | Large integer arithmetic |
| `100000` vertices and no edges | `-1` | Maximum graph size and unreachable destination |

## Edge Cases

The first edge case is an unusable road. For

```
2 1 1 2
1 2 3 5 4
```

every dry interval has length `3`, but crossing requires `4` time units. The preprocessing condition `d <= a` fails, so the edge is omitted from the adjacency lists. The priority queue contains only city `1`, and city `2` is never reached. The algorithm prints `-1`.

The second edge case is equality at the start or end of rain. For

```
2 1 1 2
1 2 3 5 3
```

the initial remainder is `0` and `a-d` is also `0`. The condition `rem <= a-d` succeeds, so Sam enters at time `0` and reaches the destination at time `3`. The answer is `3`. Using a strict inequality would incorrectly reject this path.

The third edge case is arriving in the rainy portion of a period. Consider

```
3 2 1 3
1 2 1 2 1
2 3 2 3 2
```

The first road has period `3` and dry interval length `1`. Sam crosses it from time `0` to time `1`. For the second road, the period is `5` and its dry interval is `[0,2]`. Arrival at time `1` leaves exactly one unit of dry time, but the crossing needs `2`, so `rem=1 > a-d=0`. The algorithm waits until the next period begins at time `5`, crosses until time `7`, and reaches the destination at `7`.

The fourth edge case is the beginning of a new period. Suppose a road has `a=3`, `b=5`, and `d=2`, and Sam arrives at time `8`. Its period is `8`, so `8 % 8 = 0`. The algorithm recognizes that `0 <= 3-2` and permits immediate departure. This matters because the endpoint of a rainy interval is also the beginning of the next dry interval.

The last edge case is an unreachable destination. With

```
3 1 1 3
1 2 1 1 1
```

city `3` has no incident road. Dijkstra explores the component containing city `1`, then the heap becomes empty without extracting city `3`. The algorithm prints `-1`, rather than confusing a very large waiting time with actual reachability.
