---
title: "CF 1495D - BFS Trees"
description: "We are asked to count, for every pair of vertices $i, j$ in an undirected connected graph, the number of spanning trees that simultaneously behave as BFS trees rooted at both $i$ and $j$. A BFS tree rooted at $s$ preserves the shortest distances from $s$ to every other vertex."
date: "2026-06-10T22:01:06+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "graphs", "math", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1495
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 706 (Div. 1)"
rating: 2600
weight: 1495
solve_time_s: 76
verified: false
draft: false
---

[CF 1495D - BFS Trees](https://codeforces.com/problemset/problem/1495/D)

**Rating:** 2600  
**Tags:** combinatorics, dfs and similar, graphs, math, shortest paths, trees  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count, for every pair of vertices $i, j$ in an undirected connected graph, the number of spanning trees that simultaneously behave as BFS trees rooted at both $i$ and $j$. A BFS tree rooted at $s$ preserves the shortest distances from $s$ to every other vertex. Therefore, for a tree to qualify for a pair $i, j$, it must preserve shortest distances from both $i$ and $j$.

The input is an undirected graph with $n$ vertices and $m$ edges, and we are to compute $f(i, j)$ modulo $998\,244\,353$ for all $i, j$. Given that $n \le 400$ and $m \le 600$, the solution must avoid $O(n^3 \cdot 2^n)$ or similar combinatorial enumeration approaches because they exceed $10^8$ operations. A solution with complexity roughly $O(n^3 + n \cdot m)$ is feasible.

Non-obvious edge cases include graphs where some pairs of vertices are not uniquely positioned on shortest paths. For example, a 4-cycle $1-2-3-4-1$ has multiple BFS trees for adjacent vertices. Careless implementations that assume a tree is uniquely determined by one BFS could count trees incorrectly. Another subtlety arises when two vertices are at maximum distance from each other: only specific trees maintain distances from both simultaneously.

## Approaches

A brute-force approach enumerates all spanning trees, checks for BFS consistency from both roots, and counts them. This is correct but infeasible. The number of spanning trees grows exponentially with $n$, and verifying BFS conditions for each tree is $O(n)$. For $n=400$, the total operations far exceed feasible limits.

The optimal approach relies on BFS distance properties. We first precompute all-pairs shortest distances using BFS from each vertex, yielding a distance matrix $d[i][j]$. For a tree to be a BFS tree from both $i$ and $j$, each node $v$ must lie on at least one shortest path from $i$ to $j$ or connect only to neighbors that maintain the shortest distances from both roots. In other words, the BFS tree must select, for each node $v$, edges that connect it to parents at exactly one step closer to the root.

The algorithm reduces to checking, for a pair $i, j$, whether the path between them is unique in terms of distances and counting valid parent choices for every other vertex. Each vertex $v$ outside the path can attach to neighbors $u$ such that $d[i][u] = d[i][v] - 1$ and $d[j][u] = d[j][v] - 1$. The product of counts over all vertices gives the number of BFS trees for the pair. If any vertex cannot satisfy this condition, $f(i, j) = 0$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^{n-2}) | O(n^2) | Too slow |
| Optimal | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read $n, m$ and store edges in an adjace
