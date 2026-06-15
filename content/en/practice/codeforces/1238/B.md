---
title: "CF 1238B - Kill `Em All"
description: "The corridor can be seen as a number line where all monsters start strictly on the positive side. Each monster is a point on this line, and Ivan repeatedly performs an operation that chooses a center point and affects every monster depending on whether it lies to the left, at…"
date: "2026-06-15T20:39:53+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1238
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 74 (Rated for Div. 2)"
rating: 1300
weight: 1238
solve_time_s: 153
verified: false
draft: false
---

[CF 1238B - Kill `Em All](https://codeforces.com/problemset/problem/1238/B)

**Rating:** 1300  
**Tags:** greedy, sortings  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

The corridor can be seen as a number line where all monsters start strictly on the positive side. Each monster is a point on this line, and Ivan repeatedly performs an operation that chooses a center point and affects every monster depending on whether it lies to the left, at, or to the right of that center.

If a monster is exactly at the chosen center, it is immediately removed. Otherwise it is displaced by a fixed distance `r`: left-side monsters move further left by `r`, and right-side monsters move further right by `r`. Any monster that reaches position `0` or goes negative is instantly killed by traps.

The goal is to minimize how many such operations are needed to remove all monsters, and this must be answered for multiple independent scenarios.

The key constraint signal is the total number of monsters across all queries is at most 100,000, while each query can individually also be large. This immediately suggests that anything worse than linearithmic per query, especially anything quadratic, will fail under worst-case distributions. Sorting per query is safe, but repeated simulation of movements after each explosion is not.

A subtle edge case arises from how explosions “split” monsters: a single shot can kill some monsters immediately, but also push others to new positions that may later interact with different shots. For example, if monsters are tightly clustered, one explosion may clear many at once, but if they are spaced just right relative to `r`, they may continuously shift without being eliminated, leading naive greedy “always shoot the farthest monster” strategies to fail.

## Approaches

A brute-force interpretation would simulate each shot explicitly. We would pick a center, update all monster positions according to the rules, remove those that fall to zero or less, and repeat until no monsters remain. Even if we cleverly choose centers, each shot potentially touches all remaining monsters, and there can be up to `n` shots. This leads to a worst-case `O(n^2)` simulation per test, which is far beyond feasible when total `n` reaches `10^5`.

The structure becomes simpler once we shift
