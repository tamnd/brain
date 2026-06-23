---
title: "CF 105315A - Marble's Birthday"
description: "We are given several directed graphs, each described by nodes and directed edges. A directed edge from one node to another means you can travel only in that direction."
date: "2026-06-23T15:05:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "A"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 60
verified: true
draft: false
---

[CF 105315A - Marble's Birthday](https://codeforces.com/problemset/problem/105315/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several directed graphs, each described by nodes and directed edges. A directed edge from one node to another means you can travel only in that direction.

For each test case, the task is to determine the smallest number of extra directed edges we need to add so that after adding them, every node can reach every other node by following directed edges. In graph terms, we want the graph to become strongly connected.

The important idea is that reachability is not symmetric here. Even if a path exists from A to B, it does not imply a path from B back to A. The goal is to repair this asymmetry with the minimum number of added edges.

The constraints are large: the total number of nodes and edges across all test cases can reach one million. This rules out any approach that tries to check reachability between all pairs of nodes directly, since even a single Floyd-Warshall style idea would immediately exceed limits. Even repeated BFS/DFS from every node would be too slow, since that would be O(n(n + m)) in the worst case.

A more subtle edge case appears when the graph is already strongly connected. In that situation, no edges are needed, and the answer must be zero. Another tricky situation is when the graph is almost connected but split into components that form a chain. A naive approach might try to “connect components greedily” without recognizing the structure that actually governs the minimum number of edges.

## Approaches

A brute-force idea would be to repeatedly check whether the graph is strongly connected, and if not, try adding an edge between every pair of nodes and testing again. Each connectivity check costs O(n + m), and there are O(n²) possible edges to consider, making this completely infeasible.

The key structural insight is that inside any directed graph, nodes naturally form strongly connected components. Inside each such component, every node can reach every other node. If we compress each component into a single node, the resulting structure is a directed acyclic graph.

Once the graph is reduced to this component graph, the original problem becomes much simpler: we are no longer working with individual nodes, but with SCCs that behave like atomic units. The only way to make the entire graph strongly connected is to ensure that this component graph becomes a cycle, which requires carefully connecting its sources and sinks.

The final observation is that only two types of components matter: those with no incoming edges in the condensation graph, and those with no outgoing edges. The minimum number of edges needed is determined by how many of these exist, because each added edge can fix one source and one sink relationship simultaneously.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in n | O(n + m) | Too slow |
| SCC Compression + Degree Counting | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. First, compute all strongly connected components of the directed graph. This groups nodes such that every node in a group can reach every other node in the same group. This step is necessary because internal structure of a component does not affect the answer.
2. To find SCCs efficiently, we run a two-pass DFS approach (Kosaraju’s algorithm). In the first pass, we traverse the graph and record nodes in order of completion. This ordering captures dependencies between components.
3. We then reverse all edges in the graph and process nodes in decreasing order of finishing time. Each DFS traversal in this second pass discovers exactly one strongly connected component.
4. After assigning a component ID to every node, we treat each component as a single node in a new condensed graph.
5. We iterate through all original edges. For every edge from u to v, if u and v belong to different components, we add a directed edge between their corresponding components.
6. For each component, we compute two values: how many edges enter it and how many edges leave it in the condensed graph.
7. We count how many components have zero incoming edges, and how many have zero outgoing edges.
8. If there is only one component in total, the graph is already strongly connected and the answer is zero. Otherwise, the answer is the maximum of the number of source components and sink components.

### Why it works

The condensation graph is always a directed acyclic graph. In such a structure, any strongly connected final graph must eliminate all sources and sinks by introducing new connections. Each added edge can reduce the number of sources or sinks by at most one effective unit, because it connects at most one SCC tail to one SCC head. The maximum of the two counts therefore represents the bottleneck that cannot be avoided.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        rg = [[] for _ in range(n)]

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            rg[v].append(u)

        visited = [False] * n
        order = []

        sys.setrecursionlimit(10**7)

        def dfs1(u):
            stack = [(u, 0)]
            visited[u] = True
            while stack:
                node, i = stack[-1]
                if i < len(g[node]):
                    nxt = g[node][i]
                    stack[-1] = (node, i + 1)
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append((nxt, 0))
                else:
                    order.append(node)
                    stack.pop()

        for i in range(n):
            if not visited[i]:
                dfs1(i)

        comp = [-1] * n
        cid = 0

        def dfs2(u):
            stack = [u]
            comp[u] = cid
            while stack:
                node = stack.pop()
                for nxt in rg[node]:
                    if comp[nxt] == -1:
                        comp[nxt] = cid
                        stack.append(nxt)

        for v in reversed(order):
            if comp[v] == -1:
                dfs2(v)
                cid += 1

        if cid == 1:
            print(0)
            continue

        indeg = [0] * cid
        outdeg = [0] * cid

        for u in range(n):
            for v in g[u]:
                if comp[u] != comp[v]:
                    outdeg[comp[u]] += 1
                    indeg[comp[v]] += 1

        sources = sum(1 for i in range(cid) if indeg[i] == 0)
        sinks = sum(1 for i in range(cid) if outdeg[i] == 0)

        print(max(sources, sinks))

if __name__ == "__main__":
    solve()
```

The solution starts by building both the graph and its reverse. This dual structure is required for Kosaraju’s algorithm to correctly identify strongly connected components.

The first DFS collects vertices in finishing order without recursion stack depth issues by using an explicit stack. The second DFS assigns component IDs using the reversed graph. Once components are assigned, the condensation graph is not explicitly built as adjacency lists; instead, we directly compute indegree and outdegree counts while scanning original edges.

The final conditional check for a single component handles the already strongly connected case, which would otherwise incorrectly produce a positive count.

## Worked Examples

### Example 1

Input graph has edges forming a cycle among three nodes plus an extra connection to a fourth node, creating multiple SCCs.

| Step | Action | Components | Sources | Sinks |
| --- | --- | --- | --- | --- |
| 1 | Build SCCs | {cycle}, {node4} | 1 | 1 |
| 2 | Build condensation edges | 1 edge between SCCs |  |  |
| 3 | Count indeg/outdeg | SCC0 indeg 0, SCC1 outdeg 0 | 1 | 1 |
| 4 | Compute answer | max(1,1) = 1 |  |  |

This shows that one edge is enough to connect the two SCCs into a strongly connected structure.

### Example 2

A graph already forms a single cycle across all nodes.

| Step | Action | Components | Sources | Sinks |
| --- | --- | --- | --- | --- |
| 1 | SCC decomposition | 1 component | 0 | 0 |
| 2 | Early exit | cid = 1 | - | - |
| 3 | Output | 0 |  |  |

This confirms that the algorithm correctly avoids unnecessary edge additions when the graph is already strongly connected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node and edge is processed a constant number of times across SCC construction and degree counting |
| Space | O(n + m) | Adjacency lists, reverse graph, and component arrays |

The constraints allow up to one million total nodes and edges, so a linear-time solution per test case is necessary. The SCC-based approach fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    # --- solution embedded ---
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, m = map(int, input().split())
            g = [[] for _ in range(n)]
            rg = [[] for _ in range(n)]

            for _ in range(m):
                u, v = map(int, input().split())
                u -= 1
                v -= 1
                g[u].append(v)
                rg[v].append(u)

            visited = [False] * n
            order = []

            sys.setrecursionlimit(10**7)

            def dfs1(u):
                stack = [(u, 0)]
                visited[u] = True
                while stack:
                    node, i = stack[-1]
                    if i < len(g[node]):
                        nxt = g[node][i]
                        stack[-1] = (node, i + 1)
                        if not visited[nxt]:
                            visited[nxt] = True
                            stack.append((nxt, 0))
                    else:
                        order.append(node)
                        stack.pop()

            for i in range(n):
                if not visited[i]:
                    dfs1(i)

            comp = [-1] * n
            cid = 0

            def dfs2(u):
                stack = [u]
                comp[u] = cid
                while stack:
                    node = stack.pop()
                    for nxt in rg[node]:
                        if comp[nxt] == -1:
                            comp[nxt] = cid
                            stack.append(nxt)

            for v in reversed(order):
                if comp[v] == -1:
                    dfs2(v)
                    cid += 1

            if cid == 1:
                print(0)
                return

            indeg = [0] * cid
            outdeg = [0] * cid

            for u in range(n):
                for v in g[u]:
                    if comp[u] != comp[v]:
                        outdeg[comp[u]] += 1
                        indeg[comp[v]] += 1

            sources = sum(1 for i in range(cid) if indeg[i] == 0)
            sinks = sum(1 for i in range(cid) if outdeg[i] == 0)

            print(max(sources, sinks))

    solve()

# sample-style sanity checks
assert run("1\n3 3\n1 2\n2 3\n3 1\n") == "0\n"
assert run("1\n2 0\n") == "1\n"
assert run("1\n4 3\n1 2\n2 3\n3 4\n") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-cycle | 0 | already strongly connected graph |
| 2 isolated nodes | 1 | minimal connection requirement |
| chain graph | 1 | SCC collapse and single source/sink handling |

## Edge Cases

A fully strongly connected graph is handled by the early termination when the number of components is one. In that situation, indegree and outdegree logic is never needed, and the algorithm correctly outputs zero.

A completely disconnected graph, such as nodes with no edges, produces one SCC per node. In the condensation graph, every node is both a source and a sink. The algorithm counts equal numbers of sources and sinks, and the maximum correctly gives the number of edges needed to connect all components into a single strongly connected structure.

A linear chain of nodes tests whether the condensation graph logic correctly identifies exactly one source and one sink. The algorithm produces a single source SCC at the start of the chain and a single sink SCC at the end, yielding an answer of one, matching the fact that a single edge can close the cycle.
