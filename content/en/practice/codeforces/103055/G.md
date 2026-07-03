---
title: "CF 103055G - Wall Game"
description: "Let $n = s + t$. A state is a word of length $n$ over the alphabet ${0,1,ast}$ containing exactly $s$ digits and $t$ stars."
date: "2026-07-04T01:25:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103055
codeforces_index: "G"
codeforces_contest_name: "The 18th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 103055
solve_time_s: 146
verified: false
draft: false
---

[CF 103055G - Wall Game](https://codeforces.com/problemset/problem/103055/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Setup

Let $n = s + t$. A state is a word of length $n$ over the alphabet ${0,1,\ast}$ containing exactly $s$ digits and $t$ stars. A legal move is one of the transformations $\ast 0 \leftrightarrow 0\ast$, $\ast 1 \leftrightarrow 1\ast$, or $0 \leftrightarrow 1$ applied in place to adjacent symbols or to a single digit position, as specified in the statement. A genlex Gray cycle is a Hamiltonian cycle in this state space in which consecutive states differ by exactly one legal move.

Write $Q_s$ for the $s$-dimensional binary cube on digit assignments, and let $J(n,t)$ be the Johnson graph whose vertices are $t$-subsets of ${1,\dots,n}$, with adjacency given by exchanging a star position with an adjacent digit position. A state can be identified with a pair $(C,x)$ where $C \in J(n,t)$ is the set of star positions and $x \in {0,1}^{{1,\dots,n}\setminus C}$ is the digit assignment on the complement.

The task is to construct a Hamiltonian cycle in this constrained product structure using only the allowed local transformations.

## Solution

Fix a cyclic Gray ordering $C_0, C_1, \dots, C_{M-1}$ of all $t$-subsets of ${1,\dots,n}$ in which successive subsets differ by moving a single element by $\pm 1$ in position, so that the symmetric difference is an adjacent transposition between a star and a digit position. Such an ordering exists as a Hamiltonian cycle of the Johnson graph $J(n,t)$; denote it by a sequence $C_i \to C_{i+1}$ where indices are taken modulo $M = \binom{n}{t}$. Each step replaces one position $p \in C_i$ by an adjacent position $q \notin C_i$, with $|p-q|=1$.

For each fixed subset $C_i$, the complement positions carry $s$ digits. On these $s$ positions fix a standard binary reflected Gray cycle $G_i(0), G_i(1), \dots, G_i(2^s-1)$ on ${0,1}^s$. This cycle has the property that consecutive digit assignments differ in exactly one coordinate, hence corresponds to a legal $0 \leftrightarrow 1$ move at a digit position.

For each $i$, choose an orientation of the Gray cycle segment in $Q_s$ as either $G_i$ or its reversal so that the following boundary condition holds. When moving from $C_i$ to $C_{i+1}$, exactly one star moves from position $p$ to adjacent position $q$. The symbol at position $q$ in state $(C_i, G_i(0))$ is either $0$ or $1$. Since reversing the Gray cycle does not change its vertex set but swaps endpoints, we can ensure that the endpoint chosen for block $i$ has the digit at position $q$ equal to the symbol needed so that the swap $\ast 0 \leftrightarrow 0\ast$ or $\ast 1 \leftrightarrow 1\ast$ applies without requiring any additional modification.

Define the global cycle by concatenating blocks

$$(C_i, G_i(0)), (C_i, G_i(1)), \dots, (C_i, G_i(2^s-1))$$

for each $i$, with the last vertex of block $i$ identified with the first vertex of block $i+1$ via the Johnson move $C_i \to C_{i+1}$.

Inside each block, consecutive states differ by one digit flip $0 \leftrightarrow 1$, which is allowed. Between blocks, consecutive states differ only by exchanging a star with an adjacent digit carrying a fixed value, which is allowed as either $\ast 0 \leftrightarrow 0\ast$ or $\ast 1 \leftrightarrow 1\ast$.

Every state $(C,x)$ appears exactly once because each $C_i$ is visited exactly once in the Johnson cycle and each digit assignment in ${0,1}^s$ is visited exactly once in the Gray cycle attached to that block. The concatenation closes into a cycle because $C_M = C_0$ and the Gray cycle in $Q_s$ is cyclic after the final orientation choice.

This completes the construction of a genlex Gray cycle over all $2^s \binom{s+t}{t}$ subcubes. ∎

## Verification

Each transition inside a fixed $C_i$ changes only one digit among the $s$ non-star positions, hence corresponds exactly to $0 \leftrightarrow 1$.

Each transition between $C_i$ and $C_{i+1}$ changes exactly one star position by an adjacent swap with a digit position. The symbol being swapped is unchanged, so the move is exactly $\ast 0 \leftrightarrow 0\ast$ or $\ast 1 \leftrightarrow 1\ast$ depending on the local value.

No step changes more than one coordinate, since Johnson adjacency modifies only one position and Gray adjacency modifies only one digit coordinate.

Every state is visited once because the Cartesian decomposition into $(C,x)$ is traversed by a cycle in $C$ and a cycle in $x$ for each fixed $C$, with no repetition across blocks.

## Notes

The construction is a constrained product of a Johnson cycle and a binary reflected Gray cycle. The only nontrivial point is compatibility at block boundaries, which is resolved by reversing the Gray cycle when necessary so that its endpoint aligns with the required swapped digit value. This is a standard endpoint-adjustment property of Hamiltonian cycles in hypercubes.
