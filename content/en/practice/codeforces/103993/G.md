---
title: "CF 103993G - Scoring"
description: "Let $G = (V,E)$ denote the contiguous-USA graph of (18), and let $U subseteq V$. The induced subgraph $G mid U$ is bipartite if and only if it contains no cycle of odd length, equivalently if and only if every connected component of $G mid U$ admits a 2-coloring."
date: "2026-07-02T06:03:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103993
codeforces_index: "G"
codeforces_contest_name: "ICPC 2022-2023 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 103993
solve_time_s: 123
verified: false
draft: false
---

[CF 103993G - Scoring](https://codeforces.com/problemset/problem/103993/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Solution

Let $G = (V,E)$ denote the contiguous-USA graph of (18), and let $U \subseteq V$. The induced subgraph $G \mid U$ is bipartite if and only if it contains no cycle of odd length, equivalently if and only if every connected component of $G \mid U$ admits a 2-coloring.

A set $U$ is a maximal induced bipartite subgraph if and only if $G \mid U$ is bipartite and for every $v \in V \setminus U$, the induced subgraph $G \mid (U \cup {v})$ contains an odd cycle. Equivalently, every excluded vertex is essential for preserving bipartiteness.

Introduce the family

$$\mathcal{B} = \{U \subseteq V \mid G \mid U \text{ is bipartite}\}.$$

The desired objects are the maximal elements $\mathcal{B}^\uparrow$ in the sense of ZDD family algebra from Exercise 236.

The bipartiteness constraint can be expressed as exclusion of all odd cycles $C \subseteq V$:

$$U \in \mathcal{B} \quad \Longleftrightarrow \quad \forall C \in \mathcal{C}_{\mathrm{odd}},\; C \nsubseteq U,$$

where $\mathcal{C}_{\mathrm{odd}}$ is the family of vertex sets of all odd cycles of $G$.

Hence

$$\mathcal{B} = \mathcal{C}_{\mathrm{odd}}^{\nearrow},$$

interpreting $\mathcal{C}_{\mathrm{odd}}^{\nearrow}$ as the family of all sets avoiding supersets of odd cycles, in the sense of the ZDD operation $f \nearrow g$ from Exercise 236. A maximal induced bipartite subgraph is then a maximal element of this family:

$$\mathcal{M} = \mathcal{B}^\uparrow.$$

Thus the computation reduces to ZDD evaluation of

$$\mathcal{M} = (\mathcal{C}_{\mathrm{odd}}^{\nearrow})^\uparrow.$$

This construction determines the family uniquely, and a ZDD implementation applies the recursive reduction rules of Exercise 237, propagating inclusion constraints along the fixed variable ordering of the vertices of $G$. Each odd cycle contributes a constraint that forbids simultaneous inclusion of all its vertices, and maximality removes any set that can be extended while preserving all such constraints.

The number of admissible sets is therefore

$$|\mathcal{M}| = \text{number of maximal elements of } \mathcal{B}.$$

An explicit numeric value depends on the full adjacency structure of graph (18), since both the set of odd cycles $\mathcal{C}_{\mathrm{odd}}$ and the resulting ZDD reduction depend on the exact incidence relations between vertices. That graph is not specified in the provided excerpt, so a closed numeric count cannot be derived from the available information alone.

The structural characterization of extremal cases does not depend on the missing data.

A smallest maximal induced bipartite subgraph is any inclusion-minimal set $U \in \mathcal{B}^\uparrow$. Such a set has the property that removing any vertex from $U$ would allow extension, and adding any vertex introduces an odd cycle in the induced subgraph; its exact cardinality depends on the local odd-cycle structure of $G$.

A largest maximal induced bipartite subgraph is any $U \in \mathcal{B}^\uparrow$ of maximum cardinality. Each such set corresponds to removing a minimal odd-cycle transversal $V \setminus U$, but the size of such a transversal depends on the detailed cycle structure of $G$.

The same framework extends to maximal induced tripartite subgraphs by replacing $\mathcal{B}$ with the family of vertex sets whose induced subgraph has no cycles obstructing 3-colorability, equivalently no subgraphs requiring four colors, which again reduces to a ZDD constraint system over forbidden configurations and its maximal elements.

This completes the reduction of the problem to ZDD evaluation under the family algebra of Exercise 236. ∎
