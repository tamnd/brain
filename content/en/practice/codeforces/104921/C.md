---
title: "CF 104921C - Word on the Paper"
description: "We are given several independent 8 by 8 character grids. Each grid is mostly filled with dots, but somewhere inside it a single word is hidden. The word is written straight down in exactly one column, occupying consecutive rows without interruption."
date: "2026-06-28T08:09:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104921
codeforces_index: "C"
codeforces_contest_name: "Easy_Training"
rating: 0
weight: 104921
solve_time_s: 66
verified: true
draft: false
---

[CF 104921C - Word on the Paper](https://codeforces.com/problemset/problem/104921/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent 8 by 8 character grids. Each grid is mostly filled with dots, but somewhere inside it a single word is hidden. The word is written straight down in exactly one column, occupying consecutive rows without interruption. Every other cell in the grid is a dot.

The task for each grid is to recover that hidden vertical word by reading the letters in the correct column from top to bottom.

The constraints are small and fixed. Each test case contains exactly 64 characters arranged in an 8 by 8 block, and there are at most 1000 such test cases. This means the total input size is bounded by about 64,000 characters, so any approach that scans each grid a constant number of times is easily fast enough. Even repeated full scans per test case would still be acceptable, but unnecessary.

There are no real algorithmic edge cases in terms of performance, but there are correctness traps in interpreting the layout. A naive mistake is assuming the word might be scattered or require stitching multiple columns together. Another mistake is trying to read row-wise or stopping at the first letter encountered without ensuring you stay within the same column.

For example, consider a grid where the word is `"lost"` in one column:

```
........
....l...
....o...
....s...
....t...
........
........
........
```

The correct output is `"lost"`. A flawed approach might scan row by row and pick letters wherever they appear, which would still work here but would fail if multiple columns contained letters in other problems of similar style. The defining constraint is that exactly one column contains all letters of the word.

Another edge case is when the word is a single character, such as:

```
........
........
....a...
........
........
........
........
........
```

The output must be `"a"`. Any logic that assumes at least two letters or tries to detect start and end markers could break here.

The key structural fact is that exactly one column contains non-dot characters, and those characters appear contiguously from top to bottom.

## Approaches

A brute-force interpretation would be to inspect each column and check whether it contains any letters. For each column, we could scan all 8 rows and collect characters that are not dots. If the resulting list is non-empty, that column contains the word, and we output it.

Since the grid size is fixed at 8 by 8, even an approach that tries every possible column and scans every row is effectively constant time. The worst case per test case is 64 cell checks, and with up to 1000 test cases this is only 64,000 operations, which is trivial.

The more direct observation is that we do not need to “search” at all. Because the word lies entirely in one column, every row contains at most one non-dot character overall, and all of those belong to the same column. So we can simply scan row by row, extract the first non-dot character per row if it exists, and concatenate them. This directly reconstructs the word in order.

The brute-force works because it explicitly verifies each column. The optimized approach removes the need for column selection by exploiting the uniqueness guarantee: only one column can contain letters, so any row-wise extraction automatically stays consistent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Column scanning brute force | O(8 × 8 × t) | O(1) | Accepted |
| Row-wise extraction | O(8 × t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`, since each grid is independent and must be processed separately.
2. For each test case, read 8 strings representing the 8 rows of the grid. Each string has length 8, so we can treat it as a fixed array of characters.
3. Initialize an empty list (or string builder) to accumulate the characters of the hidden word.
4. Iterate over each of the 8 rows. For a given row, scan its 8 columns from left to right until we find a character that is not `'.'`.

When we find such a character, append it to the answer and move to the next row immediately. We do not continue scanning the row because each row contains at most one relevant character by construction.
5. After processing all 8 rows, output the accumulated string.

The important design choice is scanning per row rather than trying to identify the column first. Because the word is vertically aligned, every row contributes exactly one character from the same column, so row-wise extraction preserves order automatically.

### Why it works

Each grid contains exactly one column that has letters, and within that column the letters appear in consecutive rows forming the word. All other cells are dots. Therefore, every row contains either zero letters or exactly one letter, and all non-empty rows correspond to the same column index. By extracting the first non-dot character from each row, we reconstruct the sequence of letters in top-to-bottom order. No other column can contribute a letter, so no ambiguity arises.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        grid = [input().strip() for _ in range(8)]
        word = []

        for r in range(8):
            for c in range(8):
                if grid[r][c] != '.':
                    word.append(grid[r][c])
                    break

        out.append("".join(word))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the row-wise extraction strategy directly. For each row, it scans left to right and stops at the first non-dot character. The `break` is essential because each row contributes at most one character, and continuing would be redundant.

The use of `strip()` ensures we do not accidentally include newline characters in the grid representation. The final answers are accumulated in a list and printed at once to avoid repeated I/O overhead.

## Worked Examples

### Example 1

Input grid:

```
........
....l...
....o...
....s...
....t...
........
........
........
```

| Row | Scan result | Added char | Word so far |
| --- | --- | --- | --- |
| 0 | none | - | "" |
| 1 | l | l | "l" |
| 2 | o | o | "lo" |
| 3 | s | s | "los" |
| 4 | t | t | "lost" |
| 5-7 | none | - | "lost" |

Output is `"lost"`, matching the vertical concatenation of the single active column.

### Example 2

Input grid:

```
........
........
..a.....
........
........
........
........
........
```

| Row | Scan result | Added char | Word so far |
| --- | --- | --- | --- |
| 0-1 | none | - | "" |
| 2 | a | a | "a" |
| 3-7 | none | - | "a" |

This confirms the algorithm correctly handles a single-character word without assuming any minimum length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(8 × 8 × t) | Each cell is checked at most once per row scan |
| Space | O(1) | Only stores 8 rows and the output string per test |

The total work is at most about 64,000 character checks for the maximum input size, which is comfortably within limits for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        # inline solution
        input = _sys.stdin.readline

        t = int(input())
        res = []

        for _ in range(t):
            grid = [input().strip() for _ in range(8)]
            word = []
            for r in range(8):
                for c in range(8):
                    if grid[r][c] != '.':
                        word.append(grid[r][c])
                        break
            res.append("".join(word))

        print("\n".join(res))

    return out.getvalue().strip()

# provided samples (conceptual placeholders; actual formatting may vary)
# assert run("...") == "..."

# custom cases

# single letter
assert run(
"1\n"
"........\n........\n........\n....x...\n........\n........\n........\n........\n"
) == "x"

# full column word
assert run(
"1\n"
".a......\n.b......\n.c......\n.d......\n.e......\n.f......\n.g......\n.h......\n"
) == "abcdefgh"

# word in last column
assert run(
"1\n"
".......k\n.......i\n.......t\n.......e\n.......n\n.......s\n.......u\n.......n\n"
) == "kitensun"

# all dots except one column
assert run(
"1\n"
"........\n........\n........\n....z...\n....a...\n....p...\n........\n........\n"
) == "zap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single letter grid | x | minimal word length |
| full vertical column | abcdefgh | normal contiguous case |
| last column placement | kitensun | right-edge handling |
| sparse surrounding dots | zap | ignores irrelevant cells |

## Edge Cases

A single-character word is handled because the row-wise scan still finds exactly one non-dot cell overall. For an input where only one letter exists, such as:

```
........
........
........
....x...
........
........
........
........
```

the algorithm visits each row, appends only `"x"`, and produces `"x"` as required.

A word located in the last column is handled without any special logic. For example:

```
.......k
.......i
.......t
.......e
.......n
.......s
.......u
.......n
```

Each row scan reaches column 7 and finds the letter there. The ordering remains correct because rows are processed top to bottom, preserving vertical sequence.

A grid with many dots outside the word does not affect correctness because the inner loop stops at the first non-dot character per row. Even if future variants had noise characters elsewhere, the invariant that only one column contains letters ensures no incorrect extractions.
