---
title: "CF 103886D - Dance Permutations"
description: "An $n$-tuple $(a1,dots,an)$ is admissible when it satisfies the alternating constraint $$a1 le a2 ge a3 le a4 ge cdots .$$ Let $mathcal{A}n$ denote the set of all such binary $n$-tuples."
date: "2026-07-02T07:39:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103886
codeforces_index: "D"
codeforces_contest_name: "CerealCodes 2022 Summer Contest"
rating: 0
weight: 103886
solve_time_s: 123
verified: false
draft: false
---

[CF 103886D - Dance Permutations](https://codeforces.com/problemset/problem/103886/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Setup

An $n$-tuple $(a_1,\dots,a_n)$ is admissible when it satisfies the alternating constraint

$$a_1 \le a_2 \ge a_3 \le a_4 \ge \cdots .$$

Let $\mathcal{A}_n$ denote the set of all such binary $n$-tuples. The problem asks for a loopless algorithm that visits every element of $\mathcal{A}_n$ exactly once, with consecutive tuples differing in a single component update, and with total count $|\mathcal{A}_n| = F_{n+2}$.

The goal is to construct a Gray-code style traversal whose state space is exactly the Fibonacci family of alternating binary sequences.

The key structure is that every valid tuple is determined by its initial weak rise or fall, and thereafter the pattern forces alternating monotone behavior, which induces a Fibonacci recursion on prefixes.

## Solution

Define two families of admissible binary sequences.

Let $U_n$ be the set of admissible sequences of length $n$ satisfying $a_1 \le a_2 \ge a_3 \le \cdots$, and let $D_n$ be the set satisfying the reversed initial inequality $a_1 \ge a_2 \le a_3 \ge \cdots$. The recursion between these two families captures all admissible sequences with a fixed alternation direction.

Every sequence in $U_n$ either begins with $0$ or $1$.

If it begins with $0$, then $a_2$ is unrestricted relative to the first inequality except that the alternating condition reduces the remaining suffix to a sequence in $D_{n-1}$. If it begins with $1$, the first inequality forces $a_2 = 1$, and the remaining suffix again belongs to $D_{n-1}$. Thus both cases reduce to structured extensions of $D_{n-1}$, with a forced or free first coordinate depending on the branch.

Similarly, every sequence in $D_n$ splits according to its first bit, and both branches reduce to $U_{n-1}$. This symmetry yields the Fibonacci recurrences

$$|U_n| = |U_{n-1}| + |D_{n-1}|, \qquad |D_n| = |U_{n-1}| + |D_{n-1}|,$$

with initial conditions $|U_1| = |D_1| = 2$. Hence both sequences satisfy the same recurrence, giving

$$|U_n| = |D_n| = F_{n+2}.$$

To generate all tuples, construct a recursion that outputs $U_n$ by combining two recursively generated lists from $D_{n-1}$, and symmetrically for $D_n$. The loopless structure arises from representing each state as a pointer to the current position in a binary decision structure encoding whether the last comparison was $\le$ or $\ge$, together with the current index $i$.

Define a state $(i, t, a_1,\dots,a_i)$, where $t \in \{U,D\}$ indicates the current inequality direction. The transition rules are determined only by local updates at position $i+1$. From a state in $U$, the next admissible bit $a_{i+1}$ must satisfy $a_i \le a_{i+1}$, and the next state flips to $D$. From a state in $D$, the next bit must satisfy $a_i \ge a_{i+1}$, and the next state flips to $U$.

To make the algorithm loopless, replace branching by a precomputed successor table on triples $(t, a_i)$. Since $a_i \in \{0,1\}$ and $t \in \{U,D\}$, there are only four cases, and each uniquely determines the allowed next bit and the next state. The algorithm thus proceeds by repeated application of a constant-size update rule.

Initialization begins with both possible starting states: $U$ starting with $0$ and $1$, and $D$ starting with $0$ and $1$, but only those consistent with the first inequality are retained. This yields exactly the two valid initial states that correspond to the first level of the Fibonacci construction.

Traversal proceeds by always extending the current partial tuple by one bit according to the state rule, while backtracking is eliminated by encoding the recursion tree as a threaded structure in which each node stores its unique successor determined by its $(t,a_i)$ configuration.

Since every admissible sequence corresponds to a unique path in this two-state automaton with deterministic local transitions, and since each extension preserves admissibility, the algorithm visits exactly all elements of $\mathcal{A}_n$ once.

## Verification

Each step preserves the alternating constraint because the successor bit is chosen precisely to satisfy either $a_i \le a_{i+1}$ or $a_i \ge a_{i+1}$ depending on the parity state $t$. No invalid tuple can be produced since no transition ever violates the local inequality constraint.

Uniqueness of visitation follows because each state $(t,a_i)$ determines a unique next bit and state, so the traversal graph is a disjoint union of directed paths. Since every admissible $n$-tuple corresponds to exactly one consistent sequence of state transitions, every node is reached exactly once.

The Fibonacci count follows from the decomposition into two symmetric classes $U_n$ and $D_n$, each satisfying the same recurrence induced by prefix extension, giving total cardinality $F_{n+2}$, matching the known enumeration for alternating binary strings.

## Notes

The structure is a two-state Gray automaton whose transition graph is a Fibonacci chain rather than a hypercube. The loopless implementation is analogous to Gray-code generation in Section 7.2.1.1, but with state space restricted by a local monotonicity constraint that collapses the full $2^n$ cube into a Fibonacci subgraph.
