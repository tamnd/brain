---
title: "CF 1519B - The Cake Is a Lie"
description: "We are given a rectangular grid with n rows and m columns. You start at the top-left corner (1, 1) and want to reach the bottom-right corner (n, m) by only moving right or down. Moving right from cell (x, y) costs x burles, moving down costs y burles."
date: "2026-06-10T18:10:33+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1519
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 108 (Rated for Div. 2)"
rating: 800
weight: 1519
solve_time_s: 62
verified: false
draft: false
---

[CF 1519B - The Cake Is a Lie](https://codeforces.com/problemset/problem/1519/B)

**Rating:** 800  
**Tags:** dp, math  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid with `n` rows and `m` columns. You start at the top-left corner `(1, 1)` and want to reach the bottom-right corner `(n, m)` by only moving right or down. Moving right from cell `(x, y)` costs `x` burles, moving down costs `y` burles. The question asks whether it is possible to reach the target spending exactly `k` burles.

The input provides several test cases, each specifying `n`, `m`, and `k`. The output is simply "YES" if exactly `k` burles can be spent and "NO" otherwise.

Constraints are small: both `n` and `m` are up to 100, and `k` is up to 10,000. This rules out brute-force path enumeration for larger grids, because the number of paths grows combinatorially: there are `(n+m-2 choose n-1)` possible paths. For `n = m = 100`, that is around 10^58 paths, clearly infeasible.

Subtle edge cases include single-row or single-column grids. For example, `n=1, m=4` has only one path, moving right three times. The total cost is 1 + 1 + 1 = 3. If you miscompute the cost formula, you might get it wrong. Another edge case is `n=1, m=1` where you are already at the destination and the cost is 0. Failing to handle this case leads to incorrect answers.

## Approaches

The brute-force approach is to enumerate all paths, compute the cost for each, and check whether any path sums to `k`. This works correctly because it literally checks every possibility. But the number of paths is exponential in `n+m`, which becomes infeasible even for `n=m=20`. Roughly, the number of operations is `O(2^(n+m))`, clearly too large for `n, m = 100`.

The key insight is to realize that the cost along any path is deterministic once you decide the order of moves. If you always go right until you reach the last column, then move down, the total cost is easy to compute. Similarly, if you always go down first and then right, you get the same total formula structure. Every path spends `(sum of all row indices for right moves) + (sum of all column indices for down moves)`.

Formally, there are exactly `n-1` down moves and `m-1` right moves. The sum of the row indices for right moves is `(n-1) * 1 + (n-1) * 2 + ...` but since every right move is in some row, the row index contribution is `(m-1) * sum of row indices from 1 to n-1)`. After careful checking, the pattern simplifies: the total cost to go from `(1,1)` to `(n,m)` is always `(n-1)*m + (m-1)*n = n*m - 1`.

This formula holds for every grid because you move `n-1` times down and `m-1` times right. Each right move costs the row index (from 1 to n) and is done `m-1` times across the rows, while each down move costs the column index (from 1 to m) and is done `n-1` times across the columns. Summing and simplifying gives `n*m - 1`. Once you have this formula, the problem reduces to a single comparison: check if `k == n*m - 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n+m)) | O(1) | Too slow |
| Formula Check | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. Loop over each test case. Read `n`, `m`, and `k`.
3. Compute the target cost using the formula `total_cost = n * m - 1`.
4. Compare `total_cost` with `k`. If equal, print "Y_
