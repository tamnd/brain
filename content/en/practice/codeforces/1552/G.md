---
title: "CF 1552G - A Serious Referee"
description: "We are asked to determine if a specific sequence of partial sorts can guarantee that any array of length $n$ will be fully sorted at the end. The input specifies $n$, the size of the array, and $k$, the number of sorting steps Andrea performs."
date: "2026-06-10T13:11:26+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dfs-and-similar", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1552
codeforces_index: "G"
codeforces_contest_name: "Codeforces Global Round 15"
rating: 3000
weight: 1552
solve_time_s: 74
verified: false
draft: false
---

[CF 1552G - A Serious Referee](https://codeforces.com/problemset/problem/1552/G)

**Rating:** 3000  
**Tags:** bitmasks, brute force, dfs and similar, sortings  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine if a specific sequence of partial sorts can guarantee that any array of length $n$ will be fully sorted at the end. The input specifies $n$, the size of the array, and $k$, the number of sorting steps Andrea performs. Each step is defined by a subsequence of indices; during that step, only the elements at those indices are rearranged into increasing order while all other elements remain fixed.

The output is binary: we print ACCEPTED if the sequence of partial sorts sorts every possible initial array, and REJECTED otherwise.

Looking at the constraints, $n$ is at most 40 and $k$ is at most 10. The small $n$ allows us to consider operations that involve iterating over the array or examining all pairs of indices without hitting performance limits. However, $k$ being small indicates that brute-forcing every possible initial permutation is infeasible because the number of permutations grows factorially with $n$. We need a solution that reasons about the structure of the partial sorts rather than simulating all arrays.

An edge case occurs when a step only sorts a single element or when indices of steps overlap poorly. For example, if $n=3$ and the steps are $[1,3]$ followed by $[2]$, some arrays like $[3,1,2]$ will never get fully sorted. A naive implementation that only checks whether a single array becomes sorted after applying the steps can give the wrong answer, because correctness requires sorting _any_ array.

## Approaches

A brute-force approach would be to generate every permutation of an array of size $n$ and simulate the algorithm on each one. After applying all $k$ sorting steps to each permutation, we would check if the result is sorted. This guarantees correctness because it literally tests every possible input, but the number of permutations is $n!$, which is around $8 \times 10^{47}$ for $n=40$. Even with the tiny $k$, this is computationally impossible.

The key insight is that we do not need to consider values at all; the algorithm only ever sorts subsequences. We can model the problem as a graph where each index is a node, and an edge connects two indices if there is a step that sorts both. Any pair of indices connected through a sequence of sorting steps can exchange their values. Therefore, we need to ensure that the relative ordering of every pair of array positions that are adjacent in the final sorted array is either directly sortable in a step or connected through a chain of steps.

Concretely, we can represent the connectivity using an $n \times n$ adjacency matrix, initializing edges between any pair that is in the same sorting step. Then we compute the transitive closure to determine which indices can indirectly exchange values. Finally, we check whether, for each pair of adjacent positions $i$ and $i+1$, they belong to the same connected component. If they do for all pairs, any array can be sorted, otherwise not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * k * n) | O(n) | Too slow |
| Optimal | O(k*n^2 + n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize an $n \times n$ adjacency matrix to represent connectivity between array indices. By default, each index is only connected to itself.
2. For each of the $k$ sorting steps, add edges between every pair of indices in that step. This encodes the idea that any
