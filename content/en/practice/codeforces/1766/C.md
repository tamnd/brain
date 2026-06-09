---
title: "CF 1766C - Hamiltonian Wall"
description: "We are given a grid with two rows and m columns representing a wall. Each cell is either black (B) or white (W). Monocarp wants to paint all black cells exactly once in a single continuous path that moves only between adjacent cells."
date: "2026-06-09T12:57:42+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1766
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 139 (Rated for Div. 2)"
rating: 1300
weight: 1766
solve_time_s: 168
verified: false
draft: false
---

[CF 1766C - Hamiltonian Wall](https://codeforces.com/problemset/problem/1766/C)

**Rating:** 1300  
**Tags:** dp, implementation  
**Solve time:** 2m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid with two rows and `m` columns representing a wall. Each cell is either black (`B`) or white (`W`). Monocarp wants to paint all black cells exactly once in a single continuous path that moves only between adjacent cells. Every column contains at least one black cell, so it is impossible to have a column without a black cell. The question asks whether such a Hamiltonian path exists for each test case.

The input guarantees that every column has at least one black cell, so the problem is non-trivial only in how the black cells are connected. Since there are only two rows, each column can have one or two black cells. The Hamiltonian path must traverse all black cells, visiting each exactly once and never entering a white cell. This effectively reduces to checking whether the black cells form a connected "snake" without needing to backtrack or jump over white cells.

The constraints are tight in terms of the number of test cases and column sum: `t` can reach 10^4, and the sum of all `m` across tests is ≤ 2 × 10^5. This rules out any solution that is quadratic in `m` per test case; we need a linear scan of the grid per test case.

A non-obvious edge case arises when black cells in adjacent columns are not aligned in a way that allows a continuous path. For example, if column `j` has a black cell only in the top row and column `j+1` has a black cell only in the bottom row, a valid path must "drop" from the top to bottom between columns. If such a drop occurs more than once or is blocked by white cells, it may become impossible to cover all black cells without violating adjacency or visiting a white cell.

## Approaches

A naive approach is to try every starting black cell and perform a DFS to see if a Hamiltonian path exists. This approach is correct but too slow because the number of recursive paths grows exponentially with `m`. Each test case could require O(2^m) checks in the worst case, which is infeasible given the constraints.

The optimal approach leverages the structure of the grid. Because there are only two rows, a valid Hamiltonian path must follow a zig-zag pattern along the columns, moving between rows only when necessary. We can define the "start" column as the leftmost black cell in the topmost row that contains a black cell. Then, we scan column by column, trying to follow the black cells while switching rows if necessary. If we can move from column to column without encountering a column where the black cells prevent adjacency, then a path exists. Otherwise, it does not.

The key insight is that in a 2-row grid with the "at least one black per column" guarantee, the path can always be built greedily from the leftmost black cell, switching rows whenever needed, unless there is a "hole" in the black cells that forces a jump over a white cell, which violates the rules.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (DFS all paths) | O(2^m) | O(m) | Too slow |
| Greedy zig-zag scan | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the leftmost column containing a black cell. If
