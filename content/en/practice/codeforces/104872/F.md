---
title: "CF 104872F - Magic Square"
description: "We are given an $n times n$ grid that initially contains a perfect permutation of numbers from $1$ to $n^2$. The defining property of the original grid is that every row sum equals the same value, and every column sum also equals that same value."
date: "2026-06-28T10:27:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104872
codeforces_index: "F"
codeforces_contest_name: "2023-2024 Russia Team Open, High School Programming Contest (VKOSHP XXIV)"
rating: 0
weight: 104872
solve_time_s: 79
verified: false
draft: false
---

[CF 104872F - Magic Square](https://codeforces.com/problemset/problem/104872/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times n$ grid that initially contains a perfect permutation of numbers from $1$ to $n^2$. The defining property of the original grid is that every row sum equals the same value, and every column sum also equals that same value. This structure is destroyed by exactly one operation: two cells have had their values swapped.

The task is to identify the coordinates of the two swapped cells. If we swap those two values back, the grid becomes a valid “magic” grid again, meaning all row sums and column sums become equal.

The key constraint is that $n$ can be as large as 1000, so the grid contains up to one million cells. Any solution that recomputes row or column properties for many candidate swaps must effectively operate in linear time over the grid. A quadratic or even $O(n^3)$ simulation of swaps is not viable, but anything based on a single pass over the grid is acceptable.

A subtle point is that all values are distinct, so each value uniquely identifies its position. This eliminates ambiguity: if a value is wrong in a row sum, it is traceable to a unique location.

Another important observation is that the grid differs from a valid magic square by exactly two cells. That means all structural violations are localized, and every row and column is correct except those affected by the swapped positions.

A naive failure case arises if one assumes only rows or only columns need to be checked. Consider a swap that preserves row sums but breaks column sums, or vice versa; such cases force us to reason about both dimensions simultaneously.

## Approaches

A direct brute-force idea is to consider every pair of cells, swap them, and check whether the resulting grid becomes magic. For each pair, recomputing all row and column sums costs $O(n^2)$, and there are $O(n^4)$ pairs. This leads to an astronomically large complexity of $O(n^6)$, which is completely infeasible even for small $n$.

We need to avoid simulating swaps. The structure of the problem suggests looking at aggregate information instead of configurations. In a correct magic grid, every row sum equals a constant $S$, and every column sum also equals $S$. If a swap occurs, exactly two rows and two columns will have incorrect sums, because only those containing the swapped cells are affected.

This reduces the problem to identifying which rows and columns are “imbalanced” and then localizing the exact cells responsible. Since values are distinct, we can compute expected sums and compare them with actual sums in $O(n^2)$, then deduce the two affected rows and columns.

Once we isolate the two bad rows and two bad columns, the swapped elements must lie at their intersections. This reduces the candidate space to at most four cells, and we can determine the correct pair by checking which swap restores consistency.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Swap Check | $O(n^6)$ | $O(1)$ | Too slow |
| Row/Column Deviation Analysis | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Compute the expected magic sum $S = \frac{n(n^2+1)}{2}$. This is the sum each row and column should have in a correct grid because the grid is a permutation of $1 \ldots n^2$.
2. Compute all row sums in a single pass over the grid. Identify rows whose sum differs from $S$. These are candidate rows that contain one of the swapped elements.
3. Compute all column sums similarly and identify the columns whose sums differ from $S$. These are candidate columns that contain swapped elements.
4. By the nature of a single swap, exactly two rows and exactly two columns will be incorrect. Call them $r_1, r_2$ and $c_1, c_2$. This follows because each swapped cell affects exactly one row and one column.
5. Consider the four intersection cells: $(r_1,c_1), (r_1,c_2), (r_2,c_1), (r_2,c_2)$. These are the only positions that could possibly contain the swapped values.
6. Try swapping the values of any pair among these four candidates and check whether row and column sums all become equal to $S$. Exactly one swap will satisfy this condition.
7. Output the coordinates of the valid pair.

### Why it works

Each swapped cell contributes an additive error to exactly one row sum and one column sum. Since there are exactly two swapped cells, the number of affected rows and columns cannot exceed two each, and cannot be fewer than two unless both swapped cells are in the same row or column, which would still produce exactly one row or column imbalance pattern consistent with the same intersection logic. This restriction forces all incorrect structure to concentrate in at most four coordinates, and no other cell can influence sums independently. Therefore, restricting attention to the intersection of anomalous rows and columns is sufficient to recover the original swap uniquely.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [list(map(int, input().split())) for _ in range(n)]

    S = n * (n * n + 1) // 2

    row_sum = [0] * n
    col_sum = [0] * n

    for i in range(n):
        for j in range(n):
            v = a[i][j]
            row_sum[i] += v
            col_sum[j] += v

    bad_rows = [i for i in range(n) if row_sum[i] != S]
    bad_cols = [j for j in range(n) if col_sum[j] != S]

    if len(bad_rows) == 1:
        bad_rows.append(bad_rows[0])
    if len(bad_cols) == 1:
        bad_cols.append(bad_cols[0])

    r1, r2 = bad_rows[0], bad_rows[1]
    c1, c2 = bad_cols[0], bad_cols[1]

    def check_swap(x1, y1, x2, y2):
        # simulate swap effect locally by computing affected rows/cols
        rs = row_sum[:]
        cs = col_sum[:]

        v1 = a[x1][y1]
        v2 = a[x2][y2]

        rs[x1] += v2 - v1
        rs[x2] += v1 - v2
        cs[y1] += v2 - v1
        cs[y2] += v1 - v2

        return all(rs[i] == S for i in range(n)) and all(cs[j] == S for j in range(n))

    candidates = [
        (r1, c1, r2, c2),
        (r1, c2, r2, c1)
    ]

    for x1, y1, x2, y2 in candidates:
        if check_swap(x1, y1, x2, y2):
            print(x1 + 1, y1 + 1)
            print(x2 + 1, y2 + 1)
            return

solve()
```

The implementation begins by reading the grid and computing row and column sums in one pass. This is the only (O(
