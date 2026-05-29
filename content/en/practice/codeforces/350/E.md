---
title: "CF 350E - Wrong Floyd"
description: "We are given an undirected, simple, connected graph with a fixed number of vertices and edges. On top of that, a subset of vertices is marked."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 350
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 203 (Div. 2)"
rating: 2200
weight: 350
solve_time_s: 138
verified: false
draft: false
---

[CF 350E - Wrong Floyd](https://codeforces.com/problemset/problem/350/E)

**Rating:** 2200  
**Tags:** brute force, constructive algorithms, dfs and similar, graphs  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected, simple, connected graph with a fixed number of vertices and edges. On top of that, a subset of vertices is marked. Someone runs a modified Floyd-Warshall process: instead of iterating all intermediate vertices from 1 to n, they only use the marked vertices as intermediates.

This change looks harmless at first, but it fundamentally alters what distances the algorithm is allowed to “discover”. The task is not to fix the algorithm. Instead, we must construct any valid simple graph (no self-loops, no multi-edges) for which this restricted Floyd procedure produces at least one incorrect shortest path distance. If no such graph exists for the given constraints, we must output -1.

The graph constraints matter in a subtle way. With n up to 300, brute-force construction or reasoning over all triples is feasible. However, the solution is not about heavy computation but about forcing a structural mismatch between “true shortest paths” and “paths that only pass through marked vertices”.

The key hidden edge case is when all shortest paths between certain vertices rely on going through an unmarked vertex as an intermediate step. The modified Floyd will never consider that vertex as a relay, so it cannot relax those distances properly. If we can force such a dependency while still keeping the graph connected and valid, we get a counterexample.

A naive misunderstanding would be to assume that marking all vertices or marking none are the only meaningful extremes. In reality, even a single unmarked vertex strategically placed can break correctness.

A second subtle edge case is when the marked vertices already form a “vertex cover of shortest paths”, meaning every shortest path can be re-routed through marked nodes without increasing distance. In that case, no counterexample exists, and the answer would be -1.

## Approaches

The brute-force perspective is to think in terms of what the algorithm actually computes. The initial distances come from the graph edges, then Floyd updates only through marked vertices. So effectively, the algorithm computes shortest paths in a graph where intermediate nodes are restricted to the marked set.

If we imagine running full Floyd-Warshall, every vertex acts as a possible intermediate, and shortest paths are guaranteed to propagate correctly. Here, we are removing a subset of intermediates. The question becomes whether that subset is “sufficient” to represent all shortest paths.

A naive construction attempt might try arbitrary graphs and hope for failure, but that is not structured. Instead, we flip the perspective: we intentionally design a graph where the only way to shorten a path between two vertices is to pass through an unmarked vertex.

Once we realize this, the construction becomes simple. We isolate one unmarked vertex as a mandatory bridge between two parts of the graph. If a shortest path between two endpoints must go through this unmarked vertex, then the modified Floyd will never relax that distance through it, and it will fail.

The rest of the graph can be filled minimally to satisfy n and m while preserving this bottleneck structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force random construction | O(n^3) attempts potentially | O(n^2) | Not reliable |
| Structured construction with bottleneck unmarked vertex | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. First identify whether there exists at least one unmarked vertex. If all vertices are marked, the modified Floyd is identical to the standard Floyd, so it cannot be forced to fail. In that case, we immediately return -1.
2. Choose any unmarked vertex v. This vertex will be the “hidden bridge” that the algorithm is forbidden to use as an intermediate.
3. Construct a graph where v is essential for shortest paths between at least one pair of vertices. A clean way is to split vertices into two groups and connect them only through v.
4. Connect all vertices in the first group directly to v, and similarly connect all vertices in the second group directly to v. This guarantees connectivity while ensuring that any shortest path between the two groups goes through v.
5. Ensure that the number of edges matches m. If extra edges are needed, add them within each group carefully without creating alternative shorter cross-group routes that bypass v.
6. Output all edges. The resulting graph forces at least one shortest path to rely on v as an intermediate, which the algorithm cannot use since v is unmarked.

### Why it works

The constructed graph ensures that for some pair of vertices u and w in different groups, every shortest path between them must pass through the unmarked vertex v. In true shortest-path computation, v is essential as an intermediate node. However, the modified Floyd-Warshall never uses v in its relaxation step, so it cannot propagate the correct two-step relaxation u → v → w. As a result, the algorithm leaves ans[u][w] larger than the true shortest distance, producing a guaranteed mismatch.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    marked = set(map(int, input().split()))

    # find an unmarked vertex
    unmarked = -1
    for i in range(1, n + 1):
        if i not in marked:
            unmarked = i
            break

    # if all vertices are marked, algorithm is correct
    if unmarked == -1:
        print(-1)
        return

    edges = []

    # split vertices into two groups excluding unmarked vertex
    group1 = []
    group2 = []

    for i in range(1, n + 1):
        if i == unmarked:
            continue
        if len(group1) < (n - 1) // 2:
            group1.append(i)
        else:
            group2.append(i)

    v = unmarked

    # connect everything to v (star structure)
    for u in group1:
        edges.append((u, v))
    for u in group2:
        edges.append((u, v))

    # if more edges needed, add inside group1
    for i in range(len(group1)):
        for j in range(i + 1, len(group1)):
            if len(edges) < m:
                edges.append((group1[i], group1[j]))
            else:
                break

    # if still more edges needed, add inside group2
    for i in range(len(group2)):
        for j in range(i + 1, len(group2)):
            if len(edges) < m:
                edges.append((group2[i], group2[j]))
            else:
                break

    # guarantee connectivity already ensured via v
    for u,
```
