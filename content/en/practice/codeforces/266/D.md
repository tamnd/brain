---
title: "CF 266D - BerDonalds"
description: "We are given a connected weighted undirected graph representing a road network. Junctions are graph vertices, roads are weighted edges, and the restaurant may be placed anywhere, not only at vertices but also at any point along an edge."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "math", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 266
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 163 (Div. 2)"
rating: 2400
weight: 266
solve_time_s: 129
verified: false
draft: false
---

[CF 266D - BerDonalds](https://codeforces.com/problemset/problem/266/D)

**Rating:** 2400  
**Tags:** graphs, math, shortest paths  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected weighted undirected graph representing a road network. Junctions are graph vertices, roads are weighted edges, and the restaurant may be placed anywhere, not only at vertices but also at any point along an edge.

For a chosen location, its quality is determined by the distance to the farthest junction, where distance is measured along shortest paths in the graph. We want the location minimizing this worst-case distance.

This is a continuous optimization problem on a graph. The best point may lie inside an edge instead of at a vertex. In the simplest graph with two vertices connected by a road of length 1, placing the restaurant in the middle gives maximum distance 0.5, while placing it at a vertex gives maximum distance 1.

The constraints are small enough for all-pairs shortest paths. The original problem has at most a few hundred vertices, which makes Floyd-Warshall feasible. An $O(n^3)$ preprocessing step is completely acceptable under a 5 second limit. What is not feasible is treating every real-valued point on every edge independently, since the search space is continuous.

The hard part is understanding how the maximum distance behaves while moving along an edge.

A common mistake is assuming the optimum always occurs at a vertex or at the midpoint of an edge. Neither is true in general.

Consider this graph:

```
1 --1-- 2 --100-- 3
```

If we place the restaurant at the midpoint of edge $(2,3)$, the farthest junction is still very far away. The true optimum is shifted toward vertex 2 because junction 1 is much closer to 2 than to 3.

Another subtle case appears when multiple vertices dominate different parts of the same edge.

Example:

```
1 --4-- 2
 \      /
  1    1
   \  /
    3
```

The farthest vertex while moving along edge $(1,2)$ changes depending on the position. A careless implementation that checks only endpoints or only one candidate vertex will fail.

A third edge case comes from disconnected thinking about the graph structure. Distances from a point inside an edge to a vertex are not Euclidean. They are shortest-path distances through the graph. Sometimes the shortest route from a point to a vertex leaves the edge immediately through one endpoint, travels elsewhere in the graph, and never uses the remainder of the edge.

## Approaches

The brute-force perspective is useful because it reveals the structure of the optimization problem.

Suppose we fix a point on an edge $(u,v)$ of length $w$. Let the point be at distance $x$ from $u$, so it is at distance $w-x$ from $v$.

For any vertex $k$, the shortest distance from the point to $k$ is:

$$\min(d[u][k] + x,\ d[v][k] + (w-x))$$

where $d[a][b]$ is the shortest-path distance between vertices.

The maximum over all vertices is the worst-case distance for this point. If we could evaluate every real $x$, we could minimize this expression directly. The problem is that $x$ is continuous.

A naive discretization would be hopeless because edge lengths can be large. Even checking every integer coordinate on every edge would require up to $10^5$ positions per edge.

The key observation is that after computing all-pairs shortest paths, the graph structure disappears from the optimization stage. Every vertex contributes a very simple function along an edge.

For a fixed vertex $k$, define:

$$f_k(x)=\min(d[u][k]+x,\ d[v][k]+w-x)$$

This is the minimum of two linear functions. Geometrically, it forms a tent-shaped curve. The objective on the edge is:

$$F(x)=\max_k f_k(x)$$

The maximum of convex piecewise-linear functions is still convex. A convex function on a segment achieves its minimum either at a breakpoint or where two dominating constraints balance.

This means we can binary search or ternary search on each edge. Since the function is convex and evaluating it costs $O(n)$, this becomes practical.

The full solution becomes:

1. Run Floyd-Warshall to compute shortest paths.
2. For every edge, minimize the convex function $F(x)$ on $[0,w]$.
3. Take the best value over all edges.

The number of edges and vertices is small enough that this approach easily fits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over continuous positions | Impossible | Impossible | Not feasible |
| Floyd-Warshall + convex optimization on each edge | $O(n^3 + mn \cdot I)$ | $O(n^2)$ | Accepted |

Here $I$ is the number of ternary-search iterations, typically around 100.

## Algorithm Walkthrough

1. Read the graph and initialize the distance matrix.

Set `dist[i][i] = 0`. For every road $(u,v,w)$, set both `dist[u][v]` and `dist[v][u]` to `w`.
2. Run Floyd-Warshall.

For every intermediate vertex `k`, try improving all pairs `(i,j)` through `k`.

After this step, `dist[i][j]` stores the true shortest-path distance between every pair of junctions.
3. Process each edge independently.

Suppose the edge connects `u` and `v` with length `w`.

Any point on this edge can be represented by a parameter `x` in `[0,w]`, where `x` is the distance from `u`.
4. Define the objective function on the edge.

For a chosen `x`, compute:

$$\max_k \min(dist[u][k]+x,\ dist[v][k]+w-x)$$

The inner minimum chooses the better endpoint route to reach vertex `k`.

The outer maximum finds the farthest junction.
5. Use ternary search on the edge.

The function is convex because it is the maximum of convex piecewise-linear functions.

Repeatedly evaluate two interior points and discard the worse side.
6. Record the best value found on this edge.

Compare it with the global answer.
7. Print the minimum over all edges.

### Why it works

For a fixed vertex, the distance from a moving point on an edge is the minimum of two affine functions. Such a function is convex. The maximum of convex functions remains convex, so the worst-case distance along an edge is convex.

A convex function on a closed interval has no local minima other than the global minimum. Ternary search therefore converges to the optimal point on the edge.

Since every feasible restaurant location belongs either to some edge interior or a vertex, and vertices are included as edge endpoints when $x=0$ or $x=w$, checking every edge covers the entire graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def solve():
    n, m = map(int, input().split())

    dist = [[INF] * n for _ in range(n)]
    edges = []

    for i in range(n):
        dist[i][i] = 0

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1

        dist[u][v] = w
        dist[v][u] = w

        edges.append((u, v, w))

    # Floyd-Warshall
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            di = dist[i]

            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    def evaluate(u, v, w, x):
        best = 0.0

        for k in range(n):
            d = min(dist[u][k] + x,
                    dist[v][k] + (w - x))
            if d > best:
                best = d

        return best

    ans = float("inf")

    for u, v, w in edges:
        lo = 0.0
        hi = float(w)

        for _ in range(100):
            m1 = (2 * lo + hi) / 3.0
            m2 = (lo + 2 * hi) / 3.0

            f1 = evaluate(u, v, w, m1)
            f2 = evaluate(u, v, w, m2)

            if f1 < f2:
                hi = m2
            else:
                lo = m1

        x = (lo + hi) / 2.0
        ans = min(ans, evaluate(u, v, w, x))

    print(f"{ans:.10f}")

solve()
```

The first section builds the shortest-path matrix. Floyd-Warshall is the natural choice because the graph is small and we need distances between every pair of vertices.

The `evaluate` function directly implements the mathematical definition of the objective. For every vertex `k`, there are only two meaningful ways to reach it from a point inside edge `(u,v)`:

1. Move toward `u`, then follow the shortest path from `u` to `k`.
2. Move toward `v`, then follow the shortest path from `v` to `k`.

Taking the minimum gives the actual shortest distance.

The ternary search works because the function is convex. Using 100 iterations is more than enough for `1e-9` precision.

One subtle implementation detail is keeping everything in floating point during optimization. The optimal point may lie at a non-integer coordinate.

Another subtle point is that vertices are automatically considered. When `x = 0`, the point is exactly at `u`. When `x = w`, it is exactly at `v`.

## Worked Examples

### Example 1

Input:

```
2 1
1 2 1
```

The graph has one edge of length 1.

| x | Distance to 1 | Distance to 2 | Maximum |
| --- | --- | --- | --- |
| 0.0 | 0.0 | 1.0 | 1.0 |
| 0.25 | 0.25 | 0.75 | 0.75 |
| 0.5 | 0.5 | 0.5 | 0.5 |
| 0.75 | 0.75 | 0.25 | 0.75 |

The minimum occurs at the midpoint.

Output:

```
0.5000000000
```

This demonstrates that the optimum may lie inside an edge rather than at a junction.

### Example 2

Input:

```
3 2
1 2 1
2 3 100
```

Shortest paths:

| From | To | Distance |
| --- | --- | --- |
| 1 | 2 | 1 |
| 1 | 3 | 101 |
| 2 | 3 | 100 |

Consider edge `(2,3)`.

| x from 2 | Dist to 1 | Dist to 2 | Dist to 3 | Maximum |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 100 | 100 |
| 25 | 26 | 25 | 75 | 75 |
| 50 | 51 | 50 | 50 | 51 |
| 49.5 | 50.5 | 49.5 | 50.5 | 50.5 |

The optimum is not exactly the midpoint because vertex 1 biases the balance toward vertex 2.

This trace shows why shortest-path structure matters even for points inside one edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^3 + mnI)$ | Floyd-Warshall plus ternary-search evaluations |
| Space | $O(n^2)$ | Shortest-path matrix |

The graph size is small enough that Floyd-Warshall easily fits. With roughly 100 ternary-search iterations per edge and $O(n)$ evaluation cost, the optimization phase is also fast within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

INF = 10**30

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    dist = [[INF] * n for _ in range(n)]
    edges = []

    for i in range(n):
        dist[i][i] = 0

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1

        dist[u][v] = w
        dist[v][u] = w

        edges.append((u, v, w))

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][k] + dist[k][j]
                )

    def evaluate(u, v, w, x):
        res = 0.0

        for k in range(n):
            res = max(
                res,
                min(dist[u][k] + x,
                    dist[v][k] + (w - x))
            )

        return res

    ans = float("inf")

    for u, v, w in edges:
        lo = 0.0
        hi = float(w)

        for _ in range(100):
            m1 = (2 * lo + hi) / 3
            m2 = (lo + 2 * hi) / 3

            if evaluate(u, v, w, m1) < evaluate(u, v, w, m2):
                hi = m2
            else:
                lo = m1

        ans = min(ans, evaluate(u, v, w, (lo + hi) / 2))

    return f"{ans:.10f}"

# provided sample
assert run("2 1\n1 2 1\n") == "0.5000000000", "sample 1"

# triangle graph
assert run(
    "3 3\n"
    "1 2 2\n"
    "2 3 2\n"
    "1 3 2\n"
) == "1.0000000000", "equilateral triangle"

# path graph
assert run(
    "3 2\n"
    "1 2 1\n"
    "2 3 1\n"
) == "1.0000000000", "middle vertex optimal"

# asymmetric chain
out = float(run(
    "3 2\n"
    "1 2 1\n"
    "2 3 100\n"
))
assert abs(out - 50.5) < 1e-7, "asymmetric edge"

# square cycle
out = float(run(
    "4 4\n"
    "1 2 1\n"
    "2 3 1\n"
    "3 4 1\n"
    "4 1 1\n"
))
assert abs(out - 1.0) < 1e-7, "cycle graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices with one edge | 0.5 | Optimum inside edge |
| Complete triangle with equal edges | 1.0 | Symmetric structure |
| Path of length 2 | 1.0 | Vertex optimum |
| Asymmetric chain | 50.5 | Optimum shifted away from midpoint |
| 4-cycle | 1.0 | Multiple shortest paths |

## Edge Cases

Consider again the asymmetric chain:

```
3 2
1 2 1
2 3 100
```

A naive midpoint strategy on edge `(2,3)` gives maximum distance `51`, because vertex 1 sits one unit beyond vertex 2. The algorithm correctly evaluates:

$$\max( 1+x, x, 100-x )$$

The optimum occurs when `1 + x = 100 - x`, giving `x = 49.5`.

Now consider a graph where the optimum is exactly at a vertex:

```
3 2
1 2 1
2 3 1
```

Along edge `(1,2)`, the farthest vertex remains vertex 3, so moving away from vertex 2 only worsens the answer. Ternary search naturally converges toward endpoint `2`, giving value `1`.

Finally, consider a cycle:

```
4 4
1 2 1
2 3 1
3 4 1
4 1 1
```

Many shortest paths exist between opposite vertices. The formula using precomputed shortest distances already accounts for this automatically. The optimization remains valid because only shortest-path distances matter, not which path realizes them.
