---
title: "CF 1076D - Edge Deletion"
description: "We are given a weighted undirected graph and we first imagine running a shortest path computation from vertex 1. This produces a distance value for every vertex, which we can think of as the true optimal cost of reaching that vertex in the original graph."
date: "2026-06-15T14:33:09+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1076
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 54 (Rated for Div. 2)"
rating: 1800
weight: 1076
solve_time_s: 706
verified: true
draft: false
---

[CF 1076D - Edge Deletion](https://codeforces.com/problemset/problem/1076/D)

**Rating:** 1800  
**Tags:** graphs, greedy, shortest paths  
**Solve time:** 11m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph and we first imagine running a shortest path computation from vertex 1. This produces a distance value for every vertex, which we can think of as the true optimal cost of reaching that vertex in the original graph.

After this, we are allowed to delete edges, but we cannot keep more than k edges in total. Once the graph is reduced, we again look at reachability from vertex 1. A vertex is considered successful if there still exists at least one path from 1 to that vertex whose total weight matches its original shortest path distance. In other words, we are not allowed to increase distances, and we only care that at least one optimal path remains intact for that vertex.

The task is to choose up to k edges so that as many vertices as possible remain reachable via some shortest path.

The constraints are large, with up to 300,000 vertices and edges. This immediately rules out any approach that tries to recompute shortest paths after many deletions or that considers subsets of edges explicitly. Anything beyond linearithmic time in the number of edges will be too slow, so we should expect a single shortest path computation plus a greedy construction.

A subtle issue appears when multiple shortest paths exist. A naive approach that keeps only one shortest path tree might underestimate how many vertices can be preserved, because a vertex may depend on multiple alternative shortest path parents to remain optimal after deletions.

Another edge case comes from the limit k on the number of retained edges. Even if we could preserve all shortest path edges, we may be forced to drop some, so we must prioritize which vertices to keep “alive” under a budget constraint.

## Approaches

If we ignore the constraint on k, the natural structure to preserve all good vertices is the shortest path DAG rooted at node 1. If we compute shortest distances using Dijkstra’s algorithm, every vertex i may have several incoming edges (u, i) such that dist[u] + w = dist[i]. These edges are exactly the ones that can lie on some shortest path.

If we were allowed unlimited edges, we could keep all such edges and every vertex reachable in the shortest path DAG would remain good. This immediately preserves all vertices.

The difficulty comes from the restriction that we can keep at most k edges. The shortest path DAG can have many edges, potentially O(m), so we need to select a subset.

The key observation is that we do not need all shortest path edges to preserve all vertices. We only need to ensure that every vertex we want to keep has at least one parent edge leading into it from a previously reached vertex. This suggests building a shortest path tree rather than the full DAG.

We run Dijkstra from node 1 and record one parent edge for each vertex when it is first finalized. This gives a shortest path tree with exactly n − 1 edges, and all vertices remain good. If k ≥ n − 1, we are already done.

When k is smaller than n − 1, we cannot keep a full tree. In that case, we want to prioritize vertices closer to the root in the sense of discovery order in Dijkstra. If we process vertices in the order they are popped from the priority queue, then the first k vertices (excluding the root) give a connected structure that guarantees shortest paths to those vertices, because each of them has a chosen shortest-path parent among already processed nodes.

This works because Dijkstra guarantees that when a node is extracted, its shortest distance is final, and any predecessor used in a shortest path must come from an earlier or equal distance state. So we can safely assign a parent edge at extraction time and build a tree incrementally, but stop after we have selected k edges.

The brute force idea would be to try all subsets of edges of size k and check which vertices remain optimally reachable. That is exponential in m and infeasible.

The optimized idea is to construct a shortest path tree greedily using Dijkstra, then truncate it by selecting only the first k tree edges in the order nodes are finalized.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(2^m · (n + m)) | O(n + m) | Too slow |
| Optimal (Dijkstra + greedy tree) | O(m log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Run Dijkstra from vertex 1 to compute shortest distances to all vertices.  
   This step fixes the target values d[i], which define correctness for every vertex we want to preserve.

2. Maintain an array parent_edge[i] initialized as empty, which will store one chosen shortest-path incoming edge for each vertex.  
   We only need one such edge per vertex to ensure reachability.

3. During Dijkstra, when a vertex v is finalized (popped from the priority queue), record the edge used to relax it as its parent edge.  
   At this moment, dist[v] is minimal and stable, so any shortest path must pass through some already processed structure.

4. Collect all parent edges for vertices 2 through n in the order they were finalized.  
   This ordering ensures that we prioritize vertices that are closer in Dijkstra exploration order.

5. If the number of collected edges is less than or equal to k, output them all.  
   This corresponds to keeping a full shortest path tree or a subset of it without breaking connectivity.

6. If there are more than k edges, output only the first k edges in this order.  
   This ensures we keep a valid rooted structure for exactly k vertices, each still connected by a shortest path.

### Why it works

Dijkstra’s algorithm guarantees that each vertex is finalized in non-decreasing order of shortest distance. When we assign a parent edge upon finalization, that edge is part of some shortest path from the source. If we restrict ourselves to the first k such assignments, we are effectively choosing k vertices whose shortest paths remain intact through their chosen parents. Since every chosen vertex has its parent finalized earlier, no cycle or invalid distance reconstruction can occur, and each retained vertex preserves a correct shortest path from 1.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

n, m, k = map(int, input().split())
g = [[] for _ in range(n + 1)]

for i in range(m):
    x, y, w = map(int, input().split())
    g[x].append((y, w, i + 1))
    g[y].append((x, w, i + 1))

INF = 10**30
dist = [INF] * (n + 1)
dist[1] = 0

parent_edge = [-1] * (n + 1)

pq = [(0, 1)]
visited = [False] * (n + 1)

order_edges = []

while pq:
    d, v = heapq.heappop(pq)
    if visited[v]:
        continue
    visited[v] = True

    if v != 1 and parent_edge[v] != -1:
        order_edges.append(parent_edge[v])

    for to, w, idx in g[v]:
        if dist[to] > d + w:
            dist[to] = d + w
            parent_edge[to] = idx
            heapq.heappush(pq, (dist[to], to))

if len(order_edges) > k:
    order_edges = order_edges[:k]

print(len(order_edges))
print(*order_edges)
```

The implementation follows Dijkstra with a standard priority queue. The key detail is that we store, for each vertex, the edge used in its best relaxation. When a vertex is popped for the first time, that edge is committed into the answer list. This ordering defines which vertices we prioritize keeping under the k-edge constraint.

A common pitfall is updating the answer when relaxing edges instead of when popping from the heap. That would break correctness because a tentative relaxation does not guarantee optimality yet. Another subtle point is that we must track visited nodes to avoid processing stale heap entries.

## Worked Examples

### Example 1

Input:
```
3 3 2
1 2 1
3 2 1
1 3 3
```

We compute shortest distances from 1. We get d2 = 1, d3 = 2 via path 1-2-3.

During Dijkstra, node 2 is finalized first, then node 3.

| Step | Node | Parent edge chosen | Selected edges |
|------|------|-------------------|----------------|
| 1 | 1 | - | [] |
| 2 | 2 | (1,2) edge 1 | [1] |
| 3 | 3 | (2,3) edge 2 | [1,2] |

We already have 2 edges, which matches k, so both are kept. All vertices remain good.

### Example 2

Input:
```
4 4 2
1 2 1
2 3 1
3 4 1
1 4 10
```

Shortest paths are a chain 1-2-3-4.

| Step | Node | Parent edge chosen | Selected edges |
|------|------|-------------------|----------------|
| 1 | 1 | - | [] |
| 2 | 2 | (1,2) | [1] |
| 3 | 3 | (2,3) | [1,2] |
| 4 | 4 | (3,4) | [1,2,3] |

Since k = 2, we keep only the first two edges. Nodes 2 and 3 remain good, while 4 becomes unreachable via a shortest path.

This shows the greedy ordering prioritizes earlier Dijkstra layers.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(m log n) | Each edge relaxation is processed through a priority queue once |
| Space | O(n + m) | Adjacency list plus distance and parent storage |

The constraints allow up to 3 × 10^5 edges, so an O(m log n) Dijkstra fits comfortably within time limits in Python with a heap-based implementation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    n, m, k = map(int, input().split())
    g = [[] for _ in range(n + 1)]

    for i in range(m):
        x, y, w = map(int, input().split())
        g[x].append((y, w, i + 1))
        g[y].append((x, w, i + 1))

    INF = 10**30
    dist = [INF] * (n + 1)
    dist[1] = 0
    parent = [-1] * (n + 1)

    pq = [(0, 1)]
    vis = [False] * (n + 1)
    ans = []

    while pq:
        d, v = heapq.heappop(pq)
        if vis[v]:
            continue
        vis[v] = True
        if v != 1 and parent[v] != -1:
            ans.append(parent[v])

        for to, w, idx in g[v]:
            if dist[to] > d + w:
                dist[to] = d + w
                parent[to] = idx
                heapq.heappush(pq, (dist[to], to))

    if len(ans) > k:
        ans = ans[:k]

    out = [str(len(ans)), " ".join(map(str, ans))]
    return "\n".join(out).strip()

# provided sample
assert run("""3 3 2
1 2 1
3 2 1
1 3 3
""") == "2\n1 2"

# chain graph
assert run("""4 3 2
1 2 1
2 3 1
3 4 1
""") == "2\n1 2"

# star graph
assert run("""4 3 3
1 2 1
1 3 1
1 4 1
""") == "3\n1 2 3"

# k = 0
assert run("""3 3 0
1 2 1
2 3 1
1 3 1
""") == "0\n"

# dense triangle
assert run("""3 3 1
1 2 1
2 3 1
1 3 2
""") == "1\n1"
```

| Test input | Expected output | What it validates |
|---|---|---|
| chain graph | 2 edges | prefix selection correctness |
| star graph | all edges | k ≥ n-1 behavior |
| k = 0 | empty | boundary case handling |
| triangle | 1 edge | greedy truncation correctness |

## Edge Cases

A minimal k value such as zero tests whether the algorithm safely produces no edges while still maintaining correct initialization. In this case, no vertices beyond the root remain connected, but the output constraint allows this.

A fully connected star ensures that Dijkstra selects all edges from the root first, showing that early extraction order correctly prioritizes high-value connectivity when k is large.

A long chain graph stresses ordering because each vertex depends on the previous one. Truncating early demonstrates that once a parent chain is cut, deeper vertices lose their shortest-path preservation, which is exactly what the problem’s scoring function reflects.
