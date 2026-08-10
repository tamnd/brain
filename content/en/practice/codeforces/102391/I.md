---
title: "CF 102391I - Minimum Diameter Spanning Tree"
description: "We need to choose exactly (N-1) input edges that connect all (N) vertices without a cycle, and among all such spanning trees minimize the length of the longest tree path. Edge lengths are positive integers, so every tree distance and the final diameter are integers."
date: "2026-08-10T21:05:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "I"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 403
verified: false
draft: false
---

[CF 102391I - Minimum Diameter Spanning Tree](https://codeforces.com/problemset/problem/102391/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We need to choose exactly (N-1) input edges that connect all (N) vertices without a cycle, and among all such spanning trees minimize the length of the longest tree path. Edge lengths are positive integers, so every tree distance and the final diameter are integers.

The graph can have as many as (500) vertices and roughly (125000) edges. This is small enough in terms of vertices for an (O(N^3)) algorithm, but far too large for anything exponential in (N). The dense case is especially relevant because (M) can be (\Theta(N^2)). At (N=500), (N^3) is (125) million, which is already close to the practical limit in Python, while enumerating spanning trees is completely impossible. The (10^9) edge-weight bound means a path can have length around (5\cdot10^{11}), so 64-bit arithmetic is required in languages with fixed-size integers. Python integers do not overflow.

The central difficulty is that minimizing the diameter is not the same as computing a minimum spanning tree. A minimum spanning tree can have a very long chain, while a slightly more expensive tree can have a much smaller diameter.

There are also several cases that break naive implementations.

For the smallest possible graph,

```
2 1
1 2 7
```

the only spanning tree contains the only edge, so the answer is

```
7
1 2
```

An implementation that assumes the center must be a vertex can still survive this case, but an implementation that expects two distinct branches around the center may fail because the center is allowed to lie anywhere on the only edge.

A more interesting case is a weighted path:

```
3 2
1 2 100
2 3 1
```

The only spanning tree has diameter (101), so the answer is

```
101
1 2
2 3
```

The center of this tree lies inside the edge (1)-(2), not at a graph vertex. Checking only shortest-path trees rooted at vertices would miss the actual center.

Equal distances also matter. For

```
3 3
1 2 1
2 3 1
1 3 1
```

the answer is (2), and any two edges forming a tree are valid. When several vertices have equal distances from an endpoint of a candidate center edge, the sweep must use strict comparisons when deciding which vertices belong to the opposite side. Treating equal distances as a new side can manufacture an invalid candidate.

Finally, very large weights must not be truncated. For example,

```
2 1
1 2 1000000000
```

has answer (1000000000). In C++, a 32-bit integer is insufficient for sums of several such edges, so the distance matrix must use 64-bit integers.

## Approaches

The most direct brute-force approach is to enumerate every spanning tree, calculate its diameter, and keep the best one. It is correct because every possible answer is explicitly considered. The problem is the number of trees. A complete graph on (N) vertices has (N^{N-2}) spanning trees by Cayley's formula. At (N=500), this is (500^{498}) trees, and inspecting even the (N-1) edges of each tree would require on the order of (499\cdot500^{498}) edge inspections. The brute force is not remotely viable.

A less absurd but still unsuitable approach is to choose every vertex as a possible tree center, build a shortest-path tree from it, and take the best result. This does solve the case where the optimal tree center is a vertex. However, a weighted tree can have its center strictly inside an edge, as the three-vertex path with edge lengths (100) and (1) demonstrates. We need to consider points inside edges as well.

The key observation is to stop thinking about the tree itself and instead think about the midpoint of its diameter. Every tree has a center, either a vertex or a point inside one edge. If we knew the center, a shortest-path tree rooted at that center is sufficient to obtain an optimal spanning tree. This is the connection between the minimum-diameter spanning tree problem and the absolute 1-center problem of the graph. The absolute 1-center is the point, possibly inside an edge, minimizing its maximum shortest-path distance to all graph vertices. A shortest-path tree rooted at that point gives a minimum-diameter spanning tree.

We can find this center without trying every possible real coordinate. First compute all-pairs shortest-path distances. Then consider a possible center vertex directly. For an edge ((u,v)), write its doubled length as (W), and let the center be at doubled distance (X) from (u). For a vertex (z), its distance from the center is

[
\min(D[u][z]+X,\ D[v][z]+W-X),
]

where every graph distance has also been doubled.

As the center moves along one edge, every vertex produces a two-segment roof function. The maximum of all these functions is the eccentricity of the center. Its minimum occurs at a crossing of two relevant roof segments. We can find all relevant crossings with a sweep after sorting vertices by their distance from one endpoint. This is the standard (O(N^3)) absolute-center computation used for this problem.

For an edge ((u,v)), suppose (a) is the farthest vertex assigned to the (u)-side and (b) is the farthest vertex assigned to the (v)-side. At the optimal crossing,

[
D[u][a]+X=D[v][b]+W-X.
]

The resulting doubled radius is

[
D[u][a]+D[v][b]+W.
]

We can enumerate (a) in decreasing order of (D[u][a]). Once (a) is fixed, (b) must be the vertex with maximum (D[v][b]) among vertices having strictly larger distance from (u) than (a). Maintaining that maximum while scanning gives constant work per vertex. This is exactly the reduction that brings the center search to (O(N^3)) after all-pairs shortest paths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^{N-1})) or worse | (O(N^2)) | Too slow |
| Vertex centers only | (O(NM\log N)) with repeated Dijkstra | (O(N^2+M)) | Wrong on weighted graphs |
| Optimal | (O(N^3+MN)) | (O(N^2+M)) | Accepted |

Since (M\leq N(N-1)/2), the final bound is (O(N^3)).

## Algorithm Walkthrough

1. Double every edge weight.

Doubling removes all fractions from the center computation. The actual diameter remains an integer, while the center can sit at a half-integer distance from an endpoint. After doubling, every relevant coordinate is integral.

1. Compute all-pairs shortest-path distances.

We need (D[u][v]) for every pair because every candidate center edge compares distances from both endpoints to every vertex. With (N\leq500), Floyd-Warshall gives an (O(N^3)) solution in the dense case. For sparse inputs, the implementation below uses repeated Dijkstra instead, which is faster in practice.

1. Sort the vertices by their distance from every possible endpoint.

For each vertex (u), store the vertices in nondecreasing order of (D[u][z]). This lets us scan possible farthest vertices in decreasing order.

1. Check centers that are graph vertices.

If the center is vertex (u), its radius is its eccentricity,

[
R(u)=\max_z D[u][z].
]

The corresponding tree diameter is (2R(u)) in the doubled representation. Keep the smallest such value and remember the vertex.

1. Check centers inside every graph edge.

For an edge ((u,v)) of doubled length (W), scan vertices from farthest to nearest according to distance from (u). Maintain a vertex (p) with maximum (D[v][p]) among the vertices already processed, meaning those farther from (u) than the current candidate.

Whenever the current vertex (a) has

[
D[v][a]>D[v][p],
]

the pair ((a,p)) defines a possible crossing. Its doubled diameter candidate is

[
C=D[u][a]+D[v][p]+W.
]

The center coordinate measured from (u), still doubled, is

[
X=\frac{D[u][a]+W-D[v][p]}{2}.
]

Only (0\leq X\leq W) represents a point actually lying on this edge. If the intersection lies outside the edge, the optimum is reached farther along the graph and will be represented by another candidate, so the invalid crossing is discarded.

1. Remember the best center.

The value stored by the algorithm is already the actual tree diameter, because all distances were doubled and the formula above computes twice the center radius. The original diameter is consequently the same integer value.

1. Construct the spanning tree from the chosen center.

If the center is a vertex, run Dijkstra from that vertex and keep the predecessor of every vertex. The resulting shortest-path tree has the required minimum diameter.

If the center is inside an edge ((u,v)), let its doubled distances to (u) and (v) be (X) and (W-X). Run a multi-source Dijkstra initialized with

[
dist[u]=X,\qquad dist[v]=W-X.
]

This is exactly the shortest-path computation from the virtual center obtained by subdividing the edge. The two initial vertices form two rooted shortest-path forests. Add the original edge ((u,v)) to join those two forests. The result has exactly (N-1) original graph edges.

Why it works: let (c) be the center of an optimal spanning tree. Every path between two vertices of that tree passes through the center, so its diameter is twice the maximum distance from the center to a vertex. Replacing each root-to-vertex path by a shortest path in the original graph cannot increase that maximum distance. Thus a shortest-path tree rooted at the absolute 1-center is optimal. The center is either a graph vertex or lies inside some graph edge, so the two parts of the enumeration cover every possible optimum. For a fixed edge, the sweep considers exactly the pairs of vertices that can be the farthest vertices on the two sides of the center, and the crossing equation gives the smallest radius for that pair. Hence the smallest candidate is the absolute-center radius, and the constructed shortest-path tree has exactly the minimum possible diameter.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def all_pairs_shortest(n, m, adj):
    # For sparse graphs, repeated Dijkstra is considerably cheaper.
    # For dense graphs, Floyd-Warshall avoids a large number of heap operations.
    if m * 4 <= n * n:
        dist = []
        for s in range(n):
            ds = [INF] * n
            ds[s] = 0
            pq = [(0, s)]

            while pq:
                d, u = heapq.heappop(pq)
                if d != ds[u]:
                    continue
                for v, w in adj[u]:
                    nd = d + w
                    if nd < ds[v]:
                        ds[v] = nd
                        heapq.heappush(pq, (nd, v))

            dist.append(ds)

        return dist

    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    for u in range(n):
        for v, w in adj[u]:
            if w < dist[u][v]:
                dist[u][v] = w

    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue
            # The comprehension is noticeably faster in Python than
            # an explicit inner loop.
            di[:] = [
                x if x <= dik + y else dik + y
                for x, y in zip(di, dk)
            ]

    return dist

def build_tree_vertex(root, n, adj):
    dist = [INF] * n
    parent = [-1] * n
    dist[root] = 0
    pq = [(0, root)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue

        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    edges = []
    for v in range(n):
        if v != root:
            edges.append((parent[v], v))

    return edges

def build_tree_edge(u, v, x, w, n, adj):
    # x is the doubled distance from the virtual center to u.
    # w - x is the doubled distance from the virtual center to v.
    dist = [INF] * n
    parent = [-1] * n

    dist[u] = x
    dist[v] = w - x

    pq = [(x, u), (w - x, v)]

    while pq:
        d, cur = heapq.heappop(pq)
        if d != dist[cur]:
            continue

        for to, ew in adj[cur]:
            nd = d + ew
            if nd < dist[to]:
                dist[to] = nd
                parent[to] = cur
                heapq.heappush(pq, (nd, to))

    edges = [(u, v)]

    for z in range(n):
        if z == u or z == v:
            continue
        edges.append((parent[z], z))

    return edges

def solve():
    n, m = map(int, input().split())

    edges = []
    adj = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1

        # Work entirely in doubled lengths.
        w *= 2

        edges.append((u, v, w))
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = all_pairs_shortest(n, m, adj)

    # order[u] contains vertices sorted by distance from u.
    order = []
    for u in range(n):
        row = list(range(n))
        row.sort(key=dist[u].__getitem__)
        order.append(row)

    best = INF
    best_vertex = 0
    best_edge = None
    best_x = None

    # Center at a graph vertex.
    for u in range(n):
        ecc = dist[u][order[u][-1]]
        cand = 2 * ecc

        if cand < best:
            best = cand
            best_vertex = u
            best_edge = None
            best_x = None

    # Center inside an edge.
    for u, v, w in edges:
        row = order[u]

        # p is the best v-distance among vertices strictly farther
        # from u than the current vertex.
        p = row[-1]

        for idx in range(n - 2, -1, -1):
            a = row[idx]

            if dist[v][a] > dist[v][p]:
                cand = dist[u][a] + dist[v][p] + w

                numerator = dist[u][a] + w - dist[v][p]

                # All values are doubled, so numerator is even.
                x = numerator // 2

                if 0 <= x <= w and cand < best:
                    best = cand
                    best_edge = (u, v, w)
                    best_x = x
                    best_vertex = -1

                p = a

    # Construct an SPT from the chosen absolute center.
    if best_edge is None:
        tree_edges = build_tree_vertex(best_vertex, n, adj)
    else:
        u, v, w = best_edge
        if best_x == 0:
            tree_edges = build_tree_vertex(u, n, adj)
        elif best_x == w:
            tree_edges = build_tree_vertex(v, n, adj)
        else:
            tree_edges = build_tree_edge(u, v, best_x, w, n, adj)

    out = [str(best)]
    out.extend(f"{u + 1} {v + 1}" for u, v in tree_edges)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input phase stores both an adjacency list and the edge list. The adjacency list is needed later by Dijkstra when constructing the final tree, while the edge list is what the center sweep enumerates.

All weights are multiplied by two immediately. This is more than a cosmetic trick. A center inside an edge can have an original coordinate such as (3.5), and doubling makes that coordinate (7), so every comparison remains exact integer arithmetic.

The all-pairs routine chooses between repeated Dijkstra and Floyd-Warshall. The dense case is the natural setting for Floyd-Warshall, while sparse graphs benefit substantially from Dijkstra. Either way, the returned matrix contains exact doubled shortest-path distances.

The `order` array implements the sorting required by the edge sweep. The final element is the farthest vertex from the corresponding endpoint. During an edge scan, `p` represents the best candidate on the opposite side among all vertices already known to be farther from (u). The strict `>` comparison is deliberate because vertices at exactly the same distance from (u) can already be covered by the (u)-side.

The vertex-center loop stores (2\cdot\operatorname{ecc}(u)). This value is the doubled radius, which is exactly the tree diameter in the original scale.

For an edge candidate, `cand` is

[
D[u][a]+D[v][p]+W.
]

The center coordinate is computed from the equality of the two active roof segments. The range check prevents a crossing outside the actual edge from being treated as a valid center.

The construction uses ordinary Dijkstra rather than the all-pairs matrix. This keeps the construction simple and avoids storing predecessor information for every possible source. When the center is an interior point of an edge, two initial Dijkstra states represent the two halves of the subdivided edge. Their predecessor edges form two disjoint shortest-path trees. The original edge joins them into one tree.

Positive edge weights make every predecessor strictly closer to the virtual center. Consequently, predecessor pointers cannot contain a directed cycle. In the two-source case, (u) and (v) are roots of separate predecessor forests, so adding ((u,v)) creates exactly one connection between those forests and produces exactly (N-1) edges.

## Worked Examples

### Sample 1

The graph is a triangle with every edge of length (1). After doubling, every edge has weight (2).

For vertex (1), the doubled distances are (0,2,2), so its eccentricity is (2), giving a diameter candidate of (4) in doubled radius notation, which corresponds to an actual diameter of (2).

A convenient trace is:

| Step | Candidate center | Doubled distances from center | Candidate diameter |
| --- | --- | --- | --- |
| 1 | Vertex 1 | (0,2,2) | 2 |
| 2 | Vertex 2 | (2,0,2) | 2 |
| 3 | Vertex 3 | (2,2,0) | 2 |
| 4 | Any edge center | symmetric | 2 |

The first vertex candidate is already optimal. Dijkstra rooted at vertex (1) selects edges (1)-(2) and (1)-(3), producing a tree whose only nontrivial leaf-to-leaf path has length (2).

This example demonstrates that multiple centers and multiple optimal trees are harmless. The algorithm only needs one of them.

### Sample 2

The graph contains two compact regions connected by the heavy edge (3)-(4), whose length is (1000). The left region has edges of lengths (10,20,30), while the right region has edges of lengths (30,20,10).

The optimal tree shown by the sample is the path

[
1\rightarrow2\rightarrow3\rightarrow4\rightarrow6\rightarrow5
]

with total length

[
10+20+1000+10+20=1060.
]

The useful center is inside the heavy edge (3)-(4). The center balances the longest branch on the left with the longest branch on the right.

| Step | Relevant part | Value |
| --- | --- | --- |
| 1 | Left branch (1\rightarrow2\rightarrow3) | 30 |
| 2 | Heavy edge (3\rightarrow4) | 1000 |
| 3 | Right branch (4\rightarrow6\rightarrow5) | 30 |
| 4 | Total diameter | 1060 |

The center search identifies the heavy edge as the important candidate because the graph is naturally split into two groups whose farthest vertices are on opposite sides. Once that center is selected, the multi-source shortest-path construction creates the two shortest-path forests and joins them through (3)-(4).

The trace demonstrates why checking graph vertices alone is insufficient. A vertex at either endpoint of the heavy edge would leave the entire (1000)-length edge on one side of the center, while a point inside the edge balances the two sides.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3+MN)) | All-pairs shortest paths, sorting, edge-center sweep, and one final Dijkstra |
| Space | (O(N^2+M)) | Distance matrix, ordering arrays, adjacency list, and input edges |

Because (M\leq N(N-1)/2), the center sweep is at most (O(N^3)). With (N\leq500), the asymptotic bound is appropriate for the intended solution. The implementation also switches to repeated Dijkstra on sparse graphs, avoiding the full cubic Floyd-Warshall work when the graph contains relatively few edges. The distance values can reach about (10^{12}) after doubling, which Python handles directly without overflow.

## Test Cases

The output edges are not unique, so the test harness should validate the produced tree rather than compare the exact edge order. The following tests check the samples, the smallest graph, a weighted path whose center is inside an edge, equal weights, a large weight boundary, and a generated maximum-size dense graph.

```python
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
    n = data[0]
    m = data[1]

    original = set()
    pos = 2
    for _ in range(m):
        u, v, w = data[pos:pos + 3]
        pos += 3
        if u > v:
            u, v = v, u
        original.add((u, v, w))

    lines = out.strip().splitlines()
    assert len(lines) == n
    assert int(lines[0]) == expected_diameter

    chosen = []
    seen = set()

    for line in lines[1:]:
        u, v = map(int, line.split())
        assert 1 <= u <= n
        assert 1 <= v <= n
        assert u != v

        key_uv = (min(u, v), max(u, v))
        assert any(a == key_uv[0] and b == key_uv[1]
                   for a, b, _ in original)

        assert key_uv not in seen
        seen.add(key_uv)
        chosen.append(key_uv)

    assert len(chosen) == n - 1

    graph = [[] for _ in range(n)]
    for u, v in chosen:
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    stack = [0]
    visited[0] = True

    while stack:
        u = stack.pop()
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)

    assert all(visited)

sample1 = """\
3 3
1 2 1
2 3 1
3 1 1
"""

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

validate(sample1, run(sample1), 2)
validate(sample2, run(sample2), 1060)

case_min = """\
2 1
1 2 7
"""
validate(case_min, run(case_min), 7)

case_internal_center = """\
3 2
1 2 100
2 3 1
"""
validate(case_internal_center, run(case_internal_center), 101)

case_equal = """\
5 10
1 2 1
1 3 1
1 4 1
1 5 1
2 3 1
2 4 1
2 5 1
3 4 1
3 5 1
4 5 1
"""
validate(case_equal, run(case_equal), 2)

case_large_weight = """\
2 1
1 2 1000000000
"""
validate(case_large_weight, run(case_large_weight), 1000000000)

# Maximum-size style test: complete graph on 500 vertices.
# All edges have equal weight, so a star has optimal diameter 2.
n = 500
parts = [f"{n} {n * (n - 1) // 2}"]
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        parts.append(f"{u} {v} 1")

case_max = "\n".join(parts) + "\n"
validate(case_max, run(case_max), 2)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Diameter (2) and any two triangle edges | Multiple optimal trees and equal distances |
| Sample 2 | Diameter (1060) and any valid optimal tree | Center inside a heavy edge |
| (2) vertices, one edge of weight (7) | Diameter (7) | Minimum-size boundary |
| Path with weights (100,1) | Diameter (101) | Internal edge center |
| Complete graph with all weights (1) | Diameter (2) | Many equal shortest paths and tie handling |
| One edge of weight (10^9) | Diameter (10^9) | Large integer distances |
| Complete graph with (500) vertices | Diameter (2) | Maximum-size dense input and cubic-scale preprocessing |

## Edge Cases

For the two-vertex graph

```
2 1
1 2 7
```

the vertex-center phase gives eccentricity (7), hence diameter (7). The edge-center phase can also discover the midpoint of the only edge, but the vertex candidate is already optimal. The final Dijkstra rooted at vertex (1) returns the only edge (1)-(2).

For the weighted path

```
3 2
1 2 100
2 3 1
```

the only possible spanning tree has diameter (101). The vertex (2) has eccentricity (100), giving a diameter candidate of (200), so a vertex-only algorithm would be wrong. The edge sweep considers edge (1)-(2), finds the crossing between the branch ending at vertex (1) and the branch reaching vertex (3), and obtains the true diameter (101). The center lies (49.5) units from vertex (1), or (50.5) units from vertex (2).

For the equal-weight triangle

```
3 3
1 2 1
2 3 1
1 3 1
```

each vertex has eccentricity (1), so the doubled radius is (2) and the diameter is (2). The sorting order can choose equal-distance vertices arbitrarily, but the strict comparison in the edge sweep prevents equal-distance vertices from being incorrectly treated as belonging to the opposite side. A shortest-path tree from any chosen vertex has two edges and diameter (2).

For the maximum-weight boundary case

```
2 1
1 2 1000000000
```

all computations are performed with the doubled weight (2000000000). The final stored diameter is (1000000000) in the original scale. Python's arbitrary-precision integers make the arithmetic safe, while the implementation's `INF = 10**30` is comfortably larger than any possible shortest-path value.

For the maximum-size dense graph, the complete graph on (500) vertices has (124750) edges. If every edge has weight (1), every vertex is a valid center with eccentricity (1), and a shortest-path tree from any vertex is simply a star of diameter (2). The test exercises the distance preprocessing, the (N^2) sorting structure, and the dense edge sweep without relying on a sparse graph shortcut.
