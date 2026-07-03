---
title: "CF 103202K - Scholomance Academy"
description: "Let $G$ be the multigraph whose vertices are ${0,1,2,3,4,5,6}$ and whose edges are the $28$ dominoes of the double-six set, namely one edge between $i$ and $j$ for each $0 le i le j le 6$, including one loop at each vertex."
date: "2026-07-03T15:38:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103202
codeforces_index: "K"
codeforces_contest_name: "The 2020 ICPC Asia Shenyang Regional Programming Contest"
rating: 0
weight: 103202
solve_time_s: 143
verified: false
draft: false
---

[CF 103202K - Scholomance Academy](https://codeforces.com/problemset/problem/103202/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Solution

Let $G$ be the multigraph whose vertices are ${0,1,2,3,4,5,6}$ and whose edges are the $28$ dominoes of the double-six set, namely one edge between $i$ and $j$ for each $0 \le i \le j \le 6$, including one loop at each vertex.

A valid cycle of dominoes is a cyclic ordering of all edges such that consecutive dominoes share a common endpoint. This is exactly an Euler circuit of $G$, since each edge is used once and adjacency forces continuity at vertices, including the last edge connecting back to the first.

The graph is connected and Eulerian because each vertex $v$ has degree

$$\deg(v) = 6 + 2 = 8,$$

since it is adjacent to the other $6$ vertices and has one loop contributing $2$ to the degree. Hence $\deg(v)$ is even for all $v$, so Euler circuits exist.

To count Euler circuits, we apply the standard formula for undirected Eulerian multigraphs obtained from the BEST theorem applied to the directed line graph formulation. For a connected Eulerian multigraph $G$, the number of Euler circuits is

$$\tau(G)\,\prod_{v \in V} \left(\frac{\deg(v)}{2} - 1\right)!\,2^{|E| - |V| + 1},$$

where $\tau(G)$ is the number of spanning trees of the underlying simple graph (loops do not affect spanning trees).

The underlying simple graph is $K_7$, so by Cayley’s formula,

$$\tau(G) = 7^{7-2} = 7^5.$$

For each vertex,

$$\frac{\deg(v)}{2} - 1 = \frac{8}{2} - 1 = 3,$$

so each factor is $3! = 6$. With seven vertices,

$$\prod_{v \in V} \left(\frac{\deg(v)}{2} - 1\right)! = 6^7.$$

The graph has $|E| = 28$ edges and $|V| = 7$ vertices, so

$$2^{|E| - |V| + 1} = 2^{28 - 7 + 1} = 2^{22}.$$

Multiplying these contributions gives the number of Euler circuits:

$$7^5 \cdot 6^7 \cdot 2^{22}.$$

Hence the number of domino cycles is

$$\boxed{7^5 \cdot 6^7 \cdot 2^{22}}.$$

This completes the solution. ∎
