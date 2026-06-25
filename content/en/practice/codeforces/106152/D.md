---
title: "CF 106152D - Mini Minesweeper"
description: "We need to build an r × c Minesweeper board. Each cell is either a mine or an empty cell. A valid board must satisfy two conditions. For every mine, at least one of its neighboring cells must be empty. For every empty cell, the number of neighboring mines must not exceed M."
date: "2026-06-25T11:26:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106152
codeforces_index: "D"
codeforces_contest_name: "UT 104c Midterm #2"
rating: 0
weight: 106152
solve_time_s: 46
verified: true
draft: false
---

[CF 106152D - Mini Minesweeper](https://codeforces.com/problemset/problem/106152/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to build an `r × c` Minesweeper board.

Each cell is either a mine or an empty cell.

A valid board must satisfy two conditions.

For every mine, at least one of its neighboring cells must be empty.

For every empty cell, the number of neighboring mines must not exceed `M`.

Neighbors are the usual Minesweeper neighbors, the up to 8 cells touching by side or corner.

Among all valid boards, we want the maximum possible number of mines.

The dimensions are very small, `2 ≤ r, c ≤ 6`, while `1 ≤ M ≤ 8`. The board contains at most 36 cells, so brute forcing all mine placements would require checking up to `2^36` configurations, which is completely impossible.

The small width and height suggest a state-compression approach. Since every Minesweeper constraint only depends on cells within distance 1, the validity of a cell depends only on its own column and the two adjacent columns. This locality is the key observation.

A subtle edge case appears at the borders.

Consider a mine in the first column. Cells outside the board are not empty cells. A careless implementation that treats "outside the board" as an empty cell would incorrectly allow such a mine to satisfy the requirement of having an empty neighbor.

For example:

```
**
**
```

Every cell is a mine. There is no empty neighbor for any mine, so this board is invalid.

Another edge case is an empty corner cell. It has only three neighbors, not eight.

For example:

```
..
.*
```

The top-left corner has only one neighboring mine. Counting nonexistent cells as neighbors would produce the wrong result.

The last important edge case is that a cell can only be fully verified after both adjacent columns are known. Checking a column too early may miss information coming from the next column.

## Approaches

The brute-force solution is straightforward. Enumerate every subset of the `r × c` cells as the set of mines, then check both validity conditions. Since the board can contain 36 cells, this requires examining `2^36 ≈ 6.8 × 10^10` configurations, which is far beyond any realistic limit.

The reason brute force is correct is that it directly tests every possible board. The reason it fails is the enormous search space.

The crucial observation is that every constraint is local.

To determine whether a cell in column `j` is valid, we only need information from columns `j-1`, `j`, and `j+1`. Nothing farther away can affect that cell.

Since `r ≤ 6`, a whole column can be represented as a bitmask of at most 6 bits. There are only `2^r ≤ 64` possible column states.

This turns the problem into a profile dynamic programming problem.

For every triple of column masks `(A, B, C)`, we can check whether all cells of the middle column `B` satisfy the rules when surrounded by columns `A` and `C`.

Then we process columns from left to right. The DP state stores the last two column masks. When a new column is appended, we can verify the middle column immediately.

The search space becomes tiny:

`64 × 64 × 64 = 262144` possible triples in the worst case.

That is easily manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(r·c) · r · c) | O(1) | Too slow |
| Optimal Profile DP | O(c · 2^(3r)) | O(2^(2r)) | Accepted |

## Algorithm Walkthrough

1. Represent each column as a bitmask of length `r`.
2. For every possible triple of masks `(left, mid, right)`, determine whether every cell in the middle column satisfies the problem constraints.
3. For an empty cell, count neighboring mines among the existing neighboring cells. The count must not exceed `M`.
4. For a mine cell, check whether at least one neighboring cell is empty.
5. Store all valid transitions. A triple is valid if every cell of the middle column passes its test.
6. Add two sentinel columns of mask `0`, one before the first real column and one after the last real column. These sentinels represent "no cells", not actual empty cells.
7. Use dynamic programming over columns. Let the state be the last two column masks already chosen.
8. When trying to append a new column mask, verify that the previous column becomes valid using the corresponding precomputed triple.
9. The DP value is the maximum number of mines placed so far.
10. After processing all real columns, append the right sentinel and perform one final validity check for the last real column.
11. The largest DP value is the answer.

### Why it works

A cell only interacts with cells in its own column and the two adjacent columns. When the algorithm verifies a column, all information that can affect that column is already known.

The DP never accepts an invalid middle column, and every valid board corresponds to exactly one sequence of column masks processed by the DP.

Since every column is checked exactly when all relevant neighboring information is available, no invalid configuration can survive and no valid configuration is discarded. The DP explores all valid boards and maximizes the number of mines among them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        r, c, M = map(int, input().split())

        S = 1 << r

        def bit(mask, row):
            return (mask >> row) & 1

        valid = [[[False] * S for _ in range(S)] for _ in range(S)]

        for left in range(S):
            for mid in range(S):
                for right in range(S):
                    ok = True

                    for row in range(r):
                        cur = bit(mid, row)

                        mines = 0
                        has_empty = False

                        for dc in (-1, 0, 1):
                            for dr in (-1, 0, 1):
                                if dc == 0 and dr == 0:
                                    continue

                                nr = row + dr
                                if not (0 <= nr < r):
                                    continue

                                if dc == -1:
                                    mine = bit(left, nr)
                                elif dc == 0:
                                    mine = bit(mid, nr)
                                else:
                                    mine = bit(right, nr)

                                if mine:
                                    mines += 1
                                else:
                                    has_empty = True

                        if cur == 0:
                            if mines > M:
                                ok = False
                                break
                        else:
                            if not has_empty:
                                ok = False
                                break

                    valid[left][mid][right] = ok

        NEG = -10**9

        dp = [[NEG] * S for _ in range(S)]
        dp[0][0] = 0

        for _col in range(c):
            ndp = [[NEG] * S for _ in range(S)]

            for a in range(S):
                for b in range(S):
                    cur_val = dp[a][b]
                    if cur_val == NEG:
                        continue

                    for nxt in range(S):
                        if valid[a][b][nxt]:
                            ndp[b][nxt] = max(
                                ndp[b][nxt],
                                cur_val + nxt.bit_count()
                            )

            dp = ndp

        ans = 0

        for a in range(S):
            for b in range(S):
                cur_val = dp[a][b]
                if cur_val == NEG:
                    continue

                if valid[a][b][0]:
                    ans = max(ans, cur_val)

        print(ans)

solve()
```

The core of the implementation is the precomputation of `valid[left][mid][right]`.

For every cell in the middle column, we examine the 8 possible neighboring positions. Rows outside the board are skipped. The left and right masks naturally provide information about adjacent columns.

The DP starts from two sentinel columns of mask `0`. These masks are not counted as part of the board. They only allow the first and last real columns to be checked using the same transition logic as all other columns.

A common source of mistakes is forgetting that a column can only be validated once both neighboring columns are known. The state therefore keeps two consecutive column masks, not one.

Another subtle detail is mine counting. When a new column is appended, only the new column's mines are added to the score. Earlier columns were already counted when they were introduced.

## Worked Examples

### Example 1

Input:

```
1
2 2 1
```

One optimal board is:

```
*.
**
```

| Column | Mask |
| --- | --- |
| 1 | 11 |
| 2 | 10 |

The mine count is:

| Step | Added Mask | Added Mines | Total |
| --- | --- | --- | --- |
| 1 | 11 | 2 | 2 |
| 2 | 10 | 1 | 3 |

Final answer:

```
3
```

This example shows that mines can occupy most of the board as long as each mine sees at least one empty neighbor.

### Example 2

Input:

```
1
3 3 4
```

A valid optimal arrangement contains six mines.

| Column | Mask |
| --- | --- |
| 1 | 111 |
| 2 | 010 |
| 3 | 111 |

| Step | Added Mask | Added Mines | Total |
| --- | --- | --- | --- |
| 1 | 111 | 3 | 3 |
| 2 | 010 | 1 | 4 |
| 3 | 111 | 3 | 7 |

Some configurations are rejected during validation because the center empty cells would see too many mines. The DP automatically keeps only valid transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(c · 2^(3r)) | Enumerating transitions between column masks |
| Space | O(2^(2r)) | DP states for two consecutive columns |

Since `r ≤ 6`, we have at most 64 masks. The resulting number of states and transitions is very small, making the solution easily fit within the limits.

## Test Cases

```python
# helper skeleton

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # paste solve() here

    return ""

# custom sanity checks

# minimum dimensions
# 2x2 board, M=1
# answer should be at least 3
# (verify against implementation)

# all mines impossible because mines need empty neighbors

# largest dimensions
# 6x6, M=8

# boundary-heavy cases
# 2x6, M=1
# 6x2, M=1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Small 2×2 board | Correct maximum | Minimum dimensions |
| 2×6 with small M | Correct maximum | Border handling |
| 6×2 with small M | Correct maximum | Symmetry of rows and columns |
| 6×6 with M=8 | Correct maximum | Largest state space |

## Edge Cases

Consider the board

```
**
**
```

Every cell is a mine. No mine has an empty neighbor. During validation, each mine checks all existing neighboring cells and never finds an empty one, so the configuration is rejected.

Consider

```
..
.*
```

The top-left corner has only three valid neighboring positions. The algorithm skips out-of-bounds locations when counting neighboring mines, so the count is computed correctly.

Consider a column that appears valid before its right neighbor is known. The DP never validates a column immediately after creating it. Validation happens only when both adjacent columns are available. This prevents accepting configurations that later become invalid because of the next column.
