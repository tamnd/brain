---
title: "CF 20C - Dijkstra?"
description: "We are given an undirected weighted graph. Every edge connects two vertices and has a positive cost. The task is to start at vertex 1, reach vertex n, and print one shortest path. If no route exists, we print -1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 20
codeforces_index: "C"
codeforces_contest_name: "Codeforces Alpha Round 20 (Codeforces format)"
rating: 1900
weight: 20
solve_time_s: 96
verified: true
draft: false
---
[CF 20C - Dijkstra?](https://codeforces.com/problemset/problem/20/C)

**Rating:** 1900  
**Tags:** graphs, shortest paths  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph. Every edge connects two vertices and has a positive cost. The task is to start at vertex `1`, reach vertex `n`, and print one shortest path. If no route exists, we print `-1`.

The graph is large enough that we cannot explore all possible paths. With up to `10^5` vertices and `10^5` edges, any algorithm close to `O(n^2)` is already risky in Python, and anything exponential is impossible. The graph is sparse, since the number of edges is on the same order as the number of vertices, which strongly suggests adjacency lists instead of adjacency matrices.

The edge weights are all positive. That detail changes the problem completely. Positive weights allow Dijkstra's algorithm to work, because once we finalize the shortest distance to a node, no future path can improve it.

The problem also asks for the actual path, not only the minimum distance. That means we must remember how we reached each vertex during relaxation.

Several edge cases are easy to mishandle.

A graph may be disconnected.

Input:

```
3 1
1 2 5
```

There is no path from `1` to `3`, so the correct output is:

```
-1
```

A careless implementation might still try to reconstruct a path and crash because no parent exists for node `3`.

The graph may contain multiple edges between the same pair of vertices.

Input:

```
3 3
1 2 10
1 2 1
2 3 2
```

The shortest path is:

```
1 2 3
```

with total cost `3`. If we overwrite edges or assume uniqueness, we may accidentally keep the heavier edge.

The graph may contain self-loops.

Input:

```
2 2
1 1 5
1 2 3
```

The loop on node `1` should simply be ignored naturally by the relaxation process. A buggy implementation may accidentally keep relaxing the same node forever if stale states are not handled correctly.

The shortest path can involve very large distances. Edge weights are up to `10^6`, and paths may contain many edges, so total distance can exceed 32-bit integer range. Python integers handle this automatically, but in languages like C++ we would need `long long`.

## Approaches

The brute-force idea is to enumerate all possible paths from `1` to `n`, compute their costs, and keep the minimum. This works logically because every valid route is checked, so the optimal one cannot be missed.

The problem is that the number of simple paths in a graph can grow exponentially. Even a moderately connected graph can contain millions or billions of paths. With `10^5` vertices, brute force is completely infeasible.

A slightly better naive approach is to use BFS-style relaxation repeatedly, similar to Bellman-Ford. Bellman-Ford works correctly even with negative weights, because it repeatedly improves distances until no shorter path exists. Its complexity is `O(n * m)`. Here that becomes roughly `10^10` operations in the worst case, far beyond the time limit.

The key observation is that every edge weight is positive. Positive weights give shortest paths a monotonic structure: once we extract the currently smallest tentative distance, no future path can improve it. That property is exactly what Dijkstra's algorithm relies on.

Dijkstra maintains the best known distance to every node and always expands the closest unprocessed node first. Using a priority queue keeps extraction efficient. Since the graph is sparse, adjacency lists plus a heap give complexity `O((n + m) log n)`, which easily fits the constraints.

We also store a `parent` array. Whenever we improve the shortest distance to a node, we record which previous node produced that improvement. After Dijkstra finishes, we reconstruct the path by walking backward from `n` to `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Path Enumeration | Exponential | O(n) | Too slow |
| Bellman-Ford | O(nm) | O(n) | Too slow |
| Dijkstra with Heap | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph.

Since the graph is undirected, every edge `(u, v, w)` must be added in both directions.
2. Create a distance array initialized with infinity.

`dist[x]` stores the shortest distance currently known from node `1` to node `x`. Initially only `dist[1] = 0`.
3. Create a parent array initialized with `-1`.

`parent[x]` remembers the previous node on the shortest path to `x`. This allows path reconstruction later.
4. Push `(0, 1)` into a min-heap.

The heap always gives us the node with the smallest tentative distance.
5. Repeatedly pop the smallest state from the heap.

Suppose we pop `(d, u)`. If `d` is not equal to `dist[u]`, this state is stale and should be skipped.

Multiple copies of the same node can exist in the heap because a shorter route may be discovered later.
6. Relax every edge leaving `u`.

For each neighbor `(v, w)`, check whether:

```
dist[u] + w < dist[v]
```

If true, we found a shorter route to `v`.
7. Update the distance and parent arrays.

Set:

```
dist[v] = dist[u] + w
parent[v] = u
```

Then push the updated state into the heap.
8. After the heap becomes empty, check `dist[n]`.

If it is still infinity, node `n` is unreachable and we print `-1`.
9. Reconstruct the path.

Start from node `n` and repeatedly move to `parent[cur]` until reaching `1`. Reverse the collected sequence before printing.

### Why it works

Dijkstra's algorithm relies on the fact that all edge weights are positive. When the heap extracts a node `u` with the smallest tentative distance, every other unprocessed path must already be at least as expensive. Any alternative route reaching `u` later would need to pass through another node whose distance is not smaller, and then add a positive edge weight, so it cannot improve `dist[u]`.

Because of that property, once a node is processed with its current best distance, that value is final.

The parent array always records the edge that produced the best known distance. Since distances only improve toward the true shortest values, the final parent chain reconstructs a valid shortest path.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

n, m = map(int, input().split())

graph = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))
    graph[v].append((u, w))

dist = [INF] * (n + 1)
parent = [-1] * (n + 1)

dist[1] = 0

pq = [(0, 1)]

while pq:
    d, u = heapq.heappop(pq)

    if d != dist[u]:
        continue

    for v, w in graph[u]:
        nd = d + w

        if nd < dist[v]:
            dist[v] = nd
            parent[v] = u
            heapq.heappush(pq, (nd, v))

if dist[n] == INF:
    print(-1)
else:
    path = []

    cur = n

    while cur != -1:
        path.append(cur)
        cur = parent[cur]

    path.reverse()

    print(*path)
```

The adjacency list keeps memory usage linear in the number of edges. With up to `10^5` edges, this is much more efficient than a matrix, which would require `10^10` cells.

The heap stores pairs `(distance, node)`. Python's `heapq` implements a min-heap, so the smallest distance is always processed first.

The stale-state check:

```
if d != dist[u]:
    continue
```

is essential. Suppose node `u` was previously pushed with distance `10`, and later we found a better path with distance `5`. Both states remain inside the heap. When the outdated `(10, u)` eventually appears, we must ignore it. Without this check, the algorithm still stays correct but performs unnecessary relaxations and may become too slow.

The parent update happens exactly when a shorter path is discovered. That guarantees the reconstructed chain corresponds to the final shortest distances.

Path reconstruction walks backward from `n` toward `1`. Since parents point in reverse order, we reverse the collected array before printing.

Using a large integer like `10**30` for infinity is safe because the maximum possible shortest distance is far smaller than that.

## Worked Examples

### Example 1

Input:

```
5 6
1 2 2
2 5 5
2 3 4
1 4 1
4 3 3
3 5 1
```

| Heap Pop | Relaxed Edge | Updated Distance | Parent Change |
| --- | --- | --- | --- |
| (0, 1) | 1 → 2 (2) | dist[2] = 2 | parent[2] = 1 |
| (0, 1) | 1 → 4 (1) | dist[4] = 1 | parent[4] = 1 |
| (1, 4) | 4 → 3 (3) | dist[3] = 4 | parent[3] = 4 |
| (2, 2) | 2 → 5 (5) | dist[5] = 7 | parent[5] = 2 |
| (4, 3) | 3 → 5 (1) | dist[5] = 5 | parent[5] = 3 |
| (5, 5) | none | final | final |

Final parent chain:

```
5 ← 3 ← 4 ← 1
```

Reversed path:

```
1 4 3 5
```

This trace shows how a node's distance can improve multiple times. Node `5` first receives distance `7`, then later improves to `5`.

### Example 2

Input:

```
4 2
1 2 5
3 4 1
```

| Heap Pop | Relaxed Edge | Updated Distance |
| --- | --- | --- |
| (0, 1) | 1 → 2 (5) | dist[2] = 5 |
| (5, 2) | none | none |

Nodes `3` and `4` are never reached.

Final distances:

```
dist = [∞, 0, 5, ∞, ∞]
```

Since `dist[4]` remains infinity, the algorithm prints:

```
-1
```

This example demonstrates correct handling of disconnected graphs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Every edge relaxation may push into the heap, and heap operations cost logarithmic time |
| Space | O(n + m) | Adjacency list, distance array, parent array, and heap storage |

With `10^5` vertices and edges, this complexity is fully acceptable. Heap operations remain efficient, and linear memory usage fits comfortably inside the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    INF = 10**30

    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))

    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)

    dist[1] = 0

    pq = [(0, 1)]

    while pq:
        d, u = heapq.heappop(pq)

        if d != dist[u]:
            continue

        for v, w in graph[u]:
            nd = d + w

            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    if dist[n] == INF:
        return "-1"

    path = []

    cur = n

    while cur != -1:
        path.append(cur)
        cur = parent[cur]

    path.reverse()

    return " ".join(map(str, path))

# provided sample
assert run(
"""5 6
1 2 2
2 5 5
2 3 4
1 4 1
4 3 3
3 5 1
"""
) == "1 4 3 5", "sample 1"

# disconnected graph
assert run(
"""3 1
1 2 5
"""
) == "-1", "disconnected graph"

# multiple edges
assert run(
"""3 3
1 2 10
1 2 1
2 3 2
"""
) == "1 2 3", "multiple edges"

# self-loop
assert run(
"""2 2
1 1 5
1 2 3
"""
) == "1 2", "self loop handling"

# minimum graph
assert run(
"""2 1
1 2 1
"""
) == "1 2", "minimum valid graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Disconnected graph | `-1` | Correct unreachable handling |
| Multiple edges between same nodes | `1 2 3` | Chooses minimum-weight edge |
| Self-loop present | `1 2` | Loops do not break relaxation |
| Minimum valid graph | `1 2` | Boundary size correctness |

## Edge Cases

Consider the disconnected graph:

```
3 1
1 2 5
```

The algorithm starts from node `1`, relaxes node `2`, and then the heap becomes empty. Node `3` is never reached, so:

```
dist[3] = INF
```

The final check detects this and prints:

```
-1
```

No path reconstruction is attempted, so there is no invalid parent access.

Now consider multiple edges:

```
3 3
1 2 10
1 2 1
2 3 2
```

When processing node `1`, both edges to node `2` are examined. The first gives distance `10`, but the second improves it to `1`.

The final distances become:

```
dist[2] = 1
dist[3] = 3
```

The parent chain reconstructs:

```
1 → 2 → 3
```

The algorithm naturally handles parallel edges because every edge is relaxed independently.

Finally, consider a self-loop:

```
2 2
1 1 5
1 2 3
```

When node `1` is processed, the loop edge proposes:

```
0 + 5 = 5
```

for node `1` itself. Since `dist[1]` is already `0`, no update happens.

The normal edge to node `2` gives:

```
dist[2] = 3
```

The output becomes:

```
1 2
```

The self-loop has no effect, exactly as expected.
