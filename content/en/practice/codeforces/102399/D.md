---
title: "CF 102399D - \u0414\u043e\u0440\u043e\u0433\u0438 \u0432 \u0441\u0442\u0440\u0430\u043d\u0435"
description: "We have a directed weighted graph of cities. City 1 is the capital, and every directed road u - v has a capacity w, meaning a cargo of weight at most w can traverse that road. For a fixed city s, a route from s to the capital can use several roads."
date: "2026-08-11T23:35:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "D"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 185
verified: true
draft: false
---

[CF 102399D - \u0414\u043e\u0440\u043e\u0433\u0438 \u0432 \u0441\u0442\u0440\u0430\u043d\u0435](https://codeforces.com/problemset/problem/102399/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed weighted graph of cities. City `1` is the capital, and every directed road `u -> v` has a capacity `w`, meaning a cargo of weight at most `w` can traverse that road.

For a fixed city `s`, a route from `s` to the capital can use several roads. The same cargo must survive every road on the route, so the maximum cargo weight supported by that particular route is the minimum edge capacity along it. We need the best possible route, so the answer for `s` is the maximum, over all routes from `s` to `1`, of the minimum edge capacity on that route. If there is no route to the capital, the answer is `-1`.

The official limits are `n <= 10^5` and `m <= 10^6`, with a 2 second time limit and 512 MB memory limit. The number of roads is large enough that an algorithm doing anything close to `O(nm)` is out of the question. Even `O(n^2)` is too large when `n` reaches `10^5`. We need to process the graph in roughly linear or `m log n` time. The edge capacities are at most `10^9`, so Python integers handle them directly without overflow concerns.

The direction of the roads creates the first common trap. We are asking about paths ending at city `1`, not paths starting there. For example:

```
2 1
2 1 5
```

The answer is `5`. If we accidentally run an ordinary search from city `1` over the original graph, city `2` is unreachable because the only road points toward `1`.

A second trap is taking the largest edge on a route instead of the smallest one. Consider:

```
3 2
3 2 10
2 1 3
```

The answer is:

```
3
```

The road of capacity `10` does not help beyond the capacity `3` road. A route's capacity is its bottleneck.

A third trap is accepting the first path found. Consider:

```
4 4
2 1 2
2 3 8
3 4 7
4 1 7
```

The answer for city `2` is:

```
7
7
-1
```

A DFS that immediately takes `2 -> 1` would record `2`, although `2 -> 3 -> 4 -> 1` supports weight `7`. The problem asks for the best path, not merely any reachable path.

Finally, unreachable cities must remain `-1`. For example:

```
3 1
2 1 4
```

The output is:

```
4
-1
```

A careless initialization such as `answer[v] = 0` could make an unreachable city look as though a zero-weight shipment were possible, even though the required answer is explicitly `-1`.

## Approaches

The direct brute-force solution is to enumerate paths from every city to the capital. For each path, calculate its bottleneck by taking the minimum edge capacity, then keep the largest bottleneck seen for that starting city. This is correct because every possible route is examined.

The problem is the number of paths. In a complete directed graph, a DFS that enumerates simple paths from one source can encounter

`P(n-1,1) + P(n-1,2) + ... + P(n-1,n-1)`

different paths, where `P(a,b) = a! / (a-b)!`. Across all starting cities this is on the order of `n!`, far beyond what can be processed for `n = 10^5`. Cycles make careless path enumeration even worse unless visited-state handling is added.

The brute-force works because the answer is defined by a path's minimum edge capacity, but it fails because it treats every possible path separately. The useful observation is that the value of a path can be summarized by a single number, its bottleneck. Once we know the best bottleneck already achievable from a city to the capital, extending a path by one more road only changes that value through a minimum operation.

There is also a direction issue. Since every answer describes a route toward city `1`, reverse every road. An original road `u -> v` of capacity `w` becomes a reversed edge `v -> u` with the same capacity. Now a route from the capital to `u` in the reversed graph corresponds exactly to a route from `u` to the capital in the original graph.

This transforms the problem into a maximum-bottleneck path problem starting at city `1`. We can solve it with a Dijkstra-style greedy algorithm. Instead of choosing the smallest tentative distance, we repeatedly choose the unprocessed city with the largest currently known bottleneck. If the current city has value `best[v]` and a reversed edge `v -> u` has capacity `w`, then reaching `u` through `v` supports

`min(best[v], w)`.

If that value improves `best[u]`, we push the new value into a max-heap. The same greedy ordering that makes Dijkstra work is valid here because every extension applies `min`, which can never increase the value of an already known path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential, `O(n!)` in dense graphs | `O(n + m)` plus recursion/path state | Too slow |
| Optimal | `O((n + m) log n)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Build the reversed graph. For every original road `u -> v` with capacity `w`, store an edge `v -> u` with the same capacity. This makes moving away from city `1` in the new graph equivalent to moving toward city `1` in the original graph.
2. Create `best[v]`, the largest bottleneck capacity currently known for reaching city `v` from city `1` in the reversed graph. Set `best[1]` to infinity because no road has been used yet, and set every other value to `-1` because those cities have not been reached.
3. Put `(infinity, 1)` into a max-priority queue. Python's `heapq` is a min-heap, so store the capacity as its negative and use `(-capacity, vertex)`.
4. Remove the city with the largest known bottleneck from the heap. If the heap entry is stale because `best[v]` has since become larger, discard it. This is the same lazy-deletion technique commonly used with Dijkstra's algorithm.
5. For every reversed edge `v -> u` with capacity `w`, calculate the bottleneck obtained by reaching `v` and then crossing this edge:

```
candidate = min(best[v], w)
```

If `candidate > best[u]`, update `best[u]` and push the new value into the heap. The minimum is necessary because a cargo must satisfy both the already traversed part and the new road.

1. Continue until the heap is empty. At that point every city reachable from the capital in the reversed graph has its maximum possible bottleneck. Every city still equal to `-1` cannot reach the capital in the original graph.
2. Output `best[2]`, `best[3]`, ..., `best[n]`. City `1` itself is not requested.

### Why it works

The invariant is that whenever a city `v` is extracted with the largest current bottleneck, its value is already optimal. Suppose there were a better path to `v`. Consider the first vertex on that better path that had not yet been extracted. Its predecessor on the same path must already have been extracted, because the capital was extracted first and the path progresses outward in the reversed graph. When that predecessor was processed, the algorithm would have inserted a candidate for the next vertex equal to the bottleneck of the better path's prefix. That candidate is at least the bottleneck claimed for `v`. Since the queue always extracts the largest candidate first, `v` could not have been extracted with a smaller value. Thus every finalized value is optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    # rev[v] contains (u, w) for every original edge u -> v with weight w.
    rev = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        rev[v].append((u, w))

    best = [-1] * n
    best[0] = 10**18

    # Python has a min-heap, so store negative bottlenecks.
    pq = [(-best[0], 0)]

    while pq:
        neg_value, v = heapq.heappop(pq)
        value = -neg_value

        # Ignore an outdated heap entry.
        if value != best[v]:
            continue

        for u, w in rev[v]:
            candidate = min(value, w)

            if candidate > best[u]:
                best[u] = candidate
                heapq.heappush(pq, (-candidate, u))

    sys.stdout.write("\n".join(map(str, best[1:])))

if __name__ == "__main__":
    solve()
```

The input loop converts each road into a reversed adjacency entry. If the original road is `u -> v`, reaching `v` in the reversed graph lets us move to `u`, so storing it in `rev[v]` is exactly the required transformation.

`best[0]` is initialized to `10**18`, which is safely larger than every possible edge capacity. It could also be initialized to a symbolic infinity, but using an integer keeps the bottleneck calculation simple. The first transition then becomes `min(10**18, w) = w`.

The priority queue contains negative values because `heapq` implements a min-heap. The vertex with the largest actual bottleneck consequently has the smallest stored negative number and is extracted first.

A vertex may enter the heap several times. For example, it might first be reached with capacity `3` and later improved to `7`. Rather than searching the heap to delete the old entry, the code leaves it there. When the old `(3, v)` entry is popped, `value != best[v]`, so it is ignored. This keeps the implementation simple and preserves the expected `O((n+m) log n)` bound.

The comparison is `candidate > best[u]`, not `>=`. Equal values do not improve anything, and avoiding duplicate equal heap entries is useful on graphs with many roads of identical capacity.

There are no one-based indexing operations inside the graph algorithm. Cities are converted from `1..n` to `0..n-1` immediately, so city `1` is vertex `0`. The final slice `best[1:]` removes exactly the capital from the output.

Python integers do not overflow, and all capacities are positive and at most `10^9`. The extra `10**18` sentinel is only used for the capital and never appears in the output.

## Worked Examples

### Sample 1

The original roads form the cycle

```
1 -> 2 -> 3 -> 4 -> 1
```

with capacities `3, 6, 2, 1`. Reversing them gives

```
1 -> 4 -> 3 -> 2 -> 1
```

The relevant queue and `best` states are:

| Extracted city | Extracted value | Relaxed city | Edge capacity | Candidate | Updated `best` |
| --- | --- | --- | --- | --- | --- |
| 1 | `∞` | 4 | 1 | 1 | `best[4] = 1` |
| 4 | 1 | 3 | 2 | 1 | `best[3] = 1` |
| 3 | 1 | 2 | 6 | 1 | `best[2] = 1` |
| 2 | 1 | 1 | 3 | 1 | unchanged |

The first road leaving the capital in the reversed graph has capacity `1`, so every further city on this route inherits bottleneck `1`. The resulting answers are `1, 1, 1`, matching the sample.

### Sample 2

The original roads include `2 -> 3` with capacity `3`, `3 -> 1` with capacity `7`, `2 -> 1` with capacity `2`, `2 -> 4` with capacity `9`, and `4 -> 1` with capacity `1`.

After reversal, city `1` can reach `3` with capacity `7`, `2` with capacity `2`, and `4` with capacity `1`.

| Extracted city | Extracted value | Relaxed city | Edge capacity | Candidate | Updated `best` |
| --- | --- | --- | --- | --- | --- |
| 1 | `∞` | 3 | 7 | 7 | `best[3] = 7` |
| 1 | `∞` | 2 | 2 | 2 | `best[2] = 2` |
| 1 | `∞` | 4 | 1 | 1 | `best[4] = 1` |
| 3 | 7 | 2 | 3 | 3 | `best[2] = 3` |
| 2 | 3 | no improvement |  |  | unchanged |
| 4 | 1 | no improvement |  |  | unchanged |

The crucial update is city `2`. Its direct route to the capital has capacity `2`, but the reversed route `1 -> 3 -> 2` has bottleneck `min(7, 3) = 3`. The maximum-heap extracts city `3` before city `2`, allowing this better route to be discovered. The final output is `3, 7, 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m) log n)` | Each successful relaxation inserts a heap entry, and each edge is inspected once from its reversed adjacency list. |
| Space | `O(n + m)` | The reversed graph stores all `m` roads, while `best` and the heap use `O(n + m)` additional space in the worst case. |

With `n = 10^5` and `m = 10^6`, the algorithm performs a linear scan over the roads plus heap operations, rather than enumerating paths. This is the right scale for the given limits of 2 seconds and 512 MB.

## Test Cases

The following test harness uses the same algorithm in a callable `solve()` function. The large generated case has the maximum allowed number of cities and roads, so it also checks that the implementation handles the upper input scale.

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    rev = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        rev[v].append((u, w))

    best = [-1] * n
    best[0] = 10**18

    pq = [(-best[0], 0)]

    while pq:
        neg_value, v = heapq.heappop(pq)
        value = -neg_value

        if value != best[v]:
            continue

        for u, w in rev[v]:
            candidate = min(value, w)
            if candidate > best[u]:
                best[u] = candidate
                heapq.heappush(pq, (-candidate, u))

    sys.stdout.write("\n".join(map(str, best[1:])))

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

# Sample 1
assert run(
    """4 4
1 2 3
2 3 6
3 4 2
4 1 1
"""
) == "1\n1\n1", "sample 1"

# Sample 2
assert run(
    """4 5
2 3 3
3 1 7
2 1 2
2 4 9
4 1 1
"""
) == "3\n7\n1", "sample 2"

# Sample 3
assert run(
    """3 2
2 1 2
1 3 2
"""
) == "2\n-1", "sample 3"

# Minimum-size graph, direct road only.
assert run(
    """2 1
2 1 1000000000
"""
) == "1000000000", "minimum size and maximum weight"

# All capacities equal, including a longer route.
assert run(
    """5 5
2 3 7
3 4 7
4 1 7
5 4 7
2 1 7
"""
) == "7\n7\n7\n7", "all equal capacities"

# Boundary case with a tempting direct route that is worse.
assert run(
    """4 4
2 1 2
2 3 8
3 4 7
4 1 7
"""
) == "7\n7\n7", "better indirect bottleneck"

# Maximum n and maximum m.
# The first 1000 cities form a complete directed graph with weight 5:
# 1000 * 999 = 999000 edges.
# Another 1000 edges connect cities 1001..2000 to the reachable component.
# The remaining cities are unreachable.
n = 100000
parts = [f"{n} 1000000"]

for u in range(1, 1001):
    for v in range(1, 1001):
        if u != v:
            parts.append(f"{u} {v} 5")

for u in range(1001, 2001):
    parts.append(f"{u} {u - 1} 5")

large_input = "\n".join(parts) + "\n"
large_output = run(large_input)

expected_large = "\n".join(
    ["5"] * 1999 + ["-1"] * (n - 2000)
)

assert large_output == expected_large, "maximum-size graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, one road of capacity `10^9` | `1000000000` | Minimum graph size and maximum edge capacity |
| Five cities with every useful road having capacity `7` | Four lines containing `7` | Equal capacities and longer routes |
| City `2` has a direct capacity `2` route and an indirect capacity `7` route | `7`, `7`, `7` | Choosing the maximum bottleneck rather than the first path |
| `n = 100000`, `m = 1000000` | `5` for cities `2..2000`, then `-1` | Maximum input scale, dense graph, and unreachable vertices |

## Edge Cases

The first edge case is reversed direction. For

```
2 1
2 1 5
```

the reversed graph contains `1 -> 2` with capacity `5`. The algorithm starts at city `1`, relaxes city `2` with `min(infinity, 5) = 5`, and outputs `5`. Searching the original graph from city `1` would fail, which is exactly why the reversal is necessary.

The second edge case is the bottleneck calculation. For

```
3 2
3 2 10
2 1 3
```

the reversed graph contains `1 -> 2` with capacity `3` and `2 -> 3` with capacity `10`. City `2` gets value `3`, then city `3` receives `min(3, 10) = 3`. The output is `3`, even though one road can carry `10`.

The third edge case is competing routes. For

```
4 4
2 1 2
2 3 8
3 4 7
4 1 7
```

the reversed graph starts with candidates `2` for city `2` and `7` for city `4`. City `4` is extracted first because `7 > 2`. Its edge to city `3` has capacity `7`, so city `3` receives `7`. Processing city `3` then gives city `2` the candidate `min(7, 8) = 7`, replacing its previous value `2`. The final result is `7, 7, 7`.

The fourth edge case is an unreachable vertex:

```
3 1
2 1 4
```

After reversal, only city `2` is reachable from city `1`. The heap never discovers city `3`, so `best[3]` stays `-1`. The output is `4` followed by `-1`. This is why `-1` is a useful initial state rather than `0`.
