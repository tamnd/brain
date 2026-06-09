---
title: "CF 1926B - Vlad and Shapes"
description: "We are given a very small binary image, typically at most 10 by 10 cells. Every cell is either empty or filled. The grid contains exactly one connected geometric figure formed by ones, and that figure is guaranteed to be either a perfect square or a centered triangle (upright or…"
date: "2026-06-08T18:58:43+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1926
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 928 (Div. 4)"
rating: 800
weight: 1926
solve_time_s: 82
verified: true
draft: false
---

[CF 1926B - Vlad and Shapes](https://codeforces.com/problemset/problem/1926/B)

**Rating:** 800  
**Tags:** geometry, implementation  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small binary image, typically at most 10 by 10 cells. Every cell is either empty or filled. The grid contains exactly one connected geometric figure formed by ones, and that figure is guaranteed to be either a perfect square or a centered triangle (upright or upside down).

A square here means a solid k by k block of ones aligned with the grid, with no gaps inside. A triangle means a stack of rows where the number of ones increases or decreases symmetrically by two per row, forming a centered pyramid shape.

The task is to determine which of the two shapes is present.

The constraint n ≤ 10 removes any need for optimization. Even a brute scan of all rows, columns, and shape hypotheses is fast enough. A solution can freely inspect every cell multiple times.

The main edge case comes from relying on local patterns instead of global structure. For example, the top row of a triangle and a square can look similar if it contains consecutive ones, but the triangle’s defining feature is the changing row length, while the square keeps constant row length across all rows of the shape. Another subtle case is upside-down triangles, where the widest row is at the top rather than the bottom.

A careless approach often fails when it only checks the first row or counts total ones without verifying structure. A triangle and square can sometimes have similar totals, for instance both can have 9 ones, but only one matches the required row pattern.

## Approaches

A brute-force way to solve the problem is to try identifying the bounding box of all ones and then check whether it forms a perfect square or whether it forms a triangle with some center column.

For the square check, we verify that all cells inside the bounding box are ones. For the triangle check, we try each possible apex row and center column, and validate whether row lengths match 1, 3, 5, and so on, or the reverse pattern for inverted triangles. This works because the grid is tiny, so even checking every possible center and height is inexpensive.

The inefficiency of brute force only appears if the grid were large, because we would try many possible centers. Here, since n ≤ 10, even O(n³) or O(n⁴) behavior is trivial.

The key simplification is that we do not actually need to “guess” structure. We can directly detect whether all ones form a filled rectangle. If yes, it must be a square. If not, the only remaining valid structure is a triangle, and its structure forces a single center alignment, which can be validated by checking row symmetry around a midpoint.

This reduces the problem to simple pattern verification rather than shape reconstruction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force shape fitting | O(n⁴) | O(1) | Accepted |
| Direct pattern check | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

We rely on a simple observation: squares are the only shapes where every row inside the shape has the same number of consecutive ones, while triangles always have varying row lengths.

1. Scan the grid and locate all positions containing ones. We record the minimum and maximum row and column indices containing a one. This gives us the bounding rectangle of the shape.
2. Count how many ones exist inside this bounding rectangle. If the number of ones equals the area of the rectangle, then every cell inside is filled, meaning the shape is a solid rectangle.
3. If we have a solid rectangle, we check whether its height equals its width. If so, the shape is a square, since the problem guarantees only square or triangle shapes exist.
4. If the bounding rectangle is not fully filled, then the structure must be a triangle. In that case, we verify it implicitly by recognizing that the filled region cannot be rectangular unless it is a square, so the only valid remaining configuration is a triangle.
5. Output the result accordingly.

The implementation avoids explicit triangle reconstruction because the problem guarantees validity of input shapes.

### Why it works

A square is uniquely characterized by having constant row length across all rows of the bounding box and full occupancy of all cells. Any deviation from full occupancy immediately breaks the rectangle property, and the only remaining valid structure in the problem’s constraints is a triangle. Since the input is guaranteed to contain exactly one valid shape, classification by rectangle completeness is sufficient and cannot misclassify a valid input.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    g = [input().strip() for _ in range(n)]
    
    cells = [(i, j) for i in range(n) for j in range(n) if g[i][j] == '1']
    
    min_r = min(i for i, j in cells)
    max_r = max(i for i, j in cells)
    min_c = min(j for i, j in cells)
    max_c = max(j for i, j in cells)
    
    total_ones = len(cells)
    area = (max_r - min_r + 1) * (max_c - min_c + 1)
    
    if total_ones == area and (max_r - min_r) == (max_c - min_c):
        print("SQUARE")
    else:
        print("TRIANGLE")
```

The solution works by extracting the tight bounding box around all ones and checking whether it is perfectly filled. If it is, the shape must be a square because only squares occupy full rectangles. Otherwise, the only remaining valid configuration under the problem constraints is a triangle.

A subtle point is that we never attempt to reconstruct triangle geometry explicitly. That avoids errors from misinterpreting upside-down triangles or off-center cases, since the guarantees ensure no ambiguous mixtures exist.

## Worked Examples

Consider a 3 by 3 square:

```
111
111
111
```

| Step | min_r | max_r | min_c | max_c | ones | area | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| scan | 0 | 2 | 0 | 2 | 9 | 9 | square check |
| check | 0 | 2 | 0 | 2 | 9 | 9 | SQUARE |

The bounding box is completely filled and square-shaped, so the result is SQUARE.

Now consider a triangle:

```
00111
00010
00000
00000
00000
```

| Step | min_r | max_r | min_c | max_c | ones | area | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| scan | 0 | 1 | 2 | 4 | 5 | 6 | triangle check |
| check | 0 | 1 | 2 | 4 | 5 | 6 | TRIANGLE |

The bounding box is not fully filled, so it cannot be a square, and must be a triangle.

These traces show that the algorithm relies entirely on structural completeness rather than geometric reconstruction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | We scan every cell once to collect ones and compute bounds |
| Space | O(1) | Only bounding coordinates and counters are stored |

The grid size is at most 100 cells per test case, so this solution is trivially fast under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

def solve():
    import sys
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        g = [input().strip() for _ in range(n)]
        cells = [(i, j) for i in range(n) for j in range(n) if g[i][j] == '1']
        min_r = min(i for i, j in cells)
        max_r = max(i for i, j in cells)
        min_c = min(j for i, j in cells)
        max_c = max(j for i, j in cells)
        ones = len(cells)
        area = (max_r - min_r + 1) * (max_c - min_c + 1)
        if ones == area and (max_r - min_r) == (max_c - min_c):
            res.append("SQUARE")
        else:
            res.append("TRIANGLE")
    print("\n".join(res))

# provided samples
assert run("""6
3
000
011
011
4
0000
0000
0100
1110
2
11
11
5
00111
00010
00000
00000
00000
10
0000000000
0000000000
0000000000
0000000000
0000000000
1111111110
0111111100
0011111000
0001110000
0000100000
3
111
111
111
""") == """SQUARE
TRIANGLE
SQUARE
TRIANGLE
TRIANGLE
SQUARE"""

# small custom case
assert run("""1
3
111
101
111
""") == "TRIANGLE"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| full square | SQUARE | detects perfect rectangle |
| broken rectangle | TRIANGLE | rejects non-solid region |

## Edge Cases

A key edge case is a triangle whose bounding box is still rectangular. For example, a wide triangle can have a bounding rectangle that looks almost filled, but with missing interior cells. In such a case, the area check fails because ones are fewer than total cells in the box, correctly classifying it as TRIANGLE.

Another edge case is the minimal valid shape size of 2. A 2 by 2 square passes both fullness and square checks, while any 2-row triangle necessarily leaves gaps or uneven row lengths, causing it to fail the rectangle condition.
