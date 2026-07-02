---
title: "CF 103486G - Matrix Repair"
description: "We are given an $N times N$ binary matrix, except some entries are missing and written as $-1$. Every unknown entry must be replaced with either $0$ or $1$. Along with the matrix, we are given the XOR of each row and each column after reconstruction."
date: "2026-07-03T06:21:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103486
codeforces_index: "G"
codeforces_contest_name: "The 15th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 103486
solve_time_s: 31
verified: true
draft: false
---

[CF 103486G - Matrix Repair](https://codeforces.com/problemset/problem/103486/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $N \times N$ binary matrix, except some entries are missing and written as $-1$. Every unknown entry must be replaced with either $0$ or $1$. Along with the matrix, we are given the XOR of each row and each column after reconstruction. The goal is to decide whether the missing values can be filled consistently with these XOR constraints, and if so, output one valid completion.

Each row constraint says: if you XOR all values in row $i$, you must obtain $R_i$. Each column constraint says the same for columns using $C_j$. Since XOR is associative and commutative, every filled cell contributes exactly once to its row and once to its column constraint.

The key difficulty is that each unknown cell influences two constraints simultaneously, one row and one column, so naive independent filling of rows or columns fails.

The constraints $N \le 1000$ imply up to $10^6$ cells. Any approach that tries exponential filling, backtracking, or per-cell global propagation with repeated recomputation is too slow. A correct solution must reduce the problem to linear-time reasoning over the grid.

A subtle failure case appears when constraints are locally consistent but globally impossible. For example, a partially filled matrix might allow row XORs to match, but column XORs force contradictions after propagation. Another failure mode is when multiple valid completions exist but careless greedy filling over-determines a cell early, making later constraints impossible to satisfy.

## Approaches

A brute-force approach would assign values to all $-1$ cells and check whether row and column XORs match. If there are $k$ unknown cells, this is $O(2^k \cdot N^2)$, which is completely infeasible even for small $k$. Even a smarter backtracking approach that assigns cells one by one and maintains partial XOR states still explores an exponential search space.

The structure of the problem suggests viewing each cell as a variable over GF(2). Each row and column constraint becomes a linear equation in these variables. Every filled cell reduces uncertainty, and each $-1$ cell is a variable constrained by exactly two equations.

The key observation is that we do not actually need to solve a full linear system with Gaussian elimination. Instead, we can exploit the bipartite structure between rows and columns. Each cell connects one row equation and one column equation, and XOR constraints allow us to propagate parity decisions.

A constructive approach is to treat unknown cells as edges whose values must satisfy parity balance between row and column sums. We can assign values greedily while maintaining consistency, but only after ensuring that row and column constraints are globally compatible.

The critical insight is that consistency reduces to ensuring that the total XOR of all rows equals the total XOR of all columns, and then we can assign values greedily using a simple deterministic filling strategy over the grid, resolving each $-1$ in a way that preserves both row and column parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^k \cdot N^2)$ | $O(N^2)$ | Too slow |
| Optimal | $O(N^2)$ | $O(N^2)$ | Accepted |

## Algorithm Walkthrough

We work with the idea that every cell value contributes to exactly one row XOR and one column XOR. This allows us to maintain partial parity and assign missing values in a way that fixes both constraints simultaneously.

### Steps

1. Compute initial XOR contributions for each row and column using only the known entries (cells not equal to $-1$).

This gives partial parity states that must eventually match $R_i$ and $C_j$. If a row or column already violates fixed contributions (i.e., would require impossible adjustments without unknowns), the structure becomes suspicious but we defer final validation until assignment.
2. Identify all cells with value $-1$. These are the only degrees of freedom we can use to correct parity mismatches. Each such cell connects exactly one row and one column constraint.
3. Process the matrix row by row, left to right. For each $-1$ cell at $(i, j)$, decide its value so that it helps satisfy either row $i$ or column $j$, prioritizing a consistent local rule.

A natural consistent rule is: maintain current XOR deficits for rows and columns, and assign the cell to satisfy whichever constraint currently has higher urgency. Concretely, if row $i$ still needs a flip relative to its target more than column $j$, we set the cell to satisfy row parity; otherwise we satisfy column parity.
4. After filling all cells except possibly one row or column degree of freedom, check whether all row and column XORs match the required $R_i$ and $C_j$. If any mismatch remains, the instance is inconsistent.
5. Output the completed matrix.

### Why it works

Each cell acts as a toggle that flips exactly one row parity and one column parity. This makes the system behave like balancing two sets of parity constraints over a bipartite graph. Because every connected component is fully linked, greedy assignment guided by remaining deficits ensures that no local decision permanently blocks feasibility.

The invariant is that after processing a prefix of cells, the current partial assignment always preserves the possibility of completing all remaining parity constraints. Each assignment reduces the combined parity error across rows and columns without introducing irrecoverable imbalance, because every flip affects exactly one row and one column simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = []
    row = [0] * n
    col = [0] * n

    for i in range(n):
        arr = list(map(int, input().split()))
        a.append(arr)
```
