---
title: "CF 2214E - Shortest Paths"
description: "We are given a weighted undirected graph with up to a hundred vertices. Each edge connects two numbered nodes and has a non-negative cost."
date: "2026-06-07T19:01:45+07:00"
tags: ["codeforces", "competitive-programming", "*special", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2214
codeforces_index: "E"
codeforces_contest_name: "April Fools Day Contest 2026"
rating: 0
weight: 2214
solve_time_s: 70
verified: true
draft: false
---

[CF 2214E - Shortest Paths](https://codeforces.com/problemset/problem/2214/E)

**Rating:** -  
**Tags:** *special, shortest paths  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph with up to a hundred vertices. Each edge connects two numbered nodes and has a non-negative cost. The task is to compute the minimum possible distance from node 1 to every other node, where distance means the sum of edge weights along a chosen path.

The input can be interpreted as a network of cities connected by roads with travel costs. Starting from city 1, we want to know the cheapest way to reach every other city, or determine that a city cannot be reached at all.

The constraints are small enough that classical shortest path methods are sufficient. With at most 100 nodes, an adjacency matrix or adjacency list both fit comfortably. The number of edges can reach about 5000 in the worst case, so any solution with roughly quadratic or slightly super-quadratic behavior will still run quickly. This immediately rules out any exponential search over paths, but even more importantly it makes standard Dijkstra with a binary heap more than fast enough.

A subtle edge case appears when some nodes are disconnected from node 1. In such cases, the correct output is -1, not 0 or infinity or a large sentinel value.

Another important corner case is zero-weight edges. Since weights can be zero, any algorithm relying on simple BFS or assuming strictly positive weights will fail. For example, if we had a chain like 1-2 (0), 2-3 (5), then node 3 is reachable with cost 5, but naive BFS would incorrectly treat all edges equally.

A third issue arises from multiple edges between the same pair of nodes. Since the graph is not guaranteed to be simple in input interpretation, a careless implementation that overwrites adjacency entries instead of keeping the minimum weight edge could incorrectly increase distances.

## Approaches

A brute-force idea is to try all possible paths from node 1 to every other node, keeping track of the minimum cost encountered. Conceptually, this is correct because it explores the entire search space of walks in the graph. However, the number of paths grows exponentially. Even in a graph with modest branching factor, the number of distinct walks of length up to n can explode beyond any feasible limit. This becomes especially apparent in dense graphs, where each node connects to many others and revisiting states creates an unbounded combinatorial expansion.

The key structural observation is that once we know the shortest distance to a node, we never need to reconsider a longer way of reaching it. This monotonic “finalization” property holds because all edge weights are non-negative. It allows us to greedily expand from the currently closest unreached node, always locking in the optimal distance in increasing order. This is exactly the setting where Dijkstra’s algorithm applies.

The improvement comes from replacing global path enumeration with local relaxation. Instead of exploring full paths, we repeatedly improve best-known distances using edges leaving already-reached nodes, always prioritizing the smallest tentative distance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Paths | Exponential | O(n) recursion | Too slow |
| Dijkstra (heap) | O(m log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list where each node stores pairs of neighbor and edge weight. This representation is necessary because we repeatedly traverse outgoing edges efficiently during relaxation.
2. Initialize a distance array with infinity for all nodes except node 1, which is set to 0. This encodes the fact that we start at node 1 with no cost.
3. Push the pair (0, 1) into a priority queue. The queue always stores candidate states ordered by current known shortest distance.
4. Repeatedly extract the node with the smallest tentative distance from the queue. This node represents the closest not-yet-finalized vertex under current knowledge.
5. If the extracted distance is larger than the stored distance for that node, skip it. This happens because a better path was already found and pushed later into the queue.
6. For each neighbor of the current node, compute the candidate distance through this node. If it improves the stored distance, update it and push the new pair into the priority queue.
7. Continue until the priority queue is empty, meaning all reachable nodes have been processed in increasing distance order.
8. Output the final distances for nodes 2 through n, replacing unreachable nodes (still infinity) with -1.

The reason step 5 is essential is that the same node can appear multiple times in the queue with outdated distances. Without skipping stale entries, we would incorrectly relax edges using suboptimal values and increase runtime significantly.

### Why it works

At every moment, when a node is popped from the priority queue with distance d, we claim that d is the smallest possible distance from node 1 to that node. This holds because all edge weights are non-negative, so any alternative path reaching this node later must have accumulated at least as much cost as the best currently discovered path. Therefore, once a node is popped, its distance is finalized and will never be improved. This invariant ensures that all relaxations propagate correct minimal distances outward.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    INF = 10**18
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
    
    for i in range(2, n + 1):
        if dist[i] == INF:
            print(-1)
        else:
            print(dist[i])

if __name__ == "__main__":
    solve()
```

The adjacency list construction ensures each undirected edge is usable in both directions. The distance array is initialized with a large sentinel to represent unknown shortest paths. The priority queue always expands the currently best-known frontier node.

The stale-entry check `if d != dist[u]` prevents outdated queue entries from triggering unnecessary relaxations. This is the standard optimization that keeps Dijkstra efficient under repeated updates.

Finally, unreachable nodes remain at infinity and are converted to -1 in output.

## Worked Examples

### Example 1

Input:

```
2 1
1 2 1
```

We start with dist[1] = 0 and dist[2] = INF.

| Step | PQ state | Chosen node | dist[2] |
| --- | --- | --- | --- |
| init | (0,1) | - | INF |
| pop 1 | empty | 1 | INF |
| relax (1→2) | (1,2) | - | 1 |
| pop 2 | empty | 2 | 1 |

This shows a single relaxation directly updates node 2, and no alternative paths exist.

Output:

```
1
```

### Example 2

Input:

```
4 4
1 2 1
2 3 2
1 3 10
3 4 1
```

We track shortest distances as they improve.

| Step | PQ state | Chosen node | dist[2] | dist[3] | dist[4] |
| --- | --- | --- | --- | --- | --- |
| init | (0,1) | - | INF | INF | INF |
| pop 1 | (1,2),(10,3) | 1 | 1 | 10 | INF |
| pop 2 | (3,3),(10,3) | 2 | 1 | 3 | INF |
| pop 3 | (4,4),(10,3) | 3 | 1 | 3 | 4 |
| pop 4 | (10,3) | 4 | 1 | 3 | 4 |

The direct edge 1→3 is worse than the path 1→2→3, and Dijkstra correctly corrects this when processing node 2 first.

Output:

```
1
3
4
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each edge relaxation may push a heap entry, each heap operation costs log n |
| Space | O(n + m) | adjacency list plus distance array and heap |

With n ≤ 100 and m up to about 5000, this is comfortably within limits. Even in the worst case, the heap operations are negligible.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, sys.stdin.readline().split())
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        u, v, w = map(int, sys.stdin.readline().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    INF = 10**18
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
    
    out = []
    for i in range(2, n + 1):
        out.append(str(-1 if dist[i] == INF else dist[i]))
    
    return "\n".join(out)

# provided sample
assert run("2 1\n1 2 1\n") == "1"

# disconnected node
assert run("3 1\n1 2 5\n") == "5\n-1"

# zero-weight edges
assert run("3 2\n1 2 0\n2 3 5\n") == "0\n5"

# multiple edges
assert run("3 3\n1 2 10\n1 2 3\n2 3 1\n") == "3\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1, 1 2 5 | 5, -1 | unreachable node handling |
| zero-weight chain | 0, 5 | correctness with zero edges |
| duplicate edges | 3, 4 | minimum edge handling |

## Edge Cases

A disconnected node scenario shows how infinity is preserved. Consider:

```
3 1
1 2 5
```

Node 3 is never reached. The algorithm never pushes it into the queue, so its distance remains INF and is printed as -1.

A zero-weight edge case:

```
3 2
1 2 0
2 3 5
```

Initially dist[2] becomes 0. When processing node 2, it relaxes edge to 3 with cost 5. The final result correctly reflects that zero-cost traversal is allowed without violating Dijkstra’s ordering.

A multiple-edge case:

```
3 3
1 2 10
1 2 1
2 3 1
```

The second edge improves dist[2] to 1, and all later relaxations use this improved value, ensuring correctness even when input contains redundant or dominated edges.
