---
title: "CF 2014E - Rendez-vous de Marian et Robin"
description: "We are working on a weighted undirected graph where two people start from opposite ends and want to meet as quickly as possible. One starts at vertex 1 and the other at vertex n."
date: "2026-06-08T13:00:46+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 1800
weight: 2014
solve_time_s: 74
verified: true
draft: false
---

[CF 2014E - Rendez-vous de Marian et Robin](https://codeforces.com/problemset/problem/2014/E)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, shortest paths  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a weighted undirected graph where two people start from opposite ends and want to meet as quickly as possible. One starts at vertex 1 and the other at vertex n. They move along edges, but there is a twist: some vertices contain horses, and using a horse halves all travel times after you pick it up. Each person may decide independently when to mount a horse, and once mounted, the speed boost remains permanently.

The goal is to determine the earliest possible time at which the two travelers can occupy the same vertex at the same time, assuming optimal movement and optional waiting.

The core difficulty is that each person’s travel cost is not a single shortest path problem. Instead, the cost depends on whether they have already visited a horse vertex before reaching a given point. That means each vertex effectively has two states: without horse advantage and with horse advantage.

The constraints make it clear that any solution must be near linearithmic. With up to 2×10^5 vertices and edges per test batch, any method that recomputes shortest paths from scratch per state transition or simulates meeting times explicitly is too slow. A standard Dijkstra per state is acceptable, but anything like recomputing pairwise meeting times over all vertices is not.

A few subtle failure cases appear if we ignore statefulness.

One issue arises if we treat horse vertices as simple cost modifiers applied greedily when first encountered. For example, a path may pass a horse vertex too early to benefit fully, and a naive algorithm might assume it is always optimal to take it immediately.

Another issue is assuming a single shortest path distance per node suffices. That fails because arriving at a node later without a horse may still be better than arriving earlier without one, depending on future acceleration.

Finally, a naive approach might try to compute shortest paths from both ends and take a minimum over max-distances. That breaks because the two travelers can arrive at different times and one can wait.

## Approaches

A direct brute-force approach would attempt to compute the best possible meeting time for every vertex by independently simulating both travelers’ optimal movement strategies to that vertex. For each vertex v, we would compute the minimum time Marian can reach v under all possible choices of when to mount a horse, and similarly for Robin, then take the maximum of the two arrival times. The answer would be the minimum over all vertices.

The issue is that computing a single “minimum arrival time” is already not standard shortest path due to the horse state. If we attempt to explicitly branch on whether a horse has been taken at every vertex, each path decision doubles the state space, and naive enumeration leads to exponential paths or at least O(2^n)-style reasoning over subsets of horse activations.

The key observation is that the problem decomposes cleanly into a shortest path problem on an expanded state graph with only two states per node: before horse and after horse. Once this is recognized, the movement becomes standard Dijkstra. We run a multi-source shortest path from both starts, track best arrival times with and without horse usage, and then combine results per vertex.

The second important insight is how to model horse pickup. At a horse vertex, we can transition from “normal speed” state to “fast speed” state with zero cost. From that point onward, all edges are traversed at half cost. Since all weights are even, halving preserves integrality.

Once we have shortest arrival times for both Marian and Robin for both states at every vertex, the best meeting time at a vertex is simply the minimum over all valid combinations of states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over paths and horse choices | Exponential | High | Too slow |
| 2-state Dijkstra from each source | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We treat each vertex as having two layers: layer 0 means no horse has been used yet, and layer 1 means the traveler is currently riding a horse (or has activated one earlier). Each edge traversal depends on the current layer.

1. Build a graph where each vertex has two states. State 0 transitions represent walking edges with full cost, and state 1 transitions represent riding with half cost. This captures the fact that horse usage permanently changes movement speed.
2. Initialize distances for Marian and Robin separately. For both, set distance at their starting vertex in state 0 to zero. If the start vertex has a horse, we also allow an instantaneous transition into state 1.
3. Run Dijkstra’s algorithm on the expanded state graph for Marian. Each state is (vertex, mode), and transitions follow the rules above. This computes the minimum time Marian can reach every vertex with or without a horse advantage.
4. Repeat the same Dijkstra for Robin starting from vertex n. This produces a second distance table.
5. For every vertex v, compute the best possible meeting time by considering all combinations of states: Marian in state 0 or 1 and Robin in state 0 or 1. The meeting time is the minimum over max(distM[v][i], distR[v][j]).
6. Take the minimum over all vertices. If no vertex is reachable for both, output -1.

### Why it works

The state graph construction ensures that every valid real-world strategy corresponds to exactly one path in the expanded graph. The key invariant is that once a traveler enters state 1, all subsequent edge weights are consistently halved, matching the problem’s irreversible horse effect. Dijkstra guarantees optimality because all transitions have non-negative weights, and the graph contains no hidden dependencies beyond the two-state encoding. Thus, shortest paths in this expanded space correspond exactly to optimal travel strategies in the original problem.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

INF = 10**18

def dijkstra(n, adj, horses, start):
    dist = [[INF, INF] for _ in range(n + 1)]
    pq = []

    dist[start][0] = 0
    heapq.heappush(pq, (0, start, 0))

    if horses[start]:
        dist[start][1] = 0
        heapq.heappush(pq, (0, start, 1))

    while pq:
        d, u, s = heapq.heappop(pq)
        if d != dist[u][s]:
            continue

        for v, w in adj[u]:
            if s == 0:
                nd = d + w
                ns = s
                if nd < dist[v][ns]:
                    dist[v][ns] = nd
                    heapq.heappush(pq, (nd, v, ns))
            else:
                nd = d + w // 2
                ns = s
                if nd < dist[v][ns]:
                    dist[v][ns] = nd
                    heapq.heappush(pq, (nd, v, ns))

        if s == 0 and horses[u]:
            if d < dist[u][1]:
                dist[u][1] = d
                heapq.heappush(pq, (d, u, 1))

    return dist

t = int(input())
for _ in range(t):
    n, m, h = map(int, input().split())
    horses = [0] * (n + 1)
    for x in map(int, input().split()):
        horses[x] = 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))

    distM = dijkstra(n, adj, horses, 1)
    distR = dijkstra(n, adj, horses, n)

    ans = INF
    for v in range(1, n + 1):
        ans = min(ans,
                  max(distM[v][0], distR[v][0]),
                  max(distM[v][0], distR[v][1]),
                  max(distM[v][1], distR[v][0]),
                  max(distM[v][1], distR[v][1]))

    print(-1 if ans == INF else ans)
```

The implementation encodes the horse effect as a binary state. The Dijkstra queue stores tuples of (distance, node, state), and state transitions are carefully separated. The only subtle transition is at horse vertices, where we allow switching to the accelerated state with zero cost.

When combining answers, all four state pairs are checked explicitly. This is necessary because either traveler may or may not have activated a horse before reaching the meeting vertex.

## Worked Examples

### Example 1 (simple graph with direct improvement)

Consider a graph where 1 is connected to 2 with weight 10 and 2 is connected to 3 with weight 10, and vertex 2 has a horse. Marian starts at 1 and Robin at 3.

| Step | Marian dist[2][0] | Marian dist[2][1] | Robin dist[2][0] | Robin dist[2][1] |
| --- | --- | --- | --- | --- |
| Init | 0 at 1 | 0 at 1 if horse else INF | 0 at 3 | 0 at 3 if horse else INF |
| After Dijkstra | 10, then 5 via horse | 5 | 10 | 5 via 2 |

At vertex 2, Marian arrives in 5 using the horse, Robin arrives in 5 from the other side. Meeting time is 5.

This confirms that switching state at the correct vertex is essential to optimality.

### Example 2 (delayed horse usage advantage)

A path 1-2-3-4 where only vertex 3 has a horse, and weights are large on early edges. Marian may reach 3 later but benefits significantly after activation. Robin approaches from the opposite side similarly.

The key observation is that the optimal meeting point is not necessarily where either arrives earliest in base mode. The table of states shows that delayed activation produces strictly better downstream times, validating the need for the two-layer Dijkstra model.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Two Dijkstra runs over a graph with 2 states per node, each edge processed a constant number of times |
| Space | O(n + m) | adjacency list plus distance arrays for both sources |

The total sum of vertices and edges across test cases is bounded by 2×10^5, so the approach runs comfortably within limits even with a heap-based priority queue.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict
    import heapq

    INF = 10**18

    def dijkstra(n, adj, horses, start):
        dist = [[INF, INF] for _ in range(n + 1)]
        pq = []
        dist[start][0] = 0
        heapq.heappush(pq, (0, start, 0))
        if horses[start]:
            dist[start][1] = 0
            heapq.heappush(pq, (0, start, 1))

        while pq:
            d, u, s = heapq.heappop(pq)
            if d != dist[u][s]:
                continue
            for v, w in adj[u]:
                nd = d + (w if s == 0 else w // 2)
                if nd < dist[v][s]:
                    dist[v][s] = nd
                    heapq.heappush(pq, (nd, v, s))
            if s == 0 and horses[u]:
                if d < dist[u][1]:
                    dist[u][1] = d
                    heapq.heappush(pq, (d, u, 1))
        return dist

    t = int(input())
    out = []
    for _ in range(t):
        n, m, h = map(int, input().split())
        horses = [0] * (n + 1)
        for x in map(int, input().split()):
            horses[x] = 1
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v, w = map(int, input().split())
            adj[u].append((v, w))
            adj[v].append((u, w))

        distM = dijkstra(n, adj, horses, 1)
        distR = dijkstra(n, adj, horses, n)

        ans = INF
        for v in range(1, n + 1):
            ans = min(ans,
                      max(distM[v][0], distR[v][0]),
                      max(distM[v][0], distR[v][1]),
                      max(distM[v][1], distR[v][0]),
                      max(distM[v][1], distR[v][1]))

        out.append(str(-1 if ans == INF else ans))

    return "\n".join(out)

# sample 1
assert run("""6
2 1 1
1
1 2 10
3 1 2
2 3
1 2 10
3 3 1
2
1 2 4
1 3 10
2 3 6
4 3 2
2 3
1 2 10
2 3 18
3 4 16
3 2 1
2
1 2 4
1 3 16
7 7 1
3
1 5 2
2 6 12
1 2 12
6 4 8
7 3 4
6 3 4
7 6 4
""") == """5
-1
6
19
14
12"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 5 -1 6 19 14 12 | correctness across mixed graphs and horse placements |

## Edge Cases

A key edge case is when the start node already contains a horse. In that situation, the algorithm allows immediate transition into the accelerated state with zero cost. If this transition is omitted, all downstream distances for that traveler are overestimated, producing incorrect meeting times.

Another edge case occurs when both travelers arrive at a vertex in different states, for example one with horse and one without. The correct meeting time must consider all four state combinations. Failing to check mixed-state meetings incorrectly assumes both travelers behave symmetrically, which is false because one may have gained acceleration earlier.

A final subtle case is disconnected graphs. If either distance remains infinite for all states at all vertices, the answer must be -1. The combination step naturally handles this because all max operations remain infinite and the final minimum never updates.
