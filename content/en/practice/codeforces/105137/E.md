---
title: "CF 105137E - Good Game"
description: "The structure is a rooted tree with node 1 acting as the root, but conceptually it is drawn upside down so that gravity pushes objects toward the root. Each node can hold at most one ball. We are given a sequence of starting nodes, and we drop balls one by one."
date: "2026-06-27T18:44:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105137
codeforces_index: "E"
codeforces_contest_name: "TheForces Round #30 (Good-Forces)"
rating: 0
weight: 105137
solve_time_s: 29
verified: false
draft: false
---

[CF 105137E - Good Game](https://codeforces.com/problemset/problem/105137/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

The structure is a rooted tree with node 1 acting as the root, but conceptually it is drawn upside down so that gravity pushes objects toward the root. Each node can hold at most one ball.

We are given a sequence of starting nodes, and we drop balls one by one. When a ball is dropped at a node, it tries to move along the unique path toward the root, always going upward one edge at a time. The ball continues moving as long as the next node on that path is free. As soon as it reaches a node that is already occupied, it stops at the last free node before it. If even the starting node is already occupied, the ball cannot be placed and the answer is -1 for that ball.

The output for each ball is therefore the final node where it settles, or -1 if it never finds a free position.

The constraints are large enough that both the number of nodes and the number of balls can reach one million per test case, with a total sum across test cases up to two million. This immediately rules out any solution that simulates each ball moving step by step along the tree. A single worst-case chain of length n with m balls would already lead to 10^12 operations if simulated naively.

A direct DFS or repeated upward traversal per query will fail. Even a well-optimized adjacency traversal per ball is too slow because each ball may traverse a long chain.

A subtle edge case occurs when many balls start near leaves of a long chain.

For example, consider a chain 1 - 2 - 3 - 4 - 5 (root 1), and balls arriving at 5, 5, 5, 5. The first ball goes 5 → 4 → 3 → 2 → 1, but the second ball might stop earlier depending on occupancy. A naive simulation that does not track "next available ancestor" will repeatedly walk the same paths and degrade to quadratic behavior.

Another edge case is when the root becomes occupied early. After that, all further balls on that root path must return -1 even if lower nodes still exist.

## Approaches

A brute-force simulation processes each ball independently. For each ball, we repeatedly move from the starting node to its parent until we either reach the root or find a free node. We also check occupancy at each step.

This is correct because it directly follows the movement rules. However, each query may traverse a path of length O(n), and there are m queries, leading to O(nm) behavior in a chain-shaped tree. With n, m up to 10^6, this is impossible.

The key observation is that every node transitions from “free” to “occupied” exactly once. After a node is occupied, future balls never need to consider it again. This allows us to compress repeated upward traversals using a disjoint-set structure over the tree.

Instead of repeatedly walking upward, we maintain for each node a pointer to the nearest ancestor that is still free. When a node becomes occupied, we “merge it out” by redirecting it to its parent. A find operation then jumps directly to the next available node without scanning intermediate occupied nodes.

This turns repeated path traversal into near constant amortized time per operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal (DSU on parent pointers) | O((n + m) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each node as initially available. We also precompute each node’s parent using a BFS or DFS from the root.

We then maintain a disjoint-set structure where each node points to the next candidate ancestor.

1. Root the tree at node 1 and compute parent pointers for every node. This defines the only valid upward movement path for each node.
2. Initialize a DSU array where find(x) returns x initially. This represents that every node is currently free.
3. Process balls in order. For each starting node x, compute v = find(x)
