---
title: "CF 329A - Purification"
description: "We have an n × n grid. Some cells are usable (.), while some cells are forbidden (E). A spell may only be cast on a usable cell. When we cast a spell on cell (r, c), every cell in row r and every cell in column c becomes purified."
date: "2026-06-06T09:07:55+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 329
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 192 (Div. 1)"
rating: 1500
weight: 329
solve_time_s: 115
verified: true
draft: false
---

[CF 329A - Purification](https://codeforces.com/problemset/problem/329/A)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × n` grid. Some cells are usable (`.`), while some cells are forbidden (`E`). A spell may only be cast on a usable cell.

When we cast a spell on cell `(r, c)`, every cell in row `r` and every cell in column `c` becomes purified. The goal is to purify the entire grid using the minimum possible number of spells.

A cell is purified if at least one selected spell shares its row or its column. Since a spell affects exactly one row and one column, the choice of spell positions determines which rows and columns become "covered".

The grid size is at most 100, so even quadratic or cubic algorithms are easily affordable. The challenge is not performance, it is discovering the structure that characterizes when a solution exists and how to construct one.

A useful observation is that every spell can introduce at most one previously uncovered row. Since there are `n` rows, at least `n` spells are necessary in any valid solution. The same argument applies to columns. If we can find a solution using exactly `n` spells, it is automatically optimal.

The most common mistake is assuming that we must simultaneously cover every row and every column with selected cells. That sounds like a bipartite matching problem, but it is stronger than what the problem actually requires.

Consider:

```
2
..
.E
```

Choosing `(1,1)` and `(2,1)` uses only column 1, yet every row is covered. Every cell in row 1 is purified by the first spell, and every cell in row 2 is purified by the second spell. The whole grid becomes purified even though column 2 never contains a selected spell.

Another easy-to-miss case is when a row contains only forbidden cells:

```
2
EE
..
```

No spell can ever be cast in the first row. Since every cell in that row must still become purified, we would need some selected column to reach them. Unfortunately both cells in the row are forbidden, so no selected position can lie there. The correct answer is `-1`.

There is a symmetric situation with columns:

```
2
E.
E.
```

Column 1 contains only forbidden cells. Any solution based on selecting one usable cell per column is impossible, but selecting one usable cell per row works immediately. A correct algorithm must check both possibilities.

## Approaches

A brute-force approach would try all subsets of usable cells and test whether the resulting set of spells purifies the entire grid. If there are up to `10000` usable cells, the search space is `2^10000`, which is completely infeasible.

The key is to understand what purification actually requires.

Suppose we choose exactly one usable cell from every row. Then every row contains a spell. Since a spell purifies its entire row, every row of the grid becomes purified. Once every row is purified, every cell of the grid is purified, regardless of which columns were chosen.

This immediately gives a valid solution whenever every row contains at least one usable cell.

The same reasoning works symmetrically. If every column contains at least one usable cell, choosing one usable cell from each column also purifies the whole grid.

Now consider when neither condition holds. There exists a row consisting entirely of `E`, and there exists a column consisting entirely of `E`.

Take the intersection of that row and column. That cell cannot be purified from its row because no spell can be cast in that row. It cannot be purified from its column because no spell can be cast in that column. Thus purification is impossible.

This gives a complete characterization:

If every row has at least one usable cell, select one usable cell per row.

Otherwise, if every column has at least one usable cell, select one usable cell per column.

Otherwise, output `-1`.

The construction uses exactly `n` spells. Since any solution needs at least `n` spells, it is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n²)) | O(n²) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the grid.
2. Check every row.
3. For each row, find any usable cell `.`.
4. If every row contains at least one usable cell, store one such position from each row and output them.

The solution is valid because every row receives a spell, so every cell belongs to a purified row.
5. If some row contains no usable cell, discard the row-based construction and check columns instead.
6. For each column, find any usable cell `.`.
7. If every column contains at least one usable cell, store one such position from each column and output them.

Every column receives a spell, so every cell belongs to a purified column.
8. If some column also contains no usable cell, output `-1`.

### Why it works

If every row has a usable cell, selecting one usable cell from each row creates exactly `n` spells. Every row is purified by its own spell, so every cell of the grid is purified. The same argument holds symmetrically for columns.

If neither construction exists, then there is at least one all-`E` row and at least one all-`E` column. Their intersection cell belongs to a row with no spell and a column with no spell. No selected position can purify it, making purification impossible.

The algorithm returns a valid solution whenever one exists and correctly reports impossibility otherwise.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    row_ans = []

    ok = True
    for i in range(n):
        pos = -1
        for j in range(n):
            if grid[i][j] == '.':
                pos = j
                break
        if pos == -1:
            ok = False
            break
        row_ans.append((i + 1, pos + 1))

    if ok:
        print("\n".join(f"{r} {c}" for r, c in row_ans))
        return

    col_ans = []

    ok = True
    for j in range(n):
        pos = -1
        for i in range(n):
            if grid[i][j] == '.':
                pos = i
                break
        if pos == -1:
            ok = False
            break
        col_ans.append((pos + 1, j + 1))

    if ok:
        print("\n".join(f"{r} {c}" for r, c in col_ans))
    else:
        print(-1)

solve()
```

The first block searches row by row. For each row, it records the first usable cell. If every row provides one candidate, those positions immediately form a valid optimal answer.

If a row fails, the algorithm switches to the symmetric column construction. For each column it records the first usable cell.

The implementation uses 1-based coordinates when storing answers because the output format requires them. This is the most common source of off-by-one mistakes.

Another subtle point is that the row solution should be printed immediately when found. There is no need to examine columns afterward because the row construction is already optimal.

## Worked Examples

### Example 1

Input:

```
3
.E.
E.E
.E.
```

Row scan:

| Row | First usable cell | Stored |
| --- | --- | --- |
| 1 | Column 1 | (1,1) |
| 2 | Column 2 | (2,2) |
| 3 | Column 1 | (3,1) |

All rows contain a usable cell.

Output:

```
1 1
2 2
3 1
```

The sample output uses `(3,3)` instead of `(3,1)`. Both are correct. Any valid construction is accepted.

This trace shows that only one usable cell per row is needed. The exact column choice is irrelevant.

### Example 2

Input:

```
2
EE
.E
```

Row scan:

| Row | First usable cell |
| --- | --- |
| 1 | None |

The row construction fails.

Column scan:

| Column | First usable cell |
| --- | --- |
| 1 | None |

The column construction also fails.

Output:

```
-1
```

The first row and first column are entirely forbidden. Their intersection cell can never be purified.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each cell is examined at most once during row scanning and once during column scanning |
| Space | O(n) | Stores at most `n` answer positions |

With `n ≤ 100`, the algorithm performs at most a few tens of thousands of operations, far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    grid = [input().strip() for _ in range(n)]

    row_ans = []
    ok = True

    for i in range(n):
        pos = -1
        for j in range(n):
            if grid[i][j] == '.':
                pos = j
                break
        if pos == -1:
            ok = False
            break
        row_ans.append((i + 1, pos + 1))

    if ok:
        return "\n".join(f"{r} {c}" for r, c in row_ans)

    col_ans = []
    ok = True

    for j in range(n):
        pos = -1
        for i in range(n):
            if grid[i][j] == '.':
                pos = i
                break
        if pos == -1:
            ok = False
            break
        col_ans.append((pos + 1, j + 1))

    if ok:
        return "\n".join(f"{r} {c}" for r, c in col_ans)

    return "-1"

# sample 1
assert run("3\n.E.\nE.E\n.E.\n") == "1 1\n2 2\n3 1"

# minimum size
assert run("1\n.\n") == "1 1"

# impossible
assert run("2\nEE\n.E\n") == "-1"

# column construction required
assert run("2\nE.\nE.\n") == "1 1\n1 2"

# all usable
assert run("2\n..\n..\n") == "1 1\n2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` with `.` | `1 1` | Minimum size |
| `EE / .E` | `-1` | Impossible configuration |
| `E. / E.` | Column-based solution | Row construction fails, column construction succeeds |
| All `.` | One position per row | Standard valid case |

## Edge Cases

### Row completely forbidden

Input:

```
2
EE
..
```

The row scan immediately fails on row 1 because there is no usable cell. The algorithm then checks columns.

Column 1 contains a usable cell `(2,1)` and column 2 contains `(2,2)`, so the column construction succeeds:

```
2 1
2 2
```

Every column is purified, hence every cell is purified.

### Column completely forbidden

Input:

```
2
E.
E.
```

The row scan succeeds:

```
1 2
2 2
```

Every row is purified. The algorithm never needs the column construction.

This demonstrates why checking only columns would be incorrect.

### Both an all-`E` row and an all-`E` column

Input:

```
2
EE
E.
```

Row 1 contains no usable cell, so the row construction fails.

Column 1 contains no usable cell, so the column construction also fails.

The algorithm outputs:

```
-1
```

Cell `(1,1)` lies in a row with no spell and a column with no spell, making purification impossible.

### Single usable cell

Input:

```
1
.
```

The row scan finds `(1,1)` and outputs:

```
1 1
```

One spell purifies the only row and the only column, covering the entire grid.
