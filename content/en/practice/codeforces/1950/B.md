---
title: "CF 1950B - Upscaling"
description: "We are asked to generate a checkerboard pattern that is made of larger $2 times 2$ tiles. Each tile is either fully filled with the character or fully filled with .. The size of the grid is determined by an input integer $n$, and the final grid has dimensions $2n times 2n."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1950
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 937 (Div. 4)"
rating: 800
weight: 1950
solve_time_s: 45
verified: true
draft: false
---

[CF 1950B - Upscaling](https://codeforces.com/problemset/problem/1950/B)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to generate a checkerboard pattern that is made of larger $2 \times 2$ tiles. Each tile is either fully filled with the character `#` or fully filled with `.`. The size of the grid is determined by an input integer $n$, and the final grid has dimensions $2n \times 2n`. The top-left $2 \times 2$ tile is always `#`, and tiles alternate in a checkerboard fashion both horizontally and vertically.

For example, when $n=2$, the grid is $4 \times 4$, and the top-left $2 \times 2$ tile is `#`. Its neighbor to the right is `.`, the neighbor below is `.`, and the diagonal neighbor is `#`.

The constraints are modest. $n$ can be at most 20, so the maximum grid size is $40 \times 40$, which is small enough that we can literally construct the entire grid in memory and print it. Time complexity is not a limiting factor here, but we must respect the patterning rules carefully.

Edge cases that can trip up a naive implementation include $n=1$, where the grid is just $2 \times 2$. A careless approach might try to alternate individual cells instead of $2 \times 2$ blocks, producing the wrong output. Another potential source of error is misaligning the tiles so that rows or columns do not preserve the alternating pattern when moving from one $2 \times 2$ block to the next.

## Approaches

A brute-force approach would be to iterate over each row and each column in the $2n \times 2n$ grid, calculating whether that particular cell should be `#` or `.` based on its row and column. For each cell, we could divide the row and column index by 2 to determine which $2 \times 2$ tile it belongs to, then use the sum of those tile indices modulo 2 to decide the character. This approach is correct, and for the maximum $n=20$ it results in $1600$ operations per test case, which is negligible.

The key insight is that we do not need anything more complex than this. The problem structure allows us to directly map each cell to its tile by simple integer division and parity checks. There is no need for recursion or dynamic programming. Every row consists of repeated sequences of two identical characters because each tile spans two columns. Similarly, each tile spans two rows, so the row content repeats once for the second row of the tile. Recognizing the $2 \times 2$ nature of the tiles allows us to generate the grid efficiently with simple nested loops.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n^2) | Accepted |
| Optimized with Tile Repetition | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. Loop over each test case.
2. For each test case, read `n` and compute the grid size as `2n`.
3. Iterate over `2n` rows using index `i`. Determine which horizontal tile row this is by integer division: `tile_row = i // 2`.
4. Initialize an empty string for the current row. Iterate over `2n` columns using index `j`. Determine which vertical tile column this is by integer division: `tile_col = j // 2`.
5. Compute the parity of `tile_row + tile_col`. If it is even, append `#` to the current row string; if odd, append `.`. This implements the alternating tile pattern.
6. After constructing the row string, print it immediately. Repeat until all rows for the test case are printed.
7. Do not print extra blank lines between test cases.

Why it works: Each $2 \times 2$ tile is identified by `(i//2, j//2)`. Summing the tile row and column indices and checking parity ensures that adjacent tiles alternate characters. Repeating each tile character for two rows and two columns produces the required `2x2` blocks. The invariant is that every position in the grid is correctly mapped to its tile and thus the correct character.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    size = 2 * n
    for i in range(size):
        row = ''
        tile_row = i // 2
        for j in range(size):
            tile_col = j // 2
            if (tile_row + tile_col) % 2 == 0:
                row += '#'
            else:
                row += '.'
        print(row)
```

We first read the number of test cases. For each case, we determine the total grid size as `2n`. For each row `i`, `tile_row` identifies which $2 \times 2$ horizontal block we are in. The inner loop builds the row character by character, using `(tile_row + tile_col) % 2` to decide whether it is `#` or `.`. This ensures correct alternating blocks. Rows are printed immediately without storing the entire grid in memory, although storing would also be fine for this size. Using integer division and parity checks is a common technique for constructing checkerboard patterns efficiently.

## Worked Examples

### Example 1

Input:

```
n = 1
```

| i | tile_row | j | tile_col | tile_row + tile_col | char |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | # |
| 0 | 0 | 1 | 0 | 0 | # |
| 1 | 0 | 0 | 0 | 0 | # |
| 1 | 0 | 1 | 0 | 0 | # |

Output:

```
##
##
```

This confirms the smallest grid is correctly handled, with a single `2x2` tile.

### Example 2

Input:

```
n = 2
```

| i | tile_row | j | tile_col | tile_row + tile_col | char |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | # |
| 0 | 0 | 1 | 0 | 0 | # |
| 0 | 0 | 2 | 1 | 1 | . |
| 0 | 0 | 3 | 1 | 1 | . |
| 1 | 0 | 0 | 0 | 0 | # |
| 1 | 0 | 1 | 0 | 0 | # |
| 1 | 0 | 2 | 1 | 1 | . |
| 1 | 0 | 3 | 1 | 1 | . |
| 2 | 1 | 0 | 0 | 1 | . |
| 2 | 1 | 1 | 0 | 1 | . |
| 2 | 1 | 2 | 1 | 2 | # |
| 2 | 1 | 3 | 1 | 2 | # |
| 3 | 1 | 0 | 0 | 1 | . |
| 3 | 1 | 1 | 0 | 1 | . |
| 3 | 1 | 2 | 1 | 2 | # |
| 3 | 1 | 3 | 1 | 2 | # |

Output:

```
##..
##..
..##
..##
```

This trace shows the parity sum correctly alternates tiles in both dimensions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | We loop over each cell in a `2n x 2n` grid. |
| Space | O(1) | We only store a single row at a time; no large grid array is needed. |

Given the constraints $n \le 20$, the largest grid has 1600 characters, easily manageable in Python. Multiple test cases up to 20 also fit comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        size = 2 * n
        for i in range(size):
            row = ''
            tile_row = i // 2
            for j in range(size):
                tile_col = j // 2
                row += '#' if (tile_row + tile_col) % 2 == 0 else '.'
            print(row)
    return out.getvalue().strip()

# Provided sample
assert run("4\n1\n2\n3\n4\n") == (
"##\n##\n"
"##..\n##..\n..##\n..##\n"
"##
```
