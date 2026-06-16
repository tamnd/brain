---
title: "CF 1037D - Valid BFS?"
description: "We are given a tree with vertices labeled from 1 to n, and a proposed ordering of all vertices. The task is to decide whether this ordering could arise from running a breadth-first search starting at vertex 1, under some valid choice of adjacency ordering."
date: "2026-06-16T18:47:21+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1037
codeforces_index: "D"
codeforces_contest_name: "Manthan, Codefest 18 (rated, Div. 1 + Div. 2)"
rating: 1700
weight: 1037
solve_time_s: 293
verified: false
draft: false
---

[CF 1037D - Valid BFS?](https://codeforces.com/problemset/problem/1037/D)

**Rating:** 1700  
**Tags:** dfs and similar, graphs, shortest paths, trees  
**Solve time:** 4m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with vertices labeled from 1 to n, and a proposed ordering of all vertices. The task is to decide whether this ordering could arise from running a breadth-first search starting at vertex 1, under some valid choice of adjacency ordering.

The key subtlety is that BFS is not deterministic on a tree because when we expand a node, we are free to visit its unvisited neighbors in any order. Different adjacency exploration orders can produce different global BFS sequences. The question is not whether the sequence is the lexicographically smallest BFS or a BFS with sorted adjacency, but whether there exists any neighbor ordering that produces exactly the given sequence.

The constraint n up to 200,000 implies that any solution must be linear or near linear. An O(n log n) approach is acceptable, but anything that repeatedly sorts or simulates BFS with expensive data structures per node must be carefully designed to avoid quadratic behavior. The tree structure guarantees n minus 1 edges, so adjacency lists are sparse, and we can rely on standard graph traversal techniques.

A naive but tempting idea is to simulate BFS while trying to match the given sequence greedily. This fails because BFS allows multiple valid frontier expansions, and wrong local decisions about adjacency order can lead to incorrect rejection.

A few important edge cases illustrate the pitfalls. First, if the sequence does not start with 1, it is immediately invalid, since BFS always starts there. For example, input with sequence `2 1 3` on a valid tree must output "No". Second, even if the sequence starts correctly, a locally valid step can still break global validity. For instance, if the queue contains nodes `{2, 3}` but the sequence expects visiting a deep descendant of 2 before finishing all neighbors of 1, that is impossible in BFS regardless of adjacency order.

## Approaches

A brute-force interpretation would try all possible adjacency orderings for each node, run BFS for each ordering, and check whether the resulting traversal matches the target sequence. Since each node of degree d has d! permutations, this quickly explodes. Even in a tree, worst-case degrees can be large, so this is exponential in practice and completely infeasible.

The key insight is that BFS does not depend on the exact order in which we enqueue neighbors locally, but rather on the global constraint that nodes are visited in layers. If we fix a target BFS order, then nodes should be grouped by increasing distance from 1, and within the same distance layer, the relative order must be consistent with a BFS frontier expansion.

We can reverse the perspective: instead of simulating BFS freely, we simulate it while forcing that the queue processes vertices in the exact order given by the sequence. We use a queue and compare it against the sequence, but the critical trick is that when expanding a node, we collect all its unvisited neighbors and assign them an order induced by their positions in the target sequence. If the sequence is valid BFS, then for each node, its children in BFS tree must appear as a contiguous block in the sequence immediately
