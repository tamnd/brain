---
title: "CF 1155F - Delivery Oligopoly"
description: "We are given a simple undirected graph that is already 2-edge-connected. By Menger's theorem, this means every pair of vertices has two edge-disjoint paths between them, which is exactly the condition required by the two delivery companies."
date: "2026-06-12T02:45:59+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1155
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 63 (Rated for Div. 2)"
rating: 2800
weight: 1155
solve_time_s: 128
verified: false
draft: false
---

[CF 1155F - Delivery Oligopoly](https://codeforces.com/problemset/problem/1155/F)

**Rating:** 2800  
**Tags:** brute force, dp, graphs  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple undirected graph that is already 2-edge-connected. By Menger's theorem, this means every pair of vertices has two edge-disjoint paths between them, which is exactly the condition required by the two delivery companies.

The government wants to delete as many roads as possible while keeping that property true. We must output a smallest possible subset of the original edges whose induced graph is still 2-edge-connected.

The graph is tiny. There are at most 14 vertices, although the number of edges can be as large as a complete graph. A graph with 14 vertices has at most $2^{14}=16384$ vertex subsets, which strongly suggests a bitmask dynamic programming solution. On the other hand, the number of edge subsets can be as large as $2^{91}$, so any approach that directly searches over edges is hopeless.

The key difficulty is that 2-edge-connectivity is a global property. A spanning tree is connected, but every edge of a tree is a bridge, so it is as far from 2-edge-connected as possible. A naive DP that only tracks connectivity loses too much information.

A common mistake is to think that every newly added vertex must immediately have degree at least two inside the current solution. Consider:

```
1 -- 2 -- 3 -- 4
 \___________/
```

The final graph is a cycle and is 2-edge-connected, but while constructing it we may temporarily introduce vertices that are not yet attached twice.

Another pitfall is assuming that the optimal answer is always a single cycle through all vertices. If the original graph does not contain a Hamiltonian cycle, the minimum 2-edge-connected spanning subgraph may need more than $n$ edges.

For example:

```
1-2-3
|   |
4---5
```

with suitable additional edges guaranteeing 2-edge-connectivity in the original graph. The optimal preserved subgraph is not necessarily a simple cycle.

The small value of $n$ is the real clue. We need a structural characterization that converts 2-edge-connectivity into a subset DP.

## Approaches

The brute force idea is straightforward. Enumerate every subset of edges, test whether it spans all vertices and remains 2-edge-connected, and keep the smallest valid one.

Testing a candidate graph is easy with bridge finding, but the search space is not. Even for $m=40$, there are $2^{40}$ edge subsets. The worst case here has $m=91$, which is completely out of reach.

The breakthrough comes from a classical theorem: every 2-edge-connected graph admits an ear decomposition. Starting from a single vertex, we repeatedly add an "ear". An ear is either a single new vertex attached to the existing graph by two edges, or a path whose internal vertices are new and whose two endpoints connect back to the already constructed part.

That description matches the accepted solution almost perfectly.

Suppose we already built some vertex set $S$. An ear can add:

1. One vertex $u\notin S$ having at least two neighbors in $S$.
2. A path whose internal vertices are all outside $S$, while both endpoints have neighbors in $S$.

Each ear contributes a known number of edges. Since $n\le14$, we can use a DP over vertex subsets and reconstruct an optimal ear decomposition.

The remaining task is efficiently enumerating candidate ears. Because $n$ is tiny, we precompute every simple path by its vertex set. This allows the DP to attach entire paths in one transition.

The resulting complexity is roughly $O(3^n)$, which is easily feasible for $n=14$. The solution used in accepted submissions follows exactly this strategy.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over edge subsets | $O(2^m)$ | $O(m)$ | Too slow |
| Ear decomposition DP | $O(3^n)$ | $O(2^n)$ plus path storage | Accepted |

## Algorithm Walkthrough

### Precomputation

For every vertex $i$ and every subset mask, compute:

$$\text{vtomask}[i][mask]$$

which counts how many neighbors of $i$ belong to `mask`.

This lets us instantly check whether a vertex can attach to the current constructed part.

We also precompute simple paths.

Let `road[mask][u][v]` store one simple path from $u$ to $v$ whose vertex set is exactly `mask`.

Starting from single vertices, we extend paths by one vertex at a time.

### DP State

Let:

$$dp[mask]$$

be the minimum number of edges needed to build a valid partial ear decomposition whose vertex set is exactly `mask`.

We fix vertex 0 as the starting vertex.

Initially:

$$dp[1<<0]=0.$$

### Transitions

1. Add one new vertex $u$.

If $u\notin mask$ and $u$ has at least two neighbors already inside `mask`, then we may add $u$ as a one-vertex ear.

Cost increase: 2.
2. Add a path ear.

Choose two vertices $u,v\notin mask$.

Find a simple path whose internal vertices are outside `mask`.

Let its vertex set be `tmask`.

If $u$ has a neighbor in `mask` and $v$ has a neighbor in `mask`, we can connect the path back to the existing graph.

A path containing $L$ vertices contributes $L-1$ internal edges, plus two attachment edges.

Total increase:

$$(L-1)+2=L+1.$$

This is exactly the transition used by the accepted solution.
3. Relax the destination state:

$$dp[mask\cup tmask].$$

### Reconstruction

For every DP update we store:

- previous mask,
- chosen endpoint $u$,
- chosen endpoint $v$ (or $-1$ for a one-vertex ear).

After reaching the full mask, we walk backward through the stored transitions and output all edges used by the selected ears.

### Why it works

Ear decomposition characterizes exactly the class of 2-edge-connected graphs. Every valid solution can be written as a sequence of ears starting from one vertex. Conversely, every graph produced by the DP is obtained by repeatedly attaching valid ears and is therefore 2-edge-connected.

The DP considers every possible ear whose internal vertices are new. Since every ear decomposition can be ordered so that newly introduced vertices appear only once, every optimal solution corresponds to some sequence of DP transitions.

The DP minimizes the total number of edges among all such sequences, so the final state gives a minimum-size 2-edge-connected spanning subgraph.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 9

def solve():
    n, m = map(int, input().split())

    g = [[0] * n for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u][v] = g[v][u] = 1

    N = 1 << n

    vtomask = [[0] * N for _ in range(n)]
    for i in range(n):
        for mask in range(N):
            c = 0
            mm = mask
            while mm:
                b = mm & -mm
                j = b.bit_length() - 1
                if g[i][j]:
                    c += 1
                mm ^= b
            vtomask[i][mask] = c

    road = [[[None for _ in range(n)] for _ in range(n)] for _ in range(N)]

    for i in range(n):
        road[1 << i][i][i] = [i]

    for mask in range(N):
        for u in range(n):
            for v in range(n):
                p = road[mask][u][v]
                if p is None:
                    continue

                for z in range(n):
                    if (mask >> z) & 1:
                        continue
                    if not g[v][z]:
                        continue

                    nmask = mask | (1 << z)
                    if road[nmask][u][z] is not None:
                        continue

                    road[nmask][u][z] = p + [z]

    dp = [INF] * N
    pre_mask = [-1] * N
    pre_u = [-1] * N
    pre_v = [-2] * N

    dp[1] = 0

    for mask in range(1, N):
        if dp[mask] >= INF:
            continue

        for u in range(n):
            if (mask >> u) & 1:
                continue

            if vtomask[u][mask] >= 2:
                nmask = mask | (1 << u)
                nd = dp[mask] + 2
                if nd < dp[nmask]:
                    dp[nmask] = nd
                    pre_mask[nmask] = mask
                    pre_u[nmask] = u
                    pre_v[nmask] = -1

            if vtomask[u][mask] == 0:
                continue

            for v in range(u + 1, n):
                if (mask >> v) & 1:
                    continue
                if vtomask[v][mask] == 0:
                    continue

                amask = (N - 1) ^ mask ^ (1 << u) ^ (1 << v)

                smask = amask
                while True:
                    tmask = smask | (1 << u) | (1 << v)

                    path = road[tmask][u][v]
                    if path is not None:
                        nmask = mask | tmask
                        nd = dp[mask] + len(path) + 1

                        if nd < dp[nmask]:
                            dp[nmask] = nd
                            pre_mask[nmask] = mask
                            pre_u[nmask] = u
                            pre_v[nmask] = v

                    if smask == 0:
                        break
                    smask = (smask - 1) & amask

    full = N - 1
    print(dp[full])

    ans = []

    mask = full
    while mask != 1:
        pmask = pre_mask[mask]
        u = pre_u[mask]
        v = pre_v[mask]

        if v == -1:
            need = 2
            for x in range(n):
                if need and ((pmask >> x) & 1) and g[u][x]:
                    ans.append((u + 1, x + 1))
                    need -= 1
        else:
            tmask = mask ^ pmask
            path = road[tmask][u][v]

            for i in range(1, len(path)):
                ans.append((path[i - 1] + 1, path[i] + 1))

            for x in range(n):
                if ((pmask >> x) & 1) and g[u][x]:
                    ans.append((x + 1, u + 1))
                    break

            for x in range(n):
                if ((pmask >> x) & 1) and g[v][x]:
                    ans.append((x + 1, v + 1))
                    break

        mask = pmask

    for u, v in ans:
        print(u, v)

solve()
```

The path precomputation is the most unusual part of the implementation. `road[mask][u][v]` stores one simple path whose vertices are exactly `mask`. Since $n$ is only 14, storing paths by subset is feasible.

The DP never reasons about bridges directly. Instead it works entirely through ear decomposition transitions. That is the structural insight that reduces a difficult graph property to subset DP.

During reconstruction, the code recreates the exact edges contributed by each ear. A path ear contributes its internal path edges plus one attachment edge at each endpoint. A single-vertex ear contributes two attachment edges.

## Worked Examples

### Sample 1

Input:

```
3 3
1 2
2 3
3 1
```

State evolution:

| Mask | Vertices | dp |
| --- | --- | --- |
| 001 | {1} | 0 |
| 111 | {1,2,3} | 3 |

The DP chooses the path ear $2-3$, then attaches both endpoints back to vertex 1. The resulting graph is exactly the triangle.

This example shows the smallest possible 2-edge-connected graph. Every edge is required.

### Example 2

Input:

```
4 4
1 2
2 3
3 4
4 1
```

State evolution:

| Mask | Ear Added | Cost |
| --- | --- | --- |
| 0001 | start | 0 |
| 1111 | path 2-3-4 | 4 |

The chosen ear is the path $2\to3\to4$. Its internal contribution is three path vertices, giving cost $3+1=4$.

The final graph is the original cycle.

This trace illustrates that a single path ear can introduce several new vertices at once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(3^n)$ | DP over subsets and subset enumeration inside transitions |
| Space | $O(2^n \cdot n^2)$ | DP tables and path storage |

For $n=14$, $3^{14}\approx4.8$ million. That is well within the limits, which is why the solution relies on vertex-subset DP rather than edge-subset search.

##
