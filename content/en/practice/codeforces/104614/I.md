---
title: "CF 104614I - Road To Savings"
description: "The city is modeled as an undirected weighted graph. Each intersection is a vertex and each road is an edge whose weight is its length."
date: "2026-06-29T20:31:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104614
codeforces_index: "I"
codeforces_contest_name: "2022-2023 ICPC East Central North America Regional Contest (ECNA 2022)"
rating: 0
weight: 104614
solve_time_s: 70
verified: true
draft: false
---

[CF 104614I - Road To Savings](https://codeforces.com/problemset/problem/104614/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is modeled as an undirected weighted graph. Each intersection is a vertex and each road is an edge whose weight is its length. The mayor always travels from intersection `a` to intersection `b`, and Pat only wants to pave roads that belong to at least one shortest path between those two locations.

The task is not to find one shortest path. A road should be paved if there exists any shortest path that uses it. Every remaining road is unnecessary, and we must output the sum of their lengths.

The graph contains at most 100 vertices, while the number of roads is unrestricted in the statement but can never exceed the number of edges in a simple undirected graph, which is `n(n-1)/2`. Even the densest graph has fewer than 5000 edges. These limits are small enough that running Dijkstra's algorithm several times is completely practical. There is no need for more complicated shortest path data structures.

The main difficulty is that several different shortest routes may exist. A solution that reconstructs only one shortest path will miss roads that belong to another equally short route.

Consider the following graph.

```
4 4 1 4
1 2 1
2 4 1
1 3 1
3 4 1
```

The correct output is

```
0
```

Both routes from `1` to `4` have length `2`, so every road belongs to some shortest path. A solution that stores only one parent during Dijkstra would incorrectly mark only one route and output `2`.

Another subtle case is when a direct edge exists together with a longer alternative.

```
3 3 1 3
1 2 2
2 3 2
1 3 4
```

The correct output is

```
0
```

Both paths have total length `4`, so every edge must be paved. Looking only for strictly shorter alternatives would incorrectly exclude the direct road.

A final edge case occurs when a road cannot possibly appear on any shortest path.

```
3 3 1 3
1 2 1
2 3 1
1 3 5
```

The correct output is

```
5
```

The long direct edge is never useful, so its length contributes to the answer.

## Approaches

A straightforward idea is to test every road independently. Remove the road, compute a shortest path, then force the road into a path and check whether the resulting distance equals the global optimum. This works because every edge is examined separately, but it requires running a shortest path algorithm for every road. With roughly 5000 edges and each Dijkstra taking `O(m log n)`, the total work becomes `O(m² log n)`, which is unnecessary even for these constraints.

The key observation is that whether an edge belongs to some shortest path depends only on distances from the two endpoints.

Suppose an edge connects `u` and `v` with weight `w`. If we already know the shortest distance from `a` to every vertex and from every vertex to `b`, then we can immediately test both possible directions.

The edge appears on a shortest path if either

`distA[u] + w + distB[v] == distA[b]`

or

`distA[v] + w + distB[u] == distA[b]`.

The first equation corresponds to reaching `u`, traversing the edge to `v`, then continuing to `b`. The second handles the opposite direction because the graph is undirected.

This reduces the problem to two Dijkstra runs followed by one scan through the edge list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(m² log n)` | `O(n + m)` | Too slow |
| Optimal | `O(m log n)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the undirected weighted graph while also storing every edge in a separate list. The adjacency list is used by Dijkstra, while the edge list is needed for the final scan.
2. Run Dijkstra starting from the mayor's house `a`. Record the shortest distance from `a` to every vertex in the array `distA`.
3. Run Dijkstra again starting from the mayor's office `b`. Record the shortest distance from `b` to every vertex in the array `distB`.
4. Let `best = distA[b]`, which is the length of every shortest route between the two locations.
5. Examine every road `(u, v, w)` once. Check whether either `distA[u] + w + distB[v]` or `distA[v] + w + distB[u]` equals `best`.
6. If neither equality holds, no shortest path can contain this road, so add its length to the answer.
7. Print the accumulated sum.

### Why it works

The first Dijkstra computes the minimum possible cost to reach every vertex from the start. The second computes the minimum possible remaining cost from every vertex to the destination.

Suppose an edge belongs to a shortest path. Traversing that path reaches one endpoint optimally, crosses the edge, then reaches the destination optimally. Otherwise the path could be shortened. Consequently one of the two equalities must hold.

Conversely, if one of the equalities holds, concatenating a shortest path to the first endpoint, the edge itself, and a shortest path from the second endpoint produces a path whose total length equals the global optimum. Hence the edge lies on at least one shortest path.

The test is both necessary and sufficient, so every road is classified correctly.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def dijkstra(start, graph, n):
    INF = 10 ** 18
    dist = [INF] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def solve():
    n, m, a, b = map(int, input().split())

    graph = [[] for _ in range(n + 1)]
    edges = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
        edges.append((u, v, w))

    distA = dijkstra(a, graph, n)
    distB = dijkstra(b, graph, n)

    shortest = distA[b]
    ans = 0

    for u, v, w in edges:
        if (distA[u] + w + distB[v] == shortest or
                distA[v] + w + distB[u] == shortest):
            continue
        ans += w

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution follows the algorithm directly. The graph is stored twice, once as an adjacency list for efficient shortest path computation and once as a plain edge list so every road can be checked exactly once.

The Dijkstra implementation uses the standard lazy priority queue technique. Whenever an outdated entry is removed from the heap, it is ignored by comparing its distance against the current best value.

The final scan performs two equality tests for every undirected edge. Checking both orientations is essential because a shortest path may traverse the edge in either direction. Since Python integers have arbitrary precision, there is no risk of overflow even when summing several distances.

## Worked Examples

### Sample 1

Input

```
4 5 1 4
1 2 1
1 3 2
1 4 2
4 2 1
3 4 1
```

The distance arrays are

`distA = [0, 1, 2, 2]`

`distB = [2, 1, 1, 0]`

The shortest distance is `2`.

| Edge | Expression satisfied? | On shortest path? | Running answer |
| --- | --- | --- | --- |
| (1,2,1) | Yes | Yes | 0 |
| (1,3,2) | No | No | 2 |
| (1,4,2) | Yes | Yes | 2 |
| (2,4,1) | Yes | Yes | 2 |
| (3,4,1) | No | No | 3 |

The answer is `3`. The trace shows that an edge is rejected only when neither orientation achieves the global shortest distance.

### Sample 2

Input

```
4 5 1 4
1 2 1
1 3 2
1 4 1
4 2 1
3 4 1
```

The distance arrays are

`distA = [0, 1, 2, 1]`

`distB = [1, 1, 1, 0]`

The shortest distance is `1`.

| Edge | Expression satisfied? | On shortest path? | Running answer |
| --- | --- | --- | --- |
| (1,2,1) | No | No | 1 |
| (1,3,2) | No | No | 3 |
| (1,4,1) | Yes | Yes | 3 |
| (2,4,1) | No | No | 4 |
| (3,4,1) | No | No | 5 |

Only the direct road belongs to a shortest path, so every other road contributes to the final sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(m log n)` | Two Dijkstra runs and one linear scan over all roads |
| Space | `O(n + m)` | Distance arrays, adjacency list, and edge list |

Even the densest graph with 100 vertices contains fewer than 5000 edges, so two Dijkstra executions complete comfortably within the limits.

## Test Cases

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n, m, a, b = map(int, input().split())

    graph = [[] for _ in range(n + 1)]
    edges = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
        edges.append((u, v, w))

    def dijkstra(s):
        INF = 10 ** 18
        dist = [INF] * (n + 1)
        dist[s] = 0
        pq = [(0, s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    da = dijkstra(a)
    db = dijkstra(b)
    best = da[b]

    ans = 0
    for u, v, w in edges:
        if da[u] + w + db[v] == best or da[v] + w + db[u] == best:
            continue
        ans += w
    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

assert run("""4 5 1 4
1 2 1
1 3 2
1 4 2
4 2 1
3 4 1
""") == "3"

assert run("""4 5 1 4
1 2 1
1 3 2
1 4 1
4 2 1
3 4 1
""") == "5"

assert run("""2 1 1 2
1 2 7
""") == "0"

assert run("""4 4 1 4
1 2 1
2 4 1
1 3 1
3 4 1
""") == "0"

assert run("""3 3 1 3
1 2 1
2 3 1
1 3 5
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices with one edge | 0 | Minimum graph |
| Two equal shortest paths | 0 | Every edge should be accepted |
| Long direct edge plus short detour | 5 | Edge excluded from all shortest paths |
| Sample 1 | 3 | Mixed accepted and rejected roads |
| Sample 2 | 5 | Only one road belongs to a shortest path |

## Edge Cases

The first non-obvious case is multiple shortest paths.

```
4 4 1 4
1 2 1
2 4 1
1 3 1
3 4 1
```

The shortest distance is `2`. For each edge, one of the two equality checks succeeds, so every edge is classified as belonging to a shortest path. The algorithm outputs `0`, while a parent-based reconstruction would incorrectly discard half of the edges.

The second case is when two completely different routes have the same total length.

```
3 3 1 3
1 2 2
2 3 2
1 3 4
```

The shortest distance is `4`. Both the direct edge and the two-edge route satisfy the equality test, so all three roads are paved and the answer is `0`.

The final case contains a road that is strictly worse than every alternative.

```
3 3 1 3
1 2 1
2 3 1
1 3 5
```

The shortest distance is `2`. The long edge produces `0 + 5 + 0 = 5`, which is larger than the optimum, so neither equality holds. Its length is added to the answer, producing the correct output `5`.
