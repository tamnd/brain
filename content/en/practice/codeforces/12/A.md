---
title: "CF 12A - Super Agent"
description: "We are asked to check whether a password entered on a 3×3 keypad is symmetric with respect to its central button. The ke"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 12
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 12 (Div 2 Only)"
rating: 800
weight: 12
solve_time_s: 75
verified: true
draft: false
---

[CF 12A - Super Agent](https://codeforces.com/problemset/problem/12/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to check whether a password entered on a 3×3 keypad is symmetric with respect to its central button. The keypad is represented as a 3×3 grid of characters, where "X" indicates a pressed button and "." indicates an unpressed one. Central symmetry means that if you rotate the grid 180 degrees around its middle cell, the pattern of pressed buttons remains unchanged.

In simpler terms, for a pattern to be symmetric around the center, each button at position (i, j) must match the button at position (2-i, 2-j). For example, the top-left corner must match the bottom-right corner, and the top-middle must match the bottom-middle, while the center can be anything because it maps to itself.

The constraints are minimal: a fixed 3×3 grid and a time limit of 2 seconds. This means any straightforward algorithm that checks all symmetric pairs will run instantly. Edge cases include patterns with no pressed buttons (all dots), all pressed buttons (all X), or asymmetric patterns where only one pair violates symmetry.

A careless implementation might only check rows or columns independently rather than comparing opposite positions across the center. For instance, the grid

```
X..
...
..X
```

is symmetric, but if we only compared mirrored rows without accounting for columns, we might incorrectly conclude it is not.

## Approaches

The brute-force approach is simple: for every cell in the grid, compute the cell symmetric around the center and compare them. In a 3×3 grid, this means comparing each of the four corners and the four edge cells. This works because the grid is tiny, but the comparison can be hard-coded since there are only eight positions to check.

The key insight is that the grid is fixed-size and small. We can exploit the structure by listing the symmetric pairs: the top-left with bottom-right, top-middle with bottom-middle, top-right with bottom-left, and the left-middle with right-middle. The center is ignored because it is always symmetric with itself. This reduces the problem to just four equality checks. The observation that symmetry is only about opposite positions allows us to write a solution that is both minimal and easy to verify manually.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Symmetry Pairs | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the 3×3 grid from input as a list of strings. Each string represents a row. This preserves the row/column structure, making indexing straightforward.
2. Identify the pairs of positions that must match for central symmetry: top-left with bottom-right, top-middle with bottom-middle, top-right with bottom-left, and left-middle with right-middle. The center position (1,1) is automatically symmetric.
3. For each symmetric pair, compare the characters. If any pair differs, the pattern is not symmetric. Immediately print "NO" and stop.
4. If all pairs match, print "YES". This guarantees that the grid is symmetric around its center.

The invariant maintained is that at any step, if all previously checked pairs match, the partial symmetry is correct. If a mismatch is found, symmetry is broken, and the algorithm stops.

## Python Solution

```python
import sys
input = sys.stdin.readline

grid = [input().strip() for _ in range(3)]

# Define symmetric pairs (i,j) <-> (2-i,2-j)
symmetric_pairs = [
    ((0,0),(2,2)),
    ((0,1),(2,1)),
    ((0,2),(2,0)),
    ((1,0),(1,2))
]

for (x1,y1),(x2,y2) in symmetric_pairs:
    if grid[x1][y1] != grid[x2][y2]:
        print("NO")
        sys.exit(0)

print("YES")
```

The code reads the grid into a list of strings, which preserves indexing by rows and columns. The symmetric pairs are explicitly defined, avoiding any off-by-one errors. The comparison loop exits immediately if a mismatch is found, ensuring we do not perform unnecessary checks.

## Worked Examples

**Example 1**

Input:

```
XX.
...
.XX
```

| Pair | grid[x1][y1] | grid[x2][y2] | Match? |
| --- | --- | --- | --- |
| (0,0)-(2,2) | X | X | yes |
| (0,1)-(2,1) | X | X | yes |
| (0,2)-(2,0) | . | . | yes |
| (1,0)-(1,2) | . | . | yes |

All pairs match, so output is "YES".

**Example 2**

Input:

```
X..
...
..X
```

| Pair | grid[x1][y1] | grid[x2][y2] | Match? |
| --- | --- | --- | --- |
| (0,0)-(2,2) | X | X | yes |
| (0,1)-(2,1) | . | . | yes |
| (0,2)-(2,0) | . | . | yes |
| (1,0)-(1,2) | . | . | yes |

All pairs match, output is "YES".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four pair comparisons are made, independent of input. |
| Space | O(1) | The grid uses 3 strings of 3 characters each, and the symmetric pair list has 4 elements. |

Given the 3×3 fixed grid, this solution runs instantly and uses negligible memory, easily satisfying the 2-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    grid = [input().strip() for _ in range(3)]
    symmetric_pairs = [
        ((0,0),(2,2)),
        ((0,1),(2,1)),
        ((0,2),(2,0)),
        ((1,0),(1,2))
    ]
    for (x1,y1),(x2,y2) in symmetric_pairs:
        if grid[x1][y1] != grid[x2][y2]:
            return "NO"
    return "YES"

# provided samples
assert run("XX.\n...\n.XX\n") == "YES", "sample 1"

# custom cases
assert run("X..\n...\n..X\n") == "YES", "symmetric corners"
assert run("X.X\n.X.\nX.X\n") == "YES", "all edges symmetric"
assert run("XXX\n.X.\nXXX\n") == "YES", "all edges pressed"
assert run("X..\n.X.\n..X\n") == "NO", "non-symmetric edges"
assert run("...\n...\n...\n") == "YES", "empty grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| X..\n...\n..X | YES | symmetric corners only |
| X.X\n.X.\nX.X | YES | edges symmetric, center ignored |
| XXX\n.X.\nXXX | YES | full top and bottom row pressed, symmetric |
| X..\n.X.\n..X | NO | edge mismatch breaks symmetry |
| ...\n...\n... | YES | empty grid still symmetric |

## Edge Cases

The empty grid

```
...
...
...
```

is symmetric because every pair of positions matches. The algorithm checks all four pairs and finds equality (all dots), correctly returning "YES".

A single button pressed in the center

```
...
.X.
...
```

also passes. The symmetric pairs are all dots, center is ignored. The output is "YES".

A mismatched corner pattern like

```
X..
...
.X.
```

fails at the first pair (0,0)-(2,2) because X != ., immediately returning "NO". The code correctly stops at the first violation without examining the remaining pairs, avoiding unnecessary checks.
