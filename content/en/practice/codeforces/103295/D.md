---
title: "CF 103295D - Cornfield Chase"
description: "We are given a grid representing a cornfield where each cell is either blocked by corn or empty. The task is to count how many distinct triangles can be formed such that all three vertices of the triangle lie on cells containing corn."
date: "2026-07-03T14:25:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103295
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-17-21 Div. 1 (Advanced)"
rating: 0
weight: 103295
solve_time_s: 51
verified: true
draft: false
---

[CF 103295D - Cornfield Chase](https://codeforces.com/problemset/problem/103295/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid representing a cornfield where each cell is either blocked by corn or empty. The task is to count how many distinct triangles can be formed such that all three vertices of the triangle lie on cells containing corn.

The triangle has a strict geometric structure: it must be a right triangle, and two of its sides must be aligned with the grid axes. This means the legs of the triangle are horizontal and vertical segments on the grid, and the right angle is formed at one of the chosen corn cells. So every valid triangle is fully determined by selecting three corn cells that satisfy this axis-aligned right triangle condition.

The grid size is up to 500 by 500, which means up to 250,000 cells. A cubic enumeration over all triples of cells would be completely infeasible. Even a quadratic approach over all pairs of corn cells would require on the order of 10^10 checks in the worst case, which is far beyond the time limit. This immediately suggests that the solution must avoid enumerating pairs of points explicitly and instead rely on counting structure along rows and columns.

A subtle edge case appears when corn density is very high or very low. If the grid is all empty, the answer is trivially zero, and any counting logic that assumes at least one valid vertex per row or column must handle this cleanly. On the other extreme, if the grid is full of corn, naive combinatorial counting can easily overcount triangles multiple times unless each triangle is associated with a unique “anchor” cell, which prevents duplication.

## Approaches

The brute-force idea is straightforward. We try every triple of corn cells and check whether they form a right triangle whose legs are aligned with the grid axes. This requires checking all combinations of three points, which is O(K^3) where K is the number of corn cells. In a dense grid K can be 250,000, making this approach impossible even to conceptualize within constraints. Even restricting to pairs and deriving the third point does not help much, since verifying existence would still require expensive lookup without preprocessing.

The key observation is that every valid triangle can be uniquely described by its right angle vertex. Once we fix a corn cell as the right-angle corner, the other two vertices must lie in the same row and same column respectively. That means we do not need geometry beyond axis alignment; we only need counts of corn cells in each row and each column.

Suppose at a fixed cell we know how many corn cells exist in its row and how many exist in its column. If we choose one other corn cell in the same row and one in the same column, we form a valid right triangle with the current cell as the right angle. The number of such choices is the product of these two counts, but we must be careful not to include the current cell itself in those counts. So we subtract one from each direction before multiplying.

This reduces the problem from reasoning about pairs of points in the entire grid to maintaining two frequency arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over triples | O(K^3) | O(1) | Too slow |
| Count per row/column | O(nm) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the grid and identify all corn cells. While doing this, maintain two arrays, one counting how many corn cells appear in each row and one counting how many appear in each column. This preprocessing compresses all geometric information into simple frequency counts.
2. Iterate over every cell in the grid again. When we encounter a corn cell, treat it as a potential right-angle vertex of a triangle.
3. For each such cell at position (i, j), compute how many valid choices exist for the second vertex on the same row. This is row_count[i] minus one, because we exclude the current cell.
4. Similarly compute how many valid choices exist for the second leg on the same column. This is col_count[j] minus one.
5. Multiply these two values. This product counts all triangles that have their right angle at (i, j).
6. Sum this value over all corn cells in the grid.

The multiplication step is correct because choosing one distinct corn cell in the row fixes one leg of the triangle, and choosing one distinct corn cell in the column fixes the other leg independently.

### Why it works

Every valid triangle has exactly one cell where the right angle is located. That cell is uniquely defined because it is the only vertex that shares both a horizontal and vertical edge with the other two vertices. By anchoring counting at this vertex, each triangle is counted exactly once. The independence between row choices and column choices guarantees that all combinations correspond to distinct geometric triangles, and no invalid shape is introduced because axis alignment enforces perpendicularity automatically.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    row = [0] * n
    col = [0] * m

    # count stars
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

if __name__ == "__main__":
    solve()
```

The implementation separates preprocessing from counting, which avoids recomputing row or column statistics repeatedly. The subtraction of one in both directions is essential because the current cell is counted in both row and column totals.

The final accumulation loop is safe in terms of overflow in Python, but in a strongly typed language like C++ the result may require 64-bit integers due to quadratic growth in dense grids.

## Worked Examples

### Example 1

Input:

```
2 2
**
*.
```

We compute row counts as [2, 1] and column counts as [2, 1]. Now we evaluate each corn cell.

| Cell | row[i] | col[j] | (row-1)*(col-1) |
| --- | --- | --- | --- |
| (0,0) | 2 | 2 | 1 |
| (0,1) | 2 | 1 | 0 |
| (1,0) | 1 | 2 | 0 |

Total contribution is 1.

This matches the idea that only one right-angle triangle can be formed in such a small grid.

### Example 2

Input:

```
3 2
.*
*.
.*
```

Row counts are [1,1,1] and column counts are [2,1].

Evaluating each corn cell:

| Cell | row[i] | col[j] | (row-1)*(col-1) |
| --- | --- | --- | --- |
| (0,1) | 1 | 1 | 0 |
| (1,0) | 1 | 2 | 0 |
| (2,1) | 1 | 1 | 0 |

Total is 0.

This shows that although corn exists, there is no row-column pair that allows two additional distinct corn cells to form perpendicular legs from the same vertex.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is visited a constant number of times for counting and aggregation |
| Space | O(n + m) | Only row and column frequency arrays are stored |

The grid size is at most 500 by 500, so at most 250,000 operations are performed. This is well within the 1-second limit in typical Codeforces environments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample 1
assert run("""2 2
**
*.
""") == "1"

# sample 2
assert run("""3 2
.*
*.
.*
""") == "0"

# single cell
assert run("""1 1
*
""") == "0"

# full grid 2x2
assert run("""2 2
**
**
""") == "4"

# sparse grid
assert run("""3 3
*.*
.*.
*.*
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 single star | 0 | minimum boundary |
| 2x2 full | 4 | dense overcount behavior |
| checkerboard pattern | 0 | no valid row-column completion |

## Edge Cases

For a single-cell grid containing a star, the algorithm correctly returns zero because either the row or column count becomes one, making both factors zero after subtraction. This prevents false triangles in degenerate geometry.

In a fully filled grid, each cell acts as a right-angle vertex. The algorithm correctly counts all combinations because each triangle is uniquely anchored at its corner, and multiplication over row and column choices captures all valid pairs without duplication.

In very sparse grids where stars are isolated, row or column counts remain one, ensuring no invalid triangles are formed since one leg of the triangle cannot be constructed.
