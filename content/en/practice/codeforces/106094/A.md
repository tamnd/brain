---
title: "CF 106094A - Matrix Bel Lotus"
description: "The problem gives a 5 by 5 grid containing exactly one cell with the value 1 and all other cells containing 0. A move consists of swapping two neighboring rows or swapping two neighboring columns."
date: "2026-06-25T12:02:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106094
codeforces_index: "A"
codeforces_contest_name: "SVU-HIAST CPC 2025"
rating: 0
weight: 106094
solve_time_s: 34
verified: false
draft: false
---

[CF 106094A - Matrix Bel Lotus](https://codeforces.com/problemset/problem/106094/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

The problem gives a 5 by 5 grid containing exactly one cell with the value `1` and all other cells containing `0`. A move consists of swapping two neighboring rows or swapping two neighboring columns. The goal is to move the `1` into the center cell of the grid, which is the position at row 3 and column 3 using one-based indexing. We need the minimum number of swaps required.

The key detail is that row swaps only change the row position of the `1`, and column swaps only change the column position of the `1`. The two movements are independent. If the `1` is currently in row `r`, it needs exactly `|r - 3|` row swaps to reach the middle row. Similarly, if it is in column `c`, it needs exactly `|c - 3|` column swaps to reach the middle column.

The input size is fixed, the matrix is always 5 by 5, so the entire input contains only 25 values. This means even a full scan of the matrix is trivial. We do not need advanced data structures or optimizations. Any solution that processes every cell once is easily within the limits. Even a solution that performs a small constant amount of work per cell will finish instantly.

The main edge cases come from the position of the `1` and from assuming that the answer requires simulating swaps. The first case is when the matrix is already centered.

For example:

```
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0
```

The output is:

```
0
```

A careless implementation might perform unnecessary moves because it only checks whether the value exists, not whether it is already in the target position.

Another edge case is when the `1` is at a corner.

Example:

```
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The output is:

```
4
```

The `1` must move two rows down and two columns right. If we only count row moves or only count column moves, the answer would be incomplete.

A final common mistake is mixing zero-based and one-based coordinates. With zero-based indexing the target is `(2, 2)`, while with one-based indexing it is `(3, 3)`. Using the wrong target shifts every answer by one.

## Approaches

The most direct approach is to simulate the swaps. We could locate the `1`, then repeatedly swap it with the adjacent row or column that moves it closer to the center. This would work because every swap changes the position of the `1` by exactly one step in one direction, and moving directly toward the target is always optimal.

However, simulation is unnecessary. Since the grid is tiny, the more useful observation is that the number of required moves depends only on the distance from the current position to the center. If the `1` is three rows away and two columns away, no sequence of swaps can do better than five moves because each move changes only one coordinate by one.

The brute-force simulation would still be fast here, but the same idea would become inefficient on larger grids. A general simulation approach spends time performing operations that do not reveal new information. The position of the `1` already tells us the answer.

The optimal solution is to scan the matrix, find the coordinates of the `1`, and compute the Manhattan distance to the center. Manhattan distance works because the allowed operations are exactly vertical and horizontal unit moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Accepted, but unnecessary |
| Optimal | O(25) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all 25 cells of the matrix and find the row and column where the value `1` appears. The entire problem is determined by this single position.
2. Compute the row distance from the current row to the middle row. Using zero-based indexing, the middle row is index `2`, so this distance is `abs(row - 2)`.
3. Compute the column distance from the current column to the middle column. The middle column is also index `2`, so this distance is `abs(col - 2)`.
4. Add the two distances and print the result. Each required row move and column move contributes exactly one operation, so their sum is the minimum number of operations.

Why it works:

Every valid move changes exactly one coordinate of the `1` by one. To reach the center, the row coordinate must change from its current value to `2`, requiring `abs(row - 2)` moves. The same reasoning applies to the column. Since row and column operations do not interfere with each other, performing all required row moves and column moves reaches the center in exactly the computed number of operations. No smaller number is possible because every move can reduce the total distance by at most one.
