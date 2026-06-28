---
title: "CF 104797F - Letters"
description: "We are given a rectangular grid that contains lowercase letters and empty cells. Over time, gravity acts on this grid, but not in a fixed direction."
date: "2026-06-28T13:44:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104797
codeforces_index: "F"
codeforces_contest_name: "2021-2022 ICPC Central Europe Regional Contest (CERC 21)"
rating: 0
weight: 104797
solve_time_s: 30
verified: true
draft: false
---

[CF 104797F - Letters](https://codeforces.com/problemset/problem/104797/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid that contains lowercase letters and empty cells. Over time, gravity acts on this grid, but not in a fixed direction. Instead, the grid is repeatedly “settled” under a sequence of gravity directions, where each phase fully moves all letters as far as possible in the current direction until they are blocked by either the boundary or another letter.

A single phase behaves like a physical simulation: every letter independently slides in the given direction, but letters preserve their relative order along that direction because they cannot pass through each other. After all letters come to rest, the next phase begins with a possibly different gravity direction.

The final task is to compute the configuration after applying all K gravity phases.

The constraints are small: N and M are at most 100, and K is at most 100. This immediately suggests that any solution with complexity around O(KNM) or even O(KN M log N) is likely fine. However, solutions that simulate movement one cell at a time per step are still safe because the grid is tiny.

The main subtlety is that movement is not independent per cell in a naive sense. If we incorrectly move letters one by one, earlier moves can affect later ones in the same phase. For example, in a downward phase:

```
a
b
.
```

If we move `a` first, it might incorrectly pass through `b` depending on implementation order. The correct interpretation is that all letters in a column behave like a stack that is rearranged as a whole.

Another subtle edge case is empty grids or grids with no letters. The output must remain unchanged, and any compression logic must handle empty sequences correctly.

Finally, K = 0 means no movement occurs at all, so the original grid must be printed exactly as given.

## Approaches

A direct brute force simulation would treat each phase as a physics step and repeatedly move each letter one cell at a time in the gravity direction until no movement is possible. For each phase, we might attempt something like scanning the grid, moving letters, and repeating until stable. In the worst case, a single letter might move O(max(N, M)) steps per phase, and we might need many passes to resolve interactions, leading to a complexity that can degrade toward O(KN²M²) in an inefficient implementation. This is unnecessary because the final positions inside each row or column are fully determined by sorting or compaction.

The key observation is that gravity does not create complex interactions beyond ordering along a line. In any fixed direction, the grid decomposes into independent lines: columns for vertical gravity and rows for horizontal gravity. Within each line, letters simply “pack” toward one side while preserving their relative order. This is equivalent to extracting all letters from a line, then writing them back in order from the target side, filling remaining cells with dots.

Thus each phase can be processed in O(NM): we rebuild every row or column independently by collecting letters and rewriting.

Because K is at most 100, repeating this procedure K times is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force step simulation | O(K · N² · M²) worst-case | O(1) extra | Too slow |
| Line compaction per phase | O(K · N · M) | O(NM) | Accepted |

## Algorithm Walkthrough

We repeatedly simulate each gravity phase, but instead of moving letters incrementally, we rebuild the grid in a structured way depending on direction.

### Step-by-step procedure

1. Read the grid into a mutable structure, such as a list of lists.
2. For each gravity direction in the sequence, process the entire grid in one pass.
3. If the direction is vertical (down):

We process each column independently. For each column, we scan from top to bottom, collect all letters in order, then write them back from bottom to top. This simulates gravity pulling letters downward while preserving order.
4. If the direction is up:

Again process each column. We collect letters from top to bottom, then write them back from top to bottom starting at row 0. This packs letters upward.
5. If the direction is right:

We process each row independently. We collect letters from left to right, then write them back from right to left starting at the last column.
6. If the direction is left:

We process each row independently. We collect letters from left to right, then write them back starting from the leftmost position.
7. After processing all rows or columns for a phase, the grid is updated and becomes the input to the next phase.

### Why it works

Each phase preserves the relative order of letters along the axis orthogonal to movement because letters never cross each other. The only effect of gravity is to compress all letters along a line toward one boundary. Therefore each row or column behaves like a stable ordered container whose elements are repositioned but never permuted internally. This invariant ensures that rebuilding each line by extracting and reinserting letters exactly matches the physical process.

## Python Solution

```python
import sys
input = sys.stdin.readline

def apply_down(grid, n, m):
    for col in range(m):
        stack = []
        for row in range(n):
            if grid[row][col] != '.':
                stack.append(grid[row][col])
        for row in range(n - 1, -1, -1):
            grid[row][col] = stack.pop() if stack else '.'

def apply_up(grid, n, m):
    for col in range(m):
        stack = []
        for row in range(n):
            if grid[row][col] != '.':
                stack.append(grid[row][col])
        for row in range(n):
            grid[row][col] = stack.pop(0) if stack else '.'

def apply_right(grid, n, m):
    for row in range(n):
        stack = []
        for col in range(m):
            if grid[row][col] != '.':
                stack.append(grid[row][col])
        for col in range(m - 1, -1, -1):
            grid[row][col] = stack.pop() if stack else '.'

def apply_left(grid, n, m):
    for row in range(n):
        stack = []
        for col in range(m):
            if grid[row][col] != '.':
                stack.append(grid[row][col])
        for col in range(m):
            grid[row][col] = stack.pop(0) if stack else '.'

def main():
    n, m, k = map(int, input().split())
    dirs = input().strip()
    grid = [list(input().strip()) for _ in range(n)]

    for d in dirs:
        if d == 'D':
            apply_down(grid, n, m)
        elif d == 'U':
            apply_up(grid, n, m)
        elif d == 'R':
            apply_right(grid, n, m)
        else:
            apply_left(grid, n, m)

    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    main()
```

The solution maintains the grid as a mutable 2D list. Each phase rebuilds either rows or columns depending on direction.

For downward and upward gravity, each column is extracted into a linear list of letters. For downward gravity, we refill from the bottom so letters accumulate at the lowest available cells. For upward gravity, we refill from the top.

For horizontal gravity, rows are processed similarly, with right gravity filling from the right edge and left gravity filling from the left edge.

A subtle detail is that we must preserve ordering during extraction. This is why we scan consi
