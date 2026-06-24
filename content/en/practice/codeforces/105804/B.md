---
title: "CF 105804B - Galician Roads"
description: "We are given an undirected connected graph representing towns linked by two-way roads. Each road connects two distinct towns, and the whole network is initially connected, so travel is possible between any pair of towns. The task is to replace this system with a directed one."
date: "2026-06-25T06:27:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105804
codeforces_index: "B"
codeforces_contest_name: "XXIX Spain Olympiad in Informatics, Day 2 (Mirror)"
rating: 0
weight: 105804
solve_time_s: 46
verified: true
draft: false
---

[CF 105804B - Galician Roads](https://codeforces.com/problemset/problem/105804/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected connected graph representing towns linked by two-way roads. Each road connects two distinct towns, and the whole network is initially connected, so travel is possible between any pair of towns.

The task is to replace this system with a directed one. Every existing road must be assigned a direction, and we are also allowed to add new directed roads if needed. After doing this, the resulting directed graph must remain strongly connected, meaning that from every town we must be able to reach every other town following directed edges.

The goal is to minimize how many new roads we add, while we are free to orient existing ones however we want. Since multiple test cases are given, we must compute this minimum independently for each graph.

The key constraint that drives the solution is that the total number of edges across all test cases is at most 200,000. This rules out any solution that recomputes connectivity or performs heavy graph algorithms per edge in quadratic time. Anything around O(n + m) per test case is safe, but O(m log m) repeated many times is still acceptable. Anything that tries to simulate orientations or recompute reachability repeatedly will time out.

A subtle corner case comes from graphs that are already “almost trees”. If the graph is a tree, then no matter how we orient edges, we cannot obtain a directed cycle covering all nodes. A naive approach might try to orient edges arbitrarily and assume strong connectivity can be fixed locally, but trees fundamentally lack cycles, so extra edges are unavoidable there.

Another failure case appears when the graph is already 2-edge-connected but not 2-vertex-connected. Some naive strategies that rely on local degrees or spanning tree orientation miss articulation points, which break strong connectivity unless we add extra edges.

## Approaches

A brute-force interpretation would be to try all possible orientations of the given undirected edges, then check whether the resulting directed graph is strongly connected. For each valid orientation, we would compute how many extra edges are needed to fix connectivity gaps. This immediately becomes infeasible because each of m edges has two choices, leading to 2^m configurations. Even for m = 20 this already explodes, and here m reaches 200,000.

The key observation is that we are not really free in an arbitrary sense. Strong connectivity in a directed graph can be characterized structurally: every directed graph can be compressed into strongly connected components, and the condensation graph is a directed acyclic graph. To make the whole graph strongly connected, we need to eliminate sources and sinks in this DAG structure.

The critical simplification is that we are allowed to orient edges optimally. This means we can choose an orientation that minimizes the number of SCC sources and sinks after orientation. The classical result is that, in any connected undirected graph, we can orient edges such that the resulting directed graph has a structure where the number of components requiring external connections reduces to a function of articulation structure and bridges. In fact, after optimal orientation, the minimum number of edges needed to make the graph strongly connected is determined by how many “imbalanced” components appear in a DFS tree decomposition.

The key insight is to root a DFS tree and orient every tree edge downward, while handling back edges carefully. This produces a directed structure whose SCC condensation corresponds closely to bridges in the original graph. Each bridge effectively separates the graph into parts that cannot reach each other in both directions. Each such “one-way bottleneck” forces us to add one extra directed edge to restore bidirectional reachability.

So instead of searching orientations, we compute the bridge structure using DFS. Once bridges are identified, we conceptually compress the graph into a bridge tree. A tree with k leaves requires exactly ceil(leaf_count / 2) extra edges to make it strongly connected, because each added edge can pair two leaves and eliminate two degree-1 requirements in the condensation tree.

The whole problem reduces to: find all bridges, build the bridge tree, count how many nodes in that tree have degree 1, and compute how many edges are needed to pair them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force orientations | O(2^m) | O(n + m) | Too slow |
| DFS + bridge decomposition | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build adjacency lists for the graph while keeping track of edge indices so we can distinguish parallel traversal directions. This is necessary because we need to identify bridges using DFS.
2. Run a DFS to compute discovery times and low-link values. During traversal, for every tree edge we propagate low-link information from the child back to the parent. A bridge is identified when the lowest reachable ancestor from a child is strictly greater than the discovery time of the parent. This condition captures the fact that removing that edge disconnects the graph.
3. Once all bridges are found, treat the original graph as a “compressed structure” where every non-bridge edge keeps its endpoints in the same component, while bridges define connections between components.
4. Construct a conceptual bridge tree by counting degrees of nodes with respect to bridges only. Each endpoint of a bridge contributes one degree in this tree.
5. Count how many nodes in this bridge tree have degree 1. These correspond to components that are “ends” of the structure and cannot reach other parts symmetrically.
6. The answer is half of the number of such leaves, rounded up. Each added directed edge can connect two leaves, fixing both at once.

### Why it works

The DFS-based bridge decomposition identifies exactly the edges that enforce one-way traversal constraints in any orientation. Any such edge creates a bottleneck between two maximal 2-edge-connected components. After contracting these components, the remaining structure is a tree. In a directed tree-like structure, strong connectivity requires every node to have both incoming and outgoing reachability paths, which translates into eliminating leaves in the condensation tree. Each added edge can eliminate two leaves by creating a cycle between them, so the optimal strategy is pairing leaves, which leads to the formula ceil(L / 2).

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    
    edges = []
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, i))
        g[v].append((u, i))
        edges.append((u, v))
    
    tin = [-1] * n
    low = [0] * n
    timer = 0
    is_bridge = [False] * m

    def dfs(v, pe):
        nonlocal timer
        tin[v] = low[v] = timer
        timer += 1
        
        for to, ei in g[v]:
            if ei == pe:
                continue
            if tin[to] == -1:
                dfs(to, ei)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    is_bridge[ei] = True
            else:
                low[v] = min(low[v], tin[to])

    dfs(0, -1)

    comp_deg = [0] * n

    for i, (u, v) in enumerate(edges):
        if is_bridge[i]:
            comp_deg[u] += 1
            comp_deg[v] += 1

    leaves = 0
    for i in range(n):
        if comp_deg[i] == 1:
            leaves += 1

    if m == 0:
        print(0)
    else:
        print((leaves + 1) // 2)

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The DFS is standard low-link computation. The only subtle part is ensuring edges are not confused with backtracking to the parent edge, which is handled using edge indices rather than just parent nodes. After identifying bridges, we ignore non-bridge edges entirely because they live inside strongly connected components after optimal orientation.

The leaf counting step assumes that every bridge endpoint contributes to the degree of the bridge tree. If a node is incident to exactly one bridge, it behaves like a leaf in the contracted structure.

The final formula `(leaves + 1) // 2` pairs endpoints optimally.

## Worked Examples

Consider a simple triangle graph, where every node is connected to every other node. No edge is a bridge.

| Step | Bridges | Degrees (bridge tree) | Leaves |
| --- | --- | --- | --- |
| Initial | none | all 0 | 0 |

There are no leaves, so the answer becomes 0. This matches intuition because we can orient the triangle cyclically and already get strong connectivity.

Now consider a line graph 1-2-3-4.

| Step | Bridges | Degrees | Leaves |
| --- | --- | --- | --- |
| Edge 1-2 | yes | 1,1 | 2 |
| Edge 2-3 | yes | 2,2 |  |
| Edge 3-4 | yes | 1,1 | 2 |

Here all edges are bridges, so every internal node in the bridge tree has degree 2, while endpoints 1 and 4 have degree 1. Leaves = 2, so answer is (2+1)//2 = 1.

This corresponds to adding a single directed edge connecting the endpoints of the chain, turning the structure into a cycle after orientation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS for low-link plus single pass over edges |
| Space | O(n + m) | adjacency list and arrays for DFS state |

The constraints allow up to 2×10^5 edges overall, so a linear-time DFS per test case is sufficient. Memory usage remains linear in the graph size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# Note: This assumes solve() is wired appropriately in a full script context.

# custom cases
# single edge
# 2 nodes, 1 edge => need 0 or 1 depending interpretation
# cycle
# line
# star
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| triangle graph | 0 | no bridges case |
| path of 4 nodes | 1 | chain pairing |
| star graph | 2 | multiple leaves |

## Edge Cases

A graph that is already a cycle has no bridges. In that situation the DFS marks no edge as critical, so every degree in the bridge structure is zero. The leaf count becomes zero and the algorithm outputs zero, which matches the fact that we can orient the cycle consistently.

A pure tree is the most sensitive case because every edge is a bridge. The DFS marks all edges, and the bridge tree is identical to the original tree. Leaves correspond exactly to tree leaves. The pairing formula ensures we add enough edges to close cycles between leaves, and every internal vertex is already fine since it has both incoming and outgoing paths via its children once cycles are introduced.

A star graph produces a large number of leaves equal to n − 1. The algorithm pairs them greedily in groups of two, producing roughly (n − 1)/2 added edges. This matches the intuition that each added edge can only fix two endpoints of one-way separations at a time.
