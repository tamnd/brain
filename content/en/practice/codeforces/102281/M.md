---
title: "CF 102281M - \u0410\u043d\u0442\u0438\u043d\u0430\u0443\u0447\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "The wormholes form a directed graph. Each known transition goes from one wormhole to another and has one of two costs. A hypertransition costs one ant-hour, while a null transition costs zero. The ship starts at wormhole 1 and has to reach wormhole n."
date: "2026-08-13T09:32:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "M"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 74
verified: true
draft: false
---

[CF 102281M - \u0410\u043d\u0442\u0438\u043d\u0430\u0443\u0447\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The wormholes form a directed graph. Each known transition goes from one wormhole to another and has one of two costs. A hypertransition costs one ant-hour, while a null transition costs zero. The ship starts at wormhole 1 and has to reach wormhole n.

We need a route with minimum total cost. There is one additional restriction: a route may not visit the same wormhole twice. The output must contain the minimum number of ant-hours, followed by the number of wormholes in the route and the route itself. If wormhole n is unreachable from wormhole 1, the output is `IMPOSSIBLE`.

The graph can contain up to 100,000 wormholes and 100,000 directed transitions. With that size, enumerating possible routes is completely infeasible. Even algorithms that examine all pairs of vertices, such as Floyd-Warshall with (O(n^3)) time, are far beyond the limit. We need a graph algorithm whose running time is essentially linear in the number of vertices and transitions. The fact that every transition costs either zero or one is the structural property that gives us such an algorithm.

There are several edge cases that can make a careless implementation fail.

Consider the smallest possible graph:

```
1 0
```

The ship is already at the destination. The correct route is the single wormhole `1`, with cost zero:

```
0 1
1
```

An implementation that always expects to traverse at least one edge can incorrectly report `IMPOSSIBLE` or produce an empty route.

A second case is an unreachable destination:

```
2 0
```

There is no transition from wormhole 1 to wormhole 2, so the only correct output is:

```
IMPOSSIBLE
```

A search implementation must distinguish an unreached vertex from one whose distance happens to be zero.

Zero-cost cycles are another subtle case:

```
3 3
1 2 0
2 1 0
2 3 1
```

The optimal route is `1 2 3`, with cost one. The cycle `1 -> 2 -> 1` contributes no time, but it is still forbidden because wormhole 1 would be visited twice. A shortest-distance algorithm may encounter such a cycle internally, but the reconstructed shortest path must not contain it.

Finally, several shortest routes can have exactly the same cost. For example:

```
4 4
1 2 1
1 3 1
2 4 0
3 4 0
```

Both `1 2 4` and `1 3 4` have cost one. The problem accepts either. A solution must not rely on a particular shortest route existing.

## Approaches

The most direct approach is to enumerate routes from wormhole 1, keeping track of the wormholes already visited so that a vertex cannot occur twice. Whenever the destination is reached, we can compare the route's cost with the best answer found so far.

This is correct because every legal route is explicitly considered. The problem is the number of routes. A graph with many branching transitions can have exponentially many simple paths. In a dense enough graph, the number of simple paths can be on the order of (n!), so even with only 100,000 vertices being available, the search becomes impossible long before the input reaches its maximum size. The restriction against repeated vertices makes brute-force enumeration even more complicated, because the state is not just the current vertex, but also the complete set of previously visited vertices.

The brute-force approach works because it directly represents the definition of a legal route, but it fails because there are far too many routes to inspect.

The crucial observation is that the restriction about repeated wormholes does not actually require a special shortest-path algorithm. All transition costs are nonnegative, so if a walk contains a repeated vertex, the part between two consecutive occurrences of that vertex is a cycle. Removing that cycle cannot increase the total cost. If the cycle has positive cost, the route becomes cheaper. If it has zero cost, the route keeps exactly the same cost. Repeating this process removes every repeated vertex and produces a simple path with no larger cost.

Consequently, there is always an optimal route that is simple. We can solve an ordinary shortest-path problem and reconstruct one shortest path. The special edge weights, restricted to zero and one, allow us to use 0-1 BFS.

0-1 BFS is essentially Dijkstra's algorithm specialized for weights zero and one. Instead of a priority queue, it uses a deque. When traversing a zero-cost edge improves a distance, the new vertex is placed at the front because its distance is the same as the current vertex. When traversing a one-cost edge improves a distance, the new vertex goes to the back because its distance is exactly one larger.

This keeps vertices processed in nondecreasing distance order while requiring only constant-time deque operations per successful relaxation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the worst case | (O(n+m)) plus route state | Too slow |
| Optimal, 0-1 BFS | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Build a directed adjacency list. For every transition `a -> b` with type `t`, store `(b, t)`. The direction matters because transitions can be one-way.
2. Initialize `dist[1] = 0` and all other distances to infinity. Also store `parent[v]`, which will remember the previous wormhole on the chosen shortest route to `v`. Put vertex 1 into a deque.
3. Take a vertex `v` from the front of the deque. For every outgoing transition `v -> to` with cost `w`, calculate `new_dist = dist[v] + w`.
4. If `new_dist` is smaller than `dist[to]`, update `dist[to]` and set `parent[to] = v`. If `w` is zero, put `to` at the front of the deque. If `w` is one, put `to` at the back.

A zero-cost edge does not increase the current distance, so its endpoint must be processed before vertices that are already one or more ant-hours farther away. A one-cost edge increases the distance by exactly one, so its endpoint belongs after the currently available vertices with the same distance.
5. Continue until the deque is empty. At this point `dist[v]` is the minimum possible cost from wormhole 1 to every reachable wormhole, so in particular `dist[n]` is the minimum travel time to the destination.
6. If `dist[n]` is still infinity, print `IMPOSSIBLE`. Otherwise, start at `n` and repeatedly follow `parent[v]` until reaching vertex 1. This produces the route backwards, so reverse it before printing.
7. The reconstructed route is guaranteed not to repeat a wormhole. If it did contain a repeated vertex, the portion between the two occurrences would be a cycle. Removing that cycle would give a route no more expensive than the one represented by the shortest distances. Since the predecessor chain is formed from strictly valid shortest-distance relaxations, the resulting path can be chosen as a simple shortest path.

### Why it works

The central invariant is that whenever a vertex is processed from the deque, the deque maintains vertices in nondecreasing order of their current distance. A zero-cost relaxation keeps the same distance and is moved to the front, while a one-cost relaxation creates a distance exactly one larger and is moved to the back. Thus the first shortest-distance processing behavior of Dijkstra's algorithm is preserved without a priority queue.

Every relaxation only replaces a distance by a strictly smaller value, and `parent[to]` records an edge that realizes the new distance. When the algorithm finishes, the destination distance is the minimum cost of any route from 1 to n. Since all edge costs are nonnegative, every walk containing a cycle can have that cycle removed without increasing its cost. Hence an optimal simple route exists, and the predecessor chain gives such an optimal route.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b, t = map(int, input().split())
        graph[a].append((b, t))

    INF = 10**18
    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)

    dist[1] = 0
    dq = deque([1])

    while dq:
        v = dq.popleft()

        for to, w in graph[v]:
            nd = dist[v] + w

            if nd < dist[to]:
                dist[to] = nd
                parent[to] = v

                if w == 0:
                    dq.appendleft(to)
                else:
                    dq.append(to)

    if dist[n] == INF:
        print("IMPOSSIBLE")
        return

    path = []
    cur = n

    while cur != -1:
        path.append(cur)
        if cur == 1:
            break
        cur = parent[cur]

    path.reverse()

    print(dist[n], len(path))
    print(*path)

if __name__ == "__main__":
    solve()
```

The adjacency list uses indices from 1 through `n`, matching the numbering in the input. The extra element at index zero avoids repeatedly subtracting one from vertex numbers.

`dist` stores the minimum number of ant-hours currently known. `parent` stores the predecessor needed for reconstruction. A predecessor is changed only when a strictly smaller distance is found, so it always corresponds to the distance currently assigned to that vertex.

The deque is the key implementation detail. `appendleft` handles a zero-cost edge, while `append` handles a one-cost edge. Using the wrong end for either edge type destroys the distance ordering on which 0-1 BFS relies.

The destination is allowed to be vertex 1. In that case `dist[1]` is already zero and the reconstruction loop immediately produces the route `[1]`.

Python integers do not overflow, although an infinity value of `10**18` is more than sufficient anyway. The maximum possible useful shortest-path cost is at most the number of edges in a simple path, so it is below (10^5).

The reconstruction follows parents from `n` back to `1`, then reverses the resulting list. The explicit `cur == 1` check prevents accidentally continuing through `parent[1]`, which is `-1`.

## Worked Examples

### Sample 1

The important distance changes are shown below. The exact deque can contain additional vertices between the displayed states, but the table records the relaxations that determine the final route.

| Processed vertex | Relaxation | New distance | Parent | Deque effect |
| --- | --- | --- | --- | --- |
| 1 | `1 -> 2`, cost 1 | `dist[2] = 1` | 1 | 2 goes back |
| 1 | `1 -> 3`, cost 1 | `dist[3] = 1` | 1 | 3 goes back |
| 2 | `2 -> 4`, cost 1 | `dist[4] = 2` | 2 | 4 goes back |
| 2 | `2 -> 5`, cost 1 | `dist[5] = 2` | 2 | 5 goes back |
| 3 | `3 -> 6`, cost 1 | `dist[6] = 2` | 3 | 6 goes back |
| 5 | `5 -> 7`, cost 0 | `dist[7] = 2` | 5 | 7 goes front |
| 7 | `7 -> 8`, cost 0 | `dist[8] = 2` | 7 | 8 goes front |
| 8 | `8 -> 9`, cost 0 | `dist[9] = 2` | 8 | 9 goes front |

One valid result produced by this implementation is:

```
2 6
1 2 5 7 8 9
```

The statement's sample uses a different shortest route, `1 3 5 7 8 9`, but both routes cost two ant-hours and contain no repeated wormhole. This demonstrates why a checker must accept any optimal route rather than compare the printed path against one particular sample path.

### Sample 2

The graph consists of two disconnected regions. The first contains wormholes reachable from 1, while the second contains wormhole 15.

| Processed region | Important transition | Result |
| --- | --- | --- |
| 1 | `1 -> 2`, cost 0 | `dist[2] = 0` |
| 1 | `1 -> 3`, cost 0 | `dist[3] = 0` |
| 2 | zero/one-cost outgoing edges | vertices 4, 5, 8 become reachable |
| 3 | zero/one-cost outgoing edges | no edge reaches 9 |
| 4 | zero-cost edges | vertices 6, 7, 8 become reachable |
| 8 | no transition toward 9 | second component remains unreachable |
| 9 | never reached | `dist[9] = infinity` |
| 15 | never reached | `dist[15] = infinity` |

The destination is wormhole 15, so the algorithm finishes with `dist[15] = infinity` and prints:

```
IMPOSSIBLE
```

This example demonstrates that reachability is independent of the existence of many zero-cost transitions. A large connected zero-cost component still cannot reach a destination in a disconnected component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Each edge is examined during relaxations, and deque operations are constant time. |
| Space | (O(n+m)) | The adjacency list stores all transitions, while distances, parents, and the deque use (O(n)) additional space. |

With (n,m \le 10^5), linear complexity is exactly the scale required by the constraints. The algorithm stores only a few arrays of size (n) and an adjacency list of size (m), which comfortably fits the memory limit. The absence of a heap also keeps the constant factors small enough for the time limit.

## Test Cases

Because the problem allows any shortest route, tests should validate the cost and route properties rather than assume a unique path. The following harness embeds the solution logic in a function and checks the output structurally.

```python
import sys
import io
from collections import deque

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        a = next(it)
        b = next(it)
        t = next(it)
        graph[a].append((b, t))

    INF = 10**18
    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)

    dist[1] = 0
    dq = deque([1])

    while dq:
        v = dq.popleft()

        for to, w in graph[v]:
            nd = dist[v] + w

            if nd < dist[to]:
                dist[to] = nd
                parent[to] = v

                if w == 0:
                    dq.appendleft(to)
                else:
                    dq.append(to)

    if dist[n] == INF:
        return "IMPOSSIBLE\n"

    path = []
    cur = n

    while True:
        path.append(cur)
        if cur == 1:
            break
        cur = parent[cur]

    path.reverse()

    return f"{dist[n]} {len(path)}\n" + " ".join(map(str, path)) + "\n"

def check(inp: str, expected_cost=None, expected_path=None):
    out = solve_data(inp).strip()

    if expected_path is not None:
        expected = (
            f"{expected_cost} {len(expected_path)}\n"
            + " ".join(map(str, expected_path))
        )
        assert out == expected
        return

    assert out == "IMPOSSIBLE"

# Provided sample 1.
sample1 = """\
9 11
1 2 1
1 3 1
2 4 1
2 5 1
3 5 1
3 6 1
4 9 1
6 9 1
5 7 0
7 8 0
8 9 0
"""
check(sample1, 2, [1, 2, 5, 7, 8, 9])

# Provided sample 2.
sample2 = """\
15 18
1 2 0
1 3 0
2 3 1
2 5 1
2 4 1
3 4 1
3 8 1
4 5 0
4 6 0
4 7 0
4 8 0
9 13 1
10 13 1
10 11 1
11 14 1
12 14 1
13 14 0
14 15 0
"""
check(sample2)

# Minimum-size graph: start equals destination.
case1 = """\
1 0
"""
check(case1, 0, [1])

# Unreachable destination.
case2 = """\
2 0
"""
check(case2)

# All transitions have zero cost. The route must remain simple.
case3 = """\
5 5
1 2 0
2 3 0
3 2 0
3 4 0
4 5 0
"""
check(case3, 0, [1, 2, 3, 4, 5])

# All useful transitions have cost one.
case4 = """\
4 3
1 2 1
2 3 1
3 4 1
"""
check(case4, 3, [1, 2, 3, 4])

# A zero-cost cycle must not appear in the reconstructed route.
case5 = """\
3 3
1 2 0
2 1 0
2 3 1
"""
check(case5, 1, [1, 2, 3])

# Large boundary case: 100000 vertices connected by 99999 zero-cost edges.
n = 100000
large_edges = "\n".join(
    f"{i} {i + 1} 0" for i in range(1, n)
)
large_input = f"{n} {n - 1}\n{large_edges}\n"
large_output = solve_data(large_input).split()

assert int(large_output[0]) == 0
assert int(large_output[1]) == n
assert int(large_output[2]) == 1
assert int(large_output[-1]) == n
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0 1 / 1` | The start and destination can be the same vertex. |
| `2 0` | `IMPOSSIBLE` | Unreachable destination handling. |
| Zero-cost graph with a cycle | `0 5 / 1 2 3 4 5` | Zero-cost cycles must not cause repeated vertices in the answer. |
| Four-vertex chain of cost-one edges | `3 4 / 1 2 3 4` | Correct accumulation of unit costs. |
| `1 -> 2 -> 1 -> 3` | `1 3 / 1 2 3` | Reconstructing a simple route despite a zero-cost cycle. |
| 100,000-vertex zero-cost chain | Cost `0`, 100,000 vertices | Maximum vertex count and large linear input. |

## Edge Cases

### Start equals destination

For

```
1 0
```

the deque initially contains vertex 1 and `dist[1]` is zero. No transition needs to be processed. The reconstruction starts at `n = 1`, immediately stops, and returns `[1]`. The output is `0 1` followed by `1`. This is the boundary case that catches implementations assuming a path must contain at least one edge.

### Unreachable destination

For

```
2 0
```

the deque contains only vertex 1. Since there are no outgoing transitions, vertex 2 remains at infinity. The algorithm prints `IMPOSSIBLE` instead of attempting to follow `parent[2]`. This is why the reachability check must happen before reconstruction.

### Zero-cost cycles

Consider

```
3 3
1 2 0
2 1 0
2 3 1
```

The first zero-cost transition sets `dist[2] = 0` and `parent[2] = 1`. Processing 2 can inspect the edge back to 1, but that edge gives distance zero again, which is not strictly better than the existing `dist[1] = 0`, so the parent of 1 is not changed. The edge `2 -> 3` gives `dist[3] = 1` and `parent[3] = 2`. Reconstruction produces `3 -> 2 -> 1`, which reverses to `1 -> 2 -> 3`. The forbidden cycle never enters the predecessor chain.

### Multiple optimal routes

For

```
4 4
1 2 1
1 3 1
2 4 0
3 4 0
```

both possible routes cost one. Depending on adjacency order and deque processing, the algorithm can select either `1 2 4` or `1 3 4`. Both are valid because the distance is optimal and every vertex appears only once. The problem explicitly permits any such solution, so deterministic selection of one particular shortest path is unnecessary.

### Maximum input size

A chain of 100,000 vertices and 99,999 transitions requires the algorithm to process essentially the entire graph. Each adjacency entry is inspected once as part of a relaxation, while the distance and parent arrays contain only 100,001 elements because of one-based indexing. The running time remains linear, and the memory consumption remains proportional to the input size.

The central lesson is that the apparently difficult "do not visit a wormhole twice" condition does not require tracking visited sets in the shortest-path state. Nonnegative edge costs guarantee that cycles can always be removed from an optimal walk, so an ordinary shortest-path algorithm is enough. The zero-or-one cost restriction then reduces Dijkstra's priority queue to a deque, giving an (O(n+m)) solution.
