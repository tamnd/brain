---
title: "CF 104599I - Intergalactic Terrorism"
description: "We are given a rooted tree with $n$ nodes. Each node $i$ carries a positive value $ai$. The structure is already a tree, so there are exactly $n-1$ edges, each implicitly having weight $1$."
date: "2026-06-30T03:01:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104599
codeforces_index: "I"
codeforces_contest_name: "GPL 2023 Novice"
rating: 0
weight: 104599
solve_time_s: 44
verified: true
draft: false
---

[CF 104599I - Intergalactic Terrorism](https://codeforces.com/problemset/problem/104599/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with $n$ nodes. Each node $i$ carries a positive value $a_i$. The structure is already a tree, so there are exactly $n-1$ edges, each implicitly having weight $1$. On top of this structure, we are allowed to add exactly one new edge between any two distinct nodes $u$ and $v$.

Adding this edge creates exactly one simple cycle, because in a tree there is a unique path between any two nodes. That cycle consists of the original path between $u$ and $v$, plus the new edge $(u,v)$. The total “explosion magnitude” of the cycle is defined as the sum of all edge weights on that cycle. Every original edge contributes $1$, and the added edge contributes $a_u + a_v$.

So if the distance between $u$ and $v$ in the tree is $\text{dist}(u,v)$, then the resulting explosion is

$$\text{dist}(u,v) + (a_u + a_v).$$

The task is to choose the best pair $(u,v)$ to maximize this value.

The constraints allow up to $10^5$ nodes, which rules out any solution that examines all pairs explicitly. A naive $O(n^2)$ scan over pairs would require about $10^{10}$ operations, which is far beyond a 1 second limit. Even approaches that do a BFS or LCA per pair are too slow unless carefully reduced.

A key structural constraint is that the tree is given via parent pointers, meaning we can process it in rooted form and compute depths and structural aggregates efficiently.

A few edge cases expose typical mistakes. If all $a_i$ are equal, the problem reduces to maximizing $a_u + a_v + \text{dist}(u,v)$, so the best pair is simply a diameter endpoint pair. For example, in a chain of length 3 with all $a_i = 1$, the answer is $2 + 2 = 4$ plus distance $2$, total $6$. A naive approach that only considers adjacent nodes would miss this.

Another edge case is when the largest $a_i$ sits in a leaf and pairing it with a nearby node seems attractive, but the distance term dominates and forces pairing with a farthest node instead.

## Approaches

A brute-force method checks every pair $(u,v)$. For each pair, compute the tree distance, for example using LCA or BFS. Each distance query can be done in $O(\log n)$ with preprocessing, but there are $O(n^2)$ pairs, leading to $O(n^2 \log n)$. This is immediately too large for $n = 10^5$.

The key observation is that the objective splits into two parts:

$$a_u + a_v + \text{dist}(u,v).$$

The $a$-terms depend only on endpoints, while the distance depends only on the tree structure. This suggests rewriting the expression in a form where each node contributes independently along paths.

Fix a root at node $1$. Let $d[u]$ be the depth of $u$. For any pair,

$$\text{dist}(u,v) = d[u] + d[v] - 2d[\text{lca}(u,v)].$$

So the objective becomes

$$(a_u + d[u]) + (a_v + d[v]) - 2d[\text{lca}(u,v)].$$

The complication is the LCA term, which prevents full separation. However, we can reinterpret the structure: instead of thinking globally, we can root the tree and process contributions using a “best two candidates in a subtree” idea combined with rerooting-style reasoning.

For a fixed node $x$ considered as the LCA of the optimal pair, both endpoints must lie in different child subtrees of $x$, or one endpoint is $x$ itself. This reduces the problem locally: for each node, we want to know the best candidate value coming from each child subtree, measured by

$$f[u] = a_u + d[u].$$

Then for a node $x$, any pair of nodes in different child subtrees gives candidate:

$$f[u] + f[v] - 2d[x].$$

So for each node, we only need the top values from each subtree, and we maintain best combinations across children.

This transforms the problem into a tree DP where each node aggregates the best two $f$-values from its children subtrees and propagates upward.

The final answer is the best over:

1. pairing two nodes in different subtrees at some LCA
2. pairing the node with itself is invalid since $u \ne v$

### Complexity table

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Root the tree at node $1$ and compute depths $d[u]$.

Depth is needed because every edge has weight $1$, so it directly gives distances in terms of LCA.
2. Define a transformed value $f[u] = a_u + d[u]$.

This isolates node contribution from upward movement in the tree.
3. Run a postorder DFS over the tree.

Each node will compute the two largest $f$-values seen in its entire subtree, grouped by child branches.
4. At each node $x$, collect the best $f$-value coming from each child subtree.

This is necessary because any valid LCA-based pair must come from two different branches.
5. Combine the two largest such values at node $x$.

If the best values are $f[u]$ and $f[v]$ from different children, compute candidate:

$$f[u] + f[v] - 2d[x].$$

This corresponds exactly to expanding $\text{dist}(u,v)$ via LCA.
6. Track the maximum value across all nodes.

This ensures every possible LCA is considered exactly once as a structural join point.
7. Return the maximum found.

### Why it works

Every pair of nodes has a unique lowest common ancestor $x$. The contribution of that pair is fully determined at $x$ once we know the best representatives from each child subtree. The transformation $f[u] = a_u + d[u]$ converts the distance formula into a sum where the only correction term depends solely on the LCA depth, which is fixed per aggregation point. Since each pair is considered exactly at its LCA, no pair is missed and no pair is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n = int(input())
a = list(map(int, input().split()))
parent = [0] + list(map(int, input().split()))

g = [[] for _ in range(n)]
for i in range(1, n):
    p = parent[i]
    g[p-1].append(i)

depth = [0] * n

def dfs_depth(u, p):
    for v in g[u]:
        depth[v] = depth[u] + 1
        dfs_depth(v, u)

dfs_depth(0, -1)

ans = 0

def dfs(u):
    global ans
    best = []  # store f-values from different child subtrees

    f_u = a[u] + depth[u]

    for v in g[u]:
        child_best = dfs(v)
        best.append(child_best)

    # include node itself as candidate subtree
    best.append(f_u)

    # take top two
    best.sort(reverse=True)

    if len(best) >= 2:
        ans = max(ans, best[0] + best[1] - 2 * depth[u])

    return best[0]

dfs(0)

print(ans)
```

The solution first constructs the rooted tree from the parent array, then computes depths with a DFS. These depths are used to define
