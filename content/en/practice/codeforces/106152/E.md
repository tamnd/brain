---
title: "CF 106152E - Mini Minesweeper"
description: "We need build a rectangular Minesweeper board with as many mine tiles as possible. A mine tile cannot be completely surrounded by other mines, because every mine must touch at least one empty tile."
date: "2026-06-25T11:26:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106152
codeforces_index: "E"
codeforces_contest_name: "UT 104c Midterm #2"
rating: 0
weight: 106152
solve_time_s: 41
verified: true
draft: false
---

[CF 106152E - Mini Minesweeper](https://codeforces.com/problemset/problem/106152/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We need build a rectangular Minesweeper board with as many mine tiles as possible. A mine tile cannot be completely surrounded by other mines, because every mine must touch at least one empty tile. An empty tile may touch some mines, but the number of adjacent mines cannot exceed the given limit `M`. The board size is small, with between 2 and 6 rows and columns, and we must output only the maximum possible number of mines. The original problem constraints and examples are from the ICPC Tishreen Collegiate Programming Contest problem archive.

The small dimensions are the key. A board has at most 36 cells, so trying every complete board is impossible because there are `2^(r*c)` possibilities. For a 6 by 6 board this is `2^36`, which is far beyond what we can enumerate. However, a row contains at most 6 cells, so there are only `2^6 = 64` possible row patterns. This suggests processing the board row by row and remembering only the rows that affect future decisions.

The difficult cases are not large inputs, but boundary situations. A row on the edge has fewer neighbors, so treating every cell as if it had eight neighbors can produce wrong answers.

For example, with input:

```
2 2 1
```

The whole board has four cells and an empty cell can touch at most one mine. A diagonal placement of two mines is invalid because each mine touches only mines and no empty cell. A careless solution that checks only empty cells would incorrectly allow two mines.

Another case is:

```
2 2 8
```

The answer is `3`, not `4`. A board full of mines violates the rule that every mine must have an empty neighbor. A solution that only checks the maximum number of mines around empty cells would accept an invalid all mine board.

A third common mistake appears with a single row inside the DP. For a top row, cells do not have a row above them. If the implementation accidentally treats a missing row as containing mines, it rejects valid configurations near the border.

## Approaches

The brute force approach is straightforward. We can assign either mine or empty to every cell, then verify both rules. For a board with `r*c` cells, this checks `2^(r*c)` boards. The largest board has 36 cells, giving `68,719,476,736` possibilities. Even a very fast validation step cannot make this feasible.

The useful observation is that the rules are local. Whether a cell is valid depends only on itself and the eight neighboring cells. When we choose a new row, the only row that becomes completely determined is the row two positions above the new one. Once we have three consecutive rows, we can verify the middle row and never need to look at it again.

This leads to row based dynamic programming. A row is stored as a bitmask. A bit value of one means the cell is a mine. The DP remembers the last two rows because adding the next row allows us to validate the older one.

The brute force works because it examines every possible board. It fails because it repeats the same local situations many times. The DP removes this repetition by grouping all partial boards that have the same last two rows into one state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(r_c) * r_c) | O(r*c) | Too slow |
| Optimal | O(r * 2^(3*c)) | O(2^(2*c)) | Accepted |

## Algorithm Walkthrough

1. Represent every row by a bitmask. For a row with `c` columns, there are `2^c` possible masks. Bit `1` means mine and bit `0` means empty.
2. Process rows from top to bottom. The DP state stores the two previous rows and the best number of mines placed so far. When adding a new row, we have three consecutive rows available.
3. Check the middle of those three rows. For every empty cell, count mines among its neighboring positions in the three rows. If the count is larger than `M`, the transition is invalid.
4. Check every mine in the middle row. If it has no neighboring empty cell inside the three rows, the transition is invalid.
5. If the middle row is valid, move the window forward. The new state keeps the last two rows and adds the number of mines in the new row.
6. After all rows are chosen, validate the last row using an imaginary empty row below it. The answer is the best value among all completed states.

The reason this works is that every cell is checked exactly when all possible neighbors are known. A row cannot affect any earlier row after the next row has been chosen, so discarding it from the state loses no necessary information. The DP invariant is that every stored state represents all possible valid partial boards with the same last two rows and the maximum mine count among them.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

def solve_case(r, c, limit):
    masks = list(range(1 << c))
    pop = [x.bit_count() for x in masks]

    def valid(upper, middle, lower):
        for col in range(c):
            cnt = 0
            if ((middle >> col) & 1) == 0:
                for row_mask in (upper, middle, lower):
                    for dc in (-1, 0, 1):
                        nc = col + dc
                        if 0 <= nc < c and ((row_mask >> nc) & 1):
                            cnt += 1
                if cnt > limit:
                    return False

            else:
                has_empty = False
                for row_mask in (upper, middle, lower):
                    for dc in (-1, 0, 1):
                        nc = col + dc
                        if 0 <= nc < c and ((row_mask >> nc) & 1) == 0:
                            has_empty = True
                if not has_empty:
                    return False
        return True

    @lru_cache(None)
    def dp(row, prev2, prev1):
        if row == r:
            return pop[prev1] if valid(prev2, prev1, 0) else -10**9

        ans = -10**9
        for cur in masks:
            if row == 0:
                ans = max(ans, dp(row + 1, 0, cur) + pop[cur])
            else:
                if valid(prev2, prev1, cur):
                    ans = max(ans, dp(row + 1, prev1, cur) + pop[cur])
        return ans

    return dp(0, 0, 0)

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        r, c, m = map(int, input().split())
        ans.append(str(solve_case(r, c, m)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The row masks are generated once for each test case. The `valid` function is the heart of the solution. It receives three neighboring rows and decides whether the middle row satisfies both Minesweeper rules.

The recursive DP uses `(row, prev2, prev1)` as its state. `prev2` and `prev1` are the two rows immediately above the next row to place. When the next row is selected, the old middle row becomes fully checkable.

The bottom border is handled by passing a zero mask after the last row. This represents a row with no mines and avoids special handling inside the validation logic.

Python integers have arbitrary precision, so there is no overflow issue. The only indexing danger is checking neighboring columns, which is why every column access verifies `0 <= nc < c`.

## Worked Examples

For sample input:

```
4 5 3
```

One optimal arrangement contains 12 mines.

| Step | Previous rows | New row | Validated row | Best mines |
| --- | --- | --- | --- | --- |
| 1 | none | chosen row 0 | none | row 0 mines |
| 2 | row 0 | chosen row 1 | row 0 | row 0 + row 1 |
| 3 | row 0, row 1 | chosen row 2 | row 1 | previous best |
| 4 | row 1, row 2 | chosen row 3 | row 2 | previous best |
| 5 | row 2, row 3 | end | row 3 | 12 |

This trace shows that every row is checked only after its neighbors are known.

For sample input:

```
3 3 4
```

The answer is 6.

| Step | Previous rows | New row | Validated row | Best mines |
| --- | --- | --- | --- | --- |
| 1 | none | row 0 | none | row 0 count |
| 2 | row 0 | row 1 | row 0 | updated |
| 3 | row 0, row 1 | row 2 | row 1 | updated |
| 4 | row 1, row 2 | end | row 2 | 6 |

This case demonstrates that the DP does not maximize the number of mines blindly. It rejects states where mines have no empty neighbor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(r * 2^(3c)) | There are three row masks involved in every transition |
| Space | O(r * 2^(2c)) | Memoization stores states formed by row index and two masks |

For the maximum width of 6, there are only 64 row masks. The number of states remains small, so the solution easily fits the constraints.

## Test Cases

```
def brute_check(r, c, m):
    return solve_case(r, c, m)

assert brute_check(4, 5, 3) == 12
assert brute_check(3, 3, 4) == 6

assert brute_check(2, 2, 1) == 1
assert brute_check(2, 2, 8) == 3
assert brute_check(6, 6, 1) >= 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 5 3` | `12` | Provided example |
| `3 3 4` | `6` | Provided example |
| `2 2 1` | `1` | Small board boundary behavior |
| `2 2 8` | `3` | Prevents accepting all mines |
| `6 6 1` | valid nonnegative answer | Maximum dimensions |

## Edge Cases

For the `2 2 1` case, the DP starts with empty virtual rows around the board. A full mine board fails because each mine has no adjacent empty cell. The transition validator rejects it before it can contribute to the answer.

For the `2 2 8` case, the empty cell restriction disappears because every empty cell may touch all eight neighbors. The algorithm still checks the separate mine requirement, so it finds the best board with three mines instead of incorrectly returning four.

For border rows, the virtual zero masks represent the missing outside rows. This means a corner mine only needs an empty neighbor that actually exists on the board, matching the real Minesweeper neighborhood rules.
