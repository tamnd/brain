---
title: "CF 104609H - Emergency"
description: "We are given a small grid of rooms, each room having up to four possible exits corresponding to the four cardinal directions."
date: "2026-06-30T02:47:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104609
codeforces_index: "H"
codeforces_contest_name: "Udmurt SU + Izhevsk STU Contest 2012"
rating: 0
weight: 104609
solve_time_s: 45
verified: false
draft: false
---

[CF 104609H - Emergency](https://codeforces.com/problemset/problem/104609/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small grid of rooms, each room having up to four possible exits corresponding to the four cardinal directions. Some of these exits connect to neighboring rooms, some lead directly outside the building, and some connections between adjacent rooms are explicitly blocked.

In every room we must choose exactly one usable exit and draw an arrow pointing through it. After this choice is made, every room has a single outgoing move. Starting from any room and repeatedly following the arrows, the path must eventually leave the building rather than getting stuck in an infinite loop inside the grid.

The task is to count how many such arrow assignments exist, taking into account that blocked passages remove certain possible moves between adjacent rooms. The result is required modulo 1e9 + 7.

The grid size is at most 10 by 10, so there are at most 100 rooms, and at most 10 blocked passages. This immediately rules out any brute force that tries to enumerate all arrow assignments directly. Even if each cell had only two choices on average, the number of configurations would already explode exponentially.

A subtle failure case for naive reasoning is to treat each room independently. For example, in a 2 by 2 grid with no blocked edges, one might think each cell independently chooses an exit leading outward or inward. However, choices interact globally: selecting arrows can create directed cycles entirely inside the grid, and those are invalid because they prevent escape.

The core difficulty is that validity is a global acyclicity condition over a directed structure induced by local choices.

## Approaches

Each room chooses exactly one outgoing passage. Once all choices are made, the grid becomes a directed graph where every node has outdegree exactly one. The requirement is that from every node, repeated traversal eventually reaches the outside of the grid.

This is equivalent to saying there are no directed cycles among the rooms. If a cycle exists entirely inside the grid, then starting at any node in that cycle will never reach the outside.

A brute force solution would iterate over all ways to assign an outgoing edge for each of the n^2 cells. Each cell has up to 4 options, so the number of configurations is on the order of 4^(n^2). For n = 10, this is astronomically large and completely infeasible.

The key structural observation is that the outside of the grid behaves like a single absorbing root. Every valid configuration induces a functional graph where each node points to exactly one parent, and every path eventually leads to this root. If we reverse all chosen arrows, every node except the root has exactl
