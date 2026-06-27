---
title: "CF 105172I - Nanami and the Golden Sunlight Sunflower Fields"
description: "We are given an $n times n$ grid where some cells are already occupied. Each occupied cell behaves like a node in a grid graph, and edges exist between orthogonally adjacent cells."
date: "2026-06-27T08:25:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105172
codeforces_index: "I"
codeforces_contest_name: "The 20th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105172
solve_time_s: 36
verified: false
draft: false
---

[CF 105172I - Nanami and the Golden Sunlight Sunflower Fields](https://codeforces.com/problemset/problem/105172/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times n$ grid where some cells are already occupied. Each occupied cell behaves like a node in a grid graph, and edges exist between orthogonally adjacent cells. Our task is to add new occupied cells in empty positions so that all occupied cells, original plus added, form a single connected component under 4-directional movement.

There is a hard constraint on how many cells we are allowed to add: at most $\lfloor n^2 / 2 \rfloor$. We cannot move or remove any of the original occupied cells, so the final set must strictly contain them.

The output is simply another grid of the same size, marking which cells are occupied after additions. Any valid configuration is accepted as long as all original occupied cells remain, the final occupied cells are connected, and the number of added cells does not exceed the limit.

The grid size is at most $50 \times 50$, so there are at most 2500 cells per test case. This is small enough that we can afford algorithms with quadratic behavior per test case, but not anything involving exponential search over subsets of cells.

A key structural implication of the constraint is that the final connected component cannot exceed about half the grid. Since we may add at most half the cells, the final number of occupied cells is at most $\lceil n^2 / 2 \rceil$. This means the original configuration is always sparse enough to be connectable within a limited “budget” of added cells, even if it looks scattered.

The main failure cases for naive reasoning come from connectivity assumptions.

If we try to connect components greedily without considering path overlap, we may overcount and exceed the allowed number of additions. For example, if each original cell is isolated and we connect them one by one with shortest paths, we might repeatedly traverse already used areas in different ways, effectively rebuilding large portions of the grid multiple times.

Another subtle case is when origin
