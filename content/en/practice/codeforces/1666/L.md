---
title: "CF 1666L - Labyrinth"
description: "We are given a directed graph representing a labyrinth of halls and one-way passages. A traveler starts from a fixed starting hall $s$. We are allowed to choose any other hall $t$ as a meeting point."
date: "2026-06-10T02:21:17+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1666
codeforces_index: "L"
codeforces_contest_name: "2021-2022 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1800
weight: 1666
solve_time_s: 139
verified: false
draft: false
---

[CF 1666L - Labyrinth](https://codeforces.com/problemset/problem/1666/L)

**Rating:** 1800  
**Tags:** dfs and similar, graphs  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph representing a labyrinth of halls and one-way passages. A traveler starts from a fixed starting hall $s$. We are allowed to choose any other hall $t$ as a meeting point. The goal is to construct two different simple paths from $s$ to the same chosen $t$, with a strong separation condition: the two routes are not allowed to share any intermediate halls. The only vertices they may have in common are the starting point $s$ and the final meeting point $t$.

In other words, we are looking for a vertex $t$ such that there exist two internally vertex-disjoint directed paths from $s$ to $t$. We also need to explicitly output both paths.

The constraints allow up to $2 \cdot 10^5$ vertices and edges, which immediately rules out any solution that tries to enumerate all paths or repeatedly recompute reachability between pairs of vertices. Anything beyond linear or near-linear complexity in $n + m$ will be too slow, so the solution must be essentially a single graph traversal with careful bookkeeping.

A naive attempt would be to pick a candidate $t$ and run two shortest path or DFS constructions while forbidding already used nodes. This fails because the choice of the first path can block the second path even when a valid pair exists. For example, if both valid paths diverge early and rejoin late, greedily committing to one route will destroy the other.

Another subtle failure case occurs when there are multiple overlapping partial paths. A DFS that simply records parents can produce one valid path but gives no guarantee that another disjoint route exists to the same endpoint.

The key difficulty is that we are not just searching for reachability, but for _two independent ways_ to reach the same vertex without sharing internal structure.

## Approaches

A brute-force idea is to consider every possible target $t$, and for each one try to find two vertex-disjoint paths from $s$ to $t$. This can be modeled using flow: split every vertex (except $s$ and $t$) into in-out nodes and run a max-flow check with unit capacities. If the max flow is at least 2, the vertex works.

This approach is correct, but extremely expensive. Running a flow algorithm for each possible $t$ would lead to roughly $n$ flow computations, each potentially $O(m \sqrt n)$ or worse, which is far beyond the limits.

The key insight is that we do not need to test every $t$. Instead, we can build a _single rooted exploration from $s$_ and detect the first point where two independent “branches” of reachability collide.

Think of exploring the graph from $s$. Each outgoing neighbor of $s$ starts a separate exploration “color”. If a vertex is reached by two different colors, then there are two vertex-disjoint ways to reach it: one through each colored subtree. Since each color expansion is a DFS that never merges paths internally, the two routes remain disjoint until the first collision point.

This converts the problem into detecting the first node that is reachable from at least two distinct DFS trees rooted at neighbors of $s$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Multi-flow / per-target disjoint path check | $O(n \cdot \text{flow})$ | $O(n)$ | Too slow |
| Multi-source DFS coloring from neighbors of $s$ | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat each neighbor of $s$ as a separate source of propagation and track which “branch of $s$” first reaches every node.

1. Start by assigning a distinct identifier to each outgoing neighbor of $s$. These identifiers represent independent exploration trees.
2. For every neighbor $v$ of $s$, run a DFS starting from $v$, marking all reachable nodes with the identifier of $v$, and recording parent pointers inside that DFS tree.

The DFS never revisits already assigned nodes, because once a node is claimed by a branch, we do not overwrite it.
3. During DFS, whenever we try to visit a node that is already assigned to a _different_ branch, we immediately stop and fix this node as our meeting point $t$.

This moment is crucial: the node $t$ has now been reached from two distinct subtrees that originate from different neighbors of $s$.
4. Once such a node $t$ is found, reconstruct two paths:

- First path: follow parent pointers from $t$ back to its branch root, then prepend $s$.
- Second path: do the same using the second branch that also reached $t$.
5. Output the two reconstructed paths.

The reason we explicitly track parents per branch is that each branch DFS produces a tree structure, so every node has a unique predecessor inside that branch, making reconstruction straightforward.

### Why it works

Each node (except $s$) is permanently assigned to exactly one branch, meaning every internal vertex belongs to a single DFS tree rooted at a neighbor of $s$. If a node $t$ is first encountered from a second branch, it means there exist two directed paths from $s$ to $t$ that diverge immediately at $s$ and never intersect again before $t$. This ensures internal vertex-disjointness, since no internal node can belong to both branches simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, m, s = map(int, input().split())
g = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    g[u].append(v)

# branch_id[v] = which child-o_
```
