---
title: "CF 104686H - Insertions"
description: "We are given three strings. We start with a base string s, and we are allowed to take another string t and insert it at any position inside s, including before the first character or after the last one. This produces a new combined string."
date: "2026-06-29T08:51:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104686
codeforces_index: "H"
codeforces_contest_name: "2022-2023 ICPC Central Europe Regional Contest (CERC 22)"
rating: 0
weight: 104686
solve_time_s: 26
verified: false
draft: false
---

[CF 104686H - Insertions](https://codeforces.com/problemset/problem/104686/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three strings. We start with a base string `s`, and we are allowed to take another string `t` and insert it at any position inside `s`, including before the first character or after the last one. This produces a new combined string. After performing the insertion, we count how many times a third string `p` appears as a contiguous substring in the resulting string. Occurrences may overlap, so every valid match counts independently.

The task is not to construct the best string explicitly, but to reason about all possible insertion positions. For every index `k` in `0 … |s|`, we consider inserting `t` at that position and compute how many occurrences of `p` appear. We must output four values: the maximum number of occurrences over all positions, how many positions achieve that maximum, and among those positions the smallest and largest valid index.

The constraints are large: each string can be up to 100,000 characters. Any solution that recomputes substring matches from scratch for each insertion position would be far too slow, since there are `O(n)` positions and each check could cost `O(n)`, leading to `O(n^2)` behavior which is infeasible.

A key difficulty is that occurrences of `p` can straddle the insertion boundary. Matches may start in `s` and continue into `t`, or start in `t` and continue into the suffix of `s`. A naive method that only counts occurrences inside each part independently would miss these cross-boundary patterns.

Edge cases arise when `p` is longer than either `s` or `t`, or when `p` overlaps heavily with itself. In such cases, naive splitting approaches fail because they do not account for partial prefix-suffix alignment across the insertion point.

## Approaches

A brute-force solution tries every insertion position `k`. For each `k`, we build the resulting string and run a standard substring search for `p`, for example using KMP. This already costs `O(|s|)` per position, giving `O(|s|^2)` total time. Even with optimizations, rebuilding or simulating each insertion still repeats most work unnecessarily.

The key observation is that inserting `t` changes the answer in a structured way. Any occurrence of `p` in the final string falls into exactly one of three categories. It is either fully inside `s`, fully inside `t`, or it crosses the boundary between them. The first two categories are independent of the insertion position except for shifts; only the cross-boundary occurrences depend on where we insert.

This suggests separating the problem into static contributions and dynamic contributions. We can precompute all occurrences of `p` inside `s` and inside `t`. The only remaining difficulty is to count how many occurrences appear when a prefix of `p` is in `s` and the suffix is in `t`, or vice versa across the join points.

To handle this efficiently, we use prefix-function style matching (KMP border computation). For every position in `s` and `t`, we compute how much of `p` matches as a suffix ending there or a prefix starting there. This allows us to enumerate all potential split points where `p` crosses the boundary. Then for each insertion position, we can aggregate contributions using prefix sums over valid alignments.

The final step is reducing per-position recomputation. Instead of recomputing the cross-boundary count for each `k`, we precompute how many alignments are triggered for each insertion index using difference arrays or event accumulation over the valid alignment intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | s | ^2 + |
| Optimal | O( | s | + |

## Algorithm Walkthrough

We treat occurrences of `p` as contributions from three sources: inside `s`, inside `t`, and those crossing the insertion point.

1. Compute all occurrences of `p` inside `s` and inside `t` using KMP.

This gives two base counts that are independent of insertion position. These form a constant baseline added to every candidate `k`.
2. Build prefix-function arrays for `p` and use them to compute matching information over `s` and `t`.

For each position in `s`, we determine how much of `p` can end at that position as a suffix match. Similarly, for each position in `t`, we determine prefix matches of `p` starting there. This is necessary because a crossing occurrence is determined by a split `p = A + B`, where `A` ends in `s` and `B` starts in `t`.
3. Enumerate all split lengths of `p`.

For a split position `x`, the prefix `p[0:x]` must appear ending in `s`, and the suffix `p[x:]` must appear starting in `t`. Using the precomputed match arrays, we mark all valid end positions in `s` that support prefix `x`, and all valid start positions in `t` that support suffix `x`.
4. Convert these valid match conditions into contributions over insertion positions.

A split contributes to all insertion indices `k` where the su
