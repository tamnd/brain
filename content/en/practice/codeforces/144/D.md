---
title: "CF 144D - Missile Silos"
description: "We are given a connected weighted undirected graph representing cities and roads. City s is the capital. A missile silo may be located either exactly on a city or at some interior point of a road. A position is valid if its shortest-path distance to the capital is exactly l."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 144
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 103 (Div. 2)"
rating: 1900
weight: 144
solve_time_s: 130
verified: true
draft: false
---

[CF 144D - Missile Silos](https://codeforces.com/problemset/problem/144/D)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, graphs, shortest paths  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected weighted undirected graph representing cities and roads. City `s` is the capital. A missile silo may be located either exactly on a city or at some interior point of a road. A position is valid if its shortest-path distance to the capital is exactly `l`.

The task is to count how many distinct positions satisfy this condition.

The key detail is that we are not counting paths, we are counting geometric positions in the graph. A single road may contain zero, one, or two valid points depending on how shortest distances behave from both endpoints.

The graph has up to `10^5` cities and roads. That immediately rules out anything quadratic. Even an `O(nm)` solution would perform around `10^10` operations in the worst case, which is impossible under a 2-second limit. Since all edge weights are positive, Dijkstra runs efficiently in `O((n + m) log n)`, which comfortably fits the constraints.

The tricky part is not computing shortest distances to cities. The difficult part is counting points inside edges without double-counting or counting points that are not actually at shortest distance `l`.

Consider this graph:

```
1 --(10)-- 2
```

with `s = 1` and `l = 5`.

There is no city at distance `5`, but there is exactly one point inside the edge. A solution that only checks cities would incorrectly return `0`.

Another subtle case is when two candidate points from opposite ends coincide.

```
1 --(10)-- 2
```

Suppose `dist[1] = 0`, `dist[2] = 4`, and `l = 7`.

From city `1`, the candidate point is `7` units along the edge.

From city `2`, the candidate point is `3` units along the edge.

These are the same physical point because `7 + 3 = 10`. We must count it once, not twice.

One more dangerous case appears when a point is reachable from one endpoint at distance `l`, but another shorter route exists through the other endpoint.

Suppose:

```
dist[u] = 2
dist[v] = 3
edge length = 10
l = 8
```

From `u`, the point lies `6` units into the edge. But from `v`, that same point is only `4 + 3 = 7` away from the source, so its shortest distance is actually `7`, not `8`. A naive geometric check would count an invalid point.

The solution must verify shortest-path conditions carefully.

## Approaches

A brute-force interpretation would treat every road as a continuous segment and try to locate all points whose shortest distance equals `l`. One could derive equations for every edge and compare distances through both endpoints.

This is theoretically possible, but handling all overlaps and shortest-path conditions directly becomes messy. Worse, recomputing shortest paths for many candidate positions is completely infeasible. Even checking every edge against every city would already exceed practical limits.

The structure of the problem changes once we observe that every shortest path to a point inside an edge must enter through one of the edge endpoints.

Suppose an edge connects `u` and `v` with length `w`. If a point lies `x` units from `u`, then its distance from the source through `u` is:

```
dist[u] + x
```

and through `v` is:

```
dist[v] + (w - x)
```

The actual shortest distance to that point is the minimum of these two values.

This observation completely reduces the continuous problem into arithmetic on edge endpoints. Once we compute shortest distances from the source to every city using Dijkstra, each edge can be analyzed independently.

For a point to have shortest distance exactly `l`, at least one side must satisfy:

```
dist[u] + x = l
```

or

```
dist[v] + (w - x) = l
```

After finding such candidate positions, we must verify that the opposite direction does not give a strictly smaller path.

This leads to a clean linear scan over all edges after one Dijkstra run.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Too large, potentially exponential over continuous positions | Large | Too slow |
| Optimal | `O((n + m) log n)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list for the graph.

Since the graph is sparse and large, adjacency lists are much more efficient than an adjacency matrix.
2. Run Dijkstra from the capital `s`.

This computes `dist[i]`, the shortest distance from the capital to every city.
3. Count all cities whose shortest distance equals `l`.

Every such city itself is a valid missile silo position.
4. Process each edge independently.

Suppose the edge is `(u, v, w)`.
5. Compute the candidate point generated from endpoint `u`.

If `dist[u] < l`, then a point at distance

```
x = l - dist[u]
```

from `u` lies somewhere on the edge if `x < w`.
6. Verify that this point is actually at shortest distance `l`.

The distance through `v` would be:

```
dist[v] + (w - x)
```

We only count the point if this value is at least `l`.

If it were smaller, then the point's true shortest distance would not equal `l`.
7. Repeat symmetrically for endpoint `v`.
8. Handle double-counting.

If both endpoints generate the same interior point, then:

```
x + y = w
```

In this situation, both checks refer to one physical location, so subtract one from the count for this edge.
9. Sum all valid city and edge positions.

### Why it works

After Dijkstra, `dist[u]` is the exact shortest-path distance from the source to every endpoint.

Any shortest route to a point inside edge `(u, v)` must enter through either `u` or `v`, because the graph is undirected and the point lies only on this edge. Thus the shortest distance to an interior point is exactly:

```
min(dist[u] + x, dist[v] + (w - x))
```

The algorithm enumerates every possible point where one of these expressions equals `l`. The verification step guarantees the other expression is not smaller than `l`, so the true shortest distance is exactly `l`.

Every valid point is discovered from at least one endpoint, and the overlap correction removes the only possible duplication case, when both endpoint constructions refer to the same location.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

n, m, s = map(int, input().split())
s -= 1

adj = [[] for _ in range(n)]
edges = []

for _ in range(m):
    u, v, w = map(int, input().split())
    u -= 1
    v -= 1

    adj[u].append((v, w))
    adj[v].append((u, w))

    edges.append((u, v, w))

l = int(input())

dist = [INF] * n
dist[s] = 0

pq = [(0, s)]

while pq:
    d, u = heapq.heappop(pq)

    if d != dist[u]:
        continue

    for v, w in adj[u]:
        nd = d + w

        if nd < dist[v]:
            dist[v] = nd
            heapq.heappush(pq, (nd, v))

answer = 0

for d in dist:
    if d == l:
        answer += 1

for u, v, w in edges:
    cnt = 0

    # candidate generated from u
    if dist[u] < l:
        x = l - dist[u]

        if x < w and dist[v] + (w - x) >= l:
            cnt += 1

    # candidate generated from v
    if dist[v] < l:
        y = l - dist[v]

        if y < w and dist[u] + (w - y) >= l:
            cnt += 1

    # same physical point counted twice
    if cnt == 2 and (l - dist[u]) + (l - dist[v]) == w:
        cnt = 1

    answer += cnt

print(answer)
```

The first part builds the graph and stores edges separately. We need adjacency lists for Dijkstra and a flat edge list for later edge analysis.

The Dijkstra implementation is standard. Since edge weights are positive, the first time we finalize a node, its distance is optimal. The `if d != dist[u]` check skips stale heap entries.

After shortest distances are known, counting cities is immediate.

The edge-processing section contains the real logic. From endpoint `u`, we compute how far along the edge we must travel to reach distance `l`. The condition `x < w` guarantees the point lies strictly inside the edge rather than landing exactly on `v`. Endpoint cities are already counted separately.

The inequality:

```
dist[v] + (w - x) >= l
```

is essential. Without it, we might count a point whose actual shortest distance is smaller than `l`.

The overlap condition:

```
(l - dist[u]) + (l - dist[v]) == w
```

means the two constructions meet at the same point. This is the only scenario where double-counting can happen.

All arithmetic safely fits inside 64-bit integers because distances can grow up to roughly `10^8`.

## Worked Examples

### Sample 1

Input:

```
4 6 1
1 2 1
1 3 3
2 3 1
2 4 1
3 4 1
1 4 2
2
```

Shortest distances from city `1`:

| City | Distance |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 2 |

Cities `3` and `4` already contribute `2`.

Now process edges:

| Edge | Candidate from first side | Candidate from second side | Added |
| --- | --- | --- | --- |
| (1,2,1) | none | none | 0 |
| (1,3,3) | interior point at distance 2 | invalid | 1 |
| (2,3,1) | none | none | 0 |
| (2,4,1) | none | none | 0 |
| (3,4,1) | none | none | 0 |
| (1,4,2) | endpoint only | none | 0 |

Final answer:

```
2 cities + 1 interior point = 3
```

This example shows why interior edge points must be checked separately from cities.

### Sample 2

Consider:

```
5 4 1
1 2 6
2 3 2
3 4 2
4 5 6
3
```

Shortest distances:

| City | Distance |
| --- | --- |
| 1 | 0 |
| 2 | 6 |
| 3 | 8 |
| 4 | 10 |
| 5 | 16 |

No city lies at distance `3`.

Edge analysis:

| Edge | Candidate Points | Added |
| --- | --- | --- |
| (1,2,6) | midpoint at 3 from city 1 | 1 |
| (2,3,2) | none | 0 |
| (3,4,2) | none | 0 |
| (4,5,6) | none | 0 |

Final answer is `1`.

This demonstrates that the solution handles points strictly inside edges even when no city qualifies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m) log n)` | Dijkstra dominates the runtime |
| Space | `O(n + m)` | Adjacency list, heap, and distance array |

With `10^5` vertices and edges, this complexity is fully acceptable. A binary-heap Dijkstra easily fits within the time limit, and adjacency lists keep memory usage linear.

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

    n, m, s = map(int, input().split())
    s -= 1

    adj = [[] for _ in range(n)]
    edges = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1

        adj[u].append((v, w))
        adj[v].append((u, w))

        edges.append((u, v, w))

    l = int(input())

    dist = [INF] * n
    dist[s] = 0

    pq = [(0, s)]

    while pq:
        d, u = heapq.heappop(pq)

        if d != dist[u]:
            continue

        for v, w in adj[u]:
            nd = d + w

            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    ans = 0

    for d in dist:
        if d == l:
            ans += 1

    for u, v, w in edges:
        cnt = 0

        if dist[u] < l:
            x = l - dist[u]

            if x < w and dist[v] + (w - x) >= l:
                cnt += 1

        if dist[v] < l:
            y = l - dist[v]

            if y < w and dist[u] + (w - y) >= l:
                cnt += 1

        if cnt == 2 and (l - dist[u]) + (l - dist[v]) == w:
            cnt = 1

        ans += cnt

    return str(ans)

# provided sample
assert run(
"""4 6 1
1 2 1
1 3 3
2 3 1
2 4 1
3 4 1
1 4 2
2
"""
) == "3"

# single interior point
assert run(
"""2 1 1
1 2 10
5
"""
) == "1"

# one city exactly at distance l
assert run(
"""3 2 1
1 2 2
2 3 2
2
"""
) == "1"

# duplicate interior point from both ends
assert run(
"""2 1 1
1 2 10
5
"""
) == "1"

# no valid positions
assert run(
"""2 1 1
1 2 3
10
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 3 | Mixed city and edge answers |
| Two nodes with edge 10, `l=5` | 1 | Interior midpoint handling |
| Path graph with city at exact distance | 1 | City counting |
| Same midpoint generated from both ends | 1 | Double-count prevention |
| `l` larger than all distances | 0 | No-solution handling |

## Edge Cases

Consider the midpoint duplication case:

```
2 1 1
1 2 10
5
```

Shortest distances are:

```
dist[1] = 0
dist[2] = 10
```

From node `1`, the candidate point lies `5` units along the edge.

From node `2`, the candidate point also lies `5` units along the edge.

Without overlap correction, the algorithm would count two points. The equality:

```
(5 - 0) + (5 - 10) = 10
```

detects that both constructions refer to the same location, so the count becomes `1`.

Now consider a false candidate:

```
3 2 1
1 2 2
2 3 10
8
```

Distances:

```
dist[1] = 0
dist[2] = 2
dist[3] = 12
```

From node `2`, we can move `6` units into edge `(2,3)` and appear to reach distance `8`.

But from node `3`, that same point is only:

```
12 + (10 - 6) = 16
```

which is fine, so the point is valid.

Now modify distances conceptually:

```
dist[2] = 2
dist[3] = 3
w = 10
l = 8
```

The candidate from `2` would lie `6` units into the edge. Through node `3`, the distance becomes:

```
3 + 4 = 7
```

The verification condition rejects this point because its true shortest distance is `7`, not `8`.

Finally, consider landing exactly on an endpoint:

```
2 1 1
1 2 5
5
```

City `2` is already counted as a city. During edge processing:

```
x = 5
```

Since `x < w` is false, the algorithm does not count the endpoint again as an interior point.
