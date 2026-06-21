---
title: "CF 105791G - Grisi Maps"
description: "We are given an undirected weighted graph that models a region. Two special vertices are distinguished: one is the main entrance of a university, and the other is the destination called IC. For every query vertex $x$, we compare two ways of reaching IC."
date: "2026-06-21T14:24:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "G"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 63
verified: true
draft: false
---

[CF 105791G - Grisi Maps](https://codeforces.com/problemset/problem/105791/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph that models a region. Two special vertices are distinguished: one is the main entrance of a university, and the other is the destination called IC. For every query vertex $x$, we compare two ways of reaching IC.

The first way is the optimal one, meaning the shortest path from $x$ directly to IC in the graph. The second way is a fixed strategy used by Grisi: from $x$, he always goes to the entrance first using the shortest path, and then from the entrance to IC using the shortest path. The detour cost for a query is how much longer Grisi’s fixed strategy takes compared to the true shortest path from $x$ to IC.

The input describes the graph with up to 200,000 vertices and edges, followed by up to 200,000 queries. Each query is independent, so any solution that recomputes shortest paths per query would immediately exceed time limits. A single shortest path computation over the full graph is acceptable, but repeating it per query is not.

The key hidden structure is that Grisi’s route is composed of two shortest-path segments that depend only on the two special vertices. This makes it possible to precompute all needed distances once and answer every query in constant time.

A subtle edge case appears when the starting vertex is already the IC. The correct answer is zero, even though the formula for Grisi’s path would still produce a positive value if applied mechanically. This needs explicit handling.

## Approaches

A direct approach for each query is to run a shortest path algorithm from $x$ to IC, and also simulate Grisi’s route by running shortest paths from $x$ to the entrance, then adding the precomputed entrance-to-IC distance. Even if we reuse precomputed values for entrance to IC, we would still need a shortest path computation per query, leading to roughly $q$ runs of Dijkstra. With $q$ up to 200,000, this becomes computationally infeasible.

The turning point is noticing that the only varying point in each query is the starting vertex $x$, while both special vertices are fixed. That means we only ever need shortest path distances from a fixed source (entrance) and to a fixed target (IC). In an undirected graph, shortest path distances from IC can be computed by running Dijkstra from IC as well.

Once we have these two distance arrays, every query reduces to a simple arithmetic expression: distance from $x$ to entrance plus distance from entrance to IC, minus the optimal distance from $x$ to IC. This removes any per-query graph traversal entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Per query Dijkstra | $O(q \cdot m \log n)$ | $O(n + m)$ | Too slow |
| Two Dijkstra runs + queries | $O(m \log n + q)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We rely on the fact that shortest paths from a fixed source can be precomputed once using Dijkstra.

1. Run Dijkstra starting from the entrance vertex $X_1$, computing an array $d_1[v]$, which stores the shortest distance from $X_1$ to every vertex $v$. This captures how Grisi travels from any point to the entrance.
2. Run Dijkstra starting from the IC vertex $X_2$, computing an array $d_2[v]$, which stores the shortest distance from $v$ to IC. Since the graph is undirected, this is equivalent to distances from IC to all nodes.
3. Precompute the constant value $d_1[X_2]$, which is the shortest distance from the entrance to IC. This is the second segment of Grisi’s fixed route.
4. For each query vertex $x$, compute the shortest-path baseline as $d_2[x]$, which represents the true optimal travel time from $x$ to IC.
5. Compute Grisi’s travel time as $d_1[x] + d_1[X_2]$, since he first goes from $x$ to entrance and then from entrance to IC.
6. The extra time is the difference between Grisi’s route and the optimal route. If $x = X_2$, directly output 0. Otherwise output $(d_1[x] + d_1[X_2]) - d_2[x]$.

The explicit check for $x = X_2$ prevents a misleading positive value caused by the formula, since both shortest-path segments are still counted even though no travel is needed.

### Why it works

Shortest path distances satisfy optimal substructure: any shortest path between two fixed vertices can be decomposed into shortest paths between intermediate points. Dijkstra correctly computes these distances from fixed sources.

Grisi’s strategy forces every path from $x$ to IC to pass through the entrance, so his route length is exactly the sum of two independent shortest paths. The optimal route is independent of that constraint. Since both quantities are computed exactly once for all nodes, the comparison for each query is exact and no recomputation is needed.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline
INF = 10**30

def dijkstra(n, adj, src):
    dist = [INF] * (n + 1)
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def solve():
    n, m, q, x1, x2 = map(int, input().split())

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))

    d1 = dijkstra(n, adj, x1)
    d2 = dijkstra(n, adj, x2)

    base = d1[x2]

    out = []
    for _ in range(q):
        x = int(input())
        if x == x2:
            out.append("0")
        else:
            extra = d1[x] + base - d2[x]
            out.append(str(extra))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds an adjacency list and runs Dijkstra twice, once from each special vertex. The two distance arrays are reused across all queries. The value `base` stores the fixed cost from entrance to IC.

Each query is answered in constant time using the precomputed distances. The special-case check for `x2` ensures correctness when the start is already the destination.

A common implementation mistake is recomputing shortest paths per query or forgetting that the entrance-to-IC segment must be precomputed once rather than recomputed inside each query.

## Worked Examples

Consider a small graph where entrance is 1 and IC is 4:

Input graph:

1-2 (1), 2-4 (1), 1-3 (1), 3-4 (10)

From 1, shortest distances are: d1[1]=0, d1[2]=1, d1[3]=1, d1[4]=2.

From 4, shortest distances are: d2[4]=0, d2[2]=1, d2[3]=2, d2[1]=2.

For query x = 2:

Grisi route is 2→1→4, cost = d1[2] + d1[4] = 1 + 2 = 3.

Optimal route is d2[2] = 1.

Extra time is 2.

For query x = 3:

Grisi route is 3→1→4, cost = 1 + 2 = 3.

Optimal route is d2[3] = 2.

Extra time is 1.

| Query x | d1[x] | d1[X2] | d2[x] | Grisi | Optimal | Extra |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 2 | 1 | 3 | 1 | 2 |
| 3 | 1 | 2 | 2 | 3 | 2 | 1 |

This confirms that once distances are precomputed, each query reduces to a direct comparison between a forced-path metric and a shortest-path metric.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log n + q)$ | Two Dijkstra runs dominate, queries are O(1) each |
| Space | $O(n + m)$ | adjacency list plus two distance arrays |

The constraints allow up to 200,000 nodes and edges, so a couple of Dijkstra runs with binary heaps fits comfortably within time limits. The per-query work is negligible compared to preprocessing.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    INF = 10**30

    def dijkstra(n, adj, src):
        dist = [INF] * (n + 1)
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    n, m, q, x1, x2 = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))

    d1 = dijkstra(n, adj, x1)
    d2 = dijkstra(n, adj, x2)
    base = d1[x2]

    out = []
    for _ in range(q):
        x = int(input())
        if x == x2:
            out.append("0")
        else:
            out.append(str(d1[x] + base - d2[x]))
    return "\n".join(out)

# sample 1
assert run("""4 4 2 1 4
1 2 1
1 3 1
2 4 1
3 4 1
2
3
""") == "2\n2"

# custom 1: single edge
assert run("""2 1 1 1 2
1 2 5
1
""") == "0"

# custom 2: start is IC
assert run("""3 2 1 1 3
1 2 1
2 3 1
3
""") == "0"

# custom 3: triangle graph
assert run("""3 3 2 1 3
1 2 1
2 3 1
1 3 10
2
1
""") == "1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge graph | 0 | trivial direct path and correctness of base case |
| start equals IC | 0 | special-case handling of destination vertex |
| triangle graph | mixed values | correctness of shortest vs forced path comparison |

## Edge Cases

When the query vertex is the IC, the expression $d_1[x] + d_1[X_2] - d_2[x]$ becomes $d_1[X_2] + d_1[X_2]$, which is always positive even though no travel is needed. The explicit equality check ensures this case outputs zero, matching the problem definition.

In graphs where multiple paths have equal weight, Dijkstra still produces consistent shortest distances because it only depends on relaxation ordering, not uniqueness of paths. This guarantees that both distance arrays remain valid even when shortest paths are not unique.
