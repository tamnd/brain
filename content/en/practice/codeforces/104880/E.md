---
title: "CF 104880E - Serval \u7684\u6811"
description: "We are given a tree with $n$ labeled nodes. We are allowed to repeatedly perform an operation where we pick a currently existing node, remove it, and delete all edges incident to it. Each such operation counts as one step."
date: "2026-06-28T09:21:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104880
codeforces_index: "E"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Preliminary"
rating: 0
weight: 104880
solve_time_s: 31
verified: false
draft: false
---

[CF 104880E - Serval \u7684\u6811](https://codeforces.com/problemset/problem/104880/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ labeled nodes. We are allowed to repeatedly perform an operation where we pick a currently existing node, remove it, and delete all edges incident to it. Each such operation counts as one step. After performing any number of operations, we look at what remains of the graph: some nodes and some edges between them.

The objective is to minimize a combined cost consisting of two parts. First is the number of deletion operations performed. Second is the number of edges still present in the graph after all deletions. The task is to choose which vertices to remove so that the sum of these two quantities is as small as possible.

The key interaction is that deleting a vertex removes all its incident edges immediately, so every edge is either eliminated because at least one endpoint is deleted, or survives because both endpoints are kept. Thus the remaining edges are exactly those induced by the set of vertices we decide not to delete.

Since the input is a tree, there are initially $n-1$ edges and no cycles. The constraint $n \le 5 \cdot 10^5$ implies any solution must be essentially linear or $O(n \log n)$. Quadratic or even $O(n^{1.5})$ approaches are impossible because they would exceed roughly $10^8$ operations in one second.

A naive interpretation would try all subsets of vertices to keep or delete, compute induced edges, and evaluate the cost. That is exponential and immediately infeasible.

A more subtle issue appears when thinking locally. For example, one might try to greedily delete leaves or high-degree nodes without considering global structure. On a simple path like $1 - 2 - 3 - 4$, deleting a middle node reduces edges more effectively than deleting endpoints, but the optimal pattern depends on how deletions interact across the whole tree, so purely local greedy rules can fail.

## Approaches

The problem becomes clearer if we reinterpret the cost in terms of the final set of kept vertices. Suppose we decide to keep a subset $S$. Then the number of operations equals $n - |S|$, since every deleted vertex contributes exactly one operation. The remaining edges are exactly those with both endpoints in $S$, which is the number of edges in the induced subgraph $G[S]$.

So the objective becomes:

$$(n - |S|) + |E(S)| = n + (|E(S)| - |S|)$$

Since $n$ is fixed, we are minimizing:

$$|E(S)| - |S|$$

Now we work entirely with the induced subgraph. For a tree, this expression has a very important structure: each connected component in $S$ is still a tree (because we only remove vertices, not create cycles). If a component has $k$ vertices, it has $k-1$ edges, contributing:

$$(k-1) - k = -1$$

So every connected component contributes exactly $-1$ to the objective, regardless of its size. Therefore, maximizing the number of connected components in the chosen vertex set $S$ minimizes the cost.

The problem reduces to selecting a subset of vertices that maximizes the number of connected components induced in a tree.

Now observe what controls connectivity: a component disappears when a vertex deletion splits it. Each kept vertex induces connections through edges; removing a vertex increases the number of components by the number of separated parts it creates among its neighbors in the kept set.

This leads to a standard tree DP formulation where we root the tree and decide whether each node is kept or deleted. If a node is kept, it may connect multiple kept child subtrees into one component; if it is deleted, it separates everything below it.

The optimal structure ends up being governed by a simple state per node: whether the node is included or not, and how many “active connections” it contributes upward. The final solution reduces to computing, via DP, the best achievable contribution of each subtree under these two choices.

The brute force would enumerate keep/delete for every node and recompute components, costing $O(2^n)$. The observation that the objective decomposes over connected components allows a tree DP in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Tree DP | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We root the tree at node 1 and compute a DP value for each node.

Let us define two states for each node $u$:

1. $dp_0[u]$: best contribution of the subtree of $u$ if $u$ is deleted.
2. $dp_1[u]$: best contribution if $u$ is kept.

We compute these bottom-up.

1. Initialize $dp_0[u] = 0$ for all nodes, because deleting $u$ removes it and we only combine contributions of children as separate subproblems._
