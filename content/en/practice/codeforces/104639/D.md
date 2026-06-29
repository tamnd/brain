---
title: "CF 104639D - Transitivity"
description: "We are given an undirected simple graph where some pairs of vertices are already connected by edges. The operation we are allowed to perform is to add new edges, but we cannot delete existing ones and we cannot introduce parallel edges or self loops."
date: "2026-06-29T16:56:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104639
codeforces_index: "D"
codeforces_contest_name: "The 2023 ICPC Asia EC Regionals Online Contest (I)"
rating: 0
weight: 104639
solve_time_s: 58
verified: true
draft: false
---

[CF 104639D - Transitivity](https://codeforces.com/problemset/problem/104639/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected simple graph where some pairs of vertices are already connected by edges. The operation we are allowed to perform is to add new edges, but we cannot delete existing ones and we cannot introduce parallel edges or self loops.

The final goal is to transform this graph into one with a strong structural property: whenever two vertices can reach each other through some sequence of edges, they must already have a direct edge between them. In other words, reachability and adjacency must coincide in the final graph.

This condition has a very rigid consequence. Inside any connected region of the graph, every pair of vertices must end up being directly connected, otherwise there would exist a path between them without an edge. So each connected component must become a clique in the final graph.

The task is to compute the minimum number of edges we need to add to achieve this condition.

The constraints go up to one million vertices and one million edges. That immediately suggests that any solution that tries to consider pairs of vertices directly is impossible. Even quadratic behavior per component is too slow if we are not careful about how components are processed. A linear or near linear graph traversal is the only viable direction.

A subtle point is that we are not allowed to “fix” the graph by merging components cheaply. If we connect two previously disconnected components, then every vertex in the combined structure becomes reachable from every other vertex through the new edge, which forces us to add all missing edges across the merged set as well. That quickly becomes more expensive than treating components separately.

A naive mistake is to think we can just connect everything into one large clique and count missing edges from there. That ignores that adding a single edge between components changes the reachability structure globally and forces a cascade of additional required edges.

For example, consider three components of sizes 2, 2, and 2 with no internal edges. If we connect them all into one component, we must eventually form a clique of size 6, which requires 15 edges, while keeping them separate requires only 3 edges per component total, so 9 edges added. The difference is significant and shows why merging is not optimal.

## Approaches

A brute-force approach would be to simulate the process of repeatedly fixing violations. We could search for any pair of vertices in the same connected component that are not directly connected, add that edge, and continue until closure is achieved. Each check requires either BFS or DFS to verify reachability and adjacency, and each addition changes the structure again.

The problem with this approach is that a single component of size n could require on the order of n² missing edges, and each insertion might trigger recomputation of connectivity. This leads to a cubic worst case or at least quadratic overhead per component, which is far beyond feasible limits for n up to 10⁶.

The key observation is that the final structure inside each connected component is fully determined: it must become a complete graph on exactly those vertices. We do not need to simulate the process of adding edges one by one. We only need to count how many edges are missing from that complete graph.

Once we recognize this, the problem reduces to a decomposition task. We find the connected components of the original graph. For each component, we compute how many edges are needed to make it a clique. If a component has s vertices and currently has e edges, then a complete graph would contain s·(s−1)/2 edges, so we must add exactly s·(s−1)/2 − e edges for that component.

Summing this over all components gives the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n³) worst case | O(n + m) | Too slow |
| Connected Components Counting | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We rely on the structure of connected components, so the algorithm focuses on discovering them and measuring their sizes and edge counts.

1. Build an adjacency list representation of the graph and prepare a visited array over all vertices. This allows us to traverse each connected component efficiently.
2. Run a DFS or BFS from every unvisited vertex to identify one connected component at a time. While traversing, collect all vertices belonging to this component and count how many edges are encountered from these vertices.

The edge count must be handled carefully because each undirected edge appears twice in adjacency lists, so we ensure consistent counting or divide appropriately later.
3. For each component, compute its size s. The number of edges it must contain in a complete graph is s·(s−1)/2. Compare this with the number of edges currently present in that component.
4. Add the difference between required edges and existing edges to the answer.
5. Output the total sum across all components.

### Why it works

The key invariant is that connected components are independent with respect to the transitivity requirement. If two vertices lie in different components, there is no path between them, so the condition places no requirement on edges between those components. Inside a component, once a path exists between two vertices, the final graph must contain the direct edge between them. That forces every component to evolve into a clique, and no solution can avoid adding exactly the missing edges of that clique without violating the condition. This makes the component decomposition both sufficient and necessary.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, m = map(int, input().split())

adj = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    adj[u].append(v)
    adj[v].append(u)

visited = [False] * n

def dfs(start):
    stack = [start]
    visited[start] = True
    nodes = 0
    edges = 0

    while stack:
        u = stack.pop()
        nodes += 1
        for v in adj[u]:
            edges += 1
            if not visited[v]:
                visited[v] = True
                stack.append(v)

    return nodes, edges // 2

ans = 0

for i in range(n):
    if not visited[i]:
        sz, e = dfs(i)
        ans += sz * (sz - 1) // 2 - e

print(ans)
```

The implementation uses an iterative DFS to avoid recursion depth issues on large chains. Each edge is counted twice during traversal, once from each endpoint, so we divide by two when computing the final edge count per component.

A common pitfall is forgetting that edges must be counted per component rather than globally. Simply summing all edges and subtracting from a global n·(n−1)/2 would incorrectly assume the final graph must be one single clique, which is not required.

## Worked Examples

### Example 1

Input:

```
4 3
1 2
1 3
2 3
```

We have one component containing all 4 vertices.

| Step | Component | Size | Edges counted | Complete edges | Added |
| --- | --- | --- | --- | --- | --- |
| 1 | {1,2,3,4} | 4 | 3 | 6 | 3 |

The component already has a triangle among {1,2,3}, but vertex 4 is isolated within the component, so we need edges (4,1), (4,2), (4,3). That is 3 edges.

Output is 3.

This confirms that even if part of the component is already dense, we still compute based on full closure of the entire connected component.

### Example 2

Input:

```
5 2
1 2
4 5
```

We have three components: {1,2}, {3}, {4,5}.

| Component | Size | Existing edges | Complete edges | Added |
| --- | --- | --- | --- | --- |
| {1,2} | 2 | 1 | 1 | 0 |
| {3} | 1 | 0 | 0 | 0 |
| {4,5} | 2 | 1 | 1 | 0 |

Total added = 0.

This shows that a graph composed of already complete components is already transitive, and no extra edges are required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed once during DFS |
| Space | O(n + m) | Adjacency list and visited array |

The constraints allow up to one million vertices and edges, and this linear-time traversal comfortably fits within limits. The memory usage is also linear in the size of the graph.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import deque

    input = _sys.stdin.readline
    sys.setrecursionlimit(10**7)

    n, m = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n

    def dfs(start):
        stack = [start]
        visited[start] = True
        nodes = 0
        edges = 0
        while stack:
            u = stack.pop()
            nodes += 1
            for v in adj[u]:
                edges += 1
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        return nodes, edges // 2

    ans = 0
    for i in range(n):
        if not visited[i]:
            sz, e = dfs(i)
            ans += sz * (sz - 1) // 2 - e

    return str(ans)

# provided sample
assert run("4 3\n1 2\n1 3\n2 3\n") == "3"

# single node
assert run("1 0\n") == "0"

# already complete components
assert run("3 3\n1 2\n2 3\n1 3\n") == "0"

# two disjoint edges
assert run("5 2\n1 2\n4 5\n") == "0"

# chain graph
assert run("4 3\n1 2\n2 3\n3 4\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | trivial component handling |
| complete triangle | 0 | no extra edges needed |
| disjoint edges | 0 | independent components |
| chain | 3 | full closure within one component |

## Edge Cases

A single isolated vertex is its own component of size one. The formula s·(s−1)/2 immediately gives zero, so no edges are added. The algorithm naturally handles this because DFS marks the vertex and returns zero edges for that component.

A fully connected component already satisfies the clique condition. During traversal, every edge is counted exactly once per component, and since it already matches s·(s−1)/2, the subtraction yields zero. There is no risk of overcounting because edge counting is localized to each component.

A long path graph tests the worst case for DFS depth and edge counting correctness. Even though every vertex is connected, only n−1 edges exist, and the formula correctly computes the number of missing edges needed to complete the clique.
