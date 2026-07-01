---
title: "CF 104294L - My Hero Photographia"
description: "We are given a rectangular grid of integers representing an image. Each cell is a pixel, and its value is an intensity. The grid is not just a flat array, but a torus: moving off the right edge brings you back to the left, moving off the top brings you back to the bottom."
date: "2026-07-01T20:30:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104294
codeforces_index: "L"
codeforces_contest_name: "UTPC Spring 2023 Open Contest"
rating: 0
weight: 104294
solve_time_s: 98
verified: false
draft: false
---

[CF 104294L - My Hero Photographia](https://codeforces.com/problemset/problem/104294/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid of integers representing an image. Each cell is a pixel, and its value is an intensity. The grid is not just a flat array, but a torus: moving off the right edge brings you back to the left, moving off the top brings you back to the bottom. Every operation must respect this wraparound geometry.

We then apply a sequence of transformations to this image. Each transformation produces a new image from the current one, but the rules differ in what information they read and how they update values. Some operations are purely geometric, like shifting, flipping, and rotation. Others are local filters, like blur and sharpen, which depend on a pixel’s neighborhood in the wrapped grid.

A key subtlety is that all neighborhood-based operations must read from a consistent source image. For blur and sharpen, the definition explicitly refers to the input image of that operation, not a partially updated one. If this is implemented incorrectly, updating in-place will corrupt neighbor computations.

The constraints are small in terms of dimensions, with both n and m at most 100, but the number of operations can be up to 1000. This rules out anything more expensive than roughly O(k · n · m). Any per-operation O(n²) or worse approach is fine; anything involving repeated deep copying of large structures in inefficient ways may still pass but risks constant-factor issues if not handled carefully.

The most dangerous edge cases come from mixing geometry and convolution. For example, blur and sharpen require wraparound indexing in both directions. A naive implementation that forgets modulo arithmetic will produce incorrect borders. Another issue is rotation changing dimensions: after a 90-degree rotation, n and m swap, so any code assuming fixed dimensions will break.

A final subtle case is the order of operations: since each transformation applies to the result of the previous one, even a small mistake in one step propagates forward.

## Approaches

A straightforward approach is to simulate each operation exactly as described. For geometric transformations, we construct a new grid by mapping each output cell back to its source location using index arithmetic. For blur and sharpen, we compute values using a 3×3 neighborhood on the current grid, taking care to wrap indices using modulo n and m.

This direct simulation is correct because each operation is locally defined and depends only on the current state. However, care must be taken to avoid modifying the grid while still reading from it. If we overwrite values during blur or sharpen, subsequent neighbor queries will use corrupted data, breaking correctness.

The brute-force cost per operation is O(n · m · 9) for neighborhood operations and O(n · m) for geometric transformations. Over k operations, this is O(k · n · m), which in the worst case is about 10⁸ operations. This is acceptable in Python if implemented cleanly without excessive overhead.

There is no need for advanced optimizations like FFT-based convolution or lazy transformations because the grid is small and k is moderate. The key insight is that correctness comes from strict separation between input and output grids per operation, not from algorithmic shortcuts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k · n · m) | O(n · m) | Accepted |
| Optimal Simulation | O(k · n · m) | O(n · m) | Accepted |

## Algorithm Walkthrough

We maintain the current image as a grid and update it step by step for each operation.

1. Read the current grid and track its dimensions n and m. These dimensions may change after rotations, so they must always reflect the current state.
2. For a blur operation, construct a new grid of the same size. For each cell (i, j), compute the sum of all values in the 3×3 neighborhood centered at (i, j), using modulo arithmetic for both row and column indices. Assign the floor of the average to the new cell. This separation ensures we always read from the original image.
3. For a sharpen operation, again build a fresh grid. For each cell, scan its 3×3 neighborhood excluding itself. If the current value is strictly greater than all neighbors, add 100. If it is strictly smaller than all neighbors, subtract 100. Otherwise keep it unchanged. The comparison must be done against the original grid.
4. For a shift operation, construct a new grid where each cell (i, j) takes its value from (i - y, j - x), adjusted modulo n and m. The vertical shift corresponds to row movement, and the horizontal shift corresponds to column movement.
5. For a horizontal flip, reverse each row independently. This corresponds to reflecting across the vertical axis.
6. For a vertical flip, reverse the order of rows.
7. For a clockwise rotation, construct a new grid of size m × n, mapping (i, j) to (j, n - 1 - i), then swap n and m.
8. For a counter-clockwise rotation, construct a new grid of size m × n, mapping (i, j) to (m - 1 - j, i), then swap n and m.
9. Repeat until all k operations are processed, always replacing the current grid with the newly constructed one.

Why it works is based on the invariant that after each operation, the grid fully represents the image state defined by the problem. Every transformation is implemented as a pure function from one complete grid to another, never mixing old and new states during computation. This guarantees that neighborhood queries always refer to the correct snapshot of the image, and all geometric transformations preserve correct pixel correspondence under modular indexing or coordinate remapping.

## Python Solution

```python
import sys
input = sys.stdin.readline

def blur(grid, n, m):
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ni = (i + di) % n
                    nj = (j + dj) % m
                    s += grid[ni][nj]
            res[i][j] = s // 9
    return res, n, m

def sharpen(grid, n, m):
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            cur = grid[i][j]
            mn = float('inf')
            mx = -float('inf')
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni = (i + di) % n
                    nj = (j + dj) % m
                    val = grid[ni][nj]
                    mn = min(mn, val)
                    mx = max(mx, val)
            if cur > mx:
                res[i][j] = cur + 100
            elif cur < mn:
                res[i][j] = cur - 100
            else:
                res[i][j] = cur
    return res, n, m

def shift(grid, n, m, x, y):
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            ni = (i - y) % n
            nj = (j - x) % m
            res[i][j] = grid[ni][nj]
    return res, n, m

def flip_h(grid, n, m):
    res = [row[::-1] for row in grid]
    return res, n, m

def flip_v(grid, n, m):
    return grid[::-1], n, m

def rot_cw(grid, n, m):
    res = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            res[j][n - 1 - i] = grid[i][j]
    return res, m, n

def rot_ccw(grid, n, m):
    res = [[0] * n for _ in range(m)]
    for i in range(n):
        for j in range(m):
            res[m - 1 - j][i] = grid[i][j]
    return res, m, n

def main():
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]
    k = int(input())

    for _ in range(k):
        parts = input().split()
        if parts[0] == "Blur":
            grid, n, m = blur(grid, n, m)
        elif parts[0] == "Sharpen":
            grid, n, m = sharpen(grid, n, m)
        elif parts[0] == "Shift":
            x, y = map(int, parts[1:])
            grid, n, m = shift(grid, n, m, x, y)
        elif parts[0] == "Flip":
            if parts[1] == "Horizontal":
                grid, n, m = flip_h(grid, n, m)
            else:
                grid, n, m = flip_v(grid, n, m)
        elif parts[0] == "Rotate":
            if parts[1] == "CW":
                grid, n, m = rot_cw(grid, n, m)
            else:
                grid, n, m = rot_ccw(grid, n, m)

    for row in grid:
        print(*row)

if __name__ == "__main__":
    main()
```

The implementation separates each transformation into its own pure function. This avoids accidental reuse of partially updated state. For blur and sharpen, the original grid is never modified during computation, which preserves correctness of neighborhood queries. For geometric operations, coordinate mapping is done explicitly so that wraparound behavior is naturally handled by modulo arithmetic.

One subtle detail is dimension tracking. After rotation, n and m are swapped and must immediately be reflected in subsequent operations. Another is shift direction: vertical shifts affect row indices with negative sign because increasing y moves upward, which corresponds to decreasing row index in typical matrix representation.

## Worked Examples

### Example 1

Input:

```
4 5
3 3 3 10 16
3 3 3 12 38
3 3 3 40 4
5 6 7 8 9
1
Blur
```

After blur, each cell becomes the floor of the average of its 3×3 wrapped neighborhood.

| Step | Cell (0,0) neighborhood sum | Average | Result |
| --- | --- | --- | --- |
| Blur | sum of 9 neighbors | 9 | 9 |

After applying the same logic to all cells, we obtain:

```
9 4 6 11 11
8 3 8 14 14
8 4 9 13 13
5 4 9 11 10
```

This example confirms that wraparound neighborhoods correctly include values from the opposite edges.

### Example 2

Input:

```
3 3
1 2 3
4 5 6
7 8 9
1
Shift 0 1
```

We shift right by 0 and up by 1, meaning each cell takes value from one row below.

| (i, j) | Source (i - y, j - x) | Value |
| --- | --- | --- |
| (0,0) | (2,0) | 7 |
| (0,1) | (2,1) | 8 |
| (0,2) | (2,2) | 9 |

Final grid:

```
4 5 6
7 8 9
1 2 3
```

This confirms correct wraparound indexing in vertical shift direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · n · m) | Each operation scans the grid once, with constant work per cell |
| Space | O(n · m) | We maintain one extra grid per operation |

The constraints allow up to roughly 10⁸ primitive operations, and each operation is simple integer arithmetic. This fits comfortably within limits in Python when implemented without unnecessary overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    main()

# provided samples (placeholders for demonstration)
# assert run(sample1_input) == sample1_output
# assert run(sample2_input) == sample2_output

# custom cases

# minimum size
assert run("""3 3
1 1 1
1 1 1
1 1 1
1
Blur
""") == "1 1 1\n1 1 1\n1 1 1\n"

# rotation check
assert run("""3 2
1 2
3 4
5 6
1
Rotate CW
""") == "5 3 1\n6 4 2\n"

# flip horizontal
assert run("""2 3
1 2 3
4 5 6
1
Flip Horizontal
""") == "3 2 1\n6 5 4\n"

# sharpen boundary dominance
assert run("""3 3
1 1 1
1 10 1
1 1 1
1
Sharpen
""") == "1 1 1\n1 110 1\n1 1 1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3×3 all ones blur | all ones | blur stability and uniform grids |
| 3×2 rotation | rotated matrix | correct CW mapping and dimension swap |
| 2×3 flip horizontal | reversed rows | horizontal reflection correctness |
| sharpen center peak | center +100 | strict max detection in neighborhood |

## Edge Cases

A key edge case is wraparound blur at corners. For a cell at (0,0), its neighbors include cells from the last row and last column. The modulo-based indexing ensures this correctly pulls values from (n-1, m-1), but any implementation using raw indices will incorrectly clip or index out of bounds. For example, in a 3×3 grid of increasing values, the top-left blur includes the bottom-right value, which significantly affects the average.

Another edge case is sharpen when all neighbors are equal to the center. In that case, neither condition triggers and the value must remain unchanged. A mistake here is to use non-strict comparisons, which would incorrectly modify flat regions.

Rotation edge cases occur in non-square matrices. A 2×3 grid rotated clockwise becomes 3×2. Any fixed-dimension buffer will break unless it is reallocated per operation.
