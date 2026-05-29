---
title: "CF 229B - Planets"
description: "We are given an undirected weighted graph of planets connected by stargates. Jack starts on planet 1 at time 0 and wants to reach planet n as early as possible. Moving through a stargate takes a fixed positive amount of time. The unusual part is the waiting rule."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 229
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 142 (Div. 1)"
rating: 1700
weight: 229
solve_time_s: 97
verified: true
draft: false
---

[CF 229B - Planets](https://codeforces.com/problemset/problem/229/B)

**Rating:** 1700  
**Tags:** binary search, data structures, graphs, shortest paths  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph of planets connected by stargates. Jack starts on planet `1` at time `0` and wants to reach planet `n` as early as possible.

Moving through a stargate takes a fixed positive amount of time. The unusual part is the waiting rule. Every planet has a set of blocked moments. If Jack is standing on a planet at time `t`, and `t` belongs to that planet’s blocked set, he is forbidden from leaving immediately. He must wait until the first time that is not blocked.

The restriction only applies when departing from a planet. Arriving at a blocked moment is allowed. The problem asks for the minimum arrival time at planet `n`, or `-1` if no route exists.

The graph has up to `10^5` vertices and `10^5` edges, so any algorithm worse than roughly `O((n + m) log n)` is risky in Python. A standard all-pairs shortest path algorithm is impossible here. Even `O(nm)` would mean around `10^10` operations.

The total number of blocked times across all planets is also bounded by `10^5`. That detail matters because it means we can preprocess or search inside these lists efficiently.

Several edge cases are easy to mishandle.

One subtle case happens at the starting planet. Jack starts at time `0`, but if planet `1` is blocked at time `0`, he cannot leave immediately.

Example:

```
2 1
1 2 5
1 0
0
```

The correct answer is `6`, not `5`, because Jack must wait one second before departing.

Another tricky situation is consecutive blocked times.

```
2 1
1 2 3
3 0 1 2
0
```

Jack starts at time `0`, but times `0`, `1`, and `2` are all blocked on planet `1`. He can only leave at time `3`, so the answer is `6`.

A careless implementation that checks only one blocked moment would incorrectly produce `4`.

Disconnected graphs are another source of mistakes.

```
3 1
1 2 5
0
0
0
```

Planet `3` is unreachable, so the answer must be `-1`.

Finally, arriving at a blocked time is completely legal. The restriction applies only when attempting to depart.

```
2 1
1 2 3
0
1 3
```

The answer is still `3`. Jack reaches planet `2` exactly when another traveler arrives there, but that does not matter because the journey ends.

## Approaches

The brute-force idea is straightforward. Treat every state as `(planet, current_time)`. From a state, either wait one second or traverse an edge if the current time is not blocked.

This works because all transitions are modeled explicitly. The problem is the size of the time dimension. Edge weights can accumulate far beyond `10^9`, and exploring all intermediate times is impossible.

A more refined brute-force approach would still use Dijkstra’s algorithm, but whenever we reach a planet at time `t`, we repeatedly increment `t` while it remains blocked.

That is already much better, because we no longer model every second globally. The remaining issue is efficiency. Suppose a planet has blocked times:

```
0 1 2 3 4 ... 100000
```

If many shortest-path relaxations repeatedly scan these values one by one, the total complexity can become quadratic.

The key observation is that waiting behavior is deterministic. Once we know the arrival time `t` at a planet, there is exactly one earliest valid departure time. Since blocked moments are sorted, we can jump directly to that departure time instead of incrementing blindly.

This turns the problem back into a standard shortest-path problem with modified edge relaxation.

For every planet `u`, define:

```
next_free(u, t)
```

as the earliest time `>= t` that is not blocked on `u`.

Then every edge relaxation becomes:

```
departure = next_free(u, dist[u])
arrival = departure + weight
```

The graph still has nonnegative edge costs, so Dijkstra remains valid.

To compute `next_free` efficiently, we store each blocked list in a hash set for `O(1)` membership tests. Since every blocked moment is visited at most once across all increments, the total work remains linear in the total blocked count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over time states | Impossible | Impossible | Too slow |
| Dijkstra with naive waiting scans | Potentially O(K²) | O(n + m + K) | Too slow |
| Optimized Dijkstra | O((n + m) log n + K) | O(n + m + K) | Accepted |

Here `K` is the total number of blocked moments.

## Algorithm Walkthrough

1. Build an adjacency list for the graph.

Each edge stores the neighboring planet and the travel time.
2. Store the blocked moments for every planet in a hash set.

Fast membership testing is crucial because we repeatedly ask whether a given time is blocked.
3. Precompute the earliest valid departure time for every blocked moment.

Suppose a planet has blocked moments:

```
3 4 5 8 9
```

If Jack arrives at time `3`, he must actually wait until `6`.

If he arrives at `4`, the answer is still `6`.

We preprocess this efficiently by scanning each blocked list backward.
4. Run Dijkstra’s algorithm from planet `1`.

The priority queue stores `(current_time, node)`.
5. When processing a node `u` at time `t`, determine the real departure time.

If `t` is not blocked, departure time stays `t`.

Otherwise, jump directly to the first non-blocked time after the consecutive blocked segment.
6. Relax all outgoing edges.

For an edge `(u, v, w)`:

```
new_time = departure_time + w
```

If this improves `dist[v]`, push the new state into the heap.
7. After Dijkstra finishes, print `dist[n]`.

If it remains infinite, print `-1`.

### Why it works

Dijkstra’s algorithm relies on one property: once a node is extracted with minimum distance, no shorter route to it can exist later.

The waiting rule does not violate this property because waiting only increases time, never decreases it. Every edge traversal effectively has a nonnegative dynamic cost:

```
effective_cost = waiting_time + edge_weight
```

The preprocessing step guarantees that for every arrival time, we compute the exact earliest legal departure time. Since every relaxation uses the true minimum departure, all candidate paths are evaluated correctly.

Because all effective transition costs are nonnegative, the standard Dijkstra correctness proof still applies.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b, c = map(int, input().split())
        graph[a].append((b, c))
        graph[b].append((a, c))

    nxt = [{} for _ in range(n + 1)]

    for i in range(1, n + 1):
        arr = list(map(int, input().split()))

        k = arr[0]
        times = arr[1:]

        if k == 0:
            continue

        jump = {}

        last = times[-1]
        jump[last] = last + 1

        for j in range(k - 2, -1, -1):
            cur = times[j]
            nxt_time = times[j + 1]

            if nxt_time == cur + 1:
                jump[cur] = jump[nxt_time]
            else:
                jump[cur] = cur + 1

        nxt[i] = jump

    dist = [INF] * (n + 1)
    dist[1] = 0

    pq = [(0, 1)]

    while pq:
        t, u = heapq.heappop(pq)

        if t != dist[u]:
            continue

        depart = nxt[u].get(t, t)

        for v, w in graph[u]:
            nt = depart + w

            if nt < dist[v]:
                dist[v] = nt
                heapq.heappush(pq, (nt, v))

    print(-1 if dist[n] == INF else dist[n])

solve()
```

The adjacency list is standard Dijkstra infrastructure. Since the graph is sparse, this representation keeps memory and iteration efficient.

The preprocessing step is the core trick. For every blocked time `t`, we store the first valid time strictly after the consecutive blocked segment containing `t`.

For example:

```
blocked = [3, 4, 5, 8]
```

becomes:

```
3 -> 6
4 -> 6
5 -> 6
8 -> 9
```

This lets the algorithm compute waiting time in constant expected time.

The backward scan matters. When processing `4`, we already know the answer for `5`. If `5` is consecutive, then `4` inherits the same final escape time.

Inside Dijkstra, the line:

```
depart = nxt[u].get(t, t)
```

means:

```
If t is blocked, jump forward.
Otherwise leave immediately.
```

A common mistake is recomputing waits after traversing an edge. The waiting rule applies before leaving a planet, not after arriving.

Another subtle point is stale heap entries. Dijkstra may push multiple versions of the same node into the priority queue. The check:

```
if t != dist[u]:
    continue
```

discards outdated states safely.

Python integers are arbitrary precision, so large path sums are not an overflow concern.

## Worked Examples

### Sample 1

Input:

```
4 6
1 2 2
1 3 3
1 4 8
2 3 4
2 4 5
3 4 3
0
1 3
2 3 4
0
```

Blocked moments:

```
Planet 1: none
Planet 2: {3}
Planet 3: {3, 4}
Planet 4: none
```

Preprocessed jumps:

```
Planet 2: 3 -> 4
Planet 3: 3 -> 5, 4 -> 5
```

| Step | Heap Pop | Departure Time | Relaxed Edge | New Distance |
| --- | --- | --- | --- | --- |
| 1 | (0,1) | 0 | 1→2 | 2 |
| 1 | (0,1) | 0 | 1→3 | 3 |
| 1 | (0,1) | 0 | 1→4 | 8 |
| 2 | (2,2) | 2 | 2→4 | 7 |
| 3 | (3,3) | 5 | 3→4 | 8 |
| 4 | (7,4) | 7 | none | final |

The shortest route is:

```
1 → 2 → 4
```

with total time `7`.

The trace demonstrates why waiting must be applied before leaving a node. Reaching planet `3` at time `3` forces Jack to wait until `5`.

### Disconnected Example

Input:

```
3 1
1 2 5
0
0
0
```

| Step | Heap Pop | Departure Time | Relaxed Edge | New Distance |
| --- | --- | --- | --- | --- |
| 1 | (0,1) | 0 | 1→2 | 5 |
| 2 | (5,2) | 5 | none useful | none |

Planet `3` is never reached.

Final answer:

```
-1
```

This confirms that the algorithm handles disconnected components naturally through the distance array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n + K) | Dijkstra dominates, preprocessing scans blocked times once |
| Space | O(n + m + K) | Graph, heap, distance array, blocked-time maps |

`n`, `m`, and the total blocked count `K` are all at most `10^5`, so the algorithm comfortably fits within the limits. The heap operations are logarithmic, and every blocked time participates in preprocessing exactly once.

## Test Cases

```python
import sys
import io
import heapq

INF = 10**30

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b, c = map(int, input().split())
        graph[a].append((b, c))
        graph[b].append((a, c))

    nxt = [{} for _ in range(n + 1)]

    for i in range(1, n + 1):
        arr = list(map(int, input().split()))

        k = arr[0]
        times = arr[1:]

        jump = {}

        if k:
            jump[times[-1]] = times[-1] + 1

            for j in range(k - 2, -1, -1):
                cur = times[j]

                if times[j + 1] == cur + 1:
                    jump[cur] = jump[times[j + 1]]
                else:
                    jump[cur] = cur + 1

        nxt[i] = jump

    dist = [INF] * (n + 1)
    dist[1] = 0

    pq = [(0, 1)]

    while pq:
        t, u = heapq.heappop(pq)

        if t != dist[u]:
            continue

        depart = nxt[u].get(t, t)

        for v, w in graph[u]:
            nt = depart + w

            if nt < dist[v]:
                dist[v] = nt
                heapq.heappush(pq, (nt, v))

    return str(-1 if dist[n] == INF else dist[n])

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""4 6
1 2 2
1 3 3
1 4 8
2 3 4
2 4 5
3 4 3
0
1 3
2 3 4
0
"""
) == "7"

# disconnected graph
assert run(
"""3 1
1 2 5
0
0
0
"""
) == "-1"

# starting node blocked at time 0
assert run(
"""2 1
1 2 5
1 0
0
"""
) == "6"

# consecutive waiting times
assert run(
"""2 1
1 2 3
3 0 1 2
0
"""
) == "6"

# arrival at blocked destination is allowed
assert run(
"""2 1
1 2 3
0
1 3
"""
) == "3"

print("ok")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Starting node blocked at time 0 | 6 | Waiting applies immediately at the source |
| Consecutive blocked moments | 6 | Waiting must continue through an entire blocked segment |
| Disconnected graph | -1 | Unreachable target handling |
| Blocked destination on arrival | 3 | Arrival is allowed even if the time is blocked |

## Edge Cases

Consider the case where the starting planet is blocked immediately.

```
2 1
1 2 5
1 0
0
```

The preprocessing stores:

```
0 -> 1
```

Dijkstra starts from `(0,1)`. Since time `0` is blocked, the algorithm jumps to departure time `1`. Traversing the edge takes `5` more seconds, so the final answer becomes `6`.

Now examine consecutive blocked times.

```
2 1
1 2 3
3 0 1 2
0
```

The preprocessing produces:

```
0 -> 3
1 -> 3
2 -> 3
```

When Dijkstra processes planet `1` at time `0`, it immediately jumps to departure time `3`. The arrival time at planet `2` becomes `6`.

A naive implementation that increments once would incorrectly depart at time `1`, which is still forbidden.

Finally, consider a blocked arrival at the destination.

```
2 1
1 2 3
0
1 3
```

Jack reaches planet `2` at time `3`. The algorithm never checks waiting rules after arrival unless another edge traversal is attempted. Since planet `2` is the destination, the answer remains `3`.

This matches the problem statement exactly.
