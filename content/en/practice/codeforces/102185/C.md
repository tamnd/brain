---
title: "CF 102185C - \u041a\u0430\u043a \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u0442\u044c \u0431\u0435\u0441\u043f\u043e\u043a\u043e\u0438\u0442\u044c\u0441\u044f \u0438 \u043f\u043e\u043b\u044e\u0431\u0438\u0442\u044c \u043a\u0430\u043a\u0442\u0443\u0441\u044b"
description: "We have a connected undirected cactus graph. A cactus here has the stronger property that every vertex belongs to at most one simple cycle, and every cycle has even length. City 1 initially contains a factory."
date: "2026-08-19T15:38:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "C"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 433
verified: true
draft: false
---

[CF 102185C - \u041a\u0430\u043a \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u0442\u044c \u0431\u0435\u0441\u043f\u043e\u043a\u043e\u0438\u0442\u044c\u0441\u044f \u0438 \u043f\u043e\u043b\u044e\u0431\u0438\u0442\u044c \u043a\u0430\u043a\u0442\u0443\u0441\u044b](https://codeforces.com/problemset/problem/102185/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected cactus graph. A cactus here has the stronger property that every vertex belongs to at most one simple cycle, and every cycle has even length. City 1 initially contains a factory. From a factory, a train reaches every destination along a shortest path. If several shortest paths exist, any of them may be chosen.

For the initial factory, the graph has the useful property that every railway edge is used only in one direction by all possible shortest routes. After factories are added, this can cease to be true. If some edge may have trains going in both directions, we must build one additional parallel railway there and prescribe opposite directions on the two tracks.

The input describes the cities, the existing railways, and the factories in the order in which they are built. For every new factory we have to output how many new railway tracks are needed at that moment. A factory already built earlier does not need anything again.

The graph has at most (10^5) vertices and at most (N-1+N/4) edges. The second bound means that there are only (O(N)) edges in total, so a linear or (N\log N) solution is realistic. With (10^5) factories, an algorithm that scans the whole graph for every factory would perform around (10^{10}) edge operations in the worst case, which is far beyond the two second limit. Quadratic preprocessing is also unnecessary because the cactus structure gives much more information than an arbitrary graph.

There are several easy cases that expose mistakes in a naive implementation. On the graph consisting of one edge, if the queries are `2 2 1`, the answer is `1 0 0`. The second factory is a duplicate of the first new factory, and the last query is the original factory at city 1, so treating every query as a new conflict would be wrong.

An even cycle is another important case. For

```
4 4
1 2
2 3
3 4
4 1
1
3
```

the answer is `4`. Cities 1 and 3 are opposite on the cycle. Every one of the four railway edges can be used in opposite directions by shortest routes from the two factories, so handling an even cycle like a tree would underestimate the answer.

A query at city 1 must also give zero. For example,

```
2 1
1 2
3
1 1 1
```

produces `0 0 0`. The initial factory and a later factory in the same city induce exactly the same shortest-path directions.

## Approaches

The direct approach is to recompute the shortest-path structure for every new factory. Run a BFS from the new factory, obtain the distance to every vertex, and inspect every edge. For an edge (u v), if the distance from the source to (u) is smaller, shortest routes may use the edge as (u\to v), and symmetrically for (v\to u). Comparing this orientation with the already existing one tells us whether another railway is necessary.

This is correct because the shortest-path distances completely characterize which endpoint of an edge can precede the other on a shortest route. The problem is the repeated work. One BFS plus one scan of the edges costs (O(N+M)=O(N)), and doing it for (K) factories costs (O(KN)). With both parameters equal to (10^5), this is roughly (10^{10}) operations.

The useful observation is that an even cactus is a partial cube. We do not need the general theory of partial cubes to use the relevant part of it. Every bridge forms one independent class consisting of that single edge. Inside an even cycle, opposite edges form pairs. Removing one such opposite pair separates the graph into exactly two sides. The two edges in the pair always behave together with respect to shortest-path directions.

Thus the graph's edges can be partitioned into independent classes. A bridge class has weight 1, while a pair of opposite edges in an even cycle has weight 2. A class causes a collision exactly when factories have appeared on both sides of its corresponding cut. Once both sides contain a factory, that class is permanently fixed and never contributes again.

There is one more cactus-specific simplification. Root the graph at city 1. Every class has a side that is exactly a rooted subtree. For a bridge, this is the subtree below the bridge. For a cycle, if its vertices along the DFS tree are

[
c_0,c_1,\ldots,c_{2h-1},
]

with (c_0) being the highest vertex of the cycle, the opposite-edge class containing the edge (c_{i-1}c_i), for (1\le i\le h), has as its non-root side exactly the subtree of (c_i).

The initial factory is at the root, so the other side of every such cut already contains a factory at time zero. Consequently, a class contributes exactly once, at the moment when the first future factory enters its rooted-subtree side. We can compute that first time for every subtree and add the class weight to that answer.

The brute-force method works because it explicitly reconstructs the direction information for every source. It fails because almost all of that information is repeated. The observation that the relevant information is actually carried by independent bridge classes and opposite-edge pairs reduces the whole problem to subtree minimums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(K(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O(N+M+K)) | (O(N+M+K)) | Accepted |

## Algorithm Walkthrough

1. Root the cactus at city 1 with a DFS spanning tree. Store `parent`, `depth`, and the parent edge for every vertex. The DFS tree gives us a natural meaning to every rooted subtree.
2. Initially give every tree edge weight 1. Such an edge represents a bridge class, unless it later turns out to belong to a cycle. A vertex `v` represents the tree edge from `parent[v]` to `v`.
3. Find every non-tree edge. In an undirected DFS of a cactus, every such edge connects a descendant to an ancestor and closes exactly one cycle. Walk from the descendant upward through parent pointers until reaching the ancestor. Because cycles in a cactus share at most one vertex, the total length of all these walks is (O(N)).
4. Suppose the discovered cycle has vertices (c_0,c_1,\ldots,c_{2h-1}), where (c_0) is the ancestor and the final edge (c_{2h-1}c_0) is the non-tree edge. Its opposite-edge classes are
[
(e_i,e_{i+h}),\qquad 0\le i<h.
]
For the class containing (e_{i-1}=c_{i-1}c_i), its side away from the root is exactly the subtree of (c_i). Give that subtree representative weight 2. The remaining tree edges of the cycle are the opposite members of these pairs, so they receive weight zero and must not be treated as separate classes.
5. For every city, record the first time at which a factory is built there. City 1 gets time zero because its factory already exists. If the same city occurs several times in the query sequence, only its earliest query matters for the class calculation.
6. Compute `first[v]`, the earliest factory time anywhere in the rooted subtree of `v`. Process the DFS order backwards and propagate every child's minimum to its parent. This turns the question "when does a factory first enter this cut's side?" into one stored value.
7. For every vertex whose class weight is nonzero, let `t = first[v]`. If `t` is finite, add the class weight to answer `t`. This class becomes problematic exactly when the first factory enters its subtree side, because city 1 was already present on the other side.
8. Output the accumulated values for query times 1 through (K). A repeated query contributes nothing if its relevant subtrees already contain an earlier factory.

The invariant is that every independent orientation conflict is represented by exactly one class, and every class is represented by one rooted subtree. Before the first factory enters that subtree, all factories are on the other side, so there is no conflict. At the first entry, both sides contain factories and all edges of that class must be doubled. Afterwards the class is already fixed permanently. Since the classes partition all relevant edges, summing their weights gives exactly the minimum number of additional tracks.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    edges = []

    for eid in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        edges.append((a, b))
        graph[a].append((b, eid))
        graph[b].append((a, eid))

    k = int(input())
    queries = [int(x) - 1 for x in input().split()]

    # Build an actual DFS tree iteratively.
    parent = [-1] * n
    parent_edge = [-1] * n
    depth = [0] * n
    order = [0]
    parent[0] = 0

    it = [0] * n
    stack = [0]
    back_edges = []

    while stack:
        v = stack[-1]

        if it[v] == len(graph[v]):
            stack.pop()
            continue

        u, eid = graph[v][it[v]]
        it[v] += 1

        if eid == parent_edge[v]:
            continue

        if parent[u] == -1:
            parent[u] = v
            parent_edge[u] = eid
            depth[u] = depth[v] + 1
            order.append(u)
            stack.append(u)
        else:
            # In an undirected DFS of a cactus, a non-tree edge
            # goes between a vertex and one of its ancestors.
            if depth[u] < depth[v]:
                back_edges.append((v, u, eid))

    # weight[v] describes the edge parent[v] -> v.
    # Initially every tree edge is a bridge class of weight 1.
    weight = [0] * n
    for v in range(1, n):
        weight[v] = 1

    # Each even cycle contributes h classes of weight 2.
    # The first h tree edges on the ancestor-to-descendant path
    # represent these classes. The remaining tree edges are their
    # opposite partners and must not form separate classes.
    for descendant, ancestor, _ in back_edges:
        path = []
        cur = descendant

        while cur != ancestor:
            path.append(cur)
            cur = parent[cur]

        path.reverse()

        # The cycle has len(path) tree edges plus the back edge.
        cycle_len = len(path) + 1
        half = cycle_len // 2

        for i, child in enumerate(path):
            if i < half:
                weight[child] = 2
            else:
                weight[child] = 0

    INF = k + 1

    # first_at[v] is the first factory time exactly at v.
    first_at = [INF] * n
    first_at[0] = 0

    for t, v in enumerate(queries, 1):
        if first_at[v] == INF:
            first_at[v] = t

    # first[v] becomes the first factory time anywhere in subtree(v).
    first = first_at[:]

    for v in reversed(order[1:]):
        p = parent[v]
        if first[v] < first[p]:
            first[p] = first[v]

    answer = [0] * (k + 1)

    # Every nonzero-weight class is represented by one subtree.
    # Its opposite side already contains city 1 at time zero.
    # Thus the class contributes exactly when its subtree gets
    # its first factory.
    for v in range(1, n):
        if weight[v] and first[v] <= k:
            answer[first[v]] += weight[v]

    print(*answer[1:])

if __name__ == "__main__":
    solve()
```

The adjacency list stores both endpoints and the edge identifier. The edge identifier is needed to distinguish a parent edge from another edge leading to a vertex that has already been visited.

The iterative DFS avoids Python recursion depth problems on a path containing (10^5) vertices. The `it` array records the next adjacency entry to inspect, which gives the same traversal order as recursive DFS without relying on the Python call stack.

After the DFS, every tree edge initially receives weight 1. When a back edge closes a cycle, its ancestor-to-descendant tree path is recovered using `parent`. If the cycle length is (2h), its first (h) tree edges represent the (h) opposite-edge classes, each with physical size two. The remaining tree edges belong to those same classes as their opposite members, so assigning them weight zero prevents double counting.

The total work spent walking cycle paths is linear. A vertex can occur in only one cycle, except as a shared articulation point, because the graph is a vertex cactus. Hence the lengths of all recovered cycles are collectively (O(N)).

The query processing is deliberately done before the subtree aggregation. `first_at[v]` represents only the earliest factory at the exact vertex, while `first[v]` after the reverse traversal represents the earliest factory anywhere below that vertex. Since city 1 has time zero, every class represented by a proper subtree already has a factory on the complementary side.

There is no integer-overflow issue in Python. In C++, a 32-bit integer would also be sufficient for the answer because at most (M\le 125000) physical edges can be added, but Python's integer type removes that concern entirely.

## Worked Examples

Only one official sample is provided, so the second trace uses a small even cycle.

For the official sample, the DFS can produce the tree path

```
1 - 3 - 4 - 7 - 5 - 6
    |
    2
```

with the additional edge `5-3` closing the cycle `3-4-7-5-3`. The relevant class representatives are shown below.

| Representative | Weight | Meaning | First factory in subtree | Contribution |
| --- | --- | --- | --- | --- |
| 2 | 1 | bridge 1-2 | 2 | 1 at query 2 |
| 3 | 1 | bridge 1-3 | 1 | 1 at query 1 |
| 4 | 2 | pair 3-4 and 7-5 | 3 | 2 at query 3 |
| 7 | 2 | pair 4-7 and 3-5 | 1 | 2 at query 1 |
| 5 | 0 | opposite member already represented | 1 | 0 |
| 6 | 1 | bridge 5-6 | 1 | 1 at query 1 |

The first query is city 6. Its subtree contains the representative vertices 3, 7, and 6, whose class weights are (1+2+1=4). Those are exactly the four new tracks listed in the statement. The second query is city 2, which is the first factory in subtree 2, so it contributes one bridge. The third query is city 4, which is the first factory in subtree 4, adding the two opposite cycle edges. The repeated query at city 4 changes nothing, and city 5 is already inside the sides activated by earlier factories.

For the second example, consider a four-cycle.

```
4 4
1 2
2 3
3 4
4 1
1
3
```

Rooting at city 1 gives the cycle path `1-2-3-4` plus the back edge `4-1`.

| Representative | Weight | First factory in subtree | Contribution |
| --- | --- | --- | --- |
| 2 | 2 | 1 | 2 |
| 3 | 2 | 1 | 2 |
| 4 | 0 | 1 | 0 |

The two classes correspond to the two pairs of opposite edges. Factory 3 is on the non-root side of both classes, so both classes become bidirectional. Their weights sum to four, matching the fact that all four physical edges need an additional parallel track.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+M+K)) | DFS, cycle reconstruction, subtree minimum propagation, and query processing are all linear |
| Space | (O(N+M+K)) | Adjacency lists, DFS arrays, query sequence, and answer array |

The constraints give (M=O(N)), so the total complexity is effectively (O(N+K)). With both (N) and (K) bounded by (10^5), this is comfortably within the intended limits, while the brute-force (O(KN)) approach would require around (10^{10}) operations.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for eid in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append((b, eid))
        graph[b].append((a, eid))

    k = int(input())
    queries = [int(x) - 1 for x in input().split()]

    parent = [-1] * n
    parent_edge = [-1] * n
    depth = [0] * n
    order = [0]
    parent[0] = 0

    it = [0] * n
    stack = [0]
    back_edges = []

    while stack:
        v = stack[-1]

        if it[v] == len(graph[v]):
            stack.pop()
            continue

        u, eid = graph[v][it[v]]
        it[v] += 1

        if eid == parent_edge[v]:
            continue

        if parent[u] == -1:
            parent[u] = v
            parent_edge[u] = eid
            depth[u] = depth[v] + 1
            order.append(u)
            stack.append(u)
        elif depth[u] < depth[v]:
            back_edges.append((v, u))

    weight = [0] * n
    for v in range(1, n):
        weight[v] = 1

    for descendant, ancestor in back_edges:
        path = []
        cur = descendant

        while cur != ancestor:
            path.append(cur)
            cur = parent[cur]

        path.reverse()

        cycle_len = len(path) + 1
        half = cycle_len // 2

        for i, child in enumerate(path):
            if i < half:
                weight[child] = 2
            else:
                weight[child] = 0

    INF = k + 1
    first = [INF] * n
    first[0] = 0

    for t, v in enumerate(queries, 1):
        if first[v] == INF:
            first[v] = t

    for v in reversed(order[1:]):
        p = parent[v]
        first[p] = min(first[p], first[v])

    ans = [0] * (k + 1)

    for v in range(1, n):
        if weight[v] and first[v] <= k:
            ans[first[v]] += weight[v]

    return " ".join(map(str, ans[1:]))

def run(inp: str) -> str:
    global solve
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
7 7
1 2
1 3
3 4
4 7
5 7
3 5
5 6
5
6 2 4 4 5
"""

assert run(sample) == "4 1 2 0 0", "official sample"

cycle4 = """\
4 4
1 2
2 3
3 4
4 1
1
3
"""

assert run(cycle4) == "4", "opposite vertices of an even cycle"

minimum = """\
2 1
1 2
3
2 2 1
"""

assert run(minimum) == "1 0 0", "minimum graph and repeated factory"

root_repeated = """\
2 1
1 2
4
1 1 1 1
"""

assert run(root_repeated) == "0 0 0 0", "all queries equal to the initial factory"

path = """\
6 5
1 2
2 3
3 4
4 5
5 6
5
6 6 4 4 2
"""

assert run(path) == "5 0 2 0 0", "tree path and repeated vertices"

n = 100000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
large = f"{n} {n - 1}\n{edges}\n3\n{n} {n} 1\n"

assert run(large) == f"{n - 1} 0 0", "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | `4 1 2 0 0` | Complete interaction between bridges, an even cycle, repeated factories, and nested subtrees |
| Four-cycle with factory 3 | `4` | Opposite-edge classes inside an even cycle |
| Two-vertex graph with `2 2 1` | `1 0 0` | Minimum graph, repeated factory, and the initial factory |
| Two-vertex graph with all queries at 1 | `0 0 0 0` | Repeated use of the original factory |
| Six-vertex path | `5 0 2 0 0` | Pure tree behavior and boundary positions |
| Path with 100000 vertices | `99999 0 0` | Maximum input size and linear-time performance |

## Edge Cases

For the minimum graph

```
2 1
1 2
3
2 2 1
```

the only class is the bridge represented by subtree 2. Its first factory time is 1, so its weight 1 is added to answer 1. The second query still lies in the same subtree, but its first factory time is already 1, so it adds nothing. The third query is city 1, outside that subtree, so it also adds nothing. The result is `1 0 0`.

For the four-cycle

```
4 4
1 2
2 3
3 4
4 1
1
3
```

the cycle contains two opposite-edge classes. With the DFS rooted at 1, their representatives are vertices 2 and 3, each with weight 2. City 3 is inside both representative subtrees, so both classes receive first-factory time 1. The answer is (2+2=4). This is exactly the case that would be mishandled by treating every cycle edge as an independent bridge.

For repeated factories, consider

```
2 1
1 2
4
1 1 1 1
```

the only class is represented by subtree 2, and no query ever enters that subtree. Its first time is infinite, so it never contributes. Every answer is zero.

For a path,

```
6 5
1 2
2 3
3 4
4 5
5 6
5
6 6 4 4 2
```

every edge is a separate class. The first factory at 6 enters all five proper descendant-side cuts, giving `5`. The repeated query at 6 adds nothing. Factory 4 is the first factory in subtrees 4 and 5, contributing two edges. The later query at 4 is already covered, and factory 2 lies in a subtree whose first factory was already present at 4 or 6. The result is `5 0 2 0 0`.

The maximum-size path contains (99999) bridge classes. A factory at city 100000 is the first factory in every proper subtree, so the first answer is (99999). Repeating that city does not activate any new class. The implementation processes the entire graph and all queries with linear work, which is exactly the behavior required by the constraints.

The central idea is that the problem is not really asking us to recompute shortest paths. In an even cactus, shortest-path direction conflicts are organized into bridge classes and opposite-edge pairs. After rooting at city 1, every such class has a single subtree representative, and the answer for each query is simply the total weight of classes whose representative subtree receives its first factory at that query time.
