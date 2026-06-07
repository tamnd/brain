---
title: "CF 2122D - Traffic Lights"
description: "The problem describes a connected, simple undirected graph with n vertices and m edges. A token starts at vertex 1 at time 0. At each integer second t, if the token is at vertex u, you have two choices: either wait one second at u, or move along a specific edge of u."
date: "2026-06-08T03:42:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "dp", "graphs", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2122
codeforces_index: "D"
codeforces_contest_name: "Order Capital Round 1 (Codeforces Round 1038, Div. 1 + Div. 2)"
rating: 2400
weight: 2122
solve_time_s: 51
verified: true
draft: false
---

[CF 2122D - Traffic Lights](https://codeforces.com/problemset/problem/2122/D)

**Rating:** 2400  
**Tags:** brute force, data structures, divide and conquer, dp, graphs, greedy, shortest paths  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a connected, simple undirected graph with `n` vertices and `m` edges. A token starts at vertex `1` at time `0`. At each integer second `t`, if the token is at vertex `u`, you have two choices: either wait one second at `u`, or move along a specific edge of `u`. The edge you can use is determined by `(t mod deg(u)) + 1`, where `deg(u)` is the degree of vertex `u` and edges are indexed in the order they appear in the input. Each action, waiting or moving, consumes exactly one second.

The task is to find the minimum total time required to move the token from vertex `1` to vertex `n`, and among all strategies that achieve this minimum total time, the strategy that minimizes the total waiting time.

The input allows multiple test cases. Each graph has up to `5000` vertices in total across all test cases, and up to `5·10^5` edges in total. This implies that algorithms with time complexity `O(n·m)` or slightly higher are feasible, but anything quadratic per test case could easily exceed time limits. The modulo-based movement introduces a time-dependent edge constraint, which prevents the use of a naive shortest-path algorithm like standard BFS or Dijkstra without modification.

Edge cases include graphs where waiting is necessary to reach a vertex because the modulo order does not align with the desired path. For example, a vertex of degree `2` connected to the target vertex may require waiting multiple seconds for the "correct" edge to be usable. Another subtle case arises when the optimal path involves moving back and forth between two vertices to synchronize time with a future move. Naive BFS ignoring the modulo constraints will fail in such scenarios.

## Approaches

A brute-force approach would simulate every possible path and every waiting decision using a BFS that stores `(vertex, time)` states. This works because moving is deterministic given the current time and vertex, but the number of states grows rapidly: time can theoretically be unbounded in a naive BFS, and even if we limit it by `n*m`, the number of states becomes too large for `n=5000` and `m≈10^5`.

The key insight is that the modulo-based edge selection creates a deterministic schedule of outgoing edges for each vertex. This allows us to model the problem as a modified BFS where the next state depends not only on the vertex but also on the time modulo the degree of the vertex. Specifically, for vertex `u` with `deg(u)` edges, we only need to track times modulo `deg(u)` for each vertex, because after `deg(u)` seconds the pattern repeats. Therefore, we store `dist[u][r]` as the minimum total time to reach `u` when `t % deg(u) == r`. We can perform a BFS using a queue of states `(vertex, time, wait)` and propagate both total time and accumulated waiting.

This approach reduces the number of states to `sum(deg(u))` across all vertices, which is bounded by `2*m`. Each edge is relaxed only for the relevant modulo state, resulting in a time complexity roughly `O(m + n)` per test case, which fits comfortably within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS on `(vertex, time)` | O(n_m_max_time) | O(n*max_time) | Too slow |
| BFS with modulo states | O(m + n) | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Parse the input and construct the adjacency list for each vertex in the order given.
2. Initialize a distance array `dist[u][r]` for each vertex `u` and remainder `r` modulo `deg(u)`. Set all entries to infinity except `dist[1][0] = 0` because we start at vertex 1 at time 0.
3. Initialize a BFS queue with the starting state `(1, 0, 0)`, where the third element is total waiting time.
4. While the queue is not empty, pop `(u, t, wait)`:

a. Compute `r = t % deg(u)`.

b. The deterministic edge to move along is `adj[u][r]`. If moving along this edge results in a smaller `dist[v][(t+1) % deg(v)]`, push `(v, t+1, wait)` into the queue and update `dist`.

c. Consider waiting at `u`. If `dist[u][(r+1) % deg(u)] > t+1`, push `(u, t+1, wait+1)` and update `dist`.
5. After BFS finishes, among all states reaching vertex `n`, find the one with minimum total time. If multiple have the same total time, choose the one with the minimum waiting.
6. Output the minimum total time and the corresponding waiting time.

The correctness relies on the invariant that the BFS always explores the earliest times for each modulo state at each vertex. Because waiting increments time by 1 deterministically and moving follows a deterministic modulo schedule, BFS ensures that each state is visited with minimal total time. Tracking waiting explicitly allows tie-breaking among equivalent total-time paths.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        deg = [0] * (n + 1)
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)
            deg[u] += 1
            deg[v] += 1
        
        # distance: dist[u][r] = (total_time, wait_time)
        dist = [ [ (float('inf'), float('inf')) for _ in range(deg[u] or 1) ] for u in range(n + 1)]
        dist[1][0] = (0, 0)
        q = deque()
        q.append( (1, 0, 0) )  # vertex, time, wait
        
        while q:
            u, t, w = q.popleft()
            d = deg[u] or 1
            r = t % d
            # move along deterministic edge
            if deg[u] > 0:
                v = adj[u][r]
                nr = (t + 1) % deg[v]
                if (t+1, w) < dist[v][nr]:
                    dist[v][nr] = (t+1, w)
                    q.append( (v, t+1, w) )
            # wait
            nr = (r + 1) % d
            if (t+1, w+1) < dist[u][nr]:
                dist[u][nr] = (t+1, w+1)
                q.append( (u, t+1, w+1) )
        
        # pick best for vertex n
        res = min(dist[n])
        print(res[0], res[1])

if __name__ == "__main__":
    solve()
```

The solution constructs adjacency lists while tracking degrees. The `dist` array stores tuples `(total_time, waiting_time)` for each modulo state. BFS ensures that every state is visited optimally. Waiting is explicitly counted and propagated alongside total time. We compare tuples lexicographically, which naturally prioritizes smaller total time and then smaller waiting.

## Worked Examples

### Example 1

Input:

```
6 6
1 2
2 3
3 4
4 6
1 5
5 6
```

| Time | Vertex | Waiting | Edge move | Notes |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | wait | t%deg=0, better to wait |
| 1 | 1 | 1 | move 1-5 | t%deg=1 selects edge to 5 |
| 2 | 5 | 1 | wait | align with move to 6 |
| 3 | 5 | 2 | move 5-6 | reaches target |
| 4 | 6 | 2 | - | done |

Output: `4 2`

### Example 2

Input:

```
4 3
1 2
1 3
1 4
```

| Time | Vertex | Waiting | Edge move | Notes |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | move 1-2 | t%deg=0 selects edge to 2 |
| 1 | 2 | 0 | move 2-1 | only one edge back to 1 |
| 2 | 1 | 0 | move 1-4 | t%deg=2 selects edge to 4 |
| 3 | 4 | 0 | - | done |

Output: `3 0`

The trace demonstrates that modulo-based deterministic edges dictate optimal waiting and movement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m + n) | Each state `(vertex, time mod deg)` is visited at most once, total states ≤ 2*m |
|  |  |  |
