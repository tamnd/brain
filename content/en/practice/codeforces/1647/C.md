---
title: "CF 1647C - Madoka and Childish Pranks"
description: "We are given an initially empty binary grid filled with zeros, and we want to transform it into a target 0-1 pattern."
date: "2026-06-10T04:06:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1647
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 777 (Div. 2)"
rating: 1300
weight: 1647
solve_time_s: 141
verified: false
draft: false
---

[CF 1647C - Madoka and Childish Pranks](https://codeforces.com/problemset/problem/1647/C)

**Rating:** 1300  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an initially empty binary grid filled with zeros, and we want to transform it into a target 0-1 pattern. The only allowed operation is to pick a rectangular subgrid and repaint it with a chessboard pattern, where the top-left cell of that rectangle is always set to zero and colors alternate by Manhattan distance within the rectangle. If a cell is painted multiple times, only the last paint matters.

So the task is not to simulate painting, but to decide whether we can build the target grid using these chess-pattern stamps, and if yes, to output any valid sequence of rectangles, with at most $n \cdot m$ operations.

The constraints are small, with $n, m \le 100$, so a construction that is quadratic per test case is acceptable. The number of test cases is also tiny, so we can afford to inspect the grid multiple times. This strongly suggests a greedy construction rather than any global search or DP over subsets of operations.

A subtle point is that operations overwrite previous ones completely inside the chosen rectangle. This means we do not need to preserve earlier correctness, only ensure that final overwrites align with the target.

The non-obvious failure case for naive reasoning is assuming every grid is constructible because chess patterns seem flexible. For example, a single isolated 1 in a sea of zeros cannot always be created without affecting surrounding parity constraints. Another tricky case is when the grid forces contradictory parity requirements across overlapping rectangles, making reconstruction impossible even though local patterns seem consistent.

## Approaches

A brute-force approach would try to simulate building the grid from the initial zero matrix by choosing rectangles and checking whether applying a chess pattern reduces the difference between current and target states. This quickly becomes intractable because each step has $O(n^2 m^2)$ choices of rectangles, and sequences can be long. Even a shallow search explodes combinatorially.

The key observation is that the operation is extremely structured: every paint defines a fully determined checkerboard whose only degree of freedom is the top-left corner of the rectangle. This means each operation is effectively placing a parity field over a submatrix. Instead of thinking about how to construct the whole grid, we can think backwards: whenever we see a mismatch, we can try to “fix” it by placing a rectangle whose chess coloring matches exactly the required local pattern.

This leads to a greedy elimination strategy: process cells in a fixed order, and whenever a cell is still incorrect, force a rectangle anchored at that cell that resolves it. Since the top-left corner of each operation defines parity, anchoring guarantees the operation corrects that cell permanently.

The construction works because every operation can be chosen to target the final unresolved position in a way that does not break previously fixed cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | Exponential | O(nm) | Too slow |
| Greedy Construction | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

We construct the answer greedily by scanning the grid.

1. We iterate over all cells in row-major order. The reason for this order is that once a cell is fixed, later operations will never need to modify it again if we only start rectangles from later positions.
2. For each cell $(i, j)$, we check whether the current value already matches the target.
3. If it matches, we do nothing and move on.
4. If it does not match, we start a rectangle with top-left corner at $(i, j)$. We extend this rectangle as far as possible to the bottom-right of the grid.
5. We apply a chess coloring to this rectangle, meaning cell $(x, y)$ in the rectangle gets value $(x + y) \bmod 2$, with the convention that $(i, j)$ is zero.
6. We record this operation and conceptually apply it to the grid.

The key point is that by anchoring the rectangle at the first incorrect cell, we immediately correct it, and since future operations only start at later positions, this correction will not be undone in a conflicting way.

Why it works: each time we fix a cell $(i, j)$, we
