---
title: "CF 1279E - New Year Permutations"
description: "We are given a permutation of the numbers from 1 to n, and a rather unusual procedure that breaks this permutation into consecutive “blocks” based on reachability through functional edges defined by the permutation itself."
date: "2026-06-16T02:12:53+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 1279
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 79 (Rated for Div. 2)"
rating: 2700
weight: 1279
solve_time_s: 464
verified: false
draft: false
---

[CF 1279E - New Year Permutations](https://codeforces.com/problemset/problem/1279/E)

**Rating:** 2700  
**Tags:** combinatorics, dp  
**Solve time:** 7m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of the numbers from 1 to n, and a rather unusual procedure that breaks this permutation into consecutive “blocks” based on reachability through functional edges defined by the permutation itself.

Each index points to a value, and if we keep following these pointers, we stay inside a connected structure formed by the permutation’s directed edges. Every position belongs to exactly one such reachable component, and each component becomes a block when we scan from left to right and pick the first unmarked element.

Inside each block, we list elements in the order they appear in the original permutation, then rotate the block so that its maximum value moves to the front. After processing all blocks, we sort the blocks by their first element and concatenate them.

A permutation is called good if applying this entire block decomposition and reconstruction process returns the same permutation unchanged. The task is to enumerate all such good permutations in lexicographic order and output the k-th one.

The constraint n ≤ 50 is small enough that factorial growth is impossible to enumerate directly. Even storing all permutations is already infeasible beyond n around 12 or 13. Since k can be as large as 10^18, the number of valid permutations is enormous, but still structured enough to allow combinatorial counting with DP rather than brute force generation.

A naive approach would simulate all permutations and test the transformation, but even for n = 10 this is already 10! ≈ 3.6 million states, and checking structure per permutation is expensive. Another subtle failure case appears if one tries to greedily construct permutations without understanding how blocks interact, since the transformation depends on global reachability, not just local ordering.

## Approaches

The key difficulty is understanding what structure survives the transformation unchanged.

The decomposition described is essentially extracting connected components of the permutation graph formed by edges i → p[i], but taken in the order of appearance in the array. Within each component, the rotation moves the maximum element to the front, and then blocks are sorted by that maximum.

For a permutation to be fixed by the transformation, two conditions must hold simultaneously. First, every block must already have its maximum at the first position, otherwise the rotation step would change it. Second, blocks must already appear in increasing order of their first elements, otherwise sorting would reorder them.

Now observe what a block actually is. If we look at a component formed by following p[i], this is exactly a cycle in the permutation graph. So each block corresponds to a cycle, but written in the order induced by the array scan, not necessarily cyclic order.

Inside a cycle, the transformation forces the maximum element of that cycle to be placed first. For the permutation to be unchanged, that maximum must already be the first element in the cycle as it appears in the permutation.

Therefore, every cycle must appear in the array such that its maximum element is the first occurrence of that cycle, and cycles must be ordered by increasing maximum element. This means the permutation is completely determined by a partition of {1..n} into cycles, where each cycle is written starting from its maximum, and cycles are concatenated in increasing order of their maximums.

So the problem reduces to counting and constructing permutations formed by splitting numbers into cycles, each cycle rooted at its maximum, and ordering cycles by these roots. The internal order of a cycle corresponds to a cyclic permutation of its elements, but anchored at the maximum, meaning all other elements can appear in any order consistent with a cycle structure.

This becomes a combinatorial DP over subsets, where we choose the size of the first cycle, choose its elements, assign it a cyclic structure with maximum fixed first, and recurse.

The brute force approach would try all permutations and check validity, which is factorial. The optimal approach enumerates valid cycle partitions using combinatorics, counting for each subset how many ways to form a valid rooted cycle and multiplying across blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal DP over subsets | O(n^2 · 2^n) | O(n · 2^n) | Accepted |

## Algorithm Walkthrough

We build permutations in lexicographic order, so we construct them from left to right by deciding cycles in increasing order of their maximum element.

Each number n determines which cycle it belongs to, and n is always the maximum of its cycle. This follows from the structure constraint that cycles are ordered by their maximum, so the last cycle must contain n.

We proceed by selecting the cycle containing n, removing it, and recursively solving the remaining set.

1. Fix n as the maximum of the last cycle. We choose a subset S that contains n. This subset will form a cycle.
2. The remaining elements form an independent smaller problem. Once S is chosen, all elements outside S must appear before S in the final permutation.
3. For a chosen S, we count how many valid cycles can be formed where n is the first element in the cycle representation. The number of such cycles is (|S| − 1)! because after fixing n at the front, the remaining elements can be arranged arbitrarily in the cycle order.
4. We iterate over possible subsets S in increasing lexicographic contribution order. For each candidate subset, we compute how many permutations come from it using DP,
