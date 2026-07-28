---
title: "CF 102777C - \u0426\u0432\u0435\u0442\u043d\u0430\u044f \u0434\u043e\u0441\u043a\u0430"
description: "The board has N rows and M columns. Its cells are colored with seven colors that repeat cyclically along diagonals. After Alice names a cell (X, Y), we must determine the color number assigned to that cell."
date: "2026-07-28T15:44:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "C"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 48
verified: true
draft: false
---

[CF 102777C - \u0426\u0432\u0435\u0442\u043d\u0430\u044f \u0434\u043e\u0441\u043a\u0430](https://codeforces.com/problemset/problem/102777/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The board has `N` rows and `M` columns. Its cells are colored with seven colors that repeat cyclically along diagonals. After Alice names a cell `(X, Y)`, we must determine the color number assigned to that cell.

The board dimensions can be as large as `10^6 × 10^6`, but only one cell is queried. That immediately rules out any approach that explicitly builds the board. Even storing the colors would require up to `10^12` cells, which is far beyond both memory and time limits. The solution must compute the answer directly from the coordinates.

The key observation is that every cell on the same diagonal with constant `X + Y` has the same color. Moving one step to the next diagonal increases `X + Y` by one, so the color also advances by one in the cycle of seven colors.

A common off-by-one mistake is forgetting that the colors are numbered from `1` instead of `0`. For example, for the input

```
1 1 1 1
```

the correct answer is

```
1
```

because the very first diagonal starts with color `1`. Using `(X + Y) % 7` directly would incorrectly produce `2`.

Another subtle case is when the diagonal index is a multiple of seven. For example,

```
5 9 3 6
```

has `X + Y = 9`. Since the first diagonal corresponds to `X + Y = 2`, the offset is `7`, which wraps exactly once around the cycle. The correct color is `1`, not `7`.

## Approaches

A straightforward simulation would generate the entire board diagonal by diagonal, assigning colors in the repeating order `1, 2, ..., 7, 1, ...`. This is correct because it follows the coloring rule directly. Unfortunately, the board may contain up to `10^12` cells, making both the running time and memory completely impractical.

The crucial observation is that the color depends only on the diagonal containing the queried cell. The first diagonal has `X + Y = 2` and receives color `1`. Every increase of one in `X + Y` moves to the next diagonal and advances the color by one. Since there are seven colors, we only need the diagonal offset modulo seven.

The diagonal offset is

```
(X + Y) - 2
```

and converting it back to the `1`-based color numbering gives

```
((X + Y - 2) % 7) + 1
```

This computes the answer in constant time without constructing any part of the board.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(NM) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers `N`, `M`, `X`, and `Y`. The board dimensions are not needed for the computation because the queried coordinates are guaranteed to be valid.
2. Compute the diagonal offset as `X + Y - 2`. The first diagonal has sum `2`, so subtracting `2` makes its offset equal to zero.
3. Compute the color with `((X + Y - 2) % 7) + 1`. The modulo operation wraps the colors every seven diagonals, and adding one converts the result back to the required numbering from `1` to `7`.
4. Print the resulting color.

### Why it works

Every cell on the same diagonal has the same value of `X + Y`, so they must receive the same color. Adjacent diagonals differ in `X + Y` by exactly one, matching one step forward in the repeating sequence of seven colors. Since the first diagonal starts with color `1`, shifting by `(X + Y - 2)` diagonals and taking the remainder modulo seven always produces the unique correct color.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, x, y = map(int, input().split())
print((x + y - 2) % 7 + 1)
```

The program reads the input, computes the diagonal offset, applies modulo seven, converts the result back to `1`-based numbering, and prints it.

The board dimensions are intentionally unused because they do not influence the color once the queried cell is known. The subtraction by two is the key off-by-one adjustment. Without it, the first diagonal would incorrectly start from color `3` instead of color `1`.

Python integers easily handle the maximum possible coordinate sums, so there are no overflow concerns.

## Worked Examples

### Sample 1

Input:

```
3 3 3 3
```

| X | Y | X + Y | Offset = X + Y - 2 | Offset % 7 | Color |
| --- | --- | --- | --- | --- | --- |
| 3 | 3 | 6 | 4 | 4 | 5 |

The queried cell lies on the fifth diagonal in the repeating sequence, so its color is `5`.

### Sample 2

Input:

```
5 9 3 6
```

| X | Y | X + Y | Offset = X + Y - 2 | Offset % 7 | Color |
| --- | --- | --- | --- | --- | --- |
| 3 | 6 | 9 | 7 | 0 | 1 |

This example demonstrates the wraparound. After seven diagonal shifts, the color cycle returns to `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed. |
| Space | O(1) | No additional data structures are allocated. |

The running time and memory usage are independent of the board size, so the solution easily satisfies the given limits even when `N` and `M` are at their maximum values.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    n, m, x, y = map(int, input().split())
    print((x + y - 2) % 7 + 1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out

# provided samples
assert run("3 3 3 3\n") == "5\n", "sample 1"
assert run("5 9 3 6\n") == "1\n", "sample 2"

# custom cases
assert run("1 1 1 1\n") == "1\n", "minimum board"
assert run("1000000 1000000 1000000 1000000\n") == "5\n", "maximum coordinates"
assert run("7 7 1 7\n") == "7\n", "boundary before wrap"
assert run("7 8 1 8\n") == "1\n", "exact wraparound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `1` | Smallest possible board |
| `1000000 1000000 1000000 1000000` | `5` | Maximum coordinate values |
| `7 7 1 7` | `7` | Last color before wrapping |
| `7 8 1 8` | `1` | Correct modulo wraparound |

## Edge Cases

Consider the smallest possible input:

```
1 1 1 1
```

The algorithm computes `X + Y - 2 = 0`, then `0 % 7 = 0`, and finally adds one to obtain color `1`. This confirms that the first diagonal is handled correctly.

Now consider a diagonal where the offset is exactly seven:

```
5 9 3 6
```

The offset is `3 + 6 - 2 = 7`. Taking `7 % 7` gives `0`, and adding one produces color `1`. This correctly restarts the repeating sequence after every seven diagonals.

Finally, consider the last diagonal before wrapping:

```
7 7 1 7
```

The offset is `1 + 7 - 2 = 6`. The remainder is still `6`, so the color becomes `7`. The next diagonal would wrap back to color `1`, matching the required cyclic pattern.
