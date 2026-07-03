---
title: "CF 103182K - Bathroom Tiles"
description: "A canonical basis $(alpha1,ldots,alphat)$ in Exercise 12 is represented in this section as a selection of $t$ distinguished positions among $n$, equivalently as an $(s,t)$-combination with $n=s+t$, encoded by a binary string $a{n-1}ldots a1a0$ satisfying $sum ai=t$."
date: "2026-07-03T16:24:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103182
codeforces_index: "K"
codeforces_contest_name: "AGM 2021, Final Round, Day 2"
rating: 0
weight: 103182
solve_time_s: 95
verified: false
draft: false
---

[CF 103182K - Bathroom Tiles](https://codeforces.com/problemset/problem/103182/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Solution

A canonical basis $(\alpha_1,\ldots,\alpha_t)$ in Exercise 12 is represented in this section as a selection of $t$ distinguished positions among $n$, equivalently as an $(s,t)$-combination with $n=s+t$, encoded by a binary string $a_{n-1}\ldots a_1a_0$ satisfying $\sum a_i=t$. The condition that a step changes just one bit means that consecutive configurations differ by a single toggle $a_i \leftarrow 1-a_i$.

The task is therefore to construct a Gray path that visits every binary string of length $n$ with exactly $t$ ones, with the restriction that consecutive strings differ in exactly one coordinate.

The construction uses the composition form of combinations from (7.2.1.3). Each $(s,t)$-combination corresponds uniquely to a composition

$s = q_t + \cdots + q_1 + q_0$

with $q_j \ge 0$ by equation (11), and the binary string has the structure

$a_{n-1}\ldots a_0 = 0^{q_t}1\,0^{q_{t-1}}1\cdots 1\,0^{q_0}.$

A change of a single bit in the binary string corresponds to transferring one unit between two adjacent components of the composition vector $(q_t,\ldots,q_0)$, or equivalently modifying exactly one gap between consecutive 1s.

The Gray path is constructed by induction on $t$. For $t=0$ there is a single configuration, so the claim holds. Assume a Gray path exists for all $(s',t')$ with $s'+t'<n$. For fixed $n=s+t$, partition all $(s,t)$-combinations according to the first position of a 1. If the leftmost 1 occurs at position $k$, then the remaining $t-1$ ones form an $(s-k,t-1)$-combination on the suffix of length $n-k-1$. This identifies the set of configurations with fixed $k$ as a translated copy of all $(s-k,t-1)$-combinations.

Within each fixed $k$, the induction hypothesis provides a Gray path on the suffix configurations, changing one bit at a time. The transition from block $k$ to block $k+1$ is achieved by shifting the leftmost 1 one position to the left, replacing a local pattern $01$ by $10$. This is a single bit change in the binary string.

To ensure a global Gray path, the traversal of the blocks is performed in alternating direction: when $k$ increases, the induced Gray path on the suffix is traversed forward; when $k$ decreases, it is traversed in reverse. This reflection guarantees that the endpoint of block $k$ differs from the start of block $k+1$ in exactly the same single-bit move that shifts the leftmost 1.

Thus every step either modifies the suffix by the inductive Gray path or moves the leading 1 across a single adjacent position, both of which change exactly one bit. Every $(s,t)$-combination appears exactly once because each block is exhausted exactly once and every composition is uniquely assigned to a block by the position of its leftmost 1.

This completes the proof. ∎
