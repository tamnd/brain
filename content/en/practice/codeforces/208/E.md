---
title: "CF 208E - Blood Cousins"
description: "We are given a rooted forest where each person has at most one parent. If we follow parent pointers upward, we eventually reach a root or fall off the structure. This defines a collection of trees. A “k-th ancestor” means applying the parent relation k times."
date: "2026-06-03T17:24:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 208
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 130 (Div. 2)"
rating: 2100
weight: 208
solve_time_s: 110
verified: false
draft: false
---

[CF 208E - Blood Cousins](https://codeforces.com/problemset/problem/208/E)

**Rating:** 2100  
**Tags:** binary search, data structures, dfs and similar, trees  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted forest where each person has at most one parent. If we follow parent pointers upward, we eventually reach a root or fall off the structure. This defines a collection of trees.

A “k-th ancestor” means applying the parent relation k times. So the 1-ancestor is the parent, the 2-ancestor is the parent of the parent, and so on, provided the chain exists.

For each query consisting of a person v and a distance p, we are asked to count how many other people share the same p-th ancestor as v. In other words, we look at the node u obtained by climbing p steps from v, and we count how many nodes in the entire forest also have u as their p-th ancestor. The answer excludes v itself.

The constraints push us away from any per-query traversal. With up to 100000 nodes and 100000 queries, a solution that walks upward p steps per query becomes quadratic in the worst case. Even a solution that precomputes all ancestors explicitly would require too much memory.

The key structure is that ancestor relationships are fixed by depth in a tree, so nodes that share the same ancestor at distance p form a contiguous grouping in a DFS ordering. This suggests preprocessing subtree structures so we can answer “how many nodes at a given depth exist in a subtree”.

A subtle edge case comes from nodes whose p-th ancestor does not exist. If v is too shallow, the answer must be zero. Another case is when multiple roots exist, since the input is a forest, not a single tree. Any DFS-based solution must handle multiple roots correctly.

## Approaches

A direct approach computes the p-th ancestor of each query node by walking up pointers, then scans the entire node set to count matches. This is correct but extremely slow. Each query can take O(n) in the worst case, leading to O(nm) operations, which is infeasible at 10^10 scale.

A better perspective comes from reversing the problem. Instead of asking “who shares my p-th ancestor”, we can fix a node u and ask: how many nodes have u as their p-th ancestor? This depends on the structure of the subtree rooted at u and the depth distribution inside it.

If we run a DFS from each root, we can record entry times and subtree ranges. We also compute depth of every node. Then for any node u, all nodes in its subtree appear in a contiguous segment in Euler tour order. Among these, the nodes at depth depth[u] + p are exactly those whose p-th ancestor is u.

So we need fast queries of the form: in subtree of u, how many nodes have depth exactly d. This becomes a classic offline grouping problem. We store nodes grouped by depth, and maintain for each depth a sorted list of DFS entry times. Then each query reduces to two binary searches on that list restricted to the subtree interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force ancestor walking | O(nm) | O(n) | Too slow |
| DFS + depth buckets + binary search | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build adjacency lists for the forest using the parent array. Each node with parent 0 is treated as a root. This ensures we can traverse every tree independently.
2. Run a DFS from each root, assigning each node a depth and recording its entry time tin and exit time tout. The DFS order ensures that the subtree of any node forms a continuous interval in the Euler tour.
3. For each depth value, maintain a list of entry times of nodes that appear at that depth. This groups nodes by level in a way that preserves DFS ordering.
4. For a query (v, p), compute u = ancestor p steps above v using a precomputed binary lifting table. If u does not exist, return 0 immediately because no node can share a non-existent ancestor.
5. Once u is found, we want to count nodes in subtree(u) whose depth equals depth[u] + p. We take the list corresponding to that target depth and count how many entry times lie inside [tin[u], tout[u]] using binary search.
6. Return this count minus 1 if v itself is included in the range, since the problem asks for “other people”, not including v.

Why it works is based on two structural properties of DFS on trees. First, all nodes in a subtree correspond exactly to a contiguous segment in Euler tour order. Second, depth is constant along ancestor-to-descendant differences, so nodes whose p-th ancestor is u must lie exactly p levels below u and inside its subtree. These two constraints uniquely characterize the valid nodes, so counting them via intersection of a depth bucket and subtree interval cannot overcount or miss any valid node.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(200000)

n = int(input())
parent = list(map(int, input().split()))

g = [[] for _ in range(n)]
roots = []

for i, p in enumerate(parent):
    if p == 0:
        roots.append(i)
    else:
        g[p - 1].append(i)

LOG = 17
up = [[-1] * n for _ in range(LOG)]
depth = [0] * n
tin = [0] * n
tout = [0] * n
timer = 0

depth_nodes = {}

def dfs(v, p):
    global timer
    tin[v] = timer
    timer += 1

    up[0][v] = p
    for i in range(1, LOG):
        if up[i - 1][v] != -1:
            up[i][v] = up[i - 1][up[i - 1][v]]

    d = depth[v]
    if d not in depth_nodes:
        depth_nodes[d] = []
    depth_nodes[d].append(tin[v])

    for to in g[v]:
        depth[to] = d + 1
        dfs(to, v)

    tout[v] = timer - 1

for r in roots:
    dfs(r, -1)

def lift(v, k):
    for i in range(LOG):
        if v == -1:
            return -1
        if k & (1 << i):
            v = up[i][v]
    return v

m = int(input())
out = []

for _ in range(m):
    v, p = map(int, input().split())
    v -= 1
    u = lift(v, p)

    if u == -1:
        out.append("0")
        continue

    target_depth = depth[u] + p
    arr = d
```
