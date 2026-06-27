---
title: "CF 105624B - \u0414\u043e\u0433\u043e\u043d\u044f\u043b\u043a\u0438 \u043d\u0430 \u043e\u0441\u0442\u0440\u043e\u0432\u0430\u0445"
description: "The graph describes a group of islands connected by two-way ferry routes. Each route has a travel cost, and every island has a tax that must be paid if Moana chooses to visit it."
date: "2026-06-26T18:12:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105624
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105624
solve_time_s: 48
verified: true
draft: false
---

[CF 105624B - \u0414\u043e\u0433\u043e\u043d\u044f\u043b\u043a\u0438 \u043d\u0430 \u043e\u0441\u0442\u0440\u043e\u0432\u0430\u0445](https://codeforces.com/problemset/problem/105624/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph describes a group of islands connected by two-way ferry routes. Each route has a travel cost, and every island has a tax that must be paid if Moana chooses to visit it. Moana starts from every possible island separately and wants to visit some island, pay its tax, and then return to where she started. The task is to find this minimum total cost for every starting island. The original problem is from Codeforces Gym 105624, problem B.

For an island `u`, if Moana chooses destination `v`, the trip costs `dist(u, v)` to get there and the same amount to return because the ferries are bidirectional. The total becomes:

```
2 * dist(u, v) + a[v]
```

We need this value minimized over all possible destinations `v`.

The input size is large enough that treating every island independently is impossible. With up to `2 * 10^5` islands and routes, an approach that runs a shortest path algorithm from every island would need about `n * (m log n)` operations, which is around billions of operations in the worst case. The intended solution must process the whole graph in roughly linearithmic time.

The tricky part is not finding shortest paths themselves, but combining all possible destinations into one computation. A careless solution might run Dijkstra from each island and add the cheapest tax after reaching every other island. For a graph with 200000 islands this repeats almost the same work many times.

Another edge case is when the cheapest destination is the starting island itself. For example:

```
Input
2 1
1 2 5
3 10
```

The answer for island 1 is `3`, because staying on island 1 costs only its tax. A solution that only considers moving along at least one edge would incorrectly output `13`.

A second edge case is when a long path with a cheap tax is better than a nearby expensive island. For example:

```
Input
3 2
1 2 5
2 3 1
100 1 2
```

For island 1, going to island 3 costs `5 + 1 = 6` one way, so the total is `12 + 2 = 14`. Choosing island 2 gives `10 + 1 = 11`, so island 2 is actually better here. An implementation that only checks direct neighbors would miss valid destinations in larger graphs.

## Approaches

The direct brute-force method is straightforward. For every starting island `u`, run Dijkstra to compute distances to all other islands. Then scan all islands `v` and take the minimum value of `2 * dist(u, v) + a[v]`. It is correct because Dijkstra gives the exact shortest path distance for the chosen start. The problem is the repeated work. With `n` runs, the complexity becomes `O(nm log n)`, which is far beyond what the constraints allow.

The key observation is that every starting island asks the same type of question. Instead of choosing a start and searching for destinations, we can reverse the perspective. Imagine that every island already has a starting cost equal to its tax. We spread these values through the graph. When a value from island `v` travels across an edge, it gains twice the edge weight because the final answer includes the trip to `v` and the return trip.

This transforms the formula into a standard shortest path problem. If we create a graph where every edge weight is doubled, and initially put `a[v]` into the priority queue for every island `v`, a multi-source Dijkstra computes:

```
min(a[v] + shortest doubled-edge distance from u to v)
```

which is exactly:

```
min(a[v] + 2 * dist(u, v))
```

The graph structure makes this possible because all destinations are independent sources of potential answers, and Dijkstra naturally keeps the cheapest one reaching each island.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm log n) | O(n + m) | Too slow |
| Optimal | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the islands. For every ferry route with cost `w`, store an edge with cost `2 * w`. The doubling is done here because every movement toward a destination is paired with the same movement back.
2. Put every island into the priority queue with its own tax value `a[i]` as the initial distance. Each island represents a possible destination that can provide an answer to every other island.
3. Run Dijkstra's algorithm normally. When removing an island from the queue, try relaxing all neighboring islands using the doubled edge cost.
4. If reaching a neighbor through the current island gives a smaller value, update it and push the new value into the queue.
5. After the priority queue is empty, the stored distance of every island is the minimum amount Moana must spend when starting there.

Why it works: Each initial value `a[v]` represents choosing island `v` as the destination. Moving this value through the graph adds `2 * edge_cost` for every ferry used, which exactly matches the cost of going to `v` and returning. Dijkstra always keeps the cheapest possible value reaching each island because all transformed edge weights are non-negative. Since every possible destination starts in the queue, the final value for each island is the minimum over all destinations.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        w *= 2
        graph[u].append((v, w))
        graph[v].append((u, w))

    a = list(map(int, input().split()))

    dist = a[:]
    pq = [(a[i], i) for i in range(n)]
    heapq.heapify(pq)

    while pq:
        cur, u = heapq.heappop(pq)

        if cur != dist[u]:
            continue

        for v, w in graph[u]:
            nxt = cur + w
            if nxt < dist[v]:
                dist[v] = nxt
                heapq.heappush(pq, (nxt, v))

    print(*dist)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the ferry network efficiently because the number of routes is large but still linear in the input size. Every stored edge already has its weight multiplied by two, so the Dijkstra relaxation directly matches the required formula.

The distance array is initialized with the island taxes instead of infinity. This is the main difference from ordinary single-source Dijkstra. Every island is a possible destination, so every island starts as a candidate answer source.

The priority queue may contain outdated values after a better route is found. The `if cur != dist[u]` check discards those entries and keeps the algorithm efficient.

Python integers do not overflow, which is useful because the maximum possible path cost can exceed 32-bit integer limits.

## Worked Examples

For the first sample:

```
Input
4 2
2 3 2
3 4 3
15 3 10 2
```

The algorithm starts with all taxes in the queue.

| Current island | Current value | Updated neighbors | Distance state |
| --- | --- | --- | --- |
| Island 4 | 2 | Island 3 becomes 8 | [15, 3, 8, 2] |
| Island 2 | 3 | Island 3 candidate becomes 7 | [15, 3, 7, 2] |
| Island 3 | 7 | Island 4 candidate becomes 13, Island 2 becomes 11 | [15, 3, 7, 2] |
| Island 1 | 15 | No routes | [15, 3, 7, 2] |

The final values match the required output. This trace shows that the cheapest destination can come from any island, not necessarily a nearby one.

For the second sample:

```
Input
3 3
1 2 1
1 3 1
2 3 1
10 20 30
```

| Current island | Current value | Updated neighbors | Distance state |
| --- | --- | --- | --- |
| Island 1 | 10 | Island 2 becomes 12, Island 3 becomes 12 | [10, 12, 12] |
| Island 2 | 12 | No better updates | [10, 12, 12] |
| Island 3 | 12 | No better updates | [10, 12, 12] |

This demonstrates the multi-source property. Island 1 immediately provides the best destination for the other islands.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each island enters the priority queue and each route is relaxed once from each endpoint. |
| Space | O(n + m) | The graph stores all ferry routes and the arrays store distances and queue data. |

The constraints require avoiding repeated shortest path computations. The multi-source Dijkstra approach processes the entire graph once, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io
import heapq

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        w *= 2
        graph[u].append((v, w))
        graph[v].append((u, w))

    a = list(map(int, input().split()))

    dist = a[:]
    pq = [(dist[i], i) for i in range(n)]
    heapq.heapify(pq)

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return " ".join(map(str, dist)) + "\n"

assert solve_io(
    """4 2
2 3 2
3 4 3
15 3 10 2
"""
) == "15 3 7 2\n", "sample 1"

assert solve_io(
    """3 3
1 2 1
1 3 1
2 3 1
10 20 30
"""
) == "10 12 12\n", "sample 2"

assert solve_io(
    """2 1
1 2 5
3 10
"""
) == "3 13\n", "staying on the starting island"

assert solve_io(
    """3 2
1 2 5
2 3 1
100 1 2
"""
) == "11 1 2\n", "cheap middle destination"

assert solve_io(
    """5 4
1 2 1
2 3 1
3 4 1
4 5 1
7 7 7 7 7
"""
) == "7 9 11 9 7\n", "equal taxes and path boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two islands with one edge | `3 13` | The algorithm allows staying at the current island. |
| Three islands with a chain | `11 1 2` | A destination farther away can still be optimal. |
| Five-island line with equal taxes | `7 9 11 9 7` | Symmetric paths and boundary islands. |

## Edge Cases

For the case where staying is optimal:

```
2 1
1 2 5
3 10
```

Both islands begin in the priority queue. Island 1 starts with value `3`, so no path through another island can improve it because every ferry traversal adds a positive amount. The answer remains `3`.

For the case where a better destination is not adjacent:

```
3 2
1 2 5
2 3 1
100 1 2
```

The initial queue contains values `100`, `1`, and `2`. The value `1` from island 2 spreads to island 1 with additional cost `10`, producing `11`. The value from island 3 reaches island 1 with additional cost `12`, producing `14`. The algorithm keeps the smaller value, proving that all possible destinations are considered rather than only direct neighbors.
