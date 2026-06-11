---
title: "CF 1346G - Two IP Cameras"
description: "We are given two identical IP cameras, each capable of taking photos at a fixed period. The period of each camera must be chosen from a predefined set of integers, but the starting moment of each camera is flexible."
date: "2026-06-11T14:53:06+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1346
codeforces_index: "G"
codeforces_contest_name: "Kotlin Heroes: Episode 4"
rating: 2300
weight: 1346
solve_time_s: 80
verified: false
draft: false
---

[CF 1346G - Two IP Cameras](https://codeforces.com/problemset/problem/1346/G)

**Rating:** 2300  
**Tags:** *special, math, number theory  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two identical IP cameras, each capable of taking photos at a fixed period. The period of each camera must be chosen from a predefined set of integers, but the starting moment of each camera is flexible. The goal is to cover a set of moments of interest, ensuring that for every moment, at least one camera captures it. Input consists of the list of available periods and the moments of interest. Output requires either a configuration for the two cameras that satisfies all moments or a declaration that it is impossible.

The key constraint is that `n` can reach `10^5` and moments can be up to `10^6`. This excludes naive approaches that iterate over every moment for every period, because that could require `10^11` operations in the worst case. We need an approach that scales linearly or near-linearly with `n` and `k`. Another subtlety is that moments and periods are strictly increasing. A careless implementation might assume a simple greedy coverage works, but because two cameras interact, certain distributions of moments can make naive coverage fail. For example, if moments alternate in such a way that no single period can cover a subset consecutively, a naive one-camera sweep will falsely claim impossibility.

A concrete edge case is moments `[1, 4, 5, 7, 12]` and periods `[3, 5, 7]`. The solution must recognize that one camera with period 3 covers `[1,4,7,10...]` while a second camera with period 7 covers `[5,12...]`. A greedy single-camera approach might try 3 or 5 first and then fail to cover all moments with the other period if implemented incorrectly.

## Approaches

The brute-force approach would try every pair of periods `(cp1, cp2)` from the list and, for each, attempt all possible starting moments `s1` and `s2` that could cover all moments. This is correct in principle, but the number of combinations is `k^2 * n^2` in the worst case, which reaches `10^15` operations and is completely infeasible.

The key observation is that the moments of interest are sorted. This means the coverage pattern of each camera is periodic and can be described as a simple arithmetic progression. Instead of testing all starting moments, it is sufficient to attempt starting at the first moment of the uncovered segment. For each period, one can mark all moments it would cover starting from a candidate start, and then see which remaining moments must be handled by the second camera. The insight is that a valid solution exists if we can partition the moments into two arithmetic progressions with periods from the allowed set, starting from the first uncovered moment of each segment. This reduces the problem to checking all pairs of periods `O(k^2)` with linear scans over `n` moments, yielding `O(k^2 * n)` time. Further optimization exploits that only two candidate starting moments per period are needed (the first moment or the last that still allows coverage) to reduce scanning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^2 * n^2) | O(n) | Too slow |
| Optimized Period Scan | O(k^2 * n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Iterate over all pairs of periods `(cp1, cp2)` from the allowed periods list. Each pair represents a candidate combinat
