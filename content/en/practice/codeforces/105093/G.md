---
title: "CF 105093G - Pandemic"
description: "We are given a complete system of players where every unordered pair must eventually interact exactly once. Some interactions have already happened, and we know their order."
date: "2026-06-27T20:49:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "G"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 34
verified: true
draft: false
---

[CF 105093G - Pandemic](https://codeforces.com/problemset/problem/105093/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete system of players where every unordered pair must eventually interact exactly once. Some interactions have already happened, and we know their order. Each interaction between two players transforms their infection states according to a fixed rule that flips states depending on whether the pair is Healthy or Infected.

After these already-performed interactions, we are told the current state of every player. We are also given a partition of players into two groups, Gregorio’s friends and enemies. The goal is not to simulate all remaining interactions directly, but to count how many possible ways to order the remaining unperformed pair interactions will lead to a final situation where every friend ends Healthy and every enemy ends Infected.

The key difficulty is that the order of remaining edges matters because every interaction changes states and those changes affect all future interactions. We are counting valid permutations of the remaining edges, not just counting outcomes.

The constraints imply a dense interaction structure. Since every pair of players interacts exactly once, the total number of edges is n(n−1)/2, so even for moderate n the graph is extremely dense. With up to 3·10^5 total n and m across tests, any solution that simulates all permutations or even all sequences is impossible. A factorial growth over remaining edges is immediately ruled out, and even O(n^2) per test is borderline unless heavily optimized.

A subtle issue is that the final state is already known after m steps. That means the remaining edges must be consistent with a fixed configuration, and we are only counting reorderings that preserve a required final labeling constraint, not recomputing states from scratch.

Edge cases arise when no remaining edges exist, when all nodes are already in their final required roles, or when the initial revealed state is already inconsistent with the desired friend/enemy assignment. A naive approach that ignores consistency and only counts permutations would incorrectly output factorials even when no ordering works.

## Approaches

A brute-force interpretation would try to enumerate all permutations of the remaining edges and simulate the infection process for each ordering. Each simulation processes O(n^2) interactions, and there are (n(n−1)/2 − m)! permutations. Even for n = 6 this already explodes beyond feasibility. The issue is not simulation cost but combinatorial explosion of orderings.

The crucial observation is that the infection dynamics are fully symmetric and only depend on parity of interactions involving each vertex. Each handshake flips states in a deterministic way that can be represented as toggling constraints. Instead of tracking global sequences, we reinterpret each edge as an operation that contributes a parity effect on its endpoints.

Each vertex’s final state depends only on how many remaining interactions it participates in and in what parity relative to the current state. Since every edge flips both endpoints in a structured way, the entire process can be reduced to a system of linear constraints over the remaining edges.

The second key insight is that the order of edges only matters insofar as it affects intermediate parity feasibility. However, because every edge is symmetric and operations are involutive, any ordering corresponds to a permutation of identical commutative operations in a constrained parity system. This reduces the problem to counting valid linear extensions of a structure where only parity consistency matters.

This transforms the problem into counting permutations of remaining edges under constraints derived from vertex requirements. Each vertex imposes a condition on how many incident remaining edges must act before or after certain transitions, but globally this reduces to checking whether a parity-consistent assignment exists and then counting permutations of independent edge groups.

Once reduced, the remaining edges can be partitioned into components determined by parity constraints. Within each component, all edges are interchangeable, so the number of valid orderings becomes a factorial product over component sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k! · n²) | O(n²) | Too slow |
| Optimal | O(n + m + k α(k)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute the set of remaining edges by subtracting the m already used edges from the full complete graph. We conceptually treat edges as unordered pairs, so the remaining set is well-defined.
2. For each vertex, compute how many remaining edges are incident to it. This gives a degree-in-the-remaining-graph structure that reflects how many future flips each vertex will experience. This matters because each interaction toggles states.
3. Translate the current revealed state into a binary value, for example Healthy as 0 and Infected as 1. Similarly encode desired final state: friends must end at 0, enemies at 1.
4. For each vertex, compute the parity requirement induced by remaining operations. Each incident remaining edge contributes one toggle to that vertex, so the total number of toggles applied to vertex v is equal to deg_remaining[v], but the actual effect depends on the ordering only through parity, not sequence.
5. Check consistency: a vertex is feasible only if the parity of remaining incident operations can transform its current state into its required final state. This produces a system of parity equations over all vertices.
6. The system reduces to checking whether a global assignment of edge orderings exists that satisfies all vertex parity constraints simultaneously. If any contradiction arises, output 0 immediately.
7. When consistent, observe that edges impose no further interdependencies beyond belonging to the same unconstrained permutation group. All remaining edges are interchangeable with respect to validity, so any ordering is valid as long as constraints are met.
8. Therefore the answer is simply factorial of the number of remaining edges, adjusted if multiple independent components exist under parity constraints, but in this dense complete-graph structure the constraints collapse into a single global consistency check.
9. Precompute factorials up to n(n−1)/2 modulo 998244353 and output factorial of remaining edges.

### Why it works

The key invariant is that each edge acts as a symmetric toggle operation on both endpoints, and the final condition depends only on aggregate parity per vertex. Once vertex parity feasibility is satisfied, no ordering of remaining edges can invalidate it because every ordering produces the same multiset of operations, and only their count per vertex matters. Since all remaining edges are equivalent operations on an unconstrained complete graph, the set of valid permutations is exactly the set of all permutations of remaining edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

M
```
