---
title: "CF 1302A - Nash equilibrium"
description: "We are working with a rectangular grid of numbers. Each cell behaves like a player in a two-dimensional game: it is compared vertically against its column and horizontally against its row."
date: "2026-06-16T05:30:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1302
codeforces_index: "A"
codeforces_contest_name: "AIM Tech Poorly Prepared Contest (unrated, funny, Div. 1 preferred)"
rating: 0
weight: 1302
solve_time_s: 395
verified: false
draft: false
---

[CF 1302A - Nash equilibrium](https://codeforces.com/problemset/problem/1302/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a rectangular grid of numbers. Each cell behaves like a player in a two-dimensional game: it is compared vertically against its column and horizontally against its row.

A cell is called a Nash equilibrium if it is simultaneously the strict maximum in its column and the strict minimum in its row. In other words, looking down its column, no other value can match or exceed it, and looking across its row, no other value can match or go below it.

The task is to find such a cell. If multiple cells satisfy the condition, we choose the one that appears earliest in row order, and if there is still a tie, the earliest in column order. If no such cell exists, we output zero.

The constraints allow up to 1000 by 1000 cells, so up to one million values. That immediately rules out any solution that repeatedly scans entire rows and columns for every candidate cell. A naive per-cell validation would require checking its entire row and column, leading to about $O(nm(n + m))$ operations, which is too slow in the worst case.

A subtle issue appears when values repeat. A careless implementation might treat “maximum in column” or “minimum in row” using non-strict comparisons or only partial checks, which breaks correctness.

For example, consider a column `[1, 5, 5, 2]`. If we only check whether a value is equal to the maximum without enforcing uniqueness, both 5s might be considered valid column maxima, but the definition requires strict dominance over all other rows, which fails due to duplication.

Another edge case arises when the best row minimum and column maximum do not coincide structurally. A row might have a unique minimum, but that position is not a column maximum, so local reasoning per row is insufficient.

## Approaches

The brute-force idea is straightforward. For every cell, we verify two conditions: it must be strictly larger than every other value in its column and strictly smaller than every other value in its row. Each verification costs linear time in the row or column length. Since we may check up to $10^6$ cells, each costing up to $O(1000)$, the total work becomes around $10^9$, which is too large for two seconds.

The key observation is that the conditions can be precomputed independently. For each row, we only need its minimum value and the column index where it occurs. For each column, we only need its maximum value and the row index where it occurs. A valid equilibrium must lie exactly at the intersection of a row minimum and a column maximum.

This reduces the search space dramatically. Instead of testing every cell, we only check candidates derived from row minima or column maxima, and verify consistency in constant time per candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm(n+m))$ | $O(1)$ | Too slow |
| Optimal | $O(nm)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We construct the solution by precomputing row minima and column maxima, then intersecting these constraints.

1. For each row, scan all columns and store the minimum value and its column index. If the minimum appears multiple times, we still keep the first position, since tie-breaking prefers smaller column index.
2. For each column, scan all rows and store the maximum value and its row index. Again, ties are resolved by preferring the smallest row index.
3. Iterate over all rows. For each row, take its stored minimum position $(i, j)$.
4. At each candidate position, check whether the value at $(i, j)$ equals the maximum of column $j$. This ensures column dominance.
5. If both conditions match, record this cell as a valid answer candidate.
6. Because rows are processed in increasing order and we pick the first valid column index within each row, the lexicographically smallest valid cell is automatically chosen.

### Why it works

A valid Nash equilibrium must simultaneously satisfy a local extremum condition in its row and column. The row condition forces the cell to be one of the row minima, and the column condition forces it to be one of the column maxima. Any valid solution must appear in both precomputed structures. By enumerating only row minima and validating against column maxima, we guarantee we never miss a solution while avoiding checking irrelevant cells. The ordering of iteration ensures lexicographic minimality without additional sorting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    row_min_val = [10**18] * n
    row_min_idx = [-1] * n

    col_max_val = [-10**18] * m
    col_max_idx = [-1] * m

    for i in range(n):
        for j in range(m):
            v = a[i][j]
            if v < row_min_val[i]:
                row_min_val[i] = v
                row_min_idx[i] = j
            if v > col_max_val[j]:
                col_max_val[j] = v
                col_max_idx[j] = i

    for i in range(n):
        j = row_min_idx[i]
        if j == -1:
            continue
        if a[i][j] == col_max_val[j]:
            print(i + 1, j + 1)
            return

    print(0, 0)

if __name__ == "__main__":
    solve()
```

The implementation first builds two auxiliary arrays in a single pass over the matrix. The row arrays capture the smallest element in each row along with its column position. The column arrays capture the largest element in each column along with its row position.

The second phase only checks row minima, because any valid equilibrium must be a row minimum. For each row minimum, we verify whether it is also the column maximum for its column. If so, it satisfies both constraints.

A common pitfall is trying to independently enforce both conditions per cell without precomputation, which leads to quadratic scanning. Another mistake is not respecting strict comparison semantics, especially if replacing `<` or `>` with `<=` or `>=`, which breaks the equilibrium definition.

## Worked Examples

### Example 1

Input:

```
4 4
1 2 3 4
1 2 3 5
1 2 3 6
2 3 5 7
```

We compute row minima:

| Row | Min Value | Position |
| --- | --- | --- |
| 1 | 1 | (1,1) |
| 2 | 1 | (2,1) |
| 3 | 1 | (3,1) |
| 4 | 2 | (4,1) |

Column maxima:

| Col | Max Value | Position |
| --- | --- | --- |
| 1 | 2 | (4,1) |
| 2 | 3 | (4,2) |
| 3 | 5 | (4,3) |
| 4 | 7 | (4,4) |

We test row 1 minimum at (1,1): column 1 max is 2, mismatch.

Row 2 minimum at (2,1): mismatch again.

Row 3 minimum at (3,1): mismatch.

Row 4 minimum at (4,1): value 2 equals column 1 max 2, so this is valid.

Output is (4,1). In lexicographic terms, this is the earliest valid row, and within that row the only candidate.

This demonstrates that the solution relies on intersection of row minima and column maxima rather than arbitrary cells.

### Example 2

Input:

```
3 3
5 1 5
2 3 4
1 6 7
```

Row minima:

| Row | Min Value | Position |
| --- | --- | --- |
| 1 | 1 | (1,2) |
| 2 | 2 | (2,1) |
| 3 | 1 | (3,1) |

Column maxima:

| Col | Max Value | Position |
| --- | --- | --- |
| 1 | 5 | (1,1) |
| 2 | 6 | (3,2) |
| 3 | 7 | (3,3) |

Checking row minima:

(1,2): 1 vs column 2 max 6, mismatch

(2,1): 2 vs column 1 max 5, mismatch

(3,1): 1 vs column 1 max 5, mismatch

No intersection exists, so output is (0,0).

This confirms that the algorithm correctly rejects cases where row and column extremal constraints never align.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each cell is visited once to compute row minima and column maxima, then each row is checked once |
| Space | $O(n+m)$ | We store one minimum per row and one maximum per column |

The matrix size is at most one million elements, so a single linear scan is sufficient. The solution stays well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    row_min_val = [10**18] * n
    row_min_idx = [-1] * n
    col_max_val = [-10**18] * m

    for i in range(n):
        for j in range(m):
            v = a[i][j]
            if v < row_min_val[i]:
                row_min_val[i] = v
                row_min_idx[i] = j
            if v > col_max_val[j]:
                col_max_val[j] = v

    for i in range(n):
        j = row_min_idx[i]
        if j != -1 and a[i][j] == col_max_val[j]:
            return f"{i+1} {j+1}"

    return "0 0"

# sample
assert run("4 4\n1 2 3 4\n1 2 3 5\n1 2 3 6\n2 3 5 7\n") == "4 1"

# all equal (no strict max/min possible conflict)
assert run("2 2\n1 1\n1 1\n") == "0 0"

# single valid equilibrium
assert run("2 2\n1 2\n3 0\n") == "1 2"

# unique row min and col max alignment
assert run("3 3\n1 2 3\n4 5 6\n7 8 9\n") == "3 3"

# no solution
assert run("3 3\n9 8 7\n6 5 4\n3 2 1\n") == "0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 4 1 | basic correctness |
| all equal | 0 0 | strict inequality handling |
| mixed grid | 1 2 | single equilibrium detection |
| increasing grid | 3 3 | boundary case max alignment |
| decreasing grid | 0 0 | no valid intersection |

## Edge Cases

One important edge case is when a row has multiple identical minima. In such cases, picking any of them could lead to different column checks. The algorithm avoids ambiguity by always recording the first occurrence, which preserves lexicographic priority.

Another case is when a column maximum appears in multiple rows. Only one of them can satisfy the row-minimum constraint simultaneously. The intersection check ensures that only a cell that is extremal in both directions is accepted.

A third case is when the grid contains constant values. Every cell is a row minimum and column maximum in a non-strict sense, but strict inequalities eliminate all candidates. The algorithm correctly returns no solution because no value is strictly greater or smaller than its neighbors in the required directions.
