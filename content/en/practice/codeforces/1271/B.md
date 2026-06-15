---
title: "CF 1271B - Blocks"
description: "We are given a line of blocks, each painted either black or white. The only allowed move is to pick two neighboring blocks and flip both of them at the same time, turning white into black and black into white."
date: "2026-06-16T01:14:20+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1271
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 608 (Div. 2)"
rating: 1300
weight: 1271
solve_time_s: 252
verified: false
draft: false
---

[CF 1271B - Blocks](https://codeforces.com/problemset/problem/1271/B)

**Rating:** 1300  
**Tags:** greedy, math  
**Solve time:** 4m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of blocks, each painted either black or white. The only allowed move is to pick two neighboring blocks and flip both of them at the same time, turning white into black and black into white.

The task is not to optimize the number of moves, but to decide whether we can make the entire row uniform, all blocks the same color, and if yes, output a valid sequence of operations with length at most three times the number of blocks.

Each operation only affects two adjacent positions, so any strategy must propagate changes locally. The central difficulty is that flipping a pair changes parity-like structure in a constrained way, so not every configuration can be fixed.

The constraint n ≤ 200 means we can afford O(n^2) or even O(n^3) constructions of operations. We are not forced into greedy-only thinking for speed, but we must keep the output bounded by O(n).

A key edge case appears when the number of black and white blocks both interact in a way that prevents global alignment. For example, if all blocks are identical, no moves are needed. If the string is alternating like "BWBW", brute forcing local flips can easily cycle without progress unless we enforce a systematic direction.

Another subtle case is when the last few mismatches remain isolated. Because operations always affect pairs, leaving a single “wrong parity” position at the end cannot be repaired unless earlier structure was handled correctly.

## Approaches

A brute force perspective would try to simulate sequences of adjacent flips and search for a transformation that yields all equal colors. Since each operation modifies two positions, each state has up to n−1 moves, and depth up to 3n, the naive search space grows exponentially and is infeasible even for n = 200.

The key observation is that we
