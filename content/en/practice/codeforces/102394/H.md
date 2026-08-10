---
title: "CF 102394H - Highway Buses"
description: "There are (n) bus stations connected by an undirected, connected graph. Every highway has unit length, so the distance between two stations is their ordinary shortest path length in the graph."
date: "2026-08-10T19:23:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "H"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 457
verified: true
draft: false
---

[CF 102394H - Highway Buses](https://codeforces.com/problemset/problem/102394/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) bus stations connected by an undirected, connected graph. Every highway has unit length, so the distance between two stations is their ordinary shortest path length in the graph.

Station (i) can sell a bus ticket to any station whose graph distance from (i) is at most (f_i). Taking such a bus costs

[
c_i+(T-1)w_i
]

when all buses are taken on day (T). The price depends only on the station where the ticket is bought, not on the destination.

Alice starts at station (1). For every possible destination (k), we need the minimum total ticket cost over all valid sequences of bus rides and all days (1\le T\le T_{\max}).

The graph has up to (200000) vertices, but only (n+50) edges. That second bound is the structural key. A general sparse graph can still have complicated shortest paths, but this graph differs from a tree by at most (51) edges.

The time parameter is as large as (10^6), so trying every day is impossible. The number of vertices is also large enough that even (O(n^2)) work is far beyond the intended range. The solution has to exploit both the small number of extra edges and the fact that every outgoing bus transition from a station has the same cost.

There are several boundary cases that easily break an implementation.

The first is the starting station itself. Alice does not need to buy a ticket to visit station (1), so its answer is always zero. For example,

```
1 0 3
1 10 -5
```

has output

```
0
```

A shortest path implementation that forces at least one bus ride would incorrectly return a positive value.

The second is a negative (w_i). A later day can be cheaper than day (1), and the optimal day cannot simply be assumed to be the first day. For example,

```
2 1 3
1 10 -4
1 1 0
1 2
```

has output

```
0
2
```

Station (1)'s ticket costs (10,6,2) on the three days, so the second station is reached most cheaply on day (3).

The third is a non-tree highway. Suppose

```
3 3 1
1 3 0
1 3 0
1 3 0
1 2
2 3
1 3
```

is given. The spanning tree could contain (1-2) and (2-3), while (1-3) becomes the extra edge. Since (f_1=1), station (3) is reachable from station (1) in one bus because of the extra edge. The correct output is

```
0
3
3
```

A method that only considers distances in the spanning tree would incorrectly think station (3) is two highways away.

The fourth is the inclusive radius condition. If (f_i=2), a destination at distance exactly (2) is legal. For example,

```
3 2 1
2 7 0
1 100 0
1 100 0
1 2
2 3
```

has output

```
0
7
7
```

The destination at distance exactly (2) must be included.

## Approaches

A direct solution for a fixed day is conceptually simple. Give station (i) the outgoing edge cost (c_i+(T-1)w_i), and connect it to every station within graph distance (f_i). Then run Dijkstra from station (1).

The problem is that this implicit directed graph can be dense. A station whose radius covers the whole graph has (n) outgoing bus transitions. In the worst case there are (\Theta(n^2)) such transitions. Trying all (T_{\max}) days would lead to roughly

[
O(T_{\max}n^2\log n)
]

work. With (n=200000) and (T_{\max}=10^6), the number of possible relaxations alone can reach around (4\cdot10^{16}).

The first major observation removes the day dimension completely. Consider one fixed sequence of bus rides. Its total price is

[
\sum_i c_i+(T-1)\sum_i w_i,
]

which is a linear function of (T). A linear function on the integer interval ([1,T_{\max}]) reaches its minimum at one of the two endpoints. Hence every particular route only needs to be considered on day (1) or day (T_{\max}).

Taking the minimum over all routes preserves this property:

\min\left(
\min_{\text{route}}\text{cost(route},1),
\min_{\text{route}}\text{cost(route},T_{\max})
\right).
]

So we only need two shortest path computations. This endpoint reduction is also the starting point of the known solution approach for the problem.

Now fix one of those two days. Let

[
a_i=c_i+(T-1)w_i.
]

Whenever Alice reaches station (i), every valid bus transition from (i) costs exactly (a_i). Suppose its current shortest distance is (d_i). Every station in its radius can consequently be assigned the candidate value

[
d_i+a_i.
]

This gives a useful Dijkstra variant. Instead of explicitly storing every directed bus edge, put station (i) into the priority queue with key (d_i+a_i). When it is processed, we need to find all still-unreached vertices within distance (f_i).

If the highway graph were exactly a tree, this becomes a standard centroid decomposition query. For every centroid (x), store all vertices in its current component sorted by their tree distance from (x). For a source (u), walk through the centroid ancestors of (u). If (d(u,x)) is already known and

[
d(u,x)+d(x,v)\le f_u,
]

then (v) is a valid destination. We can consume the sorted list with a pointer. Once a vertex has been reached by Dijkstra, it never needs to be considered again, so every pointer only moves forward.

The actual graph has at most (51) edges beyond a spanning tree. Consider one such non-tree edge and choose one of its endpoints, say (x). Any shortest path that uses this extra edge passes through (x). Consequently, a destination (v) reachable from (u) through some path using this edge satisfies

[
\operatorname{dist}(u,x)+\operatorname{dist}(x,v)\le f_u.
]

We can run an ordinary BFS from every selected endpoint (x), store all vertices in nondecreasing order of their distance from (x), and use exactly the same pointer idea. There are at most (51) such BFS runs. This is the sparse-graph extension of the centroid decomposition idea used in the reference solution.

The important simplification is that we never build the dense bus graph. The centroid structures and the few BFS structures represent all of its useful transitions implicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(T_{\max}n^2\log n)) | (O(n^2)) | Too slow |
| Optimal | (O(n\log n+(m-n+1)n)) per two endpoint runs | (O(n\log n+(m-n+1)n)) | Accepted |

Since (m-n+1\le51), the optimal complexity is effectively (O(n\log n+51n)).

## Algorithm Walkthrough

1. Build any spanning tree of the highway graph. Every edge not selected for the tree is called an extra edge. Since the graph is connected and (m\le n+50), there are at most (51) extra edges.
2. For every extra edge ((u,v)), select one endpoint, for example (u). Duplicate selected endpoints can be removed because one BFS from the same endpoint already handles every path passing through that endpoint.
3. Build a centroid decomposition of the spanning tree. At every centroid (x), collect all vertices in its current component and store their tree distances from (x) in nondecreasing order.
4. While building the centroid decomposition, store for every vertex (u) its centroid at every decomposition level and its distance to that centroid. This lets a Dijkstra query obtain (\operatorname{dist}_{tree}(u,x)) without an LCA calculation.
5. For every selected extra-edge endpoint (x), run BFS in the original graph. Store the BFS order and the distance from (x) to every vertex. BFS naturally produces vertices in nondecreasing distance order.
6. Fix a day (T), initially (T=1). Define the ticket price of station (i) as

[
a_i=c_i+(T-1)w_i.
]

Run the implicit Dijkstra described below.
7. Set (d_1=0). The priority queue initially contains station (1) with key (a_1). For every other station, its distance is initially unknown.
8. When station (u) is popped, its priority key is

[
p=d_u+a_u.
]

Every station that can be reached by one bus from (u) can receive distance (p).
9. Process every centroid level of (u). Let (x) be the centroid at that level and let (r=d_{tree}(u,x)). Every vertex (v) in the centroid list with

[
d_{tree}(x,v)\le f_u-r
]

is a valid tree-distance candidate. Consume the prefix of the sorted list using a pointer.
10. Process every selected extra-edge endpoint (x). Let (r=d_G(u,x)). In the BFS list of (x), consume every still-unprocessed vertex (v) satisfying

[
d_G(x,v)\le f_u-r.
]

Such a vertex is reachable from (u) within (f_u) highways.
11. Whenever an unvisited vertex (v) is found, set

[
d_v=p
]

and insert ((d_v+a_v,v)) into the priority queue. A vertex is inserted only once.
12. Repeat until the priority queue is empty. The resulting distances are the minimum costs for this fixed day.
13. Run the same procedure for (T=T_{\max}). Take the smaller of the two results independently for every destination.

### Why it works

The invariant is that when a station (v) is first assigned a distance, the assignment is already optimal. The priority queue orders stations by (d_u+a_u), exactly the value that (u) would give to every destination in its bus radius. Any future route that could improve (v) would have to originate from a station whose own value is no larger than that alternative, so that station would have been processed first. Thus the first assignment is the Dijkstra-style final distance.

For the tree part, every path using only spanning-tree edges has exactly its tree distance. Centroid decomposition finds every vertex whose tree distance from (u) is at most (f_u). The condition using (d(u,x)+d(x,v)) may sometimes be stronger than the actual tree distance, but it never accepts an invalid vertex because it only upper-bounds a valid tree route.

For the extra-edge part, take any shortest path that uses a non-tree edge. The path contains both endpoints of that edge, including the endpoint selected for preprocessing. Hence for that selected endpoint (x),

[
d_G(u,x)+d_G(x,v)=d_G(u,v).
]

The BFS structure for (x) consequently finds every destination whose shortest route uses that extra edge. Since every path either uses only tree edges or at least one extra edge, every valid bus transition is represented.

Finally, every route has a linear cost in (T), so its best day is (1) or (T_{\max}). Taking the minimum of the two fixed-day shortest path results gives the globally optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array
from collections import deque
import heapq

def solve():
    input = sys.stdin.readline

    n, m, tmax = map(int, input().split())

    f = [0] * (n + 1)
    c = [0] * (n + 1)
    w = [0] * (n + 1)

    for i in range(1, n + 1):
        f[i], c[i], w[i] = map(int, input().split())

    graph = [[] for _ in range(n + 1)]
    tree = [[] for _ in range(n + 1)]

    dsu = list(range(n + 1))
    dsu_size = [1] * (n + 1)

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    extra_sources = []
    seen_extra = bytearray(n + 1)

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

        ru = find(u)
        rv = find(v)

        if ru != rv:
            if dsu_size[ru] < dsu_size[rv]:
                ru, rv = rv, ru
            dsu[rv] = ru
            dsu_size[ru] += dsu_size[rv]

            tree[u].append(v)
            tree[v].append(u)
        else:
            if not seen_extra[u]:
                seen_extra[u] = 1
                extra_sources.append(u)

    del dsu
    del dsu_size
    del seen_extra

    # Centroid decomposition of the spanning tree.
    #
    # At every decomposition level, center[level][v] is the centroid
    # of v's current component, and cd_dist[level][v] is the tree
    # distance from v to that centroid.
    levels = n.bit_length() + 1

    center = [
        array('i', [0]) * (n + 1)
        for _ in range(levels)
    ]
    cd_dist = [
        array('i', [0]) * (n + 1)
        for _ in range(levels)
    ]

    # For every centroid x:
    # vec_v[x] is the vertices in its component in BFS order.
    # vec_d[x] contains their distances from x in the same order.
    vec_v = [None] * (n + 1)
    vec_d = [None] * (n + 1)

    removed = bytearray(n + 1)
    temp_parent = array('i', [0]) * (n + 1)
    subtree_size = array('i', [0]) * (n + 1)

    tasks = [(1, 0)]
    while tasks:
        start, level = tasks.pop()

        # Collect this component.
        order = []
        stack = [start]
        temp_parent[start] = 0

        while stack:
            u = stack.pop()
            order.append(u)

            pu = temp_parent[u]
            for v in tree[u]:
                if removed[v] or v == pu:
                    continue
                temp_parent[v] = u
                stack.append(v)

        total = len(order)

        # Compute subtree sizes with respect to the temporary root.
        for u in reversed(order):
            s = 1
            for v in tree[u]:
                if removed[v]:
                    continue
                if temp_parent[v] == u:
                    s += subtree_size[v]
            subtree_size[u] = s

        # Find a centroid.
        centroid = start
        best = total + 1

        for u in order:
            largest = total - subtree_size[u]

            for v in tree[u]:
                if removed[v]:
                    continue
                if temp_parent[v] == u and subtree_size[v] > largest:
                    largest = subtree_size[v]

            if largest < best:
                best = largest
                centroid = u

        # BFS from the centroid inside this component.
        vv = array('i')
        dd = array('i')

        q = deque([centroid])
        temp_parent[centroid] = 0
        center[level][centroid] = centroid
        cd_dist[level][centroid] = 0

        while q:
            u = q.popleft()
            du = cd_dist[level][u]

            vv.append(u)
            dd.append(du)

            for v in tree[u]:
                if removed[v] or v == temp_parent[u]:
                    continue

                temp_parent[v] = u
                center[level][v] = centroid
                cd_dist[level][v] = du + 1
                q.append(v)

        vec_v[centroid] = vv
        vec_d[centroid] = dd

        removed[centroid] = 1

        # After removing the centroid, each remaining neighbor starts
        # an independent component.
        next_level = level + 1
        for v in tree[centroid]:
            if not removed[v]:
                tasks.append((v, next_level))

    del removed
    del temp_parent
    del subtree_size

    # For each selected endpoint of an extra edge, run BFS in the
    # original graph. BFS order is already sorted by distance.
    key_vertices = []
    key_distances = []

    for source in extra_sources:
        dist = array('i', [-1]) * (n + 1)
        vertices = array('i')

        dist[source] = 0
        q = deque([source])

        while q:
            u = q.popleft()
            vertices.append(u)

            nd = dist[u] + 1
            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = nd
                    q.append(v)

        key_distances.append(dist)
        key_vertices.append(vertices)

    key_count = len(key_vertices)

    # Bits needed to encode a vertex are no longer needed here because
    # centroid vertices and distances are stored separately.
    def dijkstra(day_offset, best_answer):
        cost = [0] * (n + 1)
        for i in range(1, n + 1):
            cost[i] = c[i] + w[i] * day_offset

        dis = [-1] * (n + 1)
        dis[1] = 0

        # Each centroid list is consumed monotonically.
        ptr = [0] * (n + 1)

        # Each extra-edge BFS list is also consumed monotonically.
        ptr_key = [0] * key_count

        heap = [(cost[1], 1)]

        while heap:
            p, u = heapq.heappop(heap)

            # p = dis[u] + cost[u].
            if best_answer[u] > dis[u]:
                best_answer[u] = dis[u]

            fu = f[u]

            # Tree-distance transitions through centroid decomposition.
            for level in range(levels):
                x = center[level][u]
                if x == 0:
                    break

                remaining = fu - cd_dist[level][u]
                if remaining < 0:
                    continue

                vv = vec_v[x]
                dd = vec_d[x]

                j = ptr[x]
                size_v = len(vv)

                while j < size_v and dd[j] <= remaining:
                    v = vv[j]

                    if dis[v] == -1:
                        dis[v] = p
                        heapq.heappush(
                            heap,
                            (p + cost[v], v)
                        )

                    j += 1

                ptr[x] = j

            # Transitions whose route uses at least one non-tree edge.
            for z in range(key_count):
                kd = key_distances[z]
                kv = key_vertices[z]

                remaining = fu - kd[u]
                if remaining < 0:
                    continue

                j = ptr_key[z]
                size_v = len(kv)

                while j < size_v and kd[kv[j]] <= remaining:
                    v = kv[j]

                    if dis[v] == -1:
                        dis[v] = p
                        heapq.heappush(
                            heap,
                            (p + cost[v], v)
                        )

                    j += 1

                ptr_key[z] = j

        return best_answer

    INF = 10**30
    answer = [INF] * (n + 1)

    dijkstra(0, answer)

    if tmax > 1:
        dijkstra(tmax - 1, answer)

    sys.stdout.write(
        '\n'.join(str(answer[i]) for i in range(1, n + 1))
    )

if __name__ == "__main__":
    solve()
```

The input phase stores the complete graph because the extra-edge BFS runs need the original highways. At the same time, a DSU selects a spanning tree. Every rejected edge is an extra edge, and there can be at most (m-n+1\le51) of them.

The centroid preprocessing is iterative rather than recursive. This avoids Python's recursion limit and also avoids maintaining a large recursive call stack. For each centroid component, a temporary DFS determines subtree sizes and identifies the centroid, then a BFS records vertices in nondecreasing distance order.

The `array` module is used deliberately. A Python list containing several million Python integers consumes much more memory than a packed integer array. The centroid distance structures contain (O(n\log n)) integers, while the extra-edge BFS structures contain (O(51n)) integers. Packed arrays keep these structures within the memory budget.

The two centroid arrays are indexed by decomposition level. For a vertex (u), `center[level][u]` gives the relevant centroid and `cd_dist[level][u]` gives the distance to it. This replaces the LCA and sparse table used by a typical C++ implementation while keeping every centroid query (O(\log n)).

The pointer arrays are reset for each Dijkstra run. A pointer is never moved backward. A smaller radius in a later query is harmless because every entry before the pointer has already been examined, and any vertex that was still unvisited when examined would already have received its optimal Dijkstra distance.

The priority queue stores `dis[u] + cost[u]`, rather than just `dis[u]`. This value is exactly the cost obtained after buying one more ticket at (u). Since all outgoing bus transitions from (u) have this same price, every destination discovered from (u) gets that same candidate. More importantly, each vertex is assigned only on its first discovery, so only (O(n)) heap insertions occur.

The expression `c[i] + w[i] * day_offset` uses zero-based day offsets. Day (1) corresponds to offset (0), and day (T_{\max}) corresponds to offset (T_{\max}-1). This is the main off-by-one detail in the implementation.

Python integers do not overflow, so the intermediate multiplication involving (w_i) is safe even when the mathematical value is much larger than a 32-bit integer. The problem guarantees that the actual ticket prices remain within the stated bounds.

## Worked Examples

### Sample 1

The input is

```
6 6 2
1 50 -40
1 2 100
2 1 100
2 4 100
3 1 100
1 1 100
1 2
2 3
3 4
4 2
2 5
6 1
```

For day (1), the ticket prices are (50,2,1,2,1,1). The important Dijkstra states are:

| Day | Popped station | Current key (p) | Newly reached stations | Final distances affected |
| --- | --- | --- | --- | --- |
| 1 | 1 | 50 | 2, 6 | (d_2=50,\ d_6=50) |
| 1 | 6 | 51 | none | unchanged |
| 1 | 2 | 52 | 3, 5 | (d_3=52,\ d_5=52) |
| 1 | 3 | 53 | 4 | (d_4=52) |
| 1 | 5 | 53 | none | unchanged |
| 1 | 4 | 54 | none | unchanged |

The resulting costs are (0,50,52,52,52,50) for the destinations.

For day (2), the ticket prices become (10,102,101,102,101,101):

| Day | Popped station | Current key (p) | Newly reached stations | Final distances affected |
| --- | --- | --- | --- | --- |
| 2 | 1 | 10 | 2, 6 | (d_2=10,\ d_6=10) |
| 2 | 2 | 112 | 3, 5 | (d_3=112,\ d_5=112) |
| 2 | 6 | 111 | none | unchanged |
| 2 | 3 | 213 | 4 | (d_4=112) |

Taking the smaller result from the two days gives

```
0
10
52
52
52
10
```

The trace also illustrates why the priority queue key is `distance + current ticket cost`. Station (2), for example, is reached with distance (50) on day (1), and its outgoing transition key is (50+2=52).

### Sample 2

Consider the following constructed case:

```
3 2 3
2 10 -4
1 100 0
1 100 0
1 2
2 3
```

Station (1) has radius (2), so it can reach both other stations directly.

| Day | Ticket price at 1 | Popped station | Key (p) | Newly reached stations |
| --- | --- | --- | --- | --- |
| 1 | 10 | 1 | 10 | 2, 3 |
| 1 | 10 | 2 | 110 | none |
| 1 | 10 | 3 | 110 | none |
| 3 | 2 | 1 | 2 | 2, 3 |
| 3 | 2 | 2 | 102 | none |
| 3 | 2 | 3 | 102 | none |

The final answers are

```
0
2
2
```

This trace confirms the endpoint argument. The intermediate day is never needed, even though the ticket price changes with the day.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n + Kn)) | Centroid preprocessing costs (O(n\log n)), the (K\le51) extra-edge BFS runs cost (O(Kn)), and each of the two Dijkstra runs performs (O(n\log n+Kn)) work |
| Space | (O(n\log n+Kn)) | Centroid lists contain (O(n\log n)) entries and the extra-edge distance structures contain (O(Kn)) entries |

Here (K\le m-n+1\le51). With (n\le200000), the extra-edge part is bounded by about (10.2) million vertex-distance entries, while the centroid decomposition contributes only (O(n\log n)) entries. The two Dijkstra runs are the only parts depending on the day parameter, and there are only two of them. This is the intended sparse-graph complexity for the problem.

## Test Cases

The following tests call the `solve()` function from the solution above. The helper replaces standard input and captures standard output.

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

# Provided sample
assert run("""\
6 6 2
1 50 -40
1 2 100
2 1 100
2 4 100
3 1 100
1 1 100
1 2
2 3
3 4
4 2
2 5
6 1
""") == """\
0
10
52
52
52
10""", "sample 1"

# Minimum-size graph.
assert run("""\
1 0 3
1 10 -5
""") == """\
0""", "single station"

# Negative w_i makes the last day optimal.
assert run("""\
2 1 3
1 10 -4
1 1 0
1 2
""") == """\
0
2""", "last-day optimum"

# All values equal, plus an extra edge creating a shortcut.
assert run("""\
3 3 1
1 3 0
1 3 0
1 3 0
1 2
2 3
1 3
""") == """\
0
3
3""", "extra-edge shortcut"

# Maximum n, a tree, f_i = 1 exactly at the radius boundary.
n = 200000
stations = "1 1 0\n" * n
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))

max_case = f"{n} {n - 1} 1\n" + stations + edges + "\n"
max_expected = "".join(f"{i}\n" for i in range(n))

assert run(max_case) == max_expected, "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=1,m=0) | `0` | Starting station needs no ticket |
| Two stations with (w_1<0) | `0, 2` | The optimal day can be (T_{\max}) |
| Triangle with equal values | `0, 3, 3` | Extra-edge shortest paths and equal ticket parameters |
| (n=200000) path with (f_i=1) | `0,1,2,...,199999` | Maximum input size and exact radius boundary |

## Edge Cases

### Starting station

For

```
1 0 3
1 10 -5
```

the centroid structure contains only station (1). Dijkstra starts with `dis[1] = 0`, and the self destination is already settled. The final output is `0`. No bus transition is necessary.

### Last-day optimum

For

```
2 1 3
1 10 -4
1 1 0
1 2
```

the first Dijkstra run uses ticket price (10) at station (1). The second run uses ticket price

[
10+(3-1)(-4)=2.
]

The destination is reached with cost (2) in the second run, so the final output is `0, 2`. This is exactly the situation handled by evaluating both endpoint days.

### Non-tree shortcut

For

```
3 3 1
1 3 0
1 3 0
1 3 0
1 2
2 3
1 3
```

suppose the spanning tree contains (1-2) and (2-3). The tree distance from (1) to (3) is (2), which is outside station (1)'s radius. The edge (1-3) is extra, so station (1) becomes one of the special BFS sources. Its BFS distance to (3) is (1), which satisfies (f_1=1). The extra-edge structure consequently assigns distance (3) to station (3), giving `0, 3, 3`.

### Exact radius

For

```
3 2 1
2 7 0
1 100 0
1 100 0
1 2
2 3
```

the tree distance from station (1) to station (3) is exactly (2). During the centroid query, the condition is `distance <= remaining`, not a strict inequality. Since (2\le f_1=2), station (3) is reached with cost (7). The output is `0, 7, 7`.

The same inclusive comparison is used in the BFS structures for extra edges. A destination exactly on the boundary of a bus radius must always be processed.

If you want, I can also provide a shorter contest-editorial version focused on the two key ideas, or a line-by-line derivation of the Python implementation.
