---
title: "CF 105900M - Minimum Path"
description: "We are given a directed weighted graph where nodes represent gas stations and edges represent one-way roads with travel distances. We start at node 1 and must reach node N. Every valid route from 1 to N has two competing criteria."
date: "2026-06-21T15:19:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105900
codeforces_index: "M"
codeforces_contest_name: "VI UnBalloon Contest Mirror"
rating: 0
weight: 105900
solve_time_s: 51
verified: true
draft: false
---

[CF 105900M - Minimum Path](https://codeforces.com/problemset/problem/105900/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed weighted graph where nodes represent gas stations and edges represent one-way roads with travel distances. We start at node 1 and must reach node N. Every valid route from 1 to N has two competing criteria.

First, the total distance of the route must be as small as possible. Among all routes that achieve this minimum total distance, we then care about how “smooth” the route is in terms of fuel consumption between stops. Smoothness is measured as the largest single edge weight used along the path. The final goal is to pick a shortest path, and among those, minimize the maximum edge weight.

So the output is two values. The first is the shortest possible distance from 1 to N. The second is, among all shortest paths, the minimum possible value of the largest edge used on that path.

The constraints go up to 200,000 nodes and edges, with weights up to 100,000. This immediately rules out anything cubic or even quadratic. A single Dijkstra run is fine, but anything involving recomputing shortest paths per edge or enumerating all paths is not.

A subtle issue appears when multiple shortest paths exist. A naive shortest path algorithm that only tracks distance will happily return any shortest path, but not necessarily the one with the best bottleneck. Another pitfall is trying to optimize bottleneck first, because the bottleneck-minimal path might not be shortest in total distance.

A small illustrative conflict:

Input:

```
3 3
1 2 1
2 3 10
1 3 5
```

Shortest distance is 6 via 1 → 2 → 3, but the direct path 1 → 3 has distance 5 and is not valid for the first criterion. Among shortest paths, only 1 → 2 → 3 exists, so answer is (11, 10). A naive “minimize max edge first” would pick 1 → 3 incorrectly.

Another edge case is equal shortest distances with different bottlenecks:

```
3 3
1 2 1
2 3 2
1 3 3
```

Both 1→2→3 and 1→3 have distance 3. The first has bottleneck 2, the second has 3. Correct answer is (3, 2).

## Approaches

A brute-force idea is to enumerate all paths from 1 to N, compute their total distance and maximum edge weight, and then choose the best pair under lexicographic ordering. This is conceptually correct but immediately infeasible. Even in a sparse graph, the number of paths can grow exponentially, easily reaching 2^N in DAG-like structures. Each path evaluation costs O(N), so the total becomes exponential and unusable.

A more structured attempt is to run Dijkstra once for shortest distances, then restrict attention only to edges that lie on at least one shortest path. This leads to building a subgraph where an edge (u, v) is allowed only if dist[u] + w == dist[v]. This works because any shortest path must satisfy this equality on every step.

Once we have this shortest-path DAG, the problem reduces to choosing a path from 1 to N inside it that minimizes the maximum edge weight. That is a classic “minimize maximum edge on a path” problem, solvable with another shortest path computation where the path cost is the maximum edge along the route instead of sum. Since edge relaxation becomes `max(current, w)`, we can run a second Dijkstra-like process on the DAG.

The key insight is separation of objectives. The shortest-path condition defines a constraint surface, and inside that surface we optimize a secondary objective. The structure of Dijkstra guarantees that all shortest distances are fixed before we reason about secondary costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(N) | Too slow |
| Two-phase Dijkstra (dist + constrained bottleneck DP) | O((N + M) log N) | O(N + M) | Accepted |

## Algorithm Walkthrough

### Optimal strategy

1. Run Dijkstra from node 1 to compute the shortest distance to every node. This establishes the minimum possible total cost to reach each station. Without this, we cannot define what “shortest path” means locally at each node.
2. Construct a filtered adjacency structure that keeps only edges (u, v, w) satisfying dist[u] + w == dist[v]. This ensures that every retained edge is compatible with at least one shortest path. Any edge violating this condition can never appear in a valid shortest path, since it would strictly increase total distance.
3. On this filtered graph, we now compute a secondary DP value: the minimum possible maximum edge weight along any path from 1 to each node, restricted to shortest paths only.
4. Initialize a second Dijkstra-like process where the state cost at node v is the smallest possible value of the maximum edge used so far. Set source value to 0.
5. Use a priority queue ordered by this bottleneck value. From node u, when traversing an edge (u, v, w), the new cost becomes max(current_cost, w). This models exactly the maximum edge encountered along the path.
6. Relax v if this new bottleneck value improves its current best value.
7. After processing, the answer for node N is dist[N] as the shortest distance and best_bottleneck[N] as the minimized maximum edge under shortest-path constraint.

### Why it works

The first Dijkstra locks in exact shortest distances. That turns the graph into a layered structure where every valid move must preserve optimal distance growth. Inside this structure, any path from 1 to N corresponds to a shortest path in the original graph.

Because every retained edge preserves shortest-path optimality locally, concatenating such edges preserves global optimality of distance. This means we are not searching over all paths anymore, only over the set of shortest paths.

Within that restricted set, the second process explores all feasible shortest paths but compares them using a monotone cost function, the maximum edge seen so far. This function is compatible with Dijkstra-style relaxation because extending a path cannot decrease its maximum edge. That guarantees greedy expansion remains valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq
from collections import defaultdict

def dijkstra_dist(n, adj):
    INF = 10**30
    dist = [INF] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    
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

def dijkstra_bottleneck(n, adj, dist):
    INF = 10**30
    best = [INF] * (n + 1)
    best[1] = 0
    pq = [(0, 1)]
    
    while pq:
        cur, u = heapq.heappop(pq)
        if cur != best[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w != dist[v]:
                continue
            nc = max(cur, w)
            if nc < best[v]:
                best[v] = nc
                heapq.heappush(pq, (nc, v))
    
    return best

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        a, b, w = map(int, input().split())
        adj[a].append((b, w))
    
    dist = dijkstra_dist(n, adj)
    best = dijkstra_bottleneck(n, adj, dist)
    
    print(dist[n], best[n])

if __name__ == "__main__":
    solve()
```

The solution starts by building the full directed adjacency list. The first Dijkstra computes exact shortest distances from node 1, which are later used as a filtering condition.

The second phase reuses the same adjacency list but only allows transitions that preserve shortest-path equality. This filtering is done inline during relaxation rather than prebuilding a second graph, which saves memory and time.

A key implementation detail is the equality check `dist[u] + w != dist[v]`. This must be exact; using `>` or `<` comparisons would incorrectly allow non-shortest edges or discard valid ones.

The bottleneck DP uses a second priority queue because the state space still benefits from greedy expansion. Even though the cost is not additive, the maximum function remains monotonic along extensions, making Dijkstra-style ordering valid.

## Worked Examples

### Example 1

Input:

```
5 6
1 2 1
1 3 10
1 4 1
2 3 3
3 5 2
4 5 5
```

First Dijkstra gives shortest distances:

1=0, 2=1, 4=1, 3=4, 5=6

Filtered edges keep only those consistent with shortest paths:

1→2, 2→3, 3→5, 1→4, 4→5

Now we compute bottleneck DP.

| Step | Node | Bottleneck Value | Update |
| --- | --- | --- | --- |
| init | 1 | 0 | start |
| relax | 2 | max(0,1)=1 | update 2 |
| relax | 4 | max(0,1)=1 | update 4 |
| process 2 | 3 | max(1,3)=3 | update 3 |
| process 4 | 5 | max(1,5)=5 | candidate |
| process 3 | 5 | max(3,2)=3 | improve |

Final best path is 1→2→3→5 with bottleneck 3, total distance 6.

### Example 2

Input:

```
2 2
1 2 1
1 2 2
```

Shortest distance is 1 via the first edge only. The second edge is irrelevant because it does not improve distance.

Filtered graph keeps only edge (1,2,1). Bottleneck is 1.

This shows that edges that do not preserve shortest distance are completely eliminated before secondary optimization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | Two Dijkstra runs, each processing every edge with heap operations |
| Space | O(N + M) | adjacency list plus distance and bottleneck arrays |

The constraints allow up to 200,000 edges, so two heap-based graph traversals remain comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return run.capture(inp)

# We redefine properly for isolation
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""5 6
1 2 1
1 3 10
1 4 1
2 3 3
3 5 2
4 5 5
""") == "6 3"

# sample 2
assert run("""2 2
1 2 1
1 2 2
""") == "1 1"

# custom 1: tie shortest paths different bottleneck
assert run("""3 3
1 2 1
2 3 2
1 3 3
""") == "3 2"

# custom 2: multiple equal shortest paths
assert run("""4 4
1 2 1
2 4 1
1 3 1
3 4 1
""") == "2 1"

# custom 3: larger bottleneck forced
assert run("""4 4
1 2 1
2 4 100
1 3 1
3 4 1
""") == "2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| tie shortest paths | 3 2 | secondary optimization correctness |
| symmetric shortest paths | 2 1 | equal-cost branching |
| large edge blocking path | 2 1 | filtering of non-shortest edges |

## Edge Cases

A common failure is treating bottleneck optimization independently from shortest path computation. In the example where a direct edge is shorter in hops but longer in weight, a naive minimax approach would incorrectly select it.

The algorithm handles this because such edges are removed during the first distance pass. For instance:

```
3 3
1 2 1
2 3 10
1 3 5
```

Dijkstra gives dist[3]=5. The edge 2→3 is not on any shortest path since 1→2→3 totals 11, which exceeds 5, so it is ignored. The remaining path structure only allows valid shortest routes, and the bottleneck is computed only among them, preserving correctness.
