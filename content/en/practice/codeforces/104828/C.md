---
title: "CF 104828C - \u6570\u4e09\u5143\u56fe"
description: "We are given a tournament-style directed graph: every pair of distinct vertices has exactly one directed edge between them. For any two nodes $u$ and $v$, either $u to v$ or $v to u$, never both and never none."
date: "2026-06-28T12:26:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104828
codeforces_index: "C"
codeforces_contest_name: "The 11-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104828
solve_time_s: 25
verified: false
draft: false
---

[CF 104828C - \u6570\u4e09\u5143\u56fe](https://codeforces.com/problemset/problem/104828/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tournament-style directed graph: every pair of distinct vertices has exactly one directed edge between them. For any two nodes $u$ and $v$, either $u \to v$ or $v \to u$, never both and never none. This structure is equivalent to choosing an ordering direction for every pair.

Among all such orientations on $n$ labeled vertices, we want to count how many contain at least one directed triangle of length three, meaning there exist distinct vertices $a, b, c$ such that $a \to b$, $b \to c$, and $c \to a$. The answer must be computed modulo $p$, and there are multiple test cases.

The input constraints are extremely large: $T$ up to $10^4$, and the sum of all $n$ values up to $5 \cdot 10^6$. This immediately rules out any solution that depends on iterating over pairs or triples per test case. Even $O(n^2)$ per test case is impossible, since the worst-case total work would be around $10^{12}$.

A key structural observation is that the graph model is a complete orientation, so the total number of possible graphs is exactly $2^{\binom{n}{2}}$. The difficulty is enforcing the condition “contains at least one directed triangle”.

A naive trap is to try to directly enumerate all triples $(a,b,c)$ and check if they form a cycle. Even counting triangles in a fixed orientation is already expensive, and here we are counting orientations, not triangles inside one graph.

Another subtle issue is the “at least one triangle” condition. It is often easier to count the complement: triangle-free tournaments. Forgetting this inversion leads to overcounting or complicated inclusion-exclusion that does not scale.

Example edge cases:

For $n = 1$ or $n = 2$, no triple exists, so the answer must be 0 because no directed triangle can exist at all.

For $n = 3$, there are $2^3 = 8$ tournaments. Exactly 2 of them are cyclic triangles, and the other 6 are transitive (acyclic). So the answer should be 2.

A naive approach that tries to detect triangles per configuration would already be infeasible even for small $n$, since the state space grows exponentially.

## Approaches

The core idea is to avoid reasoning about triangles directly and instead classify all tournaments into two disjoint types: those that contain a directed cycle of length three, and those that do not. The latter class is much more structured.

A brute-force formulation would be:

Generate every orientation of all $\binom{n}{2}$ edges, and check whether it contains a directed triangle. This is c
