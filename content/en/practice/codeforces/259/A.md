---
title: "CF 259A - Little Elephant and Chess"
description: "We are given an 8 × 8 board where every cell is either white (W) or black (B). A valid chessboard has alternating colors in every row and every column. Since the upper-left corner must be white, the only valid pattern is: The allowed operation is unusual."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "strings"]
categories: ["algorithms"]
codeforces_contest: 259
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 157 (Div. 2)"
rating: 1000
weight: 259
solve_time_s: 84
verified: true
draft: false
---

[CF 259A - Little Elephant and Chess](https://codeforces.com/problemset/problem/259/A)

**Rating:** 1000  
**Tags:** brute force, strings  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an 8 × 8 board where every cell is either white (`W`) or black (`B`). A valid chessboard has alternating colors in every row and every column. Since the upper-left corner must be white, the only valid pattern is:

```
WBWBWBWB
BWBWBWBW
WBWBWBWB
...
```

The allowed operation is unusual. We are not allowed to swap arbitrary cells or columns. We may only take a single row and cyclically shift it to the right any number of times. A cyclic shift moves the last character to the front.

The task is to decide whether some sequence of row shifts can transform the given board into a proper chessboard.

The board size is fixed at 8 × 8, so even inefficient approaches are fast enough in practice. Still, the interesting part of the problem is recognizing the structural property hidden inside the rows.

A proper chessboard row always alternates between two colors. That means every valid row must look like one of these two strings:

```
WBWBWBWB
BWBWBWBW
```

A cyclic shift preserves the relative order of characters inside the row. Because of that, a row can only become a valid chessboard row if it already alternates between colors before any shifts are applied.

The most common mistake is checking only the number of white and black cells. For example:

```
WWWWBBBB
```

contains four `W` and four `B`, but no cyclic shift can make it alternating. The correct answer for such a row is impossible.

Another easy bug is forgetting that cyclic shifts can flip the starting color. Consider:

```
BWBWBWBW
```

This row already alternates correctly, just starting with black instead of white. One cyclic shift changes it into:

```
WBWBWBWB
```

So both alternating patterns must be accepted.

A third subtle case is a board where every row alternates, but adjacent rows do not match the chessboard pattern. Example:

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

At first glance this looks close to valid, but rows 1 and 2 start with the same color. Since shifting a row by one position flips its starting color, we can independently choose the parity of each row. This board is actually fixable, so the answer is `YES`.

## Approaches

A direct brute-force strategy is to try every possible shift amount for every row and check whether the final board becomes a proper chessboard.

Each row has 8 possible cyclic shifts. Since there are 8 rows, the total number of boards is:

```
8^8 = 16,777,216
```

For every generated board we would still need to verify all 64 cells. That works mathematically because the constraints are tiny, but it is completely unnecessary.

The reason brute force feels wasteful is that rows are independent. Shifting one row never affects another row. Instead of searching through all combinations, we can ask a simpler question:

"What kinds of rows can ever become alternating after cyclic shifts?"

An alternating row has exactly two possible forms:

```
WBWBWBWB
BWBWBWBW
```

Now comes the key observation. Cyclically shifting either of these rows keeps them alternating. In fact, shifting by one position simply swaps between the two patterns.

That means a row is usable if and only if every adjacent pair of characters inside the row is different.

For example:

```
WBWBWBWB   -> valid
BWBWBWBW   -> valid
WWBBWWBB   -> invalid
```

Once every row alternates internally, we can always shift rows individually so that row `i` starts with the correct color for the chessboard pattern.

So the entire problem reduces to a very small check:

For every row, verify that no two neighboring cells are equal.

If every row passes, answer `YES`. Otherwise answer `NO`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8^8 × 64) | O(1) | Too slow conceptually |
| Optimal | O(64) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all 8 rows of the board.
2. Process each row independently because row shifts never affect other rows.
3. For every row, compare adjacent characters:

```
row[j] and row[j + 1]
```

for all `0 ≤ j < 7`.
4. If two neighboring characters are equal, this row can never become alternating under cyclic shifts.

Example:

```
WWBWBWBW
```

already contains consecutive equal colors, and cyclic shifts preserve that adjacency structure.
5. Immediately print `NO` and terminate if any row fails the check.
6. If all rows alternate internally, print `YES`.

Why it works:

A cyclic shift only rotates positions, it does not change the sequence of equalities between neighboring cells in the cycle. The only rows that can match a chessboard row are the two perfectly alternating patterns. Any cyclic shift of an alternating row remains alternating. So checking whether every row already alternates is both necessary and sufficient.

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

solve()
```

The solution reads the eight rows and checks each row locally.

The inner loop compares neighboring cells inside the row. If two adjacent cells have the same color, the row cannot possibly become a valid chessboard row after any number of cyclic shifts.

The implementation stops immediately after finding an invalid row. Since the answer is already determined at that point, continuing would only waste work.

The loop runs until index `6` because we compare `i` with `i + 1`. Using `range(8)` here would cause an out-of-bounds access.

No extra arrays or simulation are necessary. We never actually perform shifts because the alternating property alone completely determines feasibility.

## Worked Examples

### Example 1

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

Trace:

| Row | Adjacent Equal Found? | Result |
| --- | --- | --- |
| WBWBWBWB | No | Valid |
| BWBWBWBW | No | Valid |
| BWBWBWBW | No | Valid |
| BWBWBWBW | No | Valid |
| WBWBWBWB | No | Valid |
| WBWBWBWB | No | Valid |
| BWBWBWBW | No | Valid |
| WBWBWBWB | No | Valid |

Final output:

```
YES
```

Every row already alternates internally. Some rows start with the wrong color, but a single cyclic shift flips the starting color, so the full chessboard can be constructed.

### Example 2

Input:

```
WWBWBWBW
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
```

Trace:

| Row | First Bad Pair | Result |
| --- | --- | --- |
| WWBWBWBW | W W | Invalid |

Final output:

```
NO
```

The first row already contains consecutive equal colors. Rotating the row only moves the bad pair somewhere else, so the board can never become a proper chessboard.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64) | We inspect each cell at most once |
| Space | O(1) | Only a few loop variables are used |

The board size is fixed at 64 cells, so the program runs instantly within the limits. Memory usage is constant because no auxiliary structures proportional to the input size are allocated.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    board = [input().strip() for _ in range(8)]

    for row in board:
        for i in range(7):
            if row[i] == row[i + 1]:
                print("NO")
                return

    print("YES")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "BWBWBWBW\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
) == "YES", "sample"

# all rows identical but alternating
assert run(
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
    "WBWBWBWB\n"
) == "YES", "rows can be shifted independently"

# completely invalid rows
assert run(
    "WWWWWWWW\n"
    "BBBBBBBB\n"
    "WWWWWWWW\n"
    "BBBBBBBB\n"
    "WWWWWWWW\n"
    "BBBBBBBB\n"
    "WWWWWWWW\n"
    "BBBBBBBB\n"
) == "NO", "equal adjacent cells"

# single bad pair in one row
assert run(
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "WBWWWBWB\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
    "BWBWBWBW\n"
) == "NO", "hidden invalid adjacency"

# already perfect chessboard
assert run(
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
    "BWBWBWBW\n"
    "WBWBWBWB\n"
    "BWBWBWBW\n"
) == "YES", "already valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All rows alternating and identical | YES | Independent row shifts |
| Rows with all equal colors | NO | Consecutive equal cells cannot be repaired |
| One hidden bad pair | NO | Detects local violations correctly |
| Already valid chessboard | YES | No unnecessary modifications |

## Edge Cases

Consider the row:

```
WWBWBWBW
```

Complete input:

```
WWBWBWBW
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
```

The algorithm checks adjacent cells in the first row:

```
W == W
```

The row immediately fails, so the answer is `NO`.

This is correct because cyclic shifts preserve the existence of consecutive equal cells.

Now consider a board where every row is identical:

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

A naive solution might reject this because adjacent rows are equal. The algorithm accepts it because every row alternates internally.

That decision is correct. Rows can be shifted independently. Shifting every second row once produces:

```
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW
...
```

which is a proper chessboard.

Finally, consider the fully uniform row:

```
BBBBBBBB
```

Every adjacent comparison fails:

```
B == B
```

The algorithm prints `NO`.

No amount of cyclic rotation changes the row because all characters are identical, so the board can never become alternating.
