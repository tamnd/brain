---
title: "CF 2178F - Conquer or of Forest"
description: "We are given a rooted tree with vertices numbered from 1 to $n$. Each vertex is colored based on the size of its subtree: if the subtree size is even, the vertex is white; otherwise, it is black."
date: "2026-06-07T22:23:30+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 2178
codeforces_index: "F"
codeforces_contest_name: "Good Bye 2025"
rating: 2200
weight: 2178
solve_time_s: 35
verified: false
draft: false
---

[CF 2178F - Conquer or of Forest](https://codeforces.com/problemset/problem/2178/F)

**Rating:** 2200  
**Tags:** combinatorics, math, trees  
**Solve time:** 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with vertices numbered from 1 to $n$. Each vertex is colored based on the size of its subtree: if the subtree size is even, the vertex is white; otherwise, it is black. The goal is to count the number of distinct trees that can be formed using a specific operation that moves white vertices around while maintaining the tree structure, such that the tree becomes “conquered.” A tree is conquered if either there are no white vertices, or all white vertices lie on a single path from the root to some vertex.

The input consists of multiple test cases, each providing the number of vertices and the list of edges. The output is the number of conquered trees modulo $998244353$.

Constraints indicate that the number of vertices can reach $2\cdot 10^5$, and the sum over all test cases is also up to $2\cdot 10^5$. This rules out any brute-force approach that tries to simulate all possible tree reconnections, because the number of potential trees grows exponentially with $n$. The solution must rely on structural properties of subtree sizes and combinatorial counting rather than explicit enumeration.

Non-obvious edge cases include trees where all vertices are black (already conquered), trees with only one white vertex deep in the tree, and trees where all non-root vertices are white. For example, a tree of 2 vertices connected directly to the root has one white vertex if the leaf’s subtree size is even; the algorithm must correctly count the possible reconnections, even when the root has no children.

## Approaches

A naive approach is to try every possible operation sequence on white vertices, reconnecting them to every valid pair of vertices and then recoloring, counting every distinct tree. This is cor
