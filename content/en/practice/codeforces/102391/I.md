---
title: "CF 102391I - Minimum Diameter Spanning Tree"
description: "We need to choose exactly (N-1) edges from a connected weighted undirected graph so that every vertex is reachable and the resulting graph is a tree. Among all such spanning trees, we want one whose longest weighted path is as short as possible."
date: "2026-08-14T14:05:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "I"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 413
verified: false
draft: false
---

[CF 102391I - Minimum Diameter Spanning Tree](https://codeforces.com/problemset/problem/102391/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We need to choose exactly (N-1) edges from a connected weighted undirected graph so that every vertex is reachable and the resulting graph is a tree. Among all such spanning trees, we want one whose longest weighted path is as short as possible. The output must contain that minimum possible diameter and the edges of one tree attaining it. The statement allows any optimal tree, so different correct outputs can contain different edges.

The key difficulty is that minimizing the diameter is not the same as minimizing total edge weight. A minimum spanning tree can have a very long branch even when the original graph contains short routes that would give a much smaller diameter.

With (N\le 500), cubic time is the natural target. A full all-pairs shortest-path computation takes (O(N^3)), which is about (125) million elementary distance updates at the maximum size. Enumerating spanning trees is completely impossible, since a complete graph on (N) vertices already has (N^{N-2}) spanning trees. The bound (M\le N(N-1)/2) also means we must be comfortable with dense graphs, so an algorithm whose main term is (O(NM)) is still (O(N^3)) in the worst case.

There are three cases that a careless solution can miss.

First, the optimal center need not be an original vertex. Consider

```
3 2
1 2 2
2 3 4
```

The only spanning tree is the graph itself, so the correct diameter is (6), using edges (1\ 2) and (2\ 3). Its center is one unit inside edge (2\ 3), not at vertex (2) or vertex (3). Looking only at vertex centers would incorrectly obtain (8), because the eccentricity of vertex (2) is (4).

Second, a graph edge used by the original graph need not belong to an optimal spanning tree. For example,

```
4 6
1 2 1
2 3 1
3 4 1
1 4 100
1 3 10
2 4 10
```

The tree (1-2-3-4) has diameter (3), which is optimal because every spanning tree has to connect vertices (1) and (4), and the graph contains the three unit edges forming this path. A careless construction that favors the edge (1-4) because it directly connects the endpoints can produce a much worse tree.

Third, several shortest paths can have the same length. For

```
3 3
1 2 1
2 3 1
1 3 1
```

the correct diameter is (2), and both the trees ({1-2,2-3}), ({1-2,1-3}), and ({1-3,2-3}) are valid answers. The implementation must not depend on a particular tie-breaking order.

## Approaches

A brute-force solution would enumerate every subset of (N-1) graph edges, test whether the subset is a spanning tree, and then compute its diameter. There are

[
\binom{M}{N-1}
]

such subsets. Testing one subset already costs at least (O(N+M)) if we use graph traversal to check connectivity, so the worst-case work is

[
O\left(\binom{M}{N-1}(N+M)\right).
]

For (N=500) and a complete graph, (M=124750), making this astronomically larger than any feasible operation count. The brute force is correct because it literally checks every possible spanning tree, but the number of candidates is the wrong quantity to enumerate.

The useful observation is that every tree has a center. Take a longest path of a tree and look at its midpoint. The midpoint is either an existing vertex or lies somewhere inside an edge. If the midpoint is a vertex (c), every vertex is at tree distance at most half the diameter from (c). Since graph shortest paths can only be shorter than tree paths, the graph eccentricity of (c) is also at most half the tree diameter.

This immediately connects the problem to shortest-path trees. If we choose a vertex (c) and build a shortest-path tree rooted at (c), every root-to-vertex distance becomes the graph distance. Its diameter is at most twice the eccentricity of (c). If (c) is the center of an optimal tree, this bound reaches the optimum.

The complication is the second case, where the center lies inside an edge. The standard solution handles this by treating an arbitrary point on an edge as a temporary dummy vertex. The minimum possible eccentricity over all such points is the absolute 1-center of the graph, and a shortest-path tree rooted at that center gives a minimum-diameter spanning tree. This equivalence is the classical reduction behind the (O(NM+N^3)) solution.

For an edge (e=(u,v)) of weight (w), suppose the dummy center is (x) units from (u). For any vertex (z), its distance from the center is

[
\min(x+d(u,z),\ w-x+d(v,z)).
]

For a fixed (z), this is a V-shaped function of (x), with slopes (+1) and (-1). The maximum over all vertices is the upper envelope of these V-shaped functions. The minimum of that envelope occurs either at an endpoint, which is already covered by the vertex-center cases, or at an intersection between two consecutive relevant functions.

For one edge, sort all vertices by (d(u,z)) in decreasing order. While scanning this order, keep only vertices whose (d(v,z)) is strictly increasing. These are exactly the vertices that can appear on the upper envelope. If consecutive retained vertices are (a) and (b), the two relevant lines intersect at

[
x=\frac{w-d(u,a)+d(v,b)}{2},
]

and the corresponding eccentricity is

[
\frac{w+d(u,a)+d(v,b)}{2}.
]

Thus the candidate diameter is simply

[
w+d(u,a)+d(v,b).
]

This turns the continuous optimization along an edge into a linear scan of (N) distance pairs.

The required all-pairs distances can be obtained by Floyd-Warshall. We also precompute the distance order for every possible endpoint once, rather than sorting separately for every graph edge. The total complexity becomes (O(N^3+NM+N^2\log N)), which is (O(N^3)) at the given bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(\binom{M}{N-1}(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O(N^3+NM+N^2\log N)) | (O(N^2+M)) | Accepted |

## Algorithm Walkthrough

1. Store the graph as an adjacency list and as a distance matrix. The matrix initially contains the given edge weights and zero on the diagonal. Since all weights are positive, there are no negative-cycle complications.
2. Run Floyd-Warshall to compute (d(u,v)), the shortest distance between every pair of original vertices. The later center computation depends only on these shortest-path distances, not on the original edge structure.
3. For every vertex (c), compute its eccentricity as the maximum value in row (c). A center located exactly at (c) gives a candidate diameter (2\operatorname{ecc}(c)). Store the best vertex candidate.
4. For every graph edge (e=(u,v)) of weight (w), consider a possible center somewhere inside that edge. For this edge, sort the vertices by (d(u,z)) in decreasing order. The sorting order is reused for every edge incident to the same (u), so it is computed only once per vertex.
5. Scan that order from farthest to nearest. Keep the last vertex whose distance from (v) is larger than the previously kept value. If the current vertex is (a) and the previous retained vertex is (b), the two corresponding envelope segments meet at a possible local minimum. Its candidate diameter is

[
d(u,a)+w+d(v,b).
]

If this value improves the answer, store (e), (a), and (b). The corresponding center position, measured twice to avoid fractions, is

[
2x=w+d(v,b)-d(u,a).
]

1. After all vertices and edges have been examined, the stored candidate is an absolute center of the graph. The minimum-diameter spanning tree can be obtained from a shortest-path tree rooted at this center. This is the central structural property of the problem.
2. If the center is an original vertex, run Dijkstra from that vertex and keep the predecessor edge of every vertex except the root. Since every predecessor is chosen along a shortest path from the center, these (N-1) edges form the required shortest-path tree.
3. If the center lies on an edge ((u,v)), remove that edge temporarily and replace it conceptually by a dummy vertex (c). The two dummy edges have lengths (x) and (w-x). We run multi-source Dijkstra by initializing (u) with distance (x) and (v) with distance (w-x). We do not need floating point arithmetic, because all distances can be doubled. Thus the initial distances are (2x) and (2(w-x)), both integers.
4. The resulting predecessor structure is a shortest-path tree in the graph with the dummy center. If only one of (u) and (v) remains directly attached to the dummy, removing that dummy attachment already leaves a spanning tree on the original vertices. If both remain attached, removing both dummy edges leaves two components, so we add the original edge ((u,v)) to reconnect them.
5. Print the stored minimum diameter and the (N-1) original graph edges obtained from the predecessor tree.

The invariant behind the whole algorithm is that the chosen center has minimum possible maximum shortest-path distance to the graph vertices. Any spanning tree with diameter (D) has a midpoint whose eccentricity is at most (D/2), so twice the eccentricity of the absolute center is a lower bound on every possible tree diameter. Conversely, a shortest-path tree rooted at that center has every vertex within the center's eccentricity, so every tree path is at most twice that value. The lower and upper bounds coincide, proving optimality. The edge scan finds the exact minimum eccentricity on every possible edge, while the vertex scan handles centers at endpoints.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def dijkstra_vertex(n, adj, root):
    dist = [INF] * n
    parent = [-1] * n
    dist[root] = 0
    pq = [(0, root)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue

        for v, w, eid in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return parent

def dijkstra_edge_center(n, adj, u, v, banned_eid, x2, w):
    # All distances are doubled.
    # The dummy center has doubled distances x2 and 2*w-x2
    # to u and v respectively.
    dist = [INF] * n
    parent = [-2] * n  # -2 means directly attached to dummy
    pq = []

    dv = 2 * w - x2

    dist[u] = x2
    dist[v] = dv
    heapq.heappush(pq, (x2, u))
    if v != u:
        heapq.heappush(pq, (dv, v))

    while pq:
        d, cur = heapq.heappop(pq)
        if d != dist[cur]:
            continue

        for to, ew, eid in adj[cur]:
            if eid == banned_eid:
                continue

            nd = d + 2 * ew
            if nd < dist[to]:
                dist[to] = nd
                parent[to] = cur
                heapq.heappush(pq, (nd, to))

    result = []

    for node in range(n):
        if parent[node] >= 0:
            result.append((parent[node], node))

    # If both u and v are still attached to the dummy, the two
    # components must be joined by the original center edge.
    if parent[u] == -2 and parent[v] == -2:
        result.append((u, v))

    return result

def solve():
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    edges = []

    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    for eid in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v, w))
        adj[u].append((v, w, eid))
        adj[v].append((u, w, eid))

        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w

    # Floyd-Warshall.
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik >= INF:
                continue

            # The explicit loop avoids creating a large temporary
            # matrix row and works well for n <= 500.
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    # Distance orders, reused for every edge.
    orders = []
    for u in range(n):
        row = dist[u]
        order = list(range(n))
        order.sort(key=row.__getitem__, reverse=True)
        orders.append(order)

    best_diameter = INF
    best_type = 0
    best_root = -1
    best_edge = -1
    best_a = -1
    best_b = -1

    # Centers at original vertices.
    for u in range(n):
        ecc = max(dist[u])
        candidate = 2 * ecc
        if candidate < best_diameter:
            best_diameter = candidate
            best_type = 0
            best_root = u

    # Centers inside graph edges.
    for eid, (u, v, w) in enumerate(edges):
        order = orders[u]

        last = order[0]
        b_last = dist[v][last]

        for now in order[1:]:
            b_now = dist[v][now]

            if b_now > b_last:
                candidate = dist[u][now] + w + b_last

                if candidate < best_diameter:
                    best_diameter = candidate
                    best_type = 1
                    best_edge = eid
                    best_a = now
                    best_b = last

                last = now
                b_last = b_now

    # Construct the shortest-path tree from the selected center.
    if best_type == 0:
        parent = dijkstra_vertex(n, adj, best_root)
        answer_edges = []

        for v in range(n):
            if v != best_root:
                answer_edges.append((parent[v], v))
    else:
        u, v, w = edges[best_edge]

        # If a is the vertex on the u-side and b is the vertex on
        # the v-side, the center position satisfies
        #
        # x = (w + d(v,b) - d(u,a)) / 2.
        #
        # We store 2*x.
        x2 = w + dist[v][best_b] - dist[u][best_a]

        answer_edges = dijkstra_edge_center(
            n, adj, u, v, best_edge, x2, w
        )

    out = [str(best_diameter)]
    out.extend(f"{u + 1} {v + 1}" for u, v in answer_edges)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The distance matrix is initialized with the original edge lengths and then closed under shortest paths by Floyd-Warshall. The graph is simple, so each pair has at most one input edge, but taking the minimum during initialization also makes the matrix construction robust.

The `orders` array is a significant implementation detail. For each endpoint (u), it stores all vertices in decreasing order of (d(u,\cdot)). An edge ((u,v)) can then reuse `orders[u]`, avoiding a sort inside the (M)-edge loop.

The vertex-center phase is deliberately simple. For each vertex, its eccentricity is just the largest value in its distance row, so the candidate diameter is twice that value.

The edge-center phase follows the upper-envelope scan. `last` is the previously retained vertex, while `now` is the current vertex in decreasing order of distance from (u). The condition `b_now > b_last` means that the second coordinate has moved in the direction required for a new upper-envelope segment. The candidate `dist[u][now] + w + b_last` is exactly twice the local minimum of the two corresponding V-shaped functions.

The center itself may lie at a half-integer position along the edge. Floating point arithmetic would be unnecessary and potentially dangerous, so the construction uses doubled distances. If the diameter is (D), the doubled distance from the dummy center to the (u)-side endpoint is

[
2x=D-2d(u,a),
]

which is the same value computed as `w + dist[v][best_b] - dist[u][best_a]`.

For an edge-centered candidate, the original center edge is temporarily excluded from Dijkstra. This is necessary because the dummy center represents a point inside that edge, not a separate route that is allowed to bypass the center. The two endpoints are initialized as sources at their distances from the dummy center.

The value `parent[node] == -2` means that the vertex is directly connected to the dummy center in the conceptual shortest-path tree. If both endpoints retain that status, the original edge must be restored after removing the dummy. If only one remains attached, the predecessor edges already form a spanning tree on the original graph.

Python integers have arbitrary precision, so edge weights up to (10^9), paths containing up to (499) edges, and doubled distances all fit without any overflow handling.

## Worked Examples

### Sample 1

The graph is a triangle with all edge lengths equal to (1).

| Stage | Key state | Value |
| --- | --- | --- |
| APSP | (d(1,2),d(1,3),d(2,3)) | (1,1,1) |
| Vertex 1 | eccentricity | (1) |
| Vertex 2 | eccentricity | (1) |
| Vertex 3 | eccentricity | (1) |
| Best vertex candidate | (2\cdot 1) | (2) |
| Edge candidates | minimum | (2) |
| Selected center | one possible vertex | (1) |
| Constructed tree | two edges | (1-2,\ 1-3) |
| Diameter | (1+1) | (2) |

Every vertex has eccentricity (1), so every vertex is an optimal center. Dijkstra from any of them produces a two-edge star, whose diameter is (2). This demonstrates that ties in shortest paths and ties between centers are harmless.

### Sample 2

The graph has a heavy bridge-like connection between the left cluster and the right cluster.

| Stage | Key state | Value |
| --- | --- | --- |
| Left cluster | short distances | (10,20,30) scale |
| Right cluster | short distances | (10,20,30) scale |
| Connecting edge | (3-4) | (1000) |
| Best vertex center | diameter candidate | larger than (1060) |
| Edge center | edge | (3-4) |
| Edge-center candidate | (d(3,a)+1000+d(4,b)) | (1060) |
| Selected diameter | minimum | (1060) |
| Constructed tree | cross-cluster edge | (3-4) |
| Final tree | five edges | (3-4,4-6,6-5,3-2,2-1) |
| Diameter | longest tree path | (1060) |

The important feature is that the optimal center lies on the edge of weight (1000). The two sides have their own short structures, so placing the center inside that heavy edge balances the two sides better than choosing either endpoint as the center.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3+NM+N^2\log N)) | Floyd-Warshall costs (O(N^3)), sorting all distance orders costs (O(N^2\log N)), and scanning every edge's order costs (O(NM)) |
| Space | (O(N^2+M)) | The distance matrix uses (O(N^2)), while the graph and edge list use (O(M)) |

With (N\le500), both (N^3) and (NM) are at most on the order of (10^8) operations. The memory requirement is modest because a (500\times500) distance matrix is only (250000) entries. The algorithm is the intended polynomial approach for these bounds, although the Floyd-Warshall portion is the performance-critical part of a Python implementation.

## Test Cases

Because the problem accepts any optimal spanning tree, the tests should validate the reported diameter and the tree itself rather than compare the complete output string character by character.

```python
# Paste the solve() implementation from the solution above before this test code.

import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str, expected_diameter: int):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)

    weights = {}
    for _ in range(m):
        u = next(it)
        v = next(it)
        w = next(it)
        if u > v:
            u, v = v, u
        weights[(u, v)] = w

    lines = out.strip().splitlines()
    assert len(lines) == n, "wrong number of output lines"

    diameter = int(lines[0])
    assert diameter == expected_diameter, (
        f"wrong diameter: got {diameter}, expected {expected_diameter}"
    )

    tree = [[] for _ in range(n)]
    used = set()

    for line in lines[1:]:
        u, v = map(int, line.split())
        assert 1 <= u <= n and 1 <= v <= n and u != v

        key = (min(u, v), max(u, v))
        assert key in weights, "output contains an edge not in the graph"
        assert key not in used, "duplicate tree edge"

        used.add(key)
        w = weights[key]
        tree[u - 1].append((v - 1, w))
        tree[v - 1].append((u - 1, w))

    assert len(used) == n - 1

    parent = [-1] * n
    parent[0] = 0
    stack = [0]
    order = []

    while stack:
        u = stack.pop()
        order.append(u)
        for v, _ in tree[u]:
            if v == parent[u]:
                continue
            assert parent[v] == -1, "cycle in output"
            parent[v] = u
            stack.append(v)

    assert len(order) == n, "output edges do not connect all vertices"

    def farthest(start):
        dist = [-1] * n
        dist[start] = 0
        stack = [start]
        best = start

        while stack:
            u = stack.pop()
            if dist[u] > dist[best]:
                best = u

            for v, w in tree[u]:
                if dist[v] != -1:
                    continue
                dist[v] = dist[u] + w
                stack.append(v)

        return best, dist[best]

    a, _ = farthest(0)
    _, tree_diameter = farthest(a)

    assert tree_diameter == expected_diameter, (
        f"constructed tree has diameter {tree_diameter}"
    )

# Sample 1.
sample1 = """\
3 3
1 2 1
2 3 1
3 1 1
"""
validate(sample1, run(sample1), 2)

# Sample 2.
sample2 = """\
6 7
1 2 10
2 3 20
1 3 30
3 4 1000
4 5 30
5 6 20
4 6 10
"""
validate(sample2, run(sample2), 1060)

# Minimum-size graph.
case_min = """\
2 1
1 2 7
"""
validate(case_min, run(case_min), 7)

# Center lies inside an edge.
case_edge_center = """\
3 2
1 2 2
2 3 4
"""
validate(case_edge_center, run(case_edge_center), 6)

# All edge weights equal.
case_equal = """\
4 6
1 2 5
1 3 5
1 4 5
2 3 5
2 4 5
3 4 5
"""
validate(case_equal, run(case_equal), 10)

# A very long direct edge should not be forced into the tree.
case_long = """\
4 6
1 2 1
2 3 1
3 4 1
1 4 100
1 3 10
2 4 10
"""
validate(case_long, run(case_long), 3)

# Maximum-size style test, 500 vertices.
# A unit-weight star is already optimal and has diameter 2.
n = 500
parts = [f"{n} {n - 1}"]
for v in range(2, n + 1):
    parts.append(f"1 {v} 1")
case_max = "\n".join(parts) + "\n"

validate(case_max, run(case_max), 2)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2 7` | Diameter (7) | Minimum (N), single-edge tree, boundary handling |
| `3 2 / 1 2 2 / 2 3 4` | Diameter (6) | Center strictly inside an edge and half-integer-safe construction |
| Complete graph on 4 vertices, every weight (5) | Diameter (10) | Equal distances, many optimal trees, tie handling |
| Four-vertex graph with a weight-(100) edge | Diameter (3) | Avoiding an attractive but harmful long edge |
| Unit star with (500) vertices | Diameter (2) | Maximum (N), sparse graph, large input size |

## Edge Cases

The first edge case is the minimum-size graph:

```
2 1
1 2 7
```

There is only one spanning tree, namely the single edge (1-2), so its diameter is (7). The vertex-center scan gives eccentricity (7) for either vertex and candidate diameter (14), which looks too large if interpreted as the tree diameter. This is why the general center argument must be understood carefully: the midpoint of a single edge is a dummy center. The edge scan considers edge (1-2), finds the center at distance (3.5) from either endpoint, and produces candidate diameter (7). The construction uses doubled dummy distances, so no floating point value (3.5) is ever stored.

The second edge case is the weighted path

```
3 2
1 2 2
2 3 4
```

The only possible tree has diameter (6). Vertex (2) has eccentricity (4), so a vertex-only algorithm would report (8). For edge (2-3), the relevant vertices are (1) and (3). Their distance pairs from the endpoints are ((2,6)) and ((4,0)). Their envelope intersection gives

[
D=2+4+0=6,
]

and the doubled center coordinate is (4+0-2=2), meaning the center is one unit from vertex (2). The edge-centered Dijkstra construction recovers the original two edges.

The third edge case is the complete equal-weight graph:

```
4 6
1 2 5
1 3 5
1 4 5
2 3 5
2 4 5
3 4 5
```

A star centered at any vertex has diameter (10), which is optimal because every pair of distinct vertices is separated by at least one edge of weight (5), and a tree on four vertices cannot have diameter below (10) in this graph. The implementation may choose a different star from the one a human expects because all distance comparisons can tie. The validator checks the tree property and diameter rather than requiring a particular edge order.

The fourth edge case contains a very long edge:

```
4 6
1 2 1
2 3 1
3 4 1
1 4 100
1 3 10
2 4 10
```

Floyd-Warshall first discovers that the shortest distances between the vertices are governed by the three unit edges. The center computation consequently favors the short central region of the graph. The final tree can use (1-2), (2-3), and (3-4), giving diameter (3). The weight-(100) edge is never required merely because it exists.

The fifth edge case is a graph whose removal of the selected center edge disconnects the graph:

```
3 2
1 2 2
2 3 4
```

When edge (2-3) is treated as the center edge, the temporary graph has two components, one containing vertex (1,2) and the other containing vertex (3). Multi-source Dijkstra starts from both sides of the dummy center. Both endpoints remain directly attached to the conceptual dummy, so the construction removes those two dummy connections and restores the original edge (2-3). Exactly two original edges remain, giving a spanning tree.

The last subtle case is a non-bridge center edge. If an alternative path connects its endpoints, multi-source Dijkstra may discover one endpoint more cheaply from the other side. Then only one endpoint remains directly attached to the dummy center. The predecessor edges already connect all original vertices into one tree, so the original center edge is not added a second time. This is why the construction checks whether both endpoints are still dummy roots rather than blindly adding the center edge.
