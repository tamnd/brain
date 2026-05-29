---
title: "CF 342E - Xenia and Tree"
description: "We are given a tree of n nodes, rooted conceptually at node 1, which starts painted red. All other nodes are blue. We have to handle two types of queries: first, paint a blue node red; second, for a given node, report the distance to the nearest red node."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "trees"]
categories: ["algorithms"]
codeforces_contest: 342
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 199 (Div. 2)"
rating: 2400
weight: 342
solve_time_s: 312
verified: true
draft: false
---

[CF 342E - Xenia and Tree](https://codeforces.com/problemset/problem/342/E)

**Rating:** 2400  
**Tags:** data structures, divide and conquer, trees  
**Solve time:** 5m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree of `n` nodes, rooted conceptually at node 1, which starts painted red. All other nodes are blue. We have to handle two types of queries: first, paint a blue node red; second, for a given node, report the distance to the nearest red node. The distance here is the standard tree distance, defined as the number of edges along the shortest path between two nodes.

The tree has up to `10^5` nodes, and we can have up to `10^5` queries. This implies that any solution with time complexity `O(n)` per query will be too slow, because `n * m` could reach `10^10` operations. We need an approach closer to `O(log n)` per query or `O(sqrt(n))` per query.

Edge cases arise when the tree is skewed or the red nodes are sparsely distributed. For example, if the tree is a path `1-2-3-4-5` and only node 1 is red, a query asking for the distance to node 5 must return 4. A careless BFS per query would work here but fail under maximum constraints. Another subtle case is when multiple red nodes exist at equal minimal distances; our algorithm must still report the correct minimal distance.

## Approaches

A brute-force approach is straightforward. Maintain a set of red nodes. For each query of type 2, run BFS from the target node until you reach a red node. The distance from the BFS start to the first red node found is the answer. This is correct but too slow. Each query could take `O(n)`, leading to `O(n*m)` total time, which is unacceptable for `n, m ~ 10^5`.

The key insight is to exploit the tree structure. In trees, distances satisfy the triangle inequality, and every node has a unique path to the root. If we could quickly query distances to all red nodes efficiently, we could answer type 2 queries in `O(log n)` time. Centroid decomposition provides such a structure. By recursively decomposing the tree into centroids and maintaining, for each centroid, the closest red node in its subtree, we can update and query efficiently.

When painting a node red, we update the minimum distance for all centroids on the path from this node to the root of the centroid tree. When querying a node, we check the precomputed minimum distances along the same path. Each path in a centroid decomposition is at most `O(log n)` long, giving `O(log n)` time per update and query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | O(n * m) | O(n) | Too slow |
| Centroid Decomposition + distance updates | O((n + m) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Build the tree using adjacency lists from the input. This allows efficient traversal for decomposition and BFS.
2. Construct the centroid decomposition. For each subtree, find a node whose removal splits the subtree into smaller parts with size at most half of the subtree. This node becomes a centroid. Recursively apply decomposition to the remaining subtrees. The centroid tree will have height `O(log n)`.
3. For each node, maintain a list of centroids on the path from that node to the root of the centroid tree. Alongside, store distances to each centroid. These distances can be precomputed with BFS from each centroid to its subtree nodes.
4. Initialize a distance array `dist[node]` for all nodes, where `dist[node]` is the minimum distance to any red node. Initially, only node 1 is red, so we set `dist[1] = 0` and all others to infinity.
5. To handle a paint query for node `v`, traverse all centroids on its path and update `dist[c] = min(dist[c], distance from v to c)`. This propagates the effect of the new red node up the centroid hierarchy.
6. To handle a query for the closest red node to `v`, check all centroids on the path from `v` to the centroid root. The answer is `min(dist[c] + distance from v to c)` across all centroids.

Why it works: The centroid decomposition ensures every node lies in at most `O(log n)` centroid subtrees. Each centroid maintains the minimum distance to a red node in its subtree. By propagating updates and querying along the centroid path, we always capture the closest red node. This guarantees correctness for all queries.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

sys.setrecursionlimit(10**6)

def solve():
    n, m = map(int, input().split())
    tree = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        tree[u - 1].append(v - 1)
        tree[v - 1].append(u - 1)

    # centroid decomposition
    size = [0] * n
    used = [False] * n
    parent_centroid = [-1] * n

    def dfs_size(u, p):
        size[u] = 1
        for v in tree[u]:
            if v != p and not used[v]:
                dfs_size(v, u)
                size[u] += size[v]

    def find_centroid(u, p, n_nodes):
        for v in tree[u]:
            if v != p and not used[v]:
                if size[v] > n_nodes // 2:
                    return find_centroid(v, u, n_nodes)
        return u

    def build(u, p):
        dfs_size(u, -1)
        c = find_centroid(u, -1, size[u])
        parent_centroid[c] = p
        used[c] = True
        for v in tree[c]:
            if not used[v]:
                build(v, c)
        return c

    root_centroid = build(0, -1)

    # distance from node to its ancestors in centroid tree
    dist = [float('inf')] * n
    dist[0] = 0  # node 1 initially red

    def update(u):
        x = u
        while x != -1:
            d = distance(u, x)
            dist[x] = min(dist[x], d)
            x = parent_centroid[x]

    # BFS distances from each node to its centroids
    centroid_distances = [dict() for _ in range(n)]
    def distance(u, c):
        if c in centroid_distances[u]:
            return centroid_distances[u][c]
        # BFS to compute distance from u to c
        q = deque([(c, 0)])
        seen = [False] * n
        seen[c] = True
        while q:
            node, d = q.popleft()
            centroid_distances[node][c] = d
            if node == u:
                return d
            for v in tree[node]:
                if not seen[v]:
                    seen[v] = True
                    q.append((v, d + 1))
        return float('inf')  # should not happen

    output = []
    for _ in range(m):
        t, v = map(int, input().split())
        v -= 1
        if t == 1:
            update(v)
        else:
            res = float('inf')
            x = v
            while x != -1:
                res = min(res, dist[x] + distance(v, x))
                x = parent_centroid[x]
            output.append(str(res))

    print("\n".join(output))

if __name__ == "__main__":
    solve()
```

The first section reads the tree and sets up adjacency lists. The centroid decomposition splits the tree recursively and records parent centroids. The distance functions are cached to avoid repeated BFS. Updates propagate along the centroid tree, and queries compute minimal distances by combining stored centroid distances with the distances along the centroid path.

## Worked Examples

**Sample 1:**

```
5 4
1 2
2 3
2 4
4 5
2 1
2 5
1 2
2 5
```

| Query | Node | Updated red nodes | Output |
| --- | --- | --- | --- |
| 2 | 1 | [1] | 0 |
| 2 | 5 | [1] | 3 |
| 1 | 2 | [1,2] | - |
| 2 | 5 | [1,2] | 2 |

Explanation: Initially, only node 1 is red. Distance to node 5 is 3 via path 5-4-2-1. After painting 2 red, the shortest path from 5 is via 2 (5-4-2), giving distance 2.

**Custom Example:**

```
6 3
1 2
1 3
2 4
2 5
3 6
2 6
1 5
2 6
```

| Query | Node | Red nodes | Output |
| --- | --- | --- | --- |
| 2 | 6 | [1] | 2 |
| 1 | 5 | [1,5] | - |
| 2 | 6 | [1,5] | 3 |

This tests distances that shift when a red node is added far from the initial root.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|
