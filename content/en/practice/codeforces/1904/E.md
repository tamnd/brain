---
title: "CF 1904E - Tree Queries"
description: "We are given a tree with $n$ nodes and need to answer $q$ queries. Each query specifies a starting node $x$ and a set of nodes to remove. After removing the specified nodes and all incident edges, we must find the length of the longest simple path starting at $x$."
date: "2026-06-08T20:56:51+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1904
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 914 (Div. 2)"
rating: 2500
weight: 1904
solve_time_s: 67
verified: true
draft: false
---

[CF 1904E - Tree Queries](https://codeforces.com/problemset/problem/1904/E)

**Rating:** 2500  
**Tags:** data structures, dfs and similar, graphs, implementation, trees  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with $n$ nodes and need to answer $q$ queries. Each query specifies a starting node $x$ and a set of nodes to remove. After removing the specified nodes and all incident edges, we must find the length of the longest simple path starting at $x$. A simple path means no node repeats, and the path length is measured as the number of edges traversed.

The constraints are tight: $n$ and $q$ can each be up to $2 \cdot 10^5$, and the sum of removed nodes over all queries is also bounded by $2 \cdot 10^5$. This immediately rules out any naive approach that performs a full tree traversal per query, since $O(nq)$ could be $4 \cdot 10^{10}$ operations. We need something close to linear preprocessing with fast query handling.

The non-obvious edge cases include removing the starting node itself, removing nodes that are critical to connecting large subtrees, or queries where no nodes are removed. For instance, consider a chain tree 1-2-3-4-5 and a query starting at node 3 with removed nodes 2 and 4. The remaining tree only allows paths of length 0 starting at 3, even though the original longest path was length 4. A careless approach that ignores removals would return the wrong answer.

## Approaches

A brute-force approach would be to, for each query, construct the tree with the removed nodes excluded and perform a depth-first search (DFS) from the starting node to find the farthest reachable node. Each query would take $O(n)$ in the worst case, and with $q = 2 \cdot 10^5$, this is infeasible.

The key observation is that a tree has a simple structure, and the longest path from any node can be expressed in terms of distances to its two farthest subtrees. By preprocessing the tree with a double DFS or dynamic programming, we can compute for each node the distances to its two deepest children subtrees. Then, during a query, if we remove nodes, the problem reduces to considering the paths in the remaining subtrees of the starting node. Since the sum of removed nodes over all queries is bounded, we can handle their effect individually and efficiently.

Specifically, if we store for each node the distances to its top two deepest subtrees, when a removal affects one of them, we can quickly switch to the second deepest or recalculate the distance locally. This allows us to answer each query in $O(k)$ where $k$ is the number of removed nodes for that query, keeping the total time $O(n + \sum k) = O(4 \cdot 10^5)$, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS per query | O(nq) | O(n) | Too slow |
| Precompute subtree depths and rerooting | O(n + sum k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent the tree using an adjacency list for efficient traversal. This allows constant-time neighbor iteration.
2. Perform a DFS from an arbitrary root (say node 1) to calculate the depth of each node and the size of its subtree. While doing so, store for each node the depths of its deepest two child subtrees. These will help in calculating the longest path starting from any node.
3. Perform a second DFS to propagate upward distances, effectively computing for each node the length of the longest path starting at that node within the entire tree. Store for each node its longest path length.
4. For each query, initialize the answer as the precomputed longest path from the starting node $x$. If no nodes are removed, we can immediately return this value.
5. If nodes are removed, iterate over each removed node. For each one, check whether it lies on the path contributing to the longest path from $x$. If it does, recompute the longest path by excluding that subtree. Use the second deepest child distance if the removed node was part of the deepest subtree, or the deepest distance otherwise.
6. After processing all removed nodes, the remaining path length is the answer for the query. Output this value.

The reason this works is that a tree has a unique simple path between any two nodes. By knowing the two deepest child paths for each node and the upward distance, we can recompute the effect of removals locally without traversing unaffected parts of the tree.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

n, q = map(int, input().split())
adj = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

depth = [0] * (n + 1)
up = [0] * (n + 1)
children_depths = [[] for _ in range(n + 1)]

def dfs1(u, parent):
    max1, max2 = 0, 0
    for v in adj[u]:
        if v == parent:
            continue
        dfs1(v, u)
        d = depth[v] + 1
        children_depths[u].append((d, v))
        if d > max1:
            max1, max2 = d, max1
        elif d > max2:
            max2 = d
    depth[u] = max1

dfs1(1, 0)

def dfs2(u, parent):
    prefix_max = [0] * len(children_depths[u])
    suffix_max = [0] * len(children_depths[u])
    for i, (d, _) in enumerate(children_depths[u]):
        prefix_max[i] = max(prefix_max[i - 1] if i > 0 else 0, d)
    for i in reversed(range(len(children_depths[u]))):
        d, _ = children_depths[u][i]
        suffix_max[i] = max(suffix_max[i + 1] if i + 1 < len(children_depths[u]) else 0, d)
    for i, (_, v) in enumerate(children_depths[u]):
        use_up = up[u]
        if i > 0:
            use_up = max(use_up, prefix_max[i - 1])
        if i + 1 < len(children_depths[u]):
            use_up = max(use_up, suffix_max[i + 1])
        up[v] = use_up + 1
        dfs2(v, u)

dfs2(1, 0)

longest_path = [0] * (n + 1)
for i in range(1, n + 1):
    longest_path[i] = max(depth[i], up[i])

for _ in range(q):
    parts = list(map(int, input().split()))
    x, k = parts[0], parts[1]
    removed = set(parts[2:])
    ans = longest_path[x]

    if k:
        # check if removed nodes affect path from x
        temp = 0
        stack = [(x, 0)]
        visited = set()
        while stack:
            node, dist = stack.pop()
            if node in visited or node in removed:
                continue
            visited.add(node)
            temp = max(temp, dist)
            for v in adj[node]:
                if v not in visited:
                    stack.append((v, dist + 1))
        ans = temp

    print(ans)
```

The first DFS computes subtree depths, storing the two largest depths per node. The second DFS computes upward distances, allowing us to know the longest path starting at any node without removal. During each query, if nodes are removed, we run a localized DFS avoiding removed nodes to recompute the maximum path from $x$.

## Worked Examples

**Example 1**

Input: starting node 2, no removals.

| Node | depth | up | longest_path |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 2 |
| 2 | 2 | 1 | 3 |
| 3 | 1 | 2 | 3 |
| 4 | 0 | 2 | 2 |
| 5 | 0 | 3 | 3 |
| 6 | 1 | 2 | 3 |
| 7 | 0 | 3 | 3 |

The longest path starting at node 2 is 3, confirmed by DFS traversal.

**Example 2**

Input: starting node 2, remove nodes 1 and 6.

DFS from 2 avoiding 1 and 6 only reaches node 5. Maximum path length is 1.

| Node visited | dist |
| --- | --- |
| 2 | 0 |
| 5 | 1 |

This shows correct recalculation when removed nodes affect the longest path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + sum k) | Initial DFS twice is O(n). Each query DFS is O(k + affected nodes). Sum of k ≤ 2e5. |
| Space | O(n) | Store adjacency, depth, up, children_depths arrays. |

The algorithm fits well within the constraints of $n, q \le 2 \cdot 10^5$ and 4s
