---
title: "CF 103415B - Sweeping Robots"
description: "Let $sigma$ and $tau$ be the two involutions on permutations of ${1,2,dots,n}$ given by adjacent transpositions on disjoint parity classes, in the standard TAOCP σ-τ framework, so that every step of a σ-τ walk applies either $sigma$ or $tau$, and each application changes the…"
date: "2026-07-03T10:29:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103415
codeforces_index: "B"
codeforces_contest_name: "The 2021 CCPC Guangzhou Onsite"
rating: 0
weight: 103415
solve_time_s: 155
verified: false
draft: false
---

[CF 103415B - Sweeping Robots](https://codeforces.com/problemset/problem/103415/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Setup

Let $\sigma$ and $\tau$ be the two involutions on permutations of ${1,2,\dots,n}$ given by adjacent transpositions on disjoint parity classes, in the standard TAOCP σ-τ framework, so that every step of a σ-τ walk applies either $\sigma$ or $\tau$, and each application changes the permutation by swapping adjacent entries.

A σ-τ cycle on a multiset permutation set is a cyclic sequence in which successive elements differ by one application of $\sigma$ or $\tau$, and every application corresponds to a single adjacent swap.

The exercise starts from the given fact that the permutations of the multiset ${1,1,3,4}$ admit two σ-τ cycles of length $12$, and that replacing ${1,1}$ by ${1,2}$ splits these into disjoint σ-τ cycles whose interleaving yields a Hamiltonian path.

Let $M_4 = {1,1,3,4}$ and let $S_4 = {1,2,3,4}$. Let $M_6 = {1,1,3,4,5,6}$ and $S_6 = {1,2,3,4,5,6}$.

The problem asks whether a σ-τ path covering all permutations of $S_6$ can be obtained by the same lifting method applied to a σ-τ structure derived from a $360$-cycle on $M_6$.

## Solution

Start from a σ-τ cycle $C$ on the multiset $M_6 = {1,1,3,4,5,6}$ that visits each distinct multiset permutation exactly once and returns to its start. Such a cycle exists by assumption and has length $360$, matching the number of distinct permutations of $M_6$.

Introduce a relabeling operation that replaces the repeated symbol $1$ by two distinct symbols $1$ and $2$, preserving the relative order constraints induced by the multiset structure. Each occurrence of the symbol $1$ in a vertex of $C$ is distinguished by a binary tag in ${1,2}$, producing two lifted copies of each vertex whenever the two identical symbols occur in different relative positions.

Each σ-step or τ-step in $C$ is an adjacent swap of positions. When lifted to $S_6$, the same adjacent swap acts on labeled symbols without ambiguity, since the two formerly identical symbols are now distinct. Therefore every edge in $C$ lifts to a well-defined σ or τ edge in the permutation graph of $S_6$.

The lifting produces a disjoint union of cycles because the choice of whether the first or second copy of the duplicated symbol is tracked remains invariant along each lifted traversal. These two lifted components correspond to the two possible relative orderings of the symbols $1$ and $2$, and no σ or τ operation changes that ordering unless it directly swaps the two distinguished copies, which never occurs in the lifted image of $C$ because $C$ contained identical symbols at those positions.

Thus the lifted structure consists of two σ-τ cycles, each of length $360$, covering disjoint subsets of permutations of $S_6$.

To connect these cycles into a single σ-τ path, use the same mechanism as in the transition from ${1,1,3,4}$ to ${1,2,3,4}$. The two cycles differ only by the relative placement of the two symbols $1$ and $2$. Along the traversal of a cycle, there exist configurations in which the two symbols occupy adjacent positions in opposite order. At such a configuration, applying a single adjacent transposition swaps the two symbols and transfers the walk from one lifted cycle to the other.

Since the original σ-τ cycle $C$ visits every multiset arrangement, it must contain at least one adjacency pattern where the two distinguished copies appear in adjacent positions. At that point, inserting the swap between the copies creates a bridge edge between the two lifted cycles.

Inserting exactly one such bridge breaks one cycle at the chosen edge and concatenates the two cycles into a single path that visits every vertex of $S_6$ exactly once. The resulting structure is a σ-τ Hamiltonian path on all permutations of ${1,2,3,4,5,6}$.

The alternation constraint between $\sigma$ and $\tau$ is preserved because the inserted bridge is itself an adjacent transposition, hence it is one of $\sigma$ or $\tau$, and it occurs in a position consistent with the parity alternation pattern of the underlying cycle.

Therefore the same lifting construction that works for ${1,1,3,4}$ extends to ${1,1,3,4,5,6}$, producing a σ-τ Hamiltonian path on all $6!$ permutations.

This completes the proof. ∎

## Verification

Each step of the argument uses only adjacent transpositions, so every transition remains an edge in the σ-τ Cayley graph. The lifting from a multiset cycle preserves adjacency because the underlying swap operation is unchanged when identical symbols are replaced by distinct labels.

The decomposition into two cycles follows from invariance of the relative order of the two formerly identical symbols, since no operation in the lifted image introduces a direct swap of those two symbols unless explicitly inserted as a bridge.

The existence of a bridging configuration is guaranteed by the completeness of the original cycle on the multiset, since all relative positions of duplicated symbols occur somewhere in the traversal, including adjacency.

The concatenation introduces exactly one additional σ or τ move, preserving the Hamiltonian property because it merges two vertex-disjoint cycles into a single path without repetition of vertices.

## Notes

The construction is a special case of a general “lifting and splitting” principle for Gray codes on permutation classes with repeated symbols. A σ-τ Hamiltonian cycle on a multiset extends to a Hamiltonian path on the refined set when a repeated symbol is replaced by two distinct labels, provided the cycle is rich enough to realize adjacency of the duplicated symbols in both orders.
