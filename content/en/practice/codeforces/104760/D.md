---
title: "CF 104760D - \u0412\u0435\u0441\u0435\u043b\u044b\u0435 \u0444\u043e\u043d\u0430\u0440\u0438"
description: "The city can be modeled as an undirected graph where each lamp post is a vertex and each street is an edge between two vertices. The task is to decide whether we can assign one of two colors to each vertex so that every street connects vertices of different colors."
date: "2026-06-29T02:21:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 69
verified: false
draft: false
---

[CF 104760D - \u0412\u0435\u0441\u0435\u043b\u044b\u0435 \u0444\u043e\u043d\u0430\u0440\u0438](https://codeforces.com/problemset/problem/104760/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

The city can be modeled as an undirected graph where each lamp post is a vertex and each street is an edge between two vertices. The task is to decide whether we can assign one of two colors to each vertex so that every street connects vertices of different colors.

This is exactly the question of whether the graph is bipartite, but the problem is phrased in a more physical setting: we are repainting lamp bulbs with two available colors and want adjacent lamp posts (connected by at least one street) to never share the same color.

The input may contain multiple test cases. For each test case we are given up to 400 vertices and up to N·(N−1)/2 edges, including self-loops and repeated edges. A self-loop immediately connects a vertex to itself, which makes a valid two-coloring impossible because that vertex would need to differ from itself.

The constraints imply that even an O(N² + M) graph traversal per test case is acceptable. A BFS or DFS based bipartite check is sufficient.

A few edge cases are easy to miss if the implementation is careless. First, self-loops must be handled explicitly. For example, input `1 1 1 1` has a single vertex with an edge to itself. The correct answer is `NO` because that vertex would need two different colors simultaneously.

Second, multiple edges between the same pair of vertices do not change correctness but can cause redundant processing if adjacency is not deduplicated. A correct approach should simply ignore duplicates.

Third, disconnected graphs must be handled by running the bipartite check from every unvisited vertex. Otherwise, one component might be checked while others remain unverified.

## Approaches

A brute-force interpretation would try all possible 2-color assignments of N vertices. Each vertex has two choices, giving 2ⁿ configurations. For each configuration, we verify all edges in O(M). This leads to O(2ⁿ · M), which becomes infeasible even for N = 30.

The key observation is that constraints are purely local: each edge only enforces inequality between its endpoints. This is exactly the constraint system of bipartite checking. Instead of searching over assignments globally, we can propagate forced assignments locally.

We pick an uncolored vertex, assign it a color, and propagate through edges: neighbors must take the opposite color. If we ever encounter a contradiction, the graph is not bipartite. This reduces the problem to a graph traversal.

The presence of self-loops immediately breaks bipartiteness because a vertex must differ from itself along an edge. Therefore we can reject early.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · M) | O(N) | Too slow |
| BFS/DFS Bipartite Check | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph, ignoring duplicate edges since they do not affect bipartiteness.
2. While reading edges, if any edge connects a vertex to itself, immediately mark the test case as invalid.
3. Maintain a color array initialized to uncolored for all vertices.
4. For every vertex that is still uncolored, start a BFS.
5. Assign the starting vertex color 0 and push it into a queue.
6. During BFS, for each edge u → v, if v is uncolored, assign it the opposite color of u and push it into the queue.
7. If v is already colored and has the same color as u, the graph is not bipartite, so we stop and output NO.
8. If BFS completes for all components without conflict, output YES.

### Why it works

The algorithm enforces that every edge imposes a strict inequality constraint between its endpoints. BFS propagation ensures that once a vertex is assigned a color, all reachable vertices receive uniquely determined colors consistent with parity of path length. If a contradiction occurs, it means there exist two different parity paths between the same pair of vertices, which implies an odd cycle. A graph is bipartite if and only if it contains no odd cycle, so the detection is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        parts = input().split()
        n = int(parts[0])
        m = int(parts[1])

        adj = [[] for _ in range(n + 1)]
        idx = 2
        ok = True

        for _ in range(m):
            u = int(parts[idx]); v = int(parts[idx + 1])
            idx += 2

            if u == v:
                ok = False
            else:
                adj[u].append(v)
                adj[v].append(u)

        if not ok:
            out.append("NO")
            continue

        color = [-1] * (n + 1)

        from collections import deque

        for i in range(1, n + 1):
            if color[i] != -1:
                continue

            color[i] = 0
            q = deque([i])

            while q and ok:
                u = q.popleft()
                for v in adj[u]:
                    if color[v] == -1:
```
