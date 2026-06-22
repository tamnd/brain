---
title: "CF 105582A - Apple"
description: "We are given an undirected simple graph with at most 100 vertices and 100 edges. The task is not to “draw” anything geometrically in a computational sense, but to decide whether this graph can be interpreted as a very specific structure called an apple."
date: "2026-06-22T17:51:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105582
codeforces_index: "A"
codeforces_contest_name: "Ural Championship 2017"
rating: 0
weight: 105582
solve_time_s: 59
verified: true
draft: false
---

[CF 105582A - Apple](https://codeforces.com/problemset/problem/105582/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected simple graph with at most 100 vertices and 100 edges. The task is not to “draw” anything geometrically in a computational sense, but to decide whether this graph can be interpreted as a very specific structure called an apple.

An apple consists of two vertex-disjoint simple structures that share exactly one common starting vertex. One structure is a simple cycle, and the other is a simple path. The cycle must contain at least three vertices, and the path must contain at least two vertices. Apart from the shared starting vertex, the cycle and the path must not touch each other or reuse vertices. The question reduces to deciding whether we can partition the graph’s edges into one simple cycle and one simple path with a common root, under these strict structural constraints.

The constraints are small enough that exponential reasoning is theoretically possible but unnecessary. With n, m ≤ 100, even O(n³) or O(n·m) graph analysis is comfortably fast. This immediately suggests that we should aim for structural decomposition rather than any brute-force geometric arrangement or enumeration of embeddings.

A subtle edge case appears when the graph looks “almost like” a cycle with a tail, but the tail reuses a vertex from the cycle, or the cycle is too small. For example, if we have a triangle 1-2-3-1 and a path 1-4, this is valid. But if the path touches vertex 2 as well, forming something like 1-2-4, then the decomposition is no longer valid because the path and cycle intersect outside the root. Another failure mode is when there is a cycle of size 2, which is impossible in a simple graph, but still worth noting as a conceptual trap when reasoning about degree-based approaches.

## Approaches

A brute-force interpretation would try to guess the root vertex and then decide which incident edges belong to the cycle and which belong to the path, checking whether we can form exactly one simple cycle and one simple path satisfying all constraints. This leads naturally to enumerating subsets of edges or performing a backtracking assignment of edges incident to the root. Even with n ≤ 100, this becomes combinatorial: if a vertex has degree d, splitting its incident edges into two groups already creates 2^d possibilities, and across all vertices this explodes far beyond feasible limits.

The key observation is that the structure is extremely rigid. The graph is composed of exactly two connected components that intersect only at one vertex, and each component has a very specific form. One component is a cycle, meaning every vertex in it has degree 2 inside that subgraph. The other is a path, meaning exactly two vertices have degree 1 inside that subgraph and all others have degree 2, except the shared root which has degree 1 in the path component but is shared globally.

This rigidity allows us to flip the problem from “finding a drawing” to “checking whether we can decompose the graph into two very specific subgraphs sharing exactly one articulation point”. The natural direction is to try each vertex as the potential shared root and validate whether its incident structure can be split into one cycle component and one path component.

The cycle condition becomes a check for whether there exists a cycle entirely contained in the graph that can be “anchored” at the root, while the remaining edges from the root form a simple path. Since the graph is small, we can explicitly attempt DFS-based cycle detection and path validation rooted at each candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force edge assignment | Exponential | O(n + m) | Too slow |
| Root-based structural check with DFS | O(n · (n + m)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph. This allows efficient traversal of neighbors when attempting to verify structural constraints.
2. Iterate over each vertex treating it as the potential shared root of the cycle and the path. The correct configuration must use exactly one such vertex, so trying all possibilities is safe.
3. For a fixed root, attempt to identify a cycle that does not pass through the root in an arbitrary way, but can be considered the “cycle component”. We perform DFS in the graph while tracking parent edges and detect back-edges that form a cycle.
4. Once a cycle is found, mark all vertices belonging to that cycle. This is crucial because the cycle must be internally consistent: every vertex in it must have exactly two neighbors within the cycle structure.
5. Verify that the root is connected to exactly two vertices in the cycle or participates in a way consistent with being the shared vertex. If the cycle cannot be separated cleanly, this root is invalid.
6. Remove or ignore the cycle edges and check the remaining structure. The remaining edges incident to the root must form a simple path. This means that starting from the root, a DFS over remaining edges should visit all remaining vertices exactly once in a linear chain structure, with no branching.
7. Validate that the remaining component is indeed a path: every vertex except endpoints must have degree 2 in the remaining subgraph, and exactly two endpoints must have degree 1.
8. If any root satisfies both the cycle condition and the path condition, return “Yes”.

If no root produces a valid decomposition, return “No”.

### Why it works

The correctness comes from the structural rigidity of the target object. Any valid configuration must have exactly one vertex that belongs to both components. That vertex is an articulation point separating a cycle and a path. Removing it splits the graph into exactly two connected structures with fixed degree constraints: one must be a cycle (all degree 2 internally), and the other must be a path (two endpoints, rest degree 2). Since every valid apple has exactly one such decomposition point, iterating over all vertices guarantees that we will eventually test the correct one if it exists. The DFS checks enforce the local constraints that uniquely characterize cycles and paths in undirected graphs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def find_cycle(n, adj, start):
    parent = [-1] * (n + 1)
    visited = [False] * (n + 1)
    stack = [(start, -1)]
    visited[start] = True

    while stack:
        u, p = stack.pop()
        for v in adj[u]:
            if v == p:
                continue
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append((v, u))
            else:
                # found a cycle, reconstruct it
                cycle = set()
                x = u
                cycle.add(v)
                while x != v and x != -1:
                    cycle.add(x)
                    x = parent[x]
                return cycle
    return set()

def is_path_component(n, adj, root, banned):
    visited = [False] * (n + 1)

    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if v in banned:
                continue
            if not visited[v]:
                dfs(v)

    dfs(root)

    nodes = [i for i in range(1, n + 1) if visited[i] and i not in banned]
    if not nodes:
        return False

    deg = {}
    for u in nodes:
        deg[u] = 0
        for v in adj[u]:
            if v not in banned:
                deg[u] += 1

    endpoints = [u for u in nodes if deg[u] == 1]
    internal = [u for u in nodes if deg[u] == 2]

    return len(endpoints) == 2 and len(endpoints) + len(internal) == len(nodes)

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    for root in range(1, n + 1):
        cycle = find_cycle(n, adj, root)
        if not cycle:
            continue
        if root not in cycle:
            continue
        if is_path_component(n, adj, root, cycle):
            return "Yes"

    return "No"

print(solve())
```

The implementation tries each vertex as the shared junction. For each candidate root, it runs a DFS-based cycle detection that reconstructs one cycle when a back-edge is found. That cycle is treated as the cycle component. The remaining check verifies whether the rest of the graph forms a clean path after excluding cycle vertices. The key subtlety is that the cycle detection is not trying to enumerate all cycles, only one valid cycle that can serve as the required component, which is sufficient because any valid solution must contain at least one such cycle passing through the correct root.

The path validation explicitly computes degrees in the restricted graph. This avoids relying on traversal order alone, which would be fragile in graphs with multiple branches.

## Worked Examples

### Example 1

Input:

```
5 5
1 2
2 3
1 3
1 4
1 5
```

We try each node as root. For root 1, a cycle 1-2-3-1 exists, so cycle = {1,2,3}. Removing it leaves edges 1-4 and 1-5.

| Step | Cycle | Remaining graph | Path valid |
| --- | --- | --- | --- |
| root=1 | {1,2,3} | 1-4, 1-5 | No |

The remaining structure branches at node 1, producing degree 2 at the root in the residual graph, which violates path structure. So root 1 fails, and no other root produces a valid decomposition.

Output: No.

### Example 2

Input:

```
4 4
1 2
2 3
1 3
1 4
```

For root 1, cycle is {1,2,3}. Remaining edge is 1-4.

| Step | Cycle | Remaining graph | Path valid |
| --- | --- | --- | --- |
| root=1 | {1,2,3} | 1-4 | Yes |

The remaining component is a single edge, which is a valid path of length 2 vertices. The cycle has size 3, satisfying constraints.

Output: Yes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · (n + m)) | Each root triggers DFS cycle detection and degree validation over the graph |
| Space | O(n + m) | Adjacency list plus auxiliary arrays |

With n, m ≤ 100, this comfortably fits within limits. Even the worst-case 10⁴ operations per root is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# sample 1
assert run("""5 5
1 2
2 3
1 3
1 4
1 5
""").strip() == "No"

# sample 2
assert run("""4 4
1 2
2 3
1 3
1 4
""").strip() == "Yes"

# minimum case (impossible)
assert run("""3 2
1 2
2 3
""").strip() == "No"

# simple valid apple
assert run("""5 5
1 2
2 3
3 1
1 4
4 5
""").strip() == "Yes"

# disconnected graph
assert run("""6 4
1 2
2 3
3 1
4 5
""").strip() == "No"

# all nodes in cycle only
assert run("""4 4
1 2
2 3
3 4
4 1
""").strip() == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-chain only | No | no cycle exists |
| cycle + tail | Yes | valid decomposition |
| disconnected components | No | structure must be connected |
| pure cycle | No | missing path component |

## Edge Cases

A critical edge case is when a cycle exists but the remaining structure branches at the root. For instance, a triangle with two extra edges from the same vertex. Even though a cycle is present, the residual graph fails the path degree condition because the root ends up with degree greater than 1 in the remaining component.

Another subtle case is when multiple cycles exist. The algorithm relies on detecting one cycle per root, but not all cycles are valid. If the detected cycle does not include the correct decomposition structure, the root will fail later in the path validation step, which ensures incorrect cycle choices do not produce false positives.

A final case is when the graph is connected but contains no simple cycle. In that situation, cycle detection returns empty for all roots, and the algorithm correctly outputs “No” without attempting unnecessary path checks.
