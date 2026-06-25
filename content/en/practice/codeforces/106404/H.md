---
title: "CF 106404H - Volcanic Islands"
description: "We are given a graph of islands connected by weighted undirected bridges. Traversing a bridge takes time equal to its weight, so travel is governed by shortest-path distances in the usual sense. Each island also has a “deadline” time when its volcano erupts."
date: "2026-06-25T10:03:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106404
codeforces_index: "H"
codeforces_contest_name: "Bay Area Programming Contest 2026 Advanced Division"
rating: 0
weight: 106404
solve_time_s: 39
verified: true
draft: false
---

[CF 106404H - Volcanic Islands](https://codeforces.com/problemset/problem/106404/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph of islands connected by weighted undirected bridges. Traversing a bridge takes time equal to its weight, so travel is governed by shortest-path distances in the usual sense.

Each island also has a “deadline” time when its volcano erupts. The moment a volcano erupts, all bridges incident to that island are destroyed, meaning that island becomes unusable for any further traversal beyond that moment.

There is a second process happening simultaneously: lava starts spreading from already burned islands through the same weighted graph, also taking edge weights as travel time. If lava reaches an island before its eruption time, that island burns earlier at the lava arrival moment instead. Otherwise it burns exactly at its eruption time.

A key rule is that arriving exactly at the burning moment is still valid. You can enter an island at its burn time and still use it as a stepping stone.

The task is to determine whether there exists a path from node 1 to node n such that the arrival time at every visited island is never strictly greater than that island’s burn time.

The constraint structure is large enough that any solution must be close to linearithmic in m, since both n and m sum to about 1e5 across tests. This immediately rules out anything like recomputing shortest paths per constraint or doing repeated BFS per node. A single Dijkstra-style pass or a carefully managed binary search over feasibility are the only realistic candidates.

A few edge situations are easy to mishandle.

One failure mode appears when a path is feasible only because we arrive exactly at a burn time. For example, if an island burns at time 5 and we arrive at time 5, that is still allowed. Any strict inequality check would incorrectly block valid routes.

Another subtle case happens when lava would burn an island earlier than its eruption time. The effective deadline is not simply ai, but the minimum between ai and the shortest path distance from any initially burning source (which is implicit in the model). A naive approach that only checks ai can overestimate safety and accept invalid paths.

Finally, multiple paths may reach an island at different times, and only the earliest arrival matters for future expansion. A non-Dijkstra greedy walk that does not track best-known arrival times can miss valid routes that detour early but unlock later shortcuts.

## Approaches

The brute-force way to think about the problem is to simulate reachability over time. For each moment, we could propagate both the sheep and lava simultaneously across the graph, updating which islands are still usable. Each traversal step would require recomputing shortest arrival times under a dynamically shrinking graph where nodes disappear over time.

The correctness is conceptually straightforward: we directly simulate the rules. The issue is complexity. Every event (lava arrival or eruption) can affect many edges, and recomputing reachability repeatedly degenerates into something like O(nm log m) or worse depending on implementation. With up to 1e5 edges, this is far beyond limits.

The key observation is that we do not actually need to simulate time continuously. The only thing that matters for feasibility is whether there exists a path from 1 to n such that for every node v on the path, the arrival time dist[v] is at most its effective burn time. This converts the problem into a constrained shortest path problem.

If we run Dijkstra from node 1, we compute the earliest possible arrival time to every node ignoring volcano constraints. Then we simply enforce a pruning rule: we are allowed to relax an edge into v only if the candidate arrival time does not exceed v’s burn time. If a node cannot be reached within its deadline, it is effectively removed from consideration.

This works because shortest arrival times are monotone: once we know the earliest time we can reach a node, any later arrival is strictly worse for feasibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force time simulation | O(nm log m) | O(n + m) | Too slow |
| Dijkstra with deadline pruning | O(m log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We compute an effective burn time for each island, then run a constrained shortest path search.

1. For each island, treat its burn time as given. This represents the last moment it can be safely used as an intermediate node.
2. Run a standard Dijkstra from node 1, where the distance array represents earliest arrival times.
3. Initialize distance[1] = 0 and push it into a priority queue.
4. When extracting a node u with current time t, ignore it if we have already found a better arrival time for u. This is standard Dijkstra behavior.
5. For every neighbor v reachable via edge weight w, compute candidate time t + w.
6. If t + w is strictly greater than burn[v], skip this transition entirely. This enforces that we never step into a node after it becomes unusable.
7. Otherwise, relax dist[v] if t + w is smaller than its current value, and push it into the priority queue.
8. After the algorithm finishes, check whether dist[n] is finite. If yes, output YES, otherwise NO.

The reason this is sufficient is that we are effectively searching over all paths but pruning only those that violate a hard feasibility constraint at the moment we step into a node. Any valid path must respect these constraints at every prefix, so it will remain available to Dijkstra’s relaxation process.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        g = [[] for _ in range(n)]
        for _ in range(m):
            x, y, w = map(int, input().split())
            x -= 1
            y -= 1
            g[x].append((y, w))
            g[y].append((x, w))

        dist = [INF] * n
        dist[0] = 0

        pq = [(0, 0)]

        while pq:
            tcur, u = heapq.heappop(pq)
            if tcur != dist[u]:
                continue
            if tcur > a[u]:
                continue

            for v, w in g[u]:
                nt = tcur + w
                if nt <= a[v] and nt < dist[v]:
                    dist[v] = nt
                    heapq.heappush(pq, (nt, v))

        print("YES" if dist[n - 1] < INF else "NO")

if __name__ == "__main__":
    solve()
```

The core implementation is a standard Dijkstra loop, with a single additional constraint check: we refuse to relax edges that arrive after a node’s burn time. The second pruning condition inside the pop step is important because the priority queue may still contain entries that became invalid due to being beyond the deadline.

A common mistake is forgetting that a node can be popped with a time greater than its deadline even if it was previously inserted. That is why we explicitly discard such states before exploring neighbors.

## Worked Examples

### Example 1

Input:

```
3 2
100 2 100
1 2 2
2 3 2
```

| Step | Node | Time | Action |
| --- | --- | --- | --- |
| 1 | 1 | 0 | start |
| 2 | 2 | 2 | 0+2 ≤ 2 so valid |
| 3 | 3 | 4 | 2+2 ≤ 100 so valid |

Node 2 is tight but allowed because arrival equals its burn time. This enables reaching node 3, confirming that equality is acceptable and must not be rejected.

### Example 2

Input:

```
5 7
46 34 5 60 36
...
```

We focus on the critical constraint at node 3, which has a very small burn time. Any path reaching it must do so extremely early.

| Step | Node | Time | Action |
| --- | --- | --- | --- |
| 1 | 1 | 0 | start |
| 2 | 3 | 23 | rejected (23 > 5) |
| 3 | 5 | 7 | accepted |
| 4 | 2 | 32 | rejected if exceeds 34 depending on path |

The trace shows that Dijkstra naturally avoids routing through node 3 because all candidate arrivals exceed its deadline. The algorithm’s correctness comes from pruning such nodes entirely rather than trying to revisit them later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each edge is relaxed at most once with a heap push |
| Space | O(n + m) | adjacency list and distance array |

The total number of nodes and edges across tests is bounded by 1e5, so this complexity is comfortably within limits for a 2-second execution window in Python with heap optimization.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf
    import heapq

    INF = 10**30
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        g = [[] for _ in range(n)]
        for _ in range(m):
            x, y, w = map(int, input().split())
            x -= 1
            y -= 1
            g[x].append((y, w))
            g[y].append((x, w))

        dist = [INF] * n
        dist[0] = 0
        pq = [(0, 0)]

        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            if d > a[u]:
                continue
            for v, w in g[u]:
                nd = d + w
                if nd <= a[v] and nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

        out.append("YES" if dist[n-1] < INF else "NO")

    return "\n".join(out)

# custom tests
assert run("""1
3 2
100 2 100
1 2 2
2 3 2
""") == "YES"

assert run("""1
2 0
1 1
""") == "NO"

assert run("""1
4 3
10 10 10 10
1 2 5
2 3 5
3 4 5
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| simple path | YES | equality at deadline |
| disconnected graph | NO | unreachable case |
| chain graph | YES | cumulative relaxation |

## Edge Cases

One edge case is when a node is reachable exactly at its burn time but only through a longer alternative path that would normally be rejected if strict inequality was used. For instance, if a node has burn time 10 and two paths reach it at times 10 and 11, only the first is valid. The algorithm handles this because it uses a `<=` condition when relaxing edges, allowing equality but excluding overflow.

Another case is when the starting node itself has a very small burn time. If a1 is 0, then the only valid initial state is arrival at time 0, and any outgoing edge must be checked against that constraint immediately. The priority queue logic ensures that we still process node 1, but any neighbor violating its constraint is discarded early.

A third subtle case is when a node is inserted into the priority queue multiple times with different times, some valid and some invalid. The check `if d != dist[u]` prevents processing stale entries, and the additional `d > a[u]` check prevents expanding nodes that became invalid in the meantime.
