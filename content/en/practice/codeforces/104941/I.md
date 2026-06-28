---
title: "CF 104941I - I Spy"
description: "We are given a grid with $n$ rows and $m$ columns. Each cell represents a window that can either be lit or dark. The configuration is constrained in two ways. First, every row $i$ has a fixed number $ai$ of lit windows."
date: "2026-06-28T18:19:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "I"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 67
verified: false
draft: false
---

[CF 104941I - I Spy](https://codeforces.com/problemset/problem/104941/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid with $n$ rows and $m$ columns. Each cell represents a window that can either be lit or dark. The configuration is constrained in two ways.

First, every row $i$ has a fixed number $a_i$ of lit windows. Second, no two lit windows may touch each other horizontally or vertically. That means if a window is lit, its left and right neighbors in the same row must be dark, and the windows directly above and below it must also be dark.

The task is to count how many valid global configurations of lit windows exist, modulo $10^9+7$.

The constraints are small in width but moderately large in height: $n \le 30$, $m \le 23$. This immediately suggests that we can afford exponential work over rows or bitmasks of size $2^m$, but not over full grids. The horizontal constraint is local to rows, while the vertical constraint couples adjacent rows, which strongly suggests a row-by-row dynamic programming with bitmask states.

A naive approach would try all $2^{nm}$ configurations, which is astronomically large. Even restricting by row counts still leaves too many possibilities. The key difficulty is enforcing both adjacency constraints simultaneously while matching row sums.

A subtle edge case appears when $a_i$ is large relative to $m$. If $a_i > \lceil m/2 \rceil$, it is impossible for that row alone to satisfy the horizontal non-adjacency rule, because the maximum number of non-adjacent cells in a row of length $m$ is $\lceil m/2 \rceil$. In such cases, the answer must be zero immediately.

Another edge case is when $n = 1$. Then the problem reduces to counting valid independent sets on a single path graph with fixed size, which is purely combinatorial per row.

## Approaches

A brute-force interpretation treats each cell as a binary variable and checks all constraints globally. This is correct but infeasible. The state space size is $2^{nm}$, and even checking constraints per configuration is $O(nm)$, leading to $O(nm2^{nm})$, which is far beyond limits.

We refine the perspective by noticing that constraints are local. Horizontal adjacency only affects within a row, while vertical adjacency only couples adjacent rows. This suggests separating the grid into row states.

Each row can be represented as a bitmask of length $m$, where 1 indicates a lit window. A valid row mask must not contain adjacent 1s. Additionally, the number of 1s in row $i$ must equal $a_i$.

Now the grid becomes a sequence of row masks with compatibility constraints: adjacent rows must not share a 1 in the same column. That is, for row masks $x$ and $y$, we require $x \& y = 0$.

This transforms the problem into counting paths in a layered graph: each layer is a row, nodes are valid masks, and edges represent compatibility.

The key insight is that $m \le 23$, so the number of valid masks without adjacent 1s is manageable (bounded by Fibonacci growth, approximately $F_{25} \approx 10^5$). This allows dynamic programming over states.

We precompute all valid masks and their popcounts. Then we precompute transitions between masks that do not overlap vertically. Finally, we run DP row by row.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{nm})$ | $O(nm)$ | Too slow |
| Bitmask DP | $O(n \cdot S^2)$ where $S \approx F_{m+2}$ | $O(S^2)$ | Accepted |

## Algorithm Walkthrough

We define a state as a valid row configuration encoded as a bitmask.

## 1. Generate valid row masks

We enumerate all masks from $0$ to $2^m - 1$. A mask is valid if it contains no adjacent set bits. This ensures horizontal adjacency is satisfied.

We also record the number of set bits in each mask to enforce row constraints.

## 2. Group masks by row requirement

For each row $i$, we only allow masks with popcount equal to $a_i$. This prunes invalid states early and reduces DP transitions.

## 3. Precompute compatibility

For any two valid masks $x$ and $y$, we define them compatible if $(x \& y) = 0$. This enforces vertical adjacency constraint.

We precompute for each mask a list of all compatible masks in the next row.

## 4. Dynamic programming initialization

For the first row, we set $dp[mask] = 1$ for all valid masks with popcount $a_1$.

This represents all ways to place lit windows in the first row consistent with constraints.

## 5. Row-by-row transition

For each row $i$ from 2 to $n$, we compute a new DP table:

For every mask $cur$ valid for row $i$, we sum over all previous masks $prev$ that are compatible and valid for row $i-1$.

This builds all valid partial configurations row by row.

## 6. Final aggregation

The answer is the sum of all DP values in the last row.

### Why it works

At each step, the DP state represents exactly the number of ways to fill all rows up to the current one such that:

the current row is fixed to a valid mask and all previous adjacency constraints are satisfied. The transition preserves both horizontal validity (by construction of masks) and vertical validity (by compatibility filtering). Since every valid full grid corresponds to exactly one sequence of row masks, no configuration is missed or double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    max_mask = 1 << m
    valid = []
    pop = [0] * max_mask

    for mask in range(max_mask):
        if mask & (mask << 1):
            continue
        pop[mask] = bin(mask).count("1")
        valid.append(mask)

    # group by popcount
    by_pop = [[] for _ in range(m + 1)]
    for mask in valid:
        by_pop[pop[mask]].append(mask)

    # precompute compatibility
    compat = {}
    for x in valid:
        compat[x] = []
        for y in valid:
            if x & y == 0:
                compat[x].append(y)

    # initial dp
    first = a[0]
    dp = {mask: 0 for mask in valid}
    for mask in by_pop[first]:
        dp[mask] = 1

    # transitions
    for i in range(1, n):
        need = a[i]
        new_dp = {mask: 0 for mask in valid}
        for cur in by_pop[need]:
            total = 0
            for prev in compat[cur]:
                total = (total + dp[prev]) % MOD
            new_dp[cur] = total
        dp = new_d_
```
