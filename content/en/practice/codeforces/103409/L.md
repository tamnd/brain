---
title: "CF 103409L - Wiring Engineering"
description: "Let $n = s + t$. An $(s,t)$-combination is represented by a binary string $a{n-1}dots a1 a0$ with exactly $t$ ones and $s$ zeros. A move is either an adjacent swap $aj leftrightarrow a{j-1}$ or an end-around swap $a{n-1} leftrightarrow a0$."
date: "2026-07-03T11:22:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103409
codeforces_index: "L"
codeforces_contest_name: "The 2021 CCPC Guilin Onsite (XXII Open Cup, Grand Prix of EDG)"
rating: 0
weight: 103409
solve_time_s: 85
verified: false
draft: false
---

[CF 103409L - Wiring Engineering](https://codeforces.com/problemset/problem/103409/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Setup

Let $n = s + t$. An $(s,t)$-combination is represented by a binary string

$a_{n-1}\dots a_1 a_0$

with exactly $t$ ones and $s$ zeros. A move is either an adjacent swap $a_j \leftrightarrow a_{j-1}$ or an end-around swap $a_{n-1} \leftrightarrow a_0$. Each move preserves the number of ones, hence preserves the set of $(s,t)$-combinations.

The problem asks for which $(s,t)$ it is possible to generate all such strings by a single sequence of allowed swaps, meaning a Hamiltonian path in the graph whose vertices are $(s,t)$-combinations and whose edges correspond to allowed swaps.

Let $G_{n,t}$ denote this graph.

## Solution

The graph $G_{n,t}$ contains, as a spanning subgraph, the standard Johnson graph structure induced by adjacent swaps $a_j \leftrightarrow a_{j-1}$. In this subgraph, each edge corresponds to exchanging a pattern $10 \leftrightarrow 01$ in adjacent positions. This is exactly the usual adjacency structure on binary strings of fixed weight $t$.

Adding the end-around swap $a_{n-1} \leftrightarrow a_0$ introduces additional edges but does not remove any existing ones, so it does not reduce connectivity or restrict reachable configurations.

The key structural fact is that the adjacency-swap graph on $(s,t)$-combinations is connected for all $s,t \ge 0$. Indeed, given any two $(s,t)$-strings, repeated application of adjacent swaps performs a bubble-sort operation that moves each $1$ to any prescribed position while preserving all others, producing any target configuration. This gives a path between any two vertices, hence connectivity.

A Hamiltonian path can therefore be constructed whenever the graph admits a traversal that visits each vertex exactly once. The standard lexicographic generation algorithm in Section 7.2.1.3 already produces such a traversal of all $(s,t)$-combinations without requiring any cyclic constraint; each transition corresponds to a single adjacent transposition, hence lies in $G_{n,t}$. Since every transition of that generation scheme is an adjacent swap, the resulting sequence is a Hamiltonian path in the adjacency-swap graph.

Introducing the end-around swap does not alter this construction, since it only adds an additional allowable edge. A Hamiltonian path that uses only adjacent swaps remains valid in the enlarged graph.

Degenerate cases $t=0$ or $t=n$ consist of a single vertex, hence are trivially generated.

Therefore the existence of a generating sequence holds for every pair $(s,t)$.

## Verification

The lexicographic generation in Algorithm $L$ visits all $t$-subsets of ${0,\dots,n-1}$ exactly once. Each transition modifies a suffix by decreasing indices and increasing a single entry, which corresponds in binary representation to moving a single $1$ leftward across a block of $0$s or rightward in the inverse step, realizable by adjacent swaps $01 \leftrightarrow 10$.

Every such modification is local and involves only adjacent positions, so it lies in the adjacency-swap graph. No step requires the end-around swap.

Since all vertices are visited and each step is an allowed move, the resulting sequence is a Hamiltonian path in $G_{n,t}$ for all $n=s+t$.

## Notes

The end-around swap introduces cyclic adjacency, turning the underlying position graph from a path into a cycle, but this does not change the existence of a Hamiltonian traversal. It only adds redundancy to the move set.

Thus the condition is not restricted by parity or binomial-coefficient considerations: those arise in Hamiltonian cycles, not in Hamiltonian paths. Here a path suffices, and one already exists for all $(s,t)$ via the standard generation scheme.

This completes the solution. ∎
