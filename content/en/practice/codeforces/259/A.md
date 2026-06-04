---
title: "CF 259A - Little Elephant and Chess"
description: "We are given an 8×8 board where each cell is either white (W) or black (B). The goal is to determine whether this board can be transformed into a standard chessboard. A standard chessboard has alternating colors both horizontally and vertically."
date: "2026-06-04T17:39:39+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "strings"]
categories: ["algorithms"]
codeforces_contest: 259
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 157 (Div. 2)"
rating: 1000
weight: 259
solve_time_s: 155
verified: true
draft: false
---

[CF 259A - Little Elephant and Chess](https://codeforces.com/problemset/problem/259/A)

**Rating:** 1000  
**Tags:** brute force, strings  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an 8×8 board where each cell is either white (`W`) or black (`B`). The goal is to determine whether this board can be transformed into a standard chessboard.

A standard chessboard has alternating colors both horizontally and vertically. Since the upper-left corner must be white, there are only two valid row patterns:

```
WBWBWBWB
BWBWBWBW
```

Rows must alternate between these two patterns.

The only operation allowed is to choose a row and perform a cyclic right shift any number of times. Since a row contains exactly eight cells, repeated shifts can rotate the row into any of its eight cyclic positions.

The board size is fixed at 8×8. That means even an exhaustive search would be tiny. There are only eight rows and each row has length eight, so any algorithm that examines all cells several times is easily fast enough. The challenge is not efficiency but recognizing the structure created by cyclic shifts.

A subtle observation is that shifting an alternating row by one position simply swaps it between the two valid chessboard patterns. For example:

```
WBWBWBWB  -> shift once ->  BWBWBWBW
```

A shift by two positions returns it to the original pattern. Since the row length is even, every cyclic shift of an alternating row produces one of these two patterns and nothing else.

The main edge case is a row that is not alternating internally.

Example:

```
WWWBWBWB
```

No amount of cyclic shifting can remove the adjacent equal `W`s. Any rotation still contains a pair of neighboring equal cells somewhere in the row. The correct answer is `NO`.

Another easy mistake is checking only whether each row can become either valid alternating pattern independently.

Example:

```
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
```

Every row is individually valid, but a proper chessboard requires neighboring rows to be different. The correct answer is still `YES`, because we may shift every second row once and obtain the alternating row sequence. A solution that only compares rows to their current positions would incorrectly reject this case.

A final edge case is a board that already forms a proper chessboard. The answer must be `YES` because using zero operations is allowed.

## Approaches

The most direct brute-force idea is to try every possible cyclic shift for every row and check whether the resulting board is a valid chessboard.

Each row has 8 possible rotations, so there are:

$$8^8 = 16,777,216$$

possible configurations. Even though the board is small, checking more than sixteen million states is unnecessary.

The key observation comes from studying a single row. For a row to appear in a valid chessboard, its colors must alternate. Since the row length is even, every cyclic shift preserves the alternating property. More importantly, an alternating row can only rotate into one of two patterns:

```
WBWBWBWB
BWBWBWBW
```

If a row is not alternating, no rotation can ever make it alternating.

This reduces the problem dramatically. Instead of considering all possible shifts, we only need to verify that every row is alternating internally. Once that is true, each row can be rotated into whichever of the two chessboard row patterns we need.

For odd-numbered rows of the target chessboard we need:

```
WBWBWBWB
```

For even-numbered rows we need:

```
BWBWBWBW
```

Since every alternating row can be transformed into either pattern by choosing an appropriate parity of shifts, the entire board is feasible if and only if every row is alternating.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8^8 · 64) | O(64) | Unnecessary |
| Optimal | O(64) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the eight rows of the board.
2. For each row, examine every pair of adjacent cells inside that row.
3. If any adjacent cells have the same color, immediately output `NO`.

A row in a chessboard must alternate colors. Cyclic shifts only rotate positions, they do not change the order of colors around the cycle. If two neighboring cells in the cycle are equal, that defect can never disappear.
4. If all rows pass the alternating check, output `YES`.

Every row is now an alternating cycle. Because the row length is even, rotating the row can produce either `WBWBWBWB` or `BWBWBWBW`. We can choose the required version independently for each row and construct the standard chessboard.

### Why it works

Consider a row as a cycle of eight cells. A cyclic shift merely changes the starting position on that cycle.

If a row contains two equal neighboring cells somewhere in the cycle, every rotation still contains that same equal pair. Such a row can never become an alternating chessboard row.

Conversely, if every neighboring pair in the cycle has different colors, the row must alternate completely. Since the cycle length is even, the row consists of alternating `W` and `B` around the entire cycle. Rotating such a row can start at either color, producing exactly the two chessboard row patterns.

Because each row can independently become whichever alternating pattern is needed, the whole board can be arranged into a proper chessboard exactly when every row is alternating.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    board = [input().strip() for _ in range(8)]

    for row in board:
        for i in range(7):
            if row[i] == row[i + 1]:
                print("NO")
                return

    print("YES")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the proof.

The outer loop processes all eight rows. For each row, we check the seven adjacent pairs inside the row. If any pair contains identical colors, the row cannot be transformed into an alternating chessboard row by any sequence of cyclic shifts, so we immediately print `NO`.

If every row passes the test, each row is already an alternating sequence. Such rows can be rotated to begin with either color, which allows us to place the required pattern on every board row. We then print `YES`.

A common mistake is trying to simulate shifts. The proof shows that simulation is unnecessary. The only property that matters is whether every row alternates.

## Worked Examples

### Sample 1

Input:

```
WBWBWBWB
BWBWBWBW
BWBWBWBW
BWBWBWBW
WBWBWBWB
WBWBWBWB
BWBWBWBW
WBWBWBWB
```

| Row | Adjacent Equal Pair Found? |
| --- | --- |
| WBWBWBWB | No |
| BWBWBWBW | No |
| BWBWBWBW | No |
| BWBWBWBW | No |
| WBWBWBWB | No |
| WBWBWBWB | No |
| BWBWBWBW | No |
| WBWBWBWB | No |

All rows alternate internally, so the algorithm outputs:

```
YES
```

This example demonstrates that the rows do not need to be in the correct chessboard arrangement initially. Since every row is alternating, suitable rotations can create the required pattern.

### Example 2

Consider:

```
WWWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
```

| Row | First Equal Adjacent Pair |
| --- | --- |
| WWWBWBWB | Positions 1 and 2 |
| BWBWBWBW | None |
| WBWBWBWB | None |
| BWBWBWBW | None |
| WBWBWBWB | None |
| BWBWBWBW | None |
| WBWBWBWB | None |
| BWBWBWBW | None |

The first row contains two consecutive `W`s. No cyclic shift can remove that defect.

Output:

```
NO
```

This example illustrates the key invariant: equal adjacent cells remain adjacent somewhere after every rotation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64) | Eight rows, seven adjacency checks per row |
| Space | O(1) | Only the input board is stored |

The board size is fixed at 8×8, so the running time is effectively constant. The solution is far below the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    board = [input().strip() for _ in range(8)]

    for row in board:
        for i in range(7):
            if row[i] == row[i + 1]:
                return "NO"

    return "YES"

# provided sample
assert run(
"""WBWBWBWB
BWBWBWBW
BWBWBWBW
BWBWBWBW
WBWBWBWB
WBWBWBWB
BWBWBWBW
WBWBWBWB
"""
) == "YES", "sample"

# already a perfect chessboard
assert run(
"""WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
"""
) == "YES", "already valid"

# all white
assert run(
"""WWWWWWWW
WWWWWWWW
WWWWWWWW
WWWWWWWW
WWWWWWWW
WWWWWWWW
WWWWWWWW
WWWWWWWW
"""
) == "NO", "all equal"

# one bad row
assert run(
"""WBWBWBWB
BWBWBWBW
WBWWWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
"""
) == "NO", "single invalid row"

# all rows alternating but identical
assert run(
"""WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
WBWBWBWB
"""
) == "YES", "rows can be shifted independently"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Perfect chessboard | YES | Zero operations allowed |
| All white cells | NO | Adjacent equal colors cannot be fixed |
| One bad row | NO | A single invalid row makes the board impossible |
| All rows equal and alternating | YES | Independent row rotations are sufficient |

## Edge Cases

Consider the board:

```
WWWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
```

The first row contains `WW` at the beginning. During the scan, the algorithm finds `row[0] == row[1]` and immediately returns `NO`. Rotating the row merely moves this pair to another location, so rejection is correct.

Consider a board where every row equals:

```
WBWBWBWB
```

repeated eight times.

The algorithm finds no equal adjacent cells in any row and returns `YES`. This is correct because every second row can be shifted once, producing:

```
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
...
```

which is exactly a proper chessboard.

Consider a board that is already a valid chessboard:

```
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
```

Every row alternates, so the algorithm returns `YES`. Since performing no operations is allowed, this is the correct result.
