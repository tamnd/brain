---
title: "CF 102391I - Minimum Diameter Spanning Tree"
description: "We have a connected undirected graph with positive edge lengths. We must select exactly (N-1) of its edges so that they form a spanning tree, and among all possible spanning trees we want one whose longest tree path is as short as possible."
date: "2026-08-11T23:12:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "I"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 541
verified: false
draft: false
---

[CF 102391I - Minimum Diameter Spanning Tree](https://codeforces.com/problemset/problem/102391/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We have a connected undirected graph with positive edge lengths. We must select exactly (N-1) of its edges so that they form a spanning tree, and among all possible spanning trees we want one whose longest tree path is as short as possible. The output must contain that minimum possible diameter and the edges of one optimal tree.

The difficulty is that the objective is not the total weight of the tree. A light spanning tree can still have a very long branch, while a heavier tree can have a much smaller diameter. A minimum spanning tree algorithm such as Kruskal or Prim is consequently solving a different problem.

The graph has at most (500) vertices, while (M) can be almost (N^2/2). That rules out anything exponential in (N), such as enumerating spanning trees. At the maximum size, a complete graph has (500\cdot499/2=124750) edges, so an algorithm with one substantial (O(MN)) pass is already around (6.2\cdot10^7) edge-vertex operations. An (O(N^3)) algorithm is also around (1.25\cdot10^8) elementary distance updates, which is consistent with the intended polynomial solution for (N=500). The edge weights can reach (10^9), and a shortest path can contain (N-1) edges, so 64-bit arithmetic is necessary. Python integers handle this automatically.

There are several edge cases where a seemingly natural solution fails.

Consider the graph consisting of only two vertices.

```
2 1
1 2 10
```

The only spanning tree has diameter (10). A solution that only considers an existing vertex as the center might compute twice the best vertex eccentricity and obtain (20). The real center is the midpoint of the edge, and its radius is (5), giving diameter (10).

The same issue appears without an obvious midpoint. Consider

```
4 3
1 2 1
2 3 1
3 4 1
```

The graph itself is already a tree, so the answer is (3). The center is the midpoint of edge (2-3). If we only try vertex centers, the best eccentricity is (2), which would suggest (4), even though the actual tree has diameter (3).

The optimal position inside an edge also need not be its midpoint. For

```
3 2
1 2 2
2 3 100
```

the only spanning tree has diameter (102). Its center lies (49) units from vertex (2) along the edge (2-3), not at the midpoint of that edge. Restricting every candidate edge center to its midpoint gives the wrong radius.

Finally, equal shortest paths can cause another implementation bug. In

```
3 3
1 2 1
2 3 1
1 3 1
```

every vertex has two shortest neighbors. If we add every edge satisfying a shortest-distance equality without maintaining a visited set, we can output all three edges and create a cycle. The desired tree has only two edges and diameter (2).

The solution must consequently handle centers at vertices, centers strictly inside edges, arbitrary fractional positions inside an edge, and ties between several shortest paths.

## Approaches

The most direct brute force is to enumerate every spanning tree, compute its diameter, and keep the best one. This is correct because every feasible answer is represented by one of those trees. Unfortunately, the complete graph (K_N) already has (N^{N-2}) spanning trees by Cayley's formula. At (N=500), that is (500^{498}) candidates. Even spending only (O(N)) operations on each candidate would require on the order of (500^{499}) basic operations, which is completely infeasible.

A more sophisticated brute force might try every vertex as the center and construct a shortest-path tree from it. That is already much better, but it still misses centers located inside edges. One could also try every edge and repeatedly run a shortest-path algorithm while moving the hypothetical center along that edge. With (M) candidate edges, this introduces another shortest-path computation for each edge and becomes far too expensive.

The key observation is to stop thinking about the tree first. Consider the original graph as a continuous network where every edge is an interval. A point (c) can be either an original vertex or a point inside an edge. Define its eccentricity as the largest shortest-path distance from (c) to any graph vertex. Such a point is called an absolute 1-center.

The crucial theorem is that a shortest-path tree rooted at an absolute 1-center is a minimum-diameter spanning tree. Conversely, the center of a minimum-diameter spanning tree gives an absolute 1-center of the original graph. Thus the tree problem becomes a network-center problem. This equivalence is the central result used by the classical Hassin-Tamir approach.

Suppose the center lies at distance (x) from endpoint (u) of an edge (uv) of length (w). For another vertex (z), its distance from the center is

[
f_z(x)=\min(d(u,z)+x,\ d(v,z)+w-x).
]

The first expression reaches (z) through (u), while the second reaches it through (v). The eccentricity of the point is the maximum of these functions over all (z).

For a fixed edge, every (f_z) is a two-piece linear function. The maximum of these functions can only attain its minimum at an endpoint or at an intersection of two active pieces. After sorting vertices by their distance from one endpoint, those relevant intersections can be scanned in linear time for that edge. This is the Kariv-Hakimi style absolute-center computation. The resulting algorithm takes (O(MN+N^2\log N)) time once the all-pairs distance matrix is available.

Because (N\le500), we can obtain all-pairs shortest-path distances with Floyd-Warshall in (O(N^3)). We then scan every edge in (O(N)), find the optimal center, and finally construct the shortest-path tree around that center.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all spanning trees | (\Omega(N^{N-1})) basic work | Exponential | Too slow |
| Try every center with repeated shortest paths | At least (O(M^2\log N)) style work | (O(M+N)) | Too slow |
| Absolute 1-center + APSP | (O(N^3+MN+N^2\log N)) | (O(N^2+M)) | Accepted |

## Algorithm Walkthrough

1. Build a matrix containing the original edge weights and initialize every diagonal entry to zero. All non-edges receive infinity. We also keep the original edge list because the final spanning tree is allowed to use only edges that actually occur in the input.
2. Compute all-pairs shortest-path distances with Floyd-Warshall. After this step, (d[u][v]) is the shortest distance between every pair of graph vertices, not merely the weight of a direct edge.
3. For every vertex (u), sort all vertices by decreasing (d[u][v]). Call this ordering (L_u). The first element is a farthest vertex from (u). These orderings let us scan the relevant edge-center constraints without sorting again for every edge.
4. Consider a vertex (u) as the center. Its eccentricity is

[
e(u)=\max_v d[u][v].
]

A shortest-path tree rooted at (u) has diameter at most (2e(u)), and an absolute center gives the exact optimum. Thus (2e(u)) is a candidate answer.

1. Now consider an original edge (uv) with weight (w), and imagine placing the center at distance (x) from (u). For every vertex (z), its distance from the center is

[
\min(d[u][z]+x,\ d[v][z]+w-x).
]

The first term increases with (x), while the second decreases with (x). The farthest vertex on the two sides determines the current upper envelope.

1. Process the vertices in (L_u) from the closest to (u) toward the farthest. Maintain `cmp`, the vertex seen so far having the largest distance from (v). Whenever a newly processed vertex has a larger distance from (v), it becomes a new active constraint. The new constraint from the (u)-side and the previous active constraint from the (v)-side intersect at

[
x=\frac{d[v][z_{\text{old}}]-d[u][z_{\text{new}}]+w}{2}.
]

At this intersection the two relevant distances are equal, so the candidate diameter is

[
d[u][z_{\text{new}}]+d[v][z_{\text{old}}]+w.
]

The scan checks every possible active intersection in linear time.

1. Repeat the edge scan for every original edge. Whenever a smaller candidate is found, store the edge endpoints and the doubled center coordinate. The doubled coordinate is useful because the true center can lie at a half-integer position even though every graph edge has an integer weight.
2. Once the optimal center is known, define (R_2[v]) as twice the shortest distance from the center to vertex (v). If the center is a vertex (s), then

[
R_2[v]=2d[s][v].
]

If the center is (x) units from (s) on an edge (st) of length (w), store (h_2=2x), giving

\min(2d[s][v]+h_2,\ 2d[t][v]+2w-h_2).
]

1. Construct the shortest-path tree by following original edges that satisfy

[
R_2[v]=R_2[u]+2w(u,v).
]

Because every edge has positive weight, the value (R_2) strictly increases whenever we move away from the center. A visited array is enough to choose one parent for every vertex and avoid cycles.

1. If the center is inside an edge, start the reconstruction from both endpoints of that edge and finally add the central edge itself. If the center is an original vertex, only that vertex is a root and no special central edge is needed.

### Why it works

Let (c) be an absolute 1-center and let (r) be its maximum shortest-path distance to any graph vertex. A shortest-path tree rooted at (c) gives every vertex a tree path from (c) of length exactly its graph distance from (c). For any two vertices (a,b), their tree path can be split at their lowest common point relative to (c), so its length is at most (d(c,a)+d(c,b)\le2r). Thus the constructed tree has diameter at most (2r).

Now take any spanning tree (T). Its diameter has a midpoint, which is either a vertex or a point inside one of its edges. The distance from that midpoint to every vertex is at most half the tree diameter. Since graph shortest paths can never be longer than paths inside (T), that midpoint is also a feasible center in the original graph. Hence every spanning tree of diameter (D) gives an absolute-center radius at most (D/2). The absolute center has radius no larger than this, so its shortest-path tree has diameter at most (D). Applying this to an optimal tree proves that the tree constructed from the absolute center is optimal. This is precisely the MDST and absolute 1-center equivalence.

The edge scan is correct because, on a fixed edge, each vertex contributes a function formed by the minimum of one increasing and one decreasing linear expression. At an optimum, either an endpoint of the edge is optimal or two currently active constraints meet. Sorting by distance from one endpoint lets us identify every change in the active constraint with one linear scan.

## Python Solution

```python
import sys

input = sys.stdin.readline

INF = 10**30

def tree_diameter(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    def farthest(start):
        stack = [(start, -1, 0)]
        best_v = start
        best_d = 0

        while stack:
            u, parent, dist = stack.pop()
            if dist > best_d:
                best_d = dist
                best_v = u

            for v, w in adj[u]:
                if v == parent:
                    continue
                stack.append((v, u, dist + w))

        return best_v, best_d

    a, _ = farthest(0)
    _, diameter = farthest(a)
    return diameter

def solve(data):
    it = iter(map(int, data.split()))
    n = next(it)
    m = next(it)

    edges = []
    dist = [[INF] * n for _ in range(n)]
    direct = [[INF] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0
        direct[i][i] = 0

    all_equal = True
    first_weight = None

    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        w = next(it)

        edges.append((u, v, w))
        direct[u][v] = w
        direct[v][u] = w
        dist[u][v] = w
        dist[v][u] = w

        if first_weight is None:
            first_weight = w
        elif first_weight != w:
            all_equal = False

    # If the input graph is already a tree, it is the only spanning tree.
    if m == n - 1:
        diameter = tree_diameter(n, edges)
        out = [str(diameter)]
        for u, v, _ in edges:
            out.append(f"{u + 1} {v + 1}")
        return "\n".join(out)

    # Complete graph with equal edge weights: any star is optimal.
    if m == n * (n - 1) // 2 and all_equal:
        w = first_weight
        diameter = w if n == 2 else 2 * w
        out = [str(diameter)]
        for v in range(1, n):
            out.append(f"1 {v + 1}")
        return "\n".join(out)

    # Floyd-Warshall.
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik >= INF:
                continue

            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    # Farthest-first ordering for every source.
    order = []
    for u in range(n):
        row = dist[u]
        order.append(sorted(range(n), key=row.__getitem__, reverse=True))

    # First consider centers that are original vertices.
    best = INF
    best_s = 0
    best_t = 0
    best_h2 = 0

    for u in range(n):
        candidate = 2 * dist[u][order[u][0]]
        if candidate < best:
            best = candidate
            best_s = u
            best_t = u
            best_h2 = 0

    # Consider centers inside every graph edge.
    for u, v, w in edges:
        # We run the scan in both orientations. This is harmless
        # asymptotically and avoids depending on which endpoint was chosen.
        for s, t in ((u, v), (v, u)):
            seq = order[s]

            # seq is farthest-first from s.
            # We scan from the closest vertex toward the farthest.
            cmp = n - 1

            for i in range(n - 2, -1, -1):
                a = seq[i]
                b = seq[cmp]

                if dist[t][a] > dist[t][b]:
                    candidate = dist[s][a] + dist[t][b] + w

                    if candidate < best:
                        best = candidate

                        # candidate =
                        # d(s,a) + d(t,b) + w
                        #
                        # If h is the center's distance from s,
                        # d(s,a) + h = d(t,b) + w - h.
                        # Store 2*h to avoid floating point.
                        best_h2 = candidate - 2 * dist[s][a]
                        best_s = s
                        best_t = t

                    cmp = i

    # Twice the center-to-vertex distances.
    radius2 = [0] * n

    if best_s == best_t:
        s = best_s
        for v in range(n):
            radius2[v] = 2 * dist[s][v]
    else:
        s = best_s
        t = best_t
        w = direct[s][t]
        h2 = best_h2

        for v in range(n):
            radius2[v] = min(
                2 * dist[s][v] + h2,
                2 * dist[t][v] + 2 * w - h2
            )

    # Build the shortest-path tree from the center.
    visited = [False] * n
    tree_edges = []

    roots = [best_s]
    if best_t != best_s:
        roots.append(best_t)

    for root in roots:
        if visited[root]:
            continue

        visited[root] = True
        stack = [root]

        while stack:
            u = stack.pop()

            for v in range(n):
                w = direct[u][v]
                if w >= INF or visited[v]:
                    continue

                if radius2[v] == radius2[u] + 2 * w:
                    visited[v] = True
                    tree_edges.append((u, v))
                    stack.append(v)

    # If the center is inside an edge, that edge belongs to the tree.
    if best_s != best_t:
        tree_edges.append((best_s, best_t))

    out = [str(best)]
    for u, v in tree_edges:
        out.append(f"{u + 1} {v + 1}")

    return "\n".join(out)

def main():
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The first special case handles (M=N-1). There is only one spanning tree, so doing the absolute-center computation would be unnecessary. Two tree traversals find its diameter directly.

The second special case handles a complete graph whose edge weights are all equal. A star has diameter (2w) for (N>2), and no spanning tree can have diameter smaller than (2w), because every nontrivial tree has two vertices at distance at least two edges. This also gives a useful maximum-size stress test without forcing the cubic implementation to process a completely symmetric instance.

The general branch first builds `dist`, then runs Floyd-Warshall. The matrix stores shortest graph distances, while `direct` retains only actual input edges. Keeping these two matrices separate is essential. A shortest path between two vertices may use many edges, but the final tree can only contain original edges.

The `order` matrix contains vertices in decreasing distance from each source. The edge-center scan reverses this order conceptually, starting from the closest vertex. `cmp` records the previously encountered vertex that has the largest distance from the opposite endpoint. Every time that value increases, a new pair of active linear constraints is found.

The expression

```
candidate = dist[s][a] + dist[t][b] + w
```

is the diameter corresponding to the intersection of those two constraints. The center coordinate is not necessarily integral, so the code stores `best_h2`, twice the distance from the first endpoint to the center. All calculations consequently remain exact integers.

The reconstruction uses `radius2`, twice the distance from the center. An original edge (uv) belongs to a shortest-path tree whenever moving from (u) to (v) increases this value by exactly twice the edge length. Because all edge weights are positive, these values strictly increase along a chosen parent edge. The visited array then selects one shortest-path parent for each vertex.

When the center lies inside an edge, both endpoints are treated as roots. The central edge is added separately. This is necessary because neither endpoint has zero distance from the center, and initializing both with their actual center distances is what preserves the geometry of the edge-centered shortest-path tree.

Python integers avoid overflow automatically. The largest possible shortest-path value is below (500\cdot10^9), so the values are comfortably representable in a normal 64-bit integer as well.

## Worked Examples

### Sample 1

The graph is a complete graph on three vertices, and every edge has weight (1). The implementation recognizes this symmetric case and constructs the star centered at vertex (1).

| Stage | Key state | Result |
| --- | --- | --- |
| Input | (N=3,M=3) | Complete graph |
| Edge weights | (1,1,1) | All equal |
| Special-case check | Complete and equal | True |
| Chosen center | Vertex (1) | Star |
| Added edges | (1-2,1-3) | Two tree edges |
| Diameter | (1+1) | (2) |

The output can consequently be

```
2
1 2
1 3
```

which differs from the sample output only in the choice of the second edge. Both are valid minimum-diameter spanning trees.

This example demonstrates that several optimal trees can exist. The program must not rely on matching the sample's particular edge ordering.

### Sample 2

The graph consists of a left part around vertices (1,2,3), a right part around (4,5,6), and the expensive bridge (3-4) of length (1000).

| Stage | Key state | Result |
| --- | --- | --- |
| Input | (N=6,M=7) | General weighted graph |
| Tree shortcut | (M\ne N-1) | Continue |
| Complete-equal shortcut | False | Continue |
| APSP | Floyd-Warshall | All (d[u][v]) known |
| Best vertex center | Greater than (1060) | Not optimal |
| Candidate edge | (3-4), weight (1000) | Strong candidate |
| Center position | Near the middle of (3-4) | Edge center |
| Left contribution | Through (3) | Controlled by left side |
| Right contribution | Through (4) | Controlled by right side |
| Best diameter | (1060) | Stored as `best` |
| Reconstruction | Shortest paths from both endpoints | Five edges |
| Output diameter | (1060) | Optimal |

The resulting tree can be the same as the sample:

```
1060
3 4
4 6
6 5
2 3
1 2
```

The long edge (3-4) dominates the geometry. The algorithm does not simply choose its midpoint. Instead, it compares the farthest constraints on both sides and chooses the exact balancing position. The branches (1-2-3) and (4-6-5) contribute different amounts, so the optimal point is determined by those distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3+MN+N^2\log N)) | Floyd-Warshall is (O(N^3)), sorting all distance rows is (O(N^2\log N)), and every edge receives an (O(N)) center scan |
| Space | (O(N^2+M)) | Two (N\times N) matrices, the ordering matrix, and the original edge list |

Since (M\le N(N-1)/2), the (MN) term is at most (O(N^3)). The overall worst-case bound is thus (O(N^3)), with (N\le500). The intended absolute-center formulation is polynomial and is known to achieve (O(MN+N^2\log N)) after shortest-path distances are available.

The memory bound is dominated by the distance and direct-edge matrices. For (N=500), each contains only (250000) entries, which is well within the (1024) MB memory limit.

## Test Cases

The output tree is not unique, so exact string comparison is inappropriate for this problem. The following test harness checks the properties that actually matter: the reported diameter, that exactly (N-1) valid input edges are printed, that those edges form a tree, and that their weighted diameter equals the reported optimum.

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    return solve(inp)

def validate(inp: str, expected_diameter: int):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)

    graph_edges = set()
    weights = {}

    for _ in range(m):
        u = next(it)
        v = next(it)
        w = next(it)

        if u > v:
            u, v = v, u

        graph_edges.add((u, v))
        weights[(u, v)] = w

    out = list(map(int, run(inp).split()))
    assert out[0] == expected_diameter

    tree_edges = []
    pos = 1

    for _ in range(n - 1):
        u = out[pos]
        v = out[pos + 1]
        pos += 2

        if u > v:
            u, v = v, u

        assert (u, v) in graph_edges
        tree_edges.append((u, v))

    assert len(set(tree_edges)) == n - 1

    adj = [[] for _ in range(n + 1)]
    for u, v in tree_edges:
        w = weights[(u, v)]
        adj[u].append((v, w))
        adj[v].append((u, w))

    seen = [False] * (n + 1)
    stack = [1]
    seen[1] = True

    while stack:
        u = stack.pop()
        for v, _ in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)

    assert all(seen[1:])

    def farthest(start):
        stack = [(start, 0, -1)]
        best_v = start
        best_d = 0

        while stack:
            u, d, parent = stack.pop()

            if d > best_d:
                best_d = d
                best_v = u

            for v, w in adj[u]:
                if v == parent:
                    continue
                stack.append((v, d + w, u))

        return best_v, best_d

    a, _ = farthest(1)
    _, diameter = farthest(a)

    assert diameter == expected_diameter

# Sample 1
sample1 = """\
3 3
1 2 1
2 3 1
3 1 1
"""
validate(sample1, 2)

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
validate(sample2, 1060)

# Minimum-size graph.
case_min = """\
2 1
1 2 1000000000
"""
validate(case_min, 1000000000)

# All-equal complete graph.
case_equal = """\
4 6
1 2 7
1 3 7
1 4 7
2 3 7
2 4 7
3 4 7
"""
validate(case_equal, 14)

# Non-midpoint edge center.
case_boundary = """\
3 2
1 2 2
2 3 100
"""
validate(case_boundary, 102)

# Maximum-size test, but already a tree, so the tree shortcut applies.
n = 500
lines = [f"{n} {n - 1}"]
for i in range(1, n):
    lines.append(f"{i} {i + 1} 1")
case_max = "\n".join(lines) + "\n"

validate(case_max, n - 1)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Diameter (2) | Multiple optimal trees and equal edge weights |
| Sample 2 | Diameter (1060) | General weighted edge-center computation |
| (2) vertices, edge (10^9) | (10^9) | Minimum-size input and center inside an edge |
| Complete (K_4), all weights (7) | (14) | Equal-weight graph and star construction |
| Path with weights (2,100) | (102) | Center is not the midpoint of the chosen edge |
| Path with (500) vertices | (499) | Maximum (N), large input size, tree shortcut |

## Edge Cases

The two-vertex graph

```
2 1
1 2 10
```

hits the first special case because (M=N-1). There is exactly one possible spanning tree, so the algorithm simply returns that edge and computes its diameter as (10). This avoids the common mistake of treating a vertex as the only possible center.

For the four-vertex path

```
4 3
1 2 1
2 3 1
3 4 1
```

the graph is again already a tree, so the answer is forced. The two tree traversals find vertices (1) and (4) as diameter endpoints, giving distance (3). The output contains all three original edges. A vertex-center-only algorithm would incorrectly reason from eccentricity (2) and lose the factor introduced by the center being inside edge (2-3).

For the asymmetric path

```
3 2
1 2 2
2 3 100
```

the only spanning tree has diameter (102). The center is (51) units from vertex (1), which places it (49) units into edge (2-3). The algorithm represents this position by `h2 = 98`, avoiding floating point. The resulting shortest-path tree is the original tree, and its diameter is exactly (102).

For the triangle

```
3 3
1 2 1
2 3 1
1 3 1
```

the equal-weight complete-graph shortcut constructs a star. Its two edges have total path length (2), which is optimal. The construction deliberately outputs only (N-1=2) edges, so ties between several shortest paths cannot accidentally create a cycle.

The large-weight boundary is also safe. A path with (499) edges of weight (10^9) would have a diameter near (5\cdot10^{11}), far beyond 32-bit signed integers. Python's arbitrary-precision integers handle the calculation directly, while the algorithm never relies on floating-point comparisons.

Finally, when an edge-centered solution has two equally good shortest paths to a vertex, either parent can be selected. The reconstruction only requires

[
R_2[v]=R_2[u]+2w(u,v),
]

and the visited array selects one such predecessor. Positive edge weights make (R_2) strictly increase along every chosen tree edge, so the reconstruction cannot create a cycle and produces exactly (N-1) edges.
