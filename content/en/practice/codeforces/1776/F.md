---
title: "CF 1776F - Train Splitting"
description: "We are given a connected undirected graph. Every edge must be assigned to a company. Suppose company c owns all edges colored c. The coloring must satisfy two conditions. The first condition says that no single company is allowed to own a connected spanning network."
date: "2026-06-09T11:46:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "F"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1700
weight: 1776
solve_time_s: 120
verified: false
draft: false
---

[CF 1776F - Train Splitting](https://codeforces.com/problemset/problem/1776/F)

**Rating:** 1700  
**Tags:** constructive algorithms, graphs, greedy  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph. Every edge must be assigned to a company.

Suppose company `c` owns all edges colored `c`. The coloring must satisfy two conditions.

The first condition says that no single company is allowed to own a connected spanning network. For every color, the graph formed only by edges of that color must be disconnected.

The second condition is much stronger. Take any two companies. If we keep all edges belonging to either of those two companies, the resulting graph must be connected.

We are free to choose the number of companies `k`, as long as `k ≥ 2`.

The graph has at most 50 vertices, and the sum of all `n` across test cases is at most 5000. These limits are tiny. The challenge is not algorithmic complexity, it is finding a construction that always works.

The most dangerous mistake is to focus only on making each color disconnected. That part is easy. The hard part is guaranteeing that every pair of colors forms a connected graph.

Consider a path `1-2-3`.

If we color edge `(1,2)` with color 1 and edge `(2,3)` with color 2, then each individual color is disconnected. However, if we introduce a third color that owns nothing useful, some pair of colors may fail to connect the graph. The pairwise connectivity requirement is global and must hold for every pair of colors.

Another easy trap appears on complete graphs.

Suppose `n = 3` and all three edges exist. If we color all edges incident to vertex 1 with color 1 and the remaining edge with color 2, then color 1 alone is connected, which violates the first condition.

The complete graph is the only situation where the main construction needs a special adjustment.

## Approaches

A brute-force mindset would try to assign colors and then verify the conditions.

For a graph with up to 1225 edges, even deciding among two colors already creates `2^m` possibilities. Checking connectivity after each assignment is easy, but the search space is astronomically large.

The key observation is that we do not need many colors.

Imagine choosing a vertex `u`. Give one color to every edge incident to `u`, and give a second color to every other edge.

If we use only two colors, then the second requirement becomes trivial. There is only one pair of colors, namely `{1,2}`, and together they contain every edge of the original graph. Since the original graph is connected, the pair is connected.

Now we only need to make sure that each individual color is disconnected.

Color 2 contains no edge touching `u`, so vertex `u` is isolated. Color 2 is automatically disconnected.

Color 1 is a star centered at `u`. This color is disconnected whenever there exists some vertex not adjacent to `u`, because that vertex has degree zero in color 1.

This immediately solves every non-complete graph. Pick a vertex whose degree is less than `n-1`.

The only remaining case is a complete graph.

In a complete graph every vertex is adjacent to everyone else, so the previous argument fails. We need one extra color.

Choose a vertex `u`.

Give one incident edge of `u` color 1.

Give all other edges incident to `u` color 2.

Give every remaining edge color 3.

Now every color is disconnected:

Color 1 contains only one edge.

Color 2 is a star missing one leaf.

Color 3 contains no edge incident to `u`.

Any pair of colors is connected:

Colors 1 and 2 contain all edges incident to `u`, which form a spanning star.

Colors 1 and 3 connect `u` through the unique color-1 edge, while color 3 contains the complete graph on the remaining vertices.

Colors 2 and 3 are symmetric.

That completely solves the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Coloring Search | O(2^m) or worse | Exponential | Too slow |
| Constructive Coloring | O(n + m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and compute the degree of every vertex.
2. Check whether some vertex `u` has degree strictly smaller than `n-1`.
3. If such a vertex exists, use `k = 2`.

Assign color 1 to every edge incident to `u`.

Assign color 2 to every other edge.

Color 2 is disconnected because `u` has no color-2 edges.

Color 1 is disconnected because at least one vertex is not adjacent to `u`, so that vertex has no color-1 edge.
4. Otherwise the graph is complete.
5. Use `k = 3`.
6. Pick any vertex, for example vertex 1.
7. Among edges incident to vertex 1, choose one edge and color it 1.
8. Color every other edge incident to vertex 1 with color 2.
9. Color all remaining edges with color 3.
10. Output the colors in the original input order.

### Why it works

For a non-complete graph, the chosen vertex `u` has at least one non-neighbor. The color-1 graph consists only of edges touching `u`, so that non-neighbor is isolated. The color-2 graph contains no edge touching `u`, so `u` itself is isolated. Both colors are disconnected.

Since there are only two colors, the union of any two colors is simply the original graph, which is connected.

For a complete graph, color 1 contains a single edge and is disconnected. Color 2 is a partial star and is disconnected because one endpoint of the color-1 edge receives no color-2 edge. Color 3 contains no edge incident to vertex 1, so vertex 1 is isolated.

For connectivity of color pairs:

`1 ∪ 2` contains every edge incident to vertex 1, forming a spanning star.

`1 ∪ 3` contains the complete graph on vertices `{2,3,...,n}` and also one edge connecting vertex 1 to that complete graph.

`2 ∪ 3` is analogous.

Hence every required condition holds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        edges = []
        deg = [0] * (n + 1)

        for _ in range(m):
            u, v = map(int, input().split())
            edges.append((u, v))
            deg[u] += 1
            deg[v] += 1

        u = -1
        for v in range(1, n + 1):
            if deg[v] < n - 1:
                u = v
                break

        if u != -1:
            print(2)

            ans = [2] * m
            for i, (a, b) in enumerate(edges):
                if a == u or b == u:
                    ans[i] = 1

            print(*ans)

        else:
            print(3)

            ans = [3] * m
            first_edge = -1

            for i, (a, b) in enumerate(edges):
                if a == 1 or b == 1:
                    first_edge = i
                    break

            ans[first_edge] = 1

            for i, (a, b) in enumerate(edges):
                if i == first_edge:
                    continue
                if a == 1 or b == 1:
                    ans[i] = 2

            print(*ans)

solve()
```

The first part computes degrees. A vertex with degree smaller than `n-1` immediately certifies that the graph is not complete.

In the non-complete case, every edge touching the chosen vertex receives color 1. All other edges remain color 2. Initializing the whole answer array with 2 and then overwriting incident edges is the simplest implementation.

In the complete-graph case, we use three colors. We locate one edge incident to vertex 1 and reserve it for color 1. Every other edge touching vertex 1 becomes color 2. The remaining edges keep color 3.

A subtle point is that we must keep the colors in the original input order. The output refers to the `i`-th input edge, so we store all edges in a list and assign colors by edge index.

## Worked Examples

### Example 1

Input graph:

```
5 9
1-2
1-3
1-4
1-5
2-3
2-4
2-5
3-4
3-5
```

Degrees:

| Vertex | Degree |
| --- | --- |
| 1 | 4 |
| 2 | 4 |
| 3 | 4 |
| 4 | 2 |
| 5 | 2 |

Since vertex 4 has degree `< n-1 = 4`, we use the two-color construction.

| Edge | Incident to 4? | Color |
| --- | --- | --- |
| 1-2 | No | 2 |
| 1-3 | No | 2 |
| 1-4 | Yes | 1 |
| 1-5 | No | 2 |
| 2-3 | No | 2 |
| 2-4 | Yes | 1 |
| 2-5 | No | 2 |
| 3-4 | Yes | 1 |
| 3-5 | No | 2 |

Color 1 is disconnected because vertex 5 is not adjacent to 4.

Color 2 is disconnected because vertex 4 has no color-2 edge.

### Example 2

Input:

```
3 3
1-2
1-3
2-3
```

This is a complete graph.

| Edge | Color |
| --- | --- |
| 1-2 | 1 |
| 1-3 | 2 |
| 2-3 | 3 |

Checking the colors:

| Color | Edges |
| --- | --- |
| 1 | {1-2} |
| 2 | {1-3} |
| 3 | {2-3} |

Each color alone is disconnected.

Any pair of colors forms a connected graph on all three vertices.

This example demonstrates why the complete graph requires three colors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One degree pass and one coloring pass |
| Space | O(m) | Store edges and color assignments |

With `n ≤ 50` and total `n ≤ 5000`, this complexity is far below the limits. Even the densest graph has only 1225 edges, so the solution runs comfortably within the time limit.

## Test Cases

```python
# These tests validate the construction properties rather than
# a specific coloring, since many valid outputs exist.

from collections import deque

def check(n, edges, k, colors):
    assert 2 <= k

    def connected(allowed):
        g = [[] for _ in range(n)]
        for (u, v), c in zip(edges, colors):
            if c in allowed:
                u -= 1
                v -= 1
                g[u].append(v)
                g[v].append(u)

        q = deque([0])
        vis = [False] * n
        vis[0] = True

        while q:
            x = q.popleft()
            for y in g[x]:
                if not vis[y]:
                    vis[y] = True
                    q.append(y)

        return all(vis)

    for c in range(1, k + 1):
        assert not connected({c})

    for a in range(1, k + 1):
        for b in range(a + 1, k + 1):
            assert connected({a, b})

# sample 1 graph
n = 5
edges = [
    (1,2),(1,3),(1,4),(1,5),
    (2,3),(2,4),(2,5),(3,4),(3,5)
]

# one valid coloring
check(n, edges, 2, [2,2,1,2,2,1,2,1,2])

# sample 2 graph
n = 3
edges = [(1,2),(3,1),(2,3)]
check(n, edges, 3, [1,2,3])

# minimum connected graph
n = 3
edges = [(1,2),(2,3)]
check(n, edges, 2, [1,2])

# complete graph K4
n = 4
edges = [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
check(n, edges, 3, [1,2,2,3,3,3])

# non-complete graph with one missing edge
n = 4
edges = [(1,2),(1,3),(2,3),(2,4),(3,4)]
check(n, edges, 2, [2,2,2,1,1])

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle | Any valid 3-color construction | Complete graph handling |
| Path of length 2 | Any valid 2-color construction | Smallest connected graph |
| K4 | Any valid 3-color construction | General complete graph case |
| One missing edge from complete graph | Any valid 2-color construction | Degree `< n-1` branch |

## Edge Cases

Consider the complete graph on three vertices:

```
1
3 3
1 2
1 3
2 3
```

Every vertex has degree `n-1 = 2`, so the graph is complete. The algorithm enters the three-color branch.

One edge incident to vertex 1 gets color 1, the other gets color 2, and the remaining edge gets color 3.

If we incorrectly used the two-color construction here, color 1 would form a connected spanning star and violate the requirements. The special complete-graph branch avoids that problem.

Now consider:

```
1
4 5
1 2
1 3
2 3
2 4
3 4
```

Vertex 1 has degree 2, which is less than `n-1 = 3`.

All edges incident to vertex 1 become color 1. The remaining edges become color 2.

Vertex 4 is not adjacent to vertex 1, so it is isolated in color 1. Vertex 1 is isolated in color 2. Both colors are disconnected, while their union is the original connected graph.

This is exactly the property the construction exploits.
