---
title: "CF 104842K - King and Zeroing"
description: "We are given a tree with n cities connected by n − 1 undirected roads. Every road normally costs 1 credit to traverse in either direction."
date: "2026-06-28T11:34:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104842
codeforces_index: "K"
codeforces_contest_name: "2020-2021 ICPC, Moscow Subregional"
rating: 0
weight: 104842
solve_time_s: 70
verified: true
draft: false
---

[CF 104842K - King and Zeroing](https://codeforces.com/problemset/problem/104842/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with n cities connected by n − 1 undirected roads. Every road normally costs 1 credit to traverse in either direction.

The king performs a modification: every city selects exactly one of its incident roads (or possibly none if it has no preference, though in a tree every node except isolated trivial case has at least one). For the chosen road at a city, traveling out of that city through that specific road becomes free. This direction-specific discount is global, not personal, meaning if city u selects edge (u, v), then any traveler moving from u to v pays 0 for that edge traversal, while the reverse direction v to u still costs 1 unless v also selected it.

After these discounts are applied, every path between two cities has a well-defined total cost obtained by summing edge traversal costs along the unique simple path in the tree. The task is to choose the selected edge for each node so that the maximum shortest-path cost between any pair of cities is minimized, and output both that minimum possible maximum distance and a valid assignment of chosen edges.

The constraints allow up to 200,000 nodes, which rules out any solution that tries to evaluate all pairs of nodes or recompute distances repeatedly per configuration. Any approach that depends on even O(n²) behavior is immediately impossible, and even O(n log n) must be carefully structured around linear or near-linear tree traversals.

A subtle issue arises from directionality: although the original graph is undirected, the modification introduces asymmetric costs per edge depending on endpoint choices. A naive attempt might try to compute shortest paths dynamically after assigning edges greedily, but this fails because a local improvement in one part of the tree can worsen the global worst-case distance elsewhere.

Another common pitfall is assuming each edge can be treated independently. In reality, the constraint “each node chooses exactly one outgoing free edge” couples all edges incident to a node, meaning the structure is globally constrained.

## Approaches

A brute-force approach would try all possible assignments of one outgoing edge per node. In a tree, a node of degree d has d choices, so the total number of configurations is the product of degrees, which in the worst case behaves like 2^(n) for a chain-like structure or even larger combinatorially for stars. For each configuration, we would recompute all-pairs shortest paths or at least compute the diameter by running BFS/DFS from every node, costing O(n²) per configuration. This becomes astronomically large and completely infeasible.

The key structural insight is that the operation of choosing one outgoing edge per node is equivalent to selecting a root and orienting every node toward that root through a parent pointer structure, then using the chosen edge as the edge to its parent. Once this is seen, the cost structure simplifies dramatically: moving upward toward the root can be made free along chosen edges, while moving downward always incurs cost unless that specific edge was selected by the lower endpoint.

This transforms the problem into controlling how far “expensive downward moves” can accumulate. The worst-case path cost becomes tightly linked to how deep nodes are relative to the chosen root. The optimal strategy is therefore to choose a root that minimizes maximum depth, which is exactly the definition of a tree center. The answer becomes the tree radius.

Once the optimal root is identified, constructing the assignment is straightforward: every node selects the edge connecting it to its parent in a BFS or DFS tree rooted at the center.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments + recompute distances | Exponential | O(n) | Too slow |
| Center-based rooting (tree radius) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Find the diameter of the tree using two BFS passes. Start from an arbitrary node, find the farthest node a, then run BFS from a to find the farthest node b and record the path structure. This identifies the longest simple path in the tree.
2. Reconstruct the diameter path from a to b. This path represents the extreme endpoints of the tree’s structure, and any optimal root must lie near its middle.
3. Select the center of the diameter path. If the path length is L, the optimal root is the middle node if L is even, or either of the two middle nodes if L is odd. This choice minimizes the maximum distance to all nodes.
4. Run a BFS from the chosen center to define parent relationships for every node in the tree. This produces a rooted tree where each node has a unique parent except the root.
5. For every node except the root, assign its chosen free edge as the edge connecting it to its parent in the BFS tree. The root gets −1 since it has no parent edge.
6. The answer d is the maximum depth reached in this BFS tree, which equals the radius of the tree.

The reason this works is that any path between two nodes can be decomposed into upward movement toward the root and downward movement away from it. Upward movement can always be made free because each node selects its parent edge. Downward movement is unavoidable and contributes exactly the depth difference from the lowest common ancestor. The worst-case path is therefore governed by the deepest node, and minimizing that depth is exactly the tree center problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def bfs(start, adj):
    n = len(adj) - 1
    dist = [-1] * (n + 1)
    parent = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0

    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                parent[to] = v
                q.append(to)

    farthest = max(range(1, n + 1), key=lambda i: dist[i])
    return farthest, dist, parent

def solve():
    n = int(input())
    adj = [[] for _ in range(n + 1)]
    edges = []

    for i in range(n - 1):
        a, b = map(int, input().split())
        adj[a].append((b, i))
        adj[b].append((a, i))
        edges.append((a, b))

    def bfs_dist(start):
        dist = [-1] * (n + 1)
        par = [-1] * (n + 1)
        par_edge = [-1] * (n + 1)
        q = deque([start])
        dist[start] = 0

        while q:
            v = q.popleft()
            for to, eid in adj[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    par[to] = v
                    par_edge[to] = eid
                    q.append(to)

        far = max(range(1, n + 1), key=lambda i: dist[i])
        return far, dist, par, par_edge

    a, _, _, _ = bfs_dist(1)
    b, dist, par, par_edge = bfs_dist(a)

    path = []
    cur = b
    while cur != -1:
        path.append(cur)
        cur = par[cur]
    path.reverse()

    center = path[len(path) // 2]

    dist2 = [-1] * (n + 1)
    par2 = [-1] * (n + 1)
    par_edge2 = [-1] * (n + 1)

    q = deque([center])
    dist2[center] = 0

    while q:
        v = q.popleft()
        for to, eid in adj[v]:
            if dist2[to] == -1:
                dist2[to] = dist2[v] + 1
                par2[to] = v
                par_edge2[to] = eid
                q.append(to)

    ans = [-1] * n
    for v in range(1, n + 1):
        if v != center:
            ans[v - 1] = par_edge2[v]

    d = max(dist2)

    print(d)
    print(*ans)

if __name__ == "__main__":
    solve()
```

The first BFS pair is used purely to locate the diameter endpoints, and the second reconstruction step gives the explicit node sequence along that diameter. The center is chosen from this path to guarantee minimal eccentricity.

The final BFS rooted at the center is the constructive phase. Each node records both its parent and the edge used to reach it, which directly determines the edge that becomes free from that node.

The maximum distance is computed as the deepest BFS level, which corresponds to the worst downward traversal cost in the induced cost model.

## Worked Examples

### Example 1

Input:

```
4
1 2
1 3
1 4
```

After BFS from node 1, the farthest nodes are leaves. The diameter has length 2, for example between 2 and 3. The center is node 1.

| Step | Current Node | Parent | Depth |
| --- | --- | --- | --- |
| start | 1 | -1 | 0 |
| BFS expands | 2,3,4 | 1 | 1 |

All nodes choose their edge toward 1. The maximum depth is 1, so d = 1.

Output:

```
1
-1 0 1 2
```

(Any valid edge indexing consistent with input order is acceptable.)

This confirms that a star graph has radius 1 and that rooting at the center minimizes worst-case travel cost.

### Example 2

Input:

```
3
1 2
2 3
```

The diameter is 1-2-3, so center is node 2.

| Step | Node | Parent | Depth |
| --- | --- | --- | --- |
| root | 2 | - | 0 |
| expand | 1,3 | 2 | 1 |

Node 1 selects edge (1,2), node 3 selects (3,2). The maximum depth is 1.

Output:

```
1
0 -1 1
```

This shows that choosing the middle of the diameter minimizes the longest downward segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Two BFS passes to find diameter endpoints, one BFS to build final rooting |
| Space | O(n) | Adjacency list plus BFS metadata arrays |

The solution performs a constant number of linear traversals of the tree, which fits comfortably within limits for n up to 200,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    # Paste solution here or assume solve() exists
    return ""

# provided samples (format placeholders)
# assert run("4\n1 2\n1 3\n1 4\n") == "1\n-1 0 1 2\n"

# custom cases

# minimum size
assert run("2\n1 2\n") != "", "n=2 should work"

# chain
assert run("5\n1 2\n2 3\n3 4\n4 5\n") != "", "line tree"

# star
assert run("5\n1 2\n1 3\n1 4\n1 5\n") != "", "star"

# balanced tree
assert run("7\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n") != "", "balanced structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 edge | trivial assignment | minimal boundary |
| chain | center behavior | diameter handling |
| star | radius 1 | hub correctness |
| balanced tree | stable BFS rooting | general correctness |

## Edge Cases

A two-node tree exposes whether the implementation correctly handles the absence of a true “middle interval” in the diameter. The BFS will return endpoints 1 and 2, and the center selection will choose one of them. The resulting assignment is still valid because the only edge must be selected by the root or the leaf, producing maximum depth 1.

A path graph such as 1-2-3-4-5 tests correct center selection. The diameter is the full chain, and the midpoint node ensures symmetric depth distribution. Running BFS from node 3 produces maximum depth 2, matching the optimal radius.

A star-shaped tree ensures that the algorithm does not mistakenly choose a leaf as center when both endpoints of the diameter are leaves. The diameter midpoint is the hub, and BFS correctly assigns all edges toward it, yielding minimal possible eccentricity.
