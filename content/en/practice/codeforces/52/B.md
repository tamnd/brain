---
title: "CF 52B - Right Triangles"
description: "We are given a rectangular grid where each cell is either empty or marked with . Every cell represents a point located at the center of that cell. We need to count how many right triangles can be formed such that:"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics"]
categories: ["algorithms"]
codeforces_contest: 52
codeforces_index: "B"
codeforces_contest_name: "Codeforces Testing Round 1"
rating: 1600
weight: 52
solve_time_s: 98
verified: true
draft: false
---
[CF 52B - Right Triangles](https://codeforces.com/problemset/problem/52/B)

**Rating:** 1600  
**Tags:** combinatorics  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid where each cell is either empty or marked with `*`. Every `*` cell represents a point located at the center of that cell. We need to count how many right triangles can be formed such that:

- all three vertices are `*` cells,
- the right angle is formed by one horizontal side and one vertical side,
- the legs of the triangle are parallel to the grid axes.

A triangle is fully determined once we choose the vertex containing the right angle. If a `*` cell has another `*` somewhere in the same row and another `*` somewhere in the same column, then those two choices form a valid right triangle.

The grid dimensions are at most `1000 × 1000`, so the total number of cells can reach one million. Any solution that checks all triples of `*` cells is completely infeasible. Even checking every cell against all cells in its row and column naively can become too slow if done repeatedly.

The useful observation is that for a fixed right-angle vertex, the horizontal and vertical choices are independent. If a cell has `r` other stars in its row and `c` other stars in its column, then it contributes `r * c` triangles.

Several edge cases can silently break incorrect implementations.

Consider a grid with only one row:

```
1 5
*****
```

The correct answer is `0`. Even though many pairs exist horizontally, no vertical leg can be formed.

Consider a grid where the right-angle vertex itself is accidentally counted as one of the choices:

```
2 2
**
**
```

The correct answer is `4`.

Each corner contributes exactly one triangle:

- top-left uses top-right and bottom-left,
- top-right uses top-left and bottom-right,
- bottom-left uses top-left and bottom-right,
- bottom-right uses top-right and bottom-left.

A careless formula using `row_count * col_count` instead of `(row_count - 1) * (col_count - 1)` would overcount by allowing the vertex to pair with itself.

Another subtle case appears when rows or columns contain exactly one star:

```
3 3
*..
.*.
..*
```

The answer is `0`. Every star is isolated in both its row and column, so no right triangle exists even though there are three stars total.

## Approaches

The brute-force idea is straightforward. Enumerate every triple of `*` cells and test whether they form a valid axis-aligned right triangle.

Suppose the grid is completely filled. Then there are `10^6` stars. Checking all triples would require roughly:

$$\binom{10^6}{3}$$

operations, which is astronomically impossible.

A slightly better brute-force approach fixes the right-angle vertex first. For every `*` cell, scan its entire row to find horizontal partners and scan its entire column to find vertical partners. If a cell has `r` horizontal choices and `c` vertical choices, then it contributes `r * c`.

This approach is correct because every valid triangle has exactly one right-angle vertex, and once that vertex is fixed, the horizontal and vertical endpoints can be chosen independently.

The problem is performance. If we scan rows and columns repeatedly for every cell, the complexity becomes:

$$O(n \cdot m \cdot (n + m))$$

With `n = m = 1000`, this becomes roughly two billion operations in the worst case.

The key observation is that row and column information never changes. Instead of recomputing counts repeatedly, we can preprocess:

- how many stars exist in each row,
- how many stars exist in each column.

Then each `*` cell can compute its contribution in constant time.

If a cell `(i, j)` contains a star:

- `row[i] - 1` gives the number of other stars in the same row,
- `col[j] - 1` gives the number of other stars in the same column.

Their product is exactly the number of right triangles using `(i, j)` as the right-angle vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · m · (n + m)) | O(1) | Too slow |
| Optimal | O(n · m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the grid and store it.
2. Create an array `row` where `row[i]` stores the number of `*` cells in row `i`.
3. Create an array `col` where `col[j]` stores the number of `*` cells in column `j`.
4. Traverse the grid once to fill these arrays.

Every time a `*` is found at `(i, j)`, increment:

- `row[i]`
- `col[j]`
5. Traverse the grid again.
6. For every `*` cell `(i, j)`, compute:

$$(row[i] - 1) \times (col[j] - 1)$$

The subtraction removes the current cell itself from both counts.

1. Add all contributions to the final answer.
2. Print the answer.

### Why it works

Every valid triangle has a unique right-angle vertex. Once that vertex is fixed, one vertex must lie in the same row and another must lie in the same column.

For a star at `(i, j)`:

- there are exactly `row[i] - 1` valid horizontal choices,
- there are exactly `col[j] - 1` valid vertical choices.

Every pair of such choices forms one unique right triangle, and every valid triangle is counted exactly once from its right-angle vertex. No duplicates occur because no triangle can have two right angles.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

grid = [input().strip() for _ in range(n)]

row = [0] * n
col = [0] * m

for i in range(n):
    for j in range(m):
        if grid[i][j] == '*':
            row[i] += 1
            col[j] += 1

ans = 0

for i in range(n):
    for j in range(m):
        if grid[i][j] == '*':
            ans += (row[i] - 1) * (col[j] - 1)

print(ans)
```

The first traversal computes how many stars appear in each row and column. This preprocessing is the entire optimization. Without it, we would repeatedly scan rows and columns for every cell.

The second traversal evaluates each `*` cell independently. The formula:

```
(row[i] - 1) * (col[j] - 1)
```

counts all possible combinations of:

- another star in the same row,
- another star in the same column.

Subtracting `1` is essential because the current cell belongs to both counts. Forgetting this creates invalid triangles where one endpoint equals the right-angle vertex itself.

The answer can grow large, but Python integers handle arbitrary size automatically. In languages with fixed-width integers, a 64-bit type is necessary.

## Worked Examples

### Example 1

Input:

```
2 2
**
*.
```

Row counts:

- row 0 → 2
- row 1 → 1

Column counts:

- col 0 → 2
- col 1 → 1

| Cell | Is `*` | row[i]-1 | col[j]-1 | Contribution |
| --- | --- | --- | --- | --- |
| (0,0) | Yes | 1 | 1 | 1 |
| (0,1) | Yes | 1 | 0 | 0 |
| (1,0) | Yes | 0 | 1 | 0 |

Total answer = `1`.

This trace shows the core idea clearly. Only the top-left cell has both a horizontal and vertical partner, so only one triangle exists.

### Example 2

Input:

```
3 3
***
***
***
```

Every row contains 3 stars and every column contains 3 stars.

| Cell | row[i]-1 | col[j]-1 | Contribution |
| --- | --- | --- | --- |
| Each of 9 cells | 2 | 2 | 4 |

Total answer:

$$9 \times 4 = 36$$

This example demonstrates that each cell independently acts as a right-angle vertex. Every vertex can pair with two horizontal choices and two vertical choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m) | Two full traversals of the grid |
| Space | O(n + m) | Row and column count arrays |

The grid contains at most one million cells. Two linear scans over that many cells fit comfortably within the time limit in Python. The auxiliary memory is tiny compared to the grid size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    grid = [input().strip() for _ in range(n)]

    row = [0] * n
    col = [0] * m

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                row[i] += 1
                col[j] += 1

    ans = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                ans += (row[i] - 1) * (col[j] - 1)

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue().strip()

# provided sample
assert run(
"""2 2
**
*.
"""
) == "1", "sample 1"

# minimum grid
assert run(
"""1 1
*
"""
) == "0", "single cell"

# full 2x2 grid
assert run(
"""2 2
**
**
"""
) == "4", "all corners form triangles"

# diagonal stars only
assert run(
"""3 3
*..
.*.
..*
"""
) == "0", "no shared row or column"

# full 3x3 grid
assert run(
"""3 3
***
***
***
"""
) == "36", "dense grid"

# one row only
assert run(
"""1 5
*****
"""
) == "0", "no vertical edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` single star | `0` | Smallest possible grid |
| Full `2x2` grid | `4` | Correct counting from each corner |
| Diagonal-only stars | `0` | No triangles despite multiple stars |
| Full `3x3` grid | `36` | Large number of overlapping triangles |
| Single-row grid | `0` | Requires both horizontal and vertical legs |

## Edge Cases

Consider the single-row case:

```
1 5
*****
```

Row count for the only row is `5`, but every column count is `1`.

For each star:

- `row[i] - 1 = 4`
- `col[j] - 1 = 0`

Every contribution becomes:

$$4 \times 0 = 0$$

The final answer is `0`, which is correct because a vertical leg cannot exist.

Now consider the fully filled `2x2` grid:

```
2 2
**
**
```

Every row count and column count equals `2`.

For each of the four cells:

- `row[i] - 1 = 1`
- `col[j] - 1 = 1`

Each contributes exactly one triangle.

Total:

$$4 \times 1 = 4$$

This confirms why subtracting `1` matters. Without subtraction, each cell would incorrectly count itself as a partner.

Finally, consider isolated stars on a diagonal:

```
3 3
*..
.*.
..*
```

Every row count and column count equals `1`.

For every star:

- `row[i] - 1 = 0`
- `col[j] - 1 = 0`

All contributions are zero, so the algorithm correctly reports that no valid right triangle exists.
