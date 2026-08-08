---
title: "CF 102441G - Sum of Distances in Cactus"
description: "We have a connected cactus graph with up to (10^5) vertices. A cactus is sparse and has a particularly useful structure: every biconnected component is either a single bridge or one simple cycle."
date: "2026-08-08T13:28:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "G"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 139
verified: true
draft: false
---

[CF 102441G - Sum of Distances in Cactus](https://codeforces.com/problemset/problem/102441/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected cactus graph with up to (10^5) vertices. A cactus is sparse and has a particularly useful structure: every biconnected component is either a single bridge or one simple cycle. For every unordered pair of vertices (u,v), we need its shortest-path distance, measured by the number of edges, and we need the sum of these distances over all pairs.

The graph contains (n) vertices and (m) edges, followed by the endpoints of every edge. The answer is one integer containing the sum over all (\binom n2) unordered pairs. The official examples have answers `3` for the triangle and `42` for the seven-vertex cactus.

The bound (n\le 10^5) rules out anything quadratic. Even (O(n^2)) already means around (10^{10}) pair operations. The graph is sparse because (m\le 2n), so an (O(n+m)) or (O((n+m)\log n)) solution is the natural target. The one-second limit makes the linear approach especially attractive. The answer itself can be much larger than a 32-bit integer. A path on (10^5) vertices already has total distance

[
\frac{n(n-1)(n+1)}6,
]

which is about (1.67\cdot10^{14}), so 64-bit arithmetic is necessary. Python integers handle this automatically.

Several small cases expose mistakes that are easy to make. With one vertex there are no pairs:

```
1 0
```

and the answer is `0`. An implementation that assumes every block contains at least one edge can fail here.

A tree must behave exactly like an ordinary tree. For example,

```
3 2
1 2
2 3
```

has pair distances (1,1,2), so the answer is `4`. Treating every biconnected component as a cycle would incorrectly classify the two bridge blocks.

A cycle cannot be handled like a tree. For a triangle,

```
3 3
1 2
2 3
3 1
```

every pair is at distance one, so the answer is `3`. A spanning-tree calculation would give (4), because it counts the pair (1,3) at distance two.

Even cycles have another boundary case. In a square,

```
4 4
1 2
2 3
3 4
4 1
```

the two opposite pairs have distance two, while the four adjacent pairs have distance one. The answer is (8). An implementation that replaces every cycle distance by one of the two directed arc lengths must handle the equal-length case correctly.

## Approaches

The direct approach is to run a breadth-first search from every vertex. One BFS gives the distance from its source to every other vertex, so summing all BFS results is correct. However, each BFS scans (O(n+m)) graph data. Repeating it (n) times costs (O(n(n+m))). At the maximum bounds, the adjacency lists contain (2m\le4\cdot10^5) entries, so merely scanning adjacency entries from all (10^5) sources can require about (4\cdot10^{10}) scans. That is far beyond the one-second limit.

The key observation is that a cactus does not have arbitrary biconnected components. Every block is either a bridge or a simple cycle. If we compress every block into a node and connect it to the original vertices contained in it, we obtain the block-cut tree. This tree describes how different blocks are connected, while the original cycle inside one block supplies the exact distance between its attachment vertices.

Root this block-cut tree. For a block (B), suppose its parent attachment vertex is (p). Every other vertex (v) belonging to (B) has a descendant region containing (v) and all blocks below it. Let its size be (s_v). From the viewpoint of (B), all vertices in that region attach to (B) exactly at (v).

There is also one region on the parent side of (B). Its size is

[
n-\sum_{v\ne p}s_v.
]

Thus every original vertex belongs to exactly one of these regions, and all pairs whose highest block is (B) can be counted by multiplying region sizes.

For a bridge, there are only two attachment vertices and their distance inside the block is one. Its contribution is simply

[
s_1s_2.
]

For a cycle with vertices arranged cyclically as (v_0,v_1,\ldots,v_{k-1}), the distance between (v_i) and (v_j) inside the block is

[
\min(|i-j|,\ k-|i-j|).
]

The remaining problem is to calculate

[
\sum_{i<j}s_i s_j\min(j-i,k-(j-i))
]

in linear time for the cycle. First calculate the ordinary line distance sum

[
T=\sum_{i<j}s_i s_j(j-i).
]

Then every pair with (j-i>k/2) was too far on the line. Its correct distance is (k-(j-i)), so the amount to subtract is

[
(j-i)-(k-(j-i))=2(j-i)-k.
]

A moving boundary identifies all such pairs in linear time, and prefix sums of (s_i) and (i s_i) give their total correction.

The brute-force method pays for every pair separately. The cactus structure lets us replace all pairs crossing one block by a weighted sum over the block's attachment vertices. The block-cut tree tells us which weights to use, and the cycle formula processes an entire cycle without enumerating its vertex pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n(n+m))) | (O(n+m)) | Too slow |
| Optimal | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Run an iterative low-link DFS and split the graph into biconnected components. Because the input is a cactus, every resulting component is either one bridge edge or one simple cycle. An iterative DFS is used so a path containing (10^5) vertices does not depend on Python's recursion stack.
2. Build the block-cut tree implicitly. For every biconnected component, store its vertices and add the component to the incidence list of each of those vertices. The cactus property guarantees that this incidence structure is a tree when blocks and articulation vertices are viewed as alternating node types.
3. Root this structure at vertex `0`. During the traversal, record the parent block of every vertex and the parent vertex of every block. Also keep the blocks in discovery order. Reversing that order later gives a bottom-up processing order.
4. Initialize every vertex subtree size to one, representing the vertex itself. Process blocks from the bottom upward. For a block (B) with parent vertex (p), every other incident vertex (v) has branch weight equal to its already computed subtree size `sub[v]`.
5. Let (S) be the sum of those child branch sizes. The parent-side branch has weight (n-S). This includes the parent vertex and everything outside the current block. The branch weights therefore sum to exactly (n).
6. If the block is a bridge, multiply its two branch weights. The unique path between the two regions must cross this bridge once, so every pair with endpoints in different regions contributes one.
7. If the block is a cycle, reconstruct its cyclic vertex order by following its two local neighbors. Associate the branch weight with every cycle vertex. The contribution of this block is the weighted sum of circular distances between every two attachment vertices.
8. Compute the cycle contribution first as a line. For every (j), maintain the prefix sums

[
P=\sum_{i<j}s_i
]

and

[
Q=\sum_{i<j}i s_i.
]

Then all pairs ending at (j) contribute

[
s_j(jP-Q).
]

This produces the sum using distance (j-i).

1. Correct the pairs that are better through the other side of the cycle. For each left endpoint (i), all relevant right endpoints satisfy

[
j-i>\left\lfloor\frac{k}{2}\right\rfloor.
]

A monotone pointer finds the first such (j). Prefix sums over the suffix then give

[
s_i\sum_j s_j(2(j-i)-k)
]

in constant time for that (i).

1. Add the block contribution to the answer and add the total child branch size to `sub[p]`. This makes the current block's entire descendant region available when its parent block is processed.

### Why it works

The invariant is that after processing a block, its parent vertex receives the exact number of original vertices lying below that block in the rooted block-cut tree. For a particular block, its incident branch regions are disjoint and together contain every original vertex. Any pair whose route uses this block has endpoints in two different regions, and its distance inside the block is exactly the distance between the corresponding attachment vertices. Such a pair is counted once at the highest block separating its two endpoints. Pairs inside one region are deliberately postponed to lower blocks. Consequently every unordered pair is counted exactly once at every block segment appearing on its shortest path, and the sum of all block contributions is exactly the sum of all shortest-path distances.

For a cycle, the only special issue is choosing the shorter of its two arcs. The line calculation gives one arc length, and the correction replaces precisely those pairs for which the other arc is shorter. When the cycle length is even and the two arcs are equal, the pair has difference exactly (k/2), so it is not included in the strict correction condition and keeps the correct distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cycle_cost(order, weights):
    k = len(order)

    pref_w = [0] * (k + 1)
    pref_iw = [0] * (k + 1)

    line_cost = 0
    for i, w in enumerate(weights):
        line_cost += w * (i * pref_w[i] - pref_iw[i])
        pref_w[i + 1] = pref_w[i] + w
        pref_iw[i + 1] = pref_iw[i] + i * w

    half = k // 2
    left = half + 1
    correction = 0

    total_w = pref_w[k]
    total_iw = pref_iw[k]

    for i, w in enumerate(weights):
        need = i + half + 1
        if left < need:
            left = need

        if left < k:
            suffix_w = total_w - pref_w[left]
            suffix_iw = total_iw - pref_iw[left]

            correction += w * (
                2 * suffix_iw - (2 * i + k) * suffix_w
            )

    return line_cost - correction

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    eu = [0] * m
    ev = [0] * m
    adj = [[] for _ in range(n)]

    for eid in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        eu[eid] = u
        ev[eid] = v
        adj[u].append((v, eid))
        adj[v].append((u, eid))

    # Iterative Tarjan DFS.
    tin = [0] * n
    low = [0] * n
    parent_edge = [-1] * n
    it = [0] * n

    edge_stack = []
    components = []

    timer = 1
    tin[0] = low[0] = timer

    dfs_stack = [0]

    while dfs_stack:
        u = dfs_stack[-1]

        if it[u] < len(adj[u]):
            v, eid = adj[u][it[u]]
            it[u] += 1

            if eid == parent_edge[u]:
                continue

            if tin[v] == 0:
                parent_edge[v] = eid
                timer += 1
                tin[v] = low[v] = timer

                edge_stack.append(eid)
                dfs_stack.append(v)
            elif tin[v] < tin[u]:
                if tin[v] < low[u]:
                    low[u] = tin[v]
                edge_stack.append(eid)

        else:
            dfs_stack.pop()

            pe = parent_edge[u]
            if pe == -1:
                continue

            p = eu[pe] if ev[pe] == u else ev[pe]

            if low[u] < low[p]:
                low[p] = low[u]

            if low[u] >= tin[p]:
                comp = []

                while True:
                    eid = edge_stack.pop()
                    comp.append(eid)
                    if eid == pe:
                        break

                components.append(comp)

    # Store vertices of every block and its incidence list.
    block_vertices = []
    incidence = [[] for _ in range(n)]

    for b, comp in enumerate(components):
        seen = {}
        verts = []

        for eid in comp:
            a = eu[eid]
            c = ev[eid]

            if a not in seen:
                seen[a] = True
                verts.append(a)

            if c not in seen:
                seen[c] = True
                verts.append(c)

        block_vertices.append(verts)

        for v in verts:
            incidence[v].append(b)

    B = len(block_vertices)

    # Root the block-cut tree at vertex 0.
    parent_block = [-1] * n
    parent_vertex = [-1] * B

    parent_block[0] = -2

    block_order = []
    vertex_order = [0]
    stack = [0]

    while stack:
        v = stack.pop()

        for b in incidence[v]:
            if b == parent_block[v]:
                continue

            if parent_vertex[b] != -1:
                continue

            parent_vertex[b] = v
            block_order.append(b)

            for x in block_vertices[b]:
                if x == v:
                    continue

                if parent_block[x] == -1:
                    parent_block[x] = b
                    vertex_order.append(x)
                    stack.append(x)

    sub = [1] * n
    answer = 0

    # Process blocks bottom-up.
    for b in reversed(block_order):
        verts = block_vertices[b]
        p = parent_vertex[b]

        child_sum = 0
        for v in verts:
            if v != p:
                child_sum += sub[v]

        parent_weight = n - child_sum

        if len(verts) == 2:
            a, c = verts

            if a == p:
                wa = parent_weight
                wc = sub[c]
            else:
                wa = sub[a]
                wc = parent_weight

            answer += wa * wc

        else:
            # A cactus block with at least three vertices is a cycle.
            local = {}

            for v in verts:
                local[v] = []

            for eid in components[b]:
                a = eu[eid]
                c = ev[eid]
                local[a].append(c)
                local[c].append(a)

            start = verts[0]
            order = []
            prev = -1
            cur = start

            for _ in range(len(verts)):
                order.append(cur)

                x, y = local[cur]
                nxt = x if x != prev else y

                prev, cur = cur, nxt

            weights = []
            for v in order:
                if v == p:
                    weights.append(parent_weight)
                else:
                    weights.append(sub[v])

            answer += cycle_cost(order, weights)

        sub[p] += child_sum

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part reads the graph while assigning every edge an ID. Edge IDs are needed by Tarjan's algorithm because an undirected edge appears twice in the adjacency lists, and the DFS must distinguish the actual parent edge from another edge leading back to an already visited vertex.

The low-link DFS maintains `tin` and `low`. When a child `u` satisfies `low[u] >= tin[p]`, all edges from the top of the edge stack through the parent edge form one biconnected component. In a cactus, these components are exactly the bridges and cycles needed by the rest of the algorithm.

The component construction uses dictionaries only temporarily for one component. The total number of entries processed is linear because every edge belongs to exactly one component. The persistent representation is the list of vertices in each block plus the incidence lists connecting original vertices to blocks.

The rooted traversal never constructs a separate block-cut tree. `parent_block` and `parent_vertex` contain exactly the information required to navigate it. Processing `block_order` backwards guarantees that every `sub[v]` used by a block has already incorporated all blocks below `v`.

The bridge case is deliberately short. Its two regions have one edge between their attachment vertices, so their cross-product is precisely the number of pairs whose path uses that bridge.

The cycle case reconstructs the actual cyclic order from the fact that every cycle vertex has exactly two neighbors inside the block. The order does not depend on which direction is chosen, because circular distance is symmetric.

The `cycle_cost` function is where the quadratic-looking part disappears. `line_cost` counts every pair using its forward distance. The two-pointer correction considers exactly the pairs whose forward distance exceeds half the cycle. The inequality is strict, which is essential for even cycles because opposite vertices already have the correct distance (k/2).

Python integers avoid overflow, but the products are still large, so keeping all calculations as integers is necessary. There is no modulo operation because the problem asks for the exact sum.

## Worked Examples

### Sample 1

The graph is a single triangle. There is one cycle block, and every vertex has branch weight one.

| Cycle position | Vertex | Branch weight |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 2 | 1 |
| 2 | 3 | 1 |

The line-distance sum is (1+2+1=4). The pair between positions zero and two is separated by three edges around the cycle, so its line distance two must be corrected to one. The correction is (2\cdot2-3=1). The cycle contribution is (4-1=3).

The final answer is `3`, matching the official sample.

### Sample 2

The graph consists of two triangles connected through vertices `1` and `3`, with a path `1-5-7` attached to vertex `1`. Rooting at vertex `1` gives the following relevant branch sizes.

| Block | Parent vertex | Child branch weights | Parent-side weight | Contribution |
| --- | --- | --- | --- | --- |
| Triangle `1-2-3` | 1 | 1, 3 | 3 | 15 |
| Edge `1-5` | 1 | 2 | 5 | 10 |
| Edge `5-7` | 5 | 1 | 6 | 6 |
| Triangle `3-4-6` | 3 | 1, 1 | 5 | 11 |

For the first triangle, the three branch weights are (3,1,3). Every pair of its attachment vertices is adjacent on the triangle, so its weighted contribution is

[
3\cdot1+1\cdot3+3\cdot3=15.
]

The second triangle has weights (5,1,1), giving

[
5\cdot1+5\cdot1+1\cdot1=11.
]

The two bridge contributions are (2\cdot5=10) and (1\cdot6=6). Their sum is

[
15+10+6+11=42.
]

The result is `42`, again matching the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Tarjan, block construction, block-cut traversal, and every cycle calculation are linear in the total graph size |
| Space | (O(n+m)) | Adjacency lists, biconnected components, incidence lists, and auxiliary arrays are all linear |

The graph has at most (2n) edges, so (n+m=O(n)). At (n=10^5), the algorithm processes only a linear number of graph objects instead of considering the roughly (5\cdot10^9) unordered vertex pairs individually. The official limit is 1 second and 256 MB, so avoiding both quadratic pair enumeration and deep recursive DFS is particularly useful here.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io
from contextlib import redirect_stdout

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin

    return out.getvalue().strip()

# Provided sample 1
assert run(
    """3 3
1 2
2 3
3 1
"""
) == "3", "sample 1"

# Provided sample 2
assert run(
    """7 8
2 1
3 1
5 1
3 2
4 3
5 7
6 3
4 6
"""
) == "42", "sample 2"

# Minimum-size graph
assert run(
    """1 0
"""
) == "0", "single vertex"

# A path of length two
assert run(
    """3 2
1 2
2 3
"""
) == "4", "tree distances"

# Five-cycle, all branch weights equal to one
assert run(
    """5 5
1 2
2 3
3 4
4 5
5 1
"""
) == "15", "odd cycle"

# Four-cycle, catches the even-cycle midpoint case
assert run(
    """4 4
1 2
2 3
3 4
4 1
"""
) == "8", "even cycle"

# Maximum-size tree, a path with 100000 vertices.
n = 100000
max_case = str(n) + " " + str(n - 1) + "\n"
max_case += "\n".join(f"{i} {i + 1}" for i in range(1, n)) + "\n"

assert run(max_case) == "166666666650000", "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0` | Minimum-size graph and empty pair set |
| `3 2`, edges `1-2`, `2-3` | `4` | Bridge handling and ordinary tree distances |
| Five-cycle | `15` | Odd cycle and equal branch weights |
| Four-cycle | `8` | Even cycle and opposite vertices |
| Path with 100000 vertices | `166666666650000` | Maximum size, large answer, and linear performance |

## Edge Cases

The single-vertex graph

```
1 0
```

has no biconnected components. The DFS visits vertex `0`, the block order remains empty, and the initial answer is `0`. No special fake block is needed.

For the path

```
3 2
1 2
2 3
```

both biconnected components are bridges. The lower bridge has branch sizes (1) and (2), contributing (2). The upper bridge has branch sizes (1) and (2), contributing another (2). The total is `4`. This shows why bridges must remain distinct from cycles.

For the triangle

```
3 3
1 2
2 3
3 1
```

the single cycle has weights (1,1,1). The ordinary line sum is `4`, and the long arc for one pair is corrected by `1`, producing `3`. This is exactly the case that a spanning-tree distance sum gets wrong.

For the square

```
4 4
1 2
2 3
3 4
4 1
```

the four branch weights are all one. The line distance sum is `10`. Only the pairs with positional difference three need correction, and each correction is (2\cdot3-4=2). The result is `8`. The pair at difference two is not corrected, because its two arcs both have length two. This strict boundary is what prevents an off-by-one error on even cycles.

For the second sample, articulation vertices belong to multiple blocks. Vertex `3`, for example, is shared by both triangles. Its subtree size includes vertices `3`, `4`, and `6` when the first triangle is processed. The parent-side weight of that first triangle then includes the rest of the graph. This is exactly why the block-cut-tree viewpoint is useful: articulation vertices are shared structurally, but every endpoint pair is still assigned to the correct block regions without double counting.
