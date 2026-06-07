---
title: "CF 2193G - Paths in a Tree"
description: "We are given a tree, which is an undirected, connected, acyclic graph of $n$ vertices. Two hidden vertices, $x$ and $y$, define a unique path because trees have exactly one simple path between any pair of vertices."
date: "2026-06-07T20:53:34+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "interactive", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2193
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1076 (Div. 3)"
rating: 2100
weight: 2193
solve_time_s: 185
verified: false
draft: false
---

[CF 2193G - Paths in a Tree](https://codeforces.com/problemset/problem/2193/G)

**Rating:** 2100  
**Tags:** dfs and similar, interactive, sortings, trees  
**Solve time:** 3m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree, which is an undirected, connected, acyclic graph of $n$ vertices. Two hidden vertices, $x$ and $y$, define a unique path because trees have exactly one simple path between any pair of vertices. We do not know the identities of $x$ and $y$, but we can interact with the tree by asking whether the path between any two chosen vertices $a$ and $b$ intersects the hidden path between $x$ and $y$. Our goal is to find at least one vertex on the hidden path using at most
