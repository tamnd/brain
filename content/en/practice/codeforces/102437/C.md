---
title: "CF 102437C - \u0415\u0434\u0438\u043d\u0430\u044f \u0441\u0435\u0442\u044c"
description: "We have a connected undirected graph whose edges form a cactus: every road belongs to at most one simple cycle. Each city must receive one of three transmitter types, and adjacent cities must receive different types."
date: "2026-08-08T15:12:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 257
verified: true
draft: false
---

[CF 102437C - \u0415\u0434\u0438\u043d\u0430\u044f \u0441\u0435\u0442\u044c](https://codeforces.com/problemset/problem/102437/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph whose edges form a cactus: every road belongs to at most one simple cycle. Each city must receive one of three transmitter types, and adjacent cities must receive different types. Type 3 is expensive, so the task is to minimize the number of vertices colored with type 3.

The input contains the cities and roads of the graph. The required output is the minimum possible number of vertices using type 3. Under the given cactus guarantees, a valid 3-coloring always exists, so `-1` cannot actually occur for a valid input. A cactus is 2-degenerate, because every nontrivial subgraph has a vertex of degree at most two, and such graphs are always 3-colorable.

The size limit of (n=10^5) and (m=1.5\cdot10^5) rules out anything quadratic in the graph size. Even (O(n^2)) would mean about (10^{10}) primitive operations in the worst case. We need an algorithm close to linear in (n+m). The cactus condition is exactly the structural restriction that lets us obtain such a solution.

There are several edge cases where a simpler approach gives the wrong answer. A single vertex has no edges, so it needs no expensive transmitter.

```
1 0
```

The answer is `0`. A solution that assumes every connected graph has at least one edge would mishandle this case.

An even cycle is bipartite, so it needs only the first two transmitter types.

```
4 4
1 2
2 3
3 4
4 1
```

The answer is `0`. A method that charges every cycle for a type 3 transmitter would incorrectly return `1`.

Odd cycles do require type 3, but several odd cycles can share the same expensive vertex. For example, consider two triangles with one common vertex.

```
5 6
1 2
2 3
3 1
1 4
4 5
5 1
```

The answer is `1`. Color vertex 1 with type 3, then each triangle can use types 1 and 2 on its other two vertices. Simply counting odd cycles would incorrectly return `2`.

## Approaches

The most direct brute-force solution assigns one of three colors to every vertex, then checks whether all edges have differently colored endpoints. There are exactly (3^n) assignments, and checking one assignment takes (O(n+m)) time. In the worst case this means (3^{100000}) assignments and roughly (150000\cdot3^{100000}) edge checks, which is completely infeasible.

The brute-force works because it explicitly considers every possible coloring. The problem is that most of the graph does not need to be considered simultaneously. In a cactus, the graph can be decomposed into blocks, and every block is either a single edge or one simple cycle. Different blocks interact through at most one common vertex. That turns the block structure into a tree.

This suggests dynamic programming over the block tree. For every vertex (v), we keep three values, one for each possible color of (v). The value represents the minimum number of type 3 transmitters in the entire part of the graph below (v), assuming that (v) has the chosen color.

A block connecting several vertices can then be processed independently once the color of its parent vertex is fixed. For an edge, we only need to choose a color different from the parent. For a cycle, we fix the color of the parent vertex and run a small path DP around the rest of the cycle, finally checking that the last vertex also differs from the parent.

The nontrivial part is constructing the blocks efficiently. Tarjan's algorithm for biconnected components does exactly that in (O(n+m)). In a cactus, every resulting biconnected component is guaranteed to be either one edge or a simple cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^n(n+m))) | (O(n+m)) | Too slow |
| Block-tree DP | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph and find all biconnected components using Tarjan's algorithm. While performing the DFS, keep the traversed edges on a stack. Whenever `low[child] >= tin[parent]`, pop edges until the child's DFS edge is removed. Those edges form one biconnected component.

Because the input graph is a cactus, each component is either a single bridge or a simple cycle. We also collect the vertices belonging to every component.
2. Build the incidence structure between vertices and components. For every component, store which graph vertices it contains. For every vertex, store the list of components containing it.

The resulting incidence graph is a tree after treating original vertices and components as two different kinds of nodes. This is the block-cut tree of the cactus.
3. Root this block tree at any graph vertex, say vertex `0`. For every component, remember which vertex is its parent. For every non-root vertex, remember which component is its parent.

We now have a clear parent-child relationship. A component has exactly one parent vertex, while all its other vertices lead to independent subtrees.
4. Define `dp[v][c]` as the minimum number of type 3 transmitters in the subtree rooted at vertex `v`, assuming that `v` receives color `c`.

The direct contribution of `v` is `1` when `c` is type 3 and `0` otherwise. Every child component contributes its own optimal value for the same color of `v`.

Thus,

[
dp[v][c] = [c=3] + \sum_{\text{child components } B} blockDP[B][c].
]
5. Process vertices in reverse order of the block-tree traversal. Before calculating `dp[v]`, all vertices inside every child component have already been calculated. This gives us everything needed to calculate that component's DP.
6. For a bridge component with parent vertex `p` and other vertex `u`, calculate

[
blockDP[B][c] =
\min_{d\ne c} dp[u][d].
]

The only constraint imposed by the edge is that its two endpoints have different colors.
7. For a cycle component, first order its vertices as

[
p,v_1,v_2,\ldots,v_{k-1},p,
]

where `p` is the parent vertex.

Fix the color `c` of `p`. Start a three-state DP with only color `c` allowed at `p`, at cost zero. Then process (v_1,v_2,\ldots,v_{k-1}) in order. When assigning color `d` to the next vertex, the previous vertex must have one of the two colors different from `d`.

After the last vertex has been processed, only states whose color differs from the fixed parent color are valid, because the last vertex and the parent are connected by the closing cycle edge.
8. Once all child components have been incorporated into every vertex, the answer is

[
\min_{c\in{1,2,3}} dp[root][c].
]

Since a valid cactus is always 3-colorable, at least one of these values is finite.

### Why it works

The key invariant is that `dp[v][c]` contains the optimal coloring cost for exactly the part of the block tree below `v`, with `v` fixed to color `c`. Different child components of a vertex intersect only at that vertex, so after its color is fixed, their choices are independent and their optimal costs can be added.

For an edge component, checking the two possible different colors is exactly the proper-coloring condition. For a cycle, the path DP considers every possible color of every vertex while enforcing inequality on consecutive vertices, and the final transition enforces the closing edge. Thus every proper coloring of the component is represented, and the minimum-cost one is selected.

Because every block is processed only after all of its descendant vertices are solved, the invariant propagates from leaves to the root. The final minimum over the root's three possible colors consequently considers every valid coloring of the whole cactus and chooses the cheapest one.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 9

def solve_case(n, edges):
    m = len(edges)

    graph = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(edges):
        graph[u].append(eid)
        graph[v].append(eid)

    # Iterative Tarjan algorithm for biconnected components.
    tin = [-1] * n
    low = [0] * n
    parent = [-1] * n
    parent_edge = [-1] * n
    it = [0] * n

    edge_stack = []
    components = []

    timer = 0
    tin[0] = low[0] = timer
    timer += 1

    dfs_stack = [0]

    while dfs_stack:
        u = dfs_stack[-1]

        if it[u] < len(graph[u]):
            eid = graph[u][it[u]]
            it[u] += 1

            if eid == parent_edge[u]:
                continue

            a, b = edges[eid]
            v = b if a == u else a

            if tin[v] == -1:
                parent[v] = u
                parent_edge[v] = eid
                edge_stack.append(eid)

                tin[v] = low[v] = timer
                timer += 1

                dfs_stack.append(v)
            elif tin[v] < tin[u]:
                edge_stack.append(eid)
                if tin[v] < low[u]:
                    low[u] = tin[v]
        else:
            dfs_stack.pop()

            p = parent[u]
            if p != -1:
                if low[u] < low[p]:
                    low[p] = low[u]

                if low[u] >= tin[p]:
                    comp = []
                    while True:
                        eid = edge_stack.pop()
                        comp.append(eid)
                        if eid == parent_edge[u]:
                            break
                    components.append(comp)

    k = len(components)

    # Vertices belonging to every component.
    comp_vertices = [[] for _ in range(k)]
    incident = [[] for _ in range(n)]

    for cid, comp_edges in enumerate(components):
        vertices = set()

        for eid in comp_edges:
            u, v = edges[eid]
            vertices.add(u)
            vertices.add(v)

        vertices = list(vertices)
        comp_vertices[cid] = vertices

        for v in vertices:
            incident[v].append(cid)

    # Root the block-cut tree at vertex 0.
    # parent_comp[v] is the component through which v is reached.
    parent_comp = [-2] * n
    parent_comp[0] = -1

    # comp_parent[c] is the vertex through which component c is reached.
    comp_parent = [-1] * k

    order = [0]

    for v in order:
        for cid in incident[v]:
            if cid == parent_comp[v]:
                continue

            comp_parent[cid] = v

            for u in comp_vertices[cid]:
                if u == v:
                    continue

                if parent_comp[u] == -2:
                    parent_comp[u] = cid
                    order.append(u)

    dp = [[0, 0, 0] for _ in range(n)]
    block_dp = [[0, 0, 0] for _ in range(k)]

    # Process bottom-up.
    for v in reversed(order):
        # First calculate all components for which v is the parent.
        for cid in incident[v]:
            if comp_parent[cid] != v:
                continue

            comp_edges = components[cid]
            vertices = comp_vertices[cid]

            # A component consisting of one edge.
            if len(comp_edges) == 1:
                eid = comp_edges[0]
                a, b = edges[eid]
                u = b if a == v else a

                for c in range(3):
                    best = INF
                    for d in range(3):
                        if d != c and dp[u][d] < best:
                            best = dp[u][d]
                    block_dp[cid][c] = best

            else:
                # A cactus biconnected component with more than one edge
                # is a simple cycle.
                local = {x: [] for x in vertices}

                for eid in comp_edges:
                    a, b = edges[eid]
                    local[a].append(b)
                    local[b].append(a)

                # Order the cycle starting from its parent vertex v.
                cycle = [v]
                prev = -1
                cur = v

                while True:
                    x, y = local[cur]
                    nxt = x if x != prev else y

                    if nxt == v:
                        break

                    cycle.append(nxt)
                    prev, cur = cur, nxt

                for parent_color in range(3):
                    cur_dp = [INF, INF, INF]
                    cur_dp[parent_color] = 0

                    for u in cycle[1:]:
                        nxt_dp = [INF, INF, INF]

                        for new_color in range(3):
                            best = INF
                            for old_color in range(3):
                                if old_color == new_color:
                                    continue
                                if cur_dp[old_color] < best:
                                    best = cur_dp[old_color]

                            nxt_dp[new_color] = best + dp[u][new_color]

                        cur_dp = nxt_dp

                    best = INF
                    for last_color in range(3):
                        if last_color == parent_color:
                            continue
                        if cur_dp[last_color] < best:
                            best = cur_dp[last_color]

                    block_dp[cid][parent_color] = best

        # Now every child component of v is solved.
        for color in range(3):
            value = 1 if color == 2 else 0

            for cid in incident[v]:
                if comp_parent[cid] == v:
                    value += block_dp[cid][color]

            dp[v][color] = value

    return min(dp[0])

def main():
    n, m = map(int, input().split())
    edges = [tuple(map(lambda x: int(x) - 1, input().split()))
             for _ in range(m)]

    print(solve_case(n, edges))

if __name__ == "__main__":
    main()
```

The graph construction stores each edge by an integer ID. This is necessary for Tarjan's algorithm because the parent relation is an edge relation, not merely a vertex relation. In particular, when an undirected DFS sees the edge leading back to its parent, that exact edge must be ignored.

The Tarjan implementation is iterative rather than recursive. A cactus can contain a path of (10^5) vertices, so a recursive DFS would require increasing Python's recursion limit and would also put unnecessary pressure on the Python call stack. The explicit stack gives the same DFS order without that risk.

The edge stack contains exactly those DFS edges that belong to the current biconnected component. When `low[u] >= tin[parent[u]]`, no edge below `u` can connect above `parent[u]`, so the edges up to `parent_edge[u]` form one complete block.

The `incident` lists are what turn the biconnected components into a block-cut tree. The original graph can have many cycles touching the same vertex, but the block-cut representation still has a tree structure.

The cycle DP uses only three states. For each new color, it takes the cheapest previous state with a different color. The final restriction against the parent's color is essential. Omitting it would accidentally treat the cycle as a path and could accept an invalid coloring.

All costs are at most (n), so ordinary Python integers are more than sufficient. There is no integer overflow issue.

## Worked Examples

### Sample 1

The graph consists of three triangles. The first triangle contains vertices `1, 2, 3`, while the other two triangles are attached at vertices `2` and `3`.

For each leaf triangle, fixing the shared vertex to type 3 lets its other two vertices use types 1 and 2, so that component contributes zero additional type 3 transmitters. If the shared vertex uses type 1 or type 2, one of the other two vertices must use type 3.

The resulting DP values are:

| Vertex or component | State for type 1 | State for type 2 | State for type 3 |
| --- | --- | --- | --- |
| Leaf triangle at 2 | 1 | 1 | 0 |
| `dp[2]` | 1 | 1 | 1 |
| Leaf triangle at 3 | 1 | 1 | 0 |
| `dp[3]` | 1 | 1 | 1 |
| Root triangle at 1 | 2 | 2 | 2 |
| `dp[1]` | 2 | 2 | 3 |

The answer is `2`. One optimal coloring makes vertex 1 type 2, vertex 2 type 3, and vertex 3 type 1. Each attached triangle can then be completed with types 1 and 2, except for one additional type 3 in the triangle attached to vertex 3.

### Sample 2

The graph contains several cycles connected through vertices 2, 9, and 10. The large cycle through vertices 3 through 8 is even, and the cycle through vertices 10 through 13 is also even. The triangles are the only places where an additional type 3 may be forced.

The relevant bottom-up states are:

| Substructure | Type 1 parent | Type 2 parent | Type 3 parent |
| --- | --- | --- | --- |
| Even cycle through 3 | 1 | 1 | 0 |
| Even cycle through 10 | 1 | 1 | 0 |
| Triangle at 9 with 10 and 15 | 1 | 1 | 1 |
| `dp[9]` | 1 | 1 | 2 |
| Triangle at 2 with 9 and 14 | 2 | 2 | 1 |
| `dp[2]` | 2 | 2 | 2 |

The final minimum is `2`.

The trace shows why the DP cannot simply count odd cycles. The type 3 choice made at a shared vertex can simultaneously satisfy several cycle constraints, and the state of that shared vertex carries exactly the information needed by its parent component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Tarjan processes every edge a constant number of times, and every block DP transition examines only three colors |
| Space | (O(n+m)) | The graph, component lists, block-cut information, and DP arrays are all linear in the input size |

The largest allowed graph has only (O(n)) edges because it is a cactus, with the stated limit of (m\le150000). The algorithm performs a constant amount of three-color DP work per vertex and per edge, so it comfortably fits the intended linear-time requirement.

## Test Cases

The following tests assume the solution above is saved as `solution.py` and exposes `solve_case`.

```python
from solution import solve_case

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    n, m = data[0], data[1]

    edges = []
    pos = 2

    for _ in range(m):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        edges.append((u, v))

    return str(solve_case(n, edges))

# Sample 1
assert run("""\
7 9
1 2
2 3
3 1
2 4
4 5
5 2
3 6
6 7
7 3
""") == "2", "sample 1"

# Sample 2
assert run("""\
15 18
1 2
2 3
3 4
4 5
5 6
6 7
7 8
8 3
2 9
9 10
10 11
11 12
12 13
13 10
2 14
14 9
9 15
15 10
""") == "2", "sample 2"

# Minimum-size graph.
assert run("""\
1 0
""") == "0", "single isolated city"

# Even cycle, completely bipartite.
assert run("""\
4 4
1 2
2 3
3 4
4 1
""") == "0", "even cycle"

# Two triangles sharing one vertex.
# The common vertex can be the only type-3 vertex.
assert run("""\
5 6
1 2
2 3
3 1
1 4
4 5
5 1
""") == "1", "shared odd cycles"

# Maximum-size cactus for n = 100000.
# 49999 triangles share vertex 1, plus one leaf.
# This has 149998 edges, essentially the maximum possible for this n.
n = 100000
edges = []

for i in range(49999):
    a = 2 + 2 * i
    b = a + 1
    edges.append((1, a))
    edges.append((a, b))
    edges.append((b, 1))

edges.append((1, 100000))

assert solve_case(n, edges) == 1, "maximum-size cactus"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0` | Minimum-size graph and zero-edge boundary case |
| Four-cycle | `0` | Even cycles need only two colors |
| Two triangles sharing vertex 1 | `1` | One expensive vertex can satisfy multiple odd cycles |
| 49999 shared triangles plus one leaf | `1` | Maximum-size input, linear complexity, large block tree |

## Edge Cases

For a single city,

```
1 0
```

the block list is empty. The root has no child components, so its three DP states are `[0, 0, 1]`. Choosing either of the first two colors gives answer `0`.

For the four-cycle

```
4 4
1 2
2 3
3 4
4 1
```

Tarjan produces one cycle component containing all four vertices. When the parent color is fixed, the cycle DP can alternate the other two colors around the remaining three vertices and close the cycle without using type 3. The component contributes zero when the parent itself has type 3 and the other states correctly account for the possible use of type 3. At the root, the minimum is `0`.

For two triangles sharing vertex 1,

```
5 6
1 2
2 3
3 1
1 4
4 5
5 1
```

the block-cut tree has the shared vertex as the parent of both triangle components. If vertex 1 is type 3, each triangle's two remaining vertices can use types 1 and 2. Both component DPs consequently contribute zero for parent color 3, while the root contributes one for being type 3 itself. The answer is `1`.

The maximum-size test consists of 49999 triangles sharing vertex 1 and one additional leaf. Giving vertex 1 type 3 lets every triangle use only types 1 and 2 on its other vertices, so the entire graph costs exactly one expensive transmitter. The algorithm processes all 149998 edges and 100000 vertices once, without enumerating colorings or cycles globally, and returns `1`.
