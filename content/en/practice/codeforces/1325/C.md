---
title: "CF 1325C - Ehab and Path-etic MEXs"
description: "We are given a tree with $n$ nodes, represented by $n-1$ edges connecting pairs of nodes. Each edge must be assigned a distinct integer label between $0$ and $n-2$."
date: "2026-06-11T16:40:17+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1325
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 628 (Div. 2)"
rating: 1500
weight: 1325
solve_time_s: 67
verified: false
draft: false
---

[CF 1325C - Ehab and Path-etic MEXs](https://codeforces.com/problemset/problem/1325/C)

**Rating:** 1500  
**Tags:** constructive algorithms, dfs and similar, greedy, trees  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ nodes, represented by $n-1$ edges connecting pairs of nodes. Each edge must be assigned a distinct integer label between $0$ and $n-2$. For any two nodes $u$ and $v$, the MEX of the path between them is defined as the smallest non-negative integer that does not appear on the edges along the unique path connecting $u$ and $v$. Our goal is to label the edges so that the maximum MEX over all possible node pairs is minimized.

The constraints indicate that $n$ can be up to $10^5$, which implies that any solution iterating over all node pairs would require on the order of $10^{10}$ operations and is therefore infeasible. This forces us to find a solution that assigns edge labels in a way that leverages the structure of the tree rather than computing all MEX values explicitly. Edge cases arise in star-shaped trees or linear chains, where naive assignments may lead to large maximum MEX values, so we must handle high-degree nodes carefully.

A small example illustrates the subtlety. For a tree of three nodes connected in a star: edges (1,2) and (1,3), assigning labels $0$ and $1$ ensures the maximum MEX is $2$. Assigning both edges labels $0$ and $2$ would unnecessarily increase the maximum MEX for the path (2,3), producing a larger result than needed.

## Approaches

A brute-force approach would attempt to assign labels to edges in every possible permutation and then compute the MEX for all $\binom{n}{2}$ node pairs. This is correct in principle but scales as $O((n-1)! \cdot n^2)$, which is completely impractical for $n = 10^5$.

The key insight comes from considering the tree's structure. The maximum MEX along a path is determined by the edges along that path. If we assign consecutive labels to edges incident to nodes of degree more than two, then the paths between high-degree nodes quickly consume the smallest available numbers. Observing that in any tree the maximum degree $\Delta$ is the number of edges incident to the most connected node, we can minimize the maximum MEX by assigning the smallest labels to edges incident to the highest-degree nodes. In practice, it suffices to detect if a node has degree three or more. If it does, the edges incident to it should receive labels starting from 0, with remaining edges assigned the next available labels. If the tree is a simple path or a star with degree at most two, we can assign labels arbitrarily along the edges because the maximum MEX will not exceed 2.

This observation reduces the problem to a simple greedy labeling based on degrees. The combinatorial explosion of the brute-force is avoided entirely by using tree degree properties.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n-1)! * n^2) | O(n^2) | Too slow |
| Degree-Based Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of nodes $n$ and store all edges in input order. Initialize an adjacency list to count the degree of each node.
2. Traverse all edges and increment the degree of both endpoints. Track the maximum degr
