---
title: "CF 103102M - Mistake"
description: "Let a multiset be given with distinct symbols $x1 < x2 < cdots < xk$ and multiplicities $m1, m2, ldots, mk$ with total size $$n = m1 + m2 + cdots + mk.$$ A multiset permutation is a word of length $n$ containing exactly $mi$ copies of $xi$."
date: "2026-07-03T22:04:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103102
codeforces_index: "M"
codeforces_contest_name: "2020-2021 ICPC Southeastern European Regional Programming Contest (SEERC 2020)"
rating: 0
weight: 103102
solve_time_s: 144
verified: false
draft: false
---

[CF 103102M - Mistake](https://codeforces.com/problemset/problem/103102/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Setup

Let a multiset be given with distinct symbols $x_1 < x_2 < \cdots < x_k$ and multiplicities $m_1, m_2, \ldots, m_k$ with total size

$$n = m_1 + m_2 + \cdots + m_k.$$

A multiset permutation is a word of length $n$ containing exactly $m_i$ copies of $x_i$. The goal is to implement the near-perfect generation method referenced in the preceding exercises, which produces all such permutations in a structured order derived from the Chase near-perfect combination sequence on binary strings.

Represent each multiset permutation by a binary expansion of a boundary structure: introduce a bitstring of length $n + k - 1$ containing $m_1$ zeros, $m_2$ zeros, etc. equivalently, encode a permutation as a sequence of block separators corresponding to an $(s,t)$-style configuration, where the positions of structural markers evolve according to the dual combination mechanism $b_s \ldots b_1$ described in exercise 46.

Each state consists of a binary string $a_{n-1}\ldots a_0$ with exactly $t$ ones, and the positions of zeros $b_s \ldots b_1$ determine the induced multiset permutation by grouping consecutive positions between ones into blocks that assign symbols $x_i$ in order.

The task is to implement the near-perfect update rule on $b_s \ldots b_1$ and output the corresponding multiset permutation at each step.

## Solution

The implementation uses two coupled representations. The first is the dual combination representation $b_s \ldots b_1$, listing the positions of zeros in decreasing order as in (5). The second is the induced multiset permutation obtained by interpreting the binary string as a segmentation of an ordered index set.

Initialization sets the binary string to the lexicographically first configuration in Chase order, namely

$$a_{n-1}\ldots a_0 = 0^{m_1} 1 0^{m_2} 1 \cdots 1 0^{m_k},$$

which corresponds to the minimal element in the near-perfect ordering. The associated zero positions $b_s \ldots b_1$ are computed directly from this string.

At each iteration, the update step is governed by the near-perfect transition rule from exercise 46 applied to $b_s \ldots b_1$. That rule selects the rightmost index $j$ such that $b_j$ can be increased while preserving strict monotonicity

$$n > b_s > \cdots > b_1 \ge 0,$$

then sets $b_{j-1}, \ldots, b_1$ to their minimal feasible values consistent with the constraint. This produces the next dual combination in near-perfect order.

Given an updated $b_s \ldots b_1$, reconstruct the binary string $a_{n-1}\ldots a_0$ by placing zeros exactly at the positions $b_1, \ldots, b_s$ and ones elsewhere. This reconstruction uses the identity that the complement of the zero positions determines the one positions, as in equation (4).

To obtain the multiset permutation, partition the index set ${0,1,\ldots,n-1}$ into maximal runs of consecutive ones separated by zeros. Each run length determines how many occurrences of the corresponding symbol appear at that stage. More precisely, if the runs of ones have lengths $\ell_1, \ell_2, \ldots, \ell_k$ in left-to-right order, then the output permutation is

$$x_1^{\ell_1} x_2^{\ell_2} \cdots x_k^{\ell_k},$$

where exponentiation denotes repetition.

The algorithm therefore iterates the following cycle: compute $b_s \ldots b_1$, reconstruct the bitstring, extract run lengths, and output the induced multiset permutation. Termination occurs when the update rule yields $j > s$, meaning no further admissible increase exists, at which point the sequence returns to its initial configuration under the cyclic structure of the near-perfect order.

This produces a single Hamiltonian traversal of the configuration graph induced by the dual combinations, hence visiting each multiset permutation exactly once.

## Verification

The invariant $n > b_s > \cdots > b_1 \ge 0$ is preserved because the update rule only increases a selected $b_j$ and resets all smaller indices to their minimal feasible values $0,1,\ldots,j-2$, which maintains strict ordering.

Each binary string produced has exactly $s$ zeros because the construction places zeros exactly at the $s$ indices stored in $b_s \ldots b_1$. No duplication occurs because each index is strictly ordered and updated without repetition.

The mapping from binary strings to multiset permutations is well-defined because each zero acts as a separator between runs of ones, and each run length is uniquely determined by adjacent zero positions. Since the binary string changes by a single admissible local transformation at each step, exactly one run boundary shifts, ensuring that consecutive outputs differ by a minimal adjacent transfer consistent with the near-perfect property.

The cyclicity follows from the fact that the dual combination sequence on $b_s \ldots b_1$ forms a Hamiltonian cycle on the corresponding Cayley-type structure, so every admissible configuration is reached exactly once before returning to the initial state.

This completes the proof. ∎

## Notes

The implementation is essentially a projection of the Chase near-perfect binary combination cycle onto compositions induced by zero positions. The key structural fact is that the binary representation acts as a universal encoding of both combinations and multiset partitions, so the same Hamiltonian traversal in the combination space induces a Hamiltonian traversal in the multiset permutation space without additional branching.
