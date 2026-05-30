---
title: "CF 470E - Chessboard"
description: "We need to print an n × n chessboard using characters. White squares are represented by . and black squares by . The square in the top-left corner is white, and colors alternate both horizontally and vertically exactly as on a real chessboard."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "E"
codeforces_contest_name: "Surprise Language Round 7"
rating: 1900
weight: 470
solve_time_s: 89
verified: true
draft: false
---

[CF 470E - Chessboard](https://codeforces.com/problemset/problem/470/E)

**Rating:** 1900  
**Tags:** *special  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to print an `n × n` chessboard using characters. White squares are represented by `.` and black squares by `#`. The square in the top-left corner is white, and colors alternate both horizontally and vertically exactly as on a real chessboard.

The input contains a single integer `n`, which gives the board size. The output must contain `n` lines, each with `n` characters describing one row of the board.

The constraints are extremely small. Since `1 ≤ n ≤ 9`, even generating every cell individually requires at most `81` operations. Any reasonable solution is fast enough. The task is not about optimization, it is about correctly reproducing the alternating color pattern.

A common mistake is getting the starting color wrong. For example:

Input:

```
1
```

Correct output:

```
.
```

The top-left square is white, so the first character must be `.`. Starting with `#` would invert the entire board.

Another easy mistake is alternating only inside each row but forgetting that consecutive rows must start with opposite colors.

Input:

```
2
```

Correct output:

```
.#
#.
```

A careless implementation might produce:

```
.#
.#
```

because it restarts every row with the same color.

A third source of errors is off-by-one indexing. The color depends on whether the sum of the row and column positions is even or odd. Using one-based indexing without adjusting the parity logic can flip the entire board.

## Approaches

The most direct approach is to examine every square and determine its color. For each position `(row, col)`, we decide whether it should contain `.` or `#`, append that character to the current row, and print the completed row.

This brute-force approach is already sufficient because there are only `n²` cells. With `n = 9`, the worst case contains just `81` positions.

The key observation is that chessboard colors alternate. If we index rows and columns from zero, then positions with even `row + col` have the same color as the top-left square, while positions with odd `row + col` have the opposite color.

Since the top-left square is white, represented by `.`, we simply output:

```
.
```

when `(row + col)` is even, and

```
#
```

when `(row + col)` is odd.

This lets us determine each cell independently with a simple parity check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) excluding output | Accepted |
| Optimal | O(n²) | O(1) excluding output | Accepted |

For this problem, the brute-force and optimal approaches are effectively the same because every cell must appear in the output.

## Algorithm Walkthrough

1. Read the integer `n`.
2. Iterate through every row index `i` from `0` to `n - 1`.
3. Build the current row character by character.
4. For each column index `j` from `0` to `n - 1`, compute `(i + j) % 2`.
5. If the result is `0`, append `.` because this square has the same color as the top-left square.
6. Otherwise append `#` because the color must alternate.
7. After constructing the row, print it.

### Why it works

The chessboard alternates colors between neighboring squares. Moving one step horizontally or vertically changes the parity of `row + col`, so the parity alternates exactly as the colors should. The top-left square `(0,0)` has even parity and is white. Every square with even parity receives `.`, every square with odd parity receives `#`, producing precisely the required chessboard pattern.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

for i in range(n):
    row = []
    for j in range(n):
        if (i + j) % 2 == 0:
            row.append('.')
        else:
            row.append('#')
    print(''.join(row))
```

The program begins by reading the board size.

The outer loop processes rows, while the inner loop processes columns. For each position `(i, j)`, the parity of `i + j` determines the color. Even parity corresponds to the same color as `(0, 0)`, which is white and represented by `.`. Odd parity corresponds to `#`.

Each row is accumulated in a list and converted into a string using `''.join(row)`. This avoids repeatedly concatenating strings and keeps the implementation clean.

The most common implementation mistake is reversing the parity rule. Since `(0,0)` must be white, even parity must map to `.` rather than `#`.

## Worked Examples

### Example 1

Input:

```
4
```

| Row `i` | Col `j` | `i+j` | Parity | Character |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Even | . |
| 0 | 1 | 1 | Odd | # |
| 0 | 2 | 2 | Even | . |
| 0 | 3 | 3 | Odd | # |

First row becomes:

```
.#.#
```

Continuing similarly:

| Row `i` | Generated Row |
| --- | --- |
| 0 | .#.# |
| 1 | #.#. |
| 2 | .#.# |
| 3 | #.#. |

Output:

```
.#.#
#.#.
.#.#
#.#.
```

This demonstrates that alternating parity naturally produces the required alternating colors both horizontally and vertically.

### Example 2

Input:

```
3
```

| Row `i` | Generated Row |
| --- | --- |
| 0 | .#. |
| 1 | #.# |
| 2 | .#. |

Output:

```
.#.
#.#
.#.
```

This example shows that odd board sizes work exactly the same way. Every adjacent square has opposite parity, so the chessboard pattern remains valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every cell of the board is generated once |
| Space | O(1) | Only a small temporary row buffer is used, excluding output |

With `n ≤ 9`, the algorithm performs at most `81` cell computations. This is far below the available limits, so the solution comfortably fits within both the time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    out = []

    for i in range(n):
        row = []
        for j in range(n):
            row.append('.' if (i + j) % 2 == 0 else '#')
        out.append(''.join(row))

    return '\n'.join(out)

# provided sample
assert run("4\n") == ".#.#\n#.#.\n.#.#\n#.#.", "sample 1"

# minimum size
assert run("1\n") == ".", "single white square"

# small even board
assert run("2\n") == ".#\n#.", "alternation across rows"

# small odd board
assert run("3\n") == ".#.\n#.#\n.#.", "odd dimension board"

# maximum size
assert run("9\n").split("\n")[0] == ".#.#.#.#.", "maximum size first row"
assert len(run("9\n").split("\n")) == 9, "maximum size row count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `.` | Minimum board size |
| `2` | `.# / #.` | Correct row-to-row alternation |
| `3` | `.#. / #.# / .#.` | Odd-sized board handling |
| `9` | 9 valid chessboard rows | Maximum constraint |

## Edge Cases

Consider the smallest possible board.

Input:

```
1
```

The algorithm visits only `(0,0)`. Since `0 + 0 = 0` is even, it outputs `.`.

Output:

```
.
```

This confirms that the starting square is white.

Consider a board where row alternation matters.

Input:

```
2
```

Execution trace:

| Position | Sum | Character |
| --- | --- | --- |
| (0,0) | 0 | . |
| (0,1) | 1 | # |
| (1,0) | 1 | # |
| (1,1) | 2 | . |

Output:

```
.#
#.
```

The first character of the second row becomes `#` automatically because the parity changes. This prevents the common mistake of restarting every row with `.`.

Consider a larger odd-sized board.

Input:

```
5
```

The first row becomes:

```
.#.#.
```

The second row becomes:

```
#.#.#
```

and the pattern continues. Since parity uniquely determines color, no special handling is required for odd dimensions. The algorithm generates the correct chessboard structure for every valid `n`.
