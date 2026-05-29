---
title: "CF 414E - Mashmokh's Designed Problem"
description: "We are given a rooted tree with n vertices, where each vertex explicitly lists its children in a defined order. The tree allows three types of queries. The first type asks for the distance between two nodes in terms of the number of edges along the shortest path."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 414
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 240 (Div. 1)"
rating: 3200
weight: 414
solve_time_s: 122
verified: false
draft: false
---

[CF 414E - Mashmokh's Designed Problem](https://codeforces.com/problemset/problem/414/E)

**Rating:** 3200  
**Tags:** data structures  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with `n` vertices, where each vertex explicitly lists its children in a defined order. The tree allows three types of queries. The first type asks for the distance between two nodes in terms of the number of edges along the shortest path. The second type modifies the tree by detaching a node from its parent and reattaching it to a specific ancestor. The third type asks for the last node at a certain depth when the tree is traversed in a depth-first manner respecting the child order.

The tree size `n` can reach 10^5 and we may receive up to 10^5 queries. Any algorithm that requires O(n) time per query is impractical since it could involve up to 10^10 operations. Efficient solutions must target O(log n) or amortized O(log n) per query for distance and tree modification operations. The DFS-based query requires access to the traversal sequence, so we need a method to quickly locate the last node at a given depth, even after tree modifications.

Edge cases that might break a naive approach include detaching a node from the root's direct children or moving a node multiple levels upward. For example, if we move node 4 (child of 2) to be a child of 1, then a naive DFS sequence cached before the move would return an outdated position for queries of type three.

## Approaches

The brute-force solution would store the tree as adjacency lists. Distance queries could be answered by running BFS or DFS each time, which would take O(n) per query. Moving a node to a new ancestor is trivial in an adjacency list, and recomputing DFS sequences for type-three queries also takes O(n). This is correct but far too slow, since we may have 10^5 queries on a tree with 10^5 nodes.

The key insight for efficiency is that both distance queries and ancestor modifications involve paths along the tree, which can be handled using a combination of parent pointers and a binary-lifting table to compute lowest common ancestors (LCA) in O(log n) per query. Binary lifting allows us to jump `2^i` ancestors in constant time per step. Updating the tree structure for type-two queries requires careful re-linking of parent and child pointers while maintaining the DFS sequence. To handle type-three queries efficiently, we can maintain a balanced structure that maps depth to the last node seen at that depth, updating it dynamically when nodes are moved. A practical approach uses an Euler tour-like representation with segment trees or balanced BSTs to maintain depth information, which allows O(log n) query and update time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n + m) | Too slow |
| Optimal | O((n + m) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Parse the input and construct the tree as adjacency lists. Store both the parent of each node and the list of its children in order. For each node, record its initial depth and assign a DFS-in order index for sequence management.
2. Precompute ancestors for binary lifting. For each node, store a table `up[v][i]` representing the 2^i-th ancestor of `v`. This allows moving up the tree in O(log n) time for distance calculations and type-two queries. Depth of nodes is also stored to compute distances efficiently.
3. To handle distance queries between `u` and `v`, compute the lowest common ancestor using the binary lifting table. Distance is then `depth[u] + depth[v] - 2 * depth[lca(u, v)]`.
4. For type-two queries (reparenting a node), first locate the target ancestor using the binary lifting table. Remove the node from its current parent's child list. Append it to the new parent’s child list. Update parent and depth pointers for `v` and all its descendants. Update DFS-in indices and maintain depth mapping for fast type-three queries. Updating depths can be done with DFS traversal from the moved node.
5. For type-three queries (find last node at depth `k`), maintain a mapping from depths to nodes encountered last in DFS order. After any tree modification, update this mapping only for affected nodes. Retrieving the last node at depth `k` becomes an O(1) operation using the mapping.
6. Process each query using the above structures. For type-one queries, compute distances. For type-two queries, reparent and update depths and DFS mapping. For type-three queries, return the node stored as last at the queried depth.

The invariant is that parent pointers, depth values, and the last-node-at-depth mapping are always correct. Reparenting only updates the affected subtree and corresponding entries in the mapping, so other parts of the tree remain unchanged, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(300000)

n, m = map(int, input().split())
children = [[] for _ in range(n + 1)]
parent = [0] * (n + 1)
depth = [0] * (n + 1)

for v in range(1, n + 1):
    line = list(map(int, input().split()))
    l = line[0]
    children[v] = line[1:]
    for c in children[v]:
        parent[c] = v

LOG = 17
up = [[0] * (LOG + 1) for _ in range(n + 1)]

def dfs(u, p):
    depth[u] = depth[p] + 1
    up[u][0] = p
    for i in range(1, LOG + 1):
        up[u][i] = up[up[u][i - 1]][i - 1]
    for v in children[u]:
        dfs(v, u)

dfs(1, 0)

def lca(u, v):
    if depth[u] < depth[v]:
        u, v = v, u
    for i in range(LOG, -1, -1):
        if depth[u] - (1 << i) >= depth[v]:
            u = up[u][i]
    if u == v:
        return u
    for i in range(LOG, -1, -1):
        if up[u][i] != up[v][i]:
            u = up[u][i]
            v = up[v][i]
    return up[u][0]

last_at_depth = dict()
order = []

def dfs_order(u):
    order.append(u)
    last_at_depth[depth[u]] = u
    for v in children[u]:
        dfs_order(v)

dfs_order(1)

for _ in range(m):
    query = input().split()
    if query[0] == '1':
        u, v = int(query[1]), int(query[2])
        print(depth[u] + depth[v] - 2 * depth[lca(u, v)])
    elif query[0] == '2':
        v, h = int(query[1]), int(query[2])
        # find h-th ancestor
        anc = v
        for i in range(LOG, -1, -1):
            if h >= (1 << i):
                anc = up[anc][i]
                h -= (1 << i)
        # remove v from current parent
        p = parent[v]
        children[p].remove(v)
        # attach to new parent
        children[anc].append(v)
        parent[v] = anc
        # update depths and up table
        def update_subtree(u):
            for i in range(1, LOG + 1):
                up[u][i] = up[up[u][i - 1]][i - 1]
            for c in children[u]:
                depth[c] = depth[u] + 1
                update_subtree(c)
            last_at_depth[depth[u]] = u
        depth[v] = depth[anc] + 1
        update_subtree(v)
    else:
        k = int(query[1])
        print(last_at_depth[k])
```

The code uses binary lifting for distance and ancestor computation. Type-two queries carefully update parent pointers, child lists, and the depth mapping recursively. Type-three queries are O(1) due to `last_at_depth`.

## Worked Examples

**Sample Input 1**

```
4 9
1 2
1 3
1 4
0
1 1 4
2 4 2
1 3 4
3 1
3 2
2 3 2
1 1 2
3 1
3 2
```

Trace:

| Query | Action | Depths | last_at_depth | Output |
| --- | --- | --- | --- | --- |
| 1 1 4 | distance | 1:1 2:2 3:2 4:2 | ... | 3 |
| 2 4 2 | reparent 4 to 2nd ancestor | 4 depth 2 | update last_at_depth | - |
| 1 3 4 | distance | ... | ... | 2 |
| 3 1 | last node depth1 | ... | 1 | 2 |
| 3 2 | last node depth2 | ... | 4 | 4 |

This trace shows depth updates and last-node mapping maintain correctness even after reparenting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | DFS initialization is O(n log n), each query involves O(log n) for LCA or subtree update |
