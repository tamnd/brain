---
title: "CF 104728L - Azur Lane"
description: "We are given the final state of a sequence of loot boxes after several days of operations. Each day, some multiset of boxes was obtained, then internally sorted in non-increasing order of rarity, and appended to the existing sequence."
date: "2026-06-29T03:26:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104728
codeforces_index: "L"
codeforces_contest_name: "Huazhong University of Science of Technology Freshmen Cup 2023"
rating: 0
weight: 104728
solve_time_s: 54
verified: false
draft: false
---

[CF 104728L - Azur Lane](https://codeforces.com/problemset/problem/104728/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the final state of a sequence of loot boxes after several days of operations. Each day, some multiset of boxes was obtained, then internally sorted in non-increasing order of rarity, and appended to the existing sequence. Over multiple days, this produces one long sequence, but the boundaries between days are lost.

The key structural property is that each day contributes a contiguous block whose values never increase from left to right. However, between two consecutive days, an increase may appear because a new day starts with a high-rarity box again.

We are given the final array and asked to reason about all possible ways to split it into exactly n days, for every n from 1 to m. For a fixed n, we consider all valid segmentations that respect the rule that each segment is non-increasing, and we want the minimum possible total cost. The cost of a day depends on how many boxes exist in the system at the end of that day, which means earlier boxes are counted multiple times across subsequent days.

So the problem is not only about finding a valid segmentation, but also about choosing one that minimizes a weighted contribution of segment positions.

The constraints push us toward an O(m log m) or O(m) solution since m can be up to 10^6. Any solution that tries to enumerate segmentations or run dynamic programming over all partitions is immediately impossible.

A few edge cases reveal the structure we must respect.

If the array has a strict increase anywhere, for example `[1, 3, 2]`, then positions inside a single day cannot cross that increase. So any valid segmentation must cut at every position where `a[i] > a[i-1]`. If we try to set n smaller than the number of forced segments, no valid construction exists.

Another subtle case is when the array is already fully non-increasing, such as `[5, 4, 3, 2]`. Then there are no forced cuts, and we have complete freedom to partition into any number of segments up to m. This flexibility is what allows optimization: different choices of cuts change the cost.

A third important observation is that splitting a valid non-increasing segment further always preserves validity. This me
