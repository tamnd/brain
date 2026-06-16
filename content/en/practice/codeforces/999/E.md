---
title: "CF 999E - Reachability from the Capital"
description: "We are given a directed graph where cities are nodes and roads are one-way edges. One city is designated as the capital. The goal is to ensure that every city can be reached by following directed roads starting from the capital."
date: "2026-06-16T23:52:51+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 999
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 490 (Div. 3)"
rating: 2000
weight: 999
solve_time_s: 75
verified: true
draft: false
---

[CF 999E - Reachability from the Capital](https://codeforces.com/problemset/problem/999/E)

**Rating:** 2000  
**Tags:** dfs and similar, graphs, greedy  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where cities are nodes and roads are one-way edges. One city is designated as the capital. The goal is to ensure that every city can be reached by following directed roads starting from the capital. If a city is not reachable, we are allowed to add new directed roads, and we want to minimize how many we add.

The core task is not to compute reachability itself, but to determine the minimum number of new directed edges that must be inserted so that the capital can eventually reach every node in the graph.

The constraints are small enough for graph algorithms that are linear or near-linear in the number of vertices and edges. With n and m both up to 5000, an O(n²) or O(nm) solution is acceptable in principle, but anything cubic or that repeatedly recomputes reachability from scratch will not scale.

A subtle issue appears when the graph contains strongly connected components. Inside a strongly connected component, every node is mutually reachable, so treating nodes individually leads to redundant reasoning. The correct abstraction is that only the structure between strongly connected components matters.

A naive approach might try simulating adding edges greedily, repeatedly running a reachability search and connecting the capital to new nodes. This fails in cases where multiple unreachable regions depend on each other indirectly. For example, if the graph has several SCCs arranged in a DAG, connecting one node in a component may unlock many others, and greedy local decisions can overcount or undercount without recognizing this structure.

## Approaches

A direct but inefficient strategy is to repeatedly run a BFS or DFS from the capital, mark all reachable nodes, then pick an unreachable node and add a road from the capital to it, repeating until everything is reachable. Each addition changes reachability, so we recompute from scratch. In the worst case, we may add O(n) edges, and each reachability computation costs O(n + m), leading to O(n(n + m)) time, which is too slow at the upper bound.

The key insight is that reachability inside strongly connected components does not matter individually. Once we contract each strongly connected component into a single node, the graph becomes a directed acyclic graph (DAG). In a DAG, reachability from the capital depends only on which components are reachable from the capital component.

Now the problem becomes: in this DAG, which components are unreachable from the capital component, and how many edges do we need to add so that all components become reachable from it? Each added edge can start in any reachable component and go to any unreachable component, so effectively we want to connect unreachable parts of the DAG.

A well-known property of DAGs helps here. If we consider the condensation graph, every weakly connected region that is not reachable from the source requires at least one incoming edge from the reachable side. The minimum number of edges required equals the number of source components in the subgraph of unreachable components, when viewed in terms of connectivity from the reachable region.

Practically, we solve this by computing strongly connected components, building the condensed DAG, marking which components are reachable from the capital, and then counting how many unreachable components have no incoming edge from another unreachable component. Each such component must receive at least one new edge.

This reduces the problem to SCC decomposition plus a linear scan over the condensed graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated DFS/BFS with edge additions | O(n(n + m)) | O(n + m) | Too slow |
| SCC + condensation graph analysis | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We first compress the graph into strongly connected components using Kosaraju’s algorithm or Tarjan’s algorithm. This step groups nodes that are mutually reachable into single units, because within such a group, reachability is already guaranteed and does not require any new edges.

Next, we build the condensation graph where each SCC becomes a node and edges represent connections between components. This graph is guaranteed to be a DAG, since cycles have been contracted.

We then identify the SCC that contains the capital. From this component, we perform a DFS or BFS over the condensation graph to mark all components that are already reachable.

After that, we focus only on components that are not marked reachable. Among these unreachable components, we compute which ones have no incoming edge from any reachable component. Each such component represents a region that cannot be reached indirectly and therefore requires at least one new edge to be connected.

Finally, we count these components and output the result.

### Why it works

After contraction into SCCs, the graph becomes a DAG, and reachability behaves like traversal in a partial order. Any node in a reachable SCC can reach all nodes in its component and all SCCs downstream. If an SCC is unreachable, it must lie in a different DAG region with no path from the capital’s component.

If an unreachable SCC has an incoming edge from another unreachable SCC, it can be reached once that upstream SCC is connected. Therefore only SCCs with no incoming edges from within the unreachable subgraph are independent “entry points” that require explicit connection. Each such SCC needs at least one new edge, and one edge is sufficient because it can connect from any reachable SCC. This establishes both lower bound and construction optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def kosaraju(n, g, rg):
    visited = [False] * n
    order = []

    def dfs1(v):
        visited[v] = True
        for to in g[v]:
            if not visited[to]:
                dfs1(to)
        order.append(v)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    comp = [-1] * n
    cid = 0

    def dfs2(v, c):
        comp[v] = c
        for to in rg[v]:
            if comp[to] == -1:
                dfs2(to, c)

    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, cid)
            cid += 1

    return comp, cid

def solve():
    n, m, s = map(int, input().split())
    s -= 1

    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        rg[v].append(u)

    comp, k = kosaraju(n, g, rg)

    cg = [[] for _ in range(k)]
    indeg = [0] * k

    for u in range(n):
        for v in g[u]:
            if comp[u] != comp[v]:
                cg[comp[u]].append(comp[v])

    cap = comp[s]

    reachable = [False] * k
    stack = [cap]
    reachable[cap] = True

    while stack:
        v = stack.pop()
        for to in cg[v]:
            if not reachable[to]:
                reachable[to] = True
                stack.append(to)

    indeg_unreach = [0] * k

    for u in range(n):
        cu = comp[u]
        if reachable[cu]:
            continue
        for v in g[u]:
            cv = comp[v]
            if not reachable[cv]:
                indeg_unreach[cv] += 1

    ans = 0
    for c in range(k):
        if not reachable[c] and indeg_unreach[c] == 0:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds both the original and reversed graphs for SCC decomposition. After computing component labels, it builds the condensation graph implicitly and explores reachability from the capital component.

A key implementation detail is separating reachable and unreachable SCCs before counting incoming edges. This prevents overcounting edges that originate from already reachable regions, which do not matter for connecting the remaining graph.

The final counting step only considers SCCs that are unreachable and have zero incoming edges from other unreachable SCCs, which corresponds exactly to independent components that must be directly connected.

## Worked Examples

### Example 1

Input:

```
9 9 1
1 2
1 3
2 3
1 5
5 6
6 1
1 8
9 8
7 1
```

After SCC decomposition, assume each node is its own component except cycles like (1,5,6). We track reachability from component of 1.

| Step | Action | Reachable SCCs |
| --- | --- | --- |
| 1 | Start from SCC(1) | {1} |
| 2 | Traverse condensation edges | {1,2,3,5,6,8} |
| 3 | Mark unreachable SCCs | {4,7,9} |
| 4 | Count SCCs with no incoming from unreachable | 3 |

The result is 3, matching the need to connect three independent unreachable regions.

This confirms that only independent unreachable SCC sources matter, not all nodes.

### Example 2 (constructed)

Input:

```
5 2 5
5 4
4 3
```

Here node 5 can reach 4 and 3, but nodes 1 and 2 are isolated.

| Step | Action | Reachable SCCs |
| --- | --- | --- |
| 1 | Start from SCC(5) | {5,4,3} |
| 2 | Remaining SCCs | {1,2} |
| 3 | Count independent unreachable SCCs | 2 |

Two edges are needed, one to reach SCC(1), one to reach SCC(2).

This shows that disconnected components each require at least one incoming connection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | SCC computation and graph traversal each run in linear time over vertices and edges |
| Space | O(n + m) | adjacency lists, reverse graph, component arrays, and auxiliary structures |

The constraints allow up to 5000 nodes and edges, and a linear-time SCC approach is comfortably within limits. The memory usage is also well within the 256 MB bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import ModuleType

    # assumes solution is defined in same file context
    return _sys.stdout.getvalue() if False else ""

# Since full harness integration isn't possible in this static format,
# below are logical assert-style cases for reference.

# sample 1
# assert run("""9 9 1
# 1 2
# 1 3
# 2 3
# 1 5
# 5 6
# 6 1
# 1 8
# 9 8
# 7 1
# """) == "3"

# minimal case
# assert run("""1 0 1
# """) == "0"

# disconnected nodes
# assert run("""3 0 1
# """) == "2"

# already strongly connected
# assert run("""3 3 1
# 1 2
# 2 3
# 3 1
# """) == "0"

# reversed chain
# assert run("""4 3 4
# 4 3
# 3 2
# 2 1
# """) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | trivial base case |
| no edges | n-1 | worst disconnected case |
| cycle graph | 0 | SCC collapse behavior |
| reversed path | 0 | full reachability from tail |

## Edge Cases

One edge case is when the capital lies in a sink component of the condensation graph. In this situation, no outgoing edges exist from its SCC, so only nodes inside its SCC are reachable. The algorithm marks only that component as reachable, and every other SCC without incoming reachability becomes counted. This correctly yields one required connection per independent unreachable region.

Another case is when the graph is already strongly connected. After SCC compression, there is only one component. The reachability step marks it as reachable immediately, and the final count finds no unreachable components, returning zero without performing any unnecessary counting.

A third case is when there are multiple small disconnected SCCs with no edges at all. Each SCC has zero incoming edges from reachable components, so each is counted once. The algorithm correctly interprets each as requiring one direct connection from the capital region.
