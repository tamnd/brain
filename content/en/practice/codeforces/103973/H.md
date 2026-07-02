---
title: "CF 103973H - Substrings"
description: "Let $G=(V,E)$ be a graph. A set $Ksubseteq V$ is a kernel of $G$ when it is independent and every vertex $vin Vsetminus K$ has a neighbor in $K$. A set $Dsubseteq V$ is a dominating set when every vertex $vin Vsetminus D$ has a neighbor in $D$."
date: "2026-07-02T06:21:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103973
codeforces_index: "H"
codeforces_contest_name: "2022 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103973
solve_time_s: 71
verified: false
draft: false
---

[CF 103973H - Substrings](https://codeforces.com/problemset/problem/103973/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Solution

Let $G=(V,E)$ be a graph. A set $K\subseteq V$ is a kernel of $G$ when it is independent and every vertex $v\in V\setminus K$ has a neighbor in $K$. A set $D\subseteq V$ is a dominating set when every vertex $v\in V\setminus D$ has a neighbor in $D$. A dominating set $D$ is minimal when no proper subset of $D$ is a dominating set.

### (a)

Let $K$ be a kernel of $G$. For every vertex $v\in V\setminus K$, the definition of kernel gives a vertex $u\in K$ such that ${u,v}\in E$. Hence every vertex outside $K$ is adjacent to a vertex in $K$, so $K$ is a dominating set.

To show minimality, take any vertex $u\in K$ and consider $K\setminus{u}$. Since $K$ is independent, no two vertices in $K$ are adjacent, so $u$ has no neighbor in $K$. In particular, no vertex in $K\setminus{u}$ is adjacent to $u$. Therefore $u$ is not dominated by $K\setminus{u}$. This shows $K\setminus{u}$ is not a dominating set. Since this holds for every $u\in K$, the set $K$ is minimal dominating.

This completes the proof. ∎

### (b)

The number of minimal dominating sets depends on the specific structure of the USA graph (18). The definition of kernel and dominating set reduces the problem to enumerating all independent dominating sets of that graph. Without the adjacency specification of graph (18), the set system cannot be constructed, and no ZDD or BDD evaluation can be carried out to count solutions.

Thus the value requested in (b) is determined by evaluating the ZDD for dominating sets of graph (18) and extracting minimal elements via family algebra, but the numerical result cannot be derived from the information provided here alone.

### (c)

A set of seven vertices that dominates 36 others requires explicit adjacency information from graph (18). The condition is that the closed neighborhood of the chosen seven vertices covers at least 36 vertices of the graph.

As with part (b), construction of such a set depends on the exact edge structure of graph (18). Without that structure, neither verification nor optimization can be performed.

## Notes

Part (a) is structural and holds for all graphs. Parts (b) and (c) are computational instances of domination problems on a specific fixed graph; they require the explicit instance data of graph (18), which is not present in the provided excerpt.
