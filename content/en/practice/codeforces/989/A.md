---
title: "CF 989A - A Blend of Springtime"
description: "We are given a short string representing a row of cells. Each cell is either empty or contains exactly one flower of one of three types, encoded as the letters A, B, and C."
date: "2026-06-17T00:43:16+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 989
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 487 (Div. 2)"
rating: 900
weight: 989
solve_time_s: 76
verified: true
draft: false
---

[CF 989A - A Blend of Springtime](https://codeforces.com/problemset/problem/989/A)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short string representing a row of cells. Each cell is either empty or contains exactly one flower of one of three types, encoded as the letters A, B, and C. When a flower “dies”, it disappears from its own cell and spreads its color to its immediate left and right neighbors. If a neighbor is outside the string, that spread is ignored. Multiple flowers can die in any order, and their effects accumulate.

The question is whether there exists some sequence of deaths such that at some moment, at least one cell contains all three colors simultaneously. A cell can accumulate colors coming from different flowers; we only care whether all three distinct colors can be present in the same position after some combination of spreads.

The string length is at most 100, so any solution that checks all relevant local configurations or simulates small combinations is easily fast enough. A brute force over all subsets of flowers would already be tiny, since there are at most 100 positions, but even that is unnecessary. The structure of the propagation makes the problem fundamentally local.

A subtle edge case is when all three colors exist but are too far apart to ever meet in a single cell. For example, if all A flowers are isolated on the far left and B and C are on the far right, the spreads never create a triple overlap. Another edge case is when one of the colors is missing entirely, for example "A.B.A", where no matter how we trigger deaths, we can never produce all three colors.

## Approaches

The brute-force viewpoint is to consider every subset of flowers as the set that “dies”, compute the resulting spread pattern, and check whether any cell accumulates A, B, and C. For a fixed subset, each death contributes at most two neighboring updates, so simulating one subset costs O(n). There are 2^n subsets, so this becomes O(n 2^n), which is completely infeasible even for n = 100.

The key observation is that we do not actually need to simulate dynamics or ordering. A cell ends up containing a color if and only if either it originally contains that flower or it is adjacent to at least one flower of that color that eventually dies. Since we are allowed to choose which flowers die, what matters is whether there exist positions that can collectively contribute all three colors into a single target cell.

Fix a cell i as the potential meeting point. For each color, we only care whether there exists at least one occurrence of that color in positions i − 1, i, or i + 1. If a flower of that color exists anywhere in this neighborhood, we can force it to die and deposit that color into i. If no such flower exists, that color can never appear in i under any sequence of operations. Therefore, the problem reduces to checking whether some position i has all three colors present in its closed neighborhood.

This reduces the entire dynamic process into a constant-size sliding window check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan every position of the string and treat it as a candidate cell where all three colors might meet.

1. For each index i in the string, we inspect the substring formed by positions i − 1, i, and i + 1, ignoring indices outside the array boundaries. This captures all possible sources that could directly contribute to i.
2. We track which of A, B, and C appear in this local neighborhood. Each character contributes its own color immediately, and any present flower can also later be forced to die to contribute its color to i.
3. If all three colors appear in this neighborhood, we immediately conclude that i can be made into a full blend and return success.
4. If we finish checking all positions without finding such a neighborhood, we conclude it is impossible.

The logic depends on the fact that any color absent from the radius-1 neighborhood cannot reach the center cell at all, because only adjacent cells can contribute petals.

### Why it works

For any fixed cell i, the only way a color can appear in i is either that the flower is already at i or that it is at i − 1 or i + 1 and is chosen to die. Flowers farther away can never contribute directly to i, since propagation only reaches immediate neighbors. Therefore, the set of colors that can possibly appear in i is exactly the union of colors present in the interval [i − 1, i + 1]. If this union contains A, B, and C, we can schedule deaths of the corresponding flowers to ensure all three contribute to i. If not, at least one color is unreachable for that cell in every possible sequence, so no valid construction exists.

## Python Solution

```
import
```
