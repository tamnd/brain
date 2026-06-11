---
title: "CF 1312G - Autocompletion"
description: "We are given a rooted construction of many strings where every node represents a string and every edge corresponds to appending one character. The root is the empty string, and each node i is created by taking its parent string pi and appending a lowercase letter ci."
date: "2026-06-11T17:13:53+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp"]
categories: ["algorithms"]
codeforces_contest: 1312
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 83 (Rated for Div. 2)"
rating: 2600
weight: 1312
solve_time_s: 51
verified: false
draft: false
---

[CF 1312G - Autocompletion](https://codeforces.com/problemset/problem/1312/G)

**Rating:** 2600  
**Tags:** data structures, dfs and similar, dp  
**Solve time:** 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted construction of many strings where every node represents a string and every edge corresponds to appending one character. The root is the empty string, and each node i is created by taking its parent string p_i and appending a lowercase letter c_i. This defines a tree where each node corresponds to a unique string.

From this tree, a subset of nodes is marked as “target strings”. For each target string, we must compute the minimum time to construct it starting from the empty string using two types of operations. One operation appends a single character, always costing one second, which corresponds to walking down one edge in the tree. The other operation is an autocompletion step: from a current string t, we look at all strings in the set S that have t as a prefix, sort them lexicographically, and we may jump to any of them in time equal to its rank in that sorted list.

The key difficulty is that autocompletion depends on lexicographic ordering among only the valid target strings under a prefix, while append operations depend on the full trie structure.

The constraints go up to n = 10^6, so any solution must be essentially linear or near-linear. A quadratic approach that recomputes prefix sets or sorts per node is immediately impossible, since even O(n log n) repeated per node would exceed limits. This pushes us toward a tree DP or DFS-based aggregation where each node is processed once and information is merged carefully.

A subtle failure case comes from misunderstanding autocompletion scope. The ranking is not among all descendants in the tree, but only among nodes that are in S and share the prefix. If one incorrectly includes all nodes or ignores lexicographic ordering, the computed cost becomes inconsistent.

## Approaches

A direct simulation would try to compute, for each target string, all valid prefixes and at each prefix compute the lexicographic list of matching strings. This quickly becomes infeasible: a node can have O(n) descendants, and sorting or maintaining ordered sets per node leads to O(n^2) or O(n log n) per node behavior in worst cases.

The key observation is that lexicographic structure of strings in a trie can be handled by processing children in character order and maintaining a DFS ordering of target nodes. Instead of recomputing prefix sets repeatedly, we compute for each node how many target nodes exist in its subtree and maintain a consistent traversal order over only relevant nodes.

We interpret the problem
