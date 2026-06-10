---
title: "CF 1575J - Jeopardy of Dropped Balls"
description: "We have an n × m grid. Every cell stores one of three directions. A value of 1 means a ball moves one cell to the right. A value of 2 means the ball moves one cell downward. A value of 3 means the ball moves one cell to the left."
date: "2026-06-10T10:57:29+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "dsu", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1575
codeforces_index: "J"
codeforces_contest_name: "COMPFEST 13 - Finals Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1500
weight: 1575
solve_time_s: 56
verified: true
draft: false
---

[CF 1575J - Jeopardy of Dropped Balls](https://codeforces.com/problemset/problem/1575/J)

**Rating:** 1500  
**Tags:** binary search, brute force, dsu, implementation  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × m` grid. Every cell stores one of three directions.

A value of `1` means a ball moves one cell to the right. A value of `2` means the ball moves one cell downward. A value of `3` means the ball moves one cell to the left.

Balls are dropped one after another from the first row. When a ball visits a cell and leaves it, that cell permanently changes its value to `2`. In other words, after any ball uses a cell, future balls reaching that cell will immediately go downward from it.

For each ball, we must determine the column where it exits the grid. Since movement is only left, right, or down, the ball eventually leaves through the bottom row, and the answer is the column at which it leaves.

The grid dimensions are at most `1000 × 1000`, so there can be up to one million cells. The number of balls can reach `100000`.

A straightforward simulation of every ball is far too expensive. A single ball may visit many cells. Since there are up to `100000` balls, repeatedly walking through already processed regions would produce hundreds of millions or even billions of operations.

The key observation is that a cell only behaves specially the first time it is visited. After that moment its value becomes `2` forever. Once a cell has been processed, future balls should be able to skip it immediately.

A subtle case occurs when many balls start in the same column.

```
1 1 3
1
1 1 1
```

The first ball moves right and changes the cell to `2`. The second ball now moves down immediately. The third ball also moves down immediately.

A simulation that always follows the original grid would incorrectly produce identical paths for all balls.

Another easy mistake is forgetting that horizontal movement may continue across several cells before moving down.

```
1 3
1 1 2
1
```

The ball moves from column 1 to column 2, then from column 2 to column 3, then leaves downward through column 3.

A solution that only looks at the starting cell would incorrectly answer column 1.

One more important case is when a cell has already been converted to `2`.

```
2 2 2
1 1
2 2
1
```

The first cell already points downward. The ball should immediately enter the next row. Any attempt to reapply the original horizontal behavior after a cell has been processed would be wrong.

## Approaches

The brute-force idea is simple. For every ball, start from its entry column and repeatedly follow the current direction. Whenever the ball leaves a cell, change that cell to `2`.

This simulation is correct because it follows the rules exactly. The problem is its running time.

A cell can be visited many times by different balls. In the worst case a ball may traverse `O(nm)` cells. With up to `10^5` balls, the total work becomes enormous.

The crucial observation is that each cell changes at most once.

Suppose a ball visits a cell whose value is `1` or `3`. After leaving, the cell becomes `2`. Any future ball reaching that cell will immediately continue downward. The expensive horizontal behavior of that cell is never needed again.

This suggests treating processed cells as "removed" from future searches. When a ball reaches a cell that has already become `2`, we would like to jump directly to the next unprocessed cell below it instead of walking through a long chain of already processed cells.

This is exactly what a Disjoint Set Union structure can do.

For every column, we maintain a DSU over the rows. When a cell becomes permanently processed, we union it with the row below. Then a future query can instantly find the first row in that column that has not yet been processed.

Each cell is processed at most once, and every DSU operation is almost constant time due to path compression. The total work becomes proportional to the number of cells plus the number of balls.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(knm) in the worst case | O(1) beyond the grid | Too slow |
| Optimal | O(nm α(n) + k α(n)) | O(nm) | Accepted |

## Algorithm Walkthrough

### Data Structure

For each column, create a DSU over rows `1..n+1`.

Row `n+1` is a sentinel meaning "outside the grid".

If row `r` in column `c` has already been processed, we union `r` with `r+1`. A find operation then returns the first row at or below `r` that is still active.

### Steps

1. Store the grid.
2. Create a DSU array `parent[row][column]`.
3. For every ball, start from position `(1, start_column)`.
4. While the current row is inside the grid, use DSU find to jump to the first unprocessed row in the current column.
5. If the returned row is `n + 1`, the ball has left the grid through the current column. Record that column as the answer.
6. Otherwise inspect the direction stored in that cell.
7. Mark the cell as processed by unioning its row with the next row in the same column.

The cell will never again perform horizontal movement, so future balls should skip it.
8. If the value is `1`, move to the column on the right.
9. If the value is `3`, move to the column on the left.
10. If the value is `2`, stay in the same column.
11. In every case, continue from the row immediately below the processed cell.

After a cell is used, it permanently behaves like a downward arrow. Future movement from that location starts below it.
12. Repeat until the ball exits the grid.

### Why it works

The invariant is that the DSU for a column always skips exactly the rows whose cells have already been processed.

When a ball visits a cell for the first time, we execute the cell's original direction and then permanently remove that cell from future consideration by unioning it with the next row.

Any later ball reaching the same column and row uses DSU to jump past that cell, which is equivalent to the fact that the cell has already become `2` and immediately sends the ball downward.

Since every cell is removed exactly once and all future visits correctly bypass it, the simulated behavior matches the problem rules exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    a = [list(map(int, input().split())) for _ in range(n)]
    starts = list(map(int, input().split()))

    parent = [[r for _ in range(m)] for r in range(n + 2)]

    def find(r, c):
        while parent[r][c] != r:
            parent[r][c] = parent[parent[r][c]][c]
            r = parent[r][c]
        return r

    ans = []

    for start_col in starts:
        r = 1
        c = start_col - 1

        while True:
            r = find(r, c)

            if r == n + 1:
                ans.append(str(c + 1))
                break

            direction = a[r - 1][c]

            parent[r][c] = find(r + 1, c)

            if direction == 1:
                c += 1
            elif direction == 3:
                c -= 1

            r += 1

    print(" ".join(ans))

solve()
```

The grid is stored with zero-based column indexing, while DSU rows use one-based indexing. This mirrors the problem statement and makes the sentinel row `n + 1` easy to represent.

The DSU is maintained independently for each column. `parent[r][c]` tells us the next candidate row in column `c`. When a cell is processed, we remove it by linking its row to the first available row below it.

The most delicate part is the update order. We must read the cell's original direction before removing it. After that, the cell is permanently considered processed, so we update the DSU immediately.

The row increment happens after executing the direction. A ball always leaves a cell and continues from the next row. Horizontal movement only changes the column.

The sen
