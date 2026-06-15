---
title: "CF 1249F - Maximum Weight Subset"
description: "We are given a tree where each vertex carries a positive weight. The task is to select a subset of vertices that maximizes the sum of chosen weights, but with a strict geometric restriction: any two selected vertices must be more than $k$ edges apart in the tree."
date: "2026-06-15T22:01:02+07:00"
tags: ["codeforces", "competitive-programming", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1249
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 595 (Div. 3)"
rating: 2200
weight: 1249
solve_time_s: 360
verified: true
draft: false
---

[CF 1249F - Maximum Weight Subset](https://codeforces.com/problemset/problem/1249/F)

**Rating:** 2200  
**Tags:** dp, trees  
**Solve time:** 6m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where each vertex carries a positive weight. The task is to select a subset of vertices that maximizes the sum of chosen weights, but with a strict geometric restriction: any two selected vertices must be more than $k$ edges apart in the tree.

Equivalently, once we pick a vertex, we “forbid” choosing any vertex within distance $k$ from it. The goal is to place selected vertices on the tree so that their pairwise distances are all strictly greater than $k$, while maximizing the total weight.

The constraint $n \le 200$ is small enough that quadratic or cubic dynamic programming over states on nodes is viable. However, a naive subset enumeration is still impossible because $2^n$ grows far beyond feasibility even for $n = 200$. This pushes us toward a structured DP over the tree.

A subtle point is that the restriction is not local to edges, it propagates through distances in the tree. This makes the problem fundamentally different from classic independent set on trees (which corresponds to $k=1$). Here, the “exclusion zone” of a chosen node is a radius-$k$ ball in the tree.

Edge cases arise when high-weight nodes are clustered. For example, consider a chain $1-2-3-4$ with $k=2$. Choosing node 1 forbids nodes 2 and 3, but node 4 is still valid. A greedy choice of local maxima can fail: picking 2 and 4 gives more weight than picking 1 alone in some weight configurations, but selecting 2 also forbids 1 and 3, changing downstream feasibility in non-local ways.

Another edge case is when $k=0$. Then no restriction exists and all nodes can be chosen. A naive DP that always enforces a parent-child exclusion would incorrectly undercount.

Finally, when $k$ is large (close to $n$), picking even two nodes is impossible unless they are extremely far apart, so the optimal answer often degenerates to the maximum single vertex. A correct solution must handle this transition smoothly.

## Approaches

A brute-force idea is to try all subsets of vertices and check validity by computing all pairwise distances. Even if distances are precomputed with BFS from each node, checking a subset still costs $O(n^2)$, and enumerating subsets costs $2^n$, leading to roughly $O(2^n \cdot n^2)$, which is infeasible.

The key observation is that the constraint is local in the sense of tree distance. If we fix a node as chosen, its forbidden region is a subtree-shaped neighborhood bounded by distance $k$. This suggests a DP where the state must remember how “close” we are to a chosen node above in the tree.

The standard trick is to root the tree and define a DP that tracks, for each node, how far it is from the nearest chosen ancestor. However, storing exact distances to all chosen nodes is too large. Instead, we compress this into a bounded parameter: the distance from the current node to the nearest selected node in its processed subtree.

This leads to a DP over nodes where each state represents whether a node is selected and how far the closest selected node in its subtree or ancestors is, capped at $k$. Since $k \le 200$, we can maintain a DP table of size $O(nk)$ per node, combining children via tree knapsack-like transitions.

The merging step resembles multi-state propagation: when processing a node, we consider whether it is chosen, and if so, all nodes within distance $k$ in its subtree cannot be chosen. When it is not chosen, children can independently contribute with updated distance states.

This transforms the global distance constraint into local transitions on a rooted tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(2^n \cdot n^2)$ | $O(n^2)$ | Too slow |
| Tree DP with distance states | $O(nk^2)$ | $O(nk)$ | Accepted |

## Algorithm Walkthrough

We root the tree at node 1 and define a DP table for each node $u$.

Let $dp_u[d]$ represent the maximum weight in the subtree of $u$ under the condition that the closest chosen node above or inside the subtree is at distance $d$, where $d$ is capped at $k$. The value $d=0$ means $u$ is selected, and larger values represent increasing distance to the nearest selected node.

We propagate information bottom-up.

1. Initialize each node $u$ with a DP array where all states are set to negative infinity, except the case where $u$ is selected. If $u$ is selected, it contributes $a_u$, and all children must respect that no node within distance $k$ can be selected in conflicting ways.
2. Process children one by one, merging their DP tables into the current node’s DP table. The merge operation considers all pairs of states from the current DP and the child DP, updating distances appropriately by increasing distance values by 1 when moving upward.
3. If a child state indicates a selected node at distance $d$, then from the parent’s perspective that node is at distance $d+1$, capped at $k$. This shift is crucial because distance increases by exactly one when moving up one edge.
4. During merging, we ensure feasibility by discarding any combination where two selected nodes would end up at distance $\le k$. This is enforced implicitly by disallowing states that violate the distance threshold when combining DP tables.
5. After processing all children, we finalize $dp_u$ by considering both cases: $u$ is selected or not selected, and propagate results upward.

At the end, the answer is the maximum value among all states of the root node.

### Why it works

The DP invariant is that for every node $u$, $dp_u[d]$ correctly represents the optimal weight of selecting a valid subset inside the subtree of $u$, consistent with a boundary condition that the nearest selected node outside the subtree is at distance $d$. Every subtree is optimized independently under this boundary constraint, and merging children preserves feasibility because distances in a tree are uniquely defined through the root path. Since every selection conflict must pass through a lowest common ancestor, the DP ensures that any forbidden pair is detected at their merging point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    sys.setrecursionlimit(10**7)

    INF_NEG = -10**18

    # dp[u][d] where d in [0..k], capped distance to nearest chosen node above
    def dfs(u, p):
        dp = [[INF_NEG] * (k + 1) for _ in range(1)]
        dp[0][k] = 0  # no restriction coming from above

        for v in g[u]:
            if v == p:
                continue
            child = dfs(v, u)

            new_dp = [[INF_NEG] * (k + 1) for _ in range(len(dp) + len(child))]

            for i in range(len(dp)):
                for j in range(len(child)):
                    for d1 in range(k + 1):
                        for d2 in range(k + 1):
                            if dp[i][d1] == INF_NEG or child[j][d2] == INF_NEG:
                                continue

                            nd1 = min(k, d1
```
