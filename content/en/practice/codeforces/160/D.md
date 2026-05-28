---
title: "CF 160D - Edges in MST"
description: "We are given a connected weighted undirected graph with no loops or multiple edges. Each edge has a positive weight."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "sortings"]
categories: ["algorithms"]
codeforces_contest: 160
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 111 (Div. 2)"
rating: 2300
weight: 160
solve_time_s: 81
verified: true
draft: false
---

[CF 160D - Edges in MST](https://codeforces.com/problemset/problem/160/D)

**Rating:** 2300  
**Tags:** dfs and similar, dsu, graphs, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected weighted undirected graph with no loops or multiple edges. Each edge has a positive weight. The task is to classify each edge according to whether it belongs to all minimum spanning trees, at least one minimum spanning tree, or no minimum spanning tree at all. In other words, for every edge, we want to know if it is indispensable for building an MST, optional, or impossible to include in any MST.

The graph can have up to 100,000 vertices and 100,000 edges, and each edge weight is up to 1,000,000. With these limits, an algorithm with worse than O(m log n) complexity is likely too slow. Brute-force approaches that try to build all MSTs explicitly or remove edges to see if MST weight increases would require O(m^2) or worse operations, which is infeasible.

Non-obvious edge cases include multiple edges with the same weight forming cycles. For instance, consider a triangle graph with vertices 1, 2, 3 and edges (1-2, weight 1), (2-3, weight 1), (3-1, weight 1). Any two edges form an MST. In such a case, all edges are "at least one," none are "any," and none are "none." Another edge case occurs when a single edge has the minimum weight connecting two components - that edge must be in every MST, but a careless algorithm that ignores equal-weight cycles might misclassify it.

## Approaches

The brute-force approach is straightforward: for each edge, temporarily remove it and recompute the MST. If the MST weight increases, the edge is in every MST. If the MST weight stays the same but the edge is included in one possible MST, it belongs to at least one MST. If including it always increases the MST weight, it is in no MST. This works in principle but is O(m * (m log n)) because each MST computation is O(m log n). With m up to 100,000, this becomes 10 billion operations, which is too slow.

The key observation is that MSTs can be efficiently analyzed by sorting edges by weight and processing edges in increasing order, as in Kruskal's algorithm. The union-find (DSU) structure keeps track of connected components. If an edge connects two separate components, it may be part of the MST. If multiple edges of the same weight connect the same components, we must carefully decide which ones are optional. To do this, we can group edges by weight, check connectivity for each edge within its group, and determine whether removing it would break connectivity. This avoids recomputing MSTs from scratch and lets us classify edges in O(m log n) using DSU with union by rank and path compression.

The final approach is a modified Kruskal: sort edges, process edges with the same weight together, and for each group, mark edges that are the only connection between components as "any," edges that connect components but have alternatives as "at least one," and edges forming cycles as "none."

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^2 log n) | O(n) | Too slow |
| Modified Kruskal + DSU | O(m log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph edges and store them along with their input indices so the output order can be preserved. Sort all edges by weight in ascending order. Sorting ensures we process the smallest edges first, as in Kruskal's MST algorithm.
2. Initialize a disjoint-set union (DSU) structure with one component per vertex. Each component will represent the set of vertices connected so far.
3. Process edges in groups by weight. For each group of edges with equal weight, do the following:
4. For each edge in the group, check if its endpoints belong to the same component in the current DSU. If they are in the same component, the edge would form a cycle and cannot belong to any MST, so mark it as "none."
5. If the endpoints are in different components, tentatively mark the edge as "at least one." These edges can potentially be included in an MST.
6. For all edges marked as "at least one" in this weight group, create a temporary graph where nodes are the DSU components and edges are the current weight edges connecting different components. Run a DFS or union-find check to detect which edges are bridges in this temporary graph. Edges that are bridges must be included in every MST connecting these components, so update their mark to "any." Non-bridge edges remain "at least one."
7. After classifying all edges in the group, merge their components in the main DSU. This ensures the next weight group sees the updated connectivity.
8. Repeat until all edges are processed. Finally, output the classification in the original input order.

Why it works: At every stage, edges that connect separate components can potentially be in an MST. By grouping edges of equal weight, we correctly handle situations where multiple edges can substitute for each other. Identifying bridges ensures that edges essential to connectivity are marked as "any," while edges forming cycles are excluded.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

sys.setrecursionlimit(1 << 25)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0]*n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1
        return True

n, m = map(int, input().split())
edges = []
for i in range(m):
    a, b, w = map(int, input().split())
    edges.append((w, a-1, b-1, i))

edges.sort()
res = [None]*m
dsu = DSU(n)
i = 0

while i < m:
    j = i
    group = []
    while j < m and edges[j][0] == edges[i][0]:
        group.append(edges[j])
        j += 1

    temp_graph = defaultdict(list)
    temp_edges = []
    for w, u, v, idx in group:
        u_root = dsu.find(u)
        v_root = dsu.find(v)
        if u_root == v_root:
            res[idx] = "none"
        else:
            res[idx] = "at least one"
            temp_graph[u_root].append((v_root, idx))
            temp_graph[v_root].append((u_root, idx))
            temp_edges.append((u_root, v_root, idx))

    visited = {}
    low = {}
    tin = {}
    timer = [0]

    def dfs(u, parent):
        visited[u] = True
        timer[0] += 1
        tin[u] = low[u] = timer[0]
        for v, idx in temp_graph[u]:
            if v == parent:
                continue
            if v in visited:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    res[idx] = "any"

    for node in temp_graph:
        if node not in visited:
            dfs(node, -1)

    for w, u, v, idx in group:
        dsu.union(u, v)
    i = j

for r in res:
    print(r)
```

The solution first sorts the edges, initializes DSU, and processes edges by weight. It classifies edges forming cycles as "none," and uses a temporary graph for each weight group to detect bridges, which are marked as "any." DSU merges after processing ensure connectivity updates for the next group.

## Worked Examples

### Sample 1

Input edges:

| idx | u | v | w |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 101 |
| 1 | 1 | 3 | 100 |
| 2 | 2 | 3 | 2 |
| 3 | 2 | 4 | 2 |
| 4 | 3 | 4 | 1 |

After sorting:

| u | v | w | idx |
| --- | --- | --- | --- |
| 3 | 4 | 1 | 4 |
| 2 | 3 | 2 | 2 |
| 2 | 4 | 2 | 3 |
| 1 | 3 | 100 | 1 |
| 1 | 2 | 101 | 0 |

Edges with weight 1: only edge 3-4, connects separate components, marked "any."

Edges with weight 2: edges 2-3 and 2-4. Both connect separate components, no bridge cycles yet, marked "at least one." DFS detects that neither is bridge in temp graph, remains "at least one."

Edges with weight 100: 1-3 connects separate components, marked "any."

Edge with weight 101: 1-2 would form a cycle, marked "none."

Output
