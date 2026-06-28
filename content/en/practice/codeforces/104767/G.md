---
title: "CF 104767G - Hamster"
description: "We are given a set of unit segments drawn on the integer grid. Each segment connects two grid intersection points that are exactly one step apart horizontally or vertically."
date: "2026-06-29T02:28:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "G"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 33
verified: false
draft: false
---

[CF 104767G - Hamster](https://codeforces.com/problemset/problem/104767/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of unit segments drawn on the integer grid. Each segment connects two grid intersection points that are exactly one step apart horizontally or vertically. If we view every grid intersection as a vertex and every given segment as an undirected edge, the input describes a sparse subgraph of the infinite grid graph.

A hamster moves along grid edges between adjacent vertices as long as there is no wall segment blocking that move. The goal is to install additional unit segments so that the hamster becomes trapped inside at least one enclosed region, meaning there is at least one bounded face in the resulting planar drawing. In graph terms, this corresponds to creating at least one simple cycle in the final graph, because any cycle in a grid graph encloses a region that cannot be escaped without crossing an edge.

The task is to determine the minimum number of additional unit edges that must be added between currently unused adjacent grid points to guarantee that the resulting graph contains at least one cycle.

The constraints
