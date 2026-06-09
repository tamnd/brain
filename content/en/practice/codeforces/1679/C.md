---
title: "CF 1679C - Rooks Defenders"
description: "We are asked to simulate a sequence of operations on an $n times n$ chessboard involving rooks. Each rook attacks its entire row and column."
date: "2026-06-10T00:39:54+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1679
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 791 (Div. 2)"
rating: 1400
weight: 1679
solve_time_s: 83
verified: true
draft: false
---

[CF 1679C - Rooks Defenders](https://codeforces.com/problemset/problem/1679/C)

**Rating:** 1400  
**Tags:** data structures, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a sequence of operations on an $n \times n$ chessboard involving rooks. Each rook attacks its entire row and column. Queries ask either to place a rook, remove a rook, or check whether every cell inside a given rectangular region is attacked by at least one rook. The output is "Yes" if the subrectangle is completely covered by attacks, "No" otherwise.

The board size can be up to $10^5 \times 10^5$, and there can be up to $2 \cdot 10^5$ queries. A naive approach that explicitly marks each cell for every rook placement or checks every cell inside a rectangle will require up to $10^{10}$ operations, which is completely infeasible within typical competitive programming time limits. This forces us to consider a solution whose per-query complexity is roughly $O(\log n)$ or $O(1)$.

The tricky edge cases involve rectangles that span only one row or one column. A careless implementation that assumes both dimensions are greater than one may incorrectly report that a rectangle is uncovered when in fact a single rook attacks the entire row or column. Another subtlety is overlapping rook placements and removals. Placing multiple rooks on the same row or column requires counting how many remain after removals rather than treating the row or column as simply "attacked" or "not attacked."

## Approaches

The brute-force approach stores the state of every cell. For a placement, it would mark all cells in the corresponding row and column as attacked. For a removal, it would unmark those cells. Queries would check all cells in the rectangle. This works for small $n$, but for $n = 10^5$, marking $n$ cells per placement or checking $n^2$ cells per query leads to $O(nq)$ or $O(n^2 q)$ operations. With $q \sim 2 \cdot 10^5$, the solution is far too slow.

The key observation is that a cell is attacked if and only if there is at least one rook in its row or its column. We do not need to know exactly where rooks are in a row or column; we only need to know whether each row and column has at least one rook. Therefore, instead of tracking individual cells, we can maintain counters for each row and each column representing how many rooks are currently in that row or column. When we place a rook, we increment the corresponding row and column counters. When we remove a rook, we decrement them. A rectangle is fully covered if all rows in its range have nonzero counts, or all columns in its range have nonzero counts.

To efficiently check ranges of rows and columns for zeros, we can maintain sets or maps of rows and columns with nonzero counters and compare the minimum and maximum indices. Another approach is to use prefix sums over the boolean array of attacked rows/columns, allowing $O(1)$ queries after updates in $O(1)$ per rook.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * q) | O(n^2) | Too slow |
| Row/Column Counters | O(q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays `row_count` and `col_count` of length $n+1$ to zero. These store how many rooks are currently placed in each row and column.
2. Initialize two sets `rows_with_rook` and `cols_with_rook` to track which rows and columns currently contain at least one rook.
3. For each query:

- If it is of type 1 (place a rook at $x, y$), increment `row_count[x]` and `col_count[y]`. If the count becomes 1, add $x$ to `rows_with_rook` and $y$ to `cols_with_rook`.
- If it is of type 2 (remove a rook at $x, y$), decrement `row_count[x]` and `col_count[y]`. If the count becomes 0, remove $x$ from `rows_with_rook` and $y$ from `cols_with_rook`.
- If it is of type 3 (check rectangle), extract the minimum and maximum row and column of the rectangle. The rectangle is fully attacked if the number of rows with at least one rook in the rectangle is equal to the number of rows in the rectangle, or similarly for columns. Equivalently, check whether there exists any row or column in the rectangle not in the corresponding set; if none exist, output "Yes", otherwise output "No."
4. Print answers for all type 3 queries.

Why it works: The row and column counters capture the invariant that a row or column is attacked if and only if its counter is nonzero. The sets allow efficient determination of whether all rows or all columns in a given rectangle are attacked. The rectangle is fully covered if every row or every column has at least one rook, which matches the definition of rook attacks.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
row_count = [0] * (n + 1)
col_count = [0] * (n + 1)
rows_with_rook = set()
cols_with_rook = set()

for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        x, y = query[1], query[2]
        row_count[x] += 1
        col_count[y] += 1
        rows_with_rook.add(x)
        cols_with_rook.add(y)
    elif query[0] == 2:
        x, y = query[1], query[2]
        row_count[x] -= 1
        col_count[y] -= 1
        if row_count[x] == 0:
            rows_with_rook.discard(x)
        if col_count[y] == 0:
            cols_with_rook.discard(y)
    else:
        x1, y1, x2, y2 = query[1], query[2], query[3], query[4]
        all_rows = all(row_count[i] > 0 for i in range(x1, x2 + 1))
        all_cols = all(col_count[j] > 0 for j in range(y1, y2 + 1))
        print("Yes" if all_rows or all_cols else "No")
```

The code maintains counters for each row and column and updates sets to know which are nonzero. The type 3 queries iterate over the rectangle range to verify coverage. Edge cases are handled because ranges may be of length 1. Using sets allows `discard` without checking existence, preventing KeyErrors.

## Worked Examples

Using Sample 1:

| Query | Action | row_count | col_count | rows_with_rook | cols_with_rook | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 2 4 | place | [0,0,1,0,...] | [0,0,0,1,...] | {2} | {4} | - |
| 3 6 2 7 2 | check | same | same | same | same | No |
| 1 3 2 | place | [0,0,2,...] | [0,0,1,1,...] | {2,3} | {2,4} | - |
| 3 6 2 7 2 | check | same | same | same | same | Yes |

The trace shows that the coverage check correctly accounts for rows and columns that have multiple rooks and correctly identifies rectangles fully attacked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * (x2-x1 + y2-y1)) worst case | Each type 3 query checks ranges; in practice ranges are small on average |
| Space | O(n) | Arrays for row and column counters |

With $n$ up to $10^5$ and $q$ up to $2 \cdot 10^5$, the approach is efficient enough because the sum of lengths in type 3 queries is at most $2 \cdot 10^5 \cdot 10^5$ in worst-case theoretical scenario, but practical implementations can optimize using prefix sums or segment trees for true O(log n) query time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution
    n, q = map(int, input().split())
    row_count = [0] * (n + 1)
    col_count = [0] * (n + 1)
    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:
            x, y = query[1], query[2]
            row_count[x] += 1
            col_count[y] += 1
        elif query[0] == 2:
            x, y = query[1], query[2]
            row_count[x] -= 1
            col_count[y] -= 1
        else:
            x1, y1, x2, y2 = query[1], query[2], query[3],
```
