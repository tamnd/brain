---
title: "CF 1324A - Yet Another Tetris Problem"
description: "We are given a Tetris-like field represented as a row of columns, each with some initial height. The columns are described by an array of integers where the $i$-th value represents the number of blocks stacked in that column."
date: "2026-06-11T16:43:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1324
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 627 (Div. 3)"
rating: 900
weight: 1324
solve_time_s: 182
verified: false
draft: false
---

[CF 1324A - Yet Another Tetris Problem](https://codeforces.com/problemset/problem/1324/A)

**Rating:** 900  
**Tags:** implementation, number theory  
**Solve time:** 3m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a Tetris-like field represented as a row of columns, each with some initial height. The columns are described by an array of integers where the $i$-th value represents the number of blocks stacked in that column. We are allowed to place vertical 2×1 pieces on top of any column. After placing a piece, every column with at least one block is reduced by one block simultaneously, simulating a "row clearing" step. The task is to determine whether it is possible to repeatedly place these pieces so that all columns eventually reach height zero.

Each test case provides the number of columns and their heights. The output for each test case is "YES" if we can clear all columns and "NO" otherwise.

The constraints are small: the number of columns $n$ is at most 100, each height $a_i$ is at most 100, and the number of test cases $t$ is at most 100. These limits imply that any solution with complexity around $O(n)$ per test case will run comfortably within the time limit. A naive simulation is feasible in principle, but we can reason about the problem mathematically instead of simulating every placement.

Edge cases occur when a column has height 1, or when all columns are initially equal and even. For instance, a single column with height 100 can always be reduced by repeatedly adding 2 and applying the row-clearing step. However, a pattern like [1, 1, 2, 1] cannot be cleared because there is no way to balance the placement of pieces such that the clearing step reduces all heights to zero simultaneously.

## Approaches

The brute-force approach would simulate the process step by step: place a 2×1 figure on some column, then decrement all positive columns until at least one column hits zero, repeat until all are zero or no valid moves remain. This approach is correct because it directly follows the problem rules. In the worst case, the total number of operations could be $O(n \cdot \max(a_i))$ per test case, which is $O(100 \cdot 100) = 10^4$ operations per test case, acceptable for $t=100$. However, simulating placement choices for each column can get tricky and unnecessarily complex.

The key insight is to consider the heights modulo 2. Each vertical piece increases a column by 2, which does not change its parit
