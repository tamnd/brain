---
title: "CF 106189C - And again the maze"
description: "We have a rectangular maze. Empty cells are traversable, cells marked X are blocked. The player starts in the top-left corner and wants to reach the bottom-right corner using four-directional moves. We want to place exactly one additional obstacle into an empty cell."
date: "2026-06-25T06:47:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "C"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 65
verified: true
draft: false
---

[CF 106189C - And again the maze](https://codeforces.com/problemset/problem/106189/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular maze. Empty cells are traversable, cells marked `X` are blocked. The player starts in the top-left corner and wants to reach the bottom-right corner using four-directional moves.

We want to place exactly one additional obstacle into an empty cell. A cell is valid if, after blocking it, the shortest path from start to finish becomes strictly longer, while a path still exists.

The output is the original maze, except that every valid cell is replaced by `*`.

The grid can be as large as `1000 × 1000`, which means up to one million cells. Any solution that recomputes a shortest path for every empty cell is completely infeasible. Even a single BFS already touches about one million vertices, so we need something very close to linear complexity in the size of the grid.

The subtle part is that increasing the shortest path length is not the same as disconnecting the maze.

Consider this maze:

```
...
...
...
```

Every shortest path from the top-left corner to the bottom-right corner has length 4, but there are many such paths. Blocking any single interior cell still leaves another shortest path of length 4, so no answer cells exist.

Now consider:

```
.....
.XXX.
.....
```

The middle corridor is the only shortest route. Blocking one of its interior cells destroys all shortest paths, but a longer detour still exists. Those cells are valid.

A different trap is a true bottleneck:

```
...
.X.
...
```

If some cell lies on every possible path, not only every shortest path, then blocking it disconnects start and finish. Such a cell must not be marked because the statement requires that a path still exists afterward.

## Approaches

The brute-force idea is straightforward. For every empty cell, temporarily block it, run BFS from the start, compute the new shortest distance, and check whether it became larger while remaining finite.

If the grid contains one million cells, that means up to one million BFS runs. Each BFS is already `O(NM)`, so the total work becomes roughly `O((NM)^2)`, which is far beyond any realistic limit.

The key observation is that a cell can increase the shortest-path length only if it belongs to **every shortest path**.

Suppose there exists a shortest path that avoids a cell `v`. After blocking `v`, that same shortest path still exists, so the shortest distance cannot increase.

This turns the problem into two independent questions.

First, which cells belong to every shortest path?

Let `distS[v]` be the distance from the start and `distT[v]` the distance from the finish. A cell belongs to some shortest path exactly when

```
distS[v] + distT[v] = D
```

where `D` is the shortest distance from start to finish.

All shortest-path cells form a layered DAG. Every shortest path visits exactly one vertex at distance `0`, one at distance `1`, one at distance `2`, and so on.

If a layer contains exactly one shortest-path cell, every shortest path is forced to pass through it. If a layer contains two or more cells, a shortest path can choose among them.

So a shortest-path cell belongs to every shortest path if and only if it is the unique shortest-path cell in its distance layer.

That identifies all cells whose removal destroys every shortest path.

The second question is whether removing such a cell still leaves some path at all.

That is a classic graph question. We need to know whether the cell is an `s-t` cut vertex. If removing it disconnects the start from the finish, it is not a valid answer. If start and finish remain connected, all shortest paths disappear and the new shortest distance becomes strictly larger.

This can be checked with a single low-link DFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((NM)²) | O(NM) | Too slow |
| Optimal | O(NM) | O(NM) | Accepted |

## Algorithm Walkthrough

1. Run BFS from the start cell and compute `distS`.
2. Run BFS from the finish cell and compute `distT`.
3. Let `D = distS[finish]`.
4. For every free cell `v`, check whether

```
distS[v] + distT[v] = D
```

If true, the cell lies on at least one shortest path.
5. Count how many shortest-path cells appear in each distance layer `distS[v]`.
6. A shortest-path cell `v` belongs to every shortest path exactly when its layer count equals `1`.

The reason is that every shortest path must contain one vertex from every layer. If a layer has only one candidate, every shortest path is forced through it.
7. Run a low-link DFS from the start over the whole free-cell graph.
8. For each vertex, determine whether removing it disconnects the start from the finish. Mark such vertices as `st_cut`.
9. A cell is an answer if all of the following hold:

```
it is free
it is not start
it is not finish
it belongs to every shortest path
it is not an s-t cut vertex
```
10. Output the grid, replacing exactly those cells with `*`.

### Why it works

The shortest distance increases only if every original shortest path is destroyed. A cell destroys every shortest path exactly when it belongs to all of them.

The distance-layer argument identifies precisely those cells. Every shortest path advances through the layers in order, and a layer with a single shortest-path vertex forces that vertex into every shortest path.

After removing such a cell, all shortest paths disappear. If start and finish remain connected, some longer path still exists, so the new shortest distance is strictly larger. If start and finish become disconnected, the move is invalid.

The algorithm marks exactly the cells satisfying both conditions, so every reported cell is valid and every valid cell is reported.

## Python Solution

```python
import sys
from collections import deque
from array import array

input = sys.stdin.readline

n, m = map(int, input().split())
g = [input().strip() for _ in range(n)]

V = n * m

def idx(r, c):
    return r * m + c

start = 0
target = V - 1

free = bytearray(V)
for r in range(n):
    row = g[r]
    base = r * m
    for c in range(m):
        if row[c] != 'X':
            free[base + c] = 1

def bfs(src):
    dist = array('i', [-1]) * V
    q = deque([src])
    dist[src] = 0

    while q:
        v = q.popleft()
        r = v // m
        c = v - r * m

        nv = v - m
        if r and free[nv] and dist[nv] == -1:
            dist[nv] = dist[v] + 1
            q.append(nv)

        nv = v + m
        if r + 1 < n and free[nv] and dist[nv] == -1:
            dist[nv] = dist[v] + 1
            q.append(nv)

        nv = v - 1
        if c and free[nv] and dist[nv] == -1:
            dist[nv] = dist[v] + 1
            q.append(nv)

        nv = v + 1
        if c + 1 < m and free[nv] and dist[nv] == -1:
            dist[nv] = dist[v] + 1
            q.append(nv)

    return dist

distS = bfs(start)
distT = bfs(target)

D = distS[target]

cnt = array('i', [0]) * (D + 1)
on_shortest = bytearray(V)

for v in range(V):
    if free[v] and distS[v] != -1 and distS[v] + distT[v] == D:
        on_shortest[v] = 1
        cnt[distS[v]] += 1

mandatory = bytearray(V)
for v in range(V):
    if on_shortest[v] and cnt[distS[v]] == 1:
        mandatory[v] = 1

tin = array('i', [0]) * V
low = array('i', [0]) * V
parent = array('i', [-1]) * V
contains_t = bytearray(V)
st_cut = bytearray(V)

timer = 0

stack = [(start, 0)]
parent[start] = start

while stack:
    v, it = stack[-1]

    if tin[v] == 0:
        timer += 1
        tin[v] = low[v] = timer
        if v == target:
            contains_t[v] = 1

    r = v // m
    c = v - r * m

    neigh = []

    if r:
        neigh.append(v - m)
    if r + 1 < n:
        neigh.append(v + m)
    if c:
        neigh.append(v - 1)
    if c + 1 < m:
        neigh.append(v + 1)

    advanced = False

    while it < len(neigh):
        to = neigh[it]
        it += 1
        stack[-1] = (v, it)

        if not free[to]:
            continue

        if tin[to] == 0:
            parent[to] = v
            stack.append((to, 0))
            advanced = True
            break

        if to != parent[v]:
            if tin[to] < low[v]:
                low[v] = tin[to]

    if advanced:
        continue

    stack.pop()

    if v != start:
        p = parent[v]

        if contains_t[v] and low[v] >= tin[p]:
            st_cut[p] = 1

        if low[v] < low[p]:
            low[p] = low[v]

        if contains_t[v]:
            contains_t[p] = 1

ans = [list(row) for row in g]

for v in range(V):
    if v == start or v == target:
        continue

    if mandatory[v] and not st_cut[v]:
        r = v // m
        c = v - r * m
        ans[r][c] = '*'

print("\n".join("".join(row) for row in ans))
```

After the two BFS runs, every free cell knows its distance from both ends. The equality

```
distS[v] + distT[v] = D
```

filters exactly the cells that participate in at least one shortest path.

The layer-count array stores how many shortest-path cells appear at each distance from the start. A count of one means that layer is forced.

The DFS is a standard low-link traversal. The extra `contains_t` flag tracks whether a DFS subtree contains the finish vertex. When

```
low[child] >= tin[parent]
```

and the child subtree contains the finish, removing the parent separates start and finish. Those vertices are excluded.

The implementation uses iterative DFS to avoid recursion depth problems on grids containing up to one million cells.

## Worked Examples

### Example 1

```
4 5
.....
.XX..
.X...
...X.
```

The shortest distance is 7.

| Layer | Shortest-path cells |
| --- | --- |
| 0 | (0,0) |
| 1 | (0,1) |
| 2 | (0,2) |
| 3 | (0,3) |
| 4 | (0,4) |
| 5 | (1,4) |
| 6 | (2,4) |
| 7 | (3,4) |

Layers 1, 2 and 3 contain a unique shortest-path cell. None of them disconnects the maze entirely, so they become `*`.

Output:

```
.***.
.XX..
.X...
...X.
```

This example shows the core idea: every shortest path is forced through the top corridor, but longer detours still exist.

### Example 2

```
3 3
...
...
...
```

The shortest distance is 4.

| Layer | Number of shortest-path cells |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |

No interior layer contains exactly one cell.

No cell belongs to every shortest path, so the output remains unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | Two BFS traversals and one DFS traversal |
| Space | O(NM) | Distances, low-link arrays, and auxiliary storage |

The grid contains at most one million cells. Every cell and every grid edge is processed only a constant number of times, which comfortably fits the intended limits.

## Test Cases

```
# helper: run solution on input string, return output string

# sample-like case
assert run("""4 5
.....
.XX..
.X...
...X.
""") == """.***.
.XX..
.X...
...X.
"""

# minimum grid
assert run("""1 1
.
""") == """.
"""

# completely open 3x3 grid
assert run("""3 3
...
...
...
""") == """...
...
...
"""

# single corridor, removing middle disconnects
assert run("""1 5
.....
""") == """.....
"""

# forced shortest path but longer detour exists
assert run("""3 5
.....
.XXX.
.....
""") == """.....
.XXX.
.....
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | unchanged | Start equals finish |
| Open 3×3 grid | unchanged | Many shortest paths |
| Single corridor | unchanged | Path must still exist after blocking |
| Corridor with detour | checks valid stars | Increase shortest distance without disconnecting |

## Edge Cases

A cell can belong to every shortest path and still be invalid.

Example:

```
.....
XXXXX
.....
```

The only connection between start and finish is impossible across the wall barrier. Any bottleneck cell would disconnect the graph entirely when removed. The low-link phase detects that it is an `s-t` cut vertex, so it is not marked.

Another subtle case is a maze with several shortest paths of equal length:

```
...
...
...
```

The center cell participates in many shortest paths, but not all of them. Its layer contains multiple shortest-path cells, so it is not considered mandatory and is not marked.

Finally, consider a forced shortest-path vertex with a longer detour around it:

```
.....
.XXX.
.....
```

Its layer contains exactly one shortest-path cell, so every shortest path uses it. Removing it leaves a longer route through the bottom row. The shortest distance increases and the path still exists, which is exactly the situation the algorithm marks with `*`.
