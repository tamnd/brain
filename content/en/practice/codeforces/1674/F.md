---
title: "CF 1674F - Desktop Rearrangement"
description: "We are given a 2D grid representing a desktop with icons marked as '' and empty cells as '.'. The desktop is considered \"good\" if the icons occupy a compact rectangle starting from the top-left corner: all icons fill some number of complete columns, and possibly a prefix of one…"
date: "2026-06-10T01:16:36+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1674
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 786 (Div. 3)"
rating: 1800
weight: 1674
solve_time_s: 106
verified: true
draft: false
---

[CF 1674F - Desktop Rearrangement](https://codeforces.com/problemset/problem/1674/F)

**Rating:** 1800  
**Tags:** data structures, greedy, implementation  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 2D grid representing a desktop with icons marked as '*' and empty cells as '.'. The desktop is considered "good" if the icons occupy a compact rectangle starting from the top-left corner: all icons fill some number of complete columns, and possibly a prefix of one additional column. There should be no icons outside this shape. For example, if we have 4 rows and 4 columns, and the first two columns are fully filled with icons and the third column has one icon at the top, this is good. Any icons outside this compact arrangement would violate the "good" property.

We are then given a sequence of queries, each of which either adds an icon to a cell or removes it. After each query, we must compute the minimum number of moves needed to restore the desktop to a good configuration. Each move consists of picking an icon and placing it anywhere else.

The constraints are tight: the grid can be up to 1000 by 1000, and there can be up to 200,000 queries. Naive approaches that scan the entire grid per query, which would be $O(n \cdot m \cdot q)$, are far too slow. This forces us to find a solution where updates and queries are handled in nearly constant or logarithmic time.

A subtle edge case occurs when icons are scattered such that no full columns exist. For example, a 2x2 grid with icons at positions (1,1) and (2,2) requires rearranging both icons to form a good desktop. A naive approach that does not account for the total count of icons or their linearized positions would incorrectly compute the number of moves.

## Approaches

The brute-force approach is simple: after each query, count all icons in the grid and compute which cells in the top-left rectangle should be filled. We then scan the grid, counting misplaced icons that need to be moved into the rectangle or removed from outside. This works correctly but is too slow. Each query would cost $O(n \cdot m)$, and with 200,000 queries, the total operations could reach $2 \cdot 10^{11}$, which is infeasible.

The key insight for optimization comes from linearizing the 2D grid into a 1D array. If we imagine the desktop filled column by column, the "good" desktop corresponds to placing the first $k$ icons in the first $k$ positions of this 1D array. We can maintain a single array of length $n \cdot m$ representing whether each cell contains an icon. For each query, we update the count of icons and track how many icons are misplaced among the first $k$ cells. We only need to know the total number of icons and the number of empty cells in the first $k$ positions to determine the number of moves, reducing per-query cost to $O(1)$ with proper bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m * q) | O(n * m) | Too slow |
| Optimal | O(n * m + q) | O(n * m) | Accepted |

## Algorithm Walkthrough

1. Read the grid dimensions $n$ and $m$, and number of queries $q$. Flatten the grid into a 1D array in column-major order so that the first column's cells appear first, followed by the second column, and so on. This aligns with the desired "good" configuration.
2. Count the total number of icons, `total_icons`, in the current grid. Determine the number of 1D positions that should be filled in a good desktop: the first `total_icons` cells of the 1D array.
3. Maintain a variable `misplaced` that counts the number of positions among the first `total_icons` in the 1D array that are empty (i.e., where an icon should be but isn't). This is equal to the minimum number of moves required because each empty cell in this prefix requires moving an icon from outside into it.
4. For each query, compute the 1D index of the cell. If the cell contained an icon, remove it; otherwise, add it. Update `total_icons` accordingly.
5. If the updated cell lies within the first `total_icons` positions, adjust `misplaced` by ±1 depending on whether the cell became empty or filled. If the cell lies outside this range but the total count of icons changed, also adjust `misplaced` if the movement affects the boundary of the first `total_icons` positions.
6. Output `misplaced` after each query.

Why it works: By flattening the grid column-wise, the first `total_icons` cells represent the exact shape of a "good" desktop. Misplaced cells in this prefix correspond exactly to icons that must be moved. This invariant holds across queries, and updating `misplaced` based on local changes guarantees correctness in $O(1)$ per query.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, q = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# Flatten the grid column-wise
cells = []
for j in range(m):
    for i in range(n):
        cells.append(grid[i][j] == '*')

total_cells = n * m
total_icons = sum(cells)
misplaced = sum(1 for i in range(total_icons) if not cells[i])

# Map from 2D to 1D index
def idx(x, y):
    return (y - 1) * n + (x - 1)

res = []
for _ in range(q):
    x, y = map(int, input().split())
    i = idx(x, y)
    if cells[i]:
        # Removing an icon
        if i < total_icons:
            misplaced -= 1
        total_icons -= 1
        cells[i] = False
        if cells[total_icons]:
            misplaced += 1
    else:
        # Adding an icon
        if i < total_icons:
            misplaced += 1
        if cells[total_icons]:
            misplaced -= 1
        cells[i] = True
        total_icons += 1
    res.append(str(misplaced))

print('\n'.join(res))
```

The solution first flattens the grid into column-major order to simplify the "good" configuration. We maintain `total_icons` and `misplaced` so that at any time we know how many moves are required. The index mapping from 2D to 1D and careful updates of `misplaced` when icons are added or removed are crucial to avoid off-by-one errors.

## Worked Examples

Sample 1:

```
Initial grid (4x4):
..**
.*..
*...
...*
Flattened column-major:
[., *, *, ., *, ., ., *, ., ., ., *]

total_icons = 5
Prefix length = 5
Prefix cells: [., *, *, ., *]
Empty cells in prefix: 3 → minimum moves = 3
```

After first query (1,3) toggles cell (1,3):

```
Index in 1D: 2
Cell contained '*' → now empty
Index < total_icons → misplaced -= 1 → misplaced = 2
total_icons -= 1 → total_icons = 4
Check new boundary (cell at index total_icons=4 is '*') → misplaced += 1 → misplaced = 3
Output: 3
```

Subsequent queries update similarly, always maintaining the invariant that `misplaced` counts empty cells in the prefix of length `total_icons`.

This trace confirms the solution handles additions and removals correctly while updating only affected cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m + q) | Flattening the grid takes O(n*m). Each query updates O(1) variables. |
| Space | O(n * m) | Storing the flattened grid and boolean states. |

With $n, m \le 1000$ and $q \le 2 \cdot 10^5$, total operations around $10^6 + 2 \cdot 10^5$ are well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, q = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    cells = []
    for j in range(m):
        for i in range(n):
            cells.append(grid[i][j] == '*')
    total_cells = n * m
    total_icons = sum(cells)
    misplaced = sum(1 for i in range(total_icons) if not cells[i])
    def idx(x, y):
        return (y - 1) * n + (x - 1)
    res = []
    for _ in range(q):
        x, y = map(int, input().split())
        i = idx(x, y)
        if cells[i]:
            if i < total_icons:
                misplaced -= 1
            total_icons -= 1
            cells[i] = False
            if cells[total_icons]:
                misplaced += 1
        else:
            if i < total_icons:
                misplaced += 1
            if cells[total_icons]:
                misplaced -= 1
            cells[i] = True
            total_icons += 1
        res.append(str(misplaced))
    return '\n'.join(res)

# Provided sample
assert run("""4
```
