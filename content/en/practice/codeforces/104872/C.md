---
title: "CF 104872C - Driving License Exam"
description: "We are given a path of intersections arranged in a line, where each adjacent pair is connected by a road with a certain length. Each intersection also contains some amount of “ice resource”."
date: "2026-06-28T10:24:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104872
codeforces_index: "C"
codeforces_contest_name: "2023-2024 Russia Team Open, High School Programming Contest (VKOSHP XXIV)"
rating: 0
weight: 104872
solve_time_s: 25
verified: false
draft: false
---

[CF 104872C - Driving License Exam](https://codeforces.com/problemset/problem/104872/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a path of intersections arranged in a line, where each adjacent pair is connected by a road with a certain length. Each intersection also contains some amount of “ice resource”. For any chosen segment of intersections from $l$ to $r$, we consider all roads inside that segment and additionally a temporary road that closes the segment into a cycle by connecting $l$ and $r$.

For a chosen segment, every road must be fully covered by ice. Ice is not freely available on roads; instead, it is stored at intersections, and each unit of ice at an endpoint can be moved to cover road length. Each intersection can distribute its ice to adjacent roads, but it cannot contribute more ice than it has.

The task of a query is to compute how much extra ice must be added to intersections so that, after redistribution, all roads in the chosen cyclic segment can be fully covered.

The input supports updates: changing ice at a node, changing road lengths, and answering these segment-cycle feasibility queries.

The key difficulty is that each query involves a different subarray plus a closing edge, and constraints are large enough that recomputing from scratch per query is impossible.

With up to $2 \cdot 10^5$ intersections and queries, any solution closer to $O(n)$ per query will fail. Even $O(n \log n)$ per query is too slow. We need roughly $O(\log n)$ per update and query combined, which strongly suggests a segment tree with carefully designed stored information.

A subtle edge case appears when a segment is barely feasible in total ice but still infeasible locally. For example, a node might have enough total ice but is positioned such that both adjacent roads require more than it can contribute simultaneously. Any correct solution must implicitly handle such local saturation constraints rather than only global sums.

## Approaches

A brute force approach would process each query of type 3 independently by extracting the segment $[l, r]$, computing all road demands including the closing edge, and simulating how ice could be distributed. One could attempt a greedy assignment: for each intersection, push ice to adjacent edges, tracking remaining deficits. This is already nontrivial, but even if implemented optimally it still costs $O(r-l+1)$ per query.

With $q$ up to $2 \cdot 10^5$, worst case behavior becomes $O(nq)$, which is far too slow.

The key observation is that feasibility depends only on local boundary interactions and additive contributions along segments. Each internal edge is shared by exactly two nodes, and each node contributes to at most two adjacent edges. This creates a structure similar to flow on a path where constraints decompose into prefix-consistent quantities.

We can reinterpret each node as having capacity $w_i$, and each edge requiring flow $d_i$. For a segment cycle, every node must distribute ice to its incident edges in that segment, and any deficit corresponds to additional required ice.

This transforms into a classic pattern: we need to maintain segment aggregates that describe how much “unmatched demand” accumulates when combining two subsegments. This is exactly the kind of state that a segment tree can merge, where each node stores not only sums but also a small number of boundary imbalance values representing how much extra ice would be needed dependi
