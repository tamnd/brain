---
title: "CF 104619F - Finding Bridges"
description: "We are given an undirected simple graph and a sequence of edge deletions. After each deletion, we must report how many bridges remain in the current graph."
date: "2026-06-29T17:26:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104619
codeforces_index: "F"
codeforces_contest_name: "2023 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 104619
solve_time_s: 21
verified: false
draft: false
---

[CF 104619F - Finding Bridges](https://codeforces.com/problemset/problem/104619/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected simple graph and a sequence of edge deletions. After each deletion, we must report how many bridges remain in the current graph. A bridge is an edge whose removal would increase the number of connected components, so it is an edge that is not part of any cycle in the current graph.

The graph changes only by deleting edges, never by adding them. This direction matters because connectivity only weakens over time, and once a structure becomes acyclic in some region, it never regains cycles.

The constraints allow up to 200,000 vertices, edges, and queries. Any solution that recomputes bridges from scratch after each deletion would repeatedly run a linear or near linear DFS or Tarjan procedure. That would lead to roughly O(q(n + m)) operations, which in the worst case is about 4 × 10^10 operations, far beyond feasible limits.

A subtle issue appears when thinking locally. Removing an edge might destroy cycles and create new bridges, but it can also eliminate a bridge if that edge was itself a bridge. This bidirectional effect means we cannot maintain a simple static marking of bridges without a dynamic structure that supports changes in connectivity.

A naive mistake is to recompute bridges only in affected components or assume only nearby edges change status. For example, consider a chain of cycles connected by single edges. Removing one edge can propagate bridge status changes across the entire structure, not locally.

## Approaches

The brute force idea is straightforward. After each deletion, rebuild the graph and run a standard bridge-finding DFS such as Tarjan’s algorithm. This correctly recomputes all low-link values and identifies edges that are not part of any cycle. However, doing this q times repeats a full O(n + m) traversal per query, which is too slow.

The key observation is that deleting edges is hard to handle directly in a dynamic graph, but adding edges is much easier if we process in reverse. If we reverse the sequence
