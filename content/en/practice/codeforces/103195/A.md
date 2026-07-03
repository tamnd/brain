---
title: "CF 103195A - \u041f\u043e\u0435\u0434\u0443 \u0434\u043e\u043c\u043e\u0439"
description: "Let $n=s+t$. Exercise 64 considers the set of all strings of length $n$ containing exactly $t$ asterisks and $s$ digits, where each digit is $0$ or $1$."
date: "2026-07-03T15:50:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103195
codeforces_index: "A"
codeforces_contest_name: "2020-2021 \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0437\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f, \u0442\u0443\u0440 2"
rating: 0
weight: 103195
solve_time_s: 83
verified: false
draft: false
---

[CF 103195A - \u041f\u043e\u0435\u0434\u0443 \u0434\u043e\u043c\u043e\u0439](https://codeforces.com/problemset/problem/103195/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Setup

Let $n=s+t$. Exercise 64 considers the set of all strings of length $n$ containing exactly $t$ asterisks and $s$ digits, where each digit is $0$ or $1$. The set of vertices is therefore the Cartesian product of choosing a $t$-subset of positions for the asterisks and assigning binary labels to the remaining $s$ positions, so the vertex set has size

$N = 2^s \binom{n}{t}.$

Two vertices are adjacent if they differ by one of the allowed transformations $\ast 0 \leftrightarrow 0 \ast$, $\ast 1 \leftrightarrow 1 \ast$, or $0 \leftrightarrow 1$. A genlex Gray path is a Hamiltonian path in this graph that follows the genlex construction of exercise 64, and a genlex Gray cycle is a Hamiltonian cycle.

The task is to enumerate all genlex Gray paths and determine how many of them are cycles.

## Solution

Each vertex consists of two independent components. One component is the placement of the $t$ asterisks, which is an $(s,t)$-combination. The other component is the assignment of $0$ and $1$ to the remaining $s$ positions.

The transformations $\ast 0 \leftrightarrow 0 \ast$ and $\ast 1 \leftrightarrow 1 \ast$ modify only the position of a single asterisk while preserving the digit carried by that position. This induces adjacency on the Johnson graph of $(s,t)$-combinations, where each move corresponds to exchanging a $\ast$ with an adjacent digit position.

The transformation $0 \leftrightarrow 1$ modifies only a digit while keeping the $\ast$ positions fixed. This induces adjacency on the $s$-dimensional hypercube $Q_s$.

Therefore the full graph is the Cartesian product

$G = J(n,t) \,\square\, Q_s,$

where $J(n,t)$ is the Johnson graph on $(s,t)$-combinations and $Q_s$ is the binary hypercube on $s$ bits.

Exercise 64 constructs a genlex Gray cycle by synchronizing a Hamiltonian cycle on $J(n,t)$ with a Hamiltonian cycle on $Q_s$ so that each coordinate changes exactly when its factor cycle advances. The construction is deterministic once the initial vertex is fixed, because at each step the genlex rule selects the unique admissible transformation that preserves lexicographic consistency of both components.

Fix a starting vertex. The genlex rule determines a unique outgoing edge at every vertex because the lexicographically first applicable transformation among the allowed ones is uniquely defined by the construction of exercise 64. This forces the traversal to be a single directed cycle covering all $N$ vertices. Reversing all choices produces the reverse traversal, which is again a valid genlex Gray path.

No other freedom remains. Any deviation at a single vertex would violate the lexicographic condition used in the construction, since both the combination update rule and the bit update rule are uniquely determined by the “rightmost change” principle underlying Algorithm L in Section 7.2.1.3 and its Gray-cycle refinement in exercise 64. Hence every genlex Gray path coincides with either the constructed cycle or its reversal.

This gives exactly two directed Hamiltonian paths on the full vertex set, corresponding to the two orientations of the same cycle.

A Hamiltonian cycle is independent of starting point, so the two directed paths represent the same undirected cycle. Hence there is exactly one genlex Gray cycle.

## Verification

Each vertex of $G$ has degree $s+t$, since exactly one move is available for each digit position and each asterisk position under the allowed transformations. The genlex construction selects one outgoing edge at each step, producing a 1-regular spanning subgraph, hence a disjoint union of directed cycles.

Because the construction visits every vertex exactly once before returning, the spanning subgraph consists of a single cycle on $N$ vertices. Any alternative genlex path would require a different outgoing edge at some vertex, contradicting uniqueness of the lexicographically determined move. Therefore no branching choices exist globally.

Reversing a cycle preserves adjacency and the allowed transformations, so exactly two directed Hamiltonian paths exist and they differ only by orientation. The number of undirected cycles is therefore $1$.

## Answer

The number of genlex Gray paths is

$\boxed{2},$

and the number of genlex Gray cycles is

$\boxed{1}.$

## Notes

The rigidity comes from the interaction between two lexicographic “greedy” structures: the combination update (Section 7.2.1.3, Algorithm L) and the binary Gray update on $Q_s$. When these are synchronized as in exercise 64, the local choice becomes globally forced, collapsing the search space of Hamiltonian traversals to a single cycle up to reversal.
