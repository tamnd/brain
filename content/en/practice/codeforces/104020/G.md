---
title: "CF 104020G - Grinding Gravel"
description: "We are given several gravel stones, each with a positive integer weight. We also have a grid made of identical cells, and each cell must be filled exactly to a fixed capacity $k$."
date: "2026-07-02T04:41:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104020
codeforces_index: "G"
codeforces_contest_name: "2022 Benelux Algorithm Programming Contest (BAPC 22)"
rating: 0
weight: 104020
solve_time_s: 36
verified: false
draft: false
---

[CF 104020G - Grinding Gravel](https://codeforces.com/problemset/problem/104020/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several gravel stones, each with a positive integer weight. We also have a grid made of identical cells, and each cell must be filled exactly to a fixed capacity $k$. The total weight of all stones is guaranteed to match the total capacity of all grid cells, so in principle a perfect packing is always possible.

The difficulty is that individual stones are not required to match the cell capacity. When a stone is too large for the remaining space in a cell, we are allowed to break it into two smaller pieces, and those pieces can be used independently. Every time we perform such a split, it costs one unit, and we want to minimize the total number of splits required to make a perfect filling of all cells.

A useful way to think about the task is that we are trying to transform the initial multiset of weights into a finer multiset of smaller pieces whose total sum is unchanged, and then arrange those pieces into consecutive blocks of sum exactly $k$. The cost is the number of times we cut a piece into two during this process.

The constraints are small on the number of stones, at most 100, but the cell capacity $k$ is at most 8 while individual weights can be large up to $10^6$. This combination suggests that we should not attempt to model each unit of weight explicitly. Instead, we need a greedy or structural argument that reduces the problem to a controlled simulation or dynamic packing process.

A naive interpretation would try to consider all possible ways to split each weight into arbitrary sequences of parts and then assign them to bins of size $k$. This immediately explodes combinatorially because each number can be split in exponentially many ways.

A subtle failure case for naive greedy packing arises when we try to always fill the current bin with the next available stone without considering future fragmentation cost.

For example, suppose $k = 5$ and we have stones $[5, 4, 4]$. If we greedily take $4$, then another $4$, we are forced to split one of them across bins, increasing cost. However, if we handle the larger stone first, we may avoid unnecessary fragmentation. This shows that order matters, and a naive FIFO strategy over input order is not safe.

## Approaches

The brute-force viewpoint is to imagine every stone being split into unit pieces, and then try to group those units into segments of size $k$. This is clearly correct but completely infeasible because a single value like $10^6$ would produce a million unit elements, and we would then solve a partitioning problem over potentially millions of items.

We can refine this idea by noticing that splitting is only expensive when a stone crosses a bin boundary. If we imagine laying bins of length $k$ one after another on a line, each stone occupies a contiguous interval on that line. A split happens exactly when that interval crosses from one bin into the next. This reframes the problem as minimizing how often intervals cross bin boundaries under a rearrangement of intervals.

The key observation is that we are free to reorder stones arbitrarily before placing them along this line. This turns the problem into a greedy packing problem: we simulate filling bins sequentially, and whenever a stone does not fit into the remaining space of the current bin, we cut it at the boundary and continue in the next bin.

Because $k \le 8$, the number of boundary interactions per stone is small, and a straightforward greedy simulation is sufficient. The critical improvement over brute force is that we never explicitly represent the final small pieces, we only count how many times a stone is forced to cross a bin boundary.

The optimal strategy becomes: process larger stones first, always fill the current bin as much as possible, and cut only when necessary. Sorting in descending order prevents small fragments from being wasted early in ways that would force large future cuts.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|---|---
