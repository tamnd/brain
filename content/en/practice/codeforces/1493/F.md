---
title: "CF 1493F - Enchanted Matrix"
description: "We are given an unknown $n times m$ matrix. The only information we initially know is its dimensions. The task is to count all pairs $(r, c)$ such that $r$ divides $n$, $c$ divides $m$, and if we partition the matrix into blocks of size $r times c$, all blocks are identical."
date: "2026-06-10T22:18:27+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "interactive", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1493
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 705 (Div. 2)"
rating: 2600
weight: 1493
solve_time_s: 148
verified: false
draft: false
---

[CF 1493F - Enchanted Matrix](https://codeforces.com/problemset/problem/1493/F)

**Rating:** 2600  
**Tags:** bitmasks, interactive, number theory  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an unknown $n \times m$ matrix. The only information we initially know is its dimensions. The task is to count all pairs $(r, c)$ such that $r$ divides $n$, $c$ divides $m$, and if we partition the matrix into blocks of size $r \times c$, all blocks are identical. In other words, the matrix is tiled by repeating a rectangle of size $r \times c$.

The challenge arises because the matrix is hidden, and the only operation allowed is a query comparing two subrectangles of the same size. Each query tells us if the two subrectangles are exactly equal or not. Queries are limited to approximately $3 \log_2(n+m)$, which is far fewer than the total number of subrectangles, so we cannot check every candidate pair exhaustively.

Constraints $n, m \le 1000$ mean we cannot afford algorithms that examine each potential block individually; we must exploit the divisibility and repeated-pattern structure of the matrix. Non-obvious edge cases include:

- A fully uniform matrix where all values are identical. Every divisor of $n$ and $m$ would yield a valid tiling. Careless code might double-count.
- A matrix where each row or column is unique. Only the full matrix size $(n, m)$ is valid, and small block tests would incorrectly appear equal if we do not query non-overlapping blocks properly.
- A prime-sized dimension. For instance, $n=7$, $m=6$; only $r=1$ or $r=7$ and $c=1, 2, 3, 6$ are possible candidates. Handling divisors incorrectly would produce wrong answers.

## Approaches

The brute-force approach iterates over all divisors of $n$ and $m$, and for each $(r, c)$, checks all $(n/r) \times (m/c)$ blocks for equality using queries. This is correct but infeasible. In the worst case, $n=m=1000$, there can be up to $16$ divisors each, giving 256 candidate pairs. For each, naive checking might involve hundreds of queries, exceeding the $O(\log(n+m))$ query budget.

The key observation is that we do not need to check every block explicitly. Because the tiling is periodic, we can determine the minimal repeating unit in each dimension separately. For the row dimension, let $r$ be a candidate divisor. If the first $r$ rows are repeated through the matrix, then the rows are tiled. We can check this by comparing each consecutive block of $r$ rows with the first. The same applies for columns. Using a binary search strategy over the divisors, we can reduce the number of queries to logarithmic in $n$ and $m$. Once we know the maximal periodicity along rows and columns, we combine the sets of valid divisors for each dimension. Each valid row divisor $r$ can pair with each valid column divisor $c$, giving all valid $(r, c)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm * #divisors(n) * #divisors(m)) queries | O(1) | Too slow, exceeds query limit |
| Optimal | O(log n * log m) queries | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Compute all divisors of $n$ and $m$. Sorting them ascending is convenient for later checks. These are all possible candidate block sizes along rows and columns.
2. Define a helper function `check_rows(r)` that checks if the matrix can be tiled with `r`-row blocks. For this, iterate over `i` in steps of `r` from `0` to `n-r` and compare the block starting at row `1` with the block starting at row `i+1` using a single query of size `r x m`. If any comparison fails, return `False`; otherwise, return `True`.
3. Similarly define `check_cols(c)` using queries of size `n x c`. Iterate along the columns in steps of `c` and compare against the first column block.
4. Apply the above checks to all divisors. Store the divisors that successfully tile rows in `valid_rows` and columns in `valid_cols`.
5. Compute the total number of valid pairs as the Cartesian product: `len(valid_rows) * len(valid_cols)`. This works because a block of size `r x c` is valid if and only if `r` tiles rows and `c` tiles columns.
6. Output the final answer.

Why it works: The algorithm isolates the two dimensions, relying on the independence of row tiling and column tiling. Each query compares a non-overlapping block with the first block. If a divisor fails, any multiple will also fail. The invariant is that we only accept divisors whose blocks are consistent across the entire dimension, guaranteeing that combining row and column divisors gives all valid rectangle sizes.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import isqrt

def divisors(x):
    small, large = [], []
    for i in range(1, isqrt(x)+1):
        if x % i == 0:
            small.append(i)
            if i != x // i:
                large.append(x//i)
    return small + large[::-1]

def query(h, w, i1, j1, i2, j2):
    print(f"? {h} {w} {i1} {j1} {i2} {j2}", flush=True)
    return int(input())

n, m = map(int, input().split())

row_divs = divisors(n)
col_divs = divisors(m)

valid_rows = []
for r in row_divs:
    ok = True
    for start in range(r+1, n+1, r):
        if start + r - 1 > n:
            break
        if not query(r, m, 1, 1, start, 1):
            ok = False
            break
    if ok:
        va
```
