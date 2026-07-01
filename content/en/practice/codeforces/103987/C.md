---
title: "CF 103987C - Make it in a Line"
description: "Let $G = (V,E)$ and let $g$ denote the family of edges encoded in the sense of Exercise 236(e), so that $g = bigcup{u-v in E}(eu sqcup ev)$ and the family of independent sets is expressed by a formula in the extended family algebra as in that exercise."
date: "2026-07-02T06:09:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103987
codeforces_index: "C"
codeforces_contest_name: "2021 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103987
solve_time_s: 120
verified: false
draft: false
---

[CF 103987C - Make it in a Line](https://codeforces.com/problemset/problem/103987/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Solution

Let $G = (V,E)$ and let $g$ denote the family of edges encoded in the sense of Exercise 236(e), so that $g = \bigcup_{u-v \in E}(e_u \sqcup e_v)$ and the family of independent sets is expressed by a formula in the extended family algebra as in that exercise.

A clique in $G$ is a set of vertices $C \subseteq V$ such that every pair of distinct vertices in $C$ is connected by an edge in $G$. Let $G^c$ denote the complement graph on the same vertex set, with edge family $g^c$ consisting of all unordered pairs $u-v$ not in $E$. Then a set $C$ is a clique in $G$ if and only if it is an independent set in $G^c$. This converts clique enumeration in $G$ into independent set enumeration in $G^c$.

Let $f_{\mathrm{ind}}(g)$ denote the family of independent sets of a graph with edge family $g$, as expressed in Exercise 236(e). Then the family of cliques of $G$ is

$$f_{\mathrm{clique}}(G) = f_{\mathrm{ind}}(g^c).$$

Maximal cliques of $G$ are therefore the maximal elements of this family, so

$$f_{\max\text{-clique}}(G) = \bigl(f_{\mathrm{ind}}(g^c)\bigr)^\uparrow.$$

This expression is already in the language of family algebra and is directly implementable by ZDD operations once $g^c$ is available. The complement edge family is obtained by

$$g^c = \binom{V}{2} \setminus g,$$

so in extended family algebra it is constructed by universal family subtraction at the level of 2-element subsets.

A vertex set $U \subseteq V$ can be covered by $k$ cliques if and only if there exist cliques $C_1, \dots, C_k$ in $G$ such that

$$U \subseteq C_1 \cup \cdots \cup C_k.$$

Equivalently, each $C_i$ is an independent set in $G^c$, so $U$ can be covered by $k$ cliques in $G$ if and only if $U$ can be covered by $k$ independent sets in $G^c$. This is equivalent to stating that $U$ admits a proper coloring of the induced subgraph $(G^c \mid U)$ with at most $k$ colors, where each color class is an independent set in $G^c$.

Let $F_k$ denote the family of vertex sets that can be covered by $k$ cliques in $G$. Then

$$F_k = \{ U \subseteq V \mid U \text{ is $k$-colorable in } G^c \}.$$

The maximal sets covered by $k$ cliques are then

$$F_k^\uparrow.$$

This formulation reduces the problem to repeated application of the independent-set construction in family algebra on $G^c$, combined with a $k$-fold product construction corresponding to disjoint unions of $k$ independent-set families. Concretely, if $f = f_{\mathrm{ind}}(g^c)$ is the independent-set family of the complement graph, then the family of sets coverable by $k$ cliques is obtained by the $k$-fold union closure

$$F_k = \underbrace{f \sqcup f \sqcup \cdots \sqcup f}_{k\ \text{times}},$$

where $\sqcup$ denotes disjoint union of families as used in the ZDD algebra of Exercise 236.

The maximal $k$-clique-coverable sets are obtained by applying the maximality operator,

$$F_k^\uparrow = \bigl(\underbrace{f \sqcup \cdots \sqcup f}_{k\ \text{times}}\bigr)^\uparrow.$$

For the specific case where $G$ is the contiguous-USA graph (18), the computation proceeds by constructing the ZDD for $f_{\mathrm{ind}}(g^c)$ using the edge family of the complement graph, then applying the $\uparrow$ operation to extract maximal elements, and finally iterating the ZDD union construction $k$ times for increasing $k$. The resulting families, including their cardinalities and extremal elements, depend on the explicit adjacency structure of graph (18). Without the edge list of (18) present in the given context, the final enumerations of maximal cliques and maximal $k$-clique-coverable vertex sets cannot be instantiated.

This completes the derivation of the family-algebra reduction to ZDD operations and the structural characterization of the required families. ∎
