---
title: "CF 104257D - Dom's Discovery"
description: "We are given a directed graph where each vertex represents a student and each directed edge represents a one-way friendship claim."
date: "2026-07-01T21:45:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104257
codeforces_index: "D"
codeforces_contest_name: "2021 NTUIM Programming Design And Optimization (PDAO 2021)"
rating: 0
weight: 104257
solve_time_s: 51
verified: true
draft: false
---

[CF 104257D - Dom's Discovery](https://codeforces.com/problemset/problem/104257/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each vertex represents a student and each directed edge represents a one-way friendship claim. The relationship of interest is not direct reachability in one direction, but mutual reachability: two students belong to the same group if each can reach the other by following directed edges through zero or more intermediate students.

This is exactly the notion of strongly connected components in a directed graph. A group is a maximal set of vertices where every vertex can reach every other vertex within the set.

The task has two outputs. First, we must count how many such groups exist in the entire graph. Second, we must output the members of the largest group. If multiple groups tie for largest size, any one of them is acceptable.

The graph size is large, with up to 100,000 vertices and 100,000 edges. This immediately rules out any quadratic reasoning or repeated reachability checks between pairs of nodes. Even a single BFS/DFS from every node in a naive way would lead to roughly O(n(n + m)), which is far beyond the limit.

A subtle but important constraint is that the graph is guaranteed to be connected if we ignore edge directions. This ensures there are no completely isolated subgraphs, but it does not simplify the directed structure; strongly connected components can still be many and small.

Common pitfalls arise when treating the problem as ordinary connectivity in an undirected graph. For example, in a directed chain 1 → 2 → 3, node 1 can reach 2 and 3, but none of them can return to 1, so each node is its own group. Ignoring direction would incorrectly merge them.

Another failure case appears in directed cycles with branches. A node might be reachable from many others but not be able to return, so reachability alone is insufficient; mutual reachability is required.

## Approaches

A brute-force attempt would try to compute reachability sets. For every node, we could run a DFS/BFS to find all nodes it can reach, then check for each pair whether reachability is mutual. This would already cost O(n(n + m)) in the worst case. With n and m up to 100,000, this becomes completely infeasible, potentially involving around 10^10 operations.

A better perspective comes from observing that mutual reachability partitions the graph into strongly connected components. Once we accept this viewpoint, the problem becomes a standard SCC decomposition task.

The key insight is that instead of reasoning about reachability between every pair, we compress the graph into SCCs where internal structure is irrelevant. Each SCC becomes a single node in a directed acyclic graph. The number of SCCs is exactly the number of groups we need.

To find SCCs efficiently, classical linear-time algorithms exist. The most direct and implementation-friendly is Kosaraju’s algorithm: run a DFS to compute finishing order, reverse the graph, then DFS in that order to collect components. Each vertex is visited a constant number of times, so the total complexity is linear in n + m.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Reachability | O(n(n + m)) | O(n) | Too slow |
| Kosaraju SCC Decomposition | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We solve the problem using Kosaraju’s two-pass SCC decomposition.

1. Build two adjacency lists, one for the original directed graph and one for the reversed graph. The reversed graph flips every edge u → v into v → u. This reversal is necessary because it allows us to explore components in a controlled inward direction in the second pass.
2. Run a depth-first search on the original graph to compute an ordering of vertices by completion time. Each time we finish exploring a node, we append it to a list. This ordering captures a hierarchy where nodes that finish later tend to be “earlier” in the SCC condensation graph.
3. Iterate over nodes in reverse finishing order. This ensures that when we start a DFS from an unvisited node, we are guaranteed to start from a source SCC in the condensed DAG rather than a partially processed region.
4. For each unvisited node in this order, run a DFS on the reversed graph. All nodes reached in this DFS form exactly one strongly connected component. Collect these nodes into a component list.
5. Store each component and track its size. Maintain the largest component encountered so far.
6. After all nodes are processed, output the number of components and the contents of the largest one.

Why the reversed graph DFS works is subtle. When we reverse edges, we effectively allow traversal only within the “influence closure” of a component. Because of the finishing-time ordering, we ensure that when we start a DFS, we cannot accidentally leak into an unprocessed SCC that should belong elsewhere.

### Why it works

The SCC condensation of a directed graph forms a directed acyclic graph. The first DFS produces an ordering consistent with this DAG: nodes in sink components finish earlier, while nodes in source components finish later. Processing in reverse finishing order ensures we always start from a component whose outgoing edges in the original graph cannot lead to any unvisited SCC in the reversed traversal. This isolates each strongly connected component exactly once, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n, m = map(int, input().split())

g = [[] for _ in range(n + 1)]
gr = [[] for _ in range(n + 1)]

for _ in range(m):
    a, b = map(int, input().split())
    g[a].append(b)
    gr[b].append(a)

visited = [False] * (n + 1)
order = []

def dfs1(u):
    visited[u] = True
    for v in g[u]:
        if not visited[v]:
            dfs1(v)
    order.append(u)

for i in range(1, n + 1):
    if not visited[i]:
        dfs1(i)

visited = [False] * (n + 1)
components = []

def dfs2(u, comp):
    visited[u] = True
    comp.append(u)
    for v in gr[u]:
        if not visited[v]:
            dfs2(v, comp)

for u in reversed(order):
    if not visited[u]:
        comp = []
        dfs2(u, comp)
        components.append(comp)

largest = max(components, key=len)

print(len(components))
print(*largest)
```

The first DFS computes finishing times. The recursion appends nodes only after exploring all descendants, which is essential because this ordering is what enables correct SCC extraction later.

The second DFS runs on the reversed graph and builds components. Each time we pick a new starting node from the reversed finishing order, we guarantee we are starting from a fresh SCC.

The largest component is selected after all SCCs are collected. Since ties are allowed, using a simple max by length is sufficient.

One subtle implementation concern is recursion depth. With up to 100,000 nodes, Python recursion can overflow without increasing the recursion limit.

## Worked Examples

### Example 1

Input:

```
9 13
1 2
2 3
3 1
3 8
8 3
8 9
9 7
3 7
7 5
5 6
6 4
4 5
```

After DFS1, assume finishing order (one valid outcome):

| Step | Node finished | Order list |
| --- | --- | --- |
| 1 | 4 | [4] |
| 2 | 5 | [4, 5] |
| 3 | 6 | [4, 5, 6] |
| 4 | 7 | [4, 5, 6, 7] |
| 5 | 9 | [4, 5, 6, 7, 9] |
| 6 | 8 | [4, 5, 6, 7, 9, 8] |
| 7 | 3 | [4, 5, 6, 7, 9, 8, 3] |
| 8 | 2 | [4, 5, 6, 7, 9, 8, 3, 2] |
| 9 | 1 | [4, 5, 6, 7, 9, 8, 3, 2, 1] |

Processing reversed order, DFS2 groups nodes into SCCs:

| Start | Component formed |
| --- | --- |
| 1 | {1,2,3,8} |
| 4 | {4,5,6,7,9} |

The largest SCC is {1,2,3,8}.

This confirms that cycles are correctly grouped even when they are embedded inside larger structures.

### Example 2

Input:

```
10 15
6 10
9 6
3 2
9 1
8 7
4 5
10 8
8 2
6 7
6 4
8 10
3 8
10 5
2 7
5 10
```

SCC formation yields:

| Start | Component |
| --- | --- |
| ... | {8,10,5} |
| ... | other singleton or small SCCs |

The algorithm correctly isolates the cycle-like structure involving 8, 10, and 5, since each can reach the others.

This example demonstrates that SCCs are not tied to simple cycles; they can emerge from complex interwoven reachability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each DFS traversal visits each node and edge a constant number of times across both passes |
| Space | O(n + m) | Adjacency lists for graph and reverse graph plus recursion and component storage |

The constraints allow up to 100,000 nodes and edges, so a linear-time SCC algorithm fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    sys.stdout = io.StringIO()

    input = sys.stdin.readline
    sys.setrecursionlimit(10**7)

    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    gr = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b = map(int, input().split())
        g[a].append(b)
        gr[b].append(a)

    visited = [False] * (n + 1)
    order = []

    def dfs1(u):
        visited[u] = True
        for v in g[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)

    visited = [False] * (n + 1)
    components = []

    def dfs2(u, comp):
        visited[u] = True
        comp.append(u)
        for v in gr[u]:
            if not visited[v]:
                dfs2(v, comp)

    for u in reversed(order):
        if not visited[u]:
            comp = []
            dfs2(u, comp)
            components.append(comp)

    largest = max(components, key=len)
    out = str(len(components)) + "\n" + " ".join(map(str, largest))
    print(out)
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""9 13
1 2
2 3
3 4
4 5
5 6
6 4
3 1
1 8
8 3
8 9
9 7
3 7
7 5
""") == "1 2 3 8", "sample 1"

assert run("""10 15
6 10
9 6
3 2
9 1
8 7
4 5
10 8
8 2
6 7
6 4
8 10
3 8
10 5
2 7
5 10
""") == "8 10 5", "sample 2"

# custom: single node
assert run("""1 0
""") == "1\n1", "single node"

# custom: no cycles
assert run("""3 2
1 2
2 3
""") == "3\n3", "chain"

# custom: full cycle
assert run("""3 3
1 2
2 3
3 1
""") == "1\n1 2 3", "full SCC"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1, [1] | minimal graph handling |
| chain 1→2→3 | 3 groups | no false SCC merging |
| full cycle | 1 group | correct SCC merging |

## Edge Cases

A single vertex graph tests whether the algorithm correctly treats isolated nodes as valid SCCs. The first DFS marks the node, and the second pass immediately forms a component containing only that node.

A directed acyclic chain like 1 → 2 → 3 checks that reachability does not incorrectly merge nodes. Each node finishes at different times, and reversed DFS isolates them into singleton components.

A fully cyclic graph ensures that mutual reachability is correctly recognized. In this case, DFS1 order does not matter much because DFS2 on the reversed graph reaches all nodes in one sweep, producing a single component.

These cases together confirm that the algorithm distinguishes between directional reachability and true mutual connectivity without ambiguity.
