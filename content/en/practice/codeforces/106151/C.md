---
title: "CF 106151C - mansion"
description: "We are given a directed graph where each vertex represents a room in a mansion and each directed edge represents a one-way door between rooms. Every door has a cost of either 0 or 1 depending on whether it is already unlocked or requires using a badge to pass through."
date: "2026-06-19T19:23:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106151
codeforces_index: "C"
codeforces_contest_name: "2025 ICPC Greek Collegiate Programming Contest (GRCPC 2025)"
rating: 0
weight: 106151
solve_time_s: 58
verified: true
draft: false
---

[CF 106151C - mansion](https://codeforces.com/problemset/problem/106151/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each vertex represents a room in a mansion and each directed edge represents a one-way door between rooms. Every door has a cost of either 0 or 1 depending on whether it is already unlocked or requires using a badge to pass through. Using the badge effectively means we can traverse a locked door, but it always adds a cost of 1 to the total travel time.

The task is to find the minimum total cost to travel from room 1 to room N, or determine that it is impossible if there is no directed path.

The constraints allow up to 100,000 rooms and 100,000 doors, which immediately rules out any solution that tries to recompute shortest paths from scratch for each edge or uses a naive O(NM) relaxation approach. We need something close to linear or linearithmic time.

A common failure case appears when treating the graph as unweighted. For example, if we run a standard BFS ignoring weights, we incorrectly assume every edge has equal cost.

Consider a small case:

Input:

1 2 1

1 3 0

3 2 0

The optimal path from 1 to 2 is 1 → 3 → 2 with cost 0, while the direct edge 1 → 2 costs 1. A plain BFS might incorrectly prioritize the direct edge depending on adjacency ordering and miss the cheaper path.

Another subtle issue comes from using Dijkstra with a binary heap but treating weights as general integers. While correct, it is slightly overkill since weights are only 0 or 1 and we can do better.

## Approaches

The brute-force idea is to use a standard shortest path algorithm like Dijkstra. Each time we relax an edge, we push the updated distance into a priority queue. This is correct because all edge weights are non-negative, so Dijkstra guarantees optimality.

However, the complexity becomes O(M log N), which is acceptable here, but it ignores the structure of the problem: weights are only 0 or 1. That structure allows us to avoid the logarithmic factor entirely.

The key observation is that every relaxation only ever increases distance by at most 1. This means we do not need a full priority queue ordering; we only need to distinguish between “same cost” and “cost + 1”. That naturally leads to a deque-based BFS variant where edges of cost 0 go to the front and edges of cost 1 go to the back.

This transforms the problem into a shortest path in a 0-1 weighted graph, solvable in O(N + M) using 0-1 BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Dijkstra with heap | O(M log N) | O(N + M) | Accepted |
| 0-1 BFS | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We process the graph using a double-ended queue, maintaining the invariant that nodes closer to the front always have smaller current distance.

1. Build an adjacency list where each edge stores its destination and weight.
2. Initialize a distance array with infinity for all nodes except node 1, which is set to 0. This represents that we start in room 1 with no cost incurred.
3. Push node 1 into a deque. The deque will act like a priority structure where cheaper states are expanded first without using a heap.
4. While the deque is not empty, pop a node from the front. This ensures we always expand the currently known cheapest state.
5. For each outgoing edge from the current node, compute the candidate distance as current distance plus edge weight. If this value is smaller than the stored distance for the neighbor, update it.
6. If the edge weight is 0, push the neighbor to the front of the deque. If the edge weight is 1, push it to the back. This ordering ensures that all zero-cost transitions are processed before any cost-1 transitions at the same level of exploration.
7. Continue until the deque is empty.
8. The answer is the distance to node N, or -1 if it remains infinite.

### Why it works

The algorithm maintains the property that nodes are processed in non-decreasing order of distance. Any time we relax an edge of weight 0, we do not increase cost, so the resulting state must be processed as soon as possible, hence it is pushed to the front. Any edge of weight 1 increases cost, so it must wait behind all current zero-cost expansions.

Because all edge weights are only 0 or 1, any shortest path can be decomposed into a sequence where transitions are correctly ordered by this deque discipline. This guarantees that when a node is first finalized (popped), its distance is already minimal and will never be improved later.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n, m = map(int, input().split())
g = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v, t = map(int, input().split())
    g[u].append((v, t))

INF = 10**18
dist = [INF] * (n + 1)
dist[1] = 0

dq = deque([1])

while dq:
    u = dq.popleft()
    for v, w in g[u]:
        nd = dist[u] + w
        if nd < dist[v]:
            dist[v] = nd
            if w == 0:
                dq.appendleft(v)
            else:
                dq.append(v)

print(-1 if dist[n] == INF else dist[n])
```

The adjacency list stores directed edges exactly as given, preserving directionality. The distance array is initialized large enough to avoid overflow issues when adding 0 or 1 repeatedly.

The deque operations are the key implementation detail: appendleft is used only for zero-weight edges to ensure immediate propagation, while append is used for weight-1 edges to delay processing appropriately.

## Worked Examples

### Sample 1

Input:

```
5 6
1 2 0
2 3 1
3 5 0
1 4 1
4 5 1
2 5 1
```

We track distances and deque state:

| Step | Node popped | Distance | Updates |
| --- | --- | --- | --- |
| 1 | 1 | 0 | dist[2]=0, dist[4]=1 |
| 2 | 2 | 0 | dist[3]=1, dist[5]=1 |
| 3 | 4 | 1 | no improvement |
| 4 | 3 | 1 | dist[5]=1 (already equal) |
| 5 | 5 | 1 | end |

The best path is 1 → 2 → 3 → 5 with cost 1.

This trace shows how 0-cost edges are prioritized, allowing node 2 to be processed before node 4 even though both were discovered early.

### Sample 2

Input:

```
3 2
1 2 1
2 1 1
```

| Step | Node popped | Distance | Updates |
| --- | --- | --- | --- |
| 1 | 1 | 0 | dist[2]=1 |
| 2 | 2 | 1 | no update to 3 |

Node 3 remains unreachable, so the output is -1.

This demonstrates correct handling of disconnected components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each node is pushed into the deque at most once per successful relaxation, and each edge is processed once |
| Space | O(N + M) | Adjacency list plus distance array and deque |

The complexity fits comfortably within limits for N, M up to 100,000. The linear behavior avoids any logarithmic overhead that would still be acceptable but unnecessary.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    n, m = map(int, sys.stdin.readline().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, t = map(int, sys.stdin.readline().split())
        g[u].append((v, t))

    INF = 10**18
    dist = [INF] * (n + 1)
    dist[1] = 0

    dq = deque([1])
    while dq:
        u = dq.popleft()
        for v, w in g[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)

    return str(-1 if dist[n] == INF else dist[n])

# provided samples
assert run("""5 6
1 2 0
2 3 1
3 5 0
1 4 1
4 5 1
2 5 1
""") == "1"

assert run("""3 2
1 2 1
2 1 1
""") == "-1"

# custom cases
assert run("""2 1
1 2 0
""") == "0", "minimum case"

assert run("""2 1
1 2 1
""") == "1", "single edge cost 1"

assert run("""4 3
1 2 1
2 3 1
3 4 1
""") == "3", "all ones chain"

assert run("""4 4
1 2 0
2 3 0
3 4 0
1 4 1
""") == "0", "zero path dominates direct 1-edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1→2 single 0 | 0 | base 0-cost edge |
| 1→2 single 1 | 1 | single locked edge |
| chain of ones | 3 | accumulation of costs |
| all-zero path vs direct | 0 | shortest path preference |

## Edge Cases

One edge case is when multiple paths exist with mixed costs and a naive BFS would incorrectly lock in a worse early route. For example:

```
4 4
1 2 1
2 4 1
1 3 0
3 4 0
```

The correct path is 1 → 3 → 4 with cost 0. The algorithm first pushes node 3 to the front due to edge weight 0, so it fully propagates through the zero-cost chain before expanding higher-cost paths. Node 4 is reached with distance 0 before the 1-cost route from node 2 is ever finalized.

Another edge case is complete disconnection. If node N is never reached, its distance remains infinity and the algorithm correctly outputs -1 without requiring explicit reachability checks beyond the final comparison.
