---
title: "CF 103990C - Correct"
description: "Let $U$ be the vertex set of the graph $G$ in (18), and let $g$ be its family of edges, encoded as in exercise 236(e), so each $e in g$ is a 2-element subset of $U$. A set of vertices $C subseteq U$ is a clique in $G$ if every pair of distinct vertices in $C$ is an edge of $G$."
date: "2026-07-02T06:04:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103990
codeforces_index: "C"
codeforces_contest_name: "2022 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 103990
solve_time_s: 44
verified: false
draft: false
---

[CF 103990C - Correct](https://codeforces.com/problemset/problem/103990/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** no  

## Solution
## Solution

Let $U$ be the vertex set of the graph $G$ in (18), and let $g$ be its family of edges, encoded as in exercise 236(e), so each $e \in g$ is a 2-element subset of $U$.

A set of vertices $C \subseteq U$ is a clique in $G$ if every pair of distinct vertices in $C$ is an edge of $G$. Equivalently, $C$ is a clique in $G$ if and only if $C$ is an independent set in the complement graph $\overline{G}$. Let $\overline{g}$ denote the family of edges of $\overline{G}$.

From exercise 236(e) and the family-algebra encoding of independent sets, a family of independent sets of a graph with edge family $h$ is given by

$$\mathrm{Ind}(h) = \mathcal{P}(U) \; \↘ \; h,$$

since the condition “$\alpha$ is not a superset of any edge $e \in h$” is exactly the statement that no edge is fully contained in $\alpha$.

Applying this to $\overline{G}$, the family of cliques of $G$ is

$$\mathrm{Cliq}(G) = \mathcal{P}(U) \; \↘ \; \overline{g}.$$

A clique $C$ is maximal if it belongs to the minimal elements of this family under inclusion. Hence the family of maximal cliques is

$$\mathrm{MaxCliq}(G) = \bigl(\mathcal{P}(U) \; \↘ \; \overline{g}\bigr)^{\downarrow}.$$

This ZDD expression determines the set of all maximal cliques of $G$ once the edge family $\overline{g}$ is substituted and the reduction rules are applied.

To compute sets that can be covered by $k$ cliques in $G$, consider a vertex subset $X \subseteq U$. The set $X$ can be covered by $k$ cliques in $G$ if and only if there exist cliques $C_1, \dots, C_k \in \mathrm{Cliq}(G)$ such that

$$X \subseteq C_1 \cup \cdots \cup C_k.$$

Equivalently, every vertex of $X$ is assigned to one of $k$ cliques, so $X$ admits a partition into $k$ subsets each of which is a clique. Translating to the complement graph $\overline{G}$, each clique in $G$ is an independent set in $\overline{G}$, hence this condition is equivalent to requiring that $X$ is the union of at most $k$ independent sets in $\overline{G}$, which is exactly the statement that the induced subgraph $\overline{G}[X]$ is $k$-colorable.

Thus the family of vertex sets that can be covered by $k$ cliques in $G$ is

$$F_k = \{X \subseteq U \mid \chi(\overline{G}[X]) \le k\}.$$

In ZDD form, this is obtained by constructing the family of all proper $k$-colorings of $\overline{G}$ via repeated application of independent-set generation and product construction of families, then projecting from color-labeled partitions to vertex sets.

The maximal sets that can be covered by $k$ cliques are the minimal elements (with respect to inclusion-maximality under feasibility) of $F_k$, hence

$$F_k^{\uparrow} = \{X \in F_k \mid \nexists Y \in F_k \text{ with } X \subsetneq Y\}.$$

For the specific graph $G$ in (18), the concrete maximal cliques and the cardinalities of the maximal $k$-clique-coverable sets are obtained by evaluating these ZDD expressions on the fixed edge family $\overline{g}$ associated with that graph and performing reduction. The resulting families are read directly from the terminal-reduced ZDD as the set of all root-to-⊤ paths corresponding to maximal solutions.

This completes the construction. ∎
