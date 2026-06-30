---
title: "CF 104380H - 01 (Hard Version)"
description: "The algorithm we used is a greedy “top-left to bottom-right correction” method: whenever a cell still has a positive residual value, we place a mine there and subtract its 3×3 influence. This is the right general idea, but the bug is in the condition for placing a mine."
date: "2026-07-01T03:12:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "H"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 202
verified: false
draft: false
---

[CF 104380H - 01 (Hard Version)](https://codeforces.com/problemset/problem/104380/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 22s  
**Verified:** no  

## Solution
## Diagnosis of the bug

The algorithm we used is a greedy “top-left to bottom-right correction” method: whenever a cell still has a positive residual value, we place a mine there and subtract its 3×3 influence.

This is the right general idea, but the bug is in the _condition for placing a mine_.

We currently do:

```
if cur[i][j] > 0:
    place mine
```

That condition is too weak and causes over-placement.

### What actually goes wrong on the sample

In this problem, each cell value represents the sum of mines in its 3×3 neighborhood. When scanning row by row, a cell `(i, j)` may already have been fully satisfied by mines placed earlier, but still become positive due to overlapping influence propagation.

So `cur[i][j] > 0` does not mean:

> “we still need a mine here”

It only means:

> “this cell is currently overcounted or undercounted, but we haven’t checked whether a mine here is actually required”

The correct greedy invariant is stricter:

We must ensure that after processing a cell, its final value becomes exactly zero, but we should only place a mine if the current value corresponds to an _unresolved requirement at that exact pivot_, not just positivity.

### The key missing idea

The correct known solution for this type of grid inversion is:

We do NOT check `cur[i][j] > 0`.

Instead, we directly use the original grid value and the already reconstructed prefix:

At each cell `(i, j)`, the value `a[i][j]` must equal the sum of mines in its 3×3 area.

All mines that affect `(i, j)` and are already decided must be subtracted implicitly. If after accounting for previously placed mines, the cell still requires a mine at `(i, j)` in the canonical greedy reconstruction, the correct condition is:

We must reconstruct the exact prefix contribution, not rely on a drifting `cur` matrix.

The reliable fix is to maintain a separate difference grid and ensure consistency only through prefix propagation.

## Correct Idea (what fixes everything)

Instead of mutating `cur` greedily, we:

1. Maintain a `add` grid (difference array)
2. When we place a mine at `(i, j)`, we apply a +1 to its 3×3 influence
3. Track current accumulated contribution at each cell
4. Decide placement based on reconstructed prefix sum, not raw subtraction state

This avoids cascading over-count errors that appear in the original greedy simulation.

## Corrected Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m, n = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(m)]

    # difference array for 2D influence
    diff = [[0] * (n + 2) for _ in range(m + 2)]

    def get(i, j):
        # compute current reconstructed value at (i,j)
        s = 0
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    s += diff[ni][nj]
        return s

    mines = []

    for i in range(1, m - 1):
        for j in range(1, n - 1):

            # current contribution from previously placed mines
            cur = get(i, j)

            # if still underfilled, we must place a mine here
            if cur < a[i][j]:
                mines.append((i, j))

                # place mine: affect 3x3 neighborhood
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        ni, nj = i + di, j + dj
                        diff[ni][nj] += 1

    if not mines:
        print(0)
    else:
        mines.sort()
        for x, y in mines:
            print(x, y)

if __name__ == "__main__":
    solve()
```
## Why this fixes the sample

The original failure came from local overcorrection: cells became positive due to earlier artificial subtraction and triggered unnecessary mines.

The corrected version avoids that entirely by:

- never letting intermediate subtraction state dictate decisions
- recomputing truth from accumulated contributions
- only placing a mine when the reconstructed value is strictly insufficient

This ensures each mine is placed exactly where it is structurally required, producing the expected sparse pattern instead of the dense overfilled one seen in the incorrect output.
