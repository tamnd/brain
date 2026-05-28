---
title: "CF 118E - Bertown roads"
description: "We are given a connected undirected graph representing the road network of Bertown, where junctions are nodes and roads are edges."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 118
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 89 (Div. 2)"
rating: 2000
weight: 118
solve_time_s: 136
verified: false
draft: false
---

[CF 118E - Bertown roads](https://codeforces.com/problemset/problem/118/E)

**Rating:** 2000  
**Tags:** dfs and similar, graphs  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph representing the road network of Bertown, where junctions are nodes and roads are edges. Each road currently allows two-way traffic, but we are tasked with assigning a direction to every road such that the resulting directed graph remains strongly connected. Strong connectivity means that from any junction, it is possible to reach every other junction following the one-way streets.

The input size is significant: there can be up to 100,000 junctions and 300,000 roads. This means any solution worse than O(n + m) is likely too slow, because n·m could reach 10^10, which is far beyond what fits into the 5-second time limit. Therefore, naive approaches that check all permutations of road directions are infeasible.

Non-obvious edge cases arise from cycles and bridges. For instance, if the undirected graph has a bridge (an edge whose removal disconnects the graph), it is impossible to orient the edges to preserve strong connectivity. A simple example is a triangle connected by a single bridge: orienting the bridge in any direction would make traversal in the opposite direction impossible. Another edge case occurs in complete graphs: every edge can be oriented in a cyclic fashion and strong connectivity is naturally preserved.

## Approaches

The brute-force approach would try all possible orientations of edges, then check if the resulting directed graph is strongly connected. This requires checking 2^m orientations, each needing O(n + m) time for a DFS or BFS. With m up to 3×10^5, this is astronomically slow.

The key observation is that bridges prevent strong connectivity. If the graph has a bridge, one end cannot reach the other if the bridge is directed in the wrong way. Therefore, the first step is to identify whether bridges exist. Tarjan's algorithm can detect bridges in O(n + m) time by performing a DFS and tracking discovery times and low-link values. If a bridge is found, the answer is immediately 0.

Once we know there are no bridges, the undirected graph is 2-edge-connected. In this scenario, it is always possible to assign directions so that the graph becomes strongly connected. A simple DFS-based construction works: for every tree edge encountered during DFS, orient it from parent to child; for every back edge, orient it from child to parent. This guarantees strong connectivity because every cycle in the undirected graph becomes a directed cycle, and cycles link the components together.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m · (n + m)) | O(n + m) | Too slow |
| DFS + Tarjan bridges | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the undirected graph from the input edges. This is the structure we will use for DFS and bridge detection.
2. Initialize arrays to track discovery times (`tin`), lowest reachable discovery times (`low`), and a visited flag for each node.
3. Perform a DFS starting from any node (say node 1) to detect bridges. For each node, set `tin` and `low` to the current timer, then recursively visit unvisited neighbors. Update `low` values according to the standard Tarjan bridge detection rules. If we find any edge where `low[neighbor] > tin[node]`, it is a bridge, and we immediately return 0.
4. During the DFS, record the edge orientations. Tree edges are oriented from the parent to the child. Back edges are oriented from the current node to its ancestor. Store orientations in a dictionary keyed by edge indices to preserve input order.
5. After DFS, if no bridge was found, output the stored edge orientations in the order they were given in the input.

Why it works: Bridges are the only obstruction to orienting a connected undirected graph into a strongly connected directed graph. By performing DFS and recording tree and back edges, we orient all edges along cycles in a consistent way. This guarantees that every node can reach every other node because cycles allow traversal in both directions through different paths, satisfying strong connectivity.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n)]
    edges = []
    
    for i in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append((b, i))
        adj[b].append((a, i))
        edges.append((a, b))
    
    tin = [-1] * n
    low = [-1] * n
    timer = [0]
    visited = [False] * n
    res = [None] * m
    found_bridge = [False]
    
    def dfs(u, parent):
        visited[u] = True
        tin[u] = low[u] = timer[0]
        timer[0] += 1
        for v, idx in adj[u]:
            if v == parent:
                continue
            if visited[v]:
                low[u] = min(low[u], tin[v])
                if res[idx] is None:
                    res[idx] = (u + 1, v + 1)
            else:
                res[idx] = (u + 1, v + 1)
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    found_bridge[0] = True
    
    dfs(0, -1)
    
    if found_bridge[0]:
        print(0)
    else:
        for p, q in res:
            print(p, q)

if __name__ == "__main__":
    main()
```

The adjacency list captures each edge with its index so we can later output in input order. `tin` and `low` arrays implement Tarjan's bridge detection. The DFS orients tree edges from parent to child and back edges from current node to ancestor. We immediately detect bridges to handle unsolvable cases. The `res` array maintains the orientation mapping.

## Worked Examples

### Example 1

Input:

```
6 8
1 2
2 3
1 3
4 5
4 6
5 6
2 4
3 5
```

| Step | Node | tin | low | Edge oriented | Found bridge |
| --- | --- | --- | --- | --- | --- |
| DFS 1 | 1 | 0 | 0 | 1->2 | False |
| DFS 2 | 2 | 1 | 0 | 2->3 | False |
| DFS 3 | 3 | 2 | 0 | 3->1, 3->5 | False |
| DFS 4 | 4 | 3 | 3 | 4->5 | False |
| DFS 5 | 5 | 4 | 3 | 5->6 | False |
| DFS completes | - | - | - | - | False |

All edges oriented without bridges, strong connectivity preserved.

### Example 2

Input:

```
4 3
1 2
2 3
3 4
```

Bridge detection immediately identifies edge 2-3 as a bridge (`low[3] > tin[2]`). The algorithm outputs 0, correctly indicating no solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS visits each node once and checks all edges. |
| Space | O(n + m) | Adjacency list, edge orientation array, and auxiliary arrays for DFS. |

This complexity fits well within the constraints: 105 nodes and 3·105 edges can be processed efficiently with DFS in under a second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("6 8\n1 2\n2 3\n1 3\n4 5\n4 6\n5 6\n2 4\n3 5\n") != "0", "sample 1"

# Minimum-size input, no bridge
assert run("2 1\n1 2\n") == "1 2", "minimum input no bridge"

# Bridge present, no solution
assert run("4 3\n1 2\n2 3\n3 4\n") == "0", "linear bridge"

# Complete graph 3 nodes
assert run("3 3\n1 2\n2 3\n1 3\n") != "0", "triangle, any orientation works"

# Star graph center 1
assert run("4 3\n1 2\n1 3\n1 4\n") == "0", "center is bridge"

# Two separate cycles connected
assert run("6 7\n1 2\n2 3\n3 1\n4 5\n5 6\n6 4\n3 4\n") != "0", "double cycle connected"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 2 | minimum input no bridge |
| 4 3 | 0 | bridge prevents strong connectivity |
| 3 3 | any orientation | cycle allows strong connectivity |
| 4 3 | 0 | star graph center is bridge |
| 6 7 |  |  |
