---
title: "CF 293E - Close Vertices"
description: "We are given a tree with n vertices, where each edge carries a non-negative weight. For any two vertices, the distance between them can be measured in two ways: the number of edges along the path connecting them, and the sum of edge weights along that path."
date: "2026-06-05T17:23:30+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "trees"]
categories: ["algorithms"]
codeforces_contest: 293
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2013 - Round 2"
rating: 2700
weight: 293
solve_time_s: 41
verified: false
draft: false
---

[CF 293E - Close Vertices](https://codeforces.com/problemset/problem/293/E)

**Rating:** 2700  
**Tags:** data structures, divide and conquer, trees  
**Solve time:** 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with _n_ vertices, where each edge carries a non-negative weight. For any two vertices, the distance between them can be measured in two ways: the number of edges along the path connecting them, and the sum of edge weights along that path. Two vertices are considered _close_ if there exists a path connecting them such that the path contains at most _l_ edges and the total weight does not exceed _w_. The task is to count all unordered pairs of distinct vertices that satisfy this closeness criterion.

The input structure is incremental: each edge connects vertex _i+1_ to some previous vertex _pᵢ_, so the tree is essentially rooted at vertex 1. The tree has up to 10^5 vertices, and edge weights can reach 10^4. The path length limit _l_ can also reach 10^5, while the weight limit _w_ can be as large as 10^9.

Given the size of _n_, any algorithm that examines all pairs explicitly will be too slow. Brute force would involve O(n²) comparisons, which is roughly 10^10 operations in the worst case, far beyond feasible. This signals that we need a more sophisticated approach that leverages the tree structure to avoid redundant computations.

Edge cases arise when the limits _l_ or _w_ are very small, potentially excluding almost all pairs, or very large, effectively counting nearly all pairs. A naive approach that does not prune infeasible paths can both waste time and produce wrong results. For example, a tree of three vertices with edges of weight 10, and limits _l_ = 1, _w_ = 5, should yield zero close pairs. A careless DFS that counts all adjacent nodes would incorrectly produce non-zero counts.

## Approaches

The brute-force solution would consider every pair of vertices, compute the path length and weight using BFS or DFS, and increment a counter if both conditions are satisfied. While correct, this approach is O(n²) in both time and potentially O(n) in space for path tracking. Clearly, it fails at the problem's upper bound of 10^5 vertices.

The key insight for optimization is that we are dealing with a tree. Trees have no cycles, which allows divide-and-conquer approaches to work efficiently. One effective method is centroid decomposition. By recursively choosing a centroid, we can split the tree into smaller subtrees and count close pairs with paths passing through the centroid. For each subtree, we perform a constrained DFS to collect distances and weights, then combine the results with an efficient data structure like a Binary Indexed Tree (Fenwick Tree) or a multiset to count how many paths satisfy both constraints.

This approach exploits the fact that every path either passes through the centroid or lies entirely within a single subtree. Handling paths through the centroid separately allows us to merge subtrees without double-counting and avoids redundant pair examinations. The decomposition guarantees that each vertex is involved in O(log n) centroid levels, giving an overall complexity of O(n log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Centroid Decomposition + Fenwick Tree | O(n log n) |  |  |
