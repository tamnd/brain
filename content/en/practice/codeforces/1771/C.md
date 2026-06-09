---
title: "CF 1771C - Hossam and Trainees"
description: "This is a Type C (optimization) problem. The requirements are to establish an upper bound on the boundary length $L$ between horizontal and vertical dominoes and to exhibit a construction that achieves the maximal possible $L$."
date: "2026-06-09T12:22:49+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1771
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 837 (Div. 2)"
rating: 1600
weight: 1771
solve_time_s: 132
verified: false
draft: false
---

[CF 1771C - Hossam and Trainees](https://codeforces.com/problemset/problem/1771/C)

**Rating:** 1600  
**Tags:** greedy, math, number theory  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a Type C (optimization) problem. The requirements are to establish an upper bound on the boundary length $L$ between horizontal and vertical dominoes and to exhibit a construction that achieves the maximal possible $L$. The proposed solution attempts both: it claims an upper bound $L\le52$ and gives a checkerboard block construction yielding $L=48$. Therefore the problem type matches the intended analysis. However, the correctness depends on the rigor of the upper-bound argument, not just the construction.

## Step-by-Step Verification

**Step 1: Definition of $L$ as the total number of unit edges separating horizontal and vertical dominoes.** - VALID.

The definition is standard and correctly captures the combinatorial quantity of interest.

**Step 2: Observation that each domino contributes at most four mixed edges, giving a naive maximum of 128.** - VALID.

This is a correct preliminary bound; no assumptions are made yet about tiling constraints.

**Step 3: Introduction of $2\times2$ squares as minimal subgrids that can contain two horizontal or vertical dominoes.** - UNJUSTIFIED. **Critical error.**

The solution repeatedly refers to $2\times2$ blocks as “minimal units” for maximal boundary counting. In an arbitrary domino tiling, dominoes can cross the boundaries of a $2\times2$ block, so it is false that each such block is internally tiled by either two horizontal or two vertical dominoes. The reduction from an $8\times8$ board to a $4\times4$ checkerboard of blocks is therefore invalid for bounding $L$ in general.

**Step 4: Checkerboard $2\times2$ block construction to achieve $L=48$.** - VALID.

As a construction, the argument is correct. All cells are covered, dominoes do not overlap, and each interface between differing block orientations contributes exactly two edges. The claimed boundary length of $48$ is achieved.

**Step 5: Upper-bound argument using counting of vertical and horizontal interfaces between rows and columns, claiming $L\le52$.** - UNJUSTIFIED. **Justification gap / incomplete.**

The solution mentions $7\times8$ vertical interfaces and $8\times7$ horizontal interfaces, with a maximum of two edges per interface, and states that tiling constraints reduce this to $52$. No detailed combinatorial argument is given to justify why some interfaces must align in orientation, so the upper bound is asserted without proof. It is plausible, but the reasoning is incomplete.

**Step 6: Complexity analysis and test cases.** - VALID.

The construction is explicit, verifiable, and requires only constant time and space. The test code correctly confirms $L=48$.

## Completeness Check

The solution correctly constructs a tiling with $L=48$ and explains its counting. However, the argument for the upper bound $L\le52$ is insufficient. The reasoning relies on informal counting of interfaces without providing a rigorous combinatorial or parity argument to exclude configurations exceeding 52. Therefore part (1) of the problem is not fully justified, and the solution does not prove that $48$ is indeed maximal beyond the checkerboard construction.

No treatment is provided of other potential tilings, dominoes crossing interfaces, or global constraints that could limit $L$, so unhandled cases exist. The conclusion that $L\le52$ and that $L=48$ is maximal does not rigorously follow from the steps given.

## Summary

The construction achieving $L=48$ is correct, but the proposed upper-bound argument for $L\le52$ is incomplete and relies on unproven assumptions about the arrangement of dominoes. The solution fails to rigorously justify part (1) of the problem, leaving the maximality of $L$ unproven.

VERDICT: FAIL - the solution does not rigorously prove the upper bound on $L$, relying on informal interface counting without handling arbitrary tilings.
