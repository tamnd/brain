---
title: "CF 1375B - Neighbor Grid"
description: "We are given a grid of integers, but the final goal is not to preserve these values exactly. Instead, we are allowed to only increase values, and we want to transform the grid into a configuration where every positive cell behaves like a “node” whose value equals how many of its…"
date: "2026-06-16T13:03:48+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1375
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 9"
rating: 1200
weight: 1375
solve_time_s: 138
verified: false
draft: false
---

[CF 1375B - Neighbor Grid](https://codeforces.com/problemset/problem/1375/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of integers, but the final goal is not to preserve these values exactly. Instead, we are allowed to only increase values, and we want to transform the grid into a configuration where every positive cell behaves like a “node” whose value equals how many of its four adjacent neighbors are also positive.

A cell with value zero is irrelevant to constraints, but any cell with value k greater than zero forces a very rigid structure: exactly k of its up, down, left, and right neighbors must also be positive. Since each cell has at most four neighbors, any positive value larger than four is immediately suspicious because it would require more neighbors than exist.

The output is either a valid transformed grid or a statement that no such transformation exists. Importantly, we can only increase values, never decrease them, so we cannot “fix” a cell by lowering it into compliance. This asymmetry is what drives the entire construction.

The constraints allow up to 100,000 total cells across all test cases, which strongly suggests a linear scan per test case is sufficient. Anything involving repeated global simulation or backtracking over configurations would be too slow.

A subtle failure case appears when large values exist in sparse regions. For example, a single cell with value 10 in any position is already impossible because even the maximum degree in a grid is four. Another tricky case is when corner or edge cells have high values, since their degree is even smaller.

## Approaches

A brute-force interpretation would be to treat this as a constraint satisfaction problem. Each cell is either active or inactive, and active cells must satisfy an exact degree condition. One might try choosing which cells become positive and then checking all constraints. This quickly explodes because there are 2^(nm) possible subsets, and even pruning by local constraints still leaves exponential structure due to interdependence between neighbors.

The key observation is that we do not actually need to preserve the given numbers beyond feasibility. Since we can only increase values, the only meaningful decision is which cells become positive in the final grid. Once a cell is positive, we can always raise its value to match the number of positive neighbors we assign it. So the real task reduces to selecting a set of cells such that each selected cell has at most four neighbors in the set, and then setting each chosen cell’s value exactly to that count.

This suggests trying a simple pattern that guarantees bounded degree everywhere. The standard trick is to use a checkerboard-like selection. If we choose cells in a pattern where no two selected cells are adjacent in certain directions, we can guarantee low degree. However, a pure checkerboard is too restrictive because it forces degree zero everywhere, which does not match arbitrary structure.

Instead, the known construction is to select cells greedily while ensuring that every chosen cell has at most two chosen neighbors. A convenient way to enforce this is to treat the grid as a graph and only select cells whose four neighbors are not all simultaneously selected. Practically, we decide the final positive set first and then assign values as degrees.

The actual CF solution simplifies further: we predefine the final positive set as all cells that are not part of a forbidden configuration, and then assign each positive cell its number of positive neighbors. If that assigned value is smaller than the original value, we increase it accordingly, which is allowed.

The critical simplification is that since we can only increase values, we should never be forced to reduce a target degree. Therefore, once we fix which cells are positive, we only need to ensure that for every chosen cell, its computed neighbor count is at least
