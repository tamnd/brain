---
title: "CF 2060E - Graph Composition"
description: "We are given two undirected graphs on the same set of vertices. One graph, call it the working graph, is the structure we are allowed to modify. The second graph is a fixed reference structure that we must eventually “match” in terms of connectivity."
date: "2026-06-08T10:40:52+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2060
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 998 (Div. 3)"
rating: 1500
weight: 2060
solve_time_s: 74
verified: true
draft: false
---

[CF 2060E - Graph Composition](https://codeforces.com/problemset/problem/2060/E)

**Rating:** 1500  
**Tags:** dfs and similar, dsu, graphs, greedy  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two undirected graphs on the same set of vertices. One graph, call it the working graph, is the structure we are allowed to modify. The second graph is a fixed reference structure that we must eventually “match” in terms of connectivity.

The allowed operation is very strong: we can freely insert any missing edge into the working graph or delete any existing edge. Each such modification costs one operation. After performing some sequence of these edits, we do not care about exact edges anymore, only about connected components. The goal is that two vertices end up connected in the working graph if and only if they are connected in the reference graph.

So the task is fundamentally about transforming one partition of vertices into another partition, where each partition is defined by connected components of a graph.

The constraints are tight: up to 2×10^5 vertices and edges across all test cases. This immediately rules out any approach that recomputes connectivity repeatedly per edge or simulates changes naively. Any solution must essentially reduce the problem to a few linear or almost-linear passes per test case, typically using DSU or DFS.

A subtle edge case arises when the two graphs already define identical connectivity but have very different edge sets. For example, if both graphs are connected but one is a tree and the other is dense, then no operations are needed because connectivity already matches, even though edge sets differ significantly. A naive approach that tries to “align edges” instead of components would incorrectly count unnecessary edits.

Another edge case occurs when both graphs are completely disconnected but partition vertices differently. For instance, if F is one component and G splits everything into singletons, then we must delete enough edges to isolate every vertex in F. Any approach focusing only on edge differences without considering component structure will overcount or undercount in such cases.

## Approaches

A brute-force perspective would try to directly transform F into some target graph that has the same connected components as G. One could imagine repeatedly checking pairs of vertices and deciding whether an edge is needed or must be removed depending on whether they should end up connected. However, each operation changes connectivity globally, so recomputing connected components after every edit leads to an expensive repeated graph traversal. Even if we carefully choose edges, maintaining dynamic connectivity under arbitrary additions and deletions pushes us into structures far heavier than necessary.

The key simplification is that we never actually need to match edges, only connected components. Once this is recognized, the problem reduces to comparing two partitions of the vertex set: components of F versus components of G.

Inside each connected component of G, all vertices must end up connected in the final graph. This means that within each G-component, the final state must be a single connected component. Conversely, vertices from different G-components must be disconnected in the final graph, so any edges of F that cross between different G-components are fundamentally “wrong” and must be removed.

Now the structure becomes clean. We first enforce that F respects the partition of G by removing all edges in F that connect different G-components. After this cleanup, each remaining component of F lies entirely inside some component of G. Within each G-component, we then need to connect possibly multiple F-components into one. Each merge of two components requires exactly one edge addition, and the best we can do is connect components greedily, so the cost is the number of components minus one per G-component.

This leads to a DSU-based solution: we use DSU for G to identify groups, then simulate F edges that are valid within those groups, count resulting components per group, and compute how many merges are needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Recompute | O(n·(m₁+m₂)) | O(n+m) | Too slow |
| DSU Component Merging | O((n+m₁+m₂) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We use disjoint set union structures twice in a conceptual way, but only one DSU is necessary in implementation.

1. Build DSU for graph G to compute its connected components. Each vertex gets assigned a representative that identifies which final component it belongs to. This step converts the problem from graph-based to component-based.
2. Initialize another DSU for vertices, but only allow unions that stay within the same G-component. This ensures we never accidentally merge across components that must remain separate in the final answer.
3. Iterate through all edges of F. For each edge (u, v), check whether u and v belong to the same G-component. If they do not, this edge is invalid in the final structure and contributes one required deletion. If they do, union u and v in the restricted DSU of F.
4. After processing all valid edges, we now have a partition of each G-component into several connected pieces formed by F’s allowed edges.
5. For each G-component, count how many DSU roots exist among its vertices. If a component has k such pieces, we need exactly k−1 operations to connect them into a single connected component.
6. Sum over all G-components the required merges, and add all deletions of cross-component edges. This total is the answer.

### Why it works

The correctness comes from separating the problem into two independent constraints: removing edges that violate required disconnections, and adding edges only to restore connectivity inside each required group. Once cross-component edges are removed, each G-component becomes an isolated subproblem. Inside such a subproblem, any connected structure with k components requires at least k−1 edges to become connected, and we can always achieve it because any missing edge inside the component is allowed to be added.

This gives both a lower bound and a constructive way to achieve it.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]

def solve():
    t = int(input())
    for _ in range(t):
        n, m1, m2 = map(int, input().split())

        g_dsu = DSU(n)

        edges_f = []
        for _ in range(m1):
            u, v = map(int, input().split())
            edges_f.append((u - 1, v - 1))

        for _ in range(m2):
            u, v = map(int, input().split())
            g_dsu.union(u - 1, v - 1)

        comp_vertices = [[] for _ in range(n)]
        for i in range(n):
            comp_vertices[g_dsu.find(i)].append(i)

        f_dsu = DSU(n)

        deletions = 0

        for u, v in edges_f:
            if g_dsu.find(u) != g_dsu.find(v):
                deletions += 1
            else:
                f_dsu.union(u, v)

        answer = deletions

        for comp in comp_vertices:
            roots = set()
            for v in comp:
                roots.add(f_dsu.find(v))
            if len(comp) > 0:
                answer += len(roots) - 1

        print(answer)

if __name__ == "__main__":
    solve()
```

The code first compresses graph G into components using DSU. Then it filters edges of F based on whether they respect those components. Any edge crossing components is counted immediately as a required deletion.

Inside each valid G-component, we track how F’s allowed edges split vertices into subcomponents. Each distinct DSU root corresponds to one piece, and we compute how many merges are needed to unify them.

A subtle implementation detail is that we never try to maintain global connectivity in F. We only rely on representative labels, because cross-component structure is irrelevant once filtered.

## Worked Examples

We trace a small case where G splits vertices differently from F.

Consider a case with n = 4.

F edges: (1,2), (2,3)

G edges: (1,2), (3,4)

G components are {1,2} and {3,4}.

### Trace

| Step | Action | DSU(G) components | DSU(F restricted) | deletions |
| --- | --- | --- | --- | --- |
| init | build G | {1,2}, {3,4} | all separate | 0 |
| process (1,2) | union allowed | {1,2}, {3,4} | {1,2} | 0 |
| process (2,3) | cross-edge | {1,2}, {3,4} | {1},{2},{3},{4} | 1 |

Now inside G-components:

For {1,2}, F has one component so cost 0.

For {3,4}, F has two singletons so cost 1.

Total answer is 2.

This trace shows how the algorithm cleanly separates deletion cost from internal merging cost, matching the decomposition of constraints.

A second case demonstrates a fully connected G.

F edges: none

G edges: forming a chain 1-2-3-4

All vertices are in one G-component, so we only compute connectivity inside F. Every vertex is isolated, so we have 4 components and need 3 merges. The algorithm naturally outputs 3, matching the idea that we only need to build a spanning tree inside the single group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m₁ + m₂) | DSU operations and single pass over edges and vertices |
| Space | O(n) | DSU arrays and grouping storage |

The constraints allow up to 2×10^5 total elements, so linear or near-linear DSU operations are well within limits, especially with path compression and union by size ensuring near-constant amortized time per operation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b]

    t = int(input())
    out = []

    for _ in range(t):
        n, m1, m2 = map(int, input().split())

        g = DSU(n)

        edges = []
        for _ in range(m1):
            u, v = map(int, input().split())
            edges.append((u - 1, v - 1))

        for _ in range(m2):
            u, v = map(int, input().split())
            g.union(u - 1, v - 1)

        f = DSU(n)

        del_cost = 0

        for u, v in edges:
            if g.find(u) != g.find(v):
                del_cost += 1
            else:
                f.union(u, v)

        comp = {}
        for i in range(n):
            r = g.find(i)
            comp.setdefault(r, []).append(i)

        ans = del_cost
        for nodes in comp.values():
            roots = set(f.find(x) for x in nodes)
            ans += len(roots) - 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""5
3 2 1
1 2
2 3
1 3
2 1 1
1 2
1 2
3 2 0
3 2
1 2
1 0 0
3 3 1
1 2
1 3
2 3
1 2
""") == """3
0
2
0
2"""

# custom cases
assert run("""1
4 0 0
1
""") == "0", "empty graphs"

assert run("""1
4 3 1
1 2
2 3
3 4
1 2
""") == "2", "chain mismatch"

assert run("""1
3 3 1
1 2
2 3
1 3
1 2
""") == "2", "triangle vs edge"

assert run("""1
5 0 4
1 2
2 3
3 4
4 5
""") == "4", "build full connectivity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty graphs | 0 | trivial alignment |
| chain mismatch | 2 | deletions plus merges |
| triangle vs edge | 2 | redundant edges in F |
| build full connectivity | 4 | pure construction cost |

## Edge Cases

A case where F is fully connected but G splits vertices into many components shows why deletion counting is essential. If all edges in F connect different G-components, every such edge must be removed, otherwise the final graph would incorrectly connect components that must remain separate.

Another case where G is fully connected but F has multiple components shows the opposite effect. No deletions are needed, but every disconnected piece inside F must be connected with exactly one fewer edges than its count. The algorithm naturally handles this because all vertices fall into one G-group, so only the internal DSU structure determines the answer.
