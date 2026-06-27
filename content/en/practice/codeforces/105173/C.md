---
title: "CF 105173C - Ring"
description: "We are given a circular necklace of length $n$, where each bead is either red or blue. The beads are indexed around a ring, so index arithmetic wraps around modulo $n$."
date: "2026-06-27T08:19:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105173
codeforces_index: "C"
codeforces_contest_name: "The 2024 CCPC National Invitational Contest (Northeast), The 18th Northeast Collegiate Programming Contest"
rating: 0
weight: 105173
solve_time_s: 37
verified: false
draft: false
---

[CF 105173C - Ring](https://codeforces.com/problemset/problem/105173/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular necklace of length $n$, where each bead is either red or blue. The beads are indexed around a ring, so index arithmetic wraps around modulo $n$. A single operation picks a starting position $i$ and a fixed odd length $k$, then looks at the $k$ consecutive beads starting at $i$ along the circle. All beads in that segment are overwritten by the majority color inside that segment.

The process is repeated until the entire ring becomes monochromatic. The twist is that the first operation is free, and every subsequent operation costs one unit. We must choose the first operation optimally, then assume optimal play afterward, and compute two things: the minimum number of paid operations needed to make all beads the same color, and how many choices of the first starting position $i$ achieve that minimum.

The constraint scale is large: $n$ can reach $10^6$ per test case and there are up to $10^5$ test cases. This immediately rules out any quadratic simulation per test case. Even $O(n \log n)$ per test is too slow in aggregate. Any valid solution must be essentially linear per test case, possibly amortized.

A subtle point is that the first operation changes the configuration in a global way, and different choices of $i$ can lead to different residual “difficulty”. A naive approach would try all $n$ first moves and simulate the process, but that would multiply a large linear cost by $n$, which is infeasible.

Edge cases that often break naive reasoning include uniform strings, where any operation is harmless, and highly alternating strings, where every window majority flips significant structure. Another tricky situation is when multiple first operations lead to identical resulting configurations, so counting distinct valid $i$ requires care.

## Approaches

A brute force interpretation is straightforward: for each possible starting position $i$, apply the first operation on that window, then repeatedly apply optimal operations until the string becomes uniform, and count how many steps are needed. Even if we assume a clever greedy strategy after the first move, we would still need to recompute the effect of that first move for all $n$ choices.

The core bottleneck is that each first move modifies $k$ consecutive positions on a cycle, and doing this for all $n$ starts already costs $O(nk)$ preprocessing in the worst case. Since $k$ can be as large as $n$, this degenerates into $O(n^2)$ per test case, which is far beyond limits.

The key observation is that the first operation only matters through how it changes local majority structure, and the remaining process depends only on where “inconsistencies” remain, not on the exact history. Because every operation replaces a length-$k$ window by a constant block, the evolution always moves toward eliminating alternating boundaries, and
