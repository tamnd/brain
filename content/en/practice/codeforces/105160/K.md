---
title: "CF 105160K - \u73af\u5f62\u6570\u7ec4(easy)"
description: "The task describes a deterministic way to assign numbers to an n by m grid. Imagine starting with an empty matrix and writing integers beginning from 1, increasing one by one, while always walking along the outer boundary of the remaining unfilled region in a clockwise spiral."
date: "2026-06-27T11:02:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "K"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 52
verified: true
draft: false
---

[CF 105160K - \u73af\u5f62\u6570\u7ec4(easy)](https://codeforces.com/problemset/problem/105160/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a deterministic way to assign numbers to an n by m grid. Imagine starting with an empty matrix and writing integers beginning from 1, increasing one by one, while always walking along the outer boundary of the remaining unfilled region in a clockwise spiral. Once the outer layer is filled, the process continues inward with the next inner boundary, repeating until every cell has been assigned a value.

The input gives only the dimensions of the grid. The output is the fully constructed matrix after this spiral filling process is completed.

The constraints allow n and m up to 1000, so the matrix can contain up to one million cells. Any solution that touches each cell a constant number of times is acceptable. A solution that tries to simulate movement inefficiently per step with repeated scanning or recursion overhead would still pass in Python only if it is strictly linear in the number of cells. Anything worse than O(nm) risks timing out because one million operations is already near the upper limit for a 1 second Python solution.

A common mistake appears when handling single row or single column cases. For example, if n equals 1 and m equals 5, the expected output is simply a straight sequence from left to right. A naive spiral implementation that always attempts to traverse all four directions without checking boundaries will either overwrite values or index out of range.

Another subtle issue arises when shrinking boundaries meet. Consider a 3 by 3 grid. After completing the outer layer, the remaining center cell must be filled exactly once. Incorrect termination conditions often lead to skipping this last cell or writing it twice.

## Approaches

The brute-force idea is to simulate the spiral movement step by step, keeping track of visited cells and repeatedly attempting to move right, down, left, or up depending on direction. Each move would check whether the next cell is inside bounds and not visited. If not, the direction changes.

This approach is correct because it directly follows the definition of the process. However, each step involves multiple checks and potentially repeated attempts to find a valid direction. While each of the n times m steps still performs constant work, Python overhead from direction checks and visited lookups makes it borderline but still acceptable. The real inefficiency comes from managing visited structures and repeated condition checks in a tight loop.

A cleaner way avoids "walking" entirely. Instead of moving step by step, we maintain four boundaries that describe the current remaining rectangle: top row, bottom row, left column, and right column. At each stage, we fill one full edge of the remaining rectangle in a single sweep, then shrink that boundary inward. This works because the spiral structure guarantees that each layer is a complete rectangle border, and once it is filled, it never needs to be revisited.

This transforms the process from cell-by-cell simulation of movement into structured layer-by-layer filling, eliminating unnecessary directional logic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step simulation with visited checks | O(nm) | O(nm) | Accepted but heavier constants |
| Boundary layer traversal | O(nm) | O(1) extra (excluding output) | Accepted |

## Algorithm Walkthrough

We maintain four pointers describing the current unfilled rectangle: top, bottom, left, and right. We also maintain a counter for the next number to place.

1. Initialize the matrix with empty values and set the counter to 1. The boundaries start as top = 0, bottom = n - 1, left = 0, right = m - 1.
2. While the top boundary is still below or equal to bottom and the left boundary is still below or equal to right, we fill one full layer of the spiral.
3. Move from left to right along the current top row, assigning consecutive values. After finishing, increment top because that row is fully used.
4. Move from top to bottom along the current right column, assigning values. After finishing, decrement right because that column is fully used.
5. If the top is still below or equal to bottom, move from right to left along the bottom row. This condition is necessary because the matrix may collapse into a single remaining row. After filling, decrement bottom.
6. If the left is still below or equal to right, move from bottom to top along the left column. This condition handles the case where only one column remains. After filling, increment left.
7. Continue until all boundaries cross, meaning every cell has been filled.

### Why it works

Each iteration fully exhausts the outer boundary of the remaining submatrix without skipping or overlapping cells. After each directional sweep, the corresponding boundary is permanently removed from consideration, so no cell is ever revisited. The invariant is that all cells outside the current rectangle are already filled in correct spiral order, and the current rectangle always represents exactly the remaining unassigned region.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    mat = [[0] * m for _ in range(n)]
    
    top, bottom = 0, n - 1
    left, right = 0, m - 1
    val = 1
    target = n * m
    
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            mat[top][j] = val
            val += 1
        top += 1
        
        for i in range(top, bottom + 1):
            mat[i][right] = val
            val += 1
        right -= 1
        
        if top <= bottom:
            for j in range(right, left - 1, -1):
                mat[bottom][j] = val
                val += 1
            bottom -= 1
        
        if left <= right:
            for i in range(bottom, top - 1, -1):
                mat[i][left] = val
                val += 1
            left += 1
    
    out = []
    for i in range(n):
        out.append(" ".join(map(str, mat[i])))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the boundary shrinking strategy directly. The matrix is preallocated so assignment is O(1). The variable val increments exactly once per cell, ensuring a strict linear progression from 1 to n times m.

The conditional checks before filling the bottom row and left column prevent overwriting in degenerate cases such as a single remaining row or column, which is the most common source of incorrect implementations.

## Worked Examples

### Example 1

Input is a 4 by 5 grid.

| Step | Top | Bottom | Left | Right | Action | Key fills |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 0 | 4 | top row left to right | 1 to 5 |
| 2 | 1 | 3 | 0 | 4 | right column top to bottom | 6 to 8 |
| 3 | 1 | 2 | 0 | 3 | bottom row right to left | 9 to 12 |
| 4 | 2 | 2 | 0 | 3 | left column bottom to top | 13 |
| 5 | 2 | 2 | 1 | 3 | top row of inner layer | 14 to 17 |
| 6 | 3 | 2 | 1 | 3 | right column (none valid after shrink stops early) | handled by condition |
| 7 | final | final | final | final | last inner row | completes 18 to 20 |

This trace confirms that each layer is fully consumed before moving inward and that the center region is reached exactly once.

### Example 2

Input 1 by 4 grid.

| Step | Top | Bottom | Left | Right | Action | Key fills |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 3 | single row left to right | 1 to 4 |

This case exercises the single-row condition. After the first pass, top becomes greater than bottom, preventing any vertical traversal. The algorithm correctly stops without attempting invalid movements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every cell is assigned exactly once during a single spiral traversal |
| Space | O(nm) | The matrix stores all output values |

The constraints allow up to one million cells, and each cell is written exactly once. This keeps runtime comfortably within the limits for Python under a 1 second constraint when implemented with simple loops and buffered output.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("4 5\n") == "\n".join([
"1 2 3 4 5",
"14 15 16 17 6",
"13 20 19 18 7",
"12 11 10 9 8"
]), "sample 1"

# minimum case
assert run("1 1\n") == "1"

# single row
assert run("1 5\n") == "1 2 3 4 5"

# single column
assert run("4 1\n") == "1\n2\n3\n4"

# square small
assert run("3 3\n") == "\n".join([
"1 2 3",
"8 9 4",
"7 6 5"
])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal matrix correctness |
| 1 5 | 1 2 3 4 5 | single-row boundary behavior |
| 4 1 | vertical sequence | single-column boundary behavior |
| 3 3 | spiral square | inner-layer correctness |

## Edge Cases

A 1 by m matrix is handled entirely by the first horizontal sweep. Since top becomes greater than bottom immediately after that sweep, no vertical or reverse traversal occurs, preventing invalid index access.

A m by 1 matrix behaves symmetrically. The first vertical sweep fills the entire column, and boundary updates prevent any horizontal passes.

A small odd-dimensional square such as 3 by 3 ensures that after completing the outer cycle, the center cell remains inside the valid boundary range for exactly one iteration. The algorithm’s boundary checks allow it to be filled as part of a final single-cell layer without duplication or omission.
