---
title: "CF 104872J - Streets of Flatland"
description: "We are given a connected structure made of $n$ locations connected by exactly $n-1$ undirected roads, so the underlying graph is a tree."
date: "2026-06-28T10:34:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104872
codeforces_index: "J"
codeforces_contest_name: "2023-2024 Russia Team Open, High School Programming Contest (VKOSHP XXIV)"
rating: 0
weight: 104872
solve_time_s: 29
verified: false
draft: false
---

[CF 104872J - Streets of Flatland](https://codeforces.com/problemset/problem/104872/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected structure made of $n$ locations connected by exactly $n-1$ undirected roads, so the underlying graph is a tree. Each road can be thought of as a directed segment in both directions, and the problem introduces the idea that certain consecutive roads can be merged into a single longer “highway” if they are geometrically compatible at their shared endpoint.

The key operation is local to a vertex: if two roads meet at a vertex $v$, say one arrives from $u$ to $v$ and another leaves from $v$ to $w$, then under a geometric rule based on the cyclic order of edges around $v$, these two roads may be considered compatible and can be merged into one continuous highway segment passing through $v$. Each successful merge reduces the number of separate highways by one.

The initial state is that every road behaves as an independent highway segment. Since there are $n-1$ roads, there are initially $n-1$ highways. The task is to perform as many valid merges as possible, and output the minimum number of highways that remain after all possible merges.

From a computational standpoint, the graph has $O(n)$ edges, and any solution must run in roughly linear or near-linear time. A solution that inspects pairs of roads globally would be too slow because there can be $O(n^2)$ potential interactions between incident edges across vertices.

A subtle issue appears when a vertex has multiple incident roads. A naive approach might try to greedily match roads locally without respecting global consistency. This can fail when local choices interfere with each other.

For example, consider a vertex with four incident edges arranged cyclically. If a greedy algorithm pairs the first edge with its clockwise neighbor without considering global matching structure, it might block a better pairing that yields more total merges. The correct behavior depends on the cyclic ordering, not arbitrary pairing.

The core difficulty is that compatibility is defined by angular adjacency, so correctness depends on ordering edges around each vertex, not just connectivity.

## Approaches

A brute-force interpretation would explicitly try to simulate all possible merges. One could repeatedly scan all vertices, look at all pairs of incident edges, check compatibility, and merge whenever possible. Each merge reduces the number of highways by one, and we would continue until no more merges are possible.

This approach is correct because it directly follows the definition of allowed operations. However, each merge requires scanning adjacency structures and updating them, and there can be $O(n)$ merges. Each scan over all vertices costs $O(n)$, giving $O(n^2)$ or worse behavior in total, which is too slow for $n$ up to $10^5$.

The key observation is that merges at different vertices are independent once we reinterpret the structure. Each road participates in compatibility decisions only through its local ordering around each endpoint. Therefore, we can decompose the problem vertex by vertex. At each vertex $v$, co
