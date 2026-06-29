---
title: "CF 104720C - Cooking Class"
description: "We are given a fixed group of competitors, each with a known skill value, and Autumn, who also has an initial skill value. Autumn must choose exactly one of several available training classes, each of which adds a fixed positive boost to her skill."
date: "2026-06-29T07:10:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 29
verified: false
draft: false
---

[CF 104720C - Cooking Class](https://codeforces.com/problemset/problem/104720/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed group of competitors, each with a known skill value, and Autumn, who also has an initial skill value. Autumn must choose exactly one of several available training classes, each of which adds a fixed positive boost to her skill. After choosing one class, her final skill becomes her initial skill plus that boost.

Once all skills are fixed, the competition ranking is determined purely by sorting participants by skill in descending order. Higher skill means better rank. If multiple people share the same skill, they share the same rank, and the next rank skips ahead by the size of the tie group.

The task is to determine which single class Autumn should pick to achieve the best possible rank after the upgrade.

The input sizes matter significantly. Both the number of competitors and the number of classes can be up to 200,000. A solution that compares every class against every competitor directly would require up to 40 billion comparisons, which is far beyond what a 2-second limit allows. This immediately rules out any quadratic interaction between the two arrays.

A subtle point is how ties affect rank. If Autumn ties with many competitors at a certain skill level, her rank depends on how many people are strictly above her, not just whether someone equals her. This means we must carefully count how many competitors have skill strictly greater than Autumn's final skill.

A naive mistake is to treat rank as “position in sorted list after insertion” without properly handling equal values. For example, if competitors have skills `[10, 10, 5]` and Autumn becomes `10`, she is not rank 2 but rank 1.

Another failure case comes from recomputing rank independently per class using sorting. For large inputs, repeatedly sorting or scanning the entire array per class will time out.

## Approaches

The brute-force idea is straightforward. For each class, compute Autumn’s final skill, then scan all competitors and count how many have strictly greater skill. That count plus one gives Autumn’s rank for that class. We then take the minimum rank over all classes.

This works because ranking depends only on how many people are strictly above Autumn, not their order among themselves. However, this approach performs $O(N)$ work per class, leading to $O(NM)$ total operations. In the worst case, this is 4×10¹⁰ comparisons, which is infeasible.

The key observation is that for a fixed candidate skill value $x$, Autumn’s rank is completely determined by the number of competitors with skill greater than $x$. If we sort the competitors’ skills once, we can answer this count using binary search in logarithmic time. Each class then reduces to a single query: “how many values are greater than $S_A + P_i$?”

Sorting once costs $O(N \log N)$, and each query costs $O(\log N)$, giving an efficient overall solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Optimal | O(N log N + M log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all competitor skills and separate Autumn’s initial
