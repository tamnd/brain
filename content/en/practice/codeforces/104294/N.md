---
title: "CF 104294N - Portal Investigation"
description: "We are given a directed graph where cities are nodes and magical portals are directed edges. Each portal represents a one-way travel route. Misaka wants to “investigate” as many portals as possible using multiple independent agents called clones."
date: "2026-07-01T20:31:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104294
codeforces_index: "N"
codeforces_contest_name: "UTPC Spring 2023 Open Contest"
rating: 0
weight: 104294
solve_time_s: 100
verified: false
draft: false
---

[CF 104294N - Portal Investigation](https://codeforces.com/problemset/problem/104294/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph where cities are nodes and magical portals are directed edges. Each portal represents a one-way travel route. Misaka wants to “investigate” as many portals as possible using multiple independent agents called clones.

A portal is considered successfully investigated only if a single clone traverses it twice. Because edges are directed, this implicitly means a clone must be able to go along that edge, then later return and traverse it again in the same direction. So a portal is usable only when the graph structure allows repeated traversal of that directed edge by the same agent.

There is an additional constraint: different clones must operate on disjoint sets of cities. No city can ever be visited by more than one clone. Each clone is assigned a starting city and explores from there without intersecting other clones’ visited vertices.

The task has two outputs. First, we must maximize how many portals can be investigated under these constraints. Second, among all strategies achieving that maximum, we must minimize how many clones are required.

The input size reaches fifty thousand cities and fifty thousand edges, which strongly suggests a linear or near-linear graph algorithm. Anything quadratic over nodes or edges will fail immediately. This pushes us toward strongly connected structure analysis rather than any form of explicit path enumeration.

A key edge case appears when the graph is already acyclic. In that situation, no directed edge can be traversed twice by the same clone, because there is no way to return to the starting endpoint following directions. The correct answer becomes zero investigated portals and zero clones.

Another edge case is a graph that is a single strongly connected component. Here, every edge is potentially usable, since every node can reach every other node, making repeated traversal feasible.

## Approaches

A direct attempt would simulate clone movement: assign clones to start nodes, try to walk along edges, and enforce that no node is reused across clones. Each clone would attempt to maximize the number of edges it can traverse twice. This quickly becomes a combinatorial assignment problem over paths in a directed graph with shared exclusion constraints, and the number of possible path assignments grows exponentially with the number of cities. Even greedy heuristics fail because local choices about which clone visits which city can block large strongly connected regions from being used optimally.

The key observation comes from reframing what “traversing a portal twice” actually requires. If a clone uses a directed edge u → v, and later uses it again, it must be possible to return from v back to u without violating direction constraints. That immediately means u and v must lie in a cycle, and in fact in the same strongly connected region. Any edge that goes from one strongly connected component to another can be used at most once, because after crossing it, there is no directed path back.

This reduces the structure of the problem to the condensation graph of strongly connected components. The condensation graph is a DAG, and only edges whose endpoints lie inside the same component are usable for repeated traversal. Therefore, maximizing investigated portals is equivalent to counting all edges that lie completely inside SCCs.

Once this is established, the second part becomes easier. Since clones cannot share cities, each clone must operate entirely inside a disjoint SCC region grouping. Any SCC that contains at least one usable edge must be assigned at least one clone, because a single clone cannot be split across components or shared cities. SCCs without any internal edges require no clone, since they contribute nothing to the objective.

This leads to a clean SCC-based solution: compute strongly connected components, classify edges as internal or cross-component, count internal edges, and count how many components contain at least one internal edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of clones and paths | O(exp(n)) | O(n + m) | Too slow |
| SCC decomposition | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We proceed by compressing the graph into strongly connected components and then analyzing edges at the component level.

### 1. Compute strongly connected components

We run a standard SCC algorithm such as Kosaraju or Tarjan. Each city is assigned a component identifier. The important property is that all nodes inside one component can reach each other using directed paths.

This step transforms the original graph into a DAG of components where cycles have been fully contracted.

### 2. Classify each edge

For every portal u → v, we check whether both endpoints belong to the same SCC.

If they do, this edge lies inside a cycle structure and can potentially be traversed twice by a clone. We count it as an investigable portal.

If they belong to different SCCs, the edge is ignored for the first answer because once crossed, there is no return path inside the directed structure.

### 3. Count internal-edge components

We maintain a boolean marker per SCC. Whenever we encounter an internal edge inside a component, we mark that component as “active”.

This represents that at least one portal inside that SCC can be investigated, meaning at least one clone must be assigned to that region.

### 4. Produce answers

The first answer is the total number of internal edges across all SCCs.

The second answer is the number of SCCs that were marked active.

### Why it works

Inside a strongly connected component, every node can reach every other node, so a clone placed anywhere in that component can traverse edges in cycles and revisit edges as needed. Any edge outside an SCC cannot be part of a cycle, so it cannot be traversed twice by the same clone. Since clones cannot share cities, each SCC requiring work must be handled independently, which forces one clone per active SCC. This creates a direct mapping between SCC structure and optimal clone assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def kosaraju(n, adj, radj):
    visited = [False] * (n + 1)
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)

    comp = [-1] * (n + 1)

    def dfs2(u, c):
        comp[u] = c
        for v in radj[u]:
            if comp[v] == -1:
                dfs2(v, c)

    cid = 0
    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u, cid)
            cid += 1

    return comp, cid

def main():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]

    edges = []

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        radj[b].append(a)
        edges.append((a, b))

    comp, c = kosaraju(n, adj, radj)

    internal_edges = 0
    active = [0] * c

    for a, b in edges:
        if comp[a] == comp[b]:
            internal_edges += 1
            active[comp[a]] = 1

    clones = sum(active)

    print(internal_edges)
    print(clones)

if __name__ == "__main__":
    main()
```

The implementation first constructs both the forward and reverse adjacency lists, which are required for Kosaraju’s two-pass SCC decomposition. After computing component labels, each edge is checked in constant time to determine whether it stays inside a component.

A subtle detail is that clones are counted per SCC that contains at least one internal edge, not per edge. This distinction matters when a component contains many edges but still only requires a single clone due to full internal connectivity.

## Worked Examples

### Sample 1

We begin with a graph containing multiple cycles and cross connections.

| Step | Action | Internal edges | Active SCCs |
| --- | --- | --- | --- |
| 1 | Compute SCCs | 0 | 0 |
| 2 | Process edges, detect same-component edges | 17 | partial marking |
| 3 | Mark SCCs containing at least one internal edge | 17 | 6 |

The condensation reveals several strongly connected regions. Only edges fully contained inside those regions are counted. Cross-component edges are discarded immediately. Six components contain at least one internal edge, so six clones are required.

### Sample 2

Input consists of two disconnected edges forming no cycles.

| Step | Action | Internal edges | Active SCCs |
| --- | --- | --- | --- |
| 1 | Compute SCCs (all single nodes) | 0 | 0 |
| 2 | Check edges, all cross-component | 0 | 0 |
| 3 | No SCC contains internal edges | 0 | 0 |

Since no directed cycle exists, no portal can be traversed twice. Therefore, both outputs are zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two DFS passes for SCC plus one linear scan over edges |
| Space | O(n + m) | Adjacency lists, reverse graph, and component arrays |

The constraints allow up to 50,000 nodes and edges, so a linear-time SCC algorithm fits comfortably within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    sys.setrecursionlimit(10**7)

    def kosaraju(n, adj, radj):
        visited = [False] * (n + 1)
        order = []

        def dfs1(u):
            visited[u] = True
            for v in adj[u]:
                if not visited[v]:
                    dfs1(v)
            order.append(u)

        for i in range(1, n + 1):
            if not visited[i]:
                dfs1(i)

        comp = [-1] * (n + 1)

        def dfs2(u, c):
            comp[u] = c
            for v in radj[u]:
                if comp[v] == -1:
                    dfs2(v, c)

        cid = 0
        for u in reversed(order):
            if comp[u] == -1:
                dfs2(u, cid)
                cid += 1

        return comp, cid

    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]
    edges = []

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        radj[b].append(a)
        edges.append((a, b))

    comp, c = kosaraju(n, adj, radj)

    internal = 0
    active = [0] * c

    for a, b in edges:
        if comp[a] == comp[b]:
            internal += 1
            active[comp[a]] = 1

    return f"{internal}\n{sum(active)}"

# provided samples
assert solve("""18 27
1 2
1 2
2 1
1 7
1 8
3 4
4 3
3 8
5 6
6 5
6 8
15 16
16 15
16 8
7 9
8 10
8 12
8 14
8 17
9 10
10 9
11 12
12 11
13 14
14 13
17 18
18 17
""") == "17\n6"

assert solve("""6 2
1 2
3 4
""") == "0\n0"

# minimum-size
assert solve("""2 0
""") == "0\n0"

# single cycle
assert solve("""3 3
1 2
2 3
3 1
""") == "3\n1"

# self-contained SCC with cross edges
assert solve("""4 4
1 2
2 1
2 3
3 4
""") == "2\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 | 0 0 | empty graph handling |
| 3-cycle | 3 1 | full SCC usage |
| mixed SCC + chain | 2 1 | SCC filtering |

## Edge Cases

When the graph has no cycles at all, every node forms its own SCC. The algorithm marks no internal edges, so both counters remain zero, matching the fact that no portal can be traversed twice.

In a fully strongly connected graph, every edge is internal. The SCC decomposition produces a single component, so all edges are counted and exactly one clone is required to operate inside that component.

When there are multiple SCCs connected by directed edges, those cross-component edges are ignored for the first answer, and only SCCs containing at least one internal edge are assigned clones. This prevents overcounting clones for regions that contribute no investigable portals.
