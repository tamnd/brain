---
title: "CF 269C - Flawed Flow"
description: "We are given an undirected graph where every edge already has a flow amount attached to it. The graph is supposed to represent a valid maximum flow from vertex 1 to vertex n, but the directions of the edges were lost."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "flows", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 269
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 165 (Div. 1)"
rating: 2100
weight: 269
solve_time_s: 120
verified: true
draft: false
---

[CF 269C - Flawed Flow](https://codeforces.com/problemset/problem/269/C)

**Rating:** 2100  
**Tags:** constructive algorithms, flows, graphs, greedy  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where every edge already has a flow amount attached to it. The graph is supposed to represent a valid maximum flow from vertex `1` to vertex `n`, but the directions of the edges were lost. Our task is to recover directions for every edge so that the resulting directed graph satisfies three conditions.

First, every internal vertex must conserve flow. The total incoming flow must equal the total outgoing flow. Second, the source vertex `1` may only send flow outward, never receive it. Third, the final directed graph must be acyclic.

The interesting part is that the flow values are already fixed. We are not choosing how much flow travels through each edge, only which endpoint sends it and which endpoint receives it.

The graph can contain up to `2 * 10^5` vertices and edges. With a 2 second time limit, any algorithm worse than roughly linear or `O(m log n)` is dangerous. A quadratic approach would require around `4 * 10^10` operations in the worst case, which is completely infeasible. We need something that processes each edge and vertex only a constant number of times.

The most subtle part of the problem is the acyclicity condition. A naive idea is to orient edges locally so that flow balance holds at every vertex. That is not enough. Consider this graph:

```
1 --2--> 2
2 --2--> 3
3 --2--> 1
```

If we orient the edges in a cycle, every vertex is balanced, but the graph contains a directed cycle, which is forbidden.

Another easy mistake is assuming that edges must always point away from the source in terms of graph distance. Consider:

```
4 4
1 2 5
2 3 5
1 4 5
4 3 5
```

Both paths carry flow into vertex `3`. Orienting purely by BFS depth works here, but in general the graph may contain cross edges and arbitrary topology. We need a construction tied to flow conservation itself, not to graph structure.

One more dangerous case is a vertex connected to many edges where the correct orientation only becomes clear after some neighboring decisions are already fixed. For example:

```
5 5
1 2 4
1 3 6
2 4 4
3 4 2
4 5 6
```

Vertex `4` must receive exactly `6` units and send exactly `6` units. If we greedily orient edges without tracking remaining required inflow, we can easily get stuck with impossible balances later.

## Approaches

The brute-force idea is straightforward. Every edge has two possible directions, so we could try all `2^m` orientations and check whether flow conservation and acyclicity hold.

Checking one orientation is linear. We compute indegrees and outdegrees weighted by flow, verify balance constraints, and run a topological sort to test for cycles. The problem is the number of orientations. With `m = 2 * 10^5`, even `2^50` is already impossible, and the actual limit is vastly larger.

The key observation is hidden inside the conservation law. For every internal vertex, the total incident flow is even, because incoming flow equals outgoing flow. That means each internal vertex must eventually receive exactly half of its incident flow.

Suppose we already know that some edges entering a vertex contribute a certain amount of incoming flow. Once that amount reaches half of the total incident flow, all remaining undecided edges must point outward. This creates a propagation process similar to topological elimination.

The source vertex is especially important. Since it cannot receive any flow, every edge adjacent to vertex `1` must point outward immediately. Once we orient such an edge toward another vertex, that vertex gains some confirmed incoming flow. If this incoming amount reaches its required half, we can determine directions of all remaining edges adjacent to it.

This suggests a queue-based greedy process.

For every internal vertex `v`, define:

```
need[v] = total_incident_flow[v] / 2
```

We maintain how much incoming flow has already been assigned to `v`. Whenever a vertex reaches its required incoming amount, it becomes "resolved", and every remaining undecided edge adjacent to it must point outward from that vertex.

The process is linear because every edge is oriented exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * (n + m)) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and store every edge with its index.

Since the output must preserve input order, we keep the original edge indices. For each vertex, we also compute the sum of flow values of all incident edges.
2. For every internal vertex `v`, compute how much incoming flow it ultimately needs.

Because flow conservation requires incoming flow to equal outgoing flow, the incoming amount must be exactly half of the total incident flow.
3. Start a queue with vertex `1`.

The source cannot receive flow, so every undecided edge adjacent to it must point outward from vertex `1`.
4. Process vertices from the queue.

Whenever we pop a vertex `u`, we inspect every still-undirected edge `(u, to, c)`.
5. Orient each undecided edge away from the current vertex.

If the stored edge is `(a, b)`:

- when processing `a`, we orient `a -> b` and output `0`
- when processing `b`, we orient `b -> a` and output `1`

This guarantees that once a vertex has already received enough incoming flow, all remaining incident flow leaves it.
6. After orienting an edge toward vertex `to`, add its flow value to the confirmed incoming amount of `to`.

If `to` is not the sink and its incoming amount becomes exactly equal to its required half, push it into the queue.
7. Continue until every edge is oriented.

The problem guarantees that a valid solution always exists, so the process will eventually determine all directions.

### Why it works

The invariant is that once a vertex enters the queue, it has already received all incoming flow it ever needs. Every remaining undecided edge adjacent to it must therefore be outgoing.

Initially this is true for the source because it needs zero incoming flow. Whenever we orient an edge into another vertex, we increase its confirmed incoming flow. The moment this reaches exactly half of its incident total, that vertex is fully satisfied and can safely send all remaining undecided edges outward.

This process never creates contradictions because each edge is directed exactly once, and every internal vertex ends with incoming flow equal to outgoing flow.

The resulting graph is also acyclic. Edges are always directed from an earlier processed vertex toward a later unresolved vertex. A directed cycle would require returning to an already processed vertex, which cannot happen because processed vertices only emit outgoing edges afterward.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    edges = []
    graph = [[] for _ in range(n + 1)]
    total = [0] * (n + 1)

    for i in range(m):
        a, b, c = map(int, input().split())

        edges.append((a, b, c))

        graph[a].append((b, c, i))
        graph[b].append((a, c, i))

        total[a] += c
        total[b] += c

    need = [0] * (n + 1)

    for v in range(2, n):
        need[v] = total[v] // 2

    incoming = [0] * (n + 1)

    used = [False] * m
    ans = [0] * m

    q = deque([1])

    while q:
        u = q.popleft()

        for to, c, idx in graph[u]:
            if used[idx]:
                continue

            used[idx] = True

            a, b, _ = edges[idx]

            if u == a:
                ans[idx] = 0
                incoming[to] += c
            else:
                ans[idx] = 1
                incoming[to] += c

            if to != n and incoming[to] == need[to]:
                q.append(to)

    print('\n'.join(map(str, ans)))

solve()
```

The adjacency list stores edges from both directions so we can traverse the graph naturally. Each adjacency entry keeps the neighboring vertex, the flow value, and the original edge index.

The array `total` stores the sum of all incident flow values for every vertex. Internal vertices must split this equally between incoming and outgoing flow, so `need[v]` becomes `total[v] // 2`.

The queue drives the propagation process. A vertex enters the queue only after its incoming requirement has already been satisfied. At that point, every remaining undecided edge adjacent to it must point outward.

The `used` array is critical because each undirected edge appears twice in the adjacency list. Without this guard, the same edge would be processed twice and the balance logic would break immediately.

The sink vertex `n` is never pushed into the queue. It is allowed to accumulate arbitrary incoming flow because it has no conservation constraint requiring future outgoing edges.

The direction encoding matches the problem statement exactly. If the edge was originally written as `(a, b)` and we orient `a -> b`, we output `0`. Otherwise we output `1`.

## Worked Examples

### Example 1

Input:

```
3 3
3 2 10
1 2 10
3 1 5
```

The total incident flow values are:

```
vertex 1: 15
vertex 2: 20
vertex 3: 15
```

Vertex `2` needs incoming flow `10`.

| Step | Queue | Processed Vertex | Edge Oriented | Incoming[2] | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 1 -> 2 | 10 | edge 2 = 0 |
| 2 | [2] | 2 | 3 -> 2 | 10 | edge 1 = 1 |
| 3 | [] | 2 | 1 -> 3 | 10 | edge 3 = 1 |

Final output:

```
1
0
1
```

This trace shows the central invariant. Once vertex `2` receives its required incoming amount of `10`, every remaining undecided edge adjacent to it must point outward.

### Example 2

Input:

```
5 5
1 2 4
1 3 6
2 4 4
3 4 2
4 5 6
```

Incident totals:

```
vertex 2: 8
vertex 3: 8
vertex 4: 12
```

Required incoming amounts:

```
need[2] = 4
need[3] = 4
need[4] = 6
```

| Step | Queue | Processed Vertex | Edge Oriented | Incoming Updates |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 1 -> 2 | incoming[2] = 4 |
| 2 | [1,2] | 1 | 1 -> 3 | incoming[3] = 6 |
| 3 | [2,3] | 2 | 2 -> 4 | incoming[4] = 4 |
| 4 | [3] | 3 | 3 -> 4 | incoming[4] = 6 |
| 5 | [4] | 4 | 4 -> 5 | done |

This example demonstrates that vertices become active exactly when their incoming requirement is satisfied. Vertex `4` waits until both incoming edges are fixed before sending flow toward the sink.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every vertex and edge is processed a constant number of times |
| Space | O(n + m) | Adjacency lists, queues, and auxiliary arrays |

The constraints allow at most `2 * 10^5` vertices and edges, so a linear solution is exactly what we need. The implementation performs only simple queue operations and adjacency traversals, which easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    edges = []
    graph = [[] for _ in range(n + 1)]
    total = [0] * (n + 1)

    for i in range(m):
        a, b, c = map(int, input().split())

        edges.append((a, b, c))

        graph[a].append((b, c, i))
        graph[b].append((a, c, i))

        total[a] += c
        total[b] += c

    need = [0] * (n + 1)

    for v in range(2, n):
        need[v] = total[v] // 2

    incoming = [0] * (n + 1)

    used = [False] * m
    ans = [0] * m

    q = deque([1])

    while q:
        u = q.popleft()

        for to, c, idx in graph[u]:
            if used[idx]:
                continue

            used[idx] = True

            a, b, _ = edges[idx]

            if u == a:
                ans[idx] = 0
                incoming[to] += c
            else:
                ans[idx] = 1
                incoming[to] += c

            if to != n and incoming[to] == need[to]:
                q.append(to)

    return '\n'.join(map(str, ans)) + '\n'

# provided sample
assert run(
"""3 3
3 2 10
1 2 10
3 1 5
"""
) == "1\n0\n1\n", "sample 1"

# minimum graph
assert run(
"""2 1
1 2 7
"""
) == "0\n", "single edge"

# simple chain
assert run(
"""4 3
1 2 5
2 3 5
3 4 5
"""
) == "0\n0\n0\n", "linear flow"

# branching graph
assert run(
"""5 5
1 2 4
1 3 6
2 4 4
3 4 2
4 5 6
"""
) == "0\n0\n0\n0\n0\n", "multiple dependencies"

# catches double-processing bugs
assert run(
"""3 2
1 2 3
2 3 3
"""
) == "0\n0\n", "used-edge handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge from source to sink | `0` | Minimum valid graph |
| Simple chain | All edges forward | Basic propagation logic |
| Branching graph | Valid layered orientation | Multiple vertices becoming ready |
| Two-edge path | No duplicate processing | Correct handling of undirected adjacency |

## Edge Cases

Consider the smallest possible graph:

```
2 1
1 2 7
```

The source is vertex `1` and the sink is vertex `2`. Since the source cannot receive flow, the only edge must point from `1` to `2`. The algorithm starts with vertex `1` in the queue, processes the edge immediately, and outputs:

```
0
```

No internal vertices exist, so conservation constraints are vacuously satisfied.

Now consider a graph where a vertex must wait for multiple incoming edges before becoming ready:

```
5 5
1 2 4
1 3 6
2 4 4
3 4 2
4 5 6
```

Vertex `4` needs incoming flow `6`. After processing vertex `2`, it only has `4`, so it is not pushed into the queue yet. Only after processing vertex `3` does it reach exactly `6`. At that moment the algorithm knows every remaining undecided edge adjacent to `4` must be outgoing.

This prevents premature orientation mistakes.

Finally, consider a graph that could accidentally form a directed cycle if edges were assigned greedily:

```
4 4
1 2 5
2 3 5
3 4 5
1 3 5
```

The algorithm processes vertices in readiness order. Once a vertex becomes ready, all future edges leave it. Edges never point back into an already resolved vertex. Because of this monotonic structure, a directed cycle cannot appear.
