---
title: "CF 104874J - Just the Last Digit"
description: "We are given a directed acyclic structure over $n$ ordered nodes, where edges only go from a smaller index to a larger index. Think of it as a downhill graph: from every spot $i$, you can only move to higher-indexed spots $j i$ if a trail exists."
date: "2026-06-28T10:08:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104874
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104874
solve_time_s: 22
verified: false
draft: false
---

[CF 104874J - Just the Last Digit](https://codeforces.com/problemset/problem/104874/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed acyclic structure over $n$ ordered nodes, where edges only go from a smaller index to a larger index. Think of it as a downhill graph: from every spot $i$, you can only move to higher-indexed spots $j > i$ if a trail exists.

The input matrix does not directly describe the trails. Instead, it gives, for every pair $i < j$, only the last digit of the number of different directed paths from $i$ to $j$. A path is any sequence of nodes where each consecutive pair is connected by a trail. The actual number of paths can be very large, but we only observe it modulo 10.

The task is to reconstruct the adjacency matrix of the original graph, meaning we must determine for each pair $i < j$ whether a direct trail exists.

The constraints allow $n \le 500$. Any solution that tries to explicitly count all paths between all pairs would require handling up to $O(n^2)$ values, each depending on potentially $O(n)$ transitions, which pushes toward $O(n^3)$ or worse. That is acceptable, but only if the transitions are simple arithmetic; any exponential enumeration of paths is impossible.

A subtle issue is that we only see path counts modulo 10, which loses most arithmetic structure. In particular, different graphs can produce the same last-digit matrix, so reconstruction must rely on structural constraints rather than numeric inversion.

A key edge case is when multiple indirect paths mask or mimic direct edges modulo 10. For example, if there are 10 distinct paths from $i$ to $j$ via intermediates, the last digit is 0, making it indistinguishable from “no path” at first glance. This makes naive “edge detection from nonzero counts” incorrect.

Another edge case is a node pair where there is no direct edge but multiple indirect paths still produce a nonzero last digit. Any approach that assumes “nonzero implies edge” fails immediately.

## Approaches

The natural starting point is to think in terms of dynamic programming over paths. Since edges only go forward, the number of paths $dp[i][j]$ can be computed as:

$$dp[i][j] = \sum_{i \to k \to j} dp[i][k] \cdot adj[k][j]$$

If the adjacency matrix were known, computing all path counts mod 10 is straightforward in $O(n^3)$. However, we are solving the inverse problem: we are given $dp[i][j] \bmod 10$ and must recover $adj[i][j]$.

A brute-force idea is to decide each edge $adj[i][j]$ independently and check consistency by recomputing all path counts. For each pair we could try both possibilities and validate the resulting matrix. This leads to an exponential search space of size $2^{O(n^2)}$, which is immediately infeasible.

The key observation is that because edges only go from smaller to larger indices, we can process nodes in increasing order and maintain correctness of already fixed rows. When deciding edges from a node $i$, all contributions from intermediate nodes $k > i$ are not yet fixed, but contributions from earlier nodes are already determined. This creates a dependency direction that allows incremental reconstruction.

Th
