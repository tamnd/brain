---
title: "CF 1246F - Cursor Distance"
description: "We are given a string of lowercase letters, where each position acts like a “tile” labeled by a character. A cursor sits on one of these positions, and we are allowed to move it using a special jump operation: pick a character and a direction, and the cursor teleports to the…"
date: "2026-06-15T04:52:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1246
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 596 (Div. 1, based on Technocup 2020 Elimination Round 2)"
rating: 3500
weight: 1246
solve_time_s: 80
verified: false
draft: false
---

[CF 1246F - Cursor Distance](https://codeforces.com/problemset/problem/1246/F)

**Rating:** 3500  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase letters, where each position acts like a “tile” labeled by a character. A cursor sits on one of these positions, and we are allowed to move it using a special jump operation: pick a character and a direction, and the cursor teleports to the nearest occurrence of that character in that direction.

The key point is that movement is not geometric distance on indices, but graph-like navigation through repeated characters. From any position, the cursor can “see” only the next occurrence of each character on the left or right, and can jump there in one step.

For every pair of positions $i, j$, we define $\mathrm{dist}(i, j)$ as the minimum number of such jumps needed to move the cursor from $i$ to $j$. The task is to sum this distance over all ordered pairs.

The string length is up to $10^5$, so any method that tries to compute shortest paths independently for each start position will fail immediately. Even $O(n^2)$ storage or traversal is already too large, and anything resembling all-pairs BFS is impossible.

A subtle edge case appears when characters are unique or nearly unique. If every character occurs once, every jump is useless, so $\mathrm{dist}(i,j)=0$ when $i=j$ and $1$ otherwise. Any correct solution must naturally collapse to this behavior without special casing.

Another nontrivial case is highly repetitive strings like `"aaaaa..."`. Here every position is adjacent in the “jump graph”, so the structure becomes dense and naive simulation would explode in transitions.

## Approaches

A direct approach is to view each position as a node in a graph, where edges represent valid cursor jumps. From a node $i$, for each character $c$, there are at most two outgoing edges: the closest occurrence of $c$ on the left and on the right. This defines a graph with $O(n)$ nodes and $O(n)$ edges.

If we run a BFS from every node to compute shortest paths, the cost becomes $O(n^2)$ BFS expansions, which is far beyond limits. Even a single BFS is $O(n)$, so total work becomes $O(n^2)$.

The key observation is that we are not asked for individual distances, but for the sum over all pairs. This suggests reversing the viewpoint: instead of asking how far each pair is, we ask how many pairs are separated by at least $k$ steps, and aggregate contributions level by level.

A more structural insight is that each character class induces a “next occurrence graph” which is a set of disjoint bidirectional chains. Any shortest path alternates between moving along these chains through different character types. This allows us to compress transitions and treat the problem as contributions from intervals between consecutive occurrences.

The final solution reduces to counting contributions of segments defined by occurrences of each character, and summing how many pairs require crossing each boundary in an implicit layered structure. This leads to an $O(n \log n)$ or $O(n)$ counting approach depending on implementation, by processing occurrences and maintaining contributions with Fenwick-style accumulation or prefix frequency bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS from each node | $O(n^2)$ | $O(n)$ | Too slow |
| Occurrence-based contribution counting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each character, store all indices where it appears.

This is necessary because every allowed move depends only on nearest occurrences in a direction.
2. For each position $i$, determine its outgoing “jump targets” by looking at adjacent occurrences of every character.

These targets define an implicit graph without explicitly building all edges.
3. Observe that shortest
