---
title: "CF 1695C - Zero Path"
description: "We have a grid whose cells contain only 1 or -1. Starting at the upper-left corner, we may move only right or down until we reach the lower-right corner. Every visited cell contributes its value to the path sum. The task is not to find the number of such paths or the minimum sum."
date: "2026-06-09T22:43:38+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "graphs", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1695
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 801 (Div. 2) and EPIC Institute of Technology Round"
rating: 1700
weight: 1695
solve_time_s: 181
verified: false
draft: false
---

[CF 1695C - Zero Path](https://codeforces.com/problemset/problem/1695/C)

**Rating:** 1700  
**Tags:** brute force, data structures, dp, graphs, greedy, shortest paths  
**Solve time:** 3m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We have a grid whose cells contain only `1` or `-1`. Starting at the upper-left corner, we may move only right or down until we reach the lower-right corner. Every visited cell contributes its value to the path sum.

The task is not to find the number of such paths or the minimum sum. We only need to determine whether at least one valid path has total sum exactly `0`.

A path from `(1,1)` to `(n,m)` always visits the same number of cells. We make exactly `n-1` downward moves and `m-1` rightward moves, so the path contains

$$L=n+m-1$$

cells.

The total size of all grids is at most $10^6$ cells. This immediately rules out any algorithm that enumerates paths. Even a $20\times20$ grid already contains

$$\binom{38}{19}\approx 3.5\times10^{10}$$

different paths. We need a solution whose work is proportional to the number of cells.

Several edge cases are easy to miss.

Consider a single cell:

```
1 1
1
```

The only path has sum $1$, so the answer is `NO`.

A more subtle case is when the path length is odd:

```
1 2
1 -1
```

The path sum is $0$, so the answer is `YES`.

But:

```
1 3
1 -1 1
```

Every path contains three
