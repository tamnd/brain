---
title: "CF 103196C - \u0414\u0435\u0434 \u0438 \u043c\u043e\u043f\u0435\u0434"
description: "Let $G$ be the multigraph whose vertices are ${0,1,2,3,4,5,6}$ and whose edges are the $28$ dominoes of the double-six set, namely one edge between $i$ and $j$ for each $0 le i le j le 6$, including one loop at each vertex."
date: "2026-07-03T15:41:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103196
codeforces_index: "C"
codeforces_contest_name: "2020-2021 \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0437\u0430\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 103196
solve_time_s: 144
verified: false
draft: false
---

[CF 103196C - \u0414\u0435\u0434 \u0438 \u043c\u043e\u043f\u0435\u0434](https://codeforces.com/problemset/problem/103196/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 24s  
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
