---
title: "CF 103666H - \u0420\u043e\u0431\u043e\u0442"
description: "Represent each domino ${i,j}$, $0 le i le j le 6$, as an undirected edge between vertices $i$ and $j$ in a multigraph $G$ on vertex set ${0,1,dots,6}$, with one loop at each vertex $i$ corresponding to ${i,i}$."
date: "2026-07-03T02:20:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103666
codeforces_index: "H"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2016"
rating: 0
weight: 103666
solve_time_s: 138
verified: false
draft: false
---

[CF 103666H - \u0420\u043e\u0431\u043e\u0442](https://codeforces.com/problemset/problem/103666/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Solution

Represent each domino ${i,j}$, $0 \le i \le j \le 6$, as an undirected edge between vertices $i$ and $j$ in a multigraph $G$ on vertex set ${0,1,\dots,6}$, with one loop at each vertex $i$ corresponding to ${i,i}$. A valid cyclic arrangement of all 28 dominoes is exactly an Euler circuit in $G$, since each domino is used once and consecutive dominoes must share an endpoint.

To apply an Euler-circuit enumeration theorem, replace $G$ by the directed Eulerian multigraph $D$ obtained by replacing each edge ${i,j}$ with two arcs $i \to j$ and $j \to i$ when $i \ne j$, and replacing each loop ${i,i}$ by a single loop arc at $i$. In $D$, each non-loop edge contributes one outgoing arc at each endpoint, and each loop contributes one outgoing and one incoming arc at its vertex.

For each vertex $v$, there are $6$ neighbors $w \ne v$, contributing $6$ outgoing arcs $v \to w$, and one loop contributing one outgoing arc $v \to v$. Hence

$\operatorname{outdeg}(v) = 7,$

and similarly $\operatorname{indeg}(v)=7$, so $D$ is Eulerian.

The BEST theorem gives the number of Euler circuits in a directed Eulerian graph rooted at a fixed starting vertex $r$ as

$$N_r = \tau_r(D)\,\prod_{v} (\operatorname{outdeg}(v)-1)!,$$

where $\tau_r(D)$ is the number of directed spanning arborescences oriented toward $r$.

Since every pair of distinct vertices in $D$ is joined in both directions, and loops do not affect arborescences, $\tau_r(D)$ equals the number of arborescences in the complete bidirected graph on $7$ vertices, which is

$$\tau_r(D) = 7^{7-2} = 7^5.$$

For each vertex,

$$(\operatorname{outdeg}(v)-1)! = 6!,$$

hence

$$\prod_v (\operatorname{outdeg}(v)-1)! = (6!)^7.$$

Therefore the number of Euler circuits in $D$ starting at a fixed vertex is

$$N_r = 7^5 (6!)^7.$$

Each Euler circuit corresponds to a cyclic ordering of the 28 dominoes. A cycle is independent of the starting point and direction. A cycle of length $28$ has exactly $28$ choices of starting edge and $2$ orientations, all yielding the same cyclic arrangement. Hence the number of distinct cycles is

$$\frac{7^5 (6!)^7}{28 \cdot 2} = \frac{7^5 (6!)^7}{56}.$$

Since $56 = 7 \cdot 8$, this simplifies to

$$\frac{7^4 (6!)^7}{8}.$$

Thus the number of valid cyclic arrangements is

$$\boxed{\frac{7^5 (6!)^7}{56}}.$$

∎
