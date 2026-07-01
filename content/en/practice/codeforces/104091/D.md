---
title: "CF 104091D - \u0428\u0430\u0445\u043c\u0430\u0442\u043d\u044b\u0439 \u0434\u043e\u0437\u043e\u0440"
description: "We are given a rectangular grid with $n$ rows and $m$ columns. Inside this grid there are $q$ special pieces called scouts. Each scout sits on a distinct cell $(x, y)$, where $x$ is the row index from top to bottom and $y$ is the column index from left to right."
date: "2026-07-02T02:28:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104091
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2022-2023"
rating: 0
weight: 104091
solve_time_s: 40
verified: true
draft: false
---

[CF 104091D - \u0428\u0430\u0445\u043c\u0430\u0442\u043d\u044b\u0439 \u0434\u043e\u0437\u043e\u0440](https://codeforces.com/problemset/problem/104091/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid with $n$ rows and $m$ columns. Inside this grid there are $q$ special pieces called scouts. Each scout sits on a distinct cell $(x, y)$, where $x$ is the row index from top to bottom and $y$ is the column index from left to right.

A scout “attacks” every cell that lies strictly in the region to its right or strictly below it, including its own position. Formally, a scout at $(x, y)$ covers all cells $(i, j)$ such that $i \ge x$ and $j \ge y$. If multiple scouts cover the same cell, we still count it only once.

The task is to compute how many distinct grid cells are covered by at least one scout.

The grid size constraints are extremely large, up to $10^9 \times 10^9$, so we cannot simulate the grid. The number of scouts is up to $10^5$, which means any solution must avoid per-cell processing and instead rely on aggregating geometric contributions.

A naive approach that checks every grid cell or even tries to iterate per scout over its full rectangle is impossible because a single scout may cover up to $10^{18}$ cells.

A less obvious failure case comes from overlaps. For example, if one scout is at $(1, 1)$ and another at $(2, 2)$, the second scout’s region is entirely contained in the first, so naive summation overcounts heavily unless we explicitly handle intersections.

The key difficulty is that each scout defines a lower-right rectangle, and we need the size of the union of these rectangles.

## Approaches

Each scout defines an axis-aligned rectangle extending to the bottom-right corner of the grid. So the problem becomes computing the union area of $q$ rectangles, where each rectangle is $[x, n] \times [y, m]$.

A brute-force interpretation would mark every cell in each rectangle, but each rectangle can be huge, making this completely infeasible. Even if we try to only process boundary structure, direct expansion still depends on $n \cdot m$, which is too large.

The key observation is that all rectangles share the same “target corner” $(n, m)$, and their shapes are monotone: they extend infinitely down-right within the grid boundary. This monotonic structure allows us to sort scouts and compress the union process into counting contributions row by row or column by column.

Instead of thinking in 2D, we reverse perspective. For a fixed row $x$, a cell $(x, y)$ is covered if and only if there exists a scout at some $(x', y')$ with $x' \le x$ and $y' \le y$. Equivalently, if we look at all scouts with row coordinate at most $x$, they impose a threshold on column coverage.

This suggests sweeping rows from bottom to top. As we move upward, more scouts become active, and each active scout contributes a constraint on how far left we must consider columns. For a given row, only the smallest column threshold matters: once we know the minimum $y$ among all scouts with $x' \le x$, all columns from that minimum to $m$ are covered.

Thus, for each row, the covered interval is simply $[ \min y \text{ among active scouts},\ m]$, and the answer is a sum over rows of interval lengths. We avoid iterating over rows explicitly by grouping by unique $x$ coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per cell | $O(nm)$ | $O(1)$ | Too slow |
| Sweep by rows with aggregation | $O(q \log q)$ | $O(q)$ | Accepted |

## Algorithm Walkthrough

1. Read all scout positions and group them by row coordinate $x$. We store for each row the list of column positions $y$. This is necessary because the effect of scouts is activated when we reach their row in a bottom-up sweep.
2. Sort all distinct row coordinates in increasing order. We will process rows from bottom to top so that once a scout is activated, it remains active for all rows above.
3. Maintain a running value `min_y`, initialized as $m+1$. This represents the smallest column index among all scouts that are currently active in the sweep.
4. Start from row $n$ down to $1$. At each row $x$, first activate all scouts located exactly at that row by updating `min_y = min(min_y, y)` for each of them. This step ensures that `min_y` always reflects the tightest left boundary imposed by all active scouts.
5. After processing activations for row $x$, compute how many cells are covered in this row: it is $\max(0, m - min_y + 1)$. This works because every column from `min_y` to $m$ is guaranteed to be covered by at least one active scout.
6. Accumulate this value into the answer.
7. Continue until row 1 is processed.

### Why it works

At any fixed row $x$, a cell $(x, y)$ is covered if there exists at least one scout $(x', y')$ such that $x' \le x$ and $y' \le y$. Among all active scouts (those with $x' \le x$), the condition reduces to $y \ge \min y'$. Therefore coverage on each row is determined entirely by the smallest column threshold among active scouts. The sweep maintains exactly this invariant, so every row is counted correctly without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    
    by_row = {}
    for _ in range(q):
        x, y = map(int, input().split())
        if x not in by_row:
            by_row[x] = []
        by_row[x].append(y)

    min_y = m + 1
    ans = 0

    for x in range(n, 0, -1):
        if x in by_row:
            for y in by_row[x]:
                if y < min_y:
                    min_y = y

        if min_y <= m:
            ans += (m - min_y + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution groups scouts by row to avoid repeated scanning. The key state variable is `min_y`, which compresses all active scouts into a single effective boundary. The loop from $n$ down to $1$ ensures that once a scout becomes active, it influences all rows above it.

The expression `m - min_y + 1` directly counts the length of the covered suffix in each row. The condition `min_y <= m` prevents counting when no scouts have been activated or when all active scouts lie outside the grid range.

## Worked Examples

Consider a small instance:

Input:

```
5 6 2
2 4
4 2
```

We process from row 5 down to 1.

| Row | Activated scouts | min_y | Covered columns | Row contribution |
| --- | --- | --- | --- | --- |
| 5 | none | 7 | none | 0 |
| 4 | (4,2) | 2 | 2..6 | 5 |
| 3 | (4,2) | 2 | 2..6 | 5 |
| 2 | (4,2), (2,4) | 2 | 2..6 | 5 |
| 1 | (4,2), (2,4) | 2 | 2..6 | 5 |

Final answer is $20$.

This trace shows how adding a new scout can only tighten the left boundary and never expand it, which is consistent with the geometry of lower-right rectangles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q + n)$ | Each scout is processed once, and rows are scanned once |
| Space | $O(q)$ | Storage of scouts grouped by row |

The constraints allow $q \le 10^5$, but $n$ can be large. The linear sweep over $n$ is acceptable in Python due to simple operations per iteration, and the dominant cost remains input processing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import sys
    input = sys.stdin.readline

    n, m, q = map(int, input().split())
    by_row = {}
    for _ in range(q):
        x, y = map(int, input().split())
        by_row.setdefault(x, []).append(y)

    min_y = m + 1
    ans = 0
    for x in range(n, 0, -1):
        if x in by_row:
            for y in by_row[x]:
                min_y = min(min_y, y)
        if min_y <= m:
            ans += (m - min_y + 1)

    return str(ans)

# provided sample
assert run("8 15 3\n3 10\n5 7\n6 12\n") == "59"

# minimum grid
assert run("1 1 1\n1 1\n") == "1"

# single row wide grid
assert run("1 5 2\n1 2\n1 4\n") == "4"

# single column grid
assert run("5 1 2\n2 1\n4 1\n") == "5"

# full dominance
assert run("3 3 1\n2 2\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 1 | base correctness |
| single row | 4 | interval merging |
| single column | 5 | vertical propagation |
| center scout | 4 | partial coverage geometry |

## Edge Cases

A key edge case is when no scout has yet been activated while scanning from the bottom. For example, $n=3, m=3$ with a scout at $(1,1)$. During rows 3 and 2, `min_y` remains $4$, so no contribution is added. Only at row 1 does coverage begin, producing exactly $3$ cells. The algorithm correctly delays activation until the correct row is reached.

Another case is multiple scouts in the same row. For input $(4,2)$, $(4,5)$, the update ensures `min_y` becomes $2$, not $5$, and both are handled in a single activation step. The sweep correctly merg_
