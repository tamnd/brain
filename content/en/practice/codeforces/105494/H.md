---
title: "CF 105494H - Hierarchy"
description: "We are given a collection of employees where each employee belongs to exactly one company, and each company is structured as a hierarchy rooted at a CEO."
date: "2026-06-23T21:03:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105494
codeforces_index: "H"
codeforces_contest_name: "2024-2025 ICPC NERC, Kyrgyzstan Qualification Contest"
rating: 0
weight: 105494
solve_time_s: 60
verified: true
draft: false
---

[CF 105494H - Hierarchy](https://codeforces.com/problemset/problem/105494/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of employees where each employee belongs to exactly one company, and each company is structured as a hierarchy rooted at a CEO. If we model employees as vertices and reporting relationships as edges, each company forms a tree, and the full system is a forest of such trees.

The task is to determine the size of each company, meaning for every employee we want to know how many people are in their connected hierarchy. Since all employees in the same tree share the same company size, this is equivalent to computing the size of each connected component in an undirected forest.

Even though the story is phrased in terms of CEOs and subordinates, the computational structure is simply an undirected graph with no cycles. Each tree corresponds to one company, and the answer for any node is the size of its tree.

The constraints in this type of problem typically allow up to around 200,000 nodes and edges, which immediately rules out any quadratic approach such as checking connectivity between every pair of nodes. Any solution that attempts repeated DFS or BFS from every node independently would degrade to O(n^2) in the worst case, which is far beyond acceptable. We need a single linear or near-linear pass over the structure.

A subtle edge case appears when the forest contains many single-node trees. For example, if there are nodes with no edges at all, each of them forms a company of size 1. Another corner case is a single large chain, where naive repeated traversals might revisit long paths many times if not carefully marked.

## Approaches

The brute-force idea is to treat each node as a potential root and run a DFS or BFS to compute how many nodes are reachable from it. This is correct because reachability in an undirected graph exactly defines connected components. However, doing this independently for every node causes massive recomputation. In a chain of length n, a single DFS already costs O(n), and repeating it n times leads to O(n^2) operations, which is not viable.

The key observation is that the graph structure does not change between queries. Each connected component has a fixed size, and every node inside it shares the same answer. This means we only need to compute each component once, then propagate its size to all nodes in that component.

There are two standard ways to achieve this efficiently. One is graph traversal using DFS or BFS. We visit each node exactly once, accumulate the size of its component during traversal, and assign that size to every visited node. The second is Disjoint Set Union, where we merge endpoints of edges and maintain component sizes in the DSU root.

Both approaches rely on the same idea: compress the forest into disjoint sets and compute sizes per set rather than per node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS from each node | O(n^2) | O(n) | Too slow |
| DFS/BFS per component | O(n) | O(n) | Accepted |
| DSU with union by size | O(n α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We describe the DFS/BFS approach first since it is the most direct interpretation of the problem.

1. Build an adjacency list for the forest from the given edges. This representation allows us to traverse neighbors of each node efficiently without scanning irrelevant pairs.
2. Maintain a visited array initialized to false for all nodes. This ensures each node is processed exactly once, preventing repeated traversal across the same component.
3. Iterate through all nodes from 1 to n. When we find a node that has not been visited, we start a traversal from it. This node acts as the entry point of a new company tree.
4. During traversal, we perform a DFS or BFS, collecting all nodes reachable from the starting node. Each visited node is marked to avoid revisiting.
5. While traversing a component, we count how many nodes are discovered. This count is the size of the current company.
6. After finishing the traversal of a component, assign the computed size to every node collected during that traversal.

The DSU approach follows the same logic but replaces traversal with union operations. Each edge merges two sets, and each set root maintains a size counter. After processing all edges, the answer for each node is simply the size of its representative.

Why it works: the visited marking in DFS, or the representative pointer in DSU, ensures that each connected component is identified exactly once. Since connectivity partitions the graph into disjoint sets, every node belongs to exactly one component, and every component is counted exactly once. No node can be counted twice because once it is assigned to a component or unioned under a root, it is never reprocessed as a separate entity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    g = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)
    
    vis = [False] * (n + 1)
    ans = [0] * (n + 1)
    
    sys.setrecursionlimit(10**7)
    
    def dfs(start):
        stack = [start]
        comp = []
        vis[start] = True
        
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in g[u]:
                if not vis[v]:
                    vis[v] = True
                    stack.append(v)
        
        size = len(comp)
        for node in comp:
            ans[node] = size
    
    for i in range(1, n + 1):
        if not vis[i]:
            dfs(i)
    
    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The solution first builds the adjacency list so that each employee knows their direct connections in the hierarchy. The DFS is implemented iteratively using a stack to avoid recursion depth issues, especially important when the hierarchy degenerates into a long chain.

Each time we encounter an unvisited node, we explore its entire connected component. The comp list stores all nodes in that component so that after traversal we can assign them the same computed size. This avoids recomputing sizes multiple times.

The ans array stores final company sizes per node, and we print all values excluding index 0.

## Worked Examples

Consider a small forest with two components: one chain of three nodes and one isolated node.

Input:

```
4 2
1 2
2 3
```

| Step | Node | Action | Component |
| --- | --- | --- | --- |
| 1 | 1 | start DFS | [1, 2, 3] |
| 2 | 4 | new DFS | [4] |

After processing, nodes 1, 2, 3 get size 3, node 4 gets size 1.

This demonstrates how the traversal automatically separates disconnected structures and assigns sizes per component rather than per node.

Now consider a fully disconnected graph:

Input:

```
3 0
```

| Step | Node | Action | Component |
| --- | --- | --- | --- |
| 1 | 1 | DFS | [1] |
| 2 | 2 | DFS | [2] |
| 3 | 3 | DFS | [3] |

Each node forms its own company, confirming that isolated vertices are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node and edge is processed once during DFS |
| Space | O(n + m) | Adjacency list and auxiliary arrays store graph structure |

The algorithm fits easily within typical constraints up to 200,000 nodes and edges since it performs only linear work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    data = inp.strip().split()
    if not data:
        return ""
    
    n, m = map(int, data[:2])
    g = [[] for _ in range(n + 1)]
    
    idx = 2
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); idx += 2
        g[u].append(v)
        g[v].append(u)
    
    vis = [False] * (n + 1)
    ans = [0] * (n + 1)
    
    sys.setrecursionlimit(10**7)
    
    def dfs(s):
        stack = [s]
        comp = []
        vis[s] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in g[u]:
                if not vis[v]:
                    vis[v] = True
                    stack.append(v)
        size = len(comp)
        for x in comp:
            ans[x] = size
    
    for i in range(1, n + 1):
        if not vis[i]:
            dfs(i)
    
    return " ".join(map(str, ans[1:]))

# single node
assert run("1 0") == "1"

# chain
assert run("4 3\n1 2\n2 3\n3 4") == "4 4 4 4"

# two components
assert run("5 3\n1 2\n2 3\n4 5") == "3 3 3 2 2"

# isolated nodes
assert run("3 0") == "1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | single node component |
| chain 4 nodes | 4 4 4 4 | linear tree propagation |
| split components | 3 3 3 2 2 | multiple trees |
| no edges | 1 1 1 | all isolated nodes |

## Edge Cases

For a single-node graph, the algorithm immediately marks that node as visited and assigns it a component size of one. There are no neighbors to process, so the DFS stack empties instantly and correctness follows directly from initialization.

For a fully disconnected graph, each iteration of the outer loop triggers a fresh DFS call. Since no edges exist, each DFS only touches a single node, producing correct size one assignments independently.

For a long chain, the iterative stack ensures we never exceed recursion limits. Each node is pushed and popped exactly once, so even in the worst skewed structure the traversal remains linear without stack overflow risks.
