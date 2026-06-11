---
title: "CF 1150B - Tiling Challenge"
description: "We are given an $n times n$ square board, where some cells are occupied and others are free. The goal is to completely tile the free cells using identical pentomino pieces shaped like a cross: a center square with four adjacent squares, one in each cardinal direction."
date: "2026-06-12T03:05:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1150
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 556 (Div. 2)"
rating: 900
weight: 1150
solve_time_s: 93
verified: true
draft: false
---

[CF 1150B - Tiling Challenge](https://codeforces.com/problemset/problem/1150/B)

**Rating:** 900  
**Tags:** greedy, implementation  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ square board, where some cells are occupied and others are free. The goal is to completely tile the free cells using identical pentomino pieces shaped like a cross: a center square with four adjacent squares, one in each cardinal direction. Each piece must cover exactly five distinct cells, cannot overlap occupied cells or other pieces, and cannot extend outside the board boundaries. The output is YES if such a tiling is possible and NO otherwise.

The board size $n$ ranges from 3 to 50. Since each piece occupies 5 cells, the total number of free cells must be divisible by 5 for a complete tiling. Even though $n$ is small, an algorithm that tries every possible combination of placements would be inefficient, as the number of subsets of free cells grows exponentially. Therefore, the solution should exploit the structure of the pentomino shape rather than trying all combinations.

Edge cases that a naive approach could fail include boards with scattered occupied cells blocking potential placements. For example, a 3×3 board with the corners filled:

```
#.#
...
#.#
```

This board is tilable because the center can host a single pentomino covering the four edge cells adjacent to it. A naive row-by-row greedy placement might incorrectly reject this configuration.

Another subtle edge case is a nearly full board with only isolated free cells that cannot form a cross; here the algorithm must correctly detect that no tiling is possible.

## Approaches

A brute-force approach would attempt to place a pentomino on every possible center cell and recursively cover remaining free cells. For an $n \times n$ board, there are roughly $O(n^2)$ center candidates, and each recursive call would branch up to 1, leading to an exponential number of configurations. This is clearly too slow for $n = 50$.

The key insight is that the pentomino always occupies a 3×3 region with the center being the middle cell. If we iterate over the board from top-left to bottom-right and greedily place a piece wherever its center can fit, we either cover the free cells immediately or detect a configuration where a cell cannot be part of any cross. Because each pentomino requires its center and four adjacent cells to be free, a left-to-right, top-to-bottom traversal ensures that when a free cell is reached, it either can serve as the center of a new cross or must already have been covered by a previously placed piece. This strategy exploits the board's grid structure and the cross-shaped pentomino's locality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n^2)) | O(n^2) | Too slow |
| Greedy scan & place | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the board size $n$ and the $n \times n$ grid representation, marking free cells as "." and occupied as "#".
2. Iterate over each cell starting from row 1 to $n-2$ and column 1 to $n-2$, treating each cell as a potential center of a pentomino.
3. For each candidate center cell, check if it and the four adjacent cells (up, down, left, right) are all free. If so, place a pentomino by marking these five cells as occupied.
4. Continue the iteration until all possible center positions have been considered.
5. After completing the scan, check if any free cells remain. If there are, output NO; otherwise, output YES.

Why it works: The greedy traversal guarantees that any free cell that can serve as a center will be used. Since the cross only extends one cell in each direction, no previously placed piece will prevent a valid placement if it is possible. Any remaining free cell after the traversal cannot be part of any pentomino and thus tiling is impossible. The invariant is that each free cell is either covered or considered for coverage exactly once.

## Python Solution

```
PythonRun
```
