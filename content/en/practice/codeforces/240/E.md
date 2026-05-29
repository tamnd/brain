---
title: "CF 240E - Road Repairs"
description: "We have a directed graph of cities and roads. City 1 is the capital. Every road is either already usable or broken. A broken road may be repaired, after which it behaves like a normal directed edge. The government wants every city to become reachable from the capital."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 240
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 145 (Div. 1, ACM-ICPC Rules)"
rating: 2800
weight: 240
solve_time_s: 118
verified: true
draft: false
---

[CF 240E - Road Repairs](https://codeforces.com/problemset/problem/240/E)

**Rating:** 2800  
**Tags:** dfs and similar, graphs, greedy  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed graph of cities and roads. City `1` is the capital. Every road is either already usable or broken. A broken road may be repaired, after which it behaves like a normal directed edge.

The government wants every city to become reachable from the capital. We are allowed to repair any subset of broken roads, and we must minimize how many repairs are performed.

The graph is directed, which changes the problem completely. A road from `u` to `v` helps only in that direction. Even if there is a path back, that does not help the capital reach the city.

The input gives every edge together with a flag:

- `0` means the road already works.
- `1` means the road is broken and can only be used if repaired.

The output is either:

- `-1` if some city is unreachable even after repairing every broken road, or
- the minimum number of repaired roads together with one valid set of edge indices.

The constraints are large: both `n` and `m` are up to `10^5`. Any algorithm that repeatedly runs graph traversals or recomputes reachability from scratch will fail. For example, trying every subset of broken roads is impossible, and even running BFS once per vertex would already become too slow.

A linear or near-linear graph algorithm is required. Something around `O(n + m)` is ideal.

Several edge cases are easy to mishandle.

Consider this graph:

```
1 -> 2 (broken)
2 -> 3 (good)
```

Input:

```
3 2
1 2 1
2 3 0
```

Repairing only the first edge is enough. A careless solution that separately minimizes repairs for every city could mistakenly count the same repaired edge multiple times.

Another dangerous case is unreachable components:

```
4 2
1 2 0
3 4 1
```

Cities `3` and `4` are disconnected from the capital even if every road is repaired. The correct answer is:

```
-1
```

Some implementations only search using currently good roads and incorrectly conclude that repairing one edge somewhere would help.

Cycles also matter:

```
3 3
1 2 1
2 3 0
3 2 0
```

Repairing edge `1 -> 2` unlocks both `2` and `3`. The optimal answer repairs one edge, not two.

The structure of the problem is global. We are not independently connecting cities. We are building one directed reachable region from the capital.

## Approaches

The brute-force idea is straightforward. Treat every broken edge as optional, try all subsets of broken edges, and check whether all vertices become reachable from the capital.

If there are `k` broken edges, this requires `2^k` subsets. Reachability checking costs `O(n + m)` each time. Even with only `40` broken edges, this becomes astronomically large.

A slightly smarter brute-force tries shortest paths independently for every city. Assign cost `0` to good edges and cost `1` to broken edges. Then compute the minimum repair count needed to reach every vertex.

This works for individual cities, but it does not solve the real optimization target. Different cities can share repaired edges. Summing independent shortest-path costs overcounts repairs.

The key observation is that we only care whether every vertex becomes reachable, not about minimizing each path separately.

Suppose we assign weight:

- `0` to good edges,
- `1` to broken edges.

Now imagine building a shortest path tree rooted at the capital, where the distance of a node means the minimum number of repaired edges needed to reach it.

If every node is reachable in this weighted graph, then selecting the parent edge used in the shortest path tree gives a globally optimal set of repaired roads.

Why does this work?

Every repaired edge in the final solution must appear somewhere on a path from the capital. A shortest path tree guarantees that each node is reached with the minimum possible number of repaired edges. More importantly, the union of all parent edges forms a directed arborescence. Any repaired edge in that tree contributes to reaching at least one new vertex. No repair is wasted.

Since edge weights are only `0` and `1`, we can compute shortest paths using 0-1 BFS in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over repaired subsets | $O(2^k \cdot (n+m))$ | $O(n+m)$ | Too slow |
| Independent shortest paths per city | $O(n(n+m))$ | $O(n+m)$ | Incorrect idea |
| 0-1 BFS + shortest path tree | $O(n+m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Build the directed graph.

For every edge, store:

- destination vertex,
- repair cost (`0` or `1`),
- original edge index.
2. Run 0-1 BFS from city `1`.

Moving through a good edge costs `0`.

Moving through a broken edge costs `1`.

Because all weights are either `0` or `1`, we can use a deque:

- push front for cost `0`,
- push back for cost `1`.

This computes the minimum number of repaired edges needed to reach every city.
3. While relaxing edges, store the parent edge that produced the best distance.

For each vertex `v`, keep:

- `parent[v]` = edge index used to reach `v`,
- `parent_cost[v]` = whether that edge is broken.
4. If some city remains unreachable, print `-1`.

This means no directed path exists even after repairing every broken edge.
5. Reconstruct the chosen repair set.

Every vertex except the capital has exactly one parent edge in the shortest path tree.

Traverse all vertices:

- if the parent edge is broken, add its index to the answer.
6. Output the collected edge indices.

The number of such edges is minimal.

### Why it works

The algorithm maintains the invariant that `dist[v]` equals the minimum number of repaired edges needed to reach `v` from the capital.

The parent pointers define a shortest path tree. Every vertex is connected to the capital through a path achieving this minimum repair count.

Suppose another solution repaired fewer roads overall. Then at least one vertex in our tree would need to be reached using fewer repaired edges than its shortest-path distance, which is impossible.

The selected repaired edges are exactly the broken edges that appear in the shortest path tree. Removing any one of them disconnects at least one subtree from the capital. Every chosen repair is necessary for the tree structure.

Because the tree reaches all vertices and uses the minimum possible number of repaired edges along every root-to-vertex path, the total number of repaired roads is globally minimal.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for idx in range(1, m + 1):
        a, b, c = map(int, input().split())
        graph[a].append((b, c, idx))

    INF = 10**18

    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)
    parent_cost = [0] * (n + 1)

    dist[1] = 0

    dq = deque([1])

    while dq:
        u = dq.popleft()

        for v, w, idx in graph[u]:
            nd = dist[u] + w

            if nd < dist[v]:
                dist[v] = nd
                parent[v] = idx
                parent_cost[v] = w

                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)

    for v in range(1, n + 1):
        if dist[v] == INF:
            print(-1)
            return

    ans = []

    for v in range(2, n + 1):
        if parent_cost[v] == 1:
            ans.append(parent[v])

    if not ans:
        print(0)
    else:
        print(len(ans))
        print(*ans)

solve()
```

The graph is stored as adjacency lists because the constraints are too large for adjacency matrices.

The central part of the implementation is the 0-1 BFS. Ordinary BFS only works for unweighted graphs, while Dijkstra would work but is unnecessarily expensive here. Since every edge weight is either `0` or `1`, a deque simulates Dijkstra in linear time.

When a relaxation improves `dist[v]`, the code also updates:

- the edge used to enter `v`,
- whether that edge required repair.

The shortest path tree is implicitly stored through these parent pointers.

One subtle point is that we only update when `nd < dist[v]`, not `<=`. Once a vertex already has an optimal distance, replacing it with another equal-distance parent is unnecessary.

Another important detail is unreachable detection. If a node still has distance `INF` after BFS, then even repairing all broken edges cannot connect it to the capital, because no directed path exists at all.

Finally, the answer is reconstructed by scanning parent edges. Every broken parent edge must be repaired.

## Worked Examples

### Example 1

Input:

```
3 2
1 3 0
3 2 1
```

| Step | Current Node | Relaxed Edge | New Distance | Parent |
| --- | --- | --- | --- | --- |
| Start | 1 | - | dist[1] = 0 | - |
| 1 | 1 | 1 → 3 (0) | dist[3] = 0 | edge 1 |
| 2 | 3 | 3 → 2 (1) | dist[2] = 1 | edge 2 |

Final distances:

| Vertex | Distance |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 0 |

The shortest path tree uses edge `1` and edge `2`. Only edge `2` is broken, so it must be repaired.

Output:

```
1
2
```

This trace shows how zero-cost edges propagate immediately through the deque while broken roads contribute one repair cost.

### Example 2

Input:

```
4 4
1 2 1
1 3 0
3 2 0
2 4 1
```

| Step | Current Node | Relaxed Edge | New Distance | Parent |
| --- | --- | --- | --- | --- |
| Start | 1 | - | dist[1] = 0 | - |
| 1 | 1 | 1 → 2 (1) | dist[2] = 1 | edge 1 |
| 2 | 1 | 1 → 3 (0) | dist[3] = 0 | edge 2 |
| 3 | 3 | 3 → 2 (0) | dist[2] = 0 | edge 3 |
| 4 | 2 | 2 → 4 (1) | dist[4] = 1 | edge 4 |

Final parent edges:

- vertex 2 uses edge 3,
- vertex 3 uses edge 2,
- vertex 4 uses edge 4.

Only edge `4` is broken inside the shortest path tree.

Output:

```
1
4
```

This example demonstrates why independent shortest paths are dangerous. A naive solution might repair edge `1 -> 2`, but the algorithm correctly discovers a free alternative path through city `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ | Every edge is processed a constant number of times in 0-1 BFS |
| Space | $O(n+m)$ | Adjacency lists, distance arrays, and parent arrays |

With `10^5` vertices and edges, linear complexity easily fits within the limits. The deque operations are all constant time, and memory usage stays proportional to the graph size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for idx in range(1, m + 1):
        a, b, c = map(int, input().split())
        graph[a].append((b, c, idx))

    INF = 10**18

    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)
    parent_cost = [0] * (n + 1)

    dist[1] = 0

    dq = deque([1])

    while dq:
        u = dq.popleft()

        for v, w, idx in graph[u]:
            nd = dist[u] + w

            if nd < dist[v]:
                dist[v] = nd
                parent[v] = idx
                parent_cost[v] = w

                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)

    for v in range(1, n + 1):
        if dist[v] == INF:
            print(-1)
            return out.getvalue()

    ans = []

    for v in range(2, n + 1):
        if parent_cost[v] == 1:
            ans.append(parent[v])

    if not ans:
        print(0)
    else:
        print(len(ans))
        print(*ans)

    return out.getvalue()

# provided sample
assert run(
    "3 2\n"
    "1 3 0\n"
    "3 2 1\n"
) == "1\n2\n"

# minimum size
assert run(
    "1 1\n"
    "1 1 0\n"
) == "0\n"

# unreachable component
assert run(
    "4 2\n"
    "1 2 0\n"
    "3 4 1\n"
) == "-1\n"

# all good roads
assert run(
    "3 2\n"
    "1 2 0\n"
    "2 3 0\n"
) == "0\n"

# alternative cheaper path
assert run(
    "4 4\n"
    "1 2 1\n"
    "1 3 0\n"
    "3 2 0\n"
    "2 4 1\n"
) == "1\n4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex graph | `0` | Capital already reaches all cities |
| Disconnected graph | `-1` | Detects impossible reachability |
| All roads good | `0` | No unnecessary repairs |
| Alternative free path | Repair only edge 4 | Confirms shortest-path-tree logic |
| Sample case | Repair edge 2 | Basic correctness |

## Edge Cases

Consider the disconnected graph:

```
4 2
1 2 0
3 4 1
```

The BFS starts from city `1` and only reaches city `2`. Cities `3` and `4` remain at distance `INF`.

The algorithm immediately prints:

```
-1
```

This is correct because no directed path from the capital exists, even if every broken road is repaired.

Now consider shared repairs:

```
3 2
1 2 1
2 3 0
```

Distances become:

- `dist[2] = 1`
- `dist[3] = 1`

Both cities depend on the same repaired edge `1 -> 2`. The shortest path tree contains only one broken edge, so the answer is:

```
1
1
```

A naive per-city approach could incorrectly count two repairs.

Finally, consider cycles:

```
3 3
1 2 1
2 3 0
3 2 0
```

The BFS repairs edge `1 -> 2` once, then the cycle between `2` and `3` is already usable through good roads.

The algorithm outputs:

```
1
1
```

The cycle does not confuse the parent-tree construction because every vertex keeps only the best known incoming edge.
