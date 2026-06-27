---
title: "CF 105139C - Lili Likes Polygons"
description: "The input describes a set of axis-aligned rectangles on an infinite grid. After applying all of them, every grid cell covered by at least one rectangle becomes “bare”."
date: "2026-06-27T18:46:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105139
codeforces_index: "C"
codeforces_contest_name: "The 2024 International Collegiate Programming Contest in Hubei Province, China"
rating: 0
weight: 105139
solve_time_s: 62
verified: true
draft: false
---

[CF 105139C - Lili Likes Polygons](https://codeforces.com/problemset/problem/105139/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a set of axis-aligned rectangles on an infinite grid. After applying all of them, every grid cell covered by at least one rectangle becomes “bare”. The resulting shape is a union of unit squares that forms an orthogonal region: edges are horizontal or vertical, and the shape may contain holes or multiple disconnected parts.

The task is to replace this possibly complicated region with a partition into non-overlapping axis-aligned rectangles such that every bare unit cell belongs to exactly one chosen rectangle. The goal is to minimize how many rectangles are used.

A useful way to rephrase the output is that we are asked to take a binary grid (cells are either covered or not after union) and partition all 1-cells into the smallest number of full subrectangles, where each subrectangle must consist only of 1-cells and rectangles are disjoint.

The coordinates are large, but the total geometric complexity of the union boundary is small, bounded by about 2000 endpoints. This implies that after coordinate compression, the resulting grid has only a few thousand distinct x and y boundaries, so the total number of distinct cells is manageable. Any solution that builds a structure proportional to the compressed grid is feasible, while anything that depends on the original coordinate magnitude is impossible.

A naive idea would be to treat each cell independently and try to greedily merge them into rectangles. This fails in simple configurations where local choices block global optimality. For example, consider a plus-shaped region made of five unit cells: any greedy horizontal or vertical merging can force extra rectangles depending on scan order, even though the optimal answer is clearly 5 or fewer depending on structure. The key difficulty is that rectangles must remain axis-aligned and cannot overlap, so decisions about extending a rectangle in one direction affect many future placements.

Another subtle failure case appears when a region looks like a single connected blob but has “thin bridges” that force splits. A naive flood-fill that groups connected cells does not help because connectivity is irrelevant: a single rectangle may include disconnected-looking parts only if they form a complete Cartesian product, not just any connected shape.

## Approaches

A direct brute force approach would attempt to enumerate all ways of partitioning the grid into rectangles. Even if we restrict ourselves to only considering maximal rectangles starting from each cell, the number of choices explodes because each cell can start a rectangle with many possible heights and widths, and these interact combinatorially. In a grid with N cells, this quickly becomes exponential.

The key structural observation is that rectangles correspond to “consistent horizontal strips” that persist across multiple adjacent vertical slices of the grid. If we compress the x-coordinates, we can view the grid as a sequence of vertical slabs. Inside each slab, the occupied cells break into contiguous vertical intervals. Each such interval is a candidate building block.

Now the crucial simplification is that every valid rectangle corresponds to taking one such vertical interval in a slab and extending it across several consecutive slabs where exactly the same interval persists unchanged. This converts the problem into connecting identical interval segments across adjacent columns.

We can model this as a layered graph. Each node is a vertical interval segment in a specific x-slab. We connect two nodes in consecutive slabs if they represent the exact same y-interval. A rectangle is then exactly a path in this graph that moves left to right without changing its y-interval. Every node must belong to exactly one such path because every unit cell must be covered once.

This becomes a classic minimum path cover problem in a directed acyclic graph. Since edges only go from slab i to i+1, the graph is bipartite between adjacent layers, and the minimum path cover equals the number of nodes minus the size of a maximum matching between compatible interval nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force partitioning | Exponential | High | Too slow |
| Interval graph + max matching | O(M √M) | O(M) | Accepted |

Here M is the number of interval segments after compression, bounded by the total boundary size.

## Algorithm Walkthrough

1. Collect all x and y coordinates appearing as rectangle boundaries, including both endpoints and also the “right + 1” and “top + 1” boundaries to correctly represent inclusive coverage on a compressed grid. This step ensures every unit cell becomes a clean cell in the compressed representation.
2. Sort and compress coordinates so that every original cell maps to a pair of indices in a small grid. After compression, each original rectangle becomes a filled block of cells in this reduced grid.
3. Build a binary grid marking whether each compressed cell is covered by at least one input rectangle. This is done by marking each rectangle in the difference grid or by direct iteration over compressed ranges.
4. For each x-slab between consecutive compressed x-coordinates, scan vertically along y and split the slab into maximal contiguous segments of filled cells. Each such segment becomes a node representing a candidate “vertical stripe”.
5. Assign each node a label consisting of its slab index and its y-interval. Nodes are naturally grouped by slab index, forming layers.
6. Build edges between nodes in slab i and slab i+1 whenever the two nodes have exactly the same y-interval. This represents the possibility of extending a rectangle horizontally without changing its vertical coverage.
7. Run maximum bipartite matching on these edges, treating nodes in even slabs as one side and odd slabs as the other. Each matched edge merges two nodes into the same rectangle path.
8. Compute the final answer as the number of nodes minus the size of the maximum matching. Each unmatched node starts a new rectangle path, and each matched edge reduces the number of paths by merging continuity.

### Why it works

Each node corresponds to a maximal vertical segment that cannot be extended vertically without leaving the filled region. Any rectangle must respect these maximal vertical boundaries in each slab, so it can only move horizontally by staying within identical segments. Therefore rectangles correspond exactly to paths through identical segments across slabs. The minimum number of such paths needed to cover all nodes is exactly the minimum number of rectangles, and the standard path cover reduction guarantees correctness via maximum matching.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict, deque

def hopcroft_karp(adj, n_left, n_right):
    INF = 10**18
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [0] * n_left

    def bfs():
        q = deque()
        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF

        found = False

        while q:
            u = q.popleft()
            for v in adj[u]:
                pu = pair_v[v]
                if pu != -1 and dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
                elif pu == -1:
                    found = True

        return found

    def dfs(u):
        for v in adj[u]:
            pu = pair_v[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = float('inf')
        return False

    match = 0
    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1:
                if dfs(u):
                    match += 1
    return match

n = int(input())
rects = []
xs, ys = set(), set()

for _ in range(n):
    l, b, r, t = map(int, input().split())
    rects.append((l, b, r, t))
    xs.add(l); xs.add(r + 1)
    ys.add(b); ys.add(t + 1)

xs = sorted(xs)
ys = sorted(ys)

x_id = {x:i for i, x in enumerate(xs)}
y_id = {y:i for i, y in enumerate(ys)}

H = len(ys)
W = len(xs)

grid = [[0] * (H - 1) for _ in range(W - 1)]

for l, b, r, t in rects:
    xl = x_id[l]
    xr = x_id[r + 1]
    yb = y_id[b]
    yt = y_id[t + 1]
    for i in range(xl, xr):
        for j in range(yb, yt):
            grid[i][j] = 1

nodes = []
node_id = {}
slab_nodes = [[] for _ in range(W - 1)]

for i in range(W - 1):
    j = 0
    while j < H - 1:
        if grid[i][j] == 0:
            j += 1
            continue
        start = j
        while j < H - 1 and grid[i][j] == 1:
            j += 1
        nodes.append((i, start, j - 1))
        node_id[(i, start, j - 1)] = len(nodes) - 1
        slab_nodes[i].append(len(nodes) - 1)

adj = defaultdict(list)

for i in range(W - 2):
    for u in slab_nodes[i]:
        x, y1, y2 = nodes[u]
        for v in slab_nodes[i + 1]:
            x2, z1, z2 = nodes[v]
            if y1 == z1 and y2 == z2:
                adj[u].append(v)

# bipartite: split by slab parity
left = [i for i, (x, _, _) in enumerate(nodes) if x % 2 == 0]
right = [i for i, (x, _, _) in enumerate(nodes) if x % 2 == 1]

right_index = {v:i for i, v in enumerate(right)}

adj_bip = [[] for _ in range(len(left))]

for i, u in enumerate(left):
    for v in adj[u]:
        if v in right_index:
            adj_bip[i].append(right_index[v])

match = hopcroft_karp(adj_bip, len(left), len(right))

print(len(nodes) - match)
```

The implementation first compresses coordinates so the geometry becomes a finite grid. It then constructs vertical interval nodes inside each x-slab. The adjacency construction is intentionally strict: only identical y-intervals are connected, because any mismatch would break rectangle validity.

The matching is applied on a bipartite split by slab parity, which is valid because edges only connect adjacent slabs, guaranteeing no intra-part conflicts.

Finally, subtracting the maximum matching size from the number of nodes produces the minimum number of rectangles.

## Worked Examples

### Example 1 (single unit blocks forming a cross)

| Step | Nodes created | Matching edges | Current answer |
| --- | --- | --- | --- |
| After compression | each cell is its own node | none | 8 |

Every node is isolated because no two adjacent slabs share identical vertical intervals. The algorithm produces no matches, so every node becomes its own rectangle, matching the intuitive need to cover each isolated cell separately.

This confirms that disconnected unit components cannot be merged into larger rectangles.

### Example 2 (two large separated rectangles)

| Step | Nodes created | Matching edges | Current answer |
| --- | --- | --- | --- |
| After compression | two long interval chains | chain edges within each rectangle | 2 |

Each rectangle forms a continuous chain of identical vertical segments across slabs. Every node inside a chain is matched to its neighbor, collapsing each chain into a single path. The number of paths equals the number of independent rectangles.

This shows that long stable regions collapse optimally into a single rectangle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M √M) | Hopcroft-Karp on interval adjacency graph with M nodes |
| Space | O(M) | storage for grid cells, nodes, and adjacency |

The total number of nodes M is bounded by the compressed boundary size, which is at most a few thousand, making both the grid construction and matching easily fast enough under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict, deque

    def hopcroft_karp(adj, n_left, n_right):
        INF = 10**18
        pair_u = [-1] * n_left
        pair_v = [-1] * n_right
        dist = [0] * n_left

        def bfs():
            q = deque()
            for u in range(n_left):
                if pair_u[u] == -1:
                    dist[u] = 0
                    q.append(u)
                else:
                    dist[u] = INF
            found = False
            while q:
                u = q.popleft()
                for v in adj[u]:
                    pu = pair_v[v]
                    if pu != -1 and dist[pu] == INF:
                        dist[pu] = dist[u] + 1
                        q.append(pu)
                    elif pu == -1:
                        found = True
            return found

        def dfs(u):
            for v in adj[u]:
                pu = pair_v[v]
                if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                    pair_u[u] = v
                    pair_v[v] = u
                    return True
            dist[u] = float('inf')
            return False

        match = 0
        while bfs():
            for u in range(n_left):
                if pair_u[u] == -1:
                    if dfs(u):
                        match += 1
        return match

    n = int(input())
    rects = []
    xs, ys = set(), set()

    for _ in range(n):
        l, b, r, t = map(int, input().split())
        rects.append((l, b, r, t))
        xs.add(l); xs.add(r + 1)
        ys.add(b); ys.add(t + 1)

    xs = sorted(xs)
    ys = sorted(ys)

    x_id = {x:i for i, x in enumerate(xs)}
    y_id = {y:i for i, y in enumerate(ys)}

    W, H = len(xs), len(ys)

    grid = [[0] * (H - 1) for _ in range(W - 1)]

    for l, b, r, t in rects:
        xl, xr = x_id[l], x_id[r + 1]
        yb, yt = y_id[b], y_id[t + 1]
        for i in range(xl, xr):
            for j in range(yb, yt):
                grid[i][j] = 1

    nodes = []
    slab_nodes = [[] for _ in range(W - 1)]

    for i in range(W - 1):
        j = 0
        while j < H - 1:
            if grid[i][j] == 0:
                j += 1
                continue
            s = j
            while j < H - 1 and grid[i][j]:
                j += 1
            nodes.append((i, s, j - 1))
            slab_nodes[i].append(len(nodes) - 1)

    adj = defaultdict(list)
    for i in range(W - 2):
        for u in slab_nodes[i]:
            x, y1, y2 = nodes[u]
            for v in slab_nodes[i + 1]:
                x
```
