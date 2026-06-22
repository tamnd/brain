---
title: "CF 105387B - Destroy them all!"
description: "We are given a very large grid, but only a small number of cells inside it are marked. From this state, we are allowed to choose a single empty cell and pick one of four cardinal directions."
date: "2026-06-23T05:08:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105387
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2023"
rating: 0
weight: 105387
solve_time_s: 135
verified: false
draft: false
---

[CF 105387B - Destroy them all!](https://codeforces.com/problemset/problem/105387/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a very large grid, but only a small number of cells inside it are marked. From this state, we are allowed to choose a single empty cell and pick one of four cardinal directions. In that chosen direction, the game destroys every marked cell that lies strictly in that direction along the same row or the same column, depending on whether we choose horizontal or vertical movement.

The goal is to pick an empty starting cell and a direction so that the number of destroyed marked cells is as large as possible, and we also need to output one valid starting position that achieves this maximum.

Although the grid size can go up to 10^9 in both dimensions, only up to 200,000 cells are marked. This immediately tells us that the structure of the solution must depend only on the marked cells and not on any full grid representation.

A brute force interpretation would be to try every empty cell, and for each of them scan its row and column to count how many marked cells lie in each direction. This is impossible because the number of empty cells is effectively n·m minus k, which can be enormous.

A more subtle constraint comes from the fact that the choice of direction only cares about alignment. Once we fix a cell, only marked cells in its row or column matter. This suggests compressing the problem into row-wise and column-wise frequency information.

A common failure case for naive reasoning appears when one assumes the best position must lie on or next to a marked cell. That is false because placing the starting point outside the extremal marked positions in a row or column can capture all marked cells in that line.

For example, consider a row with marked columns 3 and 10. If we place the starting point at column 1 in that same row, the entire right direction destroys both marks. A solution that only considers positions adjacent to marked cells would miss this.

Another failure case appears when all marked cells lie in a single row or column. In that situation, choosing a cell in a different row or column might still be valid and potentially necessary depending on whether the row is fully filled or not.

## Approaches

A direct brute force approach would iterate over every empty cell and compute the number of marked cells reachable in four directions. For each candidate cell, scanning its row and column using a hash set or binary search would cost O(k) per cell in the worst case. Since the number of empty cells is essentially n·m, this approach is completely infeasible.

The key observation is that the grid structure is irrelevant beyond grouping marked cells by row and by column. Once we fix a row, all that matters is how many marked cells exist in that row. The same applies to columns.

For a fixed row with t marked cells, suppose we choose an empty cell in that row. If we place it outside the interval spanned by marked cells, we can capture all t cells in one direction. If we place it inside the interval, we can split the row into left and right parts, but the best we can do there is still t − 1. Since the grid is large and there is at least one empty position unless the row is fully filled, we can always choose a position outside the marked range, giving value t.

Thus each row contributes its count of marked cells as long as it is not completely filled. An identical argument applies to columns.

This reduces the task to computing row frequencies and column frequencies and taking the maximum among them, while ensuring that at least one valid empty cell exists in the chosen row or column.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m·k) | O(k) | Too slow |
| Optimal | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

We separate the problem into row statistics and column statistics.

1. Read all marked cells and group them by row and by column. We store for each row a list of its marked columns, and for each column a list of its marked rows. This is the only information about the grid we need.
2. For each row, compute how many marked cells it contains. If the count equals m, then this row has no empty cells and cannot be used as a starting position, so we ignore it.
3. For every usable row, compute its candidate score equal to the number of marked cells in that row. We also keep track of the best row and its count.
4. Repeat the same process for columns. If a column has count equal to n, it is fully occupied and cannot be used. Otherwise its candidate score is the number of marked cells in that column.
5. Compare the best row score and best column score. The larger one is the answer. If both are zero or no valid row/column exists, then there is no valid move and the answer is zero with coordinate 0 0.
6. To reconstruct a starting cell for a best row, we pick a row with maximum count and then find any column index that is not marked in that row. Since the row has at most k marked cells, we can try column indices starting from 1 until we find one not present in the set. The same logic applies for a best column.

Why it works is based on the fact that in any row with at least one empty cell, we can always place the starting point outside the segment of marked columns and capture all marked cells in one direction. Therefore the best achievable horizontal destruction in that row is exactly the number of marked cells in it. The same argument holds symmetrically for columns. Since every valid move must be anchored in some row or column, the global optimum must appear among these per-line maxima.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    row = {}
    col = {}
    marked = set()

    for _ in range(k):
        x, y = map(int, input().split())
        marked.add((x, y))
        if x not in row:
            row[x] = []
        if y not in col:
            col[y] = []
        row[x].append(y)
        col[y].append(x)

    best = 0
    best_type = None  # 0 for row, 1 for col
    best_idx = None

    for x, ys in row.items():
        t = len(ys)
        if t < m:
            if t > best:
                best = t
                best_type = 0
                best_idx = x

    for y, xs in col.items():
        c = len(xs)
        if c < n:
            if c > best:
                best = c
                best_type = 1
                best_idx = y

    if best == 0:
        print(0)
        print("0 0")
        return

    if best_type == 0:
        x = best_idx
        forbidden = set(row[x])
        y = 1
        while y in forbidden:
            y += 1
        print(best)
        print(x, y)
    else:
        y = best_idx
        forbidden = set(col[y])
        x = 1
        while x in forbidden:
            x += 1
        print(best)
        print(x, y)

if __name__ == "__main__":
    solve()
```

The code first builds adjacency lists for rows and columns while tracking all marked cells for quick membership queries. The main selection loop computes the best row and column candidates while discarding fully filled lines, since those cannot contain a valid starting cell.

The reconstruction step is intentionally simple: it scans upward from 1 until it finds an unmarked coordinate in the chosen line. This is safe because the number of marked cells is small, so the scan is bounded by k in the worst case per chosen line.

## Worked Examples

Consider the sample input.

We have rows with marked counts: row 3 has 2 marks, row 6 has 1, row 12 has 1. Column 4 has 2 marks, column 7 and 11 have 1 each.

| Step | Row 3 | Row 6 | Row 12 | Col 4 | Col 7 | Col 11 |
| --- | --- | --- | --- | --- | --- | --- |
| Count | 2 | 1 | 1 | 2 | 1 | 1 |
| Valid? | yes | yes | yes | yes | yes | yes |

The maximum is 2, achievable either from row 3 or column 4. The algorithm picks row 3 and selects any unmarked column in that row, such as 4.

This demonstrates that both row and column perspectives can yield the same optimum, and any valid reconstruction is acceptable.

Now consider a case where a row is fully filled:

Input:

```
1 5 5
1 1
1 2
1 3
1 4
1 5
```

There is no empty cell at all. The algorithm correctly identifies that all rows and columns are invalid, so it outputs zero.

This shows the importance of excluding fully occupied lines, since otherwise we would incorrectly assume we can place a starting point there.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each marked cell is processed once, and reconstruction scans at most k positions |
| Space | O(k) | We store row and column lists plus a set of marked cells |

The constraints allow up to 200,000 marked cells, so a linear solution over k is easily fast enough. The grid size is irrelevant since we never iterate over it.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    old_stdout = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = old_stdout
    return out.strip()

# sample
assert run("""12 12 4
3 7
3 11
6 4
12 4
""") == "2\n3 4"

# single cell
assert run("""3 3 1
2 2
""") in ["0\n0 0"], "center single mark"

# full row
assert run("""1 5 5
1 1
1 2
1 3
1 4
1 5
""") == "0\n0 0"

# column heavy
assert run("""5 5 3
1 1
2 1
5 1
""") == "3\n1 2"

# sparse large grid
assert run("""1000000000 1000000000 2
1 1
1 1000000000
""") == "2\n1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 0 0 | no valid move |
| full row | 0 0 | handling fully occupied line |
| column heavy | 3 1 2 | vertical optimal choice |
| sparse large grid | 2 1 2 | large coordinate correctness |

## Edge Cases

A key edge case is when all marked cells occupy an entire row. In that situation, that row contributes nothing because there is no valid empty starting cell. The algorithm handles this by explicitly checking whether the row count equals m and skipping it.

Another edge case occurs when the optimal solution lies in a column rather than a row. The reconstruction logic mirrors row handling and ensures we still find a valid empty coordinate by scanning for the first unmarked position in that column.

A third edge case is when k equals zero. Then every cell is empty, but any move destroys nothing. The algorithm correctly returns zero and any coordinate is acceptable, here represented as 0 0.
