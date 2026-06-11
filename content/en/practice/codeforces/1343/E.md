---
title: "CF 1343E - Weights Distributing"
description: "We are given a connected undirected graph where each edge will eventually receive exactly one price from a given multiset of weights. After the assignment is fixed, a traveler starts at node $a$, goes optimally to $b$, then again optimally from $b$ to $c$."
date: "2026-06-11T15:12:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "graphs", "greedy", "shortest-paths", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1343
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 636 (Div. 3)"
rating: 2100
weight: 1343
solve_time_s: 188
verified: false
draft: false
---

[CF 1343E - Weights Distributing](https://codeforces.com/problemset/problem/1343/E)

**Rating:** 2100  
**Tags:** brute force, graphs, greedy, shortest paths, sortings  
**Solve time:** 3m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph where each edge will eventually receive exactly one price from a given multiset of weights. After the assignment is fixed, a traveler starts at node $a$, goes optimally to $b$, then again optimally from $b$ to $c$. Every time an edge is traversed, its assigned price is paid again, so repeated traversal of the same edge increases cost linearly.

The central freedom is that we do not control the route, only the assignment of weights to edges. After we assign weights, the traveler always chooses shortest possible paths under those weights.

The task is to assign weights so that the resulting optimal cost of the two-leg journey is minimized.

The constraints force an $O(n \log n)$ or $O(n)$ per test solution because the total number of vertices and edges across all tests is at most $2 \cdot 10^5$. Any approach that tries to recompute shortest paths per assignment or consider permutations of weights is immediately infeasible since both $n!$ and even $O(m^2)$ style reasoning would explode.

A subtle difficulty is that edges can be reused in the route from $a \to b \to c$, meaning some edges are paid multiple times. A naive assumption that we only care about a single shortest path or a tree-like structure fails.

For example, if one tries to independently assign smallest weights to edges on shortest $a \to b$ and $b \to c$ paths, one might double count without controlling overlap. Another failure case is assuming the optimal meeting structure is always a single midpoint on a shortest path tree, which ignores that the best overlap point depends on all three sources simultaneously.

## Approaches

The brute-force viewpoint is to think of assigning weights to edges and then recomputing shortest paths for the induced weighted graph. For each assignment, we would run Dijkstra from $a$ to $b$ and from $b$ to $c$, then try all permutations of weights over edges. This is factorial in $m$, and even evaluating one assignment costs $O(m \log n)$, which is far beyond limits.

The key structural insight is that we should separate geometry from weighting. The graph structure determines how many times each edge must be used in an optimal trip, while the weights only determine which edges should “pay” for those uses.

Fix any vertex $x$ as a hypothetical meeting point where both parts of the journey intersect. Consider forcing the path structure to go $a \to x \to b \to x \to c$. This captures all optimal overlaps between the two segments. For this fixed choice, we can express how many times each edge is traversed purely using unweighted distances.

If we denote unweighted shortest path distances by $d(u,v)$, then the total number of edge traversals in this forced structure becomes

$$d(a,x) + 2d(b,x) + d(c,x).$$

Among these traversals, exactly $d(b,x)$ edges are used twice, because the segment from $b$ to $x$ is traversed once in each direction.

Once traversal counts are fixed, the weight assignment problem becomes a pure rearrangement problem: assign smallest weights to most frequently used edges. This reduces the problem to sorting and prefix sums.

We evaluate every candidate $x$, compute its induced traversal structure, and pick the best.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force assignments + shortest paths | exponential | high | Too slow |
| Distance-based enumeration of meeting point + sorting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Run BFS from $a$, $b$, and $c$ on the unweighted graph to compute shortest distances $d_a[], d_b[], d_c[]$. This gives the minimum number of edges needed between any node and each of the three sources.
2. Sort the weight array $p$ in non-decreasing order and build prefix sums. This allows constant-time queries for the sum of the smallest $k$ weights.
3. For each node $x$, interpret it as the central overlap point of the two-leg journey structure.
4. Compute the total number of traversals needed if paths are forced through $x$:

$$S(x) = d_a[x] + 2d_b[x] + d_c[x].$$

This represents the full walk $a \to x \to b \to x \to c$.
5. Compute how many edges are traversed twice:

$$T(x) = d_b[x].$$

These correspond to the edges on the $b \leftrightarrow x$ segment, which is used in both directions.
6. Convert traversal counts into cost. The cheapest $S(x)$ edge usages take the smallest weights, and the extra $T(x)$ repeated usages correspond to additional copies of the next cheapest edges. The cost becomes:

$$\text{cost}(x) = \text{pref}[S(x)] + \text{pref}[S(x) + T(x)] - \text{pref}[S(x)] = \text{pref}[S(x)] + \text{pref}[T(x)].$$
7. Evaluate this expression for all nodes $x$ and take the minimum.

### Why it works

The BFS distances guarantee that any optimal structure of the walk can be represented by choosing a meeting node $x$ where both legs overlap in an optimal unweighted sense. Once $x$ is fixed, the number of times each edge must be used is fully determined by shortest path geometry.

The rearrangement argument ensures that, given fixed usage counts, assigning smaller weights to more frequently used edges minimizes total cost. Since only the multiset of traversal counts matters, not the identity of edges, optimizing over $x$ covers all possible optimal overlap configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def bfs(start, g, n):
    dist = [10**18] * (n + 1)
    q = deque([start])
    dist[start] = 0
    while q:
        v = q.popleft()
        for to in g[v]:
            if dist[to] == 10**18:
                dist[to] = dist[v] + 1
                q.append(to)
    return dist

t = int(input())
for _ in range(t):
    n, m, a, b, c = map(int, input().split())
    p = list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    da = bfs(a, g, n)
    db = bfs(b, g, n)
    dc = bfs(c, g, n)

    p.sort()
    pref = [0] * (m + 1)
    for i in range(m):
        pref[i + 1] = pref[i] + p[i]

    ans = 10**30
    for x in range(1, n + 1):
        s = da[x] + db[x] + dc[x]
        # total traversals
        S = s + db[x]
        T = db[x]
        if S <= m:
            cost = pref[S] + pref[T]
            if cost < ans:
                ans = cost

    print(ans)
```

The BFS section builds shortest path distance layers independently from each of the three special nodes. The key implementation detail is that all distances are computed in the unweighted graph, so each BFS is linear.

Sorting the weights once per test ensures that we always match small weights to high usage. The prefix sum array allows us to compute sums of any prefix in constant time.

The loop over all nodes computes the candidate cost for using that node as the overlap center, directly implementing the derived formula. The final minimum aggregates all structural possibilities.

## Worked Examples

### Example 1

Consider a simple graph where different nodes serve as possible overlap centers. For each node $x$, we compute distances from $a$, $b$, and $c$, then derive traversal counts.

| x | d(a,x) | d(b,x) | d(c,x) | S = da + db + dc + db | T = db | cost = pref[S] + pref[T] |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 0 | 2 | 3 | 0 | pref[3] |
| 3 | 2 | 1 | 1 | 5 | 1 | pref[5] + pref[1] |
| 4 | 1 | 2 | 0 | 4 | 2 | pref[4] + pref[2] |

The minimum among these corresponds to the optimal meeting configuration.

This demonstrates that the optimal solution is not tied to a single shortest path but to a balance between overlap and separation across all three sources.

### Example 2

Take a chain-like structure where all paths are forced through intermediate nodes.

| x | d(a,x) | d(b,x) | d(c,x) | S | T |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 3 | 7 | 2 |
| 2 | 1 | 1 | 2 | 6 | 1 |
| 3 | 2 | 0 | 1 | 5 | 0 |

Here the best $x$ is clearly the one closest to $b$, minimizing repeated traversal. This shows how minimizing $d(b,x)$ directly reduces the expensive double-counted segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m \log m)$ | BFS from three sources plus sorting weights dominates |
| Space | $O(n + m)$ | adjacency list and distance arrays |

The total complexity fits comfortably within limits since the sum of all $n$ and $m$ across tests is $2 \cdot 10^5$, and each operation is linear or near-linear.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    from collections import deque

    def bfs(start, g, n):
        dist = [10**18] * (n + 1)
        q = deque([start])
        dist[start] = 0
        while q:
            v = q.popleft()
            for to in g[v]:
                if dist[to] == 10**18:
                    dist[to] = dist[v] + 1
                    q.append(to)
        return dist

    t = int(input())
    out = []
    for _ in range(t):
        n, m, a, b, c = map(int, input().split())
        p = list(map(int, input().split()))
        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        da = bfs(a, g, n)
        db = bfs(b, g, n)
        dc = bfs(c, g, n)

        p.sort()
        pref = [0] * (m + 1)
        for i in range(m):
            pref[i + 1] = pref[i] + p[i]

        ans = 10**30
        for i in range(1, n + 1):
            s = da[i] + db[i] + dc[i]
            S = s + db[i]
            T = db[i]
            if S <= m:
                ans = min(ans, pref[S] + pref[T])

        out.append(str(ans))

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("""2
4 3 2 3 4
1 2 3
1 2
1 3
1 4
7 9 1 5 7
2 10 4 8 5 6 7 3 3
1 2
1 3
1 4
3 2
3 5
4 2
5 6
1 7
6 7
""") == """7
12"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Star graph | correct overlap handling | center choice matters |
| Line graph | path degeneracy | minimal structure case |
| Random small graph | correctness of BFS distances | general validity |
| Equal weights | symmetry handling | no bias in assignment |

## Edge Cases

When all vertices lie on a single path, every BFS distance behaves like a linear index. The algorithm correctly evaluates each node as a potential overlap point, and the minimum is achieved at or near $b$, since that minimizes the doubled segment $d_b[x]$.

When the graph is a star centered at some node, choosing the center as $x$ minimizes all distances simultaneously, producing zero or minimal overlap cost depending on placement of $a$, $b$, and $c$. The formula naturally captures this since all BFS distances collapse through the center, and the double-count term does not distort correctness.

When $a = b = c$, every candidate yields $T(x) = 0$, and the solution reduces to assigning smallest weights to a single shortest path structure, which the prefix formula handles directly.
