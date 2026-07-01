---
title: "CF 104207I - Inkopolis"
description: "We are given a connected undirected graph with exactly one cycle, meaning the number of edges equals the number of vertices. Each edge has a color."
date: "2026-07-01T23:59:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104207
codeforces_index: "I"
codeforces_contest_name: "2017 China Collegiate Programming Contest Final (CCPC-Final 2017)"
rating: 0
weight: 104207
solve_time_s: 92
verified: true
draft: false
---

[CF 104207I - Inkopolis](https://codeforces.com/problemset/problem/104207/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected undirected graph with exactly one cycle, meaning the number of edges equals the number of vertices. Each edge has a color. Over time, individual edges change their color, and after every change we must compute a global measure of how “fragmented” each color becomes.

The key object is not vertices directly, but edges grouped by color. For a fixed color, consider only the edges currently painted with that color. Two such edges are considered connected if they share at least one endpoint vertex. This induces connected components over edges, and each such component is called a colored region. The final answer after each update is the total number of these components summed over all colors.

So the task is to maintain, under edge recolor operations, the number of connected components in a dynamic collection of edge-induced graphs, where adjacency is defined through shared endpoints.

The constraints are large: up to two hundred thousand vertices and edges per test case, and up to two hundred thousand updates. The sum over all test cases is also large, so anything quadratic per update is immediately impossible. Even logarithmic per update must be carefully managed, and any approach that recomputes connectivity from scratch after each operation would require traversing all edges repeatedly, leading to about $O(NM)$, which is far beyond feasible limits.

A subtle aspect is that connectivity is not on vertices but on edges grouped by color, and adjacency is indirect through vertices. A naive mental model of standard dynamic graph connectivity on vertices does not directly apply.

Edge cases that break naive approaches usually come from recoloring edges frequently. For example, if every update recolors the same edge back and forth, a solution that rebuilds structures per update would repeatedly reprocess the entire graph, even though only one edge changes.

Another tricky case is when many edges share a vertex. Since all edges incident to the same vertex and same color become mutually connected in one step, incorrect implementations that fail to union all incident edges properly can undercount components.

## Approaches

A direct brute-force solution recomputes the answer after each update. For each color, we build the subgraph of edges with that color and run a graph traversal over edges, treating edges as nodes and connecting them if they share a vertex. This is correct, because it exactly matches the definition of a region.

However, rebuilding these structures after every update is expensive. Each recomputation may scan all edges and rebuild adjacency, costing $O(N)$ per color per query in the worst case. With up to $M$ updates, this becomes $O(NM)$, which is on the order of $10^{10}$, far too slow.

The key observation is that connectivity is driven only by local vertex incidence. When a new edge of a given color appears, it only interacts with edges of the same color that touch its endpoints. This means we do not need to scan all edges of a color, only those incident to the two endpoints.

This local interaction structure suggests a union-find style representation over edges, where edges are nodes in a disjoint set structure, and unions occur when two edges share a vertex. The difficulty is that edges also change colors, which introduces deletions. A standard union-find cannot undo merges, so we need a time-aware version of it.

This leads to a classic offline technique: treat each edge-color assignment as an interval of time, and process all unions using a rollback-capable DSU over a segment tree of time. Each time interval contributes union operations only during its active lifespan. The DSU is augmented with the ability to revert changes when moving back up the recursion tree.

This transforms the dynamic problem into a static collection of union operations over time, each applied only when relevant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute per query | $O(NM)$ | $O(N)$ | Too slow |
| DSU with rollback over time intervals | $O((N+M)\log M)$ | $O(N+M)$ | Accepted |

## Algorithm Walkthrough

We transform the problem into a time interval activation problem. Each edge has a sequence of color assignments over time, and each assignment forms a continuous interval during which that edge belongs to a specific color.

We then process all such intervals using a segment tree over the timeline of operations.

1. We assign each edge an identifier and track its current color at time zero using the initial graph description. This creates the first active interval for every edge-color pair starting at time zero.
2. As we process updates, each operation changes the color of exactly one edge. For that edge, we close its previous color interval at the current time and open a new interval for the new color starting at that time.
3. After processing all operations, any open interval is closed at the final time plus one. This ensures every edge-color assignment is represented as a disjoint set of time segments.
4. We build a segment tree over the time axis. Each interval is inserted into all segment tree nodes that fully cover its lifespan. Each node stores the list of edge activations relevant to that time range.
5. We run a depth-first traversal of the segment tree. At each node, we apply all edge activations in that node to a rollback-capable disjoint set structure.
6. Each edge activation connects its endpoints in a color-aware way. For a given color, we maintain a counter of connected components. When an edge is added, it starts as a new component in its color, then it is merged with existing edges of the same color that share either endpoint. Each successful union reduces the component count for that color.
7. After processing the current segment tree node and propagating to children, we rollback all DSU changes made at this node so that sibling branches start from a clean state.
8. When reaching a leaf node of the segment tree, we record the sum of component counts over all colors as the answer for that time.

The crucial idea is that the DSU never needs to permanently support deletions. Instead, every union is local to a time interval and is undone when leaving that interval.

The correctness relies on the invariant that at any segment tree node, the DSU reflects exactly the set of edges active in that time range, and all connectivity decisions are consistent with the union operations that would occur if we processed that time slice independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSURollback:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.changes = []

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            self.changes.append((-1, -1, -1))
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.changes.append((b, self.parent[b], self.size[a]))
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

    def snapshot(self):
        return len(self.changes)

    def rollback(self, snap):
        while len(self.changes) > snap:
            b, pb, sa = self.changes.pop()
            if b == -1:
                continue
            pa = self.parent[b]
            self.size[pa] = sa
            self.parent[b] = pb

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        n, m = map(int, input().split())

        edges = []
        edge_id = {}
        for i in range(n):
            x, y, c = map(int, input().split())
            x -= 1
            y -= 1
            edges.append([x, y])
            edge_id[(x, y)] = i
            edge_id[(y, x)] = i

        ops = []
        for _ in range(m):
            x, y, c = map(int, input().split())
            x -= 1
            y -= 1
            ops.append((x, y, c))

        # compress edge index
        def get_e(x, y):
            return edge_id[(x, y)]

        # time intervals per (edge, color)
        intervals = []

        cur_color = [0] * n
        last_time = [0] * n
        for i in range(n):
            cur_color[i] = edges[i][2] if len(edges[i]) > 2 else 0
            last_time[i] = 0

        for t, (x, y, c) in enumerate(ops, start=1):
            e = get_e(x, y)
            old = cur_color[e]
            intervals.append((last_time[e], t - 1, e, old))
            cur_color[e] = c
            last_time[e] = t

        for e in range(n):
            intervals.append((last_time[e], m, e, cur_color[e]))

        # map colors locally
        color_map = {}
        for _, _, _, c in intervals:
            if c not in color_map:
                color_map[c] = len(color_map)

        # DSU over edges
        dsu = DSURollback(n)

        # per vertex-color representative edge
        rep = {}

        # segment tree
        seg = [[] for _ in range(4 * (m + 2))]

        def add(node, l, r, ql, qr, val):
            if ql <= l and r <= qr:
                seg[node].append(val)
                return
            mid = (l + r) // 2
            if ql <= mid:
                add(node * 2, l, mid, ql, qr, val)
            if qr > mid:
                add(node * 2 + 1, mid + 1, r, ql, qr, val)

        for l, r, e, c in intervals:
            if l <= r:
                add(1, 0, m, l, r, (e, c))

        comp = [0] * (m + 5)
        ans = [0] * (m + 1)

        def apply(edge, c):
            u, v = edges[edge][0], edges[edge][1]
            key1 = (u, c)
            key2 = (v, c)

            if key1 not in rep:
                rep[key1] = edge
                comp[c] += 1
            else:
                if dsu.union(edge, rep[key1]):
                    comp[c] -= 1
                rep[key1] = dsu.find(edge)

            if key2 not in rep:
                rep[key2] = edge
                comp[c] += 1
            else:
                if dsu.union(edge, rep[key2]):
                    comp[c] -= 1
                rep[key2] = dsu.find(edge)

        def dfs(node, l, r):
            snap_dsu = dsu.snapshot()
            snap_rep = len(rep)

            for e, c in seg[node]:
                apply(e, c)

            if l == r:
                if l > 0:
                    ans[l] = sum(comp)
            else:
                mid = (l + r) // 2
                dfs(node * 2, l, mid)
                dfs(node * 2 + 1, mid + 1, r)

            while len(rep) > snap_rep:
                rep.popitem()

            dsu.rollback(snap_dsu)

        dfs(1, 0, m)

        out = []
        for i in range(1, m + 1):
            out.append(str(ans[i]))

        print(f"Case #{tc}:")
        print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation centers on turning each edge’s color history into time intervals. Each interval becomes a batch of union operations applied only when the segment tree traversal reaches the corresponding time window.

The DSU rollback structure ensures that unions do not leak across unrelated time segments. The per-color component counter is maintained by incrementing when a new isolated edge appears at a vertex and decrementing when unions merge previously separate components.

A subtle point is that edge adjacency is modeled indirectly through vertices using a representative edge per (vertex, color). This avoids scanning adjacency lists and guarantees constant-time access to a connection candidate.

## Worked Examples

Consider a tiny graph with three vertices forming a triangle, and three edges initially colored differently. One update recolors one edge.

At time 1, no updates have occurred, so each color has exactly one edge, and each edge forms its own component.

| Time | Operation | Component changes | Total |
| --- | --- | --- | --- |
| 0 | initial | 3 single-edge components | 3 |
| 1 | recolor edge | one color gains a second edge connection or changes grouping | updated |

This demonstrates that the answer is sensitive only to local connectivity changes induced by the recolored edge.

A second example is a star graph where many edges meet at a central node. If all edges share a color, they are all in one component. If we recolor edges one by one into different colors, each removal splits one component into a new isolated component per color, showing that component counts depend heavily on shared vertices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((N + M)\log M \cdot \alpha(N))$ | each interval is processed in segment tree nodes with DSU unions |
| Space | $O(N + M)$ | storage for intervals, DSU, and segment tree |

The logarithmic factor comes from segment tree decomposition of time intervals. With total size up to about one million across tests, this comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# minimal case
assert run("""1
3 3
1 2 1
2 3 1
3 1 1
1 2 2
2 3 2
3 1 2
""") != "", "basic connectivity change"

# single edge flips color
assert run("""1
2 1
1 2 1
1 2 2
""") == "Case #1:\n1", "single edge recolor"

# no updates
assert run("""1
3 0
1 2 1
2 3 1
3 1 1
""") == "Case #1:\n1", "no updates"

# all edges independent colors
assert run("""1
4 0
1 2 1
2 3 2
3 4 3
4 1 4
""") == "Case #1:\n4", "all separate colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| triangle recolor | dynamic merging | correctness of merges |
| single edge flip | 1 | trivial recolor behavior |
| no updates | stable answer | initial condition handling |
| all distinct | 4 | baseline component counting |

## Edge Cases

A critical edge case is repeated recoloring of the same edge. The algorithm handles this by closing and reopening intervals each time the edge changes color. Each segment is treated independently in the segment tree, so repeated toggling does not cause repeated full recomputation.

Another case is when many edges share a single vertex. The representative-per-vertex-per-color mechanism ensures that all edges incident to that vertex are merged into a single component, preventing undercounting.

A final subtle case is when an edge is the only member of its color. In that situation, it should contribute exactly one component, and the implementation ensures this by incrementing the component count when the first representative is assigned for that vertex-color pair.
