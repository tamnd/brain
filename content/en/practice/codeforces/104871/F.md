---
title: "CF 104871F - Phylogenetics"
description: "We are given a special graph construction. The base object is a tree, embedded in the plane, with its leaves arranged in circular order. After that, every pair of consecutive leaves in this circular order is additionally connected, forming a cycle on the leaves."
date: "2026-06-28T10:38:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104871
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC Central Europe Regional Contest (CERC 23)"
rating: 0
weight: 104871
solve_time_s: 39
verified: false
draft: false
---

[CF 104871F - Phylogenetics](https://codeforces.com/problemset/problem/104871/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a special graph construction. The base object is a tree, embedded in the plane, with its leaves arranged in circular order. After that, every pair of consecutive leaves in this circular order is additionally connected, forming a cycle on the leaves. The final graph is therefore the union of a tree and a simple cycle that runs through all leaves in their embedding order.

The task is to count the number of proper colorings of this final graph using K colors, where adjacent vertices must always have different colors. The answer must be computed modulo 1,000,000,007.

The constraints allow up to 100,000 nodes and colors up to 100,000 as well, which immediately rules out any solution that tries to enumerate color assignments or even store dense state per vertex. A valid approach must run in roughly linear time in N or N log N at worst.

A key structural observation is that the graph is almost a tree. The only deviation from a tree is that all leaves form an additional cycle. A naive approach would treat this as a general graph coloring problem, but the tree structure strongly constrains dependencies, and the only global constraint is introduced by that leaf cycle.

A naive mistake is to ignore the embedding order of leaves and assume any ordering works. For example, if a tree has leaves 1, 2, 3, 4 in circular order, connecting them incorrectly changes the cycle structure and therefore changes the coloring count. The cycle is fixed by the planar embedding, not arbitrary leaf adjacency.

Another subtle issue is that leaves are exactly degree 1 in the tree, but after adding cycle edges, every leaf has degree 3 in the final graph. A naive tree DP that assumes leaves are independent endpoints will fail because leaves are now mutually constrained through the cycle.

## Approaches

A brute force approach would assign colors to all N nodes and check adjacency constraints. This costs K^N possibilities, which is impossible even for small N.

A slightly more structured brute force would use backtracking with pruning on edges. This still explores an exponential number of assignments in the worst case, because the graph contains a cycle on potentially many nodes. The leaf cycle alone behaves like a standard cycle graph, whose coloring count already grows as (K−1)^n plus corrections depending on parity, but here it is coupled with a tree, so constraints propagate inward.

The key observation is that the graph is a tree with an additional simple cycle only on leaves. If we remove the cycle edges, we recover a tree, and trees are easy for counting colorings via DP. The difficulty is that the leaves are no longer independent boundary conditions, since they must also satisfy cycle adjacency constraints.

We handle this by rooting the tree and doing a DP where each subtree computes a function describing how it behaves as a “colored boundary interface” at its root. For tree coloring, a node only needs to ensure it differs from its parent, so subtree contributions factor nicely. The complication comes from the cycle, which couples all leaves in a single global constraint.

The central idea is to reduce the problem to counting colorings of a cycle where each vertex has an attached subtree that contributes a multiplicative factor depending on whether the vertex color equals its parent constraints. This transforms the problem into a cycle DP with state depending only on whether adjacent leaf colors match.

Thus we separate the problem into two layers: a tree DP that compresses each leaf attachment into a weight depending on its color relative to its parent, and a cycle DP over leaves that enforces adjacency constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K^N) | O(N) | Too slow |
| Tree + Cycle DP decomposition | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We first root the tree at any node. The structure of the tree is fixed, and leaves are known.

1. Build adjacency list for the tree part, ignoring the leaf cycle edges for now. Identify all leaves; their count is L.
2. Run a DFS-based tree DP where each node computes the number of valid colorings of its subtree given that its own color is fixed relative to its parent. Since only adjacency constraints exist in the tree, each node only needs to ensure it differs from its parent, and children subtrees are independent once the node color is fixed.

For a node u, define dp[u] as the number of valid colorings of the subtree rooted at u assuming u has a fixed color that differs from its parent. The recurrence is that each child v contributes a factor that depends only on dp[v], multiplied over children, since children subtrees are independent conditioned on u's color.

1. After computing dp, each leaf u has a value that represents how many ways its subtree is colored given the color of u. Importantly, for leaves, this is trivial because a leaf has no children in the tree, so dp[u] = 1.
2. Now consider the cycle formed by leaves in their given order. Each leaf u participates in two constraints: one from its parent in the tree, and two from its neighbors in the cycle. The tree DP already ensures consistency with the parent, so the remaining constraint is only on the cycle edges.
3. For each leaf u, define a contribution function that depends on whether its color equals or differs from its cycle neighbors. Because all colors are symmetric, we compress this into a standard cycle coloring problem: count colorings of an L-cycle using K colors with adjacency constraints, multiplied by the independent tree contributions.
4. The cycle coloring count for an L-cycle is:

(K−1)^L + (−1)^L (K−1), derived from standard chromatic polyno
