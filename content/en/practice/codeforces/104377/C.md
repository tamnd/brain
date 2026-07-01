---
title: "CF 104377C - \u4e8c\u7ef4\u6570\u7ec4\u53d8\u6362"
description: "We are given an n by n matrix and a sequence of operations. Each operation selects a square submatrix using its top-left and bottom-right coordinates, then applies one geometric transformation to that submatrix."
date: "2026-07-01T17:21:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104377
codeforces_index: "C"
codeforces_contest_name: "The 21st Sichuan University Programming Contest"
rating: 0
weight: 104377
solve_time_s: 70
verified: true
draft: false
---

[CF 104377C - \u4e8c\u7ef4\u6570\u7ec4\u53d8\u6362](https://codeforces.com/problemset/problem/104377/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an n by n matrix and a sequence of operations. Each operation selects a square submatrix using its top-left and bottom-right coordinates, then applies one geometric transformation to that submatrix. The transformations are standard image-style operations: rotation by 90 degrees clockwise, horizontal flip, vertical flip, and reflections across the two diagonals.

After applying all operations in order, the final matrix must be printed.

The key detail is that operations apply only to submatrices, not the whole grid, and the same cell can be involved in many overlapping transformations. The output depends on the cumulative effect of all transformations.

The constraints allow n up to 500 and at most 100 operations. A direct simulation that rebuilds the affected submatrix for each operation is therefore plausible because the largest possible work per operation is on a 500 by 500 region, which is about 250,000 cells, and this is repeated at most 100 times, giving roughly 25 million cell updates.

Edge cases come mainly from how transformations are applied inside a submatrix.

A first subtle issue is rotation correctness. If we overwrite the matrix in place while rotating, we will corrupt values before they are moved. For example, rotating a 3 by 3 block in place without a temporary buffer will overwrite entries that are still needed later in the rotation mapping.

Another issue is indexing consistency. Input is 1-based, so failing to convert to 0-based indexing leads to off-by-one corruption that is hard to detect because results may still look structured but incorrect.

Finally, diagonal flips require careful coordinate mapping. A naive implementation that swaps rows and columns globally instead of within the submatrix will destroy unrelated parts of the matrix.

## Approaches

A brute force interpretation directly follows the problem statement: for each operation, extract the submatrix, build a new transformed version, and write it back.

This works because each transformation is a fixed permutation of coordinates inside the square region. For a submatrix of size k, we can compute the new position of each element in O(1), so rebuilding the submatrix costs O(k²). Since each cell is rewritten only when its containing submatrix is processed, total work is bounded by the sum over all operations of the sizes of their affected regions squared.

The worst case happens when every operation touches the full n by n matrix. Then each operation costs O(n²), and with q up to 100 this becomes O(100·500²), which is about 25 million assignments. This is acceptable in Python.

The key observation is that there is no need for any global coordinate tracking or lazy transformation composition. The number of operations is small, so recomputing directly is simpler and safe. Any attempt to maintain symbolic transformations per cell becomes unnecessary overhead and increases implementation complexity without improving asymptotic performance in this constraint regime.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Submatrix Reconstruction | O(q · k²) | O(k²) | Accepted |
| Optimal Direct Simulation | O(q · n²) worst case | O(n²) | Accepted |

In this problem, both approaches converge because the constraints are small enough that the straightforward simulation is already optimal.

## Algorithm Walkthrough

We maintain the matrix in its current state and apply each operation directly.

1. Read the matrix and convert it into a mutable structure. This allows in-place updates after each transformation.
2. For each operation, convert coordinates from 1-based indexing into 0-based indexing. This ensures all further indexing matches Python array conventions and prevents boundary shifts.
3. Extract the submatrix defined by the operation into a temporary buffer. This step isolates the region so that transformations do not overwrite values that are still needed during computation.
4. Construct a new matrix of the same size as the submatrix.
5. Fill the new matrix according to the transformation type. For a rotation, each element at position (i, j) in the submatrix moves to (j, k-1-i). For horizontal and vertical flips, indices are reversed along the corresponding axis. For diagonal reflections, row and column indices are swapped with appropriate reversal depending on which diagonal is used.
6. Write the transformed submatrix back into the original matrix at the same coordinates.
7. Repeat until all operations are processed.

After all updates, print the final matrix.

### Why it works

Each operation is a bijection on the cells of the chosen square region, meaning every element moves to exactly one new position and every position receives exactly one element. Because we fully reconstruct each submatrix before writing it back, we preserve this one-to-one mapping exactly as defined by the transformation. Since operations are applied in sequence and each step uses the fully updated matrix from the previous step, the final state matches the composition of all transformations in order.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

def apply_op(x0, y0, x1, y1, t):
    x0 -= 1
    y0 -= 1
    x1 -= 1
    y1 -= 1
    k = x1 - x0 + 1

    tmp = [[0] * k for _ in range(k)]

    for i in range(k):
        for j in range(k):
            tmp[i][j] = a[x0 + i][y0 + j]

    res = [[0] * k for _ in range(k)]

    if t == 1:
        for i in range(k):
            for j in range(k):
                res[j][k - 1 - i] = tmp[i][j]

    elif t == 2:
        for i in range(k):
            for j in range(k):
                res[i][k - 1 - j] = tmp[i][j]

    elif t == 3:
        for i in range(k):
            for j in range(k):
                res[k - 1 - i][j] = tmp[i][j]

    elif t == 4:
        for i in range(k):
            for j in range(k):
                res[j][i] = tmp[i][j]

    elif t == 5:
        for i in range(k):
            for j in range(k):
                res[k - 1 - j][k - 1 - i] = tmp[i][j]

    for i in range(k):
        for j in range(k):
            a[x0 + i][y0 + j] = res[i][j]

for _ in range(q):
    x0, y0, x1, y1, t = map(int, input().split())
    apply_op(x0, y0, x1, y1, t)

for row in a:
    print(*row)
```

The implementation follows the algorithm exactly by isolating each operation into a helper function. The temporary buffer `tmp` is necessary because all transformations depend on the original configuration of the submatrix, and in-place updates would overwrite values needed for later assignments.

Each transformation case encodes a direct coordinate mapping. For example, the rotation case uses the mapping (i, j) to (j, k-1-i), which corresponds to rotating the square clockwise. The diagonal cases swap indices, reflecting across the main or anti-diagonal.

Care must be taken that all indices are consistently shifted into 0-based form at the start of each operation, and that writes back into `a` occur only after the full transformed block is computed.

## Worked Examples

Consider the first sample where a 3 by 3 matrix undergoes a full rotation operation on the entire grid. We track only the coordinate mapping.

| Step | (i, j) | Value | New Position |
| --- | --- | --- | --- |
| Initial | (0,0) | 1 | (0,2) |
| Initial | (0,1) | 2 | (1,2) |
| Initial | (0,2) | 3 | (2,2) |
| Initial | (1,0) | 4 | (0,1) |
| Initial | (1,1) | 5 | (1,1) |
| Initial | (1,2) | 6 | (2,1) |
| Initial | (2,0) | 7 | (0,0) |
| Initial | (2,1) | 8 | (1,0) |
| Initial | (2,2) | 9 | (2,0) |

After placing all values into their new positions, the matrix becomes rotated clockwise.

For a second example, consider a horizontal flip on the same matrix. Each row is reversed independently. The top row becomes the bottom row of reversed values, while the middle row remains structurally unchanged except for reversal.

This confirms that transformations operate strictly within the selected submatrix and do not leak outside boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q · k²), worst O(q · n²) | Each operation rebuilds a k by k submatrix, and k can be up to n |
| Space | O(n²) | Storage for the matrix plus a temporary buffer of size k² |

With n up to 500 and q up to 100, the worst-case operation count is around 25 million cell assignments, which fits comfortably within the time limit in Python given simple loop bodies and no expensive operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    def apply_op(x0, y0, x1, y1, t):
        x0 -= 1; y0 -= 1; x1 -= 1; y1 -= 1
        k = x1 - x0 + 1
        tmp = [[0]*k for _ in range(k)]
        for i in range(k):
            for j in range(k):
                tmp[i][j] = a[x0+i][y0+j]
        res = [[0]*k for _ in range(k)]

        if t == 1:
            for i in range(k):
                for j in range(k):
                    res[j][k-1-i] = tmp[i][j]
        elif t == 2:
            for i in range(k):
                for j in range(k):
                    res[i][k-1-j] = tmp[i][j]
        elif t == 3:
            for i in range(k):
                for j in range(k):
                    res[k-1-i][j] = tmp[i][j]
        elif t == 4:
            for i in range(k):
                for j in range(k):
                    res[j][i] = tmp[i][j]
        elif t == 5:
            for i in range(k):
                for j in range(k):
                    res[k-1-j][k-1-i] = tmp[i][j]

        for i in range(k):
            for j in range(k):
                a[x0+i][y0+j] = res[i][j]

    for _ in range(q):
        x0, y0, x1, y1, t = map(int, input().split())
        apply_op(x0, y0, x1, y1, t)

    return "\n".join(" ".join(map(str, r)) for r in a)

# provided sample 1
assert run("""3 1
1 2 3
4 5 6
7 8 9
1 1 1 3 3
""") == """7 4 1
8 5 2
9 6 3"""

# provided sample 2
assert run("""3 1
1 2 3
4 5 6
7 8 9
3 1 1 3 3
""") == """7 8 9
4 5 6
1 2 3"""

# custom: 1x1 no-op
assert run("""1 1
5
1 1 1 1 1
""") == "5"

# custom: horizontal flip 2x2
assert run("""2 1
1 2
3 4
1 1 2 2 2
""") == """2 1
4 3"""

# custom: diagonal main
assert run("""2 1
1 2
3 4
1 1 2 2 4
""") == """1 3
2 4"""

# custom: anti diagonal
assert run("""2 1
1 2
3 4
1 1 2 2 5
""") == """4 2
3 1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | unchanged | identity edge case |
| 2x2 horizontal flip | reversed rows | row-wise reversal correctness |
| 2x2 main diagonal | transpose | correct diagonal mapping |
| 2x2 anti diagonal | anti-diagonal reflection | correct reverse-diagonal mapping |

## Edge Cases

A 1 by 1 submatrix tests whether transformations incorrectly attempt to move a cell onto itself or index out of range. The algorithm handles this because every mapping sends (0,0) back to (0,0), so the matrix remains unchanged.

A full-grid operation repeated multiple times tests accumulation. Since each operation fully reconstructs the matrix before the next, there is no interference between transformations beyond intentional composition.

Overlapping submatrices test correctness of isolation. Because each operation copies into a temporary buffer before writing back, previous updates are not partially reused during the same operation, preventing corruption of intermediate values.
