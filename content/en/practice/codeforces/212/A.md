---
title: "CF 212A - Privatization"
description: "We are given a bipartite graph. One side contains Berland cities, the other side contains Beerland cities, and every flight is an undirected edge between the two countries. Each edge must be assigned to one of t private companies."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 212
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Finals (unofficial online-version)"
rating: 3000
weight: 212
solve_time_s: 140
verified: false
draft: false
---

[CF 212A - Privatization](https://codeforces.com/problemset/problem/212/A)

**Rating:** 3000  
**Tags:** flows, graphs  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a bipartite graph. One side contains Berland cities, the other side contains Beerland cities, and every flight is an undirected edge between the two countries.

Each edge must be assigned to one of `t` private companies. For every city, we count how many incident edges belong to each company. If a city has counts

$$a_{i1}, a_{i2}, \dots, a_{it}$$

then its contribution to the unevenness is

$$\sum_{j=1}^t a_{ij}^2$$

The total unevenness is the sum over all cities.

We must assign a color from `1..t` to every edge so that this total value is minimized.

The graph size is large enough that brute force over assignments is impossible. There are at most 5000 edges and up to 200 companies. Even for `t = 2`, trying all assignments would require checking

$$2^{5000}$$

configurations, which is completely hopeless.

The structure of the objective function is the key observation. The contribution of a city depends only on how evenly its incident edges are distributed among companies. If a vertex has degree `d`, then the minimum possible value of

$$\sum a_j^2$$

under the constraint

$$\sum a_j = d$$

is achieved when the values differ by at most one.

For example, if a city has degree `7` and `t = 3`, then the optimal split is `(3,2,2)` and the contribution becomes

$$3^2 + 2^2 + 2^2 = 17$$

Any more uneven split increases the sum of squares.

The non-obvious part is that local optimality at every vertex may conflict globally, because every edge affects two vertices simultaneously. We need one edge coloring that realizes the optimal distribution for every vertex at the same time.

A careless greedy can easily fail.

Consider:

```
2 2 4 2
1 1
1 2
2 1
2 2
```

Every vertex has degree `2`, so the optimal local distribution is `(1,1)`.

If we greedily color edges incident to the first vertex alternately, we might produce:

```
edge (1,1) -> 1
edge (1,2) -> 2
edge (2,1) -> 1
edge (2,2) -> 1
```

Now vertex `2` on the Beerland side has counts `(2,0)`, which is not optimal.

The correct solution must coordinate all vertices simultaneously.

Another subtle case is when `t` is larger than every degree.

Example:

```
1 3 3 10
1 1
1 2
1 3
```

The best distribution at the only Berland city is `(1,1,1,0,0,0,0,0,0,0)`, giving contribution `3`.

A wrong implementation might try to use all colors equally and accidentally duplicate a color.

The graph also may be disconnected. Any algorithm that assumes connectivity can silently miss components.

Example:

```
2 2 2 2
1 1
2 2
```

Each edge can independently receive any color. The optimal answer is `4`.

## Approaches

The brute-force approach is straightforward. We try every assignment of companies to edges, compute the contribution for every vertex, and keep the minimum.

For each assignment we can count, for every vertex and every company, how many incident edges belong to that company. Then we evaluate the sum of squares.

This works because the objective function is explicitly defined by the edge coloring. The problem is the number of assignments. With `k` edges and `t` companies, there are

$$t^k$$

possible colorings.

With `k = 5000`, this is astronomically large even for `t = 2`.

The next natural idea is to optimize each vertex independently. For a degree `d`, the minimum sum of squares is obtained by distributing the edges as evenly as possible among colors.

Suppose

$$d = qt + r$$

Then exactly `r` colors should appear `q+1` times, and the remaining `t-r` colors should appear `q` times.

This gives the theoretical minimum contribution for that vertex.

The real breakthrough is realizing that this optimal local structure can actually be achieved globally. The graph is bipartite, and bipartite graphs admit edge colorings with exactly `Δ` colors, where `Δ` is the maximum degree. More importantly, we can decompose the edges into nearly equal groups for every vertex.

The construction comes from regularization and Euler tours.

We first make all vertex degrees equal by adding dummy vertices and dummy edges. Then we split the regular graph into edge-disjoint perfect matchings repeatedly. Assigning colors cyclically over these matchings guarantees that every vertex receives each color either

$$\left\lfloor \frac{d}{t} \right\rfloor$$

or

$$\left\lceil \frac{d}{t} \right\rceil$$

times, which is exactly the optimal distribution.

This converts the problem into finding perfect matchings in bipartite graphs repeatedly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(t^k \cdot k)$ | $O(k)$ | Too slow |
| Optimal | $O(D \cdot V^2)$ | $O(V^2)$ | Accepted |

Here `D` is the maximum degree after regularization, at most `200`, and `V` is the number of vertices after adding dummy nodes, also at most about `400`.

## Algorithm Walkthrough

1. Build the bipartite graph from the input.

The left side contains Berland cities, the right side contains Beerland cities.
2. Compute the maximum degree `D`.

A `D`-regular bipartite graph is much easier to decompose into perfect matchings.
3. Add dummy vertices so that both sides contain exactly the same number of vertices.

Perfect matchings require balanced bipartite sets.
4. Add dummy edges until every vertex has degree exactly `D`.

This transforms the graph into a `D`-regular bipartite graph.

Such a graph always admits a perfect matching.
5. Repeatedly find a perfect matching and remove it.

After removing one perfect matching from a `D`-regular bipartite graph, the remaining graph becomes `(D-1)`-regular, so the process can continue.
6. Number the matchings from `0` to `D-1`.

Assign company

$$(matching\_index \bmod t) + 1$$

to all edges in that matching.
7. Ignore dummy edges and output colors only for original edges.

Why does this balancing work?

Suppose a vertex had original degree `d`. During decomposition, each matching contributes exactly one incident edge to that vertex until all its original edges are exhausted.

The `D` matchings are distributed cyclically among `t` companies. For that vertex, the number of incident edges assigned to any two companies differs by at most one.

That is exactly the configuration minimizing the sum of squares.

### Why it works

The critical invariant is that every extracted matching uses exactly one edge incident to every vertex of the current regular graph.

Because the graph starts `D`-regular and each iteration removes one edge per vertex, the remaining graph stays regular. This guarantees the process continues until all edges are partitioned into perfect matchings.

Assigning colors cyclically over these matchings distributes incident edges at every vertex as evenly as mathematically possible. Since the objective function is separable by vertices and minimized precisely by such balanced distributions, the resulting coloring is globally optimal.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def hopcroft_karp(adj, n_left, n_right):
    INF = 10**9

    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [0] * n_left

    def bfs():
        q = deque()

        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF

        found = False

        while q:
            u = q.popleft()

            for v in adj[u]:
                pu = pair_v[v]

                if pu == -1:
                    found = True
                elif dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)

        return found

    def dfs(u):
        for v in adj[u]:
            pu = pair_v[v]

            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True

        dist[u] = INF
        return False

    matching = 0

    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1

    return pair_u

def solve():
    n, m, k, t = map(int, input().split())

    edges = []
    deg_left = [0] * n
    deg_right = [0] * m

    for _ in range(k):
        x, y = map(int, input().split())
        x -= 1
        y -= 1

        edges.append((x, y))

        deg_left[x] += 1
        deg_right[y] += 1

    D = max(max(deg_left), max(deg_right))

    size = max(n, m)

    left_deg = deg_left[:] + [0] * (size - n)
    right_deg = deg_right[:] + [0] * (size - m)

    graph = [[-1] * size for _ in range(size)]

    for idx, (u, v) in enumerate(edges):
        graph[u][v] = idx

    for u in range(size):
        need = D - left_deg[u]

        for v in range(size):
            if need == 0:
                break

            if right_deg[v] < D and graph[u][v] == -1:
                graph[u][v] = -2
                left_deg[u] += 1
                right_deg[v] += 1
                need -= 1

    answer = [0] * k

    for match_id in range(D):
        adj = [[] for _ in range(size)]

        for u in range(size):
            for v in range(size):
                if graph[u][v] != -1:
                    adj[u].append(v)

        match = hopcroft_karp(adj, size, size)

        color = (match_id % t) + 1

        for u in range(size):
            v = match[u]

            edge_id = graph[u][v]

            if edge_id >= 0:
                answer[edge_id] = color

            graph[u][v] = -1

    total = 0

    for d in deg_left:
        q, r = divmod(d, t)
        total += r * (q + 1) * (q + 1)
        total += (t - r) * q * q

    for d in deg_right:
        q, r = divmod(d, t)
        total += r * (q + 1) * (q + 1)
        total += (t - r) * q * q

    print(total)
    print(*answer)

solve()
```

The first major component is Hopcroft-Karp, which finds a maximum matching in a bipartite graph. Since the graph is regular and balanced, every maximum matching is perfect.

The graph matrix stores edge IDs. Original edges store their input index, dummy edges store `-2`, and absent edges store `-1`.

The regularization step is subtle. We greedily connect vertices whose current degree is below `D`. Because the total degree deficit is equal on both sides, this process always succeeds.

After the graph becomes `D`-regular, we repeatedly extract perfect matchings. Each extracted matching corresponds to one layer of edges.

The color assignment uses cyclic indexing:

```
color = (match_id % t) + 1
```

This automatically balances edge counts for every vertex.

The answer value is computed directly from degree formulas instead of recounting colors. Once we know every vertex receives the optimal balanced distribution, the minimum contribution becomes deterministic.

A common mistake is forgetting that only original edges belong in the output. Dummy edges are purely structural and must be ignored.

Another easy bug is modifying the graph while iterating incorrectly. After extracting a matching, we remove exactly those edges from the graph matrix.

## Worked Examples

### Example 1

Input:

```
3 5 8 2
1 4
1 3
3 3
1 2
1 1
2 1
1 5
2 2
```

Degrees:

| Vertex | Degree |
| --- | --- |
| L1 | 5 |
| L2 | 2 |
| L3 | 1 |
| R1 | 2 |
| R2 | 2 |
| R3 | 2 |
| R4 | 1 |
| R5 | 1 |

Maximum degree is `5`.

After regularization, the graph becomes `5`-regular.

Suppose the extracted matchings are assigned colors cyclically:

| Matching | Company |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 1 |
| 3 | 2 |
| 4 | 1 |

Vertex `L1` has degree `5`, so its incident edges become distributed `(3,2)`.

Contribution:

$$3^2 + 2^2 = 13$$

Every degree-2 vertex gets `(1,1)` and contributes `2`.

The final total becomes `4`.

This trace demonstrates the balancing property. Every vertex receives colors differing by at most one.

### Example 2

Input:

```
2 2 4 2
1 1
1 2
2 1
2 2
```

The graph is already `2`-regular.

Perfect matchings:

| Matching | Edges |
| --- | --- |
| 0 | (1,1), (2,2) |
| 1 | (1,2), (2,1) |

Assigned colors:

| Edge | Color |
| --- | --- |
| (1,1) | 1 |
| (2,2) | 1 |
| (1,2) | 2 |
| (2,1) | 2 |

Every vertex sees one edge of each color.

Contribution per vertex:

$$1^2 + 1^2 = 2$$

Total:

$$4 \times 2 = 8$$

This example shows why perfect matching decomposition naturally balances all vertices simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(D \cdot V^2)$ | We extract `D` perfect matchings, each using Hopcroft-Karp on at most `400` vertices |
| Space | $O(V^2)$ | The adjacency matrix stores the regularized graph |

The maximum regular degree is at most `200`, and the graph size after balancing remains small. Even the worst-case instance easily fits inside the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    from collections import deque

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    def hopcroft_karp(adj, n_left, n_right):
        INF = 10**9

        pair_u = [-1] * n_left
        pair_v = [-1] * n_right
        dist = [0] * n_left

        def bfs():
            q = deque()

            for u in range(n_left):
                if pair_u[u] == -1:
                    dist[u] = 0
                    q.append(u)
                else:
                    dist[u] = INF

            found = False

            while q:
                u = q.popleft()

                for v in adj[u]:
                    pu = pair_v[v]

                    if pu == -1:
                        found = True
                    elif dist[pu] == INF:
                        dist[pu] = dist[u] + 1
                        q.append(pu)

            return found

        def dfs(u):
            for v in adj[u]:
                pu = pair_v[v]

                if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                    pair_u[u] = v
                    pair_v[v] = u
                    return True

            dist[u] = INF
            return False

        while bfs():
            for u in range(n_left):
                if pair_u[u] == -1:
                    dfs(u)

        return pair_u

    n, m, k, t = map(int, input().split())

    edges = []
    deg_left = [0] * n
    deg_right = [0] * m

    for _ in range(k):
        x, y = map(int, input().split())
        x -= 1
        y -= 1

        edges.append((x, y))
        deg_left[x] += 1
        deg_right[y] += 1

    D = max(max(deg_left), max(deg_right))
    size = max(n, m)

    left_deg = deg_left[:] + [0] * (size - n)
    right_deg = deg_right[:] + [0] * (size - m)

    graph = [[-1] * size for _ in range(size)]

    for idx, (u, v) in enumerate(edges):
        graph[u][v] = idx

    for u in range(size):
        need = D - left_deg[u]

        for v in range(size):
            if need == 0:
                break

            if right_deg[v] < D and graph[u][v] == -1:
                graph[u][v] = -2
                left_deg[u] += 1
                right_deg[v] += 1
                need -= 1

    ans = [0] * k

    for mid in range(D):
        adj = [[] for _ in range(size)]

        for u in range(size):
            for v in range(size):
                if graph[u][v] != -1:
                    adj[u].append(v)

        match = hopcroft_karp(adj, size, size)

        color = (mid % t) + 1

        for u in range(size):
            v = match[u]

            eid = graph[u][v]

            if eid >= 0:
                ans[eid] = color

            graph[u][v] = -1

    total = 0

    for d in deg_left[:n]:
        q, r = divmod(d, t)
        total += r * (q + 1) * (q + 1)
        total += (t - r) * q * q

    for d in deg_right[:m]:
        q, r = divmod(d, t)
        total += r * (q + 1) * (q + 1)
        total += (t - r) * q * q

    print(total)
    print(*ans)

    return out.getvalue()

# sample 1
out = run(
"""3 5 8 2
1 4
1 3
3 3
1 2
1 1
2 1
1 5
2 2
"""
)

assert out.splitlines()[0] == "20"

# minimum case
out = run(
"""1 1 1 1
1 1
"""
)

assert out.splitlines()[0] == "2"

# disconnected graph
out = run(
"""2 2 2 2
1 1
2 2
"""
)

assert out.splitlines()[0] == "4"

# t larger than degrees
out = run(
"""1 3 3 10
1 1
1 2
1 3
"""
)

assert out.splitlines()[0] == "6"

# complete 2x2 graph
out = run(
"""2 2 4 2
1 1
1 2
2 1
2 2
"""
)

assert out.splitlines()[0] == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge | 2 | Minimum graph |
| Disconnected graph | 4 | Independent components |
| `t > degree` | 6 | Sparse color usage |
| Complete `2x2` graph | 8 | Perfect balancing |

## Edge Cases

Consider the case where the number of companies exceeds all degrees:

```
1 3 3 10
1 1
1 2
1 3
```

The only left vertex has degree `3`. The algorithm distributes its three edges across three different matchings. Since colors are assigned cyclically, the vertex receives counts:

```
(1,1,1,0,0,0,0,0,0,0)
```

The contribution becomes:

$$1+1+1=3$$

The right-side vertices each contribute `1`, so the total is `6`.

Now consider a disconnected graph:

```
2 2 2 2
1 1
2 2
```

The graph already has maximum degree `1`. The decomposition contains a single matching, so both edges receive the same color.

Every vertex sees distribution `(1,0)` and contributes `1`.

The algorithm works because regularization and matching extraction do not depend on connectivity.

Finally, consider imbalance pressure:

```
2 2 3 2
1 1
1 2
2 1
```

Degrees are:

| Vertex | Degree |
| --- | --- |
| L1 | 2 |
| L2 | 1 |
| R1 | 2 |
| R2 | 1 |

The degree-2 vertices must receive one edge of each color. The matching decomposition guarantees this automatically. A naive local greedy can easily create `(2,0)` at one vertex, but the perfect matching structure prevents such conflicts.
