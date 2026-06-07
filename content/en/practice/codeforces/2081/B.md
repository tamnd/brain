---
title: "CF 2081B - Balancing"
description: "A partition of the vertices of a convex $n$-gon with the property that no diagonal drawn inside one part crosses a diagonal drawn inside another part is equivalent to requiring that each part induces a noncrossing set of diagonals, and different parts are nested in a laminar…"
date: "2026-06-08T06:22:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2081
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1010 (Div. 1, Unrated)"
rating: 2500
weight: 2081
solve_time_s: 112
verified: false
draft: false
---

[CF 2081B - Balancing](https://codeforces.com/problemset/problem/2081/B)

**Rating:** 2500  
**Tags:** greedy  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
A partition of the vertices of a convex $n$-gon with the property that no diagonal drawn inside one part crosses a diagonal drawn inside another part is equivalent to requiring that each part induces a noncrossing set of diagonals, and different parts are nested in a laminar fashion. This structure is precisely encoded by a plane tree whose leaves are the $n$ vertices of the polygon and whose internal nodes correspond to the blocks of the partition.

Given such a partition, construct a tree as follows. Each block of the partition becomes a node. Whenever one block is strictly contained in the convex hull structure induced by another block, make the former a child of the latter in the tree. The noncrossing condition guarantees that containment relations are well defined and do not conflict, so the resulting structure is a rooted ordered tree. Conversely, from any rooted ordered tree with $n$ leaves labeled cyclically by the polygon vertices, one recovers a noncrossing partition by grouping vertices according to the lowest common ancestor structure induced by the tree. This establishes a one-to-one correspondence between the partitions and plane trees with $n$ leaves.

Fix $n$ and $k$. The corresponding trees have $n$ labeled leaves and $k$ internal nodes, since each part of the partition corresponds to exactly one internal node in the tree representation. Such trees are counted by the Narayana numbers, since noncrossing partitions of an $n$-element cyclically ordered set into $k$ blocks are equinumerous with plane trees with $k$ internal nodes and $n$ leaves.

The number of noncrossing partitions of an $n$-gon vertices into $k$ parts is therefore

$$\frac{1}{n}\binom{n}{k}\binom{n}{k-1},$$

which is the Narayana number $N(n,k)$. This completes the correspondence and the enumeration. ∎
