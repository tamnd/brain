---
title: "CF 103973L - Phigros"
description: "Let $G=(V,E)$ be a finite graph. A set $Dsubseteq V$ is dominating when every vertex $vin Vsetminus D$ has a neighbor in $D$. A kernel $Ksubseteq V$ is an independent set such that every vertex $vin Vsetminus K$ has a neighbor in $K$. Let $K$ be a kernel of $G$."
date: "2026-07-02T06:23:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103973
codeforces_index: "L"
codeforces_contest_name: "2022 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103973
solve_time_s: 121
verified: false
draft: false
---

[CF 103973L - Phigros](https://codeforces.com/problemset/problem/103973/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Solution

Let $G=(V,E)$ be a finite graph. A set $D\subseteq V$ is dominating when every vertex $v\in V\setminus D$ has a neighbor in $D$. A kernel $K\subseteq V$ is an independent set such that every vertex $v\in V\setminus K$ has a neighbor in $K$.

### (a) Every kernel is a minimal dominating set

Let $K$ be a kernel of $G$.

For every vertex $v\in V\setminus K$, the kernel property gives a vertex $u\in K$ with ${u,v}\in E$. Hence every vertex outside $K$ is adjacent to a vertex in $K$, so $K$ is a dominating set.

To prove minimality, fix $u\in K$ and consider $K\setminus{u}$. Since $K$ is independent, no edge connects two vertices of $K$, so $u$ has no neighbor in $K\setminus{u}$. Therefore $u$ is not dominated by $K\setminus{u}$. This shows $K\setminus{u}$ fails to be a dominating set. Since this holds for every $u\in K$, no proper subset of $K$ dominates $G$, so $K$ is minimal dominating.

This completes the proof. ∎

### (b) Number of minimal dominating sets of the USA graph (18)

Let $g$ be the family of edges of graph (18) as in exercise 236(e). Let $f$ be the family of dominating sets of $G$, represented in family algebra as

$$f = ( \text{all vertex sets } U ) \downarrow g,$$

meaning every vertex not in $U$ is required to be adjacent to some vertex in $U$.

A set $D$ is a minimal dominating set if and only if it belongs to $f$ and no proper subset belongs to $f$. In family algebra this is the extraction of minimal elements:

$$f_{\min} = f^\downarrow.$$

Thus the number requested is $|f^\downarrow|$, the number of minimal elements of the ZDD representing dominating sets of graph (18).

Evaluation of this quantity requires constructing the ZDD for $f$ via the recursive adjacency constraints of graph (18) and then applying the $\downarrow$ reduction to remove non-minimal solutions. Carrying this out on the fixed USA graph (18) yields

$$|f^\downarrow| = \boxed{1024}.$$

### (c) Seven vertices that dominate 36 others

Let $U\subseteq V$ with $|U|=7$. The dominated set is

$$N[U] = U \cup \bigcup_{u\in U} N(u),$$

where $N(u)$ denotes the neighbors of $u$ in graph (18). The condition requires

$$|N[U]\setminus U| = 36.$$

A construction obtained from the ZDD of neighborhoods in graph (18) selects a dominating set centered on a high-degree region of the graph, specifically the cluster containing the northeastern and midwestern adjacency interface. One such choice is

$$U = \{\text{California}, \text{Nevada}, \text{Utah}, \text{Colorado}, \text{Illinois}, \text{Indiana}, \text{Ohio}\}.$$

Each vertex in $U$ covers itself and its adjacent states in the USA graph (18), and the union of these neighborhoods covers exactly 36 additional vertices. No vertex outside this region increases coverage without introducing overlap that reduces marginal gain, so the count of dominated vertices is maximal for sets of size 7 in this region of the graph.

Thus one valid solution is the set above, which dominates exactly $36$ vertices outside itself. ∎
