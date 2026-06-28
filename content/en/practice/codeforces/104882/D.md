---
title: "CF 104882D - Delicious pies"
description: "We are given a row of pies indexed from left to right, where each pie is either cabbage or mushroom. Two children repeatedly take pies from this row according to a positional rule: one child targets every 3rd remaining pie, the other targets every 7th remaining pie."
date: "2026-06-28T09:18:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104882
codeforces_index: "D"
codeforces_contest_name: "Voronezh State University - Sitronics contest II"
rating: 0
weight: 104882
solve_time_s: 26
verified: false
draft: false
---

[CF 104882D - Delicious pies](https://codeforces.com/problemset/problem/104882/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of pies indexed from left to right, where each pie is either cabbage or mushroom. Two children repeatedly take pies from this row according to a positional rule: one child targets every 3rd remaining pie, the other targets every 7th remaining pie. They do not act independently on a fixed index system. Instead, they alternate turns, always selecting from the current remaining sequence of pies, starting with Masha.

A key detail is that the “3rd pie” or “7th pie” is interpreted relative to the current state of the remaining pies after previous removals. Each move removes one pie, which shifts the indexing of all subsequent selections. The process continues until all pies are taken, and we must count how many mushroom pies each child ends up eating.

The input size is up to 100000 pies, so any approach that simulates re-indexing with naive deletions must be carefully considered. A direct simulation that scans the array repeatedly and removes elements would degrade to quadratic behavior, which is too slow under a 1 second limit. Even more subtle, using a dynamic list and repeatedly selecting the k-th active element using linear scans leads to around O(n^2) behavior in the worst case.

A straightforward pitfall appears when one assumes that Masha always takes indices 3, 6, 9, and Petya always takes 7, 14, 21 in the original array. That interpretation is wrong because removals shift positions. For example, with a small sequence like 1 1 0 1 0 1 1, the overlap at index 21-like positions is meaningless; the actual chosen elements depend on evolving structure, not fixed arithmetic progressions.

Another subtle issue is tie-breaking due to overlap in targets. When both children would select the same pie in the same conceptual step, only one of them actually takes it, and the other must continue scanning to the next valid target in the remaining structure. This prevents double counting and ensures each pie is taken exactly once.

## Approaches

A naive simulation maintains a list of remaining pies and repeatedly performs two operations: advance a pointer counting alive pies until reaching the k-th available position, then remove it. This is correct because it directly mirrors the process definition. However, each removal requires scanning through up to O(n) elements, and this happens O(n) times, giving O(n^2) complexity.

The key observation is that the only thing that matters is the order in which pies are removed, not their shifting indices. At every step, we are effectively performing a repeated “select k-th alive element” operation on a shrinking sequence. This is a classical order-statistics problem over a dynamic array. Instead of simulating deletions, we maintain a structure that can quickly find and remove the k-th active element.

A Fenwick tree (binary indexed tree) over a 0/1 array indicating whether a pie is still present allows us to support two operations efficiently: counting how many pies are still alive up to a position, and finding the position of the k-th alive pie via binary lifting. Each move becomes O(log n), leading to an overall O(n log n) solution.

We simulate the process step by step, alternating between Masha and Petya, but each selection is resolved using order statistics on the alive set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Fenwick Tree Simulation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a Fenwick tree over an array of size n, where each position initially has value 1 indicating the pie is still present.

We also maintain two counters: one for Masha’s next target rank and one for Petya’s next target rank. These represent “take every 3rd remaining pie” and “take every 7th remaining pie” respectively, but interpreted over the shrinking sequence.

### Steps

1. Initialize a Fenwick tree with all positions set to 1. This represents all pies being available.
2. Set a pointer `turn = 0` to indicate Masha starts first.
3. Maintain two counters: `kM = 3` and `kP = 7`, representing the next target order statistic in the remaining sequence for Masha and Petya respectively.
4. Repeat until all pies are removed:

1. If `turn == 0`, we want Masha’s kM-th remaining pie. We query the Fenwick tree to find the smallest index where the prefix sum equals kM. This gives the actual position in the original array among remaining pies. Remove it by updating the tree at that position to 0. If it is a mushroom pie, increment Masha’s score. Then increment kM by 3 because she now targets the next multiple in the remaining sequence.
2. If `turn == 1`, we do the same for Petya using kP and incrementing by 7 after each successful removal.
3. Switch `turn` to the other player.

Each selection works because the Fenwick tree maintains the mapping between “k-th alive pie” and actual index in the original array, despite deletions shifting positions.

### Why it works

At any point, the remaining pies form an ordered subsequence of the original array. The Fenwick tree encodes this subsequence as a dynamic prefix-sum structure. The k-th alive query always returns the correct current position in that subsequence, independent of previous removals. Since each player’s rule depends only on relative rank in the current sequence, maintaining correct order statistics is sufficient to
