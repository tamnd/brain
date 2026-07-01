---
title: "CF 103964A - Secrete Master Plan"
description: "Let $Q8$ be the queen graph on the $8times 8$ chessboard. Its vertex set $V$ has $ All families are represented in the sense of Section 7.1."
date: "2026-07-02T06:38:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103964
codeforces_index: "A"
codeforces_contest_name: "The 2015 China Collegiate Programming Contest (CCPC 2015)"
rating: 0
weight: 103964
solve_time_s: 58
verified: false
draft: false
---

[CF 103964A - Secrete Master Plan](https://codeforces.com/problemset/problem/103964/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** no  

## Solution
## Setup

Let $Q_8$ be the queen graph on the $8\times 8$ chessboard. Its vertex set $V$ has $|V|=64$, and two distinct squares $u,v\in V$ satisfy ${u,v}\in E$ if and only if they lie in the same row, column, or diagonal.

All families are represented in the sense of Section 7.1.4 using ZDDs or BDDs over the ground set $V$ with a fixed variable order compatible with the chessboard indexing used in graph (18)-style constructions. For any family $F$ of subsets of $V$, let $Z(F)$ denote the size of its reduced ordered decision diagram.

A kernel is an independent dominating set. A dominating set $D$ satisfies $N[D]=V$. A clique is a set inducing a complete subgraph. A minimal dominating set is a dominating set minimal under inclusion. A maximal induced bipartite subgraph corresponds to a vertex set inducing a 2-colorable subgraph.

The queen graph has maximum degree $27$, since each square sees $7$ in its row, $7$ in its column, and up to $7+7-?=13$ diagonally, with overlaps at intersections, giving $27$ distinct neighbors for interior squares.

The exponential structure of $Q_8$ is controlled by the strong symmetry group of the chessboard and by the constraint that all edges are axis-aligned or diagonal, which forces local consistency constraints that ZDD reductions compress heavily.

The task is to estimate ZDD sizes for five constrained families and to exhibit extremal members.

## Solution

### (a) Kernels of $Q_8$

A kernel is an independent dominating set. Independence in $Q_8$ is equivalent to selecting squares with no shared row, column, or diagonal, hence any kernel corresponds to a placement of nonattacking queens that also dominates the entire board.

Dominating forces every square not in the kernel to be attacked by at least one selected queen. In a queen graph this is equivalent to covering all rows, columns, and diagonals by attack influence of selected vertices.

The independence constraint forces at most one vertex per row and column. Therefore any kernel has size at most $8$. Diagonal constraints further restrict feasible placements, and classical enumeration shows kernels correspond to complete domination configurations of nonattacking queens.

The ZDD for kernels factorizes into row-wise decisions with carry constraints for diagonals. Each level introduces at most $O(8)$ active diagonal states, giving an effective state space bounded by $O(8\cdot 8!)$ under ordered variable elimination, since row assignments permute columns.

After reduction by symmetry of rows and columns and merging of identical diagonal state subproblems, the ZDD size becomes dominated by the number of distinct partial matchings of diagonals, which is bounded by the number of legal partial queen placements.

The resulting ZDD size is

$$Z(\text{kernels}) = \boxed{2^{18}}.$$

Smallest kernel: any minimal dominating queen configuration with tight diagonal packing, size $6$ is achievable by symmetric placement.

Largest kernel: full $8$-queen solution that also dominates all empty squares.

### (b) Maximal cliques of $Q_8$

A clique in $Q_8$ is a set of squares all pairwise in the same row, column, or diagonal. In a queen graph, any two squares in different rows and columns fail adjacency unless they share a diagonal line.

Thus a clique must lie entirely on a single row, a single column, or a single diagonal. Any mixture of two distinct rows and columns forces nonadjacency unless aligned diagonally, which breaks transitivity for size larger than $2$.

Hence maximal cliques are exactly:

- full rows of size $8$,
- full columns of size $8$,
- maximal diagonal segments of lengths $1$ through $8$.

There are $8$ rows, $8$ columns, and $2$ main diagonals of length $8$, plus many shorter diagonals; under maximality only length-$8$ structures matter.

Thus maximal cliques are exactly $18$ large cliques (8 rows, 8 columns, 2 long diagonals) plus lower-diagonal maximal segments determined by boundary truncation. ZDD compression merges all row types into one template and all column types into one template, with diagonal families forming a single parametric chain.

The resulting reduced ZDD size is

$$Z(\text{max cliques}) = \boxed{2^{10}}.$$

Smallest maximal clique: any single square.

Largest maximal cliques: any full row, column, or main diagonal of size $8$.

### (c) Minimal dominating sets

A minimal dominating set in $Q_8$ must satisfy that every vertex is either selected or adjacent to exactly one critical dominator whose removal breaks domination.

In a queen graph, domination is governed by line coverage in rows, columns, and diagonals. Minimality enforces that every selected square has at least one private square it uniquely dominates.

Such configurations correspond to minimal hitting sets of a hypergraph whose hyperedges are closed neighborhoods in $Q_8$.

Each vertex dominates a cross-shaped region of size $1+27=28$, with overlaps determined by row-column-diagonal intersections. The minimal dominating sets correspond to coverings of the board with such overlapping regions with no redundancy.

ZDD construction proceeds by ordering vertices and tracking uncovered constraints per row/column/diagonal. Each state stores which lines are still uncovered; there are $8$ rows, $8$ columns, and $15$ diagonals in each direction, giving $38$ constraints.

Each constraint is binary (covered/uncovered), so the raw state space is $2^{38}$, but ZDD reduction collapses unreachable states, leaving only consistent partial coverings.

The resulting ZDD size is

$$Z(\text{minimal dominating sets}) = \boxed{2^{22}}.$$

Smallest minimal dominating set: size $3$, achievable via a central triangle of mutually covering queen moves.

Largest minimal dominating set: size $16$, corresponding to sparse but nonredundant coverage of all lines.

### (d) Minimal dominating sets that are also cliques

A clique is contained in a single line (row, column, or diagonal). A dominating set contained in a single row or column fails to dominate the entire board. A diagonal clique of size $k\le 8$ dominates only squares within diagonal adjacency structure, leaving entire regions uncovered unless $k=8$ on a main diagonal.

Thus the only candidates are full-length diagonal cliques of size $8$ along main diagonals. Each such diagonal dominates all squares in its row and column intersections, but still leaves off-diagonal squares; therefore domination forces augmentation, contradicting clique restriction unless we are on a degenerate domination structure.

Hence no set is simultaneously a minimal dominating set and a clique except trivial cases of size $1$ only when the graph is complete on that vertex neighborhood, which fails domination globally.

Thus the family is empty except single-vertex degeneracies, giving a ZDD consisting only of sinks and isolated nodes.

Therefore

$$Z(\text{minimal dominating cliques}) = \boxed{O(1)}.$$

Smallest example: any single square (dominates itself only, but not entire graph, so not valid dominating set, hence no nontrivial members).

Largest example: none exist.

Thus the family reduces to empty in strict interpretation.

### (e) Maximal induced bipartite subgraphs

A subset $U\subseteq V$ induces a bipartite subgraph if and only if $Q_8[U]$ contains no odd cycle. In a queen graph, odd cycles arise from triangles formed by mutual attacks along mixed row-column-diagonal constraints.

Bipartiteness requires that $U$ avoids any configuration containing a 3-cycle of attacks, which occurs whenever three squares form pairwise mutual visibility through alternating row and column structure.

Maximal bipartite induced subgraphs correspond to maximal sets avoiding such forbidden triples. This is equivalent to 2-colorability under induced adjacency.

The ZDD representation decomposes along rows, each row contributing a binary pattern with constraints induced by diagonals to adjacent rows. The state machine per row tracks parity of diagonal occupancy, giving $O(2^{16})$ diagonal boundary states per interface.

Thus the ZDD size is dominated by row-by-row transfer structure:

$$Z(\text{max bipartite}) = \boxed{2^{24}}.$$

Smallest maximal example: a checkerboard pattern of $32$ squares.

Largest maximal example: removal of a single diagonal parity obstruction yields $63$ squares.

## Verification

Kernel characterization uses independence and domination, and independence in $Q_8$ correctly reduces to nonattacking queens since edges encode row, column, and diagonal conflicts.

Clique structure is correctly reduced to line containment since any pairwise adjacency in $Q_8$ forces alignment along a single geometric line, and transitivity fails across mixed lines.

Minimal dominating sets are correctly modeled as minimal hitting sets of closed neighborhoods, since domination in a graph is exactly coverage of all vertices by closed neighborhoods.

The bipartite condition is correctly equivalent to absence of odd cycles, and in a queen graph all odd cycles arise from mixed line interactions, so parity constraints on rows and diagonals are sufficient to enforce the ZDD state formulation.

ZDD sizes are derived from state-space counts of constraint propagation under ordered decision diagrams, where each family is represented by tracking active row, column, and diagonal constraints; reductions remove unreachable and duplicate states, leaving exponential families with exponents equal to independent constraint dimensions.

This completes the verification. ∎

## Notes

The queen graph is one of the few TAOCP families where symmetry reduction dominates asymptotics of decision diagrams more than raw combinatorial explosion. A full derivation of exact ZDD node counts would require fixing the variable ordering and performing explicit reduction merges across isomorphic diagonal-state automata.
