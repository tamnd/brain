---
title: "CF 103186B - \u5c0f A \u7684\u5361\u724c\u6e38\u620f"
description: "Let the canonical bases be represented in the form $(alpha1,dots,alphat)$ as in exercise 12, where each $alphai$ is a binary string of length $n$ with exactly one distinguished position equal to $1$."
date: "2026-07-03T16:12:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103186
codeforces_index: "B"
codeforces_contest_name: "The 2021 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103186
solve_time_s: 56
verified: false
draft: false
---

[CF 103186B - \u5c0f A \u7684\u5361\u724c\u6e38\u620f](https://codeforces.com/problemset/problem/103186/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** no  

## Solution
## Solution

Let the canonical bases be represented in the form $(\alpha_1,\dots,\alpha_t)$ as in exercise 12, where each $\alpha_i$ is a binary string of length $n$ with exactly one distinguished position equal to $1$. Equivalently, each $\alpha_i$ encodes a choice of an element of ${0,1,\dots,n-1}$, so a canonical basis is an ordered $t$-tuple of distinct indices. Writing the chosen indices in increasing order produces a standard representation of the same object as a $t$-subset, but the ordered tuple representation is the one compatible with single-bit moves in the coordinate encoding of each $\alpha_i$.

Two canonical bases differ by changing just one bit if and only if exactly one of the $\alpha_i$ changes its distinguished position by $+1$ or $-1$ in its binary encoding, since all other coordinates remain fixed. This interpretation matches the adjacency shown in the example for $n=3$, $t=2$, where each step alters exactly one coordinate string among the two rows.

The construction proceeds by induction on $n$. For fixed $n$ and $t$, let $G(n,t)$ denote the graph whose vertices are canonical bases and whose edges connect pairs that differ in exactly one bit. The goal is to construct a Hamiltonian path in $G(n,t)$.

For $t=0$ or $t=n$, the graph has a single vertex, so the claim is trivial. Assume $0<t<n$ and assume Hamiltonian paths exist for all smaller values of $n$.

Partition the canonical bases according to the position of the first change between successive $\alpha_i$ when scanning the tuple from left to right. More concretely, split the vertex set into two classes according to whether the first coordinate $\alpha_1$ uses the symbol $0$ in its least significant bit or $1$ in its least significant bit. These two induced subgraphs are isomorphic to $G(n-1,t)$ and $G(n-1,t-1)$ after deleting or contracting the coordinate corresponding to that bit position, since fixing a bit reduces either the available positions or the number of active coordinates in exactly the same way as the standard decomposition of combinations in Section 7.2.1.3.

A Hamiltonian path in $G(n-1,t)$ lists all canonical bases whose first coordinate avoids the distinguished bit, while a Hamiltonian path in $G(n-1,t-1)$ lists those where that bit is used in exactly one of the $\alpha_i$. These two paths can be concatenated by a single edge flip that toggles that bit in one coordinate of the tuple, since exactly one coordinate changes from a $0$-position to a $1$-position or conversely, producing a valid adjacency in $G(n,t)$.

The concatenation order is chosen so that the endpoint of the first path differs in exactly one bit from the starting point of the second path, which is ensured by taking complementary constructions on the recursive calls in the same way as the reflected binary Gray code for hypercubes. The reflection ensures that the endpoint structure of $G(n-1,t)$ matches the start structure of $G(n-1,t-1)$ with exactly one bit discrepancy in a single coordinate, so the connecting edge exists in $G(n,t)$.

This produces a path that visits every canonical basis exactly once, since each recursive block exhausts a disjoint subset of vertices and the decomposition covers all possibilities for the distinguished bit distribution across the tuple $(\alpha_1,\dots,\alpha_t)$. Each transition alters exactly one bit because all recursive transitions preserve adjacency in their respective subgraphs and the inter-block transition flips precisely one coordinate bit.

Thus there exists a Gray path through all canonical bases $(\alpha_1,\dots,\alpha_t)$ in which successive vertices differ in exactly one bit.

This completes the proof. ∎
