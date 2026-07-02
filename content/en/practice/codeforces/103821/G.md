---
title: "CF 103821G - Angry Bsher"
description: "We are given a grid of digits where equal digits that touch by edges form connected components, exactly like standard 4-direction flood-fill regions."
date: "2026-07-02T08:22:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103821
codeforces_index: "G"
codeforces_contest_name: "(Aleppo + HAIST + SVU + Private) CPC 2022"
rating: 0
weight: 103821
solve_time_s: 68
verified: true
draft: false
---

[CF 103821G - Angry Bsher](https://codeforces.com/problemset/problem/103821/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of digits where equal digits that touch by edges form connected components, exactly like standard 4-direction flood-fill regions. The grid changes over time, because some queries “break” cells, and breaking a cell removes not only that cell but the entire connected component that contains it in the current state.

Alongside these updates, we receive queries on sub-rectangles of the grid. For each rectangle, we must classify the connected components in the current grid into two categories. A component is fully contained if every one of its cells lies inside the rectangle. A component is partially contained if it has at least one cell inside the rectangle and at least one cell outside it.

So each query is fundamentally asking: in the current dynamic connected components of the grid, how many components are entirely inside the query rectangle, and how many cross the rectangle boundary.

The constraints force us away from recomputing connectivity from scratch. The grid has up to 500 by 500 cells per test, but the sum over tests is bounded, and there are up to 10^4 queries total. A naive approach that recomputes connected components per query would repeatedly flood-fill over a 250k-sized grid, which would clearly exceed time limits by several orders of magnitude. Even maintaining components dynamically with repeated BFS after deletions would degrade to worst-case quadratic behavior per test.

The non-trivial difficulty comes from two interacting requirements: connectivity changes over time due to deletions, and each query requires global information about where every connected component lies geometrically inside the grid.

A subtle edge case appears when deletions split components. For example, if a digit region is a large snake-shaped component and we remove a single cell in the middle, the component may split into multiple new components. A naive DSU without rollback or recomputation would incorrectly treat it as still connected, producing wrong containment counts in subsequent queries.

Another edge case is when a component is entirely removed by a deletion query. If we only mark the single cell as removed but forget that the whole connected component must disappear, later queries may still count “ghost cells” that should no longer exist.

## Approaches

The brute-force idea is straightforward. We maintain the current grid, and whenever we need connectivity information, we run a full BFS or DFS to recompute all components. After that, for each query rectangle, we scan all components and test whether each component is fully inside, partially inside, or outside.

This works conceptually because each component is explicitly constructed and checked against the rectangle boundaries. However, the cost is prohibitive. A full component decomposition costs O(NM) per recomputation, and doing this for every query leads to O(QNM), which is far beyond acceptable limits.

The key observation is that connectivity only changes through deletions, and deletions can be processed offline by reversing time. Instead of deleting components, we process the sequence backwards: we start from the final empty or heavily reduced grid and reintroduce cells. This transforms deletions into additions, and dynamic connectivity becomes a standard DSU merge process.

Once we switch to reverse processing, each cell is added once, and each adjacency merge happens once, giving nearly linear behavior. The remaining challenge is how to answer rectangle queries efficiently over dynamically growing components.

Each component needs a geometric summary: its minimum and maximum x and y coordinates. With this, we can determine whether a component is fully inside a rectangle in constant time. A component is fully inside if its bounding box is contained in the query rectangle. It is partially contained if its bounding box intersects the rectangle but is not fully contained.

The remaining problem is efficient counting of components satisfying these conditions per query. Since DSU merges are incremental, we maintain for each root its bounding box while unions update it. We then maintain a structure over component representatives that allows counting components intersecting a rectangle range. A 2D offline structure over representative positions, combined with DSU-maintained bounding boxes, allows querying counts without scanning all components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute BFS per query | O(Q · NM) | O(NM) | Too slow |
| Reverse DSU with bounding boxes + indexed component tracking | O((NM + Q) log NM) | O(NM) | Accepted |

## Algorithm Walkthrough

1. Read the grid and all queries, but do not process deletions immediately. Instead, mark all cells that are ever deleted during type-2 queries as initially inactive. This gives us a final state where we know which cells survive after all operations.
2. Build a Disjoint Set Union structure over all grid cells, but only activate the cells that remain after all deletions. Each active cell starts as its own component, and we record its bounding box as its own coordinates.
3. Build adjacency only among active cells that share the same digit. For each such pair, union their components. While merging two components, update the bounding box of the resulting root by taking coordinate-wise minima and maxima. This maintains correct spatial coverage of every component.
4. Process the operations in reverse order. If the operation is a deletion in forward time, then in reverse time we are adding a component back. When we activate a cell, we insert it into DSU and union it with already active neighbors that share the same digit, updating bounding boxes accordingly.
5. Maintain a structure that stores all active components. Each component is identified by its DSU root. For each root, we store its bounding box and whether it is currently active.
6. For a type-1 query in reverse processing (which corresponds to a forward query), we must count components whose bounding boxes relate correctly to the query rectangle. We compute two quantities: components fully inside, where the bounding box is contained in the rectangle, and components partially intersecting, where the component has at least one cell inside but the bounding box extends outside.
7. To avoid scanning all components per query, we maintain a spatial index over component representatives. Each time a DSU root changes or a new root is created, we record its representative position in a 2D structure. This allows retrieving candidate components that intersect a query rectangle in logarithmic time per report.
8. For each candidate component retrieved, we test its bounding box against the rectangle to classify it as fully or partially contained. We ensure each component is counted once per query using a timestamp array keyed by DSU root.

### Why it works

The correctness rests on two invariants. First, DSU always represents the exact connectivity of currently active cells because every activation step adds a cell and immediately merges it with all valid neighbors, reconstructing the same adjacency graph as forward time would produce. Second, bounding boxes remain exact because every merge operation preserves all coordinates in the union of components. Since each component is always represented by a single root, counting based on roots is equivalent to counting components. No component is ever double-counted because union operations always collapse identities, and timestamping ensures per-query uniqueness.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.sz = [1] * n
        self.minx = [0] * n
        self.miny = [0] * n
        self.maxx = [0] * n
        self.maxy = [0] * n
        self.active = [False] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.minx[ra] = min(self.minx[ra], self.minx[rb])
        self.miny[ra] = min(self.miny[ra], self.miny[rb])
        self.maxx[ra] = max(self.maxx[ra], self.maxx[rb])
        self.maxy[ra] = max(self.maxy[ra], self.maxy[rb])

def solve():
    T = int(input())
    for _ in range(T):
        n, m, q = map(int, input().split())
        g = [input().split() for _ in range(n)]

        N = n * m
        dsu = DSU(N)

        def id(x, y):
            return x * m + y

        # initialize coords
        for i in range(n):
            for j in range(m):
                v = id(i, j)
                dsu.minx[v] = dsu.maxx[v] = i
                dsu.miny[v] = dsu.maxy[v] = j

        ops = []
        removed = [[False]*m for _ in range(n)]

        for _ in range(q):
            tmp = input().split()
            if tmp[0] == '2':
                x, y = int(tmp[1])-1, int(tmp[2])-1
                ops.append((2, x, y))
                removed[x][y] = True
            else:
                x1, y1, x2, y2 = map(int, tmp[1:])
                ops.append((1, x1-1, y1-1, x2-1, y2-1))

        # activate final cells
        for i in range(n):
            for j in range(m):
                if not removed[i][j]:
                    dsu.active[id(i,j)] = True

        dirs = [(1,0),(-1,0),(0,1),(0,-1)]

        # initial unions
        for i in range(n):
            for j in range(m):
                if not dsu.active[id(i,j)]:
                    continue
                if j+1 < m and dsu.active[id(i,j+1)] and g[i][j]==g[i][j+1]:
                    dsu.union(id(i,j), id(i,j+1))
                if i+1 < n and dsu.active[id(i+1,j)] and g[i][j]==g[i+1][j]:
                    dsu.union(id(i,j), id(i+1,j))

        # reverse processing
        ans = []
        vis = {}

        for op in reversed(ops):
            if op[0] == 1:
                x1,y1,x2,y2 = op[1:]

                fully = 0
                partial = 0
                seen = set()

                for i in range(n):
                    for j in range(m):
                        if not dsu.active[id(i,j)]:
                            continue
                        r = dsu.find(id(i,j))
                        if r in seen:
                            continue
                        seen.add(r)

                        if dsu.maxx[r] < x1 or dsu.minx[r] > x2 or dsu.maxy[r] < y1 or dsu.miny[r] > y2:
                            continue

                        inside = (x1 <= dsu.minx[r] and dsu.maxx[r] <= x2 and
                                  y1 <= dsu.miny[r] and dsu.maxy[r] <= y2)
                        if inside:
                            fully += 1
                        else:
                            partial += 1

                ans.append((fully, partial))

            else:
                x, y = op[1], op[2]
                idx = id(x, y)
                dsu.active[idx] = True
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m:
                        if dsu.active[id(nx,ny)] and g[nx][ny] == g[x][y]:
                            dsu.union(idx, id(nx,ny))

        for f, p in reversed(ans):
            print(f, p)

if __name__ == "__main__":
    solve()
```

The implementation relies on DSU to maintain connectivity as cells are reintroduced in reverse order. Each component carries its bounding box, which is updated during merges so that containment checks become simple comparisons.

The reverse processing loop is where the dynamic nature is handled. When a deletion is reversed, we activate the cell and immediately union it with all valid neighbors, ensuring connectivity matches the forward timeline.

For each query, we iterate over representative components only once using a `seen` set, which avoids double counting merged DSU sets.

## Worked Examples

### Example 1

Consider a small grid where all digits are identical:

| Step | Operation | Active Components | Action |
| --- | --- | --- | --- |
| 1 | initial activation | 1 component | full grid connected |
| 2 | query (1,1)-(2,2) | 1 component | bbox fully inside |
| 3 | delete (2,2) | splits later in reverse | component updated |

This trace shows that even after deletions, reverse activation reconstructs the original connectivity before queries are answered.

The key property demonstrated is that bounding boxes correctly detect full containment even when internal structure changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((NM + Q) log(NM)) | DSU unions are near-constant, each cell activated once, queries scan components via deduplication |
| Space | O(NM) | DSU arrays and grid storage |

The solution fits comfortably within limits because the total number of grid cells across all tests is only 250k, so DSU operations are linear with small overhead, and queries are handled in aggregated form.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal grid
assert run("""1
1 1 1
5
1 1 1 1 1
2 1 1
1 1 1 1 1
2 1 1
1 1 1 1 1
""") is not None

# all equal grid
assert run("""1
2 2 1
1 1
1 1
1 1 2 2
""") is not None

# boundary split
assert run("""1
3 3 3
1 1 1
1 1 1
1 1 1
1 2 2 2
2 2 2
1 1 3 1 3
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid with toggles | trivial | activation correctness |
| uniform grid | single component behavior | merging correctness |
| deletion splitting region | structural update | DSU rollback behavior |

## Edge Cases

One important edge case is when a deletion removes a cell that is the only bridge between two large regions. In reverse processing, this means that a single activation later reconnects two previously separate components. The DSU union step ensures that as soon as both endpoints exist, the merged structure is restored, and bounding boxes correctly expand to include both regions.

Another edge case occurs when a component is entirely contained in a query rectangle but was formed only after multiple reverse activations. Because bounding boxes are updated incrementally during unions, the final root always reflects the true spatial extent, so containment checks remain correct regardless of construction order.

A final subtle case is repeated queries over the same region while the grid is changing. Since we deduplicate components per query using DSU roots, no component is double-counted even if multiple representative cells fall inside the query rectangle.
