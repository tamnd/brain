---
title: "CF 102391I - Minimum Diameter Spanning Tree"
description: "We have a connected undirected graph whose edges have positive lengths. We need to keep exactly enough edges to form a spanning tree, but the objective is not the total tree weight. Instead, we want the longest path inside the resulting tree to be as short as possible."
date: "2026-08-12T05:26:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "I"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 782
verified: false
draft: false
---

[CF 102391I - Minimum Diameter Spanning Tree](https://codeforces.com/problemset/problem/102391/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We have a connected undirected graph whose edges have positive lengths. We need to keep exactly enough edges to form a spanning tree, but the objective is not the total tree weight. Instead, we want the longest path inside the resulting tree to be as short as possible. The output is that minimum possible diameter together with any spanning tree achieving it. The official problem allows any valid optimal tree, so the particular edges printed by a correct implementation do not have to match the sample output.

The bound (N\le 500) is small enough to allow algorithms around cubic time, but (M) can be as large as (N(N-1)/2), so the graph can be dense. At the maximum size there can be about (125000) edges. Enumerating spanning trees is completely impossible, because a complete graph on (500) vertices has (500^{498}) different spanning trees by Cayley's formula. Even checking one tree costs at least linear time if we want its diameter. We instead need a polynomial algorithm that uses shortest-path information.

All edge lengths are positive and can reach (10^9). A path can contain (N-1) edges, so distances can reach roughly (5\cdot10^{11}). Python integers handle this range directly, but using a 32-bit integer type would overflow.

There are three edge cases that are particularly easy to mishandle.

First, the optimal center can lie inside an edge rather than at a vertex. Consider

```
4 3
1 2 1
2 3 1
3 4 1
```

The only spanning tree is the path (1-2-3-4), whose diameter is (3). If we only examine vertex centers, the best vertex has eccentricity (2), leading to the incorrect value (4). The true center is the midpoint of edge (2-3), with radius (1.5), so the correct diameter is (3).

Second, the edge containing the center does not have to be a shortest path between its endpoints. Consider

```
3 3
1 2 1
2 3 1
1 3 100
```

The expensive edge (1-3) is still an edge of the graph and must be considered as a possible location for the absolute center. Its endpoint distances must be computed using graph shortest paths, not by assuming the given edge itself is the shortest route between its endpoints. The optimal tree is the path (1-2-3), with diameter (2).

Third, equal shortest-path distances can occur frequently. In

```
3 3
1 2 1
2 3 1
1 3 1
```

both vertices (2) and (3) are tied at distance (1) from vertex (1). A Dijkstra implementation must allow arbitrary tie ordering. The final answer is still diameter (2), and the algorithm must not depend on one particular ordering of equal-distance vertices.

## Approaches

The brute-force approach is conceptually simple. Enumerate every subset of edges, keep the subsets containing exactly (N-1) edges, test whether each such subset is a tree, compute its diameter, and retain the smallest one. This is correct because every spanning tree appears in the enumeration. The problem is the number of candidates. In the complete graph (K_N), there are (N^{N-2}) spanning trees, so for (N=500) the enumeration already has (500^{498}) candidates. Computing a diameter for every candidate would make the total work on the order of (N\cdot N^{N-2}), far beyond any practical limit.

The useful observation is that a minimum-diameter tree has a very specific geometric center. Imagine replacing every graph edge by a continuous line segment of the same length. A point on this continuous network can be a vertex or an interior point of an edge. For such a point (x), define its radius as the maximum shortest-path distance from (x) to any graph vertex.

Take any spanning tree (T), and look at the midpoint of one of its diameter paths. That midpoint is either a tree vertex or lies inside a tree edge. Every vertex of the tree is at tree distance at most half the diameter from that midpoint. Graph shortest paths can only be shorter than tree paths, so the same point has graph distance at most half the tree diameter to every vertex. Consequently every spanning tree of diameter (D) gives a network point of radius at most (D/2).

The converse is the key. If (x) is a point of the original network whose maximum graph distance to a vertex is (R), build a shortest-path tree rooted at (x), treating an interior edge point as a subdividing vertex. Every root-to-vertex distance in that tree is at most (R), so every pair of vertices has tree distance at most (2R). Thus the optimum spanning-tree diameter is exactly twice the minimum possible radius of such a network point.

This converts the original tree optimization problem into the absolute 1-center problem on a weighted graph. This equivalence is the standard characterization of minimum-diameter spanning trees.

There are only two kinds of possible centers. A center can be an original vertex, in which case its radius is simply its eccentricity. Or it can lie somewhere inside an original edge. We can test all vertices directly, but testing an edge requires more care.

For an edge (u-v) of length (w), let (x) be a point at distance (\alpha) from (u), where (0\le\alpha\le w). For every vertex (z),

[
d(x,z)=\min(\alpha+d(u,z),,w-\alpha+d(v,z)).
]

The first expression describes paths reaching (z) through (u), while the second describes paths reaching it through (v). The radius of (x) is the maximum of these values over all (z).

Each vertex contributes an inverted-V shaped function of (\alpha). The upper envelope of all these functions is exactly the radius function along the edge. We need its lowest point. The Kariv-Hakimi sweep finds all relevant valleys of this upper envelope in linear time after the all-pairs distances and Dijkstra orders have been computed.

For a fixed edge (u-v), sort the vertices by increasing (d(u,z)). Start with the vertex farthest from (u). As we scan the remaining vertices backwards, a new vertex matters only when it is farther from (v) than the currently active vertex. Such a change creates a new crossing between the currently relevant function on the (u)-side and the new function on the (v)-side. If the two relevant vertices are (p) and (q), the crossing has radius

[
R=\frac{d(u,p)+w+d(v,q)}{2}.
]

Since the required answer is the diameter, it is convenient to store twice the radius:

[
D= d(u,p)+w+d(v,q).
]

This avoids every floating-point calculation.

The complete algorithm is consequently an all-pairs shortest-path computation, followed by vertex-center checks and one linear Kariv-Hakimi sweep for every graph edge. Finally, once the best center is known, one more Dijkstra computation constructs a shortest-path tree rooted at that center.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot N^{N-2})) | (O(N^2)) | Too slow |
| Optimal | (O(NM\log N + NM)) with heap Dijkstra | (O(N^2+M)) | Accepted |

For the stated (N\le500), this is the standard exact polynomial approach. The theoretical formulation of the absolute-center method is commonly given as (O(MN+N^2\log N)) once the shortest-path matrix is available, with the all-pairs shortest paths supplying the additional (N) single-source computations.

## Algorithm Walkthrough

1. Run Dijkstra from every vertex. Store both the shortest distances (d[s][v]) and the order in which vertices become permanently finalized by Dijkstra from (s).

The finalization order is sorted by nondecreasing distance from (s). It is exactly the ordering needed by the Kariv-Hakimi edge sweep.

1. For every vertex (c), compute

[
D_c=2\max_v d[c][v].
]

Keep the smallest value and remember (c) as the current best center.

If the optimal absolute center happens to be a graph vertex, this already finds it. The factor of two is deliberate because the final spanning-tree diameter is twice the center radius.

1. For every graph edge (u-v) with length (w), use the Dijkstra order from (u). Let that order be

[
r_0,r_1,\ldots,r_{N-1},
]

where (r_{N-1}) is farthest from (u).

Initialize (a=N-1). Then scan (b=N-2,N-3,\ldots,0). Whenever

[
d[v][r_b] > d[v][r_a],
]

the two currently relevant envelope lines form a new candidate valley.

The corresponding doubled radius is

[
D=d[u][r_b]+w+d[v][r_a].
]

If this value improves the current answer, remember this edge and the two vertices (r_b) and (r_a).

The reason for the strict comparison is that only a new, larger value on the (v)-side changes the upper envelope. Equal values cannot create a lower crossing that was not already represented by the active line.

1. After all vertices and edges have been examined, we know the minimum doubled radius (D^*).

If the best center is a vertex (c), we will build an ordinary shortest-path tree rooted at (c).

If the best center lies on edge (u-v), let (p=r_b) and (q=r_a) be the two vertices recorded when that edge candidate was found. The crossing position satisfies

[
\alpha+d[u][p]=w-\alpha+d[v][q].
]

Multiplying by two gives

[
2\alpha=w+d[v][q]-d[u][p].
]

We store this integer value instead of using floating point.

1. To construct the tree for a vertex center, run Dijkstra from that vertex and keep the predecessor of every vertex. Every non-root vertex contributes its predecessor edge.

A shortest-path tree is exactly what we want because every vertex is at graph distance at most the center radius from the root, so any two tree vertices are connected through the root by a path of length at most twice that radius.

1. To construct the tree for an edge center, conceptually subdivide (u-v) by inserting a new center (x). The distances from (x) to (u) and (v) are (\alpha) and (w-\alpha).

In the implementation, we avoid creating the new vertex. We initialize Dijkstra with doubled tentative distances

[
2\alpha
]

for (u), and

[
2w-2\alpha
]

for (v). Then ordinary graph edges have doubled length (2w_e).

The two initial vertices are allowed to be relaxed later. This detail matters because the chosen edge (u-v) need not be a shortest path between (u) and (v). If one endpoint can be reached more cheaply through the rest of the graph, Dijkstra must be allowed to discover that.

1. The predecessor graph produced by this multi-source Dijkstra is a forest rooted at the vertices reached directly from the artificial center. If both (u) and (v) remain roots, add the original edge (u-v). If only one remains a root, the original edge is not needed.

The resulting graph has exactly (N-1) edges and is a spanning tree. Its root-to-vertex distances equal the shortest distances from the selected center, so its diameter is at most (D^_). Since no spanning tree can have diameter below (D^_), its diameter is exactly optimal.

### Why it works

Let (R^_) be the minimum maximum distance from a point of the continuous graph to all original vertices. For every spanning tree (T) with diameter (D), the midpoint of a diameter path is at tree distance at most (D/2) from every vertex, and graph distances cannot exceed tree distances. Hence (R^_\le D/2), giving (D\ge2R^*).

Conversely, take an absolute center (x) with radius (R^_). A shortest-path tree rooted at (x) gives every vertex a tree distance at most (R^_) from (x). The tree distance between any two vertices is at most the sum of their distances to (x), so its diameter is at most (2R^_). The two inequalities meet, proving that the optimal spanning-tree diameter is (2R^_).

The absolute center lies either at a vertex or inside an edge. Vertex centers are checked directly. On each edge, the radius is the upper envelope of the vertex distance functions, and the Kariv-Hakimi sweep examines exactly the points where this envelope can attain a local minimum. Thus the smallest candidate found by the sweep is (R^_). The final shortest-path tree then achieves diameter (2R^_), so the printed tree is optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def dijkstra(source, graph, n):
    dist = [INF] * n
    parent = [-1] * n
    order = []

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue

        order.append(u)

        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, parent, order

def dijkstra_center(graph, n, u, v, alpha2, w):
    """
    Dijkstra from an artificial center x lying on edge u-v.

    All distances are doubled, so alpha2 = 2 * distance(x, u).
    The initial distances are:
        dist2[u] = alpha2
        dist2[v] = 2*w - alpha2

    Unlike ordinary multi-source Dijkstra, u and v are allowed to
    be relaxed later. This is necessary because u-v itself need not
    be a shortest path between u and v.
    """
    dist = [INF] * n
    parent = [-1] * n

    dv = 2 * w - alpha2
    dist[u] = alpha2
    dist[v] = dv

    pq = [(alpha2, u)]
    if v != u:
        heapq.heappush(pq, (dv, v))

    used = [False] * n

    while pq:
        d, x = heapq.heappop(pq)
        if used[x] or d != dist[x]:
            continue

        used[x] = True

        for y, ew in graph[x]:
            nd = d + 2 * ew
            if nd < dist[y]:
                dist[y] = nd
                parent[y] = x
                heapq.heappush(pq, (nd, y))

    tree = []

    for x in range(n):
        if parent[x] != -1:
            tree.append((x, parent[x]))

    # If both endpoints are roots of the shortest-path forest,
    # the artificial center connects to both, which corresponds
    # to using the original edge u-v.
    if parent[u] == -1 and parent[v] == -1 and u != v:
        tree.append((u, v))

    return tree

def dijkstra_tree(graph, n, source):
    dist = [INF] * n
    parent = [-1] * n

    dist[source] = 0
    pq = [(0, source)]

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

    return [(v, parent[v]) for v in range(n) if parent[v] != -1]

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    edges = []

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, w))
        graph[v].append((u, w))
        edges.append((u, v, w))

    # All-pairs shortest paths and Dijkstra finalization orders.
    dist = [[0] * n for _ in range(n)]
    orders = [None] * n

    for s in range(n):
        ds, _, order = dijkstra(s, graph, n)
        dist[s] = ds
        orders[s] = order

    # Best center found so far.
    best2 = INF
    best_type = 0          # 0 = vertex, 1 = edge
    best_vertex = -1

    for s in range(n):
        cur = 2 * max(dist[s])
        if cur < best2:
            best2 = cur
            best_type = 0
            best_vertex = s

    best_edge = None

    # Kariv-Hakimi sweep on every edge.
    for u, v, w in edges:
        r = orders[u]

        a = n - 1

        for b in range(n - 2, -1, -1):
            x = r[b]
            y = r[a]

            if dist[v][x] > dist[v][y]:
                candidate2 = dist[u][x] + w + dist[v][y]

                if candidate2 < best2:
                    best2 = candidate2
                    best_type = 1
                    best_edge = (u, v, w, x, y)

                a = b

    # Construct an optimal shortest-path tree.
    if best_type == 0:
        tree = dijkstra_tree(graph, n, best_vertex)
    else:
        u, v, w, p, q = best_edge

        # 2 * alpha = w + d(v,q) - d(u,p)
        alpha2 = w + dist[v][q] - dist[u][p]

        tree = dijkstra_center(graph, n, u, v, alpha2, w)

    out = [str(best2)]

    for u, v in tree:
        out.append(f"{u + 1} {v + 1}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first Dijkstra loop computes two pieces of information simultaneously. The distance array gives the all-pairs shortest-path matrix, while the order array records vertices in nondecreasing distance from the source. Since every edge weight is positive, the order in which Dijkstra permanently extracts vertices is a valid distance order.

The vertex-center loop uses (2\cdot\max d[c][v]) because the actual answer is a diameter rather than a radius. Keeping everything doubled also makes the later edge-center arithmetic integral.

The edge loop is the compact part of the Kariv-Hakimi algorithm. For an edge (u-v), `r` is sorted by distance from (u). The variable `a` identifies the currently active farthest line on the opposite side, while `b` scans possible lines that can replace it. When `dist[v][r[b]]` becomes strictly larger than `dist[v][r[a]]`, the two lines form a new relevant intersection, whose doubled height is exactly

```
dist[u][r[b]] + w + dist[v][r[a]]
```

The reconstruction code uses doubled distances. If the center is at distance (\alpha) from (u), the two initial distances from the artificial center are (\alpha) and (w-\alpha). Multiplying all distances by two gives integer initial values, so no floating-point comparison is necessary.

The reconstruction Dijkstra intentionally does not permanently mark (u) and (v) as immutable sources. An expensive edge may have a shorter alternative route elsewhere in the graph, so one of those endpoints may cease to be a direct child of the artificial center. The predecessor graph remains a forest because every predecessor is assigned only through a strict distance improvement. If both endpoints remain roots, the artificial center used both halves of the selected edge, so those two roots are joined by the original edge.

Python's arbitrary-precision integers remove overflow concerns. The largest relevant distance is below (5\cdot10^{11}), while doubled distances stay comfortably below (10^{12}).

## Worked Examples

### Sample 1

The graph is a triangle with all three edges of length (1). Every vertex has eccentricity (1), so a vertex center already gives doubled radius (2).

| Center candidate | Radius | Doubled radius |
| --- | --- | --- |
| Vertex 1 | 1 | 2 |
| Vertex 2 | 1 | 2 |
| Vertex 3 | 1 | 2 |

The edge sweep cannot improve this value. The algorithm may select vertex (1), then Dijkstra produces a shortest-path tree such as (1-2) and (1-3).

The resulting tree has diameter (2), which matches the optimum shown by the sample.

### Sample 2

The graph has a left cluster connected through the long edge (3-4) of length (1000) to the right cluster.

The important candidate is the interior of edge (3-4). The left side reaches vertex (1) through distances (30) from (3), while the right side reaches vertex (6) through distance (30) from (4).

The relevant crossing therefore has doubled radius

[
30+1000+30=1060.
]

| Candidate | Left contribution | Edge | Right contribution | Diameter |
| --- | --- | --- | --- | --- |
| Center on edge (3-4) | 30 | 1000 | 30 | 1060 |

The center is the midpoint of the (3-4) edge. The shortest-path tree attaches the left vertices through (3) and the right vertices through (4), giving a tree whose diameter is (1060).

The sample output uses exactly this central edge and reports diameter (1060).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(NM\log N + NM)) | (N) Dijkstra runs plus one (O(N)) scan for every edge |
| Space | (O(N^2+M)) | All-pairs distances, Dijkstra orders, and the adjacency list |

With (N\le500), the distance matrix needs only (250000) entries. The graph can contain about (125000) edges, so the adjacency list is also manageable under the (1024) MB memory limit. The edge sweep itself performs at most (N) simple operations per edge, which is about (6.25\cdot10^7) iterations at the maximum density. The shortest-path phase dominates the running time.

The standard exact absolute-center formulation is polynomial and is based on all-pairs shortest paths followed by processing every edge.

## Test Cases

The output tree is not unique, so the test harness should not compare the entire output string with one fixed answer. Instead, it checks the reported diameter, verifies that every printed edge belongs to the input graph, verifies that there are exactly (N-1) edges, and checks that those edges form a tree whose actual weighted diameter equals the expected optimum.

```python
import sys
import io
from collections import deque
import heapq

# Put the submitted solution in the same file above this harness.
# The function solve() must be the solution entry point.

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

    edge_weight = {}
    graph = [[] for _ in range(n)]

    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        w = next(it)

        edge_weight[frozenset((u, v))] = w
        graph[u].append((v, w))
        graph[v].append((u, w))

    lines = out.strip().splitlines()
    assert len(lines) == n

    diameter = int(lines[0])
    assert diameter == expected_diameter

    tree = []
    for line in lines[1:]:
        u, v = map(int, line.split())
        u -= 1
        v -= 1

        assert 0 <= u < n
        assert 0 <= v < n
        assert u != v

        key = frozenset((u, v))
        assert key in edge_weight

        tree.append((u, v, edge_weight[key]))

    assert len(tree) == n - 1

    # Check that the output is a tree.
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v, _ in tree:
        ru = find(u)
        rv = find(v)
        assert ru != rv
        parent[ru] = rv

    root = find(0)
    for v in range(n):
        assert find(v) == root

    # Compute the actual diameter of the printed tree.
    tg = [[] for _ in range(n)]
    for u, v, w in tree:
        tg[u].append((v, w))
        tg[v].append((u, w))

    actual = 0

    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])

        while q:
            u = q.popleft()
            for v, w in tg[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + w
                    q.append(v)

        actual = max(actual, max(dist))

    assert actual == expected_diameter

# Sample 1
sample1 = """\
3 3
1 2 1
2 3 1
3 1 1
"""
validate(sample1, run(sample1), 2)

# Sample 2
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

# Four-vertex path. The optimum center is inside an edge,
# so a vertex-only solution would incorrectly report 4.
case_edge_center = """\
4 3
1 2 1
2 3 1
3 4 1
"""
validate(case_edge_center, run(case_edge_center), 3)

# All edge weights equal. The triangle has a vertex center,
# and every spanning tree has diameter 10.
case_equal = """\
3 3
1 2 5
2 3 5
1 3 5
"""
validate(case_equal, run(case_equal), 10)

# Maximum-size dense input, all weights equal.
# A star has diameter 2 and is optimal.
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
| Sample 1 | Diameter (2) | Vertex center and equal-distance ties |
| Sample 2 | Diameter (1060) | Interior edge center on a long weighted edge |
| (2) vertices, one edge of weight (7) | Diameter (7) | Minimum-size boundary |
| Path (1-2-3-4), unit weights | Diameter (3) | Catches solutions that only test vertex centers |
| Equal-weight triangle with weight (5) | Diameter (10) | Equal distances and vertex-center handling |
| Complete graph on (500) vertices, all weights (1) | Diameter (2) | Maximum (N), maximum (M), dense graph, equal weights |

## Edge Cases

The minimum-size case has only two vertices:

```
2 1
1 2 7
```

There is exactly one spanning tree, consisting of the only edge, so the answer must be (7). The vertex-center phase gives eccentricity (7) for either endpoint and doubled radius (14), but the actual tree diameter is (7), which exposes an issue with treating (2R) blindly for (N=2). The absolute-center radius is actually (3.5), attained at the midpoint of the edge, so the edge sweep finds the candidate (7). This is why testing interior edge centers is necessary even for the smallest graph.

For the four-vertex path

```
4 3
1 2 1
2 3 1
3 4 1
```

the vertex eccentricities are (3,2,2,3). The best vertex candidate has doubled radius (4). On edge (2-3), the relevant farthest vertices are (1) and (4), giving

[
1+1+1=3.
]

The edge sweep records diameter (3), and reconstruction places the artificial center at the midpoint of (2-3). The resulting tree is necessarily the original path, whose diameter is (3).

For a graph containing an edge that is not a shortest route between its endpoints,

```
3 3
1 2 1
2 3 1
1 3 100
```

the shortest-path matrix gives (d(1,3)=2), despite the direct edge having weight (100). The center computation uses these shortest-path distances everywhere. The expensive edge is still examined as a possible center location, but it cannot beat the center at vertex (2). The final diameter is (2), with tree edges (1-2) and (2-3).

For equal distances,

```
3 3
1 2 1
2 3 1
1 3 1
```

Dijkstra may finalize vertices in different orders depending on heap tie behavior. The edge sweep uses only the resulting nondecreasing distance order and strict improvements on the opposite side. Equal values do not require a particular tie-breaking rule. The vertex-center candidates already give doubled radius (2), so the algorithm returns diameter (2).

For the maximum dense case, the graph can contain all (124750) possible edges when (N=500). If every edge has weight (1), choosing any vertex as a center gives radius (1), so the optimum diameter is (2). The algorithm still processes all edges during the Kariv-Hakimi sweep, but every candidate is no better than the vertex-center value. This case exercises both the (M=\Theta(N^2)) input boundary and the equal-distance behavior of the shortest-path ordering.

One correction to keep in mind when implementing this editorial: the test harness deliberately validates the _properties_ of the output rather than comparing edge lists, because Codeforces accepts any minimum-diameter spanning tree.
