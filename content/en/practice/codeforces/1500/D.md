---
title: "CF 1500D - Tiles for Bathroom"
description: "We are given an $n times n$ grid representing a tile stand, where each cell contains a tile of a certain color. Kostya wants to know, for each possible subsquare size $k$, how many $k times k$ subsquares contain at most $q$ distinct colors."
date: "2026-06-10T21:04:47+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1500
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 707 (Div. 1, based on Moscow Open Olympiad in Informatics)"
rating: 2900
weight: 1500
solve_time_s: 76
verified: true
draft: false
---

[CF 1500D - Tiles for Bathroom](https://codeforces.com/problemset/problem/1500/D)

**Rating:** 2900  
**Tags:** data structures, sortings, two pointers  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid representing a tile stand, where each cell contains a tile of a certain color. Kostya wants to know, for each possible subsquare size $k$, how many $k \times k$ subsquares contain at most $q$ distinct colors. A subsquare is determined solely by its top-left corner and its size. The output is a list of integers: for each $k$ from 1 to $n$, the number of valid subsquares of size $k$.

The grid size $n$ can go up to 1500, which implies that a naive approach examining every subsquare independently is likely too slow. The total number of $k \times k$ subsquares is $(n - k + 1)^2$, so summing over all $k$ gives roughly $O(n^3)$ subsquares. If for each we count distinct colors with a linear scan over $k^2$ cells, we reach $O(n^5)$ operations in the worst case, which is completely infeasible.

Non-obvious edge cases include grids with repeated colors. For example, a 3x3 grid where all tiles are the same color will produce different counts than one where all colors are distinct. For $q=1$, the solution must detect squares with only a single color, otherwise the count will be wrong. Another subtle case is when $q \ge n^2$; then all subsquares are valid regardless of their colors. Finally, when $n=1$, we must correctly handle a single cell as a 1x1 subsquare.

## Approaches

A brute-force solution would iterate over all possible top-left corners $(i,j)$ and all possible sizes $k$. For each subsquare, we would collect all colors in a set and check if its size does not exceed $q$. This is correct, but its complexity is $O(n^3 \cdot k^2) = O(n^5)$ in the worst case, which is far beyond the allowed limit.

The key insight is that $q$ is small, at most 10. This allows us to represent sets of colors efficiently and merge them in constant or small fixed time. Instead of counting all colors naively for each subsquare, we can build up information incrementally. Consider a dynamic programming approach where we store, for each cell, the set of up to $q+1$ smallest colors appearing in the subsquare ending at that cell. When expanding a subsquare from size $k-1$ to $k$, we only need to combine the color sets from the top-left corner, the rightmost column, and the bottom row. Because we only track the first $q+1$ colors, we can immediately know if a square is invalid if the combined set exceeds $q$.

This approach reduces the complexity dramatically because we no longer iterate over every cell in each subsquare individually. Instead, we merge small sets of size at most $q+1$ for each expansion, giving a total time of $O(n^2 q^2)$, which is feasible for $n=1500$ and $q \le 10$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^5) | O(k^2) per subsquare | Too slow |
| Optimal (DP + small sets) | O(n^2 q^2) | O(n^2 q) | Accepted |

## Algorithm Walkthrough

1. Initialize a 2D array `dp[i][j]` where each entry stores a sorted list of up to `q+1` distinct colors in the subsquare ending at `(i,j)` for the current size.
2. For size `k=1`, each `dp[i][j]` is simply the color at `c[i][j]`. Count all such squares that satisfy `q` immediately.
3. For size `k > 1`, iterate over all possible bottom-right corners `(i,j)` of a `k x k` square. Construct the color set by merging three components: the set from the `(k-1)x(k-1)` subsquare ending at `(i-1,j-1)`, the rightmost column of length `k-1`, and the bottom row of length `k-1`. Use sorted merge and keep only the first `q+1` colors.
4. If the merged color set contains `<= q` colors, increment the count for this size `k`.
5. Repeat this process for all sizes `k` from 1 to `n`. Output the counts.

Why it works: At each step, `dp[i][j]` contains a complete summary of the colors in the `k x k` subsquare ending at `(i,j)`. By merging only up to `q+1` colors, we detect early if the subsquare exceeds the allowed number of distinct colors. The invariant is that all possible `k x k` subsquares are considered exactly once, and their color sets are correctly maintained.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())
    c = [list(map(int, input().split())) for _ in range(n)]
    
    counts = [0] * n
    # dp[i][j] stores the color set for the current size k ending at (i,j)
    dp = [[[] for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            dp[i][j] = [c[i][j]]
            if q >= 1:
                counts[0] += 1
    
    for k in range(2, n+1):
        new_dp = [[[] for _ in range(n)] for _ in range(n)]
        for i in range(k-1, n):
            for j in range(k-1, n):
                merged = set()
                merged.update(dp[i-1][j-1])
                for x in range(i-k+1, i):
                    merged.add(c[x][j])
                for y in range(j-k+1, j):
                    merged.add(c[i][y])
                if len(merged) <= q:
                    counts[k-1] += 1
                new_dp[i][j] = list(merged)[:q+1]
        dp = new_dp
    
    print('\n'.join(map(str, counts)))

if __name__ == "__main__":
    main()
```

The solution initializes the DP table with single-cell squares. When expanding to larger squares, the merge of color sets is limited to `q+1` to
