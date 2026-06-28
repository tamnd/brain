---
title: "CF 104874K - King's Children"
description: "We are given an $n times m$ grid where each cell is either empty or contains exactly one castle labeled by an uppercase letter. There is exactly one castle labeled ‘A’, which belongs to the favorite child."
date: "2026-06-28T10:09:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104874
codeforces_index: "K"
codeforces_contest_name: "2019-2020 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104874
solve_time_s: 21
verified: false
draft: false
---

[CF 104874K - King's Children](https://codeforces.com/problemset/problem/104874/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times m$ grid where each cell is either empty or contains exactly one castle labeled by an uppercase letter. There is exactly one castle labeled ‘A’, which belongs to the favorite child. Every other castle is labeled by a distinct uppercase letter from ‘B’ to ‘Z’.

The task is to partition the entire grid into rectangular regions such that every cell belongs to exactly one rectangle, and each rectangle contains exactly one castle. Each rectangle is assigned to the owner of the castle it contains, and all empty cells inside that rectangle are filled with that owner’s lowercase letter.

Among all valid rectangular partitions, we must choose one that maximizes the area of the rectangle containing ‘A’.

The structure is a full tiling of the grid with axis-aligned rectangles, each anchored by exactly one special cell (a castle). This forces every rectangle to be a maximal region that can be assigned to a single castle without overlapping others.

The constraints $n, m \le 1000$ imply up to one million cells. Any solution that tries to enumerate all rectangle partitions or test all expansions independently will be far too slow. A solution must operate in roughly linear or near-linear time over the grid.

A key subtlety is that rectangles are not independent. Expanding one rectangle reduces space available for others, so a greedy local expansion without global structure can fail.

A typical failure case arises if one tries to grow each castle independently in all directions until hitting another castle. This can overclaim space or block valid partitions, because rectangles must tile the entire grid without overlap or gaps.

For example, if two castles are placed diagonally, naive expansion might let both grow into the same empty region depending on processing order, which is invalid because rectangles must partition the grid.

## Approaches

A brute-force idea is to consider every possible way of assigning each cell to one of the castles while ensuring the assigned region of each castle remains rectangular and connected. Even if we simplify and say each castle defines a rectangle, we would still need to try all possible rectangle boundaries for each castle.

For each castle, there are $O(nm)$ possible rectangles that contain it. With up to 26 castles, exploring all combinations already becomes astronomically large, on the order of $(nm)^{25}$ in the worst conceptual form. Even verifying a single full tiling would require checking overlaps and coverage, which itself is $O(nm)$. This makes brute force completely infeasible.

The key ob
