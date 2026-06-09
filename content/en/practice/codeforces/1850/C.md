---
title: "CF 1850C - Word on the Paper"
description: "We are given several independent 8 by 8 character grids. Each grid contains dots and lowercase letters, but only one meaningful structure exists inside each grid: a single column contains a vertically written word with no gaps. Every other cell is irrelevant noise."
date: "2026-06-09T05:29:21+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 800
weight: 1850
solve_time_s: 89
verified: true
draft: false
---

[CF 1850C - Word on the Paper](https://codeforces.com/problemset/problem/1850/C)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent 8 by 8 character grids. Each grid contains dots and lowercase letters, but only one meaningful structure exists inside each grid: a single column contains a vertically written word with no gaps. Every other cell is irrelevant noise.

The task for each grid is to extract that hidden word by reading the letters in the unique column that is not entirely dots. Because the word is continuous top to bottom, we simply need to scan that column in order and collect all letters.

The constraints are very small: at most 1000 test cases, each with only 64 characters. This means even a fully brute-force scan of every cell in every grid is trivial under the time limit. Any solution that inspects all characters directly is already optimal.

A common failure mode is assuming the word might appear in multiple columns or be split across rows. That leads to more complex parsing logic or premature stopping. Another subtle issue is stopping at the first letter found in a row rather than identifying the full column, which breaks cases where the word starts late in the grid.

## Approaches

A naive approach would try to detect the word by scanning row by row and collecting letters in reading order. This fails because the word is not horizontal; it is vertically aligned, so row-wise concatenation mixes unrelated columns.

Another incorrect attempt is to look for the first non-dot cell and assume the word starts there, then continue downwards only in that row index. This breaks because the word spans multiple rows in a single fixed column, not multiple columns in a single row.

The correct observation is structural. Each row contributes at most one character of the answer, and that character always lies in the same column. So the problem reduces to finding the index of the column that contains any letter, then reading that column from top to bottom.

This works because the word is guaranteed to be continuous and confined to exactly one column, so that column is uniquely identifiable by scanning for the first non-dot entry.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute scan rows and guess structure | O(8²) per test | O(1) | Unnecessary but works |
| Scan columns and extract | O(8²) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the 8 by 8 grid into memory as 8 strings. This preserves direct access to any cell without recomputation.
2. Identify the column index that contains the word. We scan all columns from left to right, and within each column scan all rows. The first column that contains any character other than a dot is the target column. This works because only one column contains letters, so detection is unambiguous.
3. Once the correct column is found, iterate from row 0 to row 7 and collect every character in that column that is not a dot. Since the word is continuous, every position in that column that is part of the word contributes exactly one letter in order.
4. Output the collected characters as the reconstructed word.

The key idea is that we separate structure detection from extraction: first find the active column, then read it linearly.

### Why it works

The grid construction guarantees that exactly one column contains non-dot characters forming a contiguous vertical string. Any other column contains only dots. Therefore, scanning column-wise will isolate a unique candidate, and reading top to bottom preserves the original order of the word. No ambiguity arises because no other structure overlaps with it.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    grid = [input().strip() for _ in range(8)]
    
    col = -1
    for j in range(8):
        for i in range(8):
            if grid[i][j] != '.':
                col = j
                break
        if col != -1:
            break
    
    res = []
    for i in range(8):
        if grid[i][col] != '.':
            res.append(grid[i][col])
    
    print("".join(res))
```

The solution first stores all rows so that column access becomes constant-time indexing. The nested loop only exists to identify the correct column; it stops immediately once a valid column is found.

A subtle detail is that we must break out of both loops once the column is detected. Failing to do so can overwrite the correct column index if implementation is careless. Another important point is that we only append non-dot characters when reading the column, since padding dots may appear outside the word segment even in the correct column.

## Worked Examples

### Example 1

Input grid:

| row | grid row |
| --- | --- |
| 0 | "........" |
| 1 | "........" |
| 2 | "........" |
| 3 | "...i...." |
| 4 | "........" |
| 5 | "........" |
| 6 | "........" |
| 7 | "........" |

The only column containing a letter is column 3.

| step | row scanned | column 3 value | collected |
| --- | --- | --- | --- |
| 0 | 0 | . | "" |
| 1 | 1 | . | "" |
| 2 | 2 | . | "" |
| 3 | 3 | i | "i" |
| 4 | 4 | . | "i" |
| 5 | 5 | . | "i" |
| 6 | 6 | . | "i" |
| 7 | 7 | . | "i" |

Final answer is "i".

This confirms that we correctly ignore empty rows and preserve vertical order.

### Example 2

A second grid:

| row | grid row |
| --- | --- |
| 0 | "........" |
| 1 | ".l......" |
| 2 | ".o......" |
| 3 | ".s......" |
| 4 | ".t......" |
| 5 | "........" |
| 6 | "........" |
| 7 | "........" |

Column 1 is the active column.

| row | value | collected |
| --- | --- | --- |
| 1 | l | "l" |
| 2 | o | "lo" |
| 3 | s | "los" |
| 4 | t | "lost" |

This shows that even when the word is not centered or starts after empty rows, scanning the full column still reconstructs it correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each grid is constant size 8 by 8, so work per test case is bounded |
| Space | O(1) | Only stores 8 strings per test case |

The constraints are small enough that even redundant scanning is negligible. The solution is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        g = [input().strip() for _ in range(8)]
        col = -1
        for j in range(8):
            for i in range(8):
                if g[i][j] != '.':
                    col = j
                    break
            if col != -1:
                break
        res = []
        for i in range(8):
            if g[i][col] != '.':
                res.append(g[i][col])
        out.append("".join(res))
    return "\n".join(out)

# provided samples
assert run("""5
........
........
........
........
...i....
........
........
........
........
.l......
.o......
.s......
.t......
........
........
........
........
........
........
........
......t.
......h.
......e.
........
........
........
........
........
.......g
.......a
.......m
.......e
a.......
a.......
a.......
a.......
a.......
a.......
a.......
a.......""") == "i\nlost\nthe\ngame\naaaaaaaa"

# custom cases
assert run("""1
........
........
........
........
....a...
....b...
....c...
....d...
""") == "abcd", "vertical word middle column"

assert run("""1
........
........
..x.....
..y.....
..z.....
........
........
........
""") == "xyz", "shifted column word"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| vertical word middle column | abcd | word not starting at top row |
| shifted column word | xyz | correct column detection |

## Edge Cases

One edge case is when the word starts in the last row of the grid. The algorithm still works because we scan all rows in the column, not just until the first or last match.

Another edge case is when multiple rows are empty before the word begins. Since we only append non-dot characters, those empty rows contribute nothing, preserving correctness without needing special handling.

A third case is when the word is a single character. The algorithm still finds the correct column and returns a single-letter string, since only one cell in that column is non-dot.
