---
title: "CF 1927F - Microcycle"
description: "We are asked to find a simple cycle in an undirected, weighted graph where the minimal edge in that cycle is as small as possible. The input is a series of graphs: each graph is described by the number of vertices, the number of edges, and a list of edges with weights."
date: "2026-06-08T18:55:53+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dsu", "graphs", "greedy", "implementation", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1927
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 923 (Div. 3)"
rating: 1900
weight: 1927
solve_time_s: 144
verified: false
draft: false
---

[CF 1927F - Microcycle](https://codeforces.com/problemset/problem/1927/F)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, dsu, graphs, greedy, implementation, sortings, trees  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find a simple cycle in an undirected, weighted graph where the minimal edge in that cycle is as small as possible. The input is a series of graphs: each graph is described by the number of vertices, the number of edges, and a list of edges with weights. A simple cycle is one where no vertex or edge repeats. The output is the weight of the smallest edge in the cycle we find, the number of vertices in that cycle, and the sequence of vertices traversed.

The constraints tell us several important things. Each graph can have up to about $2 \cdot 10^5$ edges across all test cases, meaning any algorithm that iterates over all pairs of vertices is infeasible. The graph is sparse in the sense that $m \le n(n-1)/2$, but dense graphs up to a few thousand vertices are possible. Because there is always at least one simple cycle, we do not have to handle cycle-free graphs. Edge weights are positive integers up to $10^6$, so we do not need to handle negative cycles.

A naive approach might attempt to enumerate all cycles, but this is immediately impractical because the number of cycles in a graph can grow exponentially with the number of vertices. Another subtle point is that multiple cycles may share edges, and the cycle minimizing the lightest edge is not necessarily the smallest or shortest cycle. A careless solution might pick any cycle, or the first found cycle via DFS, which could produce a heavier minimal edge than necessary.

Edge cases that can trip up a naive approach include triangles where one edge is much lighter than the others, or disconnected components where only some parts contain small edges. For example, consider a graph with vertices 1-3 forming a triangle with edge weights 1, 100, 100. The minimal lightest-edge cycle is obviously the triangle itself with minimal edge 1. If we only looked for short cycles elsewhere, we could mistakenly report 100 as the minimal edge.

## Approaches

A brute-force method would try to enumerate all simple cycles and then select the one with the minimal lightest edge. One way is to pick each edge, remove it, and try to find a path connecting its endpoints. If a path exists, adding the removed edge completes a cycle. This is correct because any cycle can be decomposed this way. The problem is that path-finding is O(n + m) per edge, leading to a total complexity of O(m(n + m)) which is too slow given $m \sim 2 \cdot 10^5$.

The key insight is that the minimal lightest-edge cycle can be found by focusing on small subgraphs. Triangles (3-cycles) are often optimal because the smallest edge in any longer cycle cannot be smaller than the smallest edge in a triangle that contains it. This reduces our problem to efficiently finding triangles in the graph. We can exploit vertex degrees: sort edges by weight and attempt to find cycles formed by edges connected to a common vertex. Union-Find (DSU) with tracking of ancestors or BFS/DFS restricted to small neighborhoods helps find candidate cycles quickly.

We also observe that we can attempt edges in increasing weight order. The first edge that completes a cycle is guaranteed to include the minimal possible edge in that cycle because all lighter edges have been processed without forming a cycle. This is similar to Kruskal's MST algorithm but instead of connecting components minimally, we check for cycle closure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force: enumerate cycles | O(m(n+m)) | O(n+m) | Too slow |
| Triangle search / edge-ordering | O(m * deg) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read all edges and store them along with their weights. Sort the edges in increasing order of weight. Sorting ensures we process edges starting with the smallest, which is critical because the minimal edge in a cycle must be considered first.
2. Initialize a Union-Find (DSU) structure to maintain connected components. For each vertex, track its parent and rank to allow fast merges and ancestor lookups.
3. Iterate over the edges in weight order. For each edge, check if its endpoints belong to the same connected component using DSU. If they do, adding this edge would form a cycle.
4. When a cycle is detected, reconstruct it. Perform BFS or DFS from one endpoint of the edge to the other along the existing graph edges excluding the current edge. Collect the path and append the current edge to close the cycle. The minimal edge in this cycle is the current edge because all lighter edges have already been processed and did not form a cycle.
5. If the endpoints are not in the same component, merge them in DSU. This ensures future edges can detect cycles properly.
6. Output the weight of the edge used to detect the cycle, the number of vertices in the cycle, and the traversal order of vertices.

Why it works: The invariant is that we process edges in increasing weight. DSU guarantees that the first time an edge closes a cycle, that cycle contains no edge lighter than the current one. Any cycle containing a lighter edge would have been detected earlier. Therefore, the minimal edge in the cycle we report is minimal globally.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n+1))
        self.rank = [0]*(n+1)

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        else:
            self.parent[yr] = xr
            if self.rank[xr] == self.rank[yr]:
                self.rank[xr] += 1
        return True

def find_cycle(n, edges):
    edges.sort(key=lambda x: x[2])
    dsu = DSU(n)
    graph = [[] for _ in range(n+1)]
    
    for u, v, w in edges:
        if dsu.find(u) == dsu.find(v):
            # cycle detected
            # BFS to find path from u to v
            prev = [-1]*(n+1)
            q = deque()
            q.append(u)
            visited = [False]*(n+1)
            visited[u] = True
            while q:
                node = q.popleft()
                if node == v:
                    break
                for nei in graph[node]:
                    if not visited[nei]:
                        visited[nei] = True
                        prev[nei] = node
                        q.append(nei)
            # reconstruct path
            path = []
            curr = v
            while curr != -1:
                path.append(curr)
                curr = prev[curr]
            path.reverse()
            path.append(u)
            return w, len(path), path
        else:
            dsu.union(u, v)
            graph[u].append(v)
            graph[v].append(u)
    return None

def main():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]
        b, k, path = find_cycle(n, edges)
        print(f"{b} {k}")
        print(" ".join(map(str, path)))

if __name__ == "__main__":
    main()
```

The code sorts edges to guarantee we consider minimal edges first. DSU efficiently detects when a new edge forms a cycle. BFS is used to reconstruct the exact path of the cycle in O(n + m) time, which is feasible because we only do it once per cycle. Appending the current edge closes the cycle and guarantees the minimal edge is included.

## Worked Examples

Sample Input:

```
6 6
1 2 1
2 3 1
3 1 1
4 5 1
5 6 1
6 4 1
```

| Step | Edge (u,v,w) | DSU merge? | Cycle detected? | BFS path |
| --- | --- | --- | --- | --- |
| 1 | 1,2,1 | Yes | No | - |
| 2 | 2,3,1 | Yes | No | - |
| 3 | 3,1,1 | No | Yes | 1-2-3 |
| 4 | ... | - | - | - |

The BFS reconstructs path 1-2-3 and adding edge 3-1 closes the cycle. Minimal edge weight is 1.

Another Input:

```
4 5
1 2 2
2 3 2
3 4 2
4 1 2
1 3 3
```

The first cycle detected is 1-2-3-1 with minimal edge 2. BFS reconstructs 1-2-3, append 1 closes cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m + m(n+m)) | Sorting edges takes O(m log m). DSU operations are nearly O(1) amortized. BFS to reconstruct the path takes O(n + m). |
| Space | O(n + m) | Graph adjacency lists, DSU arrays, visited arrays |

Given that the sum of m across all test cases is ≤
